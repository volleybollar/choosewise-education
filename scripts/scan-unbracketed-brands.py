#!/usr/bin/env python3
"""Scan every prompt-pack JSON file for product/brand names that appear OUTSIDE
of bracketed placeholders.

The pack convention is that any specific product or example should be wrapped
in brackets — "[t.ex. Microsoft Teams eller Google Classroom]" / "[e.g.
Microsoft Teams or Google Classroom]" — so the user can swap it for their
own context. This script flags any prompt that names a known product without
that bracketing, so they can be fixed.

Reports a summary plus one snippet per unique brand-mention occurrence. Does
not modify anything; safe to run repeatedly.

Usage:
    python3 scripts/scan-unbracketed-brands.py            # scan all data files
    python3 scripts/scan-unbracketed-brands.py tidsutnyttjande   # one file
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "exports/prompts/data"

# Add new products here as they appear. Keep multi-word brands before single-
# word ones so the regex is greedy enough.
BRANDS = [
    # AI tools
    "ChatGPT", "Claude", "Gemini", "NotebookLM", "Perplexity", "Apple Intelligence",
    # Microsoft
    "Microsoft Teams", "Microsoft 365", "Microsoft Word", "Microsoft PowerPoint",
    "Microsoft Excel", "Microsoft OneNote", "Microsoft Forms", "Microsoft Copilot",
    "Office 365", "OneNote", "OneDrive", "Outlook", "PowerPoint", "SharePoint",
    "Copilot",
    # Google
    "Google Classroom", "Google Workspace", "Google Docs", "Google Drive",
    "Google Slides", "Google Sheets", "Google Forms", "Google Meet", "Gmail",
    # Apple
    "iCloud", "Pages", "Numbers", "Keynote", "Safari",
    # Other
    "Canva", "Padlet", "Mentimeter", "Kahoot", "Quizlet", "Notion", "Slack",
    "Zoom", "Trello", "Asana", "Miro", "Figma", "Adobe Express", "YouTube",
    "Wikipedia", "Khan Academy", "Duolingo", "Quizizz", "Wordwall", "Flipgrid",
    "Seesaw", "Edmodo", "Schoology", "Moodle", "itslearning",
    # Swedish-school-specific
    "Vklass", "Schoolsoft", "Unikum", "InfoMentor", "Skolon", "Inläsningstjänst",
]

BRAND_RE = re.compile(r"\b(?:" + "|".join(re.escape(b) for b in BRANDS) + r")\b")


def is_inside_brackets(text, pos):
    o = text.rfind("[", 0, pos)
    c = text.rfind("]", 0, pos)
    if o > c:
        return text.find("]", pos) != -1
    return False


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    total = outside = 0
    by_file = {}
    samples = []

    for f in sorted(os.listdir(DATA)):
        if not f.endswith(".json"):
            continue
        if only and only not in f:
            continue
        with open(DATA / f) as fh:
            data = json.load(fh)
        n = 0
        for part in data.get("parts", []):
            for i, p in enumerate(part.get("prompts", [])):
                text = p if isinstance(p, str) else p.get("text", "")
                for m in BRAND_RE.finditer(text):
                    total += 1
                    if not is_inside_brackets(text, m.start()):
                        outside += 1
                        n += 1
                        s = max(0, m.start() - 60)
                        e = min(len(text), m.end() + 40)
                        samples.append((f, i + 1, m.group(0), text[s:e]))
        if n:
            by_file[f] = n

    print(f"Brand-mentions total: {total}")
    print(f"  inside brackets (good):   {total - outside}")
    print(f"  OUTSIDE brackets (flag):  {outside}")
    print()
    if by_file:
        print("Files with flagged mentions (top 25):")
        for f, n in sorted(by_file.items(), key=lambda x: -x[1])[:25]:
            print(f"  {n:3d}  {f}")
        print()
        print("Snippets (max 25):")
        for f, num, brand, snippet in samples[:25]:
            print(f"  [{f} #{num}] {brand}: ...{snippet}...")
        print()
        print("Note: review each match — some may be legitimate (e.g. 'Numbers and Arithmetic'")
        print("as a maths-topic label, not Apple Numbers).")
    else:
        print("✓ All brand mentions are inside bracketed placeholders.")


if __name__ == "__main__":
    main()
