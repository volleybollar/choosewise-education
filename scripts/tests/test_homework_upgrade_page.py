"""Vakter för sidan Homework Upgrade (/homework-upgrade-1f0cd17c/).

Sidan är bara för Skool-medlemmar: den nås via en dold länk och länkas aldrig
från resten av sajten. Exemplet, de tolv mönsterkorten, kontrollen, elevtexten,
forskningen och åldersreglerna byggs från homework-upgrade-1f0cd17c/upgrade-en.json
av scripts/build-homework-upgrade.py, så att de syns utan JavaScript. Testerna
läser den byggda sidan och kör byggskriptet. (Noindex, sitemap och att sidan
inte länkas från sajten vaktas i uppgift 3.)
Spec: docs/superpowers/specs/2026-11-14-homework-upgrade-design.md.
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
SLUG = "homework-upgrade-1f0cd17c"
PAGE = ROOT / SLUG / "index.html"
DATA = ROOT / SLUG / "upgrade-en.json"
BUILD = ROOT / "scripts/build-homework-upgrade.py"
CSS = ROOT / "assets/css/homework-upgrade.css"
LESSON_LENS = ROOT / "lesson-lens/index.html"

SECTIONS = ["hu-how", "hu-builder", "hu-patterns", "hu-check", "hu-students", "hu-clinic",
            "hu-evidence", "hu-age", "hu-next"]
# Etikettens visningsnamn per nyckel (labels i JSON-filen).
LABEL_NAMES = {"strong": "Strong", "promising": "Promising", "choosewise": "Choosewise"}
PRIVACY = ("Do not include student names or student work. "
           "The prompt only needs your subject, grade and the homework.")
HINT = "Fill in subject and the homework to see your prompt."


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


def card(pattern_id):
    m = re.search(rf'<article class="tm-move hu-pattern" id="{pattern_id}".*?</article>', html(), re.S)
    assert m, pattern_id
    return m.group(0)


def load_build():
    spec = importlib.util.spec_from_file_location("build_homework_upgrade", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_page_has_required_sections():
    ids = re.findall(r'<section[^>]*id="(hu-[a-z]+)"', html())
    assert ids == SECTIONS


def test_ids_are_unique():
    # (?<![\w-]): data-pattern-id="…" är ett attribut, inte ett id.
    ids = re.findall(r'(?<![\w-])id="([^"]+)"', html())
    assert len(ids) == len(set(ids)), sorted({i for i in ids if ids.count(i) > 1})


def test_hero_example_before_builder():
    page = html()
    d = data()
    ex = d["example"]
    block = marker("hero-example")
    assert "What an upgrade looks like" in page
    assert "History · Grade 8 · Answer from memory first · 20 minutes" in text_of(block)
    for line in ex["homework"] + [ex["keep"]] + ex["ai_risk"]:
        assert escape(line) in block, line
    upgrade = re.search(r"<dt>Upgrade</dt><dd><ol[^>]*>(.*?)</ol>", block, re.S).group(1)
    assert re.findall(r"<li>(.*?)</li>", upgrade, re.S) == [escape(s) for s in ex["upgrade"]]
    shown = text_of(block)
    for i, item in enumerate(ex["check"], start=1):
        assert f"Q{i}: {item['q']}" in shown, i
        assert f"A{i}: {item['a']}" in shown, i
    assert page.index("<!-- hero-example:start -->") < page.index('id="hu-builder"')


def test_twelve_cards_in_order():
    d = data()
    ids = re.findall(r'<article class="tm-move hu-pattern" id="([^"]+)" data-pattern-id="\1"', html())
    assert ids == [p["id"] for p in d["patterns"]]
    for p in d["patterns"]:
        c = card(p["id"])
        shown = text_of(c)
        assert f"Pattern {p['number']}" in shown, p["id"]
        assert re.search(rf'<h4 class="tm-move__name">{re.escape(escape(p["name"]))}</h4>', c), p["id"]
        assert f"Instead of: {p['instead']}" in shown, p["id"]
        assert f"Check next lesson: {p['check']}" in shown, p["id"]
        assert f"If a chatbot does it: {p['chatbot']}" in shown, p["id"]
        assert re.search(rf'class="tm-chip tm-chip--{p["label"]}">{LABEL_NAMES[p["label"]]}<', c), p["id"]
        steps = re.search(r"<ol[^>]*>(.*?)</ol>", c, re.S).group(1)
        assert re.findall(r"<li>(.*?)</li>", steps, re.S) == [escape(s) for s in p["steps"]], p["id"]
        assert f'href="?pattern={p["id"]}#hu-builder"' in c, p["id"]
        assert f'data-use-pattern="{p["id"]}"' in c, p["id"]
        assert f'aria-label="Use this pattern: {escape(p["name"])}"' in c, p["id"]
        assert ">Use this pattern</a>" in c, p["id"]


def test_card_details_hold_why_tip_and_sources():
    for p in data()["patterns"]:
        details = re.search(r"<details.*?</details>", card(p["id"]), re.S).group(0)
        assert "<summary>Why it works</summary>" in details, p["id"]
        assert escape(p["why"]) in details, p["id"]
        assert escape(p["tip"]) in details, p["id"]
        for s in p["sources"]:
            assert f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' in details, s["url"]


def test_group_headings_in_order():
    d = data()
    block = section("hu-patterns")
    headings = re.findall(r"<h3[^>]*>(.*?)</h3>", block, re.S)
    assert [unescape(h) for h in headings] == [g["name"] for g in d["groups"]]
    # Varje kort står under sin grupps rubrik.
    parts = re.split(r"<h3[^>]*>.*?</h3>", block, flags=re.S)[1:]
    for group, part in zip(d["groups"], parts):
        shown = re.findall(r'data-pattern-id="([^"]+)"', part)
        assert shown == [p["id"] for p in d["patterns"] if p["group"] == group["id"]], group["id"]


def test_legend_has_three_labels():
    d = data()
    legend = re.search(r'<ul class="tm-legend">.*?</ul>', section("hu-patterns"), re.S).group(0)
    assert len(re.findall("<li>", legend)) == 3
    for key in ("strong", "promising", "choosewise"):
        assert (f'<span class="tm-chip tm-chip--{key}">{LABEL_NAMES[key]}</span> '
                f'{escape(d["labels"][key]["definition"])}') in legend, key


def test_patterns_section_intro():
    block = section("hu-patterns")
    assert "Twelve ways to upgrade homework" in block
    assert "Grouped by what the homework is now. Each pattern works on paper, with no AI." in block


def test_pattern_select():
    d = data()
    select = re.search(r'<select[^>]*id="hu-pattern"[^>]*>(.*?)</select>', section("hu-builder"), re.S).group(1)
    assert select.lstrip().startswith('<option value="">Let the AI choose</option>')
    assert len(re.findall(r"<option", select)) == 13
    groups = re.findall(r'<optgroup label="([^"]*)">(.*?)</optgroup>', select, re.S)
    assert [unescape(label) for label, _ in groups] == [g["name"] for g in d["groups"]]
    for group, (_, body) in zip(d["groups"], groups):
        options = re.findall(r'<option value="([^"]*)">(.*?)</option>', body, re.S)
        expected = [(p["id"], escape(f"{p['number']}. {p['name']}")) for p in d["patterns"]
                    if p["group"] == group["id"]]
        assert options == expected, group["id"]
    assert 'href="#hu-patterns"' in section("hu-builder")


def test_data_block():
    m = re.search(r'<script type="application/json" id="hu-data">(.*?)</script>', html(), re.S)
    assert m
    patterns = json.loads(m.group(1))["patterns"]
    assert len(patterns) == 12
    assert patterns == [{"id": p["id"], "name": p["name"], "brief": p["brief"]} for p in data()["patterns"]]
    for p in patterns:
        assert set(p) == {"id", "name", "brief"}


def test_builder_fields_and_defaults():
    b = section("hu-builder")
    assert 'onsubmit="return false"' in b

    def tag(tag_name, element_id):
        return re.search(rf'<{tag_name}[^>]*id="{element_id}"[^>]*>', b).group(0)

    grade = re.search(r'<select[^>]*id="hu-grade"[^>]*>(.*?)</select>', b, re.S).group(1)
    assert re.findall(r'<option value="(\d+)"[^>]*>Grade \1</option>', grade) == ["7", "8", "9", "10", "11", "12"]
    assert re.findall(r'<option value="(\d+)" selected>', grade) == ["9"]

    minutes = re.search(r'<select[^>]*id="hu-minutes"[^>]*>(.*?)</select>', b, re.S).group(1)
    assert re.findall(r'<option value="(\d+)"[^>]*>\1 minutes</option>', minutes) == ["10", "15", "20", "30", "45"]
    assert re.findall(r'<option value="(\d+)" selected>', minutes) == ["20"]

    language = tag("input", "hu-language")
    assert 'value="English"' in language and 'maxlength="40"' in language

    homework = tag("textarea", "hu-homework")
    assert 'maxlength="3000"' in homework and 'rows="5"' in homework and " required" in homework
    placeholder = re.search(r'placeholder="([^"]*)"', homework).group(1)
    assert placeholder == "Read chapter 4, pages 62–71.&#10;Answer questions 1–6 on page 72."

    subject = tag("input", "hu-subject")
    assert 'maxlength="60"' in subject and " required" in subject
    assert 'placeholder="e.g. History"' in subject and 'list="hu-subjects"' in subject
    own = re.findall(r'<option value="([^"]*)">', re.search(r'<datalist id="hu-subjects">(.*?)</datalist>', b, re.S).group(1))
    lens = LESSON_LENS.read_text(encoding="utf-8")
    theirs = re.findall(r'<option value="([^"]*)">', re.search(r'<datalist id="ll-subjects">(.*?)</datalist>', lens, re.S).group(1))
    assert own == theirs and len(own) >= 10

    goal = tag("textarea", "hu-goal")
    assert 'maxlength="400"' in goal and 'rows="2"' in goal
    assert 'placeholder="e.g. Explain why the Industrial Revolution began in Britain"' in goal

    assert "readonly" in tag("textarea", "hu-prompt")
    assert PRIVACY in text_of(b)
    assert f'<p class="tm-hint" id="hu-hint" aria-live="polite">{HINT}</p>' in b
    copy = tag("button", "hu-copy")
    assert 'data-copy=""' in copy and " disabled" in copy
    # Ledtråden och knappen står i samma rad, som i Lesson Lens.
    row = re.search(r'<div class="tm-copy-row">.*?</div>', b, re.S).group(0)
    assert 'id="hu-copy"' in row and 'id="hu-hint"' in row and 'class="copy-toast"' in row
    assert ">Copy prompt</button>" in row
    for label in ("Pattern", "Subject", "Grade", "The homework as you set it",
                  "What should students be able to do afterwards? (optional)", "Time at home",
                  "Language of the homework", "Your prompt — copy it into your AI tool"):
        assert label in text_of(b), label
    assert "Paste it as students get it: the task, the questions, the pages." in text_of(b)


def test_check_section():
    d = data()["check"]
    block = section("hu-check")
    assert "The check in the next lesson" in block
    steps = re.search(r"<ol[^>]*>(.*?)</ol>", block, re.S).group(1)
    assert re.findall(r"<li>(.*?)</li>", steps, re.S) == [escape(s) for s in d["steps"]]
    assert escape(d["why"]) in block
    assert escape(d["detectors"]) in block


def test_students_copy_button():
    d = data()["students"]
    block = section("hu-students")
    assert "Tell your students why" in block
    assert escape(d["intro"]) in block
    for paragraph in d["text"]:
        assert escape(paragraph) in block, paragraph
    m = re.search(r'<button[^>]*data-copy="([^"]*)"[^>]*>(.*?)</button>\s*<span class="copy-toast"', block, re.S)
    assert m, "knappen ska ha en copy-toast direkt efter sig"
    assert unescape(m.group(1)) == "\n\n".join(d["text"])
    assert m.group(2) == "Copy text"


def test_students_data_copy_survives_a_real_parser():
    """Radbrytningar i data-copy ska överleva HTML-tolkaren."""
    found = []

    class Grab(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == "button" and dict(attrs).get("data-copy"):
                found.append(dict(attrs)["data-copy"])

    Grab().feed(section("hu-students"))
    assert found == ["\n\n".join(data()["students"]["text"])]


def test_clinic_links_to_skool():
    block = section("hu-clinic")
    assert "Homework Clinic" in block
    assert ("Homework Clinic is a weekly thread in the Choosewise community. Post one homework task "
            "as you set it, your upgraded version and what the check showed. Ask for a pattern when "
            "you are stuck, and see how teachers in other subjects upgrade theirs.") in text_of(block)
    assert re.search(r'<a [^>]*href="https://www\.skool\.com/choosewise-7103"[^>]*>Go to the community on Skool →</a>', block)


def test_evidence_lists_every_source():
    d = data()["evidence"]
    block = section("hu-evidence")
    assert "What the research says" in block
    assert "The parts are well supported. No study has tested upgraded homework as a package." in text_of(block)
    assert len(re.findall(r'class="hu-evidence__item"', block)) == 6
    for item in d:
        assert f"<strong>{escape(item['title'])}</strong>" in block, item["title"]
        assert escape(item["text"]) in block, item["title"]
        for s in item["sources"]:
            assert f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' in block, s["url"]


def test_age_section():
    d = data()
    block = section("hu-age")
    shown = text_of(block)
    assert ("You use AI to prepare. The upgraded homework needs no AI. If students use AI tools, "
            "these rules apply (November 2026):") in shown
    assert d["age_rules_date"] == "November 2026"
    for rule in d["age_rules"]:
        assert f"<li><strong>{escape(rule['tool'])}:</strong> {escape(rule['rule'])}</li>" in block, rule["tool"]
    for word in ("Copilot Chat", "Gemini", "ChatGPT", "Claude"):
        assert word in shown, word
    assert ("Rules differ between countries and change often. Check your own national rules and "
            "your school policy before students use any AI tool.") in shown


def test_next_links():
    block = section("hu-next")
    assert "<h2" in block and ">Next<" in block
    for href, label in (("/lesson-lens/", "Upgrade a lesson: Lesson Lens"),
                        ("/retrieval-rhythm/", "Weekly starters: Retrieval Rhythm"),
                        ("/study-moves/", "For your students: Study Moves")):
        assert f'<a href="{href}">{label}</a>' in block, href


def test_how_it_works_section():
    block = section("hu-how")
    steps = re.search(r"<ol[^>]*>(.*?)</ol>", block, re.S).group(1)
    assert [text_of(s) for s in re.findall(r"<li>(.*?)</li>", steps, re.S)] == [
        "Paste the homework as students get it. Choose a pattern, or let the AI choose.",
        "Copy the prompt into your AI tool. Read the answer before you hand anything out: check the "
        "facts and answers, and cut what does not fit your class.",
        "Tell students about the check when you set the homework, and start the next lesson with it.",
    ]
    assert ("No homework is AI-proof. A chatbot can do the upgraded homework too, and a student can "
            "copy its answers by hand. What changes is what the student loses by doing that, and the "
            "check in the next lesson shows it.") in text_of(block)


def test_hero_copy_and_no_hub_link():
    page = html()
    assert "For Choosewise members · Grades 7–12" in page
    assert "<h1>Homework Upgrade</h1>" in page
    assert ("Paste a homework task you have already set. Your AI tool keeps what works, turns the rest "
            "into practice students do from memory with pen and paper, says honestly what a chatbot "
            "could still do, and writes three questions to start the next lesson.") in text_of(page)
    assert "← Study + AI" not in page and 'class="tm-back"' not in page


def test_page_head():
    page = html()
    assert "<title>Homework Upgrade — choosewise.education</title>" in page
    assert ('<meta name="description" content="For Choosewise members. Paste a homework task you have '
            'already set and get, from any AI tool, a version students do from memory and a '
            'three-question check for the next lesson.">') in page
    assert '<link rel="stylesheet" href="/assets/css/homework-upgrade.css?v=20261114a">' in page
    assert '<link rel="stylesheet" href="/assets/css/thinking-moves.css?v=20261029a">' in page


def test_scripts_loaded():
    assert '<script src="/assets/js/copy-to-clipboard.js" defer></script>' in html()
    assert '<script src="/assets/js/homework-upgrade.js" defer></script>' in html()


def test_json_text_is_escaped():
    mod = load_build()
    pattern = {"id": "x", "number": 1, "group": "reading", "name": "A <b>", "instead": "i & j",
               "steps": ["<i>s</i>"] * 3, "check": "c", "why": "w & v", "label": "strong",
               "sources": [{"text": "s", "url": "https://x"}], "tip": "t", "chatbot": "cb", "brief": "b"}
    out = mod.render_pattern_card(pattern, {"strong": {"name": "Strong"}})
    assert "<b>" not in out and "&lt;b&gt;" in out and "<i>s</i>" not in out and "i &amp; j" in out


def test_data_block_cannot_close_the_script_tag():
    mod = load_build()
    d = data()
    d["patterns"][0]["brief"] = "x </script><b>"
    out = mod.render_data(d)
    assert out.count("</script>") == 1
    inner = re.search(r'id="hu-data">(.*)</script>', out, re.S).group(1)
    assert json.loads(inner)["patterns"][0]["brief"] == "x </script><b>"


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
        mod._inject("<p></p>", "patterns", "x")


def test_font_weights_only_from_tokens():
    css = CSS.read_text(encoding="utf-8")
    assert not re.search(r"font-weight:\s*\d", css)
