#!/usr/bin/env python3
# scripts/build-skool-course-covers.py
"""Bygger kursomslagen till Skool-communityts Classroom ur
exports/skool-course-cover-1460x752.html.

Två steg:
  1. Gör numrets typsnitt: Hanken Grotesk Light med kortare flagga på ettan.
     Hankens etta har en flagga som sticker ut tre stambredder åt vänster;
     den kortas till knappt hälften. Siffrorna är lika breda, så 01, 02 och
     10 står likadant i ringen.
  2. Renderar ett omslag per kurs i COURSES till PNG.

Kursstrukturen är preliminär. Ändra listan och kör om skriptet; mappen med
omslag töms först, så den speglar alltid listan.

Rendering kräver en lokal server — file:// ger fallback-typsnitt. Samma
skäl som i build-brand-assets.py.

Kör:  /usr/bin/python3 scripts/build-skool-course-covers.py
"""
from __future__ import annotations

import http.server
import re
import socketserver
import threading
from urllib.parse import urlencode
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SOURCE = "exports/skool-course-cover-1460x752.html"
OUT_DIR = ROOT / "assets/images/brand/skool/courses"
HANKEN = ROOT / "assets/fonts/hanken-grotesk/HankenGrotesk-VariableFont.woff2"
DIGITS = ROOT / "assets/fonts/cover-digits/CoverDigits-Light.woff2"
PORT = 8803

# Nummer, titelns första rad, andra rad (tom = en rad), nivå (tom = ingen).
# Johans kursstruktur 2026-11-11; Research Briefs väntar. Nivån står bara där
# den skiljer kurser med samma titel åt.
# En titel som når in i ringen stoppar bygget — dela den då på två rader.
COURSES = [
    ("01", "Start Here", "", ""),
    ("02", "AI in Teaching", "& Learning", "Basic"),
    ("03", "AI in Teaching", "& Learning", "Intermediate"),
    ("04", "AI in Teaching", "& Learning", "Advanced"),
    ("05", "AI lessons", "for students", "Younger students"),
    ("06", "AI lessons", "for students", "Older students"),
    ("07", "Resource", "Library", ""),
    ("08", "Q&A Replays", "", ""),
    ("09", "YouTube", "Library", ""),
]

TITLE_MAX_RIGHT = 820   # ringen börjar vid x = 842
FLAG_X = 200            # ettans flagga börjar vid x = 117,67 i Hanken


def build_digit_font() -> None:
    font = instantiateVariableFont(TTFont(HANKEN), {"wght": 300})
    glyf = font["glyf"]
    one = glyf["one"]
    outer = [i for i, (x, _) in enumerate(one.coordinates) if abs(x - 117.67) < 0.5]
    assert len(outer) == 2, f"Väntade flaggans två yttre punkter, hittade {len(outer)}"
    for i in outer:
        one.coordinates[i] = (FLAG_X, one.coordinates[i][1])
    one.recalcBounds(glyf)
    font["hmtx"]["one"] = (font["hmtx"]["one"][0], one.xMin)
    # Eget familjenamn, så att filen aldrig förväxlas med sajtens Hanken Grotesk
    for name_id, value in ((1, "Cover Digits"), (4, "Cover Digits Light"),
                           (6, "CoverDigits-Light"), (16, "Cover Digits")):
        font["name"].setName(value, name_id, 3, 1, 0x409)
    font.flavor = "woff2"
    font.recalcTimestamp = False   # samma fil vid varje körning, ingen ny diff i git
    DIGITS.parent.mkdir(parents=True, exist_ok=True)
    font.save(DIGITS)
    print(f"  {DIGITS.relative_to(ROOT)}")


def slug(*parts: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", " ".join(parts).lower()).strip("-")


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


def build_covers() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("*.png"):
        old.unlink()
    httpd = serve()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1460, "height": 752})
            for number, line1, line2, level in COURSES:
                params = {"n": number, "t1": line1, "t2": line2, "lv": level}
                page.goto(f"http://127.0.0.1:{PORT}/{SOURCE}?{urlencode(params)}",
                          wait_until="networkidle")
                page.wait_for_selector("body[data-ready='1']")
                # Vägra skärmdumpa om ett typsnitt saknas — annars blir
                # bilden tyst satt i ett systemtypsnitt.
                for font in ('300 112px "Hanken Grotesk"', '300 280px "Cover Digits"'):
                    if not page.evaluate(f"document.fonts.check('{font}')"):
                        raise RuntimeError(f"Typsnittet laddades inte: {font}")
                right = page.evaluate(
                    "Math.max(...['t1', 't2', 'lv'].map(id => {"
                    " const b = document.getElementById(id).getBBox(); return b.x + b.width; }))")
                if right > TITLE_MAX_RIGHT:
                    raise SystemExit(
                        f"Titeln i kurs {number} når in i ringen (x = {right:.0f}). "
                        f"Dela den på två rader i COURSES.")
                png = OUT_DIR / f"{number}-{slug(line1, line2, level)}.png"
                page.locator("svg#cover").screenshot(path=str(png))
                print(f"  {png.relative_to(ROOT)}")
            browser.close()
    finally:
        httpd.shutdown()
        httpd.server_close()


if __name__ == "__main__":
    build_digit_font()
    build_covers()
