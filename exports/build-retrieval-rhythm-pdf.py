#!/usr/bin/env python3
"""Build the Retrieval Rhythm printable pack (A4, 8 pages) from retrieval-rhythm/rhythm-en.json.

Page 1      the weekly rhythm and why it works
Pages 2–6   one student template per format, ready to print or project
Page 7      for students and parents: why we start every lesson like this
Page 8      a fill-in prompt for use without the website

Writes the HTML source to _unpublished/exports/retrieval-rhythm-pack-a4-en.html
(so the PDF always has an editable source) and the PDF to
assets/pdfs/free/retrieval-rhythm-pack-en.pdf.

Usage:
    /usr/bin/python3 exports/build-retrieval-rhythm-pdf.py
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "retrieval-rhythm/rhythm-en.json"
SRC = ROOT / "_unpublished/exports/retrieval-rhythm-pack-a4-en.html"
DST = ROOT / "assets/pdfs/free/retrieval-rhythm-pack-en.pdf"
URL = "choosewise.education/retrieval-rhythm"
TITLE = "Retrieval Rhythm"
PAGES = 8

# Svarsdelen, ordagrant som i assets/js/retrieval-rhythm.js;
# test_fill_in_matches_builder_prompt håller dem i takt.
PROMPT_TAIL = [
    "In starter quizzes and multiple choice, mix content from different times in the log: about two fifths from the newest week in the log, two fifths from one to three weeks before it, and one fifth from older entries. Count back from the newest entry in the log. If the log is short, spread the questions across all of it. Mix the order so students cannot tell which week a question comes from. The other formats follow their own description.",
    "",
    "Reply in plain text, no tables. For each lesson write:",
    "LESSON: the lesson number (with its date, if a first lesson is given), the format, and the log entries it draws on, with their dates",
    "STARTER: the starter exactly as students will see it",
    "KEY: the answer to every question, or the key points for brain dump and two things I remember",
    "Then once, at the very end:",
    'CHECK: every answer you are not fully sure of, one per line, so the teacher can verify it. Write "None" if there are none.',
]

# Samma tryckstil som kortlekarna (exports/_guide-print.css, Hanken Grotesk 300–500).
STYLE = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: var(--color-bg); }
body { font-family: var(--font-body); color: var(--color-text-soft); font-size: 10.6pt; line-height: 1.45; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
strong, b { font-weight: 500; }
.page { width: 210mm; height: 297mm; padding: 16mm 17mm 20mm; display: flex; flex-direction: column; gap: 4.5mm; page-break-after: always; overflow: hidden; }
.page:last-child { page-break-after: auto; }
h1, h2, h3 { font-family: var(--font-display); font-weight: 500; color: var(--color-text); }
.kicker { font-size: 7.5pt; letter-spacing: .12em; text-transform: uppercase; color: var(--color-highlight-ink); font-weight: 500; }
.top { border-bottom: 0.6mm solid var(--color-accent); padding-bottom: 4mm; }
.top h2 { font-size: 26pt; line-height: 1.05; letter-spacing: -.01em; margin-top: 1mm; }
.oneliner { font-size: 12.5pt; color: var(--color-text); }
.steps { padding-left: 5mm; display: flex; flex-direction: column; gap: 1mm; font-size: 9.8pt; }
.chip { display: inline-block; border: 0.35mm solid var(--color-accent); color: var(--color-accent); border-radius: 1mm; padding: .3mm 2mm; font-weight: 500; font-size: 8pt; }
.chip--strong { background: var(--color-accent); color: var(--color-bg); }
.cover h1 { font-size: 34pt; font-weight: 300; letter-spacing: -.02em; line-height: 1.05; }
.cover .lede { font-size: 12pt; color: var(--color-text); max-width: 150mm; }
.how { display: grid; grid-template-columns: repeat(3, 1fr); gap: 5mm; font-size: 9.5pt; }
.how div { border-top: 0.5mm solid var(--color-highlight); padding-top: 2mm; }
.approach h3 { font-size: 11pt; margin-bottom: 1mm; display: flex; gap: 2mm; align-items: center; }
.approach p { font-size: 9pt; }
.sheet { border: 0.35mm solid var(--color-border); border-radius: 1.5mm; padding: 6mm 7mm; flex: 1; display: flex; flex-direction: column; gap: 5mm; }
.sheet-head { display: flex; gap: 8mm; font-size: 10pt; color: var(--color-text); }
.sheet-head span { flex: 1; border-bottom: 0.3mm solid var(--color-text); padding-bottom: 1mm; }
.line { border-bottom: 0.3mm solid var(--color-border); height: 9mm; display: flex; align-items: flex-end; gap: 3mm; font-size: 10pt; color: var(--color-text); }
.box { flex: 1; border: 0.3mm dashed var(--color-border); border-radius: 1mm; }
.grid { display: grid; grid-template-columns: 30mm repeat(3, 1fr); gap: 2mm; flex: 1; }
.grid .label { font-size: 9pt; color: var(--color-text); display: flex; align-items: center; }
.grid .cell { border: 0.3mm solid var(--color-border); border-radius: 1mm; min-height: 38mm; }
.mcq { display: flex; flex-direction: column; gap: 6mm; }
.mcq .opts { display: flex; gap: 10mm; font-size: 10.5pt; color: var(--color-text); margin-top: 2mm; }
.mcq .opts span::before { content: ""; display: inline-block; width: 4mm; height: 4mm; border: 0.3mm solid var(--color-text); border-radius: 50%; margin-right: 2mm; vertical-align: -0.6mm; }
.explain { font-size: 11pt; color: var(--color-text); display: flex; flex-direction: column; gap: 4mm; max-width: 165mm; }
.explain h3 { font-size: 13pt; margin-top: 2mm; }
.prompt { border: 0.35mm dashed var(--color-accent); border-radius: 1.5mm; padding: 5.5mm 7mm; font-family: 'SF Mono', Menlo, monospace; font-size: 8pt; line-height: 1.5; color: var(--color-text); white-space: pre-wrap; }
.blank { display: inline-block; border-bottom: 0.3mm solid var(--color-text); }
.note { font-size: 8.6pt; color: var(--color-text-muted); }
.foot { margin-top: auto; font-size: 7.5pt; color: var(--color-text-muted); border-top: 0.3mm solid var(--color-border); padding-top: 2.5mm; display: flex; justify-content: space-between; }
"""


