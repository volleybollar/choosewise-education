"""Omstylingen får inte ändra ett ord i guide-PDF:erna.

Facit ligger committat i fixtures/guide-pdf-baseline.json och togs från
PDF:erna som de såg ut före stilbytet. Ett rött test här betyder antingen
att texten faktiskt flyttat sig, eller att renderaren bytt typsnitt mitt i
(svenska tecken som faller tillbaka på ett systemsnitt bryter raderna).
Båda ska stoppa arbetet.
"""
from __future__ import annotations

import json

import pytest

from . import pdf_fingerprint as fp

BASELINE = json.loads(fp.BASELINE.read_text(encoding="utf-8"))


@pytest.mark.parametrize("rel", fp.GUIDE_PDFS)
def test_text_is_unchanged(rel: str):
    path = fp.ROOT / rel
    assert path.exists(), f"{rel} saknas"
    before = BASELINE[rel]
    after = fp.fingerprints(path)
    assert len(after) == len(before), (
        f"{rel}: {len(before)} sidor före, {len(after)} efter — sidbrytningen flyttade sig"
    )
    moved = [i + 1 for i, (b, a) in enumerate(zip(before, after)) if b != a]
    assert not moved, f"{rel}: texten ändrad på sida {moved}"


def test_baseline_covers_every_guide_pdf():
    """Facit ska inte tappa en PDF tyst."""
    assert sorted(BASELINE) == sorted(fp.GUIDE_PDFS)


def test_fingerprint_catches_a_single_character_change():
    """Beviset att vakten kan bli röd på det den vaktar."""
    assert fp.fingerprint("Hanken Grotesk") != fp.fingerprint("Hanken Grotesl")


def test_fingerprint_ignores_whitespace_only_differences():
    """Spärrad text tokeniseras olika av pdftotext utan att innehållet rört sig."""
    assert fp.fingerprint("P R O M P T") == fp.fingerprint("PROMPT")
