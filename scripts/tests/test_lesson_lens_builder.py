"""Promptbyggaren på /lesson-lens/ i en riktig webbläsare.

Prompten byggs helt i webbläsaren av assets/js/lesson-lens.js från
lesson-lens/lenses-en.json. Inget sparas och inget skickas.
Formative check är förvald ("Not sure? Start here.", Johans beslut 2026-10-29).
Spec: docs/superpowers/specs/2026-10-29-lesson-lens-design.md.
"""
import functools
import http.server
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PARTS = ["KEEP:", "UPGRADE:", "NUDGE:", "CHECK:"]
LESSON = "Starter quiz on cells\nDemonstration with a microscope\nWorksheet on cell parts\nExit question"


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
    p.goto(f"{site}/lesson-lens/{query}", wait_until="networkidle")
    p.wait_for_function("document.querySelectorAll('#ll-lens option').length === 12")
    return p


@pytest.fixture
def page(site, browser):
    p = open_page(site, browser)
    yield p
    p.close()


def fill(page, subject="Biology", grade="8", lesson=LESSON, prior="", lens2=""):
    page.fill("#ll-subject", subject)
    page.select_option("#ll-grade", grade)
    page.fill("#ll-lesson", lesson)
    page.fill("#ll-prior", prior)
    page.select_option("#ll-lens2", lens2)


def prompt(page):
    return page.input_value("#ll-prompt")


def test_default_lens_preselected(page):
    assert page.input_value("#ll-lens") == "formative-check"
    assert "Not sure? Start here." in page.text_content("#ll-start")


def test_prompt_contains_inputs_and_four_parts(page):
    fill(page, prior="What a cell is")
    text = prompt(page)
    assert text.startswith("Do not include student names or student work")
    assert "Grade 8 Biology teacher" in text
    assert "Lens: Formative check (hinge question, exit ticket)." in text
    assert LESSON in text
    assert "Students already know: What a cell is" in text
    assert "at most two changes in total" in text
    lines = text.splitlines()
    for part in PARTS:
        assert any(line.startswith(part) for line in lines), part


def test_second_lens_block(page):
    fill(page, lens2="retrieval-practice")
    assert "Second lens: Retrieval practice." in prompt(page)
    page.select_option("#ll-lens2", "")
    assert "Second lens:" not in prompt(page)


def test_same_lens_twice_counts_once(page):
    fill(page, lens2="formative-check")
    text = prompt(page)
    assert "Second lens:" not in text
    assert text.count("Formative check (hinge question, exit ticket).") == 1


def test_prior_line_omitted_when_empty(page):
    fill(page)
    assert prompt(page)
    assert "Students already know" not in prompt(page)


def test_builder_requires_fields(page):
    fill(page, lesson="   ")
    assert page.is_disabled("#ll-copy")
    assert prompt(page) == ""
    assert page.is_visible("#ll-hint")
    fill(page, subject="  ")
    assert page.is_disabled("#ll-copy")
    assert prompt(page) == ""


def test_builder_keeps_special_characters(page):
    lesson = 'Starter: "Why?" <b>&</b>\n\nDemo'
    fill(page, lesson=lesson)
    assert lesson in prompt(page)
    assert page.locator("main b").count() == 0


def test_copy_button_matches_prompt(page):
    fill(page)
    assert page.is_enabled("#ll-copy")
    assert page.get_attribute("#ll-copy", "data-copy") == prompt(page)


def test_lens_preselect_from_query(site, browser):
    p = open_page(site, browser, "?lens=spacing")
    assert p.input_value("#ll-lens") == "spacing"
    p.close()


def test_use_this_lens_link_selects_lens(page):
    page.click('#belonging summary')
    page.click('#belonging a[data-use-lens="belonging"]')
    assert page.input_value("#ll-lens") == "belonging"


def test_builder_fetch_failure(site, browser):
    p = browser.new_page()
    p.route("**/lenses-en.json", lambda route: route.fulfill(status=500, body=""))
    p.goto(f"{site}/lesson-lens/", wait_until="networkidle")
    p.wait_for_function("document.getElementById('ll-hint').textContent.includes('reload')")
    assert p.text_content("#ll-hint").strip() == "Couldn't load the lenses — reload the page."
    assert p.locator("article.ll-lens").count() == 12
    assert p.locator(".ll-hero-example .ll-example").count() == 1
    assert p.is_disabled("#ll-copy")
    p.close()


def test_hint_is_shown_beside_disabled_copy_button(site, browser):
    for width in (1280, 390):
        p = open_page(site, browser, viewport={"width": width, "height": 800})
        assert p.is_disabled("#ll-copy")
        assert p.locator(".tm-copy-row #ll-hint").is_visible(), width
        p.close()
