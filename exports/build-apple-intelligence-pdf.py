#!/usr/bin/env python3
"""Regenerate Apple Intelligence (EN + SV) A4 guide PDFs.

Two-pass render: cover page gets a white-title footer (no page number),
pages 2+ get the standard grey footer. Merged via pypdf.
"""
import os
import tempfile
from pathlib import Path
from pypdf import PdfWriter
from playwright.sync_api import sync_playwright

root = Path(__file__).parent.parent


def cover_footer(title: str) -> str:
    return f"""
<div style="font-size: 8pt; color: #faf7f2; width: 100%; padding: 0 16mm 0 16mm;
            display: flex; justify-content: flex-start; align-items: center;
            font-family: 'Inter', -apple-system, sans-serif;">
  <span>{title}</span>
</div>
"""


def standard_footer(title: str, page_label: str) -> str:
    return f"""
<div style="font-size: 8pt; color: #8a8a85; width: 100%; padding: 0 16mm 0 16mm;
            display: flex; justify-content: space-between; align-items: center;
            font-family: 'Inter', -apple-system, sans-serif;">
  <span>{title}</span>
  <span>{page_label} <span class="pageNumber"></span></span>
</div>
"""


EMPTY_HEADER = "<div></div>"

PDF_KW = dict(
    format="A4",
    print_background=True,
    margin={"top": "0", "bottom": "14mm", "left": "0", "right": "0"},
    prefer_css_page_size=True,
    display_header_footer=True,
    header_template=EMPTY_HEADER,
)


jobs = [
    (
        root / "exports/apple-intelligence-print-a4-en.html",
        root / "assets/pdfs/guides/apple-intelligence-guide-en.pdf",
        "Apple Intelligence for teachers and school leaders",
        "Page",
    ),
    (
        root / "exports/apple-intelligence-print-a4-sv.html",
        root / "assets/pdfs/guides/apple-intelligence-guide-sv.pdf",
        "Apple Intelligence för lärare och skolledare",
        "Sida",
    ),
]


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    for src, dst, title, page_label in jobs:
        if not src.exists():
            print(f"Skipping {dst.name} — source {src.name} not found")
            continue
        print(f"Building {dst.name} from {src.name}")
        page.goto(src.as_uri(), wait_until="networkidle")
        page.emulate_media(media="print")

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as cover_tmp:
            cover_path = cover_tmp.name
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as rest_tmp:
            rest_path = rest_tmp.name

        try:
            page.pdf(
                path=cover_path,
                footer_template=cover_footer(title),
                page_ranges="1",
                **PDF_KW,
            )
            page.pdf(
                path=rest_path,
                footer_template=standard_footer(title, page_label),
                page_ranges="2-",
                **PDF_KW,
            )

            writer = PdfWriter()
            writer.append(cover_path)
            writer.append(rest_path)
            dst.parent.mkdir(parents=True, exist_ok=True)
            with open(dst, "wb") as f:
                writer.write(f)
            writer.close()
            print(f"  -> {dst.stat().st_size // 1024} KB")
        finally:
            for tmp in (cover_path, rest_path):
                if os.path.exists(tmp):
                    os.unlink(tmp)

    browser.close()

print("Done.")
