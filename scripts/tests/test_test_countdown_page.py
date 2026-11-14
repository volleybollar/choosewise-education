"""Planeraren på /test-countdown/ i en riktig webbläsare.

Eleven fyller i provdag, startdag, områden, minuter och veckodagar, och
assets/js/test-countdown.js bygger planen medan hon skriver. Planen och
meddelandena kommer från rena funktioner som testas för sig i
test_test_countdown_plan.py; här testas kopplingen till sidan: fälten, raderna,
noterna, adressfältet, kopieringsknappen och utskriften. Allt som skrivs in
ska hamna på sidan som ren text, aldrig som HTML.
Spec: docs/superpowers/specs/2026-11-14-test-countdown-design.md.
"""
import datetime
import functools
import http.server
import socketserver
import threading
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

import pytest

ROOT = Path(__file__).resolve().parents[2]
ALL_DAYS = [1, 2, 3, 4, 5, 6, 7]
PICK_DATE = "Pick your test date to see your plan."
NO_AREA = "Type at least one area the test covers."
NO_DAY = "Tick at least one day you can study."
NOT_AFTER = "The test date must be after the start date."


def state(test, start, areas, minutes=20, days=None):
    return {"test": test, "start": start, "areas": areas, "minutes": minutes,
            "days": ALL_DAYS if days is None else days}


# Samma fall A, E och F som i test_test_countdown_plan.py.
CASE_A = state("2026-11-20", "2026-11-09", ["A", "B", "C"], 20, [1, 2, 3, 4, 5])
CASE_E = state("2026-11-20", "2026-11-16", ["A", "B", "C", "D", "E"])
CASE_F = state("2026-12-31", "2026-11-14", ["A"])
CASE_A_QUERY = "test=2026-11-20&start=2026-11-09&min=20&days=12345&area=A&area=B&area=C"


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
    # Stockholm: webbläsarens lokala tid styr bara "idag", aldrig planen.
    ctx = browser.new_context(timezone_id="Europe/Stockholm")
    # Kopieringsknappen skriver till urklipp; i tester måste det tillåtas.
    ctx.grant_permissions(["clipboard-read", "clipboard-write"], origin=site)
    yield ctx
    ctx.close()


def open_page(ctx, url, now=None):
    """Öppnar sidan. now = ett fast ögonblick (som "2026-11-14T10:00:00Z"): då är "idag" given."""
    p = ctx.new_page()
    if now:
        p.clock.set_fixed_time(now)
    # Alla fel i konsolen och alla oväntade undantag samlas; testerna som
    # öppnar gamla eller trasiga länkar kontrollerar att listan är tom.
    p.errors = []
    p.on("console", lambda m: m.type == "error" and p.errors.append(m.text))
    p.on("pageerror", lambda e: p.errors.append(str(e)))
    p.goto(url, wait_until="networkidle")
    p.wait_for_function("window.TestCountdown && typeof window.TestCountdown.buildPlan === 'function'")
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
    """Fyller i formuläret som en elev: ett fält i taget, så varje fält ger en egen händelse."""
    page.fill("#tc-test", given["test"])
    page.fill("#tc-start", given["start"])
    page.select_option("#tc-minutes", str(given["minutes"]))
    page.fill("#tc-areas", "\n".join(given["areas"]))
    for day in ALL_DAYS:
        page.set_checked(f'#tc-days input[value="{day}"]', day in given["days"])


def rows(page):
    """Planens rader som data: klasser, barnens klasser och texterna."""
    return page.locator("#tc-plan-list > li").evaluate_all("""
        items => items.map(li => ({
          cls: li.className,
          children: Array.from(li.children).map(c => c.className),
          date: li.querySelector('.tc-row__date').textContent,
          label: li.querySelector('.tc-row__label').textContent,
          text: li.querySelector('.tc-row__text').textContent,
          minutes: li.querySelector('.tc-row__minutes')
            ? li.querySelector('.tc-row__minutes').textContent : null
        }))""")


