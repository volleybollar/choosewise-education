#!/usr/bin/env python3
"""Bygger de sex Word-mallarna på sidan Paperwork Pack (A4, en sida var).

    meeting-protocol.docx      mötesprotokoll: ett problem, ett beslut, en uppföljning
    information-note.docx      informationsnotis som ersätter ett informationsmöte
    skill-pairing.docx         parning kring en färdighet, med besök åt båda hållen
    cut-first-checklist.docx   tabell över återkommande dokument + fem kontroller
    letter-template.docx       enkelsidigt brev med [platshållare]
    messages-home.docx         fyra meddelanden hem och en termsplan

Orden kommer ur samma JSON-fil som kopieringsknapparna på sidan
(paperwork-en.json) och skrivs i samma ordning som template_text() i
scripts/build-paperwork-pack.py; testet i scripts/tests/test_paperwork_pack_docx.py
kontrollerar rad för rad att filerna och sidan har exakt samma ord.
Layouten (rubriker, rutor, tabeller) läggs på här.

Nytt jämfört med Quality Ladder: titeln och blockrubrikerna använder Words
inbyggda rubrikstilar ("Heading 1" och "Heading 2"), omformaterade till Arial,
marinblå och fetstil. Då fungerar Words navigeringsruta och skärmläsare hittar
rubrikerna. Hjälpfunktionerna är kopierade från build-quality-ladder-docx.py
i stället för importerade, så att Quality Ladder-filerna aldrig påverkas.

Filerna skrivs till paperwork-pack-f388fd9f/ bredvid sidan som länkar till dem.

Användning:
    /usr/bin/python3 exports/build-paperwork-pack-docx.py
"""
from __future__ import annotations

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
SLUG = "paperwork-pack-f388fd9f"

# Samma blå som rubrikerna på sajten: --color-accent i assets/css/tokens.css.
NAVY = RGBColor(0x0B, 0x3A, 0x6F)
LINE = "9AA7B5"                      # grå för ramar på rutor och tabeller
HEAD_FILL = "E8EEF5"                 # ljusblå bakgrund på tabellens rubrikrad
AUTHOR = "Choosewise.education"
TEXT_WIDTH_TWIPS = 9638              # 17 cm = A4 minus 2 x 2 cm marginal, i twips
FIXED_DATE = datetime(2026, 11, 23)  # fast datum i dokumentegenskaperna
# Rutornas och tabellradernas lägsta höjd (cm). En mall med många rutor (mötesprotokollet har
# sex plus en tabell) får lägre rutor för att rymmas på en A4-sida; rutorna växer när man skriver.
BOX_CM = 2.5                         # skrivruta i mall med få rutor
ROW_CM = 1.0                         # tom tabellrad
COMPACT_BOX_CM = 1.0                 # skrivruta i mall med många rutor
COMPACT_TALL_BOX_CM = 1.4            # rutan under uppföljningen i den mallen
COMPACT_ROW_CM = 0.7                 # tom tabellrad i den mallen
COMPACT_HEADING_BEFORE_PT = 4        # luft ovanför blockrubrikerna i den mallen (annars 8 pt)
COMPACT_FROM = 4                     # så många rutor eller fler gör mallen kompakt


# ───── Byggstenar ─────

def _style_heading(style, size_pt: int, before: int, after: int) -> None:
    """Gör en inbyggd rubrikstil till Arial, marinblå och fet.

    Wordmallens rubrikstilar pekar på temateckensnittet (asciiTheme, cstheme m.fl.). De attributen
    går före namnet och måste bort, annars blir rubrikerna Calibri Light/Cambria."""
    style.font.name = "Arial"
    rfonts = style.element.rPr.find(qn("w:rFonts"))
    for key in list(rfonts.attrib):
        if "theme" in key.lower():   # asciiTheme, hAnsiTheme, eastAsiaTheme och cstheme
            del rfonts.attrib[key]
    rfonts.set(qn("w:eastAsia"), "Arial")
    rfonts.set(qn("w:cs"), "Arial")
    style.font.size = Pt(size_pt)
    style.font.bold = True
    style.font.italic = False
    style.font.color.rgb = NAVY
    style.paragraph_format.space_before = Pt(before)
    style.paragraph_format.space_after = Pt(after)
    style.paragraph_format.keep_with_next = True


