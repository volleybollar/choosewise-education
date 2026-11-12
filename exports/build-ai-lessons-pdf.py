#!/usr/bin/env python3
"""Build the student PDF for every AI lesson from its lesson-en.json.

For every lesson in every track of scripts/build-ai-lessons.py this writes
  _unpublished/exports/ai-lessons/<id>-<band>-student-a4-en.html   the HTML source
  <slug>/<id>/<student_pdf.file>                            the PDF, in the hidden folder

Each page in student_pdf.pages has a title, a short instruction and blocks:
  text       {body, big?}           a line of text; big for the training text (at least 16 pt)
  table      {columns, rows, tall?} a table to fill in: rows is a number of empty rows,
                                    or a list of rows with one text per column ("" = empty);
                                    tall gives rows with room for two lines of handwriting
  slips      {count, label}         slips to fold and tear along dashed lines
  checklist  {items, checks}        one row per item, one tick box per check
  tickets    {question, count, draw?} closing-question tickets to cut off; draw gives a box
                                    to draw in instead of lines, for children who can't write yet
  cards      {cards, heading?}      picture cards to cut out: [{word, icon?}], 4 per row
  mat        {headings, icons?}     a sorting mat, one column per heading; icons puts a Tabler
                                    picture above each heading
  image      {src, alt}             a picture from the repo (src relative to the repo root)
  images     {items}                labelled pictures two by two: [{src, label, alt}]
  draw       {label}                a big box to draw in, filling the rest of the page
A checklist's items are a number (numbered rows) or a list of row labels.

Card pictures are Tabler Icons (MIT) in _unpublished/exports/ai-lessons/icons/;
only their drawing elements reach the PDF. A card without a picture gets an
empty box for students to draw in.

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
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "_unpublished/exports/ai-lessons"
ICON_DIR = SRC_DIR / "icons"
DRAWING = {"path", "circle", "line", "rect", "polyline", "polygon", "ellipse"}
GEOMETRY = {"d", "cx", "cy", "r", "rx", "ry", "x", "y", "width", "height", "x1", "y1", "x2", "y2", "points"}

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
/* Förtryckta tabeller: luft i cellerna, och kolumnerna så breda som innehållet kräver. */
.grid--data td { padding: 0 2mm; }
.grid--data th:first-child, .grid--data td:first-child, .grid--data th:last-child, .grid--data td:last-child { width: auto; }
/* Höga rader: plats för två rader handstil. */
.grid--tall td { height: 18mm; }
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
/* Rita i stället för att skriva (5–8): en ruta där linjerna annars står. */
.ticket__draw { min-height: 40mm; border: 0.3mm dashed var(--color-text-muted); border-radius: 2mm; }
.cut { font-size: 9pt; color: var(--color-text-muted); margin-bottom: -3mm; }
.grid .row-label { width: 45%; padding: 2mm; }
/* Bildkort: fyra per rad, streckade klipplinjer runt varje kort. */
.cards__heading { font-size: 12pt; font-weight: 500; margin-bottom: -2mm; }
.cards { display: grid; grid-template-columns: repeat(4, 1fr); }
.card { height: 52mm; border: 0.3mm dashed var(--color-text); margin: 0 -0.3mm -0.3mm 0; padding: 3mm; display: flex; flex-direction: column; align-items: center; justify-content: space-between; text-align: center; }
.card__pic { width: 26mm; height: 26mm; display: grid; place-items: center; }
.card__pic svg { width: 24mm; height: 24mm; color: var(--color-text); }
.card__pic--draw { border: 0.3mm dashed var(--color-text-muted); border-radius: 2mm; font-size: 9pt; color: var(--color-text-muted); }
.card__word { font-size: 13pt; font-weight: 500; line-height: 1.2; }
/* Sorteringsmatta: en kolumn per rubrik, fyller resten av sidan. */
.mat { flex: 1; min-height: 60mm; display: grid; border: 0.4mm solid var(--color-text); border-radius: 2mm; }
.mat__col + .mat__col { border-left: 0.4mm solid var(--color-text); }
.mat__head { min-height: 22mm; display: flex; flex-direction: column; gap: 1.5mm; align-items: center; justify-content: center; font-size: 15pt; font-weight: 500; text-align: center; padding: 3mm; border-bottom: 0.3mm solid var(--color-text-muted); }
/* Bild över mattans rubrik, för den som inte läser än. */
.mat__pic { display: block; width: 14mm; height: 14mm; color: var(--color-text); }
.mat__pic svg { width: 100%; height: 100%; }
/* Ritruta: fyller resten av sidan. */
.draw { flex: 1; min-height: 60mm; display: flex; flex-direction: column; gap: 2mm; }
.draw__label { font-size: 12pt; font-weight: 500; }
.draw__box { flex: 1; border: 0.4mm solid var(--color-text); border-radius: 2mm; }
.image { display: block; max-width: 100%; max-height: 150mm; margin: 0 auto; object-fit: contain; }
.images { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm 6mm; max-width: 170mm; margin: 0 auto; }
.images figure { margin: 0; text-align: center; }
.images img { display: block; max-width: 100%; max-height: 70mm; margin: 0 auto; object-fit: contain; }
.images figcaption { margin-top: 1.5mm; font-size: 12pt; }
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
    "cards": '<rect x="3" y="6" width="12" height="15" rx="2"/><path d="M9 3h10a2 2 0 0 1 2 2v13"/>',
    "mat": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M9 4v16M15 4v16"/>',
    "image": '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 17-5-5-9 7"/>',
    "draw": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 15c2-4 4 0 6-3s3-2 4-1"/>',
    "images": '<rect x="3" y="3" width="8" height="8" rx="1"/><rect x="13" y="3" width="8" height="8" rx="1"/><rect x="3" y="13" width="8" height="8" rx="1"/><rect x="13" y="13" width="8" height="8" rx="1"/>',
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
    cls = "grid grid--fill"
    if isinstance(block["rows"], list):  # förtryckta rader; tom text = en ruta att fylla i
        cls += " grid--data"
        body = "".join("<tr>" + "".join(f"<td>{escape(c)}</td>" for c in row) + "</tr>" for row in block["rows"])
    else:
        body = ("<tr>" + "<td></td>" * len(block["columns"]) + "</tr>") * block["rows"]
    if block.get("tall"):
        cls += " grid--tall"
    return f'<table class="{cls}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def _slips(block: dict) -> str:
    slip = (f'<div class="slip"><span class="slip__label">{escape(block["label"])}</span>'
            '<span class="slip__line"></span></div>')
    return f'<div class="slips">{slip * block["count"]}</div>'


def _checklist(block: dict) -> str:
    ticks = "".join('<td class="tick"><span class="box"></span></td>' for _ in block["checks"])
    checks = "".join(f'<th class="tick">{escape(c)}</th>' for c in block["checks"])
    if isinstance(block["items"], list):  # rader med text, t.ex. situationer
        head = '<th class="row-label"></th>' + checks
        rows = "".join(f'<tr><td class="row-label">{escape(item)}</td>{ticks}</tr>' for item in block["items"])
    else:  # numrerade rader
        head = "<th class=\"row-num\">#</th>" + checks
        rows = "".join(f'<tr><td class="row-num">{n}</td>{ticks}</tr>' for n in range(1, block["items"] + 1))
    return f'<table class="grid"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>'


def _tickets(block: dict) -> str:
    room = '<span class="ticket__draw"></span>' if block.get("draw") else '<span class="ticket__line"></span>' * 4
    ticket = (f'<div class="ticket"><p class="ticket__q">{escape(block["question"])}</p>'
              f'<p class="ticket__name">Name:</p>{room}</div>')
    return f'<p class="cut">Cut or tear along the dashed lines.</p><div class="tickets">{ticket * block["count"]}</div>'


def load_icon(name: str) -> str | None:
    """The drawing elements of an icon, with only their geometry: no scripts,
    links or event attributes can reach a PDF. None if the file is missing."""
    path = ICON_DIR / f"{name}.svg"
    if not path.exists():
        return None
    out = []
    for el in ElementTree.fromstring(path.read_text(encoding="utf-8")).iter():
        tag = el.tag.rsplit("}", 1)[-1]
        if tag not in DRAWING or el.get("stroke") == "none":
            continue  # Tablers osynliga ram har stroke="none"
        attrs = " ".join(f'{k}="{escape(v)}"' for k, v in el.attrib.items() if k in GEOMETRY)
        out.append(f"<{tag} {attrs}/>")
    return "".join(out)


def _tabler_svg(drawing: str) -> str:
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{drawing}</svg>')


def _card(card: dict) -> str:
    drawing = load_icon(card["icon"]) if card.get("icon") else None
    if drawing:
        pic = f'<div class="card__pic">{_tabler_svg(drawing)}</div>'
    else:
        pic = '<div class="card__pic card__pic--draw">draw it</div>'
    return f'<div class="card">{pic}<div class="card__word">{escape(card["word"])}</div></div>'


def _cards(block: dict) -> str:
    heading = f'<p class="cards__heading">{escape(block["heading"])}</p>' if block.get("heading") else ""
    return f'{heading}<div class="cards">{"".join(_card(c) for c in block["cards"])}</div>'


def _mat_pic(name: str) -> str:
    drawing = load_icon(name)
    if drawing is None:  # en matta utan bild går inte att läsa för den som inte läser än
        raise FileNotFoundError(f"Icon for the sorting mat is missing: {name}")
    return f'<span class="mat__pic">{_tabler_svg(drawing)}</span>'


def _mat(block: dict) -> str:
    pics = [_mat_pic(name) for name in block.get("icons", [])] or [""] * len(block["headings"])
    cols = "".join(f'<div class="mat__col"><p class="mat__head">{pic}{escape(h)}</p></div>'
                   for pic, h in zip(pics, block["headings"]))
    return f'<div class="mat" style="grid-template-columns: repeat({len(block["headings"])}, 1fr)">{cols}</div>'


def _image(block: dict) -> str:
    if not (ROOT / block["src"]).exists():
        raise FileNotFoundError(f"Picture for the student PDF is missing: {block['src']}")
    return f'<img class="image" src="../../../{escape(block["src"])}" alt="{escape(block["alt"])}">'


def _images(block: dict) -> str:
    figures = []
    for item in block["items"]:
        img = _image(item).replace(' class="image"', "")  # rutnätets bilder har egen storlek i STYLE
        figures.append(f"<figure>{img}<figcaption>{escape(item['label'])}</figcaption></figure>")
    return f'<div class="images">{"".join(figures)}</div>'


def _draw(block: dict) -> str:
    return f'<div class="draw"><p class="draw__label">{escape(block["label"])}</p><div class="draw__box"></div></div>'


BLOCKS = {"text": _text, "table": _table, "slips": _slips, "checklist": _checklist, "tickets": _tickets,
          "cards": _cards, "mat": _mat, "image": _image, "images": _images, "draw": _draw}


def _uses_icons(lesson: dict) -> bool:
    blocks = [b for p in lesson["student_pdf"]["pages"] for b in p["blocks"]]
    return any(c.get("icon") for b in blocks for c in b.get("cards", [])) or any(b.get("icons") for b in blocks)


def _page(lesson: dict, page: dict, n: int, total: int, rights: str) -> str:
    blocks = "".join(BLOCKS[b["kind"]](b) for b in page["blocks"])
    rights_line = ""
    if n == 1:  # användningsraden, och krediten för kortbilderna (MIT) när PDF:en har sådana
        credit = " Card pictures: Tabler Icons (MIT licence)." if _uses_icons(lesson) else ""
        rights_line = f'<p class="rights">{escape(rights)}{credit}</p>'
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


def source_path(lesson: dict) -> Path:
    """The HTML source of a lesson's PDF. The band is in the name, because the
    same lesson id can be in two tracks (ai-or-human in 9–12 and 13–15)."""
    return SRC_DIR / f"{lesson['id']}-{lesson['band']}-student-a4-en.html"


def main() -> None:
    from playwright.sync_api import sync_playwright

    build = _load_build()
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for slug in build.TRACKS:
            track = build.load_track(ROOT, slug)
            for lesson in track["lesson_data"]:
                src = source_path(lesson)
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
