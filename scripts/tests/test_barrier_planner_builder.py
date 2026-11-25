"""De två promptbyggarna på /barrier-planner-1c25533d/ i en riktig webbläsare.

Prompterna byggs helt i webbläsaren av assets/js/barrier-planner.js, med
korten från #bp-data. Inget sparas och inget skickas.
Spec: docs/superpowers/specs/2026-11-25-barrier-planner-design.md
(avsnitt B5 och B6: mallarna där gäller ord för ord).
"""
import functools
import http.server
import importlib.util
import json
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SLUG = "barrier-planner-1c25533d"
SCRIPT = ROOT / "assets" / "js" / "barrier-planner.js"
DATA = json.loads((ROOT / SLUG / "planner-en.json").read_text(encoding="utf-8"))

_spec = importlib.util.spec_from_file_location("bbp", ROOT / "scripts/build-barrier-planner.py")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
PRIVACY_COPY = _mod.PRIVACY_COPY

PLAN_HINT = "Fill in subject, the task and the barrier to see your prompt."
ADAPT_HINT = "Fill in subject and paste the text to see your prompt."
TASK = "Carry out the experiment on page 42 and record your results in the table."
FIVE = ("Start from these five strategies for the whole class and fit them to this task: "
        "flexible grouping, cognitive and metacognitive strategies, explicit instruction, "
        "technology, and scaffolding.")
HTML_TEXT = '<b>x</b> </script> "q" & r'
ADAPT_BARRIERS = {
    "reading-load": "Some students find it hard: reading a long text takes all their energy.",
    "language": "Some students find it hard: still learning the language of instruction.",
}


def card_of(card_id):
    return next(c for c in DATA["cards"] if c["id"] == card_id)


def expected_plan(i, card=None):
    """Mallen ur spec B5, ifylld. i = indata som byggaren får (redan trimmad)."""
    language = i["language"].strip()
    english = language == "" or language.lower() == "english"
    goal = i["goal"].strip()
    seen = i["seen"].strip()
    lines = [
        PRIVACY_COPY,
        "",
        f"You are helping a Grade {i['grade']} {i['subject']} teacher plan support for a barrier that some students in the class meet in one task. Plan for the task and the barrier, not for any one student. Do not ask about students, and do not ask for or use any diagnosis.",
        "",
        "The task as students get it:",
        i["task"],
        "",
        f"The learning goal, the same for every student: {goal}" if goal
        else "The learning goal: the goal of the task as it is, the same for every student.",
        f"The barrier: {card['barrier'] if card else i['other']}",
    ]
    if seen:
        lines.append(f"What the teacher sees: {seen}")
    lines.append("")
    if card:
        lines += [
            "Start from these moves and fit them to this task:",
            "For the whole class: " + "; ".join(m["short"] for m in card["whole_class"]),
            "Targeted: " + "; ".join(m["short"] for m in card["targeted"]),
        ]
    else:
        lines.append(FIVE)
    lines += [
        "",
        "Rules:",
        "- Keep the task and the learning goal the same for everyone. Change the route to the goal, not the goal.",
        "- Do not suggest colored overlays, dyslexia fonts, fidget spinners, extra time in lessons, a separate easier worksheet, or less work as the default.",
        "- Every support can be taken away later.",
        "- If a move needs something the teacher must prepare, say what in one line.",
        "",
        "Write everything in English." if english
        else f"Write everything in {language}, but keep the headings in English.",
        "",
        "Reply in plain text, no tables, in under 300 words, with exactly these parts:",
        "FOR THE WHOLE CLASS: two or three moves written for this task: what you do and what students see.",
        "TARGETED: one or two supports for the students who still meet the barrier, and how you will notice during the lesson who they are.",
        "TAKE IT AWAY: which support goes first, and what tells you it is time.",
        f"REVIEW: one question to answer in {i['review']}, and what you will look for then.",
    ]
    return "\n".join(lines)


def expected_adapt(i):
    """Mallen ur spec B6, ifylld."""
    barrier = i["barrier"]
    barrier_line = (" Some students find it hard: " + barrier[:1].lower() + barrier[1:] + ".") if barrier else ""
    return "\n".join([
        PRIVACY_COPY,
        "",
        f"Here is a text I use with Grade {i['grade']} students in {i['subject']}.{barrier_line}",
        "",
        "TEXT:",
        i["text"],
        "",
        "Keep every original sentence. Do not simplify the text or remove anything.",
        "",
        "Reply in plain text, in the language of the text, with the headings in English and exactly these parts:",
        "ADAPTED TEXT: the whole text in short sections, each with one guiding question. After hard words and phrases, add a short explanation or example in brackets.",
        f"GLOSSARY: the {i['words']} key words, each with a plain definition and an example sentence.",
        "PICTURE: one picture or diagram that shows the main idea: what it shows and where it goes.",
        "TAKE IT AWAY: which addition to remove first as students manage without it, and which last.",
    ])


