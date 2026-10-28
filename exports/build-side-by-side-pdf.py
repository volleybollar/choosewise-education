#!/usr/bin/env python3
"""Build the two Side by Side PDFs from side-by-side/pairs-en.json.

Student sheet (A4, 1 page, layout B): room for A and B on top, the three
comparison columns, "The rule we found", case C and a Think back line. It is
the students' answer sheet; the FOR STUDENTS block from the AI is printed or
shown alongside it. Nothing on it says that an AI made the pair.

Card deck (A4, 7 pages):
Page 1     cover: how to run it, the four steps, the two levels, the labels
Pages 2–6  one card per pair type, with the worked example shown as a pair
Page 7     a fill-in prompt for use without the website

Writes the HTML sources to _unpublished/exports/ (so each PDF always has an
editable source) and the PDFs to assets/pdfs/free/.

Usage:
    /usr/bin/python3 exports/build-side-by-side-pdf.py
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "side-by-side/pairs-en.json"
SHEET_SRC = ROOT / "_unpublished/exports/side-by-side-sheet-a4-en.html"
DECK_SRC = ROOT / "_unpublished/exports/side-by-side-cards-a4-en.html"
SHEET_DST = ROOT / "assets/pdfs/free/side-by-side-sheet-en.pdf"
DECK_DST = ROOT / "assets/pdfs/free/side-by-side-cards-en.pdf"
URL = "choosewise.education/side-by-side"
TITLE = "Side by Side"
EASIER_ONLY = "Easier to see only: AI tools could not build this pair reliably at the harder level."

# Regelraden och svarsdelarna, ordagrant som i assets/js/side-by-side.js;
# test_fill_in_matches_builder_word_for_word håller dem i takt.
RULES = "Rules: A and B respond to the same task and are as alike as possible apart from the difference this pair type asks for. Each of A and B is at most 60 words or six short lines, so it fits half a page width. Case C can be decided with the rule. Do not invent studies, measurements or sources; a source written for the task must say so. Write for students in this grade."
PROMPT_PARTS = [
    "Reply in plain text, no tables, in two blocks. The first block is printed for students, so it must not contain anything from the second.",
    "FOR STUDENTS",
    "TASK: the question or task both A and B respond to",
    "A: a short label, then the first item",
    "B: a short label, then the second item",
    "CASE C: a new case the rule decides, without its answer",
    "THINK BACK: one short sentence starter with a single blank, about how they thought, not what they found",
    "TEACHER KEY",
    "ONLY A: what only A has or does",
    "BOTH: what A and B share",
    "ONLY B: what only B has or does",
    "THE RULE: the principle students should reach, in one or two sentences",
    "CASE C ANSWER: the answer, and how the rule decides it",
    "PROBE: one follow-up question that pushes past the first answer",
    'CHECK: only the facts, figures, dates or sources in TASK, A, B or CASE C that could be wrong, quoted or closely paraphrased, most doubtful first, one per line, at most six lines. Write "None" if there are none.',
]

COLUMNS = [("only_a", "Only A"), ("both", "Both"), ("only_b", "Only B")]
KEY_PARTS = [("rule", "The rule"), ("case_c", "Case C"), ("case_c_answer", "Case C answer"),
             ("probe", "Probe"), ("think_back", "Think back")]

# Utseendet följer Flawed Answers kortlek och den delade tryckstilen
# exports/_guide-print.css, som laddar Hanken Grotesk 300–500.
# Inga hexfärger här: bara var(--…) från tryckstilen.
STYLE = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: var(--color-bg); }
body { font-family: var(--font-body); color: var(--color-text-soft); font-size: 10pt; line-height: 1.42; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
strong, b { font-weight: 500; }
.page { width: 210mm; height: 297mm; padding: 15mm 17mm 18mm; display: flex; flex-direction: column; gap: 4mm; page-break-after: always; overflow: hidden; }
.page:last-child { page-break-after: auto; }
h1, h2, h3, h4 { font-family: var(--font-display); font-weight: 500; color: var(--color-text); }
.kicker { font-size: 7.5pt; letter-spacing: .12em; text-transform: uppercase; color: var(--color-highlight-ink); font-weight: 500; }
.top { display: grid; grid-template-columns: 20mm 1fr; gap: 6mm; align-items: center; border-bottom: 0.6mm solid var(--color-accent); padding-bottom: 4mm; }
.top img { width: 20mm; height: 20mm; }
.top h2 { font-size: 24pt; line-height: 1.05; letter-spacing: -.01em; margin-top: 1mm; }
.oneliner { font-size: 12pt; color: var(--color-text); }
.look { display: flex; flex-direction: column; gap: 1mm; padding-left: 5mm; font-size: 9.5pt; }
.label { font-size: 8pt; letter-spacing: .08em; text-transform: uppercase; color: var(--color-accent); font-weight: 500; }
.only { font-size: 9.5pt; color: var(--color-highlight-ink); }
.chip { display: inline-block; border: 0.35mm solid var(--color-accent); color: var(--color-accent); border-radius: 1mm; padding: .3mm 2mm; font-weight: 500; font-size: 8pt; }
.chip--strong { background: var(--color-accent); color: var(--color-bg); }
.ex { border-left: 1mm solid var(--color-highlight); background: var(--color-bg-alt); padding: 4mm 5mm; display: flex; flex-direction: column; gap: 2.2mm; font-size: 9.6pt; }
.ex h3 { font-size: 11pt; }
.ex h3 span { font-weight: 400; color: var(--color-text-muted); }
.ab { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; }
.item { border: 0.3mm solid var(--color-border); background: var(--color-bg); border-radius: 1mm; padding: 2.5mm 3.5mm; color: var(--color-text); }
.item .label { display: block; margin-bottom: 1mm; }
.cols { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; }
.cols div { padding: 2mm 2.5mm; border-radius: 1mm; }
.cols div:nth-child(2) { background: var(--color-bg); }
.cols .label { display: block; margin-bottom: .8mm; }
.ex dl { display: grid; grid-template-columns: 28mm 1fr; gap: 1.1mm 4mm; }
.ex dt { font-size: 8pt; letter-spacing: .08em; text-transform: uppercase; color: var(--color-accent); font-weight: 500; padding-top: .5mm; }
.for-ai { font-size: 9.2pt; color: var(--color-text); }
.evidence { font-size: 9pt; color: var(--color-text-muted); }
.foot { margin-top: auto; font-size: 7.5pt; color: var(--color-text-muted); border-top: 0.3mm solid var(--color-border); padding-top: 2.5mm; display: flex; justify-content: space-between; }
.cover h1, .sheet h1 { font-size: 34pt; font-weight: 300; letter-spacing: -.02em; line-height: 1.05; }
.lede { font-size: 12pt; color: var(--color-text); max-width: 160mm; }
.how { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4mm; font-size: 9pt; }
.how div { border-top: 0.5mm solid var(--color-highlight); padding-top: 2mm; }
.levels { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm 8mm; font-size: 9pt; }
.levels div { border-top: 0.5mm solid var(--color-accent); padding-top: 2mm; }
.legend { display: flex; flex-direction: column; gap: 2mm; font-size: 9pt; }
.note { font-size: 9.5pt; color: var(--color-text); font-weight: 500; }
.prompt { border: 0.35mm dashed var(--color-accent); border-radius: 1.5mm; padding: 4.5mm 5.5mm; font-family: 'SF Mono', Menlo, monospace; font-size: 7.8pt; line-height: 1.55; color: var(--color-text); white-space: pre-wrap; }
.blank { display: inline-block; border-bottom: 0.3mm solid var(--color-text); }
.names { display: flex; gap: 8mm; font-size: 10pt; color: var(--color-text); }
.names span { flex: 1; border-bottom: 0.3mm solid var(--color-border); padding-bottom: 1mm; }
.task { font-size: 10pt; color: var(--color-text); border-bottom: 0.3mm solid var(--color-border); padding-bottom: 5mm; }
.paste { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; flex: 0 0 52mm; }
.paste div { border: 0.35mm dashed var(--color-border); border-radius: 1.5mm; padding: 3mm 4mm; color: var(--color-text-muted); font-size: 9pt; }
.paste strong { display: block; font-size: 14pt; color: var(--color-text); }
.compare { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; flex: 1; }
.compare div { border: 0.35mm solid var(--color-border); border-top: 0.8mm solid var(--color-accent); border-radius: 1mm; padding: 3mm 4mm; }
.compare div:nth-child(2) { background: var(--color-bg-alt); }
.compare h3, .rule-box h3, .case h3 { font-size: 12pt; }
.rule-box { border: 0.6mm solid var(--color-highlight); border-radius: 1.5mm; padding: 3mm 4mm; height: 30mm; }
.case { border: 0.35mm solid var(--color-border); border-radius: 1mm; padding: 3mm 4mm; height: 30mm; }
.case p, .rule-box p { font-size: 9pt; color: var(--color-text-muted); }
.think { border-top: 0.6mm solid var(--color-highlight); padding-top: 2.5mm; font-size: 10pt; color: var(--color-text); }
.think .line { display: block; border-bottom: 0.3mm solid var(--color-border); height: 9mm; }
"""


