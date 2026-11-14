"""Planreglerna på /test-countdown/ i en riktig webbläsare.

buildPlan, sessionText, parseAreas, toQuery/fromQuery och datumfunktionerna i
assets/js/test-countdown.js är rena funktioner. De anropas direkt via
window.TestCountdown, och varje test körs i två tidszoner (Europe/Stockholm och
America/New_York) så att en sommartidsbyte aldrig kan flytta en dag i planen.
Förväntade planer och texter är fastställda i specen, avsnittet "The planner".
Spec: docs/superpowers/specs/2026-11-14-test-countdown-design.md.
"""
import datetime
import functools
import http.server
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
ZONES = ["Europe/Stockholm", "America/New_York"]

# Områden A…F är bokstäverna själva, så att varje förväntad plan går att läsa direkt.
A, B, C, D, E, F = "A", "B", "C", "D", "E", "F"
ALL_DAYS = [1, 2, 3, 4, 5, 6, 7]

NEW_TAIL = "Then check your notes and try the ones you missed again until you get them right."
MIXED_TAIL = "Then explain one idea out loud without your notes."


def state(test, start, areas, minutes=20, days=None):
    return {"test": test, "start": start, "areas": areas, "minutes": minutes,
            "days": ALL_DAYS if days is None else days}


# Varje fall: (indata, förväntade sessioner som (datum, slag, områden, tidigare, minuter), short, capped).
# Planerna är beräknade med referensimplementationen i briefen och är auktoritativa.
CASES = {
    "A": (
        state("2026-11-20", "2026-11-09", [A, B, C], 20, [1, 2, 3, 4, 5]),
        [("2026-11-09", "new", [A], [], 20),
         ("2026-11-11", "new", [B], [A], 20),
         ("2026-11-13", "new", [C], [A, B], 20),
         ("2026-11-17", "mixed", [A, B, C], [], 20),
         ("2026-11-18", "practice", [A, B, C], [], 20),
         ("2026-11-19", "last", [A, B, C], [], 15)],
        False, False),
    "B": (
        state("2026-11-20", "2026-11-14", [A, B], 30),
        [("2026-11-14", "new", [A], [], 30),
         ("2026-11-16", "new", [B], [A], 30),
         ("2026-11-17", "mixed", [A, B], [], 30),
         ("2026-11-18", "practice", [A, B], [], 30),
         ("2026-11-19", "last", [A, B], [], 15)],
        False, False),
    "C": (
        state("2026-11-20", "2026-11-19", [A, B]),
        [("2026-11-19", "single", [A, B], [], 20)],
        True, False),
    "D": (
        state("2026-11-20", "2026-11-18", [A, B]),
        [("2026-11-18", "new", [A, B], [], 20),
         ("2026-11-19", "last", [A, B], [], 15)],
        True, False),
    "E": (
        state("2026-11-20", "2026-11-16", [A, B, C, D, E]),
        [("2026-11-16", "new", [A, B, C], [], 20),
         ("2026-11-17", "new", [D, E], [A, B, C], 20),
         ("2026-11-18", "practice", [A, B, C, D, E], [], 20),
         ("2026-11-19", "last", [A, B, C, D, E], [], 15)],
        True, False),
    "F": (
        state("2026-12-31", "2026-11-14", [A]),
        [("2026-12-10", "new", [A], [], 20),
         ("2026-12-13", "mixed", [A], [], 20),
         ("2026-12-16", "mixed", [A], [], 20),
         ("2026-12-19", "mixed", [A], [], 20),
         ("2026-12-22", "mixed", [A], [], 20),
         ("2026-12-25", "mixed", [A], [], 20),
         ("2026-12-28", "mixed", [A], [], 20),
         ("2026-12-29", "practice", [A], [], 20),
         ("2026-12-30", "last", [A], [], 15)],
        False, True),
    # G: sommartidens slut i Europa (25 okt 2026) ligger mitt i planen.
    "G": (
        state("2026-10-28", "2026-10-22", [A, B]),
        [("2026-10-22", "new", [A], [], 20),
         ("2026-10-24", "new", [B], [A], 20),
         ("2026-10-25", "mixed", [A, B], [], 20),
         ("2026-10-26", "practice", [A, B], [], 20),
         ("2026-10-27", "last", [A, B], [], 15)],
        False, False),
    # H: bara lördagar är tickade, så startdagen (söndag) är ingen studiedag.
    "H": (
        state("2026-11-20", "2026-11-01", [A], 20, [6]),
        [("2026-11-07", "new", [A], [], 20),
         ("2026-11-14", "last", [A], [], 15)],
        True, False),
    # J: sex områden och 21 dagar, exakt gränsen för tidsfönstret: ingen not om kapning.
    "J": (
        state("2026-12-01", "2026-11-10", [A, B, C, D, E, F]),
        [("2026-11-10", "new", [A], [], 20),
         ("2026-11-13", "new", [B], [A], 20),
         ("2026-11-16", "new", [C], [A, B], 20),
         ("2026-11-19", "new", [D], [A, B, C], 20),
         ("2026-11-22", "new", [E], [A, B, C, D], 20),
         ("2026-11-25", "new", [F], [A, B, C, D, E], 20),
         ("2026-11-28", "mixed", [A, B, C, D, E, F], [], 20),
         ("2026-11-29", "practice", [A, B, C, D, E, F], [], 20),
         ("2026-11-30", "last", [A, B, C, D, E, F], [], 15)],
        False, False),
    # K: exakt tre studiedagar, k = 3: kort plan fast det finns ett övningsprov.
    "K": (
        state("2026-11-20", "2026-11-17", [A]),
        [("2026-11-17", "new", [A], [], 20),
         ("2026-11-18", "practice", [A], [], 20),
         ("2026-11-19", "last", [A], [], 15)],
        True, False),
    # L1: planen går över årsskiftet och fredagen 1 jan 2027 är en tickad dag.
    "L1": (
        state("2027-01-04", "2026-12-28", [A], 20, [1, 2, 3, 4, 5]),
        [("2026-12-28", "new", [A], [], 20),
         ("2026-12-30", "mixed", [A], [], 20),
         ("2026-12-31", "practice", [A], [], 20),
         ("2027-01-01", "last", [A], [], 15)],
        False, False),
    # L2: sommartidens början i Europa (28 mars 2027).
    "L2": (
        state("2027-03-30", "2027-03-26", [A]),
        [("2027-03-26", "new", [A], [], 20),
         ("2027-03-27", "mixed", [A], [], 20),
         ("2027-03-28", "practice", [A], [], 20),
         ("2027-03-29", "last", [A], [], 15)],
        False, False),
}


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


