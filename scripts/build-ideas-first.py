#!/usr/bin/env python3
"""Build the static parts of the Ideas first page from ideas-first-778ba230/ideas-en.json.

The page is for Skool members only. It is reached through a hidden link, has
noindex (HIDDEN_PATHS in scripts/build-seo-meta.py) and is never linked from
the rest of the site.

Replaces the content between these marker pairs in ideas-first-778ba230/index.html:
  <!-- hero-example:start --> / <!-- hero-example:end -->  the worked example: four rows, a note and a closing line
  <!-- how:start -->         / <!-- how:end -->          the four steps (the <li> items), the Framework chip and its note
  <!-- choose:start -->      / <!-- choose:end -->       intro, the three checks with the follow-up copy button, the three ways
  <!-- team:start -->        / <!-- team:end -->         intro, the five-step routine, the note, the .docx link
  <!-- evidence:start -->    / <!-- evidence:end -->     lede, the Promising chip, the label legend, the six research items
  <!-- care:start -->        / <!-- care:end -->         the five care points
  <!-- next:start -->        / <!-- next:end -->         the links onward

Running it twice gives the same file. The form and the prompt box are written
by hand in index.html; the prompt itself is built in the browser by
assets/js/ideas-first.js. sheet_text() gives the plain text of the team sheet;
exports/build-ideas-first-docx.py reuses it (and SLUG) for the Word file.

Usage:
    /usr/bin/python3 scripts/build-ideas-first.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "ideas-first-778ba230"

# Teckenförklaringen listar etiketterna i den här ordningen.
LABEL_ORDER = ("strong", "promising", "framework", "choosewise")

# Första raden i varje kopierad prompt. Den läggs till av ideas-first.js, som har
# en egen kopia av raden; den här konstanten är det testerna jämför mot, så
# ändras raden ska båda ändras.
PRIVACY_COPY = "Do not include student names or student work in this conversation."

# Texten på knappen under första kontrollen.
FOLLOW_UP_BUTTON = "Copy follow-up prompt"


# ───── Ren text: teamets blad ─────

def sheet_text(sheet: dict) -> str:
    """The team sheet as plain lines, one per line, in this order: the title; the four
    header labels, each followed by ':'; the note; the routine heading and the five
    routine lines; then the three sections, each as its heading followed by its column
    labels (the 'from the AI' section has no columns and gives its hint instead).
    The text of the .docx file is compared with this, in order."""
    lines = [sheet["title"]]
    lines += [f"{label}:" for label in sheet["header"]]
    lines += [sheet["note"], sheet["routine_heading"]]
    lines += sheet["routine"]
    lines += [sheet["before_ai"]["heading"]] + sheet["before_ai"]["columns"]
    lines += [sheet["from_ai"]["heading"], sheet["from_ai"]["hint"]]
    lines += [sheet["chose"]["heading"]] + sheet["chose"]["columns"]
    return "\n".join(lines)


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


def render_example(hero: dict) -> str:
    """The worked example in the hero: four rows, the note that it is our example, and the closing line."""
    rows = "".join(f"<dt>{escape(r['term'])}</dt><dd>{escape(r['text'])}</dd>" for r in hero["rows"])
    return (
        f'<div class="tm-example if-example"><dl>{rows}</dl>'
        f'<p class="if-example__note">{escape(hero["note"])}</p>'
        f'<p class="if-example__closing">{escape(hero["closing"])}</p></div>'
    )


def render_how(how: dict, labels: dict) -> str:
    """The four steps, then the Framework chip with the line that says what the steps rest on."""
    items = "\n".join(f"<li>{escape(s)}</li>" for s in how["steps"])
    return (
        f'<ol class="tm-steps">\n{items}\n</ol>\n'
        f'<p class="if-label">{_chip(how["label"], labels)} <span class="if-label__note">{escape(how["note"])}</span></p>'
    )


def render_choose(choose: dict) -> str:
    """The intro, the three checks (the follow-up copy button sits inside the first one,
    since a <div> between two <li> would be invalid), then the three ways to change an idea."""
    checks = []
    for i, check in enumerate(choose["checks"]):
        extra = _copy_row(FOLLOW_UP_BUTTON, choose["follow_up"]) if i == 0 else ""
        checks.append(f"<li>{escape(check)}{extra}</li>")
    ways = "".join(f"<li>{escape(w)}</li>" for w in choose["ways"])
    return "\n".join([
        f'<p class="section__lede">{escape(choose["intro"])}</p>',
        '<h3 class="if-subtitle">Check before use</h3>',
        f'<ol class="if-checks">{"".join(checks)}</ol>',
        '<h3 class="if-subtitle">Three ways to change an idea</h3>',
        f'<ul class="if-ways">{ways}</ul>',
        f'<p class="if-prose">{escape(choose["ways_note"])}</p>',
    ])


def render_team(team: dict) -> str:
    """The intro, the five routine steps (step 4 links to Get ideas), the note and the .docx link."""
    steps = []
    for i, step in enumerate(team["routine"], 1):
        text = escape(step)
        if i == 4:
            assert text.count("Get ideas") == 1, "step 4 must name Get ideas exactly once"
            text = text.replace("Get ideas", '<a href="#if-ideas">Get ideas</a>')
        steps.append(f"<li>{text}</li>")
    return "\n".join([
        f'<p class="section__lede">{escape(team["intro"])}</p>',
        f'<ol class="if-routine">{"".join(steps)}</ol>',
        f'<p class="if-prose">{escape(team["routine_note"])}</p>',
        '<p class="if-download"><a href="team-idea-sheet.docx" download>Team sheet (.docx)</a></p>',
    ])


def render_legend(labels: dict) -> str:
    rows = "".join(
        f'<li><span class="tm-chip tm-chip--{key}">{escape(labels[key]["name"])}</span> '
        f'{escape(labels[key]["definition"])}</li>'
        for key in LABEL_ORDER
    )
    return f'<ul class="tm-legend">{rows}</ul>'


def render_evidence(evidence: dict, labels: dict) -> str:
    """The lede, the overall label, the label legend, then one paragraph per research
    item. An item gets a chip only when it has a label of its own."""
    out = [
        f'<p class="section__lede">{escape(evidence["lede"])}</p>',
        f'<p class="if-label">{_chip(evidence["label"], labels)}</p>',
        render_legend(labels),
    ]
    for item in evidence["items"]:
        chip = f"{_chip(item['label'], labels)} " if item["label"] else ""
        sources = f" {_source_links(item['sources'])}" if item["sources"] else ""
        out.append(
            f'<p class="if-evidence__item">{chip}<strong class="if-item-title">{escape(item["title"])}</strong> '
            f'{escape(item["text"])}{sources}</p>'
        )
    return "\n".join(out)


def render_care(items: list) -> str:
    rows = "".join(
        f'<li><strong class="if-item-title">{escape(c["risk"])}</strong> {escape(c["what_we_do"])}</li>' for c in items
    )
    return f'<ul class="if-care__list">{rows}</ul>'


def render_next(items: list) -> str:
    rows = "\n".join(f'<li><a href="{escape(n["href"])}">{escape(n["text"])}</a></li>' for n in items)
    return f'<ul class="if-next">\n{rows}\n</ul>'


def _inject(html: str, name: str, content: str) -> str:
    pattern = re.compile(rf"(<!--\s*{name}:start\s*-->)(.*?)(<!--\s*{name}:end\s*-->)", re.S)
    if not pattern.search(html):
        raise ValueError(f"Missing <!-- {name}:start --> / <!-- {name}:end --> markers")
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(3)}", html)


def build(root: Path) -> None:
    data = json.loads((root / SLUG / "ideas-en.json").read_text(encoding="utf-8"))
    page = root / SLUG / "index.html"
    html = page.read_text(encoding="utf-8")
    html = _inject(html, "hero-example", render_example(data["hero"]))
    html = _inject(html, "how", render_how(data["how"], data["labels"]))
    html = _inject(html, "choose", render_choose(data["choose"]))
    html = _inject(html, "team", render_team(data["team"]))
    html = _inject(html, "evidence", render_evidence(data["evidence"], data["labels"]))
    html = _inject(html, "care", render_care(data["care"]))
    html = _inject(html, "next", render_next(data["next"]))
    page.write_text(html, encoding="utf-8")
    print(f"Built the Ideas first sections into {page.relative_to(root)}")


if __name__ == "__main__":
    build(ROOT)
