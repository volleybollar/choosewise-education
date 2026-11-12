#!/usr/bin/env python3
"""Bygger kortleken Study Moves (A4, 13 sidor) från study-moves/moves-en.json.

Sida 1      framsida: målen och deras drag, startdraget, varför bra studier
            känns svårare och evidensetiketterna
Sida 2–11   ett kort per drag: steg, exempel, hur det känns, båda AI-versionerna
            med texten till AI:n, se upp och evidens
Sida 12     luckprompt för läraren
Sida 13     luckprompt för eleven, med åldersreglerna

Skriver HTML-källan till _unpublished/exports/study-moves-cards-a4-en.html
(så att PDF:en alltid har en redigerbar källa) och PDF:en till
assets/pdfs/free/study-moves-cards-en.pdf.

Användning:
    /usr/bin/python3 exports/build-study-moves-pdf.py
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "study-moves/moves-en.json"
SRC = ROOT / "_unpublished/exports/study-moves-cards-a4-en.html"
DST = ROOT / "assets/pdfs/free/study-moves-cards-en.pdf"
URL = "choosewise.education/study-moves"
TITLE = "Study Moves"
PAGES = 13
LABEL_ORDER = ("strong", "promising", "framework")

# Kortens utseende: samma tryckstil som kortleken för Lesson Lens, och den
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
.meta { display: flex; gap: 3mm; align-items: center; font-size: 9.5pt; color: var(--color-text-muted); margin-top: 2mm; }
.ex { border-left: 1mm solid var(--color-highlight); background: var(--color-bg-alt); padding: 3.5mm 6mm; display: flex; flex-direction: column; gap: 1.5mm; }
.ex h3 { font-size: 11pt; }
.ex h3 span { font-weight: 400; color: var(--color-text-muted); }
.part { font-size: 8pt; letter-spacing: .08em; text-transform: uppercase; color: var(--color-accent); font-weight: 500; margin-bottom: 1mm; }
.steps { padding-left: 5mm; display: flex; flex-direction: column; gap: .8mm; }
.feels { border-left: 1mm solid var(--color-highlight); padding-left: 4mm; color: var(--color-text); }
.ai { display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; }
.ai > div { border-top: 0.5mm solid var(--color-accent); padding-top: 2mm; display: flex; flex-direction: column; gap: 1.5mm; }
.for-ai { font-size: 9pt; color: var(--color-text); background: var(--color-bg-alt); padding: 2mm 3mm; border-radius: 1mm; }
.evidence { font-size: 9pt; color: var(--color-text-muted); }
.foot { margin-top: auto; font-size: 7.5pt; color: var(--color-text-muted); border-top: 0.3mm solid var(--color-border); padding-top: 2.5mm; display: flex; justify-content: space-between; }
.cover h1 { font-size: 34pt; font-weight: 300; letter-spacing: -.02em; line-height: 1.05; }
.cover .lede { font-size: 12pt; color: var(--color-text); max-width: 160mm; }
.start { border: 0.35mm solid var(--color-highlight); border-radius: 1.5mm; padding: 4mm 5mm; color: var(--color-text); }
.goals { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm 6mm; font-size: 9.5pt; }
.goals div { border-top: 0.5mm solid var(--color-accent); padding-top: 1.5mm; }
.goals strong { color: var(--color-text); display: block; }
.moves { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5mm 8mm; font-size: 9.5pt; }
.legend { display: flex; flex-direction: column; gap: 2mm; font-size: 9pt; }
.prompt { border: 0.35mm dashed var(--color-accent); border-radius: 1.5mm; padding: 6mm 7mm; font-family: 'SF Mono', Menlo, monospace; font-size: 8.6pt; line-height: 1.65; color: var(--color-text); white-space: pre-wrap; }
.blank { display: inline-block; border-bottom: 0.3mm solid var(--color-text); }
"""


def _foot(page_no: int) -> str:
    return f'<div class="foot"><span>{TITLE} · {URL}</span><span>{page_no} / {PAGES}</span></div>'


def _chip(key: str, labels: dict) -> str:
    return f'<span class="chip chip--{escape(key)}">{escape(labels[key]["name"])}</span>'


