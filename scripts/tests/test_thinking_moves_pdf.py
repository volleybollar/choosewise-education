"""Vakter för kortleken Thinking Moves (assets/pdfs/free/thinking-moves-cards-en.pdf).

14 sidor: framsida med kluster och etiketter, tolv dragkort (ett per A4) och
sist kortet med luckprompten (Johans "mellanting", 2026-10-27).
Källa och PDF byggs av exports/build-thinking-moves-pdf.py från samma JSON
som sidan.
"""
import importlib.util
import json
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "assets/pdfs/free/thinking-moves-cards-en.pdf"
SRC = ROOT / "_unpublished/exports/thinking-moves-cards-a4-en.html"
BUILD = ROOT / "exports/build-thinking-moves-pdf.py"
DATA = ROOT / "thinking-moves/moves-en.json"


def text(i):
    # pypdf delar ibland ord ("m any") och CSS-versaler kommer ut som versaler,
    # så jämförelserna görs utan blanksteg och skiftlägesokänsligt.
    return re.sub(r"\s+", "", PdfReader(PDF).pages[i].extract_text()).lower()


def has(needle, haystack):
    return re.sub(r"\s+", "", needle).lower() in haystack


def test_deck_has_fourteen_pages():
    assert len(PdfReader(PDF).pages) == 14


def test_cover_lists_clusters_and_label_note():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    cover = text(0)
    for c in data["clusters"]:
        assert has(c["name"], cover), c["name"]
    assert has("not a single five-minute move", cover)


def test_each_move_on_its_own_page():
    moves = json.loads(DATA.read_text(encoding="utf-8"))["moves"]
    for i, m in enumerate(moves):
        page = text(i + 1)
        assert has(m["name"], page), m["id"]
        for ex in m["examples"]:
            assert has(ex["subject"], page), (m["id"], ex["subject"])
        assert has("Look for", page) and has("Think back", page), m["id"]


def test_last_page_is_fill_in_prompt():
    last = text(13)
    for part in ("Do not include student names", "MOVE:", "TASK:", "LOOK FOR:", "PROBE:", "THINK BACK:", "CHECK:"):
        assert has(part, last), part


def test_pdf_fonts_allowed_weights():
    out = subprocess.run(["pdffonts", str(PDF)], capture_output=True, text=True, check=True).stdout
    assert "HankenGrotesk" in out
    assert not re.search(r"(SemiBold|Bold|Black|Heavy)", out, re.I), out


def test_source_html_is_generated_from_json():
    spec = importlib.util.spec_from_file_location("deck", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    data = json.loads(DATA.read_text(encoding="utf-8"))
    assert mod.render_deck_html(data) == SRC.read_text(encoding="utf-8")


def _builder_part_lines():
    """De sex del-raderna exakt som promptbyggaren skriver dem."""
    js = (ROOT / "assets/js/thinking-moves.js").read_text(encoding="utf-8")
    block = js[js.index("'Reply in plain text"):js.index("return lines.join")]
    lines = re.findall(r"""^\s*(['"])((?:MOVE|TASK|LOOK FOR|PROBE|THINK BACK|CHECK):.*?)\1,?\s*$""", block, re.M)
    assert len(lines) == 6, lines
    return [text for _, text in lines]


def test_fill_in_prompt_matches_builder_word_for_word():
    last = text(13)
    for line in _builder_part_lines():
        assert has(line, last), line
    assert has("Students already know (optional)", last)


def test_each_card_prints_its_ai_instruction():
    moves = json.loads(DATA.read_text(encoding="utf-8"))["moves"]
    for i, m in enumerate(moves):
        page = text(i + 1)
        assert has("For the AI", page) and has(m["prompt_brief"], page), m["id"]
