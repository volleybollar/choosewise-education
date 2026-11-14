#!/usr/bin/env python3
"""Bygger de statiska delarna av /test-countdown/ från test-countdown/countdown-en.json.

Ersätter innehållet mellan de här markörparen i test-countdown/index.html:
  <!-- howto:start -->    / <!-- howto:end -->     "How to quiz yourself": rubrik, fyra steg och noten om att det känns svårare
  <!-- why:start -->      / <!-- why:end -->       "Why the plan looks like this": rubrik, ingress och fem punkter
  <!-- notes:start -->    / <!-- notes:end -->     noterna i planen: kort tid (dold), långt avstånd (dold) och "sensible"
  <!-- share:start -->    / <!-- share:end -->     läraren: hur man delar planen med klassen
  <!-- noai:start -->     / <!-- noai:end -->      läraren: vägen utan AI
  <!-- evidence:start --> / <!-- evidence:end -->  forskningen, med källlänkar
  <!-- age:start -->      / <!-- age:end -->       ingressen med datum, AI-verktygens åldersregler och pekaren till Study Moves

Körs skriptet två gånger blir filen likadan. Planeraren, planen och
promptbyggaren är statisk HTML i sidan och har egen JavaScript
(assets/js/test-countdown.js); här byggs bara texten som kommer från JSON-filen.

Användning:
    /usr/bin/python3 scripts/build-test-countdown.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _sources(sources: list) -> str:
    """Källorna som länkar efter "Source:" eller "Sources:"."""
    word = "Source" if len(sources) == 1 else "Sources"
    items = ", ".join(f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' for s in sources)
    return f'<span class="tm-move__sources">{word}: {items}</span>'


def render_howto(data: dict) -> str:
    """Rubriken, de fyra stegen som en numrerad lista och noten om att det känns svårare."""
    how = data["how_to"]
    steps = "".join(f"<li>{escape(s)}</li>" for s in how["steps"])
    return (
        f'<h2 class="section__title">{escape(how["title"])}</h2>\n'
        f'<ol class="tc-list">{steps}</ol>\n'
        f'<p class="tm-note">{escape(data["feels_harder"])}</p>'
    )


def render_why(data: dict) -> str:
    """Rubriken, ingressen till elever och föräldrar och de fem punkterna."""
    why = data["why"]
    points = "".join(f"<li>{escape(p)}</li>" for p in why["points"])
    return (
        f'<h2 class="section__title">{escape(why["title"])}</h2>\n'
        f'<p class="section__lede">{escape(why["intro"])}</p>\n'
        f'<ul class="tc-list">{points}</ul>'
    )


def render_notes(data: dict) -> str:
    """Noterna i planen. De två första är dolda; test-countdown.js visar rätt not när planen byggs."""
    return (
        f'<p class="tm-note" id="tc-short" hidden>{escape(data["short_note"])}</p>\n'
        f'<p class="tm-note" id="tc-capped" hidden>{escape(data["capped_note"])}</p>\n'
        f'<p class="tc-sensible">{escape(data["sensible"])}</p>'
    )


def render_share(data: dict) -> str:
    return f'<p>{escape(data["share"])}</p>'


def render_noai(data: dict) -> str:
    return f'<p class="tm-note">{escape(data["no_ai"])}</p>'


def render_evidence(data: dict) -> str:
    """Varje evidenspunkt som ett stycke, med sina källor som länkar."""
    return "\n".join(
        f'<p class="tc-evidence__item">{escape(item["text"])} {_sources(item["sources"])}</p>'
        for item in data["evidence"]
    )


def render_age(data: dict) -> str:
    """Ingressen med datumet, åldersreglerna och pekaren till elevprompten i Study Moves (för elever från 13 år)."""
    rows = "".join(f"<li><strong>{escape(r['tool'])}:</strong> {escape(r['rule'])}</li>" for r in data["age_rules"])
    return (
        f'<p class="section__lede">You do not need AI for this plan. '
        f"If you use AI to make the quizzes, these rules apply ({escape(data['age_rules_date'])}):</p>\n"
        f'<ul class="tm-age">{rows}</ul>\n'
        f'<p class="tm-note">{escape(data["student_ai"])} '
        f'<a href="/study-moves/#test-yourself">Test yourself in Study Moves</a>.</p>'
    )


def _inject(html: str, name: str, content: str) -> str:
    pattern = re.compile(rf"(<!--\s*{name}:start\s*-->)(.*?)(<!--\s*{name}:end\s*-->)", re.S)
    if not pattern.search(html):
        raise ValueError(f"Missing <!-- {name}:start --> / <!-- {name}:end --> markers")
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(3)}", html)


def build(root: Path) -> None:
    data = json.loads((root / "test-countdown/countdown-en.json").read_text(encoding="utf-8"))
    page = root / "test-countdown/index.html"
    html = page.read_text(encoding="utf-8")
    html = _inject(html, "howto", render_howto(data))
    html = _inject(html, "why", render_why(data))
    html = _inject(html, "notes", render_notes(data))
    html = _inject(html, "share", render_share(data))
    html = _inject(html, "noai", render_noai(data))
    html = _inject(html, "evidence", render_evidence(data))
    html = _inject(html, "age", render_age(data))
    page.write_text(html, encoding="utf-8")
    print(f"Built the Test Countdown page into {page.relative_to(root)}")


if __name__ == "__main__":
    build(ROOT)