def _doc(title: str, pages: list) -> str:
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n"
        f"<title>{title}</title>\n"
        "<!-- Genererad av exports/build-side-by-side-pdf.py från side-by-side/pairs-en.json. "
        "Ändra i JSON-filen eller skriptet, inte här. -->\n"
        '<link rel="stylesheet" href="../../exports/_guide-print.css">\n'
        f"<style>{STYLE}</style>\n</head>\n<body>\n"
        + "\n".join(pages)
        + "\n</body>\n</html>\n"
    )


def _foot(right: str) -> str:
    return f'<div class="foot"><span>{TITLE} · {URL}</span><span>{right}</span></div>'


def render_sheet_html(data: dict) -> str:
    """The one-page student answer sheet, layout B (Johan's choice)."""
    compare = "".join(f"<div><h3>{heading}</h3></div>" for _, heading in COLUMNS)
    page = (
        '<section class="page sheet">'
        '<div class="kicker">Student sheet</div>'
        f"<h1>{TITLE}</h1>"
        '<div class="names"><span>Names:</span><span>Date:</span></div>'
        '<p class="task"><strong>Task:</strong></p>'
        '<div class="paste"><div><strong>A</strong>Paste, staple or copy A here</div>'
        '<div><strong>B</strong>Paste, staple or copy B here</div></div>'
        f'<div class="compare">{compare}</div>'
        '<div class="rule-box"><h3>The rule we found</h3><p>In one or two sentences: what does the comparison show?</p></div>'
        '<div class="case"><h3>Try it on case C</h3><p>Use your rule on the new case. What is the answer, and why?</p></div>'
        '<div class="think"><strong>Think back.</strong> One sentence about how you thought, not what you found.'
        '<span class="line"></span></div>'
        f'{_foot("Fill in the three columns before anyone explains the difference.")}</section>'
    )
    return _doc(f"{TITLE} — student sheet", [page])


