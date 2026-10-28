"""Planeringsbyggaren på /thinking-profile/ i en riktig webbläsare.

Prompten byggs helt i webbläsaren av assets/js/thinking-profile.js från fyra
JSON-filer (stegar, tankeförflyttningar, felsorter, partyper). Inget sparas
och inget skickas.
"""
import functools
import http.server
import json
import re
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
LADDERS = json.loads((ROOT / "thinking-profile/ladders-en.json").read_text(encoding="utf-8"))
MOVES = json.loads((ROOT / "thinking-moves/moves-en.json").read_text(encoding="utf-8"))
READY = "document.getElementById('tp-hint').textContent.includes('Choose a thinking cluster')"
PARTS = ["THE THINKING THREAD:", "PLAN:", "WEEK:", "TASK:", "WHAT STUDENTS DO:",
         "ROOM FOR STEP:", "BUILDER INPUTS:", "LINK:", "TELL STUDENTS:", "CHECK:"]


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
    p.goto(f"{site}/thinking-profile/", wait_until="networkidle")
    p.wait_for_function(READY)
    yield p
    p.close()


def fill(page, cluster="causes", subject="Biology", grade="10", weeks="8",
         topic="Ecosystems", overview=""):
    page.select_option("#tp-cluster", cluster)
    page.fill("#tp-subject", subject)
    page.select_option("#tp-grade", grade)
    page.fill("#tp-weeks", weeks)
    page.fill("#tp-topic", topic)
    page.fill("#tp-overview", overview)


def prompt(page):
    return page.input_value("#tp-prompt")


def task_lines(text):
    return [l for l in text.splitlines() if l.startswith("- ")]


def test_prompt_contains_inputs_and_all_parts(page):
    fill(page)
    text = prompt(page)
    assert text.startswith("Do not include student names or student work in this conversation.")
    assert "Grade 10 Biology teacher" in text
    assert "8-week unit" in text
    assert "Unit topic: Ecosystems" in text
    ladder = next(l for l in LADDERS["ladders"] if l["cluster"] == "causes")
    for i, step in enumerate(ladder["steps"], 1):
        assert f"{i}. {step['text']}" in text
    lines = text.splitlines()
    for part in PARTS:
        assert any(l.startswith(part) for l in lines), part
    for rule in LADDERS["rules"]:
        assert rule in text


def test_preferred_and_others_partition_all_tasks(page):
    fill(page, cluster="evaluating")
    text = prompt(page)
    tasks = task_lines(text)
    assert len(tasks) == 14
    names = [m["name"] for m in MOVES["moves"]] + ["Flawed Answer", "Side by Side"]
    for name in names:
        assert sum(1 for t in tasks if t.startswith(f"- {name} (")) == 1, name
    other = text.index("Other tasks you may borrow")
    pref = [t for t in tasks if text.index(t) < other]
    assert [t.split(" (")[0][2:] for t in pref] == [
        "Pick and justify", "Check the claim", "Argue it", "Flawed Answer"]
    assert "https://choosewise.education/thinking-moves/?move=check-the-claim" in text
    assert "https://choosewise.education/flawed-answer/" in text
    assert "https://choosewise.education/side-by-side/" in text
    flawed = next(t for t in tasks if t.startswith("- Flawed Answer"))
    assert "Right answer, wrong reason" in flawed
    sbs = next(t for t in tasks if t.startswith("- Side by Side"))
    assert "Two sources on the same event" in sbs


def test_regulating_rule_only_for_regulating(page):
    rr = LADDERS["rules_regulating"]
    fill(page, cluster="regulating")
    rules_line = next(l for l in prompt(page).splitlines() if l.startswith("Rules: "))
    assert rules_line == "Rules: " + " ".join(rr) + " Do not invent studies or sources."
    for i in (0, 1, 4):
        assert LADDERS["rules"][i] not in rules_line, i
    for c in ("generating", "evaluating", "comparing", "explaining", "causes"):
        fill(page, cluster=c)
        text = prompt(page)
        for rule in LADDERS["rules"]:
            assert rule in text, (c, rule)
        assert rr[0] not in text, c
        assert LADDERS["regulating_rule"] not in text, c


