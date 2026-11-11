"""Vakter för AI-lektionernas sidor (/ai-lessons-younger-3c514a93/).

Sidorna är bara för Skool-medlemmar: de nås via dolda länkar, har noindex
och får aldrig länkas från resten av sajten. Allt innehåll byggs från
track-en.json och lesson-en.json av scripts/build-ai-lessons.py.
Varje test går igenom alla lektioner i spåret.
"""
import importlib.util
import json
import re
import shutil
from html import escape
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SLUG = "ai-lessons-younger-3c514a93"
OVERVIEW = ROOT / SLUG / "index.html"
OVERVIEW_SECTIONS = ["al-hero", "al-objectives", "al-threads", "al-lessons", "al-how", "al-need", "al-resources"]
LESSON_SECTIONS = ["al-glance", "al-goals", "al-before", "al-steps", "al-gather", "al-adapt", "al-closing",
                   "al-language", "al-background", "al-frameworks", "al-age", "al-credits"]


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read(path):
    return path.read_text(encoding="utf-8")


def track():
    return json.loads(read(ROOT / SLUG / "track-en.json"))


IDS = [entry["id"] for entry in track()["lessons"]]


def lesson(lid):
    return json.loads(read(ROOT / SLUG / lid / "lesson-en.json"))


def page(lid):
    return read(ROOT / SLUG / lid / "index.html")


def lesson_url(lid):
    return f"/{SLUG}/{lid}/"


def pdf_url(lid):
    return lesson_url(lid) + lesson(lid)["student_pdf"]["file"]


def section(html, sid):
    m = re.search(rf'<section[^>]*id="{sid}".*?</section>', html, re.S)
    assert m, sid
    return m.group(0)


def test_overview_has_required_sections():
    for sid in OVERVIEW_SECTIONS:
        assert re.search(rf'<section[^>]*id="{sid}"', read(OVERVIEW)), sid


@pytest.mark.parametrize("lid", IDS)
def test_lesson_page_has_required_sections(lid):
    for sid in LESSON_SECTIONS:
        assert re.search(rf'<section[^>]*id="{sid}"', page(lid)), sid


@pytest.mark.parametrize("lid", [None] + IDS)
def test_ids_are_unique(lid):
    html = read(OVERVIEW) if lid is None else page(lid)
    ids = re.findall(r'\bid="([^"]+)"', html)
    assert len(ids) == len(set(ids)), sorted({i for i in ids if ids.count(i) > 1})


@pytest.mark.parametrize("lid", IDS)
def test_overview_links_lesson_and_pdf(lid):
    block = section(read(OVERVIEW), "al-lessons")
    assert f'href="{lesson_url(lid)}"' in block
    assert f'href="{pdf_url(lid)}"' in block


def test_overview_lists_lessons_in_number_order():
    block = section(read(OVERVIEW), "al-lessons")
    for band in track()["bands"]:
        numbers = [lesson(lid)["number"] for lid in IDS if lesson(lid)["band"] == band["id"]]
        shown = [int(n) for n in re.findall(r'class="tm-move__num">Lesson (\d+)<', block)]
        in_band = [n for n in shown if n in numbers]
        assert in_band == sorted(numbers), (band["id"], in_band)


@pytest.mark.parametrize("lid", IDS)
def test_lesson_page_links_back_and_to_pdf(lid):
    assert f'href="/{SLUG}/"' in page(lid)
    assert f'href="{pdf_url(lid)}"' in section(page(lid), "al-glance")


@pytest.mark.parametrize("lid", IDS)
def test_materials_are_at_a_glance(lid):
    """Specen: lektionen i korthet visar material; förberedelserna står under Before the lesson."""
    glance = section(page(lid), "al-glance")
    for m in lesson(lid)["materials"]:
        assert escape(m) in glance, m


@pytest.mark.parametrize("lid", IDS)
def test_framework_line_links_both_frameworks(lid):
    block = section(page(lid), "al-frameworks")
    for f in track()["frameworks"]:
        assert f'href="{escape(f["url"])}"' in block, f["name"]


