#!/usr/bin/env python3
"""Build the static parts of the Unit Studio page from unit-studio-541ebd12/studio-en.json.

The page is for Skool members only. It is reached through a hidden link, has
noindex (HIDDEN_PATHS in scripts/build-seo-meta.py) and is never linked from
the rest of the site.

Replaces the content between these marker pairs in unit-studio-541ebd12/index.html:
  <!-- hero-example:start -->  / <!-- hero-example:end -->   the example unit and the step 4 reply
  <!-- data:start -->          / <!-- data:end -->           the steps as JSON for the prompt builder
  <!-- steps:start -->         / <!-- steps:end -->          the five step cards
  <!-- final-example:start --> / <!-- final-example:end -->  the example final plan
  <!-- legend:start -->        / <!-- legend:end -->         the evidence label legend
  <!-- sources:start -->       / <!-- sources:end -->        every approach and its sources
  <!-- age:start -->           / <!-- age:end -->            AI tools and age rules

Running it twice gives the same file. The prompt text lives in
assets/js/unit-studio.js, not in the JSON.

Usage:
    /usr/bin/python3 scripts/build-unit-studio.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "unit-studio-541ebd12"

STEP4_PARTS = [("keep", "Keep"), ("suggest", "Suggest"), ("question", "Question"), ("ai_can_also", "AI can also")]
FINAL_PARTS = [("goal_and_evidence", "Goal and evidence"), ("prior_knowledge", "Prior knowledge"),
               ("lessons", "Lessons"), ("retrieval", "Retrieval"), ("checkpoints", "Checkpoints"),
               ("ai_use", "AI use"), ("changes", "Changes"), ("check", "Check")]


def _dl(pairs) -> str:
    return "<dl>" + "".join(f'<dt>{label}</dt><dd class="us-text">{escape(text)}</dd>' for label, text in pairs) + "</dl>"


def render_hero_example(ex: dict) -> str:
    """The teacher's original unit next to the AI's reply to step 4."""
    reply = _dl((label, ex["step4_reply"][key]) for key, label in STEP4_PARTS)
    return (
        '<div class="tm-example us-example">'
        f'<h3 class="tm-example__subject">{escape(ex["title"])} <span>· Grade {int(ex["grade"])} {escape(ex["subject"].lower())}, '
        f'{int(ex["weeks"])} weeks</span></h3>'
        '<div class="us-example__cols">'
        f'<div><p class="us-example__label">The unit as planned</p><p class="us-text">{escape(ex["unit_text"])}</p></div>'
        f'<div><p class="us-example__label">Step 4: retrieval and checkpoints</p>{reply}</div>'
        "</div></div>"
    )


def render_data(steps: list) -> str:
    """The steps the prompt builder needs, as JSON. Escapes < so the text can
    never close the script tag."""
    slim = [{"num": s["num"], "id": s["id"], "name": s["name"], "brief": s["brief"]} for s in steps]
    text = json.dumps({"steps": slim}, ensure_ascii=False).replace("<", "\\u003c")
    return f'<script type="application/json" id="us-data">{text}</script>'


def render_step_card(step: dict, approaches: dict, labels: dict) -> str:
    """One step: what to look for, why, and the evidence behind it."""
    questions = "".join(f"<li>{escape(q)}</li>" for q in step["look_for"])
    evidence = "".join(
        f'<p class="us-step__evidence"><strong>{escape(approaches[aid]["name"])}</strong> '
        f'<span class="tm-chip tm-chip--{escape(approaches[aid]["label"])}">{escape(labels[approaches[aid]["label"]]["name"])}</span></p>'
        for aid in step["approach_ids"]
    )
    return (
        f'<article class="tm-move us-step" id="step-{escape(step["id"])}">\n'
        f'  <div class="tm-move__head"><div><span class="tm-move__num">Step {int(step["num"])}</span>'
        f'<h3 class="tm-move__name">{escape(step["name"])}</h3></div></div>\n'
        f'  <p class="tm-move__line">{escape(step["why"])}</p>\n'
        f'  <p class="us-step__label">Look for</p><ul class="us-look">{questions}</ul>\n'
        f"  {evidence}\n"
        f'  <a class="tm-move__use" href="?step={int(step["num"])}#us-builder" data-use-step="{int(step["num"])}" '
        f'aria-label="Use step {int(step["num"])}: {escape(step["name"])}">Use this step</a>\n'
        f"</article>"
    )


def render_final_example(ex: dict) -> str:
    return (
        '<div class="tm-example us-example">'
        f'<h3 class="tm-example__subject">The improved plan <span>· {escape(ex["title"])}</span></h3>'
        + _dl((label, ex["final_plan"][key]) for key, label in FINAL_PARTS)
        + "</div>"
    )


def render_legend(labels: dict) -> str:
    rows = "".join(
        f'<li><span class="tm-chip tm-chip--{key}">{escape(labels[key]["name"])}</span> {escape(labels[key]["definition"])}</li>'
        for key in ("strong", "promising", "framework", "choosewise")
    )
    return f'<ul class="tm-legend">{rows}</ul>'


def render_approaches(approaches: list, labels: dict) -> str:
    out = []
    for a in approaches:
        sources = ", ".join(f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' for s in a["sources"])
        out.append(
            f'<div class="us-approach">'
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
    data = json.loads((root / SLUG / "studio-en.json").read_text(encoding="utf-8"))
    page = root / SLUG / "index.html"
    html = page.read_text(encoding="utf-8")
    approaches = {a["id"]: a for a in data["approaches"]}
    html = _inject(html, "hero-example", render_hero_example(data["example"]))
    html = _inject(html, "data", render_data(data["steps"]))
    html = _inject(html, "steps", "\n".join(render_step_card(s, approaches, data["labels"]) for s in data["steps"]))
    html = _inject(html, "final-example", render_final_example(data["example"]))
    html = _inject(html, "legend", render_legend(data["labels"]))
    html = _inject(html, "sources", render_approaches(data["approaches"], data["labels"]))
    html = _inject(html, "age", render_age(data["age_rules"]))
    page.write_text(html, encoding="utf-8")
    print(f"Built {len(data['steps'])} steps into {page.relative_to(root)}")


if __name__ == "__main__":
    build(ROOT)
