#!/usr/bin/env python3
"""Build the static parts of /thinking-moves/ from thinking-moves/moves-en.json.

Replaces the content between these marker pairs in thinking-moves/index.html:
  <!-- moves:start -->    / <!-- moves:end -->     the twelve move cards
  <!-- clusters:start --> / <!-- clusters:end -->  the six clusters
  <!-- legend:start -->   / <!-- legend:end -->    the evidence label legend
  <!-- age:start -->      / <!-- age:end -->       AI tools and age rules

Running it twice gives the same file. The prompt builder reads the same JSON
in the browser (assets/js/thinking-moves.js).

Usage:
    /usr/bin/python3 scripts/build-thinking-moves.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXAMPLE_PARTS = [("task", "Task"), ("look_for", "Look for"), ("probe", "Probe"), ("think_back", "Think back")]


def _example_html(ex: dict) -> str:
    rows = "".join(f"<dt>{label}</dt><dd>{escape(ex[key])}</dd>" for key, label in EXAMPLE_PARTS)
    return (
        f'<div class="tm-example">'
        f'<h4 class="tm-example__subject">{escape(ex["subject"])} <span>· Grade {int(ex["grade"])}</span></h4>'
        f"<dl>{rows}</dl>"
        f"</div>"
    )


def render_move_card(move: dict, labels: dict) -> str:
    """One move as an <article>. All JSON text is HTML-escaped."""
    mid = escape(move["id"])
    label = escape(move["label"])
    sources = ", ".join(
        f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' for s in move["sources"]
    )
    examples = "".join(_example_html(ex) for ex in move["examples"])
    return (
        f'<article class="tm-move" id="{mid}" data-move-id="{mid}">\n'
        f'  <div class="tm-move__head">'
        f'<img class="tm-move__icon" src="/thinking-moves/icons/{mid}.svg" alt="" width="48" height="48">'
        f'<div><span class="tm-move__num">Move {int(move["number"])}</span>'
        f'<h3 class="tm-move__name">{escape(move["name"])}</h3></div></div>\n'
        f'  <p class="tm-move__line">{escape(move["one_liner"])}</p>\n'
        f'  <p class="tm-move__meta"><span class="tm-chip tm-chip--{label}">{escape(labels[move["label"]]["name"])}</span> '
        f'<span>{escape(move["modes"])}</span></p>\n'
        f'  <details class="tm-move__more"><summary>Two worked examples and the evidence</summary>'
        f"{examples}"
        f'<p class="tm-move__evidence"><strong>Evidence.</strong> {escape(move["evidence"])} '
        f'The label rates research on teaching this kind of thinking regularly, not a single five-minute move. '
        f'<span class="tm-move__sources">Source: {sources}</span></p>'
        f"</details>\n"
        f'  <a class="tm-move__use" href="?move={mid}#tm-builder" data-use-move="{mid}">Use this move</a>\n'
        f"</article>"
    )


def render_clusters(clusters: list, moves: list) -> str:
    """The six clusters with their modes and the moves that train them."""
    names = {m["id"]: m["name"] for m in moves}
    out = []
    for i, c in enumerate(clusters, start=1):
        modes = []
        for mode in c["modes"]:
            added = ' <span class="tm-added">added</span>' if mode.get("added") else ""
            note = f' <span class="tm-cluster__note">{escape(mode["note"])}</span>' if mode.get("note") else ""
            modes.append(f"<li>{escape(mode['name'])}{added}{note}</li>")
        links = ", ".join(f'<a href="#{escape(mid)}">{escape(names[mid])}</a>' for mid in c["moves"])
        out.append(
            f'<div class="tm-cluster">'
            f'<h3><span class="tm-cluster__num">{i}</span> {escape(c["name"])}</h3>'
            f'<p>{escape(c["description"])}</p>'
            f'<ul class="tm-cluster__modes">{"".join(modes)}</ul>'
            f'<p class="tm-cluster__moves">Moves: {links}</p>'
            f"</div>"
        )
    return "\n".join(out)


def render_legend(labels: dict) -> str:
    rows = "".join(
        f'<li><span class="tm-chip tm-chip--{key}">{escape(labels[key]["name"])}</span> {escape(labels[key]["definition"])}</li>'
        for key in ("strong", "promising", "framework")
    )
    return f'<ul class="tm-legend">{rows}</ul>\n<p class="tm-legend__note">{escape(labels["note"])}</p>'


def render_age(rules: list) -> str:
    rows = "".join(f"<li><strong>{escape(r['tool'])}:</strong> {escape(r['rule'])}</li>" for r in rules)
    return f'<ul class="tm-age">{rows}</ul>'


def _inject(html: str, name: str, content: str) -> str:
    pattern = re.compile(rf"(<!--\s*{name}:start\s*-->)(.*?)(<!--\s*{name}:end\s*-->)", re.S)
    if not pattern.search(html):
        raise ValueError(f"Missing <!-- {name}:start --> / <!-- {name}:end --> markers")
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(3)}", html)


def build(root: Path) -> None:
    data = json.loads((root / "thinking-moves/moves-en.json").read_text(encoding="utf-8"))
    page = root / "thinking-moves/index.html"
    html = page.read_text(encoding="utf-8")
    html = _inject(html, "moves", "\n".join(render_move_card(m, data["labels"]) for m in data["moves"]))
    html = _inject(html, "clusters", render_clusters(data["clusters"], data["moves"]))
    html = _inject(html, "legend", render_legend(data["labels"]))
    html = _inject(html, "age", render_age(data["age_rules"]))
    page.write_text(html, encoding="utf-8")
    print(f"Built {len(data['moves'])} moves into {page.relative_to(root)}")


if __name__ == "__main__":
    build(ROOT)
