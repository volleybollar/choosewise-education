#!/usr/bin/env python3
"""Build the Two-Minute Debrief printable pack (A4, 7 pages) from two-minute-debrief/debrief-en.json.

Page 1      the debrief card: four questions to keep in a planner
Pages 2–3   the four exit tickets, with Microsoft Forms and Google Forms steps
Page 4      a fill-in debrief prompt for use without the website
Page 5      a fill-in weekly roll-up prompt
Page 6      one worked debrief in full
Page 7      why it works

Writes the HTML source to _unpublished/exports/two-minute-debrief-pack-a4-en.html
(so the PDF always has an editable source) and the PDF to
assets/pdfs/free/two-minute-debrief-pack-en.pdf.

Usage:
    /usr/bin/python3 exports/build-two-minute-debrief-pdf.py
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "two-minute-debrief/debrief-en.json"
SRC = ROOT / "_unpublished/exports/two-minute-debrief-pack-a4-en.html"
DST = ROOT / "assets/pdfs/free/two-minute-debrief-pack-en.pdf"
URL = "choosewise.education/two-minute-debrief"
TITLE = "Two-Minute Debrief"
PAGES = 7
PRIVACY = "Do not include student names or student results in this conversation."

# Svarsdelen, ordagrant som i assets/js/two-minute-debrief.js;
# test_fill_in_prompts_match_builder håller dem i takt.
DEBRIEF_TAIL = [
    "Reply in plain text, no tables, in exactly this format:",
    "LIKELY CAUSES: two possible explanations, numbered 1 and 2, each tied to this lesson's content, and what would tell them apart. Look beyond the first explanation: missing prior knowledge, too much new at once, a common misconception, a task that did not make students think about the goal, or too little practice.",
    'NEXT LESSON: one concrete move aimed at the more likely cause, with minutes. Not "re-teach".',
    'CHECK FIRST: one quick question or task, written exactly as students will see it, and when to move on, for example "Move on if about 4 in 5 get it right". If the evidence is only a feeling, also say what to look at to turn the feeling into evidence.',
    "ONE QUESTION: one question back to the teacher, to think further.",
]
ROLLUP_HEAD = ("You are helping a teacher look back on a week of lesson debriefs. Each debrief has a date, a group, "
               "a goal, evidence, a surprise and a next step. Some evidence starts with the result of a check from an earlier lesson.")
ROLLUP_TAIL = [
    "Reply in plain text, no tables, in exactly this format:",
    "PATTERNS: up to three patterns across the week that one lesson would not show. After each, name the debriefs it comes from by date and group.",
    'WHAT WORKED: any change whose later check showed improvement. If there are no check results yet, write "Not enough check results yet".',
    "ONE CHANGE FOR NEXT WEEK: one concrete change to the teacher's routine.",
    "ONE QUESTION: one question back to the teacher.",
]

QUESTIONS = [
    ("Goal", "What should students have learned?"),
    ("Evidence", "What did they show? A feeling is fine; counts and patterns are better. No names, no individual results."),
    ("Surprise", "What turned out differently from the plan? (optional)"),
    ("Next", "What comes next with this group, and when?"),
]
REPLY_PARTS = [("likely_causes", "Likely causes"), ("next_lesson", "Next lesson"),
               ("check_first", "Check first"), ("one_question", "One question")]

# Samma tryckstil som de andra paketen (exports/_guide-print.css, Hanken Grotesk 300–500).
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
.cover h1 { font-size: 30pt; font-weight: 300; letter-spacing: -.02em; line-height: 1.05; }
.lede { font-size: 11.5pt; color: var(--color-text); max-width: 160mm; }
.q { border-top: 0.5mm solid var(--color-highlight); padding-top: 2mm; display: flex; flex-direction: column; gap: 1mm; }
.q h2 { font-size: 15pt; }
.q p { font-size: 9.5pt; }
.line { border-bottom: 0.3mm solid var(--color-border); height: 8mm; }
.privacy { font-size: 9pt; color: var(--color-text); border: 0.35mm solid var(--color-accent); border-radius: 1.5mm; padding: 2.5mm 4mm; }
.ticket { border: 0.35mm solid var(--color-border); border-radius: 1.5mm; padding: 4.5mm 6mm; display: flex; flex-direction: column; gap: 2mm; flex: 1; }
.ticket h2 { font-size: 15pt; }
.ticket .when { font-size: 9.5pt; color: var(--color-text); }
.student { border: 0.3mm dashed var(--color-text-muted); border-radius: 1mm; padding: 3mm 4mm; font-size: 10pt; color: var(--color-text); white-space: pre-line; }
.setup { display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; font-size: 8.4pt; }
.setup h3 { font-size: 9pt; margin-bottom: 1mm; }
.setup ol { padding-left: 4mm; display: flex; flex-direction: column; gap: .6mm; }
.prompt { border: 0.35mm dashed var(--color-accent); border-radius: 1.5mm; padding: 5.5mm 7mm; font-family: 'SF Mono', Menlo, monospace; font-size: 8.4pt; line-height: 1.55; color: var(--color-text); white-space: pre-wrap; }
.blank { display: inline-block; border-bottom: 0.3mm solid var(--color-text); }
.note { font-size: 8.8pt; color: var(--color-text-muted); }
.example { display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; font-size: 9.4pt; }
.example h3 { font-size: 10pt; text-transform: uppercase; letter-spacing: .08em; color: var(--color-text-muted); margin-bottom: 1.5mm; }
.example dt { font-weight: 500; color: var(--color-text); margin-top: 2mm; }
.example dd { white-space: pre-line; }
.chip { display: inline-block; border: 0.35mm solid var(--color-accent); color: var(--color-accent); border-radius: 1mm; padding: .3mm 2mm; font-weight: 500; font-size: 8pt; }
.chip--strong { background: var(--color-accent); color: var(--color-bg); }
.approach h3 { font-size: 11pt; margin-bottom: 1mm; display: flex; gap: 2mm; align-items: center; }
.approach p { font-size: 9pt; }
.foot { margin-top: auto; font-size: 7.5pt; color: var(--color-text-muted); border-top: 0.3mm solid var(--color-border); padding-top: 2.5mm; display: flex; justify-content: space-between; }
"""


