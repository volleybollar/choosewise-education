"""Vakter för de två PDF:erna till Flawed Answer.

Elevramen (flawed-answer-frame-en.pdf) är en A4-sida med de fyra stegen och
Think back. Kortleken (flawed-answer-cards-en.pdf) har framsida, sex
feltypskort och sist luckprompten — 8 sidor.
Båda byggs av exports/build-flawed-answer-pdf.py från samma JSON som sidan.
"""
import importlib.util
import json
import re
import subprocess
from pathlib import Path

import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
FRAME = ROOT / "assets/pdfs/free/flawed-answer-frame-en.pdf"
DECK = ROOT / "assets/pdfs/free/flawed-answer-cards-en.pdf"
FRAME_SRC = ROOT / "_unpublished/exports/flawed-answer-frame-a4-en.html"
DECK_SRC = ROOT / "_unpublished/exports/flawed-answer-cards-a4-en.html"
BUILD = ROOT / "exports/build-flawed-answer-pdf.py"
DATA = ROOT / "flawed-answer/flaws-en.json"
FRAME_LINE = "This answer was written by AI. Find where its reasoning goes wrong."


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def text(pdf, i):
    # pypdf delar ibland ord och CSS-versaler kommer ut som versaler, så
    # jämförelserna görs utan blanksteg och skiftlägesokänsligt.
    return re.sub(r"\s+", "", PdfReader(pdf).pages[i].extract_text()).lower()


def has(needle, haystack):
    return re.sub(r"\s+", "", needle).lower() in haystack


def load_build():
    spec = importlib.util.spec_from_file_location("fa_pdf", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_frame_is_one_page_with_four_steps_and_line():
    assert len(PdfReader(FRAME).pages) == 1
    page = text(FRAME, 0)
    assert has(FRAME_LINE, page)
    for step in data()["steps"]:
        assert has(step["name"], page), step["name"]
    assert has("Think back", page)
    assert has("Staple or paste the AI-generated answer here", page)


def test_deck_page_count():
    assert len(PdfReader(DECK).pages) == 8


def test_deck_cover_has_steps_levels_and_legend():
    cover = text(DECK, 0)
    d = data()
    for step in d["steps"]:
        assert has(step["name"], cover), step["name"]
    for level in d["levels"]:
        assert has(level["name"], cover), level["name"]
    assert has("Strong", cover) and has("Thin", cover) and has("not a single use", cover)


def test_deck_cards_have_example_key_and_for_the_ai():
    for i, f in enumerate(data()["flaws"]):
        page = text(DECK, i + 1)
        ex = f["example"]
        assert has(f["name"], page), f["id"]
        assert has("AI-generated answer", page), f["id"]
        for key in ("question", "answer", "flaw", "fix", "why_convincing", "test_it", "probe", "think_back"):
            assert has(ex[key], page), (f["id"], key)
        for sign in f["telltale_signs"]:
            assert has(sign, page), (f["id"], sign)
        assert has("For the AI", page) and has(f["prompt_brief"], page), f["id"]
        assert has("Easier to spot only", page) == (not f["harder_ok"]), f["id"]


def _builder_lines():
    """Rules-raden och de nio del-raderna exakt som promptbyggaren skriver dem."""
    js = (ROOT / "assets/js/flawed-answer.js").read_text(encoding="utf-8")
    block = js[js.index("'Rules:"):js.index("return lines.join")]
    lines = re.findall(r"""^\s*(['"])((?:Rules|QUESTION|ANSWER|THE FLAW|FIX|WHY IT CONVINCES|TEST IT|PROBE|THINK BACK|CHECK):.*?)\1,?\s*$""",
                       block, re.M)
    assert len(lines) == 10, lines
    return [t for _, t in lines]


def test_fill_in_matches_builder_word_for_word():
    mod = load_build()
    builder = _builder_lines()
    assert [mod.RULES] + mod.PROMPT_PARTS == builder
    last = text(DECK, 7)
    for line in builder:
        assert has(line, last), line
    assert has("Do not include student names or student work", last)
    assert has("Students already know (optional)", last)


def test_sources_are_generated_from_json():
    mod = load_build()
    assert mod.render_frame_html(data()) == FRAME_SRC.read_text(encoding="utf-8")
    assert mod.render_deck_html(data()) == DECK_SRC.read_text(encoding="utf-8")


@pytest.mark.parametrize("src", [FRAME_SRC, DECK_SRC], ids=lambda p: p.name)
def test_templates_have_no_hex(src):
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b", src.read_text(encoding="utf-8"))


@pytest.mark.parametrize("pdf", [FRAME, DECK], ids=lambda p: p.name)
def test_pdf_fonts_allowed_weights(pdf):
    out = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True, check=True).stdout
    assert "HankenGrotesk" in out
    assert not re.search(r"(SemiBold|Bold|Black|Heavy)", out, re.I), out