def form_values(page):
    return page.evaluate("""() => ({
        test: document.getElementById('tc-test').value,
        start: document.getElementById('tc-start').value,
        minutes: document.getElementById('tc-minutes').value,
        areas: document.getElementById('tc-areas').value,
        days: Array.from(document.querySelectorAll('#tc-days input'))
          .filter(i => i.checked).map(i => i.value)
      })""")


def hint(page):
    return page.inner_text("#tc-hint")


def query_of(page):
    return urlparse(page.url).query


# Länken till fall A öppnad efter respektive före första passet (mån 9 nov).
NOW_AFTER_START = "2026-11-14T10:00:00Z"
NOW_BEFORE_START = "2026-11-08T10:00:00Z"
PAST_LINK_QUERY = "start=2026-11-09&test=2026-11-20&area=A"


def local_today(zone):
    return datetime.datetime.now(ZoneInfo(zone)).date().isoformat()


def test_initial_state(context, base):
    # "Idag" i Stockholm räknas före och efter att sidan öppnats, så att ett
    # midnattsskifte under testet inte kan ge ett falskt fel.
    before = local_today("Europe/Stockholm")
    page = open_page(context, base)
    after = local_today("Europe/Stockholm")
    assert hint(page) == PICK_DATE
    assert page.is_hidden("#tc-plan")
    assert page.input_value("#tc-start") in {before, after}
    # Resten av formuläret står på sina standardvärden.
    assert page.input_value("#tc-test") == ""
    assert page.input_value("#tc-areas") == ""
    assert page.input_value("#tc-minutes") == "20"
    assert page.locator("#tc-days input:checked").count() == 7
    # En vanlig sidladdning rör inte adressen, och länken pekar på den.
    assert query_of(page) == ""
    assert page.evaluate("location.search") == ""
    assert page.get_attribute("#tc-link", "data-copy") == page.url
    assert page.errors == []


@pytest.mark.parametrize("zone, instant, expected", [
    # 00:30 i Stockholm är fortfarande dagen innan i UTC.
    ("Europe/Stockholm", "2026-11-13T23:30:00Z", "2026-11-14"),
    # 19:00 i Los Angeles är redan nästa dag i UTC.
    ("America/Los_Angeles", "2026-11-14T03:00:00Z", "2026-11-13"),
])
def test_today_is_the_local_date(browser, base, zone, instant, expected):
    # Klockan är fast och tidszonen vald, så "idag" måste komma från lokala
    # getters: UTC-datumet skulle ge fel dag i bägge fallen.
    ctx = browser.new_context(timezone_id=zone)
    try:
        p = ctx.new_page()
        p.clock.set_fixed_time(instant)
        p.goto(base, wait_until="networkidle")
        p.wait_for_function("window.TestCountdown")
        assert p.input_value("#tc-start") == expected
    finally:
        # Sammanhanget stängs även när något av ovanstående faller.
        ctx.close()


