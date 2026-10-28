"""Vakter för översiktssidan Think + AI (/think/), menyvalet och SEO-posterna.

Översiktssidan visar bara verktyg som finns. Kommande verktyg nämns inte vid
namn (Johans beslut 2026-10-27). Flawed Answer, Side by Side och Thinking Profile fick sina kort 2026-10-28.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HUB = ROOT / "think/index.html"
HEADER = ROOT / "assets/partials/header-en.html"
UNANNOUNCED = ["Sparring Partner"]


def test_hub_links_thinking_profile():
    html = HUB.read_text(encoding="utf-8")
    cards = re.findall(r'<a class="think-card"[^>]*href="([^"]+)"', html)
    assert cards == ["/thinking-moves/", "/flawed-answer/", "/side-by-side/", "/thinking-profile/"]
    assert "a whole unit" in html
    assert "More tools are on the way." in html


def test_hub_mentions_more_tools_without_names():
    html = HUB.read_text(encoding="utf-8")
    assert "More tools" in html
    for name in UNANNOUNCED:
        assert name not in html, name


def test_menu_link_after_gap_tracer():
    lines = HEADER.read_text(encoding="utf-8").splitlines()
    gap = next(i for i, l in enumerate(lines) if 'href="/gap-tracer/"' in l)
    assert 'href="/think/"' in lines[gap + 1] and ">Think + AI<" in lines[gap + 1]


def test_og_images_absolute():
    for page, png in (("think/index.html", "think-en.png"), ("thinking-moves/index.html", "thinkingmoves-en.png"),
                      ("flawed-answer/index.html", "flawedanswer-en.png"),
                      ("side-by-side/index.html", "sidebyside-en.png"),
                      ("thinking-profile/index.html", "thinkingprofile-en.png")):
        html = (ROOT / page).read_text(encoding="utf-8")
        m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        assert m and m.group(1) == f"https://choosewise.education/assets/images/brand/og/{png}", page
        assert (ROOT / "assets/images/brand/og" / png).exists(), png


def test_llms_lists_flawed_answer():
    text = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "https://choosewise.education/flawed-answer/" in text


def test_llms_lists_side_by_side():
    text = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "https://choosewise.education/side-by-side/" in text


def test_llms_lists_thinking_profile():
    text = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "https://choosewise.education/thinking-profile/" in text


def test_hub_cards_equal_height():
    """Fyra kort sida vid sida är lika höga per rad (Johans regel)."""
    import functools, http.server, socketserver, threading
    from playwright.sync_api import sync_playwright
    # Sidan använder rotrelativa länkar (/assets/...), så den måste serveras.
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    handler.log_message = lambda *a, **k: None
    server = socketserver.TCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"http://127.0.0.1:{server.server_address[1]}/think/")
        for width in (1280, 900):
            page.set_viewport_size({"width": width, "height": 900})
            boxes = page.eval_on_selector_all(
                ".think-card", "els => els.map(e => { const r = e.getBoundingClientRect(); return [Math.round(r.top), Math.round(r.height)]; })")
            assert len(boxes) == 4
            rows = {}
            for top, h in boxes:
                rows.setdefault(top, set()).add(h)
            assert all(len(hs) == 1 for hs in rows.values()), (width, boxes)
        browser.close()
    server.shutdown()


def test_llms_lists_both_pages():
    text = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "https://choosewise.education/think/" in text
    assert "https://choosewise.education/thinking-moves/" in text
