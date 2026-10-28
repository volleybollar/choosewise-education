"""Promptbyggaren på /flawed-answer/ i en riktig webbläsare.

Prompten byggs helt i webbläsaren av assets/js/flawed-answer.js från
flawed-answer/flaws-en.json. Inget sparas och inget skickas.
Spec: docs/superpowers/specs/2026-10-28-flawed-answer-design.md.
"""
import functools
import http.server
import json
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "flawed-answer/flaws-en.json"
PARTS = ["QUESTION:", "ANSWER:", "THE FLAW:", "FIX:", "WHY IT CONVINCES:", "TEST IT:",
         "PROBE:", "THINK BACK:", "CHECK:"]
READY = "document.querySelectorAll('#fa-flaw option').length === 6"


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


@pytest.fixture
def page(site, browser):
    p = browser.new_page()
    p.goto(f"{site}/flawed-answer/", wait_until="networkidle")
    p.wait_for_function(READY)
    yield p
    p.close()


def fill(page, flaw="missing-step", subject="Chemistry", topic="Rates of reaction", grade="10", prior=""):
    page.select_option("#fa-flaw", flaw)
    page.fill("#fa-subject", subject)
    page.select_option("#fa-grade", grade)
    page.fill("#fa-topic", topic)
    page.fill("#fa-prior", prior)


def prompt(page):
    return page.input_value("#fa-prompt")


def test_prompt_contains_inputs_and_nine_parts(page):
    fill(page, prior="Particle model")
    text = prompt(page)
    assert text.startswith("Do not include student names or student work")
    assert "Grade 10 Chemistry teacher" in text
    assert "Lesson topic: Rates of reaction" in text
    assert "Students already know: Particle model" in text
    assert "Flaw type: Missing step." in text
    assert "Difficulty: Easier to spot." in text
    assert "AI-generated answer" in text
    lines = text.splitlines()
    for part in PARTS:
        assert any(line.startswith(part) for line in lines), part


def test_prior_line_omitted_when_empty(page):
    fill(page)
    assert prompt(page)
    assert "Students already know" not in prompt(page)


def test_builder_requires_fields(page):
    fill(page, topic="   ")
    assert page.is_disabled("#fa-copy")
    assert prompt(page) == ""
    assert page.is_visible("#fa-hint")
    fill(page, subject="  ", topic="Rates of reaction")
    assert page.is_disabled("#fa-copy")
    assert prompt(page) == ""


def test_builder_keeps_special_characters(page):
    topic = 'Ohm\'s law "V = IR" <b>&</b>\nline 2'
    fill(page, topic=topic)
    assert topic in prompt(page)
    assert page.locator("main b").count() == 0


def test_copy_button_matches_prompt(page):
    fill(page)
    assert page.is_enabled("#fa-copy")
    assert page.get_attribute("#fa-copy", "data-copy") == prompt(page)


def test_flaw_preselect_from_query(site, browser):
    p = browser.new_page()
    p.goto(f"{site}/flawed-answer/?flaw=hidden-assumption", wait_until="networkidle")
    p.wait_for_function(READY)
    assert p.input_value("#fa-flaw") == "hidden-assumption"
    p.close()


def test_unknown_flaw_param_is_ignored(site, browser):
    p = browser.new_page()
    errors = []
    p.on("pageerror", lambda e: errors.append(e))
    p.goto(f"{site}/flawed-answer/?flaw=<nope>", wait_until="networkidle")
    p.wait_for_function(READY)
    assert p.input_value("#fa-flaw") == "wrong-cause"
    assert not errors
    p.close()


def test_use_this_flaw_link_selects_flaw(page):
    page.click('#overgeneralisation a[data-use-flaw="overgeneralisation"]')
    assert page.input_value("#fa-flaw") == "overgeneralisation"


def test_level_in_prompt(page):
    fill(page)
    page.check('input[name="fa-level"][value="harder"]')
    assert "Difficulty: Harder to spot." in prompt(page)
    assert "120–150 words" in prompt(page)


def test_level_falls_back_for_easier_only_type(site, browser):
    data = json.loads(DATA.read_text(encoding="utf-8"))
    data["flaws"][2]["harder_ok"] = False  # missing-step
    p = browser.new_page()
    p.route("**/flaws-en.json", lambda route: route.fulfill(
        status=200, content_type="application/json", body=json.dumps(data)))
    p.goto(f"{site}/flawed-answer/", wait_until="networkidle")
    p.wait_for_function(READY)
    fill(p, flaw="wrong-cause")
    p.check('input[name="fa-level"][value="harder"]')
    assert "Difficulty: Harder to spot." in prompt(p)
    p.select_option("#fa-flaw", "missing-step")
    assert p.is_disabled('input[name="fa-level"][value="harder"]')
    assert "Difficulty: Easier to spot." in prompt(p)
    assert p.text_content("#fa-level-note").strip()
    p.select_option("#fa-flaw", "wrong-cause")
    assert p.is_enabled('input[name="fa-level"][value="harder"]')
    p.close()


def test_builder_fetch_failure(site, browser):
    p = browser.new_page()
    p.route("**/flaws-en.json", lambda route: route.fulfill(status=500, body=""))
    p.goto(f"{site}/flawed-answer/", wait_until="networkidle")
    p.wait_for_function("document.getElementById('fa-hint').textContent.includes('reload')")
    assert p.text_content("#fa-hint").strip() == "Couldn't load the flaw types — reload the page."
    assert p.locator("article.fa-flaw").count() == 6
    assert p.is_disabled("#fa-copy")
    p.close()


def test_hint_is_shown_beside_disabled_copy_button(site, browser):
    for width in (1280, 390):
        p = browser.new_page(viewport={"width": width, "height": 800})
        p.goto(f"{site}/flawed-answer/", wait_until="networkidle")
        p.wait_for_function(READY)
        assert p.is_disabled("#fa-copy")
        assert p.locator(".tm-copy-row #fa-hint").is_visible(), width
        btn = p.locator("#fa-copy").bounding_box()
        hint = p.locator("#fa-hint").bounding_box()
        assert hint["y"] < btn["y"] + btn["height"] + 40, (width, btn, hint)
        p.close()


def test_variant_copy_matches_student_prompt(site, browser):
    data = json.loads(DATA.read_text(encoding="utf-8"))
    ctx = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
    p = ctx.new_page()
    p.goto(f"{site}/flawed-answer/", wait_until="networkidle")
    assert p.get_attribute("#fa-variant-copy", "data-copy") == data["variant"]["student_prompt"]
    p.click("#fa-variant-copy")
    assert p.evaluate("navigator.clipboard.readText()") == data["variant"]["student_prompt"]
    ctx.close()


def test_flaw_cards_side_by_side_are_equal_height(site, browser):
    # Kort som står bredvid varandra i samma rad ska vara lika höga.
    for width in (1280, 900):
        p = browser.new_page(viewport={"width": width, "height": 900})
        p.goto(f"{site}/flawed-answer/", wait_until="networkidle")
        rows = {}
        for box in (c.bounding_box() for c in p.locator("article.fa-flaw").all()):
            rows.setdefault(round(box["y"]), []).append(box["height"])
        assert any(len(h) > 1 for h in rows.values()), width
        for heights in rows.values():
            assert max(heights) - min(heights) < 1, (width, heights)
        p.close()
