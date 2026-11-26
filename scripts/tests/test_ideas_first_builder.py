"""Promptbyggaren på /ideas-first-778ba230/ i en riktig webbläsare.

Prompten byggs helt i webbläsaren av assets/js/ideas-first.js. Inget sparas
och inget skickas. Spec: docs/superpowers/specs/2026-11-26-ideas-first-design.md
(avsnitt B4: mallen och varianterna där gäller ord för ord).
"""
import functools
import http.server
import importlib.util
import re
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SLUG = "ideas-first-778ba230"
SCRIPT = ROOT / "assets" / "js" / "ideas-first.js"

_spec = importlib.util.spec_from_file_location("bif", ROOT / "scripts/build-ideas-first.py")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
PRIVACY_COPY = _mod.PRIVACY_COPY

HINT = "Write the subject, the goal and at least one idea of your own to see your prompt."
HTML_TEXT = '$& $1 <b>x</b> </script> "q" & r'
DEFAULT = dict(
    who="me", subject="Geography", grade="8",
    goal="explain why towns grew up beside rivers",
    own="a map of local rivers and towns\na short text with questions",
    fit="", language="English",
)


def idea_lines(own):
    out = []
    for line in re.split(r"\r?\n", own):
        line = re.sub(r"^(?:[-•*]|\d+[.)])\s*", "", line.strip())
        if line:
            out.append(line)
    return out


def expected_prompt(i):
    """Mallen ur spec B4, ifylld. i = indata som byggaren får."""
    team = i["who"] == "team"
    subject, goal = i["subject"].strip(), i["goal"].strip()
    fit, language = i["fit"].strip(), i["language"].strip()
    english = language == "" or language.lower() == "english"
    lines = [
        PRIVACY_COPY,
        "",
        (f"We are a team of teachers who teach {subject} to Grade {i['grade']}." if team
         else f"I teach {subject} to Grade {i['grade']}.")
        + f" The goal of the lesson is: {goal}",
    ]
    if fit:
        lines.append(f"The ideas must fit this: {fit}")
    lines += [
        "",
        "Our ideas so far:" if team else "My own ideas so far:",
    ]
    lines += ["- " + x for x in idea_lines(i["own"])]
    lines += [
        "",
        ("Give us eight ideas for an activity that reaches this goal, each clearly different from the others and from all of ours: vary the format (written, spoken, hands-on, visual), the context and the level of challenge."
         if team else
         "Give me eight ideas for an activity that reaches this goal, each clearly different from the others and from mine: vary the format (written, spoken, hands-on, visual), the context and the level of challenge."),
        "",
        "Write everything in English." if english else f"Write everything in {language}.",
        "",
        "Reply in plain text, no tables, as a numbered list of eight ideas, one or two sentences each. Start each idea with its format in parentheses, for example (hands-on). "
        + ("Do not rank them or choose one for us." if team else "Do not rank them or choose one for me."),
    ]
    return "\n".join(lines)


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
    p.wait_for_function("window.IdeasFirst && typeof window.IdeasFirst.buildIdeasPrompt === 'function'",
                        timeout=3000)
    yield p
    p.close()


def fill(page, **kw):
    v = {**DEFAULT, **kw}
    page.select_option("#if-who", v["who"])
    page.fill("#if-subject", v["subject"])
    page.select_option("#if-grade", v["grade"])
    page.fill("#if-goal", v["goal"])
    page.fill("#if-own", v["own"])
    page.fill("#if-fit", v["fit"])
    page.fill("#if-language", v["language"])
    return v


def prompt(page):
    return page.input_value("#if-prompt")


def test_script_exists():
    assert SCRIPT.is_file()


def test_default_me(page):
    v = fill(page)
    out = prompt(page)
    assert out == expected_prompt(v)
    assert page.get_attribute("#if-copy", "data-copy") == out
    assert out.startswith("Do not include student names or student work in this conversation.\n\n")
    assert "Do not rank them or choose one for me." in out
    assert not page.is_disabled("#if-copy")
    assert not page.is_visible("#if-hint")
    assert not out.endswith("\n")


