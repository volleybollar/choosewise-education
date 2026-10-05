"""Typsnitten ska vara självhostade. Inga anrop till Google."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brandguard import ROOT, published_files  # noqa: E402

EXPECTED_FONT_FILES = [
    "assets/fonts/hanken-grotesk/HankenGrotesk-VariableFont.woff2",
    "assets/fonts/instrument-serif/InstrumentSerif-Regular.woff2",
    "assets/fonts/instrument-serif/InstrumentSerif-Italic.woff2",
]


@pytest.mark.parametrize("rel", EXPECTED_FONT_FILES)
def test_font_file_is_self_hosted(rel):
    path = ROOT / rel
    assert path.exists(), f"{rel} saknas"
    assert path.stat().st_size > 10_000, f"{rel} ser trunkerad ut"


def test_fontface_declares_both_families():
    css = (ROOT / "assets/css/fonts.css").read_text(encoding="utf-8")
    assert "Hanken Grotesk" in css
    assert "Instrument Serif" in css
    assert "Fraunces" not in css
    assert "Work Sans" not in css


def test_hanken_covers_the_weights_we_use():
    css = (ROOT / "assets/css/fonts.css").read_text(encoding="utf-8")
    assert "font-weight: 300 600" in css


def test_no_published_file_calls_google_fonts():
    offenders = []
    for path in published_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "fonts.googleapis.com" in text or "fonts.gstatic.com" in text:
            offenders.append(str(path.relative_to(ROOT)))
    assert offenders == [], f"Hämtar typsnitt från Google: {offenders}"
