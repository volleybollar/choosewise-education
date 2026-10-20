#!/usr/bin/env python3
"""Regenerate the A4 PDF for "AI or human?" (EN, printable text + image tests).

Dark cover AND dark back cover, so a three-pass render:
  - Cover (page 1): white footer with the title only, no page number.
  - Pages 2..n-1: standard grey footer with title + page number.
  - Back cover (page n): no footer, the licence line sits in the page itself.
Then merged into a single PDF via pypdf.
"""
import os
import tempfile
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from playwright.sync_api import sync_playwright

root = Path(__file__).parent.parent

SRC = root / "_unpublished/exports/ai-or-human-print-a4-en.html"
DST = root / "assets/pdfs/free/ai-or-human-en.pdf"
TITLE = "AI or human?"
PAGE_LABEL = "Page"


def cover_footer(title: str) -> str:
    """Footer for the dark cover. Colour mirrors --color-dark-text (#EFF2F6);
    print-color-adjust: exact for the same reason as build-ai-for-elever-pdf.py."""
    return f"""
<div style="font-size: 8pt; color: #EFF2F6; width: 100%; padding: 0 16mm 0 16mm;
            display: flex; justify-content: flex-start; align-items: center;
            -webkit-print-color-adjust: exact; print-color-adjust: exact;
            font-family: 'Hanken Grotesk', Helvetica, sans-serif;">
  <span>{title}</span>
</div>
"""


def standard_footer(title: str, page_label: str) -> str:
    """Footer for content pages. Colour mirrors --color-text-muted (#656F7B)."""
    return f"""
<div style="font-size: 8pt; color: #656F7B; width: 100%; padding: 0 16mm 0 16mm;
            display: flex; justify-content: space-between; align-items: center;
            -webkit-print-color-adjust: exact; print-color-adjust: exact;
            font-family: 'Hanken Grotesk', Helvetica, sans-serif;">
  <span>{title}</span>
  <span>{page_label} <span class="pageNumber"></span></span>
</div>
"""


EMPTY = "<div></div>"

PDF_KW = dict(
    format="A4",
    print_background=True,
    margin={"top": "0", "bottom": "14mm", "left": "0", "right": "0"},
    prefer_css_page_size=True,
    display_header_footer=True,
    header_template=EMPTY,
)


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    print(f"Building {DST.name} from {SRC.name}")
    page.goto(SRC.as_uri(), wait_until="networkidle")
    page.emulate_media(media="print")

    tmps = [tempfile.NamedTemporaryFile(suffix=".pdf", delete=False).name for _ in range(4)]
    full, cover, rest, back = tmps
    try:
        # A footer-less full render tells us the page count, so the
        # middle and back-cover ranges can be expressed exactly.
        page.pdf(path=full, footer_template=EMPTY, **PDF_KW)
        n = len(PdfReader(full).pages)

        page.pdf(path=cover, footer_template=cover_footer(TITLE), page_ranges="1", **PDF_KW)
        page.pdf(path=rest, footer_template=standard_footer(TITLE, PAGE_LABEL),
                 page_ranges=f"2-{n - 1}", **PDF_KW)
        page.pdf(path=back, footer_template=EMPTY, page_ranges=str(n), **PDF_KW)

        writer = PdfWriter()
        for part in (cover, rest, back):
            writer.append(part)
        writer.add_metadata({"/Title": TITLE, "/Author": "Johan Lindström"})
        DST.parent.mkdir(parents=True, exist_ok=True)
        with open(DST, "wb") as f:
            writer.write(f)
        writer.close()
        print(f"  -> {n} pages, {DST.stat().st_size // 1024} KB")
    finally:
        for tmp in tmps:
            if os.path.exists(tmp):
                os.unlink(tmp)

    browser.close()

print("Done.")