@pytest.mark.parametrize("lid", IDS)
def test_every_step_with_mode_and_minutes(lid):
    steps = section(page(lid), "al-steps")
    for s in lesson(lid)["steps"]:
        assert escape(s["title"]) in steps, s["title"]
    assert len(re.findall(r'class="al-mode', steps)) == len(lesson(lid)["steps"])


@pytest.mark.parametrize("lid", IDS)
def test_steps_are_numbered(lid):
    """Lärarsidan hänvisar till steg med nummer; stegen måste alltså synas numrerade."""
    items = re.findall(r'<li class="al-step.*?</li>', section(page(lid), "al-steps"), re.S)
    assert len(items) == len(lesson(lid)["steps"])
    for n, item in enumerate(items, start=1):
        assert f">Step {n}<" in item, n


@pytest.mark.parametrize("lid", IDS)
def test_pages_are_hidden(lid):
    hidden = load("build_seo_meta", "scripts/build-seo-meta.py").HIDDEN_PATHS
    assert f"/{SLUG}/" in hidden and lesson_url(lid) in hidden
    for html in (read(OVERVIEW), page(lid)):
        assert '<meta name="robots" content="noindex,nofollow">' in html
        assert 'rel="canonical"' not in html


def test_hidden_pages_are_not_linked_anywhere():
    for rel in ["sitemap.xml", "llms.txt", "index.html", "pedagogy/index.html", "robots.txt"]:
        assert SLUG not in read(ROOT / rel), rel
    for p in (ROOT / "assets/partials").glob("*"):
        assert SLUG not in read(p), p.name


@pytest.mark.parametrize("lid", IDS)
def test_reader_note_and_use_rights_on_pages(lid):
    note, rights = escape(track()["reader_note"]), escape(track()["use_rights"])
    assert note in section(read(OVERVIEW), "al-resources")
    assert rights in section(read(OVERVIEW), "al-resources")
    assert note in section(page(lid), "al-age")
    assert rights in section(page(lid), "al-credits")


@pytest.mark.parametrize("lid", IDS)
def test_age_section_fits_the_lesson(lid):
    """Med verktyg: daterad tabell med just de verktygen. Utan: en rad som säger
    att lektionen inte använder något AI-verktyg, och ingen tom tabell."""
    age = section(page(lid), "al-age")
    tools = track()["age_limits"]["tools"]
    if lesson(lid)["tools"]:
        assert "Checked 2026-11-11" in age
        for tid in lesson(lid)["tools"]:
            assert escape(tools[tid]["name"]) in age, tid
    else:
        assert "This lesson uses no AI tool." in age
        assert "<table" not in age


def test_overview_age_table_shows_checked_date():
    assert "Checked 2026-11-11" in section(read(OVERVIEW), "al-resources")


@pytest.mark.parametrize("lid", IDS)
def test_credits_are_linked(lid):
    credits = section(page(lid), "al-credits")
    for c in lesson(lid)["credits"]:
        assert f'href="{escape(c["url"])}"' in credits and escape(c["text"]) in credits, c["text"]


def test_committed_pages_match_a_fresh_build(tmp_path):
    shutil.copytree(ROOT / SLUG, tmp_path / SLUG)
    mod = load("build_ai_lessons", "scripts/build-ai-lessons.py")
    paths = ["index.html"] + [f"{lid}/index.html" for lid in IDS]
    mod.build(tmp_path)
    once = [(tmp_path / SLUG / p).read_bytes() for p in paths]
    assert once == [(ROOT / SLUG / p).read_bytes() for p in paths]
    mod.build(tmp_path)
    assert [(tmp_path / SLUG / p).read_bytes() for p in paths] == once


@pytest.mark.parametrize("lid", [None] + IDS)
def test_stylesheet_linked(lid):
    html = read(OVERVIEW) if lid is None else page(lid)
    assert '<link rel="stylesheet" href="/assets/css/ai-lessons.css?v=20261111a">' in html
    assert '<link rel="stylesheet" href="/assets/css/thinking-moves.css?v=20261029a">' in html
