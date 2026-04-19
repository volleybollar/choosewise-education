#!/usr/bin/env python3
"""Append a CC BY-NC-SA 4.0 license page to the existing Claude guide PDFs.

The premium Claude full-guide PDFs (claude-guide-en.pdf, claude-guide-sv.pdf)
do not have editable source HTML in this repo. Rather than try to recreate the
layout from scratch, this script renders a standalone license page via
Playwright and appends it as a new final page using pypdf. The original
premium layout is preserved verbatim.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import pypdf

root = Path(__file__).parent.parent

jobs = [
    (
        root / "exports/claude-guide-license-en.html",
        root / "assets/pdfs/guides/claude-guide-en.pdf",
    ),
    (
        root / "exports/claude-guide-license-sv.html",
        root / "assets/pdfs/guides/claude-guide-sv.pdf",
    ),
]

# Render license pages to temporary single-page PDFs
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    for src_html, target_pdf in jobs:
        tmp_pdf = src_html.with_suffix(".pdf")
        url = src_html.as_uri()
        print(f"Rendering license page for {target_pdf.name}")
        page.goto(url, wait_until="networkidle")
        page.emulate_media(media="print")
        page.pdf(
            path=str(tmp_pdf),
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
            prefer_css_page_size=True,
        )
    browser.close()

# Append the license page to each existing guide PDF
for src_html, target_pdf in jobs:
    tmp_pdf = src_html.with_suffix(".pdf")

    reader = pypdf.PdfReader(str(target_pdf))
    existing_pages = len(reader.pages)

    # If the last page is already our license page (identified by a marker),
    # replace it instead of appending. For the first run this is a no-op.
    # Simple heuristic: check if existing last page has the title "Licensed" or "Licensierad".
    last_page_text = reader.pages[-1].extract_text() or ""
    if "CC BY-NC-SA 4.0" in last_page_text:
        print(f"{target_pdf.name}: license page already present — replacing")
        writer = pypdf.PdfWriter()
        for page in reader.pages[:-1]:
            writer.add_page(page)
    else:
        print(f"{target_pdf.name}: appending license page ({existing_pages} -> {existing_pages + 1} pages)")
        writer = pypdf.PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

    # Append license page from tmp
    license_reader = pypdf.PdfReader(str(tmp_pdf))
    for page in license_reader.pages:
        writer.add_page(page)

    # Write back to target
    with open(target_pdf, "wb") as f:
        writer.write(f)

    final_pages = len(pypdf.PdfReader(str(target_pdf)).pages)
    size_kb = target_pdf.stat().st_size // 1024
    print(f"  -> {target_pdf.name}: {final_pages} pages, {size_kb} KB")

    # Clean up tmp file
    tmp_pdf.unlink()

print("Done.")