@pytest.fixture(params=ZONES)
def page(request, site, browser):
    # Ett eget sammanhang per tidszon: webbläsarens lokala tid styr bara "idag",
    # aldrig planen, och det är just det som testerna ska fånga.
    ctx = browser.new_context(timezone_id=request.param)
    p = ctx.new_page()
    p.goto(f"{site}/test-countdown/", wait_until="networkidle")
    p.wait_for_function("window.TestCountdown && typeof window.TestCountdown.buildPlan === 'function'")
    yield p
    ctx.close()


def call(page, name, *args):
    return page.evaluate("([n, a]) => window.TestCountdown[n].apply(null, a)", [name, list(args)])


def build(page, s):
    return call(page, "buildPlan", s)


def rows(plan):
    return [(s["date"], s["kind"], s["areas"], s["earlier"], s["minutes"]) for s in plan["sessions"]]


def plan_of(page, case):
    plan = build(page, CASES[case][0])
    assert plan["ok"] is True, plan
    return plan


@pytest.mark.parametrize("case", list(CASES))
def test_expected_plans(page, case):
    given, expected, short, capped = CASES[case]
    plan = plan_of(page, case)
    assert rows(plan) == expected
    assert plan["short"] is short
    assert plan["capped"] is capped
    assert plan["test"] == given["test"]
    assert plan["areas"] == given["areas"]
    # Exakt de fält som gränssnittet utlovar, varken fler eller färre.
    assert set(plan) == {"ok", "test", "areas", "sessions", "short", "capped"}
    assert all(set(s) == {"date", "kind", "areas", "earlier", "minutes"} for s in plan["sessions"])


