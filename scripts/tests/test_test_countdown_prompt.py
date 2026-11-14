"""Lärarens quizprompt på /test-countdown/ i en riktig webbläsare.

buildPrompt i assets/js/test-countdown.js är en ren funktion: planen och tre
fält (ämne, årskurs, språk) in, en text ut. Texten är fastställd ordagrant i
specen, avsnittet "Quiz prompt (For teachers)", och de förväntade texterna här
är byggda av specens rader, aldrig av koden som testas. Därefter testas
kopplingen till sidan: knappen och ledtråden följer planen och ämnet, och
prompten byggs om när planen eller fälten ändras.
Spec: docs/superpowers/specs/2026-11-14-test-countdown-design.md.
"""
import functools
import http.server
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
ALL_DAYS = [1, 2, 3, 4, 5, 6, 7]
HINT_NOT_READY = "Make a plan above, then fill in your subject."


def state(test, start, areas, minutes=20, days=None):
    return {"test": test, "start": start, "areas": areas, "minutes": minutes,
            "days": ALL_DAYS if days is None else days}


# Fall A, C, D, E, H och L1 från test_test_countdown_plan.py (där finns planerna förklarade).
CELLS, PHOTO, FOOD = "Cells", "Photosynthesis", "Food chains"
CASE_A = state("2026-11-20", "2026-11-09", [CELLS, PHOTO, FOOD], 20, [1, 2, 3, 4, 5])
CASE_A_QUERY = "test=2026-11-20&start=2026-11-09&min=20&days=12345&area=A&area=B&area=C"
CASE_C = state("2026-11-20", "2026-11-19", ["A", "B"])
CASE_D = state("2026-11-20", "2026-11-18", ["A", "B"])
CASE_E = state("2026-11-20", "2026-11-16", ["A", "B", "C", "D", "E"])
CASE_H = state("2026-11-20", "2026-11-01", ["A"], 20, [6])
CASE_L1 = state("2027-01-04", "2026-12-28", [CELLS], 20, [1, 2, 3, 4, 5])

# Specens mall, rad för rad. Det som varierar med planen kommer in via spec_prompt.
INTRO = "Do not include student names or student work in this conversation."
STUDENTS = ("Students will prepare with short study sessions on different days. Each session starts with a quiz "
            "that students answer on paper with their notes closed, and then check against the answers.")
QUIZ_INTRO = "Write one quiz for each of these sessions:"
CLOSE_PRACTICE = "The last session works on the mistakes from the practice test, so it needs no quiz."
CLOSE_NO_PRACTICE = "The last session goes back over the first quiz, so it needs no quiz of its own."
BULLETS = [
    '- Ask about the most important content in each area: what the test is most likely to ask. If I paste my own '
    'teaching material or an old test after this prompt, base the questions on that material and make the practice '
    'test look like the old test.',
    '- Each question asks one thing. Most answers are a word, a number or a short phrase; add a few "explain why" '
    'questions.',
    '- When a session comes back to an earlier area, ask in a new way, not the same question again.',
    '- Do not give away one answer in another question.',
]
REPLY = ('Reply in plain text, no tables. For each session, write SESSION 1:, SESSION 2: and so on, with the '
         'questions numbered Q1:, Q2: and so on, ready to print. Then write ANSWERS, with the answers for each '
         'session numbered to match. End with CHECK: every fact, figure, date or name in the answers that I '
         'should verify, one per line.')


def spec_prompt(areas_sentence, session_lines, closing, grade="9", subject="Biology", language="English"):
    """Hela prompten ur specens mall. closing är None när planen saknar sista kväll."""
    lines = [INTRO, "",
             f"You are helping a Grade {grade} {subject} teacher. {areas_sentence} {STUDENTS}", "",
             f"Write everything in {language}.", "",
             QUIZ_INTRO] + session_lines
    if closing:
        lines.append(closing)
    return "\n".join(lines + [""] + BULLETS + ["", REPLY])


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
def context(site, browser):
    ctx = browser.new_context(timezone_id="Europe/Stockholm")
    # Kopieringsknappen skriver till urklipp; i tester måste det tillåtas.
    ctx.grant_permissions(["clipboard-read", "clipboard-write"], origin=site)
    yield ctx
    ctx.close()


