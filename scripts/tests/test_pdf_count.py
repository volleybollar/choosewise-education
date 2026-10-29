"""PDF-nedladdningar räknas som anonyma GoatCounter-händelser.

GoatCounters riktiga skript (gc.zgo.at/count.js) byts mot en stub som
skickar varje anrop till testet via expose_function. Anropet ska ha formen
{path: 'pdf/<sökväg under assets/pdfs utan .pdf>', title: <filnamn>, event: true}
— dashboardens innehållskarta i AI OS läser exakt det formatet.

/dl/ är sidan som mejllänkarna går via: den räknar och skickar vidare,
men bara till PDF:er under /assets/pdfs/ på den egna sajten.
"""
from __future__ import annotations

import functools
import http.server
import json
import socketserver
import threading
import time
from pathlib import Path
from urllib.parse import urlparse

import pytest

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = "/scripts/tests/fixtures/pdf-count.html"
GC = "**/gc.zgo.at/**"
# Stubben härmar det count.js gör som spelar roll här: behåller inställningar
# som sidan redan satt, skickar en sidvisning vid laddning om inte no_onload
# är satt, och låter en path-funktion skriva om sidvisningens sökväg.
# Händelser (count med argument) går till __gcCount, sidvisningar till __gcPageview.
STUB = """(function () {
  var g = window.goatcounter = window.goatcounter || {};
  g.count = function (o) {
    if (o) { window.__gcCount(JSON.stringify(o)); return; }
    var p = location.pathname + location.search;
    if (typeof g.path === 'function') p = g.path(p);
    window.__gcPageview(p);
  };
  if (!g.no_onload) g.count();
})();"""


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


def _make_page(browser, goatcounter="stub"):
    ctx = browser.new_context()
    p = ctx.new_page()
    p.calls = []      # GoatCounter-händelser, som dict
    p.pageviews = []  # GoatCounter-sidvisningar, som sökväg
    p.pdf_hits = []   # PDF-adresser webbläsaren försökte öppna
    p.errors = []     # okastade JS-fel på sidan
    ctx.expose_function("__gcCount", lambda s: p.calls.append(json.loads(s)))
    ctx.expose_function("__gcPageview", lambda s: p.pageviews.append(s))
    p.on("pageerror", lambda e: p.errors.append(str(e)))

    def on_pdf(route):
        p.pdf_hits.append(route.request.url)
        route.fulfill(status=200, body="%PDF-1.4", headers={"content-type": "application/pdf"})

    # Matcha på sökvägen, inte hela adressen: /dl/?f=x.pdf slutar också på .pdf.
    p.route(lambda url: urlparse(url).path.endswith(".pdf"), on_pdf)
    if goatcounter == "stub":
        p.route(GC, lambda r: r.fulfill(status=200, body=STUB,
                                        headers={"content-type": "text/javascript"}))
    else:  # blockerat, som av en annonsblockerare
        p.route(GC, lambda r: r.abort())
    return ctx, p


@pytest.fixture
def page(browser):
    ctx, p = _make_page(browser)
    yield p
    ctx.close()


@pytest.fixture
def blocked_page(browser):
    ctx, p = _make_page(browser, goatcounter="blocked")
    yield p
    ctx.close()


def wait_for(page, cond, timeout=3.0):
    # page.wait_for_timeout, inte time.sleep: Playwrights sync-API tar bara emot
    # anrop från sidan (expose_function, route) medan ett Playwright-anrop pågår.
    end = time.time() + timeout
    while time.time() < end:
        if cond():
            return True
        page.wait_for_timeout(50)
    return cond()


def open_fixture(page, site):
    page.goto(f"{site}{FIXTURE}")
    page.wait_for_function("typeof window.cwCountPdf === 'function'")


# ── Vanliga PDF-länkar ──

