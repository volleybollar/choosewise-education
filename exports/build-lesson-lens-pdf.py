#!/usr/bin/env python3
"""Build the Lesson Lens card deck (A4, 14 pages) from lesson-lens/lenses-en.json.

Page 1      cover: how to use it, the start lens and the evidence labels
Pages 2–13  one card per lens, with its worked example complete
Page 14     a fill-in prompt for use without the website

Writes the HTML source to _unpublished/exports/lesson-lens-cards-a4-en.html
(so the PDF always has an editable source) and the PDF to
assets/pdfs/free/lesson-lens-cards-en.pdf.

Usage:
    /usr/bin/python3 exports/build-lesson-lens-pdf.py
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "lesson-lens/lenses-en.json"
SRC = ROOT / "_unpublished/exports/lesson-lens-cards-a4-en.html"
DST = ROOT / "assets/pdfs/free/lesson-lens-cards-en.pdf"
URL = "choosewise.education/lesson-lens"
TITLE = "Lesson Lens"

# Svarsformatet, ordagrant som i assets/js/lesson-lens.js;
# test_fill_in_matches_builder_prompt håller dem i takt.
PROMPT_PARTS = [
    "KEEP: one or two lines on what already works in this lesson and why.",
    "UPGRADE: at most two changes in total, numbered. Each must use this lesson's own content and be small enough to make this evening.",
    'NUDGE: one question, only if the research behind the lens (or lenses) points to a clearly stronger option than what is planned. Otherwise write "None".',
    "CHECK: what the teacher should look for in class to see whether it worked.",
]

# Kortens utseende: samma tryckstil som kortleken för Thinking Moves, och den
# delade exports/_guide-print.css, som laddar Hanken Grotesk 300–500.
STYLE = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: var(--color-bg); }
body { font-family: var(--font-body); color: var(--color-text-soft); font-size: 10.6pt; line-height: 1.45; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
strong, b { font-weight: 500; }
.page { width: 210mm; height: 297mm; padding: 16mm 17mm 20mm; display: flex; flex-direction: column; gap: 4.5mm; page-break-after: always; overflow: hidden; }
.page:last-child { page-break-after: auto; }
h1, h2, h3, h4 { font-family: var(--font-display); font-weight: 500; color: var(--color-text); }
.kicker { font-size: 7.5pt; letter-spacing: .12em; text-transform: uppercase; color: var(--color-highlight-ink); font-weight: 500; }
.top { border-bottom: 0.6mm solid var(--color-accent); padding-bottom: 4mm; }
.top h2 { font-size: 26pt; line-height: 1.05; letter-spacing: -.01em; margin-top: 1mm; }
.oneliner { font-size: 13pt; color: var(--color-text); }
.chip { display: inline-block; border: 0.35mm solid var(--color-accent); color: var(--color-accent); border-radius: 1mm; padding: .3mm 2mm; font-weight: 500; font-size: 8pt; }
.chip--strong { background: var(--color-accent); color: var(--color-bg); }
.chip--framework { border-color: var(--color-border); border-style: dashed; color: var(--color-text-muted); }
.chip--choosewise { border-color: var(--color-highlight); border-style: dashed; color: var(--color-highlight-ink); }
.ex { border-left: 1mm solid var(--color-highlight); background: var(--color-bg-alt); padding: 4.5mm 6mm; display: flex; flex-direction: column; gap: 2mm; }
.ex h3 { font-size: 12pt; }
.ex h3 span { font-weight: 400; color: var(--color-text-muted); }
.ex dl { display: grid; grid-template-columns: 22mm 1fr; gap: 1.6mm 4mm; }
.ex dt { font-size: 8.5pt; letter-spacing: .08em; text-transform: uppercase; color: var(--color-accent); font-weight: 500; padding-top: .5mm; }
.ex ol { padding-left: 4.5mm; }
.for-ai { font-size: 9.5pt; color: var(--color-text); }
.evidence { font-size: 9pt; color: var(--color-text-muted); }
.foot { margin-top: auto; font-size: 7.5pt; color: var(--color-text-muted); border-top: 0.3mm solid var(--color-border); padding-top: 2.5mm; display: flex; justify-content: space-between; }
.cover h1 { font-size: 34pt; font-weight: 300; letter-spacing: -.02em; line-height: 1.05; }
.cover .lede { font-size: 12pt; color: var(--color-text); max-width: 150mm; }
.start { border: 0.35mm solid var(--color-highlight); border-radius: 1.5mm; padding: 4mm 5mm; color: var(--color-text); }
.lenses { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5mm 8mm; font-size: 9.5pt; }
.legend { display: flex; flex-direction: column; gap: 2mm; font-size: 9pt; }
.prompt { border: 0.35mm dashed var(--color-accent); border-radius: 1.5mm; padding: 6mm 7mm; font-family: 'SF Mono', Menlo, monospace; font-size: 8.6pt; line-height: 1.65; color: var(--color-text); white-space: pre-wrap; }
.blank { display: inline-block; border-bottom: 0.3mm solid var(--color-text); }
.how { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4mm; font-size: 9pt; }
.how div { border-top: 0.5mm solid var(--color-highlight); padding-top: 2mm; }
"""


