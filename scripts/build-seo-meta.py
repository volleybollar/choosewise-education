#!/usr/bin/env python3
# Inject canonical, hreflang, and per-page JSON-LD into every page,
# inject a visible "Last updated" stamp on section landings, and emit
# a complete sitemap.xml. Idempotent — re-running replaces any block
# previously emitted by this script (delimited by SEO_MARK_*).

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://choosewise.education"
SEO_MARK_START = "<!-- seo:start (build-seo-meta.py) -->"
SEO_MARK_END = "<!-- seo:end -->"
LU_MARK_START = "<!-- last-updated:start (build-seo-meta.py) -->"
LU_MARK_END = "<!-- last-updated:end -->"

# -- Pair map: EN canonical-path -> SV canonical-path
PAIR_MAP = {
    "/": "/sv/",
    "/wise/": "/sv/ratt/",
    "/presentation-skills/": "/sv/presentationsteknik/",
    "/guides/": "/sv/guider/",
    "/prompts/": "/sv/promptar/",
    "/notebooklm-styles/": "/sv/notebooklm-stilar/",
    "/blog/": "/sv/blog/",
    "/about/": "/sv/om/",
    "/guides/claude/": "/sv/guider/claude/",
    "/guides/gemini-notebooklm/": "/sv/guider/gemini-notebooklm/",
    "/guides/apple-intelligence/": "/sv/guider/apple-intelligence/",
    "/guides/copilot/": "/sv/guider/copilot/",
    "/guides/ai-for-students/": "/sv/guider/ai-for-elever/",
    "/blog/posts/why-i-built-choosewise-education.html":
        "/sv/blog/posts/varfor-jag-byggt-choosewise-education.html",
    "/prompts/after-school-care/": "/sv/promptar/fritids/",
    "/prompts/art/": "/sv/promptar/bild/",
    "/prompts/biology/": "/sv/promptar/biologi/",
    "/prompts/career-counselors/": "/sv/promptar/syv/",
    "/prompts/chemistry/": "/sv/promptar/kemi/",
    "/prompts/crafts/": "/sv/promptar/slojd/",
    "/prompts/cross-curricular/": "/sv/promptar/amnesovergripande/",
    "/prompts/digital-tools/": "/sv/promptar/digitala-verktyg/",
    "/prompts/district-administrators/": "/sv/promptar/admin-central/",
    "/prompts/district-it-managers/": "/sv/promptar/it-ansvariga-central/",
    "/prompts/early-numeracy/": "/sv/promptar/lara-sig-rakna/",
    "/prompts/edtech-coaches/": "/sv/promptar/ikt-pedagoger/",
    "/prompts/education-strategists/": "/sv/promptar/strateger/",
    "/prompts/english/": "/sv/promptar/engelska/",
    "/prompts/english-upper-secondary/": "/sv/promptar/engelska-gymnasiet/",
    "/prompts/geography/": "/sv/promptar/geografi/",
    "/prompts/history/": "/sv/promptar/historia/",
    "/prompts/history-upper-secondary/": "/sv/promptar/historia-gymnasiet/",
    "/prompts/home-economics/": "/sv/promptar/hkk/",
    "/prompts/lead-teachers/": "/sv/promptar/forstelarare/",
    "/prompts/learning-new-skills/": "/sv/promptar/lar-dig-nya-saker/",
    "/prompts/mathematics/": "/sv/promptar/matematik/",
    "/prompts/mathematics-upper-secondary/": "/sv/promptar/matematik-gymnasiet/",
    "/prompts/megaprompts-1/": "/sv/promptar/megapromptar-1/",
    "/prompts/megaprompts-2/": "/sv/promptar/megapromptar-2/",
    "/prompts/megaprompts-3/": "/sv/promptar/megapromptar-3/",
    "/prompts/modern-languages/": "/sv/promptar/moderna-sprak/",
    "/prompts/modern-languages-upper-secondary/": "/sv/promptar/moderna-sprak-gymnasiet/",
    "/prompts/music/": "/sv/promptar/musik/",
    "/prompts/outdoor-education/": "/sv/promptar/utomhuspedagogik/",
    "/prompts/physical-education/": "/sv/promptar/idh/",
    "/prompts/physical-education-upper-secondary/": "/sv/promptar/idh-gymnasiet/",
    "/prompts/physics/": "/sv/promptar/fysik/",
    "/prompts/preschool/": "/sv/promptar/forskola/",
    "/prompts/principals/": "/sv/promptar/rektorer/",
    "/prompts/reception/": "/sv/promptar/forskoleklass/",
    "/prompts/religious-studies/": "/sv/promptar/religion/",
    "/prompts/religious-studies-upper-secondary/": "/sv/promptar/religion-gymnasiet/",
    "/prompts/research-on-learning/": "/sv/promptar/studier-om-larande/",
    "/prompts/school-administrators/": "/sv/promptar/administratorer/",
    "/prompts/school-caretakers/": "/sv/promptar/skolvaktmastare/",
    "/prompts/school-catering-staff/": "/sv/promptar/skolmaltidspersonal/",
    "/prompts/school-counselors/": "/sv/promptar/kuratorer/",
    "/prompts/school-it-managers/": "/sv/promptar/it-ansvariga-skola/",
    "/prompts/school-librarians/": "/sv/promptar/skolbibliotekarier/",
    "/prompts/school-nurses/": "/sv/promptar/skolskoterskor/",
    "/prompts/school-psychologists/": "/sv/promptar/skolpsykologer/",
    "/prompts/social-studies/": "/sv/promptar/samhallskunskap/",
    "/prompts/social-studies-general/": "/sv/promptar/so/",
    "/prompts/social-studies-upper-secondary/": "/sv/promptar/samhallskunskap-gymnasiet/",
    "/prompts/special-education-specialists/": "/sv/promptar/specialpedagoger/",
    "/prompts/special-education-teachers/": "/sv/promptar/speciallarare/",
    "/prompts/student-assistants/": "/sv/promptar/elevassistenter/",
    "/prompts/superintendents/": "/sv/promptar/skolchefer/",
    "/prompts/teachers/": "/sv/promptar/larare/",
    "/prompts/technology/": "/sv/promptar/teknik/",
    "/prompts/time-management/": "/sv/promptar/tidsutnyttjande/",
}
SV_TO_EN = {sv: en for en, sv in PAIR_MAP.items()}

