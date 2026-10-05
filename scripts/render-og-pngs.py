#!/usr/bin/env python3
"""Rendera varje og-SVG till PNG i 1200×630.

Gjordes tidigare för hand i webbläsare. Det glömdes bort, och felet
syns först när någon delar en länk på LinkedIn. Nu är det ett kommando.

Kräver en lokal server så att självhostade typsnitt laddas — file://
ger fallback-snitt och fel radbrytning.
"""
from __future__ import annotations

import http.server
import socketserver
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OG_DIR = ROOT / "assets/images/brand/og"
PORT = 8799


def serve() -> socketserver.TCPServer:
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(
        *a, directory=str(ROOT), **kw
    )
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def main() -> None:
    httpd = serve()
    svgs = sorted(OG_DIR.glob("*.svg"))
    if not svgs:
        raise SystemExit("Inga SVG-filer i assets/images/brand/og/")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1200, "height": 630}, device_scale_factor=1
        )
        for svg in svgs:
            rel = svg.relative_to(ROOT)
            page.goto(f"http://127.0.0.1:{PORT}/{rel}", wait_until="networkidle")
            page.wait_for_timeout(300)  # låt typsnitten sätta sig
            out = svg.with_suffix(".png")
            page.screenshot(path=str(out))
            print(f"renderade {out.relative_to(ROOT)}")
        browser.close()

    httpd.shutdown()


if __name__ == "__main__":
    main()
