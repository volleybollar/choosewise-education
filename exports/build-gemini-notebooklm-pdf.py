#!/usr/bin/env python3
"""Regenerate Gemini & NotebookLM (EN + SV) A4 guide PDFs from the print HTML sources.

The CSS @page rule reserves 16mm at the bottom of every page for a running
footer, so content cannot overlap it. Playwright renders in two passes:

  1. Page 1 (the cover) with display_header_footer=False — no footer drawn.
  2. Pages 2+ with the running footer template — footer painted in the
     CSS-reserved 16mm margin box.

Then pypdf stitches the two slices into the final PDF.

Why two passes? Chrome's print engine does not always honour
`@page :first { margin: 0 }` as a way to suppress a Playwright-injected
header/footer on page 1, even if the CSS margin is explicitly zero. The
two-pass approach is a guaranteed workaround.

EN build is the canonical deliverable. SV source may not exist yet; if
missing we skip rather than fail — same pattern as the Claude builds.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import pypdf

root = Path(__file__).parent.parent


def footer(title: str, page_label: str) -> str:
    return f"""
<div style="font-size: 8pt; color: #a5a59f; width: 100%; padding: 0 22mm;
            display: flex; justify-content: space-between; align-items: center;
            font-family: 'Inter', -apple-system, sans-serif;">
  <span>{title}</span>
  <span>{page_label} <span class="pageNumber"></span></span>
</div>
"""


EMPTY_HEADER = "<div></div>"

jobs = [
    (
        root / "exports/gemini-notebooklm-print-a4-en.html",
        root / "assets/pdfs/guides/gemini-notebooklm-guide-en.pdf",
        footer("Gemini &amp; NotebookLM for teachers and school leaders", "Page"),
    ),
    (
        root / "exports/gemini-notebooklm-print-a4-sv.html",
        root / "assets/pdfs/guides/gemini-notebooklm-guide-sv.pdf",
        footer("Gemini &amp; NotebookLM för lärare och skolledare", "Sida"),
    ),
]


def render(page, src_uri: str, dst: Path, *, page_ranges: str, with_footer: bool,
           footer_template: str) -> None:
    """Render a slice of the document with or without the running footer."""
    page.goto(src_uri, wait_until="networkidle")
    page.emulate_media(media="print")
    pdf_kwargs = dict(
        path=str(dst),
        format="A4",
        print_background=True,
        margin={"top": "0", "bottom": "16mm", "left": "0", "right": "0"},
        prefer_css_page_size=True,
        page_ranges=page_ranges,
    )
    if with_footer:
        pdf_kwargs["display_header_footer"] = True
        pdf_kwargs["header_template"] = EMPTY_HEADER
        pdf_kwargs["footer_template"] = footer_template
    page.pdf(**pdf_kwargs)


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    for src, dst, footer_template in jobs:
        if not src.exists():
            print(f"Skipping {dst.name} — source {src.name} not found")
            continue

        uri = src.as_uri()
        print(f"Building {dst.name} from {src.name}")

        cover_tmp = src.with_suffix(".cover.tmp.pdf")
        rest_tmp = src.with_suffix(".rest.tmp.pdf")

        render(page, uri, cover_tmp, page_ranges="1",
               with_footer=False, footer_template=footer_template)
        render(page, uri, rest_tmp, page_ranges="2-",
               with_footer=True, footer_template=footer_template)

        writer = pypdf.PdfWriter()
        for pg in pypdf.PdfReader(str(cover_tmp)).pages:
            writer.add_page(pg)
        for pg in pypdf.PdfReader(str(rest_tmp)).pages:
            writer.add_page(pg)

        dst.parent.mkdir(parents=True, exist_ok=True)
        with open(dst, "wb") as fh:
            writer.write(fh)

        cover_tmp.unlink(missing_ok=True)
        rest_tmp.unlink(missing_ok=True)

        pages = len(pypdf.PdfReader(str(dst)).pages)
        print(f"  -> {dst.name}: {pages} pages, {dst.stat().st_size // 1024} KB")

    browser.close()

print("Done.")
