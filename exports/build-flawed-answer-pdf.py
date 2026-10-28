#!/usr/bin/env python3
"""Build the two Flawed Answer PDFs from flawed-answer/flaws-en.json.

Student frame (A4, 1 page): the frame line, a box for the AI-generated
answer, the four step boxes and a Think back line.

Card deck (A4, 8 pages):
Page 1     cover: how to run it, the four steps, the two levels, the labels
Pages 2–7  one card per flaw type, with the full worked example and key
Page 8     a fill-in prompt for use without the website

Writes the HTML sources to _unpublished/exports/ (so each PDF always has an
editable source) and the PDFs to assets/pdfs/free/.

Usage:
    /usr/bin/python3 exports/build-flawed-answer-pdf.py
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "flawed-answer/flaws-en.json"
FRAME_SRC = ROOT / "_unpublished/exports/flawed-answer-frame-a4-en.html"
DECK_SRC = ROOT / "_unpublished/exports/flawed-answer-cards-a4-en.html"
FRAME_DST = ROOT / "assets/pdfs/free/flawed-answer-frame-en.pdf"
DECK_DST = ROOT / "assets/pdfs/free/flawed-answer-cards-en.pdf"
URL = "choosewise.education/flawed-answer"
TITLE = "Flawed Answer"
FRAME_LINE = "This answer was written by AI. Find where its reasoning goes wrong."
EASIER_ONLY = "Easier to spot only: AI tools could not plant this flaw reliably at the harder level."

# Regelraden och de nio delarna, ordagrant som i assets/js/flawed-answer.js;
# test_fill_in_matches_builder_word_for_word håller dem i takt.
RULES = "Rules: the answer contains exactly one error. It is an error of reasoning of the type above, not a factual slip or a typo. The flawed sentence makes one claim only. Every other sentence is correct in general, not just in typical cases, and no other sentence states or hints at the correct reasoning. Use \"always\", \"never\" or \"all\" only if the flaw type is Overgeneralisation. Do not invent studies, measurements or sources. Write in a confident, fluent style, as an AI assistant would."
PROMPT_PARTS = [
    "QUESTION: the question the answer responds to, in one sentence, without hinting at the flaw",
    'ANSWER: start with the line "AI-generated answer", then the answer',
    "THE FLAW: quote the flawed sentence exactly, then say what is wrong in at most two sentences",
    "FIX: the corrected sentence or step",
    "WHY IT CONVINCES: the true-sounding idea or common misconception that makes the flaw believable",
    "TEST IT: one way students could check this in class or at home",
    "PROBE: one follow-up question that pushes past the first answer",
    "THINK BACK: one sentence starter about how they thought, not what they found",
    'CHECK: every fact, figure, date, general rule or source in ANSWER or THE FLAW that the teacher should verify, quoted or closely paraphrased as it appears there, one per line, starting with the claims you are least sure of. Do not add claims from FIX or TEST IT. Write "None" only if ANSWER contains no checkable claim.',
]

KEY_PARTS = [("flaw", "The flaw"), ("fix", "Fix"), ("why_convincing", "Why it convinces"),
             ("test_it", "Test it"), ("probe", "Probe"), ("think_back", "Think back")]

# Utseendet följer Thinking Moves kortlek (alternativ B) och den delade
# tryckstilen exports/_guide-print.css, som laddar Hanken Grotesk 300–500.
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
.top h2 { font-size: 26pt; line-height: 1.05; letter-spacing: -.01em; margin-top: 1mm; }
.oneliner { font-size: 12.5pt; color: var(--color-text); }
.signs { display: flex; flex-direction: column; gap: 1mm; padding-left: 5mm; font-size: 10pt; }
.label { font-size: 8pt; letter-spacing: .08em; text-transform: uppercase; color: var(--color-accent); font-weight: 500; }
.only { font-size: 9.5pt; color: var(--color-highlight-ink); }
.chip { display: inline-block; border: 0.35mm solid var(--color-accent); color: var(--color-accent); border-radius: 1mm; padding: .3mm 2mm; font-weight: 500; font-size: 8pt; }
.chip--strong { background: var(--color-accent); color: var(--color-bg); }
.chip--thin { border-color: var(--color-border); border-style: dashed; color: var(--color-text-muted); }
.ex { border-left: 1mm solid var(--color-highlight); background: var(--color-bg-alt); padding: 4.5mm 6mm; display: flex; flex-direction: column; gap: 2.5mm; font-size: 10.2pt; }
.ex h3 { font-size: 11.5pt; }
.ex h3 span { font-weight: 400; color: var(--color-text-muted); }
.answer { border: 0.3mm dashed var(--color-border); background: var(--color-bg); border-radius: 1mm; padding: 3mm 4mm; color: var(--color-text); }
.answer .label { color: var(--color-text-muted); display: block; margin-bottom: 1mm; }
.ex dl { display: grid; grid-template-columns: 30mm 1fr; gap: 1.2mm 4mm; }
.ex dt { font-size: 8pt; letter-spacing: .08em; text-transform: uppercase; color: var(--color-accent); font-weight: 500; padding-top: .5mm; }
.for-ai { font-size: 9.3pt; color: var(--color-text); }
.evidence { font-size: 9pt; color: var(--color-text-muted); }
.foot { margin-top: auto; font-size: 7.5pt; color: var(--color-text-muted); border-top: 0.3mm solid var(--color-border); padding-top: 2.5mm; display: flex; justify-content: space-between; }
.cover h1, .frame h1 { font-size: 34pt; font-weight: 300; letter-spacing: -.02em; line-height: 1.05; }
.lede { font-size: 12pt; color: var(--color-text); max-width: 160mm; }
.how { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4mm; font-size: 9pt; }
.how div { border-top: 0.5mm solid var(--color-highlight); padding-top: 2mm; }
.levels { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm 8mm; font-size: 9pt; }
.levels div { border-top: 0.5mm solid var(--color-accent); padding-top: 2mm; }
.legend { display: flex; flex-direction: column; gap: 2mm; font-size: 9pt; }
.note { font-size: 9.5pt; color: var(--color-text); font-weight: 500; }
.prompt { border: 0.35mm dashed var(--color-accent); border-radius: 1.5mm; padding: 5mm 6mm; font-family: 'SF Mono', Menlo, monospace; font-size: 8.2pt; line-height: 1.6; color: var(--color-text); white-space: pre-wrap; }
.blank { display: inline-block; border-bottom: 0.3mm solid var(--color-text); }
.frame .line { font-size: 13pt; color: var(--color-text); font-weight: 500; }
.paste { flex: 0 0 62mm; border: 0.35mm dashed var(--color-border); border-radius: 1.5mm; display: flex; align-items: center; justify-content: center; color: var(--color-text-muted); font-size: 10pt; }
.boxes { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; flex: 1; }
.box { border: 0.35mm solid var(--color-border); border-top: 0.8mm solid var(--color-accent); border-radius: 1mm; padding: 3mm 4mm; display: flex; flex-direction: column; gap: 1mm; }
.box h3 { font-size: 12pt; }
.box p { font-size: 9pt; color: var(--color-text-muted); }
.think { border-top: 0.6mm solid var(--color-highlight); padding-top: 2.5mm; font-size: 10pt; color: var(--color-text); }
.think .rule { display: block; border-bottom: 0.3mm solid var(--color-border); height: 9mm; }
.names { display: flex; gap: 8mm; font-size: 10pt; color: var(--color-text); }
.names span { flex: 1; border-bottom: 0.3mm solid var(--color-border); padding-bottom: 1mm; }
"""