def _new_document(title: str) -> Document:
    """A4 stående, 2 cm marginal, Arial 11, rubrikstilarna och dokumentegenskaperna."""
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

    _style_heading(doc.styles["Heading 1"], 20, before=0, after=8)
    _style_heading(doc.styles["Heading 2"], 13, before=8, after=2)

    doc.core_properties.author = AUTHOR
    doc.core_properties.last_modified_by = AUTHOR
    doc.core_properties.title = title
    # Fasta värden så att bygget är reproducerbart och ingen gammal metadata
    # ("python-docx"-kommentaren, mallens datum) syns för lärarna.
    doc.core_properties.created = FIXED_DATE
    doc.core_properties.modified = FIXED_DATE
    doc.core_properties.comments = ""
    return doc


def _highlighted(paragraph, text: str) -> None:
    """Skriver text i ett stycke och markerar [platshållare] med gul överstrykning."""
    for part in re.split(r"(\[[^\]]+\])", text):
        if not part:
            continue
        run = paragraph.add_run(part)
        if part.startswith("[") and part.endswith("]"):
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW


def _table(doc: Document, widths: list[int], rows: int) -> "docx.table.Table":
    """En ramad tabell över hela textbredden med fast layout.

    Bredden sätts uttryckligen (kolumnerna summerar till 9638 dxa = 17 cm) och layouten
    låses som fast, vilket Word och Google Dokument följer. Quick Look ignorerar bredden
    och kan visa en smalare tabell; den förhandsvisningen är godtagen. Varje cell har ett
    enda tomt stycke i normal storlek, så att den som skriver hamnar i vanlig text."""
    table = doc.add_table(rows=rows, cols=len(widths))
    table.autofit = False                      # w:tblLayout fixed, på rätt plats i tblPr
    tblpr = table._tbl.tblPr
    tbl_w = tblpr.find(qn("w:tblW"))
    tbl_w.set(qn("w:type"), "dxa")
    tbl_w.set(qn("w:w"), str(sum(widths)))
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b = OxmlElement(f"w:{side}")
        for key, val in (("val", "single"), ("sz", "4"), ("space", "0"), ("color", LINE)):
            b.set(qn(f"w:{key}"), val)
        borders.append(b)
    # Schemat kräver w:tblBorders före w:tblLayout och w:tblLook.
    tblpr.find(qn("w:tblLayout")).addprevious(borders)
    for grid, w in zip(table._tbl.tblGrid.findall(qn("w:gridCol")), widths):
        grid.set(qn("w:w"), str(w))
    for row in table.rows:
        for cell, w in zip(row.cells, widths):
            tcw = cell._tc.get_or_add_tcPr().get_or_add_tcW()
            tcw.set(qn("w:type"), "dxa")
            tcw.set(qn("w:w"), str(w))
            cell.paragraphs[0].paragraph_format.space_after = Pt(0)
    return table


def _row_height(row, cm: float) -> None:
    h = OxmlElement("w:trHeight")
    h.set(qn("w:val"), str(int(cm * 567)))   # 1 cm = 567 twips
    h.set(qn("w:hRule"), "atLeast")
    row._tr.get_or_add_trPr().append(h)


def _box(doc: Document, height_cm: float) -> None:
    """En tom ruta med ram över hela textbredden: plats för det man skriver in."""
    table = _table(doc, [TEXT_WIDTH_TWIPS], rows=1)
    _row_height(table.rows[0], height_cm)


