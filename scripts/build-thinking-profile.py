#!/usr/bin/env python3
"""Build the static parts of /thinking-profile/ from thinking-profile/ladders-en.json.

Replaces the content between these marker pairs in thinking-profile/index.html:
  <!-- why:start -->      / <!-- why:end -->       the intro: what it is, why a whole unit, the teacher quote
  <!-- ladders:start -->  / <!-- ladders:end -->   the six ladder cards
  <!-- notgraded:start --> / <!-- notgraded:end --> the "never graded" sentence (inline)
  <!-- honesty:start -->  / <!-- honesty:end -->   the honesty sentence about the ladders (inline)
  <!-- example:start -->  / <!-- example:end -->   the worked unit (Biology, Grade 8)
  <!-- legend:start -->   / <!-- legend:end -->    the evidence label legend
  <!-- evidence:start --> / <!-- evidence:end -->  the evidence claims
  <!-- sources:start -->  / <!-- sources:end -->   every source once
  <!-- age:start -->      / <!-- age:end -->       AI tools and age rules

Cluster names and descriptions, move names, evidence labels and age rules come
from thinking-moves/moves-en.json; pair names from side-by-side/pairs-en.json,
so the Think + AI pages never disagree. Running it twice gives the same file.

Usage:
    /usr/bin/python3 scripts/build-thinking-profile.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Verktyg utan eget uppgifts-id: namnet är verktygets.
TOOL_NAMES = {"flawed-answer": "Flawed Answer", "side-by-side": "Side by Side"}


def _task_name(task: dict, names: dict) -> str:
    """Name of a task entry {tool, id?}: the move or pair name, else the tool name."""
    return names[task["id"]] if "id" in task else TOOL_NAMES[task["tool"]]


def render_ladder_card(ladder: dict, cluster: dict, moves: dict, pairs: dict) -> str:
    """One ladder as an <article>. `moves` and `pairs` map id to name. All JSON text is escaped."""
    cid = escape(ladder["cluster"])
    names = {**moves, **pairs}
    steps = "".join(f"<li>{escape(s['text'])}</li>" for s in ladder["steps"])
    trained = ", ".join(escape(_task_name(t, names)) for t in ladder["tasks"])
    return (
        f'<article class="tm-move tp-ladder" id="{cid}" data-cluster="{cid}">\n'
        f'  <div class="tm-move__head">'
        f'<img class="tm-move__icon" src="{escape(ladder["icon"])}" alt="" width="48" height="48">'
        f'<div><h3 class="tm-move__name">{escape(cluster["name"])}</h3></div></div>\n'
        f'  <p class="tm-move__line">{escape(cluster["description"])}</p>\n'
        f'  <p class="tp-card__label">The four steps</p>\n'
        f'  <ol class="tp-steps">{steps}</ol>\n'
        f'  <p class="tp-trained"><strong>Trained by:</strong> {trained}</p>\n'
        f'  <a class="tm-move__use" href="?cluster={cid}#tp-builder" data-use-cluster="{cid}" '
        f'aria-label="Plan with this ladder: {escape(cluster["name"])}">Plan with this ladder</a>\n'
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


def render_evidence(evidence: list, labels: dict) -> str:
    rows = "".join(
        f'<li><span class="tm-chip tm-chip--{escape(e["label"])}">{escape(labels[e["label"]]["name"])}</span> '
        f'<strong>{escape(e["claim"])}.</strong> {escape(e["text"])}'
        f' <span class="tm-move__sources">Source: {_source_links(e["sources"])}</span></li>'
        for e in evidence
    )
    return f'<ul class="tp-evidence">{rows}</ul>'


def render_sources(evidence: list) -> str:
    """Every source once, in the order it first appears."""
    seen = {}
    for e in evidence:
        for s in e["sources"]:
            seen.setdefault(s["url"], s["text"])
    rows = "".join(f'<li><a href="{escape(url)}">{escape(text)}</a></li>' for url, text in seen.items())
    return f'<ul class="tm-sources">{rows}</ul>'


def render_why(intro: dict) -> str:
    return (
        f'<p class="section__lede">{escape(intro["what"])}</p>\n'
        f'<p class="tm-note">{escape(intro["why_unit"])}</p>\n'
        f'<p class="tp-card__label">How you might retell it to a colleague:</p>\n'
        f'<blockquote class="tp-tell">{escape(intro["retell"])}</blockquote>'
    )


def render_age(rules: list) -> str:
    rows = "".join(f"<li><strong>{escape(r['tool'])}:</strong> {escape(r['rule'])}</li>" for r in rules)
    return f'<ul class="tm-age">{rows}</ul>'


def render_example(example: dict, names: dict | None = None) -> str:
    """The worked unit: thread, week-by-week plan with builder inputs, the sentence for students
    and two fictional student answers. `names` may hold {"clusters", "tasks"} id->name maps."""
    names = names or {}
    tasks = names.get("tasks", {})
    cluster = names.get("clusters", {}).get(example["cluster"], example["cluster"])

    def task_label(tool: str, task: str) -> str:
        name = tasks.get(task) or TOOL_NAMES.get(tool) or task
        # Side by Side-uppgifter visas som "Side by Side: parnamn" så att läsaren ser verktyget.
        return f"Side by Side: {name}" if tool == "side-by-side" and task in tasks else name

    plan = "".join(
        f'<li class="tp-plan__item">'
        f'<p class="tp-plan__week">Week {int(p["week"])} · {escape(task_label(p["tool"], p["task"]))} '
        f'<span>· room for step {int(p["step"])}</span></p>'
        f'<p>{escape(p["what"])}</p>'
        f'<details class="tp-plan__inputs"><summary>What to enter in the builder</summary>'
        f'<ul>{"".join(f"<li>{escape(i)}</li>" for i in p["inputs"])}</ul>'
        f'<a class="tm-move__use" href="{escape(p["url"])}">Open this task in its builder</a></details>'
        f"</li>"
        for p in example["plan"]
    )
    students = "".join(
        f'<div class="tp-student"><h4>{escape(s["name"])} <span>· {escape(task_label("", s["task"]))} · '
        f'step {int(s["step"])}</span></h4>'
        f'<p class="tp-student__answer">{escape(s["answer"])}</p>'
        f'<dl><dt>What shows it</dt><dd>{escape(s["shows"])}</dd>'
        f'<dt>My next step</dt><dd>{escape(s["next"])}</dd></dl></div>'
        for s in example["students"]
    )
    return (
        f'<div class="tm-example tp-example">'
        f'<h3 class="tm-example__subject">{escape(example["subject"])} <span>· Grade {int(example["grade"])} · '
        f'{int(example["weeks"])} weeks · {escape(example["topic"])} · {escape(cluster)}</span></h3>'
        f'<p class="tp-thread">{escape(example["thread"])}</p></div>\n'
        f'<h3 class="tp-sub">The plan, week by week</h3>\n'
        f'<ol class="tp-plan">{plan}</ol>\n'
        f'<h3 class="tp-sub">What you say to students</h3>\n'
        f'<blockquote class="tp-tell">{escape(example["tell_students"])}</blockquote>\n'
        f'<h3 class="tp-sub">Two students, one task</h3>\n'
        f'<p class="tp-note">{escape(example["students_note"])}</p>\n'
        f'<div class="tp-students">{students}</div>'
    )


def _inject(html: str, name: str, content: str) -> str:
    pattern = re.compile(rf"(<!--\s*{name}:start\s*-->)(.*?)(<!--\s*{name}:end\s*-->)", re.S)
    if not pattern.search(html):
        raise ValueError(f"Missing <!-- {name}:start --> / <!-- {name}:end --> markers")
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(3)}", html)


def build(root: Path) -> None:
    data = json.loads((root / "thinking-profile/ladders-en.json").read_text(encoding="utf-8"))
    tm = json.loads((root / "thinking-moves/moves-en.json").read_text(encoding="utf-8"))
    sb = json.loads((root / "side-by-side/pairs-en.json").read_text(encoding="utf-8"))
    clusters = {c["id"]: c for c in tm["clusters"]}
    moves = {m["id"]: m["name"] for m in tm["moves"]}
    pairs = {p["id"]: p["name"] for p in sb["pairs"]}
    page = root / "thinking-profile/index.html"
    html = page.read_text(encoding="utf-8")
    cards = "\n".join(render_ladder_card(l, clusters[l["cluster"]], moves, pairs) for l in data["ladders"])
    html = _inject(html, "ladders", cards)
    html = _inject(html, "example", render_example(
        data["example"], {"clusters": {k: v["name"] for k, v in clusters.items()}, "tasks": {**moves, **pairs}}))
    html = _inject(html, "why", render_why(data["intro"]))
    html = _inject(html, "notgraded", escape(data["not_graded"]))
    html = _inject(html, "honesty", escape(data["honesty"]))
    html = _inject(html, "legend", render_legend(tm["labels"]))
    html = _inject(html, "evidence", render_evidence(data["evidence"], tm["labels"]))
    html = _inject(html, "sources", render_sources(data["evidence"]))
    html = _inject(html, "age", render_age(tm["age_rules"]))
    page.write_text(html, encoding="utf-8")
    print(f"Built {len(data['ladders'])} ladders into {page.relative_to(root)}")


if __name__ == "__main__":
    build(ROOT)
