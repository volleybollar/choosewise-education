#!/usr/bin/env python3
"""Bygger lärarkitet The Study Experiment (A4, 7 sidor) från study-experiment/experiment-en.json.

Sida 1  överblick: de två lektionerna i korthet, vad man kan vänta sig,
        material och förberedelser
Sida 2  Lesson 1-manus med minuter per steg
Sida 3  grupplappar: fyra lappar (Group 1, Group 2, Group 1, Group 2) att klippa ut
Sida 4  åtta gissningslappar att klippa ut
Sida 5  åtta poänglappar att klippa ut
Sida 6  Lesson 2-manus, diskussionsfrågorna, de tre förklaringarna, rutan för
        ett jämnt resultat och "ingen dator"
Sida 7  luckprompt för läraren, ordagrant lika med teacherLines i
        assets/js/study-experiment.js, med luckor för årskurs (två ställen),
        ämne, område och språk

Skriver HTML-källan till _unpublished/exports/study-experiment-kit-a4-en.html
(så att PDF:en alltid har en redigerbar källa) och PDF:en till
assets/pdfs/free/study-experiment-kit-en.pdf.

Användning:
    /usr/bin/python3 exports/build-study-experiment-pdf.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "study-experiment/experiment-en.json"
SRC = ROOT / "_unpublished/exports/study-experiment-kit-a4-en.html"
DST = ROOT / "assets/pdfs/free/study-experiment-kit-en.pdf"
URL = "choosewise.education/study-experiment"
TITLE = "The Study Experiment"
PAGES = 7

# Kitets utseende: samma tryckstil som kortleken Study Moves, och den delade
# exports/_guide-print.css, som laddar Hanken Grotesk 300–500. Färgerna kommer
# bara från tokens i den filen. Längst ner står det som är nytt för kitet:
# manusraderna, klipplapparna och rutorna.
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
.part { font-size: 8pt; letter-spacing: .08em; text-transform: uppercase; color: var(--color-accent); font-weight: 500; margin-bottom: 1mm; }
.evidence { font-size: 9pt; color: var(--color-text-muted); }
.foot { margin-top: auto; font-size: 7.5pt; color: var(--color-text-muted); border-top: 0.3mm solid var(--color-border); padding-top: 2.5mm; display: flex; justify-content: space-between; }
.cover h1 { font-size: 34pt; font-weight: 300; letter-spacing: -.02em; line-height: 1.05; }
.cover .lede { font-size: 12pt; color: var(--color-text); max-width: 160mm; }
.prompt { border: 0.35mm dashed var(--color-accent); border-radius: 1.5mm; padding: 6mm 7mm; font-size: 9.6pt; line-height: 1.6; color: var(--color-text); white-space: pre-wrap; }
.blank { display: inline-block; border-bottom: 0.3mm solid var(--color-text); }

/* ---- Nytt för kitet ---- */
/* Överblicken: de två lektionerna bredvid varandra, sedan material och förberedelser. */
.glance { display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; }
.glance > div { border-left: 1mm solid var(--color-highlight); background: var(--color-bg-alt); padding: 3.5mm 5mm; display: flex; flex-direction: column; gap: 1.5mm; }
.glance h3 { font-size: 12pt; }
.expect { color: var(--color-text); font-size: 10.2pt; }
.cols { display: grid; grid-template-columns: 62mm 1fr; gap: 8mm; }
.list { padding-left: 4.5mm; display: flex; flex-direction: column; gap: 1.6mm; font-size: 10.2pt; }
.note { border: 0.35mm solid var(--color-highlight); border-radius: 1.5mm; padding: 3mm 4mm; color: var(--color-text); font-size: 10pt; }

/* Manusraderna: nummer, minuter och text i tre kolumner. Ett steg utan tid får en tom ruta. */
.intro { font-size: 12pt; color: var(--color-text); }
.hint { font-size: 10pt; color: var(--color-text-soft); }
.script { list-style: none; display: flex; flex-direction: column; }
.script li { display: grid; grid-template-columns: 6mm 15mm 1fr; gap: 2mm; padding: 3.6mm 0; border-top: 0.3mm solid var(--color-border); font-size: 12pt; color: var(--color-text); }
.script li:last-child { border-bottom: 0.3mm solid var(--color-border); }
.script .n { font-weight: 500; color: var(--color-accent); }
.script .min { font-weight: 500; color: var(--color-highlight-ink); font-size: 9.5pt; padding-top: .8mm; }

/* Klipplapparna: ett rutnät med streckade linjer mellan och runt lapparna. Linjerna
   ritas av lapparnas högra och nedre kant plus rutnätets övre och vänstra, så att varje
   linje bara är en linje. */
.sheet { flex: 1; display: grid; grid-template-columns: 1fr 1fr; border-top: 0.35mm dashed var(--color-text-muted); border-left: 0.35mm dashed var(--color-text-muted); }
.sheet--cards { grid-template-rows: 1fr 1fr; }
.sheet--slips { grid-template-rows: repeat(4, 1fr); }
.slip { border-right: 0.35mm dashed var(--color-text-muted); border-bottom: 0.35mm dashed var(--color-text-muted); padding: 6mm 7mm; display: flex; flex-direction: column; gap: 3.5mm; justify-content: center; }
.card { border-right: 0.35mm dashed var(--color-text-muted); border-bottom: 0.35mm dashed var(--color-text-muted); padding: 6mm 8mm; display: flex; flex-direction: column; gap: 3mm; }
.card h3 { font-size: 22pt; font-weight: 300; line-height: 1.1; }
.card .steps { padding-left: 5mm; display: flex; flex-direction: column; gap: 2.2mm; font-size: 11.2pt; color: var(--color-text); }
.q { font-size: 11.5pt; color: var(--color-text); }
.opts { list-style: none; display: flex; flex-direction: column; gap: 2.4mm; color: var(--color-text); }
.opts li, .check { display: flex; align-items: center; gap: 3mm; }
.line { font-size: 12.5pt; color: var(--color-text); }
.check { font-size: 9.5pt; color: var(--color-text-soft); border-top: 0.3mm solid var(--color-border); padding-top: 3mm; }
/* Rutan ritas med CSS och inte med ett Unicode-tecken för kryssruta, så att inget reservtypsnitt kommer med i PDF:en. */
.tick { display: inline-block; flex: none; width: 4.4mm; height: 4.4mm; border: 0.4mm solid var(--color-text); border-radius: 0.7mm; }

/* Sida 6 rymmer mycket: lite mindre text och tätare rader, men aldrig under 9,5 pt. */
.dense { font-size: 9.6pt; line-height: 1.38; padding-top: 12mm; gap: 2.6mm; }
.dense .top { padding-bottom: 2.5mm; }
.dense .top h2 { font-size: 22pt; }
.dense .intro { font-size: 9.8pt; }
.dense .script .n { font-size: 9.6pt; }
.dense .script .min { padding-top: 0; }
.dense .script li { font-size: 9.6pt; padding: 0.9mm 0; }
.dense .script .min { font-size: 9.5pt; }
.dense .qs, .dense .points { padding-left: 4.5mm; display: flex; flex-direction: column; gap: .6mm; color: var(--color-text); }
.dense .points { list-style: none; padding-left: 0; gap: 1.4mm; }
.box { border-left: 1mm solid var(--color-highlight); background: var(--color-bg-alt); padding: 2.8mm 5mm; display: flex; flex-direction: column; gap: 1mm; }
.box h3 { font-size: 10.6pt; }
.dense .note { font-size: 9.6pt; padding: 2mm 4mm; }
"""