def test_case_a_renders(page):
    fill_plan(page, CASE_A)
    assert page.is_visible("#tc-plan")
    assert hint(page) == ""
    assert page.inner_text("#tc-plan-title") == "Your plan: 6 sessions before the test on Fri 20 Nov"
    assert page.inner_text("#tc-plan-total") == "115 minutes in all, spread over 11 days."

    got = rows(page)
    assert len(got) == 7
    assert [(r["date"], r["label"], r["minutes"]) for r in got] == [
        ("Mon 9 Nov", "Quiz", "20 min"),
        ("Wed 11 Nov", "Quiz", "20 min"),
        ("Fri 13 Nov", "Quiz", "20 min"),
        ("Tue 17 Nov", "Mixed quiz", "20 min"),
        ("Wed 18 Nov", "Practice test", "20 min"),
        ("Thu 19 Nov", "Last evening", "15 min"),
        ("Fri 20 Nov", "Test", None),
    ]
    # Radens slag syns som klass, och byggstenarna ligger i ordningen datum, text, minuter.
    assert [r["cls"] for r in got] == [
        "tc-row tc-row--new", "tc-row tc-row--new", "tc-row tc-row--new", "tc-row tc-row--mixed",
        "tc-row tc-row--practice", "tc-row tc-row--last", "tc-row tc-row--test"]
    assert got[0]["children"] == ["tc-row__date", "tc-row__main", "tc-row__minutes"]
    assert got[6]["children"] == ["tc-row__date", "tc-row__main"]
    # Texterna kommer från sessionText och testRow.
    assert got[0]["text"] == ("Quiz yourself on A. Then check your notes and try the ones "
                              "you missed again until you get them right.")
    assert got[5]["text"] == "Only what you got wrong on the practice test. Keep it short, then get a good night's sleep."
    assert got[6]["text"] == "Test day. You have practised for it."
    # Planen är en lista med rollen kvar även när punkterna är borttagna med CSS.
    assert page.get_attribute("#tc-plan-list", "role") == "list"
    assert page.is_hidden("#tc-short")
    assert page.is_hidden("#tc-capped")
    assert page.errors == []


def test_minutes_and_days_change_the_plan(page):
    # Minuterna kommer från rullgardinen och dagarna från kryssrutorna.
    fill_plan(page, CASE_A)
    page.select_option("#tc-minutes", "45")
    assert [r["minutes"] for r in rows(page)] == ["45 min"] * 5 + ["15 min", None]
    assert page.inner_text("#tc-plan-total") == "240 minutes in all, spread over 11 days."
    # Med lördag och söndag ikryssade finns elva studiedagar i stället för nio:
    # sju pass, där de nya passen ligger varannan dag och två är blandade.
    page.set_checked('#tc-days input[value="6"]', True)
    page.set_checked('#tc-days input[value="7"]', True)
    assert [r["date"] for r in rows(page)] == [
        "Mon 9 Nov", "Wed 11 Nov", "Fri 13 Nov", "Sun 15 Nov", "Tue 17 Nov", "Wed 18 Nov", "Thu 19 Nov", "Fri 20 Nov"]
    assert page.inner_text("#tc-plan-title") == "Your plan: 7 sessions before the test on Fri 20 Nov"
    assert page.inner_text("#tc-plan-total") == "285 minutes in all, spread over 11 days."
    assert page.errors == []


def test_area_text_is_text(context, base):
    area = '<b>x</b> & "y"'
    page = open_page(context, base)
    fill_plan(page, state("2026-11-20", "2026-11-19", [area]))
    got = rows(page)
    assert len(got) == 2
    assert got[0]["text"] == (f"Quiz yourself on the most important ideas in {area}. Check your notes, "
                              "try the ones you missed again, and finish in time for your normal bedtime.")
    # Inga element av texten: <b> blev aldrig HTML.
    assert page.locator("#tc-plan-list b").count() == 0
    assert "&lt;b&gt;" in page.inner_html("#tc-plan-list")
    assert page.errors == []

    # Samma text kommer tillbaka ur länken, i fältet och i planen.
    again = open_page(context, page.url)
    assert again.input_value("#tc-areas") == area
    assert rows(again) == got
    assert again.locator("#tc-plan-list b").count() == 0
    assert again.errors == []


def test_notes_toggle(page):
    fill_plan(page, CASE_E)
    assert page.is_visible("#tc-short")
    assert page.is_hidden("#tc-capped")
    fill_plan(page, CASE_F)
    assert page.is_hidden("#tc-short")
    assert page.is_visible("#tc-capped")
    fill_plan(page, CASE_A)
    assert page.is_hidden("#tc-short")
    assert page.is_hidden("#tc-capped")
    # Den alltid synliga noten står kvar.
    assert page.is_visible(".tc-sensible")