# Section landings get visible "Last updated" + WebPage / CollectionPage / AboutPage schema
SECTION_LANDINGS = {
    "/wise/":               "WebPage",
    "/sv/ratt/":            "WebPage",
    "/guides/":             "CollectionPage",
    "/sv/guider/":          "CollectionPage",
    "/prompts/":            "CollectionPage",
    "/sv/promptar/":        "CollectionPage",
    "/notebooklm-styles/":  "CollectionPage",
    "/sv/notebooklm-stilar/": "CollectionPage",
    "/about/":              "AboutPage",
    "/sv/om/":              "AboutPage",
}

LAST_UPDATED_LABEL = {
    "en": "Last updated",
    "sv": "Senast uppdaterad",
}

# Pages to skip (templates, admin, brainstorm dumps, etc.)
EXCLUDE_DIR_PARTS = {".git", ".superpowers", ".playwright-mcp", "exports",
                     "node_modules", "scripts", "assets/partials"}
EXCLUDE_FILES = {
    "blog/post.html",
    "sv/blog/post.html",
    "research-presentation.html",
    "wise-framework.html",
    "ratt-modellen.html",
    "404.html",
}


def is_excluded(rel_path: str) -> bool:
    parts = Path(rel_path).parts
    for ex in EXCLUDE_DIR_PARTS:
        ex_parts = ex.split("/")
        for i in range(len(parts) - len(ex_parts) + 1):
            if list(parts[i:i+len(ex_parts)]) == ex_parts:
                return True
    return rel_path in EXCLUDE_FILES


def path_to_canonical(rel_path: str) -> str:
    if rel_path == "index.html":
        return "/"
    if rel_path.endswith("/index.html"):
        return "/" + rel_path[:-len("index.html")]
    return "/" + rel_path


def detect_lang(rel_path: str, html: str) -> str:
    if rel_path.startswith("sv/") or rel_path == "sv/index.html":
        return "sv"
    m = re.search(r'<html[^>]*\blang="([^"]+)"', html)
    if m:
        return m.group(1).lower().split("-")[0]
    return "en"


