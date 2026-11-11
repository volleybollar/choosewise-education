#!/usr/bin/env python3
"""Build the student PDF for every AI lesson from its lesson-en.json.

For every lesson in every track of scripts/build-ai-lessons.py this writes
  _unpublished/exports/ai-lessons/<id>-student-a4-en.html   the HTML source
  <slug>/<id>/<student_pdf.file>                            the PDF, in the hidden folder

Each page in student_pdf.pages has a title, a short instruction and blocks:
  text       {body, big?}           a line of text; big for the training text (at least 16 pt)
  table      {columns, rows}        an empty table to fill in
  slips      {count, label}         slips to fold and tear along dashed lines
  checklist  {items, checks}        one row per item, one tick box per check
  tickets    {question, count}      closing-question tickets to cut off

The PDF is A4. Every page is a box of 210 × 279 mm, centred on the A4 page,
with the content inside 190 × 265 mm, so nothing is clipped when a teacher
prints it at 100 % on US Letter.
Black-and-white friendly: no meaning carried by colour alone.

Usage:
    /usr/bin/python3 exports/build-ai-lessons-pdf.py
"""
from __future__ import annotations

import importlib.util
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "_unpublished/exports/ai-lessons"

# Samma typsnitt och färger som de andra paketen (exports/_guide-print.css, Hanken Grotesk 300–500).
STYLE = """
/* Sidrutan står mitt på A4 (9 mm marginal upptill och nedtill). Skrivs A4 ut i
   100 % på US Letter försvinner just de 9 mm, och ingenting klipps. */
@page { size: A4; margin: 9mm 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: white; }
body { font-family: var(--font-body); color: var(--color-text); font-size: 12pt; line-height: 1.4; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
strong, b { font-weight: 500; }
/* Sidrutan: 210 × 279 mm, innehållet högst 190 × 265 mm. */
.page { width: 210mm; height: 279mm; margin: 0 auto; padding: 7mm 10mm; display: flex; flex-direction: column; gap: 5mm; page-break-after: always; overflow: hidden; }
.page:last-child { page-break-after: auto; }
/* Sidhuvud: sidnummer i en ring, rubrik och en kort instruktion med symbol. */
.head { display: flex; gap: 4mm; align-items: center; border-bottom: 0.4mm solid var(--color-text); padding-bottom: 3mm; }
.num { flex: none; display: grid; place-items: center; width: 12mm; height: 12mm; border-radius: 50%; border: 0.5mm solid var(--color-text); font-size: 16pt; font-weight: 500; }
h1 { font-family: var(--font-display); font-size: 22pt; font-weight: 500; line-height: 1.1; }
.instr { display: flex; gap: 2.5mm; align-items: center; font-size: 14pt; margin-top: 1mm; }
.instr svg { width: 7mm; height: 7mm; flex: none; }
/* Blocken. */
.text { font-size: 13pt; }
.text--big { font-size: 21pt; line-height: 1.8; border: 0.3mm solid var(--color-text-muted); border-radius: 2mm; padding: 6mm 7mm; }
.grid { width: 100%; border-collapse: collapse; font-size: 12pt; }
.grid th { text-align: left; font-weight: 500; border-bottom: 0.4mm solid var(--color-text); padding: 2mm; }
.grid td { height: 14mm; border-bottom: 0.3mm solid var(--color-text-muted); }
.grid--fill th:first-child, .grid--fill td:first-child { width: 35%; }
.grid--fill th:last-child, .grid--fill td:last-child { width: 15%; }
.grid .row-num { width: 14mm; font-weight: 500; text-align: center; }
.box { display: inline-block; width: 7mm; height: 7mm; border: 0.4mm solid var(--color-text); border-radius: 1mm; }
.grid .tick { text-align: center; }
.slips { display: grid; grid-template-columns: repeat(4, 1fr); border-top: 0.4mm dashed var(--color-text); border-left: 0.4mm dashed var(--color-text); }
.slip { height: 30mm; border-right: 0.4mm dashed var(--color-text); border-bottom: 0.4mm dashed var(--color-text); padding: 2mm 3mm; display: flex; flex-direction: column; justify-content: space-between; }
.slip__label { font-size: 8pt; color: var(--color-text-muted); }
.slip__line { border-bottom: 0.3mm solid var(--color-text-muted); height: 8mm; }
.tickets { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0; border-top: 0.4mm dashed var(--color-text); }
.ticket { padding: 4mm 4mm 2mm; display: flex; flex-direction: column; gap: 2mm; }
.ticket + .ticket { border-left: 0.4mm dashed var(--color-text); }
.ticket__q { font-size: 12pt; font-weight: 500; }
.ticket__name { font-size: 10pt; color: var(--color-text-soft); }
.ticket__line { border-bottom: 0.3mm solid var(--color-text-muted); height: 9mm; }
.cut { font-size: 9pt; color: var(--color-text-muted); margin-bottom: -3mm; }
/* Sidfot på varje sida; användningsraden på sidan 1. */
.foot { margin-top: auto; font-size: 8pt; color: var(--color-text-muted); border-top: 0.3mm solid var(--color-border); padding-top: 2mm; }
.rights { margin-bottom: 1.5mm; color: var(--color-text-soft); }
"""

