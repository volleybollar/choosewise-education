#!/usr/bin/env python3
"""Bygger Word-bladet på sidan Ideas first (A4, en sida).

    team-idea-sheet.docx   teambladet: mål, idéer före AI, det AI gav, vad teamet valde

Orden kommer ur samma JSON-fil som sidan (ideas-en.json, nyckeln team.sheet) och
skrivs i samma ordning som sheet_text() i scripts/build-ideas-first.py; testet i
scripts/tests/test_ideas_first_docx.py kontrollerar rad för rad att filen och sidan
har exakt samma ord. Layouten (rubriker, rutor, tabeller) läggs på här.

Hjälpfunktionerna (Arial, rubrikstilarna Heading 1 och 2, ramade rutor, tabeller
med fast bredd 9638 dxa) hämtas från build-paperwork-pack-docx.py. Bara
dokumentdatumet byts mot 2026-11-26.

Filen skrivs till ideas-first-778ba230/ bredvid sidan som länkar till den.

Användning:
    /usr/bin/python3 exports/build-ideas-first-docx.py
"""
from __future__ import annotations

import importlib.util
import json
from datetime import datetime
from pathlib import Path

from docx.shared import Pt

ROOT = Path(__file__).resolve().parent.parent
SLUG = "ideas-first-778ba230"
FIXED_DATE = datetime(2026, 11, 26)   # fast datum i dokumentegenskaperna


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pp = _load(ROOT / "exports/build-paperwork-pack-docx.py", "pp_docx_helpers")

# Låga rutor och rader så att hela bladet ryms på en A4-sida.
HEADER_ROW_CM = 1.0    # raden Subject / Grade / Goal / Date
BEFORE_ROW_CM = 0.8    # tom rad i tabellen "Ideas before AI"
BOX_CM = 2.8           # rutan för det AI:n gav
CHOSE_ROW_CM = 0.9     # tom rad i tabellen "What we chose and changed"
# Goal får mer plats än de andra; andelarna av textbredden (summerar till 9638).
HEADER_WIDTHS = [2300, 1500, 3638, 2200]


def _new_document(title: str):
    doc = pp._new_document(title)
    doc.core_properties.created = FIXED_DATE
    doc.core_properties.modified = FIXED_DATE
    return doc


def _heading2(doc, text: str, before: int = 6):
    h = doc.add_heading(text, level=2)
    h.paragraph_format.space_before = Pt(before)
    return h


def _header_row(doc, labels: list[str]) -> None:
    """En rad med ram där varje cell börjar med sin etikett och har plats att skriva efter."""
    table = pp._table(doc, HEADER_WIDTHS, rows=1)
    pp._row_height(table.rows[0], HEADER_ROW_CM)
    for cell, text in zip(table.rows[0].cells, labels):
        run = cell.paragraphs[0].add_run(text)
        run.bold = True
        run.font.size = Pt(10)


def build_docx(root: Path) -> list[Path]:
    """Skriver filen i mappen `root` och returnerar sökvägen. Ordningen följer sheet_text()."""
    s = json.loads((ROOT / SLUG / "ideas-en.json").read_text(encoding="utf-8"))["team"]["sheet"]
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)

    doc = _new_document(s["title"])
    doc.add_heading(s["title"], level=1)
    _header_row(doc, [f"{h}:" for h in s["header"]])

    # Anteckningen om att inga namn går in i AI, kursiv rad direkt under huvudet.
    p = doc.add_paragraph()
    p.add_run(s["note"]).italic = True
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(0)

    # Rutinen som riktig numrerad lista (stilen List Number), så texten är exakt JSON-raden.
    _heading2(doc, s["routine_heading"])
    for line in s["routine"]:
        item = doc.add_paragraph(line, style="List Number")
        item.paragraph_format.space_after = Pt(2)
        for run in item.runs:
            run.font.size = Pt(10)

    _heading2(doc, s["before_ai"]["heading"])
    pp._grid(doc, s["before_ai"]["columns"], s["before_ai"]["rows"], BEFORE_ROW_CM)

    _heading2(doc, s["from_ai"]["heading"])
    hint = doc.add_paragraph(s["from_ai"]["hint"])
    hint.paragraph_format.space_after = Pt(3)
    hint.paragraph_format.keep_with_next = True
    for run in hint.runs:
        run.font.size = Pt(10)
    pp._box(doc, BOX_CM)

    _heading2(doc, s["chose"]["heading"])
    pp._grid(doc, s["chose"]["columns"], s["chose"]["rows"], CHOSE_ROW_CM)
    pp._closing_paragraph(doc)

    dst = root / "team-idea-sheet.docx"
    doc.save(str(dst))
    return [dst]


if __name__ == "__main__":
    for path in build_docx(ROOT / SLUG):
        print(path.relative_to(ROOT))
