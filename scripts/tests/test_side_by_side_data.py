"""Vakter för datafilen till Side by Side (side-by-side/pairs-en.json).

Filen är enda källan för sidan, promptbyggaren och båda PDF:erna.
Spec: docs/superpowers/specs/2026-10-28-side-by-side-design.md.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "side-by-side/pairs-en.json"

ORDER = ["two-ways", "right-and-wrong", "one-change", "confusable-concepts", "two-sources"]
NAMES = ["Two ways to the same answer", "Right next to wrong", "One thing changed",
         "Two concepts that are easily confused", "Two sources on the same event"]
EXAMPLE_FIELDS = ["subject", "grade", "level", "task", "a_label", "a", "b_label", "b",
                  "only_a", "both", "only_b", "rule", "case_c", "case_c_answer",
                  "probe", "think_back"]
ERROR_LINE = "This solution has an error."


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_five_pairs_in_order():
    pairs = data()["pairs"]
    assert [p["id"] for p in pairs] == ORDER
    assert [p["name"] for p in pairs] == NAMES
    assert [p["number"] for p in pairs] == [1, 2, 3, 4, 5]


def test_examples_cover_five_subjects_and_both_levels():
    examples = [p["example"] for p in data()["pairs"]]
    assert len({e["subject"] for e in examples}) == 5
    assert {e["level"] for e in examples} == {"easier", "harder"}


def test_every_example_field_present_and_nonempty():
    for p in data()["pairs"]:
        for key in ("name", "one_liner", "prompt_brief"):
            assert p[key].strip(), (p["id"], key)
        assert 2 <= len(p["look_for"]) <= 3, p["id"]
        assert isinstance(p["harder_ok"], bool), p["id"]
        for key in EXAMPLE_FIELDS:
            value = p["example"][key]
            assert value if isinstance(value, int) else value.strip(), (p["id"], key)


def test_levels_exact():
    levels = data()["levels"]
    assert [lv["id"] for lv in levels] == ["easier", "harder"]
    assert [lv["name"] for lv in levels] == ["Easier to see", "Harder to see"]


def test_four_steps_in_order():
    names = [s["name"] for s in data()["steps"]]
    assert names == ["Compare", "Write the rule", "Try it on case C", "Think back"]


def test_labels_used_are_defined():
    d = data()
    used = {p["label"] for p in d["pairs"]} | {e["label"] for e in d["evidence"]}
    assert used <= set(d["labels"]) - {"note"}
    assert {"strong", "promising"} <= used


def test_every_source_has_https_url():
    d = data()
    sources = [s for e in d["evidence"] for s in e["sources"]] + d["context"]["sources"]
    assert sources
    for s in sources:
        assert s["text"].strip() and s["url"].startswith("https://"), s


def test_no_marzano():
    # Marzanos effektstorlek för "likheter och skillnader" saknar oberoende
    # granskning (spec: citeras aldrig).
    assert "marzano" not in DATA.read_text(encoding="utf-8").lower()


def test_right_and_wrong_marks_the_error():
    ex = next(p for p in data()["pairs"] if p["id"] == "right-and-wrong")["example"]
    assert [ERROR_LINE in ex["a"], ERROR_LINE in ex["b"]].count(True) == 1


def test_variant_prompt_starts_with_privacy_line_and_lists_types():
    prompt = data()["variant"]["student_prompt"]
    assert prompt.startswith("Do not include names or personal details in this conversation.")
    for name in NAMES:
        assert name in prompt, name


def test_grades_7_to_12():
    for p in data()["pairs"]:
        assert 7 <= p["example"]["grade"] <= 12, p["id"]


def test_five_icons_match_style():
    allowed = {"#0b3a6f", "#c2793a", "#0c1a2e"}
    for pid in ORDER:
        svg = (ROOT / f"side-by-side/icons/{pid}.svg").read_text(encoding="utf-8")
        assert 'viewBox="0 0 48 48"' in svg, pid
        colours = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{3,6}\b", svg)}
        assert colours <= allowed, (pid, colours)
        assert "#c2793a" in colours, pid


def _example(pid):
    return next(p for p in data()["pairs"] if p["id"] == pid)["example"]


def test_one_change_case_c_turns_on_the_changed_variable():
    # Regeln handlar om ljus, så fall C måste också handla om ljus — annars
    # kan eleverna inte avgöra det med regeln de just skrev (spec, anti-mål).
    case_c = _example("one-change")["case_c"].lower()
    assert "dark" in case_c or "light" in case_c, case_c
    assert "dry" not in case_c


def test_two_sources_rule_covers_purpose_used_in_case_c():
    # Svaret på fall C bygger på syftet (att övertyga), så regeln måste nämna det.
    ex = _example("two-sources")
    assert "persuade" in ex["case_c_answer"]
    assert "persuade" in ex["rule"]
