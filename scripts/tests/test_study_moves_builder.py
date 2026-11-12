"""Promptbyggaren på /study-moves/ i en riktig webbläsare.

Prompten byggs helt i webbläsaren av assets/js/study-moves.js från
study-moves/moves-en.json. Inget sparas och inget skickas. Läraren är
förvald och Test yourself är startdraget. Prompttexterna är fastställda
ordagrant i specen (avsnittet "Prompt builder"); TEACHER och STUDENT nedan
är kopior av dem.
Spec: docs/superpowers/specs/2026-11-12-study-moves-design.md.
"""
import functools
import http.server
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
HINT_EMPTY = "Fill in subject and topic to see your prompt."
HINT_FAILED = "Couldn't load the moves — reload the page."
PARTS = ["MOVE:", "FOR STUDENTS:", "ANSWERS:", "CHECK:"]

TEACHER = """Do not include student names or student work in this conversation.

You are helping a Grade {g} {subject} teacher prepare study material that students will use on their own, on paper and without AI.

Study move: {name}. {one_liner}
What to make: {brief}

Topic: {topic}
Students already know: {prior}

Use only this topic's content. Do not repeat a question. If you write multiple-choice questions, make all options about the same length.

Reply in plain text, no tables, with exactly these four parts:
MOVE: the move's name and one sentence, written to students, on why it works.
FOR STUDENTS: the material, written to the students and ready to print.
ANSWERS: the answers or a checklist students use to check their own work, numbered Q1:, Q2: and so on to match.
CHECK: every fact, figure, date or source in FOR STUDENTS or ANSWERS that the teacher should verify, one per line. Write "None" if there are none."""

STUDENT = """Do not include your name or other personal details in this conversation.

You are my study partner. I am a Grade {g} student studying {subject}.
Topic: {topic}
What I already know: {prior}

Study move: {name}. {one_liner}
Your role: {brief}

Rules for the whole conversation:
- Give me one question or task at a time, then wait for my answer.
- Never give me the answer to a question before I have tried it. If I am stuck, give a small hint first.
- Keep every message short.
- Do not write my homework, essays or answers for me, even if I ask.
- If you are not sure a fact is right, say so. I will check facts in my textbook or notes.

Start now."""

LABELS = {
    "teacher": ("What is the topic?", "What do students already know? (optional)",
                "Do not include student names or student work. The prompt only needs your subject, grade and topic."),
    "student": ("What are you studying?", "What do you already know? (optional)",
                "Do not include your name or other personal details. Check that you are old enough for your AI tool and that your school allows it."),
}


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
    p.goto(f"{site}/study-moves/{query}", wait_until="networkidle")
    p.wait_for_function("document.querySelectorAll('#sm-move option').length === 10")
    return p


@pytest.fixture
def page(site, browser):
    p = open_page(site, browser)
    yield p
    p.close()


def fill(page, subject="Biology", grade="9", topic="Cells and their parts", prior=""):
    page.fill("#sm-subject", subject)
    page.select_option("#sm-grade", grade)
    page.fill("#sm-topic", topic)
    page.fill("#sm-prior", prior)


def prompt(page):
    return page.input_value("#sm-prompt")


def who(page):
    return page.evaluate("() => document.querySelector('input[name=\"sm-who\"]:checked').value")


def texts(page):
    return (page.text_content("#sm-topic-label").strip(), page.text_content("#sm-prior-label").strip(),
            " ".join(page.text_content("#sm-privacy").split()))


def expected(template, prior, **values):
    """Mallen med värden, utan raden om förkunskaper när prior är tom."""
    lines = template.splitlines()
    if not prior:
        lines = [l for l in lines if "{prior}" not in l]
    return "\n".join(lines).format(prior=prior, **values)


def test_defaults(page):
    assert page.input_value("#sm-move") == "test-yourself"
    assert who(page) == "teacher"
    assert page.is_checked("#sm-who-teacher")
    assert page.input_value("#sm-grade") == "9"
    assert "Not sure? Start here." in page.text_content("#sm-start")
    assert texts(page) == LABELS["teacher"]


def test_build_prompt_matches_spec_word_for_word(page):
    move = {"name": "N", "one_liner": "One line.", "teacher_ai": {"brief": "TB"}, "student_ai": {"brief": "SB"}}
    for prior in ("", "P"):
        for kind, template, brief in (("teacher", TEACHER, "TB"), ("student", STUDENT, "SB")):
            got = page.evaluate(
                "(a) => window.StudyMoves.buildPrompt({who: a.who, move: a.move, subject: 'S', grade: '8', topic: 'T', prior: a.prior})",
                {"who": kind, "move": move, "prior": prior})
            assert got == expected(template, prior, g="8", subject="S", name="N", one_liner="One line.",
                                   brief=brief, topic="T"), (kind, prior)


def test_teacher_prompt(page):
    fill(page, topic="Cells and their parts")
    text = prompt(page)
    assert text.startswith("Do not include student names or student work")
    assert "Grade 9 Biology teacher" in text
    assert "Study move: Test yourself." in text
    assert "What to make: " in text
    assert "Topic: Cells and their parts" in text
    lines = text.splitlines()
    for part in PARTS:
        assert any(line.startswith(part) for line in lines), part
    assert "numbered Q1:" in text


