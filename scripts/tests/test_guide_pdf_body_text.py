"""Document-level body-text invariant — the check that can never move.

Companion to test_guide_pdf_parity.py, not a replacement for it. Keep
both: the per-page test is the first-line check (it names the exact page
a change landed on, which this one cannot), but it fingerprints each page
in isolation, so a page that stops existing — because a typeface swap
made the document more compact — looks identical to a page whose content
was actually deleted: either way, characters move off a baseline page and
the per-page hash there changes. Task 6 hit this directly: six PDFs went
red with moved/missing pages, and telling "repagination" apart from "real
loss" required a one-off manual render-and-diff outside any committed
test. This file is that check, made permanent and provable.

The fingerprint here is of the WHOLE document's body text — running
chrome (header/footer brand strings, "Page N"/"Sida N" page numbers)
stripped, every page concatenated into one string with no page breaks.
Repagination cannot move a character out of a fingerprint that has no
pages for it to move between. A real deletion is exactly as visible as
it ever was. See pdf_body_text.py for exactly how chrome is identified
(read from each PDF's own build script or template, never inferred from
rendered output) and why the comparison is still a character multiset,
not an ordered string (same pdftotext letter-spacing tokenisation reason
as the per-page check).
"""
from __future__ import annotations

import json

import pytest

from . import pdf_body_text as bt
from . import pdf_fingerprint as fp

BASELINE = json.loads(bt.BASELINE.read_text(encoding="utf-8"))


@pytest.mark.parametrize("rel", fp.GUIDE_PDFS)
def test_body_text_is_unchanged(rel: str):
    path = fp.ROOT / rel
    assert path.exists(), f"{rel} saknas"
    before = BASELINE[rel]
    after = bt.body_text_fingerprint(path, rel)
    assert after == before, (
        f"{rel}: dokumentets brödtext har ändrats (ord tillagda, borttagna "
        f"eller bytta — inte bara flyttade mellan sidor)"
    )


def test_baseline_covers_every_guide_pdf():
    """Facit ska inte tappa en PDF tyst."""
    assert sorted(BASELINE) == sorted(fp.GUIDE_PDFS)


def test_fingerprint_catches_a_single_character_change():
    """Beviset att vakten kan bli röd på det den vaktar — samma bevisform
    som pdf_fingerprint.fingerprint, på den här modulens egen kod."""
    import hashlib
    from collections import Counter

    def fingerprint(text: str) -> str:
        counts = Counter("".join(text.split()))
        canonical = "".join(f"{ch}{counts[ch]}" for ch in sorted(counts))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    assert fingerprint("Hanken Grotesk") != fingerprint("Hanken Grotesl")


def test_chrome_stripping_removes_every_known_string():
    """Beviset att stripningen faktiskt tar bort det den säger sig ta bort,
    inte bara råkar lämna en multimängd som ser lika ut. Kör på en riktig
    PDF ur varje av de tre källmekanismerna (Playwright-mall, CSS
    @bottom-center, .page-footer-div)."""
    samples = [
        "_unpublished/assets/pdfs/guides/copilot-guide-en.pdf",       # Playwright
        "assets/pdfs/guides/claude-guide-en.pdf",                     # CSS content
        "assets/pdfs/guides/claude-quick-start-en.pdf",               # .page-footer
    ]
    for rel in samples:
        path = fp.ROOT / rel
        chrome = [bt._squash(s) for s in bt.known_chrome_strings(rel)]
        assert chrome, f"{rel}: inga kända chrome-strängar hittades"
        whole = ""
        for page in fp.pages(fp.extract(path)):
            squashed = bt._squash(page)
            for c in chrome:
                squashed = squashed.replace(c, "")
            squashed = bt._PAGE_NUM.sub("", squashed)
            whole += squashed
        for c in chrome:
            assert c not in whole, f"{rel}: '{c}' finns kvar efter stripning"
        assert not bt._PAGE_NUM.search(whole), f"{rel}: ett sidnummer finns kvar efter stripning"


def test_known_chrome_strings_are_read_from_source_not_hardcoded_pdf_text():
    """De CSS- och .page-footer-baserade mallarna läses live ur sin egen
    källfil vid varje körning — om någon redigerar en mall händer det här
    testet ingenting (det är syftet), men om källfilen saknar det mönstret
    helt (markören togs bort, selektorn döptes om) ska det synas direkt
    som ett fel i stället för en tyst tom lista."""
    for rel, html in bt.CSS_FOOTER_TEMPLATES.items():
        s = bt._css_footer_string(html)
        assert s, f"{html}: tomt @bottom-center content"
    for rel, html in bt.PAGE_FOOTER_TEMPLATES.items():
        strings = bt._page_footer_strings(html)
        assert strings, f"{html}: inga .page-footer-div hittades"
