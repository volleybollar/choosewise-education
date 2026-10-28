"""Promptbyggaren på /thinking-moves/ i en riktig webbläsare.

Prompten byggs helt i webbläsaren av assets/js/thinking-moves.js från
thinking-moves/moves-en.json. Inget sparas och inget skickas.
Spec: docs/superpowers/specs/2026-10-27-thinking-moves-design.md.
"""
import functools
import http.server
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PARTS = ["MOVE:", "TASK:", "LOOK FOR:", "PROBE:", "THINK BACK:", "CHECK:"]


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
    p.goto(f"{site}/thinking-moves/", wait_until="networkidle")
    p.wait_for_function("document.querySelectorAll('#tm-move option').length === 12")
    yield p
    p.close()


def fill(page, move="best-explanation", subject="Chemistry", topic="Rates of reaction", grade="10", prior=""):
    page.select_option("#tm-move", move)
    page.fill("#tm-subject", subject)
    page.select_option("#tm-grade", grade)
    page.fill("#tm-topic", topic)
    page.fill("#tm-prior", prior)


def prompt(page):
    return page.input_value("#tm-prompt")


def test_prompt_contains_all_inputs_and_six_parts(page):
    fill(page, prior="Particle model")
    text = prompt(page)
    assert "Grade 10 Chemistry teacher" in text
    assert "Lesson topic: Rates of reaction" in text
    assert "Thinking move: Best explanation." in text
    assert "Students already know: Particle model" in text
    assert text.startswith("Do not include student names or student work")
    lines = [line for line in text.splitlines()]
    for part in PARTS:
        assert any(line.startswith(part) for line in lines), part


def test_prior_line_omitted_when_empty(page):
    fill(page)
    assert prompt(page)
    assert "Students already know" not in prompt(page)


def test_builder_requires_fields(page):
    fill(page, topic="   ")
    assert page.is_disabled("#tm-copy")
    assert prompt(page) == ""
    assert page.is_visible("#tm-hint")
    fill(page, subject="  ", topic="Rates of reaction")
    assert page.is_disabled("#tm-copy")


def test_builder_keeps_special_characters(page):
    topic = 'Ohm\'s law "V = IR" <b>&</b>\nline 2'
    fill(page, topic=topic)
    assert topic in prompt(page)
    assert page.locator("main b").count() == 0


def test_copy_button_matches_prompt(page):
    fill(page)
    assert page.is_enabled("#tm-copy")
    assert page.get_attribute("#tm-copy", "data-copy") == prompt(page)


def test_move_preselect_from_query(site, browser):
    p = browser.new_page()
    p.goto(f"{site}/thinking-moves/?move=then-what", wait_until="networkidle")
    p.wait_for_function("document.querySelectorAll('#tm-move option').length === 12")
    assert p.input_value("#tm-move") == "then-what"
    p.close()


def test_use_this_move_link_selects_move(page):
    page.click('#map-the-loop a[data-use-move="map-the-loop"]')
    assert page.input_value("#tm-move") == "map-the-loop"


def test_builder_fetch_failure(site, browser):
    p = browser.new_page()
    p.route("**/moves-en.json", lambda route: route.fulfill(status=500, body=""))
    p.goto(f"{site}/thinking-moves/", wait_until="networkidle")
    p.wait_for_function("document.getElementById('tm-hint').textContent.includes('reload')")
    assert p.text_content("#tm-hint").strip() == "Couldn't load the moves — reload the page."
    assert p.locator("article.tm-move").count() == 12
    assert p.is_disabled("#tm-copy")
    p.close()


def test_copied_toast_does_not_cover_the_button(site, browser):
    p = browser.new_page(viewport={"width": 390, "height": 800})
    p.goto(f"{site}/thinking-moves/", wait_until="networkidle")
    btn = p.locator("#tm-copy").bounding_box()
    toast = p.locator(".tm-copy-row .copy-toast").bounding_box()
    apart = (toast["x"] >= btn["x"] + btn["width"] or toast["y"] >= btn["y"] + btn["height"])
    assert apart, (btn, toast)
    p.close()


def test_copy_toast_text_changes_so_screen_readers_hear_it(site, browser):
    ctx = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
    p = ctx.new_page()
    p.goto(f"{site}/thinking-moves/", wait_until="networkidle")
    p.wait_for_function("document.querySelectorAll('#tm-move option').length === 12")
    fill(p)
    p.evaluate("""() => {
        window.__toastChanges = 0;
        new MutationObserver(m => { window.__toastChanges += m.length; })
          .observe(document.querySelector('.tm-copy-row .copy-toast'), {childList: true, characterData: true, subtree: true});
    }""")
    p.click("#tm-copy")
    p.wait_for_function("window.__toastChanges >= 2")
    p.wait_for_function("document.querySelector('.tm-copy-row .copy-toast').textContent === 'Copied'")
    ctx.close()


def test_hint_is_shown_beside_disabled_copy_button(site, browser):
    for width in (1280, 390):
        p = browser.new_page(viewport={"width": width, "height": 800})
        p.goto(f"{site}/thinking-moves/", wait_until="networkidle")
        p.wait_for_function("document.querySelectorAll('#tm-move option').length === 12")
        assert p.is_disabled("#tm-copy")
        assert p.locator(".tm-copy-row #tm-hint").is_visible(), width
        btn = p.locator("#tm-copy").bounding_box()
        hint = p.locator("#tm-hint").bounding_box()
        assert hint["y"] < btn["y"] + btn["height"] + 40, (width, btn, hint)
        p.close()


def test_move_cards_side_by_side_are_equal_height(site, browser):
    # Kort som står bredvid varandra i samma rad ska vara lika höga.
    for width in (1280, 900):
        p = browser.new_page(viewport={"width": width, "height": 900})
        p.goto(f"{site}/thinking-moves/", wait_until="networkidle")
        rows = {}
        for box in (c.bounding_box() for c in p.locator("article.tm-move").all()):
            rows.setdefault(round(box["y"]), []).append(box["height"])
        assert any(len(h) > 1 for h in rows.values()), width
        for heights in rows.values():
            assert max(heights) - min(heights) < 1, (width, heights)
        p.close()
