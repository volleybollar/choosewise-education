"""Document-level body-text invariant for the 22 guide PDFs.

Why this exists alongside `pdf_fingerprint.py`'s per-page check: that one
fingerprints each PDF *page*, so it is blind to the one failure mode that
matters most for a typeface swap — a page that stops existing because the
new font is more compact. When a page vanishes, its characters don't
disappear, they move onto a neighbouring page's fingerprint, and the
per-page check (correctly) reports "texten ändrad på sida N". It has no
way to tell that apart from a paragraph someone actually deleted — both
look like "the characters on this page changed". Task 6 hit exactly this:
six PDFs went red with moved pages, and distinguishing legitimate
repagination from real loss required rendering the pre-conversion
template by hand and diffing whole-document character multisets outside
any committed test. That manual step is what this module makes permanent.

The idea: strip the running chrome (header/footer brand text, "Page N" /
"Sida N" page numbers, "Page NN / TT" quick-start footers) from every
page, concatenate what's left into ONE string with no page breaks, and
fingerprint that. Repagination cannot move a character out of this
fingerprint's reach, because the fingerprint has no pages for it to move
between. A real deletion is still just as visible as it ever was.

Stripping removes at most ONE occurrence of each known chrome string per
page — the last one, where chrome reliably sits — not every occurrence.
A chrome string is not guaranteed unique to the footer: it can coincide
with real body text (a quick start's own sentence mentioning
"choosewise.education", or a cover's <h1>+subtitle squashing to the exact
same string as the footer title). Removing every occurrence would delete
that body text along with the chrome; removing only the last keeps any
earlier, legitimate occurrence in the fingerprint. See
`_strip_last_occurrence` for the full reasoning and the verification that
chrome is reliably last in reading order across all three mechanisms.

Chrome is read from its own source, not inferred from rendered PDF text:
- Guides whose footer is painted by Playwright's own `footer_template`
  mechanism (build-apple-intelligence-pdf.py, build-copilot-pdf.py,
  build-ai-for-elever-pdf.py, build-gemini-notebooklm-pdf.py): the title/
  page-label strings below are copied verbatim from each script's own
  `jobs` list — see the cited file for each entry in PLAYWRIGHT_FOOTERS.
- Guides whose footer comes from the CSS `@page { @bottom-center {
  content: "..." } }` mechanism (claude, presentation-skills,
  presentationsteknik): the content string is parsed live out of the
  template's own <style> block at test time, so it can never drift from
  the source the way a hand-copied literal could.
- Quick starts, whose footer is a static `.page-footer` div in the body:
  parsed live out of each page's own markup at test time, same reasoning.

This is deliberately still blind to intra-page word reordering (same
known limitation as the per-page check, same reason: pdftotext's
letter-spacing tokenisation makes a stricter ordered comparison noisy
for no benefit). What it adds is immunity to *which page* the surviving
text ends up on.
"""
from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path

from . import pdf_fingerprint as fp

ROOT = fp.ROOT

# ── Playwright `footer_template` guides ────────────────────────────────
# (title, page_label) copied verbatim from each build script's `jobs` list.
PLAYWRIGHT_FOOTERS: dict[str, tuple[str, str]] = {
    # exports/build-apple-intelligence-pdf.py jobs[]
    "_unpublished/assets/pdfs/guides/apple-intelligence-guide-en.pdf":
        ("Apple Intelligence for teachers and school leaders", "Page"),
    "_unpublished/assets/pdfs/guides/apple-intelligence-guide-sv.pdf":
        ("Apple Intelligence för lärare och skolledare", "Sida"),
    # exports/build-copilot-pdf.py jobs[]
    "_unpublished/assets/pdfs/guides/copilot-guide-en.pdf":
        ("Microsoft Copilot for teachers and school leaders", "Page"),
    "_unpublished/assets/pdfs/guides/copilot-guide-sv.pdf":
        ("Microsoft Copilot för lärare och skolledare", "Sida"),
    # exports/build-ai-for-elever-pdf.py jobs[]
    "_unpublished/assets/pdfs/guides/ai-for-elever-sv.pdf":
        ("Ska eleverna använda AI på lektionstid?", "Sida"),
    "_unpublished/assets/pdfs/guides/ai-for-students-en.pdf":
        ("Should students use AI in class?", "Page"),
    # exports/build-gemini-notebooklm-pdf.py jobs[] (footer() calls)
    "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-en.pdf":
        ("Gemini & NotebookLM for teachers and school leaders", "Page"),
    "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-sv.pdf":
        ("Gemini & NotebookLM för lärare och skolledare", "Sida"),
}