def test_student_prompt(page):
    fill(page)
    page.check("#sm-who-student")
    text = prompt(page)
    assert text.startswith("Do not include your name or other personal details")
    assert "I am a Grade 9 student studying Biology." in text
    assert "Your role: " in text
    assert "Never give me the answer to a question before I have tried it." in text
    assert "even if I ask" in text
    assert text.endswith("Start now.")
    assert "FOR STUDENTS:" not in text


def test_switch_updates_everything(page):
    fill(page, prior="Plants need light")
    teacher = (prompt(page), texts(page), page.get_attribute("#sm-copy", "data-copy"))
    assert teacher[1] == LABELS["teacher"] and teacher[2] == teacher[0]
    page.check("#sm-who-student")
    student = (prompt(page), texts(page), page.get_attribute("#sm-copy", "data-copy"))
    assert student[1] == LABELS["student"] and student[2] == student[0]
    assert student[0] != teacher[0] and student[0].startswith("Do not include your name")
    page.check("#sm-who-teacher")
    assert (prompt(page), texts(page), page.get_attribute("#sm-copy", "data-copy")) == teacher


def test_prior_lines_only_when_filled(page):
    for kind, line in (("teacher", "Students already know: "), ("student", "What I already know: ")):
        page.check(f"#sm-who-{kind}")
        fill(page)
        assert prompt(page) and "already know" not in prompt(page), kind
        fill(page, prior="  ")
        assert "already know" not in prompt(page), kind
        fill(page, prior="Plants need light")
        assert line + "Plants need light" in prompt(page), kind


def test_requires_subject_and_topic(page):
    for subject, topic in (("", "Cells"), ("Biology", ""), ("  ", "Cells"), ("Biology", " \n ")):
        fill(page, subject=subject, topic=topic)
        assert page.is_disabled("#sm-copy"), (subject, topic)
        assert prompt(page) == "", (subject, topic)
        assert page.get_attribute("#sm-copy", "data-copy") == ""
        assert page.is_visible("#sm-hint")
        assert page.text_content("#sm-hint").strip() == HINT_EMPTY
    fill(page)
    assert page.is_enabled("#sm-copy")
    assert page.text_content("#sm-hint").strip() == ""


def test_special_characters_kept(page):
    topic = 'Why? "<b>&</b>"\n\nnext'
    for kind in ("teacher", "student"):
        page.check(f"#sm-who-{kind}")
        fill(page, topic=topic)
        assert "Topic: " + topic in prompt(page), kind
        assert page.get_attribute("#sm-copy", "data-copy") == prompt(page)
    assert page.locator("main b").count() == 0


def test_query_preselects(site, browser):
    p = open_page(site, browser, "?move=draw-it&for=student")
    assert p.input_value("#sm-move") == "draw-it"
    assert who(p) == "student"
    assert texts(p) == LABELS["student"]
    p.close()


def test_bad_query_falls_back(site, browser):
    # Objektets egna egenskapsnamn får inte hitta något (movesById utan prototyp).
    for query in ("?move=constructor", "?move=__proto__", "?move=toString", "?for=admin",
                  "?move=constructor&for=__proto__"):
        p = open_page(site, browser, query)
        assert p.input_value("#sm-move") == "test-yourself", query
        assert who(p) == "teacher", query
        p.close()


def test_card_links_set_move_and_who(page):
    page.click("#ask-why summary")
    page.click('#ask-why a[data-use-for="student"]')
    assert page.input_value("#sm-move") == "ask-why"
    assert who(page) == "student"
    assert texts(page) == LABELS["student"]
    page.click('#draw-it a[data-use-for="teacher"]')
    assert page.input_value("#sm-move") == "draw-it"
    assert who(page) == "teacher"


def test_fetch_failure(site, browser):
    p = browser.new_page()
    p.route("**/moves-en.json", lambda route: route.fulfill(status=500, body=""))
    p.goto(f"{site}/study-moves/", wait_until="networkidle")
    p.wait_for_function("document.getElementById('sm-hint').textContent.includes('reload')")
    assert p.text_content("#sm-hint").strip() == HINT_FAILED
    assert p.locator("article.sm-move").count() == 10
    assert p.locator("#sm-goals .sm-goal").count() == 6
    assert p.locator("#sm-goals .sm-goal").first.is_visible()
    assert p.is_disabled("#sm-copy")
    # Valet Teacher/Student får inte skriva över felmeddelandet.
    p.check("#sm-who-student")
    assert p.text_content("#sm-hint").strip() == HINT_FAILED
    assert p.is_disabled("#sm-copy")
    p.close()


def test_hint_beside_disabled_button(site, browser):
    for width in (1280, 390):
        p = open_page(site, browser, viewport={"width": width, "height": 800})
        assert p.is_disabled("#sm-copy")
        assert p.locator(".tm-copy-row #sm-hint").is_visible(), width
        p.close()