def _foot(page_no: int) -> str:
    return f'<div class="foot"><span>{TITLE} · {URL}</span><span>{page_no} / {PAGES}</span></div>'


def _top(kicker: str, title: str) -> str:
    return f'<div class="top"><div class="kicker">{escape(kicker)}</div><h2>{escape(title)}</h2></div>'


def _card_step(step: str) -> str:
    """Tiden i slutet ("(4 minutes)") hålls ihop med ett hårt mellanslag, så att den inte bryts mitt i."""
    return re.sub(r"\((\d+) (minutes?)\)", "(\\1\u00a0\\2)", escape(step))


def _blank(mm: int) -> str:
    return f'<span class="blank" style="width:{mm}mm"></span>'


def _text(s: str) -> str:
    """Fast text i prompten: ' och " lämnas som de är, så att raden står ordagrant."""
    return escape(s, quote=False)


def _overview(data: dict) -> str:
    # De två lektionerna i korthet hämtas ur lesson1.intro och lesson2.intro i JSON,
    # så att sidan, kitet och manusen säger samma sak.
    glance = "".join(
        f'<div><h3>Lesson {n}</h3><p>{escape(data[f"lesson{n}"]["intro"])}</p></div>' for n in (1, 2)
    )
    materials = "".join(f"<li>{escape(m)}</li>" for m in data["materials"])
    before = "".join(f"<li>{escape(b)}</li>" for b in data["before"])
    return (
        '<section class="page cover">'
        '<div class="kicker">Free classroom kit · Grades 7–12</div>'
        f"<h1>{TITLE}</h1>"
        '<p class="lede">Your class studies two short texts, one by reading it twice and one by '
        "testing themselves. A week later, a surprise quiz shows which worked better. Students see "
        "the answer in their own scores, not in a poster about research.</p>"
        f'<div class="glance">{glance}</div>'
        f'<div><h3 class="part">What to expect</h3><p class="expect">{escape(data["expect"])}</p></div>'
        '<div class="cols">'
        f'<div><h3 class="part">Materials</h3><ul class="list">{materials}</ul></div>'
        f'<div><h3 class="part">Before you start</h3><ol class="list">{before}</ol></div>'
        "</div>"
        # Texten i JSON säger "on this page" om webbsidan, där promptbyggaren och
        # resultatvyn finns. I den utskrivna PDF:en behöver det sägas.
        f'<p class="note">The prompt builder and the results view are on the web page {URL}. '
        'Wherever this kit says "this page", it means that page.</p>'
        f"{_foot(1)}</section>"
    )


