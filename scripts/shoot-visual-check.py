#!/usr/bin/env python3
"""Skärmbilder av tolv representativa sidor i tre bredder, båda språken.

Körs mot en lokal server på ny port — cachen ljuger annars.
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
PORT = 8847

PAGES = [
    ("", "home-en"), ("sv/", "home-sv"),
    ("wise/", "wise-en"), ("sv/ratt/", "wise-sv"),
    ("prompts/", "prompts-en"), ("sv/promptar/", "prompts-sv"),
    ("prompts/teachers/", "pack-en"), ("sv/promptar/larare/", "pack-sv"),
    ("guides/claude/", "guide-en"), ("sv/guider/claude/", "guide-sv"),
    ("evidence/", "evidence-en"), ("visual-codes/", "visualcodes-en"),
]
WIDTHS = [(390, "phone"), (834, "tablet"), (1440, "desktop")]


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
                page.wait_for_timeout(600)
                page.screenshot(path=str(OUT / f"{name}-{wname}.png"), full_page=True)
                print(f"{name}-{wname}")
            page.close()
        browser.close()
    httpd.shutdown()


if __name__ == "__main__":
    main()
