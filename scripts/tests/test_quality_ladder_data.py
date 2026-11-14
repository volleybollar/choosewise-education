"""Vakter för datafilen till Quality Ladder (/quality-ladder-ec1c2f8c/).

Datafilen är sidans och Word-mallarnas enda källa för text. Rutinen, etiketterna
och formuleringarna om AI är beslutade i specen
(docs/superpowers/specs/2026-11-14-what-teachers-do-design.md, del B) — ändra dem
inte här utan att specen ändras först.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLUG = "quality-ladder-ec1c2f8c"
DATA_PATH = ROOT / SLUG / "ladder-en.json"
COUNTDOWN_PATH = ROOT / "test-countdown/countdown-en.json"

KEYS = {"labels", "example", "routine", "whole_class", "policy", "colleagues", "evidence",
        "care", "age_rules", "age_rules_date"}
LEVELS = {"weakest", "middle", "strongest"}
# Etikett per forskningspunkt, i specens ordning (avsnitt B7).
EVIDENCE_LABELS = ["strong", "strong", "promising", "promising", "framework", "promising"]
PLACEHOLDERS = {"[School]", "[Team]", "[Date]", "[Review date]"}
# Ord som aldrig får stå på sidan: löften om AI-säkerhet, nedvärderande ord om
# effektstorlekar och amerikansk stavning (sidan skrivs på brittisk engelska).
BANNED = ["ai-proof", "low effect", "doesn't work", "does not work", "color", "behavior",
          "organize"]


def data():
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def all_strings(node):
    """Varje textsträng i JSON-trädet, på alla djup."""
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from all_strings(value)
    elif isinstance(node, list):
        for value in node:
            yield from all_strings(value)


def test_top_level_keys():
    assert set(data()) == KEYS


def test_example_order():
    example = data()["example"]
    assert [s["letter"] for s in example["samples"]] == ["A", "B", "C"]
    assert [k["letter"] for k in example["key"]] == ["A", "B", "C"]
    assert {k["level"] for k in example["key"]} == LEVELS
    # Eleverna ska bedöma kvaliteten själva: A får aldrig vara det svagaste svaret.
    assert example["key"][0]["level"] != "weakest"
    assert len(example["criteria"]) == 3
    for k in example["key"]:
        assert k["note"] and k["up"]


def test_routine_has_six_steps_and_second_answer_at_reveal():
    routine = data()["routine"]
    assert len(routine["steps"]) == 6
    assert "second strong answer" in routine["steps"][3].lower()
    assert "aloud" in routine["younger"]
    assert len(routine["sheet"]) == 3


def test_whole_class_keeps_names_out_of_ai():
    wc = data()["whole_class"]
    text = " ".join(all_strings(wc))
    assert "on paper or in this document, never in an AI tool" in text
    assert len(wc["sections"]) >= 5


def test_evidence_labels():
    evidence = data()["evidence"]
    assert [e["label"] for e in evidence] == EVIDENCE_LABELS
    for item in evidence:
        assert item["title"] and item["text"] and item["sources"]
        for source in item["sources"]:
            assert source["url"].startswith("https://"), source


def test_labels():
    labels = data()["labels"]
    assert set(labels) == {"strong", "promising", "framework", "choosewise"}
    assert {v["name"] for v in labels.values()} == {"Strong", "Promising", "Framework", "Choosewise"}


def test_policy_placeholders():
    policy = data()["policy"]
    assert PLACEHOLDERS <= set(policy["placeholders"])
    text = policy["intro"] + " ".join(p["title"] + " " + p["text"] for p in policy["principles"])
    for placeholder in PLACEHOLDERS:
        assert placeholder in text, placeholder


def test_care_points():
    care = data()["care"]
    assert len(care) == 4
    for item in care:
        assert item["risk"] and item["what_we_do"]


def test_age_rules_match_countdown():
    countdown = json.loads(COUNTDOWN_PATH.read_text(encoding="utf-8"))
    d = data()
    assert d["age_rules"] == countdown["age_rules"]
    assert d["age_rules_date"] == countdown["age_rules_date"]


def test_banned_words():
    for text in all_strings(data()):
        lowered = text.lower()
        for word in BANNED:
            assert word not in lowered, (word, text)
