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
OLDER = "ai-lessons-older-319cf15d"
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
    t = copy.deepcopy(track())  # 5–8 har lektioner sedan 2026-11-12; tomt band skapas här
    t["lesson_data"] = [lesson for lesson in t["lesson_data"] if lesson["band"] != "5-8"]
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
    assert re.search(pattern, mod.render_overview(two)).group(1) == str(len(t["lesson_data"]) + 1)


def test_demo_fallback_rendered():
    t = track()
    lesson = next(x for x in t["lesson_data"] if x["ai_use"] == "teacher-demo")
    steps = section(build_mod().render_lesson(t, lesson), "al-steps")
    demo = next(s for s in lesson["steps"] if s.get("demo"))
    assert escape(demo["fallback"]) in steps
    assert "If the demo does not go as planned:" in steps  # etiketten passar alla lektioners demo
    for prompt in demo["prompts"]:
        assert escape(prompt) in steps


def test_overview_shows_only_bands_with_lessons():
    """Ett åldersband syns på översikten när det har sin första lektion, inte före."""
    mod = build_mod()
    for slug in mod.TRACKS:
        t = mod.load_track(ROOT, slug)
        shown = section(mod.render_overview(t), "al-lessons")
        with_lessons = {entry["band"] for entry in t["lessons"]}
        for band in t["bands"]:
            assert (escape(band["ages"]) in shown) == (band["id"] in with_lessons), (slug, band["id"])


def test_student_ai_step_shows_the_path_without_ai():
    t = build_mod().load_track(ROOT, OLDER)
    lesson = copy.deepcopy(t["lesson_data"][0])
    lesson["steps"][0].update(student_ai=True, without_ai="Use the <saved> answer.", prompts=["Ask me one question."])
    steps = section(build_mod().render_lesson(t, lesson), "al-steps")
    assert steps.count('class="al-step al-step--ai"') == 1
    assert "<strong>Without AI:</strong> " + escape("Use the <saved> answer.") in steps
    assert escape("Ask me one question.") in steps
    assert ".al-step--ai" in (ROOT / "assets/css/ai-lessons.css").read_text(encoding="utf-8")


def test_optional_ai_use_has_a_label():
    assert build_mod().AI_USE["optional"] == "Optional for students"


def test_overview_shows_the_tracks_ai_use_note():
    """Resurserna säger vad eleverna i just det spåret behöver; spår 2 ärver
    inte spår 1:s "never use AI themselves"."""
    mod = build_mod()
    for slug in mod.TRACKS:
        t = mod.load_track(ROOT, slug)
        assert escape(t["ai_use_note"]) in section(mod.render_overview(t), "al-resources"), slug
    older = mod.render_overview(mod.load_track(ROOT, OLDER))
    assert "never use AI" not in section(older, "al-resources")


def test_demo_prompts_in_order_are_numbered():
    """Lektioner som hänvisar till prompt 1, 2, 3 visar dem numrerade; andra
    behåller "pick one" (spår 1 oförändrat)."""
    t = track()
    lesson = copy.deepcopy(next(x for x in t["lesson_data"] if x["ai_use"] == "teacher-demo"))
    demo = next(s for s in lesson["steps"] if s.get("demo"))
    demo.pop("prompts_in_order", None)
    assert "Prompts to try (pick one)" in section(build_mod().render_lesson(t, lesson), "al-steps")
    demo["prompts_in_order"] = True
    steps = section(build_mod().render_lesson(t, lesson), "al-steps")
    assert "pick one" not in steps and "Prompts, in order" in steps
    for n in range(1, len(demo["prompts"]) + 1):
        assert f"Prompt {n}" in steps, n
