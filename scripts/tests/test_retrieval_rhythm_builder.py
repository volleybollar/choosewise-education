"""Promptbyggaren på /retrieval-rhythm/ i en riktig webbläsare.

Prompten byggs helt i webbläsaren av assets/js/retrieval-rhythm.js från
retrieval-rhythm/rhythm-en.json. Inget sparas och inget skickas.
Spec: docs/superpowers/specs/2026-10-30-retrieval-rhythm-design.md.
"""
import functools
import http.server
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PARTS = ["LESSON:", "STARTER:", "KEY:", "CHECK:"]
LOG = "2026-09-01\tCauses of WWI\tMAIN\n2026-10-27\tPropaganda\tDORA 1914"


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
    p.goto(f"{site}/retrieval-rhythm/{query}", wait_until="networkidle")
    p.wait_for_function("document.querySelectorAll('#rr-format option').length === 6")
    return p


@pytest.fixture
def page(site, browser):
    p = open_page(site, browser)
    yield p
    p.close()


def fill(page, subject="History", grade="9", lessons="3", questions="5", date="", log=LOG):
    page.fill("#rr-subject", subject)
    page.select_option("#rr-grade", grade)
    page.select_option("#rr-lessons", lessons)
    page.select_option("#rr-questions", questions)
    page.fill("#rr-date", date)
    page.fill("#rr-log", log)


def prompt(page):
    return page.input_value("#rr-prompt")


def test_default_format_is_mix(page):
    assert page.input_value("#rr-format") == "mix"


def test_prompt_contains_inputs_and_parts(page):
    fill(page, date="2026-11-02")
    text = prompt(page)
    assert text.startswith("Do not include student names or student results")
    assert "Grade 9 History teacher" in text
    assert "Format: Mix." in text
    assert "Number of lessons: 3" in text
    assert "Questions per starter: 5" in text
    assert "First lesson: 2026-11-02" in text
    assert LOG in text
    lines = text.splitlines()
    for part in PARTS:
        assert any(line.startswith(part) for line in lines), part


def test_date_line_omitted_when_empty(page):
    fill(page)
    assert prompt(page)
    assert "First lesson:" not in prompt(page)


def test_log_keeps_tabs_and_special_characters(page):
    log = 'Week 1\t"Atoms" <b>&</b>\n\nWeek 2\tIons'
    fill(page, log=log)
    assert log in prompt(page)
    assert page.locator("main b").count() == 0


def test_builder_requires_fields(page):
    fill(page, log="   ")
    assert page.is_disabled("#rr-copy")
    assert prompt(page) == ""
    assert page.is_visible("#rr-hint")
    fill(page, subject="  ")
    assert page.is_disabled("#rr-copy")
    assert prompt(page) == ""


def test_copy_button_matches_prompt(page):
    fill(page)
    assert page.is_enabled("#rr-copy")
    assert page.get_attribute("#rr-copy", "data-copy") == prompt(page)


def test_format_preselect_from_query(site, browser):
    p = open_page(site, browser, "?format=brain-dump")
    assert p.input_value("#rr-format") == "brain-dump"
    p.close()
    for name in ("constructor", "__proto__"):
        p = open_page(site, browser, f"?format={name}")
        assert p.input_value("#rr-format") == "mix", name
        p.close()


def test_use_this_format_link_selects_format(page):
    page.click('#two-things a[data-use-format="two-things"]')
    assert page.input_value("#rr-format") == "two-things"


def test_builder_fetch_failure(site, browser):
    p = browser.new_page()
    p.route("**/rhythm-en.json", lambda route: route.fulfill(status=500, body=""))
    p.goto(f"{site}/retrieval-rhythm/", wait_until="networkidle")
    p.wait_for_function("document.getElementById('rr-hint').textContent.includes('reload')")
    assert p.text_content("#rr-hint").strip() == "Couldn't load the formats — reload the page."
    assert p.locator("article.rr-format").count() == 5
    assert p.locator(".rr-hero-example .rr-example").count() == 1
    assert p.is_disabled("#rr-copy")
    p.close()


def test_hint_is_shown_beside_disabled_copy_button(site, browser):
    for width in (1280, 390):
        p = open_page(site, browser, viewport={"width": width, "height": 800})
        assert p.is_disabled("#rr-copy")
        assert p.locator(".tm-copy-row #rr-hint").is_visible(), width
        p.close()