def get_pair(canonical_path: str):
    if canonical_path in PAIR_MAP:
        return PAIR_MAP[canonical_path]
    if canonical_path in SV_TO_EN:
        return SV_TO_EN[canonical_path]
    return None


# ---- Blog manifest lookup ----

def load_blog_manifest():
    posts = {}
    for manifest_path, base in [
        (ROOT / "blog/posts-en.json", "/blog/posts/"),
        (ROOT / "sv/blog/posts-sv.json", "/sv/blog/posts/"),
    ]:
        if not manifest_path.exists():
            continue
        for entry in json.loads(manifest_path.read_text()):
            url = base + entry["slug"] + ".html"
            posts[url] = entry
    return posts


BLOG_POSTS = load_blog_manifest()


# ---- FAQ extraction ----

# Match <details class="faq-item">...<summary>Q?</summary>...<p>A</p>...</details>
RE_FAQ_DETAILS = re.compile(
    r'<details[^>]*\bclass="[^"]*\bfaq-item\b[^"]*"[^>]*>(.*?)</details>',
    re.DOTALL | re.IGNORECASE)
RE_SUMMARY = re.compile(r'<summary[^>]*>(.*?)</summary>', re.DOTALL | re.IGNORECASE)
RE_BODY_TAG = re.compile(r'<(p|div)[^>]*>(.*?)</\1>', re.DOTALL | re.IGNORECASE)


def strip_tags(s: str) -> str:
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()


def extract_faqs(html_body: str):
    """Return list of {question, answer} from <details class="faq-item">."""
    out = []
    for m in RE_FAQ_DETAILS.finditer(html_body):
        block = m.group(1)
        sm = RE_SUMMARY.search(block)
        if not sm:
            continue
        q = strip_tags(sm.group(1))
        # Take everything after </summary> as the answer
        post_summary = block[sm.end():]
        a = strip_tags(post_summary)
        if q and a:
            out.append({"question": q, "answer": a})
    return out


# ---- Build entities ----

def build_organization():
    return {
        "@type": "Organization",
        "@id": f"{BASE_URL}/#organization",
        "name": "choosewise.education",
        "url": f"{BASE_URL}/",
        "description": ("Independent education resource on AI in schools. "
                        "The WISE Framework for Education, guides, and prompts "
                        "for teachers and school leaders."),
        "founder": {"@id": f"{BASE_URL}/#johan"},
        "sameAs": [
            "https://www.linkedin.com/in/johan-lindstrom/",
            "https://jlsu.se/",
        ],
    }


def build_website():
    return {
        "@type": "WebSite",
        "@id": f"{BASE_URL}/#website",
        "url": f"{BASE_URL}/",
        "name": "choosewise.education",
        "publisher": {"@id": f"{BASE_URL}/#organization"},
        "inLanguage": ["en", "sv"],
    }


def build_person():
    return {
        "@type": "Person",
        "@id": f"{BASE_URL}/#johan",
        "name": "Johan Lindström",
        "jobTitle": "Education consultant and author",
        "url": f"{BASE_URL}/about/",
        "sameAs": [
            "https://www.linkedin.com/in/johan-lindstrom/",
            "https://jlsu.se/",
        ],
        "knowsAbout": [
            "AI in education",
            "EU AI Act",
            "School digitalization",
            "Pedagogical leadership",
            "Educational technology",
            "Source criticism",
            "Prompt engineering for education",
        ],
        "worksFor": {"@id": f"{BASE_URL}/#organization"},
        "knowsLanguage": ["sv", "en"],
        "description": ("Swedish education consultant with 28 years in schools "
                        "(10 as teacher, 7 as school leader, 11 in EdTech). "
                        "Recognized voice on AI and digitalization in Swedish education."),
    }


def build_article(canonical_path: str, post: dict, lang: str, last_modified: str):
    url = BASE_URL + canonical_path
    image = post.get("og_image") or post.get("cover_image")
    return {
        "@type": "Article",
        "@id": f"{url}#article",
        "headline": post["title"],
        "description": post.get("excerpt", ""),
        "image": (BASE_URL + image) if image else None,
        "author": {"@id": f"{BASE_URL}/#johan"},
        "publisher": {"@id": f"{BASE_URL}/#organization"},
        "datePublished": post["date"],
        "dateModified": last_modified,
        "inLanguage": lang,
        "isPartOf": {"@id": f"{BASE_URL}/#website"},
        "mainEntityOfPage": url,
    }


