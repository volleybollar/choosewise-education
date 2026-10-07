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


# Märkets eget 64-rutnät (spec §2): nålen sträcker sig y=6..58, dvs 52 av
# 64 enheter. Frizonen är 11 enheter (en nålbredd, spec §2 "Frizon"). Att
# rymma nålen PLUS en frizon på båda sidor inom rutan ger den skala märket
# ska ritas i: (52 + 2*11) enheter ska få plats på 64, så skalan är
# 64 / 74 — inte en lös decimal, utan de två mått specen faktiskt anger.
_MARK_NEEDLE_SPAN = 58 - 6        # y=6 till y=58 i märkets eget rutnät
_MARK_CLEAR_ZONE = 11             # spec §2: en nålbredd runt om
_MARK_INNER_FRACTION = 64 / (_MARK_NEEDLE_SPAN + 2 * _MARK_CLEAR_ZONE)  # ≈0.865


def tile_svg(size: int, radius_pct: float = 22.0, state: str = "dark") -> str:
    """Märket på varumärkesblå botten med rundade hörn.

    Botten är inte dekoration: en transparent favicon försvinner mot
    mörkt flikgränssnitt.
    """
    r = size * radius_pct / 100
    inner = size * _MARK_INNER_FRACTION  # märket fyller rutan minus frizonen, se konstanterna ovan
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


# Måste matcha @font-face-källan i card_svg() (och i render-og-pngs.py,
# som vaktar samma väg för de 12 og-korten).
FONT_SUFFIX = "fonts/hanken-grotesk/HankenGrotesk-VariableFont.woff2"


def render_png(page, svg_text: str, w: int, h: int, out: Path,
                omit_background: bool = True, svg_path: Path | None = None) -> None:
    """Rendera en SVG till PNG.

    De tre korten från card_svg() deklarerar ett @font-face mot det
    självhostade typsnittet. Som render-og-pngs.py: vägra skärmdumpa
    förrän en lyckad begäran mot typsnittet faktiskt observerats — en
    bar wait_for_timeout gissar en tid och kan tyst falla tillbaka till
    ett systemtypsnitt utan att skriptet märker det.

    Ett font-bärande kort navigeras till (page.goto mot `svg_path`,
    precis som render-og-pngs.py) i stället för set_content: inom SAMMA
    sida ger set_content ingen ny nätverksbegäran för ett typsnitt som
    redan hämtats tidigare i körningen — Blinks typsnittscache fyller i
    tyst utan att gå via nätverksstacken, så lyssnaren aldrig ser en
    händelse (bekräftat genom att testa båda vägarna). En riktig
    navigering hämtar om varje gång och gör lyssnaren pålitlig. Rena
    märkesplattor (favicon, Skool-logga, LinkedIn page-logo) har ingen
    @font-face och väntar därför inte alls.
    """
    out.parent.mkdir(parents=True, exist_ok=True)
    page.set_viewport_size({"width": w, "height": h})

    needs_font = FONT_SUFFIX in svg_text
    font_response: dict[str, object] = {"seen": False, "ok": False, "status": None}

    def on_response(resp):
        if resp.url.endswith(FONT_SUFFIX):
            font_response["seen"] = True
            font_response["ok"] = resp.ok
            font_response["status"] = resp.status

    if needs_font:
        assert svg_path is not None, (
            f"{out.name} har ett @font-face men fick ingen svg_path att "
            f"navigera till")
        page.on("response", on_response)
        rel = svg_path.relative_to(ROOT)
        page.goto(f"http://127.0.0.1:{PORT}/{rel}", wait_until="networkidle")
        page.wait_for_timeout(300)  # låt typsnittet sätta sig
        page.remove_listener("response", on_response)
        if not font_response["seen"] or not font_response["ok"]:
            raise RuntimeError(
                f"Hanken Grotesk laddades inte för {out.relative_to(ROOT)} — "
                f"väntade en lyckad begäran till .../{FONT_SUFFIX}, fick "
                f"seen={font_response['seen']} status={font_response['status']}. "
                f"Vägrar skärmdumpa ett kort som tyst skulle falla tillbaka "
                f"till ett systemtypsnitt.")
    else:
        page.set_content(
            f'<body style="margin:0">{svg_text}</body>',
            wait_until="load")

    page.screenshot(path=str(out), omit_background=omit_background)

    if needs_font:
        # En navigering till en fristående SVG-fil gör dokumentet till ett
        # SVG-dokument, inte ett HTML-dokument — nästa anrops set_content()
        # (för en ren märkesplatta utan typsnitt) skulle annars misslyckas
        # med "Only HTML documents support open()". Gå tillbaka till
        # serverroten, som är HTML, innan sidan återanvänds.
        page.goto(f"http://127.0.0.1:{PORT}/")


