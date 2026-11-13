"""Vakter för lärarkitet The Study Experiment (assets/pdfs/free/study-experiment-kit-en.pdf).

Sju sidor: överblick, Lesson 1-manus, grupplappar, gissningslappar, poänglappar,
Lesson 2-manus med diskussion och förklaringar, samt en luckprompt som citerar
promptbyggarens fasta rader ordagrant. Källa och PDF byggs av
exports/build-study-experiment-pdf.py från study-experiment/experiment-en.json,
samma JSON som sidan. Fri nedladdning, ingen e-postgrind (specen).
Spec: docs/superpowers/specs/2026-11-13-study-experiment-design.md.
"""
import importlib.util
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "assets/pdfs/free/study-experiment-kit-en.pdf"
SRC = ROOT / "_unpublished/exports/study-experiment-kit-a4-en.html"
BUILD = ROOT / "exports/build-study-experiment-pdf.py"
DATA = ROOT / "study-experiment/experiment-en.json"
JS = ROOT / "assets/js/study-experiment.js"

PAGES = 7
FOOTER = "The Study Experiment · choosewise.education/study-experiment"


def text(i):
    # pypdf delar ibland ord och CSS-versaler kommer ut som versaler, så
    # jämförelserna görs utan blanksteg och skiftlägesokänsligt.
    return re.sub(r"\s+", "", PdfReader(PDF).pages[i].extract_text()).lower()


def norm(s):
    return re.sub(r"\s+", "", s).lower()


def has(needle, haystack):
    return norm(needle) in haystack


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_seven_pages():
    assert len(PdfReader(PDF).pages) == PAGES


def test_every_page_has_footer_and_number():
    for i in range(PAGES):
        page = text(i)
        assert has(FOOTER, page), i + 1
        assert has(f"{i + 1} / {PAGES}", page), i + 1


def test_overview_page():
    d = data()
    page = text(0)
    assert has("The Study Experiment", page)
    for item in d["materials"] + d["before"]:
        assert has(item, page), item
    for lesson in ("lesson1", "lesson2"):
        assert has(d[lesson]["intro"], page), lesson
    assert has(d["expect"], page)


def test_lesson_pages():
    d = data()
    lesson1 = text(1)
    assert has(d["lesson1"]["intro"], lesson1)
    for step in d["lesson1"]["steps"]:
        assert has(step["text"], lesson1), step["text"]
    lesson2 = text(5)
    assert has(d["lesson2"]["intro"], lesson2)
    for step in d["lesson2"]["steps"]:
        assert has(step["text"], lesson2), step["text"]
    for question in d["discussion"]:
        assert has(question, lesson2), question
    assert has(d["explain"]["title"], lesson2)
    for point in d["explain"]["points"]:
        assert has(point, lesson2), point
    assert has(d["even_result"]["title"], lesson2)
    assert has(d["even_result"]["text"], lesson2)
    assert has(d["no_computer"], lesson2)


def test_step_minutes_in_source():
    # Minuterna står i en egen ruta per steg; ett steg utan tid får en tom ruta.
    d = data()
    src = SRC.read_text(encoding="utf-8")
    shown = re.findall(r'<span class="min">(.*?)</span>', src)
    expected = [
        f"{s['minutes']} min" if s["minutes"] else ""
        for lesson in ("lesson1", "lesson2")
        for s in d[lesson]["steps"]
    ]
    assert shown == expected


def test_group_cards_page():
    d = data()
    page = text(2)
    assert has("Print one page for every four students.", page)
    cards = d["group_cards"]
    assert len(cards) == 2
    for card in cards:
        # Varje lapp står två gånger på sidan: Group 1, Group 2, Group 1, Group 2.
        assert page.count(norm(card["title"])) == 2, card["title"]
    steps = Counter(step for card in cards for step in card["steps"])
    for step, n in steps.items():
        assert page.count(norm(step)) == 2 * n, step


def test_slip_pages():
    d = data()
    pred = text(3)
    slip = d["prediction_slip"]
    assert pred.count(norm(slip["question"])) == 8
    for option in slip["options"]:
        assert pred.count(norm(option)) == 8, option
    assert "name" not in pred

    score = text(4)
    for line in d["score_slip"]["lines"]:
        # Luckan "____" ritas med CSS (en linje att skriva på), inte med understreck.
        assert score.count(norm(line.replace("____", ""))) == 8, line
    assert score.count(norm(d["score_slip"]["check"])) == 8
    assert "name" not in score


