#!/usr/bin/env python3
"""Validate the Evidence Toolkit audit ledger (2026-10).

The ledger is a JSON list with one entry per card that has an effect size.
Allowed values come from the audit plan's criteria table. A "holds" verdict
needs all four: the source exists, the number is confirmed, the source fits
the card's practice, and the source is not retracted or contested (plus a
real DOI). "holds_reword" and "downgrade" keep the number on the site, so
they too need a confirmed number from a source that is not retracted.

Usage:
    /usr/bin/python3 scripts/audit_ledger.py LEDGER_PATH [--partial]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "evidence" / "data"

ENUMS = {
    "exists": {"yes", "mismatch", "not_found"},
    "number": {"exact", "rounded", "converted_ok", "different", "unconfirmed"},
    "outcome": {"achievement", "other_student", "teacher", "mixed"},
    "population": {"k12", "higher_ed", "mixed", "adult", "unclear"},
    "fit": {"exact", "near", "proxy"},
    "status": {"clean", "retracted", "concern", "corrected", "contested"},
}
QUALITY_FLAGS = {"few_studies", "high_heterogeneity", "publication_bias", "researcher_made_tests", "low_tier_venue", "contested"}
ACCESS = {"full", "abstract"}
VERDICTS = {"holds", "holds_reword", "downgrade", "replace_source", "remove_number"}
CHECKED_BY = re.compile(r"^(batch-[1-8]|adversarial|johan|external)$")
CONFIRMED_NUMBERS = {"exact", "rounded", "converted_ok"}
KEEPS_NUMBER = {"holds", "holds_reword", "downgrade"}
TEXT_FIELDS = ("doi", "number_location", "fit_reason", "newer_source")


def _blank(value) -> bool:
    return not isinstance(value, str) or not value.strip()


def validate_entry(entry: dict) -> list[str]:
    card = entry.get("card_id", "?")
    errors = []
    criteria = entry.get("criteria")
    if not isinstance(criteria, dict):
        errors.append(f"{card}: criteria must be an object, got {criteria!r}")
        criteria = {}
    for field, allowed in ENUMS.items():
        if criteria.get(field) not in allowed:
            errors.append(f"{card}: criteria.{field} = {criteria.get(field)!r} not in {sorted(allowed)}")
    for field in TEXT_FIELDS:
        if _blank(criteria.get(field)):
            errors.append(f"{card}: criteria.{field} is empty")
    flags = criteria.get("quality_flags")
    if not isinstance(flags, list) or any(not isinstance(f, str) or f not in QUALITY_FLAGS for f in flags):
        errors.append(f"{card}: criteria.quality_flags {flags!r} has unknown values")
    if entry.get("access") not in ACCESS:
        errors.append(f"{card}: access = {entry.get('access')!r} not in {sorted(ACCESS)}")
    if entry.get("verdict") not in VERDICTS:
        errors.append(f"{card}: verdict = {entry.get('verdict')!r} not in {sorted(VERDICTS)}")
    if _blank(entry.get("verdict_reason")):
        errors.append(f"{card}: verdict_reason is empty")
    if not CHECKED_BY.fullmatch(str(entry.get("checked_by", ""))):
        errors.append(f"{card}: checked_by = {entry.get('checked_by')!r} not recognised")

    if (entry.get("access") == "abstract" and criteria.get("number") in CONFIRMED_NUMBERS
            and criteria.get("number_location") != "abstract"):
        errors.append(f"{card}: number confirmed in {criteria.get('number_location')!r} but only the abstract was read")

    if entry.get("verdict") in KEEPS_NUMBER:
        if not (criteria.get("exists") == "yes" and criteria.get("number") in CONFIRMED_NUMBERS
                and criteria.get("status") not in {"retracted", "concern"}):
            errors.append(f"{card}: '{entry.get('verdict')}' keeps the number, so it needs exists=yes, "
                          "a confirmed number and a source that is not retracted or flagged")
    if entry.get("verdict") == "holds":
        if not (criteria.get("fit") in {"exact", "near"} and criteria.get("status") == "clean"
                and str(criteria.get("doi", "")).startswith("10.")):
            errors.append(f"{card}: 'holds' also needs fit exact/near, status clean and a real DOI")
        if criteria.get("newer_source") != "none" or "contested" in (flags if isinstance(flags, list) else []):
            errors.append(f"{card}: 'holds' cannot stand with a newer source or a 'contested' flag; "
                          "use replace_source or holds_reword")
    return errors


def _cards_with_d(data_dir: Path) -> dict[str, str]:
    cards = {}
    for data_file in sorted(data_dir.glob("*.json")):
        for card in json.loads(data_file.read_text())["skills"]:
            if card.get("effect_d") is not None:
                cards[card["id"]] = f"{card['effect_d_source']}|{card['effect_d_year']}"
    return cards


def validate_ledger(path: Path, data_dir: Path, require_complete: bool = True) -> list[str]:
    entries = json.loads(Path(path).read_text())
    if not isinstance(entries, list):
        return ["ledger must be a JSON list of entries"]
    expected = _cards_with_d(data_dir)
    errors, seen = [], set()
    for position, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entry {position}: not an object ({entry!r})")
            continue
        card = entry.get("card_id")
        errors.extend(validate_entry(entry))
        if card in seen:
            errors.append(f"{card}: listed twice")
        seen.add(card)
        if card not in expected:
            errors.append(f"{card}: no card with an effect size has this id")
        elif entry.get("source_key") != expected[card]:
            errors.append(f"{card}: source_key {entry.get('source_key')!r} does not match the card ({expected[card]!r})")
    if require_complete:
        for card in sorted(set(expected) - seen):
            errors.append(f"{card}: missing from the ledger")
    return errors


if __name__ == "__main__":
    problems = validate_ledger(Path(sys.argv[1]), DATA_DIR, require_complete="--partial" not in sys.argv)
    print("\n".join(problems) or "ledger OK")
    sys.exit(1 if problems else 0)
