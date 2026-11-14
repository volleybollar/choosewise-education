"""Promptbyggaren på /quality-ladder-ec1c2f8c/ i en riktig webbläsare.

Prompten byggs helt i webbläsaren av assets/js/quality-ladder.js. Sidan har
inget JSON-block: allt som behövs finns i skriptet. Inget sparas och inget
skickas.
Spec: docs/superpowers/specs/2026-11-14-what-teachers-do-design.md
(avsnittet B4 "The prompt builder" — mallen där gäller ord för ord).
"""
import functools
import http.server
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SLUG = "quality-ladder-ec1c2f8c"
SCRIPT = ROOT / "assets" / "js" / "quality-ladder.js"
HINT = "Fill in subject and the task to see your prompt."
TASK = "Why did the Industrial Revolution begin in Britain? Explain with at least two reasons."
CRITERIA = "Gives reasons\nLinks each reason to an effect\nUses evidence"

# Mallen ur spec B4, ifylld för fall A: History, årskurs 8, tre kriterier,
# ingen vanlig miss, ett stycke, andra starka svaret med, engelska. Skriven ut
# i sin helhet med flit: ändras mallen ska detta test säga ifrån.
EXPECTED_A = """Do not include student names or student work in this conversation.

You are helping a Grade 8 History teacher show students what quality looks like in one task. Write three made-up student answers to the task below, at three levels of quality, so that students can compare them with their own draft and see what would lift it one level. These are teaching samples. Do not grade, score or mark them.

The task as students get it:
Why did the Industrial Revolution begin in Britain? Explain with at least two reasons.

Criteria for a strong answer:
1. Gives reasons
2. Links each reason to an effect
3. Uses evidence

Length of a strong answer: one paragraph.

Rules for the samples:
- Write as real Grade 8 students would, in words they use. No names.
- The three samples are about the same length, the longest at most a fifth longer than the shortest. They differ in what they do against the criteria, not in how much they write.
- The weakest sample shows a mistake Grade 8 students often make in this task and meets few of the criteria. The middle one meets some. The strongest meets all of them and is realistic for a strong Grade 8 student, not an expert.
- Apart from that mistake, every fact in the samples is correct.

Write everything in English.

Reply in plain text, no tables, with exactly these five parts:
CRITERIA: the criteria numbered, in words a Grade 8 student understands.
FOR STUDENTS: the three samples labelled Sample A, Sample B and Sample C, in mixed order so that A is not the weakest, with no levels or comments. This part is handed out as it is.
TEACHER KEY: for each sample, its level (weakest, middle or strongest), one or two lines on what it does and does not do against the criteria, and ONE LEVEL UP: the one change that would lift it a level. For the strongest, say what would make it even better.
SECOND STRONG ANSWER: another strong answer that meets all the criteria in a clearly different way, so that students see there is more than one way to do it well.
QUESTIONS: three questions for the class discussion after students have ranked the samples."""

MISTAKE = "lists causes without effects"
MISTAKE_LINE = f"A common mistake in this task: {MISTAKE}"
LENGTH_LINE = "Length of a strong answer: one paragraph."
NO_CRITERIA = ("Criteria: none given. First write three to five criteria for a strong answer "
               "to this task at Grade 8, then use them.")
WEAKEST_WITH_MISTAKE = ("- The weakest sample shows the common mistake above and meets few of the criteria. "
                        "The middle one meets some.")


