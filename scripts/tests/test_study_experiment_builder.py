"""Promptbyggaren på /study-experiment/ i en riktig webbläsare.

Prompten byggs helt i webbläsaren av assets/js/study-experiment.js. Inget
sparas och inget skickas, och ingen datafil hämtas: prompten är fast text
med fyra luckor ({g} två gånger, {subject}, {topic}, {language}). Texten är
fastställd ordagrant i specen (avsnittet "Prompt builder"); TEACHER nedan är
en kopia av den.
Spec: docs/superpowers/specs/2026-11-13-study-experiment-design.md.
"""
import functools
import http.server
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
HINT_EMPTY = "Fill in subject and topic area to see your prompt."
PARTS = ["TEXT A:", "TEXT B:", "QUIZ:", "ANSWERS:", "CHECK:"]

TEACHER = """Do not include student names or student work in this conversation.

You are helping a Grade {g} {subject} teacher run a classroom experiment on two study methods. Students will study two short texts: one by reading it twice, the other by reading it once, writing down everything they remember and then checking it against the text. A week later they take a surprise quiz on both texts.

Topic area: {topic}
Write everything in {language}.

Write two texts, TEXT A and TEXT B, each on a different part of this topic area that students have not been taught yet.
- Make each text about 250 words, and keep the two texts within 20 words of each other in length.
- Make them equally hard: ten key facts each, similar sentence length and similar words, at a reading level for Grade {g}.
- Spread the key facts evenly through each text. No headings or lists inside the texts.
- Use only facts that are well established and easy to check.

Then write a quiz: Q1 to Q6 on Text A and Q7 to Q12 on Text B.
- Each question tests a different key point of the text, the kind of thing a student would write down when recalling it. The answer is a word, a number or a short phrase from the text.
- Ask about what this text says, so that a student who has not read it cannot answer from general knowledge. Do not ask what a word means.
- Spread the questions over the whole text, and do not give away one answer in another question.

Reply in plain text, no tables, with exactly these five parts:
TEXT A: a short title, then the text.
TEXT B: a short title, then the text.
QUIZ: the twelve questions, numbered Q1: to Q12:, ready to print.
ANSWERS: the answers, numbered Q1: to Q12: to match, with other answers that should also count as right.
CHECK: every fact, figure, date or name in the texts that the teacher should verify, one per line."""


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


def open_page(site, browser, **kw):
    p = browser.new_page(**kw)
    p.goto(f"{site}/study-experiment/", wait_until="networkidle")
    # Skriptet har laddats när objektet finns (det hämtar ingen data).
    p.wait_for_function("window.StudyExperiment && typeof window.StudyExperiment.buildPrompt === 'function'")
    return p


@pytest.fixture
def page(site, browser):
    p = open_page(site, browser)
    yield p
    p.close()


def fill(page, subject="Biology", grade="9", topic="How animals survive the winter", language="English"):
    page.fill("#se-subject", subject)
    page.select_option("#se-grade", grade)
    page.fill("#se-topic", topic)
    page.fill("#se-language", language)


def prompt(page):
    return page.input_value("#se-prompt")


def test_defaults(page):
    assert page.input_value("#se-grade") == "9"
    assert page.input_value("#se-language") == "English"
    assert page.is_disabled("#se-copy")
    assert prompt(page) == ""
    assert page.text_content("#se-hint").strip() == HINT_EMPTY


def test_build_prompt_matches_spec_word_for_word(page):
    got = page.evaluate(
        "() => window.StudyExperiment.buildPrompt({subject: 'S', grade: '8', topic: 'T', language: 'Swedish'})")
    assert got == TEACHER.format(g="8", subject="S", topic="T", language="Swedish")


def test_prompt(page):
    fill(page)
    text = prompt(page)
    assert text.startswith("Do not include student names or student work")
    assert "Grade 9 Biology teacher" in text
    assert "Topic area: How animals survive the winter" in text
    assert "Write everything in English." in text
    assert "Q1 to Q6 on Text A and Q7 to Q12 on Text B" in text
    lines = text.splitlines()
    for part in PARTS:
        assert any(line.startswith(part) for line in lines), part
    assert page.get_attribute("#se-copy", "data-copy") == text
    assert page.is_enabled("#se-copy")
    assert page.text_content("#se-hint").strip() == ""


def test_prompt_matches_template_via_form(page):
    fill(page, subject="  Biology ", grade="10", topic=" Why? ", language=" Swedish ")
    assert prompt(page) == TEACHER.format(g="10", subject="Biology", topic="Why?", language="Swedish")


def test_language_used(page):
    fill(page, language="Swedish")
    assert "Write everything in Swedish." in prompt(page)
    for empty in ("", "   "):
        fill(page, language=empty)
        assert "Write everything in English." in prompt(page), repr(empty)
        assert page.is_enabled("#se-copy"), repr(empty)


def test_grade_used_twice(page):
    fill(page, grade="11")
    text = prompt(page)
    assert "Grade 11 Biology teacher" in text
    assert "reading level for Grade 11" in text
    assert text.count("Grade 11") == 2


def test_requires_subject_and_topic(page):
    for subject, topic in (("", "Cells"), ("Biology", ""), ("  ", "Cells"), ("Biology", " \n ")):
        fill(page, subject=subject, topic=topic)
        assert page.is_disabled("#se-copy"), (subject, topic)
        assert prompt(page) == "", (subject, topic)
        assert page.get_attribute("#se-copy", "data-copy") == ""
        assert page.is_visible("#se-hint")
        assert page.text_content("#se-hint").strip() == HINT_EMPTY
    fill(page)
    assert page.is_enabled("#se-copy")
    assert page.text_content("#se-hint").strip() == ""


def test_special_characters_kept(page):
    topic = 'Why? "<b>&</b>"\n\nnext'
    fill(page, topic=topic)
    assert "Topic area: " + topic in prompt(page)
    assert page.get_attribute("#se-copy", "data-copy") == prompt(page)
    assert page.locator("main b").count() == 0


def test_hint_beside_disabled_button(site, browser):
    for width in (1280, 390):
        p = open_page(site, browser, viewport={"width": width, "height": 800})
        assert p.is_disabled("#se-copy")
        assert p.locator(".tm-copy-row #se-hint").is_visible(), width
        p.close()