PLAN_DEFAULT = dict(subject="Science", grade="6", task=TASK, barrier="multi-step",
                    other="", seen="stops after the first step and waits",
                    goal="Record results from a fair test", review="three weeks",
                    language="English")
ADAPT_TEXT = "The Roman Republic fell slowly. Rival generals used their armies for power. Augustus ended the argument."
ADAPT_DEFAULT = dict(subject="History", grade="10", barrier="", words="8", text=ADAPT_TEXT)


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
    p.errors = []
    p.on("console", lambda m: m.type == "error" and p.errors.append(f"{m.text} {m.location.get('url', '')}"))
    p.on("pageerror", lambda e: p.errors.append(str(e)))
    p.goto(f"{site}/{SLUG}/", wait_until="networkidle")
    # Kort tidsgräns: saknas skriptet ska testet falla direkt.
    p.wait_for_function("window.BarrierPlanner && typeof window.BarrierPlanner.buildPlanPrompt === 'function'",
                        timeout=3000)
    yield p
    p.close()


def fill_plan(page, **kw):
    v = {**PLAN_DEFAULT, **kw}
    page.fill("#bp-subject", v["subject"])
    page.select_option("#bp-grade", v["grade"])
    page.fill("#bp-task", v["task"])
    page.select_option("#bp-barrier", v["barrier"])
    if v["barrier"] == "other":
        page.fill("#bp-barrier-other", v["other"])
    page.fill("#bp-seen", v["seen"])
    page.fill("#bp-goal", v["goal"])
    page.select_option("#bp-review", v["review"])
    page.fill("#bp-language", v["language"])
    return v


def fill_adapt(page, **kw):
    v = {**ADAPT_DEFAULT, **kw}
    page.fill("#bp-a-subject", v["subject"])
    page.select_option("#bp-a-grade", v["grade"])
    page.select_option("#bp-a-barrier", v["barrier"])
    page.select_option("#bp-a-words", v["words"])
    page.fill("#bp-a-text", v["text"])
    return v


def plan(page):
    return page.input_value("#bp-prompt")


def adapt(page):
    return page.input_value("#bp-a-prompt")


def test_script_exists():
    assert SCRIPT.is_file(), "assets/js/barrier-planner.js saknas"


def test_default_plan(page):
    v = fill_plan(page)
    out = plan(page)
    assert out == expected_plan(v, card_of("multi-step"))
    assert out.startswith(PRIVACY_COPY + "\n\n")
    assert "do not ask for or use any diagnosis" in out
    assert page.get_attribute("#bp-copy", "data-copy") == out
    assert not page.is_disabled("#bp-copy")
    assert page.text_content("#bp-hint").strip() == ""


def test_goal_empty(page):
    fill_plan(page, goal="")
    assert "The learning goal: the goal of the task as it is, the same for every student.\n" in plan(page)
    assert "The learning goal, the same" not in plan(page)


def test_seen_empty(page):
    v = fill_plan(page, seen="")
    assert "What the teacher sees:" not in plan(page)
    assert plan(page) == expected_plan(v, card_of("multi-step"))


def test_something_else(page):
    other = "copies the board slowly and misses the start of the task"
    v = fill_plan(page, barrier="other", other=other)
    out = plan(page)
    assert f"The barrier: {other}\n" in out
    assert FIVE in out
    assert "Targeted:" not in out
    assert out == expected_plan(v)


def test_switch_other_and_back(page):
    page.select_option("#bp-barrier", "other")
    assert page.is_visible("#bp-barrier-other")
    assert page.eval_on_selector("#bp-barrier-other", "e => e.required")
    page.fill("#bp-barrier-other", "needs the board read out")
    v = fill_plan(page, barrier="attention")
    assert not page.is_visible("#bp-barrier-other")
    assert not page.eval_on_selector("#bp-barrier-other", "e => e.required")
    assert plan(page) == expected_plan({**v, "barrier": "attention"}, card_of("attention"))
    page.select_option("#bp-barrier", "other")
    assert page.input_value("#bp-barrier-other") == "needs the board read out"
    assert "The barrier: needs the board read out\n" in plan(page)


