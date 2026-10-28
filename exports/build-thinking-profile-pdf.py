#!/usr/bin/env python3
"""Build the two Thinking Profile PDFs from thinking-profile/ladders-en.json.

Ladder deck (A4, 9 pages):
Page 1     cover: what it is, one cluster per unit, the self-check, the labels
Pages 2–7  one page per cluster: the four-step ladder with what each step shows
Page 8     the worked example (Biology, Grade 8, Causes and systems), short form
Page 9     the prompt card, word for word as the builder writes it

Self-check sheets (A4, 6 pages): one per cluster, for students (Grades 7–12).
The ladder on top, six task rows with a staircase to mark the step reached.

Cluster names and descriptions come from thinking-moves/moves-en.json, move
names and labels likewise; pair and flaw names are the tool names.

Writes the HTML sources to _unpublished/exports/ (so each PDF always has an
editable source) and the PDFs to assets/pdfs/free/.

Usage:
    /usr/bin/python3 exports/build-thinking-profile-pdf.py
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "thinking-profile/ladders-en.json"
MOVES = ROOT / "thinking-moves/moves-en.json"
PAIRS = ROOT / "side-by-side/pairs-en.json"
DECK_SRC = ROOT / "_unpublished/exports/thinking-profile-deck-a4-en.html"
SHEETS_SRC = ROOT / "_unpublished/exports/thinking-profile-sheets-a4-en.html"
DECK_DST = ROOT / "assets/pdfs/free/thinking-profile-deck-en.pdf"
SHEETS_DST = ROOT / "assets/pdfs/free/thinking-profile-sheets-en.pdf"
URL = "choosewise.education/thinking-profile"
TITLE = "Thinking Profile"
TOOL_NAMES = {"flawed-answer": "Flawed Answer", "side-by-side": "Side by Side"}

# Promptkortet, ordagrant som i assets/js/thinking-profile.js (buildPrompt);
# test_prompt_card_matches_builder_word_for_word håller dem i takt.
PRIVACY = "Do not include student names or student work in this conversation."
BUILDER_LINE = "Each task below is made in its own free builder on choosewise.education; the teacher types in the inputs you give, and the builder makes the task sheet students answer on paper."
FIELDS_LINE = "Builder fields. All three: Subject, Grade, What is the lesson about? (at most 400 characters), What do students already know? (optional). Thinking Moves also has Thinking move (the task name); grades 8 to 12. Flawed Answer also has Flaw type and How hard should the flaw be to spot? (Easier to spot or Harder to spot); grades 8 to 12. Side by Side also has Pair type and How hard should the difference be to see? (Easier to see or Harder to see); grades 7 to 12. If the unit grade is not offered, use the nearest. The builder writes the task itself, so put the case, numbers or text for students into What is the lesson about?"
PROMPT_PARTS = [
    "Reply in plain text, no tables, in this order:",
    "THE THINKING THREAD: one or two sentences on what kind of thinking this unit trains and why it fits the topic",
    "PLAN: four to six tasks spread across the weeks. For each task write",
    "WEEK:",
    "TASK: the task name and the tool",
    "WHAT STUDENTS DO: one sentence",
    "ROOM FOR STEP: the highest step this task gives room for",
    "BUILDER INPUTS: one Field: value line per field listed above; skip a field you leave empty",
    "LINK: the builder link",
    "TELL STUDENTS: three or four sentences the teacher reads at the start of the unit, introducing the ladder and saying it is never graded",
    'CHECK: facts or claims in the plan that could be wrong, one per line, at most four lines. Write "None" if there are none.',
]

# Utseendet följer Side by Sides kortlek och den delade tryckstilen
# exports/_guide-print.css, som laddar Hanken Grotesk 300–500.
# Inga hexfärger här: bara var(--…) från tryckstilen.
STYLE = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: var(--color-bg); }
body { font-family: var(--font-body); color: var(--color-text-soft); font-size: 10pt; line-height: 1.42; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
strong, b { font-weight: 500; }
.page { width: 210mm; height: 297mm; padding: 15mm 17mm 16mm; display: flex; flex-direction: column; gap: 4mm; page-break-after: always; overflow: hidden; }
.page:last-child { page-break-after: auto; }
h1, h2, h3, h4 { font-family: var(--font-display); font-weight: 500; color: var(--color-text); }
.kicker { font-size: 7.5pt; letter-spacing: .12em; text-transform: uppercase; color: var(--color-highlight-ink); font-weight: 500; }
.label { font-size: 8pt; letter-spacing: .08em; text-transform: uppercase; color: var(--color-accent); font-weight: 500; }
.chip { display: inline-block; border: 0.35mm solid var(--color-accent); color: var(--color-accent); border-radius: 1mm; padding: .3mm 2mm; font-weight: 500; font-size: 8pt; }
.chip--strong { background: var(--color-accent); color: var(--color-bg); }
.top { display: grid; grid-template-columns: 20mm 1fr; gap: 6mm; align-items: center; border-bottom: 0.6mm solid var(--color-accent); padding-bottom: 4mm; }
.top img { width: 20mm; height: 20mm; }
.top h2 { font-size: 24pt; line-height: 1.05; letter-spacing: -.01em; margin-top: 1mm; }
.oneliner { font-size: 12pt; color: var(--color-text); }
.foot { margin-top: auto; font-size: 7.5pt; color: var(--color-text-muted); border-top: 0.3mm solid var(--color-border); padding-top: 2.5mm; display: flex; justify-content: space-between; }
.cover h1 { font-size: 34pt; font-weight: 300; letter-spacing: -.02em; line-height: 1.05; }
.lede { font-size: 12pt; color: var(--color-text); max-width: 160mm; }
.clusters { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm 8mm; font-size: 9pt; }
.clusters div { border-top: 0.5mm solid var(--color-accent); padding-top: 2mm; }
.checks { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; font-size: 9.5pt; color: var(--color-text); }
.checks div { border-top: 0.5mm solid var(--color-highlight); padding-top: 2mm; }
.legend { display: flex; flex-direction: column; gap: 2mm; font-size: 9pt; }
.note { font-size: 9.5pt; color: var(--color-text); font-weight: 500; }
.evidence { font-size: 9pt; color: var(--color-text-muted); }
.steps { display: flex; flex-direction: column; gap: 3mm; }
.step { display: grid; grid-template-columns: 11mm 1fr; gap: 4mm; align-items: start; border-left: 1mm solid var(--color-highlight); background: var(--color-bg-alt); padding: 3.5mm 5mm; }
.step .n { font-family: var(--font-display); font-size: 22pt; font-weight: 300; color: var(--color-accent); line-height: 1; }
.step p { color: var(--color-text); font-size: 11pt; }
.step .shows { margin-top: 1.5mm; font-size: 9.2pt; color: var(--color-text-soft); }
.ex { border-left: 1mm solid var(--color-highlight); background: var(--color-bg-alt); padding: 4mm 5mm; display: flex; flex-direction: column; gap: 2.2mm; font-size: 9.6pt; }
.plan { display: grid; grid-template-columns: 14mm 30mm 1fr 17mm; gap: 1.6mm 3mm; font-size: 8.8pt; }
.plan .h { font-size: 7.5pt; letter-spacing: .08em; text-transform: uppercase; color: var(--color-accent); font-weight: 500; }
.plan .c { border-top: 0.3mm solid var(--color-border); padding-top: 1.4mm; }
.prompt { border: 0.35mm dashed var(--color-accent); border-radius: 1.5mm; padding: 4.5mm 5.5mm; font-family: 'SF Mono', Menlo, monospace; font-size: 7pt; line-height: 1.33; color: var(--color-text); white-space: pre-wrap; }
.names { display: flex; gap: 8mm; font-size: 10pt; color: var(--color-text); }
.names span { flex: 1; border-bottom: 0.3mm solid var(--color-border); padding-bottom: 1mm; }
.sheet h1 { font-size: 26pt; font-weight: 300; letter-spacing: -.02em; line-height: 1.05; }
.sheet { gap: 2.4mm; padding-top: 12mm; padding-bottom: 12mm; }
.mini { display: flex; flex-direction: column; gap: 1.4mm; font-size: 9pt; color: var(--color-text); }
.mini div { display: grid; grid-template-columns: 6mm 1fr; }
.mini b { color: var(--color-accent); }
.rule { border: 0.6mm solid var(--color-highlight); border-radius: 1.5mm; padding: 2mm 4mm; font-size: 9pt; color: var(--color-text); }
.rows { display: flex; flex-direction: column; gap: 2.2mm; flex: 1; min-height: 0; }
.row { border: 0.35mm solid var(--color-border); border-radius: 1mm; padding: 1.6mm 3.5mm 1.6mm; display: grid; grid-template-columns: 44mm 1fr 1fr; gap: 0 5mm; flex: 1; }
.row .task { grid-column: 1 / -1; font-size: 9pt; color: var(--color-text); border-bottom: 0.3mm solid var(--color-border); padding-bottom: .6mm; margin-bottom: 1mm; }
.row .q { font-size: 7.4pt; letter-spacing: .04em; color: var(--color-accent); font-weight: 500; line-height: 1.25; }
.row .ln { display: block; border-bottom: 0.3mm solid var(--color-border); height: 6.2mm; }
.stair { display: flex; align-items: flex-end; gap: 1.4mm; margin-top: 1mm; }
.stair span { flex: 1; border: 0.35mm solid var(--color-accent); border-radius: .8mm; text-align: center; font-size: 8pt; line-height: 1; padding-top: 1mm; color: var(--color-accent); font-weight: 500; }
.stair span:nth-child(1) { height: 4.5mm; }
.stair span:nth-child(2) { height: 7mm; }
.stair span:nth-child(3) { height: 9.5mm; }
.stair span:nth-child(4) { height: 12mm; }
"""


