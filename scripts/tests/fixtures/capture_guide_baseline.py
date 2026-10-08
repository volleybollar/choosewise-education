"""Fångar facit för de 22 guide-PDF:erna. Körs EN gång, före stilbytet.

Körs den igen efter en stiländring skriver den över facit med det nya
läget och paritetstestet slutar betyda något. Den vägrar därför skriva
över en befintlig fixtur om inte --force anges.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pdf_fingerprint as fp  # noqa: E402

force = "--force" in sys.argv
if fp.BASELINE.exists() and not force:
    sys.exit(f"{fp.BASELINE} finns redan. Kör med --force bara om du MENAR att "
             "slänga facit — efter en stiländring är det liktydigt med att "
             "slå av paritetsvakten.")

data = {}
for rel in fp.GUIDE_PDFS:
    path = fp.ROOT / rel
    if not path.exists():
        sys.exit(f"saknas: {rel}")
    entry = fp.capture(path)
    data[rel] = entry
    print(f"{len(entry['pages']):3} sidor  {len(entry['images']):2} bilder  {rel}")

fp.BASELINE.parent.mkdir(parents=True, exist_ok=True)
fp.BASELINE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"\nfacit skrivet: {fp.BASELINE} ({len(data)} PDF:er)")