def test_team(page):
    v = fill(page, who="team")
    out = prompt(page)
    assert out == expected_prompt(v)
    for s in ("We are a team of teachers who teach Geography to Grade 8.", "Our ideas so far:",
              "Give us eight ideas", "from all of ours", "choose one for us."):
        assert s in out
    assert page.text_content("#if-own-label").strip() == "Your team's ideas"
    assert page.text_content("#if-own-note").strip() == "Everyone's ideas, one per line."


def test_fit_line(page):
    v = fill(page, fit="20 minutes, no computers")
    out = prompt(page)
    assert out == expected_prompt(v)
    lines = out.split("\n")
    i = next(n for n, l in enumerate(lines) if "The goal of the lesson is:" in l)
    assert lines[i + 1] == "The ideas must fit this: 20 minutes, no computers"
    fill(page, fit="")
    assert "The ideas must fit this" not in prompt(page)
    assert "\n\n\n" not in prompt(page)


@pytest.mark.parametrize("lang,line", [
    ("Swedish", "Write everything in Swedish."),
    (" english ", "Write everything in English."),
    ("ENGLISH", "Write everything in English."),
    ("", "Write everything in English."),
])
def test_language(page, lang, line):
    fill(page, language=lang)
    assert line in prompt(page).split("\n")


def test_list_markers_stripped(page):
    v = fill(page, own="- one\n• two\n* three\n1. four\n2) five\n\n  six  ")
    out = prompt(page)
    assert out == expected_prompt(v)
    assert "- one\n- two\n- three\n- four\n- five\n- six\n" in out


def test_marker_only_lines_count_as_empty(page):
    fill(page, own="-\n1.\n  \n")
    assert prompt(page) == ""
    assert page.is_disabled("#if-copy")
    assert page.get_attribute("#if-copy", "data-copy") == ""
    assert page.text_content("#if-hint").strip() == HINT


@pytest.mark.parametrize("blank", ["subject", "goal", "own"])
def test_empty_state(page, blank):
    fill(page)
    assert prompt(page) != ""
    assert not page.is_visible("#if-hint")
    page.fill(f"#if-{blank}", "")
    assert prompt(page) == ""
    assert page.is_disabled("#if-copy")
    assert page.get_attribute("#if-copy", "data-copy") == ""
    assert page.is_visible("#if-hint")
    assert page.text_content("#if-hint").strip() == HINT


def test_whitespace_counts_as_empty(page):
    fill(page, subject="   ")
    assert prompt(page) == ""
    # Ett enradsfält tar inte emot "\n" via fill(); blanksteg och tabb gör samma nytta.
    fill(page, goal=" \t  ")
    assert prompt(page) == "" and page.is_disabled("#if-copy")


def test_switch_team_and_back(page):
    v = fill(page, own="one\ntwo")
    page.select_option("#if-who", "team")
    assert page.input_value("#if-own") == "one\ntwo"
    page.select_option("#if-who", "me")
    assert page.input_value("#if-own") == "one\ntwo"
    assert page.text_content("#if-own-label").strip() == "Your own ideas"
    assert page.text_content("#if-own-note").strip() == "Two or three is enough."
    assert prompt(page) == expected_prompt(v)


def test_dollar_and_html_are_literal(page):
    v = fill(page, goal=HTML_TEXT, own=HTML_TEXT)
    out = prompt(page)
    assert out == expected_prompt(v)
    assert f"The goal of the lesson is: {HTML_TEXT}" in out
    assert f"- {HTML_TEXT}" in out
    assert page.get_attribute("#if-copy", "data-copy") == out
    assert page.query_selector("#if-form b") is None


def test_crlf_lines(page):
    # fill() på en textarea normaliserar radbrytningar, så skriptet får värdet direkt.
    out = page.evaluate("""() => window.IdeasFirst.buildIdeasPrompt(
        {who: 'me', subject: 'S', grade: '8', goal: 'g', own: 'a\\r\\nb', fit: '', language: ''})""")
    assert "- a\n- b\n" in out
    assert "\r" not in out
    assert page.evaluate("() => window.IdeasFirst.ideaLines('a\\r\\nb')") == ["a", "b"]


def test_no_console_errors(page):
    fill(page)
    fill(page, who="team", own="-")
    assert page.errors == []