def _steps(steps: list[dict]) -> str:
    rows = []
    for i, step in enumerate(steps, start=1):
        minutes = f'{int(step["minutes"])} min' if step["minutes"] else ""
        rows.append(
            f'<li><span class="n">{i}</span><span class="min">{minutes}</span>'
            f'<span>{escape(step["text"])}</span></li>'
        )
    return f'<ol class="script">{"".join(rows)}</ol>'


def _lesson1(data: dict) -> str:
    lesson = data["lesson1"]
    return (
        '<section class="page">'
        + _top("Teacher script", "Lesson 1")
        + f'<p class="intro">{escape(lesson["intro"])}</p>'
        + _steps(lesson["steps"])
        + _foot(2)
        + "</section>"
    )


def _group_cards(data: dict) -> str:
    # Två grupper, var och en två gånger: en sida räcker till fyra elever.
    def card(c: dict) -> str:
        steps = "".join(f"<li>{_card_step(s)}</li>" for s in c["steps"])
        return (
            '<div class="card"><div class="kicker">Lesson 1</div>'
            f'<h3>{escape(c["title"])}</h3><ol class="steps">{steps}</ol></div>'
        )

    first, second = data["group_cards"]
    return (
        '<section class="page">'
        + _top("Lesson 1 · cut along the dashed lines", "Group cards")
        + '<p class="intro">Print one page for every four students.</p>'
        + f'<div class="sheet sheet--cards">{card(first)}{card(second)}{card(first)}{card(second)}</div>'
        + _foot(3)
        + "</section>"
    )