# Enkla symboler i stället för text, så att instruktionen går att förstå
# utan att kunna läsa engelska. Väljs efter sidans viktigaste block.
ICONS = {
    "text": '<circle cx="10" cy="10" r="6"/><path d="M14.5 14.5 20 20"/>',
    "table": '<path d="M5 5v14M9 5v14M13 5v14M17 5v14M3 16 19 8"/>',
    "slips": '<path d="M5 8h14l-2 12H7z"/><path d="M9 8V4h6v4"/>',
    "checklist": '<rect x="4" y="4" width="16" height="16" rx="2"/><path d="m8 12 3 3 5-6"/>',
    "tickets": '<path d="M4 20l4-1 11-11-3-3L5 16z"/>',
}


def _load_build():
    spec = importlib.util.spec_from_file_location("build_ai_lessons", ROOT / "scripts/build-ai-lessons.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _icon(page: dict) -> str:
    kinds = [b["kind"] for b in page["blocks"] if b["kind"] != "text"] or ["text"]
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[kinds[0]]}</svg>')


def _text(block: dict) -> str:
    cls = "text text--big" if block.get("big") else "text"
    return f'<p class="{cls}">{escape(block["body"])}</p>'


def _table(block: dict) -> str:
    head = "".join(f"<th>{escape(c)}</th>" for c in block["columns"])
    row = "<tr>" + "<td></td>" * len(block["columns"]) + "</tr>"
    return f'<table class="grid grid--fill"><thead><tr>{head}</tr></thead><tbody>{row * block["rows"]}</tbody></table>'


def _slips(block: dict) -> str:
    slip = (f'<div class="slip"><span class="slip__label">{escape(block["label"])}</span>'
            '<span class="slip__line"></span></div>')
    return f'<div class="slips">{slip * block["count"]}</div>'


def _checklist(block: dict) -> str:
    head = "<th class=\"row-num\">#</th>" + "".join(f'<th class="tick">{escape(c)}</th>' for c in block["checks"])
    ticks = "".join('<td class="tick"><span class="box"></span></td>' for _ in block["checks"])
    rows = "".join(f'<tr><td class="row-num">{n}</td>{ticks}</tr>' for n in range(1, block["items"] + 1))
    return f'<table class="grid"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>'


def _tickets(block: dict) -> str:
    ticket = (f'<div class="ticket"><p class="ticket__q">{escape(block["question"])}</p>'
              '<p class="ticket__name">Name:</p>' + '<span class="ticket__line"></span>' * 4 + "</div>")
    return f'<p class="cut">Cut or tear along the dashed lines.</p><div class="tickets">{ticket * block["count"]}</div>'


BLOCKS = {"text": _text, "table": _table, "slips": _slips, "checklist": _checklist, "tickets": _tickets}


def _page(lesson: dict, page: dict, n: int, total: int, rights: str) -> str:
    blocks = "".join(BLOCKS[b["kind"]](b) for b in page["blocks"])
    rights_line = f'<p class="rights">{escape(rights)}</p>' if n == 1 else ""
    return (
        f'<section class="page">'
        f'<header class="head"><span class="num">{n}</span><div><h1>{escape(page["title"])}</h1>'
        f'<p class="instr">{_icon(page)}{escape(page["instruction"])}</p></div></header>'
        f"{blocks}"
        f'<footer class="foot">{rights_line}<p>{escape(lesson["title"])} · choosewise.education · {n} / {total}</p></footer>'
        f"</section>"
    )


def render_student_html(track: dict, lesson: dict) -> str:
    """The complete HTML source of the student PDF. Same JSON in, same text out."""
    pages = lesson["student_pdf"]["pages"]
    body = "\n".join(_page(lesson, p, n, len(pages), track["use_rights"]) for n, p in enumerate(pages, start=1))
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n"
        f"<title>{escape(lesson['title'])} — student sheets</title>\n"
        f"<!-- Generated by exports/build-ai-lessons-pdf.py from {escape(track['slug'])}/{escape(lesson['id'])}/lesson-en.json. "
        "Edit the JSON or the script, not this file. -->\n"
        '<link rel="stylesheet" href="../../../exports/_guide-print.css">\n'
        f"<style>{STYLE}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n"
    )


def main() -> None:
    from playwright.sync_api import sync_playwright

    build = _load_build()
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for slug in build.TRACKS:
            track = build.load_track(ROOT, slug)
            for lesson in track["lesson_data"]:
                src = SRC_DIR / f"{lesson['id']}-student-a4-en.html"
                dst = ROOT / slug / lesson["id"] / lesson["student_pdf"]["file"]
                src.write_text(render_student_html(track, lesson), encoding="utf-8")
                page = browser.new_page()
                page.goto(src.as_uri(), wait_until="networkidle")
                page.emulate_media(media="print")
                page.pdf(path=str(dst), format="A4", print_background=True,
                         margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
                         prefer_css_page_size=True)
                page.close()
                print(f"Built {dst.relative_to(ROOT)} from {src.relative_to(ROOT)}")
        browser.close()


if __name__ == "__main__":
    main()