def _closing_paragraph(doc: Document) -> None:
    """Ett tomt stycke på 1 pt utan avstånd, sist efter en avslutande tabell.

    Word lägger alltid ett stycke efter en tabell som slutar dokumentet; det är 11 pt med 6 pt
    efter om vi inte skriver ett eget. På mötesprotokollet, som har minst marginal, kan det
    stycket annars ge en tom sida 2."""
    p = doc.add_paragraph()
    fmt = p.paragraph_format
    fmt.space_before = Pt(0)
    fmt.space_after = Pt(0)
    fmt.line_spacing = Pt(1)                    # exakt 1 pt radhöjd
    mark = OxmlElement("w:rPr")                 # styckets egen radbrytningsmarkering
    p._p.get_or_add_pPr().append(mark)          # rPr kommer sist i pPr, efter spacing
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "2")                    # halva punkter: 2 = 1 pt
    mark.append(sz)


def _grid(doc: Document, columns: list[str], rows: int, row_cm: float) -> None:
    """En tabell med rubrikrad och `rows` tomma rader. Kolumnerna är lika breda."""
    n = len(columns)
    widths = [TEXT_WIDTH_TWIPS // n] * n
    widths[-1] += TEXT_WIDTH_TWIPS - sum(widths)   # resten läggs i sista kolumnen
    table = _table(doc, widths, rows=rows + 1)
    head = table.rows[0]
    _row_height(head, 0.8)
    head._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))   # upprepas på ny sida
    for cell, text in zip(head.cells, columns):
        run = cell.paragraphs[0].add_run(text)
        run.bold = True
        run.font.size = Pt(10)
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), HEAD_FILL)
        cell._tc.get_or_add_tcPr().append(shd)
    for row in table.rows[1:]:
        _row_height(row, row_cm)


# ───── Ett dokument per mall ─────

def _template(t: dict, dst: Path) -> None:
    """Titel (Heading 1), ingress, sedan varje block: rubrik (Heading 2), rader, ruta eller tabell.

    Ordningen och orden följer template_text(t)."""
    doc = _new_document(t["title"])
    compact = sum(1 for b in t["blocks"] if b["box"]) >= COMPACT_FROM
    doc.add_heading(t["title"], level=1)
    doc.add_paragraph(t["intro"])
    for block in t["blocks"]:
        heading = doc.add_heading(block["heading"], level=2)
        if compact:
            # Word 2026-11-24: mötesprotokollet spillde en tabellrad till sida 2 med 8 pt och 1,2 cm rutor.
            heading.paragraph_format.space_before = Pt(COMPACT_HEADING_BEFORE_PT)
        if "columns" in block:
            _grid(doc, block["columns"], block["rows"], COMPACT_ROW_CM if compact else ROW_CM)
            continue
        lines = block["lines"]
        for i, line in enumerate(lines):
            p = doc.add_paragraph()
            _highlighted(p, line)
            last = i == len(lines) - 1
            p.paragraph_format.space_after = Pt(3 if not last or block["box"] else 6)
            # Rubrik, rader och ruta hålls ihop så att en ruta aldrig hamnar ensam på nästa sida.
            p.paragraph_format.keep_with_next = block["box"]
        if block["box"]:
            if not compact:
                height = BOX_CM
            else:
                height = COMPACT_TALL_BOX_CM if block["heading"] == "Follow-up" else COMPACT_BOX_CM
            _box(doc, height)
    if doc.element.body[-2].tag == qn("w:tbl"):
        _closing_paragraph(doc)             # body[-1] är sectPr
    doc.save(str(dst))


def build_docx(root: Path) -> list[Path]:
    """Skriver de sex filerna i mappen `root` och returnerar sökvägarna."""
    data = json.loads((ROOT / SLUG / "paperwork-en.json").read_text(encoding="utf-8"))
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    out = []
    for section in data["sections"]:
        for t in section["templates"]:
            dst = root / t["file"]
            _template(t, dst)
            out.append(dst)
    return out


if __name__ == "__main__":
    for path in build_docx(ROOT / SLUG):
        print(path.relative_to(ROOT))