# ── CSS `@page { @bottom-center { content: "..." } }` guides ───────────
# Maps PDF -> its own main template. Parsed live, not copied, below.
CSS_FOOTER_TEMPLATES: dict[str, str] = {
    "assets/pdfs/guides/claude-guide-en.pdf": "exports/claude-print-a4-en.html",
    "assets/pdfs/guides/claude-guide-sv.pdf": "exports/claude-print-a4-sv.html",
    "assets/pdfs/presentation-skills-guide-en.pdf": "exports/presentation-skills-print-a4-en.html",
    "assets/pdfs/presentationsteknik-guide-sv.pdf": "exports/presentationsteknik-print-a4-sv.html",
}

# ── `.page-footer` div guides (quick starts) ────────────────────────────
# Each PDF renders from exactly one template; parsed live, below.
PAGE_FOOTER_TEMPLATES: dict[str, str] = {
    "assets/pdfs/guides/claude-quick-start-en.pdf": "exports/claude-quick-start-en.html",
    "assets/pdfs/guides/claude-quick-start-sv.pdf": "exports/claude-quick-start-sv.html",
    "assets/pdfs/presentation-skills-summary-en.pdf": "exports/presentation-skills-quick-start-en.html",
    "assets/pdfs/presentationsteknik-sammanfattning-sv.pdf": "exports/presentationsteknik-quick-start-sv.html",
    "_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-en.pdf": "_unpublished/exports/apple-intelligence-quick-start-en.html",
    "_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf": "_unpublished/exports/apple-intelligence-quick-start-sv.html",
    "_unpublished/assets/pdfs/guides/copilot-quick-start-en.pdf": "_unpublished/exports/copilot-quick-start-en.html",
    "_unpublished/assets/pdfs/guides/copilot-quick-start-sv.pdf": "_unpublished/exports/copilot-quick-start-sv.html",
    "_unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-en.pdf": "_unpublished/exports/gemini-notebooklm-quick-start-en.html",
    "_unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-sv.pdf": "_unpublished/exports/gemini-notebooklm-quick-start-sv.html",
}

# gemini-notebooklm's build script renders its cover with `with_footer=False`
# (see build-gemini-notebooklm-pdf.py) — no footer of any kind on page 1,
# unlike every other Playwright-footer guide, whose cover gets a footer too
# (apple-intelligence/copilot/ai-for-elever/students's `cover_footer()`).
# On that one page, the title string is 100% body text (the cover's own
# <h1>+subtitle, squashed, happens to equal the full title) with no second,
# competing footer occurrence for "last occurrence" to isolate — so it must
# never be treated as chrome there at all, not even as a last-occurrence
# candidate. Found during verification of the Finding 1 fix, by checking
# every Playwright-footer guide's page-0 occurrence count of its own title
# string: six show 2 (body + real footer — safe), these two show 1 (body
# only — unsafe until excluded here).
NO_FOOTER_ON_COVER: set[str] = {
    "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-en.pdf",
    "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-sv.pdf",
}

BASELINE = Path(__file__).parent / "fixtures" / "guide-pdf-body-baseline.json"

_TAG = re.compile(r"<[^>]+>")
_PAGE_NUM = re.compile(r"(Page|Sida)\d+(/\d+)?")


def _squash(text: str) -> str:
    """Whitespace removed entirely — same normalisation the per-page
    fingerprint uses, for the same reason (letter-spaced CSS text tokenises
    unpredictably in pdftotext's output)."""
    return "".join(text.split())


def _css_footer_string(rel_html: str) -> str:
    html = (ROOT / rel_html).read_text(encoding="utf-8")
    m = re.search(r'@bottom-center\s*\{\s*content:\s*"([^"]+)"', html)
    if not m:
        raise ValueError(f"{rel_html}: no @bottom-center content string found")
    return m.group(1)


def _page_footer_strings(rel_html: str) -> list[str]:
    html = (ROOT / rel_html).read_text(encoding="utf-8")
    blocks = re.findall(r'<div class="page-footer">(.*?)</div>', html, re.S)
    if not blocks:
        raise ValueError(f"{rel_html}: no .page-footer divs found")
    return [_TAG.sub("", b) for b in blocks]


