"""Vakter för sidan Quality Ladder (/quality-ladder-ec1c2f8c/).

Sidan är bara för Skool-medlemmar: den nås via en dold länk och länkas aldrig
från resten av sajten. Exemplet, rutinen, mallarna, forskningen, varningarna och
åldersreglerna byggs från quality-ladder-ec1c2f8c/ladder-en.json av
scripts/build-quality-ladder.py, så att de syns utan JavaScript. Promptbyggaren
(formuläret) är statisk HTML här; logiken skrivs i assets/js/quality-ladder.js.
Det finns inget #ql-data-block: prompten behöver ingen data från JSON-filen.
Spec: docs/superpowers/specs/2026-11-14-what-teachers-do-design.md, del B.
"""
import importlib.util
import json
import re
import shutil
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SLUG = "quality-ladder-ec1c2f8c"
PAGE = ROOT / SLUG / "index.html"
DATA = ROOT / SLUG / "ladder-en.json"
BUILD = ROOT / "scripts/build-quality-ladder.py"
CSS = ROOT / "assets/css/quality-ladder.css"
LESSON_LENS = ROOT / "lesson-lens/index.html"

SECTIONS = ["ql-how", "ql-builder", "ql-lesson", "ql-feedback", "ql-policy", "ql-colleagues",
            "ql-evidence", "ql-care", "ql-age", "ql-next"]
MARKERS = ["hero-example", "routine", "whole-class", "policy", "colleagues", "evidence", "care", "age"]
LABEL_NAMES = {"strong": "Strong", "promising": "Promising", "framework": "Framework",
               "choosewise": "Choosewise"}
PRIVACY = ("Do not include student names or student work. "
           "The prompt only needs your task, criteria, subject and grade.")
HINT = "Fill in subject and the task to see your prompt."


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


def text_of(fragment):
    """Texten i ett HTML-stycke: taggar borta, tecken avkodade, blanksteg samlade."""
    no_tags = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", unescape(no_tags)).strip()


