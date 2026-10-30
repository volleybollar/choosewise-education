#!/usr/bin/env python3
"""Build the static parts of /two-minute-debrief/ from two-minute-debrief/debrief-en.json.

Replaces the content between these marker pairs in two-minute-debrief/index.html:
  <!-- hero-example:start -->   / <!-- hero-example:end -->    the hero debrief and its reply
  <!-- examples:start -->       / <!-- examples:end -->        the four worked debriefs
  <!-- rollup-example:start --> / <!-- rollup-example:end -->  the weekly roll-up example
  <!-- exit-tickets:start -->   / <!-- exit-tickets:end -->    the four exit ticket templates
  <!-- journal:start -->        / <!-- journal:end -->         the example unit journal
  <!-- legend:start -->         / <!-- legend:end -->          the evidence label legend
  <!-- sources:start -->        / <!-- sources:end -->         the approaches and their sources
  <!-- age:start -->            / <!-- age:end -->             AI tools and age rules

Running it twice gives the same file. The prompt text lives in
assets/js/two-minute-debrief.js, not in the JSON.

Usage:
    /usr/bin/python3 scripts/build-two-minute-debrief.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Rubrikerna i AI:ns svar, i den ordning prompten ber om dem.
REPLY_PARTS = [("likely_causes", "Likely causes"), ("next_lesson", "Next lesson"),
               ("check_first", "Check first"), ("one_question", "One question")]
ROLLUP_PARTS = [("patterns", "Patterns"), ("what_worked", "What worked"),
                ("one_change", "One change for next week"), ("one_question", "One question")]


def render_example(ex: dict, heading: str = "h4") -> str:
    """One debrief (the teacher's four answers) and the AI's four-part reply.

    heading is h3 in the hero (under an h2) and h4 in the examples (under an h3)."""
    answers = "".join(
        f'<dt>{label}</dt><dd class="td-text">{escape(ex[key])}</dd>'
        for key, label in (("goal", "Goal"), ("evidence", "Evidence"), ("surprise", "Surprise"), ("next", "Next"))
    )
    reply = "".join(
        f'<dt>{label}</dt><dd class="td-text">{escape(ex["reply"][key])}</dd>' for key, label in REPLY_PARTS
    )
    return (
        f'<div class="tm-example td-example">'
        f'<{heading} class="tm-example__subject">{escape(ex["group"])} <span>· Grade {int(ex["grade"])}</span></{heading}>'
        f'<div class="td-example__cols">'
        f'<div><p class="td-example__label">The teacher writes</p><dl>{answers}</dl></div>'
        f'<div><p class="td-example__label">The AI replies</p><dl>{reply}</dl></div>'
        f"</div>"
        f"</div>"
    )


def render_examples(examples: list) -> str:
    """The four worked debriefs, each folded under its title."""
    return "\n".join(
        f'<details class="tm-move__more td-more"><summary>{escape(ex["title"])}'
        f' <span class="td-more__meta">· {escape(ex["group"])}, Grade {int(ex["grade"])}</span></summary>'
        f"{render_example(ex)}</details>"
        for ex in examples
    )


def render_rollup_example(rx: dict) -> str:
    """A week of saved debriefs and the roll-up reply."""
    rows = "".join(
        f'<li><span class="td-date">{escape(d["date"])}</span> <strong>{escape(d["group"])}</strong> '
        f'<span class="td-small">Goal: {escape(d["goal"])} Evidence: {escape(d["evidence"])} '
        f'Surprise: {escape(d["surprise"])} Next: {escape(d["next"])}</span></li>'
        for d in rx["debriefs"]
    )
    reply = "".join(
        f'<dt>{label}</dt><dd class="td-text">{escape(rx["reply"][key])}</dd>' for key, label in ROLLUP_PARTS
    )
    return (
        f'<div class="tm-example td-example">'
        f'<h3 class="tm-example__subject">A week of debriefs <span>· four lessons</span></h3>'
        f'<ul class="td-list">{rows}</ul>'
        f'<p class="td-example__label">The AI replies</p><dl>{reply}</dl>'
        f"</div>"
    )


def render_exit_ticket(t: dict) -> str:
    """One exit ticket: when to use it, the text for students and the setup steps."""
    forms = "".join(f"<li>{escape(s)}</li>" for s in t["forms_steps"])
    google = "".join(f"<li>{escape(s)}</li>" for s in t["google_steps"])
    return (
        f'<article class="tm-move td-ticket" id="ticket-{escape(t["id"])}">\n'
        f'  <h3 class="tm-move__name">{escape(t["name"])}</h3>\n'
        f'  <p class="tm-move__line">{escape(t["when"])}</p>\n'
        f'  <p class="td-ticket__text td-text">{escape(t["student_text"])}</p>\n'
        f'  <details class="tm-move__more"><summary>Set it up in Microsoft Forms</summary><ol class="td-steps">{forms}</ol></details>\n'
        f'  <details class="tm-move__more"><summary>Set it up in Google Forms</summary><ol class="td-steps">{google}</ol></details>\n'
        f'  <p class="tm-note">{escape(t["paper_note"])}</p>\n'
        f"</article>"
    )


def render_journal_example(rows: list) -> str:
    """The example unit journal as a list (a table with eight columns does not
    fit on a phone)."""
    items = "".join(
        f'<li><span class="td-date">{escape(r["date"])}</span> <strong>{escape(r["goal"])}</strong> '
        f'<span class="td-small">Change: {escape(r["change"])} · Check: {escape(r["check"])}</span></li>'
        for r in rows
    )
    return f'<ul class="td-list">{items}</ul>'


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
            f'<div class="td-approach">'
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
    data = json.loads((root / "two-minute-debrief/debrief-en.json").read_text(encoding="utf-8"))
    page = root / "two-minute-debrief/index.html"
    html = page.read_text(encoding="utf-8")
    hero = next(e for e in data["examples"] if e["id"] == data["hero_example"])
    html = _inject(html, "hero-example", render_example(hero, heading="h3"))
    html = _inject(html, "examples", render_examples(data["examples"]))
    html = _inject(html, "rollup-example", render_rollup_example(data["rollup_example"]))
    html = _inject(html, "exit-tickets", "\n".join(render_exit_ticket(t) for t in data["exit_tickets"]))
    html = _inject(html, "journal", render_journal_example(data["journal_example"]))
    html = _inject(html, "legend", render_legend(data["labels"]))
    html = _inject(html, "sources", render_approaches(data["approaches"], data["labels"]))
    html = _inject(html, "age", render_age(data["age_rules"]))
    page.write_text(html, encoding="utf-8")
    print(f"Built {len(data['examples'])} examples and {len(data['exit_tickets'])} exit tickets into {page.relative_to(root)}")


if __name__ == "__main__":
    build(ROOT)
