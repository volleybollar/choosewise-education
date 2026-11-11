"""Vakter för elev-PDF:en till The Word-Guessing Machine.

Fyra sidor: träningstexten, räknebladet, ordlapparna och meningskollen med
avslutande frågor. PDF:en är A4 men innehållet ska rymmas på US Letter, och
varje sida bär sin sidfot. Källan är genererad HTML i
_unpublished/exports/ai-lessons/, byggd ur lesson-en.json.
"""
import importlib.util
import json
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
SLUG = "ai-lessons-younger-3c514a93"
LESSON = "word-guessing-machine"
PDF = ROOT / SLUG / LESSON / "word-guessing-machine-student-en.pdf"
SRC = ROOT / "_unpublished/exports/ai-lessons/word-guessing-machine-student-a4-en.html"
BUILD = ROOT / "exports/build-ai-lessons-pdf.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def squash(text):
    return re.sub(r"\s+", "", text).lower()


def pages(pdf=PDF):
    return [squash(p.extract_text()) for p in PdfReader(pdf).pages]


def has(needle, haystack):
    return squash(needle) in haystack


def lesson():
    return json.loads((ROOT / SLUG / LESSON / "lesson-en.json").read_text(encoding="utf-8"))


def track():
    return json.loads((ROOT / SLUG / "track-en.json").read_text(encoding="utf-8"))


def footers_ok(texts):
    title = lesson()["title"]
    return all(has(f"{n} / {len(texts)}", t) and has(title, t) and has("choosewise.education", t)
               for n, t in enumerate(texts, start=1))


def test_pdf_has_four_pages():
    assert len(PdfReader(PDF).pages) == 4


def test_every_page_has_its_footer():
    assert footers_ok(pages())


def test_training_text_on_page_one():
    assert has(lesson()["training_text"], pages()[0])


def test_use_rights_on_page_one():
    assert has(track()["use_rights"], pages()[0])


def test_pdf_fonts_allowed_weights():
    out = subprocess.run(["pdffonts", str(PDF)], capture_output=True, text=True, check=True).stdout
    assert "HankenGrotesk" in out
    assert not re.search(r"(SemiBold|Bold|Black|Heavy)", out, re.I), out


def test_source_html_is_generated_from_json():
    build = load("build_ai_lessons", ROOT / "scripts/build-ai-lessons.py")
    t = build.load_track(ROOT, SLUG)
    mod = load("build_ai_lessons_pdf", BUILD)
    assert mod.render_student_html(t, t["lesson_data"][0]) == SRC.read_text(encoding="utf-8")


def test_fits_us_letter(tmp_path):
    """Samma källa på US Letter: lika många sidor och alla sidfötter kvar,
    alltså inget klipps när en lärare skriver ut på Letter."""
    from playwright.sync_api import sync_playwright

    html = SRC.read_text(encoding="utf-8")
    letter = html.replace("size: A4;", "size: letter;", 1)
    assert letter != html
    letter = letter.replace("<head>", f'<head>\n<base href="{SRC.parent.as_uri()}/">', 1)
    page_file, out = tmp_path / "letter.html", tmp_path / "letter.pdf"
    page_file.write_text(letter, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(page_file.as_uri(), wait_until="networkidle")
        page.emulate_media(media="print")
        page.pdf(path=str(out), print_background=True, prefer_css_page_size=True,
                 margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        browser.close()
    texts = pages(out)
    assert len(texts) == 4
    assert footers_ok(texts)
