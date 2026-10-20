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
    "free/visual-codes/index.html": ("visual-codes-50-en", "/assets/pdfs/free/visual-codes-50-en.pdf"),
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


def test_visual_codes_page_links_to_its_free_page():
    page = read("visual-codes/index.html")
    assert 'href="/free/visual-codes/"' in page
    assert "data-gate" not in page


def test_hub_has_no_coming_soon_left():
    assert "Coming soon" not in HUB.read_text(encoding="utf-8")


def test_nav_has_free_resources_link():
    assert '<a class="nav__link" href="/free/">Free resources</a>' in read("assets/partials/header-en.html")
    assert "/free/" not in read("assets/partials/header-sv.html")


def test_swedish_ai_page_is_untouched_by_free_resources():
    assert "/free/" not in read("sv/ai-eller-manniska/index.html")


# ── robots.txt och integritetssidan (Task 6) ──

GATED_PDF_RULES = ("Disallow: /assets/pdfs/free/", "Disallow: /assets/pdfs/prompts/*-en.pdf$")


def robots_groups() -> list[str]:
    """Varje User-agent-grupp för sig: en crawler läser bara sin mest
    specifika grupp, så AI-crawlarnas egna Allow: /-grupper måste också
    bära raderna."""
    text = read("robots.txt")
    return [g for g in re.split(r"\n(?=User-agent:)", text) if g.startswith("User-agent:")]


def test_robots_hides_gated_pdfs_in_every_group():
    for group in robots_groups():
        for rule in GATED_PDF_RULES:
            assert rule in group, group.splitlines()[0]


def test_robots_keeps_wise_and_swedish_open():
    rules = [l for l in read("robots.txt").splitlines() if l.startswith("Disallow:")]
    for path in ("/assets/pdfs/wise/wise-framework-en.pdf", "/assets/pdfs/prompts/larare-sv.pdf"):
        for rule in rules:
            pattern = re.escape(rule.split(":", 1)[1].strip()).replace(r"\*", ".*").replace(r"\$", "$")
            assert not re.match(pattern, path), f"{rule} träffar {path}"


def test_privacy_mentions_source_and_role():
    page = read("privacy/index.html")
    assert "where you arrived from" in page and "your role" in page
    assert "varifrån du kom" in page and "din roll" in page


def test_privacy_no_longer_says_prompt_packs_need_no_email():
    assert "prompt packs, and NotebookLM styles do <em>not</em> require an email" not in read("privacy/index.html")