def open_page(ctx, url):
    p = ctx.new_page()
    p.errors = []
    p.on("console", lambda m: m.type == "error" and p.errors.append(m.text))
    p.on("pageerror", lambda e: p.errors.append(str(e)))
    p.goto(url, wait_until="networkidle")
    p.wait_for_function("window.TestCountdown && typeof window.TestCountdown.buildPrompt === 'function'")
    return p


@pytest.fixture
def base(site):
    return f"{site}/test-countdown/"


@pytest.fixture
def page(context, base):
    p = open_page(context, base)
    yield p
    p.close()


def fill_plan(page, given):
    """Fyller i planeraren som en elev: ett fält i taget, så varje fält ger en egen händelse."""
    page.fill("#tc-test", given["test"])
    page.fill("#tc-start", given["start"])
    page.select_option("#tc-minutes", str(given["minutes"]))
    page.fill("#tc-areas", "\n".join(given["areas"]))
    for day in ALL_DAYS:
        page.set_checked(f'#tc-days input[value="{day}"]', day in given["days"])


def prompt_for(page, given, subject="Biology", grade="9", language="English"):
    """Planen ur buildPlan och prompten ur buildPrompt, båda som rena funktioner."""
    plan = page.evaluate("s => window.TestCountdown.buildPlan(s)", given)
    assert plan["ok"] is True, plan
    return page.evaluate("([p, o]) => window.TestCountdown.buildPrompt(p, o)",
                         [plan, {"subject": subject, "grade": grade, "language": language}])


def builder(page):
    return page.evaluate("""() => ({
        prompt: document.getElementById('tc-prompt').value,
        copy: document.getElementById('tc-copy').getAttribute('data-copy'),
        disabled: document.getElementById('tc-copy').disabled,
        hint: document.getElementById('tc-prompt-hint').textContent
      })""")


def test_prompt_case_a_exact(page):
    # Specens exempel, rad för rad: Biology, Grade 9, English, tre områden, fall A.
    expected = "\n".join([
        "Do not include student names or student work in this conversation.",
        "",
        "You are helping a Grade 9 Biology teacher. The class has a test on these areas: Cells; Photosynthesis; "
        "Food chains. Students will prepare with short study sessions on different days. Each session starts "
        "with a quiz that students answer on paper with their notes closed, and then check against the answers.",
        "",
        "Write everything in English.",
        "",
        "Write one quiz for each of these sessions:",
        "Session 1: five questions on Cells.",
        "Session 2: five questions on Photosynthesis, and three on Cells.",
        "Session 3: five questions on Food chains, and three on Cells and Photosynthesis.",
        "Session 4: eight questions mixing all areas.",
        "Session 5: a practice test of twelve questions on all areas, in the same format as the real test.",
        "The last session works on the mistakes from the practice test, so it needs no quiz.",
        "",
        "- Ask about the most important content in each area: what the test is most likely to ask. If I paste my "
        "own teaching material or an old test after this prompt, base the questions on that material and make the "
        "practice test look like the old test.",
        '- Each question asks one thing. Most answers are a word, a number or a short phrase; add a few '
        '"explain why" questions.',
        "- When a session comes back to an earlier area, ask in a new way, not the same question again.",
        "- Do not give away one answer in another question.",
        "",
        "Reply in plain text, no tables. For each session, write SESSION 1:, SESSION 2: and so on, with the "
        "questions numbered Q1:, Q2: and so on, ready to print. Then write ANSWERS, with the answers for each "
        "session numbered to match. End with CHECK: every fact, figure, date or name in the answers that I "
        "should verify, one per line.",
    ])
    assert prompt_for(page, CASE_A) == expected
    # Den hopsatta mallen i testet ger samma text, så de andra fallen kan jämföras mot den.
    assert expected == spec_prompt(
        "The class has a test on these areas: Cells; Photosynthesis; Food chains.",
        ["Session 1: five questions on Cells.",
         "Session 2: five questions on Photosynthesis, and three on Cells.",
         "Session 3: five questions on Food chains, and three on Cells and Photosynthesis.",
         "Session 4: eight questions mixing all areas.",
         "Session 5: a practice test of twelve questions on all areas, in the same format as the real test."],
        CLOSE_PRACTICE)


