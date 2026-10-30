#!/usr/bin/env python3
"""Build the static parts of the Pedagogy Compass page from pedagogy-compass-59ecb8db/compass-en.json.

The page is for Skool members only. It is reached through a hidden link, has
noindex (HIDDEN_PATHS in scripts/build-seo-meta.py) and is never linked from
the rest of the site.

Replaces the content between these marker pairs in pedagogy-compass-59ecb8db/index.html:
  <!-- problems:start --> / <!-- problems:end -->  the ten problem cards
  <!-- data:start -->     / <!-- data:end -->      problems and models as JSON for the prompt builder
  <!-- map:start -->      / <!-- map:end -->       categories A–E with their model cards
  <!-- recipes:start -->  / <!-- recipes:end -->   the three combination recipes
  <!-- myths:start -->    / <!-- myths:end -->     category F, the myth check
  <!-- legend:start -->   / <!-- legend:end -->    the label legend
  <!-- age:start -->      / <!-- age:end -->       AI tools and age rules

Running it twice gives the same file. The prompt text lives in
assets/js/pedagogy-compass.js, not in the JSON.

Usage:
    /usr/bin/python3 scripts/build-pedagogy-compass.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "pedagogy-compass-59ecb8db"


def _chip(label: str, labels: dict) -> str:
    return f'<span class="tm-chip tm-chip--{escape(label)}">{escape(labels[label]["name"])}</span>'


def _model_link(m: dict, labels: dict) -> str:
    return f'<li><a href="#model-{escape(m["id"])}">{escape(m["name"])}</a> {_chip(m["category"], labels)}</li>'


def render_problem(p: dict, models: dict, labels: dict) -> str:
    """One problem: what it looks like and the models that address it, strongest first."""
    links = "".join(_model_link(models[mid], labels) for mid in p["model_ids"])
    return (
        f'<article class="tm-move pc-problem" id="problem-{escape(p["id"])}">\n'
        f'  <h3 class="tm-move__name">{escape(p["name"])}</h3>\n'
        f'  <p class="tm-move__line">{escape(p["what_it_looks_like"])}</p>\n'
        f'  <p class="pc-label">What helps, strongest evidence first</p><ol class="pc-models">{links}</ol>\n'
        f'  <a class="tm-move__use" href="?problem={escape(p["id"])}#pc-builder" data-use-problem="{escape(p["id"])}" '
        f'aria-label="Use in the prompt: {escape(p["name"])}">Use in the prompt</a>\n'
        f"</article>"
    )


def render_data(data: dict) -> str:
    """What the prompt builder needs, as JSON. Escapes < so the text can never
    close the script tag."""
    labels = data["labels"]
    slim = {
        "problems": [{"id": p["id"], "name": p["name"], "model_ids": p["model_ids"]} for p in data["problems"]],
        "models": [{"id": m["id"], "name": m["name"], "label": labels[m["category"]]["name"],
                    "one_liner": m.get("one_liner", "")} for m in data["models"]],
    }
    text = json.dumps(slim, ensure_ascii=False).replace("<", "\\u003c")
    return f'<script type="application/json" id="pc-data">{text}</script>'


def render_model_card(m: dict, labels: dict) -> str:
    """One model as a folded card: one-liner first, the rest on opening."""
    sources = ", ".join(f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' for s in m.get("sources", []))
    return (
        f'<details class="pc-card" id="model-{escape(m["id"])}">'
        f'<summary><span class="pc-card__name">{escape(m["name"])}</span> {_chip(m["category"], labels)}'
        f'<span class="pc-card__line">{escape(m.get("one_liner", ""))}</span></summary>'
        f'<p class="pc-card__origin">{escape(m["origin"])}</p>'
        f'<dl class="pc-card__body">'
        f'<dt>On an ordinary Tuesday</dt><dd>{escape(m.get("tuesday", ""))}</dd>'
        f'<dt>Where AI helps</dt><dd>{escape(m.get("ai_helps", ""))}</dd>'
        f'<dt>Where AI gets in the way</dt><dd>{escape(m.get("ai_harms", ""))}</dd>'
        f'<dt>The evidence</dt><dd>{escape(m.get("evidence", ""))}</dd>'
        f"</dl>"
        f'<p class="tm-move__sources">Source: {sources}</p>'
        f"</details>"
    )


def render_map(data: dict) -> str:
    """Categories A–E, each with its model cards. F has its own section."""
    out = []
    for c in data["categories"]:
        if c["id"] == "contested":
            continue
        cards = "\n".join(render_model_card(m, data["labels"]) for m in data["models"] if m["category"] == c["id"])
        out.append(
            f'<div class="pc-category" id="category-{escape(c["id"])}">'
            f'<h3 class="pc-category__title"><span class="pc-letter">{escape(c["letter"])}</span> {escape(c["name"])} '
            f'{_chip(c["label"], data["labels"])}</h3>'
            f'<p class="pc-category__q">{escape(c["question"])}</p>'
            f'<div class="pc-cards">\n{cards}\n</div></div>'
        )
    return "\n".join(out)


def render_recipe(r: dict, models: dict, labels: dict) -> str:
    links = "".join(_model_link(models[mid], labels) for mid in r["model_ids"])
    steps = "".join(f"<li>{escape(s)}</li>" for s in r["steps"])
    return (
        f'<article class="tm-move pc-recipe" id="recipe-{escape(r["id"])}">'
        f'<h3 class="tm-move__name">{escape(r["name"])}</h3>'
        f'<ul class="pc-models pc-models--inline">{links}</ul>'
        f'<ol class="pc-steps">{steps}</ol>'
        f"</article>"
    )


def render_legend(labels: dict) -> str:
    rows = "".join(f'<li>{_chip(k, labels)} {escape(v["definition"])}</li>' for k, v in labels.items())
    return f'<ul class="tm-legend">{rows}</ul>'


def render_age(rules: list) -> str:
    rows = "".join(f"<li><strong>{escape(r['tool'])}:</strong> {escape(r['rule'])}</li>" for r in rules)
    return f'<ul class="tm-age">{rows}</ul>'


def _inject(html: str, name: str, content: str) -> str:
    pattern = re.compile(rf"(<!--\s*{name}:start\s*-->)(.*?)(<!--\s*{name}:end\s*-->)", re.S)
    if not pattern.search(html):
        raise ValueError(f"Missing <!-- {name}:start --> / <!-- {name}:end --> markers")
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(3)}", html)


def build(root: Path) -> None:
    data = json.loads((root / SLUG / "compass-en.json").read_text(encoding="utf-8"))
    page = root / SLUG / "index.html"
    html = page.read_text(encoding="utf-8")
    models = {m["id"]: m for m in data["models"]}
    labels = data["labels"]
    html = _inject(html, "problems", "\n".join(render_problem(p, models, labels) for p in data["problems"]))
    html = _inject(html, "data", render_data(data))
    html = _inject(html, "map", render_map(data))
    html = _inject(html, "recipes", "\n".join(render_recipe(r, models, labels) for r in data["recipes"]))
    html = _inject(html, "myths", "\n".join(render_model_card(m, labels) for m in data["models"] if m["category"] == "contested"))
    html = _inject(html, "legend", render_legend(labels))
    html = _inject(html, "age", render_age(data["age_rules"]))
    page.write_text(html, encoding="utf-8")
    print(f"Built {len(data['problems'])} problems and {len(data['models'])} models into {page.relative_to(root)}")


if __name__ == "__main__":
    build(ROOT)
