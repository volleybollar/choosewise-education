"""Vakter för Pedagogy Compass-affischen (pedagogy-compass-59ecb8db/pedagogy-compass-poster-en.pdf).

Två sidor: de tio problemen med sina modeller, och modellkartan med
etiketter plus promptens svarsformat ordagrant som i
assets/js/pedagogy-compass.js. Affischen ligger i den dolda mappen.
"""
import importlib.util
import json
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "pedagogy-compass-59ecb8db/pedagogy-compass-poster-en.pdf"
SRC = ROOT / "_unpublished/exports/pedagogy-compass-poster-a4-en.html"
BUILD = ROOT / "exports/build-pedagogy-compass-pdf.py"
DATA = ROOT / "pedagogy-compass-59ecb8db/compass-en.json"
JS = ROOT / "assets/js/pedagogy-compass.js"


def pages():
    return [re.sub(r"\s+", "", p.extract_text()).lower() for p in PdfReader(PDF).pages]


def has(needle, haystack):
    return re.sub(r"\s+", "", needle).lower() in haystack


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_poster_has_two_pages():
    assert len(PdfReader(PDF).pages) == 2


def test_every_problem_on_page_one():
    first = pages()[0]
    for p in data()["problems"]:
        assert has(p["name"], first), p["id"]


def test_every_model_on_page_two():
    second = pages()[1]
    for m in data()["models"]:
        assert has(m["name"], second), m["id"]


def test_format_lines_match_builder():
    js = JS.read_text(encoding="utf-8")
    lines = [m.group(1).replace("\\'", "'") for m in re.finditer(r"'((?:[^'\\]|\\.)*)'", js)
             if m.group(1).startswith(("Reply in plain text", "BEST FIRST STEP:", "NEXT LESSON:", "WATCH FOR:", "AI:", "HONEST NOTE:"))]
    assert len(lines) == 6, lines
    for line in lines:
        assert has(line, pages()[1]), line


def test_pdf_fonts_allowed_weights():
    out = subprocess.run(["pdffonts", str(PDF)], capture_output=True, text=True, check=True).stdout
    assert "HankenGrotesk" in out
    assert not re.search(r"(SemiBold|Bold|Black|Heavy)", out, re.I), out


def test_source_html_is_generated_from_json():
    spec = importlib.util.spec_from_file_location("poster", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.render_poster_html(data()) == SRC.read_text(encoding="utf-8")


def test_no_page_is_clipped():
    for i, page in enumerate(pages(), start=1):
        assert has(f"{i} / 2", page), i
