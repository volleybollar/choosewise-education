#!/usr/bin/env python3
"""Bygger de tre Word-mallarna på sidan Quality Ladder (A4, en sida var).

    quality-ladder-routine.docx   elevblad: de fyra stegen, yngre elever och skrivrader
    whole-class-feedback.docx     mall för helklassåterkoppling, med plats för lärarens anteckningar
    feedback-policy.docx          återkopplingspolicy med [platshållare] markerade

Texten kommer från samma hjälpfunktioner som kopieringsknapparna på sidan
(routine_text, whole_class_text, policy_text i scripts/build-quality-ladder.py),
så filerna och sidan har alltid exakt samma ord. Layouten (rubriker, skrivrader,
anteckningsrutor) läggs på här.

Filerna skrivs till quality-ladder-ec1c2f8c/ bredvid sidan som länkar till dem.

Användning:
    /usr/bin/python3 exports/build-quality-ladder-docx.py
"""
from __future__ import annotations

import importlib.util
import json
import re
from datetime import datetime
from pathlib import Path

from docx import Document
from docx.enum.text import WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
SLUG = "quality-ladder-ec1c2f8c"

# Samma blå som rubrikerna på sajten: --color-accent i assets/css/tokens.css.
NAVY = RGBColor(0x0B, 0x3A, 0x6F)
SOFT = RGBColor(0x4E, 0x5A, 0x68)   # --color-text-soft, för vägledningstext
LINE = "9AA7B5"                      # grå för skrivrader och rutor
AUTHOR = "Choosewise.education"
TEXT_WIDTH_CM = 17                   # 21 cm minus 2 x 2 cm marginal
FIXED_DATE = datetime(2026, 11, 14)   # fast datum i dokumentegenskaperna
TEXT_WIDTH_TWIPS = 9638              # samma bredd i twips (1 cm = 566,9)


