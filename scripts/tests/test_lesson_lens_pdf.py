"""Vakter för kortleken Lesson Lens (assets/pdfs/free/lesson-lens-cards-en.pdf).

14 sidor: framsida med etiketterna och startlinsen, tolv linskort (ett per A4)
och sist kortet med luckprompten, som är ordagrant densamma som byggarens.
Källa och PDF byggs av exports/build-lesson-lens-pdf.py från samma JSON
som sidan. Fri nedladdning, ingen e-postgrind (Johans beslut 2026-10-29).
"""
import importlib.util
import json
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "assets/pdfs/free/lesson-lens-cards-en.pdf"
SRC = ROOT / "_unpublished/exports/lesson-lens-cards-a4-en.html"
BUILD = ROOT / "exports/build-lesson-lens-pdf.py"
DATA = ROOT / "lesson-lens/lenses-en.json"
JS = ROOT / "assets/js/lesson-lens.js"


def text(i):
    # pypdf delar ibland ord och CSS-versaler kommer ut som versaler, så
    # jämförelserna görs utan blanksteg och skiftlägesokänsligt.
    return re.sub(r"\s+", "", PdfReader(PDF).pages[i].extract_text()).lower()


def has(needle, haystack):
    return re.sub(r"\s+", "", needle).lower() in haystack


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_deck_has_fourteen_pages():
    assert len(PdfReader(PDF).pages) == 14


def test_cover_has_labels_and_start_lens():
    cover = text(0)
    for label in data()["labels"].values():
        assert has(label["name"], cover) and has(label["definition"], cover), label["name"]
    assert has("Not sure? Start here", cover) and has("Formative check", cover)


def test_each_lens_on_its_own_page():
    for i, lens in enumerate(data()["lenses"]):
        page = text(i + 1)
        assert has(lens["name"], page), lens["id"]
        assert has(lens["example"]["subject"], page), lens["id"]
        assert has(lens["example"]["check"], page), lens["id"]
        # Evidensen står sist på kortet: syns slutet har inget klippts bort.
        assert has(lens["evidence"][-60:], page), lens["id"]
        for part in ("Keep", "Upgrade", "Nudge", "Check", "For the AI"):
            assert has(part, page), (lens["id"], part)


def _builder_fixed_lines():
    """Raderna i promptbyggaren som inte innehåller lärarens egna uppgifter."""
    js = JS.read_text(encoding="utf-8")
    block = js[js.index("function buildPrompt"):js.index("return lines.join")]
    strings = re.findall(r"""(['"])((?:Reply in plain text|KEEP:|UPGRADE:|NUDGE:|CHECK:).*?)\1,?\s*$""", block, re.M)
    lines = [s for _, s in strings]
    assert len(lines) == 5, lines
    # Två fasta texter står mitt i en rad i JS-filen; de kontrolleras ordagrant.
    for fixed in ("'The lesson as planned:'", "Keep their lesson and their way of teaching. Do not rewrite the lesson."):
        assert fixed in block, fixed
        lines.append(fixed.strip("'"))
    return [l.replace('\\"', '"') for l in lines]


def test_fill_in_matches_builder_prompt():
    last = text(13)
    assert has("Do not include student names or student work in this conversation.", last)
    for line in _builder_fixed_lines():
        assert has(line, last), line
    assert has("Students already know:", last)


def test_fill_in_prompt_box_is_copyable_as_is():
    # Det läraren skriver av ska vara exakt prompten: hjälptexterna står
    # utanför rutan eller på rätt rad, och "(optional)" hör inte till prompten.
    src = SRC.read_text(encoding="utf-8")
    box = re.search(r'<div class="prompt">(.*?)</div>', src, re.S).group(1)
    assert "(optional)" not in box
    lens_line = next(l for l in box.splitlines() if l.startswith("Lens:"))
    how_line = next(l for l in box.splitlines() if l.startswith("How to apply it:"))
    assert "name and one-line description" in lens_line
    assert "For the AI" in how_line and "name" not in how_line


def test_pdf_fonts_allowed_weights():
    out = subprocess.run(["pdffonts", str(PDF)], capture_output=True, text=True, check=True).stdout
    assert "HankenGrotesk" in out
    assert not re.search(r"(SemiBold|Bold|Black|Heavy)", out, re.I), out


def test_source_html_is_generated_from_json():
    spec = importlib.util.spec_from_file_location("deck", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.render_deck_html(data()) == SRC.read_text(encoding="utf-8")


def test_nudge_line_covers_two_lenses():
    js = JS.read_text(encoding="utf-8")
    assert "the research behind the lens (or lenses)" in js
