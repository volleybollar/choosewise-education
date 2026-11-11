"""Vakter för AI-lektionernas elev-PDF:er.

En PDF per lektion, 1–4 sidor. PDF:en är A4 men innehållet ska rymmas när
den skrivs ut i 100 % på US Letter, och varje sida bär sin sidfot. Källan är
genererad HTML i _unpublished/exports/ai-lessons/, byggd ur lesson-en.json.
Varje test går igenom alla lektioner i spåret.
"""
import importlib.util
import json
import re
import subprocess
from pathlib import Path

import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
SLUG = "ai-lessons-younger-3c514a93"
SRC_DIR = ROOT / "_unpublished/exports/ai-lessons"
BUILD = ROOT / "exports/build-ai-lessons-pdf.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def track():
    return json.loads((ROOT / SLUG / "track-en.json").read_text(encoding="utf-8"))


IDS = [entry["id"] for entry in track()["lessons"]]


def lesson(lid):
    return json.loads((ROOT / SLUG / lid / "lesson-en.json").read_text(encoding="utf-8"))


def pdf(lid):
    return ROOT / SLUG / lid / lesson(lid)["student_pdf"]["file"]


def src(lid):
    return SRC_DIR / f"{lid}-student-a4-en.html"


def squash(text):
    return re.sub(r"\s+", "", text).lower()


def pages(path):
    return [squash(p.extract_text()) for p in PdfReader(path).pages]


def has(needle, haystack):
    return squash(needle) in haystack


@pytest.mark.parametrize("lid", IDS)
def test_every_pdf_matches_its_page_count_and_footers(lid):
    texts = pages(pdf(lid))
    assert len(texts) == len(lesson(lid)["student_pdf"]["pages"])
    for n, t in enumerate(texts, start=1):
        assert has(f"{n} / {len(texts)}", t) and has(lesson(lid)["title"], t) and has("choosewise.education", t), n


def test_training_text_on_page_one():
    for lid in IDS:
        if "training_text" in lesson(lid):
            assert has(lesson(lid)["training_text"], pages(pdf(lid))[0]), lid


@pytest.mark.parametrize("lid", IDS)
def test_use_rights_on_page_one(lid):
    assert has(track()["use_rights"], pages(pdf(lid))[0])


@pytest.mark.parametrize("lid", IDS)
def test_pdf_fonts_allowed_weights(lid):
    out = subprocess.run(["pdffonts", str(pdf(lid))], capture_output=True, text=True, check=True).stdout
    assert "HankenGrotesk" in out
    assert not re.search(r"(SemiBold|Bold|Black|Heavy)", out, re.I), out


@pytest.mark.parametrize("lid", IDS)
def test_source_html_is_generated_from_json(lid):
    build = load("build_ai_lessons", ROOT / "scripts/build-ai-lessons.py")
    t = build.load_track(ROOT, SLUG)
    mod = load("build_ai_lessons_pdf", BUILD)
    data = next(x for x in t["lesson_data"] if x["id"] == lid)
    assert mod.render_student_html(t, data) == src(lid).read_text(encoding="utf-8")


@pytest.mark.parametrize("lid", IDS)
def test_fits_us_letter(lid, tmp_path):
    """En lärare skriver ut A4-PDF:en på US Letter i 100 %, centrerat, på en
    skrivare som inte når de yttersta 5 mm. Letter är 279,4 mm hög, så 8,8 mm
    försvinner upptill och nedtill på A4, och skrivaren tar 5 mm till; på
    bredden är Letter större. Varje ord måste ligga inom det som blir kvar."""
    out = tmp_path / "bbox.html"
    subprocess.run(["pdftotext", "-bbox", str(pdf(lid)), str(out)], check=True)
    mm = 25.4 / 72
    top = (297 - 279.4) / 2 + 5
    side = max(0.0, 5 - (215.9 - 210) / 2)
    texts = re.split(r"<page ", out.read_text(encoding="utf-8"))[1:]
    assert len(texts) == len(lesson(lid)["student_pdf"]["pages"])
    for n, text in enumerate(texts, start=1):
        words = re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)<', text)
        assert words, n
        for x0, y0, x1, y1, word in words:
            assert top <= float(y0) * mm and float(y1) * mm <= 297 - top, (n, word, float(y0) * mm, float(y1) * mm)
            assert side <= float(x0) * mm and float(x1) * mm <= 210 - side, (n, word)


def test_cards_have_cut_lines_and_words():
    mod = load("build_ai_lessons_pdf", BUILD)
    block = {"kind": "cards", "cards": [{"word": "bus", "icon": "bus"}, {"word": "hovercraft"}]}
    out = mod.BLOCKS["cards"](block)
    cards = re.findall(r'<div class="card">.*?</div></div>', out, re.S)
    assert len(cards) == 2
    assert "bus" in cards[0] and "<path" in cards[0]
    assert "hovercraft" in cards[1] and "draw it" in cards[1]
    css = mod.STYLE
    assert re.search(r"\.card\s*\{[^}]*dashed", css), "cards need dashed cut lines"


def test_mat_has_one_column_per_heading():
    mod = load("build_ai_lessons_pdf", BUILD)
    out = mod.BLOCKS["mat"]({"kind": "mat", "headings": ["Land", "Water", "Air"]})
    assert len(re.findall(r'class="mat__col"', out)) == 3 and "Water" in out


def test_checklist_takes_labelled_rows():
    mod = load("build_ai_lessons_pdf", BUILD)
    out = mod.BLOCKS["checklist"]({"kind": "checklist", "items": ["The next video", "The ads"], "checks": ["Me", "The app"]})
    assert "The next video" in out and out.count('class="box"') == 4


def test_missing_image_stops_the_build():
    mod = load("build_ai_lessons_pdf", BUILD)
    with pytest.raises(FileNotFoundError, match="no-such-picture.jpg"):
        mod.BLOCKS["image"]({"kind": "image", "src": "assets/images/no-such-picture.jpg", "alt": "x"})
