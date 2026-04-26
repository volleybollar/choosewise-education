#!/usr/bin/env python3
"""Generate per-section OG (Open Graph) images as SVG, based on the
brand-defaults template at assets/images/brand/og-default.svg.

Each card is 1200×630, dark warm background gradient with the section
title on two lines and the brand wordmark below.

Idempotent: rewrites every file on each run.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets/images/brand/og"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Each section: (slug, line1, line2, eyebrow, accent_hex)
# accent_hex tints the gradient's right stop and the wordmark.
SECTIONS = [
    # English
    ("wise-en",            "The WISE Framework",        "for Education",          "CHOOSEWISE.EDUCATION", "#2d5a3f"),
    ("guides-en",          "AI Guides",                 "for schools",            "CHOOSEWISE.EDUCATION", "#2d5a3f"),
    ("prompts-en",         "Prompts",                   "for schools",            "CHOOSEWISE.EDUCATION", "#2d5a3f"),
    ("notebooklm-en",      "140 visual styles",         "for NotebookLM",         "CHOOSEWISE.EDUCATION", "#2d5a3f"),
    ("about-en",           "Johan Lindström",           "Education consultant",   "CHOOSEWISE.EDUCATION", "#c66b3d"),
    # Swedish
    ("wise-sv",            "RÄTT-modellen",             "för utbildning",         "CHOOSEWISE.EDUCATION", "#2d5a3f"),
    ("guides-sv",          "AI-guider",                 "för skolan",             "CHOOSEWISE.EDUCATION", "#2d5a3f"),
    ("prompts-sv",         "Promptar",                  "för skolan",             "CHOOSEWISE.EDUCATION", "#2d5a3f"),
    ("notebooklm-sv",      "140 visuella stilar",       "för NotebookLM",         "CHOOSEWISE.EDUCATION", "#2d5a3f"),
    ("about-sv",           "Johan Lindström",           "Skolutvecklingskonsult", "CHOOSEWISE.EDUCATION", "#c66b3d"),
]

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1a1a18"/>
      <stop offset="100%" stop-color="{accent}"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <text x="80" y="360" font-family="Fraunces,Georgia,serif" font-size="{size1}" font-weight="500" fill="#faf7f2">{line1}</text>
  <text x="80" y="{y2}" font-family="Fraunces,Georgia,serif" font-size="{size2}" font-weight="500" fill="#faf7f2">{line2}</text>
  <text x="80" y="540" font-family="Work Sans,Inter,sans-serif" font-size="24" fill="#c66b3d" letter-spacing="2">{eyebrow}</text>
</svg>
"""


def pick_size(text: str, base: int) -> int:
    if len(text) <= 20:
        return base
    if len(text) <= 26:
        return int(base * 0.85)
    return int(base * 0.7)


def main() -> None:
    written = 0
    for slug, line1, line2, eyebrow, accent in SECTIONS:
        size1 = pick_size(line1, 80)
        size2 = pick_size(line2, 80)
        y2 = 360 + size1 + 10
        svg = TEMPLATE.format(
            accent=accent,
            line1=line1,
            line2=line2,
            eyebrow=eyebrow,
            size1=size1,
            size2=size2,
            y2=y2,
        )
        out = OUT_DIR / f"{slug}.svg"
        out.write_text(svg, encoding="utf-8")
        written += 1
        print(f"  ✓ {out.relative_to(ROOT)}")
    print(f"Generated {written} OG SVG card(s) in {OUT_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
