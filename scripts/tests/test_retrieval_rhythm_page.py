"""Vakter för sidan Retrieval Rhythm (/retrieval-rhythm/).

Exemplet överst, exempelloggen, formatkorten, evidensen och åldersreglerna
byggs från retrieval-rhythm/rhythm-en.json av scripts/build-retrieval-rhythm.py.
Spec: docs/superpowers/specs/2026-10-30-retrieval-rhythm-design.md.
"""
import importlib.util
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "retrieval-rhythm/index.html"
DATA = ROOT / "retrieval-rhythm/rhythm-en.json"
BUILD = ROOT / "scripts/build-retrieval-rhythm.py"

CARDS = ["starter-quiz", "brain-dump", "retrieval-grid", "multiple-choice", "two-things"]
SECTIONS = ["rr-rhythm", "rr-builder", "rr-formats", "rr-evidence", "rr-age", "rr-download"]


def html():
    return PAGE.read_text(encoding="utf-8")


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def section(section_id):
    m = re.search(rf'<section[^>]*id="{section_id}".*?</section>', html(), re.S)
    assert m, section_id
    return m.group(0)


def cards():
    return re.findall(r'<article class="tm-move rr-format"[^>]*>.*?</article>', html(), re.S)


def marker(name):
    m = re.search(rf"<!-- {name}:start -->(.*?)<!-- {name}:end -->", html(), re.S)
    assert m, name
    return m.group(1)


def load_build():
    spec = importlib.util.spec_from_file_location("build_retrieval_rhythm", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fmt(fid):
    return next(f for f in data()["formats"] if f["id"] == fid)


def test_five_format_cards_in_order():
    ids = re.findall(r'<article class="tm-move rr-format" id="([^"]+)" data-format-id="\1"', html())
    assert ids == CARDS


def test_cards_show_minutes_steps_and_example():
    for fid, card in zip(CARDS, cards()):
        f = fmt(fid)
        assert f"{f['minutes']} min" in card, fid
        for step in f["steps"]:
            assert escape(step) in card, (fid, step)
        assert escape(f["example"]["starter"].splitlines()[0]) in card, fid
        assert ">Key<" in card, fid
        assert f'data-use-format="{fid}"' in card and f'href="?format={fid}#rr-builder"' in card


def test_hero_shows_starter_quiz_example_before_builder():
    hero = marker("hero-example")
    ex = fmt("starter-quiz")["example"]
    assert escape(ex["key"].splitlines()[0]) in hero
    assert '<h3 class="tm-example__subject">' in hero
    assert html().index("<!-- hero-example:start -->") < html().index('id="rr-builder"')


def test_example_log_rendered():
    log = marker("log")
    for row in data()["example_log"]:
        assert escape(row["topic"]) in log and row["date"] in log


def test_build_is_idempotent():
    mod = load_build()
    mod.build(ROOT)
    first = PAGE.read_bytes()
    mod.build(ROOT)
    assert PAGE.read_bytes() == first
    assert len(cards()) == 5


def test_page_has_required_sections():
    for sid in SECTIONS:
        assert re.search(rf'<section[^>]*id="{sid}"', html()), sid


def test_evidence_shows_approaches_and_every_source():
    evidence = section("rr-evidence")
    for a in data()["approaches"]:
        assert escape(a["name"]) in evidence, a["id"]
        for s in a["sources"]:
            assert escape(s["url"]) in evidence, s["url"]
    for name in ("Strong", "Promising", "Framework"):
        assert f">{name}<" in evidence


def test_age_section_has_reader_note():
    text = section("rr-age")
    for word in ("Copilot Chat", "Gemini", "ChatGPT", "Claude", "national", "school policy"):
        assert word in text, word


def test_privacy_line_visible():
    assert "Do not include student names or student results" in section("rr-builder")


def test_downloads():
    dl = section("rr-download")
    assert 'href="/assets/downloads/retrieval-rhythm-log.xlsx"' in dl
    assert 'href="/assets/pdfs/free/retrieval-rhythm-pack-en.pdf"' in dl


def test_back_link_to_hub():
    assert 'href="/pedagogy/"' in html()


def test_json_text_is_escaped():
    mod = load_build()
    f = {"id": "x", "name": "A <b>", "one_liner": "Q & A", "minutes": 5, "prompt_brief": "p",
         "steps": ["<i>s</i>"], "example": {"lesson": 1, "starter": "<u>q</u>", "key": "k"}}
    out = mod.render_format_card(f)
    assert "<b>" not in out and "&lt;b&gt;" in out and "<i>s</i>" not in out and "<u>q</u>" not in out
