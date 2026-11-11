#!/usr/bin/env python3
# scripts/build-skool-promo.py
"""Bygger säljbilden för Skool-communityt ur exports/skool-community-1920x1080.html.

Två steg:
  1. Renderar framsidan på de tre guiderna som visas i bilden ur PDF:erna,
     så att omslagen följer med när en guide uppdateras.
  2. Renderar källfilens två versioner till PNG, plus WebP till sajten.

Rendering kräver en lokal server — file:// ger fallback-typsnitt. Samma
skäl som i build-brand-assets.py.

Kör:  /usr/bin/python3 scripts/build-skool-promo.py
"""
from __future__ import annotations

import http.server
import socketserver
import subprocess
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SKOOL = ROOT / "assets/images/brand/skool"
SOURCE = "exports/skool-community-1920x1080.html"
PORT = 8802

# Guiderna i bilden. Alla tre finns bara i Skool, inte på sajten.
COVERS = {
    "gemini-notebook-guide-en": ROOT / "_unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf",
    "visual-codes-200-en": ROOT.parent / "visual-codes-pdf/build/visual-codes-200-en.pdf",
    "ai-for-students-en": ROOT / "_unpublished/assets/pdfs/guides/ai-for-students-en.pdf",
}

# version i källfilen -> filnamn
VERSIONS = {"web": "community-web", "about": "community-about"}


def build_covers() -> None:
    """Första sidan i varje PDF som PNG, 900 px på längden."""
    out_dir = SKOOL / "covers"
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, pdf in COVERS.items():
        subprocess.run(
            ["pdftoppm", "-f", "1", "-l", "1", "-png", "-singlefile",
             "-scale-to", "900", str(pdf), str(out_dir / name)],
            check=True)


class _Server(socketserver.TCPServer):
    # Annars är porten upptagen en stund efter en avbruten körning
    allow_reuse_address = True


def serve() -> socketserver.TCPServer:
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(
        *a, directory=str(ROOT), **kw)
    try:
        httpd = _Server(("127.0.0.1", PORT), handler)
    except OSError as exc:
        raise SystemExit(
            f"Kunde inte binda 127.0.0.1:{PORT} ({exc}). Troligen en kvarglömd "
            f"server — kör `lsof -i :{PORT}`, avsluta processen, eller ändra PORT.")
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def build_images() -> None:
    httpd = serve()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1920, "height": 1080})
            for version, name in VERSIONS.items():
                page.goto(f"http://127.0.0.1:{PORT}/{SOURCE}?v={version}",
                          wait_until="networkidle")
                # Ladda typsnitten uttryckligen och vägra skärmdumpa om något
                # saknas — annars blir bilden tyst satt i ett systemtypsnitt.
                for font in ('600 30px "Hanken Grotesk"', '88px "Instrument Serif"',
                             'italic 48px "Instrument Serif"'):
                    page.evaluate(f"document.fonts.load('{font}')")
                    if not page.evaluate(f"document.fonts.check('{font}')"):
                        raise RuntimeError(f"Typsnittet laddades inte: {font}")
                png = SKOOL / f"{name}.png"
                page.screenshot(path=str(png))
                print(f"  {png.relative_to(ROOT)}")
            browser.close()
    finally:
        httpd.shutdown()
        httpd.server_close()

    # Sajten får WebP (samma kvalitet som scripts/optimize-image.py)
    web_png = SKOOL / f"{VERSIONS['web']}.png"
    Image.open(web_png).save(web_png.with_suffix(".webp"), "WEBP", quality=82, method=6)
    print(f"  {web_png.with_suffix('.webp').relative_to(ROOT)}")


if __name__ == "__main__":
    build_covers()
    build_images()
