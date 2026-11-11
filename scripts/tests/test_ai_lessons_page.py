"""Vakter för AI-lektionernas sidor (/ai-lessons-younger-3c514a93/).

Sidorna är bara för Skool-medlemmar: de nås via dolda länkar, har noindex
och får aldrig länkas från resten av sajten. Allt innehåll byggs från
track-en.json och lesson-en.json av scripts/build-ai-lessons.py.
"""
import importlib.util
import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLUG = "ai-lessons-younger-3c514a93"
LESSON = "word-guessing-machine"
OVERVIEW = ROOT / SLUG / "index.html"
PAGE = ROOT / SLUG / LESSON / "index.html"
OVERVIEW_SECTIONS = ["al-hero", "al-objectives", "al-threads", "al-lessons", "al-how", "al-need", "al-resources"]
LESSON_SECTIONS = ["al-glance", "al-goals", "al-before", "al-steps", "al-gather", "al-adapt", "al-closing",
                   "al-language", "al-background", "al-frameworks", "al-age", "al-credits"]
LESSON_URL = f"/{SLUG}/{LESSON}/"
PDF_URL = f"/{SLUG}/{LESSON}/word-guessing-machine-student-en.pdf"


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read(path):
    return path.read_text(encoding="utf-8")


def track():
    return json.loads(read(ROOT / SLUG / "track-en.json"))


def lesson():
    return json.loads(read(ROOT / SLUG / LESSON / "lesson-en.json"))


def section(html, sid):
    m = re.search(rf'<section[^>]*id="{sid}".*?</section>', html, re.S)
    assert m, sid
    return m.group(0)


def test_pages_have_required_sections():
    for path, ids in ((OVERVIEW, OVERVIEW_SECTIONS), (PAGE, LESSON_SECTIONS)):
        for sid in ids:
            assert re.search(rf'<section[^>]*id="{sid}"', read(path)), (path.parent.name, sid)


def test_ids_are_unique():
    for path in (OVERVIEW, PAGE):
        ids = re.findall(r'\bid="([^"]+)"', read(path))
        assert len(ids) == len(set(ids)), sorted({i for i in ids if ids.count(i) > 1})


def test_overview_links_lesson_and_pdf():
    block = section(read(OVERVIEW), "al-lessons")
    assert f'href="{LESSON_URL}"' in block
    assert f'href="{PDF_URL}"' in block


def test_lesson_page_links_back_and_to_pdf():
    html = read(PAGE)
    assert f'href="/{SLUG}/"' in html
    assert f'href="{PDF_URL}"' in section(html, "al-glance")


def test_materials_are_at_a_glance():
    """Specen: lektionen i korthet visar material; förberedelserna står under Before the lesson."""
    glance = section(read(PAGE), "al-glance")
    for m in lesson()["materials"]:
        assert escape(m) in glance, m


def test_framework_line_links_both_frameworks():
    block = section(read(PAGE), "al-frameworks")
    for f in track()["frameworks"]:
        assert f'href="{escape(f["url"])}"' in block, f["name"]


def test_every_step_with_mode_and_minutes():
    steps = section(read(PAGE), "al-steps")
    for s in lesson()["steps"]:
        assert escape(s["title"]) in steps, s["title"]
    assert len(re.findall(r'class="al-mode', steps)) == len(lesson()["steps"])


def test_pages_are_hidden():
    hidden = load("build_seo_meta", "scripts/build-seo-meta.py").HIDDEN_PATHS
    assert f"/{SLUG}/" in hidden and LESSON_URL in hidden
    for path in (OVERVIEW, PAGE):
        assert '<meta name="robots" content="noindex,nofollow">' in read(path)
        assert 'rel="canonical"' not in read(path)


def test_hidden_pages_are_not_linked_anywhere():
    for rel in ["sitemap.xml", "llms.txt", "index.html", "pedagogy/index.html", "robots.txt"]:
        assert SLUG not in read(ROOT / rel), rel
    for p in (ROOT / "assets/partials").glob("*"):
        assert SLUG not in read(p), p.name


def test_reader_note_and_use_rights_on_pages():
    note, rights = escape(track()["reader_note"]), escape(track()["use_rights"])
    assert note in section(read(OVERVIEW), "al-resources")
    assert rights in section(read(OVERVIEW), "al-resources")
    assert note in section(read(PAGE), "al-age")
    assert rights in section(read(PAGE), "al-credits")


def test_age_table_shows_checked_date():
    assert "Checked 2026-11-11" in section(read(OVERVIEW), "al-resources")
    age = section(read(PAGE), "al-age")
    assert "Checked 2026-11-11" in age
    tools = track()["age_limits"]["tools"]
    for tid in lesson()["tools"]:
        assert escape(tools[tid]["name"]) in age, tid


def test_committed_pages_match_a_fresh_build(tmp_path):
    shutil.copytree(ROOT / SLUG, tmp_path / SLUG)
    mod = load("build_ai_lessons", "scripts/build-ai-lessons.py")
    mod.build(tmp_path)
    once = [(tmp_path / SLUG / "index.html").read_bytes(), (tmp_path / SLUG / LESSON / "index.html").read_bytes()]
    assert once == [OVERVIEW.read_bytes(), PAGE.read_bytes()]
    mod.build(tmp_path)
    assert [(tmp_path / SLUG / "index.html").read_bytes(), (tmp_path / SLUG / LESSON / "index.html").read_bytes()] == once


def test_stylesheet_linked():
    for path in (OVERVIEW, PAGE):
        assert '<link rel="stylesheet" href="/assets/css/ai-lessons.css?v=20261111a">' in read(path)
        assert '<link rel="stylesheet" href="/assets/css/thinking-moves.css?v=20261029a">' in read(path)
