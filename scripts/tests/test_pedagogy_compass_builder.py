"""Promptbyggaren i Pedagogy Compass i en riktig webbläsare.

Prompttexten är fastställd i planen och bor i assets/js/pedagogy-compass.js.
Ändra den bara tillsammans med affischens baksida
(exports/build-pedagogy-compass-pdf.py).
"""
import functools
import http.server
import json
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
URL = "/pedagogy-compass-59ecb8db/"
DATA = json.loads((ROOT / "pedagogy-compass-59ecb8db/compass-en.json").read_text(encoding="utf-8"))
MODELS = {m["id"]: m for m in DATA["models"]}
FIRST = DATA["problems"][0]

FORMAT = """Reply in plain text, no tables, in exactly this format:
BEST FIRST STEP: which approach to try first and why, given what the teacher sees
NEXT LESSON: what it looks like in one concrete lesson in this subject, with minutes
WATCH FOR: how the teacher will know within two weeks whether it is working
AI: one way AI could help the teacher with this, and one way students' use of AI could make the problem worse
HONEST NOTE: what the evidence label means for this approach, in one or two lines"""


def approaches(ids):
    return "\n".join(
        f'- {MODELS[i]["name"]} ({DATA["labels"][MODELS[i]["category"]]["name"]}): {MODELS[i]["one_liner"]}' for i in ids)


def expected(problem, situation, block):
    return f"""Do not include student names or student results in this conversation.

You are helping a Grade 8 Science teacher with a problem in class: {problem}
What the teacher sees: {situation}

{block}

""" + FORMAT


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


def open_page(site, browser, query=""):
    p = browser.new_page()
    p.goto(f"{site}{URL}{query}", wait_until="networkidle")
    p.wait_for_function("window.PedagogyCompass !== undefined", timeout=5000)
    return p


@pytest.fixture
def page(site, browser):
    p = open_page(site, browser)
    yield p
    p.close()


def test_prompt_is_exact(page):
    page.fill("#pc-subject", "Science")
    page.fill("#pc-situation", "Most of the class.")
    block = "The teacher is looking at these approaches, strongest evidence first:\n" + approaches(FIRST["model_ids"])
    assert page.input_value("#pc-prompt") == expected(FIRST["name"], "Most of the class.", block)
    assert page.inner_text("#pc-hint") == "Your prompt is ready."
    assert page.get_attribute("#pc-copy", "data-copy") == page.input_value("#pc-prompt")


def test_empty_situation_fallback(page):
    page.fill("#pc-subject", "Science")
    assert "What the teacher sees: Nothing more described." in page.input_value("#pc-prompt")


def test_checkboxes_follow_the_problem(page):
    p2 = DATA["problems"][2]
    page.select_option("#pc-problem", p2["id"])
    boxes = page.locator("#pc-models input[type=checkbox]")
    assert boxes.count() == len(p2["model_ids"])
    assert all(boxes.nth(i).is_checked() for i in range(boxes.count()))


def test_unticking_removes_an_approach(page):
    page.fill("#pc-subject", "Science")
    first = MODELS[FIRST["model_ids"][0]]["name"]
    page.locator("#pc-models li").filter(has_text=first).locator("input").uncheck()
    assert f"- {first} (" not in page.input_value("#pc-prompt")


def test_no_models_ticked_asks_ai_to_suggest(page):
    page.fill("#pc-subject", "Science")
    boxes = page.locator("#pc-models input[type=checkbox]")
    for i in range(boxes.count()):
        boxes.nth(i).uncheck()
    text = page.input_value("#pc-prompt")
    assert ("The teacher has not chosen any approaches yet. Suggest two or three research-based approaches "
            "that fit this problem, strongest evidence first, and give each one of these labels: Strong (meta-analyses "
            "of classroom studies), Promising (controlled studies, but mixed or dependent on context) or Framework "
            "(useful for planning, not tested as a method).") in text
    assert "strongest evidence first:\n-" not in text


def test_own_problem(page):
    page.select_option("#pc-problem", "own")
    assert page.is_visible("#pc-own")
    page.fill("#pc-subject", "Science")
    assert page.input_value("#pc-prompt") == ""
    page.fill("#pc-own", "They rush through tasks.")
    text = page.input_value("#pc-prompt")
    assert "with a problem in class: They rush through tasks." in text
    assert "The teacher has not chosen any approaches yet." in text


def test_required_fields(page):
    assert page.is_disabled("#pc-copy")
    assert page.inner_text("#pc-hint") == "Choose a problem and fill in your subject to see your prompt."


def test_problem_preselect_from_query(site, browser):
    pid = DATA["problems"][4]["id"]
    p = open_page(site, browser, f"?problem={pid}")
    assert p.input_value("#pc-problem") == pid
    p.close()
    for bad in ("nope", "constructor"):
        p = open_page(site, browser, f"?problem={bad}")
        assert p.input_value("#pc-problem") == FIRST["id"], bad
        p.close()


def test_use_in_the_prompt_link(page):
    pid = DATA["problems"][6]["id"]
    page.click(f'[data-use-problem="{pid}"]')
    assert page.input_value("#pc-problem") == pid


def test_long_situation_stays_intact(page):
    page.fill("#pc-subject", "Science")
    long = ("Line with\ttab and • bullet. " * 130)[:3990]
    page.fill("#pc-situation", long)
    assert long.strip() in page.input_value("#pc-prompt")


def test_user_text_is_never_html(page):
    page.fill("#pc-subject", '<img src=x onerror="window.pwned=1">')
    assert '<img src=x onerror="window.pwned=1">' in page.input_value("#pc-prompt")
    assert page.evaluate("window.pwned === undefined")
