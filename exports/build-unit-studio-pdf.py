#!/usr/bin/env python3
"""Build the Unit Studio method card (A4, 2 pages) from unit-studio-541ebd12/studio-en.json.

Page 1   the five steps with their look-for questions and evidence labels
Page 2   a fill-in step prompt and the final prompt's format, for planning
         without the website

The card is for Skool members, so it lives in the hidden folder, not under
/assets/pdfs/free/. Writes the HTML source to
_unpublished/exports/unit-studio-method-card-a4-en.html and the PDF to
unit-studio-541ebd12/unit-studio-method-card-en.pdf.

Usage:
    /usr/bin/python3 exports/build-unit-studio-pdf.py
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "unit-studio-541ebd12"
DATA = ROOT / SLUG / "studio-en.json"
SRC = ROOT / "_unpublished/exports/unit-studio-method-card-a4-en.html"
DST = ROOT / SLUG / "unit-studio-method-card-en.pdf"
TITLE = "Unit Studio"
PAGES = 2
PRIVACY = "Do not include student names or student results in this conversation."

# Svarsformaten, ordagrant som i assets/js/unit-studio.js;
# test_fill_in_prompt_matches_builder håller dem i takt.
STEP_FORMAT = [
    "Reply in plain text, no tables, in exactly this format:",
    "KEEP: what already works for this step, in one or two lines. For a new unit, what in the topic and goals is already clear.",
    "SUGGEST: at most three changes for this step, numbered, each tied to this unit's content, each with one line on why it helps students learn.",
    "QUESTION: one question back to the teacher before the next step.",
    "AI CAN ALSO: one other way an AI tool could help with this step, written as a short prompt the teacher can copy.",
]
FINAL_FORMAT = [
    "Reply in plain text, no tables, in exactly this format:",
    "GOAL AND EVIDENCE: what students should be able to do by the end, and how the teacher will see it",
    "PRIOR KNOWLEDGE: what students need first, and how to check it in the first lesson",
    "LESSONS: one line per lesson, numbered, with what students do and roughly how long",
    "RETRIEVAL: which earlier content returns in which lessons",
    "CHECKPOINTS: where in the unit to check understanding, how, and what to do if fewer than about 4 in 5 get it",
    "AI USE: where students use AI in this unit, where they do not, and why",
    'CHANGES: what is different from the original plan, one line each, or "New unit"',
    'CHECK: anything the teacher should verify before teaching, one per line, or "None"',
]

# Samma tryckstil som de andra paketen (exports/_guide-print.css, Hanken Grotesk 300–500).
STYLE = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: var(--color-bg); }
body { font-family: var(--font-body); color: var(--color-text-soft); font-size: 10.4pt; line-height: 1.42; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
strong, b { font-weight: 500; }
.page { width: 210mm; height: 297mm; padding: 15mm 17mm 18mm; display: flex; flex-direction: column; gap: 4mm; page-break-after: always; overflow: hidden; }
.page:last-child { page-break-after: auto; }
h1, h2, h3 { font-family: var(--font-display); font-weight: 500; color: var(--color-text); }
.kicker { font-size: 7.5pt; letter-spacing: .12em; text-transform: uppercase; color: var(--color-highlight-ink); font-weight: 500; }
h1 { font-size: 28pt; font-weight: 300; letter-spacing: -.02em; line-height: 1.05; }
.lede { font-size: 11pt; color: var(--color-text); max-width: 165mm; }
.step { border-top: 0.5mm solid var(--color-highlight); padding-top: 2mm; display: flex; flex-direction: column; gap: 1mm; }
.step h2 { font-size: 13.5pt; display: flex; gap: 2mm; align-items: baseline; flex-wrap: wrap; }
.step h2 .num { font-size: 9pt; color: var(--color-highlight-ink); letter-spacing: .08em; text-transform: uppercase; }
.step ul { padding-left: 5mm; font-size: 9.6pt; color: var(--color-text); display: flex; flex-direction: column; gap: .5mm; }
.chip { display: inline-block; border: 0.35mm solid var(--color-accent); color: var(--color-accent); border-radius: 1mm; padding: .2mm 1.6mm; font-weight: 500; font-size: 7.5pt; font-family: var(--font-body); }
.chip--strong { background: var(--color-accent); color: var(--color-bg); }
.chip--choosewise { border-style: dashed; }
.prompt { border: 0.35mm dashed var(--color-accent); border-radius: 1.5mm; padding: 5mm 6.5mm; font-family: 'SF Mono', Menlo, monospace; font-size: 7.8pt; line-height: 1.5; color: var(--color-text); white-space: pre-wrap; }
.blank { display: inline-block; border-bottom: 0.3mm solid var(--color-text); }
.note { font-size: 8.6pt; color: var(--color-text-muted); }
.foot { margin-top: auto; font-size: 7.5pt; color: var(--color-text-muted); border-top: 0.3mm solid var(--color-border); padding-top: 2.5mm; display: flex; justify-content: space-between; }
"""


