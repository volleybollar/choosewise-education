#!/usr/bin/env python3
"""Bygger de statiska delarna av /study-moves/ från study-moves/moves-en.json.

Ersätter innehållet mellan de här markörparen i study-moves/index.html:
  <!-- goals:start -->     / <!-- goals:end -->      startnoten, de sex målrutorna och 80/20-noten
  <!-- feels:start -->     / <!-- feels:end -->      varför bra studier känns svårare, med källor
  <!-- moves:start -->     / <!-- moves:end -->      de tio dragkorten
  <!-- legend:start -->    / <!-- legend:end -->     förklaringen av evidensetiketterna
  <!-- classroom:start --> / <!-- classroom:end -->  noten om klassrum kontra labb
  <!-- sources:start -->   / <!-- sources:end -->    varje källa, med de drag som använder den
  <!-- age:start -->       / <!-- age:end -->        ingressen med datum och AI-verktygens åldersregler

Körs skriptet två gånger blir filen likadan. Promptbyggaren läser samma
JSON i webbläsaren (assets/js/study-moves.js), och kortleken byggs från den
av exports/build-study-moves-pdf.py.

Användning:
    /usr/bin/python3 scripts/build-study-moves.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABEL_ORDER = ("strong", "promising", "framework")


def _links(links: list, sep: str = " · ") -> str:
    return sep.join(f'<a href="{escape(l["href"])}">{escape(l["text"])}</a>' for l in links)


def _sources(sources: list) -> str:
    """Källorna som länkar efter "Source:" eller "Sources:"."""
    word = "Source" if len(sources) == 1 else "Sources"
    items = ", ".join(f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' for s in sources)
    return f'<span class="tm-move__sources">{word}: {items}</span>'


def render_goals(data: dict) -> str:
    """Startnoten, en ruta per mål med länkar till dess drag, och 80/20-noten."""
    by_id = {m["id"]: m for m in data["moves"]}
    start = by_id[data["default_move"]]
    tiles = "".join(
        f'<li class="sm-goal"><h3 class="sm-goal__name">{escape(g["name"])}</h3>'
        f'<p class="sm-goal__desc">{escape(g["description"])}</p>'
        f'<ul class="sm-goal__moves">'
        + "".join(f'<li><a href="#{escape(mid)}">{escape(by_id[mid]["name"])}</a></li>' for mid in g["moves"])
        + "</ul></li>"
        for g in data["goals"]
    )
    return (
        f'<p class="sm-start" id="sm-start"><strong>Not sure? Start here.</strong> '
        f'Try <a href="#{escape(start["id"])}">{escape(start["name"])}</a> first. {escape(start["one_liner"])}</p>\n'
        f'<ul class="sm-goals">{tiles}</ul>\n'
        f'<p class="tm-note sm-eighty">{escape(data["eighty_twenty"])}</p>'
    )


def render_feels(feels: dict) -> str:
    return f'<p class="sm-feels">{escape(feels["text"])} {_sources(feels["sources"])}</p>'


def render_move_card(move: dict, data: dict) -> str:
    """Ett drag som <article>. All text från JSON-filen HTML-escapas."""
    mid = escape(move["id"])
    name = escape(move["name"])
    label = escape(move["label"])
    goal_names = {g["id"]: g["name"] for g in data["goals"]}
    goals = " · ".join(escape(goal_names[g]) for g in move["goals"])
    steps = "".join(f"<li>{escape(s)}</li>" for s in move["steps"])
    ex = move["example"]
    return (
        f'<article class="tm-move sm-move" id="{mid}" data-move-id="{mid}">\n'
        f'  <div class="tm-move__head"><div><span class="tm-move__num">Move {int(move["number"])}</span>'
        f'<h3 class="tm-move__name">{name}</h3></div></div>\n'
        f'  <p class="tm-move__meta"><span class="tm-chip tm-chip--{label}">{escape(data["labels"][move["label"]]["name"])}</span> '
        f'<span class="sm-move__research">{escape(move["research_name"])}</span></p>\n'
        f'  <p class="tm-move__line">{escape(move["one_liner"])}</p>\n'
        f'  <p class="sm-move__goals">Good for: {goals}</p>\n'
        f'  <details class="tm-move__more"><summary>How to do it, with and without AI</summary>'
        f'<h4 class="sm-part">How to do it</h4><ol class="sm-steps">{steps}</ol>'
        f'<div class="tm-example sm-example"><h4 class="tm-example__subject">Example: {escape(ex["subject"])} '
        f'<span>· Grade {int(ex["grade"])}</span></h4><p>{escape(ex["text"])}</p></div>'
        f'<h4 class="sm-part">How it feels</h4><p class="sm-feels">{escape(move["feels"])}</p>'
        f'<h4 class="sm-part">With AI: your teacher</h4><p>{escape(move["teacher_ai"]["card"])}</p>'
        f'<h4 class="sm-part">With AI: you (13+)</h4><p>{escape(move["student_ai"]["card"])}</p>'
        f'<h4 class="sm-part">Watch out</h4><p>{escape(move["watch_out"])}</p>'
        f'<p class="tm-move__evidence"><strong>Evidence.</strong> {escape(move["evidence"])} {_sources(move["sources"])}</p>'
        f'<p class="tm-move__evidence sm-move__read">Read more: {_links(move["toolkit"] + move["related"])}</p>'
        f"</details>\n"
        f'  <div class="sm-move__use">'
        f'<a class="tm-move__use" href="?move={mid}&amp;for=teacher#sm-builder" data-use-move="{mid}" data-use-for="teacher" '
        f'aria-label="{name}, teacher: prepare it with AI">Teacher: prepare it with AI</a>'
        f'<a class="tm-move__use" href="?move={mid}&amp;for=student#sm-builder" data-use-move="{mid}" data-use-for="student" '
        f'aria-label="{name}, student: study with AI (13+)">Student: study with AI (13+)</a>'
        f"</div>\n"
        f"</article>"
    )


def render_legend(labels: dict) -> str:
    rows = "".join(
        f'<li><span class="tm-chip tm-chip--{key}">{escape(labels[key]["name"])}</span> {escape(labels[key]["definition"])}</li>'
        for key in LABEL_ORDER
    )
    return f'<ul class="tm-legend">{rows}</ul>'


def render_classroom(note: str) -> str:
    return f'<p class="tm-note">{escape(note)}</p>'


def render_sources(moves: list) -> str:
    """Varje källa en gång, i den ordning den först används, med dragen som citerar den."""
    cited = {}
    for move in moves:
        for s in move["sources"]:
            cited.setdefault(s["url"], (s["text"], []))[1].append(move)
    rows = "".join(
        f'<li><a href="{escape(url)}">{escape(text)}</a> — '
        + ", ".join(f'<a href="#{escape(m["id"])}">{escape(m["name"])}</a>' for m in ms)
        + "</li>"
        for url, (text, ms) in cited.items()
    )
    return f'<ul class="tm-sources">{rows}</ul>'


def render_age_lede(date: str) -> str:
    return (
        f'<p class="section__lede">You never need AI to use a move. '
        f"If you use AI yourself, these rules apply ({escape(date)}):</p>"
    )


def render_age(rules: list) -> str:
    rows = "".join(f"<li><strong>{escape(r['tool'])}:</strong> {escape(r['rule'])}</li>" for r in rules)
    return f'<ul class="tm-age">{rows}</ul>'


def _inject(html: str, name: str, content: str) -> str:
    pattern = re.compile(rf"(<!--\s*{name}:start\s*-->)(.*?)(<!--\s*{name}:end\s*-->)", re.S)
    if not pattern.search(html):
        raise ValueError(f"Missing <!-- {name}:start --> / <!-- {name}:end --> markers")
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(3)}", html)


def build(root: Path) -> None:
    data = json.loads((root / "study-moves/moves-en.json").read_text(encoding="utf-8"))
    page = root / "study-moves/index.html"
    html = page.read_text(encoding="utf-8")
    html = _inject(html, "goals", render_goals(data))
    html = _inject(html, "feels", render_feels(data["feels_harder"]))
    html = _inject(html, "moves", "\n".join(render_move_card(m, data) for m in data["moves"]))
    html = _inject(html, "legend", render_legend(data["labels"]))
    html = _inject(html, "classroom", render_classroom(data["classroom_note"]))
    html = _inject(html, "sources", render_sources(data["moves"]))
    html = _inject(html, "age", render_age_lede(data["age_rules_date"]) + "\n" + render_age(data["age_rules"]))
    page.write_text(html, encoding="utf-8")
    print(f"Built {len(data['moves'])} moves into {page.relative_to(root)}")


if __name__ == "__main__":
    build(ROOT)
