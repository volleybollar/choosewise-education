"""Omstylingen får inte ändra ett ord — eller en bild — i guide-PDF:erna.

Facit ligger committat i fixtures/guide-pdf-baseline.json och togs från
PDF:erna som de såg ut före stilbytet. Ett rött test här betyder antingen
att texten faktiskt flyttat sig, eller att renderaren bytt typsnitt mitt i
(svenska tecken som faller tillbaka på ett systemsnitt bryter raderna).
Båda ska stoppa arbetet.

Textavtrycket är blint för bilder (det är en teckenmultimängd — en trasig
bildsökväg som faller tillbaka på alt-text syns bara om alt-texten råkar
göra sidans teckenmultimängd olik, inte för att en bild försvann). Facit
lagrar därför även varje PDF:s bildinventering (antal + bredd/höjd per
bild), så en omstyling som tappar eller byter ut en bild stoppas här
också — se test_image_inventory_is_unchanged.
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
    before = BASELINE[rel]["pages"]
    after = fp.fingerprints(path)
    assert len(after) == len(before), (
        f"{rel}: {len(before)} sidor före, {len(after)} efter — sidbrytningen flyttade sig"
    )
    moved = [i + 1 for i, (b, a) in enumerate(zip(before, after)) if b != a]
    assert not moved, f"{rel}: texten ändrad på sida {moved}"


@pytest.mark.parametrize("rel", fp.GUIDE_PDFS)
def test_image_inventory_is_unchanged(rel: str):
    path = fp.ROOT / rel
    assert path.exists(), f"{rel} saknas"
    before = BASELINE[rel]["images"]
    after = fp.image_sizes(path)
    assert after == before, (
        f"{rel}: bildinventeringen ändrades — före {before!r}, efter {after!r}"
    )


def test_baseline_covers_every_guide_pdf():
    """Facit ska inte tappa en PDF tyst."""
    assert sorted(BASELINE) == sorted(fp.GUIDE_PDFS)


def test_fingerprint_catches_a_single_character_change():
    """Beviset att vakten kan bli röd på det den vaktar."""
    assert fp.fingerprint("Hanken Grotesk") != fp.fingerprint("Hanken Grotesl")


def test_fingerprint_ignores_whitespace_only_differences():
    """Spärrad text tokeniseras olika av pdftotext utan att innehållet rört sig."""
    assert fp.fingerprint("P R O M P T") == fp.fingerprint("PROMPT")


def test_image_inventory_catches_a_dropped_image():
    """Beviset att bildvakten kan bli röd: en bild som försvinner ur en
    riktig PDF:s facit ska inte längre jämföras som lika."""
    before = BASELINE["assets/pdfs/guides/claude-guide-en.pdf"]["images"]
    assert before, "facit-antagande: den här PDF:en har minst en bild"
    after = before[1:]
    assert after != before


def test_image_inventory_catches_a_resized_image():
    """Samma bevis för en bild som bytt dimensioner — den trasiga
    notebooklm-sökvägen gav just det: en bild krympt till 14x16 px."""
    before = BASELINE["assets/pdfs/guides/claude-guide-en.pdf"]["images"]
    w, h = before[0]
    after = [[w, h + 1]] + before[1:]
    assert after != before
