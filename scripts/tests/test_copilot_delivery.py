"""Leveransen är de två engelska PDF:erna, inte HTML:en de renderas ur.

Varje annan vakt i rundan läser HTML. Rättas HTML:en utan att PDF:erna
renderas om går hela sviten grön medan filen som går till Skool
fortfarande bär den svenska inramningen. Den här vakten läser det som
levereras.

Den täcker också quick-starten, som med avsikt står utanför
ytkonsistensvakten (spec §7) och annars inte bevakas av något som läser
dess innehåll.
"""
from __future__ import annotations

import re

import pytest

from . import pdf_fingerprint as fp

DELIVERED = (
    "_unpublished/assets/pdfs/guides/copilot-guide-en.pdf",
    "_unpublished/assets/pdfs/guides/copilot-quick-start-en.pdf",
)

# Strängar som inte får stå i de engelska PDF:erna när rundan är klar.
# "Swedish"/"Sweden" täcker inramningen, "Skolverket"/"IMY" myndigheterna,
# "Schrems"/"GDPR" den rättsliga analysen väg A tar bort, "April 2026"
# datumstämpeln och "kr 350" SEK-priset i den engelska SKU-tabellen.
FORBIDDEN = (
    "Swedish", "Sweden", "Skolverket", "IMY", "Schrems", "GDPR",
    "April 2026", "kr 350",
)


def _flat(rel: str) -> str:
    """pdftotext -layout bryter rader mitt i meningar; en sträng som
    'Swedish schools' står med radbrytning emellan i den renderade
    filen. Platta till allt blankt till ett mellanslag innan sökning."""
    return re.sub(r"\s+", " ", fp.extract(fp.ROOT / rel))


@pytest.mark.parametrize("rel", DELIVERED)
@pytest.mark.xfail(reason="röd till Task 10 har renderat om PDF:erna", strict=True)
def test_the_delivered_pdfs_carry_no_swedish_framing(rel):
    """Granskningsfokus 2."""
    flat = _flat(rel)
    found = [needle for needle in FORBIDDEN if needle in flat]
    assert found == [], f"{rel} bär kvar: {found}"


def test_the_quick_start_pdf_is_part_of_the_delivery_guard():
    """Granskningsfokus 3: quick-starten står utanför ytvakten med
    avsikt. Faller den också ur den här vakten bevakas dess innehåll av
    ingenting alls."""
    assert any("quick-start" in rel for rel in DELIVERED)
    for rel in DELIVERED:
        assert rel in fp.UNPUBLISHED_GUIDE_PDFS, f"{rel} står inte i facitlistan"