def test_errors_in_order(page):
    ok = state("2026-11-20", "2026-11-09", [A])
    messages = {
        "test": "Pick your test date to see your plan.",
        "area": "Type at least one area the test covers.",
        "six": "Use at most six areas. Combine some, for example by chapter.",
        "start": "Pick a start date.",
        "after": "The test date must be after the start date.",
        "day": "Tick at least one day you can study.",
        "free": "There are no study days before the test. Tick more days or start earlier.",
    }

    def err(**changes):
        got = build(page, dict(ok, **changes))
        assert got["ok"] is False, got
        assert set(got) == {"ok", "error"}
        return got["error"]

    # Varje meddelande på egen hand.
    assert err(test="") == messages["test"]
    assert err(test="2026-02-30") == messages["test"]
    assert err(test="not a date") == messages["test"]
    assert err(areas=[]) == messages["area"]
    assert err(areas=call(page, "parseAreas", "A\nB\nC\nD\nE\nF\nG")) == messages["six"]
    assert err(start="") == messages["start"]
    assert err(start="2026-13-01") == messages["start"]
    assert err(start="2026-11-20") == messages["after"]
    assert err(start="2026-11-25") == messages["after"]
    assert err(days=[]) == messages["day"]
    # Torsdag 19 nov är enda dagen före provet; bara måndagar är tickade.
    assert err(start="2026-11-19", days=[1]) == messages["free"]

    # Ordningen: det första felet i listan vinner.
    assert err(test="", areas=[], start="", days=[]) == messages["test"]
    assert err(areas=[], start="", days=[]) == messages["area"]
    seven = call(page, "parseAreas", "A\nB\nC\nD\nE\nF\nG")
    assert err(areas=seven, start="") == messages["six"]
    assert err(start="", days=[]) == messages["start"]
    assert err(start="2026-11-25", days=[]) == messages["after"]
    assert err(days=[], start="2026-11-19") == messages["day"]


@pytest.mark.parametrize("minutes", [15, 20, 30, 45])
def test_minutes_last_is_capped(page, minutes):
    given = dict(CASES["A"][0], minutes=minutes)
    plan = build(page, given)
    assert [s["minutes"] for s in plan["sessions"]] == [minutes] * 5 + [15]


def test_never_more_than_nine(page):
    # Rutnät av indata: testdagar som spänner över sommartidsbyten och årsskiftet,
    # starter 1–60 dagar före, 1–6 områden, alla dagar tickade. Allt kontrolleras
    # med Pythons datetime, så att datumräkningen i JavaScript har en oberoende facit.
    tests = ["2026-10-28", "2026-11-20", "2027-01-04", "2027-03-30"]
    states = []
    meta = []
    for test in tests:
        test_day = datetime.date.fromisoformat(test)
        for before in range(1, 61):
            start = test_day - datetime.timedelta(days=before)
            for n in range(1, 7):
                states.append(state(test, start.isoformat(), list("ABCDEF"[:n])))
                meta.append((test_day, start, before, n))
    plans = page.evaluate("s => s.map(x => window.TestCountdown.buildPlan(x))", states)
    assert len(plans) == len(tests) * 60 * 6
    problems = []
    for plan, (test_day, start, before, n) in zip(plans, meta):
        tag = (test_day.isoformat(), start.isoformat(), n)
        if plan["ok"] is not True:
            problems.append((tag, "not ok", plan))
            continue
        dates = [datetime.date.fromisoformat(s["date"]) for s in plan["sessions"]]
        if not 1 <= len(dates) <= 9:
            problems.append((tag, "count", len(dates)))
        if any(b <= a for a, b in zip(dates, dates[1:])):
            problems.append((tag, "not increasing"))
        if any(d >= test_day for d in dates):
            problems.append((tag, "not before the test"))
        # Fönstret: från starten, men högst 21 dagar före provet.
        first_allowed = max(start, test_day - datetime.timedelta(days=21))
        if dates[0] < first_allowed:
            problems.append((tag, "before the window"))
        if plan["capped"] is not (before > 21):
            problems.append((tag, "capped flag", plan["capped"]))
        # Alla dagar är tickade: sista kvällen är dagen före provet.
        if dates[-1] != test_day - datetime.timedelta(days=1):
            problems.append((tag, "last is not the evening before"))
        # Med minst n + 4 lediga dagar övas varje område i minst tre pass
        # (eget pass, ett senare pass och övningsprovet).
        available = min(before, 21)
        if available >= n + 4:
            for area in "ABCDEF"[:n]:
                passes = [s for s in plan["sessions"]
                          if s["kind"] in ("new", "mixed", "practice")
                          and (area in s["areas"] or area in s["earlier"])]
                if len(passes) < 3:
                    problems.append((tag, "area practised too rarely", area, len(passes)))
    assert problems == []


