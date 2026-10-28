"""Vakter för de två PDF:erna till Thinking Profile.

Trappkortleken (thinking-profile-deck-en.pdf) har 9 sidor: framsida, sex
stegsidor, det genomarbetade exemplet och promptkortet. Självskattnings-
bladen (thinking-profile-sheets-en.pdf) är sex A4-sidor, en per kluster.
Båda byggs av exports/build-thinking-profile-pdf.py från ladders-en.json,
tankeförflyttningarna och partyperna.
"""
import importlib.util
import json
import re
import subprocess
from pathlib import Path

import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
DECK = ROOT / "assets/pdfs/free/thinking-profile-deck-en.pdf"
SHEETS = ROOT / "assets/pdfs/free/thinking-profile-sheets-en.pdf"
DECK_SRC = ROOT / "_unpublished/exports/thinking-profile-deck-a4-en.html"
SHEETS_SRC = ROOT / "_unpublished/exports/thinking-profile-sheets-a4-en.html"
BUILD = ROOT / "exports/build-thinking-profile-pdf.py"
DATA = ROOT / "thinking-profile/ladders-en.json"
JS = ROOT / "assets/js/thinking-profile.js"


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def moves():
    return json.loads((ROOT / "thinking-moves/moves-en.json").read_text(encoding="utf-8"))


def raw(pdf, i):
    return PdfReader(pdf).pages[i].extract_text()


def text(pdf, i):
    # pypdf delar ibland ord och CSS-versaler kommer ut som versaler, så
    # jämförelserna görs utan blanksteg och skiftlägesokänsligt.
    return re.sub(r"\s+", "", raw(pdf, i)).lower()


def has(needle, haystack):
    return re.sub(r"\s+", "", needle).lower() in haystack


def load_build():
    spec = importlib.util.spec_from_file_location("tp_pdf", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_deck_page_count():
    assert len(PdfReader(DECK).pages) == 9


def test_sheets_page_count():
    assert len(PdfReader(SHEETS).pages) == 6


def test_each_sheet_has_its_ladder_six_rows_and_not_graded():
    d = data()
    names = {c["id"]: c["name"] for c in moves()["clusters"]}
    for i, lad in enumerate(d["ladders"]):
        page = text(SHEETS, i)
        assert has(names[lad["cluster"]], page), lad["cluster"]
        for s in lad["steps"]:
            assert has(s["text"], page), (lad["cluster"], s["text"])
        assert has(d["not_graded"], page), lad["cluster"]
        q = d["self_check"]["questions"]
        for question in q:
            assert page.count(re.sub(r"\s+", "", question).lower()) == 6, (lad["cluster"], question)


def test_regulating_sheet_has_think_back_rule():
    d = data()
    for i, lad in enumerate(d["ladders"]):
        page = text(SHEETS, i)
        assert has(d["regulating_rule"], page) == (lad["cluster"] == "regulating"), lad["cluster"]


def test_deck_cover_has_honesty_and_not_graded():
    d = data()
    cover = text(DECK, 0)
    assert has(d["honesty"], cover) and has(d["not_graded"], cover)
    for q in d["self_check"]["questions"]:
        assert has(q, cover), q
    for name in ("Strong", "Promising", "Framework"):
        assert has(name, cover), name
    for c in moves()["clusters"]:
        assert has(c["name"], cover), c["id"]


def test_deck_ladder_pages_have_steps_shows_and_tasks():
    d = data()
    mv = {m["id"]: m["name"] for m in moves()["moves"]}
    for i, lad in enumerate(d["ladders"]):
        page = text(DECK, i + 1)
        for s in lad["steps"]:
            assert has(s["text"], page) and has(s["shows"], page), (lad["cluster"], s["text"])
        assert has(lad["in_class"], page), lad["cluster"]
        for t in lad["tasks"]:
            name = mv[t["id"]] if t.get("id") else ("Flawed Answer" if t["tool"] == "flawed-answer" else "Side by Side")
            assert has(name, page), (lad["cluster"], name)
        assert has("Evidence", page), lad["cluster"]


def test_deck_example_page():
    ex = data()["example"]
    page = text(DECK, 7)
    assert has(ex["topic"], page) and has(ex["tell_students"], page)
    for w in ex["plan"]:
        assert has(w["what"], page), w["week"]


def _builder_lines():
    """Svarsformatets rader exakt som promptbyggaren skriver dem."""
    js = JS.read_text(encoding="utf-8")
    block = js[js.index("'Reply in plain text"):js.index("return lines.join")]
    lines = [m.group(1) for m in re.finditer(r"^\s*'(.*)',?\s*$", block, re.M)]
    return [line for line in lines if line]


def test_prompt_card_matches_builder_word_for_word():
    mod = load_build()
    builder = _builder_lines()
    assert len(builder) == 11, builder
    assert mod.PROMPT_PARTS == builder
    js = JS.read_text(encoding="utf-8")
    for fixed in (mod.PRIVACY, mod.BUILDER_LINE, mod.FIELDS_LINE):
        assert "'" + fixed + "'" in js, fixed
    assert data()["not_graded"].replace("'", "\\'") in js
    last = text(DECK, 8)
    for line in builder + [mod.PRIVACY, mod.BUILDER_LINE, mod.FIELDS_LINE, data()["not_graded"]]:
        assert has(line, last), line
    for rule in data()["rules"] + data()["rules_regulating"]:
        assert has(rule, last), rule


def test_sources_are_generated_from_json():
    mod = load_build()
    assert mod.render_deck_html(data()) == DECK_SRC.read_text(encoding="utf-8")
    assert mod.render_sheets_html(data()) == SHEETS_SRC.read_text(encoding="utf-8")


@pytest.mark.parametrize("src", [DECK_SRC, SHEETS_SRC], ids=lambda p: p.name)
def test_templates_have_no_hex(src):
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b", src.read_text(encoding="utf-8"))


@pytest.mark.parametrize("src", [DECK_SRC, SHEETS_SRC], ids=lambda p: p.name)
def test_template_comment_is_swedish(src):
    assert "<!-- Genererad av exports/build-thinking-profile-pdf.py" in src.read_text(encoding="utf-8")


@pytest.mark.parametrize("pdf", [DECK, SHEETS], ids=lambda p: p.name)
def test_pdf_fonts_allowed_weights(pdf):
    out = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True, check=True).stdout
    assert "HankenGrotesk" in out
    assert not re.search(r"(SemiBold|Bold|Black|Heavy)", out, re.I), out


@pytest.mark.parametrize("src", [DECK_SRC, SHEETS_SRC], ids=lambda p: p.name)
def test_no_page_overflows(src):
    sync_playwright = pytest.importorskip("playwright.sync_api").sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        p = b.new_page()
        p.goto(src.as_uri(), wait_until="networkidle")
        p.emulate_media(media="print")
        over = p.evaluate("[...document.querySelectorAll('.page')].map((el, i) => [i + 1, el.scrollHeight - el.clientHeight]).filter(x => x[1] > 0)")
        b.close()
    assert over == [], over
