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
    ("wise-en",            "The WISE Framework",        "for Education",          "CHOOSEWISE.EDUCATION", "#0B3A6F"),
    ("guides-en",          "AI Guides",                 "for schools",            "CHOOSEWISE.EDUCATION", "#0B3A6F"),
    ("prompts-en",         "Prompts",                   "for schools",            "CHOOSEWISE.EDUCATION", "#0B3A6F"),
    ("notebooklm-en",      "140 visual styles",         "for NotebookLM",         "CHOOSEWISE.EDUCATION", "#0B3A6F"),
    ("evidence-en",        "Evidence Toolkit",          "for schools",            "CHOOSEWISE.EDUCATION", "#0B3A6F"),
    ("visualcodes-en",     "50 visual codes",           "for ChatGPT",            "CHOOSEWISE.EDUCATION", "#0B3A6F"),
    ("about-en",           "Johan Lindström",           "Education consultant",   "CHOOSEWISE.EDUCATION", "#C2793A"),
    # Swedish
    ("wise-sv",            "RÄTT-modellen",             "för utbildning",         "CHOOSEWISE.EDUCATION", "#0B3A6F"),
    ("guides-sv",          "AI-guider",                 "för skolan",             "CHOOSEWISE.EDUCATION", "#0B3A6F"),
    ("prompts-sv",         "Promptar",                  "för skolan",             "CHOOSEWISE.EDUCATION", "#0B3A6F"),
    ("notebooklm-sv",      "140 visuella stilar",       "för NotebookLM",         "CHOOSEWISE.EDUCATION", "#0B3A6F"),
    ("about-sv",           "Johan Lindström",           "Skolutvecklingskonsult", "CHOOSEWISE.EDUCATION", "#C2793A"),
]

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <defs>
    <style>
      @font-face {{
        font-family: 'Hanken Grotesk';
        src: url('../../../fonts/hanken-grotesk/HankenGrotesk-VariableFont.woff2') format('woff2');
        font-weight: 300 600;
        font-style: normal;
      }}
    </style>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07284D"/>
      <stop offset="100%" stop-color="{accent}"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <text x="80" y="360" font-family="Hanken Grotesk, sans-serif" font-size="{size1}" font-weight="300" fill="#FBFAF8">{line1}</text>
  <text x="80" y="{y2}" font-family="Hanken Grotesk, sans-serif" font-size="{size2}" font-weight="300" fill="#FBFAF8">{line2}</text>
  <text x="80" y="540" font-family="Hanken Grotesk, sans-serif" font-size="24" font-weight="500" fill="#EFF2F6" letter-spacing="2">{eyebrow}</text>
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