def _doc(title: str, pages: list) -> str:
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n"
        f"<title>{title}</title>\n"
        "<!-- Genererad av exports/build-thinking-profile-pdf.py från thinking-profile/ladders-en.json. "
        "Ändra i JSON-filen eller skriptet, inte här. -->\n"
        '<link rel="stylesheet" href="../../exports/_guide-print.css">\n'
        f"<style>{STYLE}</style>\n</head>\n<body>\n"
        + "\n".join(pages)
        + "\n</body>\n</html>\n"
    )


def _foot(right: str) -> str:
    return f'<div class="foot"><span>{TITLE} · {URL}</span><span>{right}</span></div>'


def _lookups():
    m = json.loads(MOVES.read_text(encoding="utf-8"))
    clusters = {c["id"]: c for c in m["clusters"]}
    moves = {x["id"]: x for x in m["moves"]}
    return m["labels"], clusters, moves


def _plan_task_name(w: dict, moves: dict) -> str:
    """Name of a plan week's task: a move name, or a pair name for Side by Side."""
    if w["tool"] == "side-by-side":
        pairs = json.loads(PAIRS.read_text(encoding="utf-8"))["pairs"]
        return next(p["name"] for p in pairs if p["id"] == w["task"])
    return moves[w["task"]]["name"]


