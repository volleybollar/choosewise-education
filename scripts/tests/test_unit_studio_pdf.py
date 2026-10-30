"""Vakter för Unit Studios metodkort (unit-studio-541ebd12/unit-studio-method-card-en.pdf).

Två sidor: de fem stegen med frågorna att titta efter, och en luckprompt
ordagrant som i assets/js/unit-studio.js. Kortet ligger i den dolda mappen,
inte under /assets/pdfs/free/.
"""
import importlib.util
import json
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "unit-studio-541ebd12/unit-studio-method-card-en.pdf"
SRC = ROOT / "_unpublished/exports/unit-studio-method-card-a4-en.html"
BUILD = ROOT / "exports/build-unit-studio-pdf.py"
DATA = ROOT / "unit-studio-541ebd12/studio-en.json"
JS = ROOT / "assets/js/unit-studio.js"


def pages():
    return [re.sub(r"\s+", "", p.extract_text()).lower() for p in PdfReader(PDF).pages]


def has(needle, haystack):
    return re.sub(r"\s+", "", needle).lower() in haystack


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_card_has_two_pages():
    assert len(PdfReader(PDF).pages) == 2


def test_every_step_and_question_on_page_one():
    first = pages()[0]
    for s in data()["steps"]:
        assert has(s["name"], first), s["id"]
        for q in s["look_for"]:
            assert has(q, first), q


def _js_format_lines():
    js = JS.read_text(encoding="utf-8")
    prefixes = ("KEEP:", "SUGGEST:", "QUESTION:", "AI CAN ALSO:", "Reply in plain text, no tables, in exactly this format:",
                "GOAL AND EVIDENCE:", "PRIOR KNOWLEDGE:", "LESSONS:", "RETRIEVAL:", "CHECKPOINTS:", "AI USE:", "CHANGES:", "CHECK:")
    lines = []
    for m in re.finditer(r"'((?:[^'\\]|\\.)*)'", js):
        s = m.group(1).replace("\\'", "'")
        if s.startswith(prefixes):
            lines.append(s)
    assert len(lines) == 14, lines  # "Reply in plain text…" står i båda formaten
    return lines


def test_fill_in_prompt_matches_builder():
    second = pages()[1]
    assert has("Do not include student names or student results in this conversation.", second)
    assert has("We work through five steps, one at a time.", second)
    for line in _js_format_lines():
        assert has(line, second), line


def test_pdf_fonts_allowed_weights():
    out = subprocess.run(["pdffonts", str(PDF)], capture_output=True, text=True, check=True).stdout
    assert "HankenGrotesk" in out
    assert not re.search(r"(SemiBold|Bold|Black|Heavy)", out, re.I), out


def test_source_html_is_generated_from_json():
    spec = importlib.util.spec_from_file_location("card", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.render_card_html(data()) == SRC.read_text(encoding="utf-8")


def test_no_page_is_clipped():
    for i, page in enumerate(pages(), start=1):
        assert has(f"{i} / 2", page), i


def test_each_label_once_per_step():
    # Steg 4 har två Strong-ansatser; kortet visar etiketten en gång.
    assert "strongstrong" not in pages()[0]
