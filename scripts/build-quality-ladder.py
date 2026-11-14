#!/usr/bin/env python3
"""Build the static parts of the Quality Ladder page from quality-ladder-ec1c2f8c/ladder-en.json.

The page is for Skool members only. It is reached through a hidden link, has
noindex (HIDDEN_PATHS in scripts/build-seo-meta.py) and is never linked from
the rest of the site.

Replaces the content between these marker pairs in quality-ladder-ec1c2f8c/index.html:
  <!-- hero-example:start --> / <!-- hero-example:end -->  the worked example: task, criteria, samples A-C, teacher key
  <!-- routine:start -->      / <!-- routine:end -->       the student routine, the Grades 1-3 note, copy button, download
  <!-- whole-class:start -->  / <!-- whole-class:end -->   the whole-class feedback template, copy button, download
  <!-- policy:start -->       / <!-- policy:end -->        the one-page feedback policy, copy button, download
  <!-- colleagues:start -->   / <!-- colleagues:end -->    using the samples with colleagues
  <!-- evidence:start -->     / <!-- evidence:end -->      the label legend and the six research items
  <!-- care:start -->         / <!-- care:end -->          the four care points
  <!-- age:start -->          / <!-- age:end -->           AI tools and age rules

Running it twice gives the same file. The prompt text lives in
assets/js/quality-ladder.js, not in the JSON, so there is no JSON data block
in the page. The three *_text() functions give the plain text that the copy
buttons put on the clipboard (and that exports/build-quality-ladder-docx.py
reuses for the Word files).

Usage:
    /usr/bin/python3 scripts/build-quality-ladder.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "quality-ladder-ec1c2f8c"

# Teckenförklaringen listar etiketterna i den här ordningen.
LABEL_ORDER = ("strong", "promising", "framework", "choosewise")


# ───── Ren text: det som kopieringsknapparna lägger i urklipp ─────

def routine_text(routine: dict) -> str:
    """The routine as plain text: a title, the numbered steps, the Grades 1-3 note."""
    steps = "\n".join(f"{i}. {step}" for i, step in enumerate(routine["steps"], start=1))
    return f"The lesson, step by step\n\n{steps}\n\n{routine['younger']}"


def whole_class_text(wc: dict) -> str:
    """The whole-class feedback template: each heading with its guidance, then the follow-up."""
    parts = [f"{s['heading']}\n{s['guide']}" for s in wc["sections"]]
    return "Whole-class feedback\n\n" + "\n\n".join(parts) + f"\n\n{wc['followup']}"


def policy_text(policy: dict) -> str:
    """The feedback policy: the intro, then the numbered principles with their sources."""
    lines = []
    for i, p in enumerate(policy["principles"], start=1):
        source = f" ({p['source']})" if p["source"] else ""
        lines.append(f"{i}. {p['title']}: {p['text']}{source}")
    return policy["intro"] + "\n\n" + "\n".join(lines)


# ───── HTML ─────

def _source_links(sources: list) -> str:
    """'Source: a, b' as links. 'Sources:' when there is more than one."""
    links = ", ".join(f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' for s in sources)
    word = "Sources" if len(sources) > 1 else "Source"
    return f'<span class="tm-move__sources">{word}: {links}</span>'


def _copy_row(label: str, text: str) -> str:
    """A copy button with its 'Copied' toast. The toast must follow the button:
    copy-to-clipboard.js looks for it among the button's siblings."""
    return (
        '<div class="tm-copy-row">'
        f'<button type="button" class="btn btn--primary" data-copy="{escape(text)}">{escape(label)}</button>'
        '<span class="copy-toast" role="status">Copied</span>'
        "</div>"
    )


def _download(filename: str, label: str) -> str:
    return f'<p class="ql-download"><a href="{escape(filename)}" download>{escape(label)}</a></p>'


def render_example(data: dict) -> str:
    """The worked example. What students get (task, criteria, samples A-C) comes
    first; the teacher key, with the levels, is a separate block after it."""
    ex = data["example"]
    criteria = "".join(f"<li>{escape(c)}</li>" for c in ex["criteria"])
    samples = "".join(
        '<article class="ql-sample">'
        f'<p class="ql-sample__title">Sample {escape(s["letter"])}</p>'
        f'<p class="ql-sample__text">{escape(s["text"])}</p>'
        "</article>"
        for s in ex["samples"]
    )
    key = "".join(
        "<li>"
        f'<p class="ql-key__head"><strong>Sample {escape(k["letter"])}</strong> '
        f'<span class="ql-key__level">{escape(k["level"].capitalize())}</span></p>'
        f'<p>{escape(k["note"])}</p>'
        f'<p><strong>One level up:</strong> {escape(k["up"])}</p>'
        "</li>"
        for k in ex["key"]
    )
    return (
        '<div class="tm-example ql-example">'
        f'<h3 class="tm-example__subject">{escape(ex["subject"])} <span>· Grade {int(ex["grade"])}</span></h3>'
        "<dl>"
        f"<dt>The task</dt><dd>{escape(ex['task'])}</dd>"
        f'<dt>Criteria</dt><dd><ol class="ql-example__list">{criteria}</ol></dd>'
        "</dl>"
        '<h4 class="ql-example__heading">What students get: three samples</h4>'
        f'<div class="ql-samples">{samples}</div>'
        '<aside class="ql-key" aria-label="Teacher key">'
        '<h4 class="ql-example__heading">Teacher key · not for students</h4>'
        f'<ul class="ql-key__list">{key}</ul>'
        "</aside>"
        "</div>"
    )


