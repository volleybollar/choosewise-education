#!/usr/bin/env python3
"""Build the AI lesson pages for students (Skool courses 5 and 6) from JSON.

One hidden folder per track. For every track in TRACKS this writes
  <slug>/index.html         the overview page, from <slug>/track-en.json
  <slug>/<id>/index.html    one teacher page per lesson, from <slug>/<id>/lesson-en.json

The pages are generated whole: edit the JSON or this script, not the HTML.
The block that scripts/build-seo-meta.py owns (noindex for these hidden pages)
is carried over from the page on disk, so the two scripts can run in any order.
Running it twice gives the same files.

The pages are for Skool members only. They are reached through hidden links,
have noindex (HIDDEN_PATHS in scripts/build-seo-meta.py) and are never linked
from the rest of the site.

Usage:
    /usr/bin/python3 scripts/build-ai-lessons.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ["ai-lessons-younger-3c514a93", "ai-lessons-older-319cf15d"]
SEO_BLOCK = re.compile(r"<!-- seo:start \(build-seo-meta\.py\) -->.*?<!-- seo:end -->", re.S)
AI_USE = {"none": "No AI", "teacher-demo": "Teacher demo", "students": "Students use AI"}

# Samma stilmallar som Pedagogy Compass, plus det som är nytt för lektionerna (prefix al-).
HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — choosewise.education</title>
  <meta name="description" content="{description}">
  <link rel="stylesheet" href="/assets/css/fonts.css">
  <link rel="stylesheet" href="/assets/css/tokens.css">
  <link rel="stylesheet" href="/assets/css/base.css">
  <link rel="stylesheet" href="/assets/css/components.css?v=20261020a">
  <link rel="stylesheet" href="/assets/css/pages.css?v=20261020c">
  <!-- Delade stilar för verktygssidorna (prefix tm-), och sedan det som är
       nytt för AI-lektionerna (prefix al-). -->
  <link rel="stylesheet" href="/assets/css/thinking-moves.css?v=20261029a">
  <link rel="stylesheet" href="/assets/css/ai-lessons.css?v=20261111a">
  <!-- Sidan är bara för Skool-medlemmar. build-seo-meta.py lägger in noindex
       här (HIDDEN_PATHS), och sidan länkas aldrig från resten av sajten.
       Sidan byggs av scripts/build-ai-lessons.py: ändra JSON-filen, inte HTML:en. -->
</head>
<body>
  <div data-include="/assets/partials/header-en.html"></div>

  <main>
"""

FOOT = """  </main>

  <div data-include="/assets/partials/footer-en.html"></div>

  <script src="/assets/js/include.js"></script>
</body>
</html>
"""


def load_track(root: Path, slug: str) -> dict:
    """The track, plus "lesson_data": every built lesson in the track's order."""
    track = json.loads((root / slug / "track-en.json").read_text(encoding="utf-8"))
    track["lesson_data"] = [json.loads((root / slug / entry["id"] / "lesson-en.json").read_text(encoding="utf-8"))
                            for entry in track["lessons"]]
    return track


def lesson_url(track: dict, lesson: dict) -> str:
    return f"/{track['slug']}/{lesson['id']}/"


def pdf_url(track: dict, lesson: dict) -> str:
    return lesson_url(track, lesson) + lesson["student_pdf"]["file"]


def keep_seo_block(old: str | None, new: str) -> str:
    """Copy build-seo-meta.py's block from the page on disk into the new page,
    just before </head>, exactly where that script puts it."""
    m = SEO_BLOCK.search(old or "")
    if not m:
        return new
    return new.replace("</head>", m.group(0) + "\n</head>", 1)


def _list(items: list, cls: str = "") -> str:
    attr = f' class="{cls}"' if cls else ""
    return f"<ul{attr}>" + "".join(f"<li>{escape(i)}</li>" for i in items) + "</ul>"


def _band(track: dict, band_id: str) -> dict:
    return next(b for b in track["bands"] if b["id"] == band_id)


