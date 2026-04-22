#!/usr/bin/env python3
"""Build choosewise.education prompt-library PDFs (EN + SV) from HTML sources.

Scans exports/prompts/ for *.html source files, renders each to an A4 PDF
using Playwright (same pipeline as the other print exports), and writes
the result to assets/pdfs/prompts/.

File naming convention:
  <nr>-<slug>-<lang>.html       →  prompts/<slug>-<lang>.pdf
  e.g. 01-larare-sv.html         →  prompts/larare-sv.pdf
       01-teachers-en.html       →  prompts/teachers-en.pdf

Run:
  pip install -r exports/requirements.txt   # one-time
  python3 exports/prompts/build-prompts-pdf.py
  python3 exports/prompts/build-prompts-pdf.py 01-larare-sv   # build one
"""
import re
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).parent.parent.parent
src_dir = Path(__file__).parent
out_dir = root / "assets/pdfs/prompts"
out_dir.mkdir(parents=True, exist_ok=True)

# Collect source HTML files — ignore anything starting with underscore (partials)
only = sys.argv[1] if len(sys.argv) > 1 else None
sources = sorted(
    f for f in src_dir.glob("*.html")
    if not f.name.startswith("_") and (only is None or f.stem == only)
)

if not sources:
    print("No matching prompt HTML files found.")
    sys.exit(1)


def out_name_for(src: Path) -> str:
    """01-larare-sv.html → larare-sv.pdf (strip the leading number)."""
    m = re.match(r"^\d+-(.+)$", src.stem)
    return (m.group(1) if m else src.stem) + ".pdf"


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    for src in sources:
        pdf_path = out_dir / out_name_for(src)
        print(f"  Rendering {src.name} → {pdf_path.name}")
        page.goto(src.as_uri(), wait_until="networkidle")
        page.emulate_media(media="print")
        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        kb = pdf_path.stat().st_size // 1024
        print(f"  -> {pdf_path.name} ({kb} KB)")

    browser.close()

print("Done.")
