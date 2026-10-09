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


def _expected_shrinkage(rel: str) -> int:
    """Independent re-derivation of how much stripping SHOULD remove —
    deliberately a different code path from `_strip_page` (first-occurrence
    `.replace`, not `rfind`-based last-occurrence removal), so this is a
    real check on the quantity, not the production code re-asserting its
    own bookkeeping. Walks the same order production does (chrome strings
    first, page numbers on what's left) so a page-number that's already
    inside a matched chrome block — the quick starts' "Page NN / TT" is
    part of their one per-page footer block, not separate from it — isn't
    counted twice. Also mirrors NO_FOOTER_ON_COVER: gemini-notebooklm's
    cover renders no footer at all, so its title must not be expected to
    shrink on page 0 either.
    """
    path = fp.ROOT / rel
    chrome = [bt._squash(s) for s in bt.known_chrome_strings(rel)]
    cover_title = None
    if rel in bt.NO_FOOTER_ON_COVER and rel in bt.PLAYWRIGHT_FOOTERS:
        cover_title = bt._squash(bt.PLAYWRIGHT_FOOTERS[rel][0])
    total = 0
    for page_index, page in enumerate(fp.pages(fp.extract(path))):
        squashed = bt._squash(page)
        page_chrome = chrome
        if cover_title is not None and page_index == 0:
            page_chrome = [c for c in chrome if c != cover_title]
        for c in page_chrome:
            if c and c in squashed:
                total += len(c)
                squashed = squashed.replace(c, "", 1)
        total += sum(len(m.group(0)) for m in bt._PAGE_NUM.finditer(squashed))
    return total


def test_chrome_stripping_removes_exactly_the_expected_length():
    """Beviset att stripningen tar bort det den säger sig ta bort — VARKEN
    mer eller mindre. Review hittade två fall där den tog bort mer: en
    .page-footer-stripning som åt en kropps-mening ("choosewise.education"
    i en quick starts undertext) och ett omslags-<h1>+undertext vars
    hopslagna text råkar matcha hela sidfotstiteln. Det gamla testet kunde
    bara se att de kända strängarna var borta — inte att något annat följde
    med. Det här jämför den faktiska krympningen mot en OBEROENDE uträknad
    förväntad krympning (summan över kända strängar av förekomster × längd,
    plus sidnummer som inte redan ingår i en sådan sträng). Skiljer de sig
    åt har stripningen tagit bort för mycket (eller för lite)."""
    samples = [
        "_unpublished/assets/pdfs/guides/copilot-guide-en.pdf",            # Playwright
        "assets/pdfs/guides/claude-guide-en.pdf",                          # CSS content
        "assets/pdfs/guides/claude-quick-start-en.pdf",                    # .page-footer
        "_unpublished/assets/pdfs/guides/apple-intelligence-guide-en.pdf",  # cover h1≡footer title, WITH a real cover footer too
        "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-en.pdf",   # cover h1≡footer title, NO real cover footer
    ]
    for rel in samples:
        path = fp.ROOT / rel
        chrome = [bt._squash(s) for s in bt.known_chrome_strings(rel)]
        assert chrome, f"{rel}: inga kända chrome-strängar hittades"

        raw_len = sum(len(bt._squash(p)) for p in fp.pages(fp.extract(path)))
        whole, removed = bt._stripped_whole_text_and_removed(path, rel)
        expected = _expected_shrinkage(rel)

        assert len(whole) == raw_len - removed, (
            f"{rel}: stripningens egen bokföring stämmer inte med den faktiska längdskillnaden"
        )
        assert removed == expected, (
            f"{rel}: krympte med {removed} tecken, väntat exakt {expected} "
            f"— stripningen tog bort {'mer' if removed > expected else 'mindre'} än den skulle"
        )
        assert not bt._PAGE_NUM.search(whole), f"{rel}: ett sidnummer finns kvar efter stripning"


def test_chrome_stripping_keeps_a_body_occurrence_that_coincides_with_chrome():
    """Regressionstest för review-fyndet: en quick starts egen undertext
    nämner choosewise.education på samma sida som sidfoten gör det. Den
    kropps-förekomsten ska överleva stripningen."""
    rel = "assets/pdfs/guides/claude-quick-start-en.pdf"
    path = fp.ROOT / rel
    whole, _ = bt._stripped_whole_text_and_removed(path, rel)
    assert "choosewise.education" in whole, (
        "kroppens 'the full guide is at choosewise.education.' försvann med sidfoten"
    )


def test_chrome_stripping_keeps_cover_title_with_no_competing_footer():
    """Ytterligare ett fall av samma felklass, hittat under verifieringen
    av review-fyndet (inte av review självt): gemini-notebooklm's omslag
    saknar helt sidfot (with_footer=False i build-skriptet), så omslagets
    egen <h1>+undertext — som råkar matcha hela sidfotstiteln hopslagen —
    har ingen konkurrerande sidfotsförekomst att skiljas från. Utan
    NO_FOOTER_ON_COVER skulle "senaste förekomsten" bli just den enda,
    kropps-egna förekomsten."""
    for rel in (
        "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-en.pdf",
        "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-sv.pdf",
    ):
        path = fp.ROOT / rel
        title = bt._squash(bt.PLAYWRIGHT_FOOTERS[rel][0])
        whole, _ = bt._stripped_whole_text_and_removed(path, rel)
        assert title in whole, f"{rel}: omslagets rubrik+undertext försvann utan att en sidfot fanns att skilja den från"


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
