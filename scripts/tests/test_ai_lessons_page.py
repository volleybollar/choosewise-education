"""Vakter för AI-lektionernas sidor (ett dolt spår per Skool-kurs).

Sidorna är bara för Skool-medlemmar: de nås via dolda länkar, har noindex
och får aldrig länkas från resten av sajten. Allt innehåll byggs från
track-en.json och lesson-en.json av scripts/build-ai-lessons.py.
Varje test går igenom alla spår och alla lektioner i dem.
"""
import importlib.util
import json
import re
import shutil
from html import escape
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
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


TRACKS = load("build_ai_lessons", "scripts/build-ai-lessons.py").TRACKS


def track(slug):
    return json.loads(read(ROOT / slug / "track-en.json"))


PAIRS = [(slug, entry["id"]) for slug in TRACKS for entry in track(slug)["lessons"]]


def overview(slug):
    return read(ROOT / slug / "index.html")


def lesson(slug, lid):
    return json.loads(read(ROOT / slug / lid / "lesson-en.json"))


def page(slug, lid):
    return read(ROOT / slug / lid / "index.html")


def lesson_url(slug, lid):
    return f"/{slug}/{lid}/"


def pdf_url(slug, lid):
    return lesson_url(slug, lid) + lesson(slug, lid)["student_pdf"]["file"]


def section(html, sid):
    m = re.search(rf'<section[^>]*id="{sid}".*?</section>', html, re.S)
    assert m, sid
    return m.group(0)


@pytest.mark.parametrize("slug", TRACKS)
def test_overview_has_required_sections(slug):
    for sid in OVERVIEW_SECTIONS:
        assert re.search(rf'<section[^>]*id="{sid}"', overview(slug)), sid


@pytest.mark.parametrize("slug,lid", PAIRS)
def test_lesson_page_has_required_sections(slug, lid):
    for sid in LESSON_SECTIONS:
        assert re.search(rf'<section[^>]*id="{sid}"', page(slug, lid)), sid


@pytest.mark.parametrize("slug,lid", [(slug, None) for slug in TRACKS] + PAIRS)
def test_ids_are_unique(slug, lid):
    html = overview(slug) if lid is None else page(slug, lid)
    ids = re.findall(r'\bid="([^"]+)"', html)
    assert len(ids) == len(set(ids)), sorted({i for i in ids if ids.count(i) > 1})


@pytest.mark.parametrize("slug,lid", PAIRS)
def test_overview_links_lesson_and_pdf(slug, lid):
    block = section(overview(slug), "al-lessons")
    assert f'href="{lesson_url(slug, lid)}"' in block
    assert f'href="{pdf_url(slug, lid)}"' in block


@pytest.mark.parametrize("slug", TRACKS)
def test_overview_lists_lessons_in_number_order(slug):
    """Per åldersband: korten står i nummerordning. Spår 2 har lektion 1–5 i
    både 13–15 och 16–19, så korten läses band för band."""
    chunks = re.split(r'<h3 class="al-band__title">', section(overview(slug), "al-lessons"))[1:]
    shown = {c.split("<", 1)[0]: [int(n) for n in re.findall(r'class="tm-move__num">Lesson (\d+)<', c)]
             for c in chunks}
    ids = [lid for s, lid in PAIRS if s == slug]
    for band in track(slug)["bands"]:
        numbers = [lesson(slug, lid)["number"] for lid in ids if lesson(slug, lid)["band"] == band["id"]]
        if numbers:
            assert shown[band["ages"]] == sorted(numbers), (band["id"], shown)


@pytest.mark.parametrize("slug,lid", PAIRS)
def test_lesson_page_links_back_and_to_pdf(slug, lid):
    assert f'href="/{slug}/"' in page(slug, lid)
    assert f'href="{pdf_url(slug, lid)}"' in section(page(slug, lid), "al-glance")


@pytest.mark.parametrize("slug,lid", PAIRS)
def test_materials_are_at_a_glance(slug, lid):
    """Specen: lektionen i korthet visar material; förberedelserna står under Before the lesson."""
    glance = section(page(slug, lid), "al-glance")
    for m in lesson(slug, lid)["materials"]:
        assert escape(m) in glance, m


@pytest.mark.parametrize("slug,lid", PAIRS)
def test_framework_line_links_both_frameworks(slug, lid):
    block = section(page(slug, lid), "al-frameworks")
    for f in track(slug)["frameworks"]:
        assert f'href="{escape(f["url"])}"' in block, f["name"]


@pytest.mark.parametrize("slug,lid", PAIRS)
def test_every_step_with_mode_and_minutes(slug, lid):
    steps = section(page(slug, lid), "al-steps")
    for s in lesson(slug, lid)["steps"]:
        assert escape(s["title"]) in steps, s["title"]
    assert len(re.findall(r'class="al-mode', steps)) == len(lesson(slug, lid)["steps"])


