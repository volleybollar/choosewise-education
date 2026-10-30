"""Vakter för Pedagogy Compass-sidan (/pedagogy-compass-59ecb8db/).

Sidan är bara för Skool-medlemmar: den nås via en dold länk, har noindex
och får aldrig länkas från resten av sajten (Johans beslut 2026-10-30).
Allt innehåll byggs från compass-en.json av scripts/build-pedagogy-compass.py.
"""
import importlib.util
import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLUG = "pedagogy-compass-59ecb8db"
PAGE = ROOT / SLUG / "index.html"
DATA = ROOT / SLUG / "compass-en.json"
BUILD = ROOT / "scripts/build-pedagogy-compass.py"
SECTIONS = ["pc-problems", "pc-builder", "pc-map", "pc-recipes", "pc-myths", "pc-age", "pc-download"]


def html():
    return PAGE.read_text(encoding="utf-8")


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def section(sid):
    m = re.search(rf'<section[^>]*id="{sid}".*?</section>', html(), re.S)
    assert m, sid
    return m.group(0)


def load_build():
    spec = importlib.util.spec_from_file_location("build_pedagogy_compass", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_page_has_required_sections():
    for sid in SECTIONS:
        assert re.search(rf'<section[^>]*id="{sid}"', html()), sid


def test_ids_are_unique():
    ids = re.findall(r'\bid="([^"]+)"', html())
    assert len(ids) == len(set(ids)), sorted({i for i in ids if ids.count(i) > 1})


def test_every_problem_with_its_models_and_link():
    block = section("pc-problems")
    names = {m["id"]: m["name"] for m in data()["models"]}
    for p in data()["problems"]:
        assert escape(p["name"]) in block, p["id"]
        for mid in p["model_ids"]:
            assert f'href="#model-{mid}"' in block, (p["id"], mid)
            assert escape(names[mid]) in block
        assert f'data-use-problem="{p["id"]}"' in block


def test_every_model_card_once():
    for m in data()["models"]:
        assert html().count(f'id="model-{m["id"]}"') == 1, m["id"]
    myths = section("pc-myths")
    for m in data()["models"]:
        if m["category"] == "contested":
            assert f'id="model-{m["id"]}"' in myths, m["id"]


def test_map_has_categories_a_to_e():
    block = section("pc-map")
    for c in data()["categories"][:5]:
        assert escape(c["question"]) in block, c["id"]


def test_recipes_rendered():
    block = section("pc-recipes")
    for r in data()["recipes"]:
        assert escape(r["name"]) in block
        for s in r["steps"]:
            assert escape(s) in block


def test_data_block_for_the_builder():
    m = re.search(r'<script type="application/json" id="pc-data">(.*?)</script>', html(), re.S)
    assert m
    d = json.loads(m.group(1))
    assert [p["id"] for p in d["problems"]] == [p["id"] for p in data()["problems"]]
    assert {x["id"] for x in d["models"]} == {x["id"] for x in data()["models"]}


def test_age_section_has_reader_note():
    text = section("pc-age")
    for word in ("Copilot Chat", "Gemini", "ChatGPT", "Claude", "national", "school policy"):
        assert word in text, word


def test_privacy_line_visible():
    assert "Do not include student names or student results" in section("pc-builder")


def test_builder_ids():
    for el in ("pc-problem", "pc-own", "pc-subject", "pc-grade", "pc-situation", "pc-models", "pc-prompt", "pc-copy", "pc-hint"):
        assert f'id="{el}"' in html(), el


def test_poster_link():
    assert f'href="/{SLUG}/pedagogy-compass-poster-en.pdf"' in section("pc-download")


def test_page_is_noindex():
    assert '<meta name="robots" content="noindex,nofollow">' in html()
    assert 'rel="canonical"' not in html()


def test_hidden_page_is_not_linked_anywhere():
    for rel in ["sitemap.xml", "llms.txt", "pedagogy/index.html", "index.html", "robots.txt"]:
        assert SLUG not in (ROOT / rel).read_text(encoding="utf-8"), rel
    for p in (ROOT / "assets/partials").glob("*"):
        assert SLUG not in p.read_text(encoding="utf-8"), p.name


def test_scripts_loaded():
    assert '<script src="/assets/js/copy-to-clipboard.js" defer></script>' in html()
    assert '<script src="/assets/js/pedagogy-compass.js" defer></script>' in html()


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
    m = {"id": "x", "name": "A <b>", "origin": "o", "category": "strong", "one_liner": "<i>1</i>", "tuesday": "t",
         "ai_helps": "h", "ai_harms": "a", "evidence": "e & f", "sources": [{"text": "s", "url": "https://x"}]}
    out = mod.render_model_card(m, data()["labels"])
    assert "<b>" not in out and "&lt;b&gt;" in out and "<i>1</i>" not in out