@pytest.mark.parametrize("lang,line", [
    ("Swedish", "Write everything in Swedish, but keep the headings in English."),
    (" english ", "Write everything in English."),
    ("ENGLISH", "Write everything in English."),
    ("", "Write everything in English."),
])
def test_language(page, lang, line):
    fill_plan(page, language=lang)
    out = plan(page)
    assert f"\n{line}\n" in out
    if line == "Write everything in English.":
        assert "keep the headings" not in out


def test_review_two_weeks(page):
    fill_plan(page, review="two weeks")
    assert "REVIEW: one question to answer in two weeks, and what you will look for then." in plan(page)


def test_read_the_card_link(page):
    for c in DATA["cards"]:
        page.select_option("#bp-barrier", c["id"])
        assert page.get_attribute("#bp-card-link", "href") == f"#bp-barrier-{c['id']}"
        assert page.is_visible("#bp-card-link")
        assert page.query_selector(f"#bp-barrier-{c['id']}")
    for hidden in ("", "other"):
        page.select_option("#bp-barrier", hidden)
        assert not page.is_visible("#bp-card-link")


@pytest.mark.parametrize("blank", ["subject", "task", "barrier", "other"])
def test_plan_empty_state(page, blank):
    fill_plan(page, barrier="other" if blank == "other" else "multi-step", other="x")
    assert plan(page) != ""
    if blank == "barrier":
        page.select_option("#bp-barrier", "")
    elif blank == "other":
        page.fill("#bp-barrier-other", "")
    else:
        page.fill(f"#bp-{blank}", "")
    assert plan(page) == ""
    assert page.is_disabled("#bp-copy")
    assert page.get_attribute("#bp-copy", "data-copy") == ""
    assert page.text_content("#bp-hint").strip() == PLAN_HINT


def test_whitespace_counts_as_empty(page):
    fill_plan(page, subject="   ")
    assert plan(page) == ""
    fill_plan(page, task="\n \n")
    assert plan(page) == ""
    fill_plan(page, barrier="other", other="  ")
    assert plan(page) == "" and page.is_disabled("#bp-copy")
    fill_adapt(page, text="\n")
    assert adapt(page) == "" and page.is_disabled("#bp-a-copy")
    assert page.text_content("#bp-a-hint").strip() == ADAPT_HINT


def test_default_adapt(page):
    v = fill_adapt(page)
    out = adapt(page)
    assert out == expected_adapt(v)
    assert "Some students find it hard" not in out
    assert "GLOSSARY: the 8 key words" in out
    assert page.get_attribute("#bp-a-copy", "data-copy") == out
    assert not page.is_disabled("#bp-a-copy")
    assert page.text_content("#bp-a-hint").strip() == ""


@pytest.mark.parametrize("value", ["reading-load", "language"])
def test_adapt_barrier_line(page, value):
    label = page.eval_on_selector(f'#bp-a-barrier option[value="{value}"]', "o => o.textContent.trim()")
    v = fill_adapt(page, barrier=value, words="5")
    out = adapt(page)
    assert ADAPT_BARRIERS[value] in out
    assert "the 5 key words" in out
    assert out == expected_adapt({**v, "barrier": label})


def test_adapt_empty_state(page):
    assert adapt(page) == ""
    assert page.is_disabled("#bp-a-copy")
    assert page.text_content("#bp-a-hint").strip() == ADAPT_HINT
    fill_adapt(page)
    page.fill("#bp-a-subject", "")
    assert adapt(page) == ""
    assert page.text_content("#bp-a-hint").strip() == ADAPT_HINT


def test_html_is_literal(page):
    fill_plan(page, task=HTML_TEXT)
    fill_adapt(page, text=HTML_TEXT)
    for field, copy in (("#bp-prompt", "#bp-copy"), ("#bp-a-prompt", "#bp-a-copy")):
        assert HTML_TEXT in page.input_value(field)
        assert HTML_TEXT in page.get_attribute(copy, "data-copy")
    assert page.query_selector("#bp-plan-form b, #bp-adapt-form b, #bp-prompt b, #bp-a-prompt b") is None


def test_no_console_errors(page):
    fill_plan(page)
    fill_adapt(page)
    assert page.errors == []
