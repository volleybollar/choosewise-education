#!/usr/bin/env python3
"""Bygger de två Word-filerna på sidan Barrier Planner (A4, en sida var).

    needs-and-measures.docx       formuläret: behov och insatser, att fylla i för hand
    popular-but-unsupported.docx  listan över populära men obelagda anpassningar

Orden kommer ur samma JSON-fil som kopieringsknapparna på sidan (planner-en.json)
och skrivs i samma ordning som record_text() och unsupported_text() i
scripts/build-barrier-planner.py; testet i scripts/tests/test_barrier_planner_docx.py
kontrollerar rad för rad att filerna och sidan har exakt samma ord. Layouten
(rubriker, rutor, tabeller) läggs på här.

Hjälpfunktionerna (Arial, rubrikstilarna Heading 1 och 2, ramade rutor, tabeller
med fast bredd 9638 dxa, avslutande 1 pt-stycke) hämtas från
build-paperwork-pack-docx.py. Bara dokumentdatumet byts mot 2026-11-25.

Filerna skrivs till barrier-planner-1c25533d/ bredvid sidan som länkar till dem.

Användning:
    /usr/bin/python3 exports/build-barrier-planner-docx.py
"""
from __future__ import annotations

import importlib.util
import json
from datetime import datetime
from pathlib import Path

from docx.shared import Pt

ROOT = Path(__file__).resolve().parent.parent
SLUG = "barrier-planner-1c25533d"
FIXED_DATE = datetime(2026, 11, 25)   # fast datum i dokumentegenskaperna


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pp = _load(ROOT / "exports/build-paperwork-pack-docx.py", "pp_docx_helpers")
page = _load(ROOT / "scripts/build-barrier-planner.py", "bp_page_helpers")

# Lägre rutor än Paperwork Packs så att hela formuläret ryms på en A4-sida.
NAME_ROW_CM = 1.1     # formulärhuvudet: rad med plats under etiketten
BOX_CM = 1.2          # skrivruta för de två fritextblocken
LINE_CM = 0.8         # kort ruta för granskningsdatumet
MEASURE_ROW_CM = 0.9  # tom rad i insatstabellen
OUTCOME_ROW_CM = 1.1  # skrivrad under Keep / Change / Stop


def _new_document(title: str):
    doc = pp._new_document(title)
    doc.core_properties.created = FIXED_DATE
    doc.core_properties.modified = FIXED_DATE
    return doc


def _heading2(doc, text: str, before: int = 6):
    h = doc.add_heading(text, level=2)
    h.paragraph_format.space_before = Pt(before)
    return h


def _hint(doc, text: str) -> None:
    """Ledtråden under en blockrubrik, hålls ihop med rutan under."""
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    for run in p.runs:
        run.font.size = Pt(10)


def _labels_row(doc, labels: list[str], height_cm: float) -> None:
    """En rad med ram där varje cell börjar med sin etikett och har plats att skriva under."""
    n = len(labels)
    widths = [pp.TEXT_WIDTH_TWIPS // n] * n
    widths[-1] += pp.TEXT_WIDTH_TWIPS - sum(widths)
    table = pp._table(doc, widths, rows=1)
    pp._row_height(table.rows[0], height_cm)
    for cell, text in zip(table.rows[0].cells, labels):
        run = cell.paragraphs[0].add_run(text)
        run.bold = True
        run.font.size = Pt(10)


def _numbered(doc, items: list[str]) -> None:
    for i, text in enumerate(items, 1):
        p = doc.add_paragraph(f"{i}. {text}")
        p.paragraph_format.space_after = Pt(2)
        for run in p.runs:
            run.font.size = Pt(10)


def _needs_and_measures(d: dict, dst: Path) -> None:
    """Ordningen och orden följer record_text(record)."""
    r = d["record"]
    doc = _new_document(page.RECORD_TITLE)
    doc.add_heading(page.RECORD_TITLE, level=1)

    # Varningen: första meningen fet, som på sidan. Direkt efter kommer formulärhuvudet.
    first, rest = r["warning"].split(". ", 1)
    p = doc.add_paragraph()
    p.add_run(first + ".").bold = True
    p.add_run(" " + rest)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    _labels_row(doc, [f"{h}:" for h in r["header"]], NAME_ROW_CM)

    for block in r["blocks"]:
        _heading2(doc, block["heading"])
        _hint(doc, block["hint"])
        kind = block["kind"]
        if kind == "box":
            pp._box(doc, BOX_CM)
        elif kind == "measures":
            pp._grid(doc, r["measure_columns"], 3, MEASURE_ROW_CM)
        elif kind == "line":
            pp._box(doc, LINE_CM)
        elif kind == "outcomes":
            pp._grid(doc, r["outcomes"], 1, OUTCOME_ROW_CM)

    _heading2(doc, page.REVIEW_QUESTIONS_TITLE)
    _numbered(doc, r["review_questions"])
    _heading2(doc, page.EEF_TITLE)
    _numbered(doc, r["eef_questions"])
    p = doc.add_paragraph(r["country_line"])
    p.paragraph_format.space_before = Pt(6)
    for run in p.runs:
        run.font.size = Pt(10)
    doc.save(str(dst))


def _unsupported(d: dict, dst: Path) -> None:
    """Ordningen och orden följer unsupported_text(u)."""
    u = d["unsupported"]
    doc = _new_document(page.UNSUPPORTED_TITLE)
    doc.add_heading(page.UNSUPPORTED_TITLE, level=1)
    for item in u["items"]:
        doc.add_heading(item["title"], level=2)
        p = doc.add_paragraph(item["research"])
        p.paragraph_format.space_after = Pt(3)
        p = doc.add_paragraph()
        p.add_run("Instead:").bold = True
        p.add_run(" " + item["instead"])
    p = doc.add_paragraph(u["movement_note"])
    p.paragraph_format.space_before = Pt(8)
    doc.save(str(dst))


def build_docx(root: Path) -> list[Path]:
    """Skriver de två filerna i mappen `root` och returnerar sökvägarna."""
    d = json.loads((ROOT / SLUG / "planner-en.json").read_text(encoding="utf-8"))
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    out = []
    for name, build in (("needs-and-measures.docx", _needs_and_measures),
                        ("popular-but-unsupported.docx", _unsupported)):
        dst = root / name
        build(d, dst)
        out.append(dst)
    return out


if __name__ == "__main__":
    for path in build_docx(ROOT / SLUG):
        print(path.relative_to(ROOT))
