"""Rutan "How to use a style" på infografikstilsidorna (engelska och svenska).

Filmen om de 140 stilarna skickar lärarna hit. Kortens prompter är bara
stildelen; rutan ger innehållsdelen som en mall med luckor, inställningarna
i Gemini Notebook och åldersgränsen. Rutan är öppen och kräver ingen e-post.

Läser HTML:en statiskt, som test_free_resources.py.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

# Sida -> meningen som mallen alltid ska ha. Den svenska mallen är skriven
# på svenska, så den bär samma krav med svenska ord.
PAGES = {
    "infographic-styles/index.html": "Use only facts from the sources",
    "sv/infografik-stilar/index.html": "Använd bara fakta från källorna",
}


def box(rel: str) -> str:
    """Rutans HTML, från <section class="style-howto"> till dess </section>,
    utan HTML-kommentarer: de är till för Johan och syns inte på sidan, så
    ett "18" i en kommentar får inte räknas."""
    page = (ROOT / rel).read_text(encoding="utf-8")
    m = re.search(r'<section class="style-howto"[^>]*>(.*?)</section>', page, re.S)
    assert m, f'{rel} saknar rutan <section class="style-howto">'
    return re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S)


def plain(fragment: str) -> str:
    """Texten utan taggar och teckenkoder, som webbläsaren visar den."""
    return html.unescape(re.sub(r"<[^>]+>", "", fragment))


@pytest.mark.parametrize("rel", PAGES)
def test_box_exists(rel):
    box(rel)


@pytest.mark.parametrize("rel, sentence", PAGES.items(), ids=list(PAGES))
def test_template_keeps_to_the_sources(rel, sentence):
    """Mallen står i ett kodblock, och kopieringsknappen kopierar samma
    text som syns. Står de två isär kopierar läraren något annat än det
    hon läser."""
    content = box(rel)
    shown = re.search(r"<pre[^>]*>\s*<code[^>]*>(.*?)</code>\s*</pre>", content, re.S)
    assert shown, f"{rel}: mallen står inte i ett kodblock"
    copied = re.search(r'data-copy="([^"]*)"', content)
    assert copied, f"{rel}: rutan saknar kopieringsknappen (data-copy)"
    assert sentence in plain(shown.group(1)), f"{rel}: mallen saknar {sentence!r}"
    assert plain(shown.group(1)) == html.unescape(copied.group(1)), (
        f"{rel}: knappen kopierar inte samma mall som syns"
    )


@pytest.mark.parametrize("rel", PAGES)
def test_box_states_the_age_limit(rel):
    assert re.search(r"\b18\b", plain(box(rel))), f"{rel}: åldersgränsen 18 står inte i rutan"


@pytest.mark.parametrize("rel", PAGES)
def test_box_asks_for_no_email(rel):
    content = box(rel)
    assert "<form" not in content, f"{rel}: rutan har ett formulär"
    assert 'type="email"' not in content, f"{rel}: rutan har ett e-postfält"
    assert "data-gate" not in content, f"{rel}: rutan går genom e-postgrinden"