def _foot(page_no: int) -> str:
    return f'<div class="foot"><span>{TITLE} · {URL}</span><span>{page_no} / {PAGES}</span></div>'


def _cover(data: dict) -> str:
    labels = data["labels"]
    approaches = "".join(
        f'<div class="approach"><h3>{escape(a["name"])} <span class="chip chip--{escape(a["label"])}">{escape(labels[a["label"]]["name"])}</span></h3>'
        f'<p>{escape(a["evidence"])}</p></div>'
        for a in data["approaches"]
    )
    how = (
        '<div><strong>After each lesson · 1 min</strong><br>Add a row to your log: the date, the topic and two or three key points.</div>'
        '<div><strong>On Friday · 5 min</strong><br>Paste the log into the prompt and copy it into your AI tool.</div>'
        '<div><strong>Before Monday · 3 min</strong><br>Check the answer key, especially anything under CHECK.</div>'
    )
    return (
        '<section class="page cover">'
        '<div class="kicker">Pedagogy + AI · Grades 6–12 · free printable pack</div>'
        f"<h1>{TITLE}</h1>"
        '<p class="lede">Start every lesson with students answering from memory, mixing last lesson, '
        "last month and last term. About ten minutes of preparation a week.</p>"
        f'<h3>Your weekly rhythm</h3><div class="how">{how}</div>'
        f"<h3>Why it works</h3>{approaches}"
        f"{_foot(1)}</section>"
    )


def _frame(fid: str) -> str:
    """The blank student frame for one format."""
    if fid == "starter-quiz":
        return "".join(f'<div class="line">{n}.</div>' for n in range(1, 7)) + '<div class="line">Score: ___ / ___</div>'
    if fid == "brain-dump":
        return ('<div class="line">Topic:</div>'
                '<p class="note">Write everything you remember. Then add what you missed in a different colour.</p>'
                '<div class="box"></div>')
    if fid == "retrieval-grid":
        rows = [("Newest week", "1 point"), ("1–3 weeks before", "2 points"), ("Older", "3 points")]
        cells = "".join(
            f'<div class="label">{name}<br>{points}</div><div class="cell"></div><div class="cell"></div><div class="cell"></div>'
            for name, points in rows
        )
        return f'<div class="grid">{cells}</div><div class="line">Total points:</div>'
    if fid == "multiple-choice":
        q = '<div><div class="line">{n}.</div><div class="opts"><span>A</span><span>B</span><span>C</span><span>D</span></div></div>'
        return '<div class="mcq">' + "".join(q.format(n=n) for n in range(1, 5)) + "</div>"
    if fid == "two-things":
        return ('<div class="line">Lesson:</div>'
                '<div class="line">1. One thing I remember:</div><div class="line"></div>'
                '<div class="line">2. Another thing I remember:</div><div class="line"></div>'
                '<div class="line">A question I still have:</div><div class="line"></div>')
    raise ValueError(fid)


