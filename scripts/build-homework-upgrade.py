#!/usr/bin/env python3
"""Build the static parts of the Homework Upgrade page from homework-upgrade-1f0cd17c/upgrade-en.json.

The page is for Skool members only. It is reached through a hidden link, has
noindex (HIDDEN_PATHS in scripts/build-seo-meta.py) and is never linked from
the rest of the site.

Replaces the content between these marker pairs in homework-upgrade-1f0cd17c/index.html:
  <!-- hero-example:start -->    / <!-- hero-example:end -->     the worked example (History, Grade 8)
  <!-- data:start -->            / <!-- data:end -->             the patterns as JSON for the prompt builder
  <!-- pattern-options:start --> / <!-- pattern-options:end -->  the pattern choices in the builder's select
  <!-- patterns:start -->        / <!-- patterns:end -->         the legend, the seven groups and the twelve cards
  <!-- check:start -->           / <!-- check:end -->            the check in the next lesson
  <!-- students:start -->        / <!-- students:end -->         the text for students, with its copy button
  <!-- evidence:start -->        / <!-- evidence:end -->         the six research items and their sources
  <!-- age:start -->             / <!-- age:end -->              AI tools and age rules

Running it twice gives the same file. The prompt text lives in
assets/js/homework-upgrade.js, not in the JSON.

Usage:
    /usr/bin/python3 scripts/build-homework-upgrade.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "homework-upgrade-1f0cd17c"

# The legend lists the labels in this order (there is no Framework label here).
LABEL_ORDER = ("strong", "promising", "choosewise")


def _source_links(sources: list) -> str:
    """'Source: a, b' as links. 'Sources:' when there is more than one."""
    links = ", ".join(f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' for s in sources)
    word = "Sources" if len(sources) > 1 else "Source"
    return f'<span class="tm-move__sources">{word}: {links}</span>'


def render_example(data: dict) -> str:
    """The worked example: the homework as set, and the four-part answer the prompt asks for."""
    ex = data["example"]
    pattern = next(p for p in data["patterns"] if p["id"] == ex["pattern"])
    homework = "".join(f"<li>{escape(line)}</li>" for line in ex["homework"])
    upgrade = "".join(f"<li>{escape(step)}</li>" for step in ex["upgrade"])
    risk = "".join(f"<p>{escape(line)}</p>" for line in ex["ai_risk"])
    check = "".join(
        f'<li><p class="hu-qa__q"><strong>Q{i}:</strong> {escape(item["q"])}</p>'
        f'<p class="hu-qa__a"><strong>A{i}:</strong> {escape(item["a"])}</p></li>'
        for i, item in enumerate(ex["check"], start=1)
    )
    return (
        '<div class="tm-example hu-example">'
        f'<h3 class="tm-example__subject">{escape(ex["subject"])} <span>· Grade {int(ex["grade"])} · '
        f'{escape(pattern["name"])} · {int(ex["minutes"])} minutes</span></h3>'
        "<dl>"
        f'<dt>The homework as set</dt><dd><ul class="hu-example__list">{homework}</ul></dd>'
        f'<dt>Keep</dt><dd>{escape(ex["keep"])}</dd>'
        f'<dt>Upgrade</dt><dd><ol class="hu-example__list">{upgrade}</ol></dd>'
        f"<dt>AI risk</dt><dd>{risk}</dd>"
        f'<dt>Check</dt><dd><ul class="hu-qa">{check}</ul></dd>'
        "</dl>"
        "</div>"
    )


def render_pattern_options(data: dict) -> str:
    """The twelve patterns as <optgroup>s, one per group. The first option
    ("Let the AI choose") is written by hand in the page."""
    groups = []
    for group in data["groups"]:
        options = "".join(
            f'<option value="{escape(p["id"])}">{int(p["number"])}. {escape(p["name"])}</option>'
            for p in data["patterns"]
            if p["group"] == group["id"]
        )
        groups.append(f'<optgroup label="{escape(group["name"])}">{options}</optgroup>')
    return "\n".join(groups)


def render_pattern_card(pattern: dict, labels: dict) -> str:
    """One pattern as an <article>. All JSON text is HTML-escaped."""
    pid = escape(pattern["id"])
    label = escape(pattern["label"])
    steps = "".join(f"<li>{escape(step)}</li>" for step in pattern["steps"])
    return (
        f'<article class="tm-move hu-pattern" id="{pid}" data-pattern-id="{pid}">\n'
        f'  <div class="tm-move__head"><div><span class="tm-move__num">Pattern {int(pattern["number"])}</span>'
        f'<h4 class="tm-move__name">{escape(pattern["name"])}</h4></div></div>\n'
        f'  <p class="tm-move__line"><strong>Instead of:</strong> {escape(pattern["instead"])}</p>\n'
        f'  <p class="tm-move__meta"><span class="tm-chip tm-chip--{label}">{escape(labels[pattern["label"]]["name"])}</span></p>\n'
        f'  <ol class="hu-steps">{steps}</ol>\n'
        f'  <p class="tm-move__line"><strong>Check next lesson:</strong> {escape(pattern["check"])}</p>\n'
        f'  <details class="tm-move__more"><summary>Why it works</summary>'
        f'<p class="tm-move__evidence">{escape(pattern["why"])}</p>'
        f'<p class="tm-move__evidence">{escape(pattern["tip"])}</p>'
        f'<p class="tm-move__evidence"><strong>If a chatbot does it:</strong> {escape(pattern["chatbot"])}</p>'
        f'<p class="tm-move__evidence">{_source_links(pattern["sources"])}</p>'
        f"</details>\n"
        f'  <a class="tm-move__use" href="?pattern={pid}#hu-builder" data-use-pattern="{pid}" '
        f'aria-label="Use this pattern: {escape(pattern["name"])}">Use this pattern</a>\n'
        f"</article>"
    )


def render_legend(labels: dict) -> str:
    rows = "".join(
        f'<li><span class="tm-chip tm-chip--{key}">{escape(labels[key]["name"])}</span> {escape(labels[key]["definition"])}</li>'
        for key in LABEL_ORDER
    )
    return f'<ul class="tm-legend">{rows}</ul>'


def render_patterns(data: dict) -> str:
    """The legend, then each group: an h3 and the cards of its patterns."""
    out = [render_legend(data["labels"])]
    for group in data["groups"]:
        cards = "\n".join(
            render_pattern_card(p, data["labels"]) for p in data["patterns"] if p["group"] == group["id"]
        )
        out.append(
            f'<div class="hu-group">\n<h3 class="hu-group__title">{escape(group["name"])}</h3>\n'
            f'<div class="tm-grid">\n{cards}\n</div>\n</div>'
        )
    return "\n".join(out)


def render_check(check: dict) -> str:
    steps = "".join(f"<li>{escape(step)}</li>" for step in check["steps"])
    return (
        f'<ol class="hu-list">{steps}</ol>\n'
        f'<p class="hu-prose">{escape(check["why"])}</p>\n'
        f'<p class="hu-prose">{escape(check["detectors"])}</p>'
    )


def render_students(students: dict) -> str:
    """The intro, the four paragraphs in a box and a button that copies them
    (separated by a blank line). The copy-toast must follow the button: the
    shared script looks for it among the button's siblings."""
    paragraphs = "".join(f"<p>{escape(p)}</p>" for p in students["text"])
    joined = "\n\n".join(students["text"])
    return (
        f'<p class="section__lede">{escape(students["intro"])}</p>\n'
        f'<div class="hu-students__text">{paragraphs}</div>\n'
        '<div class="tm-copy-row">'
        f'<button type="button" class="btn btn--primary" data-copy="{escape(joined)}">Copy text</button>'
        '<span class="copy-toast" role="status">Copied</span>'
        "</div>"
    )