def _load_helpers():
    """Hämtar textfunktionerna ur sidbyggaren (filnamnet har bindestreck, så importlib)."""
    path = ROOT / "scripts/build-quality-ladder.py"
    spec = importlib.util.spec_from_file_location("build_quality_ladder", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ───── Byggstenar ─────

def _new_document(title: str) -> Document:
    """A4 stående, 2 cm marginal, Arial 11 och dokumentegenskaperna."""
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.left_margin = sec.right_margin = sec.top_margin = sec.bottom_margin = Cm(2)

    normal = doc.styles["Normal"]
    # Arial finns på Mac utan Office, på Windows och i Google Docs.
    normal.font.name = "Arial"
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    normal.element.rPr.rFonts.set(qn("w:cs"), "Arial")
    normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(6)

    doc.core_properties.author = AUTHOR
    doc.core_properties.last_modified_by = AUTHOR
    doc.core_properties.title = title
    # Fasta värden så att bygget är reproducerbart och ingen gammal metadata
    # ("python-docx"-kommentaren, mallens datum) syns för lärarna.
    doc.core_properties.created = FIXED_DATE
    doc.core_properties.modified = FIXED_DATE
    doc.core_properties.comments = ""
    return doc


def _title(doc: Document, text: str) -> None:
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(20)
    r.font.color.rgb = NAVY
    p.paragraph_format.space_after = Pt(8)


def _heading(doc: Document, text: str) -> None:
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = NAVY
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True


def _guide(doc: Document, text: str) -> None:
    """Vägledningen under en rubrik: mindre och grå, så att den inte tar över."""
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(10)
    r.font.color.rgb = SOFT
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True


def _notes_box(doc: Document, height_cm: float) -> None:
    """En tom ruta med ram över hela textbredden: plats för elevens eller lärarens text.

    Bredden sätts uttryckligen (17 cm = A4 minus 2 x 2 cm marginal) och tabellen låses med
    fast layout, vilket Word och Google Dokument följer. Rutan har ett enda tomt stycke i
    normal storlek, så att den som skriver hamnar i vanlig text. Quick Look ignorerar
    bredden och kan visa en smalare ruta; den förhandsvisningen är godtagen."""
    table = doc.add_table(rows=1, cols=1)
    table.autofit = False                      # w:tblLayout fixed, på rätt plats i tblPr
    tblpr = table._tbl.tblPr
    tbl_w = tblpr.find(qn("w:tblW"))
    tbl_w.set(qn("w:type"), "dxa")
    tbl_w.set(qn("w:w"), str(TEXT_WIDTH_TWIPS))
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right"):
        b = OxmlElement(f"w:{side}")
        for key, val in (("val", "single"), ("sz", "4"), ("space", "0"), ("color", LINE)):
            b.set(qn(f"w:{key}"), val)
        borders.append(b)
    # Schemat kräver w:tblBorders före w:tblLayout och w:tblLook.
    tblpr.find(qn("w:tblLayout")).addprevious(borders)
    table.columns[0].width = Cm(TEXT_WIDTH_CM)
    row = table.rows[0]
    h = OxmlElement("w:trHeight")
    h.set(qn("w:val"), str(int(height_cm * 567)))   # 1 cm = 567 twips
    h.set(qn("w:hRule"), "atLeast")
    row._tr.get_or_add_trPr().append(h)
    cell = row.cells[0]
    cell.width = Cm(TEXT_WIDTH_CM)
    cell.paragraphs[0].paragraph_format.space_after = Pt(0)


def _highlighted(paragraph, text: str) -> None:
    """Skriver text i ett stycke och markerar [platshållare] med gul överstrykning."""
    for part in re.split(r"(\[[^\]]+\])", text):
        if not part:
            continue
        run = paragraph.add_run(part)
        if part.startswith("[") and part.endswith("]"):
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW


# ───── De tre dokumenten ─────

def _routine(h, data: dict, dst: Path) -> None:
    """Elevblad. Ordningen och orden följer routine_text; en skrivruta ligger under varje fråga."""
    r = data["routine"]
    doc = _new_document("Quality Ladder — student sheet")
    _title(doc, "Quality Ladder — student sheet")
    # Rubriken och raderna "1. …" är samma text som i routine_text.
    _heading(doc, h.routine_text(r).split("\n", 1)[0])
    for i, step in enumerate(r["steps"], start=1):
        doc.add_paragraph(f"{i}. {step}").paragraph_format.space_after = Pt(3)
    p = doc.add_paragraph(r["younger"])
    p.paragraph_format.space_before = Pt(6)
    for run in p.runs:
        run.italic = True
        run.font.color.rgb = SOFT

    # Frågorna på elevbladet: en skrivruta under varje, "My new version" får en hög.
    for prompt in r["sheet"]:
        _heading(doc, prompt)
        _notes_box(doc, 7.0 if prompt.startswith("My new version") else 2.0)
    doc.save(str(dst))


def _whole_class(data: dict, dst: Path) -> None:
    """Mall för helklassåterkoppling: rubrik, vägledning och en anteckningsruta per avsnitt."""
    wc = data["whole_class"]
    doc = _new_document("Whole-class feedback")
    _title(doc, "Whole-class feedback")
    doc.add_paragraph(wc["intro"])
    for sec in wc["sections"]:
        _heading(doc, sec["heading"])
        _guide(doc, sec["guide"])
        _notes_box(doc, 1.4)
    p = doc.add_paragraph(wc["followup"])
    p.paragraph_format.space_before = Pt(10)
    doc.save(str(dst))


def _policy(data: dict, dst: Path) -> None:
    """Policyn: samma rader som policy_text, med [platshållare] gulmarkerade."""
    policy = data["policy"]
    doc = _new_document("Feedback policy")
    _title(doc, "Feedback policy")
    _highlighted(doc.add_paragraph(), policy["intro"])
    for i, pr in enumerate(policy["principles"], start=1):
        source = f" ({pr['source']})" if pr["source"] else ""
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(f"{i}. {pr['title']}")
        run.bold = True
        run.font.color.rgb = NAVY
        _highlighted(p, f": {pr['text']}{source}")
    doc.save(str(dst))


def build_docx(root: Path) -> list[Path]:
    """Skriver de tre filerna i mappen `root` och returnerar sökvägarna."""
    h = _load_helpers()
    data = json.loads((ROOT / SLUG / "ladder-en.json").read_text(encoding="utf-8"))
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    jobs = (
        ("quality-ladder-routine.docx", lambda d, dst: _routine(h, d, dst)),
        ("whole-class-feedback.docx", _whole_class),
        ("feedback-policy.docx", _policy),
    )
    out = []
    for name, fn in jobs:
        dst = root / name
        fn(data, dst)
        out.append(dst)
    return out


if __name__ == "__main__":
    for path in build_docx(ROOT / SLUG):
        print(path.relative_to(ROOT))
