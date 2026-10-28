"""Vakter för sidan Side by Side (/side-by-side/).

Parkorten, evidensen, åldersreglerna och gymnasievarianten byggs från
side-by-side/pairs-en.json (och åldersreglerna från
thinking-moves/moves-en.json) av scripts/build-side-by-side.py, så att de
syns utan JavaScript. Testerna läser den byggda sidan och kör byggskriptet.
Spec: docs/superpowers/specs/2026-10-28-side-by-side-design.md.
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
PAGE = ROOT / "side-by-side/index.html"
DATA = ROOT / "side-by-side/pairs-en.json"
TM_DATA = ROOT / "thinking-moves/moves-en.json"
BUILD = ROOT / "scripts/build-side-by-side.py"

ORDER = ["two-ways", "right-and-wrong", "one-change", "confusable-concepts", "two-sources"]
SECTIONS = ["sb-builder", "sb-how", "sb-pairs", "sb-variant", "sb-evidence", "sb-age", "sb-download"]
EASIER_ONLY = "Easier to see only: AI tools could not build this pair reliably at the harder level."
COLUMNS = [("only_a", "Only A"), ("both", "Both"), ("only_b", "Only B")]


def html():
    return PAGE.read_text(encoding="utf-8")


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def section(section_id):
    m = re.search(rf'<section[^>]*id="{section_id}".*?</section>', html(), re.S)
    assert m, section_id
    return m.group(0)


def cards():
    return re.findall(r'<article class="tm-move sb-pair"[^>]*>.*?</article>', html(), re.S)


def load_build():
    spec = importlib.util.spec_from_file_location("build_side_by_side", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_five_cards_in_order():
    ids = re.findall(r'<article class="tm-move sb-pair" id="([^"]+)" data-pair-id="\1"', html())
    assert ids == ORDER


def test_card_shows_icon_look_for_and_example_key():
    for pair, card in zip(data()["pairs"], cards()):
        assert f'src="/side-by-side/icons/{pair["id"]}.svg"' in card, pair["id"]
        for item in pair["look_for"]:
            assert esc(item) in card, item
        details = re.search(r"<details.*?</details>", card, re.S).group(0)
        ex = pair["example"]
        for key in ("task", "a_label", "b_label", "rule", "case_c", "case_c_answer", "probe", "think_back"):
            assert esc(ex[key]) in details, (pair["id"], key)
        for line in ex["a"].splitlines() + ex["b"].splitlines():
            assert esc(line) in details, (pair["id"], line)
        for key, heading in COLUMNS:
            assert f">{heading}<" in details and esc(ex[key]) in details, (pair["id"], key)


def test_example_items_sit_in_a_pair():
    for card in cards():
        pair = re.search(r'<div class="sb-ab">(.*?)</div></div>', card, re.S)
        assert pair, card[:80]
        assert pair.group(0).count('class="sb-item"') == 2


def test_build_is_idempotent():
    mod = load_build()
    mod.build(ROOT)
    first = PAGE.read_bytes()
    mod.build(ROOT)
    assert PAGE.read_bytes() == first
    assert len(cards()) == 5


def test_json_text_is_escaped():
    mod = load_build()
    pair = dict(data()["pairs"][0], name="A <b>", look_for=["<i>s</i>", "t"])
    pair["example"] = dict(pair["example"], a="<script>x</script>", task="<q>")
    out = mod.render_pair_card(pair, data()["levels"], data()["labels"])
    assert "<b>" not in out and "&lt;b&gt;" in out
    assert "<script>" not in out and "<i>s</i>" not in out


def test_page_has_required_sections():
    for sid in SECTIONS:
        assert re.search(rf'<section[^>]*id="{sid}"', html()), sid


def test_evidence_labels_and_toolkit_link():
    ev = section("sb-evidence")
    assert ">Strong<" in ev and ">Promising<" in ev
    assert 'href="/evidence/"' in ev
    assert "not a single use" in ev


def test_sources_list_every_url():
    d = data()
    ev = section("sb-evidence")
    urls = [s["url"] for e in d["evidence"] for s in e["sources"]] + [s["url"] for s in d["context"]["sources"]]
    for url in urls:
        assert esc(url) in ev, url


def test_age_rules_match_thinking_moves():
    age = section("sb-age")
    for rule in json.loads(TM_DATA.read_text(encoding="utf-8"))["age_rules"]:
        assert esc(rule["rule"]) in age, rule["tool"]
    assert "national" in age and "school policy" in age


def test_easier_only_line_shown_iff_harder_ok_false():
    mod = load_build()
    for pair, card in zip(data()["pairs"], cards()):
        assert (EASIER_ONLY in card) == (not pair["harder_ok"]), pair["id"]
    pair = dict(data()["pairs"][0], harder_ok=False)
    assert EASIER_ONLY in mod.render_pair_card(pair, data()["levels"], data()["labels"])


def test_download_links_both_pdfs():
    dl = section("sb-download")
    assert 'href="/assets/pdfs/free/side-by-side-sheet-en.pdf"' in dl
    assert 'href="/assets/pdfs/free/side-by-side-cards-en.pdf"' in dl


def test_privacy_line_visible():
    assert "Do not include student names or student work" in section("sb-builder")


def test_use_links_name_their_pair():
    for pair, card in zip(data()["pairs"], cards()):
        assert f'href="?pair={pair["id"]}#sb-builder"' in card
        assert f'data-use-pair="{pair["id"]}"' in card
        assert f'aria-label="Use this pair: {esc(pair["name"])}"' in card, pair["id"]


def test_variant_shows_student_prompt_and_rules():
    variant = section("sb-variant")
    assert esc(data()["variant"]["student_prompt"]) in variant
    assert "approved" in variant and "age rules" in variant


def test_hero_promise_and_back_link():
    hero = re.search(r'<section class="page-hero.*?</section>', html(), re.S).group(0)
    assert 'href="/think/"' in hero
    assert "About 10 minutes to prepare, 15 minutes in class, no student devices needed" in hero


def test_how_section_says_students_go_first():
    how = section("sb-how")
    assert "FOR STUDENTS" in how
    assert "before" in how and "rule" in how


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


def test_example_pair_side_by_side_and_stacks(site, browser):
    # Exemplet ska vara ett riktigt par: A och B bredvid varandra på datorn,
    # under varandra på mobilen utan att sidan går att skrolla i sidled.
    for width in (1280, 390):
        p = browser.new_page(viewport={"width": width, "height": 900})
        p.goto(f"{site}/side-by-side/", wait_until="networkidle")
        p.click("#two-ways summary")
        a, b = (box.bounding_box() for box in p.locator("#two-ways .sb-item").all())
        if width == 1280:
            assert abs(a["y"] - b["y"]) < 1 and b["x"] > a["x"] + a["width"] - 1, (a, b)
        else:
            assert b["y"] >= a["y"] + a["height"] - 1, (a, b)
            assert p.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
        p.close()
