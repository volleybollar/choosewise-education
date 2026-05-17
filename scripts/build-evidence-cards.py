#!/usr/bin/env python3
"""Build static skill cards for /evidence/<domain>/ pages from JSON data.

Reads evidence/data/<domain>.json and replaces the content between
<!-- cards:start --> and <!-- cards:end --> markers in
evidence/<domain>/index.html with the rendered card HTML.

Usage:
    python3 scripts/build-evidence-cards.py memory
    python3 scripts/build-evidence-cards.py --all
"""
from __future__ import annotations

import argparse
import json
import re
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "evidence" / "data"


def band_for_months(months):
    """Return 'below' / 'around' / 'above' / None for a months-of-progress value."""
    if months is None:
        return None
    if months <= 2:
        return "below"
    if months <= 4:
        return "around"
    return "above"


def band_for_d(d):
    """Return 'below' / 'around' / 'above' / None for a Cohen's d value."""
    if d is None:
        return None
    if d < 0.30:
        return "below"
    if d < 0.60:
        return "around"
    return "above"


def _months_pill(skill):
    months = skill.get("effect_months")
    band = band_for_months(months)
    if band is None:
        return (
            '<div class="metric-cell">'
            '<span class="metric-pill metric-pill--months band-none">no EEF strand</span>'
            '</div>'
        )
    src = skill.get("effect_months_source")
    yr = skill.get("effect_months_year")
    src_html = escape(src) if src else ""
    yr_html = f'<span class="metric-year">{yr}</span>' if yr else ""
    source_span = (
        f'<span class="metric-source">{src_html}{yr_html}</span>'
        if (src_html or yr_html) else ""
    )
    return (
        f'<div class="metric-cell">'
        f'<span class="metric-pill metric-pill--months band-{band}">+{months} months</span>'
        f'{source_span}'
        f'</div>'
    )


def _d_pill(skill):
    d = skill.get("effect_d")
    band = band_for_d(d)
    if band is None:
        return (
            '<div class="metric-cell">'
            '<span class="metric-pill metric-pill--d band-none">no independent meta-analysis found</span>'
            '</div>'
        )
    src = skill.get("effect_d_source")
    journal = skill.get("effect_d_journal")
    yr = skill.get("effect_d_year")
    source_parts = []
    if src:
        source_parts.append(escape(src))
    if journal:
        source_parts.append(f'<em>{escape(journal)}</em>')
    source_text = ", ".join(source_parts)
    yr_html = f'<span class="metric-year">{yr}</span>' if yr else ""
    source_span = (
        f'<span class="metric-source">{source_text}{yr_html}</span>'
        if (source_text or yr_html) else ""
    )
    return (
        f'<div class="metric-cell">'
        f'<span class="metric-pill metric-pill--d band-{band}">d = {d:.2f}</span>'
        f'{source_span}'
        f'</div>'
    )


def _impl_pill(skill):
    level = skill.get("implementation_cost")
    labels = {"low": "Low", "medium": "Medium", "high": "High"}
    if level not in labels:
        raise ValueError(
            f"implementation_cost must be one of {sorted(labels)}, got {level!r}"
        )
    return (
        f'<div class="metric-cell">'
        f'<span class="impl-pill impl-pill--{level}">{labels[level]}</span>'
        f'<span class="metric-source">Implementation</span>'
        f'</div>'
    )


def _tags_html(skill):
    tags = skill.get("tags") or []
    pills = "".join(f'<span class="skill-tag">{escape(t)}</span>' for t in tags)
    return f'<div class="skill-tags">{pills}</div>'


def render_card(skill, domain_label):
    """Render a single skill card as HTML."""
    title = escape(skill["display_title"])
    desc = escape(skill["description"])
    skill_id = escape(skill["id"])
    domain = escape(domain_label)
    return (
        f'<article class="skill-card" data-skill-id="{skill_id}">'
        f'  <div class="skill-domain">{domain}</div>'
        f'  <h3 class="skill-title">{title}</h3>'
        f'  <p class="skill-desc">{desc}</p>'
        f'  <div class="metric-block">'
        f'    {_months_pill(skill)}'
        f'    {_d_pill(skill)}'
        f'    {_impl_pill(skill)}'
        f'  </div>'
        f'  <footer class="skill-footer">'
        f'    {_tags_html(skill)}'
        f'    <button class="skill-action" data-action="interrogate" data-skill-id="{skill_id}">'
        f'      Interrogate <span aria-hidden="true">→</span>'
        f'    </button>'
        f'  </footer>'
        f'</article>'
    )


CARDS_PATTERN = re.compile(
    r"(<!--\s*cards:start\s*-->)(.*?)(<!--\s*cards:end\s*-->)",
    re.DOTALL,
)


def inject_into_template(template, new_content):
    """Replace content between cards:start / cards:end markers."""
    if not CARDS_PATTERN.search(template):
        raise ValueError(
            "Template missing required <!-- cards:start --> and <!-- cards:end --> markers."
        )
    return CARDS_PATTERN.sub(
        lambda m: f"{m.group(1)}\n{new_content}\n{m.group(3)}",
        template,
    )


def build_domain(domain_slug: str) -> None:
    """Build cards for one domain and write them into the page template."""
    data_file = DATA_DIR / f"{domain_slug}.json"
    page_file = ROOT / "evidence" / domain_slug / "index.html"
    if not data_file.exists():
        raise SystemExit(f"Data file not found: {data_file}")
    if not page_file.exists():
        raise SystemExit(f"Page file not found: {page_file}")

    data = json.loads(data_file.read_text(encoding="utf-8"))
    domain_label = data["domain_label"]
    cards_html = "\n".join(
        render_card(skill, domain_label=domain_label) for skill in data["skills"]
    )

    template = page_file.read_text(encoding="utf-8")
    new_html = inject_into_template(template, cards_html)
    page_file.write_text(new_html, encoding="utf-8")
    print(f"Built {len(data['skills'])} cards into {page_file.relative_to(ROOT)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("domain", nargs="?", help="Domain slug (e.g. 'memory')")
    parser.add_argument("--all", action="store_true", help="Build all domains in evidence/data/")
    args = parser.parse_args()

    if args.all:
        for data_file in sorted(DATA_DIR.glob("*.json")):
            build_domain(data_file.stem)
    elif args.domain:
        build_domain(args.domain)
    else:
        parser.print_help()
        raise SystemExit(2)
