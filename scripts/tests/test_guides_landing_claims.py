"""Landningssidorna får inte lova fler guider än som finns.

Fyra av de fem guiderna — Copilot, Gemini/NotebookLM, Apple Intelligence
och elevguiden — ligger som utkast i `_unpublished/`. De är skrivna och
har PDF:er, men är aldrig publicerade och svarar 404 (GitHub Pages
serverar inte kataloger som börjar med understreck). Landningssidorna
annonserade dem ändå som nedladdningsbara.

Det är värre än ett vanligt skrivfel: svarskapseln är i en kommentar
uttryckligen skriven för att svarsmotorer ska kunna extrahera den
fristående, så överdriften matades vidare till ChatGPT och liknande.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

LANDING = {
    "guides/index.html": "guides/guides-en.json",
    "sv/guider/index.html": "sv/guider/guides-sv.json",
}

# Påståenden som var osanna och inte får skrivas tillbaka.
RETIRED = {
    "guides/index.html": [
        "Downloadable PDFs are available for each guide",
        "Five free comprehensive guides",
    ],
    "sv/guider/index.html": [
        "Nedladdningsbara pdf:er finns till varje guide",
        "Fem fria, utförliga guider",
    ],
}

_TAG = re.compile(r"<[^>]+>")


@pytest.mark.parametrize("page", sorted(RETIRED))
def test_the_retired_claims_are_not_written_back(page):
    text = (ROOT / page).read_text(encoding="utf-8")
    for claim in RETIRED[page]:
        assert claim not in text, f"{page}: {claim!r} står kvar"


@pytest.mark.parametrize("page,data", sorted(LANDING.items()))
def test_every_guide_the_page_offers_actually_resolves(page, data):
    """Den positiva sidan av samma krav: varje guide som listas som
    `available` måste ha en sida som finns på disk. Rutnätet byggs ur
    JSON, så det är där löftet ges."""
    guides = json.loads((ROOT / data).read_text(encoding="utf-8"))
    available = [g for g in guides if g.get("status") == "available"]
    assert available, f"{data}: inga guider — vakten vore tom"
    for g in available:
        target = ROOT / g["url"].strip("/") / "index.html"
        assert target.exists(), f"{data}: {g['id']} pekar på {g['url']} som inte finns"
