"""Promptbyggaren på /side-by-side/ i en riktig webbläsare.

Prompten byggs helt i webbläsaren av assets/js/side-by-side.js från
side-by-side/pairs-en.json. Inget sparas och inget skickas.
Spec: docs/superpowers/specs/2026-10-28-side-by-side-design.md.
"""
import functools
import http.server
import json
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "side-by-side/pairs-en.json"
STUDENT_PARTS = ["TASK:", "A:", "B:", "CASE C:", "THINK BACK:"]
KEY_PARTS = ["ONLY A:", "BOTH:", "ONLY B:", "THE RULE:", "CASE C ANSWER:", "PROBE:", "CHECK:"]
READY = "document.querySelectorAll('#sb-pair option').length === 5"


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
    p.goto(f"{site}/side-by-side/", wait_until="networkidle")
    p.wait_for_function(READY)
    yield p
    p.close()


def fill(page, pair="two-ways", subject="Chemistry", topic="Rates of reaction", grade="10", prior=""):
    page.select_option("#sb-pair", pair)
    page.fill("#sb-subject", subject)
    page.select_option("#sb-grade", grade)
    page.fill("#sb-topic", topic)
    page.fill("#sb-prior", prior)


def prompt(page):
    return page.input_value("#sb-prompt")


def test_prompt_contains_inputs_and_all_parts(page):
    fill(page, prior="Particle model")
    text = prompt(page)
    assert text.startswith("Do not include student names or student work in this conversation.")
    assert "Grade 10 Chemistry teacher" in text
    assert "Lesson topic: Rates of reaction" in text
    assert "Students already know: Particle model" in text
    assert "Pair type: Two ways to the same answer." in text
    assert "Difficulty: Easier to see." in text
    lines = text.splitlines()
    assert "FOR STUDENTS" in lines and "TEACHER KEY" in lines
    for part in STUDENT_PARTS + KEY_PARTS:
        assert any(line.startswith(part) for line in lines), part


def test_student_block_has_no_key_parts(page):
    fill(page)
    lines = prompt(page).splitlines()
    student, key = lines.index("FOR STUDENTS"), lines.index("TEACHER KEY")
    assert student < key
    for line in lines[:key]:
        assert not any(line.startswith(part) for part in KEY_PARTS), line
    for line in lines[key:]:
        assert not any(line.startswith(part) for part in STUDENT_PARTS if part != "CASE C:"), line


def test_prior_line_omitted_when_empty(page):
    fill(page)
    assert prompt(page)
    assert "Students already know" not in prompt(page)


def test_builder_requires_fields(page):
    fill(page, topic="   ")
    assert page.is_disabled("#sb-copy")
    assert prompt(page) == ""
    assert page.is_visible("#sb-hint")
    fill(page, subject="  ", topic="Rates of reaction")
    assert page.is_disabled("#sb-copy")
    assert prompt(page) == ""


def test_builder_keeps_special_characters(page):
    topic = 'Ohm\'s law "V = IR" <b>&</b>\nline 2'
    fill(page, topic=topic)
    assert topic in prompt(page)
    assert page.locator("main b").count() == 0


def test_copy_button_matches_prompt(page):
    fill(page)
    assert page.is_enabled("#sb-copy")
    assert page.get_attribute("#sb-copy", "data-copy") == prompt(page)


def test_pair_preselect_from_query(site, browser):
    p = browser.new_page()
    p.goto(f"{site}/side-by-side/?pair=two-sources", wait_until="networkidle")
    p.wait_for_function(READY)
    assert p.input_value("#sb-pair") == "two-sources"
    p.close()


def test_unknown_pair_param_is_ignored(site, browser):
    p = browser.new_page()
    errors = []
    p.on("pageerror", lambda e: errors.append(e))
    p.goto(f"{site}/side-by-side/?pair=<nope>", wait_until="networkidle")
    p.wait_for_function(READY)
    assert p.input_value("#sb-pair") == "two-ways"
    assert not errors
    p.close()