def _format_page(fmt: dict, page_no: int) -> str:
    steps = "".join(f"<li>{escape(s)}</li>" for s in fmt["steps"])
    return (
        '<section class="page">'
        f'<div class="top"><div class="kicker">Starter format · {int(fmt["minutes"])} min</div>'
        f'<h2>{escape(fmt["name"])}</h2></div>'
        f'<p class="oneliner">{escape(fmt["one_liner"])}</p>'
        f'<p class="note">For the teacher</p><ol class="steps">{steps}</ol>'
        '<div class="sheet"><div class="sheet-head"><span>Name</span><span>Date</span></div>'
        f"{_frame(fmt['id'])}</div>"
        f"{_foot(page_no)}</section>"
    )


def _explainer() -> str:
    return (
        '<section class="page">'
        '<div class="kicker">For students and parents</div>'
        '<div class="top"><h2>Why we start every lesson like this</h2></div>'
        '<div class="explain">'
        "<p>Most lessons now begin with a few questions answered from memory, without notes or books. "
        "Some questions are about last lesson, some about a few weeks ago, and some about last term.</p>"
        "<h3>Why from memory?</h3>"
        "<p>Every time you pull something out of memory, it becomes easier to find again. "
        "Reading your notes again feels useful, but it helps much less than trying to remember first.</p>"
        "<h3>Why old topics too?</h3>"
        "<p>We forget quickly. Coming back to a topic after a few weeks, just as it starts to fade, "
        "makes it last much longer than practising it many times in one go.</p>"
        "<h3>Why does it feel harder?</h3>"
        "<p>It is supposed to. A quiz feels harder than listening to a recap, and that effort is exactly "
        "what makes it stick. Getting an answer wrong is part of it: the starter is practice, not a test, "
        "and it shows us what to go over again.</p>"
        "<h3>How you can help at home</h3>"
        "<p>Ask: \"What did you have to remember at the start of the lesson today?\" "
        "Trying to explain it once more is another round of practice.</p>"
        "</div>"
        f"{_foot(7)}</section>"
    )


def _fill_in(data: dict) -> str:
    def blank(mm: int) -> str:
        return f'<span class="blank" style="width:{mm}mm"></span>'

    # Raderna är ordagrant desamma som i promptbyggaren (assets/js/retrieval-rhythm.js),
    # utom att lärarens uppgifter är luckor.
    prompt = "\n".join([
        "Do not include student names or student results in this conversation.",
        "",
        f"You are helping a Grade {blank(12)} {blank(45)} teacher plan retrieval practice starters for next week. "
        "Ask only about content in the topic log below. The KEY may add a short explanation.",
        "",
        f"Format: {blank(60)} (the format's name, and its line from the list below)",
        f"Number of lessons: {blank(12)}",
        f"First lesson: {blank(30)}",
        f"Questions per starter: {blank(12)} (for starter quizzes and multiple choice)",
        "",
        "Topic log (date, topic, key points):",
        f"{blank(160)}",
        f"{blank(160)}",
        f"{blank(160)}",
        "",
        *PROMPT_TAIL,
    ])
    briefs = "".join(
        f"<p><strong>{escape(f['name'])}.</strong> {escape(f['prompt_brief'])}</p>" for f in data["formats"]
    )
    return (
        '<section class="page">'
        '<div class="kicker">Without the website</div>'
        '<h2 style="font-size:22pt">Your own prompt</h2>'
        '<p class="note">Fill in the blanks, then type the prompt into any AI tool: Copilot, Gemini, ChatGPT or Claude. '
        'Leave out the line "First lesson" if you do not need dates. Faster online: the builder at '
        + URL + " fills this in and lets you paste your log.</p>"
        f'<div class="prompt">{prompt}</div>'
        f'<div class="note">{briefs}</div>'
        f"{_foot(8)}</section>"
    )


def render_pack_html(data: dict) -> str:
    """The complete HTML source of the pack. Same JSON in, same text out."""
    real = [f for f in data["formats"] if f["id"] != "mix"]
    pages = [_cover(data)]
    pages += [_format_page(f, i) for i, f in enumerate(real, start=2)]
    pages += [_explainer(), _fill_in(data)]
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n"
        f"<title>{TITLE} — printable pack</title>\n"
        "<!-- Generated by exports/build-retrieval-rhythm-pdf.py from retrieval-rhythm/rhythm-en.json. "
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
    SRC.write_text(render_pack_html(data), encoding="utf-8")
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