def _cover(data: dict) -> str:
    labels = data["labels"]
    by_id = {m["id"]: m for m in data["moves"]}
    start = by_id[data["default_move"]]
    goals = "".join(
        f'<div><strong>{escape(g["name"])}</strong>'
        + ", ".join(f'{int(by_id[mid]["number"])}. {escape(by_id[mid]["name"])}' for mid in g["moves"])
        + "</div>"
        for g in data["goals"]
    )
    moves = "".join(
        f'<p>{int(m["number"])}. {escape(m["name"])} {_chip(m["label"], labels)}</p>' for m in data["moves"]
    )
    legend = "".join(f'<p>{_chip(k, labels)} {escape(labels[k]["definition"])}</p>' for k in LABEL_ORDER)
    return (
        '<section class="page cover">'
        '<div class="kicker">Study + AI · Grades 7–12 · free card deck</div>'
        f"<h1>{TITLE}</h1>"
        '<p class="lede">Ten ways to study that research shows work. Pick what you want to do, '
        "then use the move with a book, pen and paper. Your teacher can prepare it with AI, "
        "and if you are 13 or older you can study with AI.</p>"
        f'<p class="start"><strong>Not sure? Start here: {escape(start["name"])}.</strong> '
        f'{escape(start["one_liner"])}</p>'
        f'<h3>What do you want to do?</h3><div class="goals">{goals}</div>'
        f'<h3>Why good studying feels harder</h3><p class="feels">{escape(data["feels_harder"]["text"])}</p>'
        f'<h3>The ten moves</h3><div class="moves">{moves}</div>'
        f'<h3>How strong is the evidence?</h3><div class="legend">{legend}</div>'
        f"{_foot(1)}</section>"
    )


def _card(move: dict, data: dict, page_no: int) -> str:
    ex = move["example"]
    goal_names = {g["id"]: g["name"] for g in data["goals"]}
    goals = " · ".join(escape(goal_names[g]) for g in move["goals"])
    steps = "".join(f"<li>{escape(s)}</li>" for s in move["steps"])
    return (
        '<section class="page">'
        f'<div class="top"><div class="kicker">Move {int(move["number"])} · Good for: {goals}</div>'
        f'<h2>{escape(move["name"])}</h2>'
        f'<p class="meta">{_chip(move["label"], data["labels"])} {escape(move["research_name"])}</p></div>'
        f'<p class="oneliner">{escape(move["one_liner"])}</p>'
        f'<div><h3 class="part">How to do it</h3><ol class="steps">{steps}</ol></div>'
        f'<div class="ex"><h3>Example: {escape(ex["subject"])} <span>· Grade {int(ex["grade"])}</span></h3>'
        f'<p>{escape(ex["text"])}</p></div>'
        f'<div><h3 class="part">How it feels</h3><p class="feels">{escape(move["feels"])}</p></div>'
        '<div class="ai">'
        f'<div><h3 class="part">With AI: your teacher</h3><p>{escape(move["teacher_ai"]["card"])}</p>'
        f'<p class="for-ai"><strong>For the AI (teacher).</strong> {escape(move["teacher_ai"]["brief"])}</p></div>'
        f'<div><h3 class="part">With AI: you (13+)</h3><p>{escape(move["student_ai"]["card"])}</p>'
        f'<p class="for-ai"><strong>For the AI (student).</strong> {escape(move["student_ai"]["brief"])}</p></div>'
        "</div>"
        f'<div><h3 class="part">Watch out</h3><p>{escape(move["watch_out"])}</p></div>'
        f'<p class="evidence"><strong>Evidence.</strong> {escape(move["evidence"])}</p>'
        f"{_foot(page_no)}</section>"
    )


def _blank(mm: int) -> str:
    return f'<span class="blank" style="width:{mm}mm"></span>'


