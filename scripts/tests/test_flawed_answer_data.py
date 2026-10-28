"""Vakter för datafilen till Flawed Answer (flawed-answer/flaws-en.json).

Filen är enda källan för sidan, promptbyggaren och båda PDF:erna.
Spec: docs/superpowers/specs/2026-10-28-flawed-answer-design.md.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "flawed-answer/flaws-en.json"

ORDER = ["wrong-cause", "correlation-as-cause", "missing-step", "overgeneralisation",
         "hidden-assumption", "right-for-wrong-reason"]
EXAMPLE_FIELDS = ["subject", "grade", "level", "question", "answer", "flaw", "fix",
                  "why_convincing", "test_it", "probe", "think_back"]


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_six_flaws_in_order():
    flaws = data()["flaws"]
    assert [f["id"] for f in flaws] == ORDER
    assert [f["number"] for f in flaws] == [1, 2, 3, 4, 5, 6]


def test_examples_cover_six_subjects_and_both_levels():
    examples = [f["example"] for f in data()["flaws"]]
    assert len({e["subject"] for e in examples}) == 6
    levels = [e["level"] for e in examples]
    assert levels.count("easier") == 3 and levels.count("harder") == 3


def test_every_example_field_present_and_nonempty():
    for f in data()["flaws"]:
        for key in ("name", "one_liner", "prompt_brief"):
            assert f[key].strip(), (f["id"], key)
        assert 2 <= len(f["telltale_signs"]) <= 3, f["id"]
        assert isinstance(f["harder_ok"], bool), f["id"]
        for key in EXAMPLE_FIELDS:
            value = f["example"][key]
            assert value if isinstance(value, int) else value.strip(), (f["id"], key)


def test_levels_exact():
    levels = data()["levels"]
    assert [lv["id"] for lv in levels] == ["easier", "harder"]
    assert [lv["name"] for lv in levels] == ["Easier to spot", "Harder to spot"]


def test_labels_strong_and_thin():
    d = data()
    used = {e["label"] for e in d["evidence"]}
    assert used == {"strong", "thin"}
    assert all(label in d["labels"] for label in used)


def test_every_source_has_https_url():
    d = data()
    sources = [s for e in d["evidence"] for s in e["sources"]] + d["context"]["sources"]
    assert sources
    for s in sources:
        assert s["text"].strip() and s["url"].startswith("https://"), s


def test_variant_prompt_starts_with_privacy_line():
    assert data()["variant"]["student_prompt"].startswith("Do not include names")


def test_grades_8_to_12():
    for f in data()["flaws"]:
        assert 8 <= f["example"]["grade"] <= 12, f["id"]


def test_four_steps_in_order():
    names = [s["name"] for s in data()["steps"]]
    assert names == ["Find", "Fix", "Explain why it convinces", "How would we test it?"]


def test_six_icons_match_style():
    allowed = {"#0b3a6f", "#c2793a", "#0c1a2e"}
    for fid in ORDER:
        svg = (ROOT / f"flawed-answer/icons/{fid}.svg").read_text(encoding="utf-8")
        assert 'viewBox="0 0 48 48"' in svg, fid
        colours = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{3,6}\b", svg)}
        assert colours <= allowed, (fid, colours)
        assert "#c2793a" in colours, fid


def test_every_key_quotes_a_whole_sentence_from_the_answer():
    """Nyckeln ska citera den felaktiga meningen ordagrant (spec: en
    kontrollerbar nyckel). Ett avkortat citat lär läraren att godta lösa
    citat när AI:ns nyckel granskas."""
    for f in data()["flaws"]:
        ex = f["example"]
        quote = re.match(r'"(.+?[.!?])"', ex["flaw"])
        assert quote, f["id"]
        sentences = re.split(r"(?<=[.!?])\s+", ex["answer"])
        assert quote.group(1) in sentences, (f["id"], quote.group(1))