def _foot(right: str) -> str:
    return f'<div class="foot"><span>{TITLE} · {URL}</span><span>{right}</span></div>'


def _chip(key: str, labels: dict) -> str:
    return f'<span class="chip chip--{escape(key)}">{escape(labels[key]["name"])}</span>'


def _cover(data: dict) -> str:
    labels = data["labels"]
    default = next(l for l in data["lenses"] if l["id"] == data["default_lens"])
    lenses = "".join(
        f'<p>{int(l["number"])}. {escape(l["name"])} {_chip(l["label"], labels)}</p>' for l in data["lenses"]
    )
    legend = "".join(
        f'<p>{_chip(k, labels)} {escape(labels[k]["definition"])}</p>'
        for k in ("strong", "promising", "framework", "choosewise")
    )
    how = (
        '<div><strong>Plan as usual</strong><br>A few lines: what happens, in what order.</div>'
        '<div><strong>Read Keep first</strong><br>It names what already works.</div>'
        '<div><strong>Try at most two upgrades</strong><br>The Nudge is a question you can ignore.</div>'
        '<div><strong>Look for the Check</strong><br>It tells you whether the change worked.</div>'
    )
    return (
        '<section class="page cover">'
        '<div class="kicker">Pedagogy + AI · Grades 6–12 · free card deck</div>'
        f'<h1>{TITLE}</h1>'
        '<p class="lede">Run the lesson you have already planned through a research lens. '
        'Your AI tool keeps your lesson and suggests at most two small, concrete upgrades.</p>'
        f'<p class="start"><strong>Not sure? Start here: {escape(default["name"])}.</strong> '
        'It fits almost any lesson: it shows you what students understood before you move on.</p>'
        f'<h3>Using the answer</h3><div class="how">{how}</div>'
        f'<h3>The twelve lenses</h3><div class="lenses">{lenses}</div>'
        f'<h3>How strong is the evidence?</h3><div class="legend">{legend}</div>'
        f'{_foot("1 / 14")}</section>'
    )


