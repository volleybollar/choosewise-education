#!/usr/bin/env python3
"""Build the Thinking Moves card deck (A4, 14 pages) from thinking-moves/moves-en.json.

Page 1   cover: the six clusters and the evidence labels
Pages 2–13  one card per move, with both worked examples complete
Page 14  a fill-in prompt for use without the website

Writes the HTML source to _unpublished/exports/thinking-moves-cards-a4-en.html
(so the PDF always has an editable source) and the PDF to
assets/pdfs/free/thinking-moves-cards-en.pdf.

Usage:
    /usr/bin/python3 exports/build-thinking-moves-pdf.py
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "thinking-moves/moves-en.json"
SRC = ROOT / "_unpublished/exports/thinking-moves-cards-a4-en.html"
DST = ROOT / "assets/pdfs/free/thinking-moves-cards-en.pdf"
URL = "choosewise.education/thinking-moves"
TITLE = "Thinking Moves"

PARTS = [("task", "Task"), ("look_for", "Look for"), ("probe", "Probe"), ("think_back", "Think back")]

# Kortens utseende. Följer mockupen Johan valde (alternativ B) och den delade
# tryckstilen exports/_guide-print.css, som laddar Hanken Grotesk 300–500.
STYLE = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: var(--color-bg); }
body { font-family: var(--font-body); color: var(--color-text-soft); font-size: 10.8pt; line-height: 1.45; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
strong, b { font-weight: 500; }
.page { width: 210mm; height: 297mm; padding: 16mm 17mm 20mm; display: flex; flex-direction: column; gap: 5mm; page-break-after: always; overflow: hidden; }
.page:last-child { page-break-after: auto; }
h1, h2, h3, h4 { font-family: var(--font-display); font-weight: 500; color: var(--color-text); }
.kicker { font-size: 7.5pt; letter-spacing: .12em; text-transform: uppercase; color: var(--color-highlight-ink); font-weight: 500; }
.top { display: grid; grid-template-columns: 22mm 1fr; gap: 6mm; align-items: center; border-bottom: 0.6mm solid var(--color-accent); padding-bottom: 4.5mm; }
.top img { width: 22mm; height: 22mm; }
.top h2 { font-size: 28pt; line-height: 1.05; letter-spacing: -.01em; margin-top: 1mm; }
.oneliner { font-size: 13pt; color: var(--color-text); }
.meta { display: flex; gap: 4mm; align-items: center; font-size: 9.5pt; color: var(--color-text-muted); }
.chip { display: inline-block; border: 0.35mm solid var(--color-accent); color: var(--color-accent); border-radius: 1mm; padding: .3mm 2mm; font-weight: 500; font-size: 8pt; }
.chip--strong { background: var(--color-accent); color: var(--color-bg); }
.chip--framework { border-color: var(--color-border); border-style: dashed; color: var(--color-text-muted); }
.ex { border-left: 1mm solid var(--color-highlight); background: var(--color-bg-alt); padding: 4.5mm 6mm; display: flex; flex-direction: column; gap: 2mm; }
.ex h3 { font-size: 12pt; }
.ex h3 span { font-weight: 400; color: var(--color-text-muted); }
.ex dl { display: grid; grid-template-columns: 24mm 1fr; gap: 1.4mm 4mm; }
.ex dt { font-size: 8.5pt; letter-spacing: .08em; text-transform: uppercase; color: var(--color-accent); font-weight: 500; padding-top: .5mm; }
.evidence { font-size: 9.5pt; color: var(--color-text-muted); }
.foot { margin-top: auto; font-size: 7.5pt; color: var(--color-text-muted); border-top: 0.3mm solid var(--color-border); padding-top: 2.5mm; display: flex; justify-content: space-between; }
.cover h1 { font-size: 34pt; font-weight: 300; letter-spacing: -.02em; line-height: 1.05; }
.cover .lede { font-size: 12pt; color: var(--color-text); max-width: 150mm; }
.clusters { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm 8mm; }
.cluster { border-top: 0.5mm solid var(--color-accent); padding-top: 2.5mm; }
.cluster h3 { font-size: 11pt; margin-bottom: 1mm; }
.cluster p { font-size: 8.8pt; }
.legend { display: flex; flex-direction: column; gap: 2mm; font-size: 9pt; }
.note { font-size: 9.5pt; color: var(--color-text); font-weight: 500; }
.prompt { border: 0.35mm dashed var(--color-accent); border-radius: 1.5mm; padding: 6mm 7mm; font-family: 'SF Mono', Menlo, monospace; font-size: 9.2pt; line-height: 1.7; color: var(--color-text); white-space: pre-wrap; }
.blank { display: inline-block; border-bottom: 0.3mm solid var(--color-text); }
.how { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4mm; font-size: 9pt; }
.how div { border-top: 0.5mm solid var(--color-highlight); padding-top: 2mm; }
"""


def _icon(move_id: str) -> str:
    # Ikonen länkas som bild i stället för att bäddas in, så att mallen
    # inte bär hårdkodade hexfärger (test_guide_print_css.py).
    return f'<img src="../../thinking-moves/icons/{move_id}.svg" alt="">'


def _foot(right: str) -> str:
    return f'<div class="foot"><span>{TITLE} · {URL}</span><span>{right}</span></div>'