def build_favicons(page) -> None:
    """Tre filer: SVG för moderna webbläsare, .ico för äldre, PNG för hemskärm."""
    (ROOT / "favicon.svg").write_text(tile_svg(64), encoding="utf-8")

    # apple-touch-icon.png är INTE samma tillskärning som favicon.svg/.ico:
    # iOS lägger sin egen squircle-mask ovanpå och komponerar genomskinlighet
    # mot SVART, så en rundad, transparent platta får mörka hörn på
    # hemskärmen. Plattan är därför fyrkantig (radius 0) och helt opak —
    # ingen botten att vara transparent mot.
    render_png(page, tile_svg(180, radius_pct=0), 180, 180,
               ROOT / "apple-touch-icon.png", omit_background=False)

    # .ico ska bära BÅDA 16 och 32 som sanna renderingar, inte 32 nedskalad
    # till 16 (vilket raderar skärpan just i de storlekar märket används
    # mest). Pillow matchar varje begärd storlek i `sizes` mot en bild av
    # exakt den storleken bland basbilden + append_images, och skalar bara
    # om ingen av dem passar — därför renderas båda separat och ges in.
    # OBS: `sizes=` ensamt skyddar inte mot allt. Den här kombinationen
    # fångar ett explicit fel enstorleks-anrop (t.ex. `sizes=[(32, 32)]`),
    # men inte att kwargen tappas bort helt — utelämnas `sizes` fyller
    # Pillow själv i sin egen lista (16/24/32/48/64/128/256) genom att
    # skala om basbilden, och bland de storlekarna finns både 16 och 32.
    render_png(page, tile_svg(16), 16, 16, ROOT / "_ico16.png")
    render_png(page, tile_svg(32), 32, 32, ROOT / "_ico32.png")
    img16 = Image.open(ROOT / "_ico16.png").convert("RGBA")
    img32 = Image.open(ROOT / "_ico32.png").convert("RGBA")
    img32.save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32)],
               append_images=[img16])
    (ROOT / "_ico16.png").unlink()
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
    cover = card_svg(
        w=1400, h=790, mark_size=168, mark_x=112, mark_y=150,
        title=TITLE, subtitle=SUBTITLE,
        title_pt=104, sub_pt=42, text_x=112,
        title_y=438, sub_y=512, band=24,
    )
    cover_svg_path = out / "cover.svg"
    cover_svg_path.write_text(cover, encoding="utf-8")
    render_png(page, cover, 1400, 790, out / "cover.png", svg_path=cover_svg_path)


def build_linkedin(page) -> None:
    out = BRAND / "linkedin"
    render_png(page, tile_svg(300, radius_pct=0), 300, 300, out / "page-logo.png")

    page_banner = card_svg(
        w=1128, h=191, mark_size=88, mark_x=56, mark_y=46,
        title=TITLE, subtitle=SUBTITLE,
        title_pt=46, sub_pt=21, text_x=176,
        title_y=94, sub_y=130, band=8,
    )
    page_banner_svg_path = out / "page-banner.svg"
    page_banner_svg_path.write_text(page_banner, encoding="utf-8")
    render_png(page, page_banner, 1128, 191, out / "page-banner.png",
               svg_path=page_banner_svg_path)

    # Den personliga bannern: specen (§3) kräver att vänstra tredjedelen
    # (0–528 av 1584) hålls fri från märke OCH text, eftersom LinkedIn
    # lägger profilbilden där — till skillnad från sidbannern ovan, som
    # inte har någon avatar att ta hänsyn till. Märket börjar vid x=560
    # (35,4 %) och texten vid x=712 (45 %), båda efter 528-gränsen.
    personal = card_svg(
        w=1584, h=396, mark_size=120, mark_x=560, mark_y=138,
        title=TITLE, subtitle=SUBTITLE,
        title_pt=62, sub_pt=28, text_x=712,
        title_y=196, sub_y=246, band=12,
    )
    personal_svg_path = out / "personal-banner.svg"
    personal_svg_path.write_text(personal, encoding="utf-8")
    render_png(page, personal, 1584, 396, out / "personal-banner.png",
               svg_path=personal_svg_path)


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
