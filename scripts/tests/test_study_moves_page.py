"""Layoutvakter för /study-moves/ och översiktssidan /study/ i en riktig webbläsare.

Kort sida vid sida är lika höga per rad, och länkarna står längst ned på
samma linje (Johans regel, specen "Constraints"). På en telefon (390 px)
får ingen av sidorna scrolla i sidled. Bredderna finns först när
webbläsaren har räknat, så det här kan inga statiska tester se.
Spec: docs/superpowers/specs/2026-11-12-study-moves-design.md.
"""
import functools
import http.server
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
WIDTHS = (1280, 820)
BOXES = """sel => Array.from(document.querySelectorAll(sel)).map(e => {
  const r = e.getBoundingClientRect();
  return {top: r.top + window.scrollY, height: r.height};
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


def open_page(site, browser, width, path="/study-moves/"):
    p = browser.new_page(viewport={"width": width, "height": 900})
    p.goto(f"{site}{path}", wait_until="networkidle")
    return p


def rows(boxes):
    """Grupperar rutorna per rad: samma överkant inom 1 px."""
    out = []
    for box in sorted(boxes, key=lambda b: b["top"]):
        if out and abs(out[-1][0]["top"] - box["top"]) <= 1:
            out[-1].append(box)
        else:
            out.append([box])
    return out


def assert_equal_heights(page, selector, width, expected_count):
    boxes = page.evaluate(BOXES, selector)
    assert len(boxes) == expected_count, (selector, width)
    grouped = rows(boxes)
    # Minst en rad med flera kort, annars säger testet ingenting.
    assert any(len(r) > 1 for r in grouped), (selector, width)
    for row in grouped:
        heights = [b["height"] for b in row]
        assert max(heights) - min(heights) <= 1, (selector, width, heights)


def test_cards_equal_height_per_row(site, browser):
    for width in WIDTHS:
        p = open_page(site, browser, width)
        assert_equal_heights(p, "article.sm-move", width, 10)
        assert_equal_heights(p, "#sm-goals .sm-goal", width, 6)
        p.close()


def test_card_links_at_bottom(site, browser):
    for width in WIDTHS:
        p = open_page(site, browser, width)
        cards = p.evaluate(BOXES, "article.sm-move")
        links = p.evaluate(BOXES, "article.sm-move .sm-move__use")
        for row in rows(cards):
            idx = [cards.index(c) for c in row]
            tops = [links[i]["top"] for i in idx]
            assert max(tops) - min(tops) <= 1, (width, tops)
        # Målrutornas draglänkar står också längst ned.
        tiles = p.evaluate(BOXES, "#sm-goals .sm-goal")
        moves = p.evaluate(BOXES, "#sm-goals .sm-goal__moves")
        for row in rows(tiles):
            idx = [tiles.index(t) for t in row]
            bottoms = [moves[i]["top"] + moves[i]["height"] for i in idx]
            assert max(bottoms) - min(bottoms) <= 1, (width, bottoms)
        p.close()


@pytest.mark.parametrize("path", ["/study-moves/", "/study/"])
def test_no_horizontal_overflow(site, browser, path):
    if not (ROOT / path.strip("/") / "index.html").exists():
        pytest.skip(f"{path} finns inte än")
    p = open_page(site, browser, 390, path)
    assert p.evaluate("document.documentElement.scrollWidth") <= 390, path
    if path == "/study-moves/":
        # Även med alla kort öppna.
        p.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
        assert p.evaluate("document.documentElement.scrollWidth") <= 390, path
    p.close()


def test_goal_tiles_link_to_cards(site, browser):
    p = open_page(site, browser, 1280)
    hrefs = p.eval_on_selector_all('#sm-goals a[href^="#"]', "els => els.map(e => e.getAttribute('href'))")
    assert len(hrefs) >= 12
    for href in hrefs:
        assert p.locator(f"[id='{href[1:]}']").count() == 1, href
    p.close()