def _prediction_slips(data: dict) -> str:
    slip = data["prediction_slip"]
    options = "".join(f'<li><span class="tick"></span>{escape(o)}</li>' for o in slip["options"])
    one = f'<div class="slip"><p class="q">{escape(slip["question"])}</p><ul class="opts">{options}</ul></div>'
    return (
        '<section class="page">'
        + _top("Lesson 1 · cut along the dashed lines", "Prediction slips")
        + '<p class="hint">Hand out at the end of Lesson 1, once the texts are collected and before anyone '
        "talks about the two ways. Students tick one box and hand the slip in. The slips are anonymous. "
        "Print one slip per student.</p>"
        + f'<div class="sheet sheet--slips">{one * 8}</div>'
        + _foot(4)
        + "</section>"
    )


def _score_slips(data: dict) -> str:
    slip = data["score_slip"]
    lines = []
    for line in slip["lines"]:
        # "____" i JSON blir en linje att skriva siffran på.
        before, _, after = line.partition("____")
        lines.append(f'<p class="line">{escape(before)}{_blank(15)}{escape(after)}</p>')
    one = (
        '<div class="slip">'
        + "".join(lines)
        + f'<p class="check"><span class="tick"></span>{escape(slip["check"])}</p></div>'
    )
    return (
        '<section class="page">'
        + _top("Lesson 2 · cut along the dashed lines", "Score slips")
        + '<p class="hint">Hand out once students have marked their own quiz and you have told each half which '
        "text they read twice. Students fill in both scores, fold the slip and hand it in. Leave a slip out of the "
        "results view if its box is ticked. Print one slip per student.</p>"
        + f'<div class="sheet sheet--slips">{one * 8}</div>'
        + _foot(5)
        + "</section>"
    )


def _lesson2(data: dict) -> str:
    lesson = data["lesson2"]
    questions = "".join(f"<li>{escape(q)}</li>" for q in data["discussion"])
    points = []
    for p in data["explain"]["points"]:
        # Varje punkt öppnar med en rubrikmening ("Why ..."): den sätts i halvfet stil.
        lead, dot, rest = p.partition(". ")
        points.append(f"<li><strong>{escape(lead + dot.strip())}</strong> {escape(rest)}</li>" if dot else f"<li>{escape(p)}</li>")
    even = data["even_result"]
    return (
        '<section class="page dense">'
        + _top("Teacher script", "Lesson 2")
        + f'<p class="intro">{escape(lesson["intro"])}</p>'
        + _steps(lesson["steps"])
        + f'<div><h3 class="part">Discussion questions</h3><ol class="qs">{questions}</ol></div>'
        + f'<div><h3 class="part">{escape(data["explain"]["title"])}</h3><ol class="points">{"".join(points)}</ol></div>'
        + f'<div class="box"><h3>{escape(even["title"])}</h3><p>{escape(even["text"])}</p></div>'
        + f'<p class="note">{escape(data["no_computer"])}</p>'
        + _foot(6)
        + "</section>"
    )