@pytest.mark.parametrize("link, path, title", [
    ("#rel", "pdf/free/visual-codes-50-en", "visual-codes-50-en.pdf"),
    ("#abs", "pdf/nlm-140-prompts-en", "nlm-140-prompts-en.pdf"),
    ("#up", "pdf/prompts/biology-en", "biology-en.pdf"),
])
def test_click_on_pdf_link_is_counted(page, site, link, path, title):
    open_fixture(page, site)
    page.click(link)
    assert wait_for(page, lambda: page.calls)
    assert page.calls == [{"path": path, "title": title, "event": True}]


def test_pdf_outside_assets_pdfs_is_not_counted(page, site):
    open_fixture(page, site)
    page.click("#outside")
    assert wait_for(page, lambda: page.pdf_hits)
    page.wait_for_timeout(300)
    assert page.calls == []


def test_count_waits_in_queue_until_goatcounter_loads(blocked_page, site):
    page = blocked_page
    open_fixture(page, site)
    page.evaluate("window.cwCountPdf('/assets/pdfs/free/visual-codes-50-en.pdf')")
    page.wait_for_timeout(300)
    assert page.calls == []
    page.evaluate(STUB)
    assert wait_for(page, lambda: page.calls)
    assert page.calls == [{"path": "pdf/free/visual-codes-50-en",
                           "title": "visual-codes-50-en.pdf", "event": True}]


def test_blocked_goatcounter_throws_nothing_and_pdf_still_opens(blocked_page, site):
    page = blocked_page
    open_fixture(page, site)
    with page.expect_request("**/visual-codes-50-en.pdf"):
        page.click("#rel")
    assert page.errors == []


# ── E-postgrinden ──

def test_returning_subscriber_gate_click_is_counted_once(page, site):
    page.add_init_script("localStorage.setItem('cw-subscribed', '1')")
    open_fixture(page, site)
    with page.expect_request("**/teachers-en.pdf"):
        page.click("#gate")
    assert wait_for(page, lambda: page.calls)
    page.wait_for_timeout(300)
    assert page.calls == [{"path": "pdf/prompts/teachers-en",
                           "title": "teachers-en.pdf", "event": True}]


def test_new_visitor_counts_on_download_link_not_on_modal(page, site):
    page.route("**/assets.mailerlite.com/**", lambda r: r.fulfill(status=200, body=""))
    open_fixture(page, site)
    page.click("#gate")
    page.wait_for_selector(".modal-backdrop--open")
    page.wait_for_timeout(300)
    assert page.calls == []  # att öppna rutan är ingen nedladdning
    page.fill("#gate-email", "test@school.edu")
    page.click(".modal__submit")
    page.wait_for_selector(".modal__success--visible")
    page.click(".modal__success a")
    assert wait_for(page, lambda: page.calls)
    page.wait_for_timeout(300)
    assert page.calls == [{"path": "pdf/prompts/teachers-en",
                           "title": "teachers-en.pdf", "event": True}]


# ── /dl/ för mejllänkar ──

@pytest.mark.parametrize("f", [
    "free/visual-codes-50-en.pdf",
    "/assets/pdfs/free/visual-codes-50-en.pdf",
    "https://choosewise.education/assets/pdfs/free/visual-codes-50-en.pdf",
    "https%3A%2F%2Fchoosewise.education%2Fassets%2Fpdfs%2Ffree%2Fvisual-codes-50-en.pdf",
])
def test_dl_counts_and_opens_the_pdf(page, site, f):
    with page.expect_request("**/assets/pdfs/free/visual-codes-50-en.pdf"):
        page.goto(f"{site}/dl/?f={f}")
    wait_for(page, lambda: page.calls and page.pdf_hits)
    assert page.calls == [{"path": "pdf/free/visual-codes-50-en",
                           "title": "visual-codes-50-en.pdf", "event": True}]
    assert page.pdf_hits == [f"{site}/assets/pdfs/free/visual-codes-50-en.pdf"]


def test_dl_top_level_pdf(page, site):
    with page.expect_request("**/assets/pdfs/nlm-140-prompts-en.pdf"):
        page.goto(f"{site}/dl/?f=nlm-140-prompts-en.pdf")
    wait_for(page, lambda: page.calls)
    assert page.calls == [{"path": "pdf/nlm-140-prompts-en",
                           "title": "nlm-140-prompts-en.pdf", "event": True}]


