"""Typsnitten ska vara självhostade. Inga anrop till Google."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brandguard import ROOT, published_files  # noqa: E402

EXPECTED_FONT_FILES = [
    "assets/fonts/hanken-grotesk/HankenGrotesk-VariableFont.woff2",
    "assets/fonts/instrument-serif/InstrumentSerif-Regular.woff2",
    "assets/fonts/instrument-serif/InstrumentSerif-Italic.woff2",
]


@pytest.mark.parametrize("rel", EXPECTED_FONT_FILES)
def test_font_file_is_self_hosted(rel):
    path = ROOT / rel
    assert path.exists(), f"{rel} saknas"
    assert path.stat().st_size > 10_000, f"{rel} ser trunkerad ut"


def test_fontface_declares_both_families():
    css = (ROOT / "assets/css/fonts.css").read_text(encoding="utf-8")
    assert "Hanken Grotesk" in css
    assert "Instrument Serif" in css
    assert "Fraunces" not in css
    assert "Work Sans" not in css


def test_hanken_covers_the_weights_we_use():
    css = (ROOT / "assets/css/fonts.css").read_text(encoding="utf-8")
    assert "font-weight: 300 600" in css


def test_no_published_file_calls_google_fonts():
    offenders = []
    for path in published_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "fonts.googleapis.com" in text or "fonts.gstatic.com" in text:
            offenders.append(str(path.relative_to(ROOT)))
    assert offenders == [], f"Hämtar typsnitt från Google: {offenders}"


def test_published_files_excludes_untracked_files():
    """Vakten ska spegla vad GitHub Pages serverar — bara spårade filer.
    research-presentation.html är gitignorerad och får inte scannas."""
    names = {p.name for p in published_files()}
    assert "research-presentation.html" not in names


# Guidernas webbytor ligger under guides/ respektive _unpublished/guides/.
# published_files() utesluter HELA _unpublished/ (se brandguard.py), och
# guide_templates() täcker bara _unpublished/exports/*.html — alltså
# tryckmallarna, inte webbsidorna. Guidernas webbytor har därför aldrig
# haft någon typsnittsvakt, och det är precis därför både Copilots och
# Geminis sidor kunde ligga med Google Fonts.
#
# Listan är de guider vars webbyta ÄR städad och ska förbli det. Apples
# alla fyra sökvägar (EN och SV) står nu här efter den rundan.
# ai-for-students' ENGELSKA webbyta städades i den här rundans Task 12 och
# står nu här också. Det enda som saknas är ai-for-students' SVENSKA
# webbyta (_unpublished/sv/guider/ai-for-elever/) — den är fryst med
# avsikt (Johans beslut 2026-10-14, samma runda) och tas inte upp här.
# Copilots och Geminis SVENSKA webbytor (_unpublished/sv/guider/copilot/,
# _unpublished/sv/guider/gemini-notebooklm/) bär också kvar typsnitten
# och är fortsatt skuld — de står utanför den här listan för att de inte
# är guide-webbytor under _unpublished/guides/, inte för att de är
# städade. En glob över alla guider vore röd för dem från dag ett och
# därmed en vakt någon slår av.
GUIDE_WEB_SURFACES = (
    "guides/claude/index.html",
    "guides/claude/styles.css",
    "_unpublished/guides/copilot/index.html",
    "_unpublished/guides/copilot/styles.css",
    "_unpublished/guides/gemini-notebook/index.html",
    "_unpublished/guides/gemini-notebook/styles.css",
    # Apple är den första guiden vars SVENSKA webbyta också står här.
    # Frysningen av de svenska ytorna gäller prosan, inte CSS-hygienen:
    # ett typsnittsbyte ändrar noll tecken normaliserad text och syns
    # därför inte i ytkonsistensvakten. Copilots och Geminis svenska
    # ytor bär kvar sina Crestiora-typsnitt och är fortsatt skuld.
    "_unpublished/guides/apple-intelligence/index.html",
    "_unpublished/guides/apple-intelligence/styles.css",
    "_unpublished/sv/guider/apple-intelligence/index.html",
    "_unpublished/sv/guider/apple-intelligence/styles.css",
    "_unpublished/guides/ai-for-students/index.html",
    "_unpublished/guides/ai-for-students/styles.css",
)

# Crestioras två typsnitt. 'Inter' söks med citattecken och som
# attributvärde: ordet "inter" förekommer i vanlig engelska ("interact",
# "interface") och en bar delsträngsökning vore brus.
_CRESTIORA_FONTS = (
    "Playfair",
    "'Inter'",
    '"Inter"',
    'font-family="Inter',
    "fonts.googleapis.com",
    "fonts.gstatic.com",
)


@pytest.mark.parametrize("rel", GUIDE_WEB_SURFACES)
def test_the_guide_web_surfaces_have_no_crestiora_fonts(rel):
    """Granskningsfokus 4: ett inline-`font-family`-attribut i en SVG
    vinner över varje token i `tokens.css` och syns inte i någon
    CSS-vakt. Gemini-guidens sida bar sjutton sådana (sex Playfair, elva
    Inter) utöver de tre `<link>`-raderna och de tre `--font-*`-
    överskrivningarna — tas bara raderna bort står diagrammens text kvar
    i Crestiora-typsnitt och ingenting blir rött.
    """
    text = (ROOT / rel).read_text(encoding="utf-8")
    found = [needle for needle in _CRESTIORA_FONTS if needle in text]
    assert found == [], f"{rel} bär kvar: {found}"