def build_webpage(canonical_path: str, page_type: str, lang: str, last_modified: str):
    url = BASE_URL + canonical_path
    return {
        "@type": page_type,
        "@id": f"{url}#webpage",
        "url": url,
        "isPartOf": {"@id": f"{BASE_URL}/#website"},
        "inLanguage": lang,
        "dateModified": last_modified,
        "about": {"@id": f"{BASE_URL}/#organization"},
        "primaryImageOfPage": None,  # filled later if og:image found
    }


def build_faqpage(canonical_path: str, faqs: list):
    return {
        "@type": "FAQPage",
        "@id": f"{BASE_URL}{canonical_path}#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f["question"],
                "acceptedAnswer": {"@type": "Answer", "text": f["answer"]},
            }
            for f in faqs
        ],
    }


# ---- HTML rewriting ----

def build_seo_block(canonical_path: str, lang: str, html: str,
                    last_modified: str) -> str:
    canonical_url = BASE_URL + canonical_path
    lines = [
        SEO_MARK_START,
        f'<link rel="canonical" href="{canonical_url}">',
    ]
    pair = get_pair(canonical_path)
    if pair:
        if lang == "en":
            en_path, sv_path = canonical_path, pair
        else:
            en_path, sv_path = pair, canonical_path
        en_url = BASE_URL + en_path
        sv_url = BASE_URL + sv_path
        lines += [
            f'<link rel="alternate" hreflang="en" href="{en_url}">',
            f'<link rel="alternate" hreflang="sv" href="{sv_url}">',
            f'<link rel="alternate" hreflang="x-default" href="{en_url}">',
        ]

    # Build @graph with site-wide entities + per-page entities
    graph = [build_organization(), build_website(), build_person()]

    # Article (blog post)
    if canonical_path in BLOG_POSTS:
        graph.append(build_article(canonical_path, BLOG_POSTS[canonical_path],
                                    lang, last_modified))

    # WebPage / CollectionPage / AboutPage (section landing)
    if canonical_path in SECTION_LANDINGS:
        graph.append(build_webpage(canonical_path,
                                    SECTION_LANDINGS[canonical_path],
                                    lang, last_modified))

    # FAQPage (any page with <details class="faq-item">)
    faqs = extract_faqs(html)
    if faqs:
        graph.append(build_faqpage(canonical_path, faqs))

    payload = {"@context": "https://schema.org", "@graph": graph}
    # Drop None values from entities
    def clean(o):
        if isinstance(o, dict):
            return {k: clean(v) for k, v in o.items() if v is not None}
        if isinstance(o, list):
            return [clean(x) for x in o]
        return o
    payload = clean(payload)
    json_ld = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    lines.append(f'<script type="application/ld+json">{json_ld}</script>')
    lines.append(SEO_MARK_END)
    return "\n".join(lines)


def build_last_updated_block(lang: str, last_modified: str) -> str:
    label = LAST_UPDATED_LABEL.get(lang, "Last updated")
    # human-readable date in lang
    try:
        d = datetime.strptime(last_modified, "%Y-%m-%d")
        if lang == "sv":
            months = ["januari", "februari", "mars", "april", "maj", "juni",
                      "juli", "augusti", "september", "oktober", "november", "december"]
            human = f"{d.day} {months[d.month-1]} {d.year}"
        else:
            human = d.strftime("%B %-d, %Y")
    except Exception:
        human = last_modified
    return (f'{LU_MARK_START}\n'
            f'<aside class="page-last-updated" aria-label="{label}">'
            f'<p><span class="page-last-updated__label">{label}:</span> '
            f'<time datetime="{last_modified}">{human}</time></p></aside>\n'
            f'{LU_MARK_END}')


RE_OUR_BLOCK = re.compile(
    re.escape(SEO_MARK_START) + r'.*?' + re.escape(SEO_MARK_END) + r'\s*\n?',
    re.DOTALL)
RE_LU_BLOCK = re.compile(
    re.escape(LU_MARK_START) + r'.*?' + re.escape(LU_MARK_END) + r'\s*\n?',
    re.DOTALL)
