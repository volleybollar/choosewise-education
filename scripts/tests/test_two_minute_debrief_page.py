"""Vakter för sidan Two-Minute Debrief (/two-minute-debrief/).

Exemplen, sammanställningsexemplet, exit tickets, evidensen och åldersreglerna
byggs från two-minute-debrief/debrief-en.json av
scripts/build-two-minute-debrief.py.
Spec: docs/superpowers/specs/2026-10-30-two-minute-debrief-design.md.
"""
import importlib.util
import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "two-minute-debrief/index.html"
DATA = ROOT / "two-minute-debrief/debrief-en.json"
BUILD = ROOT / "scripts/build-two-minute-debrief.py"

SECTIONS = ["td-how", "td-builder", "td-rollup", "td-tickets", "td-examples", "td-evidence", "td-age", "td-download"]


def html():
    return PAGE.read_text(encoding="utf-8")


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def section(section_id):
    m = re.search(rf'<section[^>]*id="{section_id}".*?</section>', html(), re.S)
    assert m, section_id
    return m.group(0)


def marker(name):
    m = re.search(rf"<!-- {name}:start -->(.*?)<!-- {name}:end -->", html(), re.S)
    assert m, name
    return m.group(1)


def load_build():
    spec = importlib.util.spec_from_file_location("build_two_minute_debrief", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_page_has_required_sections():
    for sid in SECTIONS:
        assert re.search(rf'<section[^>]*id="{sid}"', html()), sid


def test_hero_shows_hero_example_before_builder():
    hero = marker("hero-example")
    ex = next(e for e in data()["examples"] if e["id"] == data()["hero_example"])
    assert escape(ex["evidence"]) in hero
    assert escape(ex["reply"]["next_lesson"]) in hero
    assert '<h3 class="tm-example__subject">' in hero
    assert html().index("<!-- hero-example:start -->") < html().index('id="td-builder"')


def test_four_examples_rendered():
    block = marker("examples")
    for e in data()["examples"]:
        assert escape(e["title"]) in block, e["id"]
        assert escape(e["reply"]["likely_causes"].splitlines()[0]) in block, e["id"]


def test_rollup_example_rendered():
    block = marker("rollup-example")
    rx = data()["rollup_example"]
    assert escape(rx["reply"]["one_change"]) in block
    for d in rx["debriefs"]:
        assert escape(d["group"]) in block


def test_four_exit_tickets_with_both_setups():
    block = section("td-tickets")
    for t in data()["exit_tickets"]:
        assert escape(t["name"]) in block, t["id"]
        assert escape(t["forms_steps"][0]) in block, t["id"]
        assert escape(t["google_steps"][0]) in block, t["id"]
    assert "Microsoft Forms" in block and "Google Forms" in block


def test_evidence_shows_every_source_and_label_names():
    evidence = section("td-evidence")
    for a in data()["approaches"]:
        assert escape(a["name"]) in evidence, a["id"]
        for s in a["sources"]:
            assert escape(s["url"]) in evidence, s["url"]
    for name in ("Strong", "Promising", "Framework"):
        assert f">{name}<" in evidence


def test_age_section_has_reader_note():
    text = section("td-age")
    for word in ("Copilot Chat", "Gemini", "ChatGPT", "Claude", "national", "school policy"):
        assert word in text, word


def test_privacy_line_visible():
    assert "Do not include student names or student results" in section("td-builder")


def test_storage_line_visible():
    assert "Saved only in this browser on this device" in section("td-builder")


def test_before_you_meet_the_group_again():
    assert "Run it before you meet the group again." in section("td-builder")


def test_lessons_that_did_not_go_as_planned_line_in_hero():
    hero = html()[:html().index('id="td-how"')]
    assert "For the lessons that didn&#x27;t go as planned" in hero or "For the lessons that didn't go as planned" in hero


def test_evidence_hint_asks_for_patterns_not_names():
    builder = section("td-builder")
    assert "11 of 27 forgot to divide the + 5" in builder
    assert "No names, no individual results." in builder


def test_form_has_the_builder_ids():
    for el in ("td-group", "td-grade", "td-goal", "td-evidence", "td-surprise", "td-next", "td-followup",
               "td-prompt", "td-copy", "td-hint", "td-save", "td-storage-note", "td-saved", "td-batch-copy",
               "td-batch-prompt", "td-batch-hint", "td-delete-all", "td-rollup-list", "td-rollup-paste",
               "td-rollup-prompt", "td-rollup-copy", "td-rollup-hint", "td-hinge-prompt", "td-hinge-copy"):
        assert f'id="{el}"' in html(), el


def test_downloads():
    dl = section("td-download")
    assert 'href="/assets/downloads/two-minute-debrief-journal.xlsx"' in dl
    assert 'href="/assets/pdfs/free/two-minute-debrief-pack-en.pdf"' in dl


def test_back_link_to_hub():
    assert 'href="/pedagogy/"' in html()


def test_scripts_loaded():
    assert '<script src="/assets/js/copy-to-clipboard.js" defer></script>' in html()
    assert '<script src="/assets/js/two-minute-debrief.js" defer></script>' in html()


def test_committed_page_matches_a_fresh_build(tmp_path):
    # Bygger på en kopia, så att testet fångar en JSON-ändring som inte
    # byggts in, i stället för att tyst bygga om den riktiga sidan.
    shutil.copytree(ROOT / "two-minute-debrief", tmp_path / "two-minute-debrief")
    mod = load_build()
    mod.build(tmp_path)
    once = (tmp_path / "two-minute-debrief/index.html").read_bytes()
    assert once == PAGE.read_bytes()
    mod.build(tmp_path)
    assert (tmp_path / "two-minute-debrief/index.html").read_bytes() == once


def test_json_text_is_escaped():
    mod = load_build()
    ex = {"id": "x", "title": "t", "group": "A <b>", "grade": 8, "goal": "<i>g</i>", "evidence": "e & f",
          "surprise": "s", "next": "n",
          "reply": {"likely_causes": "<u>1.</u>", "next_lesson": "n", "check_first": "c", "one_question": "q?"}}
    out = mod.render_example(ex)
    assert "<b>" not in out and "&lt;b&gt;" in out and "<i>g</i>" not in out and "<u>1.</u>" not in out
