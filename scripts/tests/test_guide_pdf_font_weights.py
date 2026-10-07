# scripts/tests/test_guide_pdf_font_weights.py
"""Render-level guard: no converted guide PDF may embed a font whose name
indicates a weight above the Blueprint scale (display 300 / heading 400 /
body 400 / emphasis 500).

Why a render-level guard on top of the CSS-level ones (test_guide_print_css.py,
test_tokens.py): those read font-weight declarations in stylesheets, but a
font can be embedded at a heavier cut for reasons no stylesheet text shows.
Task 4's review caught exactly that — `.term-body strong` carried no
font-weight rule at all, so the browser requested its native bold (700);
Hanken Grotesk's variable font declares a 300–600 weight axis, so the
request clamped to 600, and HankenGrotesk-Regular_SemiBold got embedded in
all four re-rendered guides. The CSS-level weight guard could not see this —
there was no font-weight declaration to read, CSS or otherwise. Only reading
the rendered PDF's embedded fonts (via pdffonts) catches it.

Scope: no guide PDF is fully converted to Blueprint yet. The licence page
task 4 just finished is one page inside four guides whose A4 bodies are
still on the old styling and legitimately still embed Playfair Black,
Inter Bold and friends — those PDFs would fail this guard today for reasons
outside this task's scope. CONVERTED_PDFS is the allowlist of guide PDFs
whose templates are entirely Blueprint, checked by path relative to repo
root; it is empty after task 4. Tasks 5 and 6 add entries as their
templates convert; task 9 must assert the list covers all 22 guide PDFs
(see fp.GUIDE_PDFS in pdf_fingerprint.py).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdf_fingerprint import ROOT  # noqa: E402

# Populated by task 5 with the ten quick-start PDFs (fully converted — each
# quick start is its own PDF, not a chapter inside a larger guide). Task 6
# appends the twelve A4 guides as they convert. Task 9 asserts this list ==
# GUIDE_PDFS.
CONVERTED_PDFS: list[str] = [
    "assets/pdfs/guides/claude-quick-start-en.pdf",
    "assets/pdfs/guides/claude-quick-start-sv.pdf",
    "assets/pdfs/presentation-skills-summary-en.pdf",
    "assets/pdfs/presentationsteknik-sammanfattning-sv.pdf",
    "_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-en.pdf",
    "_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf",
    "_unpublished/assets/pdfs/guides/copilot-quick-start-en.pdf",
    "_unpublished/assets/pdfs/guides/copilot-quick-start-sv.pdf",
    "_unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-en.pdf",
    "_unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-sv.pdf",
]

# A font's PostScript name carries its weight as a name fragment
# (…_SemiBold, …-Bold, …-Black, …-Heavy) — there is no numeric weight to
# read once a PDF has been rendered, only the name the renderer subset and
# embedded. 300/400/500 (Regular, Medium) are allowed; anything heavier is not.
FORBIDDEN_WEIGHT_NAMES = re.compile(r"(SemiBold|Bold|Black|Heavy)", re.I)


def embedded_font_names(pdf_path: Path) -> list[str]:
    """Every embedded font's name column, via `pdffonts`."""
    out = subprocess.run(
        ["pdffonts", str(pdf_path)],
        capture_output=True, text=True, check=True,
    ).stdout
    lines = out.splitlines()[2:]  # drop the header row + its dashed underline
    return [line.split()[0] for line in lines if line.strip()]


def test_forbidden_weight_detector_catches_a_semibold_name():
    """Red-proof: the detector must be provably able to fail, independent of
    CONVERTED_PDFS being empty. AAAAAA+HankenGrotesk-Regular_SemiBold is the
    literal subset name this task's bug embedded — see the report."""
    assert FORBIDDEN_WEIGHT_NAMES.search("AAAAAA+HankenGrotesk-Regular_SemiBold")


def test_forbidden_weight_detector_catches_bold_black_and_heavy():
    for sample in ["BAAAAA+PlayfairDisplayRoman-Black", "AAAAAA+Inter-Regular_Bold",
                   "XAAAAA+SomeFont-Heavy"]:
        assert FORBIDDEN_WEIGHT_NAMES.search(sample), f"missade {sample}"


def test_forbidden_weight_detector_allows_regular_and_medium():
    for sample in ["AAAAAA+HankenGrotesk-Regular", "AAAAAA+HankenGrotesk-Regular_Medium"]:
        assert not FORBIDDEN_WEIGHT_NAMES.search(sample), f"fällde {sample} felaktigt"


@pytest.mark.parametrize("rel", CONVERTED_PDFS)
def test_converted_pdf_embeds_no_font_above_the_scale(rel: str):
    path = ROOT / rel
    assert path.exists(), f"{rel} saknas"
    offenders = sorted({n for n in embedded_font_names(path) if FORBIDDEN_WEIGHT_NAMES.search(n)})
    assert offenders == [], f"{rel} embeddar typsnitt utanför skalan: {offenders}"
