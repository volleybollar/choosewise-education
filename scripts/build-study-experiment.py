#!/usr/bin/env python3
"""Bygger de statiska delarna av /study-experiment/ från study-experiment/experiment-en.json.

Ersätter innehållet mellan de här markörparen i study-experiment/index.html:
  <!-- overview:start -->   / <!-- overview:end -->    de två lektionerna i korthet, material, före start och "What to expect"
  <!-- lesson1:start -->    / <!-- lesson1:end -->     lektion 1: ingress och numrerade steg
  <!-- lesson2:start -->    / <!-- lesson2:end -->     lektion 2: ingress och numrerade steg
  <!-- discussion:start --> / <!-- discussion:end -->  frågorna, de tre förklaringarna, jämnt resultat och "no computer"
  <!-- noai:start -->       / <!-- noai:end -->        stycket om hur man gör utan AI, under byggaren
  <!-- evidence:start -->   / <!-- evidence:end -->    forskningen, med källlänkar
  <!-- age:start -->        / <!-- age:end -->         ingressen med datum och AI-verktygens åldersregler

Körs skriptet två gånger blir filen likadan. Byggaren och resultatvyn är
statisk HTML i sidan och har egen JavaScript (assets/js/study-experiment.js);
PDF-kitet byggs från samma JSON av exports/build-study-experiment-pdf.py.

Användning:
    /usr/bin/python3 scripts/build-study-experiment.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Två rader om vad varje lektion går ut på, till översikten. De ligger här och
# inte i JSON-filen eftersom de bara är rubriktext till rutorna; stegen och
# tiderna kommer från JSON-filen.
GLANCE = (
    ("lesson1", "Lesson 1", "#se-lesson1",
     "Every student studies two texts, one by reading it twice and one by testing themselves, "
     "and predicts which will be remembered better."),
    ("lesson2", "Lesson 2, one week later", "#se-lesson2",
     "A surprise quiz on both texts. The class result goes on the board, and you talk about what it means."),
)


def _sources(sources: list) -> str:
    """Källorna som länkar efter "Source:" eller "Sources:"."""
    word = "Source" if len(sources) == 1 else "Sources"
    items = ", ".join(f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' for s in sources)
    return f'<span class="tm-move__sources">{word}: {items}</span>'


def render_overview(data: dict) -> str:
    """De två lektionerna i korthet (med minuter), material, före start och "What to expect"."""
    boxes = "".join(
        f'<li class="se-glance__box"><h3 class="se-glance__title"><a href="{href}">{escape(title)}</a></h3>'
        f'<p class="se-glance__time">{int(data["minutes"][key])} minutes</p>'
        f'<p class="se-glance__text">{escape(text)}</p></li>'
        for key, title, href, text in GLANCE
    )
    materials = "".join(f"<li>{escape(m)}</li>" for m in data["materials"])
    before = "".join(f"<li>{escape(b)}</li>" for b in data["before"])
    return (
        f'<ul class="se-glance">{boxes}</ul>\n'
        f'<div class="se-prep">\n'
        f'  <div class="se-prep__col"><h3 class="se-prep__title">You need</h3><ul class="se-list">{materials}</ul></div>\n'
        f'  <div class="se-prep__col"><h3 class="se-prep__title">Before you start</h3><ol class="se-list">{before}</ol></div>\n'
        f"</div>\n"
        f'<div class="tm-note se-expect"><h3 class="se-prep__title">What to expect</h3>'
        f'<p>{escape(data["expect"])}</p></div>'
    )


def render_lesson(lesson: dict, data: dict, number: int) -> str:
    """Ingressen och stegen som en numrerad lista. Ett steg med minuter får en liten etikett."""
    steps = "".join(
        "<li>"
        + (f'<span class="se-minutes">{int(s["minutes"])} min</span>' if s["minutes"] is not None else "")
        + f'<span class="se-step__text">{escape(s["text"])}</span></li>'
        for s in lesson["steps"]
    )
    total = int(data["minutes"][f"lesson{number}"])
    return (
        f'<p class="section__lede">{escape(lesson["intro"])}</p>\n'
        f'<ol class="se-steps" aria-label="Lesson {int(number)}, {total} minutes">{steps}</ol>'
    )


def render_discussion(data: dict) -> str:
    """Frågorna, de tre förklaringarna, det jämna resultatet och vägen utan dator."""
    questions = "".join(f"<li>{escape(q)}</li>" for q in data["discussion"])
    points = "".join(f"<li>{escape(p)}</li>" for p in data["explain"]["points"])
    even = data["even_result"]
    return (
        f'<div class="se-talk">\n'
        f'  <h3 class="se-talk__title">Questions for the class</h3>\n'
        f'  <ol class="se-list">{questions}</ol>\n'
        f'  <h3 class="se-talk__title">{escape(data["explain"]["title"])}</h3>\n'
        f'  <ol class="se-list">{points}</ol>\n'
        f'  <div class="se-even-result" id="se-even-result">\n'
        f'    <h3 class="se-talk__title">{escape(even["title"])}</h3>\n'
        f'    <p>{escape(even["text"])}</p>\n'
        f"  </div>\n"
        f'  <p class="tm-note se-nocomputer">{escape(data["no_computer"])}</p>\n'
        f"</div>"
    )


def render_noai(data: dict) -> str:
    return f'<p class="tm-note se-noai">{escape(data["no_ai"])}</p>'


def render_evidence(data: dict) -> str:
    """Varje evidenspunkt som ett stycke, med sina källor som länkar."""
    return "\n".join(
        f'<p class="se-evidence">{escape(item["text"])} {_sources(item["sources"])}</p>' for item in data["evidence"]
    )


def render_age(data: dict) -> str:
    """Ingressen med datumet och AI-verktygens åldersregler."""
    rows = "".join(f"<li><strong>{escape(r['tool'])}:</strong> {escape(r['rule'])}</li>" for r in data["age_rules"])
    return (
        f'<p class="section__lede">Students do not use AI in this experiment. '
        f"If you use AI to make the material, these rules apply ({escape(data['age_rules_date'])}):</p>\n"
        f'<ul class="tm-age">{rows}</ul>'
    )


def _inject(html: str, name: str, content: str) -> str:
    pattern = re.compile(rf"(<!--\s*{name}:start\s*-->)(.*?)(<!--\s*{name}:end\s*-->)", re.S)
    if not pattern.search(html):
        raise ValueError(f"Missing <!-- {name}:start --> / <!-- {name}:end --> markers")
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(3)}", html)


def build(root: Path) -> None:
    data = json.loads((root / "study-experiment/experiment-en.json").read_text(encoding="utf-8"))
    page = root / "study-experiment/index.html"
    html = page.read_text(encoding="utf-8")
    html = _inject(html, "overview", render_overview(data))
    html = _inject(html, "lesson1", render_lesson(data["lesson1"], data, 1))
    html = _inject(html, "lesson2", render_lesson(data["lesson2"], data, 2))
    html = _inject(html, "discussion", render_discussion(data))
    html = _inject(html, "noai", render_noai(data))
    html = _inject(html, "evidence", render_evidence(data))
    html = _inject(html, "age", render_age(data))
    page.write_text(html, encoding="utf-8")
    print(f"Built the Study Experiment page into {page.relative_to(root)}")


if __name__ == "__main__":
    build(ROOT)
