"""Delade hjälpare för varumärkestesterna.

Vanlig modul, inte testfil — scripts/tests/ är ett paket, så testfiler
kan inte importera varandra direkt.
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parents[2]

# Kataloger som är spårade i git men ligger utanför våg 1 — inte det som
# avgör om en fil är publicerad (det gör git ls-files), men de ska ändå
# hoppas över när vi letar efter publicerade filer.
PUBLISHED_EXCLUDE = {
    ".git", "exports", "_unpublished", "docs",
    ".superpowers", ".playwright-mcp", "node_modules", "__pycache__",
}


def published_files(
    suffixes: tuple[str, ...] = (".html", ".css", ".js", ".svg"),
) -> Iterator[Path]:
    """Filer som GitHub Pages faktiskt serverar: spårade i git, utanför de
    kataloger som ligger utanför våg 1."""
    tracked = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z"],
        capture_output=True, text=True, check=True,
    ).stdout.split("\0")
    for rel in tracked:
        if not rel:
            continue
        path = ROOT / rel
        if path.suffix not in suffixes or not path.is_file():
            continue
        if PUBLISHED_EXCLUDE & set(Path(rel).parts):
            continue
        yield path
