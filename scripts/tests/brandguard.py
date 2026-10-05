"""Delade hjälpare för varumärkestesterna.

Vanlig modul, inte testfil — scripts/tests/ är ett paket, så testfiler
kan inte importera varandra direkt.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parents[2]

# Samma definition av "publicerad fil" i varje test i sviten.
PUBLISHED_EXCLUDE = {
    ".git", "exports", "_unpublished", "docs",
    ".superpowers", ".playwright-mcp", "node_modules", "__pycache__",
}


def published_files(
    suffixes: tuple[str, ...] = (".html", ".css", ".js", ".svg"),
) -> Iterator[Path]:
    """Alla filer som faktiskt serveras av GitHub Pages."""
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in suffixes:
            continue
        if PUBLISHED_EXCLUDE & set(path.relative_to(ROOT).parts):
            continue
        yield path