def test_prompt_single_area(page):
    # Fall L1 med ett enda område: egen mening om provet och egna formuleringar för blandat pass och övningsprov.
    got = prompt_for(page, CASE_L1)
    assert "The class has a test on Cells. Students will prepare" in got
    assert "these areas" not in got
    lines = got.split("\n")
    assert "Session 1: five questions on Cells." in lines
    assert "Session 2: eight new questions on Cells." in lines
    assert ("Session 3: a practice test of twelve questions on Cells, in the same format as the real test."
            in lines)
    assert got == spec_prompt(
        "The class has a test on Cells.",
        ["Session 1: five questions on Cells.",
         "Session 2: eight new questions on Cells.",
         "Session 3: a practice test of twelve questions on Cells, in the same format as the real test."],
        CLOSE_PRACTICE)


def test_prompt_short_plans(page):
    # Fall C: en enda studiedag. Ingen sista kväll, alltså ingen mening om sista passet.
    got = prompt_for(page, CASE_C)
    assert "Session 1: ten questions on the most important ideas in A and B." in got.split("\n")
    assert "last session" not in got
    assert got == spec_prompt(
        "The class has a test on these areas: A; B.",
        ["Session 1: ten questions on the most important ideas in A and B."], None)

    # Fall D: kärnquiz på båda områdena och sista kvällen utan övningsprov.
    got = prompt_for(page, CASE_D)
    assert "Session 1: five questions on the most important ideas in A and B." in got.split("\n")
    assert CLOSE_NO_PRACTICE in got.split("\n")
    assert "Session 2" not in got
    assert "practice test, so it needs no quiz" not in got
    assert got == spec_prompt(
        "The class has a test on these areas: A; B.",
        ["Session 1: five questions on the most important ideas in A and B."], CLOSE_NO_PRACTICE)

    # Fall H: ett enda område och två studiedagar. Kort plan med ett område.
    got = prompt_for(page, CASE_H)
    assert got == spec_prompt(
        "The class has a test on A.",
        ["Session 1: five questions on the most important ideas in A."], CLOSE_NO_PRACTICE)


def test_prompt_grouped(page):
    # Fall E: fem områden på två byggpass. Kort plan, så båda grupperna är "de viktigaste idéerna".
    got = prompt_for(page, CASE_E)
    lines = got.split("\n")
    assert "Session 1: five questions on the most important ideas in A, B and C." in lines
    assert "Session 2: five questions on the most important ideas in D and E, and three on A, B and C." in lines
    assert "Session 3: a practice test of twelve questions on all areas, in the same format as the real test." in lines
    assert "The class has a test on these areas: A; B; C; D; E." in got
    assert got == spec_prompt(
        "The class has a test on these areas: A; B; C; D; E.",
        ["Session 1: five questions on the most important ideas in A, B and C.",
         "Session 2: five questions on the most important ideas in D and E, and three on A, B and C.",
         "Session 3: a practice test of twelve questions on all areas, in the same format as the real test."],
        CLOSE_PRACTICE)


def test_language_default(page):
    # Tomt eller bara mellanslag i språkfältet ger engelska; språket trimmas.
    assert "\nWrite everything in English.\n" in prompt_for(page, CASE_A, language="  ")
    assert "\nWrite everything in English.\n" in prompt_for(page, CASE_A, language="")
    assert "\nWrite everything in Swedish.\n" in prompt_for(page, CASE_A, language="  Swedish ")
    # Ämnet trimmas, och årskursen står som den är.
    got = prompt_for(page, CASE_A, subject="  Biology  ", grade="11")
    assert "You are helping a Grade 11 Biology teacher. The class has" in got


