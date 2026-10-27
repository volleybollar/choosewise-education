"""E-postgrinden på de engelska prompt-PDF:erna (scripts/gate-prompt-downloads.py).

Promptsidorna själva förblir öppna; bara PDF-länken grindas. Svenska sidor
rörs inte — Johans beslut 2026-10-20 gäller bara engelska.
"""
from __future__ import annotations

import importlib.util
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE_SCRIPT = '<script type="module" src="/assets/js/mailerlite-gate.js" defer></script>'
LINK_RE = re.compile(r'<a\b[^>]*href="/assets/pdfs/prompts/([a-z0-9-]+)-en\.pdf"[^>]*>')

spec = importlib.util.spec_from_file_location("gate_prompts", ROOT / "scripts/gate-prompt-downloads.py")
gate_prompts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate_prompts)


def english_pack_pages() -> list[Path]:
    return sorted(p for p in (ROOT / "prompts").glob("*/index.html") if LINK_RE.search(p.read_text(encoding="utf-8")))


def test_there_are_59_english_packs():
    assert len(english_pack_pages()) == 59


def test_every_english_prompt_pdf_link_is_gated():
    for page in english_pack_pages():
        for m in LINK_RE.finditer(page.read_text(encoding="utf-8")):
            tag, slug = m.group(0), m.group(1)
            assert f'data-gate="prompts-{slug}-en"' in tag, page
            assert f'data-gate-pdf="/assets/pdfs/prompts/{slug}-en.pdf"' in tag, page
            assert " download" not in tag, page


def test_gated_pages_load_the_gate_script():
    for page in english_pack_pages():
        assert page.read_text(encoding="utf-8").count(GATE_SCRIPT) == 1, page


def test_gated_links_keep_href_for_no_js():
    for page in english_pack_pages():
        for m in LINK_RE.finditer(page.read_text(encoding="utf-8")):
            assert (ROOT / f"assets/pdfs/prompts/{m.group(1)}-en.pdf").is_file()


def test_no_swedish_page_is_gated():
    for page in (ROOT / "sv").rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        assert "data-gate" not in text and "mailerlite-gate.js" not in text, page


def test_script_is_idempotent(tmp_path):
    site = tmp_path / "site"
    (site / "prompts").mkdir(parents=True)
    for src in [ROOT / "prompts/teachers", ROOT / "prompts/chemistry"]:
        shutil.copytree(src, site / "prompts" / src.name)
    (site / "free/prompts").mkdir(parents=True)
    shutil.copy(ROOT / "free/prompts/index.html", site / "free/prompts/index.html")
    gate_prompts.run(site)
    first = {p: p.read_bytes() for p in site.rglob("*.html")}
    gate_prompts.run(site)
    assert {p: p.read_bytes() for p in site.rglob("*.html")} == first


def test_free_prompts_lists_every_english_pack():
    hub = (ROOT / "free/prompts/index.html").read_text(encoding="utf-8")
    block = hub.split("<!-- PACKS:START -->")[1].split("<!-- PACKS:END -->")[0]
    for page in english_pack_pages():
        slug = LINK_RE.search(page.read_text(encoding="utf-8")).group(1)
        assert f'data-gate="prompts-{slug}-en"' in block, slug
        assert f'href="/prompts/{page.parent.name}/"' in block, slug
