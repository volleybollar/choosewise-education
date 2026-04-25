#!/usr/bin/env python3
"""Refresh the "Five sample prompts" / "Fem exempel" section on every prompt-pack
landing page (sv/promptar/<slug>/index.html and prompts/<slug>/index.html).

Picks 5 prompts evenly spread across the pack's full prompt list (so visitors
see the breadth before downloading) and renders them with bracketed
placeholders highlighted via <em>. Megaprompt pages are skipped — they have
their own structure.

Idempotent: cleans up any previous standalone or inline-block sample sections
before inserting fresh ones.

Usage:
    python3 scripts/refresh-prompt-pack-samples.py            # all packs
    python3 scripts/refresh-prompt-pack-samples.py tidsutnyttjande   # one slug
"""
import os
import re
import json
import html
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "exports/prompts/data"

LANG_CONFIG = {
    "sv": {
        "page_dir": ROOT / "sv/promptar",
        "data_suffix": "",
        "heading": "Fem exempel på promptar från den här promptsamlingen",
        "lede": "Varje prompt är en mall med hakparenteser <em>[byt ut den här texten]</em> som du byter ut mot din egen kontext.",
        "after_heading": "Så här använder du dem",
    },
    "en": {
        "page_dir": ROOT / "prompts",
        "data_suffix": "-en",
        "heading": "Five sample prompts from this prompt pack",
        "lede": "Every prompt is a template with bracketed placeholders <em>[replace this text]</em> that you swap for your own context.",
        "after_heading": "How to use them",
    },
}

# Earlier versions used these heading variants — kept here so cleanup stays
# idempotent across iterations.
LEGACY_HEADINGS = {
    "sv": ["Fem exempel ur paketet"],
    "en": ["Five sample prompts"],
}


def pick_indices(total):
    if total <= 5:
        return list(range(total))
    return [round(i * (total - 1) / 4) for i in range(5)]


def flatten_prompts(data):
    out = []
    for part in data.get("parts", []):
        for p in part.get("prompts", []):
            text = p if isinstance(p, str) else p.get("text", "")
            out.append(text)
    return out


def wrap_brackets(text):
    escaped = html.escape(text)
    return re.sub(r"\[([^\[\]]+)\]", r"<em>[\1]</em>", escaped)


def build_section(prompts, cfg):
    items = "\n".join(
        f"        <li>{wrap_brackets(text)}</li>" for text in prompts
    )
    return (
        '    <section class="section container section--flush-top section--flush-bottom" data-reveal>\n'
        f'      <h2 class="section__title">{cfg["heading"]}</h2>\n'
        f'      <p class="prose">{cfg["lede"]}</p>\n'
        '      <ol class="example-prompts">\n'
        f"{items}\n"
        "      </ol>\n"
        "    </section>\n\n"
    )


def remove_standalone_sections(html_src, cfg, lang):
    headings = [cfg["heading"]] + LEGACY_HEADINGS.get(lang, [])
    for h in headings:
        pattern = re.compile(
            r"    <section class=\"section container[^\"]*\" data-reveal>\s*\n"
            r"\s*<h2 class=\"section__title\">"
            + re.escape(h)
            + r"</h2>.*?</section>\s*\n\s*\n",
            re.DOTALL,
        )
        html_src = pattern.sub("", html_src)
    return html_src


def remove_inline_block(html_src, cfg, lang):
    headings = [cfg["heading"]] + LEGACY_HEADINGS.get(lang, [])
    for h in headings:
        pattern = re.compile(
            r"\n      <div class=\"section-block\">\s*\n"
            r"\s*<h2 class=\"section__title\">"
            + re.escape(h)
            + r"</h2>.*?</div>\n    ",
            re.DOTALL,
        )
        html_src = pattern.sub("", html_src)
    return html_src


def insert_section_before_after_heading(html_src, section, after_heading):
    pattern = re.compile(
        r'(    <section class="section container(?: [^"]+)?" data-reveal>\s*\n\s*<h2 class="section__title">'
        + re.escape(after_heading)
        + r"</h2>)",
        re.MULTILINE,
    )
    m = pattern.search(html_src)
    if not m:
        return None
    return html_src[: m.start()] + section + html_src[m.start():]


def strip_flush_top_from_after_section(html_src, after_heading):
    return re.sub(
        r'(    <section class="section container) section--flush-top(" data-reveal>\s*\n\s*<h2 class="section__title">'
        + re.escape(after_heading)
        + r"</h2>)",
        r"\1\2",
        html_src,
    )


def process_page(lang, slug):
    cfg = LANG_CONFIG[lang]
    page_path = cfg["page_dir"] / slug / "index.html"
    data_path = DATA / f"{slug}{cfg['data_suffix']}.json"

    if not page_path.exists():
        return False, "HTML saknas"
    if not data_path.exists():
        return False, "JSON saknas"

    with open(data_path) as f:
        data = json.load(f)

    all_prompts = flatten_prompts(data)
    if not all_prompts:
        return False, "Inga promptar"

    indices = pick_indices(len(all_prompts))
    selected = [all_prompts[i] for i in indices]

    with open(page_path) as f:
        src = f.read()

    src = remove_inline_block(src, cfg, lang)
    src = remove_standalone_sections(src, cfg, lang)
    src = strip_flush_top_from_after_section(src, cfg["after_heading"])

    new_section = build_section(selected, cfg)
    result = insert_section_before_after_heading(src, new_section, cfg["after_heading"])
    if result is None:
        return False, f'Hittade inte "{cfg["after_heading"]}"-sektionen'

    with open(page_path, "w") as f:
        f.write(result)
    return True, f"{len(all_prompts)} promptar -> {[i+1 for i in indices]}"


def main():
    targets = []
    for lang, cfg in LANG_CONFIG.items():
        if not cfg["page_dir"].exists():
            continue
        for d in sorted(os.listdir(cfg["page_dir"])):
            full = cfg["page_dir"] / d
            if not full.is_dir():
                continue
            if d.startswith("megaprompt"):
                continue
            targets.append((lang, d))

    only = sys.argv[1] if len(sys.argv) > 1 else None
    ok = fail = 0
    for lang, slug in targets:
        if only and only not in f"{lang}/{slug}":
            continue
        success, msg = process_page(lang, slug)
        status = "OK" if success else "FAIL"
        print(f"[{status}] {lang}/{slug}: {msg}")
        if success:
            ok += 1
        else:
            fail += 1
    print(f"\nTotalt: {ok} OK, {fail} FAIL")


if __name__ == "__main__":
    main()
