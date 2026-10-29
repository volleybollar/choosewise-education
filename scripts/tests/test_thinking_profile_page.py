"""Vakter för sidan Thinking Profile (/thinking-profile/).

Trappkorten, exemplet, evidensen, källorna och åldersreglerna byggs från
thinking-profile/ladders-en.json (namn och etiketter från
thinking-moves/moves-en.json och side-by-side/pairs-en.json) av
scripts/build-thinking-profile.py, så att de syns utan JavaScript.
"""
import functools
import http.server
import importlib.util
import json
import re
import socketserver
import threading
from html import escape as esc
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "thinking-profile/index.html"
DATA = ROOT / "thinking-profile/ladders-en.json"
TM_DATA = ROOT / "thinking-moves/moves-en.json"
SB_DATA = ROOT / "side-by-side/pairs-en.json"
BUILD = ROOT / "scripts/build-thinking-profile.py"

ORDER = ["generating", "evaluating", "comparing", "explaining", "causes", "regulating"]
SECTIONS = ["tp-why", "tp-ladders", "tp-builder", "tp-how", "tp-example", "tp-evidence", "tp-age", "tp-download"]


def html():
    return PAGE.read_text(encoding="utf-8")


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def tm():
    return json.loads(TM_DATA.read_text(encoding="utf-8"))


def section(section_id):
    m = re.search(rf'<section[^>]*id="{section_id}".*?</section>', html(), re.S)
    assert m, section_id
    return m.group(0)


def cards():
    return re.findall(r'<article class="tm-move tp-ladder"[^>]*>.*?</article>', html(), re.S)


