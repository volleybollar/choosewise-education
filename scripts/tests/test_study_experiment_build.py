"""Vakter för sidan The Study Experiment (/study-experiment/) och dess byggskript.

Översikten, de två lektionerna, diskussionen, evidensen och åldersreglerna
byggs från study-experiment/experiment-en.json av
scripts/build-study-experiment.py, så att de syns utan JavaScript och kan
indexeras. Byggaren och resultatvyn är statisk HTML här; deras JavaScript
vaktas av egna tester. Testerna läser den byggda sidan och kör byggskriptet.
Spec: docs/superpowers/specs/2026-11-13-study-experiment-design.md.
"""
import importlib.util
import json
import re
import shutil
from html import escape
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "study-experiment/index.html"
DATA = ROOT / "study-experiment/experiment-en.json"
BUILD = ROOT / "scripts/build-study-experiment.py"

SECTIONS = ["se-how", "se-lesson1", "se-lesson2", "se-make", "se-results", "se-evidence", "se-age", "se-download"]


def html():
    return PAGE.read_text(encoding="utf-8")


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def load_build():
    spec = importlib.util.spec_from_file_location("build_study_experiment", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def section(section_id, page=None):
    m = re.search(rf'<section[^>]*id="{section_id}".*?</section>', page or html(), re.S)
    assert m, section_id
    return m.group(0)


def test_render_escapes_text():
    lesson = {"intro": "I <i>", "steps": [{"minutes": 4, "text": "A <b>&</b>"}, {"minutes": None, "text": "B"}]}
    out = load_build().render_lesson(lesson, {"minutes": {"lesson1": 4}}, 1)
    assert "&lt;b&gt;" in out and "<b>" not in out and "<i>" not in out


def test_lessons_have_all_steps():
    d = data()
    for number in (1, 2):
        lesson = d[f"lesson{number}"]
        sec = section(f"se-lesson{number}")
        assert escape(lesson["intro"]) in sec, number
        for step in lesson["steps"]:
            assert escape(step["text"]) in sec, (number, step["text"])
            if step["minutes"] is not None:
                assert f'<span class="se-minutes">{step["minutes"]} min</span>' in sec, (number, step["minutes"])
        # Steg utan egen tid får ingen minutetikett.
        assert sec.count('class="se-minutes"') == sum(1 for s in lesson["steps"] if s["minutes"] is not None)
        assert len(re.findall(r"<li", re.search(r'<ol class="se-steps".*?</ol>', sec, re.S).group(0))) == len(lesson["steps"])
    assert "4 min" in html()


def test_discussion_and_even_result():
    d = data()
    sec = section("se-lesson2")
    for question in d["discussion"]:
        assert escape(question) in sec, question
    assert escape(d["explain"]["title"]) in sec
    assert len(d["explain"]["points"]) == 3
    for point in d["explain"]["points"]:
        assert escape(point) in sec, point
    assert escape(d["even_result"]["title"]) in sec and escape(d["even_result"]["text"]) in sec
    assert 'id="se-even-result"' in sec
    assert escape(d["no_computer"]) in sec


def test_overview_has_expect():
    d = data()
    how = section("se-how")
    assert escape(d["expect"]) in how
    assert "What to expect" in how
    assert f'{d["minutes"]["lesson1"]} minutes' in how and f'{d["minutes"]["lesson2"]} minutes' in how
    assert "20 minutes" in how and "25 minutes" in how
    for text in d["materials"] + d["before"]:
        assert escape(text) in how, text


def test_build_is_idempotent(tmp_path):
    (tmp_path / "study-experiment").mkdir()
    shutil.copy(PAGE, tmp_path / "study-experiment/index.html")
    shutil.copy(DATA, tmp_path / "study-experiment/experiment-en.json")
    mod = load_build()
    mod.build(tmp_path)
    first = (tmp_path / "study-experiment/index.html").read_bytes()
    mod.build(tmp_path)
    assert (tmp_path / "study-experiment/index.html").read_bytes() == first


def test_page_is_built_from_current_json(tmp_path):
    # Den incheckade sidan ska vara byggd från den incheckade JSON-filen.
    (tmp_path / "study-experiment").mkdir()
    shutil.copy(PAGE, tmp_path / "study-experiment/index.html")
    shutil.copy(DATA, tmp_path / "study-experiment/experiment-en.json")
    load_build().build(tmp_path)
    assert (tmp_path / "study-experiment/index.html").read_text(encoding="utf-8") == html()


def test_missing_marker_raises():
    with pytest.raises(ValueError):
        load_build()._inject("<p>no markers</p>", "overview", "x")


def test_page_states_age_rules_date():
    age = section("se-age")
    assert f'({data()["age_rules_date"]})' in age
    assert "Students do not use AI in this experiment." in age
    for rule in data()["age_rules"]:
        assert escape(rule["tool"]) in age and escape(rule["rule"]) in age
    assert ("Rules differ between countries and change often. Check your own national rules "
            "and your school policy before students use any AI tool.") in age


def test_every_evidence_source_linked():
    evidence = section("se-evidence")
    for item in data()["evidence"]:
        assert escape(item["text"]) in evidence, item["text"]
        for s in item["sources"]:
            assert f'href="{escape(s["url"])}"' in evidence, s["url"]
            assert escape(s["text"]) in evidence, s["text"]


def test_sections_in_order():
    page = html()
    positions = [page.index(f'id="{sid}"') for sid in SECTIONS]
    assert positions == sorted(positions)


def test_hero_back_link_and_download():
    page = html()
    assert '<a class="tm-back" href="/study/">← Study + AI</a>' in page
    assert "Free classroom kit · Grades 7–12" in page and "<h1>The Study Experiment</h1>" in page
    assert 'content="https://choosewise.education/assets/images/brand/og/studyexperiment-en.png"' in page
    assert "study-experiment.css?v=20261113a" in page
    download = section("se-download")
    assert 'href="/assets/pdfs/free/study-experiment-kit-en.pdf"' in download
    assert ">Download the teacher kit (PDF)<" in download
    assert 'href="/study-moves/#test-yourself"' in download


def test_noai_paragraph_sits_under_builder():
    make = section("se-make")
    assert escape(data()["no_ai"]) in make
    assert make.index('id="se-builder"') < make.index(escape(data()["no_ai"]))


def test_builder_has_fields_and_defaults():
    make = section("se-make")
    builder = re.search(r'id="se-builder".*', make, re.S).group(0)
    for el in ("se-subject", "se-subjects", "se-grade", "se-topic", "se-language", "se-prompt", "se-copy", "se-hint"):
        assert f'id="{el}"' in builder, el
    assert '<option value="9" selected>' in builder
    grades = re.findall(r'<option value="(\d+)"', re.search(r'<select[^>]*id="se-grade".*?</select>', builder, re.S).group(0))
    assert grades == [str(g) for g in range(7, 13)]
    assert re.search(r'<textarea[^>]*id="se-topic"[^>]*maxlength="300"', builder)
    assert re.search(r'<input[^>]*id="se-language"[^>]*value="English"[^>]*maxlength="40"', builder)
    assert re.search(r'<textarea[^>]*id="se-prompt"[^>]*readonly', builder)
    assert re.search(r'<button[^>]*id="se-copy"[^>]*data-copy=""[^>]*aria-describedby="se-hint"[^>]*disabled', builder)
    assert "Fill in subject and topic area to see your prompt." in builder
    # Samma ämnesförslag som Study Moves.
    moves = (ROOT / "study-moves/index.html").read_text(encoding="utf-8")
    options = lambda page, dl: re.findall(r'<option value="([^"]+)">', re.search(rf'<datalist id="{dl}">.*?</datalist>', page, re.S).group(0))
    assert options(builder, "se-subjects") == options(moves, "sm-subjects")


def test_results_form_has_fields():
    results = section("se-results")
    assert re.search(r'<input[^>]*id="se-max"[^>]*type="number"[^>]*min="1"[^>]*max="20"[^>]*value="6"', results) or \
        re.search(r'<input[^>]*type="number"[^>]*id="se-max"[^>]*min="1"[^>]*max="20"[^>]*value="6"', results)
    for el in ("se-pred-twice", "se-pred-tested", "se-pred-same"):
        assert re.search(rf'<input[^>]*id="{el}"[^>]*min="0"', results), el
        assert re.search(rf'<input[^>]*type="number"[^>]*id="{el}"|<input[^>]*id="{el}"[^>]*type="number"', results), el
    assert 'id="se-scores"' in results and "<textarea" in results
    assert re.search(r'id="se-errors"[^>]*aria-live="polite"|aria-live="polite"[^>]*id="se-errors"', results)
    for el in ("se-summary", "se-chart"):
        assert f'id="{el}"' in results, el
    assert re.search(r'<p[^>]*id="se-even"[^>]*hidden', results)
    assert 'href="#se-even-result"' in results
    for label in ("Questions per text", "Predicted: the text read twice", "Predicted: the text tested",
                  "Predicted: about the same",
                  "Scores, one slip per line: the text read twice, then the text tested (for example 3 5)"):
        assert label in results, label
