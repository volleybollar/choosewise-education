#!/usr/bin/env python3
"""Pre-render each blog post as a static HTML file with proper OG metadata.

Why static: social media crawlers (LinkedIn, X, Facebook) do not execute
JavaScript when scraping a page for sharing previews. The dynamic
/blog/post.html?slug=… renderer therefore can't deliver per-post OG
images; every share would show the default site card. This script
produces /<lang>/blog/posts/<slug>.html files with the OG metadata
baked into <head> and the markdown content rendered into the body —
so every post gets its own preview card on every social platform.

Usage:
    python3 scripts/build-blog-posts.py

Reads:
    blog/posts-en.json    + blog/posts/<slug>.md     → blog/posts/<slug>.html
    sv/blog/posts-sv.json + sv/blog/posts/<slug>.md  → sv/blog/posts/<slug>.html

Each post entry in the JSON manifest may include `og_image` (recommended:
1200×630 JPG generated via `optimize-image.py --og`); falls back to
`cover_image` if omitted.

Idempotent: rewrites every <slug>.html on each run, even if the source
hasn't changed. Cheap to re-run after every edit.
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("Python 'markdown' package required. Install: pip3 install --user markdown")


ROOT = Path(__file__).parent.parent
SITE_URL = "https://choosewise.education"

LANGS = [
    {
        "code": "en",
        "html_lang": "en",
        "manifest": ROOT / "blog/posts-en.json",
        "posts_dir": ROOT / "blog/posts",
        "header_partial": "/assets/partials/header-en.html",
        "footer_partial": "/assets/partials/footer-en.html",
        "back_label": "← All posts",
        "back_url": "/blog/",
        "site_name": "choosewise.education",
    },
    {
        "code": "sv",
        "html_lang": "sv",
        "manifest": ROOT / "sv/blog/posts-sv.json",
        "posts_dir": ROOT / "sv/blog/posts",
        "header_partial": "/assets/partials/header-sv.html",
        "footer_partial": "/assets/partials/footer-sv.html",
        "back_label": "← Alla inlägg",
        "back_url": "/sv/blog/",
        "site_name": "choosewise.education",
    },
]


def render_post(meta: dict, body_html: str, lang: dict) -> str:
    """Build a complete static HTML page for one post."""
    title = meta["title"]
    excerpt = meta.get("excerpt", "")
    date = meta["date"]
    reading_time = meta.get("reading_time", "")
    cover = meta.get("cover_image")
    og_image_path = meta.get("og_image") or cover or "/assets/images/brand/og-default.svg"
    og_image_url = SITE_URL + og_image_path
    canonical = f"{SITE_URL}/{lang['posts_dir'].relative_to(ROOT).as_posix()}/{meta['slug']}.html"
    page_title = f"{title} — {lang['site_name']}"

    cover_html = (
        f'<img class="post__cover" src="{html.escape(cover)}" alt="" loading="eager" decoding="async">'
        if cover else ''
    )
    eyebrow_text = html.escape(date) + (f' · {html.escape(reading_time)}' if reading_time else '')

    return f"""<!DOCTYPE html>
<html lang="{lang['html_lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(page_title)}</title>
<meta name="description" content="{html.escape(excerpt)}">
<link rel="canonical" href="{canonical}">

<!-- Open Graph (LinkedIn, Facebook) -->
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(excerpt)}">
<meta property="og:image" content="{og_image_url}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{lang['site_name']}">
<meta property="article:published_time" content="{date}">

<!-- Twitter / X -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(excerpt)}">
<meta name="twitter:image" content="{og_image_url}">

<link rel="stylesheet" href="/assets/css/fonts.css">
<link rel="stylesheet" href="/assets/css/tokens.css">
<link rel="stylesheet" href="/assets/css/base.css">
<link rel="stylesheet" href="/assets/css/components.css">
<link rel="stylesheet" href="/assets/css/pages.css">
</head>
<body>
<div data-include="{lang['header_partial']}"></div>

<main class="container">
  <article class="post">
    <header class="post__header">
      {cover_html}
      <h1>{html.escape(title)}</h1>
      <span class="eyebrow">{eyebrow_text}</span>
    </header>
    <div class="post__body prose">
{body_html}
    </div>
    <footer class="post__footer">
      <a class="btn btn--ghost" href="{lang['back_url']}">{lang['back_label']}</a>
    </footer>
  </article>
</main>

<div data-include="{lang['footer_partial']}"></div>
<script defer src="/assets/js/include.js"></script>
</body>
</html>
"""


def main() -> None:
    md_engine = markdown.Markdown(extensions=["extra", "smarty"])
    total = 0
    for lang in LANGS:
        if not lang["manifest"].exists():
            continue
        manifest_data = json.loads(lang["manifest"].read_text())
        for meta in manifest_data:
            slug = meta["slug"]
            md_path = lang["posts_dir"] / f"{slug}.md"
            if not md_path.exists():
                print(f"  WARN: {md_path.relative_to(ROOT)} not found, skipping")
                continue
            md_content = md_path.read_text()
            body_html = md_engine.reset().convert(md_content)
            html_out = render_post(meta, body_html, lang)
            out_path = lang["posts_dir"] / f"{slug}.html"
            out_path.write_text(html_out)
            kb = len(html_out) // 1024
            print(f"  ✓ {out_path.relative_to(ROOT)} ({kb} KB)")
            total += 1
    print(f"\nDone. Rendered {total} post(s).")


if __name__ == "__main__":
    main()
