#!/usr/bin/env python3
"""Regenerate WISE (EN) and RÄTT (SV) A4 handout PDFs from the print-a4 HTML files."""
import sys, os
from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).parent.parent
jobs = [
    (root / "exports/wise-print-a4.html", root / "assets/pdfs/wise/wise-framework-en.pdf"),
    (root / "exports/print-a4.html",      root / "assets/pdfs/wise/ratt-modellen-sv.pdf"),
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
        print(f"  → {dst.stat().st_size // 1024} KB")
    browser.close()
print("Done.")