def load_build():
    spec = importlib.util.spec_from_file_location("build_thinking_profile", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def task_names():
    names = {m["id"]: m["name"] for m in tm()["moves"]}
    names.update({p["id"]: p["name"] for p in json.loads(SB_DATA.read_text(encoding="utf-8"))["pairs"]})
    return names


def test_six_ladder_cards_in_order():
    ids = re.findall(r'<article class="tm-move tp-ladder" id="([^"]+)" data-cluster="\1"', html())
    assert ids == ORDER


def test_card_shows_steps_and_trained_by():
    clusters = {c["id"]: c for c in tm()["clusters"]}
    moves = task_names()
    tool_names = {"flawed-answer": "Flawed Answer", "side-by-side": "Side by Side"}
    for ladder, card in zip(data()["ladders"], cards()):
        cluster = clusters[ladder["cluster"]]
        assert esc(cluster["name"]) in card and esc(cluster["description"]) in card
        assert f'src="{ladder["icon"]}"' in card
        ol = re.search(r"<ol.*?</ol>", card, re.S).group(0)
        assert ol.count("<li>") == 4
        for step in ladder["steps"]:
            assert esc(step["text"]) in ol, step["text"]
        trained = re.search(r'class="tp-trained".*?</p>', card, re.S).group(0)
        for task in ladder["tasks"]:
            name = moves[task["id"]] if "id" in task else tool_names[task["tool"]]
            assert esc(name) in trained, (ladder["cluster"], name)


def test_build_is_idempotent():
    mod = load_build()
    mod.build(ROOT)
    first = PAGE.read_bytes()
    mod.build(ROOT)
    assert PAGE.read_bytes() == first
    assert len(cards()) == 6


def test_json_text_is_escaped():
    mod = load_build()
    d = data()
    clusters = {c["id"]: c for c in tm()["clusters"]}
    ladder = dict(d["ladders"][0], steps=[dict(s, text="<b>x</b>") for s in d["ladders"][0]["steps"]])
    out = mod.render_ladder_card(ladder, clusters["generating"], task_names(), {})
    assert "<b>" not in out and "&lt;b&gt;" in out
    ex = dict(d["example"], thread="<script>x</script>")
    assert "<script>" not in mod.render_example(ex)


def test_page_has_required_sections():
    for sid in SECTIONS:
        assert re.search(rf'<section[^>]*id="{sid}"', html()), sid


def test_not_graded_and_honesty_sentences_shown():
    d = data()
    assert esc(d["not_graded"]) in section("tp-how")
    assert esc(d["honesty"]) in section("tp-evidence")


def test_evidence_labels_and_toolkit_link():
    ev = section("tp-evidence")
    assert ">Strong<" in ev and ">Promising<" in ev and ">Framework<" in ev
    assert 'href="/evidence/"' in ev
    assert "not a single use" in ev


def test_sources_list_every_url():
    ev = section("tp-evidence")
    for e in data()["evidence"]:
        for s in e["sources"]:
            assert esc(s["url"]) in ev, s["url"]


def test_age_rules_match_thinking_moves():
    age = section("tp-age")
    for rule in tm()["age_rules"]:
        assert esc(rule["rule"]) in age, rule["tool"]
    assert "national" in age and "school policy" in age


def test_example_lists_plan_with_builder_links():
    ex = data()["example"]
    sec = section("tp-example")
    assert esc(ex["thread"]) in sec and esc(ex["tell_students"]) in sec
    assert esc(ex["students_note"]) in sec
    for item in ex["plan"]:
        assert esc(item["what"]) in sec, item["week"]
        assert f'href="{item["url"]}"' in sec, item["url"]
        for line in item["inputs"]:
            assert esc(line) in sec, line
    for s in ex["students"]:
        for key in ("answer", "shows", "next"):
            assert esc(s[key]) in sec, (s["name"], key)
    assert len(re.findall(r'class="tp-plan__week"', sec)) == len(ex["plan"])


def test_downloads_are_gated_and_keep_href():
    dl = section("tp-download")
    for kind, title in (("deck", "ladder deck"), ("sheets", "self-check sheets")):
        pdf = f"/assets/pdfs/free/thinking-profile-{kind}-en.pdf"
        tag = re.search(rf'<a [^>]*data-gate="thinking-profile-{kind}-en"[^>]*>', dl)
        assert tag, kind
        tag = tag.group(0)
        assert f'href="{pdf}"' in tag and f'data-gate-pdf="{pdf}"' in tag
        assert f'data-gate-title="Get the {title} (PDF)"' in tag
        assert 'class="btn btn--primary"' in tag
    assert re.search(r'<script type="module" src="/assets/js/mailerlite-gate.js"[^>]*>', html())


def test_privacy_line_visible():
    assert "Do not include student names or student work in this conversation." in section("tp-builder")


def test_builder_form_has_task4_ids():
    b = section("tp-builder")
    for i in ("tp-form", "tp-cluster", "tp-subject", "tp-grade", "tp-weeks", "tp-topic",
              "tp-overview", "tp-prompt", "tp-copy", "tp-hint"):
        assert f'id="{i}"' in b, i
    values = re.findall(r'<option value="([^"]*)"', re.search(r'<select[^>]*id="tp-cluster".*?</select>', b, re.S).group(0))
    assert values == [""] + ORDER
    assert re.search(r'<input[^>]*id="tp-weeks"[^>]*min="3"[^>]*max="8"[^>]*value="6"', b)
    assert 'id="tp-prompt"' in b and re.search(r"<textarea[^>]*id=\"tp-prompt\"[^>]*readonly", b)
    assert re.search(r'<button[^>]*id="tp-copy"[^>]*disabled', b)


def test_use_links_name_their_cluster():
    clusters = {c["id"]: c for c in tm()["clusters"]}
    for ladder, card in zip(data()["ladders"], cards()):
        cid = ladder["cluster"]
        assert f'href="?cluster={cid}#tp-builder"' in card
        assert f'data-use-cluster="{cid}"' in card
        assert f'aria-label="Plan with this ladder: {esc(clusters[cid]["name"])}"' in card


def test_hero_promise_and_back_link():
    hero = re.search(r'<section class="page-hero.*?</section>', html(), re.S).group(0)
    assert 'href="/think/"' in hero
    assert "One kind of thinking, one unit. A plan in about 30 minutes, two minutes of self-check after each task." in hero


@pytest.fixture(scope="module")
def site():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    class Server(socketserver.TCPServer):
        allow_reuse_address = True

    srv = Server(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()


@pytest.fixture(scope="module")
def browser():
    pw = pytest.importorskip("playwright.sync_api").sync_playwright().start()
    b = pw.chromium.launch()
    yield b
    b.close()
    pw.stop()


def test_ladder_cards_side_by_side_are_equal_height(site, browser):
    # Kort bredvid varandra är lika höga och "Plan with this ladder" ligger
    # sist och på en rad.
    for width in (1280, 900):
        p = browser.new_page(viewport={"width": width, "height": 900})
        p.goto(f"{site}/thinking-profile/", wait_until="networkidle")
        boxes = p.evaluate("""() => [...document.querySelectorAll('.tp-ladder')].map(c => {
            const r = c.getBoundingClientRect(), l = c.querySelector('.tm-move__use');
            const lr = l.getBoundingClientRect();
            const lh = parseFloat(getComputedStyle(l).lineHeight) || 20;
            return {top: Math.round(r.top + scrollY), h: r.height, linkTop: lr.top + scrollY,
                    linkH: lr.height, lh, last: c.lastElementChild === l};
        })""")
        rows = {}
        for b in boxes:
            rows.setdefault(b["top"], []).append(b)
        assert any(len(r) > 1 for r in rows.values()), width
        for row in rows.values():
            assert max(b["h"] for b in row) - min(b["h"] for b in row) < 1.5, (width, row)
            assert max(b["linkTop"] for b in row) - min(b["linkTop"] for b in row) < 1.5, (width, row)
        for b in boxes:
            assert b["last"] and b["linkH"] < b["lh"] * 1.6, (width, b)
        p.close()


def test_retell_quote_has_lead_in_and_week_five_names_its_tool():
    html = PAGE.read_text(encoding="utf-8") if "PAGE" in globals() else (ROOT / "thinking-profile/index.html").read_text(encoding="utf-8")
    lead = "How you might retell it to a colleague:"
    assert lead + "</p>\n<blockquote class=\"tp-tell\">" + esc(data()["intro"]["retell"]) in html
    assert "Week 5 · Side by Side: One thing changed" in html


def test_grades_start_at_8():
    # Johans beslut 2026-10-29: Thinking Profile gäller åk 8–12, som
    # Thinking Moves och Flawed Answer.
    html = (ROOT / "thinking-profile/index.html").read_text(encoding="utf-8")
    grades = re.findall(r'<option value="(\d+)"[^>]*>Grade', html)
    assert grades == ["8", "9", "10", "11", "12"]
    assert "7–12" not in html and "Grades 8–12" in html
    assert "7–12" not in (ROOT / "exports/build-thinking-profile-pdf.py").read_text(encoding="utf-8")


def test_self_assessment_sources_are_cited_directly():
    # Johans beslut 2026-10-29: en källa står bara i listan om texten hänvisar
    # direkt till den (Brown & Harris togs bort när de bara citerades via Andrade).
    data = json.loads((ROOT / "thinking-profile/ladders-en.json").read_text(encoding="utf-8"))
    for ev in data["evidence"]:
        if not ev["claim"].startswith("Self-assessment"):
            continue
        for src in ev["sources"]:
            author = src["text"].split(",")[0].split(" 20")[0].split(" ")[0]
            assert author in ev["text"], (ev["claim"], src["text"])


def test_example_headings_and_step_label():
    # Rubrikerna i exemplet följer på varandra (h3 → h4), och veckoraden säger
    # "room for step" som prompten och lärarhäftet.
    html = (ROOT / "thinking-profile/index.html").read_text(encoding="utf-8")
    assert "<h5" not in html and html.count('<div class="tp-student"><h4>') == 2
    assert "aim: step" not in html and html.count("· room for step ") == 6