def test_parse_areas(page):
    assert call(page, "parseAreas", "  A \n\n B\n") == ["A", "B"]
    assert call(page, "parseAreas", "x" * 70) == ["x" * 60]
    assert call(page, "parseAreas", "  " + "y" * 61 + "  ") == ["y" * 60]
    assert call(page, "parseAreas", "A\r\nB\r\n") == ["A", "B"]
    # Kapas området mitt i ett mellanrum ska det inte sluta på ett mellanslag.
    assert call(page, "parseAreas", "x" * 59 + " xyz") == ["x" * 59]
    assert call(page, "parseAreas", "") == []
    assert call(page, "parseAreas", " \n\t\n ") == []
    # Ingen gräns på antalet: sjuradslistan avvisas först av buildPlan.
    assert call(page, "parseAreas", "1\n2\n3\n4\n5\n6\n7\n8") == ["1", "2", "3", "4", "5", "6", "7", "8"]
    # Texten lämnas orörd; det är sidan som bara sätter den med textContent.
    assert call(page, "parseAreas", '<b>&"') == ['<b>&"']


def test_format_date_and_join(page):
    assert call(page, "formatDate", "2026-11-09") == "Mon 9 Nov"
    assert call(page, "formatDate", "2026-11-20") == "Fri 20 Nov"
    assert call(page, "formatDate", "2026-10-25") == "Sun 25 Oct"
    assert call(page, "formatDate", "2027-03-28") == "Sun 28 Mar"
    assert call(page, "formatDate", "2027-01-01") == "Fri 1 Jan"
    assert call(page, "formatDate", "2026-12-31") == "Thu 31 Dec"
    assert call(page, "formatDate", "2028-02-29") == "Tue 29 Feb"
    assert call(page, "joinList", ["A"]) == "A"
    assert call(page, "joinList", ["A", "B"]) == "A and B"
    assert call(page, "joinList", ["A", "B", "C"]) == "A, B and C"
    assert call(page, "joinList", ["A", "B", "C", "D", "E", "F"]) == "A, B, C, D, E and F"


def texts(page, case):
    plan = plan_of(page, case)
    return plan, [call(page, "sessionText", s, plan) for s in plan["sessions"]]


