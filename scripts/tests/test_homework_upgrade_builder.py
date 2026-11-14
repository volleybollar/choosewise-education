"""Promptbyggaren på /homework-upgrade-1f0cd17c/ i en riktig webbläsare.

Prompten byggs helt i webbläsaren av assets/js/homework-upgrade.js. Mönstren
läses ur JSON-blocket #hu-data i sidan. Inget sparas och inget skickas.
Spec: docs/superpowers/specs/2026-11-14-homework-upgrade-design.md
(avsnittet "The prompt builder" — mallen där gäller ord för ord).
"""
import functools
import http.server
import json
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SLUG = "homework-upgrade-1f0cd17c"
DATA = ROOT / SLUG / "upgrade-en.json"
HINT = "Fill in subject and the homework to see your prompt."
HOMEWORK = "Read chapter 4, pages 62–71.\nAnswer questions 1–6 on page 72."

# Mallen ur spec, ifylld för fall A: inget valt mönster, History, årskurs 9,
# två rader läxa, inget mål, 20 minuter, engelska. Skriven ut i sin helhet med
# flit: ändras mallen ska detta test säga ifrån.
EXPECTED_A = """Do not include student names or student work in this conversation.

You are helping a Grade 9 History teacher upgrade a homework task they have already set. Students do it at home on their own, and most of them can reach a chatbot. Keep the teacher's content and purpose. Change how students work, so that they practise from memory and the next lesson shows what each student can do alone.

The homework as set:
Read chapter 4, pages 62–71.
Answer questions 1–6 on page 72.

Time at home: about 20 minutes.

Pattern: choose the one that fits this homework best, for example answering from memory before opening the book, writing down everything students remember after reading, self-test cards, a solved example followed by a similar problem, a mixed problem set, or explaining or drawing from memory.

Rules for the upgraded homework:
- Unless the pattern says otherwise, students do the main part with the book and notes closed, then open them to check, correct and add what was missing in a different colour.
- If students are likely to remember very little, give them headings or a few prompts to recall from.
- It needs only paper, a pen and material students already have: no AI, no apps, nothing to print at home.
- It practises the content of the original task, nothing new. It takes no longer than the original task and fits in the time above.
- If you write new questions or problems, put their answers at the end of the homework, so students can check their own work.
- It ends by telling students that the next lesson starts with three short questions on it, with books closed.
- Write it to the student, in plain words a Grade 9 student can follow alone.

Write everything in English.

Reply in plain text, no tables, with exactly these four parts:
KEEP: one or two lines on what already works in the task and why, for example a clear purpose or a link to the lesson.
UPGRADE: the new homework written to the student, ready to hand out: numbered steps, then any questions or problems in their own numbered list.
AI RISK: one line on how easily a chatbot could do the original task, and one line on what a student would lose by letting a chatbot do the upgraded one and how the check below would show it. Do not call any version AI-proof.
CHECK: three short questions for the start of the next lesson, on what the homework practised and in the same kind of task, answered on paper with books closed in about four minutes, numbered Q1:, Q2: and Q3:. At least one asks students to use the content, not only repeat it. Then the answers, numbered A1:, A2: and A3:. The check is not graded: students mark their own answers. End with one line on what to do if many students miss the same question."""

GOAL = "Explain why it began in Britain"
GOAL_LINE = f"What students should be able to do afterwards: {GOAL}"
TIME_LINE = "Time at home: about 20 minutes."


def patterns():
    """De tolv mönstren ur JSON-filen, i sidans ordning."""
    return json.loads(DATA.read_text(encoding="utf-8"))["patterns"]


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


def open_page(site, browser, query="", **kw):
    p = browser.new_page(**kw)
    p.errors = []
    p.on("console", lambda m: m.type == "error" and p.errors.append(f"{m.text} {m.location.get('url', '')}"))
    p.on("pageerror", lambda e: p.errors.append(str(e)))
    p.goto(f"{site}/{SLUG}/{query}", wait_until="networkidle")
    # Kort tidsgräns: saknas skriptet ska testet falla direkt, inte efter 30 s.
    p.wait_for_function("window.HomeworkUpgrade && typeof window.HomeworkUpgrade.buildPrompt === 'function'",
                        timeout=3000)
    return p


@pytest.fixture
def page(site, browser):
    p = open_page(site, browser)
    yield p
    p.close()


def fill(page, subject="History", homework=HOMEWORK, goal="", grade="9", minutes="20", language="English"):
    """Fyller i formuläret som en lärare: ett fält i taget, så varje fält ger en egen händelse."""
    page.fill("#hu-subject", subject)
    page.select_option("#hu-grade", grade)
    page.fill("#hu-homework", homework)
    page.fill("#hu-goal", goal)
    page.select_option("#hu-minutes", minutes)
    page.fill("#hu-language", language)


def prompt(page):
    return page.input_value("#hu-prompt")