def _task_name(task: dict, moves: dict) -> str:
    return moves[task["id"]]["name"] if task.get("id") else TOOL_NAMES[task["tool"]]


def _ladder_cover(data: dict) -> str:
    labels, clusters, _ = _lookups()
    cl = "".join(
        f'<div><strong>{escape(c["name"])}</strong><br>{escape(c["description"])}</div>'
        for c in clusters.values()
    )
    checks = "".join(
        f'<div><strong>{i}. </strong>{escape(q)}</div>' for i, q in enumerate(data["self_check"]["questions"], start=1)
    )
    legend = "".join(
        f'<p><span class="chip chip--{k}">{escape(labels[k]["name"])}</span> {escape(labels[k]["definition"])}</p>'
        for k in ("strong", "promising", "framework")
    )
    return (
        '<section class="page cover">'
        '<div class="kicker">Think + AI · Grades 7–12 · free ladder deck</div>'
        f"<h1>{TITLE}</h1>"
        f'<p class="lede">{escape(data["intro"]["what"])} '
        'Pick one kind of thinking for the unit, plan four to six tasks around it, and let students rate every answer on the same four-step ladder.</p>'
        f'<h3>One cluster per unit</h3><div class="clusters">{cl}</div>'
        f'<h3>After every task, students ask</h3><div class="checks">{checks}</div>'
        f'<p class="note">{escape(data["not_graded"])}</p>'
        f'<p class="evidence">{escape(data["honesty"])}</p>'
        f'<h3>What the labels mean</h3><div class="legend">{legend}</div>'
        f'{_foot("1 / 9")}</section>'
    )