def test_session_texts(page):
    # A: tre områden, ett övningsprov; nytt första, nytt senare, blandat, övning, sista kväll.
    plan, got = texts(page, "A")
    assert got[0] == {"label": "Quiz", "text": "Quiz yourself on A. " + NEW_TAIL}
    assert got[1] == {"label": "Quiz", "text": "Quiz yourself on B, then a few questions on A. " + NEW_TAIL}
    assert got[2] == {"label": "Quiz", "text": "Quiz yourself on C, then a few questions on A and B. " + NEW_TAIL}
    assert got[3] == {"label": "Mixed quiz",
                      "text": "Mixed quiz on all areas, starting with what you missed last time. " + MIXED_TAIL}
    assert got[4] == {"label": "Practice test",
                      "text": "Practice test on all areas: no notes, timed, in the same format as the real test. "
                              "Then check your answers and try the ones you got wrong again."}
    assert got[5] == {"label": "Last evening",
                      "text": "Only what you got wrong on the practice test. "
                              "Keep it short, then get a good night's sleep."}

    # E: kort plan, där områdena delar pass: "the most important ideas".
    plan, got = texts(page, "E")
    assert got[0] == {"label": "Quiz",
                      "text": "Quiz yourself on the most important ideas in A, B and C. " + NEW_TAIL}
    assert got[1] == {"label": "Quiz",
                      "text": "Quiz yourself on the most important ideas in D and E, "
                              "then a few questions on A, B and C. " + NEW_TAIL}

    # K: kort plan med ett enda område.
    plan, got = texts(page, "K")
    assert got[0] == {"label": "Quiz", "text": "Quiz yourself on the most important ideas in A. " + NEW_TAIL}
    assert got[1]["label"] == "Practice test"
    assert got[1]["text"].startswith("Practice test on A: no notes, timed, ")

    # L2: ett enda område, ett blandat pass och ett övningsprov.
    plan, got = texts(page, "L2")
    assert got[0] == {"label": "Quiz", "text": "Quiz yourself on A. " + NEW_TAIL}
    assert got[1] == {"label": "Quiz again",
                      "text": "Quiz yourself on A again, starting with what you missed last time. " + MIXED_TAIL}
    assert got[2] == {"label": "Practice test",
                      "text": "Practice test on A: no notes, timed, in the same format as the real test. "
                              "Then check your answers and try the ones you got wrong again."}
    assert got[3] == {"label": "Last evening",
                      "text": "Only what you got wrong on the practice test. "
                              "Keep it short, then get a good night's sleep."}

    # D: ingen övningsprov (två studiedagar): kärnquiz och en annan sista kväll.
    plan, got = texts(page, "D")
    assert got[0] == {"label": "Quiz",
                      "text": "Quiz yourself on the most important ideas in A and B. " + NEW_TAIL}
    assert got[1] == {"label": "Last evening",
                      "text": "Quiz yourself again on what you missed, then one quick round of the most "
                              "important ideas. Keep it short, then get a good night's sleep."}

    # C: ett enda pass.
    plan, got = texts(page, "C")
    assert got == [{"label": "Quiz",
                    "text": "Quiz yourself on the most important ideas in A and B. Check your notes, "
                            "try the ones you missed again, and finish in time for your normal bedtime."}]

    # Testdagen.
    assert call(page, "testRow") == {"label": "Test", "text": "Test day. You have practised for it."}


def test_session_text_is_plain_text(page):
    # Områdesnamn sätts in som text. Sidan sätter dem med textContent, så här
    # får tecknen passera orörda: ingen escapning i JavaScript.
    given = state("2026-11-20", "2026-11-19", ['<b>"x"</b> & co'])
    plan = build(page, given)
    got = call(page, "sessionText", plan["sessions"][0], plan)
    assert got["text"] == ('Quiz yourself on the most important ideas in <b>"x"</b> & co. '
                           "Check your notes, try the ones you missed again, and finish in time for your normal bedtime.")


def test_title_and_total(page):
    plan_a = plan_of(page, "A")
    assert call(page, "planTitle", plan_a) == "Your plan: 6 sessions before the test on Fri 20 Nov"
    assert call(page, "planTotal", plan_a) == "115 minutes in all, spread over 11 days."
    plan_c = plan_of(page, "C")
    assert call(page, "planTitle", plan_c) == "Your plan: 1 session before the test on Fri 20 Nov"
    assert call(page, "planTotal", plan_c) == "20 minutes in all."
    # F: kapad plan över månadsskiftet, första passet 10 dec och provet 31 dec: 21 dagar.
    plan_f = plan_of(page, "F")
    assert call(page, "planTitle", plan_f) == "Your plan: 9 sessions before the test on Thu 31 Dec"
    assert call(page, "planTotal", plan_f) == "175 minutes in all, spread over 21 days."
    # D: två pass, 20 + 15 minuter.
    assert call(page, "planTotal", plan_of(page, "D")) == "35 minutes in all, spread over 2 days."


