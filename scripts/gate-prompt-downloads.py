#!/usr/bin/env python3
"""Put the email gate on the English prompt-pack PDF links, and list every
English pack on /free/prompts/.

For each prompts/<page>/index.html that links /assets/pdfs/prompts/<slug>-en.pdf:
  - the <a> gets data-gate="prompts-<slug>-en" and data-gate-pdf, and loses
    `download` (otherwise the browser can fetch the file before the gate opens)
  - the page loads assets/js/mailerlite-gate.js once
Then free/prompts/index.html gets the full list between PACKS:START/END.

Swedish pages are never touched (sv/ is outside prompts/). Idempotent:
re-run after adding a new English pack.

    /usr/bin/python3 scripts/gate-prompt-downloads.py
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GATE_SCRIPT = '<script type="module" src="/assets/js/mailerlite-gate.js" defer></script>'
LINK_RE = re.compile(r'<a\b[^>]*href="/assets/pdfs/prompts/([a-z0-9-]+)-en\.pdf"[^>]*>')
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S)
LIST_RE = re.compile(r"(<!-- PACKS:START -->\n).*?(<!-- PACKS:END -->)", re.S)


def gate_tag(slug: str) -> str:
    pdf = f"/assets/pdfs/prompts/{slug}-en.pdf"
    return f'<a class="btn btn--primary" href="{pdf}" data-gate="prompts-{slug}-en" data-gate-pdf="{pdf}">'


def gate_page(path: Path) -> tuple[str, str] | None:
    """Gate one pack page. Returns (slug, title) if it is an English pack."""
    text = path.read_text(encoding="utf-8")
    m = LINK_RE.search(text)
    if not m:
        return None
    slug = m.group(1)
    new = LINK_RE.sub(lambda mm: gate_tag(mm.group(1)), text)
    if GATE_SCRIPT not in new:
        new = new.replace("</body>", f"  {GATE_SCRIPT}\n</body>", 1)
    if new != text:
        path.write_text(new, encoding="utf-8")
    title = re.sub(r"<[^>]+>", "", H1_RE.search(new).group(1)).strip()
    return slug, html.unescape(title)


def pack_list(packs: list[tuple[str, str, str]]) -> str:
    rows = []
    for page, slug, title in sorted(packs, key=lambda p: p[2].lower()):
        rows.append(
            f'        <li class="pack-list__item">\n'
            f'          <a class="pack-list__title" href="/prompts/{page}/">{html.escape(title)}</a>\n'
            f'          {gate_tag(slug)}PDF</a>\n'
            f'        </li>'
        )
    return '      <ul class="pack-list">\n' + "\n".join(rows) + "\n      </ul>\n"


def run(root: Path = ROOT) -> int:
    packs = []
    for path in sorted((root / "prompts").glob("*/index.html")):
        found = gate_page(path)
        if found:
            packs.append((path.parent.name, *found))
    hub = root / "free/prompts/index.html"
    text = hub.read_text(encoding="utf-8")
    new = LIST_RE.sub(lambda m: m.group(1) + pack_list(packs) + m.group(2), text)
    if new != text:
        hub.write_text(new, encoding="utf-8")
    return len(packs)


if __name__ == "__main__":
    n = run(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT)
    print(f"Gated {n} English prompt packs and listed them on /free/prompts/.")