def test_overview_line_omitted_when_empty(page):
    fill(page)
    assert "Unit outline" not in prompt(page)
    fill(page, overview="  Week 1: food chains  ")
    assert "Unit outline: Week 1: food chains" in prompt(page)


def test_long_overview_kept_verbatim(page):
    overview = ("Week 1: food chains.\nWeek 2: <b>loops</b> & \"cycles\". " + "x" * 1800)[:2000]
    fill(page, overview=overview)
    assert f"Unit outline: {overview}" in prompt(page)
    assert page.locator("main b").count() == 0


@pytest.mark.parametrize("weeks,expected", [
    ("1", 3), ("2", 3), ("3", 3), ("8", 8), ("9", 8), ("40", 8), ("", 6), ("-5", 3)])
def test_weeks_are_clamped(page, weeks, expected):
    fill(page, weeks=weeks)
    assert f"plan a {expected}-week unit" in prompt(page)


def test_builder_requires_cluster_subject_topic(page):
    hint = "Choose a thinking cluster, then fill in subject and topic."
    assert page.text_content("#tp-hint").strip() == hint
    fill(page, cluster="")
    assert prompt(page) == "" and page.is_disabled("#tp-copy")
    fill(page, subject="   ")
    assert prompt(page) == "" and page.is_disabled("#tp-copy")
    fill(page, topic="   ")
    assert prompt(page) == "" and page.is_disabled("#tp-copy")
    assert page.text_content("#tp-hint").strip() == hint
    fill(page)
    assert prompt(page) and page.is_enabled("#tp-copy")
    assert page.text_content("#tp-hint").strip() == ""


def test_copy_button_matches_prompt(page):
    fill(page)
    assert page.is_enabled("#tp-copy")
    assert page.get_attribute("#tp-copy", "data-copy") == prompt(page)
    fill(page, topic="")
    assert page.get_attribute("#tp-copy", "data-copy") == ""


def test_cluster_preselect_from_query(site, browser):
    p = browser.new_page()
    p.goto(f"{site}/thinking-profile/?cluster=comparing", wait_until="networkidle")
    p.wait_for_function(READY)
    assert p.input_value("#tp-cluster") == "comparing"
    p.close()


def test_unknown_cluster_param_is_ignored(site, browser):
    p = browser.new_page()
    errors = []
    p.on("pageerror", lambda e: errors.append(e))
    p.goto(f"{site}/thinking-profile/?cluster=<nope>", wait_until="networkidle")
    p.wait_for_function(READY)
    assert p.input_value("#tp-cluster") == ""
    assert not errors
    p.close()


def test_plan_with_this_ladder_link_selects_cluster(page):
    page.click('#explaining a[data-use-cluster="explaining"]')
    assert page.input_value("#tp-cluster") == "explaining"


@pytest.mark.parametrize("name", ["ladders-en.json", "moves-en.json", "flaws-en.json", "pairs-en.json"])
def test_builder_fetch_failure(site, browser, name):
    p = browser.new_page()
    p.route(f"**/{name}", lambda route: route.abort())
    p.goto(f"{site}/thinking-profile/", wait_until="load")
    p.wait_for_function("document.getElementById('tp-hint').textContent.includes('reload')")
    assert p.text_content("#tp-hint").strip() == "Couldn't load the ladders — reload the page."
    assert p.is_disabled("#tp-copy")
    p.close()


def test_hint_is_shown_beside_disabled_copy_button(site, browser):
    for width in (1280, 390):
        p = browser.new_page(viewport={"width": width, "height": 800})
        p.goto(f"{site}/thinking-profile/", wait_until="networkidle")
        p.wait_for_function(READY)
        assert p.is_disabled("#tp-copy")
        assert p.locator(".tm-copy-row #tp-hint").is_visible(), width
        btn = p.locator("#tp-copy").bounding_box()
        hint = p.locator("#tp-hint").bounding_box()
        assert hint["y"] < btn["y"] + btn["height"] + 40, (width, btn, hint)
        p.close()