def _cover(data: dict) -> str:
    names = {m["id"]: m["name"] for m in data["moves"]}
    clusters = "".join(
        f'<div class="cluster"><h3>{i}. {escape(c["name"])}</h3>'
        f'<p>{escape(", ".join(names[mid] for mid in c["moves"]))}</p></div>'
        for i, c in enumerate(data["clusters"], start=1)
    )
    labels = data["labels"]
    legend = "".join(
        f'<p><span class="chip chip--{k}">{escape(labels[k]["name"])}</span> {escape(labels[k]["definition"])}</p>'
        for k in ("strong", "promising", "framework")
    )
    how = (
        '<div><strong>Task · 2 min</strong><br>Students work alone, on paper.</div>'
        '<div><strong>Pair talk · 1 min</strong><br>Compare and improve one answer.</div>'
        '<div><strong>Share · 1 min</strong><br>Take two or three answers; ask the Probe.</div>'
        '<div><strong>Think back · 1 min</strong><br>Each student finishes the sentence starter.</div>'
    )
    return (
        '<section class="page cover">'
        '<div class="kicker">Think + AI · Grades 8–12 · free card deck</div>'
        f'<h1>{TITLE}</h1>'
        '<p class="lede">Twelve five-minute thinking tasks, each built on the topic you are teaching. '
        'AI can prepare a new task in seconds; your students do the thinking without devices.</p>'
        f'<h3>Five minutes in the lesson</h3><div class="how">{how}</div>'
        f'<h3>Six kinds of thinking</h3><div class="clusters">{clusters}</div>'
        f'<h3>How strong is the evidence?</h3><div class="legend">{legend}</div>'
        f'<p class="note">{escape(labels["note"])}</p>'
        f'{_foot("1 / 14")}</section>'
    )


def _card(move: dict, data: dict, page_no: int) -> str:
    cluster = next(c["name"] for c in data["clusters"] if c["id"] == move["cluster"])
    examples = "".join(
        f'<div class="ex"><h3>{escape(ex["subject"])} <span>· Grade {int(ex["grade"])}</span></h3><dl>'
        + "".join(f"<dt>{label}</dt><dd>{escape(ex[key])}</dd>" for key, label in PARTS)
        + "</dl></div>"
        for ex in move["examples"]
    )
    label = data["labels"][move["label"]]["name"]
    return (
        '<section class="page">'
        f'<div class="top">{_icon(move["id"])}<div>'
        f'<div class="kicker">Move {int(move["number"])} · {escape(cluster)}</div>'
        f'<h2>{escape(move["name"])}</h2></div></div>'
        f'<p class="oneliner">{escape(move["one_liner"])}</p>'
        f'<div class="meta"><span class="chip chip--{escape(move["label"])}">{escape(label)}</span>'
        f'<span>{escape(move["modes"])} · 5 minutes · no devices</span></div>'
        f"{examples}"
        f'<p class="evidence"><strong>Evidence.</strong> {escape(move["evidence"])} '
        f'Labels rate research on teaching this kind of thinking regularly, not a single move.</p>'
        f'{_foot(f"{page_no} / 14")}</section>'
    )


def _fill_in() -> str:
    def blank(mm: int) -> str:
        return f'<span class="blank" style="width:{mm}mm"></span>'

    prompt = (
        "Do not include student names or student work in this conversation.\n\n"
        f"You are helping a Grade {blank(12)} {blank(45)} teacher plan a\n"
        "five-minute thinking task for tomorrow's lesson.\n\n"
        f"Thinking move: {blank(60)} (copy the move's name and\n"
        "one-line description from its card)\n\n"
        f"Lesson topic: {blank(110)}\n"
        f"Students already know: {blank(92)}\n\n"
        "Write the task so it can only be done by thinking about this\n"
        "topic's content, and so students need no devices: paper,\n"
        "whiteboards or talk.\n\n"
        "Reply in plain text, no tables, with exactly these six parts:\n"
        "MOVE: the move's name and one line on what it trains\n"
        "TASK: the task, written to the students: at most three\n"
        "  short steps, under 80 words, about two minutes of work\n"
        "LOOK FOR: at most five short bullets: the strongest answer\n"
        "  first, then the most common mistake\n"
        "PROBE: one follow-up question that pushes past the first answer\n"
        "THINK BACK: one sentence starter about how they thought\n"
        "CHECK: every fact, figure, date or source to verify,\n"
        "  one per line, or None"
    )
    return (
        '<section class="page">'
        '<div class="kicker">Without the website</div>'
        '<h2 style="font-size:24pt">Your own task</h2>'
        '<p class="oneliner">Fill in the blanks, then type the prompt into any AI tool: Copilot, Gemini, ChatGPT or Claude. '
        'Check the answer before the lesson, especially anything under CHECK.</p>'
        f'<div class="prompt">{prompt}</div>'
        '<p class="evidence">Faster online: the prompt builder at ' + URL + ' fills this in for you. '
        'Students do not need AI for any move. If older students use AI themselves, check the tool\'s age rules, '
        'your national rules and your school policy first.</p>'
        f'{_foot("14 / 14")}</section>'
    )


def render_deck_html(data: dict) -> str:
    """The complete HTML source of the deck. Same JSON in, same text out."""
    pages = [_cover(data)]
    pages += [_card(m, data, i) for i, m in enumerate(data["moves"], start=2)]
    pages.append(_fill_in())
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n"
        f"<title>{TITLE} — card deck</title>\n"
        "<!-- Generated by exports/build-thinking-moves-pdf.py from thinking-moves/moves-en.json. "
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
