"""Gratismaterialet på /free/ (engelska): hubben, djuplänkarna och
noteringarna på de sidor vars material laddas ner där.

Läser HTML:en statiskt. Själva grindens beteende vaktas i
test_mailerlite_gate.py.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HUB = ROOT / "free/index.html"
GATE_SCRIPT = '<script type="module" src="/assets/js/mailerlite-gate.js"'

# Djuplänk -> (resurs-id, PDF-adress) för de grindade resurser som är live.
DEEP_LINKS = {
    "free/ai-or-human/index.html": ("ai-or-human-en", "/assets/pdfs/free/ai-or-human-en.pdf"),
}


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def gates(html: str) -> list[tuple[str, str]]:
    return re.findall(r'data-gate="([^"]+)"[^>]*data-gate-pdf="([^"]+)"', html)


def test_hub_links_every_deep_link():
    hub = HUB.read_text(encoding="utf-8")
    for rel in [*DEEP_LINKS, "free/prompts/index.html"]:
        href = "/" + rel.removesuffix("index.html")
        assert f'href="{href}"' in hub, f"hubben länkar inte {href}"


def test_deep_links_gate_the_right_pdf():
    for rel, (gate_id, pdf) in DEEP_LINKS.items():
        assert (gate_id, pdf) in gates(read(rel)), rel


def test_gated_pdfs_exist_and_are_not_under_unpublished():
    for rel in [*DEEP_LINKS, "free/index.html"]:
        for _, pdf in gates(read(rel)):
            assert not pdf.startswith("/_unpublished/"), pdf
            assert (ROOT / pdf.lstrip("/")).is_file(), f"{rel}: {pdf} saknas"


def test_free_pages_load_the_gate_script():
    for rel in ["free/index.html", *DEEP_LINKS]:
        assert GATE_SCRIPT in read(rel), rel


def test_gate_ids_are_english():
    for rel in ["free/index.html", *DEEP_LINKS]:
        for gate_id, _ in gates(read(rel)):
            assert gate_id.endswith("-en"), gate_id


def test_open_section_has_no_gates():
    hub = HUB.read_text(encoding="utf-8")
    m = re.search(r'<section[^>]*id="open"[^>]*>(.*?)</section>', hub, re.S)
    assert m, "hubben saknar avdelningen id=\"open\""
    assert "data-gate" not in m.group(1)
    assert m.group(1).count('class="card') >= 3


def test_ai_or_human_page_links_to_its_free_page():
    page = read("ai-or-human/index.html")
    assert 'href="/free/ai-or-human/"' in page
    assert "data-gate" not in page


def test_swedish_ai_page_is_untouched_by_free_resources():
    assert "/free/" not in read("sv/ai-eller-manniska/index.html")
