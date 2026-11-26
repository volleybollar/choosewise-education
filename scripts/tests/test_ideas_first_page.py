"""Vakter för sidan Ideas first (/ideas-first-778ba230/).

Sidan är bara för Skool-medlemmar: den nås via en dold länk och länkas aldrig
från resten av sajten. Exemplet, de fyra stegen, kontrollerna, teamrutinen,
forskningen, varningarna och länkarna byggs från ideas-first-778ba230/ideas-en.json
av scripts/build-ideas-first.py, så att de syns utan JavaScript. Promptbyggarens
logik får assets/js/ideas-first.js (nästa steg); här prövas bara dess markup.
Spec: docs/superpowers/specs/2026-11-26-ideas-first-design.md, del B.
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
SLUG = "ideas-first-778ba230"
PAGE = ROOT / SLUG / "index.html"
DATA = ROOT / SLUG / "ideas-en.json"
BUILD = ROOT / "scripts/build-ideas-first.py"
CSS = ROOT / "assets/css/ideas-first.css"
BARRIER_PAGE = ROOT / "barrier-planner-1c25533d/index.html"

SECTIONS = ["if-how", "if-ideas", "if-choose", "if-team", "if-evidence", "if-care", "if-next"]
MARKERS = ["hero-example", "how", "choose", "team", "evidence", "care", "next"]
LABEL_NAMES = {"strong": "Strong", "promising": "Promising", "framework": "Framework",
               "choosewise": "Choosewise"}
HERO_LEDE = ("AI makes ideas easy to get, and they tend to look alike. Write your own ideas "
             "first, ask for many that differ on purpose, then choose one and make it yours. "
             "No student details needed.")
PRIVACY_LINE = ("<strong>Do not include student names or student work.</strong> The prompt "
                "only needs the subject, the goal and your own ideas.")
WRITING_AID = "This prompt is a writing aid, not an evidence-based method."
HINT = "Write the subject, the goal and at least one idea of your own to see your prompt."
BRITISH = re.compile(r"\b(behaviour\w*|colour\w*|programme|practis\w*|organis\w*|recognis\w*"
                     r"|labelled|centre|pupils?|maths|defence)\b", re.IGNORECASE)
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
    spec = importlib.util.spec_from_file_location("build_ideas_first", BUILD)
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


def form():
    m = re.search(r'<form[^>]*id="if-form".*?</form>', html(), re.S)
    assert m
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
    assert re.findall(r'<section[^>]*id="(if-[a-z]+)"', html()) == SECTIONS


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
    assert "<h1>Ideas first</h1>" in page
    assert '<a class="tm-back" href="/what-teachers-do-354716b7/">← What teachers do</a>' in page
    assert f'<p class="lede">{HERO_LEDE}</p>' in page
    assert ">What it looks like</h2>" in page
    block = marker("hero-example")
    for row in data()["hero"]["rows"]:
        assert f"<dt>{escape(row['term'])}</dt>" in block, row["term"]
        assert f"<dd>{escape(row['text'])}</dd>" in block, row["term"]
    assert escape(data()["hero"]["note"]) in block
    assert escape(data()["hero"]["closing"]) in block


def test_jump_links():
    page = html()
    wanted = [("#if-how", "Four steps"), ("#if-ideas", "Get ideas"),
              ("#if-choose", "Choose and change"), ("#if-team", "In a team"),
              ("#if-evidence", "What the research says")]
    for href, label in wanted:
        assert f'<a href="{href}">{label}</a>' in page, href
    head = page[:page.index('id="if-how"')]
    assert re.findall(r'<a href="(#if-[a-z]+)">', head) == [h for h, _ in wanted]


def test_four_steps():
    block = section("if-how")
    assert ">Four steps</h2>" in block
    items = re.findall(r"<li>(.*?)</li>", block, re.S)
    assert [unescape(i) for i in items] == data()["how"]["steps"]
    assert len(items) == 4
    assert '<span class="tm-chip tm-chip--framework">Framework</span>' in block
    assert escape(data()["how"]["note"]) in block


# ───── Get ideas ─────

def test_privacy_line_before_form():
    block = section("if-ideas")
    assert ">Get ideas</h2>" in block
    assert f'<p class="tm-privacy">{PRIVACY_LINE}</p>' in block
    assert block.index(PRIVACY_LINE) < block.index('<form class="tm-form" id="if-form"')


def test_fields():
    f = form()
    for fid, name in (("if-who", "select"), ("if-subject", "input"), ("if-grade", "select"),
                      ("if-goal", "input"), ("if-own", "textarea"), ("if-fit", "input"),
                      ("if-language", "input")):
        assert tag(f, fid, name), fid
    for fid, name in (("if-subject", "input"), ("if-goal", "input"), ("if-own", "textarea")):
        assert "required" in tag(f, fid, name), fid
    for fid, name, limit in (("if-subject", "input", 60), ("if-goal", "input", 200),
                             ("if-own", "textarea", 1500), ("if-fit", "input", 200),
                             ("if-language", "input", 40)):
        assert f'maxlength="{limit}"' in tag(f, fid, name), fid
    assert 'rows="4"' in tag(f, "if-own", "textarea")
    assert 'list="if-subjects"' in tag(f, "if-subject", "input")
    assert 'value="English"' in tag(f, "if-language", "input")
    assert options_of(f, "if-who") == [("me", "Just me", True), ("team", "Our team", False)]
    grades = options_of(f, "if-grade")
    assert [t for _, t, _ in grades] == [f"Grade {i}" for i in range(1, 13)]
    assert [t for _, t, sel in grades if sel] == ["Grade 8"]
    for ph in ("e.g. Geography", "e.g. explain why towns grew up beside rivers",
               "One idea per line, e.g. a map of local rivers and towns",
               "e.g. 20 minutes, no computers"):
        assert f'placeholder="{ph}"' in f, ph
    notes = re.findall(r'<span class="tm-field__note"[^>]*>(.*?)</span>', f)
    assert notes == ["What students should be able to do.", "Two or three is enough.",
                     "About the lesson or the class as a whole, never a student."]
    assert re.search(r'<span[^>]*id="if-own-label"[^>]*>Your own ideas</span>', f)
    assert re.search(r'<span[^>]*id="if-own-note"[^>]*>Two or three is enough\.</span>', f)
    labels = re.findall(r'<span class="tm-field__label"[^>]*>(.*?)</span>', f)
    assert labels == ["Who is planning", "Subject", "Grade", "The goal of the lesson",
                      "Your own ideas", "Anything the ideas must fit (optional)",
                      "Language of the ideas"]


def test_prompt_box_and_copy_row():
    block = section("if-ideas")
    assert "readonly" in tag(block, "if-prompt", "textarea")
    assert "Your prompt — copy it into your AI tool" in block
    assert block.index('id="if-prompt"') > block.index("</form>")
    copy = tag(block, "if-copy", "button")
    assert "disabled" in copy and 'data-copy=""' in copy and 'aria-describedby="if-hint"' in copy
    assert re.search(rf'<p class="tm-hint" id="if-hint" aria-live="polite">{re.escape(HINT)}</p>', block)
    assert ">Copy prompt</button>" in block
    assert re.search(r'<button[^>]*id="if-copy"[^>]*>Copy prompt</button>\s*(?:<!--.*?-->\s*)?'
                     r'<p class="tm-hint"[^>]*id="if-hint"[^>]*>.*?</p>\s*'
                     r'<span class="copy-toast" role="status">Copied</span>', block, re.S)


def test_no_label_asks_about_a_student():
    """Fältets namn, hjälptexten i fältet och alternativen frågar aldrig efter en elev.
    De två bindande anteckningarna (.tm-field__note) får innehålla ordet."""
    f = form()
    labels = re.findall(r'<span class="tm-field__label"[^>]*>(.*?)</span>', f)
    placeholders = re.findall(r'placeholder="([^"]*)"', f)
    options = re.findall(r"<option[^>]*>([^<]*)</option>", f)
    for text in labels + placeholders + options:
        assert "student" not in unescape(text).lower(), text


def test_writing_aid_line():
    block = section("if-ideas")
    assert WRITING_AID in text_of(block)
    assert block.index(WRITING_AID) > block.index('id="if-prompt"')


def test_subject_datalist():
    source = re.search(r'<datalist id="bp-subjects">(.*?)</datalist>',
                       BARRIER_PAGE.read_text(encoding="utf-8"), re.S).group(1)
    mine = re.search(r'<datalist id="if-subjects">(.*?)</datalist>', html(), re.S).group(1)
    assert re.findall(r'<option value="([^"]+)"', mine) == re.findall(r'<option value="([^"]+)"', source)


# ───── Choose and change, In a team ─────

def test_choose_section():
    d = data()["choose"]
    block = section("if-choose")
    assert ">Choose and change</h2>" in block
    assert escape(d["intro"]) in block
    assert ">Check before use</h3>" in block
    ol = re.search(r"<ol[^>]*>(.*?)</ol>", block, re.S).group(1)
    items = re.findall(r"<li>(.*?)</li>", ol, re.S)
    assert len(items) == 3
    for item, check in zip(items, d["checks"]):
        assert item.startswith(escape(check)), check
    # Följdprompten ligger i den första punkten, direkt efter kontrollen.
    assert items[0] == (escape(d["checks"][0]) + '<div class="tm-copy-row">'
                        f'<button type="button" class="btn btn--primary" data-copy="{escape(d["follow_up"])}">'
                        'Copy follow-up prompt</button><span class="copy-toast" role="status">Copied</span></div>')
    assert "data-copy" not in items[1] and "data-copy" not in items[2]
    assert ">Three ways to change an idea</h3>" in block
    ways = re.search(r'<ul class="if-ways">(.*?)</ul>', block, re.S).group(1)
    assert [unescape(w) for w in re.findall(r"<li>(.*?)</li>", ways, re.S)] == d["ways"]
    assert escape(d["ways_note"]) in block
    assert block.index(escape(d["ways_note"])) > block.index("</ul>")


def test_team_section():
    d = data()["team"]
    block = section("if-team")
    assert ">In a team</h2>" in block
    assert escape(d["intro"]) in block
    ol = re.search(r"<ol[^>]*>(.*?)</ol>", block, re.S).group(1)
    items = re.findall(r"<li>(.*?)</li>", ol, re.S)
    assert [unescape(re.sub(r"<[^>]+>", "", i)) for i in items] == d["routine"]
    assert '<a href="#if-ideas">Get ideas</a>' in items[3]
    assert "<a" not in "".join(items[:3] + items[4:])
    assert escape(d["routine_note"]) in block
    assert '<a href="team-idea-sheet.docx" download>Team sheet (.docx)</a>' in block
    assert block.index("</ol>") < block.index("team-idea-sheet.docx")
    assert "data-copy" not in block


def test_data_copy_survives_a_real_parser():
    """Citattecken, apostrof, & och radbrytningar i data-copy ska överleva HTML-tolkaren."""
    assert copy_values(section("if-choose")) == [data()["choose"]["follow_up"]]


def test_copy_buttons_are_followed_by_a_toast():
    for sid in ("if-ideas", "if-choose"):
        block = section(sid)
        buttons = len(re.findall(r"<button[^>]*data-copy", block))
        toasts = len(re.findall(r'<span class="copy-toast" role="status">Copied</span>', block))
        assert buttons == toasts and buttons > 0, sid


# ───── Resten av avsnitten ─────

def test_evidence_and_legend():
    d = data()
    block = section("if-evidence")
    assert ">What the research says</h2>" in block
    assert escape(d["evidence"]["lede"]) in block
    lede_at = block.index(escape(d["evidence"]["lede"]))
    legend = re.search(r'<ul class="tm-legend">.*?</ul>', block, re.S)
    chip = '<span class="tm-chip tm-chip--promising">Promising</span>'
    assert lede_at < block.index(chip) < legend.start()
    assert len(re.findall("<li>", legend.group(0))) == 4
    for key, name in LABEL_NAMES.items():
        assert (f'<span class="tm-chip tm-chip--{key}">{name}</span> '
                f'{escape(d["labels"][key]["definition"])}') in legend.group(0), key
    items = block.split('class="if-evidence__item"')[1:]
    assert len(items) == len(d["evidence"]["items"]) == 6
    for item, e in zip(items, d["evidence"]["items"]):
        assert f'<strong class="if-item-title">{escape(e["title"])}</strong>' in item
        assert escape(e["text"]) in item
        if e["label"]:
            assert f'<span class="tm-chip tm-chip--{e["label"]}">' in item
        else:
            assert "tm-chip" not in item
        for s in e["sources"]:
            assert f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' in item, s["url"]
    assert [bool(re.search("tm-chip", i)) for i in items] == [False] * 5 + [True]


def test_care_section():
    block = section("if-care")
    assert ">Watch out for</h2>" in block
    care = data()["care"]
    assert len(re.findall(r"<li>", block)) == len(care) == 5
    for c in care:
        assert escape(c["risk"]) in block and escape(c["what_we_do"]) in block, c["risk"]


def test_next_links():
    block = section("if-next")
    assert ">Next</h2>" in block
    nxt = data()["next"]
    assert re.findall(r'href="([^"]+)"', block) == [n["href"] for n in nxt]
    items = re.findall(r"<li>(.*?)</li>", block, re.S)
    assert [text_of(i) for i in items] == [n["text"] for n in nxt]
    for i in items:
        assert i.startswith("<a ") and i.endswith("</a>")


def test_anchors_exist():
    page = html()
    for sid in ("if-ideas", "if-choose", "if-team"):
        assert f'id="{sid}"' in page, sid


def test_no_british_spelling_in_frame():
    page = html()
    for name in MARKERS:
        page = re.sub(rf"<!-- {name}:start -->.*?<!-- {name}:end -->", "", page, flags=re.S)
    shown = QUOTED.sub("", text_of(re.sub(r"<!--.*?-->", "", page, flags=re.S)))
    assert not BRITISH.findall(shown), BRITISH.findall(shown)


# ───── Teamets blad som text ─────

def test_sheet_text_order():
    mod = load_build()
    sheet = data()["team"]["sheet"]
    lines = mod.sheet_text(sheet).split("\n")
    expected = [sheet["title"]] + [f"{h}:" for h in sheet["header"]] + [sheet["note"],
                                                                        sheet["routine_heading"]]
    expected += sheet["routine"]
    expected += [sheet["before_ai"]["heading"]] + sheet["before_ai"]["columns"]
    expected += [sheet["from_ai"]["heading"], sheet["from_ai"]["hint"]]
    expected += [sheet["chose"]["heading"]] + sheet["chose"]["columns"]
    assert lines == expected
    assert mod.sheet_text(sheet) == mod.sheet_text(json.loads(json.dumps(sheet)))


def test_constants():
    mod = load_build()
    assert mod.SLUG == SLUG
    assert mod.PRIVACY_COPY == "Do not include student names or student work in this conversation."


# ───── Sidan som helhet ─────

def test_page_head():
    page = html()
    assert "<title>Ideas first — Choosewise</title>" in page
    assert '<meta name="description" content="' in page
    assert '<link rel="stylesheet" href="/assets/css/ideas-first.css?v=20261126a">' in page
    assert '<link rel="stylesheet" href="/assets/css/thinking-moves.css?v=20261029a">' in page


def test_noindex():
    assert '<meta name="robots" content="noindex,nofollow">' in html()


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
    assert '<script src="/assets/js/ideas-first.js" defer></script>' in page


def test_json_text_is_escaped():
    mod = load_build()
    labels = data()["labels"]
    out = mod.render_care([{"risk": "A <b>", "what_we_do": "i & j"}])
    assert "<b>" not in out and "&lt;b&gt;" in out and "i &amp; j" in out
    out = mod.render_evidence({"lede": "l <l>", "label": "promising", "items": [
        {"title": "T <b>", "text": "a & b", "label": None,
         "sources": [{"text": "s <i>", "url": "https://x?a=1&b=2"}]}]}, labels)
    assert "<b>" not in out and "<i>" not in out and "<l>" not in out
    assert "a &amp; b" in out and "a=1&amp;b=2" in out
    choose = dict(data()["choose"], follow_up='say "hi" & <go> →')
    out = mod.render_choose(choose)
    assert "<go>" not in out and "&lt;go&gt;" in out
    assert copy_values(out) == [choose["follow_up"]]


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