def _doc(title: str, pages: list) -> str:
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n"
        f"<title>{title}</title>\n"
        "<!-- Generated by exports/build-flawed-answer-pdf.py from flawed-answer/flaws-en.json. "
        "Edit the JSON or the script, not this file. -->\n"
        '<link rel="stylesheet" href="../../exports/_guide-print.css">\n'
        f"<style>{STYLE}</style>\n</head>\n<body>\n"
        + "\n".join(pages)
        + "\n</body>\n</html>\n"
    )


def _foot(right: str) -> str:
    return f'<div class="foot"><span>{TITLE} · {URL}</span><span>{right}</span></div>'


def render_frame_html(data: dict) -> str:
    """The one-page student frame. Neutral wording, so it also works for the
    upper-secondary variant, where the answer may have no planted error."""
    boxes = "".join(
        f'<div class="box"><h3>{i}. {escape(s["name"])}</h3><p>{escape(s["prompt"])}</p></div>'
        for i, s in enumerate(data["steps"], start=1)
    )
    page = (
        '<section class="page frame">'
        '<div class="kicker">Think + AI · student frame</div>'
        f"<h1>{TITLE}</h1>"
        f'<p class="line">{FRAME_LINE}</p>'
        '<div class="names"><span>Names:</span><span>Date:</span></div>'
        '<div class="paste">Staple or paste the AI-generated answer here</div>'
        f'<div class="boxes">{boxes}</div>'
        '<div class="think"><strong>Think back.</strong> One sentence about how you thought, not what you found.'
        '<span class="rule"></span></div>'
        f'{_foot("If you find no error, mark the weakest step and say what would make it stronger.")}</section>'
    )
    return _doc(f"{TITLE} — student frame", [page])


def _cover(data: dict) -> str:
    steps = "".join(f'<div><strong>{escape(s["name"])}</strong><br>{escape(s["prompt"])}</div>' for s in data["steps"])
    levels = "".join(f'<div><strong>{escape(lv["name"])}</strong><br>{escape(lv["instruction"])}</div>'
                     for lv in data["levels"])
    labels = data["labels"]
    legend = "".join(
        f'<p><span class="chip chip--{k}">{escape(labels[k]["name"])}</span> {escape(labels[k]["definition"])}</p>'
        for k in ("strong", "thin")
    )
    evidence = "".join(
        f'<p><span class="chip chip--{escape(e["label"])}">{escape(labels[e["label"]]["name"])}</span> '
        f'<strong>{escape(e["claim"])}.</strong> {escape(e["text"])}</p>'
        for e in data["evidence"]
    )
    return (
        '<section class="page cover">'
        '<div class="kicker">Think + AI · Grades 8–12 · free card deck</div>'
        f"<h1>{TITLE}</h1>"
        '<p class="lede">Use any AI tool to write a fluent, confident answer about your lesson topic with exactly one '
        'error of reasoning. Tell students an AI wrote it. In pairs, they work through four steps in about fifteen minutes.</p>'
        f'<h3>Four steps, then Think back</h3><div class="how">{steps}</div>'
        f'<h3>Two levels</h3><div class="levels">{levels}</div>'
        '<p class="evidence">Before you print, read the key and check everything listed under CHECK. '
        'If the flaw is not where the key says, or there is a second error, generate a new answer.</p>'
        f'<h3>How strong is the evidence?</h3><div class="legend">{legend}{evidence}</div>'
        f'<p class="note">{escape(labels["note"])}</p>'
        f'{_foot("1 / 8")}</section>'
    )