def _fill_in() -> str:
    # Raderna är ordagrant desamma som i teacherLines i assets/js/study-experiment.js,
    # utom att lärarens uppgifter är luckor: årskurs (två ställen), ämne, område och
    # språk. test_fill_in_matches_js håller dem i takt.
    prompt = "\n".join([
        _text("Do not include student names or student work in this conversation."),
        "",
        _text("You are helping a Grade ") + _blank(12) + " " + _blank(40)
        + _text(" teacher run a classroom experiment on two study methods. Students will study two short "
                "texts: one by reading it twice, the other by reading it once, writing down everything they "
                "remember and then checking it against the text. A week later they take a surprise quiz on "
                "both texts."),
        "",
        _text("Topic area: ") + _blank(110),
        _text("Write everything in ") + _blank(40) + ".",
        "",
        _text("Write two texts, TEXT A and TEXT B, each on a different part of this topic area that students "
              "have not been taught yet."),
        _text("- Make each text about 250 words, and keep the two texts within 20 words of each other in length."),
        _text("- Make them equally hard: ten key facts each, similar sentence length and similar words, at a "
              "reading level for Grade ") + _blank(12) + ".",
        _text("- Spread the key facts evenly through each text. No headings or lists inside the texts."),
        _text("- Use only facts that are well established and easy to check."),
        "",
        _text("Then write a quiz: Q1 to Q6 on Text A and Q7 to Q12 on Text B."),
        _text("- Each question tests a different key point of the text, the kind of thing a student would write "
              "down when recalling it. The answer is a word, a number or a short phrase from the text."),
        _text("- Ask about what this text says, so that a student who has not read it cannot answer from "
              "general knowledge. Do not ask what a word means."),
        _text("- Spread the questions over the whole text, and do not give away one answer in another question."),
        "",
        _text("Reply in plain text, no tables, with exactly these five parts:"),
        _text("TEXT A: a short title, then the text."),
        _text("TEXT B: a short title, then the text."),
        _text("QUIZ: the twelve questions, numbered Q1: to Q12:, ready to print."),
        _text("ANSWERS: the answers, numbered Q1: to Q12: to match, with other answers that should also count "
              "as right."),
        _text("CHECK: every fact, figure, date or name in the texts that the teacher should verify, one per line."),
    ])
    return (
        '<section class="page">'
        + _top("Without the website · for teachers", "Your own prompt")
        + '<p class="intro" style="font-size:10.6pt">Fill in the blanks: the grade (it appears twice), your subject, '
        "the topic area and the language of the texts. Then type the prompt into any AI tool: Copilot, Gemini, "
        "ChatGPT or Claude. Read both texts and the quiz, and check every fact, before you print them: the AI "
        "proposes, you decide.</p>"
        + f'<div class="prompt">{prompt}</div>'
        + f'<p class="evidence">Faster online: the prompt builder at {URL} fills this in for you. Students do '
        "not use AI in this experiment. AI tools have age rules that change often: check them on the web page, "
        "and check your national rules and your school policy before you start.</p>"
        + _foot(7)
        + "</section>"
    )


def render_kit_html(data: dict) -> str:
    """Hela kitets HTML-källa. Samma JSON in ger samma text ut."""
    pages = [
        ("Sida 1: överblick", _overview(data)),
        ("Sida 2: Lesson 1-manus", _lesson1(data)),
        ("Sida 3: grupplappar att klippa ut", _group_cards(data)),
        ("Sida 4: gissningslappar att klippa ut", _prediction_slips(data)),
        ("Sida 5: poänglappar att klippa ut", _score_slips(data)),
        ("Sida 6: Lesson 2-manus, diskussion och förklaringar", _lesson2(data)),
        ("Sida 7: luckprompt för läraren", _fill_in()),
    ]
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n"
        f"<title>{TITLE} — teacher kit</title>\n"
        "<!-- Genererad av exports/build-study-experiment-pdf.py från study-experiment/experiment-en.json. "
        "Ändra JSON-filen eller skriptet, inte den här filen. -->\n"
        '<link rel="stylesheet" href="../../exports/_guide-print.css">\n'
        f"<style>{STYLE}</style>\n</head>\n<body>\n"
        + "\n".join(f"<!-- {label} -->\n{html}" for label, html in pages)
        + "\n</body>\n</html>\n"
    )


def main() -> None:
    from playwright.sync_api import sync_playwright

    data = json.loads(DATA.read_text(encoding="utf-8"))
    SRC.parent.mkdir(parents=True, exist_ok=True)
    SRC.write_text(render_kit_html(data), encoding="utf-8")
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
