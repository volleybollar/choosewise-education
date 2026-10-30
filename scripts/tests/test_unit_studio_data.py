"""Vakter för datafilen till Unit Studio (dold sida för Skool-medlemmar).

Datafilen är källan för stegen, evidensen, exemplet och metodkortet.
Prompttexten bor i assets/js/unit-studio.js.
Spec: docs/superpowers/specs/2026-10-30-unit-studio-design.md.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "unit-studio-541ebd12/studio-en.json"
LL_DATA = ROOT / "lesson-lens/lenses-en.json"

STEPS = ["goal-evidence", "prior-knowledge", "sequence-load", "retrieval-checkpoints", "motivation-ai"]
APPROACHES = {"backward-design": "framework", "prior-knowledge": "promising", "explicit-instruction": "strong",
              "retrieval-spacing": "strong", "formative-checkpoints": "strong", "belonging": "promising",
              "trade-off": "choosewise"}
FINAL_PARTS = ["goal_and_evidence", "prior_knowledge", "lessons", "retrieval", "checkpoints", "ai_use", "changes", "check"]


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_five_steps_in_order():
    assert [s["id"] for s in data()["steps"]] == STEPS
    assert [s["num"] for s in data()["steps"]] == [1, 2, 3, 4, 5]


def test_every_step_is_complete():
    for s in data()["steps"]:
        assert s["name"] and s["why"] and s["brief"], s["id"]
        assert 2 <= len(s["look_for"]) <= 4, s["id"]
        assert all(q.strip().endswith("?") for q in s["look_for"]), s["id"]


def test_step5_names_the_trade_off_question():
    step5 = data()["steps"][4]
    assert "what would students get worse at if AI did this part?" in step5["brief"]


def test_approach_labels():
    assert {a["id"]: a["label"] for a in data()["approaches"]} == APPROACHES
    assert set(data()["labels"]) == {"strong", "promising", "framework", "choosewise"}


def test_every_source_https():
    for a in data()["approaches"]:
        assert a["sources"], a["id"]
        for s in a["sources"]:
            assert s["text"] and s["url"].startswith("https://"), a["id"]


def test_every_step_approach_exists():
    ids = {a["id"] for a in data()["approaches"]}
    for s in data()["steps"]:
        assert s["approach_ids"] and set(s["approach_ids"]) <= ids, s["id"]


def test_example_final_plan_has_every_part_and_one_line_per_lesson():
    ex = data()["example"]
    for part in FINAL_PARTS:
        assert ex["final_plan"][part].strip(), part
    lessons = [l for l in ex["final_plan"]["lessons"].splitlines() if re.match(r"^\d+\.", l)]
    assert len(lessons) == ex["weeks"] * ex["lessons"]
    for key in ("keep", "suggest", "question", "ai_can_also"):
        assert ex["step4_reply"][key].strip(), key
    assert ex["step4_reply"]["question"].strip().endswith("?")
    assert len(re.findall(r"^\d\.", ex["step4_reply"]["suggest"], re.M)) <= 3


def test_age_rules_match_lesson_lens():
    ll = json.loads(LL_DATA.read_text(encoding="utf-8"))
    assert data()["age_rules"] == ll["age_rules"]
