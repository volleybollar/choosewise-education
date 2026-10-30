"""Vakter för Unit Studio-sidan (/unit-studio-541ebd12/).

Sidan är bara för Skool-medlemmar: den nås via en dold länk, har noindex
och får aldrig länkas från resten av sajten (Johans beslut 2026-10-30).
Stegen, exemplet, evidensen och åldersreglerna byggs från
unit-studio-541ebd12/studio-en.json av scripts/build-unit-studio.py.
"""
import importlib.util
import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLUG = "unit-studio-541ebd12"
PAGE = ROOT / SLUG / "index.html"
DATA = ROOT / SLUG / "studio-en.json"
BUILD = ROOT / "scripts/build-unit-studio.py"
SECTIONS = ["us-how", "us-builder", "us-steps", "us-final", "us-evidence", "us-age", "us-download"]


def html():
    return PAGE.read_text(encoding="utf-8")


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def section(sid):
    m = re.search(rf'<section[^>]*id="{sid}".*?</section>', html(), re.S)
    assert m, sid
    return m.group(0)


def marker(name):
    m = re.search(rf"<!-- {name}:start -->(.*?)<!-- {name}:end -->", html(), re.S)
    assert m, name
    return m.group(1)


def load_build():
    spec = importlib.util.spec_from_file_location("build_unit_studio", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_page_has_required_sections():
    for sid in SECTIONS:
        assert re.search(rf'<section[^>]*id="{sid}"', html()), sid


def test_ids_are_unique():
    ids = re.findall(r'\bid="([^"]+)"', html())
    assert len(ids) == len(set(ids)), sorted({i for i in ids if ids.count(i) > 1})


def test_five_step_cards_with_questions_and_evidence():
    block = section("us-steps")
    approaches = {a["id"]: a for a in data()["approaches"]}
    for s in data()["steps"]:
        assert escape(s["name"]) in block, s["id"]
        for q in s["look_for"]:
            assert escape(q) in block, q
        for aid in s["approach_ids"]:
            assert escape(approaches[aid]["name"]) in block, aid


def test_hero_shows_example_before_builder():
    hero = marker("hero-example")
    ex = data()["example"]
    assert escape(ex["unit_text"].splitlines()[0]) in hero
    assert escape(ex["step4_reply"]["question"]) in hero
    assert html().index("<!-- hero-example:start -->") < html().index('id="us-builder"')


def test_final_example_has_every_part():
    block = marker("final-example")
    for part in data()["example"]["final_plan"].values():
        assert escape(part.splitlines()[0]) in block


def test_step_data_block_for_the_builder():
    m = re.search(r'<script type="application/json" id="us-data">(.*?)</script>', html(), re.S)
    assert m
    steps = json.loads(m.group(1))["steps"]
    assert [(s["num"], s["name"], s["brief"]) for s in steps] == [(s["num"], s["name"], s["brief"]) for s in data()["steps"]]


def test_evidence_shows_every_source_and_labels():
    block = section("us-evidence")
    for a in data()["approaches"]:
        for s in a["sources"]:
            assert escape(s["url"]) in block, s["url"]
    for name in ("Strong", "Promising", "Framework", "Choosewise"):
        assert f">{name}<" in block


def test_age_section_has_reader_note():
    text = section("us-age")
    for word in ("Copilot Chat", "Gemini", "ChatGPT", "Claude", "national", "school policy"):
        assert word in text, word


def test_privacy_line_visible():
    assert "Do not include student names or student results" in section("us-builder")


def test_builder_ids():
    for el in ("us-mode-improve", "us-mode-new", "us-subject", "us-grade", "us-weeks", "us-lessons", "us-unit",
               "us-unit-label", "us-step", "us-decisions", "us-prompt", "us-copy", "us-hint"):
        assert f'id="{el}"' in html(), el
    assert int(re.search(r'id="us-unit"[^>]*maxlength="(\d+)"', html()).group(1)) >= 40000


def test_method_card_link():
    assert f'href="/{SLUG}/unit-studio-method-card-en.pdf"' in section("us-download")


def test_page_is_noindex():
    assert '<meta name="robots" content="noindex,nofollow">' in html()
    assert "rel=\"canonical\"" not in html()


def test_hidden_page_is_not_linked_anywhere():
    # Den dolda länken finns bara i Skool.
    for rel in ["sitemap.xml", "llms.txt", "pedagogy/index.html", "index.html", "robots.txt"]:
        assert SLUG not in (ROOT / rel).read_text(encoding="utf-8"), rel
    for p in (ROOT / "assets/partials").glob("*"):
        assert SLUG not in p.read_text(encoding="utf-8"), p.name


def test_scripts_loaded():
    assert '<script src="/assets/js/copy-to-clipboard.js" defer></script>' in html()
    assert '<script src="/assets/js/unit-studio.js" defer></script>' in html()


def test_committed_page_matches_a_fresh_build(tmp_path):
    shutil.copytree(ROOT / SLUG, tmp_path / SLUG)
    mod = load_build()
    mod.build(tmp_path)
    once = (tmp_path / SLUG / "index.html").read_bytes()
    assert once == PAGE.read_bytes()
    mod.build(tmp_path)
    assert (tmp_path / SLUG / "index.html").read_bytes() == once


def test_json_text_is_escaped():
    mod = load_build()
    step = {"id": "x", "num": 1, "name": "A <b>", "look_for": ["<i>q</i>?"], "why": "w & v", "brief": "b",
            "approach_ids": []}
    out = mod.render_step_card(step, {}, {})
    assert "<b>" not in out and "&lt;b&gt;" in out and "<i>q</i>" not in out