def _cover(data: dict) -> str:
    steps = "".join(f'<div><strong>{escape(s["name"])}</strong><br>{escape(s["prompt"])}</div>' for s in data["steps"])
    levels = "".join(f'<div><strong>{escape(lv["name"])}</strong><br>{escape(lv["instruction"])}</div>'
                     for lv in data["levels"])
    labels = data["labels"]
    legend = "".join(
        f'<p><span class="chip chip--{k}">{escape(labels[k]["name"])}</span> {escape(labels[k]["definition"])}</p>'
        for k in labels if k != "note"
    )
    # Framsidan visar bara påståendena med etikett; studierna och källorna
    # står på webbsidan (hela texterna fick inte plats på en A4).
    evidence = "".join(
        f'<p><span class="chip chip--{escape(e["label"])}">{escape(labels[e["label"]]["name"])}</span> '
        f'{escape(e["claim"])}</p>'
        for e in data["evidence"]
    ) + f'<p>Findings, limits and sources for each claim: {URL}</p>'
    return (
        '<section class="page cover">'
        '<div class="kicker">Think + AI · Grades 7–12 · free card deck</div>'
        f"<h1>{TITLE}</h1>"
        '<p class="lede">Use any AI tool to build two items placed side by side: two solutions, cases, concepts or sources. '
        'Students compare them, write the rule they found and try it on a new case, in about fifteen minutes.</p>'
        f'<h3>Four steps</h3><div class="how">{steps}</div>'
        f'<h3>Two levels</h3><div class="levels">{levels}</div>'
        '<p class="evidence">Copy only the FOR STUDENTS block for students. Before you print, read the TEACHER KEY and check '
        'everything listed under CHECK. Let students write the rule before you confirm it.</p>'
        f'<h3>How strong is the evidence?</h3><div class="legend">{legend}{evidence}</div>'
        f'<p class="note">{escape(labels["note"])}</p>'
        f'{_foot("1 / 7")}</section>'
    )


def _item(letter: str, label: str, text: str) -> str:
    lines = "<br>".join(escape(line) for line in text.splitlines())
    return f'<div class="item"><span class="label">{letter} · {escape(label)}</span>{lines}</div>'


