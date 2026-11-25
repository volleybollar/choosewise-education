#!/usr/bin/env python3
"""Build the static parts of the Barrier Planner page from barrier-planner-1c25533d/planner-en.json.

The page is for Skool members only. It is reached through a hidden link, has
noindex (HIDDEN_PATHS in scripts/build-seo-meta.py) and is never linked from
the rest of the site.

Replaces the content between these marker pairs in barrier-planner-1c25533d/index.html:
  <!-- hero-example:start -->    / <!-- hero-example:end -->     the worked example: one plan, four rows
  <!-- how:start -->             / <!-- how:end -->              the three steps (the <li> items)
  <!-- barriers:start -->        / <!-- barriers:end -->         the diagnosis help text, the privacy line, the eight cards
  <!-- barrier-options:start --> / <!-- barrier-options:end -->  the eight <option> items of the barrier list
  <!-- adapt-example:start -->   / <!-- adapt-example:end -->    the worked sentence, the check line, the picture links
  <!-- record:start -->          / <!-- record:end -->           intro, warning, the blank form, questions, EEF box, copy and .docx
  <!-- unsupported:start -->     / <!-- unsupported:end -->      intro, the six items, the movement note, copy and .docx
  <!-- evidence:start -->        / <!-- evidence:end -->         lede, the label legend, the nine research items
  <!-- care:start -->            / <!-- care:end -->             the five care points
  <!-- data:start -->            / <!-- data:end -->             #bp-data: what the prompt builder needs, as JSON

Running it twice gives the same file. Every copy button that carries a fixed
text (the form and the list) is the site's own data-copy button;
copy-to-clipboard.js does the copying. record_text() and unsupported_text()
give the plain text that those buttons put on the clipboard;
exports/build-barrier-planner-docx.py reuses them for the Word files. The two
prompt builders are filled in by assets/js/barrier-planner.js, from #bp-data.

Usage:
    /usr/bin/python3 scripts/build-barrier-planner.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "barrier-planner-1c25533d"

# Teckenförklaringen listar etiketterna i den här ordningen.
LABEL_ORDER = ("strong", "promising", "framework", "choosewise")

# Första raden i varje kopierad prompt. Den läggs till av barrier-planner.js
# (steg 3); konstanten står här så att alla delar av sidan använder samma rad.
PRIVACY_COPY = "Do not include student names or student work in this conversation."

# Rubriker som både sidan och Word-filen visar. Ändras de, ändras båda.
RECORD_TITLE = "Needs and measures"
REVIEW_QUESTIONS_TITLE = "Questions for the review meeting"
EEF_TITLE = "The EEF's three questions"
UNSUPPORTED_TITLE = "Popular but unsupported"


# ───── Ren text: det som kopieringsknapparna lägger i urklipp ─────

def _numbered(items: list) -> str:
    return "\n".join(f"{i}. {text}" for i, text in enumerate(items, 1))


def record_text(record: dict) -> str:
    """The needs-and-measures form as plain text: the title, the warning, the header
    lines (each followed by ':'), then the blocks in order. A block is its heading and
    hint; the measures block adds the column names joined by ' | ', and the outcomes
    block adds the outcomes joined by ' | '. The five review questions, the EEF's three
    questions and the country line close it. This is both the clipboard text and the
    text of the .docx file."""
    parts = [RECORD_TITLE, record["warning"], "\n".join(f"{h}:" for h in record["header"])]
    for block in record["blocks"]:
        lines = [block["heading"], block["hint"]]
        if block["kind"] == "measures":
            lines.append(" | ".join(record["measure_columns"]))
        elif block["kind"] == "outcomes":
            lines.append(" | ".join(record["outcomes"]))
        parts.append("\n".join(lines))
    parts.append(f"{REVIEW_QUESTIONS_TITLE}\n{_numbered(record['review_questions'])}")
    parts.append(f"{EEF_TITLE}\n{_numbered(record['eef_questions'])}")
    parts.append(record["country_line"])
    return "\n\n".join(parts)


def unsupported_text(u: dict) -> str:
    """The list of popular but unsupported adjustments as plain text: the title, then
    each item as its title, the research line and 'Instead: ...', then the movement note."""
    parts = [UNSUPPORTED_TITLE]
    for item in u["items"]:
        parts.append(f"{item['title']}\n{item['research']}\nInstead: {item['instead']}")
    parts.append(u["movement_note"])
    return "\n\n".join(parts)


def bp_data(data: dict) -> dict:
    """What the prompt builder needs: per card its id, the barrier sentence and the short
    form of every whole-class move and targeted support."""
    return {"cards": [
        {"id": c["id"], "barrier": c["barrier"],
         "whole_class": [m["short"] for m in c["whole_class"]],
         "targeted": [m["short"] for m in c["targeted"]]}
        for c in data["cards"]
    ]}


# ───── HTML ─────

def _source_links(sources: list) -> str:
    """'Source: a, b' as links. 'Sources:' when there is more than one."""
    links = ", ".join(f'<a href="{escape(s["url"])}">{escape(s["text"])}</a>' for s in sources)
    word = "Sources" if len(sources) > 1 else "Source"
    return f'<span class="tm-move__sources">{word}: {links}</span>'


def _chip(key: str, labels: dict) -> str:
    return f'<span class="tm-chip tm-chip--{escape(key)}">{escape(labels[key]["name"])}</span>'


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
    return f'<p class="bp-download"><a href="{escape(filename)}" download>{escape(label)}</a></p>'


def _definition_list(rows: list) -> str:
    return "<dl>" + "".join(f"<dt>{escape(r['term'])}</dt><dd>{escape(r['text'])}</dd>" for r in rows) + "</dl>"


def render_example(hero: dict) -> str:
    """The worked plan in the hero: four rows, then the note that it is our example."""
    return (
        f'<div class="tm-example bp-example">{_definition_list(hero["rows"])}'
        f'<p class="bp-example__note">{escape(hero["note"])}</p></div>'
    )


def render_how(items: list) -> str:
    return "\n".join(f"<li>{escape(i)}</li>" for i in items)


def _render_moves(moves: list, labels: dict) -> str:
    """A list of moves. A move with a label of its own gets a small chip after the text."""
    rows = "".join(
        f'<li>{escape(m["text"])}'
        + (f' {_chip(m["label"], labels)}' if m["label"] else "")
        + "</li>"
        for m in moves
    )
    return f'<ul class="bp-card__list">{rows}</ul>'


def _render_card(c: dict, labels: dict) -> str:
    """One barrier card, open and printable without JavaScript. 'Not this' only shows
    when the card has something to warn about; the link only when the card has one."""
    signs = "".join(f"<li>{escape(s)}</li>" for s in c["signs"])
    parts = [
        f'<article class="bp-card" id="bp-barrier-{escape(c["id"])}">',
        f'<header class="bp-card__head"><h3 class="bp-card__title">{escape(c["barrier"])}</h3>'
        f'{_chip(c["label"], labels)}</header>',
        '<h4 class="bp-card__heading">What you see</h4>',
        f'<ul class="bp-card__list">{signs}</ul>',
        '<h4 class="bp-card__heading">For the whole class</h4>',
        _render_moves(c["whole_class"], labels),
        '<h4 class="bp-card__heading">Targeted</h4>',
        _render_moves(c["targeted"], labels),
    ]
    if c["not_this"]:
        items = "".join(f"<li>{escape(n)}</li>" for n in c["not_this"])
        parts += ['<h4 class="bp-card__heading">Not this</h4>', f'<ul class="bp-card__list">{items}</ul>']
    parts += [
        '<h4 class="bp-card__heading">Look for in three weeks</h4>',
        f'<p class="bp-card__review">{escape(c["review"])}</p>',
        f'<p class="bp-card__sources">{_source_links(c["sources"])}</p>',
    ]
    if c["link"]:
        parts.append(f'<p class="bp-card__link"><a href="{escape(c["link"]["href"])}">{escape(c["link"]["text"])}</a></p>')
    parts.append("</article>")
    return "".join(parts)


def render_barriers(data: dict) -> str:
    """The help text for someone with a diagnosis in mind, the privacy line and the cards."""
    intro = data["barriers_intro"]
    cards = "".join(_render_card(c, data["labels"]) for c in data["cards"])
    return (
        f'<p class="section__lede bp-diagnosis">{escape(intro["diagnosis"])}</p>\n'
        f'<p class="tm-privacy"><strong>{escape(intro["privacy"])}</strong></p>\n'
        f'<div class="bp-cards">{cards}</div>'
    )


def render_barrier_options(cards: list) -> str:
    return "\n".join(f'<option value="{escape(c["id"])}">{escape(c["barrier"])}</option>' for c in cards)


def render_adapt_example(adapt: dict) -> str:
    """The worked sentence (original, elaborated, glossary, question, picture), the check
    line from lesson 8 and the three places to make the picture."""
    links = "".join(f'<li><a href="{escape(l["href"])}">{escape(l["text"])}</a></li>' for l in adapt["links"])
    return (
        f'<div class="tm-example bp-example">{_definition_list(adapt["example"])}</div>\n'
        f'<p class="bp-prose"><strong>{escape(adapt["check"])}</strong></p>\n'
        f'<ul class="bp-links">{links}</ul>'
    )


def _warning_html(text: str) -> str:
    """The warning above the form: the first sentence in bold, as in the course."""
    first, sep, rest = text.partition(". ")
    if not sep:
        return f"<strong>{escape(text)}</strong>"
    return f"<strong>{escape(first)}.</strong> {escape(rest)}"


def _render_form_block(block: dict, record: dict) -> str:
    """One block of the blank form. A box and a line are bordered fill-in areas; the
    measures block is a real table whose cells carry their column name (data-label), so
    that it can stack at phone width; the outcomes block is one tick box per outcome."""
    head = (f'<h4 class="bp-block__heading">{escape(block["heading"])}</h4>'
            f'<p class="bp-block__hint">{escape(block["hint"])}</p>')
    kind = block["kind"]
    if kind == "measures":
        cols = record["measure_columns"]
        th = "".join(f'<th scope="col">{escape(c)}</th>' for c in cols)
        cells = "".join(f'<td data-label="{escape(c)}"></td>' for c in cols)
        rows = "".join(f"<tr>{cells}</tr>" for _ in range(3))
        body = f'<div class="bp-table-wrap"><table class="bp-table"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>'
    elif kind == "outcomes":
        items = "".join(f'<li><span class="bp-tick" aria-hidden="true"></span>{escape(o)}</li>' for o in record["outcomes"])
        body = f'<ul class="bp-outcomes">{items}</ul>'
    elif kind == "line":
        body = '<div class="bp-line"></div>'
    else:
        body = '<div class="bp-box"></div>'
    return f'<div class="bp-block bp-block--{escape(kind)}">{head}{body}</div>'


def render_record(record: dict) -> str:
    """The needs-and-measures form as a finished blank. The warning stands directly above
    the form's first line, with nothing between them. The five questions, the EEF's three
    questions and the country line follow the form; one copy button and the .docx link
    close the section."""
    header = "".join(
        f'<div class="bp-form__field"><span class="bp-form__label">{escape(h)}</span>'
        '<span class="bp-form__fill"></span></div>'
        for h in record["header"]
    )
    blocks = "".join(_render_form_block(b, record) for b in record["blocks"])
    questions = "".join(f"<li>{escape(q)}</li>" for q in record["review_questions"])
    eef = "".join(f"<li>{escape(q)}</li>" for q in record["eef_questions"])
    return "\n".join([
        f'<p class="section__lede">{escape(record["intro"])}</p>',
        f'<p class="bp-warning">{_warning_html(record["warning"])}</p>',
        f'<div class="bp-form"><div class="bp-form__row">{header}</div>{blocks}</div>',
        f'<h3 class="bp-subtitle">{escape(REVIEW_QUESTIONS_TITLE)}</h3>',
        f'<ol class="bp-questions">{questions}</ol>',
        f'<div class="bp-eef"><h3 class="bp-eef__title">{escape(EEF_TITLE)}</h3><ol class="bp-questions">{eef}</ol></div>',
        f'<p class="tm-note bp-country">{escape(record["country_line"])}</p>',
        _copy_row("Copy text", record_text(record)),
        _download("needs-and-measures.docx", f"{RECORD_TITLE} (.docx)"),
    ])


def render_unsupported(u: dict) -> str:
    """The intro, the six items (what the research says, then 'Instead:'), the movement
    note, and the copy button and .docx link for the list."""
    items = "".join(
        f'<li class="bp-unsupported__item"><strong>{escape(i["title"])}</strong> {escape(i["research"])} '
        f'<span class="bp-unsupported__instead">Instead: {escape(i["instead"])}</span></li>'
        for i in u["items"]
    )
    return "\n".join([
        f'<p class="section__lede">{escape(u["intro"])}</p>',
        f'<ul class="bp-unsupported__list">{items}</ul>',
        f'<p class="bp-prose">{escape(u["movement_note"])}</p>',
        _copy_row("Copy text", unsupported_text(u)),
        _download("popular-but-unsupported.docx", f"{UNSUPPORTED_TITLE} (.docx)"),
    ])


def render_legend(labels: dict) -> str:
    rows = "".join(
        f'<li><span class="tm-chip tm-chip--{key}">{escape(labels[key]["name"])}</span> '
        f'{escape(labels[key]["definition"])}</li>'
        for key in LABEL_ORDER
    )
    return f'<ul class="tm-legend">{rows}</ul>'


def render_evidence(evidence: dict, labels: dict) -> str:
    """The lede, the label legend, then one paragraph per research item with its label
    chip and linked sources."""
    out = [f'<p class="section__lede">{escape(evidence["lede"])}</p>', render_legend(labels)]
    for item in evidence["items"]:
        out.append(
            f'<p class="bp-evidence__item">{_chip(item["label"], labels)} '
            f'<strong>{escape(item["title"])}</strong> '
            f'{escape(item["text"])} {_source_links(item["sources"])}</p>'
        )
    return "\n".join(out)


def render_care(items: list) -> str:
    rows = "".join(
        f'<li><strong>{escape(c["risk"])}</strong> {escape(c["what_we_do"])}</li>' for c in items
    )
    return f'<ul class="bp-care__list">{rows}</ul>'


def render_data(data: dict) -> str:
    """What the prompt builder needs, as JSON. '</' is written '<\\/' so the text can
    never close the script tag."""
    text = json.dumps(bp_data(data), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/json" id="bp-data">{text}</script>'


def _inject(html: str, name: str, content: str) -> str:
    pattern = re.compile(rf"(<!--\s*{name}:start\s*-->)(.*?)(<!--\s*{name}:end\s*-->)", re.S)
    if not pattern.search(html):
        raise ValueError(f"Missing <!-- {name}:start --> / <!-- {name}:end --> markers")
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(3)}", html)


def build(root: Path) -> None:
    data = json.loads((root / SLUG / "planner-en.json").read_text(encoding="utf-8"))
    page = root / SLUG / "index.html"
    html = page.read_text(encoding="utf-8")
    html = _inject(html, "hero-example", render_example(data["hero"]))
    html = _inject(html, "how", render_how(data["how"]))
    html = _inject(html, "barriers", render_barriers(data))
    html = _inject(html, "barrier-options", render_barrier_options(data["cards"]))
    html = _inject(html, "adapt-example", render_adapt_example(data["adapt"]))
    html = _inject(html, "record", render_record(data["record"]))
    html = _inject(html, "unsupported", render_unsupported(data["unsupported"]))
    html = _inject(html, "evidence", render_evidence(data["evidence"], data["labels"]))
    html = _inject(html, "care", render_care(data["care"]))
    html = _inject(html, "data", render_data(data))
    page.write_text(html, encoding="utf-8")
    print(f"Built the Barrier Planner sections into {page.relative_to(root)}")


if __name__ == "__main__":
    build(ROOT)