def test_query_round_trip(page):
    given = CASES["A"][0]
    query = call(page, "toQuery", given)
    assert query == "test=2026-11-20&start=2026-11-09&min=20&days=12345&area=A&area=B&area=C"
    assert call(page, "fromQuery", query) == {
        "test": "2026-11-20", "start": "2026-11-09", "minutes": 20, "days": [1, 2, 3, 4, 5], "areas": [A, B, C]}
    assert call(page, "fromQuery", "?" + query) == call(page, "fromQuery", query)
    # Adressens exempel i specen.
    assert call(page, "toQuery", state("2026-11-20", "2026-11-09", ["Cells", "Photosynthesis"])) == \
        "test=2026-11-20&start=2026-11-09&min=20&days=1234567&area=Cells&area=Photosynthesis"


def test_query_days_are_sorted_digits(page):
    given = state("2026-11-20", "2026-11-09", [A], 30, [7, 1, 5, 3])
    assert "&min=30&days=1357&area=A" in call(page, "toQuery", given)


def test_query_round_trip_with_awkward_text(page):
    # Mellanslag, &, =, %, HTML och icke-ASCII ska komma tillbaka som exakt samma områden.
    areas = ["Food chains", "A&B=C", "100% <b>sure</b>", "Växter och djur", "a+b"]
    given = state("2026-11-20", "2026-11-09", areas, 45, [2, 4, 6])
    query = call(page, "toQuery", given)
    assert "<" not in query and " " not in query
    assert call(page, "fromQuery", query) == {
        "test": "2026-11-20", "start": "2026-11-09", "minutes": 45, "days": [2, 4, 6], "areas": areas}


def test_from_query_ignores_bad_parts(page):
    # Gamla eller handredigerade länkar: ogiltiga delar ignoreras, inget kastas.
    assert call(page, "fromQuery", "?test=2026-02-30&start=x&min=17&days=08&area=&area=+") == {}
    assert call(page, "fromQuery", "") == {}
    assert call(page, "fromQuery", "?") == {}
    assert call(page, "fromQuery", "?days=771") == {"days": [1, 7]}
    for bad_days in ("days=", "days=0", "days=8", "days=18", "days=1,2", "days=1%202"):
        assert call(page, "fromQuery", "?" + bad_days) == {}, bad_days
    for bad_min in ("min=", "min=17", "min=20x", "min=020", "min=1e1", "min=-20", "min=%2020"):
        assert call(page, "fromQuery", "?" + bad_min) == {}, bad_min
    for good_min in (15, 20, 30, 45):
        assert call(page, "fromQuery", f"?min={good_min}") == {"minutes": good_min}
    # Datum måste finnas i kalendern: 2028 är skottår, 2027 inte.
    assert call(page, "fromQuery", "?test=2028-02-29") == {"test": "2028-02-29"}
    assert call(page, "fromQuery", "?test=2027-02-29") == {}
    for bad_date in ("2026-1-5", "20261105", "2026-11-31", "2026-00-10", "2026-11-00", "2026-11-05T10:00"):
        assert call(page, "fromQuery", "?start=" + bad_date) == {}, bad_date
    # Ett giltigt datum bredvid ett ogiltigt behålls.
    assert call(page, "fromQuery", "?test=2026-11-20&start=2026-02-30") == {"test": "2026-11-20"}
    # Sju områden: de sex första behålls. Tomma värden hoppas över.
    seven = "&".join(f"area={c}" for c in "ABCDEFG")
    assert call(page, "fromQuery", "?" + seven) == {"areas": list("ABCDEF")}
    assert call(page, "fromQuery", "?area=&area=A&area=%20&area=B") == {"areas": [A, B]}
    # Områdesvärden går genom samma regler som textrutan: trimmas och kapas vid 60 tecken.
    assert call(page, "fromQuery", "?area=" + "z" * 70) == {"areas": ["z" * 60]}
    assert call(page, "fromQuery", "?area=%3Cb%3E%26") == {"areas": ["<b>&"]}