def test_past_note_shows_when_the_first_session_has_passed(context, base):
    # Länken har startdag mån 9 nov, och planens första pass ligger då på den dagen.
    # Öppnad 14 nov har det passet redan varit: noten visas.
    page = open_page(context, base + "?" + PAST_LINK_QUERY, now=NOW_AFTER_START)
    assert rows(page)[0]["date"] == "Mon 9 Nov"
    assert page.is_visible("#tc-past")
    assert page.inner_text("#tc-past") == ("Some of these sessions are already in the past. "
                                           "To plan from today, set Start on to today.")
    # Startdagen sätts till idag: första passet är idag, inget ligger bakåt, och noten försvinner.
    page.fill("#tc-start", "2026-11-14")
    assert rows(page)[0]["date"] == "Sat 14 Nov"
    assert page.is_hidden("#tc-past")
    # Sätts startdagen bakåt igen kommer noten tillbaka.
    page.fill("#tc-start", "2026-11-12")
    assert page.is_visible("#tc-past")
    assert page.errors == []

    # Öppnad 8 nov har inget pass hunnit gå.
    early = open_page(context, base + "?" + PAST_LINK_QUERY, now=NOW_BEFORE_START)
    assert early.is_visible("#tc-plan")
    assert early.is_hidden("#tc-past")
    assert early.errors == []


def test_past_note_uses_the_local_date(browser, base):
    # Passet 14 nov är idag (inte bakåt) hela dagen, även 00:30 i Stockholm när UTC fortfarande är 13 nov.
    ctx = browser.new_context(timezone_id="Europe/Stockholm")
    try:
        page = open_page(ctx, base + "?start=2026-11-14&test=2026-11-20&area=A", now="2026-11-13T23:30:00Z")
        assert page.input_value("#tc-start") == "2026-11-14"
        assert page.is_hidden("#tc-past")
        # Samma länk en dag senare: då har 14 nov gått.
        late = open_page(ctx, base + "?start=2026-11-14&test=2026-11-20&area=A", now="2026-11-14T23:30:00Z")
        assert late.is_visible("#tc-past")
    finally:
        ctx.close()


def test_messages(page):
    fill_plan(page, CASE_A)
    assert page.is_visible("#tc-plan")

    page.fill("#tc-areas", "")
    assert hint(page) == NO_AREA
    assert page.is_hidden("#tc-plan")

    page.fill("#tc-areas", "A\nB\nC")
    assert hint(page) == ""
    assert page.is_visible("#tc-plan")

    for day in ALL_DAYS:
        page.set_checked(f'#tc-days input[value="{day}"]', False)
    assert hint(page) == NO_DAY
    assert page.is_hidden("#tc-plan")

    page.set_checked('#tc-days input[value="1"]', True)
    assert hint(page) == ""
    assert page.is_visible("#tc-plan")

    page.fill("#tc-start", "2026-11-20")
    assert hint(page) == NOT_AFTER
    assert page.is_hidden("#tc-plan")

    page.fill("#tc-test", "")
    assert hint(page) == PICK_DATE
    assert page.is_hidden("#tc-plan")
    assert page.errors == []


def test_hint_is_written_only_when_it_changes(page):
    # Ledtråden är aria-live: skrivs samma text om och om igen läser en
    # skärmläsare upp den för varje tangenttryckning.
    page.evaluate("""() => {
        window.hintWrites = 0;
        new MutationObserver(records => { window.hintWrites += records.length; })
          .observe(document.getElementById('tc-hint'), { childList: true, characterData: true, subtree: true });
      }""")
    page.fill("#tc-start", "2026-11-09")
    page.focus("#tc-areas")
    page.keyboard.type("Cells")
    assert hint(page) == PICK_DATE
    assert page.evaluate("window.hintWrites") == 0
    # Provdagen gör att ledtråden byter text en gång; första tecknet i området en gång till.
    page.fill("#tc-test", "2026-11-20")
    assert hint(page) == ""
    assert page.evaluate("window.hintWrites") == 1
    page.focus("#tc-areas")
    page.keyboard.type(" and more")
    assert page.evaluate("window.hintWrites") == 1