def test_builder_states(context, base):
    page = open_page(context, base)
    # Ingen plan än: knappen är grå och ledtråden säger varför.
    assert builder(page) == {"prompt": "", "copy": "", "disabled": True, "hint": HINT_NOT_READY}

    # En plan men inget ämne: fortfarande inget.
    fill_plan(page, CASE_A)
    assert builder(page) == {"prompt": "", "copy": "", "disabled": True, "hint": HINT_NOT_READY}
    # Bara mellanslag är inget ämne.
    page.fill("#tc-subject", "   ")
    assert builder(page)["disabled"] is True

    # Ämnet kommer in ordagrant, som text: ingen <b> blir ett element.
    subject = 'Bio "<b>"&'
    page.fill("#tc-subject", subject)
    got = builder(page)
    assert got["disabled"] is False
    assert got["hint"] == ""
    assert f'You are helping a Grade 9 {subject} teacher.' in got["prompt"]
    assert got["copy"] == got["prompt"] == page.input_value("#tc-prompt")
    assert got["prompt"] == page.evaluate(
        "([p, o]) => window.TestCountdown.buildPrompt(p, o)",
        [page.evaluate("s => window.TestCountdown.buildPlan(s)", CASE_A),
         {"subject": subject, "grade": "9", "language": "English"}])
    assert page.locator("#tc-builder b").count() == 0
    assert page.is_enabled("#tc-copy")

    # Årskurs och språk följer med.
    page.select_option("#tc-grade", "11")
    page.fill("#tc-language", "Swedish")
    got = builder(page)["prompt"]
    assert f"You are helping a Grade 11 {subject} teacher." in got
    assert "\nWrite everything in Swedish.\n" in got
    page.fill("#tc-language", "  ")
    assert "\nWrite everything in English.\n" in builder(page)["prompt"]
    page.fill("#tc-language", "English")
    page.select_option("#tc-grade", "9")

    # Minuterna står inte i prompten, men planen byggs om och prompten förblir densamma.
    before = builder(page)
    page.select_option("#tc-minutes", "45")
    assert builder(page) == before

    # Områden och dagar ändrar planen, och prompten med den.
    page.fill("#tc-areas", "Cells")
    got = builder(page)
    assert "The class has a test on Cells. Students will prepare" in got["prompt"]
    assert got["copy"] == got["prompt"]
    page.fill("#tc-areas", "\n".join(CASE_A["areas"]))
    page.set_checked('#tc-days input[value="6"]', True)
    page.set_checked('#tc-days input[value="7"]', True)
    changed = builder(page)["prompt"]
    assert "Session 6:" in changed and "Session 7:" not in changed
    assert "Session 6:" not in before["prompt"]

    # En plan som blir ogiltig tar bort prompten igen.
    page.fill("#tc-areas", "")
    assert builder(page) == {"prompt": "", "copy": "", "disabled": True, "hint": HINT_NOT_READY}
    page.fill("#tc-areas", "Cells")
    assert builder(page)["disabled"] is False

    # Tömt ämne likaså.
    page.fill("#tc-subject", "")
    assert builder(page) == {"prompt": "", "copy": "", "disabled": True, "hint": HINT_NOT_READY}
    assert page.errors == []


def test_copy_button_copies_the_prompt(page):
    fill_plan(page, CASE_A)
    page.fill("#tc-subject", "Biology")
    page.click("#tc-copy")
    assert page.evaluate("navigator.clipboard.readText()") == page.input_value("#tc-prompt")
    assert page.evaluate("navigator.clipboard.readText()").startswith("Do not include student names")


def test_first_plan_event_is_not_missed(context, base):
    # Sidan öppnas på en länk med en färdig plan: planerarens första tc:plan skickas
    # redan vid laddningen, innan eleven rört något. Då räcker det att fylla i ämnet.
    page = open_page(context, base + "?" + CASE_A_QUERY)
    assert builder(page)["disabled"] is True
    page.fill("#tc-subject", "Biology")
    got = builder(page)
    assert got["disabled"] is False
    assert "Session 5: a practice test of twelve questions on all areas" in got["prompt"]
    assert page.errors == []


def test_plan_event_is_idempotent(page):
    # tc:plan kan komma två gånger per ändring (input och change): samma plan igen ska inte ändra något.
    fill_plan(page, CASE_A)
    page.fill("#tc-subject", "Biology")
    before = builder(page)
    page.evaluate("""() => {
        window.hintWrites = 0;
        new MutationObserver(records => { window.hintWrites += records.length; })
          .observe(document.getElementById('tc-prompt-hint'), { childList: true, characterData: true, subtree: true });
      }""")
    page.evaluate("""s => {
        const plan = window.TestCountdown.buildPlan(s);
        document.dispatchEvent(new CustomEvent('tc:plan', { detail: plan }));
        document.dispatchEvent(new CustomEvent('tc:plan', { detail: plan }));
      }""", CASE_A)
    assert builder(page) == before
    assert page.evaluate("window.hintWrites") == 0

    # Utan plan (detail null) blir knappen grå, och två gånger i rad ger samma läge.
    page.evaluate("""() => {
        document.dispatchEvent(new CustomEvent('tc:plan', { detail: null }));
        document.dispatchEvent(new CustomEvent('tc:plan', { detail: null }));
      }""")
    assert builder(page) == {"prompt": "", "copy": "", "disabled": True, "hint": HINT_NOT_READY}
    # Ledtråden skrevs en gång när den bytte text, inte en gång per händelse.
    assert page.evaluate("window.hintWrites") == 1
