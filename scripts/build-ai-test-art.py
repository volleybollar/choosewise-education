#!/usr/bin/env python3
"""Ritar illustrationen till AI-eller-människa-blocket på de två startsidorna.

Varför ett skript och inte handritad SVG: allt som ligger PÅ glasrutan måste
följa dess vridning, och rutan är en trapets. Varje punkt räknas fram genom
att mappa in en enhetsruta i trapetsen med bilinjär interpolation. Bara
bildrutnätet är nio fyrhörningar med fyra hörn vardera — 36 koordinater som
alla måste ligga i samma plan. De går inte att flytta för hand.

Skriptet skriver in figuren i index.html och sv/index.html, mellan taggarna
<svg class="ai-test__art"> och </svg>. Det är idempotent: en körning utan
ändrade värden lämnar `git diff` tom. Ändra geometrin här, kör, och granska
diffen — rör aldrig koordinaterna i HTML-filerna.

Körs utan argument från repo-roten:  python3 scripts/build-ai-test-art.py
"""
from __future__ import annotations

import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ("index.html", "sv/index.html")

# Glasrutans fyra hörn. Kanten närmast betraktaren (vänster) är kort, kanten
# längst bort (höger) är lång — rutan öppnar sig alltså bort från henne.
TL, TR = (210, 118), (420, 70)
BL, BR = (210, 272), (420, 300)

# Bildytan är beskuren till det som faktiskt är ritat. Tomrum här blir till
# ren höjd på sidan, eftersom SVG:n skalar efter spaltbredden.
VIEWBOX = "0 56 450 284"

INDENT = " " * 10


def P(u: float, v: float) -> tuple[float, float]:
    """Enhetskvadraten (u,v) → en punkt i trapetsen."""
    top = ((1 - u) * TL[0] + u * TR[0], (1 - u) * TL[1] + u * TR[1])
    bot = ((1 - u) * BL[0] + u * BR[0], (1 - u) * BL[1] + u * BR[1])
    return (round((1 - v) * top[0] + v * bot[0], 1),
            round((1 - v) * top[1] + v * bot[1], 1))


def pts(seq) -> str:
    return " ".join(f"{x},{y}" for x, y in seq)


def quad(u0: float, v0: float, u1: float, v1: float) -> str:
    return pts([P(u0, v0), P(u1, v0), P(u1, v1), P(u0, v1)])


def line(u0: float, u1: float, v: float) -> str:
    a, b = P(u0, v), P(u1, v)
    return f"M {a[0]} {a[1]} L {b[0]} {b[1]}"


def ring(cu: float, cv: float, ru: float, rv: float, n: int = 28) -> str:
    """En cirkel på rutan blir en ellips i planet — ritas som månghörning."""
    return pts([P(cu + ru * math.cos(2 * math.pi * i / n),
                  cv + rv * math.sin(2 * math.pi * i / n)) for i in range(n)])


def render() -> str:
    text_lines = " ".join([line(0.10, 0.88, 0.13),
                           line(0.10, 0.88, 0.20),
                           line(0.10, 0.62, 0.27)])
    cells = "\n".join(
        f"{INDENT}    <polygon points=\""
        f"{quad(0.10 + i * 0.13, 0.38 + j * 0.14, 0.10 + i * 0.13 + 0.11, 0.38 + j * 0.14 + 0.12)}\"/>"
        for j in range(3) for i in range(3))
    play_ring = ring(0.72, 0.58, 0.135, 0.17)
    play_tri = pts([P(0.675, 0.49), P(0.80, 0.58), P(0.675, 0.67)])
    sheen = f"M {P(0.12, 0.84)[0]} {P(0.12, 0.84)[1]} L {P(0.62, 0.08)[0]} {P(0.62, 0.08)[1]}"

    return f"""<svg class="ai-test__art" viewBox="{VIEWBOX}" role="img" aria-hidden="true">
{INDENT}  <!-- Scenen ses från sidan. Betraktaren står till vänster, i profil mot
{INDENT}       glasrutan. Rutan är en trapets vars korta kant vetter mot henne
{INDENT}       och långa kant bort, och de tre testerna — texterna, de nio
{INDENT}       bilderna, filmen — ligger på rutan och följer dess vridning.
{INDENT}       Varje punkt på rutan är räknad genom att mappa in en enhetsruta i
{INDENT}       trapetsen, därav de till synes godtyckliga decimalerna. Ska något
{INDENT}       på skärmen flyttas måste hela figuren räknas om — ändra inte en
{INDENT}       enskild koordinat för hand, den hamnar ur plan.
{INDENT}       Byggs av scripts/build-ai-test-art.py. -->

{INDENT}  <polygon points="{pts([TL, TR, BR, BL])}"
{INDENT}           fill="var(--color-bg)" fill-opacity="0.76"
{INDENT}           stroke="var(--color-border-strong)" stroke-width="2"/>
{INDENT}  <path d="{sheen}" stroke="var(--color-bg)" stroke-width="12"
{INDENT}        stroke-opacity="0.5" fill="none" stroke-linecap="round"/>

{INDENT}  <!-- Test 1: texterna -->
{INDENT}  <path d="{text_lines}" stroke="var(--color-highlight)" stroke-width="3"
{INDENT}        stroke-linecap="round" fill="none"/>
{INDENT}  <!-- Test 2: de nio bilderna -->
{INDENT}  <g stroke="var(--color-highlight)" stroke-width="2" fill="none">
{cells}
{INDENT}  </g>
{INDENT}  <!-- Test 3: filmerna -->
{INDENT}  <g stroke="var(--color-highlight)" stroke-width="2" fill="none">
{INDENT}    <polygon points="{play_ring}"/>
{INDENT}    <polygon points="{play_tri}"/>
{INDENT}  </g>

{INDENT}  <!-- Betraktaren, i profil mot rutan och beskuren av bildens nederkant. -->
{INDENT}  <g stroke="var(--color-accent)" stroke-width="2" fill="none">
{INDENT}    <path d="M 18 340 C 18 156, 126 156, 120 340"/>
{INDENT}    <circle cx="72" cy="165" r="34" fill="var(--color-bg)"/>
{INDENT}    <path d="M 104 161 L 114 168 L 104 175"/>
{INDENT}  </g>
{INDENT}</svg>"""


BLOCK = re.compile(r'<svg class="ai-test__art".*?</svg>', re.S)


def main() -> None:
    art = render()
    for rel in PAGES:
        path = ROOT / rel
        before = path.read_text(encoding="utf-8")
        if not BLOCK.search(before):
            raise SystemExit(f"{rel}: hittade ingen <svg class=\"ai-test__art\"> att ersätta")
        after = BLOCK.sub(lambda _: art, before, count=1)
        if after == before:
            print(f"oförändrad: {rel}")
            continue
        path.write_text(after, encoding="utf-8")
        print(f"uppdaterad: {rel}")


if __name__ == "__main__":
    main()
