"""Build-skripten ska peka på filer som finns.

De fjorton opublicerade guidmallarna flyttades till _unpublished/exports/
i 430f6d0 men skripten följde inte med. Testet fångar både att indata
saknas och att utdata skrivs till fel katalog — ett skript som skriver en
opublicerad guide till assets/pdfs/guides/ publicerar den av misstag.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = sorted((ROOT / "exports").glob("build-*.py"))

HTML_REF = re.compile(r'["\']([\w./-]*exports/[\w.-]+\.html)["\']')
PDF_REF = re.compile(r'["\']([\w./-]*(?:assets/pdfs|_unpublished)[\w./-]*\.pdf)["\']')


def _tracked_pdfs() -> set[str]:
    out = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "*.pdf"],
        capture_output=True, text=True, check=True,
    ).stdout.split()
    return set(out)


@pytest.mark.parametrize("script", SCRIPTS, ids=lambda p: p.name)
def test_every_html_input_exists(script: Path):
    missing = [r for r in sorted(set(HTML_REF.findall(script.read_text(encoding="utf-8"))))
               if not (ROOT / r).exists()]
    assert not missing, f"{script.name} pekar på HTML som inte finns: {missing}"


@pytest.mark.parametrize("script", SCRIPTS, ids=lambda p: p.name)
def test_every_pdf_output_matches_where_the_pdf_lives(script: Path):
    """Utdatasökvägen ska vara där PDF:en faktiskt ligger i git.

    En opublicerad guide som skrivs till assets/pdfs/guides/ hamnar i
    nästa commit som publicerad.
    """
    tracked = _tracked_pdfs()
    wrong = []
    for ref in sorted(set(PDF_REF.findall(script.read_text(encoding="utf-8")))):
        if ref in tracked:
            continue
        name = Path(ref).name
        elsewhere = [t for t in tracked if Path(t).name == name]
        if elsewhere:
            wrong.append(f"{ref} -> ligger i själva verket på {elsewhere[0]}")
    assert not wrong, f"{script.name} skriver till fel katalog: {wrong}"
