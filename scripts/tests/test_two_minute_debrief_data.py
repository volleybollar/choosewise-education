"""Vakter för datafilen till Two-Minute Debrief (/two-minute-debrief/).

Datafilen är källan för sidans exempel, exit tickets, evidens, enhetsjournalens
exempel och PDF:en. Prompttexten bor i assets/js/two-minute-debrief.js.
Spec: docs/superpowers/specs/2026-10-30-two-minute-debrief-design.md.
"""
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "two-minute-debrief/debrief-en.json"
LL_DATA = ROOT / "lesson-lens/lenses-en.json"

APPROACHES = {"formative-assessment": "strong", "feedback": "strong", "worked-examples": "strong",
              "hinge-questions": "framework", "teacher-reflection": "framework"}
TICKETS = ["one-question", "hinge", "confidence", "one-sentence"]
NAMES = ["Emma", "Liam", "Noah", "Olivia", "Ali", "Sara"]


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def examples():
    return data()["examples"]


def test_four_debrief_examples_cover_the_cases():
    exs = examples()
    assert len(exs) == 4
    assert all(6 <= e["grade"] <= 12 for e in exs)
    assert sum("math" in e["group"].lower() for e in exs) <= 1
    assert any(not re.search(r"\d", e["evidence"]) for e in exs), "an example with only a feeling"
    assert any(re.search(r"\d+ of \d+", e["evidence"]) for e in exs), "an example with exit ticket counts"
    assert any(e["evidence"].startswith("Check:") for e in exs), "a follow-up example"
    for e in exs:
        for key in ("id", "title", "group", "goal", "evidence", "surprise", "next"):
            assert e[key].strip(), (e.get("id"), key)


def test_hero_example_exists():
    assert data()["hero_example"] in [e["id"] for e in examples()]


def test_every_reply_has_two_causes_minutes_and_a_question():
    for e in examples():
        r = e["reply"]
        assert "1." in r["likely_causes"] and "2." in r["likely_causes"], e["id"]
        assert re.search(r"\d+ min", r["next_lesson"]), e["id"]
        assert r["check_first"].strip(), e["id"]
        assert r["one_question"].strip().endswith("?"), e["id"]


def test_rollup_example_is_complete():
    rx = data()["rollup_example"]
    assert 4 <= len(rx["debriefs"]) <= 5
    for key in ("patterns", "what_worked", "one_change", "one_question"):
        assert rx["reply"][key].strip(), key
    assert rx["reply"]["one_question"].strip().endswith("?")


def test_exit_tickets_are_the_four_types():
    tickets = data()["exit_tickets"]
    assert [t["id"] for t in tickets] == TICKETS
    for t in tickets:
        assert 1 <= len(t["forms_steps"]) <= 5, t["id"]
        assert 1 <= len(t["google_steps"]) <= 5, t["id"]
        assert t["name"] and t["when"] and t["student_text"] and t["paper_note"], t["id"]


def test_examples_contain_no_names():
    texts = [e["evidence"] for e in examples()] + [d["evidence"] for d in data()["rollup_example"]["debriefs"]]
    texts += [r["evidence"] for r in data()["journal_example"]]
    for t in texts:
        assert not any(re.search(rf"\b{n}\b", t) for n in NAMES), t
        assert not re.search(r"\bstudent [A-Z]", t), t


def test_approaches_and_labels():
    assert {a["id"]: a["label"] for a in data()["approaches"]} == APPROACHES
    assert set(data()["labels"]) == {"strong", "promising", "framework"}
    for a in data()["approaches"]:
        assert a["sources"], a["id"]
        for s in a["sources"]:
            assert s["text"] and s["url"].startswith("https://"), a["id"]


def test_journal_example_shows_improvement():
    rows = data()["journal_example"]
    assert len(rows) == 5
    days = [date.fromisoformat(r["date"]) for r in rows]
    assert days == sorted(days)
    first = int(re.search(r"\d+", rows[0]["check"]).group())
    last = int(re.search(r"\d+", rows[-1]["check"]).group())
    assert last > first


def test_fact_check_corrections_2026_10_30():
    # Faktagranskningen: att dividera först är giltigt — felet är att +5 inte divideras;
    # 11 var antalet fel, så utgångsläget var 16 rätt; dagtid är det inte natt i Storbritannien.
    exs = {e["id"]: e for e in examples()}
    assert "divided by 3 first but left the + 5 unchanged" in exs["maths-equations"]["evidence"]
    assert "the + 5 must then be divided too" in exs["maths-equations"]["reply"]["likely_causes"]
    assert "night in Australia" in exs["science-day-night"]["reply"]["check_first"]
    rx = data()["rollup_example"]
    assert rx["debriefs"][1]["evidence"] == "Check: 20 of 27 right, up from 16."
    assert "from 16 to 20 of 27 right" in rx["reply"]["what_worked"]
    assert rx["debriefs"][3]["group"] == "10B English"
    hinge = next(t for t in data()["exit_tickets"] if t["id"] == "hinge")
    assert "a dry log" in hinge["student_text"]
    approaches = {a["id"]: a for a in data()["approaches"]}
    assert "letter cards everyone holds up at once" in approaches["hinge-questions"]["evidence"]
    assert "no meta-analysis shows that it improves student learning" in approaches["teacher-reflection"]["evidence"]


def test_age_rules_match_lesson_lens():
    ll = json.loads(LL_DATA.read_text(encoding="utf-8"))
    assert data()["age_rules"] == ll["age_rules"]
