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
BRAND_DIR = ROOT / "assets/images/brand"
OG_DIR = BRAND_DIR / "og"
OG_DEFAULT = BRAND_DIR / "og-default.svg"
PORT = 8799

# Måste matcha @font-face-källan i build-og-images.py (och i og-default.svg,
# som är handskriven). Om vägen någonsin ändras där, ändra den här med.
FONT_SUFFIX = "fonts/hanken-grotesk/HankenGrotesk-VariableFont.woff2"


def serve() -> socketserver.TCPServer:
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(
        *a, directory=str(ROOT), **kw
    )
    try:
        httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    except OSError as exc:
        raise SystemExit(
            f"Kunde inte binda 127.0.0.1:{PORT} ({exc}). Troligen en "
            f"kvarglömd server från en tidigare körning av det här skriptet — "
            f"kör `lsof -i :{PORT}` för att hitta processen och avsluta den, "
            f"eller ändra PORT i render-og-pngs.py."
        ) from exc
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def render_one(page, svg: Path) -> None:
    """Rendera en SVG till PNG — men vägra skärmdumpa om det självhostade
    typsnittet inte faktiskt laddades. Utan den här kontrollen skulle ett
    brutet typsnitt-path (eller en borttagen @font-face) tyst falla tillbaka
    till ett systemtypsnitt och skriptet skulle ändå rapportera framgång —
    precis det osynliga felet det här skriptet finns för att stänga."""
    font_response: dict[str, object] = {"seen": False, "ok": False, "status": None}

    def on_response(resp):
        if resp.url.endswith(FONT_SUFFIX):
            font_response["seen"] = True
            font_response["ok"] = resp.ok
            font_response["status"] = resp.status

    page.on("response", on_response)
    rel = svg.relative_to(ROOT)
    page.goto(f"http://127.0.0.1:{PORT}/{rel}", wait_until="networkidle")
    page.wait_for_timeout(300)  # låt typsnitten sätta sig
    page.remove_listener("response", on_response)

    if not font_response["seen"] or not font_response["ok"]:
        raise RuntimeError(
            f"Hanken Grotesk laddades inte för {svg.relative_to(ROOT)} — "
            f"väntade en lyckad begäran till .../{FONT_SUFFIX}, "
            f"fick seen={font_response['seen']} status={font_response['status']}. "
            f"Kontrollera @font-face src i filen (eller i TEMPLATE om det är "
            f"ett genererat kort). Vägrar skärmdumpa ett kort som tyst skulle "
            f"falla tillbaka till ett systemtypsnitt."
        )

    out = svg.with_suffix(".png")
    page.screenshot(path=str(out))
    print(f"renderade {out.relative_to(ROOT)}")


def main() -> None:
    httpd = serve()
    svgs = sorted(OG_DIR.glob("*.svg"))
    if OG_DEFAULT.exists():
        svgs.append(OG_DEFAULT)
    if not svgs:
        raise SystemExit("Inga SVG-filer i assets/images/brand/og/")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1200, "height": 630}, device_scale_factor=1
        )
        for svg in svgs:
            render_one(page, svg)
        browser.close()

    httpd.shutdown()


if __name__ == "__main__":
    main()
