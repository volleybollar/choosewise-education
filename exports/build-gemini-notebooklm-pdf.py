#!/usr/bin/env python3
"""Regenerate Gemini & NotebookLM (EN + SV) A4 guide PDFs from the print HTML sources.

EN build is the canonical deliverable. SV source may not exist yet; if missing we
skip rather than fail — same pattern as build-claude-quickstart-pdf.py.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).parent.parent
jobs = [
    (
        root / "exports/gemini-notebooklm-print-a4-en.html",
        root / "assets/pdfs/guides/gemini-notebooklm-guide-en.pdf",
    ),
    (
        root / "exports/gemini-notebooklm-print-a4-sv.html",
        root / "assets/pdfs/guides/gemini-notebooklm-guide-sv.pdf",
    ),
]

# Per-page footer template used by Playwright's display_header_footer.
# CSS inside the template needs explicit color — Chromium prints these elements
# independently of the document body.
FOOTER_TEMPLATE = """
<div style="font-size: 8pt; color: #a5a59f; width: 100%; padding: 0 16mm 0 16mm;
            display: flex; justify-content: space-between; align-items: center;
            font-family: 'Inter', -apple-system, sans-serif;">
  <span>Gemini &amp; NotebookLM for teachers and school leaders</span>
  <span>Page <span class="pageNumber"></span></span>
</div>
"""

EMPTY_HEADER = "<div></div>"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    for src, dst in jobs:
        if not src.exists():
            print(f"Skipping {dst.name} — source {src.name} not found")
            continue
        url = src.as_uri()
        print(f"Building {dst.name} from {src.name}")
        page.goto(url, wait_until="networkidle")
        page.emulate_media(media="print")
        dst.parent.mkdir(parents=True, exist_ok=True)
        page.pdf(
            path=str(dst),
            format="A4",
            print_background=True,
            # Small top/bottom margins create the room the footer template needs;
            # left/right stay flush because the print HTML has its own 20mm padding.
            margin={"top": "0", "bottom": "14mm", "left": "0", "right": "0"},
            prefer_css_page_size=True,
            display_header_footer=True,
            header_template=EMPTY_HEADER,
            footer_template=FOOTER_TEMPLATE,
        )
        print(f"  -> {dst.stat().st_size // 1024} KB")
    browser.close()
print("Done.")
