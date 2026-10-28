#!/usr/bin/env python3
"""Build the static parts of /flawed-answer/ from flawed-answer/flaws-en.json.

Replaces the content between these marker pairs in flawed-answer/index.html:
  <!-- flaws:start -->    / <!-- flaws:end -->     the six flaw-type cards
  <!-- legend:start -->   / <!-- legend:end -->    the evidence label legend
  <!-- evidence:start --> / <!-- evidence:end -->  the evidence claims and the context
  <!-- sources:start -->  / <!-- sources:end -->   every source once
  <!-- age:start -->      / <!-- age:end -->       AI tools and age rules
  <!-- variant:start -->  / <!-- variant:end -->   the upper-secondary variant

The age rules come from thinking-moves/moves-en.json, so the two pages
always show the same rules. Running it twice gives the same file. The prompt
builder reads the same JSON in the browser (assets/js/flawed-answer.js).

Usage:
    /usr/bin/python3 scripts/build-flawed-answer.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EASIER_ONLY = "Easier to spot only: AI tools could not plant this flaw reliably at the harder level."
KEY_PARTS = [("flaw", "The flaw"), ("fix", "Fix"), ("why_convincing", "Why it convinces"),
             ("test_it", "Test it"), ("probe", "Probe"), ("think_back", "Think back")]


def _example_html(ex: dict, levels: list) -> str:
    level = {lv["id"]: lv["name"] for lv in levels}[ex["level"]]
    rows = "".join(f"<dt>{label}</dt><dd>{escape(ex[key])}</dd>" for key, label in KEY_PARTS)
    return (
        f'<div class="tm-example">'
        f'<h4 class="tm-example__subject">{escape(ex["subject"])} <span>· Grade {int(ex["grade"])} · {escape(level)}</span></h4>'
        f'<p class="fa-question"><strong>Question:</strong> {escape(ex["question"])}</p>'
        f'<blockquote class="fa-answer"><p class="fa-answer__label">AI-generated answer</p>'
        f'<p>{escape(ex["answer"])}</p></blockquote>'
        f"<dl>{rows}</dl>"
        f"</div>"
    )


def render_flaw_card(flaw: dict, levels: list) -> str:
    """One flaw type as an <article>. All JSON text is HTML-escaped."""
    fid = escape(flaw["id"])
    signs = "".join(f"<li>{escape(s)}</li>" for s in flaw["telltale_signs"])
    easier_only = "" if flaw["harder_ok"] else f'  <p class="fa-flaw__only">{EASIER_ONLY}</p>\n'
    return (
        f'<article class="tm-move fa-flaw" id="{fid}" data-flaw-id="{fid}">\n'
        f'  <div class="tm-move__head">'
        f'<img class="tm-move__icon" src="/flawed-answer/icons/{fid}.svg" alt="" width="48" height="48">'
        f'<div><span class="tm-move__num">Flaw {int(flaw["number"])}</span>'
        f'<h3 class="tm-move__name">{escape(flaw["name"])}</h3></div></div>\n'
        f'  <p class="tm-move__line">{escape(flaw["one_liner"])}</p>\n'
        f'  <p class="fa-flaw__signs-title">Telltale signs</p>\n'
        f'  <ul class="fa-flaw__signs">{signs}</ul>\n'
        f"{easier_only}"
        f'  <details class="tm-move__more"><summary>Worked example with the teacher\'s key</summary>'
        f"{_example_html(flaw['example'], levels)}"
        f"</details>\n"
        f'  <a class="tm-move__use" href="?flaw={fid}#fa-builder" data-use-flaw="{fid}" '
        f'aria-label="Use this flaw: {escape(flaw["name"])}">Use this flaw</a>\n'
        f"</article>"
    )


def render_legend(labels: dict) -> str:
    rows = "".join(
        f'<li><span class="tm-chip fa-chip--{key}">{escape(labels[key]["name"])}</span> {escape(labels[key]["definition"])}</li>'
        for key in ("strong", "thin")
    )
    return f'<ul class="tm-legend">{rows}</ul>\n<p class="tm-legend__note">{escape(labels["note"])}</p>'


def _source_links(sources: list) -> str:
    return ", ".join(f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' for s in sources)


def render_evidence(evidence: list, context: dict, labels: dict) -> str:
    """Each claim with its label, then the context paragraph (not evidence for the tool)."""
    rows = "".join(
        f'<li><span class="tm-chip fa-chip--{escape(e["label"])}">{escape(labels[e["label"]]["name"])}</span> '
        f'<strong>{escape(e["claim"])}.</strong> {escape(e["text"])}'
        + (f' <span class="tm-move__sources">Source: {_source_links(e["sources"])}</span>' if e["sources"] else "")
        + "</li>"
        for e in evidence
    )
    return (
        f'<ul class="fa-evidence">{rows}</ul>\n'
        f'<p class="fa-context"><strong>Why it matters now.</strong> {escape(context["text"])}</p>'
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
        f'<ol class="fa-variant__steps">{steps}</ol>\n'
        f'<label class="tm-field tm-field--wide"><span class="tm-field__label">Student prompt</span>'
        f'<textarea class="input tm-prompt" id="fa-variant-prompt" rows="6" readonly>{prompt}</textarea></label>\n'
        f'<div class="tm-copy-row"><button type="button" class="btn btn--primary" id="fa-variant-copy" data-copy="{prompt}">Copy student prompt</button>'
        f'<span class="copy-toast" role="status">Copied</span></div>'
    )


def _inject(html: str, name: str, content: str) -> str:
    pattern = re.compile(rf"(<!--\s*{name}:start\s*-->)(.*?)(<!--\s*{name}:end\s*-->)", re.S)
    if not pattern.search(html):
        raise ValueError(f"Missing <!-- {name}:start --> / <!-- {name}:end --> markers")
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(3)}", html)


def build(root: Path) -> None:
    data = json.loads((root / "flawed-answer/flaws-en.json").read_text(encoding="utf-8"))
    age_rules = json.loads((root / "thinking-moves/moves-en.json").read_text(encoding="utf-8"))["age_rules"]
    page = root / "flawed-answer/index.html"
    html = page.read_text(encoding="utf-8")
    html = _inject(html, "flaws", "\n".join(render_flaw_card(f, data["levels"]) for f in data["flaws"]))
    html = _inject(html, "legend", render_legend(data["labels"]))
    html = _inject(html, "evidence", render_evidence(data["evidence"], data["context"], data["labels"]))
    html = _inject(html, "sources", render_sources(data["evidence"], data["context"]))
    html = _inject(html, "age", render_age(age_rules))
    html = _inject(html, "variant", render_variant(data["variant"]))
    page.write_text(html, encoding="utf-8")
    print(f"Built {len(data['flaws'])} flaw types into {page.relative_to(root)}")


if __name__ == "__main__":
    build(ROOT)
