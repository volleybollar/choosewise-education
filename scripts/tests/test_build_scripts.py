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


# ── Byggskriptens egen palett/typsnittsvakt (slutgranskningens fynd 1) ───
#
# test_guide_print_css.py vaktar de 26 handskrivna MALLARNA (.html) mot
# gammal palett, externa typsnittsanrop och förbjudna typsnitt i
# font-family-kontext. Den vakten globbar bara *.html — fyra byggskript
# (build-copilot-pdf.py, build-apple-intelligence-pdf.py,
# build-ai-for-elever-pdf.py, build-gemini-notebooklm-pdf.py) målar sin
# löpande sidfot som en inline HTML-sträng rakt i Playwrights eget
# footer_template, i KÄLLKOD (.py), inte i en .html-mall. Ingen vakt såg
# det — exakt därför bar alla fyra kvar 'Inter' och gammal grå/grädde
# genom hela vågens åtta granskningar. Samma förbjudna värden som
# mallvakten använder (test_guide_print_css.py:s CRESTIORA/OLD_CHOOSEWISE
# och dess font-family-kontextmönster), duplicerade här av samma skäl
# denna fils docstring redan ger för HTML_REF/PDF_REF: scripts/tests/ är
# ett paket, test_*.py-filer kan inte importera varandra direkt.
CRESTIORA = ["#1B2733", "#C8A86B", "#F6F3EE"]
OLD_CHOOSEWISE = ["#2d5a3f", "#f7f4ec", "#1e1e1c"]
# Fyndets egna sidfotsgråer/-grädde — inte i någon av ovanstående listor,
# men den faktiska gamla paletten som satt i de fyra byggskriptens
# footer_template ända till den här fixen. Läggs till här eftersom
# sidfoten var den enda platsen de användes: en framtida återkomst ska
# stoppas av samma vakt som hittade dem första gången.
OLD_FOOTER_VALUES = ["#faf7f2", "#8a8a85", "#a5a59f"]

# De elva guide-byggarna i den här vågen — samma lista och samma
# motivering som test_guide_asset_paths.py SCRIPTS: INTE
# build-nlm-prompts-en.py (redan ett dokumenterat, avsiktligt undantag —
# struket ur vågen, bär fortfarande Crestioras palett och Playfair, se
# pr-body.md) och inte Johans egna build-wise-*.py, som aldrig hört till
# den här vågen.
GUIDE_BUILD_SCRIPT_NAMES = {
    "build-claude-pdf.py", "build-claude-quickstart-pdf.py",
    "build-presentationsteknik-pdf.py", "build-presentationsteknik-quickstart-pdf.py",
    "build-gemini-notebooklm-pdf.py", "build-gemini-quickstart-pdf.py",
    "build-copilot-pdf.py", "build-copilot-quickstart-pdf.py",
    "build-apple-intelligence-pdf.py", "build-apple-intelligence-quickstart-pdf.py",
    "build-ai-for-elever-pdf.py",
}
GUIDE_BUILD_SCRIPTS = [s for s in SCRIPTS if s.name in GUIDE_BUILD_SCRIPT_NAMES]


def test_the_guide_build_script_list_is_not_empty():
    """Red-proof: faller SCRIPTS-globbet ihop eller tappar ett namn skulle
    de tre vakterna nedan tyst skanna färre skript och ändå bli gröna."""
    assert len(GUIDE_BUILD_SCRIPTS) == 11, [p.name for p in GUIDE_BUILD_SCRIPTS]


@pytest.mark.parametrize("script", GUIDE_BUILD_SCRIPTS, ids=lambda p: p.name)
def test_no_old_palette_in_build_scripts(script: Path):
    text = script.read_text(encoding="utf-8")
    for value in CRESTIORA + OLD_CHOOSEWISE + OLD_FOOTER_VALUES:
        assert value.lower() not in text.lower(), f"{script.name} bär {value}"


@pytest.mark.parametrize("script", GUIDE_BUILD_SCRIPTS, ids=lambda p: p.name)
def test_no_external_font_calls_in_build_scripts(script: Path):
    assert "fonts.googleapis.com" not in script.read_text(encoding="utf-8")


@pytest.mark.parametrize("script", GUIDE_BUILD_SCRIPTS, ids=lambda p: p.name)
def test_only_blueprint_typefaces_in_build_script_font_family_context(script: Path):
    """Samma kontextmedvetna mönster som test_guide_print_css.py:s
    test_only_blueprint_typefaces_in_font_family_context, tillämpat på
    byggskriptens inline footer_template-strängar i stället för en
    mallfils <style>-block eller markup."""
    families = re.findall(r"font-family:\s*[\"']?([^;}\"'>]+)", script.read_text(encoding="utf-8"))
    banned = [f for f in families if re.search(r"Playfair|Fraunces|Work Sans|\bInter\b", f)]
    assert not banned, f"{script.name}: {banned}"