def _card(pair: dict, data: dict, page_no: int) -> str:
    ex = pair["example"]
    labels = data["labels"]
    level = {lv["id"]: lv["name"] for lv in data["levels"]}[ex["level"]]
    look = "".join(f"<li>{escape(s)}</li>" for s in pair["look_for"])
    cols = "".join(f'<div><span class="label">{heading}</span>{escape(ex[k])}</div>' for k, heading in COLUMNS)
    key = "".join(f"<dt>{label}</dt><dd>{escape(ex[k])}</dd>" for k, label in KEY_PARTS)
    only = f'<p class="only">{EASIER_ONLY}</p>' if not pair["harder_ok"] else ""
    chip = f'<span class="chip chip--{escape(pair["label"])}">{escape(labels[pair["label"]]["name"])}</span>'
    return (
        '<section class="page">'
        f'<div class="top"><img src="../../side-by-side/icons/{escape(pair["id"])}.svg" alt=""><div>'
        f'<div class="kicker">Pair {int(pair["number"])}</div>'
        f'<h2>{escape(pair["name"])}</h2></div></div>'
        f'<p class="oneliner">{escape(pair["one_liner"])}</p>'
        f'<div><div class="label">What to look for</div><ul class="look">{look}</ul></div>'
        f"{only}"
        f'<div class="ex"><h3>{escape(ex["subject"])} <span>· Grade {int(ex["grade"])} · {escape(level)}</span></h3>'
        f'<p><strong>Task:</strong> {escape(ex["task"])}</p>'
        f'<div class="ab">{_item("A", ex["a_label"], ex["a"])}{_item("B", ex["b_label"], ex["b"])}</div>'
        f'<div class="cols">{cols}</div>'
        f"<dl>{key}</dl></div>"
        f'<p class="for-ai"><strong>For the AI.</strong> {escape(pair["prompt_brief"])}</p>'
        f'<p class="evidence"><strong>Evidence.</strong> {chip} Comparing cases in general: Strong. '
        f'Labels rate research on teaching with comparisons regularly, not a single use.</p>'
        f'{_foot(f"{page_no} / 7")}</section>'
    )


def _fill_in() -> str:
    def blank(mm: int) -> str:
        return f'<span class="blank" style="width:{mm}mm"></span>'

    prompt = "\n".join([
        "Do not include student names or student work in this conversation.",
        "",
        f"You are helping a Grade {blank(12)} {blank(40)} teacher prepare a fifteen-minute \"Side by Side\" task. "
        "Students compare two items placed next to each other: what is only in A, what is in both, and what is only in B. "
        "Then they write the rule they found and try it on a new case C. Students work on paper, without AI.",
        "",
        f"Lesson topic: {blank(110)}",
        f"Students already know (optional): {blank(70)}",
        "",
        f"Pair type: {blank(60)} (copy the name and one-line description from its card)",
        f"How to build the pair: {blank(30)} (copy the \"For the AI\" text from its card)",
        f"Difficulty: {blank(60)} (copy one level from the cover)",
        "",
        escape(RULES),
        "",
        *[escape(p) for p in PROMPT_PARTS],
    ])
    return (
        '<section class="page">'
        '<div class="kicker">Without the website</div>'
        '<h2 style="font-size:24pt">Your own pair</h2>'
        '<p class="oneliner">Fill in the blanks, then type the prompt into any AI tool: Copilot, Gemini, ChatGPT or Claude. '
        'Check the key before the lesson, especially anything under CHECK.</p>'
        f'<div class="prompt">{prompt}</div>'
        '<p class="evidence">Faster online: the prompt builder at ' + URL + ' fills this in for you. '
        'Students need no AI for the main task. If older students use AI themselves, check the tool\'s age rules, '
        'your national rules and your school policy first.</p>'
        f'{_foot("7 / 7")}</section>'
    )


def render_deck_html(data: dict) -> str:
    """The complete HTML source of the deck. Same JSON in, same text out."""
    pages = [_cover(data)]
    pages += [_card(p, data, i) for i, p in enumerate(data["pairs"], start=2)]
    pages.append(_fill_in())
    return _doc(f"{TITLE} — card deck", pages)


def _pdf(page, src: Path, dst: Path) -> None:
    page.goto(src.as_uri(), wait_until="networkidle")
    page.emulate_media(media="print")
    page.pdf(path=str(dst), format="A4", print_background=True,
             margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
             prefer_css_page_size=True)
    print(f"Built {dst.relative_to(ROOT)} from {src.relative_to(ROOT)}")


def main() -> None:
    from playwright.sync_api import sync_playwright

    data = json.loads(DATA.read_text(encoding="utf-8"))
    SHEET_SRC.parent.mkdir(parents=True, exist_ok=True)
    SHEET_SRC.write_text(render_sheet_html(data), encoding="utf-8")
    DECK_SRC.write_text(render_deck_html(data), encoding="utf-8")
    SHEET_DST.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        _pdf(page, SHEET_SRC, SHEET_DST)
        _pdf(page, DECK_SRC, DECK_DST)
        browser.close()


if __name__ == "__main__":
    main()
