"""Layoutvakter för /study-experiment/ och översiktssidan /study/ i en riktig webbläsare.

På en telefon (390 px) får ingen av sidorna scrolla i sidled, och diagrammets
etiketter och antal ska ligga helt inne i fönstret. De två lektionsrutorna i
"How it works" är lika höga på dator. Bredderna finns först när webbläsaren har
räknat, så det här kan inga statiska tester se.
Spec: docs/superpowers/specs/2026-11-13-study-experiment-design.md.
"""
import functools
import http.server
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PHONE = 390
RECTS = """sel => Array.from(document.querySelectorAll(sel)).map(e => {
  const r = e.getBoundingClientRect();
  return {left: r.left, right: r.right, height: r.height, text: e.textContent.trim()};
})"""


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


def open_page(site, browser, width, path="/study-experiment/"):
    p = browser.new_page(viewport={"width": width, "height": 900})
    p.goto(f"{site}{path}", wait_until="networkidle")
    return p


def fill_results(page):
    """Fyller resultatvyn med så mycket data att alla delar ritas."""
    page.fill("#se-pred-twice", "15")
    page.fill("#se-pred-tested", "7")
    page.fill("#se-pred-same", "3")
    page.fill("#se-scores", "3 5\n4 4\n5 3\n2 6\nabc")


def scroll_width(page):
    return page.evaluate("document.documentElement.scrollWidth")


@pytest.mark.parametrize("path", ["/study-experiment/", "/study/"])
def test_no_horizontal_overflow(site, browser, path):
    p = open_page(site, browser, PHONE, path)
    if path == "/study-experiment/":
        fill_results(p)
    assert scroll_width(p) <= PHONE, (path, scroll_width(p))
    p.close()


def test_chart_labels_inside_viewport(site, browser):
    p = open_page(site, browser, PHONE)
    fill_results(p)
    texts = p.evaluate(RECTS, "#se-chart .se-chart__label, #se-chart .se-chart__count")
    assert len(texts) == 12  # tre rader i två grupper, etikett och antal var
    for t in texts:
        assert t["left"] >= 0 and t["right"] <= PHONE, t
    p.close()


def test_overview_equal_height(site, browser):
    p = open_page(site, browser, 1280)
    boxes = p.evaluate(RECTS, "#se-how .se-glance__box")
    assert len(boxes) == 2
    assert abs(boxes[0]["height"] - boxes[1]["height"]) <= 1, boxes
    p.close()
