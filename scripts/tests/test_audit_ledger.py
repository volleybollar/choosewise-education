"""Tests for scripts/audit_ledger.py (Evidence Toolkit audit, 2026-10)."""
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audit_ledger import validate_entry, validate_ledger  # noqa: E402

DATA_DIR = Path(__file__).resolve().parents[2] / "evidence" / "data"

GOOD = {
    "card_id": "memory-learning-science/spaced-practice-scheduler",
    "source_key": "Latimier, Peyre & Ramus|2021",
    "access": "full",
    "criteria": {
        "exists": "yes",
        "doi": "10.0000/test-fixture",
        "number": "exact",
        "number_location": "abstract",
        "outcome": "achievement",
        "population": "mixed",
        "fit": "exact",
        "fit_reason": "Meta-analysis of spaced versus massed retrieval practice.",
        "quality_flags": [],
        "status": "clean",
        "newer_source": "none",
    },
    "verdict": "holds",
    "verdict_reason": "Number, source and fit confirmed.",
    "checked_by": "batch-1",
}


def _with(**changes):
    entry = copy.deepcopy(GOOD)
    for key, value in changes.items():
        if key in entry["criteria"]:
            entry["criteria"][key] = value
        else:
            entry[key] = value
    return entry


def test_good_entry_is_valid():
    assert validate_entry(GOOD) == []


def test_holds_requires_all_four_conditions():
    assert validate_entry(_with(fit="proxy"))
    assert validate_entry(_with(status="contested"))
    assert validate_entry(_with(number="unconfirmed"))
    assert validate_entry(_with(exists="mismatch"))
    assert validate_entry(_with(fit="proxy", verdict="downgrade")) == []


def test_abstract_access_cannot_confirm_table_number():
    assert validate_entry(_with(access="abstract", number_location="Table 3"))
    assert validate_entry(_with(access="abstract", number_location="abstract")) == []
    unconfirmed = _with(access="abstract", number="unconfirmed", number_location="Table 3", verdict="remove_number")
    assert validate_entry(unconfirmed) == []


def test_same_source_different_fit_is_allowed(tmp_path):
    source = "Barbieri, Miller-Cotto, Clerjuste & Chawla|2023"
    exact = _with(card_id="memory-learning-science/worked-example-fading-designer", source_key=source)
    proxy = _with(card_id="explicit-instruction/practice-problem-sequence-designer", source_key=source,
                  fit="proxy", verdict="downgrade")
    ledger = tmp_path / "ledger.json"
    ledger.write_text(json.dumps([exact, proxy]))
    assert validate_ledger(ledger, DATA_DIR, require_complete=False) == []


def test_unknown_enum_value_rejected():
    assert validate_entry(_with(population="primary"))
    assert validate_entry(_with(quality_flags=["vibes"]))
    assert validate_entry(_with(verdict="fine"))


def test_ledger_must_cover_every_card_with_d(tmp_path):
    ledger = tmp_path / "ledger.json"
    ledger.write_text(json.dumps([GOOD]))
    assert any("missing" in e for e in validate_ledger(ledger, DATA_DIR))
    assert validate_ledger(ledger, DATA_DIR, require_complete=False) == []


def test_verdicts_that_keep_the_number_need_it_confirmed():
    assert validate_entry(_with(verdict="holds_reword", number="different"))
    assert validate_entry(_with(verdict="downgrade", fit="proxy", status="retracted"))
    assert validate_entry(_with(verdict="downgrade", fit="proxy", exists="not_found"))
    assert validate_entry(_with(verdict="holds_reword", status="concern"))
    assert validate_entry(_with(verdict="downgrade", fit="proxy", status="corrected")) == []
    assert validate_entry(_with(verdict="remove_number", number="different")) == []


def test_holds_requires_a_real_doi():
    assert validate_entry(_with(doi="unconfirmed"))
    assert validate_entry(_with(doi="unconfirmed", verdict="downgrade", fit="proxy")) == []


def test_verdict_reason_required():
    assert validate_entry(_with(verdict_reason=""))
    assert validate_entry(_with(fit_reason=" "))
