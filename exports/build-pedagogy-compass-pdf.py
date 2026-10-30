#!/usr/bin/env python3
"""Build the Pedagogy Compass poster (A4, 2 pages) from pedagogy-compass-59ecb8db/compass-en.json.

Page 1   the ten classroom problems, each with its models, strongest evidence first
Page 2   the model map: every model by category with its label, and the reply
         format of the prompt, for use without the website

The poster is for Skool members, so it lives in the hidden folder. Writes the
HTML source to _unpublished/exports/pedagogy-compass-poster-a4-en.html and the
PDF to pedagogy-compass-59ecb8db/pedagogy-compass-poster-en.pdf.

Usage:
    /usr/bin/python3 exports/build-pedagogy-compass-pdf.py
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "pedagogy-compass-59ecb8db"
DATA = ROOT / SLUG / "compass-en.json"
SRC = ROOT / "_unpublished/exports/pedagogy-compass-poster-a4-en.html"
DST = ROOT / SLUG / "pedagogy-compass-poster-en.pdf"
TITLE = "Pedagogy Compass"
PAGES = 2

# Svarsformatet, ordagrant som i assets/js/pedagogy-compass.js;
# test_format_lines_match_builder håller dem i takt.
FORMAT = [
    "Reply in plain text, no tables, in exactly this format:",
    "BEST FIRST STEP: which approach to try first and why, given what the teacher sees",
    "NEXT LESSON: what it looks like in one concrete lesson in this subject, with minutes",
    "WATCH FOR: how the teacher will know within two weeks whether it is working",
    "AI: one way AI could help the teacher with this, and one way students' use of AI could make the problem worse",
    "HONEST NOTE: what the evidence label means for this approach, in one or two lines",
]

# Samma tryckstil som de andra paketen (exports/_guide-print.css, Hanken Grotesk 300–500).
STYLE = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: var(--color-bg); }
body { font-family: var(--font-body); color: var(--color-text-soft); font-size: 9.6pt; line-height: 1.38; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
strong, b { font-weight: 500; }
.page { width: 210mm; height: 297mm; padding: 14mm 15mm 16mm; display: flex; flex-direction: column; gap: 3.5mm; page-break-after: always; overflow: hidden; }
.page:last-child { page-break-after: auto; }
h1, h2, h3 { font-family: var(--font-display); font-weight: 500; color: var(--color-text); }
.kicker { font-size: 7.5pt; letter-spacing: .12em; text-transform: uppercase; color: var(--color-highlight-ink); font-weight: 500; }
h1 { font-size: 26pt; font-weight: 300; letter-spacing: -.02em; line-height: 1.05; }
.lede { font-size: 10.4pt; color: var(--color-text); }
.problems { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm 6mm; }
.problem { border-top: 0.5mm solid var(--color-highlight); padding-top: 1.5mm; }
.problem h3 { font-size: 10.6pt; margin-bottom: .8mm; }
.problem ol { padding-left: 4.5mm; font-size: 8.8pt; color: var(--color-text); }
.map { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 3mm 5mm; }
.cat h3 { font-size: 10pt; margin-bottom: .8mm; display: flex; gap: 1.5mm; align-items: center; }
.cat ul { list-style: none; font-size: 8.3pt; color: var(--color-text); display: flex; flex-direction: column; gap: .2mm; }
.letter { display: inline-grid; place-items: center; width: 5mm; height: 5mm; border-radius: 50%; border: 0.3mm solid var(--color-accent); color: var(--color-accent); font-size: 7.5pt; }
.chip { display: inline-block; border: 0.3mm solid var(--color-accent); color: var(--color-accent); border-radius: 1mm; padding: 0 1.2mm; font-weight: 500; font-size: 6.8pt; font-family: var(--font-body); }
.chip--strong { background: var(--color-accent); color: var(--color-bg); }
.prompt { border: 0.35mm dashed var(--color-accent); border-radius: 1.5mm; padding: 3.5mm 5mm; font-family: 'SF Mono', Menlo, monospace; font-size: 7.4pt; line-height: 1.45; color: var(--color-text); white-space: pre-wrap; }
.note { font-size: 8.2pt; color: var(--color-text-muted); }
.foot { margin-top: auto; font-size: 7.5pt; color: var(--color-text-muted); border-top: 0.3mm solid var(--color-border); padding-top: 2.5mm; display: flex; justify-content: space-between; }
"""


