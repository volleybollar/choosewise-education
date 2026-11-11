"""Interna Markdown-filer får inte bli webbsidor.

GitHub Pages bygger sajten med Jekyll, som gör om varje Markdown-fil till en
sida, även utan front matter. Så låg docs/ och prompt-pipelinens README ute
på choosewise.education fram till 2026-11-11. _config.yml stänger ute dem.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def excluded():
    lines = (ROOT / "_config.yml").read_text(encoding="utf-8").splitlines()
    start = lines.index("exclude:")
    return [l.strip()[2:] for l in lines[start + 1:] if l.strip().startswith("- ")]


def test_internal_markdown_is_excluded_from_the_site():
    assert "docs" in excluded()
    assert "exports/prompts/BATCH-README.md" in excluded()