def _foot(page_no: int) -> str:
    return f'<div class="foot"><span>{TITLE} · {URL}</span><span>{page_no} / {PAGES}</span></div>'


def _blank(mm: int) -> str:
    return f'<span class="blank" style="width:{mm}mm"></span>'


def _card() -> str:
    """Debriefkortet: de fyra frågorna med skrivrader."""
    qs = "".join(
        f'<div class="q"><h2>{name}</h2><p>{escape(hint)}</p><div class="line"></div><div class="line"></div></div>'
        for name, hint in QUESTIONS
    )
    return (
        '<section class="page cover">'
        '<div class="kicker">Pedagogy + AI · Grades 6–12 · free printable pack</div>'
        f"<h1>{TITLE}</h1>"
        "<p class=\"lede\">For the lessons that didn't go as planned. Answer four questions, then paste them into the "
        f"prompt on page 4 or at {URL}. <strong>Run it before you meet the group again.</strong></p>"
        f"{qs}"
        f'<p class="privacy"><strong>{PRIVACY}</strong> Describe what the group showed in counts and patterns.</p>'
        '<p class="note">The loop closes itself: the result of the check becomes the evidence in your next debrief for that group.</p>'
        f"{_foot(1)}</section>"
    )


def _ticket(t: dict) -> str:
    forms = "".join(f"<li>{escape(s)}</li>" for s in t["forms_steps"])
    google = "".join(f"<li>{escape(s)}</li>" for s in t["google_steps"])
    return (
        f'<div class="ticket"><h2>{escape(t["name"])}</h2>'
        f'<p class="when">{escape(t["when"])}</p>'
        f'<div class="student">{escape(t["student_text"])}</div>'
        f'<div class="setup"><div><h3>Microsoft Forms</h3><ol>{forms}</ol></div>'
        f'<div><h3>Google Forms</h3><ol>{google}</ol></div></div>'
        f'<p class="note">{escape(t["paper_note"])}</p></div>'
    )


def _tickets(tickets: list, page_no: int) -> str:
    return (
        '<section class="page">'
        f'<div class="kicker">Exit tickets · {page_no - 1} of 2</div>'
        + "".join(_ticket(t) for t in tickets)
        + f"{_foot(page_no)}</section>"
    )


