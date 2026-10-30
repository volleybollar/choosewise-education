"""Vakter för utskriftspaketet Two-Minute Debrief (assets/pdfs/free/two-minute-debrief-pack-en.pdf).

7 sidor: debriefkortet, exit tickets (två sidor), luckprompten för en
debrief, luckprompten för veckosammanställningen, ett helt exempel och
evidensen. Luckpromptarna är ordagrant desamma som i
assets/js/two-minute-debrief.js. Byggs av exports/build-two-minute-debrief-pdf.py
från samma JSON som sidan.
"""
import importlib.util
import json
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "assets/pdfs/free/two-minute-debrief-pack-en.pdf"
SRC = ROOT / "_unpublished/exports/two-minute-debrief-pack-a4-en.html"
BUILD = ROOT / "exports/build-two-minute-debrief-pdf.py"
DATA = ROOT / "two-minute-debrief/debrief-en.json"
JS = ROOT / "assets/js/two-minute-debrief.js"


def pages():
    return [re.sub(r"\s+", "", p.extract_text()).lower() for p in PdfReader(PDF).pages]


def has(needle, haystack):
    return re.sub(r"\s+", "", needle).lower() in haystack


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_pack_has_seven_pages():
    assert len(PdfReader(PDF).pages) == 7


def test_debrief_card_has_four_questions():
    first = pages()[0]
    for word in ("Goal", "Evidence", "Surprise", "Next", "Do not include student names",
                 "Run it before you meet the group again"):
        assert has(word, first), word


def test_exit_tickets_present():
    text = "".join(pages()[1:3])
    for t in data()["exit_tickets"]:
        assert has(t["name"], text), t["id"]
        assert has(t["forms_steps"][-1], text), t["id"]
        assert has(t["google_steps"][-1], text), t["id"]


def _js_fixed_lines():
    """De fasta raderna i promptarna, som de står i JS-filen."""
    js = JS.read_text(encoding="utf-8")
    prefixes = ("LIKELY CAUSES:", "NEXT LESSON:", "CHECK FIRST:", "ONE QUESTION:", "PATTERNS:", "WHAT WORKED:",
                "ONE CHANGE FOR NEXT WEEK:", "Reply in plain text, no tables, in exactly this format:",
                "You are helping a teacher look back")
    lines = []
    for m in re.finditer(r"'((?:[^'\\]|\\.)*)'", js):
        s = m.group(1).replace("\\'", "'")
        if s.startswith(prefixes):
            lines.append(s)
    assert len(lines) == 11, lines  # "Reply in plain text…" står i båda promptarna
    return lines


def test_fill_in_prompts_match_builder():
    debrief, rollup = pages()[3], pages()[4]
    for page in (debrief, rollup):
        assert has("Do not include student names or student results in this conversation.", page)
    assert has("that did not go as planned. Base everything on what the teacher writes below, "
               "and tie every point to this lesson's content.", debrief)
    for line in _js_fixed_lines():
        to_rollup = line.startswith(("PATTERNS", "WHAT WORKED", "ONE CHANGE", "You are helping a teacher look back")) \
            or line == "ONE QUESTION: one question back to the teacher."
        target = rollup if to_rollup else debrief
        assert has(line, target), line
    assert has("ONE QUESTION: one question back to the teacher.", rollup)


def test_hero_example_in_full():
    page = pages()[5]
    ex = next(e for e in data()["examples"] if e["id"] == data()["hero_example"])
    for key in ("goal", "evidence", "next"):
        assert has(ex[key], page), key
    for key in ("likely_causes", "next_lesson", "check_first", "one_question"):
        assert has(ex["reply"][key], page), key


def test_evidence_page():
    page = pages()[6]
    for a in data()["approaches"]:
        assert has(a["name"], page), a["id"]


def test_pdf_fonts_allowed_weights():
    out = subprocess.run(["pdffonts", str(PDF)], capture_output=True, text=True, check=True).stdout
    assert "HankenGrotesk" in out
    assert not re.search(r"(SemiBold|Bold|Black|Heavy)", out, re.I), out


def test_source_html_is_generated_from_json():
    spec = importlib.util.spec_from_file_location("pack", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.render_pack_html(data()) == SRC.read_text(encoding="utf-8")


def test_no_page_is_clipped():
    # Sidfoten står sist på varje sida: syns den har inget klippts bort ovanför.
    for i, page in enumerate(pages(), start=1):
        assert has(f"{i} / 7", page), i
    assert has(data()["approaches"][-1]["evidence"][-40:], pages()[6])
    assert has(data()["exit_tickets"][-1]["paper_note"][-40:], pages()[2])