RE_OLD_CANONICAL = re.compile(
    r'^[ \t]*<link[^>]*\brel=["\']canonical["\'][^>]*>\s*\n?', re.MULTILINE)
RE_OLD_HREFLANG = re.compile(
    r'^[ \t]*<link[^>]*\bhreflang=["\'][^"\']*["\'][^>]*>\s*\n?', re.MULTILINE)


def inject_head(html: str, block: str) -> str:
    html = RE_OUR_BLOCK.sub("", html)
    html = RE_OLD_CANONICAL.sub("", html)
    html = RE_OLD_HREFLANG.sub("", html)
    if "</head>" not in html:
        return html
    return html.replace("</head>", block + "\n</head>", 1)


def inject_last_updated(html: str, block: str) -> str:
    html = RE_LU_BLOCK.sub("", html)
    if "</main>" not in html:
        return html
    return html.replace("</main>", block + "\n  </main>", 1)


# ---- Sitemap ----

def git_lastmod(rel_path: str) -> str:
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%cI", "--", rel_path],
            cwd=ROOT, stderr=subprocess.DEVNULL, text=True).strip()
        if out:
            return out.split("T")[0]
    except Exception:
        pass
    p = ROOT / rel_path
    if p.exists():
        ts = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc)
        return ts.date().isoformat()
    return datetime.now(timezone.utc).date().isoformat()


def collect_html_files() -> list:
    files = []
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT).as_posix()
        if is_excluded(rel):
            continue
        files.append(rel)
    return sorted(files)


def main():
    dry_run = "--dry-run" in sys.argv
    files = collect_html_files()
    written = 0
    lu_written = 0
    pages_with_pair = 0

    for rel in files:
        path = ROOT / rel
        html = path.read_text(encoding="utf-8")
        canonical_path = path_to_canonical(rel)
        lang = detect_lang(rel, html)
        last_mod = git_lastmod(rel)

        block = build_seo_block(canonical_path, lang, html, last_mod)
        new_html = inject_head(html, block)

        # Visible Last updated only on section landings
        if canonical_path in SECTION_LANDINGS:
            lu_block = build_last_updated_block(lang, last_mod)
            new_html2 = inject_last_updated(new_html, lu_block)
            if new_html2 != new_html:
                lu_written += 1
            new_html = new_html2

        if new_html != html:
            if not dry_run:
                path.write_text(new_html, encoding="utf-8")
            written += 1
        if get_pair(canonical_path):
            pages_with_pair += 1

    print(f"Pages processed: {len(files)}, head updates: {written}, "
          f"last-updated injections: {lu_written}, dry_run={dry_run}")
    print(f"  with hreflang pair: {pages_with_pair}")
    print(f"  blog Articles emitted: "
          f"{sum(1 for f in files if path_to_canonical(f) in BLOG_POSTS)}")
    print(f"  section landings updated: "
          f"{sum(1 for f in files if path_to_canonical(f) in SECTION_LANDINGS)}")

    # ---- Generate sitemap.xml with hreflang ----
    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for f in files:
        canonical = path_to_canonical(f)
        url = BASE_URL + canonical
        lastmod = git_lastmod(f)
        pair = get_pair(canonical)
        sitemap_lines.append("  <url>")
        sitemap_lines.append(f"    <loc>{url}</loc>")
        sitemap_lines.append(f"    <lastmod>{lastmod}</lastmod>")
        if pair:
            this_lang = "sv" if canonical.startswith("/sv/") else "en"
            other = pair
            if this_lang == "en":
                en_url, sv_url = url, BASE_URL + other
            else:
                en_url, sv_url = BASE_URL + other, url
            sitemap_lines.append(
                f'    <xhtml:link rel="alternate" hreflang="en" href="{en_url}"/>')
            sitemap_lines.append(
                f'    <xhtml:link rel="alternate" hreflang="sv" href="{sv_url}"/>')
            sitemap_lines.append(
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{en_url}"/>')
        sitemap_lines.append("  </url>")
    sitemap_lines.append("</urlset>")
    sitemap = "\n".join(sitemap_lines) + "\n"

    sm_path = ROOT / "sitemap.xml"
    if not dry_run:
        sm_path.write_text(sitemap, encoding="utf-8")
    print(f"Sitemap urls: {len(files)} -> {sm_path}")


if __name__ == "__main__":
    main()
