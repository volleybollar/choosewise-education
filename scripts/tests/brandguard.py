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


# published_files() utesluter hela exports/ — rätt i våg 1, där mallarna låg
# utanför arbetet. Våg 2a konverterar mallarna själva, så de behöver sin
# egen vakt (se test_guide_print_css.py). GUIDE_TEMPLATE_GLOBS räknar upp
# guidfamiljens handskrivna mallar explicit snarare än att försöka hitta
# dem via published_files() + ett undantag, eftersom _unpublished/ redan är
# helt uteslutet ur published_files() och mallarna där är precis lika
# mycket i scope för den här vakten som de publicerade.
GUIDE_TEMPLATE_GLOBS = (
    "exports/claude-print-a4-*.html",
    "exports/claude-guide-license-*.html",
    "exports/claude-quick-start-*.html",
    "exports/presentation-skills-*.html",
    "exports/presentationsteknik-*.html",
    "_unpublished/exports/*.html",
)

# nlm-140-prompts-en.html är dropped ur våg 2a (ruling 2026-10-07): dess
# builder läser /tmp/nlm-prompts-en-chunk{1..4}.json, filer som inte finns
# och aldrig committats, så PDF:en går inte att bygga om från repot alls.
# Ingenting vaktar idag dess palett, typsnitt eller vikter — se
# scripts/tests/pdf_fingerprint.py. (Den matchar inga av globarna ovan
# ändå, så det här är ett dokumenterat säkerhetsnät, inte det som
# faktiskt håller den borta.)
GENERATED = {"nlm-140-prompts-en.html"}


def guide_templates() -> Iterator[Path]:
    """De handskrivna tryckmallarna bakom guide-PDF:erna (våg 2a)."""
    seen: set[Path] = set()
    for pattern in GUIDE_TEMPLATE_GLOBS:
        for path in sorted(ROOT.glob(pattern)):
            if path.name in GENERATED or path in seen:
                continue
            seen.add(path)
            yield path
