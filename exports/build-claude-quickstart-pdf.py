#!/usr/bin/env python3
"""Regenerate Claude Quick Start (EN + SV) 2-page A4 PDFs from the HTML sources."""
from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).parent.parent
jobs = [
    (root / "exports/claude-quick-start-en.html", root / "assets/pdfs/guides/claude-quick-start-en.pdf"),
    (root / "exports/claude-quick-start-sv.html", root / "assets/pdfs/guides/claude-quick-start-sv.pdf"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    for src, dst in jobs:
        url = src.as_uri()
        print(f"Building {dst.name} from {src.name}")
        page.goto(url, wait_until="networkidle")
        page.emulate_media(media="print")
        dst.parent.mkdir(parents=True, exist_ok=True)
        page.pdf(
            path=str(dst),
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
            prefer_css_page_size=True,
        )
        print(f"  -> {dst.stat().st_size // 1024} KB")
    browser.close()
print("Done.")
