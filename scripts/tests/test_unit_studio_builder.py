"""Promptbyggaren i Unit Studio i en riktig webbläsare.

Prompttexten är fastställd i planen och bor i assets/js/unit-studio.js.
Ändra den bara tillsammans med metodkortets luckprompt
(exports/build-unit-studio-pdf.py).
"""
import functools
import http.server
import json
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
URL = "/unit-studio-541ebd12/"
STEP3 = json.loads((ROOT / "unit-studio-541ebd12/studio-en.json").read_text(encoding="utf-8"))["steps"][2]
UNIT = "Week 1: Forces.\nWeek 2: Weight and mass."

STEP_FORMAT = """Reply in plain text, no tables, in exactly this format:
KEEP: what already works for this step, in one or two lines. For a new unit, what in the topic and goals is already clear.
SUGGEST: at most three changes or additions for this step, numbered, each tied to this unit's content, each with one line on why it helps students learn.
QUESTION: one question back to the teacher before the next step.
AI CAN ALSO: one other way an AI tool could help with this step, written as a short prompt the teacher can copy."""

EXPECTED_STEP3 = f"""Do not include student names or student results in this conversation.

You are helping a Grade 8 Science teacher improve a unit of 4 weeks with 3 lessons a week. We work through five steps, one at a time. This is step 3 of 5: Sequence and load.

The unit as the teacher has planned it:
{UNIT}

Decisions so far: None yet. If earlier steps are in this conversation, build on what the teacher decided there.

{STEP3["brief"]}

""" + STEP_FORMAT

EXPECTED_FINAL = f"""Do not include student names or student results in this conversation.

You are helping a Grade 8 Science teacher write the improved plan for a unit of 4 weeks with 3 lessons a week. Use the unit and the decisions below. Where the teacher has not decided something, choose what the research behind the five steps supports, and say so.

The unit as the teacher has planned it:
{UNIT}

Decisions from the five steps: Keep the practicals.

Reply in plain text, no tables, in exactly this format:
GOAL AND EVIDENCE: what students should be able to do by the end, and how the teacher will see it
PRIOR KNOWLEDGE: what students need first, and how to check it in the first lesson
LESSONS: one line per lesson, numbered, with what students do and roughly how long
RETRIEVAL: which earlier content returns in which lessons
CHECKPOINTS: where in the unit to check understanding, how, and what to do if fewer than about 4 in 5 get it
AI USE: where students use AI in this unit, where they do not, and why
CHANGES: what is different from the original plan, one line each, or "New unit"
CHECK: anything the teacher should verify before teaching, one per line, or "None\""""


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
    p.wait_for_function("window.UnitStudio !== undefined", timeout=5000)
    return p


@pytest.fixture
def page(site, browser):
    p = open_page(site, browser)
    yield p
    p.close()


def fill(page, subject="Science", unit=UNIT, step="3", decisions=""):
    page.fill("#us-subject", subject)
    page.fill("#us-unit", unit)
    page.select_option("#us-step", step)
    page.fill("#us-decisions", decisions)


def test_step_prompt_is_exact(page):
    fill(page)
    assert page.input_value("#us-prompt") == EXPECTED_STEP3
    assert page.inner_text("#us-hint") == "Your prompt is ready."


def test_new_unit_wording_and_label(page):
    page.check("#us-mode-new")
    fill(page, unit="Forces and motion. Goals: explain balanced forces.")
    text = page.input_value("#us-prompt")
    assert "The teacher is planning a new unit. Topic and goals:\nForces and motion." in text
    assert page.inner_text("#us-unit-label") == "The topic and goals of the new unit"


def test_final_prompt_is_exact(page):
    fill(page, step="final", decisions="Keep the practicals.")
    assert page.input_value("#us-prompt") == EXPECTED_FINAL


def test_final_prompt_decisions_fallback(page):
    fill(page, step="final")
    assert "Decisions from the five steps: See the earlier steps in this conversation. If there are none, plan from the unit as written." in page.input_value("#us-prompt")


def test_required_fields(page):
    for field in ("#us-subject", "#us-unit"):
        fill(page)
        page.fill(field, "  ")
        assert page.input_value("#us-prompt") == "", field
        assert page.is_disabled("#us-copy")
        assert page.inner_text("#us-hint") == "Fill in subject and your unit to see your prompt."


def test_copy_button_matches_prompt(page):
    fill(page)
    assert page.get_attribute("#us-copy", "data-copy") == page.input_value("#us-prompt")


def test_step_preselect_from_query(site, browser):
    p = open_page(site, browser, "?step=4")
    assert p.input_value("#us-step") == "4"
    p.close()
    p = open_page(site, browser, "?step=final")
    assert p.input_value("#us-step") == "final"
    p.close()
    for bad in ("9", "constructor", "x"):
        p = open_page(site, browser, f"?step={bad}")
        assert p.input_value("#us-step") == "1", bad
        p.close()


def test_use_this_step_link_selects_step(page):
    fill(page, step="1")
    page.click('[data-use-step="5"]')
    assert page.input_value("#us-step") == "5"
    assert "This is step 5 of 5: Motivation and AI decisions." in page.input_value("#us-prompt")


def test_mode_switch_keeps_the_text(page):
    fill(page)
    page.check("#us-mode-new")
    assert page.input_value("#us-unit") == UNIT
    page.check("#us-mode-improve")
    assert page.input_value("#us-unit") == UNIT
    assert page.inner_text("#us-unit-label") == "The unit as you have planned it"


def test_long_pasted_unit_stays_intact(page):
    long_unit = "\n".join(f"Week {i}\tLesson {j}\t• Topic text here" for i in range(1, 11) for j in range(1, 7)) * 6
    assert len(long_unit) > 12000
    fill(page, unit=long_unit)
    assert long_unit in page.input_value("#us-prompt")


def test_user_text_is_never_html(page):
    fill(page, unit='<img src=x onerror="window.pwned=1">')
    assert '<img src=x onerror="window.pwned=1">' in page.input_value("#us-prompt")
    assert page.evaluate("window.pwned === undefined")


def test_new_unit_mode_says_plan_not_improve(page):
    # Slutgranskningen: en ny enhet ska planeras, inte förbättras.
    page.check("#us-mode-new")
    fill(page, unit="Ratio. Goals: simplify ratios.")
    step = page.input_value("#us-prompt")
    assert "teacher plan a unit of 4 weeks" in step and "improve" not in step.split("\n")[2]
    page.select_option("#us-step", "final")
    final = page.input_value("#us-prompt")
    assert "teacher write the plan for a unit of 4 weeks" in final and "improved plan" not in final


def test_warns_at_the_length_limit(page):
    fill(page, unit="x" * 40000)
    assert "40,000-character limit" in page.inner_text("#us-hint")