def test_slips_have_cut_lines_and_css_tick_boxes():
    # Rutorna ritas med CSS (en ram på ett inline-block), aldrig med tecknet ☐,
    # så att inget reservtypsnitt kommer med i PDF:en.
    src = SRC.read_text(encoding="utf-8")
    assert "☐" not in src and "□" not in src
    assert src.count('class="slip"') == 16
    assert src.count('class="tick"') == 8 * 3 + 8
    assert src.count('class="card"') == 4
    assert re.search(r"dashed", src)
    for token in ("slip", "card"):
        rule = re.search(r"\." + token + r"\s*\{[^}]*\}", src)
        assert rule and "dashed" in rule.group(0), token


def _literals(fn, next_fn):
    """Alla strängar i en funktion i study-experiment.js, utom tomma rader och
    rena mellanrum eller punkter mellan luckor.

    Varje sträng är en fast rad eller en fast del av en rad, så var och en
    måste stå ordagrant i luckprompten."""
    js = JS.read_text(encoding="utf-8")
    block = js[js.index(f"function {fn}"):js.index(f"function {next_fn}")]
    block = re.sub(r"/\*.*?\*/", "", block, flags=re.S)
    block = re.sub(r"^\s*//.*$", "", block, flags=re.M)
    found = [m.group(2) for m in re.finditer(r"(['\"])((?:\\.|(?!\1)[^\\\n])*)\1", block)]
    unescaped = [s.replace("\\'", "'").replace('\\"', '"') for s in found]
    return [s for s in unescaped if s.strip(" .")]


def test_fill_in_matches_js():
    page = text(6)
    lines = _literals("teacherLines", "buildPrompt")
    assert len(lines) >= 20, lines
    assert "Do not include student names or student work in this conversation." in lines
    assert any(l.startswith("- Make each text about 250 words") for l in lines)
    assert any(l.startswith("CHECK: every fact") for l in lines)
    for line in lines:
        assert has(line, page), line
    # Den andra meningen står ordagrant (specen och sidans prompt).
    assert has(
        "Students will study two short texts: one by reading it twice, the other by "
        "reading it once, writing down everything they remember and then checking it "
        "against the text.", page)


def test_fill_in_has_blanks_for_the_four_fields():
    # Årskurs två gånger, ämne, område och språk: fem luckor i rutan, och
    # inget förifyllt värde i dem.
    src = SRC.read_text(encoding="utf-8")
    boxes = re.findall(r'<div class="prompt">(.*?)</div>', src, re.S)
    assert len(boxes) == 1
    box = boxes[0]
    assert box.count('class="blank"') == 5
    assert "(optional)" not in box
    for label in ("Topic area:", "Write everything in"):
        assert label in box
    assert box.count("Grade") >= 2


def test_pdf_fonts_allowed_weights():
    out = subprocess.run(["pdffonts", str(PDF)], capture_output=True, text=True, check=True).stdout
    assert "HankenGrotesk" in out
    assert not re.search(r"(SemiBold|Bold|Black|Heavy)", out, re.I), out


def test_pdf_has_no_fallback_fonts():
    out = subprocess.run(["pdffonts", str(PDF)], capture_output=True, text=True, check=True).stdout
    names = [line.split()[0].split("+")[-1] for line in out.splitlines()[2:] if line.strip()]
    assert names, out
    for name in names:
        assert name.startswith("HankenGrotesk"), (name, out)


def _rendered(script):
    """Kör ett JS-uttryck mot källsidan i Chromium (print-läge, som i bygget)."""
    sync_playwright = pytest.importorskip("playwright.sync_api").sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        p = b.new_page()
        p.goto(SRC.as_uri(), wait_until="networkidle")
        p.emulate_media(media="print")
        out = p.evaluate(script)
        b.close()
    return out


def test_no_page_overflows():
    # .page har overflow:hidden, så innehåll som inte får plats klipps tyst
    # (texten finns kvar i PDF:en och textvakterna ser det inte). Varje sida ska rymmas.
    over = _rendered("[...document.querySelectorAll('.page')].map((el, i) => [i + 1, el.scrollHeight - el.clientHeight]).filter(x => x[1] > 0)")
    assert over == [], over


def test_page_six_body_text_stays_readable():
    # Sida 6 rymmer manus, diskussion, förklaringar och rutor på en sida. Fick det
    # inte plats vid läsbar storlek skulle det bli sju plus en sida: brödtexten får
    # aldrig gå under cirka 9,5 pt (12,67 px).
    sizes = _rendered("""[...document.querySelectorAll('.page')[5].querySelectorAll('.script li, .qs li, .points li, .box p, .note, .intro')]
        .map(el => parseFloat(getComputedStyle(el).fontSize))""")
    assert sizes and min(sizes) >= 12.6, sizes


def test_source_html_is_generated_from_json():
    spec = importlib.util.spec_from_file_location("kit", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.render_kit_html(data()) == SRC.read_text(encoding="utf-8")
