"""Vakter för byggskriptet till AI-lektionerna (scripts/build-ai-lessons.py).

Skriptet bygger översiktssidan och varje lärarsida i sin helhet ur JSON och
behåller blocket som build-seo-meta.py äger, så att de två skripten kan köras
i vilken ordning som helst utan att sidorna ändras.
"""
import copy
import importlib.util
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLUG = "ai-lessons-younger-3c514a93"
SEO_START = "<!-- seo:start (build-seo-meta.py) -->"


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_mod():
    return load("build_ai_lessons", "scripts/build-ai-lessons.py")


def track():
    return build_mod().load_track(ROOT, SLUG)


def section(html, sid):
    m = re.search(rf'<section[^>]*id="{sid}".*?</section>', html, re.S)
    assert m, sid
    return m.group(0)


def test_keep_seo_block_moves_block_before_head():
    seo = load("build_seo_meta", "scripts/build-seo-meta.py")
    block = f'{SEO_START}\n<meta name="robots" content="noindex,nofollow">\n<!-- seo:end -->'
    old = f"<html><head>\n<title>old</title>\n{block}\n</head><body></body></html>"
    new = "<html><head>\n<title>new</title>\n  <!-- note -->\n</head><body></body></html>"
    out = build_mod().keep_seo_block(old, new)
    assert out.count(SEO_START) == 1
    assert block + "\n</head>" in out
    assert out == seo.inject_head(new, block)  # samma bytes som build-seo-meta.py ger


def test_keep_seo_block_without_old():
    new = "<html><head><title>x</title></head></html>"
    assert build_mod().keep_seo_block(None, new) == new
    assert build_mod().keep_seo_block("<html><head></head></html>", new) == new


def test_render_escapes_text():
    t = track()
    lesson = copy.deepcopy(t["lesson_data"][0])
    lesson["steps"][0]["title"] = "<b>bold</b>"
    out = build_mod().render_lesson(t, lesson)
    assert "<b>bold</b>" not in out
    assert "&lt;b&gt;bold&lt;/b&gt;" in section(out, "al-steps")


def test_overview_hides_empty_bands():
    t = track()
    assert all(lesson["band"] != "5-8" for lesson in t["lesson_data"])
    out = build_mod().render_overview(t)
    assert "Ages 5–8" not in section(out, "al-lessons")
    assert "Ages 9–12" in section(out, "al-lessons")


def test_overview_counts_built_lessons():
    mod = build_mod()
    t = track()
    pattern = r'al-stat__label">Lessons</span><strong class="al-stat__value">(\d+)<'
    assert re.search(pattern, mod.render_overview(t)).group(1) == str(len(t["lesson_data"]))
    two = copy.deepcopy(t)
    extra = copy.deepcopy(two["lesson_data"][0])
    extra["id"] = "another-lesson"
    two["lesson_data"].append(extra)
    assert re.search(pattern, mod.render_overview(two)).group(1) == "2"


def test_demo_fallback_rendered():
    t = track()
    lesson = t["lesson_data"][0]
    steps = section(build_mod().render_lesson(t, lesson), "al-steps")
    demo = next(s for s in lesson["steps"] if s.get("demo"))
    assert escape(demo["fallback"]) in steps
    for prompt in demo["prompts"]:
        assert escape(prompt) in steps
