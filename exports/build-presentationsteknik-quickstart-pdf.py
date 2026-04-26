#!/usr/bin/env python3
"""Build the Presentationsteknik quick-start PDF (SV) from HTML source.

Output:
  assets/pdfs/presentationsteknik-sammanfattning-sv.pdf

Run:
  pip install -r exports/requirements.txt   # one-time
  python3 exports/build-presentationsteknik-quickstart-pdf.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import pypdf

root = Path(__file__).parent.parent
pdf_out_dir = root / "assets/pdfs"
pdf_out_dir.mkdir(parents=True, exist_ok=True)

jobs = [
    {
        "lang": "sv",
        "main_html": root / "exports/presentationsteknik-quick-start-sv.html",
        "final_pdf": pdf_out_dir / "presentationsteknik-sammanfattning-sv.pdf",
    },
]


def render_pdf(page, html_path: Path, pdf_path: Path) -> None:
    page.goto(html_path.as_uri(), wait_until="networkidle")
    page.emulate_media(media="print")
    page.pdf(
        path=str(pdf_path),
        format="A4",
        print_background=True,
        prefer_css_page_size=True,
        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
    )


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    for job in jobs:
        lang = job["lang"]
        main_html = job["main_html"]
        final_pdf = job["final_pdf"]

        if not main_html.exists():
            print(f"[{lang}] Skipping — source missing: {main_html.name}")
            continue

        print(f"[{lang}] Rendering quick-start from {main_html.name}")
        render_pdf(page, main_html, final_pdf)
        pages = len(pypdf.PdfReader(str(final_pdf)).pages)
        size_kb = final_pdf.stat().st_size // 1024
        print(f"[{lang}] -> {final_pdf.name}: {pages} pages, {size_kb} KB")

    browser.close()

print("Done.")
