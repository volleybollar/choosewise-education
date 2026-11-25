"""Vakter för sidan Barrier Planner (/barrier-planner-1c25533d/).

Sidan är bara för Skool-medlemmar: den nås via en dold länk och länkas aldrig
från resten av sajten. Korten, exemplen, blanketten, listan över obelagda
anpassningar, forskningen och varningarna byggs från
barrier-planner-1c25533d/planner-en.json av scripts/build-barrier-planner.py,
så att de syns utan JavaScript. De två promptbyggarna får sin logik i
assets/js/barrier-planner.js (nästa steg); här prövas bara deras markup.
Spec: docs/superpowers/specs/2026-11-25-barrier-planner-design.md, del B.
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
SLUG = "barrier-planner-1c25533d"
PAGE = ROOT / SLUG / "index.html"
DATA = ROOT / SLUG / "planner-en.json"
BUILD = ROOT / "scripts/build-barrier-planner.py"
CSS = ROOT / "assets/css/barrier-planner.css"
LESSON_LENS = ROOT / "lesson-lens/index.html"
COMPASS = ROOT / "pedagogy-compass-59ecb8db/index.html"

SECTIONS = ["bp-how", "bp-barriers", "bp-plan", "bp-adapt", "bp-record", "bp-unsupported",
            "bp-evidence", "bp-care", "bp-next"]
MARKERS = ["hero-example", "how", "barriers", "barrier-options", "adapt-example", "record",
           "unsupported", "evidence", "care", "data"]
CARD_IDS = ["getting-started", "multi-step", "reading-load", "writing", "attention", "changes",
            "not-alone", "language"]
LABEL_NAMES = {"strong": "Strong", "promising": "Promising", "framework": "Framework",
               "choosewise": "Choosewise"}
HERO_LEDE = ("Start from the barrier you see in a task, not from a label. Find it among eight "
             "common barriers, read what helps the whole class, then build a prompt that fits "
             "those moves to your own task. No diagnosis and no student details, ever.")
PRIVACY_ADAPT = "Use your own text or one you are allowed to share. Never student work."
PRIVACY_FORM = "This form never goes through AI. Fill it in by hand or in your school's system for records."
NEXT_HREFS = ["/what-teachers-do-354716b7/", "/pedagogy-compass-59ecb8db/",
              "/quality-ladder-ec1c2f8c/", "/prompts/teachers/", "/study-moves/",
              "/visual-codes/", "https://www.skool.com/choosewise-7103"]
# Brittisk stavning som inte får stå i sidans ram (samma regel som i datafilens vakt).
BRITISH = re.compile(r"\b(behaviour\w*|colour\w*|programme|practis\w*|organis\w*|recognis\w*"
                     r"|labelled|centre|pupils?|maths)\b", re.IGNORECASE)
QUOTED = re.compile(r'"[^"]*"|“[^”]*”')


def html():
    return PAGE.read_text(encoding="utf-8")


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def section(sid):
    m = re.search(rf'<section[^>]*id="{sid}".*?</section>', html(), re.S)
    assert m, sid
    return m.group(0)


def marker(name, page=None):
    page = html() if page is None else page
    m = re.search(rf"<!-- {name}:start -->(.*?)<!-- {name}:end -->", page, re.S)
    assert m, name
    return m.group(1)


def text_of(fragment):
    """Texten i ett HTML-stycke: taggar borta, tecken avkodade, blanksteg samlade."""
    no_tags = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", unescape(no_tags)).strip()


def load_build():
    spec = importlib.util.spec_from_file_location("build_barrier_planner", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def copy_values(fragment):
    """Alla data-copy-värden i ordning, lästa av en riktig HTML-tolkare."""
    found = []

    class Grab(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == "button" and dict(attrs).get("data-copy"):
                found.append(dict(attrs)["data-copy"])

    Grab().feed(fragment)
    return found


def form(fid):
    m = re.search(rf'<form[^>]*id="{fid}".*?</form>', html(), re.S)
    assert m, fid
    return m.group(0)


def tag(fragment, element_id, name):
    """Startetiketten för elementet med ett visst id."""
    m = re.search(rf'<{name}\b[^>]*\bid="{element_id}"[^>]*>', fragment)
    assert m, element_id
    return m.group(0)


def options_of(fragment, select_id):
    """(värde, text, vald) för varje option i en select."""
    block = re.search(rf'<select[^>]*id="{select_id}".*?</select>', fragment, re.S).group(0)
    return [(m.group(1), unescape(m.group(3)), "selected" in m.group(2))
            for m in re.finditer(r'<option value="([^"]*)"([^>]*)>([^<]*)</option>', block)]


# ───── Sidans byggstenar ─────

def test_sections_in_order():
    ids = re.findall(r'<section[^>]*id="(bp-[a-z]+)"', html())
    assert ids == SECTIONS


def test_ids_are_unique():
    ids = re.findall(r'(?<![\w-])id="([^"]+)"', html())
    assert len(ids) == len(set(ids)), sorted({i for i in ids if ids.count(i) > 1})


def test_all_markers_present_in_pairs():
    page = html()
    for name in MARKERS:
        assert page.count(f"<!-- {name}:start -->") == 1, name
        assert page.count(f"<!-- {name}:end -->") == 1, name


def test_hero():
    page = html()
    assert '<span class="eyebrow">For Choosewise members · All school stages</span>' in page
    assert "<h1>Barrier Planner</h1>" in page
    assert '<a class="tm-back" href="/what-teachers-do-354716b7/">← What teachers do</a>' in page
    assert HERO_LEDE in text_of(page)
    assert ">What a plan looks like</h2>" in page
    block = marker("hero-example")
    for row in data()["hero"]["rows"]:
        assert f"<dt>{escape(row['term'])}</dt>" in block, row["term"]
        assert escape(row["text"]) in block, row["term"]
    assert escape(data()["hero"]["note"]) in block


def test_jump_links():
    page = html()
    for href, label in (("#bp-barriers", "Eight barriers"), ("#bp-plan", "Plan for a barrier"),
                        ("#bp-adapt", "Adapt a text"), ("#bp-record", "Needs and measures"),
                        ("#bp-unsupported", "Popular but unsupported")):
        assert re.search(rf'<a href="{href}">{label}</a>', page), href
    links = re.findall(r'<a href="(#bp-[a-z]+)">', page[:page.index('id="bp-how"')])
    assert links == ["#bp-barriers", "#bp-plan", "#bp-adapt", "#bp-record", "#bp-unsupported"]


def test_how_it_works():
    block = section("bp-how")
    items = re.findall(r"<li>(.*?)</li>", block, re.S)
    assert [unescape(i) for i in items] == data()["how"]
    assert len(items) == 3


# ───── De åtta korten ─────

def test_cards():
    d = data()
    page = html()
    ids = re.findall(r'<article[^>]*\bid="(bp-barrier-[a-z-]+)"', page)
    assert ids == [f"bp-barrier-{i}" for i in CARD_IDS]
    assert "<details" not in section("bp-barriers")
    for c in d["cards"]:
        card = re.search(rf'<article[^>]*id="bp-barrier-{c["id"]}".*?</article>', page, re.S).group(0)
        shown = text_of(card)
        for part in ("What you see", "For the whole class", "Targeted", "Look for in three weeks"):
            assert part in shown, (c["id"], part)
        assert ("Not this" in shown) == bool(c["not_this"]), c["id"]
        assert 'tm-chip tm-chip--framework">Framework</span>' in card, c["id"]
        assert escape(c["barrier"]) in card, c["id"]
        assert escape(c["review"]) in card, c["id"]
        for s in c["signs"] + c["not_this"]:
            assert escape(s) in card, (c["id"], s)
        for move in c["whole_class"] + c["targeted"]:
            assert escape(move["text"]) in card, (c["id"], move["text"])
            if move["label"]:
                assert f'tm-chip--{move["label"]}">{LABEL_NAMES[move["label"]]}</span>' in card
        for s in c["sources"]:
            assert f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' in card, s["url"]
        if c["link"]:
            assert f'<a href="{escape(c["link"]["href"])}">{escape(c["link"]["text"])}</a>' in card
        else:
            assert "bp-card__link" not in card, c["id"]


def test_diagnosis_help_above_cards():
    block = section("bp-barriers")
    d = data()["barriers_intro"]
    assert d["diagnosis"] in text_of(block) and d["privacy"] in text_of(block)
    assert block.index(escape(d["diagnosis"])) < block.index("<article")
    assert block.index(escape(d["privacy"])) < block.index("<article")


# ───── Byggarna och blanketten ─────

def test_privacy_lines():
    page = html()
    plan, adapt, record = section("bp-plan"), section("bp-adapt"), section("bp-record")
    line = ("<strong>Do not include student names, student work or a diagnosis.</strong> "
            "The prompt only needs the task, the barrier and what you see.")
    assert line in plan
    assert plan.index(line) < plan.index("<form")
    assert f"<strong>{PRIVACY_ADAPT}</strong>" in adapt
    assert adapt.index(PRIVACY_ADAPT) < adapt.index("<form")
    assert PRIVACY_FORM in text_of(record)
    assert page.count("<strong>This form never goes through AI.</strong>") == 1
    # Varningen står direkt före blanketten, utan något emellan, och blanketten börjar med rubrikraden.
    m = re.search(r'<p class="bp-warning">.*?</p>\s*(<[a-z]+[^>]*>)', record, re.S)
    assert m and m.group(1) == '<div class="bp-form">', m and m.group(1)
    first_row = re.search(r'<div class="bp-form">\s*<div class="bp-form__row">(.*?)</div>\s*</div>\s*<div',
                          record, re.S)
    assert first_row
    for label in ("Student or class", "Date", "Who took part"):
        assert label in text_of(first_row.group(1)), label
    assert record.index("bp-warning") < record.index('class="bp-form"') < record.index("data-copy")


def test_plan_fields():
    plan = section("bp-plan")
    f = form("bp-plan-form")
    for fid, name in (("bp-subject", "input"), ("bp-grade", "select"), ("bp-task", "textarea"),
                      ("bp-barrier", "select"), ("bp-barrier-other", "input"), ("bp-seen", "input"),
                      ("bp-goal", "input"), ("bp-review", "select"), ("bp-language", "input")):
        assert tag(f, fid, name), fid
    assert "required" in tag(f, "bp-subject", "input")
    assert "required" in tag(f, "bp-task", "textarea")
    for fid, name, limit in (("bp-subject", "input", 60), ("bp-task", "textarea", 2000),
                             ("bp-barrier-other", "input", 200), ("bp-seen", "input", 300),
                             ("bp-goal", "input", 200), ("bp-language", "input", 40)):
        assert f'maxlength="{limit}"' in tag(f, fid, name), fid
    assert 'list="bp-subjects"' in tag(f, "bp-subject", "input")
    assert 'value="English"' in tag(f, "bp-language", "input")
    grades = options_of(f, "bp-grade")
    assert [v for v, _, _ in grades] == [str(i) for i in range(1, 13)]
    assert [v for v, _, sel in grades if sel] == ["8"]
    barriers = options_of(f, "bp-barrier")
    assert barriers[0][:2] == ("", "Choose a barrier")
    assert [b[:2] for b in barriers[1:-1]] == [(c["id"], c["barrier"]) for c in data()["cards"]]
    assert barriers[-1][:2] == ("other", "Something else")
    assert [(v, sel) for v, _, sel in options_of(f, "bp-review")] == [("two weeks", False), ("three weeks", True)]
    assert "What happens in the task, not who it happens to." in f
    assert "It stays the same for every student." in f
    # Fältet "Something else" är dolt tills byggaren visar det; länken till kortet står vid listan.
    assert "hidden" in tag(plan, "bp-other-field", "label")
    assert re.search(r'<a[^>]*id="bp-card-link"[^>]*>Read the card</a>', plan)
    assert "readonly" in tag(plan, "bp-prompt", "textarea")
    copy = tag(plan, "bp-copy", "button")
    assert "disabled" in copy and 'data-copy=""' in copy
    assert 'id="bp-hint"' in plan and "Fill in subject, the task and the barrier to see your prompt." in plan
    assert ">Copy prompt</button>" in plan


def test_adapt_fields():
    adapt = section("bp-adapt")
    f = form("bp-adapt-form")
    for fid, name in (("bp-a-subject", "input"), ("bp-a-grade", "select"), ("bp-a-barrier", "select"),
                      ("bp-a-words", "select"), ("bp-a-text", "textarea")):
        assert tag(f, fid, name), fid
    assert 'list="bp-subjects"' in tag(f, "bp-a-subject", "input")
    assert "required" in tag(f, "bp-a-subject", "input")
    text = tag(f, "bp-a-text", "textarea")
    assert "required" in text and 'maxlength="8000"' in text and 'rows="8"' in text
    grades = options_of(f, "bp-a-grade")
    assert len(grades) == 12 and [v for v, _, sel in grades if sel] == ["8"]
    assert [(v, t) for v, t, _ in options_of(f, "bp-a-barrier")] == [
        ("", "No particular barrier"),
        ("reading-load", "Reading a long text takes all their energy"),
        ("language", "Still learning the language of instruction")]
    assert [(v, sel) for v, _, sel in options_of(f, "bp-a-words")] == [("5", False), ("8", True), ("10", False)]
    assert "readonly" in tag(adapt, "bp-a-prompt", "textarea")
    copy = tag(adapt, "bp-a-copy", "button")
    assert "disabled" in copy and 'data-copy=""' in copy
    assert "Fill in subject and paste the text to see your prompt." in adapt and 'id="bp-a-hint"' in adapt
    assert ">Copy prompt</button>" in adapt
    assert escape(data()["adapt"]["intro"]) in adapt


def test_no_field_asks_for_a_diagnosis():
    for fid in ("bp-plan-form", "bp-adapt-form"):
        f = form(fid)
        shown = " ".join(re.findall(r"<label\b.*?</label>", f, re.S)
                         + re.findall(r'placeholder="([^"]*)"', f)
                         + re.findall(r"<option[^>]*>([^<]*)</option>", f))
        assert "diagnos" not in shown.lower(), fid
    # Raden om diagnos står i ett <p> ovanför formuläret, inte i en etikett.
    plan = section("bp-plan")
    assert "diagnosis" in plan[:plan.index("<form")]


def test_subject_datalist():
    source = re.search(r'<datalist id="ll-subjects">(.*?)</datalist>',
                       LESSON_LENS.read_text(encoding="utf-8"), re.S).group(1)
    expected = [v if v != "Maths" else "Math" for v in re.findall(r'<option value="([^"]+)"', source)]
    mine = re.search(r'<datalist id="bp-subjects">(.*?)</datalist>', html(), re.S).group(1)
    assert re.findall(r'<option value="([^"]+)"', mine) == expected
    assert "Math" in expected and "Maths" not in expected


def test_section_chips():
    adapt = section("bp-adapt")
    assert 'tm-chip tm-chip--promising">Promising</span>' in adapt
    assert "Pictures and diagrams are Strong" in text_of(adapt)
    assert adapt.index("tm-chip") < adapt.index("<form")
    record = section("bp-record")
    assert 'tm-chip tm-chip--framework">Framework</span>' in record
    assert record.index("tm-chip") < record.index("<!-- record:start -->")


# ───── Data till byggarna ─────

def parse_data_block(page):
    m = re.search(r'<script type="application/json" id="bp-data">(.*?)</script>', page, re.S)
    assert m
    return json.loads(m.group(1))


def test_bp_data_matches_json():
    mod = load_build()
    out = mod.bp_data(data())
    assert parse_data_block(html()) == out
    assert [c["id"] for c in out["cards"]] == CARD_IDS
    first = data()["cards"][0]
    assert out["cards"][0] == {"id": first["id"], "barrier": first["barrier"],
                               "whole_class": [m["short"] for m in first["whole_class"]],
                               "targeted": [m["short"] for m in first["targeted"]]}


def test_bp_data_is_script_safe(tmp_path):
    mod = load_build()
    d = data()
    d["cards"][0]["whole_class"][0]["short"] = "a </script><b>"
    shutil.copytree(ROOT / SLUG, tmp_path / SLUG)
    (tmp_path / SLUG / "planner-en.json").write_text(json.dumps(d), encoding="utf-8")
    mod.build(tmp_path)
    page = (tmp_path / SLUG / "index.html").read_text(encoding="utf-8")
    block = re.search(r'<script type="application/json" id="bp-data">(.*?)</script>', page, re.S).group(1)
    assert "</script>" not in block and "</" not in block
    assert parse_data_block(page)["cards"][0]["whole_class"][0] == "a </script><b>"


# ───── Kopieringsrader och nedladdningar ─────

def test_copy_rows():
    mod = load_build()
    d = data()
    record = section("bp-record")
    assert mod.record_text(d["record"]) in copy_values(record)
    assert ">Copy text</button>" in record
    assert '<a href="needs-and-measures.docx" download>' in record
    unsupported = section("bp-unsupported")
    assert mod.unsupported_text(d["unsupported"]) in copy_values(unsupported)
    assert '<a href="popular-but-unsupported.docx" download>' in unsupported


def test_record_text_order():
    mod = load_build()
    r = data()["record"]
    text = mod.record_text(r)
    assert text.startswith("Needs and measures\n\n" + r["warning"] + "\n\n")
    order = ["Needs and measures", r["warning"]] + [h + ":" for h in r["header"]]
    for b in r["blocks"]:
        order += [b["heading"], b["hint"]]
        if b["kind"] == "measures":
            order += r["measure_columns"]
        if b["kind"] == "outcomes":
            order += r["outcomes"]
    order += ["Questions for the review meeting"] + r["review_questions"]
    order += ["The EEF's three questions"] + r["eef_questions"] + [r["country_line"]]
    at = -1
    for piece in order:
        found = text.find(piece, at + 1)
        assert found > at, piece
        at = found
    assert "<" not in text and "&amp;" not in text


def test_unsupported_text_shape():
    mod = load_build()
    u = data()["unsupported"]
    text = mod.unsupported_text(u)
    assert text.startswith("Popular but unsupported\n\n")
    assert text.endswith(u["movement_note"])
    at = 0
    for item in u["items"]:
        for piece in (item["title"], item["research"], "Instead: " + item["instead"]):
            at = text.index(piece, at)


def test_privacy_copy_constant():
    assert load_build().PRIVACY_COPY == "Do not include student names or student work in this conversation."


def test_data_copy_survives_a_real_parser():
    """Citattecken, apostrof, & och radbrytningar i data-copy ska överleva HTML-tolkaren."""
    mod = load_build()
    d = data()
    found = copy_values(section("bp-record")) + copy_values(section("bp-unsupported"))
    assert found == [mod.record_text(d["record"]), mod.unsupported_text(d["unsupported"])]


def test_copy_buttons_are_followed_by_a_toast():
    for sid in ("bp-plan", "bp-adapt", "bp-record", "bp-unsupported"):
        block = section(sid)
        buttons = len(re.findall(r"<button[^>]*data-copy", block))
        # Toasten följer knappen som syskon: direkt efter, eller efter ledtråden i byggarnas rad.
        toasts = len(re.findall(r'<span class="copy-toast" role="status">Copied</span>', block))
        assert buttons == toasts and buttons > 0, sid
        for row in re.findall(r'<div class="tm-copy-row">.*?</div>', block, re.S):
            assert row.index("<button") < row.index("copy-toast"), sid


# ───── Resten av avsnitten ─────

def test_adapt_example_and_links():
    d = data()["adapt"]
    block = marker("adapt-example")
    for row in d["example"]:
        assert f"<dt>{escape(row['term'])}</dt>" in block and escape(row["text"]) in block, row["term"]
    assert [r["term"] for r in d["example"]] == ["Original", "Elaborated", "Glossary", "Section question", "Picture"]
    assert escape(d["check"]) in block
    assert re.findall(r'href="([^"]+)"', block) == ["/visual-codes/", "/free/study-codes/", "/infographic-styles/"]
    assert block.index(escape(d["check"])) < block.index("<a ")


def test_unsupported_section():
    d = data()["unsupported"]
    block = section("bp-unsupported")
    assert ">Popular but unsupported</h2>" in block
    assert len(d["items"]) == 6
    for item in d["items"]:
        assert escape(item["title"]) in block and escape(item["research"]) in block, item["title"]
        assert escape(item["instead"]) in block, item["title"]
    assert text_of(block).count("Instead:") == 6
    assert escape(d["movement_note"]) in block
    assert escape(d["intro"]) in block


def test_evidence_and_legend():
    d = data()
    block = section("bp-evidence")
    assert ">What the research says</h2>" in block
    assert escape(d["evidence"]["lede"]) in block
    legend = re.search(r'<ul class="tm-legend">.*?</ul>', block, re.S).group(0)
    assert len(re.findall("<li>", legend)) == 4
    for key, name in LABEL_NAMES.items():
        assert (f'<span class="tm-chip tm-chip--{key}">{name}</span> '
                f'{escape(d["labels"][key]["definition"])}') in legend, key
    items = block.split('class="bp-evidence__item"')[1:]
    assert len(items) == len(d["evidence"]["items"]) == 9
    for item, e in zip(items, d["evidence"]["items"]):
        assert f"<strong>{escape(e['title'])}</strong>" in item
        assert escape(e["text"]) in item
        assert f'<span class="tm-chip tm-chip--{e["label"]}">{LABEL_NAMES[e["label"]]}</span>' in item
        for s in e["sources"]:
            assert f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' in item, s["url"]


def test_care_section():
    block = section("bp-care")
    assert ">Watch out for</h2>" in block
    care = data()["care"]
    assert len(re.findall(r"<li>", block)) == len(care) == 5
    for c in care:
        assert escape(c["risk"]) in block and escape(c["what_we_do"]) in block, c["risk"]


def test_next_links():
    block = section("bp-next")
    assert ">Next</h2>" in block
    assert re.findall(r'href="([^"]+)"', block) == NEXT_HREFS
    items = re.findall(r"<li>(.*?)</li>", block, re.S)
    assert "86" in items[3] and "67" in items[3]
    assert "write the barrier you see, not a diagnosis" in text_of(items[3])
    shown = text_of(block)
    for label in ("Back to the overview: What teachers do", "Pedagogy Compass", "Quality Ladder",
                  "Prompts for teachers", "Study Moves", "Visual codes"):
        assert label in shown, label


def test_anchors_exist():
    page = html()
    for sid in ("bp-plan", "bp-adapt", "bp-record"):
        assert f'id="{sid}"' in page, sid
    compass = COMPASS.read_text(encoding="utf-8")
    for anchor in ("problem-dont-start", "problem-overload", "problem-not-alone"):
        assert f'id="{anchor}"' in compass, anchor


def test_no_british_spelling_in_frame():
    page = html()
    for name in MARKERS:
        page = re.sub(rf"<!-- {name}:start -->.*?<!-- {name}:end -->", "", page, flags=re.S)
    shown = QUOTED.sub("", text_of(re.sub(r"<!--.*?-->", "", page, flags=re.S)))
    assert not BRITISH.findall(shown), BRITISH.findall(shown)


# ───── Sidan som helhet ─────

def test_page_head():
    page = html()
    assert "<title>Barrier Planner — Choosewise</title>" in page
    assert '<meta name="description" content="' in page
    assert '<link rel="stylesheet" href="/assets/css/barrier-planner.css?v=20261125a">' in page
    assert '<link rel="stylesheet" href="/assets/css/thinking-moves.css?v=20261029a">' in page


def test_noindex():
    assert '<meta name="robots" content="noindex,nofollow">' in html()
    assert 'rel="canonical"' not in html()


def test_no_canonical_or_og():
    page = html()
    assert 'rel="canonical"' not in page
    assert "og:image" not in page and 'property="og:' not in page


def test_hidden_page_is_not_linked_anywhere():
    for rel in ["sitemap.xml", "llms.txt", "index.html", "robots.txt", "study/index.html",
                "pedagogy/index.html", "think/index.html"]:
        assert SLUG not in (ROOT / rel).read_text(encoding="utf-8"), rel
    for p in (ROOT / "assets/partials").glob("*"):
        assert SLUG not in p.read_text(encoding="utf-8"), p.name


def test_scripts_loaded():
    page = html()
    assert '<script src="/assets/js/copy-to-clipboard.js" defer></script>' in page
    assert '<script src="/assets/js/barrier-planner.js" defer></script>' in page


def test_json_text_is_escaped():
    mod = load_build()
    labels = data()["labels"]
    out = mod.render_care([{"risk": "A <b>", "what_we_do": "i & j"}])
    assert "<b>" not in out and "&lt;b&gt;" in out and "i &amp; j" in out
    out = mod.render_evidence({"lede": "l <l>", "items": [
        {"title": "T <b>", "text": "a & b", "label": "strong",
         "sources": [{"text": "s <i>", "url": "https://x?a=1&b=2"}]}]}, labels)
    assert "<b>" not in out and "<i>" not in out and "<l>" not in out
    assert "a &amp; b" in out and "a=1&amp;b=2" in out
    out = mod.render_unsupported({"intro": "x <u>", "movement_note": "m & n", "items": [
        {"title": "T <s>", "research": "r & s", "instead": "i <a>"}]})
    assert "<u>" not in out and "<s>" not in out and "<a>" not in out and "m &amp; n" in out
    rec = dict(data()["record"], warning='say "hi" & <go> →')
    out = mod.render_record(rec)
    assert "<go>" not in out and "&lt;go&gt;" in out
    assert copy_values(out)[0] == mod.record_text(rec)


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
    with pytest.raises(ValueError, match="care"):
        mod._inject("<p></p>", "care", "x")


def test_swedish_comments():
    """Varje sektion har minst en kommentar (utöver markörerna) som förklarar den."""
    page = html()
    for sid in SECTIONS:
        start = page.index(f'id="{sid}"')
        before = page[:start]
        prev = before.rfind("</section>")
        gap = before[prev if prev != -1 else 0:]
        comments = re.findall(r"<!--(.*?)-->", gap, re.S)
        explaining = [c for c in comments if not re.match(r"\s*[a-z-]+:(start|end)\b", c)]
        assert explaining, sid


def test_font_weights_only_from_tokens():
    css = CSS.read_text(encoding="utf-8")
    assert not re.search(r"font-weight:\s*\d", css)