def render_evidence(items: list) -> str:
    return "\n".join(
        f'<p class="hu-evidence__item"><strong>{escape(item["title"])}</strong> {escape(item["text"])} '
        f'{_source_links(item["sources"])}</p>'
        for item in items
    )


def render_age(rules: list, date: str) -> str:
    rows = "".join(f"<li><strong>{escape(r['tool'])}:</strong> {escape(r['rule'])}</li>" for r in rules)
    return (
        '<p class="section__lede">You use AI to prepare. The upgraded homework needs no AI. '
        f"If students use AI tools, these rules apply ({escape(date)}):</p>\n"
        f'<ul class="tm-age">{rows}</ul>'
    )


def render_data(data: dict) -> str:
    """The patterns the prompt builder needs, as JSON. '</' is written '<\\/' so
    the text can never close the script tag."""
    slim = [{"id": p["id"], "name": p["name"], "brief": p["brief"]} for p in data["patterns"]]
    text = json.dumps({"patterns": slim}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/json" id="hu-data">{text}</script>'


def _inject(html: str, name: str, content: str) -> str:
    pattern = re.compile(rf"(<!--\s*{name}:start\s*-->)(.*?)(<!--\s*{name}:end\s*-->)", re.S)
    if not pattern.search(html):
        raise ValueError(f"Missing <!-- {name}:start --> / <!-- {name}:end --> markers")
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(3)}", html)


def build(root: Path) -> None:
    data = json.loads((root / SLUG / "upgrade-en.json").read_text(encoding="utf-8"))
    page = root / SLUG / "index.html"
    html = page.read_text(encoding="utf-8")
    html = _inject(html, "hero-example", render_example(data))
    html = _inject(html, "data", render_data(data))
    html = _inject(html, "pattern-options", render_pattern_options(data))
    html = _inject(html, "patterns", render_patterns(data))
    html = _inject(html, "check", render_check(data["check"]))
    html = _inject(html, "students", render_students(data["students"]))
    html = _inject(html, "evidence", render_evidence(data["evidence"]))
    html = _inject(html, "age", render_age(data["age_rules"], data["age_rules_date"]))
    page.write_text(html, encoding="utf-8")
    print(f"Built {len(data['patterns'])} patterns into {page.relative_to(root)}")


if __name__ == "__main__":
    build(ROOT)