def _age_table(track: dict, tool_ids: list) -> str:
    """Åldersgränserna som tabell, daterade (global regel för AI-innehåll)."""
    tools = track["age_limits"]["tools"]
    rows = "".join(
        f"<tr><th scope=\"row\">{escape(tools[t]['name'])}</th><td>{escape(tools[t]['min_age'])}</td>"
        f"<td>{escape(tools[t]['note'])}</td></tr>"
        for t in tool_ids
    )
    return (
        '<table class="al-table">'
        "<thead><tr><th scope=\"col\">Tool</th><th scope=\"col\">Minimum age</th><th scope=\"col\">Notes</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
        f'<p class="al-checked">Checked {escape(track["age_limits"]["checked"])}. Age rules change often.</p>'
    )


def _further_reading(items: list) -> str:
    return "<ul class=\"tm-sources\">" + "".join(
        f'<li><a href="{escape(i["url"])}">{escape(i["title"])}</a></li>' for i in items) + "</ul>"


# ───── Översiktssidan ─────

def _lesson_card(track: dict, lesson: dict) -> str:
    """Ett lektionskort: titel, en rad, längd och AI-användning, länkar till lärarsida och PDF."""
    return (
        '<article class="tm-move al-card">'
        f'<span class="tm-move__num">Lesson {lesson["number"]}</span>'
        f'<h4 class="tm-move__name"><a href="{lesson_url(track, lesson)}">{escape(lesson["title"])}</a></h4>'
        f'<p class="tm-move__line">{escape(lesson["line"])}</p>'
        f'<p class="tm-move__meta"><span>{lesson["minutes"]} min</span><span>{escape(AI_USE[lesson["ai_use"]])}</span></p>'
        '<p class="al-card__links">'
        f'<a class="btn btn--primary" href="{lesson_url(track, lesson)}">Teacher guide</a>'
        f'<a class="al-card__pdf" href="{pdf_url(track, lesson)}" download>Student PDF</a>'
        "</p></article>"
    )


