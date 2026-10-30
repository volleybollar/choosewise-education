"""Gemensamma fixturer för webbläsartesterna av Two-Minute Debrief.

En lokal server för sajtens rot och en Chromium via Playwright. Importeras
av test_two_minute_debrief_builder.py, _saved.py och _rollup.py.
"""
import functools
import http.server
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
URL = "/two-minute-debrief/"


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


def open_page(site, browser, init_script=None, **kw):
    ctx = browser.new_context(**kw)
    if init_script:
        ctx.add_init_script(init_script)
    p = ctx.new_page()
    p.goto(f"{site}{URL}", wait_until="networkidle")
    p.wait_for_function("window.TwoMinuteDebrief !== undefined", timeout=5000)
    return p


@pytest.fixture
def page(site, browser):
    p = open_page(site, browser)
    yield p
    p.context.close()


def fill(page, group="8B maths", grade="8", goal="Solve two-step equations.",
         evidence="11 of 27 divided before subtracting.", surprise="", next_="Word problems, Thursday."):
    page.fill("#td-group", group)
    page.select_option("#td-grade", grade)
    page.fill("#td-goal", goal)
    page.fill("#td-evidence", evidence)
    page.fill("#td-surprise", surprise)
    page.fill("#td-next", next_)
