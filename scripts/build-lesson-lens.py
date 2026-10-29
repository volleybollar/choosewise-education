#!/usr/bin/env python3
"""Build the static parts of /lesson-lens/ from lesson-lens/lenses-en.json.

Replaces the content between these marker pairs in lesson-lens/index.html:
  <!-- hero-example:start --> / <!-- hero-example:end -->  the default lens's example
  <!-- lenses:start -->       / <!-- lenses:end -->        the twelve lens cards
  <!-- legend:start -->       / <!-- legend:end -->        the evidence label legend
  <!-- sources:start -->      / <!-- sources:end -->       every source, with the lenses that use it
  <!-- age:start -->          / <!-- age:end -->           AI tools and age rules

Running it twice gives the same file. The prompt builder reads the same JSON
in the browser (assets/js/lesson-lens.js).

Usage:
    /usr/bin/python3 scripts/build-lesson-lens.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def render_example(lens: dict) -> str:
    """A lesson as planned and the four-part answer the prompt asks for."""
    ex = lens["example"]
    lesson = "".join(f"<li>{escape(line)}</li>" for line in ex["lesson"])
    upgrade = "".join(f"<li>{escape(u)}</li>" for u in ex["upgrade"])
    return (
        f'<div class="tm-example ll-example">'
        f'<h4 class="tm-example__subject">{escape(ex["subject"])} <span>· Grade {int(ex["grade"])} · {escape(lens["name"])}</span></h4>'
        f"<dl>"
        f'<dt>Lesson</dt><dd><ol class="ll-example__lesson">{lesson}</ol></dd>'
        f'<dt>Keep</dt><dd>{escape(ex["keep"])}</dd>'
        f'<dt>Upgrade</dt><dd><ol class="ll-example__upgrade">{upgrade}</ol></dd>'
        f'<dt>Nudge</dt><dd>{escape(ex["nudge"])}</dd>'
        f'<dt>Check</dt><dd>{escape(ex["check"])}</dd>'
        f"</dl>"
        f"</div>"
    )


def render_lens_card(lens: dict, labels: dict) -> str:
    """One lens as an <article>. All JSON text is HTML-escaped."""
    lid = escape(lens["id"])
    label = escape(lens["label"])
    sources = ", ".join(
        f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' for s in lens["sources"]
    )
    sources_html = f'<span class="tm-move__sources">Source: {sources}</span>' if sources else ""
    toolkit = " · ".join(
        f'<a href="{escape(t["href"])}">{escape(t["text"])}</a>' for t in lens["toolkit"]
    )
    return (
        f'<article class="tm-move ll-lens" id="{lid}" data-lens-id="{lid}">\n'
        f'  <div class="tm-move__head"><div><span class="tm-move__num">Lens {int(lens["number"])}</span>'
        f'<h3 class="tm-move__name">{escape(lens["name"])}</h3></div></div>\n'
        f'  <p class="tm-move__line">{escape(lens["one_liner"])}</p>\n'
        f'  <p class="tm-move__meta"><span class="tm-chip tm-chip--{label}">{escape(labels[lens["label"]]["name"])}</span></p>\n'
        f'  <details class="tm-move__more"><summary>A worked example and the evidence</summary>'
        f"{render_example(lens)}"
        f'<p class="tm-move__evidence"><strong>Evidence.</strong> {escape(lens["evidence"])} {sources_html}</p>'
        f'<p class="tm-move__evidence ll-lens__toolkit">Read more: {toolkit}</p>'
        f"</details>\n"
        f'  <a class="tm-move__use" href="?lens={lid}#ll-builder" data-use-lens="{lid}" '
        f'aria-label="Use this lens: {escape(lens["name"])}">Use this lens</a>\n'
        f"</article>"
    )


def render_legend(labels: dict) -> str:
    rows = "".join(
        f'<li><span class="tm-chip tm-chip--{key}">{escape(labels[key]["name"])}</span> {escape(labels[key]["definition"])}</li>'
        for key in ("strong", "promising", "framework", "choosewise")
    )
    return f'<ul class="tm-legend">{rows}</ul>'


def render_sources(lenses: list) -> str:
    """Every source once, in first-use order, with the lenses that cite it."""
    cited = {}
    for lens in lenses:
        for s in lens["sources"]:
            cited.setdefault(s["url"], (s["text"], []))[1].append(lens)
    rows = "".join(
        f'<li><a href="{escape(url)}">{escape(text)}</a> — '
        + ", ".join(f'<a href="#{escape(l["id"])}">{escape(l["name"])}</a>' for l in ls)
        + "</li>"
        for url, (text, ls) in cited.items()
    )
    return f'<ul class="tm-sources">{rows}</ul>'


def render_age(rules: list) -> str:
    rows = "".join(f"<li><strong>{escape(r['tool'])}:</strong> {escape(r['rule'])}</li>" for r in rules)
    return f'<ul class="tm-age">{rows}</ul>'


def _inject(html: str, name: str, content: str) -> str:
    pattern = re.compile(rf"(<!--\s*{name}:start\s*-->)(.*?)(<!--\s*{name}:end\s*-->)", re.S)
    if not pattern.search(html):
        raise ValueError(f"Missing <!-- {name}:start --> / <!-- {name}:end --> markers")
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(3)}", html)


def build(root: Path) -> None:
    data = json.loads((root / "lesson-lens/lenses-en.json").read_text(encoding="utf-8"))
    page = root / "lesson-lens/index.html"
    html = page.read_text(encoding="utf-8")
    default = next(l for l in data["lenses"] if l["id"] == data["default_lens"])
    html = _inject(html, "hero-example", render_example(default))
    html = _inject(html, "lenses", "\n".join(render_lens_card(l, data["labels"]) for l in data["lenses"]))
    html = _inject(html, "legend", render_legend(data["labels"]))
    html = _inject(html, "sources", render_sources(data["lenses"]))
    html = _inject(html, "age", render_age(data["age_rules"]))
    page.write_text(html, encoding="utf-8")
    print(f"Built {len(data['lenses'])} lenses into {page.relative_to(root)}")


if __name__ == "__main__":
    build(ROOT)