def _card(flaw: dict, data: dict, page_no: int) -> str:
    ex = flaw["example"]
    level = {lv["id"]: lv["name"] for lv in data["levels"]}[ex["level"]]
    signs = "".join(f"<li>{escape(s)}</li>" for s in flaw["telltale_signs"])
    key = "".join(f"<dt>{label}</dt><dd>{escape(ex[k])}</dd>" for k, label in KEY_PARTS)
    only = f'<p class="only">{EASIER_ONLY}</p>' if not flaw["harder_ok"] else ""
    return (
        '<section class="page">'
        f'<div class="top"><img src="../../flawed-answer/icons/{escape(flaw["id"])}.svg" alt=""><div>'
        f'<div class="kicker">Flaw {int(flaw["number"])}</div>'
        f'<h2>{escape(flaw["name"])}</h2></div></div>'
        f'<p class="oneliner">{escape(flaw["one_liner"])}</p>'
        f'<div><div class="label">Telltale signs</div><ul class="signs">{signs}</ul></div>'
        f"{only}"
        f'<div class="ex"><h3>{escape(ex["subject"])} <span>· Grade {int(ex["grade"])} · {escape(level)}</span></h3>'
        f'<p><strong>Question:</strong> {escape(ex["question"])}</p>'
        f'<div class="answer"><span class="label">AI-generated answer</span>{escape(ex["answer"])}</div>'
        f"<dl>{key}</dl></div>"
        f'<p class="for-ai"><strong>For the AI.</strong> {escape(flaw["prompt_brief"])}</p>'
        f'<p class="evidence"><strong>Evidence.</strong> Explicit teaching of critical thinking: Strong. '
        f'Students critiquing AI answers: Thin. Labels rate research on teaching this kind of thinking regularly, not a single use.</p>'
        f'{_foot(f"{page_no} / 8")}</section>'
    )


def _fill_in() -> str:
    def blank(mm: int) -> str:
        return f'<span class="blank" style="width:{mm}mm"></span>'

    prompt = "\n".join([
        "Do not include student names or student work in this conversation.",
        "",
        f"You are helping a Grade {blank(12)} {blank(40)} teacher prepare a fifteen-minute \"Flawed Answer\" task. "
        "Students will be told that an AI wrote the answer, and their job is to find the error in its reasoning.",
        "",
        f"Lesson topic: {blank(110)}",
        f"Students already know (optional): {blank(70)}",
        "",
        f"Flaw type: {blank(60)} (copy the name and one-line description from its card)",
        f"How to plant it: {blank(40)} (copy the \"For the AI\" text from its card)",
        f"Difficulty: {blank(60)} (copy one level from the cover)",
        "",
        escape(RULES),
        "",
        "Reply in plain text, no tables, with exactly these nine parts:",
        *[escape(p) for p in PROMPT_PARTS],
    ])
    return (
        '<section class="page">'
        '<div class="kicker">Without the website</div>'
        '<h2 style="font-size:24pt">Your own flawed answer</h2>'
        '<p class="oneliner">Fill in the blanks, then type the prompt into any AI tool: Copilot, Gemini, ChatGPT or Claude. '
        'Check the answer and the key before the lesson, especially anything under CHECK.</p>'
        f'<div class="prompt">{prompt}</div>'
        '<p class="evidence">Faster online: the prompt builder at ' + URL + ' fills this in for you. '
        'Students need no AI for the main task. If older students use AI themselves, check the tool\'s age rules, '
        'your national rules and your school policy first.</p>'
        f'{_foot("8 / 8")}</section>'
    )


def render_deck_html(data: dict) -> str:
    """The complete HTML source of the deck. Same JSON in, same text out."""
    pages = [_cover(data)]
    pages += [_card(f, data, i) for i, f in enumerate(data["flaws"], start=2)]
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
    FRAME_SRC.parent.mkdir(parents=True, exist_ok=True)
    FRAME_SRC.write_text(render_frame_html(data), encoding="utf-8")
    DECK_SRC.write_text(render_deck_html(data), encoding="utf-8")
    FRAME_DST.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        _pdf(page, FRAME_SRC, FRAME_DST)
        _pdf(page, DECK_SRC, DECK_DST)
        browser.close()


if __name__ == "__main__":
    main()
