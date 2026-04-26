#!/usr/bin/env python3
"""Build the Presentation Skills full-guide PDFs (SV + EN) from HTML sources.

Idempotent: renders exports/presentationsteknik-print-a4-sv.html and
exports/presentation-skills-print-a4-en.html to PDF, then appends the
CC BY-NC-SA 4.0 license page (from the matching license HTML) as the
final page of each.

Outputs:
  assets/pdfs/presentationsteknik-guide-sv.pdf
  assets/pdfs/presentation-skills-guide-en.pdf

Run:
  pip install -r exports/requirements.txt   # one-time
  python3 exports/build-presentationsteknik-pdf.py
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
        "main_html": root / "exports/presentationsteknik-print-a4-sv.html",
        "license_html": root / "exports/presentationsteknik-license-sv.html",
        "final_pdf": pdf_out_dir / "presentationsteknik-guide-sv.pdf",
    },
    {
        "lang": "en",
        "main_html": root / "exports/presentation-skills-print-a4-en.html",
        "license_html": root / "exports/presentation-skills-license-en.html",
        "final_pdf": pdf_out_dir / "presentation-skills-guide-en.pdf",
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
        license_html = job["license_html"]
        final_pdf = job["final_pdf"]

        if not main_html.exists():
            print(f"[{lang}] Skipping — source missing: {main_html.name}")
            continue

        # 1. Render the main guide to a temp PDF.
        main_tmp = main_html.with_suffix(".tmp.pdf")
        print(f"[{lang}] Rendering main guide from {main_html.name}")
        render_pdf(page, main_html, main_tmp)
        main_pages = len(pypdf.PdfReader(str(main_tmp)).pages)
        print(f"[{lang}]   main: {main_pages} pages")

        # 2. Render the license page (if source exists).
        license_tmp = None
        if license_html.exists():
            license_tmp = license_html.with_suffix(".tmp.pdf")
            print(f"[{lang}] Rendering license page from {license_html.name}")
            render_pdf(page, license_html, license_tmp)

        # 3. Concatenate: main guide + license page.
        writer = pypdf.PdfWriter()
        for pg in pypdf.PdfReader(str(main_tmp)).pages:
            writer.add_page(pg)
        if license_tmp is not None:
            for pg in pypdf.PdfReader(str(license_tmp)).pages:
                writer.add_page(pg)

        with open(final_pdf, "wb") as fh:
            writer.write(fh)

        final_pages = len(pypdf.PdfReader(str(final_pdf)).pages)
        size_kb = final_pdf.stat().st_size // 1024
        print(f"[{lang}] -> {final_pdf.name}: {final_pages} pages, {size_kb} KB")

        # 4. Clean up.
        main_tmp.unlink(missing_ok=True)
        if license_tmp is not None:
            license_tmp.unlink(missing_ok=True)

    browser.close()

print("Done.")
