"""Vakter för datafilen till Retrieval Rhythm (/retrieval-rhythm/).

Datafilen är sidans, promptbyggarens, loggmallens och PDF:ens enda källa.
Spec: docs/superpowers/specs/2026-10-30-retrieval-rhythm-design.md.
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "retrieval-rhythm/rhythm-en.json"
LL_DATA = ROOT / "lesson-lens/lenses-en.json"

ORDER = ["mix", "starter-quiz", "brain-dump", "retrieval-grid", "multiple-choice", "two-things"]
APPROACHES = {"retrieval-practice": "strong", "spacing": "strong",
              "interleaving": "promising", "misconception-options": "promising"}


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def formats():
    return data()["formats"]


def test_formats_in_agreed_order():
    assert [f["id"] for f in formats()] == ORDER


def test_default_format_is_mix():
    assert data()["default_format"] == "mix"


def test_every_format_is_complete():
    for f in formats():
        assert f["name"] and f["one_liner"] and f["prompt_brief"], f["id"]
        assert isinstance(f["minutes"], int) and 1 <= f["minutes"] <= 10, f["id"]
        assert f["steps"] and all(s.strip() for s in f["steps"]), f["id"]


def test_every_real_format_has_an_example():
    for f in formats():
        if f["id"] == "mix":
            assert "example" not in f
            continue
        ex = f["example"]
        assert ex["starter"].strip() and ex["key"].strip(), f["id"]
        assert 1 <= ex["lesson"] <= 5, f["id"]


def test_mix_brief_names_all_five_formats():
    brief = next(f for f in formats() if f["id"] == "mix")["prompt_brief"].lower()
    for f in formats()[1:]:
        assert f["name"].lower() + " (" in brief, f["name"]


def test_multiple_choice_example_has_four_options():
    starter = next(f for f in formats() if f["id"] == "multiple-choice")["example"]["starter"]
    for letter in ("A ", "B ", "C ", "D "):
        assert letter in starter, letter


def test_approaches_and_labels():
    assert {a["id"]: a["label"] for a in data()["approaches"]} == APPROACHES
    assert set(data()["labels"]) == {"strong", "promising", "framework"}


def test_every_source_has_https_url():
    for a in data()["approaches"]:
        assert a["sources"], a["id"]
        for s in a["sources"]:
            assert s["text"] and s["url"].startswith("https://"), a["id"]


def test_example_log_spans_eight_weeks_in_order():
    rows = data()["example_log"]
    assert 6 <= len(rows) <= 10
    days = [date.fromisoformat(r["date"]) for r in rows]
    assert days == sorted(days)
    assert (days[-1] - days[0]).days >= 56
    for r in rows:
        assert r["topic"].strip() and r["key_points"].strip()


def test_age_rules_match_lesson_lens():
    ll = json.loads(LL_DATA.read_text(encoding="utf-8"))
    assert data()["age_rules"] == ll["age_rules"]


def test_grid_counts_back_from_the_newest_entry():
    f = {x["id"]: x for x in formats()}
    assert "counting back from the newest entry" in f["retrieval-grid"]["prompt_brief"]
    assert "Newest week (1 point each)" in f["retrieval-grid"]["example"]["starter"]
    assert "one to three weeks before" in f["mix"]["prompt_brief"]


def test_starter_quiz_does_not_promise_five_questions():
    quiz = next(x for x in formats() if x["id"] == "starter-quiz")
    assert "Five" not in quiz["one_liner"]


def test_multiple_choice_options_are_the_same_length():
    # Johans provkörning 2026-10-30: det rätta svaret var ofta det längsta.
    f = {x["id"]: x for x in formats()}
    assert "Make the four options about the same length." in f["multiple-choice"]["prompt_brief"]
    assert "options A to D of about the same length" in f["mix"]["prompt_brief"]
