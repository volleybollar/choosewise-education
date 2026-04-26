# SEO + AI-citation optimization plan for choosewise.education

**Date drafted:** 2026-04-25
**Status:** Approved approach, implementation pending — Johan asked to save and execute later
**Source inputs:**
1. The AI Citation Hunter's Playbook (Yogesh Agarwal, marketing PDF on Desktop) — distilled the 4 citation triggers + filtered out the WP-plugin sales fluff
2. Local site audit (technical state at 2026-04-25)
3. Independent research synthesis (April 2026 best practices) — sources catalogued at end

---

## The 4 citation triggers (PDF, validated by 2026 research)

1. **Extractability** — can an AI engine pull a clean standalone answer in <2 sec? 50–80-word answer block under question-style H2.
2. **Entity Clarity** — Organization schema, Person schema for authors, About pages declaring expertise. Strong author entity can beat a stronger domain.
3. **Crawler Accessibility** — GPTBot, ClaudeBot, PerplexityBot etc. must reach pages. #1 cause of zero citations is silent blocks (CDN, security plugin, robots.txt).
4. **Content Freshness** — AI weights freshness aggressively. ~50% of AI citations are content <13 weeks old.

## Current state at choosewise.education (audit 2026-04-25)

**In place:**
- Generic robots.txt (`User-agent: *` `Allow: /` + sitemap reference)
- Static sitemap.xml — but only 20 URLs (covers 150+ index.html pages incompletely)
- `<title>` + `<meta description>` on ~308 pages
- OG/Twitter cards on blog posts; partial on guides
- Canonical tags on 7 pages only
- Proper H1/H2 hierarchy
- Date stamps on blog posts

**Missing:**
- llms.txt
- All JSON-LD structured data (no Organization, Person, Article, FAQPage)
- Hreflang reciprocal linking (SV↔EN)
- Canonical on ~143 pages
- Author/Person schema for Johan
- Search Console / Bing verification
- OG images on /wise/, /guides/, /prompts/, /notebooklm-styles/, /about/
- Sitemap completeness (missing all individual prompts, guides, blog posts)
- AI-crawler-explicit allowlist in robots.txt

---

## Prioritized action plan

### Tier 1 — High ROI, low effort (~2–3 h implementation)

1. **robots.txt — explicit AI crawler allowlist.** Add `Allow:` for: `GPTBot`, `OAI-SearchBot`, `ChatGPT-User`, `ClaudeBot`, `Claude-User`, `Claude-SearchBot`, `PerplexityBot`, `Google-Extended`, `GoogleOther`, `Applebot-Extended`, `meta-externalagent`. Keeps default `User-agent: *` `Allow: /`.
2. **JSON-LD: Organization + Person (Johan) site-wide.** Inject via `assets/partials/header-{en,sv}.html`. Organization.sameAs → LinkedIn + jlsu.se. Person.jobTitle, knowsAbout, worksFor, alumniOf.
3. **`/llms.txt`.** Curated `# choosewise.education` + summary blockquote + H2 sections linking to /wise/, /prompts/, /guides/, /notebooklm-styles/. Cheap to ship; non-zero upside.
4. **Hreflang reciprocal links** on every SV/EN paired page. Use `sv`, `en`, `x-default`. Mandatory return-link from each side.
5. **Canonical URL on every page** (currently only 7). Inject into header partial or via build-time script.
6. **Complete sitemap.xml.** Generator script that walks the file tree, includes every published index.html, with `<lastmod>` from git commit date, and `<xhtml:link rel="alternate" hreflang="...">` per page.

### Tier 2 — Medium effort, strong lift