def test_use_this_pair_link_selects_pair(page):
    page.click('#one-change a[data-use-pair="one-change"]')
    assert page.input_value("#sb-pair") == "one-change"


def test_level_in_prompt(page):
    fill(page)
    page.check('input[name="sb-level"][value="harder"]')
    assert "Difficulty: Harder to see." in prompt(page)


def test_level_falls_back_for_easier_only_type(site, browser):
    data = json.loads(DATA.read_text(encoding="utf-8"))
    data["pairs"][2]["harder_ok"] = False  # one-change
    p = browser.new_page()
    p.route("**/pairs-en.json", lambda route: route.fulfill(
        status=200, content_type="application/json", body=json.dumps(data)))
    p.goto(f"{site}/side-by-side/", wait_until="networkidle")
    p.wait_for_function(READY)
    fill(p, pair="two-ways")
    p.check('input[name="sb-level"][value="harder"]')
    assert "Difficulty: Harder to see." in prompt(p)
    p.select_option("#sb-pair", "one-change")
    assert p.is_disabled('input[name="sb-level"][value="harder"]')
    assert "Difficulty: Easier to see." in prompt(p)
    assert p.text_content("#sb-level-note").strip()
    p.select_option("#sb-pair", "two-ways")
    assert p.is_enabled('input[name="sb-level"][value="harder"]')
    p.close()


def test_builder_fetch_failure(site, browser):
    p = browser.new_page()
    p.route("**/pairs-en.json", lambda route: route.fulfill(status=500, body=""))
    p.goto(f"{site}/side-by-side/", wait_until="networkidle")
    p.wait_for_function("document.getElementById('sb-hint').textContent.includes('reload')")
    assert p.text_content("#sb-hint").strip() == "Couldn't load the pair types — reload the page."
    assert p.locator("article.sb-pair").count() == 5
    assert p.is_disabled("#sb-copy")
    p.close()


def test_hint_is_shown_beside_disabled_copy_button(site, browser):
    for width in (1280, 390):
        p = browser.new_page(viewport={"width": width, "height": 800})
        p.goto(f"{site}/side-by-side/", wait_until="networkidle")
        p.wait_for_function(READY)
        assert p.is_disabled("#sb-copy")
        assert p.locator(".tm-copy-row #sb-hint").is_visible(), width
        btn = p.locator("#sb-copy").bounding_box()
        hint = p.locator("#sb-hint").bounding_box()
        assert hint["y"] < btn["y"] + btn["height"] + 40, (width, btn, hint)
        p.close()


def test_variant_copy_matches_student_prompt(site, browser):
    data = json.loads(DATA.read_text(encoding="utf-8"))
    ctx = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
    p = ctx.new_page()
    p.goto(f"{site}/side-by-side/", wait_until="networkidle")
    assert p.get_attribute("#sb-variant-copy", "data-copy") == data["variant"]["student_prompt"]
    p.click("#sb-variant-copy")
    assert p.evaluate("navigator.clipboard.readText()") == data["variant"]["student_prompt"]
    ctx.close()


def test_pair_cards_side_by_side_are_equal_height(site, browser):
    # Kort som står bredvid varandra i samma rad ska vara lika höga.
    for width in (1280, 900):
        p = browser.new_page(viewport={"width": width, "height": 900})
        p.goto(f"{site}/side-by-side/", wait_until="networkidle")
        rows = {}
        for box in (c.bounding_box() for c in p.locator("article.sb-pair").all()):
            rows.setdefault(round(box["y"]), []).append(box["height"])
        assert any(len(h) > 1 for h in rows.values()), width
        for heights in rows.values():
            assert max(heights) - min(heights) < 1, (width, heights)
        p.close()


def test_rules_ask_for_a_new_case_c(page):
    # ChatGPT-testet 2: fall C var samma par med nya namn, så regeln prövades aldrig.
    fill(page)
    assert "Case C is a new situation, not the same pair with new names." in prompt(page)