@pytest.fixture(scope="module")
def site():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    class Server(socketserver.TCPServer):
        allow_reuse_address = True

    srv = Server(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()


@pytest.fixture(scope="module")
def browser():
    pw = pytest.importorskip("playwright.sync_api").sync_playwright().start()
    b = pw.chromium.launch()
    yield b
    b.close()
    pw.stop()


def open_page(site, browser):
    p = browser.new_page()
    p.errors = []
    p.on("console", lambda m: m.type == "error" and p.errors.append(f"{m.text} {m.location.get('url', '')}"))
    p.on("pageerror", lambda e: p.errors.append(str(e)))
    p.goto(f"{site}/{SLUG}/", wait_until="networkidle")
    # Kort tidsgräns: saknas skriptet ska testet falla direkt, inte efter 30 s.
    p.wait_for_function("window.QualityLadder && typeof window.QualityLadder.buildPrompt === 'function'",
                        timeout=3000)
    return p


@pytest.fixture
def page(site, browser):
    p = open_page(site, browser)
    yield p
    p.close()


def fill(page, subject="History", grade="8", task=TASK, criteria=CRITERIA, mistake="",
         length="One paragraph", second=True, language="English"):
    """Fyller i formuläret som en lärare: ett fält i taget, så varje fält ger en egen händelse."""
    page.fill("#ql-subject", subject)
    page.select_option("#ql-grade", grade)
    page.fill("#ql-task", task)
    page.fill("#ql-criteria", criteria)
    page.fill("#ql-mistake", mistake)
    page.select_option("#ql-length", length)
    page.set_checked("#ql-second", second)
    page.fill("#ql-language", language)


def prompt(page):
    return page.input_value("#ql-prompt")


def test_script_exists():
    assert SCRIPT.is_file(), "assets/js/quality-ladder.js saknas"


def test_empty_state(page):
    assert prompt(page) == ""
    assert page.is_disabled("#ql-copy")
    assert page.get_attribute("#ql-copy", "data-copy") == ""
    assert page.text_content("#ql-hint").strip() == HINT


@pytest.mark.parametrize("empty", ["subject", "task"])
def test_missing_required_field_empties_prompt(page, empty):
    fill(page)
    assert prompt(page) == EXPECTED_A
    page.fill("#ql-subject" if empty == "subject" else "#ql-task", "   ")
    assert prompt(page) == ""
    assert page.is_disabled("#ql-copy")
    assert page.get_attribute("#ql-copy", "data-copy") == ""
    assert page.text_content("#ql-hint").strip() == HINT


def test_default_prompt(page):
    fill(page)
    assert prompt(page) == EXPECTED_A
    assert page.get_attribute("#ql-copy", "data-copy") == EXPECTED_A
    assert page.is_enabled("#ql-copy")
    assert page.text_content("#ql-hint").strip() == ""


def test_mistake_line(page):
    fill(page, mistake=MISTAKE)
    text = prompt(page)
    assert f"{MISTAKE_LINE}\n{LENGTH_LINE}" in text
    assert WEAKEST_WITH_MISTAKE in text
    assert "a mistake Grade 8 students often make" not in text
    fill(page, mistake="")
    assert prompt(page) == EXPECTED_A


def test_empty_criteria(page):
    for empty in ("", "\n  \n"):
        fill(page, criteria=empty)
        text = prompt(page)
        assert f"The task as students get it:\n{TASK}\n\n{NO_CRITERIA}\n\n{LENGTH_LINE}\n\n" in text
        assert "Criteria for a strong answer" not in text
        assert "\n1. " not in text
        # Delen CRITERIA finns kvar i svarsformatet.
        assert "\nCRITERIA: the criteria numbered" in text


def test_blank_lines_in_criteria(page):
    fill(page, criteria="a\n\n  b \n")
    text = prompt(page)
    assert "Criteria for a strong answer:\n1. a\n2. b\n\n" in text
    assert "3. " not in text


def test_second_toggle(page):
    fill(page)
    page.uncheck("#ql-second")
    text = prompt(page)
    assert "with exactly these four parts:" in text
    assert "five parts" not in text
    assert "SECOND STRONG ANSWER" not in text
    assert text.endswith("QUESTIONS: three questions for the class discussion after students have ranked the samples.")
    page.check("#ql-second")
    assert prompt(page) == EXPECTED_A
    assert page.input_value("#ql-subject") == "History"
    assert page.input_value("#ql-task") == TASK
    assert page.input_value("#ql-criteria") == CRITERIA


def test_language(page):
    fill(page, language="Swedish")
    assert "Write everything in Swedish, but keep the headings in English." in prompt(page)
    assert "Write everything in English." not in prompt(page)
    for english in (" english ", "ENGLISH", ""):
        fill(page, language=english)
        text = prompt(page)
        assert "Write everything in English.\n" in text, repr(english)
        assert "keep the headings" not in text, repr(english)


def test_length_lowercased(page):
    fill(page, length="About a page")
    assert "Length of a strong answer: about a page." in prompt(page)
    fill(page, length="A few sentences")
    assert "Length of a strong answer: a few sentences." in prompt(page)


def test_grade_inserted(page):
    fill(page, grade="3")
    text = prompt(page)
    assert "a Grade 3 History teacher" in text
    assert "as real Grade 3 students would" in text
    assert "a mistake Grade 3 students often make" in text
    assert "realistic for a strong Grade 3 student" in text
    assert "in words a Grade 3 student understands" in text


def test_html_is_literal(page):
    fill(page, task="<b>x</b> </script>")
    assert "The task as students get it:\n<b>x</b> </script>\n" in prompt(page)
    assert page.locator("#ql-builder b").count() == 0


def test_typed_grade_placeholder_is_not_replaced(page):
    fill(page, task="Explain {grade} briefly", criteria="Uses {grade}", mistake="says {grade}")
    text = prompt(page)
    assert "Explain {grade} briefly" in text
    assert "1. Uses {grade}" in text
    assert "A common mistake in this task: says {grade}" in text


def test_build_prompt_is_pure(page):
    inp = {"subject": "History", "grade": "8", "task": TASK, "criteria": CRITERIA.split("\n"),
           "mistake": "", "length": "One paragraph", "second": True, "language": "English"}
    assert page.evaluate("input => window.QualityLadder.buildPrompt(input)", inp) == EXPECTED_A
    assert page.evaluate("input => window.QualityLadder.buildPrompt(input)", inp) == EXPECTED_A


def test_parse_criteria(page):
    assert page.evaluate("t => window.QualityLadder.parseCriteria(t)", "a\n\n  b \n") == ["a", "b"]
    assert page.evaluate("t => window.QualityLadder.parseCriteria(t)", "\n  \n") == []
    assert page.evaluate("t => window.QualityLadder.parseCriteria(t)", "") == []


def test_no_console_errors(site, browser):
    p = open_page(site, browser)
    fill(p, mistake=MISTAKE)
    p.uncheck("#ql-second")
    fill(p, subject="", task="")
    assert p.errors == []
    p.close()
