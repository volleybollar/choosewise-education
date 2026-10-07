#!/usr/bin/env python3
# exports/build-guide-pdfs.py
"""Kör alla guidbyggare i ordning. Elva skript, en kommandorad.

  /usr/bin/python3 exports/build-guide-pdfs.py           # alla
  /usr/bin/python3 exports/build-guide-pdfs.py claude    # bara de som matchar

Skriptet bygger inget själv — det startar de befintliga byggarna, så att
omrendering efter en stiländring är ett steg och inte elva.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
BUILDERS = [
    "build-claude-pdf.py",
    "build-claude-quickstart-pdf.py",
    "build-presentationsteknik-pdf.py",
    "build-presentationsteknik-quickstart-pdf.py",
    # build-nlm-prompts-en.py dropped from the wave (ruling 2026-10-07): it
    # reads /tmp/nlm-prompts-en-chunk{1..4}.json, those chunks don't exist
    # and were never committed, so the script can't run at all from this
    # repo. Recovering the chunks is its own job — don't re-add it here
    # until that's solved.
    "build-gemini-notebooklm-pdf.py",
    "build-gemini-quickstart-pdf.py",
    "build-copilot-pdf.py",
    "build-copilot-quickstart-pdf.py",
    "build-apple-intelligence-pdf.py",
    "build-apple-intelligence-quickstart-pdf.py",
    "build-ai-for-elever-pdf.py",
]

needle = sys.argv[1] if len(sys.argv) > 1 else ""
selected = [b for b in BUILDERS if needle in b]
if not selected:
    sys.exit(f"inget byggskript matchar {needle!r}")

failed = []
for name in selected:
    print(f"\n=== {name} ===", flush=True)
    result = subprocess.run([sys.executable, str(HERE / name)])
    if result.returncode != 0:
        failed.append(name)

print()
if failed:
    sys.exit("misslyckades: " + ", ".join(failed))
print(f"klart: {len(selected)} byggskript")
