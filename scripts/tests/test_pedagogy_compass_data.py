"""Vakter för datafilen till Pedagogy Compass (dold sida för Skool-medlemmar).

Datafilen är källan för problemen, modellkorten, recepten och affischen.
Prompttexten bor i assets/js/pedagogy-compass.js.
Spec: docs/superpowers/specs/2026-10-30-pedagogy-compass-design.md.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "pedagogy-compass-59ecb8db/compass-en.json"
LL_DATA = ROOT / "lesson-lens/lenses-en.json"

CATEGORIES = ["strong", "promising", "framework", "theory", "school", "contested"]
RANK = {c: i for i, c in enumerate(CATEGORIES)}


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def models():
    return {m["id"]: m for m in data()["models"]}


def test_six_categories_in_order():
    cats = data()["categories"]
    assert [c["id"] for c in cats] == CATEGORIES
    assert [c["letter"] for c in cats] == list("ABCDEF")
    for c in cats:
        assert c["name"] and c["question"] and c["label"] in data()["labels"], c["id"]


def test_about_fifty_models_each_in_a_category():
    ms = data()["models"]
    assert 45 <= len(ms) <= 52
    assert len({m["id"] for m in ms}) == len(ms)
    for m in ms:
        assert m["category"] in CATEGORIES, m["id"]
        assert m["name"], m["id"]


def test_ten_problems_point_to_existing_models():
    ps = data()["problems"]
    assert len(ps) == 10
    for p in ps:
        assert p["name"] and p["what_it_looks_like"], p["id"]
        assert 2 <= len(p["model_ids"]) <= 4, p["id"]
        assert set(p["model_ids"]) <= set(models()), p["id"]


def test_problems_list_strongest_evidence_first():
    for p in data()["problems"]:
        ranks = [RANK[models()[i]["category"]] for i in p["model_ids"]]
        assert ranks == sorted(ranks), p["id"]


def test_recipes_reference_existing_models():
    rs = data()["recipes"]
    assert len(rs) == 3
    for r in rs:
        assert r["name"] and r["steps"], r["id"]
        assert set(r["model_ids"]) <= set(models()), r["id"]


def test_labels():
    assert set(data()["labels"]) == {"strong", "promising", "framework", "theory", "school", "contested"}
    for v in data()["labels"].values():
        assert v["name"] and v["definition"]


def test_age_rules_match_lesson_lens():
    ll = json.loads(LL_DATA.read_text(encoding="utf-8"))
    assert data()["age_rules"] == ll["age_rules"]


CARD_FIELDS = ["one_liner", "tuesday", "ai_helps", "ai_harms", "evidence"]


def test_every_card_is_complete():
    for m in data()["models"]:
        for f in CARD_FIELDS:
            assert m.get(f, "").strip(), (m["id"], f)
        assert len(m["one_liner"]) <= 140, m["id"]
        assert 1 <= len(m["sources"]) <= 3, m["id"]
        for s in m["sources"]:
            assert s["text"] and s["url"].startswith("https://"), m["id"]


def test_corrections_to_johans_document_are_in_the_cards():
    ms = models()
    assert "axon" in ms["neuroplasticity"]["evidence"].lower() + ms["neuroplasticity"]["tuesday"].lower()
    assert "metaphor" in ms["cognitivism"]["evidence"].lower() + ms["cognitivism"]["one_liner"].lower()
    assert "contested" in ms["visible-learning"]["evidence"].lower()
    assert all("Waldorff" not in json.dumps(m) for m in data()["models"])