@pytest.mark.parametrize("slug,lid", PAIRS)
def test_steps_are_numbered(slug, lid):
    """Lärarsidan hänvisar till steg med nummer; stegen måste alltså synas numrerade."""
    items = re.findall(r'<li class="al-step.*?</li>', section(page(slug, lid), "al-steps"), re.S)
    assert len(items) == len(lesson(slug, lid)["steps"])
    for n, item in enumerate(items, start=1):
        assert f">Step {n}<" in item, n


@pytest.mark.parametrize("slug", TRACKS)
def test_overview_is_hidden(slug):
    hidden = load("build_seo_meta", "scripts/build-seo-meta.py").HIDDEN_PATHS
    assert f"/{slug}/" in hidden
    assert '<meta name="robots" content="noindex,nofollow">' in overview(slug)
    assert 'rel="canonical"' not in overview(slug)


@pytest.mark.parametrize("slug,lid", PAIRS)
def test_pages_are_hidden(slug, lid):
    hidden = load("build_seo_meta", "scripts/build-seo-meta.py").HIDDEN_PATHS
    assert lesson_url(slug, lid) in hidden
    assert '<meta name="robots" content="noindex,nofollow">' in page(slug, lid)
    assert 'rel="canonical"' not in page(slug, lid)


@pytest.mark.parametrize("slug", TRACKS)
def test_hidden_pages_are_not_linked_anywhere(slug):
    for rel in ["sitemap.xml", "llms.txt", "index.html", "pedagogy/index.html", "robots.txt"]:
        assert slug not in read(ROOT / rel), rel
    for p in (ROOT / "assets/partials").glob("*"):
        assert slug not in read(p), p.name


@pytest.mark.parametrize("slug", TRACKS)
def test_reader_note_and_use_rights_on_overview(slug):
    resources = section(overview(slug), "al-resources")
    assert escape(track(slug)["reader_note"]) in resources
    assert escape(track(slug)["use_rights"]) in resources


@pytest.mark.parametrize("slug,lid", PAIRS)
def test_reader_note_and_use_rights_on_pages(slug, lid):
    assert escape(track(slug)["reader_note"]) in section(page(slug, lid), "al-age")
    assert escape(track(slug)["use_rights"]) in section(page(slug, lid), "al-credits")


@pytest.mark.parametrize("slug,lid", PAIRS)
def test_age_section_fits_the_lesson(slug, lid):
    """Med verktyg: daterad tabell med just de verktygen. Utan: en rad som säger
    att lektionen inte använder något AI-verktyg, och ingen tom tabell."""
    age = section(page(slug, lid), "al-age")
    tools = track(slug)["age_limits"]["tools"]
    if lesson(slug, lid)["tools"]:
        assert "Checked 2026-11-11" in age
        for tid in lesson(slug, lid)["tools"]:
            assert escape(tools[tid]["name"]) in age, tid
    else:
        assert "This lesson uses no AI tool." in age
        assert "<table" not in age


@pytest.mark.parametrize("slug", TRACKS)
def test_overview_age_table_shows_checked_date(slug):
    assert "Checked 2026-11-11" in section(overview(slug), "al-resources")


@pytest.mark.parametrize("slug,lid", PAIRS)
def test_credits_are_linked(slug, lid):
    credits = section(page(slug, lid), "al-credits")
    for c in lesson(slug, lid)["credits"]:
        assert f'href="{escape(c["url"])}"' in credits and escape(c["text"]) in credits, c["text"]


def test_committed_pages_match_a_fresh_build(tmp_path):
    for slug in TRACKS:
        shutil.copytree(ROOT / slug, tmp_path / slug)
    mod = load("build_ai_lessons", "scripts/build-ai-lessons.py")
    paths = [f"{slug}/index.html" for slug in TRACKS] + [f"{slug}/{lid}/index.html" for slug, lid in PAIRS]
    mod.build(tmp_path)
    once = [(tmp_path / p).read_bytes() for p in paths]
    assert once == [(ROOT / p).read_bytes() for p in paths]
    mod.build(tmp_path)
    assert [(tmp_path / p).read_bytes() for p in paths] == once


@pytest.mark.parametrize("slug,lid", [(slug, None) for slug in TRACKS] + PAIRS)
def test_stylesheet_linked(slug, lid):
    html = overview(slug) if lid is None else page(slug, lid)
    assert '<link rel="stylesheet" href="/assets/css/ai-lessons.css?v=20261112a">' in html
    assert '<link rel="stylesheet" href="/assets/css/thinking-moves.css?v=20261029a">' in html
