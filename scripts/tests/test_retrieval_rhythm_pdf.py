"""Vakter för utskriftspaketet Retrieval Rhythm (assets/pdfs/free/retrieval-rhythm-pack-en.pdf).

8 sidor: veckorytmen och evidensen, de fem formatens elevmallar (en per sida),
en sida till elever och föräldrar, och sist luckprompten, som är ordagrant
densamma som byggarens. Byggs av exports/build-retrieval-rhythm-pdf.py från
samma JSON som sidan.
"""
import importlib.util
import json
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "assets/pdfs/free/retrieval-rhythm-pack-en.pdf"
SRC = ROOT / "_unpublished/exports/retrieval-rhythm-pack-a4-en.html"
BUILD = ROOT / "exports/build-retrieval-rhythm-pdf.py"
DATA = ROOT / "retrieval-rhythm/rhythm-en.json"
JS = ROOT / "assets/js/retrieval-rhythm.js"


def text(i):
    return re.sub(r"\s+", "", PdfReader(PDF).pages[i].extract_text()).lower()


def has(needle, haystack):
    return re.sub(r"\s+", "", needle).lower() in haystack


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_pack_has_eight_pages():
    assert len(PdfReader(PDF).pages) == 8


def test_first_page_has_rhythm_and_evidence():
    first = text(0)
    for word in ("After each lesson", "On Friday", "Before Monday"):
        assert has(word, first), word
    for a in data()["approaches"]:
        assert has(a["name"], first), a["id"]


def test_each_format_on_its_own_page():
    real = [f for f in data()["formats"] if f["id"] != "mix"]
    for i, f in enumerate(real):
        page = text(i + 1)
        assert has(f["name"], page), f["id"]
        assert has(f"{f['minutes']} min", page), f["id"]
        assert has(f["steps"][-1], page), f["id"]
        assert has("Name", page), f["id"]


def test_student_and_parent_page():
    page = text(6)
    assert has("Why we start every lesson like this", page)
    assert has("harder", page)


def _builder_fixed_lines():
    js = JS.read_text(encoding="utf-8")
    block = js[js.index("function buildPrompt"):js.index("return lines.join")]
    strings = re.findall(r"""^\s*(['"])((?:Reply in plain text|LESSON:|STARTER:|KEY:|Then once|CHECK:|Topic log|For each lesson, mix).*?)\1,?\s*$""", block, re.M)
    lines = [s for _, s in strings]
    assert len(lines) == 8, lines
    fixed = "Use only content from the topic log below. Do not add new content."
    assert fixed in block
    return lines + [fixed]


def test_fill_in_matches_builder_prompt():
    last = text(7)
    assert has("Do not include student names or student results in this conversation.", last)
    for line in _builder_fixed_lines():
        assert has(line, last), line


def test_fill_in_prompt_box_is_copyable_as_is():
    src = SRC.read_text(encoding="utf-8")
    box = re.search(r'<div class="prompt">(.*?)</div>', src, re.S).group(1)
    assert "(optional)" not in box


def test_pdf_fonts_allowed_weights():
    out = subprocess.run(["pdffonts", str(PDF)], capture_output=True, text=True, check=True).stdout
    assert "HankenGrotesk" in out
    assert not re.search(r"(SemiBold|Bold|Black|Heavy)", out, re.I), out


def test_source_html_is_generated_from_json():
    spec = importlib.util.spec_from_file_location("pack", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.render_pack_html(data()) == SRC.read_text(encoding="utf-8")