def _foot(page_no: int) -> str:
    return f'<div class="foot"><span>{TITLE} · for Choosewise members</span><span>{page_no} / {PAGES}</span></div>'


def _chip(label: str, labels: dict) -> str:
    return f'<span class="chip chip--{escape(label)}">{escape(labels[label]["name"])}</span>'


def _problems_page(data: dict) -> str:
    models = {m["id"]: m for m in data["models"]}
    items = "".join(
        f'<div class="problem"><h3>{escape(p["name"])}</h3><ol>'
        + "".join(f"<li>{escape(models[mid]['name'])} {_chip(models[mid]['category'], data['labels'])}</li>" for mid in p["model_ids"])
        + "</ol></div>"
        for p in data["problems"]
    )
    return (
        '<section class="page">'
        '<div class="kicker">Pedagogy + AI · for Choosewise members</div>'
        f"<h1>{TITLE}</h1>"
        '<p class="lede">Start from what is going wrong. Each problem lists the models that address it, strongest evidence first.</p>'
        f'<div class="problems">{items}</div>'
        f"{_foot(1)}</section>"
    )


def _map_page(data: dict) -> str:
    cats = "".join(
        f'<div class="cat"><h3><span class="letter">{escape(c["letter"])}</span> {escape(c["name"])}</h3><ul>'
        + "".join(f"<li>{escape(m['name'])}</li>" for m in data["models"] if m["category"] == c["id"])
        + "</ul></div>"
        for c in data["categories"]
    )
    legend = " ".join(f'{_chip(k, data["labels"])} {escape(v["definition"])}' for k, v in data["labels"].items())
    return (
        '<section class="page">'
        '<div class="kicker">The model map</div>'
        '<h2 style="font-size:18pt">About fifty models, six categories</h2>'
        f'<div class="map">{cats}</div>'
        f'<p class="note">{legend}</p>'
        '<h2 style="font-size:12pt">Ask any AI tool</h2>'
        '<p class="note">Describe the problem, your subject and grade, and the approaches you are considering, '
        "strongest evidence first. Then ask for the reply in this format:</p>"
        f'<div class="prompt">{chr(10).join(FORMAT)}</div>'
        f"{_foot(2)}</section>"
    )


def render_poster_html(data: dict) -> str:
    """The complete HTML source of the poster. Same JSON in, same text out."""
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n"
        f"<title>{TITLE} — poster</title>\n"
        "<!-- Generated by exports/build-pedagogy-compass-pdf.py from pedagogy-compass-59ecb8db/compass-en.json. "
        "Edit the JSON or the script, not this file. -->\n"
        '<link rel="stylesheet" href="../../exports/_guide-print.css">\n'
        f"<style>{STYLE}</style>\n</head>\n<body>\n"
        + _problems_page(data) + "\n" + _map_page(data)
        + "\n</body>\n</html>\n"
    )


def main() -> None:
    from playwright.sync_api import sync_playwright

    data = json.loads(DATA.read_text(encoding="utf-8"))
    SRC.parent.mkdir(parents=True, exist_ok=True)
    SRC.write_text(render_poster_html(data), encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(SRC.as_uri(), wait_until="networkidle")
        page.emulate_media(media="print")
        page.pdf(path=str(DST), format="A4", print_background=True,
                 margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
                 prefer_css_page_size=True)
        browser.close()
    print(f"Built {DST.relative_to(ROOT)} from {SRC.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