def _foot(page_no: int) -> str:
    return f'<div class="foot"><span>{TITLE} · for Choosewise members</span><span>{page_no} / {PAGES}</span></div>'


def _blank(mm: int) -> str:
    return f'<span class="blank" style="width:{mm}mm"></span>'


def _steps_page(data: dict) -> str:
    labels = data["labels"]
    approaches = {a["id"]: a for a in data["approaches"]}
    steps = []
    for s in data["steps"]:
        # En etikett per sort, även när två ansatser delar etikett (steg 4).
        kinds = list(dict.fromkeys(approaches[a]["label"] for a in s["approach_ids"]))
        chips = " ".join(f'<span class="chip chip--{escape(k)}">{escape(labels[k]["name"])}</span>' for k in kinds)
        questions = "".join(f"<li>{escape(q)}</li>" for q in s["look_for"])
        steps.append(
            f'<div class="step"><h2><span class="num">Step {int(s["num"])}</span> {escape(s["name"])} {chips}</h2>'
            f"<ul>{questions}</ul></div>"
        )
    return (
        '<section class="page">'
        '<div class="kicker">Pedagogy + AI · the method card</div>'
        f"<h1>{TITLE}</h1>"
        '<p class="lede">Five steps for every unit you plan. Ask the questions yourself, or give each step to an AI tool '
        "with the prompt overleaf. Then let the AI write the improved plan, and review it before you teach it.</p>"
        + "".join(steps)
        + f"{_foot(1)}</section>"
    )


def _prompt_page() -> str:
    # Raderna är ordagrant desamma som i promptbyggaren, utom att lärarens
    # uppgifter är luckor.
    step_prompt = "\n".join([
        PRIVACY,
        "",
        f"You are helping a Grade {_blank(10)} {_blank(30)} teacher improve a unit of {_blank(10)} weeks with {_blank(10)} "
        f"lessons a week. We work through five steps, one at a time. This is step {_blank(8)} of 5: {_blank(45)}.",
        "",
        "The unit as the teacher has planned it:",
        f"{_blank(165)}",
        f"{_blank(165)}",
        "",
        f"Decisions so far: {_blank(135)}",
        "",
        "(the step's description from the website, or your own words for it)",
        "",
        *STEP_FORMAT,
    ])
    final = "\n".join(FINAL_FORMAT)
    return (
        '<section class="page">'
        '<div class="kicker">Without the website</div>'
        '<h2 style="font-size:20pt">Your step prompt</h2>'
        '<p class="note">Fill in the blanks and type the prompt into any AI tool. For a new unit, write '
        '"The teacher is planning a new unit. Topic and goals:" instead of the unit line.</p>'
        f'<div class="prompt">{step_prompt}</div>'
        '<h2 style="font-size:14pt">The final step: ask for the improved plan in this format</h2>'
        f'<div class="prompt">{final}</div>'
        f"{_foot(2)}</section>"
    )


def render_card_html(data: dict) -> str:
    """The complete HTML source of the card. Same JSON in, same text out."""
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n"
        f"<title>{TITLE} — method card</title>\n"
        "<!-- Generated by exports/build-unit-studio-pdf.py from unit-studio-541ebd12/studio-en.json. "
        "Edit the JSON or the script, not this file. -->\n"
        '<link rel="stylesheet" href="../../exports/_guide-print.css">\n'
        f"<style>{STYLE}</style>\n</head>\n<body>\n"
        + _steps_page(data) + "\n" + _prompt_page()
        + "\n</body>\n</html>\n"
    )


def main() -> None:
    from playwright.sync_api import sync_playwright

    data = json.loads(DATA.read_text(encoding="utf-8"))
    SRC.parent.mkdir(parents=True, exist_ok=True)
    SRC.write_text(render_card_html(data), encoding="utf-8")
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
