"""Crestioras palett och typsnitt får aldrig finnas i publicerade filer.

Crestiora Books är en anonym utgivare. choosewise.education är Johans
namngivna sajt. Delar de visuellt uttryck går varumärkena att koppla ihop.
Spec §3.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brandguard import ROOT, published_files  # noqa: E402

CRESTIORA_FORBIDDEN = [
    "1B2733",          # navy
    "C8A86B",          # mässing
    "F6F3EE",          # grädde
    "2E4057",          # slate
    "Playfair Display",
]


def scan(forbidden):
    """Returnera {relativ sökväg: [träffade värden]} för publicerade filer."""
    hits = {}
    for path in published_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        found = [f for f in forbidden if f.lower() in text.lower()]
        if found:
            hits[str(path.relative_to(ROOT))] = found
    return hits


def test_no_crestiora_values_in_published_files():
    hits = scan(CRESTIORA_FORBIDDEN)
    assert hits == {}, (
        "Crestioras varumärke läcker in på Johans namngivna sajt:\n"
        + "\n".join(f"  {k}: {v}" for k, v in sorted(hits.items()))
    )