def render_overview(track: dict) -> str:
    lessons = track["lesson_data"]
    stats = track["stats"][:1] + [{"label": "Lessons", "value": str(len(lessons))}] + track["stats"][1:]
    stat_items = "".join(f'<li class="al-stat"><span class="al-stat__label">{escape(s["label"])}</span>'
                         f'<strong class="al-stat__value">{escape(s["value"])}</strong></li>' for s in stats)
    chips = "".join(f"<li>{escape(c)}</li>" for c in track["chips"])
    threads = "".join(f'<div class="tm-cluster"><h3>{escape(t["name"])}</h3><p>{escape(t["line"])}</p></div>'
                      for t in track["threads"])
    bands = []
    for band in track["bands"]:
        cards = [_lesson_card(track, lesson) for lesson in lessons if lesson["band"] == band["id"]]
        if cards:  # ett åldersband visas bara när det har färdiga lektioner
            bands.append(f'<h3 class="al-band__title">{escape(band["ages"])}</h3>'
                         f'<p class="al-band__line">{escape(band["line"])}</p>'
                         f'<div class="tm-grid">{"".join(cards)}</div>')
    frameworks = "".join(f'<li><a href="{escape(f["url"])}">{escape(f["name"])}</a>: {escape(f["full"])}</li>'
                         for f in track["frameworks"])
    reading = {r["url"]: r for lesson in lessons for r in lesson["further_reading"]}
    return (
        HEAD.format(title=escape(track["title"]), description=escape(track["lede"]))
        + f"""    <!-- Hero: vad spåret är, taggar och nyckeltal (som codeyogi.org/ai/basic, men lärarlett). -->
    <section class="page-hero container" id="al-hero">
      <span class="eyebrow">{escape(track["eyebrow"])}</span>
      <h1>{escape(track["title"])}</h1>
      <p class="lede">{escape(track["lede"])}</p>
      <ul class="al-chips">{chips}</ul>
      <ul class="al-stats">{stat_items}</ul>
    </section>

    <!-- Vad eleverna ska kunna efter spåret. -->
    <section class="section section--alt" id="al-objectives">
      <div class="container">
        <h2 class="section__title">What students learn</h2>
        {_list(track["objectives"], "al-list")}
      </div>
    </section>

    <!-- De fem trådarna som återkommer i varje åldersband (en spiral). -->
    <section class="section" id="al-threads">
      <div class="container">
        <h2 class="section__title">Five threads</h2>
        <p class="section__lede">The same five threads come back in every age band, a step further each time.</p>
        <div class="tm-clusters">{threads}</div>
      </div>
    </section>

    <!-- Lektionerna, grupperade per åldersband. Bara färdiga lektioner visas. -->
    <section class="section section--alt" id="al-lessons">
      <div class="container">
        <h2 class="section__title">The lessons</h2>
        <p class="section__lede">Each lesson works on its own. Open the teacher guide, print the student PDF.</p>
        {"".join(bands)}
      </div>
    </section>

    <!-- Hur en lektion går till. -->
    <section class="section" id="al-how">
      <div class="container">
        <h2 class="section__title">How a lesson works</h2>
        {_list(track["how_it_works"], "al-list")}
      </div>
    </section>

    <!-- Vad läraren behöver. -->
    <section class="section section--alt" id="al-need">
      <div class="container">
        <h2 class="section__title">What you need</h2>
        {_list(track["what_you_need"], "al-list")}
      </div>
    </section>

    <!-- Ramverk, vidare läsning, åldersgränser, läsarnot och användningsrätt. -->
    <section class="section" id="al-resources">
      <div class="container">
        <h2 class="section__title">Resources</h2>
        <h3 class="al-sub">Frameworks</h3>
        <p class="al-text">Every teacher guide maps its lesson to both frameworks.</p>
        <ul class="tm-sources">{frameworks}</ul>
        <h3 class="al-sub">Further reading</h3>
        {_further_reading(list(reading.values()))}
        <h3 class="al-sub">AI tools and age limits</h3>
        <p class="al-text">{escape(track["ai_use_note"])}</p>
        {_age_table(track, list(track["age_limits"]["tools"]))}
        <p class="tm-note">{escape(track["reader_note"])}</p>
        <p class="al-rights">{escape(track["use_rights"])}</p>
      </div>
    </section>
"""
        + FOOT
    )


# ───── Lärarsidan ─────

def _step(step: dict, start: int, n: int) -> str:
    """Ett steg i tidslinjen: nummer, minuter, arbetsform, vad läraren gör och vad hen kan säga."""
    end = start + step["minutes"]
    parts = [
        f'<li class="al-step{" al-step--demo" if step.get("demo") else ""}">',
        f'<p class="al-step__head"><span class="al-step__num">Step {n}</span><span class="al-step__time">{start}–{end} min</span>'
        f'<span class="al-mode al-mode--{step["mode"].lower()}">{escape(step["mode"])}</span></p>',
        f'<h3 class="al-step__title">{escape(step["title"])}</h3>',
        f'<p class="al-step__do">{escape(step["do"])}</p>',
    ]
    if step.get("say"):
        parts.append(f'<p class="al-say"><span class="al-say__label">Say</span> {escape(step["say"])}</p>')
    if step.get("prompts_in_order"):  # stegen hänvisar till prompt 1, 2 …, så de numreras
        parts.append('<p class="al-label">Prompts, in order</p><ol class="al-prompts">' + "".join(
            f"<li><strong>Prompt {n}:</strong> {escape(p)}</li>" for n, p in enumerate(step["prompts"], start=1)) + "</ol>")
    elif step.get("prompts"):
        parts.append('<p class="al-label">Prompts to try (pick one)</p>'
                     + _list(step["prompts"], "al-prompts"))
    if step.get("fallback"):
        parts.append(f'<p class="al-fallback"><strong>If the demo does not go as planned:</strong> {escape(step["fallback"])}</p>')
    parts.append("</li>")
    return "".join(parts)