def _ladder_page(lad: dict, data: dict, page_no: int) -> str:
    labels, clusters, moves = _lookups()
    c = clusters[lad["cluster"]]
    steps = "".join(
        f'<div class="step"><div class="n">{i}</div><div><p>{escape(s["text"])}</p>'
        f'<p class="shows"><strong>Shows it:</strong> {escape(s["shows"])}</p></div></div>'
        for i, s in enumerate(lad["steps"], start=1)
    )
    trained = []
    for t in lad["tasks"]:
        name = escape(_task_name(t, moves))
        if t.get("id"):
            k = moves[t["id"]]["label"]
            name += f' <span class="chip chip--{k}">{escape(labels[k]["name"])}</span>'
        trained.append(f"<li>{name}</li>")
    ev = {e["claim"]: e for e in data["evidence"]}
    return (
        '<section class="page">'
        f'<div class="top"><img src="../..{escape(lad["icon"])}" alt=""><div>'
        f'<div class="kicker">Cluster {page_no - 1}</div>'
        f'<h2>{escape(c["name"])}</h2></div></div>'
        f'<p class="oneliner">{escape(c["description"])}</p>'
        f'<div class="steps">{steps}</div>'
        f'<div><div class="label">In class</div><p>{escape(lad["in_class"])}</p></div>'
        f'<div><div class="label">Trained by</div><ul style="padding-left:5mm">{"".join(trained)}</ul></div>'
        '<div class="legend"><div class="label">Evidence</div>'
        f'<p><span class="chip chip--strong">{escape(labels["strong"]["name"])}</span> Teaching students to plan, monitor and evaluate their own learning (metacognition).</p>'
        f'<p><span class="chip chip--promising">{escape(labels["promising"]["name"])}</span> Self-assessment against concrete criteria.</p>'
        f'<p><span class="chip chip--framework">{escape(labels["framework"]["name"])}</span> These ladders, built on the logic of the SOLO taxonomy and not tested in research.</p></div>'
        f'<p class="note">{escape(data["not_graded"])}</p>'
        f'{_foot(f"{page_no} / 9")}</section>'
    )


def _example_page(data: dict) -> str:
    _, clusters, moves = _lookups()
    ex = data["example"]
    rows = "".join(
        f'<div class="c">Week {int(w["week"])}</div><div class="c">{escape(_plan_task_name(w, moves))}</div>'
        f'<div class="c">{escape(w["what"])}</div><div class="c">Step {int(w["step"])}</div>'
        for w in ex["plan"]
    )
    return (
        '<section class="page">'
        '<div class="kicker">Worked example</div>'
        f'<h2 style="font-size:24pt">{escape(ex["subject"])}, Grade {int(ex["grade"])}: {escape(ex["topic"])}</h2>'
        f'<p class="oneliner">{int(ex["weeks"])} weeks · following {escape(clusters[ex["cluster"]]["name"])}</p>'
        f'<div class="ex"><span class="label">The thinking thread</span><p>{escape(ex["thread"])}</p></div>'
        f'<div class="plan"><div class="h">Week</div><div class="h">Task</div><div class="h">What students do</div>'
        f'<div class="h">Room for</div>{rows}</div>'
        f'<div class="ex"><span class="label">Tell students</span><p>{escape(ex["tell_students"])}</p></div>'
        f'{_foot("8 / 9")}</section>'
    )


