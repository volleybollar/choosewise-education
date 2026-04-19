#!/usr/bin/env python3
"""Regenerate Apple Intelligence (EN + SV) A4 guide PDFs from the print HTML sources.

EN build is the canonical deliverable. SV source may not exist yet (Phase 4 will
add it); if missing we skip rather than fail — same pattern as the Gemini build.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).parent.parent

def footer(title: str, page_label: str) -> str:
    return f"""
<div style="font-size: 8pt; color: #8a8a85; width: 100%; padding: 0 16mm 0 16mm;
            display: flex; justify-content: space-between; align-items: center;
            font-family: 'Inter', -apple-system, sans-serif;">
  <span>{title}</span>
  <span>{page_label} <span class="pageNumber"></span></span>
</div>
"""

jobs = [
    (
        root / "exports/apple-intelligence-print-a4-en.html",
        root / "assets/pdfs/guides/apple-intelligence-guide-en.pdf",
        footer("Apple Intelligence for teachers and school leaders", "Page"),
    ),
    (
        root / "exports/apple-intelligence-print-a4-sv.html",
        root / "assets/pdfs/guides/apple-intelligence-guide-sv.pdf",
        footer("Apple Intelligence för lärare och skolledare", "Sida"),
    ),
]

EMPTY_HEADER = "<div></div>"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    for src, dst, footer_template in jobs:
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
            # Small bottom margin to make room for the footer template;
            # left/right stay flush because the print HTML has its own 20mm padding.
            margin={"top": "0", "bottom": "14mm", "left": "0", "right": "0"},
            prefer_css_page_size=True,
            display_header_footer=True,
            header_template=EMPTY_HEADER,
            footer_template=footer_template,
        )
        print(f"  -> {dst.stat().st_size // 1024} KB")
    browser.close()
print("Done.")