def test_status_announces_the_plan(page):
    # Skärmläsarens ruta bär planens rubrik; utan plan är den tom.
    assert page.text_content("#tc-status") == ""
    fill_plan(page, CASE_A)
    title = "Your plan: 6 sessions before the test on Fri 20 Nov"
    assert page.text_content("#tc-status") == title
    assert page.text_content("#tc-status") == page.inner_text("#tc-plan-title")
    # Rutan ligger utanför #tc-plan, så den läses upp även när planen byggs om.
    assert page.evaluate("!document.getElementById('tc-plan').contains(document.getElementById('tc-status'))")
    assert page.get_attribute("#tc-status", "aria-live") == "polite"
    # En annan plan ger en annan rubrik, och utan plan töms rutan.
    page.set_checked('#tc-days input[value="6"]', True)
    page.set_checked('#tc-days input[value="7"]', True)
    assert page.text_content("#tc-status") == "Your plan: 7 sessions before the test on Fri 20 Nov"
    page.fill("#tc-areas", "")
    assert page.text_content("#tc-status") == ""
    assert page.errors == []


def test_status_is_written_only_when_it_changes(page):
    # Rutan är aria-live: samma rubrik skriven om och om igen läses upp varje gång.
    fill_plan(page, CASE_A)
    page.evaluate("""() => {
        window.statusWrites = 0;
        new MutationObserver(records => { window.statusWrites += records.length; })
          .observe(document.getElementById('tc-status'), { childList: true, characterData: true, subtree: true });
      }""")
    # Minuterna ändrar planen men inte rubriken; samma plan igen, två gånger per ändring.
    page.select_option("#tc-minutes", "30")
    page.select_option("#tc-minutes", "20")
    page.fill("#tc-areas", "\n".join(CASE_A["areas"]))
    page.evaluate("""() => {
        const form = document.getElementById('tc-form');
        form.dispatchEvent(new Event('input', { bubbles: true }));
        form.dispatchEvent(new Event('change', { bubbles: true }));
      }""")
    assert page.evaluate("window.statusWrites") == 0
    assert page.text_content("#tc-status") == "Your plan: 6 sessions before the test on Fri 20 Nov"
    # Lördagen ensam ändrar planen men inte rubriken (fortfarande sex pass): inget skrivs.
    page.set_checked('#tc-days input[value="6"]', True)
    assert page.evaluate("window.statusWrites") == 0
    # Söndagen också ger sju pass: en ny rubrik skrivs, en gång.
    page.set_checked('#tc-days input[value="7"]', True)
    assert page.text_content("#tc-status") == "Your plan: 7 sessions before the test on Fri 20 Nov"
    assert page.evaluate("window.statusWrites") == 1
    # Samma rubrik igen (minuterna ändras): inget nytt skrivs.
    page.select_option("#tc-minutes", "30")
    assert page.evaluate("window.statusWrites") == 1


def test_plan_event(context, base):
    # Task 5 lyssnar på tc:plan: planen när det finns en, annars null, och en
    # första gång redan vid laddningen.
    context.add_init_script("""
        window.tcEvents = [];
        document.addEventListener('tc:plan', e => window.tcEvents.push(e.detail));
      """)
    page = open_page(context, base)
    assert page.evaluate("window.tcEvents") == [None]
    fill_plan(page, CASE_A)
    last = page.evaluate("window.tcEvents[window.tcEvents.length - 1]")
    assert last["ok"] is True
    assert last["test"] == "2026-11-20"
    assert len(last["sessions"]) == 6
    page.fill("#tc-areas", "")
    assert page.evaluate("window.tcEvents[window.tcEvents.length - 1]") is None
    assert page.errors == []