def load_build():
    spec = importlib.util.spec_from_file_location("build_quality_ladder", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def copy_button(fragment):
    """(data-copy, knapptext) för knappen som följs av en copy-toast."""
    m = re.search(r'<button[^>]*data-copy="([^"]*)"[^>]*>(.*?)</button>\s*<span class="copy-toast"',
                  fragment, re.S)
    assert m, "knappen ska ha en copy-toast direkt efter sig"
    return unescape(m.group(1)), m.group(2)


# ───── Sidans byggstenar ─────

def test_page_has_required_sections_in_order():
    ids = re.findall(r'<section[^>]*id="(ql-[a-z]+)"', html())
    assert ids == SECTIONS


def test_ids_are_unique():
    ids = re.findall(r'(?<![\w-])id="([^"]+)"', html())
    assert len(ids) == len(set(ids)), sorted({i for i in ids if ids.count(i) > 1})


def test_all_markers_present_in_pairs():
    page = html()
    for name in MARKERS:
        assert page.count(f"<!-- {name}:start -->") == 1, name
        assert page.count(f"<!-- {name}:end -->") == 1, name


def test_no_data_block():
    assert "ql-data" not in html()
    assert 'type="application/json"' not in html()


def test_hero():
    page = html()
    assert '<span class="eyebrow">For Choosewise members · All school stages</span>' in page
    assert "<h1>Quality Ladder</h1>" in page
    assert '<a class="tm-back" href="/what-teachers-do-354716b7/">← What teachers do</a>' in page
    assert ("Describe quality once, for the whole class. Your AI tool writes three made-up answers "
            "to your task at three levels. Students write their own first, rank the three against "
            "your criteria, and lift their own answer one level. No grading, and no student work "
            "in the AI.") in text_of(page)
    assert ">What a ladder looks like</h2>" in page
    assert page.index("<!-- hero-example:start -->") < page.index('id="ql-builder"')


def test_how_it_works_steps():
    block = section("ql-how")
    steps = re.search(r"<ol[^>]*>(.*?)</ol>", block, re.S).group(1)
    assert [text_of(s) for s in re.findall(r"<li>(.*?)</li>", steps, re.S)] == [
        "Enter the task and your criteria. Copy the prompt into your AI tool, and read the three "
        "samples before the lesson: check the facts and that the levels differ in what they do, "
        "not in length.",
        "In class, students write their own answer first, then rank Samples A, B and C and explain "
        "the differences with the criteria. Then you reveal the levels.",
        "Students lift their own answer one level. You give whole-class feedback instead of thirty "
        "separate comments.",
    ]


def test_privacy_line():
    assert PRIVACY in text_of(section("ql-builder"))


def test_builder_fields():
    b = section("ql-builder")
    assert 'onsubmit="return false"' in b

    def tag(tag_name, element_id):
        return re.search(rf'<{tag_name}[^>]*id="{element_id}"[^>]*>', b).group(0)

    subject = tag("input", "ql-subject")
    assert 'maxlength="60"' in subject and " required" in subject
    assert 'placeholder="e.g. History"' in subject and 'list="ql-subjects"' in subject
    own = re.findall(r'<option value="([^"]*)">', re.search(r'<datalist id="ql-subjects">(.*?)</datalist>', b, re.S).group(1))
    lens = LESSON_LENS.read_text(encoding="utf-8")
    theirs = re.findall(r'<option value="([^"]*)">', re.search(r'<datalist id="ll-subjects">(.*?)</datalist>', lens, re.S).group(1))
    assert own == theirs and len(own) >= 10

    grade = re.search(r'<select[^>]*id="ql-grade"[^>]*>(.*?)</select>', b, re.S).group(1)
    assert re.findall(r'<option value="(\d+)"[^>]*>Grade \1</option>', grade) == [str(n) for n in range(1, 13)]
    assert re.findall(r'<option value="(\d+)" selected>', grade) == ["8"]

    task = tag("textarea", "ql-task")
    assert 'maxlength="2000"' in task and 'rows="4"' in task and " required" in task
    assert ('placeholder="Why did the Industrial Revolution begin in Britain? '
            'Explain with at least two reasons."') in task

    criteria = tag("textarea", "ql-criteria")
    assert 'maxlength="800"' in criteria and 'rows="4"' in criteria and " required" not in criteria
    assert ('placeholder="Gives reasons&#10;Links each reason to an effect&#10;Uses evidence"') in criteria
    assert "Three to five work best. Leave it empty and the AI suggests criteria." in text_of(b)

    mistake = tag("input", "ql-mistake")
    assert 'maxlength="200"' in mistake and " required" not in mistake
    assert 'placeholder="e.g. lists causes without saying what each one led to"' in mistake

    length = re.search(r'<select[^>]*id="ql-length"[^>]*>(.*?)</select>', b, re.S).group(1)
    assert re.findall(r'<option value="([^"]*)"[^>]*>\1</option>', length) == [
        "A few sentences", "One paragraph", "Several paragraphs", "About a page"]
    assert re.findall(r'<option value="([^"]*)" selected>', length) == ["One paragraph"]

    second = tag("input", "ql-second")
    assert 'type="checkbox"' in second and " checked" in second

    language = tag("input", "ql-language")
    assert 'value="English"' in language and 'maxlength="40"' in language

    assert "readonly" in tag("textarea", "ql-prompt")
    assert f'<p class="tm-hint" id="ql-hint" aria-live="polite">{HINT}</p>' in b
    copy = tag("button", "ql-copy")
    assert 'data-copy=""' in copy and " disabled" in copy
    row = re.search(r'<div class="tm-copy-row">.*?</div>', b, re.S).group(0)
    assert 'id="ql-copy"' in row and 'id="ql-hint"' in row and 'class="copy-toast"' in row
    assert ">Copy prompt</button>" in row
    shown = text_of(b)
    for label in ("Subject", "Grade", "The task as students get it", "Criteria (optional)",
                  "A common mistake in this task (optional)", "Length of a strong answer",
                  "Add a second strong answer that solves the task differently",
                  "Language of the samples", "Your prompt — copy it into your AI tool"):
        assert label in shown, label


def test_form_has_id_for_the_script():
    assert re.search(r'<form[^>]*id="ql-builder-form"', section("ql-builder"))


# ───── Exemplet ─────

def test_example_rendered_in_letter_order():
    d = data()["example"]
    block = marker("hero-example")
    shown = text_of(block)
    assert "History · Grade 8" in shown
    assert escape(d["task"]) in block
    for criterion in d["criteria"]:
        assert escape(criterion) in block, criterion
    positions = [block.index(f"Sample {s['letter']}") for s in d["samples"]]
    assert positions == sorted(positions)
    for s in d["samples"]:
        assert escape(s["text"]) in block, s["letter"]
    assert [m for m in re.findall(r'class="ql-sample__title">Sample ([A-Z])<', block)] == ["A", "B", "C"]


def test_key_is_separate():
    d = data()["example"]
    block = marker("hero-example")
    m = re.search(r'<aside class="ql-key".*?</aside>', block, re.S)
    assert m, "nyckeln ska vara ett eget block"
    key = m.group(0)
    outside = block.replace(key, "")
    # Nyckeln kommer efter elevernas svar.
    assert block.index(key) > block.index("Sample C")
    # Nivåerna får bara synas i nyckeln.
    for level in ("weakest", "middle", "strongest"):
        assert level not in outside.lower(), level
        assert level in key.lower(), level
    assert "Teacher key" in text_of(key)
    for k in d["key"]:
        assert escape(k["note"]) in key, k["letter"]
        assert escape(k["up"]) in key, k["letter"]
    # Elevernas svar ligger inte i nyckeln.
    for s in d["samples"]:
        assert escape(s["text"]) not in key


# ───── Rutinen, mallen och policyn ─────

def test_routine_steps_and_copy():
    mod = load_build()
    d = data()["routine"]
    block = section("ql-lesson")
    assert ">The lesson, step by step</h2>" in block
    items = re.findall(r"<li>(.*?)</li>", block, re.S)
    assert items == [escape(s) for s in d["steps"]] and len(items) == 6
    assert re.search(r"<ol[^>]*>", block)
    assert escape(d["younger"]) in block
    assert escape(d["time"]) in block
    copied, label = copy_button(block)
    assert copied == mod.routine_text(d)
    assert label == "Copy text"
    assert '<a href="quality-ladder-routine.docx" download>Student sheet (.docx)</a>' in block


def test_whole_class_and_policy_copy():
    mod = load_build()
    d = data()
    feedback = section("ql-feedback")
    assert ">Whole-class feedback</h2>" in feedback
    assert escape(d["whole_class"]["intro"]) in feedback
    for s in d["whole_class"]["sections"]:
        assert escape(s["heading"]) in feedback and escape(s["guide"]) in feedback, s["heading"]
    assert escape(d["whole_class"]["followup"]) in feedback
    copied, label = copy_button(feedback)
    assert copied == mod.whole_class_text(d["whole_class"])
    assert label == "Copy template"
    assert '<a href="whole-class-feedback.docx" download>Whole-class feedback template (.docx)</a>' in feedback

    policy = section("ql-policy")
    assert "A one-page feedback policy" in policy
    assert escape(d["policy"]["intro"]) in policy
    for p in d["policy"]["principles"]:
        assert escape(p["title"]) in policy and escape(p["text"]) in policy, p["title"]
        if p["source"]:
            assert escape(p["source"]) in policy, p["title"]
    copied, label = copy_button(policy)
    assert copied == mod.policy_text(d["policy"])
    assert label == "Copy policy"
    assert '<a href="feedback-policy.docx" download>Feedback policy (.docx)</a>' in policy


def test_text_helpers_hold_all_the_content():
    """Hjälparna är enda källan till kopieringsknapparna och .docx-filerna: allt ska vara med."""
    mod = load_build()
    d = data()
    r = d["routine"]
    routine = mod.routine_text(r)
    for i, step in enumerate(r["steps"], start=1):
        assert f"{i}. {step}" in routine
    assert r["younger"] in routine
    for line in r["sheet"]:
        assert line in routine, line
    assert routine.index(r["steps"][-1]) < routine.index(r["younger"]) < routine.index(r["sheet"][0])
    w = d["whole_class"]
    wc = mod.whole_class_text(w)
    assert w["intro"] in wc and w["followup"] in wc
    for s in w["sections"]:
        assert s["heading"] in wc and s["guide"] in wc
    assert wc.index(w["intro"]) < wc.index(w["sections"][0]["heading"])
    pol = d["policy"]
    policy = mod.policy_text(pol)
    assert pol["intro"] in policy
    for p in pol["principles"]:
        assert p["title"] in policy and p["text"] in policy
    for text in (routine, wc, policy):
        assert "<" not in text and "&amp;" not in text


def test_framework_chip_on_template_and_policy():
    chip = '<span class="tm-chip tm-chip--framework">Framework</span>'
    for sid, name in (("ql-feedback", "whole-class"), ("ql-policy", "policy")):
        block = section(sid)
        assert chip in block, sid
        # Etiketten står överst, före det byggda innehållet.
        assert block.index(chip) < block.index(f"<!-- {name}:start -->"), sid


def test_data_copy_survives_a_real_parser():
    """Radbrytningar i data-copy ska överleva HTML-tolkaren."""
    mod = load_build()
    d = data()
    found = []

    class Grab(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == "button" and dict(attrs).get("data-copy"):
                found.append(dict(attrs)["data-copy"])

    for sid in ("ql-lesson", "ql-feedback", "ql-policy"):
        Grab().feed(section(sid))
    assert found == [mod.routine_text(d["routine"]), mod.whole_class_text(d["whole_class"]),
                     mod.policy_text(d["policy"])]


def test_downloads_linked():
    page = html()
    for name in ("quality-ladder-routine.docx", "whole-class-feedback.docx", "feedback-policy.docx"):
        assert re.search(rf'<a href="{re.escape(name)}" download>', page), name


def test_colleagues():
    block = section("ql-colleagues")
    assert ">Use the same samples with colleagues</h2>" in block
    assert escape(data()["colleagues"]) in block


# ───── Forskning, försiktighet och åldersregler ─────

def test_evidence_and_legend():
    d = data()
    block = section("ql-evidence")
    assert ">What the research says</h2>" in block
    assert ("Students judging work against criteria is well supported in school. Samples written by "
            "AI at three levels have not been tested yet.") in text_of(block)
    assert "Quality Ladder as a whole: Promising, with a Strong core." in text_of(block)
    assert block.index("Quality Ladder as a whole") < block.index("<!-- evidence:start -->")
    legend = re.search(r'<ul class="tm-legend">.*?</ul>', block, re.S).group(0)
    assert len(re.findall("<li>", legend)) == 4
    for key, name in LABEL_NAMES.items():
        assert (f'<span class="tm-chip tm-chip--{key}">{name}</span> '
                f'{escape(d["labels"][key]["definition"])}') in legend, key
    assert len(re.findall(r'class="ql-evidence__item"', block)) == 6
    items = block.split('class="ql-evidence__item"')[1:]
    for item, e in zip(items, d["evidence"]):
        assert f'<span class="tm-chip tm-chip--{e["label"]}">{LABEL_NAMES[e["label"]]}</span>' in item
        assert f"<strong>{escape(e['title'])}</strong>" in item
        assert escape(e["text"]) in item
        for s in e["sources"]:
            assert f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' in item, s["url"]


def test_care_section():
    block = section("ql-care")
    assert ">Watch out for</h2>" in block
    care = data()["care"]
    assert len(re.findall(r"<li>", block)) == 4
    for c in care:
        assert escape(c["risk"]) in block and escape(c["what_we_do"]) in block, c["risk"]


def test_age_rules():
    d = data()
    block = section("ql-age")
    shown = text_of(block)
    assert ("You use AI to prepare. Students need no AI for Quality Ladder. If students use AI "
            f"tools, these rules apply ({d['age_rules_date']}):") in shown
    for rule in d["age_rules"]:
        assert f"<li><strong>{escape(rule['tool'])}:</strong> {escape(rule['rule'])}</li>" in block, rule["tool"]
    assert ("Rules differ between countries and change often. Check your own national rules and "
            "your school policy before students use any AI tool.") in shown


def test_next_links():
    block = section("ql-next")
    assert ">Next</h2>" in block
    for href in ("/what-teachers-do-354716b7/", "/lesson-lens/", "/homework-upgrade-1f0cd17c/",
                 "https://www.skool.com/choosewise-7103"):
        assert f'href="{href}"' in block, href
    shown = text_of(block)
    for label in ("Back to the overview: What teachers do", "Feedback in a lesson plan: Lesson Lens",
                  "Checks after homework: Homework Upgrade"):
        assert label in shown, label


# ───── Sidan som helhet ─────

def test_page_head():
    page = html()
    assert "<title>Quality Ladder — Choosewise</title>" in page
    assert '<meta name="description" content="' in page
    assert '<link rel="stylesheet" href="/assets/css/quality-ladder.css?v=20261114a">' in page
    assert '<link rel="stylesheet" href="/assets/css/thinking-moves.css?v=20261029a">' in page


def test_noindex():
    assert '<meta name="robots" content="noindex,nofollow">' in html()
    assert 'rel="canonical"' not in html()
    assert "og:image" not in html()


def test_hidden_page_is_not_linked_anywhere():
    for rel in ["sitemap.xml", "llms.txt", "index.html", "robots.txt", "study/index.html",
                "pedagogy/index.html", "think/index.html"]:
        assert SLUG not in (ROOT / rel).read_text(encoding="utf-8"), rel
    for p in (ROOT / "assets/partials").glob("*"):
        assert SLUG not in p.read_text(encoding="utf-8"), p.name


def test_scripts_loaded():
    page = html()
    assert '<script src="/assets/js/copy-to-clipboard.js" defer></script>' in page
    assert '<script src="/assets/js/quality-ladder.js" defer></script>' in page


def test_json_text_is_escaped():
    mod = load_build()
    out = mod.render_care([{"risk": "A <b>", "what_we_do": "i & j"}])
    assert "<b>" not in out and "&lt;b&gt;" in out and "i &amp; j" in out
    out = mod.render_colleagues("x <i>y</i> & z")
    assert "<i>" not in out and "&lt;i&gt;" in out and "&amp; z" in out
    labels = data()["labels"]
    out = mod.render_evidence([{"title": "T <b>", "text": "a & b", "label": "strong",
                                "sources": [{"text": "s <i>", "url": "https://x?a=1&b=2"}]}], labels)
    assert "<b>" not in out and "<i>" not in out and "a &amp; b" in out and "a=1&amp;b=2" in out
    policy = {"intro": "i <b>", "principles": [{"title": "t & u", "text": "<x>", "source": "s <y>"}]}
    out = mod.render_policy(policy)
    assert "<b>" not in out and "<x>" not in out and "t &amp; u" in out


def test_committed_page_matches_a_fresh_build(tmp_path):
    shutil.copytree(ROOT / SLUG, tmp_path / SLUG)
    mod = load_build()
    mod.build(tmp_path)
    once = (tmp_path / SLUG / "index.html").read_bytes()
    assert once == PAGE.read_bytes()
    mod.build(tmp_path)
    assert (tmp_path / SLUG / "index.html").read_bytes() == once


def test_missing_marker_raises():
    mod = load_build()
    with pytest.raises(ValueError):
        mod._inject("<p></p>", "routine", "x")


def test_swedish_comments():
    """Varje sektion har minst en kommentar (utöver markörerna) som förklarar den."""
    page = html()
    for sid in SECTIONS:
        start = page.index(f'id="{sid}"')
        before = page[:start]
        # Kommentaren står rakt före sektionen: hitta den sista <section> före och titta efter den.
        prev = before.rfind("</section>")
        gap = before[prev if prev != -1 else 0:]
        comments = re.findall(r"<!--(.*?)-->", gap, re.S)
        explaining = [c for c in comments if not re.match(r"\s*[a-z-]+:(start|end)\b", c)]
        assert explaining, sid


def test_font_weights_only_from_tokens():
    css = CSS.read_text(encoding="utf-8")
    assert not re.search(r"font-weight:\s*\d", css)
