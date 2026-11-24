"""Vakter för sidan Paperwork Pack (/paperwork-pack-f388fd9f/).

Sidan är bara för Skool-medlemmar: den nås via en dold länk och länkas aldrig
från resten av sajten. Mallar, prompter, forskning och varningar byggs från
paperwork-pack-f388fd9f/paperwork-en.json av scripts/build-paperwork-pack.py,
så att de syns utan JavaScript. Kopieringsknapparna är sajtens egna (data-copy
+ copy-to-clipboard.js); sidan har ingen egen JavaScript.
Spec: docs/superpowers/specs/2026-11-23-paperwork-pack-design.md, del C.
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
SLUG = "paperwork-pack-f388fd9f"
PAGE = ROOT / SLUG / "index.html"
DATA = ROOT / SLUG / "paperwork-en.json"
BUILD = ROOT / "scripts/build-paperwork-pack.py"
CSS = ROOT / "assets/css/paperwork-pack.css"

SECTIONS = ["pp-meetings", "pp-admin", "pp-parents", "pp-evidence", "pp-care", "pp-next"]
COURSE_SECTIONS = ["pp-meetings", "pp-admin", "pp-parents"]
MARKERS = ["hero-example", "meetings", "admin", "parents", "evidence", "care"]
LABEL_NAMES = {"strong": "Strong", "promising": "Promising", "framework": "Framework",
               "choosewise": "Choosewise"}
PRIVACY_PAGE = "Do not include student names or student work."
BRACKETS = "Fill in the brackets afterwards, outside AI."
PRIVACY_COPY = "Do not include student names or student work in this conversation."
HERO_LEDE = ("One-page templates for meetings, administration and messages home, and a few prompts "
             "to make your own. Cut first, then standardise what is left. Names, grades and details "
             "go in afterwards, outside AI.")
EVIDENCE_LEDE = ("Meetings about one problem and short messages home have promising evidence. "
                 "Cutting administration rests on expert guidance, not trials. We have found no "
                 "controlled study of AI for report writing or parent communication by school teachers.")
COUNTRY_ADMIN = ("Rules differ between countries. Check what applies where you work before you "
                 "stop keeping a record or change what you document.")
COUNTRY_PARENTS = ("Rules differ between countries. Check what applies where you work before you "
                   "send messages home, store parents' contact details or translate for families.")
NEXT_HREFS = ["/what-teachers-do-354716b7/", "/quality-ladder-ec1c2f8c/#ql-policy",
              "/prompts/lead-teachers/", "/two-minute-debrief/", "/test-countdown/",
              "/homework-upgrade-1f0cd17c/", "https://www.skool.com/choosewise-7103"]


def html():
    return PAGE.read_text(encoding="utf-8")


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def section(sid):
    m = re.search(rf'<section[^>]*id="{sid}".*?</section>', html(), re.S)
    assert m, sid
    return m.group(0)


def text_of(fragment):
    """Texten i ett HTML-stycke: taggar borta, tecken avkodade, blanksteg samlade."""
    no_tags = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", unescape(no_tags)).strip()


def load_build():
    spec = importlib.util.spec_from_file_location("build_paperwork_pack", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def all_templates():
    return [t for s in data()["sections"] for t in s["templates"]]


def all_prompts():
    return [p for s in data()["sections"] for p in s["prompts"]]


def copy_values(fragment):
    """Alla data-copy-värden i ordning, lästa av en riktig HTML-tolkare."""
    found = []

    class Grab(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == "button" and dict(attrs).get("data-copy"):
                found.append(dict(attrs)["data-copy"])

    Grab().feed(fragment)
    return found


# ───── Sidans byggstenar ─────

def test_sections_in_order():
    ids = re.findall(r'<section[^>]*id="(pp-[a-z]+)"', html())
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
    assert "<h1>Paperwork Pack</h1>" in page
    assert '<a class="tm-back" href="/what-teachers-do-354716b7/">← What teachers do</a>' in page
    assert HERO_LEDE in text_of(page)
    assert ">What a template looks like</h2>" in page


def test_hero_example_has_every_line_and_its_job():
    block = re.search(r"<!-- hero-example:start -->(.*?)<!-- hero-example:end -->", html(), re.S).group(1)
    lines = data()["hero"]["lines"]
    assert len(lines) == 5
    for line in lines:
        assert escape(line["text"]) in block and escape(line["job"]) in block, line["text"]


def test_jump_links():
    page = html()
    for href, label in (("#pp-meetings", "Meetings about teaching"),
                        ("#pp-admin", "Administration"), ("#pp-parents", "Messages home")):
        assert re.search(rf'<a href="{href}">{label}</a>', page), href


def test_course_anchors_exist():
    page = html()
    for sid in COURSE_SECTIONS:
        assert re.search(rf'<section[^>]*id="{sid}"', page), sid


def test_section_headings_and_labels():
    expected = {"pp-meetings": ("Meetings about teaching", "promising"),
                "pp-admin": ("Administration", "framework"),
                "pp-parents": ("Messages home", "promising")}
    for sid, (title, label) in expected.items():
        block = section(sid)
        assert f'class="section__title">{title}</h2>' in block, sid
        assert f'<span class="tm-chip tm-chip--{label}">{LABEL_NAMES[label]}</span>' in block, sid
        # Etiketten står överst, före det byggda innehållet.
        assert block.index("tm-chip") < block.index("<!-- " + sid[3:] + ":start -->"), sid
    # Paperwork Pack som helhet får ingen etikett: hero har inget chip.
    hero = html()[:html().index('id="pp-meetings"')]
    assert "tm-chip" not in hero
    # Själva protokollet är ett Framework, och det sägs i avsnittet om möten.
    assert "the protocol itself" in text_of(section("pp-meetings"))
    assert 'tm-chip--framework">Framework</span>' in section("pp-meetings")


def test_privacy_line_in_each_section():
    for sid in COURSE_SECTIONS:
        block = section(sid)
        shown = text_of(block)
        assert f"{PRIVACY_PAGE} {BRACKETS}" in shown, sid
        privacy_at = block.index(PRIVACY_PAGE)
        assert privacy_at < block.index('class="pp-prompt"'), sid
        # Raden står en gång per avsnitt, ovanför prompterna.
        assert block.count(PRIVACY_PAGE) == 1, sid


def test_prompts_are_marked_as_writing_aids():
    """Samma rad en gång per avsnitt, direkt under rubriken över prompterna."""
    line = "These prompts are writing aids, not evidence-based methods."
    for sid in COURSE_SECTIONS:
        block = section(sid)
        assert text_of(block).count(line) == 1, sid
        assert block.index("Prompts to make your own") < block.index(line) < block.index('class="pp-prompt"'), sid


def test_evidence_absence_claim_names_school_teachers():
    ai = next(e for e in data()["evidence"] if e["title"] == "AI for these tasks")
    assert ("We have found no controlled study of AI for report writing or parent "
            "communication by school teachers.") in ai["text"]


# ───── Mallarna och prompterna ─────

def test_template_copy_buttons():
    mod = load_build()
    for t in all_templates():
        sid = next(s["id"] for s in data()["sections"] if t in s["templates"])
        block = section(sid)
        assert mod.template_text(t) in copy_values(block), t["id"]
        assert f'<a href="{t["file"]}" download>' in block, t["id"]


def test_template_text_shape():
    mod = load_build()
    t = next(t for t in all_templates() if t["id"] == "meeting-protocol")
    text = mod.template_text(t)
    assert text.startswith(t["title"] + "\n\n" + t["intro"] + "\n\n")
    for block in t["blocks"]:
        assert block["heading"] in text
        for line in block["lines"]:
            assert line in text
    # Ett tabellblock blir rubriken och kolumnnamnen på en rad.
    assert "Decision log\nDate | Decision | Result" in text
    for t in all_templates():
        out = mod.template_text(t)
        assert "<" not in out and "&amp;" not in out


def test_table_blocks_are_real_tables():
    d = data()
    for s in d["sections"]:
        block = section(s["id"])
        for t in s["templates"]:
            for b in t["blocks"]:
                if "columns" not in b:
                    continue
                m = re.search(rf'<h4[^>]*>{re.escape(escape(b["heading"]))}</h4>\s*<div class="pp-table-wrap"><table class="pp-table">(.*?)</table>',
                              block, re.S)
                assert m, b["heading"]
                head = re.findall(r"<th\b[^>]*>(.*?)</th>", m.group(1), re.S)
                assert head == [escape(c) for c in b["columns"]], b["heading"]
                body = re.search(r"<tbody>(.*?)</tbody>", m.group(1), re.S).group(1)
                assert len(re.findall(r"<tr>", body)) == b["rows"], b["heading"]
                for c in b["columns"]:
                    assert f'data-label="{escape(c)}"' in body, c


def test_message_copy_buttons():
    """Varje meddelande hem har en egen knapp som kopierar meddelandet och avsändarraden,
    inte rubriken; knappen står direkt efter meddelandet."""
    mod = load_build()
    t = next(t for t in all_templates() if t["id"] == "messages-home")
    block = section("pp-parents")
    messages = [b for b in t["blocks"] if b.get("copy")]
    assert len(messages) == 4
    for b in messages:
        assert mod.message_text(b) == "\n".join(b["lines"])
        assert mod.message_text(b) in copy_values(block), b["heading"]
        m = re.search(rf'<h4[^>]*>{re.escape(escape(b["heading"]))}</h4>.*?</div></div>', block, re.S)
        assert m and ">Copy message</button>" in m.group(0), b["heading"]
        assert 'class="btn btn--secondary" data-copy' in m.group(0), b["heading"]
    assert block.count(">Copy message</button>") == 4


def test_every_table_has_a_phone_note():
    mod = load_build()
    tables = [b for t in all_templates() for b in t["blocks"] if "columns" in b]
    page = html()
    note = f'<p class="pp-table__note">{escape(mod.TABLE_NOTE)}</p>'
    assert page.count(note) == len(tables) == 3
    assert page.count("</table></div>" + note) == 3
    assert ".docx" not in mod.TABLE_NOTE and "Word file" in mod.TABLE_NOTE


def test_cut_first_checks_and_note():
    t = next(t for t in all_templates() if t["id"] == "cut-first-checklist")
    headings = [b["heading"] for b in t["blocks"]]
    assert headings == ["Our recurring documents", "Five checks, with examples from England",
                        "Where these come from"]
    checks = t["blocks"][1]
    assert len(checks["lines"]) == 5
    assert t["blocks"][2]["box"] is False


def test_prompt_copy_buttons():
    mod = load_build()
    for s in data()["sections"]:
        block = section(s["id"])
        values = copy_values(block)
        for p in s["prompts"]:
            expected = mod.prompt_text(p)
            assert expected in values, p["id"]
            assert expected.startswith(PRIVACY_COPY + "\n\n"), p["id"]
            assert expected == PRIVACY_COPY + "\n\n" + p["body"]
            assert escape(p["body"]) in block, p["id"]
    assert mod.PRIVACY_COPY == PRIVACY_COPY
    assert len(all_prompts()) == 7


def test_data_copy_survives_a_real_parser():
    """Citattecken, &, → och radbrytningar i data-copy ska överleva HTML-tolkaren."""
    mod = load_build()
    expected = []
    for s in data()["sections"]:
        expected += [mod.template_text(t) for t in s["templates"]]
        expected += [mod.prompt_text(p) for p in s["prompts"]]
        expected += [mod.message_text(b) for t in s["templates"] for b in t["blocks"] if b.get("copy")]
    found = []
    for sid in COURSE_SECTIONS:
        found += copy_values(section(sid))
    assert sorted(found) == sorted(expected)
    assert len(found) == len(expected) == 6 + 7 + 4


def test_copy_buttons_are_followed_by_a_toast():
    for sid in COURSE_SECTIONS:
        block = section(sid)
        buttons = len(re.findall(r"<button[^>]*data-copy", block))
        toasts = len(re.findall(r'</button><span class="copy-toast" role="status">Copied</span>', block))
        assert buttons == toasts and buttons > 0, sid


def test_country_lines_placed():
    assert COUNTRY_ADMIN in text_of(section("pp-admin"))
    assert COUNTRY_PARENTS in text_of(section("pp-parents"))
    assert "Rules differ between countries" not in section("pp-meetings")
    assert COUNTRY_ADMIN not in section("pp-parents")


def test_feedback_policy_link():
    block = section("pp-admin")
    assert 'href="/quality-ladder-ec1c2f8c/#ql-policy"' in block


# ───── Forskning, försiktighet och nästa steg ─────

def test_evidence_and_legend():
    d = data()
    block = section("pp-evidence")
    assert ">What the research says</h2>" in block
    assert EVIDENCE_LEDE in text_of(block)
    assert block.index(EVIDENCE_LEDE) < block.index("<!-- evidence:start -->")
    legend = re.search(r'<ul class="tm-legend">.*?</ul>', block, re.S).group(0)
    assert len(re.findall("<li>", legend)) == 4
    for key, name in LABEL_NAMES.items():
        assert (f'<span class="tm-chip tm-chip--{key}">{name}</span> '
                f'{escape(d["labels"][key]["definition"])}') in legend, key
    assert len(re.findall(r'class="pp-evidence__item"', block)) == len(d["evidence"]) == 7
    items = block.split('class="pp-evidence__item"')[1:]
    for item, e in zip(items, d["evidence"]):
        assert f"<strong>{escape(e['title'])}</strong>" in item
        assert escape(e["text"]) in item
        if e["label"]:
            assert f'<span class="tm-chip tm-chip--{e["label"]}">{LABEL_NAMES[e["label"]]}</span>' in item
        else:
            assert "tm-chip" not in item, e["title"]
        for s in e["sources"]:
            assert f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' in item, s["url"]


def test_care_section():
    block = section("pp-care")
    assert ">Watch out for</h2>" in block
    care = data()["care"]
    assert len(re.findall(r"<li>", block)) == len(care) == 5
    for c in care:
        assert escape(c["risk"]) in block and escape(c["what_we_do"]) in block, c["risk"]


def test_next_links():
    block = section("pp-next")
    assert ">Next</h2>" in block
    assert re.findall(r'href="([^"]+)"', block) == NEXT_HREFS
    shown = text_of(block)
    for label in ("Back to the overview: What teachers do", "Feedback policy: Quality Ladder",
                  "Prompt pack for lead teachers", "Exit tickets for the meeting: Two-Minute Debrief",
                  "Texts for home: Test Countdown", "Homework Upgrade"):
        assert label in shown, label


# ───── Sidan som helhet ─────

def test_page_head():
    page = html()
    assert "<title>Paperwork Pack — Choosewise</title>" in page
    assert '<meta name="description" content="' in page
    assert '<link rel="stylesheet" href="/assets/css/paperwork-pack.css?v=20261123a">' in page
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
    assert "paperwork-pack.js" not in page


def test_json_text_is_escaped():
    mod = load_build()
    out = mod.render_care([{"risk": "A <b>", "what_we_do": "i & j"}])
    assert "<b>" not in out and "&lt;b&gt;" in out and "i &amp; j" in out
    labels = data()["labels"]
    out = mod.render_evidence([{"title": "T <b>", "text": "a & b", "label": "strong",
                                "sources": [{"text": "s <i>", "url": "https://x?a=1&b=2"}]}], labels)
    assert "<b>" not in out and "<i>" not in out and "a &amp; b" in out and "a=1&amp;b=2" in out
    section_data = {"id": "pp-x", "title": "T", "lesson": 5, "intro": "i <b> & j",
                    "templates": [{"id": "t", "title": "T <i>", "file": "t.docx", "intro": "x & y",
                                   "blocks": [{"heading": "H <u>", "lines": ["l <s> & m"], "box": True},
                                              {"heading": "Tab & co", "columns": ["A <a>", "B"],
                                               "rows": 2, "lines": [], "box": False}]}],
                    "prompts": [{"id": "P9", "title": "P <b>", "body": "say \"hi\" & <go> →\nnext",
                                 "reused_from": None}],
                    "links": [{"text": "L <l>", "href": "/a?b=1&c=2"}], "country_line": "c <c> & d"}
    out = mod.render_section(section_data)
    for bad in ("<b>", "<i>", "<u>", "<s>", "<a>", "<go>", "<l>", "<c>"):
        assert bad not in out, bad
    assert "i &lt;b&gt; &amp; j" in out and 'href="/a?b=1&amp;c=2"' in out
    assert "&quot;hi&quot; &amp; &lt;go&gt;" in out
    # Rubrikerna i ett tabellblock skrivs ut som text, och radbrytningen i data-copy överlever.
    assert copy_values(out)[0] == mod.template_text(section_data["templates"][0])
    assert copy_values(out)[1] == mod.prompt_text(section_data["prompts"][0])


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
        # Kommentaren står rakt före sektionen: hitta den sista </section> före och titta efter den.
        prev = before.rfind("</section>")
        gap = before[prev if prev != -1 else 0:]
        comments = re.findall(r"<!--(.*?)-->", gap, re.S)
        explaining = [c for c in comments if not re.match(r"\s*[a-z-]+:(start|end)\b", c)]
        assert explaining, sid


def test_font_weights_only_from_tokens():
    css = CSS.read_text(encoding="utf-8")
    assert not re.search(r"font-weight:\s*\d", css)


# ───── Fyllbara tabeller i telefonläge ─────

@pytest.fixture(scope="module")
def site():
    """Lokal server på ledig port: sidans CSS ligger på absoluta sökvägar, så file:// räcker inte."""
    import functools
    import http.server
    import socketserver
    import threading

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):  # sviten ska vara tyst
            pass

    class Server(socketserver.TCPServer):
        allow_reuse_address = True

    srv = Server(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()


COUNT_VISIBLE_ROWS = """() => [...document.querySelectorAll('.pp-table')].map(t => ({
    total: t.querySelectorAll('tbody tr').length,
    visible: [...t.querySelectorAll('tbody tr')].filter(r => getComputedStyle(r).display !== 'none').length,
    note: getComputedStyle(t.closest('.pp-block').querySelector('.pp-table__note')).display !== 'none'
}))"""


def test_fill_in_tables_show_one_row_on_a_phone_and_all_rows_on_desktop(site):
    """Vid 390 px visas exakt en tom rad per tabell (annars blir det långa stackar av identiska kort)
    och raden om Word-filen; vid 1280 px syns alla rader men inte raden, och alla rader finns kvar i HTML:en."""
    sync_api = pytest.importorskip("playwright.sync_api")
    with sync_api.sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            for width, phone in ((390, True), (1280, False)):
                page = browser.new_page(viewport={"width": width, "height": 900})
                page.goto(f"{site}/{SLUG}/")
                tables = page.evaluate(COUNT_VISIBLE_ROWS)
                assert len(tables) == 3, tables
                for t in tables:
                    assert t["total"] >= 4, (width, t)
                    assert t["visible"] == (1 if phone else t["total"]), (width, t)
                    # Raden om Word-filen syns bara när raderna är gömda.
                    assert t["note"] is phone, (width, t)
                page.close()
        finally:
            browser.close()