def _fill_in_debrief() -> str:
    # Raderna är ordagrant desamma som i debriefens promptbyggare, utom att
    # lärarens uppgifter är luckor.
    prompt = "\n".join([
        PRIVACY,
        "",
        f"You are helping a Grade {_blank(12)} teacher think through a lesson with {_blank(40)} that did not go as planned. "
        "Base everything on what the teacher writes below, and tie every point to this lesson's content.",
        "",
        f"Goal: {_blank(150)}",
        f"Evidence: {_blank(140)}",
        f"{_blank(160)}",
        f"Surprise: {_blank(140)}",
        f"Next: {_blank(150)}",
        "",
        *DEBRIEF_TAIL,
    ])
    return (
        '<section class="page">'
        '<div class="kicker">Without the website</div>'
        '<h2 style="font-size:22pt">Your debrief prompt</h2>'
        '<p class="note">Fill in the blanks, then type the prompt into any AI tool: Copilot, Gemini, ChatGPT or Claude. '
        f'With no surprise, write "None given". Faster online: the builder at {URL} fills this in and can save debriefs for the end of the day.</p>'
        f'<div class="prompt">{prompt}</div>'
        f"{_foot(4)}</section>"
    )


def _fill_in_rollup() -> str:
    prompt = "\n".join([
        PRIVACY,
        "",
        ROLLUP_HEAD,
        "",
        "Debriefs:",
        f"{_blank(160)}",
        f"{_blank(160)}",
        f"{_blank(160)}",
        f"{_blank(160)}",
        "",
        *ROLLUP_TAIL,
    ])
    return (
        '<section class="page">'
        '<div class="kicker">Once a week</div>'
        '<h2 style="font-size:22pt">Your weekly roll-up prompt</h2>'
        "<p class=\"note\">Write one line per debrief from the week: date, group, goal, evidence, surprise and next. "
        "Rows from the unit journal work too. The roll-up finds patterns one lesson wouldn't show.</p>"
        f'<div class="prompt">{prompt}</div>'
        f"{_foot(5)}</section>"
    )


def _example(ex: dict) -> str:
    answers = "".join(
        f"<dt>{name}</dt><dd>{escape(ex[name.lower()])}</dd>" for name, _ in QUESTIONS
    )
    reply = "".join(f"<dt>{label}</dt><dd>{escape(ex['reply'][key])}</dd>" for key, label in REPLY_PARTS)
    return (
        '<section class="page">'
        '<div class="kicker">A worked debrief</div>'
        f'<h2 style="font-size:22pt">{escape(ex["title"])} · {escape(ex["group"])}, Grade {int(ex["grade"])}</h2>'
        f'<div class="example"><div><h3>The teacher writes</h3><dl>{answers}</dl></div>'
        f'<div><h3>The AI replies</h3><dl>{reply}</dl></div></div>'
        f"{_foot(6)}</section>"
    )


def _evidence(data: dict) -> str:
    labels = data["labels"]
    approaches = "".join(
        f'<div class="approach"><h3>{escape(a["name"])} <span class="chip chip--{escape(a["label"])}">{escape(labels[a["label"]]["name"])}</span></h3>'
        f'<p>{escape(a["evidence"])}</p></div>'
        for a in data["approaches"]
    )
    legend = " ".join(f'<strong>{escape(labels[k]["name"])}:</strong> {escape(labels[k]["definition"])}'
                      for k in ("strong", "promising", "framework"))
    return (
        '<section class="page">'
        '<div class="kicker">Why it works</div>'
        '<h2 style="font-size:22pt">The research behind the debrief</h2>'
        f'<p class="note">{legend}</p>'
        f"{approaches}"
        f'<p class="note">Sources and links: {URL}</p>'
        f"{_foot(7)}</section>"
    )


def render_pack_html(data: dict) -> str:
    """The complete HTML source of the pack. Same JSON in, same text out."""
    tickets = data["exit_tickets"]
    hero = next(e for e in data["examples"] if e["id"] == data["hero_example"])
    pages = [_card(), _tickets(tickets[:2], 2), _tickets(tickets[2:], 3), _fill_in_debrief(),
             _fill_in_rollup(), _example(hero), _evidence(data)]
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n"
        f"<title>{TITLE} — printable pack</title>\n"
        "<!-- Generated by exports/build-two-minute-debrief-pdf.py from two-minute-debrief/debrief-en.json. "
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