def known_chrome_strings(rel_pdf: str) -> list[str]:
    """Every literal chrome string that may appear on a page of this PDF,
    read from its own authoritative source (never inferred from rendered
    PDF text). Page numbers are handled separately, by regex, since they
    vary per page."""
    strings: list[str] = []
    if rel_pdf in PLAYWRIGHT_FOOTERS:
        title, label = PLAYWRIGHT_FOOTERS[rel_pdf]
        strings.append(title)
        # `label` itself ("Page"/"Sida") is covered by _PAGE_NUM below.
    if rel_pdf in CSS_FOOTER_TEMPLATES:
        strings.append(_css_footer_string(CSS_FOOTER_TEMPLATES[rel_pdf]))
    if rel_pdf in PAGE_FOOTER_TEMPLATES:
        # Each page's whole .page-footer block (title + brand + page number,
        # concatenated) is one chrome string — NOT also "choosewise.education"
        # on its own. That standalone addition was the actual source of the
        # over-stripping review found: by the time it ran, the real footer's
        # own "choosewise.education" was already consumed by the full-block
        # match above, so the standalone strip had only the body's legitimate
        # "...the full guide is at choosewise.education." sentence left to
        # remove — and removed it. The full per-page block already contains
        # the brand string in its one real position; nothing else is needed.
        strings.extend(_page_footer_strings(PAGE_FOOTER_TEMPLATES[rel_pdf]))
    return strings


def _strip_last_occurrence(haystack: str, needle: str) -> tuple[str, int]:
    """Remove only the LAST occurrence of `needle` in `haystack`, returning
    (result, removed_length — 0 if `needle` doesn't occur).

    Why last, not "all": a chrome string is not guaranteed to be unique to
    the footer. Two real cases found by review: (1) "choosewise.education"
    is also the literal text of a body sentence in several quick starts
    ("the full guide is at choosewise.education"), on the same page as the
    footer's own brand span; (2) six of the eight Playwright-footer guides
    repeat their cover's own <h1>+subtitle text, squashed, as an exact
    match for the footer title string, on the very page whose footer also
    paints that title. Stripping every occurrence silently deletes real
    body content in both cases.

    Why last is safe: across all three chrome mechanisms (a Playwright
    page-margin box, a CSS @page margin box, and a `.page-footer` div
    pushed down by `margin-top: auto`), the footer is the last thing
    pdftotext extracts for that page — verified against real rendered
    output for all three families, not assumed. Any earlier occurrence of
    the same string is therefore body text and must survive."""
    idx = haystack.rfind(needle)
    if idx == -1:
        return haystack, 0
    return haystack[:idx] + haystack[idx + len(needle):], len(needle)


def _strip_page(squashed_page: str, chrome: list[str]) -> tuple[str, int]:
    """Strip at most one occurrence of each known chrome string from one
    page's squashed text (the last one, if present), plus every page-number
    token. Returns (result, total_characters_removed)."""
    removed = 0
    for c in chrome:
        squashed_page, n = _strip_last_occurrence(squashed_page, c)
        removed += n
    page_num_matches = _PAGE_NUM.findall(squashed_page)
    if page_num_matches:
        # findall with groups returns tuples; re-match the whole span instead.
        total_num_len = sum(len(m.group(0)) for m in _PAGE_NUM.finditer(squashed_page))
        squashed_page = _PAGE_NUM.sub("", squashed_page)
        removed += total_num_len
    return squashed_page, removed


def body_text_fingerprint(pdf: Path, rel_pdf: str) -> str:
    """One fingerprint for the whole document's body text, chrome and page
    numbers stripped, pages concatenated so repagination cannot move a
    character out of its reach."""
    whole, _ = _stripped_whole_text_and_removed(pdf, rel_pdf)
    counts = Counter(whole)
    canonical = "".join(f"{ch}{counts[ch]}" for ch in sorted(counts))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _stripped_whole_text_and_removed(pdf: Path, rel_pdf: str) -> tuple[str, int]:
    chrome = [_squash(s) for s in known_chrome_strings(rel_pdf)]
    cover_title = None
    if rel_pdf in NO_FOOTER_ON_COVER and rel_pdf in PLAYWRIGHT_FOOTERS:
        cover_title = _squash(PLAYWRIGHT_FOOTERS[rel_pdf][0])
    whole = ""
    total_removed = 0
    for page_index, page in enumerate(fp.pages(fp.extract(pdf))):
        squashed = _squash(page)
        page_chrome = chrome
        if cover_title is not None and page_index == 0:
            # No footer renders on this PDF's cover — the title string here
            # is body text only, never chrome, so exclude it before stripping.
            page_chrome = [c for c in chrome if c != cover_title]
        squashed, removed = _strip_page(squashed, page_chrome)
        whole += squashed
        total_removed += removed
    return whole, total_removed


def capture(rel_pdf: str) -> str:
    return body_text_fingerprint(ROOT / rel_pdf, rel_pdf)