def render_routine(routine: dict) -> str:
    """The six steps, the Grades 1-3 note, the time estimate, the copy button and the download link."""
    steps = "".join(f"<li>{escape(step)}</li>" for step in routine["steps"])
    return (
        f'<ol class="ql-list">{steps}</ol>\n'
        f'<p class="ql-prose">{escape(routine["younger"])}</p>\n'
        f'<p class="ql-prose ql-time">{escape(routine["time"])}</p>\n'
        f'{_copy_row("Copy text", routine_text(routine))}\n'
        f'{_download("quality-ladder-routine.docx", "Student sheet (.docx)")}'
    )


def render_whole_class(wc: dict) -> str:
    """The intro, the template headings with one line of guidance each, the follow-up,
    the copy button and the download link."""
    rows = "".join(
        f'<div class="ql-template__row"><dt>{escape(s["heading"])}</dt><dd>{escape(s["guide"])}</dd></div>'
        for s in wc["sections"]
    )
    return (
        f'<p class="section__lede">{escape(wc["intro"])}</p>\n'
        f'<dl class="ql-template">{rows}</dl>\n'
        f'<p class="ql-prose">{escape(wc["followup"])}</p>\n'
        f'{_copy_row("Copy template", whole_class_text(wc))}\n'
        f'{_download("whole-class-feedback.docx", "Whole-class feedback template (.docx)")}'
    )


def render_policy(policy: dict) -> str:
    """The intro, the principles (a principle with no source shows none), the copy button and the download link."""
    items = []
    for p in policy["principles"]:
        source = f' <span class="ql-principle__source">{escape(p["source"])}</span>' if p["source"] else ""
        items.append(f"<li><strong>{escape(p['title'])}.</strong> {escape(p['text'])}{source}</li>")
    return (
        f'<p class="section__lede">{escape(policy["intro"])}</p>\n'
        f'<ol class="ql-list ql-principles">{"".join(items)}</ol>\n'
        f'{_copy_row("Copy policy", policy_text(policy))}\n'
        f'{_download("feedback-policy.docx", "Feedback policy (.docx)")}'
    )


def render_colleagues(text: str) -> str:
    return f'<p class="ql-prose">{escape(text)}</p>'


def render_legend(labels: dict) -> str:
    rows = "".join(
        f'<li><span class="tm-chip tm-chip--{key}">{escape(labels[key]["name"])}</span> '
        f'{escape(labels[key]["definition"])}</li>'
        for key in LABEL_ORDER
    )
    return f'<ul class="tm-legend">{rows}</ul>'


def render_evidence(items: list, labels: dict) -> str:
    """The label legend, then one paragraph per research item with its label chip and linked sources."""
    out = [render_legend(labels)]
    for item in items:
        label = item["label"]
        out.append(
            f'<p class="ql-evidence__item"><span class="tm-chip tm-chip--{escape(label)}">'
            f'{escape(labels[label]["name"])}</span> <strong>{escape(item["title"])}</strong> '
            f'{escape(item["text"])} {_source_links(item["sources"])}</p>'
        )
    return "\n".join(out)


def render_care(items: list) -> str:
    rows = "".join(
        f'<li><strong>{escape(c["risk"])}</strong> {escape(c["what_we_do"])}</li>' for c in items
    )
    return f'<ul class="ql-care__list">{rows}</ul>'


def render_age(rules: list, date: str) -> str:
    rows = "".join(f"<li><strong>{escape(r['tool'])}:</strong> {escape(r['rule'])}</li>" for r in rules)
    return (
        '<p class="section__lede">You use AI to prepare. Students need no AI for Quality Ladder. '
        f"If students use AI tools, these rules apply ({escape(date)}):</p>\n"
        f'<ul class="tm-age">{rows}</ul>'
    )


def _inject(html: str, name: str, content: str) -> str:
    pattern = re.compile(rf"(<!--\s*{name}:start\s*-->)(.*?)(<!--\s*{name}:end\s*-->)", re.S)
    if not pattern.search(html):
        raise ValueError(f"Missing <!-- {name}:start --> / <!-- {name}:end --> markers")
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(3)}", html)


def build(root: Path) -> None:
    data = json.loads((root / SLUG / "ladder-en.json").read_text(encoding="utf-8"))
    page = root / SLUG / "index.html"
    html = page.read_text(encoding="utf-8")
    html = _inject(html, "hero-example", render_example(data))
    html = _inject(html, "routine", render_routine(data["routine"]))
    html = _inject(html, "whole-class", render_whole_class(data["whole_class"]))
    html = _inject(html, "policy", render_policy(data["policy"]))
    html = _inject(html, "colleagues", render_colleagues(data["colleagues"]))
    html = _inject(html, "evidence", render_evidence(data["evidence"], data["labels"]))
    html = _inject(html, "care", render_care(data["care"]))
    html = _inject(html, "age", render_age(data["age_rules"], data["age_rules_date"]))
    page.write_text(html, encoding="utf-8")
    print(f"Built the Quality Ladder sections into {page.relative_to(root)}")


if __name__ == "__main__":
    build(ROOT)
