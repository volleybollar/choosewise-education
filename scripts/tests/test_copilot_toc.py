"""Innehållsförteckningens sidnummer mot den renderade PDF:en.

Våg 2b:s dyraste fel: 13 av 15 hårdkodade sidnummer i Claude-guidens
förteckning var fel, och ingen vakt såg det — texten granskades sexton
gånger utan att någon öppnade dokumentet. Copilots förteckning bär sex
nummer i klassen `toc__page`, och ett av dem (FAQ:n) var fel innan den
här rundan började.

Vakten läser numren ur mallen och letar upp varje avsnitts faktiska
startsida i den renderade PDF:en. Ankarsträngarna är valda ur
`pdftotext`-utskriften, inte ur HTML:en: extraktionen spärrar versaler
oförutsägbart, så en spärrad etikett vore ett ankare som aldrig matchar.
Sökningen börjar på sidan efter förteckningen själv — annars matchar
varje ankare förteckningens egen rad.
"""
from __future__ import annotations

import re

import pytest

from . import pdf_fingerprint as fp
from . import surfacecheck

TEMPLATE = "_unpublished/exports/copilot-print-a4-en.html"
PDF = "_unpublished/assets/pdfs/guides/copilot-guide-en.pdf"
TOC_PAGE = 2  # förteckningen står själv på sidan 2 och räknas inte som träff

# Förteckningens rubrik (som den står i `toc__title`, före eventuell
# `toc__sub`) -> en sträng som står på den sida avsnittet BÖRJAR på och
# ingen tidigare sida. Nycklarna är lästa ur mallen 2026-10-09 och
# normaliseras med surfacecheck.normalise, så `&amp;` jämförs som `&`.
#
# Två av ankarna i den ursprungliga listan visade sig vara stale eller
# tvetydiga vid kontroll mot steg 1:s pdftotext-utskrift och byttes:
#   - Part 3: "What CDP actually gives you" förekommer inte i PDF:en
#     alls (Task 6 skrev om Part 3 och texten säger "EDP", inte "CDP").
#   - About this guide: "the entire compliance story" förekommer ÄVEN
#     på sidan 3 (den inledande meningen "...is the entire compliance
#     story for Copilot...") och skulle ha matchat fel sida. Bytt mot
#     citatets attribution, som bara finns på sida 25.
ANCHORS = {
    "Why this guide exists": "Why this guide exists",
    "Part 1 · Get started": "Which product are you actually using?",
    "Part 2 · Work smarter": "Copilot Chat (with your work data)",
    "Part 3 · Compliance & licensing": "What EDP actually gives you",
    "FAQ": "Questions teachers ask",
    "About this guide": "Johan Lindström, October 2026",
}

_TOC_ROW = re.compile(
    r'<span class="toc__title">(?P<title>.*?)(?:<span class="toc__sub">.*?</span>)?'
    r'\s*</span>.*?<span class="toc__page">(?P<page>\d+)</span>',
    re.S)


def toc_rows() -> list:
    """surfacecheck.normalise gör entiteterna till tecken, så nyckeln
    `Part 3 · Compliance & licensing` matchar markupens `&amp;`."""
    html = (fp.ROOT / TEMPLATE).read_text(encoding="utf-8")
    return [(surfacecheck.normalise(re.sub(r"<[^>]+>", " ", m.group("title"))),
             int(m.group("page")))
            for m in _TOC_ROW.finditer(html)]


def test_the_toc_has_the_six_rows_we_think_it_has():
    """Går regexen sönder blir listan tom, och en tom parametrisering är
    en grön vakt som vaktar ingenting."""
    rows = toc_rows()
    assert len(rows) == 6, rows
    assert [title for title, _ in rows] == list(ANCHORS), rows


@pytest.mark.parametrize("title", list(ANCHORS))
def test_every_toc_page_number_matches_the_rendered_pdf(title):
    claimed = dict(toc_rows())[title]
    anchor = surfacecheck.normalise(ANCHORS[title])
    pages = [surfacecheck.normalise(page)
             for page in fp.pages(fp.extract(fp.ROOT / PDF))]
    actual = next((i + 1 for i, page in enumerate(pages)
                   if i + 1 > TOC_PAGE and anchor in page), None)
    assert actual is not None, (
        f"ankaret {anchor!r} står inte på någon sida efter {TOC_PAGE} — "
        "välj ett ankare ur pdftotext-utskriften, inte ur HTML:en")
    assert actual == claimed, (
        f"{title!r}: förteckningen säger {claimed}, avsnittet börjar på {actual}")
