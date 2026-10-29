#!/usr/bin/env python3
"""Build the static parts of /retrieval-rhythm/ from retrieval-rhythm/rhythm-en.json.

Replaces the content between these marker pairs in retrieval-rhythm/index.html:
  <!-- hero-example:start --> / <!-- hero-example:end -->  the starter quiz example
  <!-- log:start -->          / <!-- log:end -->           the example topic log
  <!-- formats:start -->      / <!-- formats:end -->       the five format cards
  <!-- legend:start -->       / <!-- legend:end -->        the evidence label legend
  <!-- sources:start -->      / <!-- sources:end -->       the approaches and their sources
  <!-- age:start -->          / <!-- age:end -->           AI tools and age rules

Running it twice gives the same file. The prompt builder reads the same JSON
in the browser (assets/js/retrieval-rhythm.js).

Usage:
    /usr/bin/python3 scripts/build-retrieval-rhythm.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def render_example(fmt: dict, heading: str = "h4") -> str:
    """One starter as students see it, and its key.

    heading is h3 in the hero (under an h2) and h4 in the cards (under an h3)."""
    ex = fmt["example"]
    return (
        f'<div class="tm-example rr-example">'
        f'<{heading} class="tm-example__subject">Lesson {int(ex["lesson"])} <span>· {escape(fmt["name"])}</span></{heading}>'
        f"<dl>"
        f'<dt>Starter</dt><dd class="rr-example__text">{escape(ex["starter"])}</dd>'
        f'<dt>Key</dt><dd class="rr-example__text">{escape(ex["key"])}</dd>'
        f"</dl>"
        f"</div>"
    )


def render_format_card(fmt: dict) -> str:
    """One format as an <article>. All JSON text is HTML-escaped."""
    fid = escape(fmt["id"])
    steps = "".join(f"<li>{escape(s)}</li>" for s in fmt["steps"])
    return (
        f'<article class="tm-move rr-format" id="{fid}" data-format-id="{fid}">\n'
        f'  <div class="tm-move__head"><div><span class="tm-move__num">{int(fmt["minutes"])} min</span>'
        f'<h3 class="tm-move__name">{escape(fmt["name"])}</h3></div></div>\n'
        f'  <p class="tm-move__line">{escape(fmt["one_liner"])}</p>\n'
        f'  <ol class="rr-steps">{steps}</ol>\n'
        f'  <details class="tm-move__more"><summary>An example from the History log</summary>'
        f"{render_example(fmt)}"
        f"</details>\n"
        f'  <a class="tm-move__use" href="?format={fid}#rr-builder" data-use-format="{fid}" '
        f'aria-label="Use this format: {escape(fmt["name"])}">Use this format</a>\n'
        f"</article>"
    )


def render_example_log(rows: list) -> str:
    """The example log as a list, one row per lesson (a list does not
    overflow on a phone the way a four-column table does)."""
    items = "".join(
        f'<li><span class="rr-log__date">{escape(r["date"])}</span> '
        f'<strong>{escape(r["topic"])}</strong> '
        f'<span class="rr-log__points">{escape(r["key_points"])}</span></li>'
        for r in rows
    )
    return f'<ul class="rr-log">{items}</ul>'


def render_legend(labels: dict) -> str:
    rows = "".join(
        f'<li><span class="tm-chip tm-chip--{key}">{escape(labels[key]["name"])}</span> {escape(labels[key]["definition"])}</li>'
        for key in ("strong", "promising", "framework")
    )
    return f'<ul class="tm-legend">{rows}</ul>'


def render_approaches(approaches: list, labels: dict) -> str:
    out = []
    for a in approaches:
        sources = ", ".join(f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' for s in a["sources"])
        out.append(
            f'<div class="rr-approach">'
            f'<h3>{escape(a["name"])} <span class="tm-chip tm-chip--{escape(a["label"])}">{escape(labels[a["label"]]["name"])}</span></h3>'
            f'<p>{escape(a["evidence"])}</p>'
            f'<p class="tm-move__sources">Source: {sources}</p>'
            f"</div>"
        )
    return "\n".join(out)


def render_age(rules: list) -> str:
    rows = "".join(f"<li><strong>{escape(r['tool'])}:</strong> {escape(r['rule'])}</li>" for r in rules)
    return f'<ul class="tm-age">{rows}</ul>'


def _inject(html: str, name: str, content: str) -> str:
    pattern = re.compile(rf"(<!--\s*{name}:start\s*-->)(.*?)(<!--\s*{name}:end\s*-->)", re.S)
    if not pattern.search(html):
        raise ValueError(f"Missing <!-- {name}:start --> / <!-- {name}:end --> markers")
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(3)}", html)


def build(root: Path) -> None:
    data = json.loads((root / "retrieval-rhythm/rhythm-en.json").read_text(encoding="utf-8"))
    page = root / "retrieval-rhythm/index.html"
    html = page.read_text(encoding="utf-8")
    formats = [f for f in data["formats"] if f["id"] != "mix"]
    quiz = next(f for f in formats if f["id"] == "starter-quiz")
    html = _inject(html, "hero-example", render_example(quiz, heading="h3"))
    html = _inject(html, "log", render_example_log(data["example_log"]))
    html = _inject(html, "formats", "\n".join(render_format_card(f) for f in formats))
    html = _inject(html, "legend", render_legend(data["labels"]))
    html = _inject(html, "sources", render_approaches(data["approaches"], data["labels"]))
    html = _inject(html, "age", render_age(data["age_rules"]))
    page.write_text(html, encoding="utf-8")
    print(f"Built {len(formats)} formats into {page.relative_to(root)}")


if __name__ == "__main__":
    build(ROOT)