def test_empty_state(page):
    assert prompt(page) == ""
    assert page.is_disabled("#hu-copy")
    assert page.get_attribute("#hu-copy", "data-copy") == ""
    assert page.text_content("#hu-hint").strip() == HINT


def test_case_a_prompt_exact(page):
    fill(page)
    assert prompt(page) == EXPECTED_A
    assert page.text_content("#hu-hint").strip() == ""
    assert page.is_enabled("#hu-copy")


def test_goal_line_only_when_filled(page):
    fill(page, goal=GOAL)
    assert f"{GOAL_LINE}\n{TIME_LINE}" in prompt(page)
    fill(page, goal="")
    assert GOAL_LINE not in prompt(page)
    assert "What students should be able to do afterwards" not in prompt(page)
    assert prompt(page) == EXPECTED_A


def test_grade_and_minutes_inserted(page):
    fill(page, grade="11", minutes="45")
    text = prompt(page)
    assert "a Grade 11 History teacher" in text
    assert "a Grade 11 student can follow alone" in text
    assert "Time at home: about 45 minutes." in text
    assert "Grade 9" not in text


def test_language_lines(page):
    fill(page, language="Svenska")
    text = prompt(page)
    assert "Write everything in Svenska, but keep the four headings in English." in text
    assert "Write everything in English." not in text
    for language in ("english", " English ", ""):
        fill(page, language=language)
        text = prompt(page)
        assert "Write everything in English." in text, repr(language)
        assert "but keep the four headings" not in text, repr(language)


def test_each_pattern_brief_reaches_prompt(page):
    values = page.eval_on_selector_all("#hu-pattern option", "els => els.map(e => e.value)")
    assert values[0] == ""
    assert values[1:] == [p["id"] for p in patterns()]
    fill(page)
    for p in patterns():
        page.select_option("#hu-pattern", p["id"])
        text = prompt(page)
        assert f"Pattern: {p['name']}. {p['brief']}" in text, p["id"]
        assert "Pattern: choose the one that fits" not in text, p["id"]


def test_multiline_homework_keeps_line_breaks(page):
    homework = "Read pages 10–15.\nMake notes.\nAnswer question 3."
    fill(page, homework=homework)
    assert f"The homework as set:\n{homework}\n\nTime at home:" in prompt(page)


def test_whitespace_only_fields_count_as_empty(page):
    fill(page, subject="   ")
    assert page.is_disabled("#hu-copy")
    assert prompt(page) == ""
    assert page.text_content("#hu-hint").strip() == HINT
    fill(page, homework="  \n  ")
    assert page.is_disabled("#hu-copy")
    assert prompt(page) == ""


def test_special_characters_kept(page):
    homework = 'Read <b>pages</b> & answer "Q1"'
    fill(page, homework=homework)
    assert homework in prompt(page)
    # Texten sätts som värde, aldrig som HTML.
    assert page.locator("#hu-builder b").count() == 0


def test_copy_button_matches_prompt(page):
    fill(page)
    assert page.is_enabled("#hu-copy")
    assert page.get_attribute("#hu-copy", "data-copy") == prompt(page)


def test_pattern_preselect_from_query(site, browser):
    p = open_page(site, browser, "?pattern=mixed-set")
    assert p.input_value("#hu-pattern") == "mixed-set"
    p.close()
    # Egenskapsnamn på objekt och okända id:n lämnar "Let the AI choose".
    for name in ("constructor", "__proto__", "nope"):
        p = open_page(site, browser, f"?pattern={name}")
        assert p.input_value("#hu-pattern") == "", name
        # Listan ska stå kvar på "Let the AI choose", inte bli blank.
        assert p.eval_on_selector("#hu-pattern", "s => s.options[s.selectedIndex].text") == "Let the AI choose", name
        p.close()


def test_use_pattern_link_keeps_typed_text(page):
    page.fill("#hu-subject", "History")
    page.fill("#hu-homework", HOMEWORK)
    page.click('a[data-use-pattern="mixed-set"]')
    assert page.input_value("#hu-pattern") == "mixed-set"
    assert page.input_value("#hu-subject") == "History"
    assert page.input_value("#hu-homework") == HOMEWORK
    assert page.evaluate("window.location.search") == ""
    assert "Pattern: Mixed set." in prompt(page)


def test_build_prompt_is_pure(page):
    text = page.evaluate(
        "input => window.HomeworkUpgrade.buildPrompt(input)",
        {"pattern": None, "subject": "History", "grade": "9", "homework": HOMEWORK,
         "goal": "", "minutes": "20", "language": "English"},
    )
    assert text == EXPECTED_A


def test_no_console_errors(site, browser):
    p = open_page(site, browser)
    fill(p)
    p.select_option("#hu-pattern", "mixed-set")
    p.click('a[data-use-pattern="ask-why"]')
    assert p.errors == []
    p.close()