def test_link_restores_plan(context, page):
    fill_plan(page, CASE_A)
    # Adressen är planens indata, och länkknappen kopierar just den adressen.
    assert query_of(page) == CASE_A_QUERY
    assert query_of(page) == page.evaluate("s => window.TestCountdown.toQuery(s)", CASE_A)
    assert page.get_attribute("#tc-link", "data-copy") == page.url
    # Knappen kopierar den på riktigt, via copy-to-clipboard.js.
    page.click("#tc-link")
    assert page.evaluate("navigator.clipboard.readText()") == page.url
    assert page.locator(".tm-copy-row .copy-toast--visible").count() == 1

    # En ny flik på den adressen visar samma formulär och samma rader.
    again = open_page(context, page.url)
    assert form_values(again) == form_values(page)
    assert form_values(again) == {"test": "2026-11-20", "start": "2026-11-09", "minutes": "20",
                                  "areas": "A\nB\nC", "days": ["1", "2", "3", "4", "5"]}
    assert rows(again) == rows(page)
    assert again.inner_text("#tc-plan-title") == page.inner_text("#tc-plan-title")
    assert hint(again) == ""
    # Öppnad med parametrar: adressen skrivs om till formulärets läge, oförändrad här.
    assert query_of(again) == CASE_A_QUERY
    assert again.get_attribute("#tc-link", "data-copy") == again.url
    assert again.errors == []


def test_copy_link_is_built_from_the_form(page, base):
    # Kopieringsadressen byggs av samma läge som planen, inte av location.href.
    fill_plan(page, CASE_A)
    expected = f"{base}?{CASE_A_QUERY}"
    assert page.get_attribute("#tc-link", "data-copy") == expected
    assert expected == base + "?" + page.evaluate("s => window.TestCountdown.toQuery(s)", CASE_A)
    page.click("#tc-link")
    assert page.evaluate("navigator.clipboard.readText()") == expected


def test_copy_link_survives_a_refusing_history(page, base):
    # Safari kan vägra replaceState efter en snabb följd av ändringar: planen och
    # länken ska ändå stämma med formuläret, medan adressfältet står kvar som det var.
    page.evaluate("() => { history.replaceState = () => { throw new Error('refused'); }; }")
    fill_plan(page, CASE_A)
    assert page.is_visible("#tc-plan")
    assert rows(page)[0]["date"] == "Mon 9 Nov"
    assert query_of(page) == ""
    assert page.get_attribute("#tc-link", "data-copy") == f"{base}?{CASE_A_QUERY}"
    # Nästa ändring ger en ny länk, fortfarande utan att adressfältet rörs.
    page.select_option("#tc-minutes", "30")
    assert page.get_attribute("#tc-link", "data-copy") == f"{base}?{CASE_A_QUERY.replace('min=20', 'min=30')}"
    assert page.errors == []


def test_copy_link_keeps_the_hash(context, base):
    page = open_page(context, base + "?" + CASE_A_QUERY + "#tc-make")
    assert page.get_attribute("#tc-link", "data-copy") == f"{base}?{CASE_A_QUERY}#tc-make"
    assert page.errors == []


def test_link_without_minutes_and_days_gets_the_defaults(context, base):
    # En länk som bara har provdag och område: resten fylls i med standardvärdena
    # och adressen skrivs om så att den beskriver planen som visas.
    page = open_page(context, base + "?test=2026-11-20&start=2026-11-09&area=A")
    assert form_values(page)["minutes"] == "20"
    assert len(form_values(page)["days"]) == 7
    assert rows(page)[0]["date"] == "Mon 9 Nov"
    assert query_of(page) == "test=2026-11-20&start=2026-11-09&min=20&days=1234567&area=A"
    assert page.get_attribute("#tc-link", "data-copy") == page.url
    assert page.errors == []


