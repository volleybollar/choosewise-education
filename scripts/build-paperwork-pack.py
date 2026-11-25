#!/usr/bin/env python3
"""Build the static parts of the Paperwork Pack page from paperwork-pack-f388fd9f/paperwork-en.json.

The page is for Skool members only. It is reached through a hidden link, has
noindex (HIDDEN_PATHS in scripts/build-seo-meta.py) and is never linked from
the rest of the site.

Replaces the content between these marker pairs in paperwork-pack-f388fd9f/index.html:
  <!-- hero-example:start --> / <!-- hero-example:end -->  the worked example: a parent message, one line per job
  <!-- meetings:start -->     / <!-- meetings:end -->      intro, three templates, privacy line, prompts P1-P2
  <!-- admin:start -->        / <!-- admin:end -->         intro, two templates, privacy line, prompts P3-P4, link, country line
  <!-- parents:start -->      / <!-- parents:end -->       intro, one template, privacy line, prompts P5-P7, country line
  <!-- evidence:start -->     / <!-- evidence:end -->      the label legend and the seven research items
  <!-- care:start -->         / <!-- care:end -->          the five care points

Running it twice gives the same file. Every copy button (templates and
prompts) is the site's own data-copy button: copy-to-clipboard.js does the
copying, so the page has no JavaScript of its own. template_text() and
prompt_text() give the plain text that the buttons put on the clipboard;
exports/build-paperwork-pack-docx.py reuses template_text() for the Word files.

Usage:
    /usr/bin/python3 scripts/build-paperwork-pack.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "paperwork-pack-f388fd9f"

# Teckenförklaringen listar etiketterna i den här ordningen.
LABEL_ORDER = ("strong", "promising", "framework", "choosewise")

# Första raden i varje kopierad prompt. Den står inte i JSON-filen: prompterna
# där är ordagrant som i kurslektionerna, och raden läggs till här, på ett ställe.
PRIVACY_COPY = "Do not include student names or student work in this conversation."

# Raden under "Prompts to make your own" i varje avsnitt (som "untested" i kurslektionerna).
PROMPTS_NOTE = "These prompts are writing aids, not evidence-based methods."

# Raden under varje tabell. Den syns bara på mobil, där tabellen visar en enda rad.
TABLE_NOTE = "On a small screen, only the first row is shown. The Word file below has the full table."


# ───── Ren text: det som kopieringsknapparna lägger i urklipp ─────

def template_text(t: dict) -> str:
    """A template as plain text: the title, the intro, then each block as its heading
    and its lines. A table block is its heading, then the column names joined by ' | '
    on one line. This is both the clipboard text and the text of the .docx file."""
    parts = []
    for block in t["blocks"]:
        body = " | ".join(block["columns"]) if "columns" in block else "\n".join(block["lines"])
        parts.append(f"{block['heading']}\n{body}")
    return f"{t['title']}\n\n{t['intro']}\n\n" + "\n\n".join(parts)


def message_text(block: dict) -> str:
    """A message home as its own copy button gives it: the message and the sign-off, no heading."""
    return "\n".join(block["lines"])


def prompt_text(p: dict) -> str:
    """A prompt as the copy button gives it: the privacy line, a blank line, the prompt."""
    return PRIVACY_COPY + "\n\n" + p["body"]


# ───── HTML ─────

def _source_links(sources: list) -> str:
    """'Source: a, b' as links. 'Sources:' when there is more than one."""
    links = ", ".join(f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' for s in sources)
    word = "Sources" if len(sources) > 1 else "Source"
    return f'<span class="tm-move__sources">{word}: {links}</span>'


def _copy_row(label: str, text: str, kind: str = "primary") -> str:
    """A copy button with its 'Copied' toast. The toast must follow the button:
    copy-to-clipboard.js looks for it among the button's siblings. kind="secondary"
    is the lighter button, for the four messages inside a template."""
    return (
        '<div class="tm-copy-row">'
        f'<button type="button" class="btn btn--{kind}" data-copy="{escape(text)}">{escape(label)}</button>'
        '<span class="copy-toast" role="status">Copied</span>'
        "</div>"
    )


def _download(filename: str, label: str) -> str:
    return f'<p class="pp-download"><a href="{escape(filename)}" download>{escape(label)}</a></p>'


def render_example(hero: dict) -> str:
    """The worked example: the parent message from lesson 10, one row per sentence,
    with the job that sentence does next to it."""
    rows = "".join(
        '<li class="pp-example__row">'
        f'<span class="pp-example__text">{escape(line["text"])}</span>'
        f'<span class="pp-example__job">{escape(line["job"])}</span>'
        "</li>"
        for line in hero["lines"]
    )
    return f'<div class="tm-example pp-example"><ol class="pp-example__list">{rows}</ol></div>'


def _render_block(block: dict) -> str:
    """One block of a template. A table block is a real table whose cells carry their
    column name (data-label), so that it can stack at phone width, followed by a note that
    only shows on a phone. Other blocks are a heading and paragraphs; box: true gives a
    bordered fill-in area, and copy: true (the four messages home) gives the block its own
    copy button."""
    heading = f'<h4 class="pp-block__heading">{escape(block["heading"])}</h4>'
    if "columns" in block:
        head = "".join(f'<th scope="col">{escape(c)}</th>' for c in block["columns"])
        cells = "".join(f'<td data-label="{escape(c)}"></td>' for c in block["columns"])
        body = "".join(f"<tr>{cells}</tr>" for _ in range(block["rows"]))
        return (
            '<div class="pp-block pp-block--table">'
            f"{heading}"
            '<div class="pp-table-wrap"><table class="pp-table">'
            f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody>"
            "</table></div>"
            f'<p class="pp-table__note">{escape(TABLE_NOTE)}</p>'
            "</div>"
        )
    lines = "".join(f"<p>{escape(line)}</p>" for line in block["lines"])
    box = " pp-block--box" if block["box"] else ""
    copy = _copy_row("Copy message", message_text(block), "secondary") if block.get("copy") else ""
    return f'<div class="pp-block{box}">{heading}{lines}{copy}</div>'


def _render_template(t: dict) -> str:
    download_label = t["title"] + " (.docx)"
    blocks = "".join(_render_block(b) for b in t["blocks"])
    return (
        '<article class="pp-template">'
        f'<h3 class="pp-template__title">{escape(t["title"])}</h3>'
        f'<p class="pp-template__intro">{escape(t["intro"])}</p>'
        f'<div class="pp-template__body">{blocks}</div>'
        f'{_copy_row("Copy text", template_text(t))}'
        f'{_download(t["file"], download_label)}'
        "</article>"
    )


def _render_prompt(p: dict) -> str:
    return (
        '<article class="pp-prompt">'
        f'<h4 class="pp-prompt__title">{escape(p["id"])} · {escape(p["title"])}</h4>'
        f'<p class="pp-prompt__text">{escape(p["body"])}</p>'
        f'{_copy_row("Copy prompt", prompt_text(p))}'
        "</article>"
    )


def render_section(sec: dict) -> str:
    """Everything inside a course section below its heading and label: the intro, the
    templates, the privacy line, the prompts, the links and the country line."""
    out = [f'<p class="section__lede">{escape(sec["intro"])}</p>']
    out.append('<div class="pp-templates">' + "".join(_render_template(t) for t in sec["templates"]) + "</div>")
    out.append('<h3 class="pp-subtitle">Prompts to make your own</h3>')
    # Samma rad i alla tre avsnitt: prompterna är skrivstöd, inte prövade metoder.
    out.append('<p class="pp-prompts__note">' + escape(PROMPTS_NOTE) + "</p>")
    out.append(
        '<p class="tm-privacy"><strong>Do not include student names or student work.</strong> '
        "Fill in the brackets afterwards, outside AI.</p>"
    )
    out.append('<div class="pp-prompts">' + "".join(_render_prompt(p) for p in sec["prompts"]) + "</div>")
    if sec.get("links"):
        items = "".join(f'<li><a href="{escape(l["href"])}">{escape(l["text"])}</a></li>' for l in sec["links"])
        out.append(f'<ul class="pp-links">{items}</ul>')
    if sec.get("country_line"):
        out.append(f'<p class="tm-note pp-country">{escape(sec["country_line"])}</p>')
    return "\n".join(out)


def render_legend(labels: dict) -> str:
    rows = "".join(
        f'<li><span class="tm-chip tm-chip--{key}">{escape(labels[key]["name"])}</span> '
        f'{escape(labels[key]["definition"])}</li>'
        for key in LABEL_ORDER
    )
    return f'<ul class="tm-legend">{rows}</ul>'


def render_evidence(items: list, labels: dict) -> str:
    """The label legend, then one paragraph per research item with its label chip
    (an item with no label shows none) and linked sources."""
    out = [render_legend(labels)]
    for item in items:
        label = item["label"]
        chip = (
            f'<span class="tm-chip tm-chip--{escape(label)}">{escape(labels[label]["name"])}</span> '
            if label else ""
        )
        out.append(
            f'<p class="pp-evidence__item">{chip}<strong>{escape(item["title"])}</strong> '
            f'{escape(item["text"])} {_source_links(item["sources"])}</p>'
        )
    return "\n".join(out)


def render_care(items: list) -> str:
    rows = "".join(
        f'<li><strong>{escape(c["risk"])}</strong> {escape(c["what_we_do"])}</li>' for c in items
    )
    return f'<ul class="pp-care__list">{rows}</ul>'


def _inject(html: str, name: str, content: str) -> str:
    pattern = re.compile(rf"(<!--\s*{name}:start\s*-->)(.*?)(<!--\s*{name}:end\s*-->)", re.S)
    if not pattern.search(html):
        raise ValueError(f"Missing <!-- {name}:start --> / <!-- {name}:end --> markers")
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(3)}", html)


def build(root: Path) -> None:
    data = json.loads((root / SLUG / "paperwork-en.json").read_text(encoding="utf-8"))
    page = root / SLUG / "index.html"
    html = page.read_text(encoding="utf-8")
    html = _inject(html, "hero-example", render_example(data["hero"]))
    for sec in data["sections"]:
        # Markörens namn är avsnittets id utan "pp-": pp-meetings -> meetings.
        html = _inject(html, sec["id"].removeprefix("pp-"), render_section(sec))
    html = _inject(html, "evidence", render_evidence(data["evidence"], data["labels"]))
    html = _inject(html, "care", render_care(data["care"]))
    page.write_text(html, encoding="utf-8")
    print(f"Built the Paperwork Pack sections into {page.relative_to(root)}")


if __name__ == "__main__":
    build(ROOT)
