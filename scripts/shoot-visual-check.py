#!/usr/bin/env python3
"""Skärmbilder av tolv representativa sidor i tre bredder, båda språken.

Körs mot en lokal server på ny port — cachen ljuger annars.

En fast wait_for_timeout(600) höll inte: startsidans hero tonar in över
~3s (se assets/css/pages.css), och data-reveal/lazy-laddat innehåll på de
flesta andra sidorna hinner inte rendera på 600ms heller — resultatet var
36 "granskade" bilder där de flesta var till stora delar tomma. settle()
nedan ersätter gissningen med riktiga villkor: en scroll genom hela sidan
(utlöser lazy-bilder och JS-populerade grids), tillbaka till toppen, och
en poll på startsidans hero-text i stället för att gissa hur länge den tar.

prefers-reduced-motion övervägdes (sajten respekterar den redan) men
testades bort: den tar bort GSAP-pinningen på wise-sidans signaturdiagram
helt, vilket får alla fyra panelerna att visas samtidigt, överlappande,
på desktop/tablet-bredd — läsbart kaos i stället för en ren bild. Den
riktiga scrollningen ger en enda, ren (om något godtycklig) panel, vilket
är det bästa en statisk skärmbild kan göra med en scroll-skrubbad
animation.
"""
from __future__ import annotations

import http.server
import socketserver
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(
    "/Users/johan/Projekt/Choosewise/choosewise-education/"
    ".superpowers/sdd/2026-10-05-visual-identity-wave-1/task-10-screenshots"
)
PORT = 8870

PAGES = [
    ("", "home-en"), ("sv/", "home-sv"),
    ("wise/", "wise-en"), ("sv/ratt/", "wise-sv"),
    ("prompts/", "prompts-en"), ("sv/promptar/", "prompts-sv"),
    ("prompts/teachers/", "pack-en"), ("sv/promptar/larare/", "pack-sv"),
    ("guides/claude/", "guide-en"), ("sv/guider/claude/", "guide-sv"),
    ("evidence/", "evidence-en"), ("visual-codes/", "visualcodes-en"),
]
WIDTHS = [(390, "phone"), (834, "tablet"), (1440, "desktop")]

# Hero-text-fade (home-en/home-sv only): assets/css/pages.css delays
# .hero__content's children up to animation-delay 3.0s + 1s duration.
HERO_SETTLED = """() => {
    const els = document.querySelectorAll('.hero__content > *');
    if (els.length === 0) return true;  // not the homepage — nothing to wait for
    return Array.from(els).every(el => getComputedStyle(el).opacity === '1');
}"""


def settle(page) -> None:
    """Replace a guessed sleep with real conditions: scroll through the
    page once (triggers data-reveal fades, lazy images, JS-populated
    grids), return to the top, then poll the one animation this site
    deliberately delays instead of guessing how long it takes."""
    page.wait_for_load_state("networkidle")
    height = page.evaluate("document.body.scrollHeight")
    y = 0
    while y < height:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(150)
        y += 700
        height = page.evaluate("document.body.scrollHeight")  # content can grow as it loads
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_load_state("networkidle")
    try:
        page.wait_for_function(HERO_SETTLED, timeout=6000)
    except Exception:
        pass  # better a late/odd frame than a crashed run
    page.wait_for_timeout(200)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(
        *a, directory=str(ROOT), **kw
    )
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for width, wname in WIDTHS:
            page = browser.new_page(viewport={"width": width, "height": 1000})
            for path, name in PAGES:
                page.goto(f"http://127.0.0.1:{PORT}/{path}", wait_until="networkidle")
                settle(page)
                page.screenshot(path=str(OUT / f"{name}-{wname}.png"), full_page=True)
                print(f"{name}-{wname}")
            page.close()
        browser.close()
    httpd.shutdown()


if __name__ == "__main__":
    main()