def _teacher_fill_in() -> str:
    # Raderna är ordagrant desamma som i teacherLines i assets/js/study-moves.js,
    # utom att lärarens uppgifter är luckor. test_teacher_fill_in_matches_js
    # håller dem i takt.
    prompt = "\n".join([
        "Do not include student names or student work in this conversation.",
        "",
        f"You are helping a Grade {_blank(12)} {_blank(40)} teacher prepare study material "
        "that students will use on their own, on paper and without AI.",
        "",
        f"Study move: {_blank(50)} (the move's name and one-line description from its card)",
        f"What to make: {_blank(60)} (the \"For the AI (teacher)\" text from its card)",
        "",
        f"Topic: {_blank(140)}",
        f"Students already know: {_blank(110)}",
        "",
        escape("Use only this topic's content. Do not repeat a question. If you write multiple-choice "
               "questions, make all options about the same length.", quote=False),
        "",
        "Reply in plain text, no tables, with exactly these four parts:",
        escape("MOVE: the move's name and one sentence, written to students, on why it works.", quote=False),
        "FOR STUDENTS: the material, written to the students and ready to print.",
        "ANSWERS: the answers or a checklist students use to check their own work, numbered Q1:, Q2: "
        "and so on to match.",
        escape('CHECK: every fact, figure, date or source in FOR STUDENTS or ANSWERS that the teacher '
               'should verify, one per line. Write "None" if there are none.', quote=False),
    ])
    return (
        '<section class="page">'
        '<div class="kicker">Without the website · for teachers</div>'
        '<h2 style="font-size:24pt">Your own prompt: teacher</h2>'
        '<p class="oneliner">Fill in the blanks, then type the prompt into any AI tool: Copilot, Gemini, '
        'ChatGPT or Claude. Leave out the line "Students already know" if you have nothing to add. '
        "Check the material before you hand it out: the AI proposes, you decide.</p>"
        f'<div class="prompt">{prompt}</div>'
        f'<p class="evidence">Faster online: the prompt builder at {URL} fills this in for you. '
        "Students use the material on paper, without AI.</p>"
        f"{_foot(12)}</section>"
    )


def _student_fill_in(data: dict) -> str:
    # Raderna är ordagrant desamma som i studentLines i assets/js/study-moves.js,
    # utom att elevens uppgifter är luckor. test_student_fill_in_matches_js
    # håller dem i takt.
    prompt = "\n".join([
        "Do not include your name or other personal details in this conversation.",
        "",
        f"You are my study partner. I am a Grade {_blank(12)} student studying {_blank(36)}.",
        f"Topic: {_blank(140)}",
        f"What I already know: {_blank(110)}",
        "",
        f"Study move: {_blank(50)} (the move's name and one-line description from its card)",
        f"Your role: {_blank(60)} (the \"For the AI (student)\" text from its card)",
        "",
        "Rules for the whole conversation:",
        "- Give me one question or task at a time, then wait for my answer.",
        "- Never give me the answer to a question before I have tried it. If I am stuck, give a small hint first.",
        "- Keep every message short.",
        "- Do not write my homework, essays or answers for me, even if I ask.",
        "- If you are not sure a fact is right, say so. I will check facts in my textbook or notes.",
        "",
        "Start now.",
    ])
    rules = " ".join(f"<strong>{escape(r['tool'])}:</strong> {escape(r['rule'])}" for r in data["age_rules"])
    return (
        '<section class="page">'
        '<div class="kicker">Without the website · for students aged 13 and over</div>'
        '<h2 style="font-size:24pt">Your own prompt: student</h2>'
        '<p class="oneliner">Fill in the blanks, then type the prompt into your AI tool. '
        'Leave out the line "What I already know" if you have nothing to add. '
        "The AI asks and you answer: you do the thinking.</p>"
        f'<div class="prompt">{prompt}</div>'
        f'<p class="evidence"><strong>AI tools and age rules ({escape(data["age_rules_date"])}).</strong> {rules} '
        "Rules change often: check your school's rules and your national rules before you start. "
        "You never need AI to use a move.</p>"
        f"{_foot(13)}</section>"
    )


def render_deck_html(data: dict) -> str:
    """Hela kortlekens HTML-källa. Samma JSON in ger samma text ut."""
    pages = [_cover(data)]
    pages += [_card(m, data, i) for i, m in enumerate(data["moves"], start=2)]
    pages += [_teacher_fill_in(), _student_fill_in(data)]
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n"
        f"<title>{TITLE} — card deck</title>\n"
        "<!-- Generated by exports/build-study-moves-pdf.py from study-moves/moves-en.json. "
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
