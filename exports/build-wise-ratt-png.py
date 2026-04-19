#!/usr/bin/env python3
"""Regenerate WISE + RÄTT PNG renders from HTML sources.

Covers the presentation (1920x1080) and LinkedIn (1200x1200) shares
for both frameworks. PNGs land next to the HTML in exports/.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).parent.parent

jobs = [
    (root / "exports/wise-presentation-1920x1080.html",
     root / "exports/wise-framework-presentation-1920x1080.png",
     1920, 1080),
    (root / "exports/wise-linkedin-1200x1200.html",
     root / "exports/wise-framework-linkedin-1200x1200.png",
     1200, 1200),
    (root / "exports/ratt-presentation-1920x1080.html",
     root / "exports/ratt-modellen-presentation-1920x1080.png",
     1920, 1080),
    (root / "exports/ratt-linkedin-1200x1200.html",
     root / "exports/ratt-modellen-linkedin-1200x1200.png",
     1200, 1200),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for src, dst, w, h in jobs:
        print(f"Rendering {dst.name} ({w}x{h}) from {src.name}")
        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        page.goto(src.as_uri(), wait_until="networkidle")
        page.screenshot(path=str(dst), full_page=False, omit_background=False)
        page.close()
        print(f"  -> {dst.stat().st_size // 1024} KB")
    browser.close()
print("Done.")
