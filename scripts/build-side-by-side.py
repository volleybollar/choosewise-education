#!/usr/bin/env python3
"""Build the static parts of /side-by-side/ from side-by-side/pairs-en.json.

Replaces the content between these marker pairs in side-by-side/index.html:
  <!-- pairs:start -->    / <!-- pairs:end -->     the five pair-type cards
  <!-- legend:start -->   / <!-- legend:end -->    the evidence label legend
  <!-- evidence:start --> / <!-- evidence:end -->  the evidence claims and the context
  <!-- sources:start -->  / <!-- sources:end -->   every source once
  <!-- age:start -->      / <!-- age:end -->       AI tools and age rules
  <!-- variant:start -->  / <!-- variant:end -->   the upper-secondary variant

The age rules come from thinking-moves/moves-en.json, so the Think + AI pages
always show the same rules. Running it twice gives the same file. The prompt
builder reads the same JSON in the browser (assets/js/side-by-side.js).

Usage:
    /usr/bin/python3 scripts/build-side-by-side.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EASIER_ONLY = "Easier to see only: AI tools could not build this pair reliably at the harder level."
COLUMNS = [("only_a", "Only A"), ("both", "Both"), ("only_b", "Only B")]
KEY_PARTS = [("rule", "The rule"), ("case_c", "Case C"), ("case_c_answer", "Case C answer"),
             ("probe", "Probe"), ("think_back", "Think back")]


def _lines(text: str) -> str:
    """Line breaks in A and B (worked solutions) are kept as <br>."""
    return "<br>".join(escape(line) for line in text.splitlines())


def _item(letter: str, label: str, text: str) -> str:
    return (f'<div class="sb-item"><p class="sb-item__label">{letter} · {escape(label)}</p>'
            f"<p>{_lines(text)}</p></div>")


def _example_html(ex: dict, levels: list) -> str:
    level = {lv["id"]: lv["name"] for lv in levels}[ex["level"]]
    columns = "".join(f'<div class="sb-col"><h5>{heading}</h5><p>{escape(ex[key])}</p></div>'
                      for key, heading in COLUMNS)
    rows = "".join(f"<dt>{label}</dt><dd>{escape(ex[key])}</dd>" for key, label in KEY_PARTS)
    return (
        f'<div class="tm-example sb-example">'
        f'<h4 class="tm-example__subject">{escape(ex["subject"])} <span>· Grade {int(ex["grade"])} · {escape(level)}</span></h4>'
        f'<p class="sb-task"><strong>Task:</strong> {escape(ex["task"])}</p>'
        f'<div class="sb-ab">{_item("A", ex["a_label"], ex["a"])}{_item("B", ex["b_label"], ex["b"])}</div>'
        f'<p class="sb-key__title">Teacher\'s key</p>'
        f'<div class="sb-key">{columns}</div>'
        f"<dl>{rows}</dl>"
        f"</div>"
    )


def render_pair_card(pair: dict, levels: list, labels: dict) -> str:
    """One pair type as an <article>. All JSON text is HTML-escaped."""
    pid = escape(pair["id"])
    look_for = "".join(f"<li>{escape(s)}</li>" for s in pair["look_for"])
    easier_only = "" if pair["harder_ok"] else f'  <p class="sb-pair__only">{EASIER_ONLY}</p>\n'
    label = escape(pair["label"])
    return (
        f'<article class="tm-move sb-pair" id="{pid}" data-pair-id="{pid}">\n'
        f'  <div class="tm-move__head">'
        f'<img class="tm-move__icon" src="/side-by-side/icons/{pid}.svg" alt="" width="48" height="48">'
        f'<div><span class="tm-move__num">Pair {int(pair["number"])}</span>'
        f'<h3 class="tm-move__name">{escape(pair["name"])}</h3></div></div>\n'
        f'  <p class="tm-move__line">{escape(pair["one_liner"])}</p>\n'
        f'  <p class="tm-move__meta"><span class="tm-chip tm-chip--{label}">{escape(labels[pair["label"]]["name"])}</span></p>\n'
        f'  <p class="sb-pair__look-title">What to look for</p>\n'
        f'  <ul class="sb-pair__look">{look_for}</ul>\n'
        f"{easier_only}"
        f'  <details class="tm-move__more"><summary>Worked example with the teacher\'s key</summary>'
        f"{_example_html(pair['example'], levels)}"
        f"</details>\n"
        f'  <a class="tm-move__use" href="?pair={pid}#sb-builder" data-use-pair="{pid}" '
        f'aria-label="Use this pair: {escape(pair["name"])}">Use this pair</a>\n'
        f"</article>"
    )


def render_legend(labels: dict) -> str:
    rows = "".join(
        f'<li><span class="tm-chip tm-chip--{key}">{escape(labels[key]["name"])}</span> {escape(labels[key]["definition"])}</li>'
        for key in labels if key != "note"
    )
    return f'<ul class="tm-legend">{rows}</ul>\n<p class="tm-legend__note">{escape(labels["note"])}</p>'


def _source_links(sources: list) -> str:
    return ", ".join(f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' for s in sources)


def render_evidence(evidence: list, context: dict, labels: dict) -> str:
    """Each claim with its label, then the context paragraph (not evidence for the tool)."""
    rows = "".join(
        f'<li><span class="tm-chip tm-chip--{escape(e["label"])}">{escape(labels[e["label"]]["name"])}</span> '
        f'<strong>{escape(e["claim"])}.</strong> {escape(e["text"])}'
        f' <span class="tm-move__sources">Source: {_source_links(e["sources"])}</span></li>'
        for e in evidence
    )
    return (
        f'<ul class="sb-evidence">{rows}</ul>\n'
        f'<p class="sb-context"><strong>In the classroom.</strong> {escape(context["text"])}</p>'
    )


def render_sources(evidence: list, context: dict) -> str:
    """Every source once, in the order it first appears."""
    seen = {}
    for s in [s for e in evidence for s in e["sources"]] + context["sources"]:
        seen.setdefault(s["url"], s["text"])
    rows = "".join(f'<li><a href="{escape(url)}">{escape(text)}</a></li>' for url, text in seen.items())
    return f'<ul class="tm-sources">{rows}</ul>'


def render_age(rules: list) -> str:
    rows = "".join(f"<li><strong>{escape(r['tool'])}:</strong> {escape(r['rule'])}</li>" for r in rules)
    return f'<ul class="tm-age">{rows}</ul>'


def render_variant(variant: dict) -> str:
    """Intro, steps and the student prompt with its own Copy button."""
    steps = "".join(f"<li>{escape(s)}</li>" for s in variant["steps"])
    prompt = escape(variant["student_prompt"])
    return (
        f'<p class="section__lede">{escape(variant["intro"])}</p>\n'
        f'<ol class="sb-variant__steps">{steps}</ol>\n'
        f'<label class="tm-field tm-field--wide"><span class="tm-field__label">Student prompt</span>'
        f'<textarea class="input tm-prompt" id="sb-variant-prompt" rows="8" readonly>{prompt}</textarea></label>\n'
        f'<div class="tm-copy-row"><button type="button" class="btn btn--primary" id="sb-variant-copy" data-copy="{prompt}">Copy student prompt</button>'
        f'<span class="copy-toast" role="status">Copied</span></div>'
    )


def _inject(html: str, name: str, content: str) -> str:
    pattern = re.compile(rf"(<!--\s*{name}:start\s*-->)(.*?)(<!--\s*{name}:end\s*-->)", re.S)
    if not pattern.search(html):
        raise ValueError(f"Missing <!-- {name}:start --> / <!-- {name}:end --> markers")
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(3)}", html)


def build(root: Path) -> None:
    data = json.loads((root / "side-by-side/pairs-en.json").read_text(encoding="utf-8"))
    age_rules = json.loads((root / "thinking-moves/moves-en.json").read_text(encoding="utf-8"))["age_rules"]
    page = root / "side-by-side/index.html"
    html = page.read_text(encoding="utf-8")
    html = _inject(html, "pairs", "\n".join(render_pair_card(p, data["levels"], data["labels"]) for p in data["pairs"]))
    html = _inject(html, "legend", render_legend(data["labels"]))
    html = _inject(html, "evidence", render_evidence(data["evidence"], data["context"], data["labels"]))
    html = _inject(html, "sources", render_sources(data["evidence"], data["context"]))
    html = _inject(html, "age", render_age(age_rules))
    html = _inject(html, "variant", render_variant(data["variant"]))
    page.write_text(html, encoding="utf-8")
    print(f"Built {len(data['pairs'])} pair types into {page.relative_to(root)}")


if __name__ == "__main__":
    build(ROOT)