def _card(lens: dict, data: dict, page_no: int) -> str:
    ex = lens["example"]
    lesson = "".join(f"<li>{escape(line)}</li>" for line in ex["lesson"])
    upgrade = "".join(f"<li>{escape(u)}</li>" for u in ex["upgrade"])
    return (
        '<section class="page">'
        f'<div class="top"><div class="kicker">Lens {int(lens["number"])}</div>'
        f'<h2>{escape(lens["name"])}</h2></div>'
        f'<p class="oneliner">{escape(lens["one_liner"])}</p>'
        f'<p>{_chip(lens["label"], data["labels"])}</p>'
        f'<div class="ex"><h3>{escape(ex["subject"])} <span>· Grade {int(ex["grade"])}</span></h3><dl>'
        f"<dt>Lesson</dt><dd><ol>{lesson}</ol></dd>"
        f'<dt>Keep</dt><dd>{escape(ex["keep"])}</dd>'
        f"<dt>Upgrade</dt><dd><ol>{upgrade}</ol></dd>"
        f'<dt>Nudge</dt><dd>{escape(ex["nudge"])}</dd>'
        f'<dt>Check</dt><dd>{escape(ex["check"])}</dd>'
        "</dl></div>"
        f'<p class="for-ai"><strong>For the AI.</strong> {escape(lens["prompt_brief"])}</p>'
        f'<p class="evidence"><strong>Evidence.</strong> {escape(lens["evidence"])}</p>'
        f'{_foot(f"{page_no} / 14")}</section>'
    )


def _fill_in() -> str:
    def blank(mm: int) -> str:
        return f'<span class="blank" style="width:{mm}mm"></span>'

    # Raderna är ordagrant desamma som i promptbyggaren (assets/js/lesson-lens.js),
    # utom att lärarens uppgifter är luckor. Den andra linsen är utelämnad.
    prompt = "\n".join([
        "Do not include student names or student work in this conversation.",
        "",
        f"You are helping a Grade {blank(12)} {blank(45)} teacher improve a lesson they have already planned. "
        "Keep their lesson and their way of teaching. Do not rewrite the lesson.",
        "",
        f"Lens: {blank(70)} (the lens's name and one-line description from its card)",
        f"How to apply it: {blank(60)} (the \"For the AI\" text from its card)",
        "",
        "The lesson as planned:",
        f"{blank(160)}",
        f"{blank(160)}",
        f"{blank(160)}",
        "",
        f"Students already know: {blank(90)}",
        "",
        "Reply in plain text, no tables, with exactly these four parts:",
        *[escape(p, quote=False) for p in PROMPT_PARTS],
    ])
    return (
        '<section class="page">'
        '<div class="kicker">Without the website</div>'
        '<h2 style="font-size:24pt">Your own prompt</h2>'
        '<p class="oneliner">Fill in the blanks, then type the prompt into any AI tool: Copilot, Gemini, ChatGPT or Claude. '
        'Leave out the line "Students already know" if you have nothing to add. '
        'Check the suggestions before the lesson. The AI proposes; you decide.</p>'
        f'<div class="prompt">{prompt}</div>'
        '<p class="evidence">Faster online: the prompt builder at ' + URL + ' fills this in for you, '
        'and lets you add a second lens. If students use AI themselves, check the tool\'s age rules, '
        'your national rules and your school policy first.</p>'
        f'{_foot("14 / 14")}</section>'
    )


def render_deck_html(data: dict) -> str:
    """The complete HTML source of the deck. Same JSON in, same text out."""
    pages = [_cover(data)]
    pages += [_card(l, data, i) for i, l in enumerate(data["lenses"], start=2)]
    pages.append(_fill_in())
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n"
        f"<title>{TITLE} — card deck</title>\n"
        "<!-- Generated by exports/build-lesson-lens-pdf.py from lesson-lens/lenses-en.json. "
        "Edit the JSON or the script, not this file. -->\n"
        '<link rel="stylesheet" href="../../exports/_guide-print.css">\n'
        f"<style>{STYLE}</style>\n</head>\n<body>\n"
        + "\n".join(pages)
        + "\n</body>\n</html>\n"
    )


def main() -> None:
    from playwright.sync_api import sync_playwright

    data = json.loads(DATA.read_text(encoding="utf-8"))
    SRC.parent.mkdir(parents=True, exist_ok=True)
    SRC.write_text(render_deck_html(data), encoding="utf-8")
    DST.parent.mkdir(parents=True, exist_ok=True)
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