@pytest.mark.parametrize("f", [
    "https://evil.example/x.pdf",
    "https%3A%2F%2Fevil.example%2Fassets%2Fpdfs%2Fx.pdf",
    "../x.pdf",
    "%2e%2e%2fx.pdf",
    "free/%2e%2e/%2e%2e/x.pdf",
    "%252e%252e%252fx.pdf",
    "//evil.example/x.pdf",
    "free/sub/x.pdf",
    "Free/X.pdf",
    "free/x.pdf.exe",
    "https://choosewise.education/assets/pdfs/free/x.pdf?y=1",
    "javascript:alert(1)//x.pdf",
    "",
])
def test_dl_refuses_anything_else(page, site, f):
    url = f"{site}/dl/?f={f}"
    page.goto(url)
    page.wait_for_selector("#dl-refused:not([hidden])")
    page.wait_for_timeout(1300)  # längre än /dl/:s väntan på GoatCounter
    assert page.url == url
    assert page.pdf_hits == []
    assert page.calls == []
    assert page.locator('#dl-refused a[href="/free/"]').count() >= 1


def test_dl_without_f_refuses(page, site):
    page.goto(f"{site}/dl/")
    page.wait_for_selector("#dl-refused:not([hidden])")
    assert page.pdf_hits == []


def test_dl_still_opens_the_pdf_when_goatcounter_is_blocked(blocked_page, site):
    page = blocked_page
    start = time.time()
    with page.expect_request("**/assets/pdfs/free/visual-codes-50-en.pdf"):
        page.goto(f"{site}/dl/?f=free/visual-codes-50-en.pdf")
    assert time.time() - start < 3
    assert page.errors == []


def test_dl_is_noindex():
    html = (ROOT / "dl/index.html").read_text(encoding="utf-8")
    assert '<meta name="robots" content="noindex">' in html


# ── Fixrunda 1 ──

def test_dl_sends_only_the_pdf_event_no_pageview(page, site):
    """/dl/ är ingen sida att räkna: bara PDF-händelsen ska nå GoatCounter."""
    with page.expect_request("**/assets/pdfs/free/visual-codes-50-en.pdf"):
        page.goto(f"{site}/dl/?f=free/visual-codes-50-en.pdf")
    wait_for(page, lambda: page.calls)
    page.wait_for_timeout(300)
    assert page.pageviews == []
    assert page.calls == [{"path": "pdf/free/visual-codes-50-en",
                           "title": "visual-codes-50-en.pdf", "event": True}]


def test_pageview_path_has_no_query_string(page, site):
    """Spårningsparametrar från mejllänkar får inte följa med in i statistiken."""
    page.goto(f"{site}/free/?ml_subscriber=123&src=yt")
    assert wait_for(page, lambda: page.pageviews)
    assert page.pageviews == ["/free/"]


def test_dl_redirects_even_without_pdf_count(page, site):
    """Blockeras pdf-count.js ska /dl/ ändå öppna PDF:en."""
    page.route("**/assets/js/pdf-count.js", lambda r: r.abort())
    # wait_until="commit": omdirigeringen sker då innan sidan hunnit ladda klart.
    with page.expect_request("**/assets/pdfs/free/visual-codes-50-en.pdf"):
        page.goto(f"{site}/dl/?f=free/visual-codes-50-en.pdf", wait_until="commit")
    assert page.errors == []


def test_dl_fallback_link_points_at_the_pdf(page, site):
    """Reservlänken i väntetexten leder till samma PDF som omdirigeringen."""
    page.route("**/assets/js/pdf-count.js", lambda r: r.fulfill(
        status=200, body="window.cwCountPdf = function () {};"
                         "window.cwCountPdf.settled = function () { return new Promise(function () {}); };",
        headers={"content-type": "text/javascript"}))
    page.goto(f"{site}/dl/?f=free/visual-codes-50-en.pdf")
    assert page.get_attribute("#dl-link", "href") == "/assets/pdfs/free/visual-codes-50-en.pdf"
    assert page.is_visible("#dl-link")