def render_lesson(track: dict, lesson: dict) -> str:
    band = _band(track, lesson["band"])
    starts = [sum(s["minutes"] for s in lesson["steps"][:i]) for i in range(len(lesson["steps"]))]
    steps = "".join(_step(s, t, n) for n, (s, t) in enumerate(zip(lesson["steps"], starts), start=1))
    words = "".join(f"<dt>{escape(k['word'])}</dt><dd>{escape(k['meaning'])}</dd>" for k in lesson["key_words"])
    gather = "".join(
        f'<li><p class="al-gather__q">{escape(g["question"])}</p>'
        f'<p class="al-label">Students often say</p>{_list(g["students_say"], "al-said")}</li>'
        for g in lesson["gather"]
    )
    background = "".join(f'<p class="al-text">{escape(p)}</p>' for p in lesson["background"])
    frameworks = "".join(f'<p class="al-text"><a href="{escape(f["url"])}"><strong>{escape(f["name"])}</strong></a>: '
                         f'{escape(lesson["frameworks"][f["name"]])}</p>' for f in track["frameworks"])
    example = ""
    if "training_text" in lesson:  # lektioner med en träningstext visar det engelska exemplet
        example = f"""
        <p class="al-label">The English example (page 1 of the PDF)</p>
        <blockquote class="al-example">{escape(lesson["training_text"])}</blockquote>
        <p class="al-text"><strong>Starting words:</strong> {escape(", ".join(lesson["starting_words"]))}</p>"""
    language = f"""
    <!-- Byta språk: hur läraren gör elevmaterialet till klassens språk. -->
    <section class="section section--alt" id="al-language">
      <div class="container">
        <h2 class="section__title">Teaching in another language</h2>
        <p class="al-text">{escape(lesson["language_swap"])}</p>{example}
      </div>
    </section>
"""
    credits = ""
    if lesson["credits"]:  # källor och licenser, t.ex. ISTE (CC BY 4.0) och kortbilderna
        credits = '<h3 class="al-sub">Credits</h3><ul class="tm-sources">' + "".join(
            f'<li><a href="{escape(c["url"])}">{escape(c["text"])}</a></li>' for c in lesson["credits"]) + "</ul>"
    if lesson["tools"]:
        age = f'<p class="al-text">{escape(lesson["age_note"])}</p>\n        ' + _age_table(track, lesson["tools"])
    else:  # ingen tom tabell när lektionen inte använder något AI-verktyg
        age = ('<p class="al-text">This lesson uses no AI tool. Students don\'t use one, and you don\'t show one.</p>\n'
               f'        <p class="al-text">{escape(lesson["age_note"])}</p>')
    return (
        HEAD.format(title=escape(lesson["title"]), description=escape(lesson["line"]))
        + f"""    <!-- Hero: tillbaka till översikten, lektionens namn och en rad om vad eleverna gör. -->
    <section class="page-hero container">
      <a class="tm-back" href="/{track["slug"]}/">← {escape(track["title"])}</a>
      <span class="eyebrow">{escape(band["ages"])} · Lesson {lesson["number"]}</span>
      <h1>{escape(lesson["title"])}</h1>
      <p class="lede">{escape(lesson["line"])}</p>
    </section>

    <!-- Lektionen i korthet, materialet och elev-PDF:en. -->
    <section class="section section--alt" id="al-glance">
      <div class="container">
        <h2 class="section__title">At a glance</h2>
        <dl class="al-glance">
          <div><dt>Ages</dt><dd>{escape(band["ages"].replace("Ages ", ""))}</dd></div>
          <div><dt>Time</dt><dd>{lesson["minutes"]} min</dd></div>
          <div><dt>Groups</dt><dd>{escape(lesson["groups"])}</dd></div>
          <div><dt>AI use</dt><dd>{escape(AI_USE[lesson["ai_use"]])}</dd></div>
          <div><dt>Preparation</dt><dd>{lesson["prep_minutes"]} min</dd></div>
        </dl>
        <h3 class="al-sub">Materials</h3>
        {_list(lesson["materials"], "al-list")}
        <a class="btn btn--primary al-download" href="{pdf_url(track, lesson)}" download>Download the student PDF</a>
      </div>
    </section>

    <!-- Lärandemål och nyckelord med elevvänliga förklaringar. -->
    <section class="section" id="al-goals">
      <div class="container">
        <h2 class="section__title">Learning goals</h2>
        <p class="al-text">By the end of the lesson, students can:</p>
        {_list(lesson["goals"], "al-list")}
        <h3 class="al-sub">Key words</h3>
        <dl class="al-words">{words}</dl>
      </div>
    </section>

    <!-- Förberedelser: vad läraren skriver ut, skriver och provar före lektionen. -->
    <section class="section section--alt" id="al-before">
      <div class="container">
        <h2 class="section__title">Before the lesson</h2>
        <p class="al-text">About {lesson["prep_minutes"]} minutes.</p>
        {_list(lesson["before"], "al-list")}
      </div>
    </section>

    <!-- Steg för steg: minut för minut, varje steg enskilt, i par eller alla. -->
    <section class="section" id="al-steps">
      <div class="container">
        <h2 class="section__title">Step by step</h2>
        <ol class="al-steps">{steps}</ol>
      </div>
    </section>

    <!-- Uppsamling i helklass: frågor och vad elever brukar svara. -->
    <section class="section section--alt" id="al-gather">
      <div class="container">
        <h2 class="section__title">Gather it up</h2>
        <p class="al-text">Questions for the whole-class talk, with answers students often give.</p>
        <ul class="al-gather">{gather}</ul>
      </div>
    </section>

    <!-- Enklare och svårare varianter. -->
    <section class="section" id="al-adapt">
      <div class="container">
        <h2 class="section__title">Make it simpler, make it harder</h2>
        <div class="al-adapt">
          <div><h3 class="al-sub">Simpler</h3><p class="al-text">{escape(lesson["simpler"])}</p></div>
          <div><h3 class="al-sub">Harder</h3><p class="al-text">{escape(lesson["harder"])}</p></div>
        </div>
      </div>
    </section>

    <!-- Avslutande fråga (exit ticket) som varje elev svarar på. -->
    <section class="section section--alt" id="al-closing">
      <div class="container">
        <h2 class="section__title">Closing question</h2>
        <p class="al-closing">{escape(lesson["closing_question"])}</p>
      </div>
    </section>
{language}
    <!-- Bakgrund för läraren: två minuters läsning. -->
    <section class="section" id="al-background">
      <div class="container">
        <h2 class="section__title">Background for you</h2>
        {background}
      </div>
    </section>

    <!-- Koppling till ramverken AILit och AI4K12. -->
    <section class="section section--alt" id="al-frameworks">
      <div class="container">
        <h2 class="section__title">Framework links</h2>
        {frameworks}
      </div>
    </section>

    <!-- Åldersgränser för verktygen lektionen nämner, och läsarnoten (globala regler). -->
    <section class="section" id="al-age">
      <div class="container">
        <h2 class="section__title">AI tools and age limits</h2>
        {age}
        <p class="tm-note">{escape(track["reader_note"])}</p>
      </div>
    </section>

    <!-- Källor, vidare läsning och vad medlemmar får göra med materialet. -->
    <section class="section section--alt" id="al-credits">
      <div class="container">
        <h2 class="section__title">Sources and use</h2>
        {credits}
        <h3 class="al-sub">Further reading</h3>
        {_further_reading(lesson["further_reading"])}
        <p class="al-rights">{escape(track["use_rights"])}</p>
      </div>
    </section>
"""
        + FOOT
    )


def _write(path: Path, html: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else None
    path.write_text(keep_seo_block(old, html), encoding="utf-8")


def build(root: Path = ROOT) -> None:
    for slug in TRACKS:
        track = load_track(root, slug)
        _write(root / slug / "index.html", render_overview(track))
        for lesson in track["lesson_data"]:
            _write(root / slug / lesson["id"] / "index.html", render_lesson(track, lesson))
        print(f"Built {slug}: overview and {len(track['lesson_data'])} lesson page(s)")


if __name__ == "__main__":
    build(ROOT)
