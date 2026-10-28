"""Vakter för de två PDF:erna till Side by Side.

Elevarket (side-by-side-sheet-en.pdf) är elevernas svarsark på en A4-sida,
form B: paret överst, jämförelsen i tre spalter, regeln, fall C och Think
back. Kortleken (side-by-side-cards-en.pdf) har framsida, fem partypkort och
sist luckprompten — 7 sidor. Båda byggs av exports/build-side-by-side-pdf.py
från samma JSON som sidan.
"""
import importlib.util
import json
import re
import subprocess
from pathlib import Path

import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
SHEET = ROOT / "assets/pdfs/free/side-by-side-sheet-en.pdf"
DECK = ROOT / "assets/pdfs/free/side-by-side-cards-en.pdf"
SHEET_SRC = ROOT / "_unpublished/exports/side-by-side-sheet-a4-en.html"
DECK_SRC = ROOT / "_unpublished/exports/side-by-side-cards-a4-en.html"
BUILD = ROOT / "exports/build-side-by-side-pdf.py"
DATA = ROOT / "side-by-side/pairs-en.json"


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def raw(pdf, i):
    return PdfReader(pdf).pages[i].extract_text()


def text(pdf, i):
    # pypdf delar ibland ord och CSS-versaler kommer ut som versaler, så
    # jämförelserna görs utan blanksteg och skiftlägesokänsligt.
    return re.sub(r"\s+", "", raw(pdf, i)).lower()


def has(needle, haystack):
    return re.sub(r"\s+", "", needle).lower() in haystack


def load_build():
    spec = importlib.util.spec_from_file_location("sb_pdf", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_sheet_is_one_page_with_columns_rule_and_case_c():
    assert len(PdfReader(SHEET).pages) == 1
    page = text(SHEET, 0)
    for heading in ("Side by Side", "Only A", "Both", "Only B", "The rule we found",
                    "Try it on case C", "Think back"):
        assert has(heading, page), heading
    # Elevarket säger inte att AI gjorde paret (spec).
    assert not re.search(r"\bAI\b", raw(SHEET, 0))


def test_deck_page_count():
    assert len(PdfReader(DECK).pages) == 7


def test_deck_cover_has_steps_levels_and_legend():
    cover = text(DECK, 0)
    d = data()
    for step in d["steps"]:
        assert has(step["name"], cover), step["name"]
    for level in d["levels"]:
        assert has(level["name"], cover), level["name"]
    assert has("Strong", cover) and has("Promising", cover) and has("not a single use", cover)


def test_deck_cards_have_example_key_and_for_the_ai():
    for i, p in enumerate(data()["pairs"]):
        page = text(DECK, i + 1)
        ex = p["example"]
        assert has(p["name"], page), p["id"]
        for key in ("task", "only_a", "both", "only_b", "rule", "case_c", "case_c_answer", "probe", "think_back"):
            assert has(ex[key], page), (p["id"], key)
        for item in ex["a"].splitlines() + ex["b"].splitlines():
            assert has(item, page), (p["id"], item)
        for item in p["look_for"]:
            assert has(item, page), (p["id"], item)
        assert has("For the AI", page) and has(p["prompt_brief"], page), p["id"]
        assert has("This pair type:", page), p["id"]
        assert has("Easier to see only", page) == (not p["harder_ok"]), p["id"]


def _builder_lines():
    """Regelraden och svarsdelarna exakt som promptbyggaren skriver dem."""
    js = (ROOT / "assets/js/side-by-side.js").read_text(encoding="utf-8")
    block = js[js.index("'Rules:"):js.index("return lines.join")]
    lines = [m.group(1) for m in re.finditer(r"^\s*'(.*)',?\s*$", block, re.M)]
    return [line for line in lines if line]


def test_fill_in_matches_builder_word_for_word():
    mod = load_build()
    builder = _builder_lines()
    assert len(builder) == 16, builder
    assert [mod.RULES] + mod.PROMPT_PARTS == builder
    last = text(DECK, 6)
    for line in builder:
        assert has(line, last), line
    assert has("Do not include student names or student work", last)
    assert has("Students already know:", last) and has("(optional)", last)


def test_sources_are_generated_from_json():
    mod = load_build()
    assert mod.render_sheet_html(data()) == SHEET_SRC.read_text(encoding="utf-8")
    assert mod.render_deck_html(data()) == DECK_SRC.read_text(encoding="utf-8")


@pytest.mark.parametrize("src", [SHEET_SRC, DECK_SRC], ids=lambda p: p.name)
def test_templates_have_no_hex(src):
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b", src.read_text(encoding="utf-8"))


@pytest.mark.parametrize("src", [SHEET_SRC, DECK_SRC], ids=lambda p: p.name)
def test_template_comment_is_swedish(src):
    assert "<!-- Genererad av exports/build-side-by-side-pdf.py" in src.read_text(encoding="utf-8")


@pytest.mark.parametrize("pdf", [SHEET, DECK], ids=lambda p: p.name)
def test_pdf_fonts_allowed_weights(pdf):
    out = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True, check=True).stdout
    assert "HankenGrotesk" in out
    assert not re.search(r"(SemiBold|Bold|Black|Heavy)", out, re.I), out


@pytest.mark.parametrize("src", [SHEET_SRC, DECK_SRC], ids=lambda p: p.name)
def test_no_page_overflows(src):
    # .page har overflow:hidden, så innehåll som inte får plats klipps tyst
    # (slutgranskningen: framsidans sidfot klipptes). Varje sida ska rymmas.
    sync_playwright = pytest.importorskip("playwright.sync_api").sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        p = b.new_page()
        p.goto(src.as_uri(), wait_until="networkidle")
        p.emulate_media(media="print")
        over = p.evaluate("[...document.querySelectorAll('.page')].map((el, i) => [i + 1, el.scrollHeight - el.clientHeight]).filter(x => x[1] > 0)")
        b.close()
    assert over == [], over
