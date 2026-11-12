"""Vakter för kortleken Study Moves (assets/pdfs/free/study-moves-cards-en.pdf).

13 sidor: framsida med målen och deras drag, startdraget, varför bra
studier känns svårare och etiketterna; tio dragkort (ett per A4); sist en
luckprompt för läraren och en för eleven, som citerar byggarens fasta rader
ordagrant. Källa och PDF byggs av exports/build-study-moves-pdf.py från
samma JSON som sidan. Fri nedladdning, ingen e-postgrind (specen).
Spec: docs/superpowers/specs/2026-11-12-study-moves-design.md.
"""
import importlib.util
import json
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "assets/pdfs/free/study-moves-cards-en.pdf"
SRC = ROOT / "_unpublished/exports/study-moves-cards-a4-en.html"
BUILD = ROOT / "exports/build-study-moves-pdf.py"
DATA = ROOT / "study-moves/moves-en.json"
JS = ROOT / "assets/js/study-moves.js"


def text(i):
    # pypdf delar ibland ord och CSS-versaler kommer ut som versaler, så
    # jämförelserna görs utan blanksteg och skiftlägesokänsligt.
    return re.sub(r"\s+", "", PdfReader(PDF).pages[i].extract_text()).lower()


def has(needle, haystack):
    return re.sub(r"\s+", "", needle).lower() in haystack


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_thirteen_pages():
    assert len(PdfReader(PDF).pages) == 13


def test_cover_has_goals_labels_and_start():
    d = data()
    cover = text(0)
    for goal in d["goals"]:
        assert has(goal["name"], cover), goal["id"]
    for move in d["moves"]:
        assert has(move["name"], cover), move["id"]
    for label in d["labels"].values():
        assert has(label["name"], cover) and has(label["definition"], cover), label["name"]
    start = next(m for m in d["moves"] if m["id"] == d["default_move"])
    assert has(f"Not sure? Start here: {start['name']}", cover)
    assert has(d["feels_harder"]["text"], cover)


def test_each_move_on_its_own_page():
    for i, move in enumerate(data()["moves"]):
        page = text(i + 1)
        assert has(move["name"], page), move["id"]
        assert has(move["research_name"], page), move["id"]
        assert has(move["steps"][0], page), move["id"]
        assert has(move["example"]["subject"], page), move["id"]
        assert has(move["teacher_ai"]["brief"], page), move["id"]
        assert has(move["student_ai"]["brief"], page), move["id"]
        assert has(move["watch_out"], page), move["id"]
        # Evidensen står sist på kortet: syns slutet har inget klippts bort.
        assert has(move["evidence"][-60:], page), move["id"]
        for part in ("How to do it", "How it feels", "For the AI (teacher)", "For the AI (student)"):
            assert has(part, page), (move["id"], part)
        assert has(f"{i + 2} / 13", page), move["id"]


def _literals(fn, next_fn):
    """Alla strängar i en funktion i study-moves.js, utom tomma rader.

    Varje sträng är en fast rad eller en fast del av en rad, så var och en
    måste stå ordagrant i luckprompten."""
    js = JS.read_text(encoding="utf-8")
    block = js[js.index(f"function {fn}"):js.index(f"function {next_fn}")]
    block = re.sub(r"/\*.*?\*/", "", block, flags=re.S)
    block = re.sub(r"^\s*//.*$", "", block, flags=re.M)
    found = [m.group(2) for m in re.finditer(r"(['\"])((?:\\.|(?!\1)[^\\\n])*)\1", block)]
    unescaped = [s.replace("\\'", "'").replace('\\"', '"') for s in found]
    return [s for s in unescaped if s.strip(" .")]


def test_teacher_fill_in_matches_js():
    page = text(11)
    lines = _literals("teacherLines", "studentLines")
    assert len(lines) >= 12, lines
    assert "Do not include student names or student work in this conversation." in lines
    for line in lines:
        assert has(line, page), line
    assert has("12 / 13", page)


def test_student_fill_in_matches_js():
    page = text(12)
    lines = _literals("studentLines", "buildPrompt")
    assert len(lines) >= 12, lines
    assert "Start now." in lines
    assert any(l.startswith("- Never give me the answer") for l in lines)
    for line in lines:
        assert has(line, page), line
    assert has("13 / 13", page)


def test_student_fill_in_states_age_rules():
    d = data()
    page = text(12)
    for rule in d["age_rules"]:
        assert has(rule["tool"], page), rule["tool"]
    assert has(d["age_rules_date"], page)
    assert has("your school's rules", page)


def test_fill_in_prompt_boxes_are_copyable_as_is():
    # Det man skriver av ska vara exakt prompten: "(optional)" hör inte dit,
    # och hjälptexterna står på rätt rad.
    src = SRC.read_text(encoding="utf-8")
    boxes = re.findall(r'<div class="prompt">(.*?)</div>', src, re.S)
    assert len(boxes) == 2
    for box in boxes:
        assert "(optional)" not in box
        move_line = next(l for l in box.splitlines() if l.startswith("Study move:"))
        assert "name and one-line description" in move_line
    teacher, student = boxes
    assert "For the AI (teacher)" in next(l for l in teacher.splitlines() if l.startswith("What to make:"))
    assert "For the AI (student)" in next(l for l in student.splitlines() if l.startswith("Your role:"))


def test_pdf_fonts_allowed_weights():
    out = subprocess.run(["pdffonts", str(PDF)], capture_output=True, text=True, check=True).stdout
    assert "HankenGrotesk" in out
    assert not re.search(r"(SemiBold|Bold|Black|Heavy)", out, re.I), out


def test_source_html_is_generated_from_json():
    spec = importlib.util.spec_from_file_location("deck", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.render_deck_html(data()) == SRC.read_text(encoding="utf-8")
