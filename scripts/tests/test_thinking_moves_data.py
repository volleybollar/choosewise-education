"""Vakter för datafilen till Thinking Moves (/thinking-moves/).

Datafilen är sidans, promptbyggarens och PDF:ens enda källa. Ordning,
etiketter och kluster är beslutade av Johan 2026-10-27 — ändra dem inte här
utan att specen ändras först.
Spec: docs/superpowers/specs/2026-10-27-thinking-moves-design.md.
"""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "thinking-moves/moves-en.json"
ICONS = ROOT / "thinking-moves/icons"

ORDER = ["many-ways", "pick-and-justify", "check-the-claim", "argue-it", "like-what",
         "best-explanation", "strip-it-down", "estimate-it", "model-it", "then-what",
         "map-the-loop", "think-back"]
LABELS = {"many-ways": "promising", "pick-and-justify": "promising", "check-the-claim": "strong",
          "argue-it": "promising", "like-what": "strong", "best-explanation": "promising",
          "strip-it-down": "framework", "estimate-it": "framework", "model-it": "promising",
          "then-what": "framework", "map-the-loop": "promising", "think-back": "strong"}
CLUSTERS = {"generating": ["many-ways"],
            "evaluating": ["pick-and-justify", "check-the-claim", "argue-it"],
            "comparing": ["like-what"],
            "explaining": ["best-explanation", "strip-it-down", "estimate-it", "model-it"],
            "causes": ["then-what", "map-the-loop"],
            "regulating": ["think-back"]}
ORIGINAL_13 = {"divergent", "convergent", "lateral", "systems", "associative", "critical",
               "analogical", "abductive", "first principles", "inversion", "second-order",
               "janusian", "metacognitive"}
MATHS_SCIENCE = {"Maths", "Physics", "Chemistry", "Biology", "Science"}
EXAMPLE_FIELDS = ["subject", "grade", "task", "look_for", "probe", "think_back"]
ICON_COLOURS = {"#0B3A6F", "#C2793A", "#0C1A2E"}


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def moves():
    return data()["moves"]


def test_moves_in_agreed_order():
    assert [m["id"] for m in moves()] == ORDER


def test_moves_numbered_and_named():
    for i, m in enumerate(moves(), start=1):
        assert m["number"] == i
        for key in ("name", "one_liner", "modes", "evidence", "prompt_brief"):
            assert m[key].strip(), (m["id"], key)


def test_labels_match_spec():
    assert {m["id"]: m["label"] for m in moves()} == LABELS


def test_clusters_and_their_moves():
    clusters = data()["clusters"]
    assert {c["id"]: c["moves"] for c in clusters} == CLUSTERS
    by_move = {m["id"]: m["cluster"] for m in moves()}
    for c in clusters:
        for mid in c["moves"]:
            assert by_move[mid] == c["id"], mid


def test_all_thirteen_modes_listed():
    names = {mode["name"].lower() for c in data()["clusters"] for mode in c["modes"]}
    assert ORIGINAL_13 <= names, ORIGINAL_13 - names


def test_janusian_and_inversion_have_a_thin_note():
    for c in data()["clusters"]:
        for mode in c["modes"]:
            if mode["name"].lower() in {"janusian", "inversion"}:
                assert "thin" in mode.get("note", "").lower(), mode


def test_two_complete_examples_per_move():
    for m in moves():
        assert len(m["examples"]) == 2, m["id"]
        for ex in m["examples"]:
            for field in EXAMPLE_FIELDS:
                assert str(ex[field]).strip(), (m["id"], field)
            assert 8 <= ex["grade"] <= 12, (m["id"], ex["grade"])


def test_subjects_spread():
    subjects = [ex["subject"] for m in moves() for ex in m["examples"]]
    assert len(set(subjects)) >= 12, sorted(set(subjects))
    assert sum(s in MATHS_SCIENCE for s in subjects) <= 12


def test_label_note_says_regular_teaching():
    assert "not a single five-minute move" in data()["labels"]["note"]
    assert set(data()["labels"]) >= {"strong", "promising", "framework", "note"}


def test_no_unconfirmed_effect_sizes():
    for m in moves():
        if m["id"] in {"like-what", "strip-it-down", "estimate-it", "then-what"}:
            assert not re.search(r"\b[dg]\s*=", m["evidence"]), m["id"]


def test_every_source_has_https_url():
    for m in moves():
        assert m["sources"], m["id"]
        for s in m["sources"]:
            assert s["text"].strip() and s["url"].startswith("https://"), (m["id"], s)


def test_age_rules_cover_four_tools():
    assert {r["tool"] for r in data()["age_rules"]} == {
        "Copilot Chat", "Gemini for Education", "ChatGPT", "Claude"}


def test_every_move_has_an_icon():
    for mid in ORDER:
        path = ICONS / f"{mid}.svg"
        assert path.exists(), mid
        root = ET.fromstring(path.read_text(encoding="utf-8"))
        assert root.get("viewBox") == "0 0 48 48", mid
        colours = {c.upper() for c in re.findall(r"#[0-9A-Fa-f]{6}", path.read_text(encoding="utf-8"))}
        assert colours <= ICON_COLOURS, (mid, colours - ICON_COLOURS)
        assert root.find(".//{http://www.w3.org/2000/svg}text") is None, mid
