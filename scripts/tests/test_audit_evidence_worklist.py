"""Tests for scripts/audit_evidence_worklist.py (Evidence Toolkit audit, 2026-10)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audit_evidence_worklist import build_worklist  # noqa: E402

DATA_DIR = Path(__file__).resolve().parents[2] / "evidence" / "data"


def _cards_in(filename):
    return {s["id"] for s in json.loads((DATA_DIR / filename).read_text())["skills"]}


def test_worklist_counts_match_data():
    # The October 2026 audit ran on 53 d-sources and 10 months-sources; the corrections
    # changed the data since, so count what the data holds now.
    skills = [s for f in DATA_DIR.glob("*.json") for s in json.loads(f.read_text())["skills"]]
    d_sources = {f"{s['effect_d_source']}|{s['effect_d_year']}" for s in skills if s.get("effect_d") is not None}
    month_sources = {s["effect_months_source"] for s in skills if s.get("effect_months") is not None}
    worklist = build_worklist(DATA_DIR)
    assert sum(1 for e in worklist if e["kind"] == "d") == len(d_sources)
    assert sum(1 for e in worklist if e["kind"] == "months") == len(month_sources)


def test_reused_source_lists_all_cards():
    worklist = build_worklist(DATA_DIR)
    yao = [e for e in worklist if e["kind"] == "d" and e["source_key"] == "Yao, Amos, Snider & Brown|2024"]
    assert len(yao) == 1
    assert len(yao[0]["cards"]) == 5


def test_batches_cover_every_d_source_once():
    worklist = build_worklist(DATA_DIR)
    d_entries = [e for e in worklist if e["kind"] == "d"]
    assert len({e["source_key"] for e in d_entries}) == len(d_entries)
    assert {e["batch"] for e in d_entries} == set(range(1, 9))
    assert all(e["batch"] == 0 for e in worklist if e["kind"] == "months")


def test_batch_one_is_memory_and_explicit_instruction():
    worklist = build_worklist(DATA_DIR)
    pilot_cards = _cards_in("memory.json") | _cards_in("explicit-instruction.json")
    for e in worklist:
        if e["kind"] != "d":
            continue
        uses_pilot_card = bool(pilot_cards & set(e["cards"]))
        assert (e["batch"] == 1) == uses_pilot_card, e["source_key"]


def test_assign_batches_never_leaves_a_batch_empty():
    from audit_evidence_worklist import assign_batches
    for n in (7, 8, 9, 36, 42, 50):
        batches = assign_batches(n)
        assert len(batches) == n
        assert set(batches) == set(range(2, 9)), n
        assert batches == sorted(batches)