def _prompt_card(data: dict) -> str:
    _, clusters, _ = _lookups()
    rules = " ".join(data["rules"])
    prompt = "\n".join([
        PRIVACY,
        "",
        "You are helping a Grade {grade} {subject} teacher plan a {weeks}-week unit so that students practise one kind of thinking "
        "all the way through it, instead of handing their thinking to AI. Students do the tasks on paper, without AI. "
        "After each task they mark which step of a four-step ladder their answer reached. "
        "The ladder is for students' own self-check. It is never graded.",
        "",
        "Unit topic: {topic}",
        "Unit outline: {overview}   (optional)",
        "",
        "Thinking to follow: {cluster name}. {cluster description}",
        "The ladder:",
        "1. {step 1}",
        "2. {step 2}",
        "3. {step 3}",
        "4. {step 4}",
        "",
        BUILDER_LINE,
        FIELDS_LINE,
        "Preferred tasks, because they train {cluster name}:",
        "- {task name} ({tool}): {one-line description} {link}",
        "Other tasks you may borrow:",
        "- {task name} ({tool}): {one-line description} {link}",
        "",
        "Rules: " + rules + " Do not invent studies or sources.",
        "",
        *PROMPT_PARTS,
    ])
    return (
        '<section class="page">'
        '<div class="kicker">Without the website</div>'
        '<h2 style="font-size:24pt">Your own unit plan</h2>'
        '<p class="oneliner">Replace everything in {braces}, then type the prompt into any AI tool: Copilot, Gemini, ChatGPT or Claude. '
        'Check the plan before the unit, especially anything under CHECK.</p>'
        f'<div class="prompt">{escape(prompt)}</div>'
        '<p class="evidence"><strong>Regulating your own thinking.</strong> For this cluster use these rules instead of the Rules line above: '
        f'{escape(" ".join(data["rules_regulating"]))}</p>'
        f'<p class="evidence">Faster online: the planner at {URL} fills this in for you and picks the preferred tasks. '
        'Students need no AI for the tasks. If older students use AI themselves, check the tool\'s age rules, '
        'your national rules and your school policy first.</p>'
        f'{_foot("9 / 9")}</section>'
    )


def render_deck_html(data: dict) -> str:
    """The complete HTML source of the deck. Same JSON in, same text out."""
    pages = [_ladder_cover(data)]
    pages += [_ladder_page(lad, data, i) for i, lad in enumerate(data["ladders"], start=2)]
    pages.append(_example_page(data))
    pages.append(_prompt_card(data))
    return _doc(f"{TITLE} — ladder deck", pages)


def _sheet(lad: dict, data: dict, page_no: int) -> str:
    _, clusters, _ = _lookups()
    c = clusters[lad["cluster"]]
    q1, q2, q3 = (escape(q) for q in data["self_check"]["questions"])
    ladder = "".join(f'<div><b>{i}</b><span>{escape(s["text"])}</span></div>' for i, s in enumerate(lad["steps"], start=1))
    rule = f'<p class="rule">{escape(data["regulating_rule"])}</p>' if lad["cluster"] == "regulating" else ""
    stair = "".join(f"<span>{i}</span>" for i in range(1, 5))
    row = (
        '<div class="row"><div class="task">Task: <span style="display:inline-block;width:80mm;border-bottom:0.3mm solid var(--color-border)"></span>'
        ' Date: <span style="display:inline-block;width:24mm;border-bottom:0.3mm solid var(--color-border)"></span></div>'
        f'<div><div class="q">{q1}</div><div class="stair">{stair}</div></div>'
        f'<div><div class="q">{q2}</div><span class="ln"></span><span class="ln"></span></div>'
        f'<div><div class="q">{q3}</div><span class="ln"></span><span class="ln"></span></div></div>'
    )
    return (
        '<section class="page sheet">'
        f'<div class="kicker">Self-check sheet · {escape(TITLE)}</div>'
        f'<h1>{escape(c["name"])}</h1>'
        '<div class="names"><span>Name:</span><span>Unit:</span></div>'
        f'<div class="mini">{ladder}</div>'
        f"{rule}"
        f'<p class="evidence">{escape(data["not_graded"])} Circle the step your answer reached.</p>'
        f'<div class="rows">{row * 6}</div>'
        f'{_foot(f"{page_no} / 6")}</section>'
    )


def render_sheets_html(data: dict) -> str:
    pages = [_sheet(lad, data, i) for i, lad in enumerate(data["ladders"], start=1)]
    return _doc(f"{TITLE} — self-check sheets", pages)


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
    DECK_SRC.parent.mkdir(parents=True, exist_ok=True)
    DECK_SRC.write_text(render_deck_html(data), encoding="utf-8")
    SHEETS_SRC.write_text(render_sheets_html(data), encoding="utf-8")
    DECK_DST.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        _pdf(page, DECK_SRC, DECK_DST)
        _pdf(page, SHEETS_SRC, SHEETS_DST)
        browser.close()


if __name__ == "__main__":
    main()