def test_bad_link_keeps_defaults(context, base):
    page = open_page(context, base + "?test=2026-02-30&min=17&days=9")
    got = form_values(page)
    assert got["test"] == ""
    assert got["minutes"] == "20"
    assert got["days"] == ["1", "2", "3", "4", "5", "6", "7"]
    assert got["areas"] == ""
    assert got["start"] != ""
    assert hint(page) == PICK_DATE
    assert page.is_hidden("#tc-plan")
    # Inget av parametrarna var giltigt, så adressen lämnas som den var, och länken följer med.
    assert query_of(page) == "test=2026-02-30&min=17&days=9"
    assert page.get_attribute("#tc-link", "data-copy") == page.url
    assert page.errors == []


def test_unrelated_parameters_keep_the_address(context, base):
    # En länk med bara andra parametrar (till exempel från ett utskick) lämnas orörd
    # tills eleven ändrar något; då skrivs adressen om till planens indata.
    page = open_page(context, base + "?utm_source=mail")
    assert query_of(page) == "utm_source=mail"
    assert page.get_attribute("#tc-link", "data-copy") == page.url
    assert hint(page) == PICK_DATE
    assert page.errors == []
    page.fill("#tc-areas", "A")
    assert "utm_source" not in query_of(page)
    assert query_of(page).endswith("&min=20&days=1234567&area=A")
    assert page.get_attribute("#tc-link", "data-copy") == page.url
    assert page.errors == []


def test_no_overflow_390(browser, base):
    ctx = browser.new_context(timezone_id="Europe/Stockholm", viewport={"width": 390, "height": 844})
    page = open_page(ctx, base)
    fill_plan(page, CASE_A)
    assert page.is_visible("#tc-plan")
    assert page.evaluate("document.documentElement.scrollWidth") <= 390
    # Sex områden på 60 tecken utan mellanslag: längsta tänkbara text i en rad.
    long_area = "Photosynthesisandcellularrespirationinplantsandanimalsofallkinds"[:60]
    fill_plan(page, state("2026-12-01", "2026-11-10", [long_area] * 6))
    assert page.is_visible("#tc-plan")
    assert page.evaluate("document.documentElement.scrollWidth") <= 390
    assert page.errors == []
    ctx.close()


def test_print_button_prints(page):
    fill_plan(page, CASE_A)
    page.evaluate("() => { window.printCalls = 0; window.print = () => { window.printCalls += 1; }; }")
    page.click("#tc-print")
    assert page.evaluate("window.printCalls") == 1


def test_print_view(page):
    fill_plan(page, CASE_A)
    # På skärmen syns rubriken över formuläret; på papper ska den inte skrivas ut.
    assert page.is_visible("#tc-make > .section__title")
    page.emulate_media(media="print")
    # Bara planen, hur man testar sig själv och varför ska skrivas ut.
    for hidden in ("#tc-form", "#tc-teachers", "#tc-evidence", "#tc-age", "#tc-link", "#tc-print",
                   "#tc-make > .section__title"):
        assert page.is_hidden(hidden), hidden
    for shown in ("#tc-plan", "#tc-howto", "#tc-why"):
        assert page.is_visible(shown), shown


def test_print_hides_the_past_note_and_the_status(context, base):
    # Dagens datum är fast: planen har pass som redan varit, så noten syns på skärmen
    # men ska inte skrivas ut. Skärmläsarens ruta är aldrig till för papper.
    page = open_page(context, base + "?" + CASE_A_QUERY, now=NOW_AFTER_START)
    assert page.is_visible("#tc-past")
    display = lambda sel: page.evaluate("s => getComputedStyle(document.querySelector(s)).display", sel)
    assert display("#tc-status") != "none"
    page.emulate_media(media="print")
    assert page.is_hidden("#tc-past")
    assert display("#tc-past") == "none"
    assert display("#tc-status") == "none"
    assert page.is_visible("#tc-plan")
    assert page.errors == []
