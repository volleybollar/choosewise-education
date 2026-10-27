#!/usr/bin/env python3
"""Build the source worklist for the Evidence Toolkit audit (2026-10).

One entry per unique source: effect-size sources (kind "d") are split into
review batches 1-8, EEF months sources (kind "months") all get batch 0.
Batch 1 is the pilot: every source used by a card in memory.json or
explicit-instruction.json.

Usage:
    /usr/bin/python3 scripts/audit_evidence_worklist.py OUT_PATH
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "evidence" / "data"
PILOT_FILES = {"memory.json", "explicit-instruction.json"}
D_BATCHES = 8


def assign_batches(n: int) -> list[int]:
    """Spread n sources in order over batches 2-8 as evenly as possible, none left empty (n >= 7)."""
    batches = D_BATCHES - 1
    return [2 + i * batches // n for i in range(n)]


def build_worklist(data_dir: Path) -> list[dict]:
    entries: dict[tuple[str, str], dict] = {}
    first_file: dict[tuple[str, str], str] = {}
    pilot_keys: set[tuple[str, str]] = set()

    for data_file in sorted(data_dir.glob("*.json")):
        for card in json.loads(data_file.read_text())["skills"]:
            sources = []
            if card.get("effect_d") is not None:
                sources.append(("d", f"{card['effect_d_source']}|{card['effect_d_year']}", card.get("effect_d_journal")))
            if card.get("effect_months") is not None:
                sources.append(("months", card["effect_months_source"], None))
            for kind, source_key, journal in sources:
                key = (kind, source_key)
                entry = entries.setdefault(key, {"source_key": source_key, "kind": kind, "journal": journal, "cards": [], "batch": 0})
                entry["cards"].append(card["id"])
                first_file.setdefault(key, data_file.name)
                if kind == "d" and data_file.name in PILOT_FILES:
                    pilot_keys.add(key)

    # Remaining d sources: keep sources from the same domain file together, then chunk into batches 2-8.
    rest = sorted((k for k in entries if k[0] == "d" and k not in pilot_keys), key=lambda k: (first_file[k], k[1]))
    for key, batch in zip(rest, assign_batches(len(rest))):
        entries[key]["batch"] = batch
    for key in pilot_keys:
        entries[key]["batch"] = 1

    return sorted(entries.values(), key=lambda e: (e["source_key"], e["kind"]))


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.parent.mkdir(parents=True, exist_ok=True)
    worklist = build_worklist(DATA_DIR)
    out.write_text(json.dumps(worklist, indent=2, ensure_ascii=False) + "\n")
    print(f"{len(worklist)} sources -> {out}")