7. **Article + Person-author JSON-LD on blog posts.** Extend `scripts/build-blog-posts.py` to inject `<script type="application/ld+json">` with `author` (Person reference), `datePublished`, `dateModified`, `inLanguage`.
8. **Visible "Last updated" + dateModified** on /wise/, /guides/, /prompts/, /notebooklm-styles/ (not just blog). Match `<lastmod>` in sitemap, `dateModified` in JSON-LD, and the visible HTML stamp exactly.
9. **Answer capsule (50–80 words) at the top** of /wise/, /about/, /prompts/, /guides/, /notebooklm-styles/. Concise summary above the fold so AI can extract directly.
10. **Question-form H2s** on /wise/, /prompts/, /guides/. Examples: "What is the WISE Framework for Education?", "Who should use WISE?", "Which prompt pack should I download?". Maps to actual user queries.
11. **FAQPage schema.** First on Gemini NotebookLM guide (already has FAQ blocks without schema). Then add 4–5 Q/A pairs to /wise/ with FAQPage schema.
12. **Custom OG images** on /wise/, /about/, /guides/, /prompts/, /notebooklm-styles/. Currently all use `og-default.svg`. Reuse the WISE/RÄTT hero approach.

### Tier 3 — Ongoing / next month

13. **Visible author byline** on blog posts ("By Johan Lindström") + linked Person schema → /about/.
14. **BreadcrumbList JSON-LD** on all subordinate pages.
15. **LearningResource (or HowTo) schema** on prompt-pack pages — better match than Dataset.
16. **Diagnostic curl test** for AI bots:
    ```bash
    curl -I -A "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.1; +https://openai.com/gptbot" https://choosewise.education/
    # Expect HTTP 200. Repeat for ClaudeBot, PerplexityBot.
    ```
17. **Google Search Console + Bing Webmaster Tools verification.** Monitor GSC's "AI Overview" impressions filter — free AI-citation leading indicator.
18. **Monthly freshness pass:** real content edits to 2–3 older guides + update dateModified. Don't fake-bump dates — AI engines detect that.

---

## What to skip from the PDF

- **GEO Optimizer plugin** — WordPress only; this site is static.
- **Otterly.ai / Profound / Peec AI** — paid citation trackers. Free stack (GSC + Bing Webmaster + server logs) is enough at current scale.
- **AI Writer for content generation** — research shows authority beats AI-optimized prose; risk of generic-sounding content.
- **5-day/week protocol** — overkill until baseline citations are measured. Monthly 30-min scan suffices.

## Things flagged as outdated or contested

- "Add schema, get cited" — Dec 2024 Quoleady study found no correlation between schema volume and citation rate alone. Schema works **paired with** clean structure and authority signals.
- llms.txt as a "must-have" — server-log audits show very low actual fetch rates from AI bots. Ship it (cheap), don't count on it.
- Specific citation-lift numbers (2.8×, 67%, etc.) — vendor-funded, methodology unpublished. Use as directional, not proof.

---

## Sources (key)

- [llmstxt.org](https://llmstxt.org)
- [OpenAI bots overview](https://platform.openai.com/docs/bots)
- [Anthropic crawler docs](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)
- [Google common crawlers](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers)
- [Perplexity bots guide](https://docs.perplexity.ai/guides/bots)
- [Google hreflang docs](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Apple Applebot](https://support.apple.com/en-us/119829)
- [Meta web crawlers](https://developers.facebook.com/docs/sharing/webmasters/web-crawlers/)
- [Bing crawlers](https://www.bing.com/webmasters/help/which-crawlers-does-bing-use-8c184ec0)
- [Cloudflare: Perplexity stealth crawling](https://blog.cloudflare.com/perplexity-is-using-stealth-undeclared-crawlers-to-evade-website-no-crawl-directives/)
- [Ahrefs: AI Overview citations from top 10 dropped from 76% → 38%](https://ahrefs.com/blog/ai-overview-citations-top-10/)
- [Position.digital: AI SEO statistics](https://www.position.digital/blog/ai-seo-statistics/)
- [Search Engine Journal: Anthropic's Claude bots](https://www.searchenginejournal.com/anthropics-claude-bots-make-robots-txt-decisions-more-granular/568253/)
- [Semrush: Optimize for AI search engines](https://www.semrush.com/blog/how-to-optimize-content-for-ai-search-engines/)
- [Longato.ch llms.txt audit (low actual usage)](https://www.longato.ch/llms-recommendation-2025-august/)

---

## Execution path when picking this back up

When ready, paste back to me: *"Run Tier 1 from the SEO plan"* — and I'll start with #1 (robots.txt). Tier 1 is fully implementable by me on the static site without further design decisions; Tier 2 has a couple of content-touch decisions (which queries become FAQ Q/A; what custom OG images look like for the section landing pages).
