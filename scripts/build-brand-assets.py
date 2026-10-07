#!/usr/bin/env python3
# scripts/build-brand-assets.py
"""Genererar varje varumärkestillgång ur de två källfilerna.

Varför ett skript: specen kräver att favicon, Skool-logga, omslag och
LinkedIn-tillgångar kommer ur SAMMA teckning. Handarbete glömmer det
förr eller senare; ett skript som läser källan kan inte.

Rendering kräver en lokal server — file:// ger fallback-typsnitt och fel
radbrytning. Samma skäl som i render-og-pngs.py.

Kör:  /usr/bin/python3 scripts/build-brand-assets.py
"""
from __future__ import annotations

import http.server
import re
import socketserver
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "assets/images/brand"
PORT = 8801

BLUE = "#0B3A6F"
CREAM = "#FBFAF8"
COPPER_DK = "#E8C9A8"

# Märkets element plockas UT ur källfilen, aldrig skrivna på nytt här.
# Skriver man dem två gånger har man två sanningar.
_INNER = re.compile(r"<svg[^>]*>(.*)</svg>", re.S)


def mark_markup(state: str) -> str:
    """state: 'dark' eller 'light'."""
    src = BRAND / f"mark-on-{state}.svg"
    body = _INNER.search(src.read_text(encoding="utf-8")).group(1)
    # Kommentarer ur källan följer inte med in i genererade filer.
    return re.sub(r"<!--.*?-->", "", body, flags=re.S).strip()


def tile_svg(size: int, radius_pct: float = 22.0, state: str = "dark") -> str:
    """Märket på varumärkesblå botten med rundade hörn.

    Botten är inte dekoration: en transparent favicon försvinner mot
    mörkt flikgränssnitt.
    """
    r = size * radius_pct / 100
    inner = size * 0.62          # märket upptar 62 % av rutan
    off = (size - inner) / 2     # frizonen runt om
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 {size} {size}">'
        f'<rect width="{size}" height="{size}" rx="{r:.2f}" fill="{BLUE}"/>'
        f'<svg x="{off:.2f}" y="{off:.2f}" width="{inner:.2f}" height="{inner:.2f}" '
        f'viewBox="0 0 64 64">{mark_markup(state)}</svg>'
        f'</svg>'
    )


def serve() -> socketserver.TCPServer:
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(
        *a, directory=str(ROOT), **kw)
    try:
        httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    except OSError as exc:
        raise SystemExit(
            f"Kunde inte binda 127.0.0.1:{PORT} ({exc}). Troligen en kvarglömd "
            f"server — kör `lsof -i :{PORT}`, avsluta processen, eller ändra PORT.")
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def render_png(page, svg_text: str, w: int, h: int, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    page.set_viewport_size({"width": w, "height": h})
    page.set_content(
        f'<body style="margin:0">{svg_text}</body>',
        wait_until="load")
    page.wait_for_timeout(220)   # typsnittet ska hinna in innan bilden tas
    page.screenshot(path=str(out), omit_background=True)


def build_favicons(page) -> None:
    """Tre filer: SVG för moderna webbläsare, .ico för äldre, PNG för hemskärm."""
    (ROOT / "favicon.svg").write_text(tile_svg(64), encoding="utf-8")

    render_png(page, tile_svg(180), 180, 180, ROOT / "apple-touch-icon.png")

    # .ico ska innehålla BÅDE 16 och 32. Utelämnas sizes skriver Pillow en
    # enda bild, och äldre webbläsare skalar då 32 ned till 16 själva med
    # dåligt resultat.
    render_png(page, tile_svg(32), 32, 32, ROOT / "_ico32.png")
    img = Image.open(ROOT / "_ico32.png").convert("RGBA")
    img.save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32)])
    (ROOT / "_ico32.png").unlink()


def card_svg(w: int, h: int, mark_size: int, mark_x: int, mark_y: int,
             title: str | None, subtitle: str | None,
             title_pt: int, sub_pt: int, text_x: int,
             title_y: int, sub_y: int, band: int) -> str:
    """Mörkt kort med märket, rubrik, underrubrik och kopparbandet nederst.

    Bandet är samma band som sajtens footer. Det är det som binder
    Skool och LinkedIn till sajten visuellt.
    """
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}">',
        '<style>@font-face{font-family:"Hanken Grotesk";'
        'src:url("/assets/fonts/hanken-grotesk/HankenGrotesk-VariableFont.woff2") '
        'format("woff2");font-weight:300 600}</style>',
        f'<rect width="{w}" height="{h}" fill="{BLUE}"/>',
        f'<rect y="{h - band}" width="{w}" height="{band}" fill="#C2793A"/>',
        f'<svg x="{mark_x}" y="{mark_y}" width="{mark_size}" height="{mark_size}" '
        f'viewBox="0 0 64 64">{mark_markup("dark")}</svg>',
    ]
    if title:
        parts.append(
            f'<text x="{text_x}" y="{title_y}" font-family="Hanken Grotesk, sans-serif" '
            f'font-size="{title_pt}" font-weight="300" fill="{CREAM}" '
            f'letter-spacing="-2">{title}</text>')
    if subtitle:
        parts.append(
            f'<text x="{text_x}" y="{sub_y}" font-family="Hanken Grotesk, sans-serif" '
            f'font-size="{sub_pt}" font-weight="400" fill="{COPPER_DK}" '
            f'letter-spacing="1.6">{subtitle}</text>')
    parts.append("</svg>")
    return "".join(parts)


TITLE = "Choosewise"
SUBTITLE = "AI &amp; EdTech for Educators"


def build_skool(page) -> None:
    out = BRAND / "skool"
    render_png(page, tile_svg(1024, radius_pct=0), 1024, 1024, out / "logo.png")
    cover = card_svg(1400, 790, 168, 112, 150, TITLE, SUBTITLE,
                     104, 42, 112, 438, 512, 24)
    (out / "cover.svg").write_text(cover, encoding="utf-8")
    render_png(page, cover, 1400, 790, out / "cover.png")


def build_linkedin(page) -> None:
    out = BRAND / "linkedin"
    render_png(page, tile_svg(300, radius_pct=0), 300, 300, out / "page-logo.png")

    page_banner = card_svg(1128, 191, 88, 56, 46, TITLE, SUBTITLE,
                           46, 21, 176, 94, 130, 8)
    (out / "page-banner.svg").write_text(page_banner, encoding="utf-8")
    render_png(page, page_banner, 1128, 191, out / "page-banner.png")

    # Den personliga bannern: LinkedIn lägger profilbilden över vänstra
    # delen, så märket och texten börjar längre in än på sidbannern.
    personal = card_svg(1584, 396, 120, 90, 138, TITLE, SUBTITLE,
                        62, 28, 248, 196, 246, 12)
    (out / "personal-banner.svg").write_text(personal, encoding="utf-8")
    render_png(page, personal, 1584, 396, out / "personal-banner.png")


def main() -> None:
    with sync_playwright() as pw:
        httpd = serve()
        browser = pw.chromium.launch()
        page = browser.new_page(device_scale_factor=1)
        try:
            # set_content ärver det aktuella dokumentets ursprung. Utan den
            # här navigeringen är sidan about:blank och absoluta sökvägar
            # (t.ex. typsnitt) kan inte slå upp mot servern.
            page.goto(f"http://127.0.0.1:{PORT}/")
            build_favicons(page)
            build_skool(page)
            build_linkedin(page)
        finally:
            browser.close()
            httpd.shutdown()


if __name__ == "__main__":
    main()
