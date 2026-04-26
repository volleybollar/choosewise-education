# AI or human? Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the new `/ai-or-human/` (EN) and `/sv/ai-eller-manniska/` (SV) pages with three interactive tests (text, image, video) and an optional 1–6 difficulty rating widget that posts anonymous data to a Johan-owned Google Sheet. Concurrently rename "NotebookLM Styles" → "Infographic Styles" with a URL move + redirect shims, and reorder the primary navigation.

**Architecture:** Plain HTML/CSS/JS, no build step. Test logic lives in a single `assets/js/ai-or-human.js` IIFE that hooks into `data-` attributes on per-test containers. CSS is additive in `assets/css/components.css`. Pages are mirrored EN/SV per the existing site pattern. Telemetry is fire-and-forget POST to a Google Apps Script Web App, with a constant `TELEMETRY_URL` that gracefully no-ops when empty.

**Tech Stack:** HTML5, CSS3 (custom properties + grid), vanilla JS (ES2017+), Python `http.server` for local preview, Google Apps Script for telemetry sink.

**Spec reference:** `docs/superpowers/specs/2026-04-26-ai-or-human-design.md`

**Critical workflow constraint:** Per Johan's preference (memory: preview-then-commit), every phase's commit step requires Johan's explicit "kör" after the preview gate. Do **not** auto-commit phase work.

---

## Phase A — Navigation + URL rename

**Goal:** Rename "NotebookLM Styles" → "Infographic Styles" with URL change, install redirect shims, reorder nav, add the "AI or human?" item, update all internal references.

### Task A1: Move the Infographic Styles directories

**Files:**
- Move: `notebooklm-styles/` → `infographic-styles/`
- Move: `sv/notebooklm-stilar/` → `sv/infografik-stilar/`

- [ ] **Step 1: Move EN directory**

```bash
git mv notebooklm-styles infographic-styles
```

- [ ] **Step 2: Move SV directory**

```bash
git mv sv/notebooklm-stilar sv/infografik-stilar
```

- [ ] **Step 3: Update canonical + hreflang inside the moved EN file**

In `infographic-styles/index.html`, search for the `<!-- seo:start` block and update:

```html
<link rel="canonical" href="https://choosewise.education/infographic-styles/">
<link rel="alternate" hreflang="en" href="https://choosewise.education/infographic-styles/">
<link rel="alternate" hreflang="sv" href="https://choosewise.education/sv/infografik-stilar/">
<link rel="alternate" hreflang="x-default" href="https://choosewise.education/infographic-styles/">
```

Also update any `@id` JSON-LD entries that reference `/notebooklm-styles/` to `/infographic-styles/`.

- [ ] **Step 4: Update canonical + hreflang inside the moved SV file**

In `sv/infografik-stilar/index.html`, update the SEO block analogously to point at `/sv/infografik-stilar/` (canonical + hreflang sv) and `/infographic-styles/` (hreflang en + x-default).

- [ ] **Step 5: Verify with grep**

```bash
grep -n "notebooklm-styles\|notebooklm-stilar" infographic-styles/index.html sv/infografik-stilar/index.html
```

Expected: zero matches (any remaining match is a bug).

### Task A2: Add redirect shims at the old paths

**Files:**
- Create: `notebooklm-styles/index.html`
- Create: `sv/notebooklm-stilar/index.html`

- [ ] **Step 1: Create EN redirect shim**

`notebooklm-styles/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Redirecting to Infographic Styles — choosewise.education</title>
  <meta name="robots" content="noindex">
  <link rel="canonical" href="https://choosewise.education/infographic-styles/">
  <meta http-equiv="refresh" content="0;url=/infographic-styles/">
</head>
<body>
  <p>This page has moved to <a href="/infographic-styles/">/infographic-styles/</a>.</p>
</body>
</html>
```

- [ ] **Step 2: Create SV redirect shim**

`sv/notebooklm-stilar/index.html`:

```html
<!DOCTYPE html>
<html lang="sv">
<head>
  <meta charset="UTF-8">
  <title>Omdirigerar till Infografik-stilar — choosewise.education</title>
  <meta name="robots" content="noindex">
  <link rel="canonical" href="https://choosewise.education/sv/infografik-stilar/">
  <meta http-equiv="refresh" content="0;url=/sv/infografik-stilar/">
</head>
<body>
  <p>Den här sidan har flyttats till <a href="/sv/infografik-stilar/">/sv/infografik-stilar/</a>.</p>
</body>
</html>
```

### Task A3: Update nav partials

**Files:**
- Modify: `assets/partials/header-en.html`
- Modify: `assets/partials/header-sv.html`

- [ ] **Step 1: Replace EN nav `<ul>`**

In `assets/partials/header-en.html`, replace the `<ul class="nav__links">` block with:

```html
<ul class="nav__links">
  <li><a class="nav__link" href="/wise/">The WISE Framework</a></li>
  <li><a class="nav__link" href="/guides/">AI Guides</a></li>
  <li><a class="nav__link" href="/ai-or-human/">AI or human?</a></li>
  <li><a class="nav__link" href="/prompts/">Prompts</a></li>
  <li><a class="nav__link" href="/presentation-skills/">Presentation Skills</a></li>
  <li><a class="nav__link" href="/infographic-styles/">Infographic Styles</a></li>
  <li><a class="nav__link" href="/blog/">Blog</a></li>
  <li><a class="nav__link" href="/about/">About</a></li>
</ul>
```

- [ ] **Step 2: Replace SV nav `<ul>`**

In `assets/partials/header-sv.html`, replace the `<ul class="nav__links">` block with:

```html
<ul class="nav__links">
  <li><a class="nav__link" href="/sv/ratt/">RÄTT-modellen</a></li>
  <li><a class="nav__link" href="/sv/guider/">Guider</a></li>
  <li><a class="nav__link" href="/sv/ai-eller-manniska/">AI eller människa?</a></li>
  <li><a class="nav__link" href="/sv/promptar/">Promptar</a></li>
  <li><a class="nav__link" href="/sv/presentationsteknik/">Presentationsteknik</a></li>
  <li><a class="nav__link" href="/sv/infografik-stilar/">Infografik-stilar</a></li>
  <li><a class="nav__link" href="/sv/blog/">Blogg</a></li>
  <li><a class="nav__link" href="/sv/om/">Om</a></li>
</ul>
```

### Task A4: Update internal references (sweep)

**Files:**
- Modify: `sitemap.xml`
- Modify: `llms.txt`
- Modify: `assets/partials/footer-en.html`
- Modify: `assets/partials/footer-sv.html`
- Modify: `blog/posts/why-i-built-choosewise-education.html`
- Modify: `sv/blog/posts/varfor-jag-byggt-choosewise-education.html`
- Modify: `guides/gemini-notebooklm/index.html`
- Modify: `sv/guider/gemini-notebooklm/index.html`
- Modify: `exports/gemini-notebooklm-print-a4-en.html`
- Modify: `exports/gemini-notebooklm-print-a4-sv.html`
- Modify: `scripts/parse-nlm-html.js`

- [ ] **Step 1: Find all current references**

```bash
grep -rln "notebooklm-styles\|notebooklm-stilar" \
  --include="*.html" --include="*.json" --include="*.js" --include="*.xml" --include="*.txt" --include="*.css" \
  | grep -v ^notebooklm-styles/ | grep -v ^sv/notebooklm-stilar/
```

Expected: ~13 files. The redirect shims (`notebooklm-styles/index.html`, `sv/notebooklm-stilar/index.html`) are excluded — they SHOULD still contain the old slug.

- [ ] **Step 2: Replace EN URL in non-shim files**

For each file from Step 1 that references `/notebooklm-styles/`, replace with `/infographic-styles/`:

```bash
# For each file:
sed -i '' 's|/notebooklm-styles/|/infographic-styles/|g' "$FILE"
```

Do this carefully — the shim files at `notebooklm-styles/index.html` and `sv/notebooklm-stilar/index.html` MUST keep their references intact.

- [ ] **Step 3: Replace SV URL in non-shim files**

Same approach:

```bash
sed -i '' 's|/sv/notebooklm-stilar/|/sv/infografik-stilar/|g' "$FILE"
```

- [ ] **Step 4: Replace label text everywhere**

Update visible label "NotebookLM Styles" → "Infographic Styles" and "NotebookLM-stilar" → "Infografik-stilar" only in **non-content** files (footer, sitemap labels). Do NOT change blog post body text or guide content where the term refers to the historical NotebookLM tool itself — those are about the tool, not our page name.

Files where label changes are appropriate:
- `assets/partials/footer-en.html`, `assets/partials/footer-sv.html` (link text)
- Any nav-like links

Files where the visible string should remain unchanged (referring to the tool):
- Blog posts, guide pages, exports — only the URL changes, not body text.

- [ ] **Step 5: Update `sitemap.xml` entries**

Replace `<loc>https://choosewise.education/notebooklm-styles/</loc>` with `<loc>https://choosewise.education/infographic-styles/</loc>`. Same for SV. Update `lastmod` to today (2026-04-26).

- [ ] **Step 6: Update `llms.txt`**

Replace any `/notebooklm-styles/` and `/sv/notebooklm-stilar/` lines with the new paths. Update title text from "NotebookLM Styles" → "Infographic Styles".

- [ ] **Step 7: Update `scripts/parse-nlm-html.js`**

Search for hardcoded path constants. If the script writes to `notebooklm-styles/`, update to write to `infographic-styles/`. Verify by re-running the script if Johan needs to regenerate styles.

- [ ] **Step 8: Verify the sweep**

```bash
grep -rln "notebooklm-styles\|notebooklm-stilar" \
  --include="*.html" --include="*.json" --include="*.js" --include="*.xml" --include="*.txt" --include="*.css" \
  | grep -v ^notebooklm-styles/index.html | grep -v ^sv/notebooklm-stilar/index.html
```

Expected: zero matches (only the two redirect shim files should still reference the old slugs).

### Task A5: Add new pages to sitemap.xml

**Files:**
- Modify: `sitemap.xml`

- [ ] **Step 1: Add the two new entries**

Add these inside `<urlset>`:

```xml
<url>
  <loc>https://choosewise.education/ai-or-human/</loc>
  <lastmod>2026-04-26</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.8</priority>
  <xhtml:link rel="alternate" hreflang="en" href="https://choosewise.education/ai-or-human/"/>
  <xhtml:link rel="alternate" hreflang="sv" href="https://choosewise.education/sv/ai-eller-manniska/"/>
  <xhtml:link rel="alternate" hreflang="x-default" href="https://choosewise.education/ai-or-human/"/>
</url>
<url>
  <loc>https://choosewise.education/sv/ai-eller-manniska/</loc>
  <lastmod>2026-04-26</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.8</priority>
  <xhtml:link rel="alternate" hreflang="en" href="https://choosewise.education/ai-or-human/"/>
  <xhtml:link rel="alternate" hreflang="sv" href="https://choosewise.education/sv/ai-eller-manniska/"/>
  <xhtml:link rel="alternate" hreflang="x-default" href="https://choosewise.education/ai-or-human/"/>
</url>
```

(Empty `ai-or-human/` and `sv/ai-eller-manniska/` directories will get their `index.html` in Phase B.)

### Task A6: Phase A preview gate

- [ ] **Step 1: Start (or verify) local server**

```bash
cd "/Users/johan/Projekt/JLSU/Ny JLSU hemsida"
# Check if already running:
lsof -ti:8000 || python3 -m http.server 8000 &
```

- [ ] **Step 2: Open EN home and verify nav**

```bash
open "http://localhost:8000/"
```

Look for: new menu order, "AI or human?" item present (link will 404 — fine), "Infographic Styles" label present.

- [ ] **Step 3: Open SV home and verify nav**

```bash
open "http://localhost:8000/sv/"
```

Look for: new menu order, "AI eller människa?" item present, "Infografik-stilar" label present.

- [ ] **Step 4: Verify Infographic Styles new URL works**

```bash
open "http://localhost:8000/infographic-styles/"
open "http://localhost:8000/sv/infografik-stilar/"
```

Look for: same content as before (just at new URL). Page renders normally.

- [ ] **Step 5: Verify the redirect shims redirect**

```bash
open "http://localhost:8000/notebooklm-styles/"
open "http://localhost:8000/sv/notebooklm-stilar/"
```

Look for: page immediately navigates to the new URL.

- [ ] **Step 6: Wait for Johan's "kör"**

Pause here. Do NOT commit until Johan inspects the preview and says "kör".

- [ ] **Step 7: Commit Phase A (after "kör")**

```bash
git add -A \
  notebooklm-styles/ sv/notebooklm-stilar/ \
  infographic-styles/ sv/infografik-stilar/ \
  assets/partials/header-en.html assets/partials/header-sv.html \
  assets/partials/footer-en.html assets/partials/footer-sv.html \
  sitemap.xml llms.txt \
  blog/posts/why-i-built-choosewise-education.html \
  sv/blog/posts/varfor-jag-byggt-choosewise-education.html \
  guides/gemini-notebooklm/index.html \
  sv/guider/gemini-notebooklm/index.html \
  exports/gemini-notebooklm-print-a4-en.html \
  exports/gemini-notebooklm-print-a4-sv.html \
  scripts/parse-nlm-html.js

git commit -m "$(cat <<'EOF'
refactor(nav): rename NotebookLM Styles → Infographic Styles + add AI or human?

- Move /notebooklm-styles/ → /infographic-styles/ (EN+SV)
- Add meta-refresh redirect shims at old paths (canonical points new)
- Reorder primary nav (both languages) + add "AI or human?" entry
- Update all 13 internal references (sitemap, llms.txt, footers, blogs, guides, exports, scripts)
- Add new test-page URLs to sitemap.xml

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Phase B — Page skeleton + image asset

**Goal:** Create the new EN and SV pages with hero, empty section stubs for the three tests, and the optimized photo grid asset in place. SEO meta complete.

### Task B1: Move and optimize the photo-grid image

**Files:**
- Create: `assets/images/ai-or-human/photo-grid.jpg`
- Source: `~/Desktop/AI eller digitalt fotografi.jpeg`

- [ ] **Step 1: Create destination directory**

```bash
mkdir -p assets/images/ai-or-human
```

- [ ] **Step 2: Optimize and copy**

Use the existing optimize script if it accepts arbitrary input, otherwise use `sips` (built into macOS):

```bash
# Option A — sips (always available on macOS):
sips -s format jpeg -s formatOptions 85 \
     --resampleWidth 1600 \
     "/Users/johan/Desktop/AI eller digitalt fotografi.jpeg" \
     --out "assets/images/ai-or-human/photo-grid.jpg"

# Verify size is reasonable (target ≤300 KB):
ls -lh assets/images/ai-or-human/photo-grid.jpg
```

If output exceeds 300 KB, re-run with quality 75 instead of 85.

- [ ] **Step 3: Verify image renders**

Manually open the file:

```bash
open assets/images/ai-or-human/photo-grid.jpg
```

Expected: 3×3 grid of 9 numbered photos visible, sharp.

### Task B2: Create EN page skeleton

**Files:**
- Create: `ai-or-human/index.html`

- [ ] **Step 1: Write the page skeleton**

`ai-or-human/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI or human? — choosewise.education</title>
  <meta name="description" content="Three short tests where you check whether you can tell AI-generated text, images, and video apart from content created by humans.">
  <meta property="og:title" content="AI or human? — choosewise.education">
  <meta property="og:description" content="Three short tests where you check whether you can tell AI-generated text, images, and video apart from content created by humans.">
  <meta property="og:image" content="/assets/images/brand/og/wise-en.svg">
  <link rel="stylesheet" href="/assets/css/fonts.css">
  <link rel="stylesheet" href="/assets/css/tokens.css">
  <link rel="stylesheet" href="/assets/css/base.css">
  <link rel="stylesheet" href="/assets/css/components.css">
  <link rel="stylesheet" href="/assets/css/pages.css">
  <link rel="canonical" href="https://choosewise.education/ai-or-human/">
  <link rel="alternate" hreflang="en" href="https://choosewise.education/ai-or-human/">
  <link rel="alternate" hreflang="sv" href="https://choosewise.education/sv/ai-eller-manniska/">
  <link rel="alternate" hreflang="x-default" href="https://choosewise.education/ai-or-human/">
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage","@id":"https://choosewise.education/ai-or-human/#webpage","url":"https://choosewise.education/ai-or-human/","inLanguage":"en","name":"AI or human?","dateModified":"2026-04-26"}</script>
</head>
<body>
  <div data-include="/assets/partials/header-en.html"></div>

  <main>
    <section class="page-hero container">
      <span class="eyebrow" data-reveal>Test yourself</span>
      <h1 data-reveal>AI or human?</h1>
      <p class="lede" data-reveal>As technology advances rapidly, it gets harder and harder to tell AI-generated text, images, and video apart from content that is not. I'm not thinking about mass-produced AI slop, but the kind of output produced by people who know how to create quality content with these tools. On this page I've put together a few short exercises where you can test whether you can see what's AI-generated and what's not.</p>
    </section>

    <!-- Test 1 — Texts (added in Phase C) -->
    <section class="section container quiz-section" id="test-text" data-test="text">
      <h2 class="section__title">Test 1 — Texts</h2>
      <p class="section__lede">Coming next.</p>
    </section>

    <!-- Test 2 — Images (added in Phase D) -->
    <section class="section section--alt container quiz-section" id="test-image" data-test="image">
      <h2 class="section__title">Test 2 — Images</h2>
      <p class="section__lede">Coming next.</p>
    </section>

    <!-- Test 3 — Videos (added in Phase E) -->
    <section class="section container quiz-section" id="test-video" data-test="video">
      <h2 class="section__title">Test 3 — Videos</h2>
      <p class="section__lede">Coming next.</p>
    </section>
  </main>

  <div data-include="/assets/partials/footer-en.html"></div>

  <script src="/assets/js/include.js"></script>
  <script src="/assets/js/scroll-reveals.js"></script>
  <!-- ai-or-human.js loaded in Phase C -->
</body>
</html>
```

### Task B3: Create SV page skeleton

**Files:**
- Create: `sv/ai-eller-manniska/index.html`

- [ ] **Step 1: Write the SV mirror**

`sv/ai-eller-manniska/index.html`:

```html
<!DOCTYPE html>
<html lang="sv">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI eller människa? — choosewise.education</title>
  <meta name="description" content="Tre korta övningar där du testar om du kan se skillnad på text, bild och video som är AI-genererad och innehåll skapat av människor.">
  <meta property="og:title" content="AI eller människa? — choosewise.education">
  <meta property="og:description" content="Tre korta övningar där du testar om du kan se skillnad på text, bild och video som är AI-genererad och innehåll skapat av människor.">
  <meta property="og:image" content="/assets/images/brand/og/wise-sv.svg">
  <link rel="stylesheet" href="/assets/css/fonts.css">
  <link rel="stylesheet" href="/assets/css/tokens.css">
  <link rel="stylesheet" href="/assets/css/base.css">
  <link rel="stylesheet" href="/assets/css/components.css">
  <link rel="stylesheet" href="/assets/css/pages.css">
  <link rel="canonical" href="https://choosewise.education/sv/ai-eller-manniska/">
  <link rel="alternate" hreflang="en" href="https://choosewise.education/ai-or-human/">
  <link rel="alternate" hreflang="sv" href="https://choosewise.education/sv/ai-eller-manniska/">
  <link rel="alternate" hreflang="x-default" href="https://choosewise.education/ai-or-human/">
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage","@id":"https://choosewise.education/sv/ai-eller-manniska/#webpage","url":"https://choosewise.education/sv/ai-eller-manniska/","inLanguage":"sv","name":"AI eller människa?","dateModified":"2026-04-26"}</script>
</head>
<body>
  <div data-include="/assets/partials/header-sv.html"></div>

  <main>
    <section class="page-hero container">
      <span class="eyebrow" data-reveal>Testa dig själv</span>
      <h1 data-reveal>AI eller människa?</h1>
      <p class="lede" data-reveal>I takt med den snabba teknikutvecklingen blir det allt svårare att se skillnad på text, bild och video som är AI-genererad och text, bild och video som inte är det. Jag tänker inte på massproducerad AI-slop, utan det som genereras av människor som har kompetens att skapa kvalitativt innehåll. På den här sidan har jag skapat några enkla övningar där du kan testa om du kan se vad som är AI-genererat och vad som inte är det.</p>
    </section>

    <section class="section container quiz-section" id="test-text" data-test="text">
      <h2 class="section__title">Test 1 — Text</h2>
      <p class="section__lede">Kommer härnäst.</p>
    </section>

    <section class="section section--alt container quiz-section" id="test-image" data-test="image">
      <h2 class="section__title">Test 2 — Bilder</h2>
      <p class="section__lede">Kommer härnäst.</p>
    </section>

    <section class="section container quiz-section" id="test-video" data-test="video">
      <h2 class="section__title">Test 3 — Video</h2>
      <p class="section__lede">Kommer härnäst.</p>
    </section>
  </main>

  <div data-include="/assets/partials/footer-sv.html"></div>

  <script src="/assets/js/include.js"></script>
  <script src="/assets/js/scroll-reveals.js"></script>
  <!-- ai-or-human.js loaded in Phase C -->
</body>
</html>
```

### Task B4: Phase B preview gate

- [ ] **Step 1: Open EN page**

```bash
open "http://localhost:8000/ai-or-human/"
```

Expected: hero with eyebrow + h1 + lede; three section stubs each with "Coming next."; nav and footer included.

- [ ] **Step 2: Open SV page**

```bash
open "http://localhost:8000/sv/ai-eller-manniska/"
```

Expected: same structure in Swedish.

- [ ] **Step 3: Verify language switcher**

Click the EN↔SV switcher in the top-right of each page. The other language's page should load and the switcher state should flip.

- [ ] **Step 4: Wait for Johan's "kör"**

Pause. Do not commit until "kör".

- [ ] **Step 5: Commit Phase B (after "kör")**

```bash
git add ai-or-human/ sv/ai-eller-manniska/ assets/images/ai-or-human/
git commit -m "$(cat <<'EOF'
feat(ai-or-human): add page skeleton + photo-grid asset

EN at /ai-or-human/ and SV at /sv/ai-eller-manniska/. Hero + three
empty test-section stubs. SEO meta + JSON-LD complete.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Phase C — Test 1: Texts

**Goal:** Build the 4-card 2×2 text test with selection cap, position randomization, submit-then-flip flow, score, reset.

### Task C1: Append CSS

**Files:**
- Modify: `assets/css/components.css`

- [ ] **Step 1: Append the quiz block**

Append to `assets/css/components.css`:

```css
/* ───── AI or human — quiz components ───── */

.quiz-section { margin-top: var(--space-8); }
.quiz-section .section__lede { max-width: var(--content-text-max); }

.quiz-grid--2x2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-5);
  margin-top: var(--space-6);
}
.quiz-grid--3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-5);
  margin-top: var(--space-6);
}

.quiz-controls {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
  align-items: center;
  margin-top: var(--space-5);
}
.quiz-options {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
}
.quiz-option {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-pill);
  background: var(--color-bg);
  cursor: pointer;
  font-size: var(--fs-small);
}
.quiz-option input[type="checkbox"],
.quiz-option input[type="radio"] {
  margin: 0;
}

.quiz-feedback {
  margin-top: var(--space-4);
  font-family: var(--font-display);
  font-size: var(--fs-h3);
  min-height: 1.5em;
}
.quiz-feedback[hidden] { display: none; }

.quiz-reset {
  background: none;
  border: 0;
  color: var(--color-accent);
  cursor: pointer;
  text-decoration: underline;
  font-family: var(--font-body);
  font-size: var(--fs-small);
  padding: 0;
}
.quiz-reset:hover { color: var(--color-accent-hover); }

/* Text-card variant — taller, no aspect-ratio lock */
.flipcard--text { aspect-ratio: auto; min-height: 22rem; }
.flipcard--text .flipcard__face {
  padding: var(--space-5);
  justify-content: space-between;
}
.flipcard--text .flipcard__front {
  background: var(--color-bg);
  color: var(--color-text);
}
.flipcard--text .flipcard__body {
  font-size: var(--fs-body);
  line-height: var(--lh-normal);
  margin: 0 0 var(--space-4);
}
.flipcard--text .flipcard__choice {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--fs-small);
  border-top: 1px solid var(--color-border);
  padding-top: var(--space-3);
}
.flipcard--text .flipcard__back {
  align-items: center;
  justify-content: center;
  text-align: center;
}
.flipcard--text .flipcard__verdict {
  font-family: var(--font-display);
  font-size: var(--fs-h2);
  margin: 0 0 var(--space-3);
}
.flipcard--text .flipcard__explain {
  font-size: var(--fs-body);
  opacity: 0.85;
}

/* Image-frame for Test 2 photo */
.image-frame {
  padding: var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  background: var(--color-bg);
  margin-top: var(--space-5);
}
.image-frame img {
  display: block;
  width: 100%;
  height: auto;
  border-radius: var(--radius-sm);
}

/* Video-tile for Test 3 */
.video-tile {
  position: relative;
  aspect-ratio: 16 / 9;
  background: var(--color-bg-alt);
  border-radius: var(--radius-md);
  overflow: hidden;
}
.video-tile video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.video-tile__placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-display);
  color: var(--color-text-soft);
  background: var(--color-bg-alt);
}
.video-tile__label {
  position: absolute;
  top: var(--space-2);
  left: var(--space-2);
  background: var(--color-dark-bg);
  color: var(--color-dark-text);
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-pill);
  font-family: var(--font-display);
  font-size: var(--fs-small);
  z-index: 1;
}

/* Difficulty rating widget */
.rating {
  margin-top: var(--space-5);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border);
}
.rating[hidden] { display: none; }
.rating__heading {
  font-family: var(--font-display);
  font-size: var(--fs-body);
  margin: 0 0 var(--space-2);
}
.rating__hint {
  font-size: var(--fs-small);
  color: var(--color-text-soft);
  margin: 0 0 var(--space-3);
}
.rating__scale {
  display: flex;
  gap: var(--space-2);
  align-items: center;
  flex-wrap: wrap;
}
.rating__endlabel {
  font-size: var(--fs-small);
  color: var(--color-text-soft);
}
.rating__btn {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  background: var(--color-bg);
  cursor: pointer;
  font-family: var(--font-body);
  font-weight: 500;
  transition: all 0.2s;
}
.rating__btn:hover:not(:disabled) { border-color: var(--color-accent); }
.rating__btn[aria-pressed="true"] {
  background: var(--color-accent);
  color: var(--color-dark-text);
  border-color: var(--color-accent);
}
.rating__btn:disabled { cursor: default; opacity: 0.6; }
.rating__btn[aria-pressed="true"]:disabled { opacity: 1; }

/* Mobile responsive */
@media (max-width: 720px) {
  .quiz-grid--2x2 { grid-template-columns: 1fr; }
  .quiz-grid--3 { grid-template-columns: 1fr; }
  .rating__scale { gap: var(--space-1); }
  .rating__btn { width: 2.25rem; height: 2.25rem; }
}
```

### Task C2: Write Test 1 markup (EN)

**Files:**
- Modify: `ai-or-human/index.html` (replace the Test 1 section stub)

- [ ] **Step 1: Replace the EN Test 1 stub**

Replace the `<!-- Test 1 -->` section in `ai-or-human/index.html` with:

```html
<section class="section container quiz-section" id="test-text" data-test="text"
         data-feedback-template="You got {score} of 2 right. Click the cards to flip them and see which texts were AI-generated."
         data-feedback-zero="You got 0 of 2 right. Click the cards to flip them and see which texts were AI-generated.">
  <h2 class="section__title">Test 1 — Texts</h2>
  <p class="section__lede">Which two texts are AI-generated?</p>

  <div class="quiz-grid--2x2" data-quiz-cards>
    <!-- Topic A row (shuffled per page-load by JS, kept side-by-side) -->
    <article class="flipcard flipcard--text" data-topic="A" data-truth="ai">
      <div class="flipcard__inner">
        <div class="flipcard__face flipcard__front">
          <p class="flipcard__body">[TOPIC_A_AI_TEXT_EN]</p>
          <label class="flipcard__choice">
            <input type="checkbox" data-quiz-choice>
            <span>This is AI-generated</span>
          </label>
        </div>
        <div class="flipcard__face flipcard__back">
          <p class="flipcard__verdict">AI-generated</p>
          <p class="flipcard__explain">Generated by an AI model in Johan's voice.</p>
        </div>
      </div>
    </article>

    <article class="flipcard flipcard--text" data-topic="A" data-truth="human">
      <div class="flipcard__inner">
        <div class="flipcard__face flipcard__front">
          <p class="flipcard__body"><!-- TODO: replace with Johan's text on Topic A -->Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam.</p>
          <label class="flipcard__choice">
            <input type="checkbox" data-quiz-choice>
            <span>This is AI-generated</span>
          </label>
        </div>
        <div class="flipcard__face flipcard__back">
          <p class="flipcard__verdict">Not AI-generated</p>
          <p class="flipcard__explain">Written by Johan.</p>
        </div>
      </div>
    </article>

    <!-- Topic B row -->
    <article class="flipcard flipcard--text" data-topic="B" data-truth="ai">
      <div class="flipcard__inner">
        <div class="flipcard__face flipcard__front">
          <p class="flipcard__body">[TOPIC_B_AI_TEXT_EN]</p>
          <label class="flipcard__choice">
            <input type="checkbox" data-quiz-choice>
            <span>This is AI-generated</span>
          </label>
        </div>
        <div class="flipcard__face flipcard__back">
          <p class="flipcard__verdict">AI-generated</p>
          <p class="flipcard__explain">Generated by an AI model in Johan's voice.</p>
        </div>
      </div>
    </article>

    <article class="flipcard flipcard--text" data-topic="B" data-truth="human">
      <div class="flipcard__inner">
        <div class="flipcard__face flipcard__front">
          <p class="flipcard__body"><!-- TODO: replace with Johan's text on Topic B -->Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
          <label class="flipcard__choice">
            <input type="checkbox" data-quiz-choice>
            <span>This is AI-generated</span>
          </label>
        </div>
        <div class="flipcard__face flipcard__back">
          <p class="flipcard__verdict">Not AI-generated</p>
          <p class="flipcard__explain">Written by Johan.</p>
        </div>
      </div>
    </article>
  </div>

  <div class="quiz-controls">
    <button type="button" class="btn btn--primary" data-quiz-submit disabled>Show answers</button>
    <button type="button" class="quiz-reset" data-quiz-reset>Reset</button>
  </div>
  <p class="quiz-feedback" data-quiz-feedback hidden aria-live="polite"></p>
</section>
```

### Task C3: Write Test 1 markup (SV)

**Files:**
- Modify: `sv/ai-eller-manniska/index.html` (replace the Test 1 section stub)

- [ ] **Step 1: Replace the SV Test 1 stub**

Mirror the EN markup with these string substitutions:
- Section heading: `Test 1 — Text`
- Lede: `Vilka två texter är AI-genererade?`
- `data-feedback-template`: `Du fick {score} av 2 rätt. Klicka på korten för att vända dem och se vilka texter som var AI-genererade.`
- `data-feedback-zero`: same template with 0
- Card body placeholders: `[ÄMNE_A_AI_TEXT_SV]`, `[ÄMNE_B_AI_TEXT_SV]`
- Card body ipsum: same Lorem
- Verdict front: `AI-genererad` / `Inte AI-genererad`
- Verdict explain: `Genererad av en AI-modell i Johans stil.` / `Skriven av Johan.`
- Choice label: `Detta är AI-genererat`
- Submit button: `Visa svar`
- Reset button: `Nollställ`

### Task C4: Write the 2 AI-style texts in Johan's voice

**Files:**
- Modify: `ai-or-human/index.html` (replace `[TOPIC_A_AI_TEXT_EN]` and `[TOPIC_B_AI_TEXT_EN]`)
- Modify: `sv/ai-eller-manniska/index.html` (replace `[ÄMNE_A_AI_TEXT_SV]` and `[ÄMNE_B_AI_TEXT_SV]`)

- [ ] **Step 1: Write Topic A SV (lärares användning av AI för effektivisering)**

Aim: ~120 words, in Johan's voice (warm, slightly provocative, peer-expert) — but with subtle AI tells (over-balanced both-sides hedging, tidy parallel constructions, slightly too-clean transitions, generic illustrative examples).

Suggested draft (refine before merge):

> När jag pratar med lärare som börjat använda AI som verktyg i sitt arbete märker jag samma sak om och om igen: det är inte själva tekniken som gör skillnaden, utan vad de gör med den tid de frigör. Att låta AI ta första utkastet på en återkoppling, ett föräldrabrev eller en lektionsförklaring sparar minuter — men det är vad som händer i de minuterna efteråt som avgör om eleverna får mer av läraren. Den som lägger den frigjorda tiden på att möta eleven där hen är, ser tydliga effekter. Den som bara skickar AI:ns första utkast vidare gör inte det. Det är fortfarande den professionella bedömningen som bär kvaliteten — inte modellen.

(Word count: ~118.)

- [ ] **Step 2: Write Topic B SV (skolans roll i samhället)**

> Skolan har alltid varit mer än en plats där barn lär sig saker. Den är samhällets sätt att forma nästa generation — vilka frågor de ställer, vilka beslut de orkar fatta, vilken sorts människor de blir. När vi diskuterar skolan idag stannar vi alltför ofta vid resultat, ranking och resurser. Det är viktigt, men det är inte allt. En skola som bara producerar elever med rätt svar på rätt prov har glömt halva sitt uppdrag. Den andra halvan handlar om att rusta unga människor för en värld som vi själva inte kan förutspå. Det kräver lärare som vågar tänka stort, ledare som tar ansvar, och en samhällsdebatt som behandlar skolan med den allvarliga respekt frågan förtjänar.

(Word count: ~125.)

- [ ] **Step 3: Translate Topic A to EN**

> When I talk with teachers who have started using AI as a tool in their work, I notice the same thing again and again: it's not the technology itself that makes the difference, but what they do with the time it frees up. Letting AI take the first draft of a piece of feedback, a parent letter, or a lesson explanation saves minutes — but it's what happens in those minutes afterwards that decides whether students get more of the teacher. Those who use the freed-up time to meet the student where they are see clear effects. Those who just forward the AI's first draft do not. Professional judgment is still what carries the quality — not the model.

- [ ] **Step 4: Translate Topic B to EN**

> School has always been more than a place where children learn things. It is society's way of shaping the next generation — what questions they ask, what decisions they have the courage to make, what kind of people they become. When we discuss school today we too often stop at results, rankings, and resources. That matters, but it is not everything. A school that only produces students with the right answers on the right tests has forgotten half its mission. The other half is about preparing young people for a world we cannot ourselves predict. That requires teachers who dare to think big, leaders who take responsibility, and a public conversation that treats schools with the seriousness the question deserves.

- [ ] **Step 5: Substitute placeholders in HTML**

In `ai-or-human/index.html`, replace `[TOPIC_A_AI_TEXT_EN]` with the EN Topic A text from Step 3, and `[TOPIC_B_AI_TEXT_EN]` with the EN Topic B text from Step 4.

In `sv/ai-eller-manniska/index.html`, replace `[ÄMNE_A_AI_TEXT_SV]` with the SV Topic A text from Step 1, and `[ÄMNE_B_AI_TEXT_SV]` with the SV Topic B text from Step 2.

### Task C5: Create `assets/js/ai-or-human.js` with initTextTest

**Files:**
- Create: `assets/js/ai-or-human.js`

- [ ] **Step 1: Write the IIFE wrapper + utilities + initTextTest**

`assets/js/ai-or-human.js`:

```js
// ai-or-human.js
// Drives the three tests on /ai-or-human/ and /sv/ai-eller-manniska/.
//
// Tests are independent and discovered via [data-test="text|image|video"]
// containers. Each test reads its facit from data-attributes on the container
// or its cards. JS strings are taken from data-attributes so all user-facing
// copy stays in the per-language HTML.
//
// Telemetry: optional 1–6 difficulty rating per test. POSTs to a Google
// Apps Script Web App URL set in TELEMETRY_URL. Empty URL = no network call.

(function () {
  'use strict';

  // ───── Telemetry endpoint ─────
  // Set this to the Apps Script deployment URL once Johan creates the Sheet.
  // Empty string = telemetry disabled (UI still shows "Tack!" confirmation).
  const TELEMETRY_URL = '';

  // ───── Utilities ─────

  function shuffleInPlace(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  function flipCard(cardEl, toState) {
    if (toState === 'flipped') cardEl.classList.add('is-flipped');
    else if (toState === 'front') cardEl.classList.remove('is-flipped');
    else cardEl.classList.toggle('is-flipped');
  }

  // ───── Test 1: Texts ─────

  function initTextTest(rootEl) {
    const grid = rootEl.querySelector('[data-quiz-cards]');
    if (!grid) return;

    const submitBtn = rootEl.querySelector('[data-quiz-submit]');
    const resetBtn = rootEl.querySelector('[data-quiz-reset]');
    const feedback = rootEl.querySelector('[data-quiz-feedback]');
    const tmpl = rootEl.dataset.feedbackTemplate || 'Score: {score}/2';

    let phase = 'select'; // 'select' | 'revealed'

    // Shuffle within each topic row so AI/human position is randomized.
    function shuffleByTopic() {
      const cards = Array.from(grid.querySelectorAll('.flipcard'));
      const byTopic = {};
      cards.forEach(c => {
        const t = c.dataset.topic;
        (byTopic[t] = byTopic[t] || []).push(c);
      });
      // Re-append in topic order: A, B, then within each topic shuffled.
      grid.innerHTML = '';
      ['A', 'B'].forEach(t => {
        const pair = byTopic[t] || [];
        shuffleInPlace(pair);
        pair.forEach(c => grid.appendChild(c));
      });
    }

    function getChoiceCheckboxes() {
      return Array.from(grid.querySelectorAll('[data-quiz-choice]'));
    }

    function getCheckedCount() {
      return getChoiceCheckboxes().filter(cb => cb.checked).length;
    }

    function syncSubmitState() {
      submitBtn.disabled = getCheckedCount() !== 2;
    }

    // Cap selection at 2: if user checks a 3rd, deselect oldest.
    let selectionOrder = [];
    function onChoiceChange(e) {
      if (phase !== 'select') return;
      const cb = e.target;
      if (!cb.matches('[data-quiz-choice]')) return;
      if (cb.checked) {
        selectionOrder.push(cb);
        if (selectionOrder.length > 2) {
          const oldest = selectionOrder.shift();
          oldest.checked = false;
        }
      } else {
        selectionOrder = selectionOrder.filter(x => x !== cb);
      }
      syncSubmitState();
    }

    function onCardClick(e) {
      if (phase !== 'revealed') return;
      // Don't intercept clicks on the checkbox or its label.
      if (e.target.closest('.flipcard__choice')) return;
      const card = e.target.closest('.flipcard');
      if (card) flipCard(card);
    }

    function onSubmit() {
      if (getCheckedCount() !== 2) return;
      // Score: count correct guesses. A "correct" guess is a checkbox checked
      // on a card whose data-truth === "ai".
      let score = 0;
      getChoiceCheckboxes().forEach(cb => {
        const card = cb.closest('.flipcard');
        const isAI = card.dataset.truth === 'ai';
        if (cb.checked && isAI) score += 1;
      });
      // Lock checkboxes, enable flipping.
      getChoiceCheckboxes().forEach(cb => { cb.disabled = true; });
      phase = 'revealed';
      feedback.textContent = tmpl.replace('{score}', String(score));
      feedback.hidden = false;
      submitBtn.disabled = true;
      // Reveal the rating widget for this test.
      revealRating(rootEl);
    }

    function onReset() {
      // Reshuffle, uncheck, unflip, re-enable.
      selectionOrder = [];
      shuffleByTopic();
      getChoiceCheckboxes().forEach(cb => {
        cb.checked = false;
        cb.disabled = false;
      });
      Array.from(grid.querySelectorAll('.flipcard')).forEach(c => flipCard(c, 'front'));
      feedback.hidden = true;
      feedback.textContent = '';
      phase = 'select';
      syncSubmitState();
    }

    // Wire up.
    shuffleByTopic();
    grid.addEventListener('change', onChoiceChange);
    grid.addEventListener('click', onCardClick);
    submitBtn.addEventListener('click', onSubmit);
    resetBtn.addEventListener('click', onReset);
    syncSubmitState();
  }

  // ───── Rating placeholder (filled in Phase F) ─────
  function revealRating(_rootEl) {
    // Filled in Phase F. No-op for now.
  }

  // ───── Bootstrap ─────
  function bootstrap() {
    document.querySelectorAll('[data-test="text"]').forEach(initTextTest);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootstrap);
  } else {
    bootstrap();
  }
})();
```

- [ ] **Step 2: Add the script tag to both pages**

In `ai-or-human/index.html` and `sv/ai-eller-manniska/index.html`, add immediately before `</body>`:

```html
<script src="/assets/js/ai-or-human.js"></script>
```

(Place it after the existing `include.js` and `scroll-reveals.js` script tags.)

### Task C6: Phase C preview gate

- [ ] **Step 1: Open EN page**

```bash
open "http://localhost:8000/ai-or-human/"
```

- [ ] **Step 2: Verify Test 1 behavior — selection cap**

- Click 1 checkbox → "Show answers" should remain disabled.
- Click a 2nd checkbox → "Show answers" should enable.
- Click a 3rd checkbox → the first selection should auto-deselect and the new one stays checked.

- [ ] **Step 3: Verify Test 1 behavior — reveal**

- With 2 checked, click "Show answers" → score line appears, e.g. "You got 1 of 2 right…"
- Cards should now flip on click. Checkboxes should be disabled.

- [ ] **Step 4: Verify Test 1 behavior — reset**

- Click "Reset" → checkboxes uncheck, score hides, all cards flip back to front, card positions within each row may change.

- [ ] **Step 5: Verify SV page**

```bash
open "http://localhost:8000/sv/ai-eller-manniska/"
```

Repeat steps 2–4 in Swedish; copy should be in Swedish, behavior identical.

- [ ] **Step 6: Verify mobile layout**

Open the page in the iPhone preset of the browser's responsive mode (or resize to ≤720px). Cards should stack to a single column.

- [ ] **Step 7: Wait for Johan's "kör"**

- [ ] **Step 8: Commit Phase C (after "kör")**

```bash
git add assets/css/components.css assets/js/ai-or-human.js \
        ai-or-human/index.html sv/ai-eller-manniska/index.html
git commit -m "$(cat <<'EOF'
feat(ai-or-human): Test 1 — text flipcards with submit-then-reveal flow

2x2 grid of flipcards, position randomized within each topic row, max 2
selections, "Show answers" gates the flip-to-reveal, score and reset.
Includes Claude-written AI-style texts on two topics; ipsum placeholders
for Johan's own text on the same two topics.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Phase D — Test 2: Images

**Goal:** Add the photo grid + 9-checkbox quiz + 2 hint flipcards.

### Task D1: Write Test 2 markup (EN)

**Files:**
- Modify: `ai-or-human/index.html` (replace the Test 2 section stub)

- [ ] **Step 1: Replace EN Test 2 stub**

```html
<section class="section section--alt container quiz-section" id="test-image" data-test="image"
         data-correct-not-ai="1,6,8"
         data-feedback-template="You got {score} of 9 right.">
  <h2 class="section__title">Test 2 — Images</h2>
  <p class="section__lede">9 images. Some are AI-generated and some are not. Tick the ones you think are AI-generated.</p>

  <figure class="image-frame">
    <img src="/assets/images/ai-or-human/photo-grid.jpg" alt="Nine numbered photographs in a 3x3 grid; some AI-generated, some not.">
  </figure>

  <div class="quiz-options" data-quiz-checkboxes>
    <label class="quiz-option"><input type="checkbox" value="1"><span>1</span></label>
    <label class="quiz-option"><input type="checkbox" value="2"><span>2</span></label>
    <label class="quiz-option"><input type="checkbox" value="3"><span>3</span></label>
    <label class="quiz-option"><input type="checkbox" value="4"><span>4</span></label>
    <label class="quiz-option"><input type="checkbox" value="5"><span>5</span></label>
    <label class="quiz-option"><input type="checkbox" value="6"><span>6</span></label>
    <label class="quiz-option"><input type="checkbox" value="7"><span>7</span></label>
    <label class="quiz-option"><input type="checkbox" value="8"><span>8</span></label>
    <label class="quiz-option"><input type="checkbox" value="9"><span>9</span></label>
  </div>

  <div class="quiz-controls">
    <button type="button" class="btn btn--primary" data-quiz-submit>Done!</button>
    <button type="button" class="quiz-reset" data-quiz-reset>Reset</button>
  </div>
  <p class="quiz-feedback" data-quiz-feedback hidden aria-live="polite"></p>

  <div class="quiz-grid--2x2" data-quiz-hints style="margin-top: var(--space-7);">
    <article class="flipcard" data-hint-card>
      <div class="flipcard__inner">
        <div class="flipcard__face flipcard__front">
          <div class="flipcard__overlay">
            <p class="flipcard__title">Hint 1</p>
          </div>
        </div>
        <div class="flipcard__face flipcard__back">
          <p class="flipcard__prompt">Six of the images are AI-generated.</p>
        </div>
      </div>
    </article>
    <article class="flipcard" data-hint-card>
      <div class="flipcard__inner">
        <div class="flipcard__face flipcard__front">
          <div class="flipcard__overlay">
            <p class="flipcard__title">Hint 2</p>
          </div>
        </div>
        <div class="flipcard__face flipcard__back">
          <p class="flipcard__prompt">Each row contains exactly one image that is NOT AI-generated. Each column does too.</p>
        </div>
      </div>
    </article>
  </div>
</section>
```

### Task D2: Write Test 2 markup (SV)

**Files:**
- Modify: `sv/ai-eller-manniska/index.html`

- [ ] **Step 1: Mirror to SV with these substitutions**

- Heading: `Test 2 — Bilder`
- Lede: `9 bilder. En del är AI-genererade och en del är inte det. Kryssa i de du tror är AI-genererade.`
- `data-feedback-template`: `Du fick {score} av 9 rätt.`
- Image alt: `Nio numrerade fotografier i ett 3x3-rutnät; vissa AI-genererade, andra inte.`
- Submit: `Klar!`, Reset: `Nollställ`
- Hint 1 title: `Ledtråd 1`, back: `Det finns 6 st AI-genererade bilder.`
- Hint 2 title: `Ledtråd 2`, back: `I varje kolumn finns en bild som inte är AI-genererad. I varje rad finns en bild som inte är AI-genererad.`

### Task D3: Add `initImageTest` to JS

**Files:**
- Modify: `assets/js/ai-or-human.js`

- [ ] **Step 1: Add the function before the bootstrap block**

Add inside the IIFE, after `initTextTest`:

```js
// ───── Test 2: Images ─────

function initImageTest(rootEl) {
  const checks = Array.from(rootEl.querySelectorAll('[data-quiz-checkboxes] input[type="checkbox"]'));
  const submitBtn = rootEl.querySelector('[data-quiz-submit]');
  const resetBtn = rootEl.querySelector('[data-quiz-reset]');
  const feedback = rootEl.querySelector('[data-quiz-feedback]');
  const hintCards = Array.from(rootEl.querySelectorAll('[data-hint-card]'));
  const tmpl = rootEl.dataset.feedbackTemplate || 'Score: {score}/9';

  // Truth set: numbers (as strings) that are NOT AI.
  const notAI = new Set(
    (rootEl.dataset.correctNotAi || '').split(',').map(s => s.trim()).filter(Boolean)
  );

  function onSubmit() {
    let score = 0;
    checks.forEach(cb => {
      const isNotAI = notAI.has(cb.value);
      const userSaysAI = cb.checked;
      // Correct if (userSaysAI && !isNotAI) or (!userSaysAI && isNotAI).
      if (userSaysAI !== isNotAI) score += 1;
    });
    feedback.textContent = tmpl.replace('{score}', String(score));
    feedback.hidden = false;
    revealRating(rootEl);
  }

  function onReset() {
    checks.forEach(cb => { cb.checked = false; });
    feedback.hidden = true;
    feedback.textContent = '';
    hintCards.forEach(c => flipCard(c, 'front'));
  }

  function onHintClick(e) {
    const card = e.target.closest('[data-hint-card]');
    if (card) flipCard(card);
  }

  submitBtn.addEventListener('click', onSubmit);
  resetBtn.addEventListener('click', onReset);
  hintCards.forEach(c => c.addEventListener('click', onHintClick));
}
```

- [ ] **Step 2: Add the bootstrap call**

In the `bootstrap()` function, add:

```js
document.querySelectorAll('[data-test="image"]').forEach(initImageTest);
```

### Task D4: Phase D preview gate

- [ ] **Step 1: Verify EN behavior**

```bash
open "http://localhost:8000/ai-or-human/#test-image"
```

- Tick a few checkboxes → click "Done!" → score appears.
- Click "Reset" → checkboxes clear, score hides, hint cards flip back to front.
- Click a hint card → flips to back, showing the hint text.

- [ ] **Step 2: Verify scoring math**

The truth set is `{1, 6, 8}` not-AI. Test cases:
- All unchecked: score = 3 (the three non-AI you correctly didn't mark + 6 AI you correctly didn't mark = wait, 0 marked vs 6 AI = 6 wrongs, 3 not-AI not marked = 3 right → total 3).
  - Actually: 9 cells. For each: correct iff (userSaysAI === !isNotAI). User said no AI → for non-AI cells (1,6,8) that's correct (3); for AI cells (2,3,4,5,7,9) that's wrong (0). Score = 3. ✓
- Mark exactly 2,3,4,5,7,9: score = 9 (perfect).
- Mark all 9: score = 6 (the AI ones; the 3 non-AI marked are wrong).

- [ ] **Step 3: Verify SV behavior**

```bash
open "http://localhost:8000/sv/ai-eller-manniska/#test-image"
```

Same checks in Swedish.

- [ ] **Step 4: Wait for Johan's "kör"**

- [ ] **Step 5: Commit Phase D (after "kör")**

```bash
git add assets/js/ai-or-human.js ai-or-human/index.html sv/ai-eller-manniska/index.html
git commit -m "$(cat <<'EOF'
feat(ai-or-human): Test 2 — image grid quiz with hint flipcards

Photo grid in image-frame, 9 numbered checkboxes, score against
data-correct-not-ai, two flippable hint cards. Reset flips hints back.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Phase E — Test 3: Videos

**Goal:** Three video placeholders, single-choice radios, score against `data-correct-video`.

### Task E1: Write Test 3 markup (EN)

**Files:**
- Modify: `ai-or-human/index.html`

- [ ] **Step 1: Replace EN Test 3 stub**

```html
<section class="section container quiz-section" id="test-video" data-test="video"
         data-correct-video="2"
         data-feedback-correct="Correct!"
         data-feedback-wrong="Wrong — it was video {correct}."
         data-feedback-pending="Videos coming soon — Johan will fill the answer in once they're up.">
  <h2 class="section__title">Test 3 — Videos</h2>
  <p class="section__lede">Three videos. One is AI-generated, two are not. Which one do you think is AI?</p>

  <div class="quiz-grid--3" data-quiz-videos>
    <article class="video-tile">
      <span class="video-tile__label">1</span>
      <video controls preload="metadata" data-src="/assets/videos/ai-or-human/video-a.mp4"></video>
    </article>
    <article class="video-tile">
      <span class="video-tile__label">2</span>
      <video controls preload="metadata" data-src="/assets/videos/ai-or-human/video-b.mp4"></video>
    </article>
    <article class="video-tile">
      <span class="video-tile__label">3</span>
      <video controls preload="metadata" data-src="/assets/videos/ai-or-human/video-c.mp4"></video>
    </article>
  </div>

  <div class="quiz-options" data-quiz-radios>
    <label class="quiz-option"><input type="radio" name="video-guess" value="1"><span>Video 1</span></label>
    <label class="quiz-option"><input type="radio" name="video-guess" value="2"><span>Video 2</span></label>
    <label class="quiz-option"><input type="radio" name="video-guess" value="3"><span>Video 3</span></label>
  </div>

  <div class="quiz-controls">
    <button type="button" class="btn btn--primary" data-quiz-submit disabled>Done!</button>
    <button type="button" class="quiz-reset" data-quiz-reset>Reset</button>
  </div>
  <p class="quiz-feedback" data-quiz-feedback hidden aria-live="polite"></p>
</section>
```

### Task E2: Write Test 3 markup (SV)

**Files:**
- Modify: `sv/ai-eller-manniska/index.html`

- [ ] **Step 1: Mirror to SV with these substitutions**

- Heading: `Test 3 — Video`
- Lede: `Tre videor. En är AI-genererad, två är det inte. Vilken tror du är AI-genererad?`
- `data-feedback-correct`: `Rätt!`
- `data-feedback-wrong`: `Fel — det var video {correct}.`
- `data-feedback-pending`: `Video kommer snart — facit läggs in när videorna är på plats.`
- Video labels: `Video 1`, `Video 2`, `Video 3`
- Placeholder text: `Video kommer snart`
- Submit: `Klar!`, Reset: `Nollställ`

### Task E3: Add `initVideoTest` to JS

**Files:**
- Modify: `assets/js/ai-or-human.js`

- [ ] **Step 1: Add the function**

After `initImageTest` inside the IIFE:

```js
// ───── Test 3: Videos ─────

function initVideoTest(rootEl) {
  const radios = Array.from(rootEl.querySelectorAll('[data-quiz-radios] input[type="radio"]'));
  const submitBtn = rootEl.querySelector('[data-quiz-submit]');
  const resetBtn = rootEl.querySelector('[data-quiz-reset]');
  const feedback = rootEl.querySelector('[data-quiz-feedback]');
  const correct = parseInt(rootEl.dataset.correctVideo || '0', 10);
  const tmplCorrect = rootEl.dataset.feedbackCorrect || 'Correct!';
  const tmplWrong = rootEl.dataset.feedbackWrong || 'Wrong — it was video {correct}.';
  const tmplPending = rootEl.dataset.feedbackPending || 'Answer not yet defined.';

  // Wire video src from data-src (so empty string = no media loaded).
  rootEl.querySelectorAll('video[data-src]').forEach(v => {
    if (v.dataset.src) {
      v.src = v.dataset.src;
      const ph = v.parentElement.querySelector('.video-tile__placeholder');
      if (ph) ph.remove();
    }
  });

  function onRadioChange() {
    submitBtn.disabled = !radios.some(r => r.checked);
  }

  function onSubmit() {
    const picked = radios.find(r => r.checked);
    if (!picked) return;
    if (correct === 0) {
      feedback.textContent = tmplPending;
    } else if (parseInt(picked.value, 10) === correct) {
      feedback.textContent = tmplCorrect;
    } else {
      feedback.textContent = tmplWrong.replace('{correct}', String(correct));
    }
    feedback.hidden = false;
    revealRating(rootEl);
  }

  function onReset() {
    radios.forEach(r => { r.checked = false; });
    feedback.hidden = true;
    feedback.textContent = '';
    submitBtn.disabled = true;
  }

  radios.forEach(r => r.addEventListener('change', onRadioChange));
  submitBtn.addEventListener('click', onSubmit);
  resetBtn.addEventListener('click', onReset);
}
```

- [ ] **Step 2: Bootstrap**

In the `bootstrap()` function:

```js
document.querySelectorAll('[data-test="video"]').forEach(initVideoTest);
```

### Task E4: Phase E preview gate

- [ ] **Step 1: Verify EN**

```bash
open "http://localhost:8000/ai-or-human/#test-video"
```

- Three video tiles render with "Video coming soon" overlay and a "1/2/3" badge top-left.
- Submit disabled until a radio is selected.
- After picking and clicking "Done!" with `data-correct-video="2"`: pending message shown.

- [ ] **Step 2: Test the wired-up case (temporary local test)**

In DevTools console on the EN page:

```js
const sec = document.querySelector('#test-video');
sec.dataset.correctVideo = '2';
```

Then refresh the section by clicking "Reset" then re-selecting Video 2 → "Done!" → "Correct!". Pick Video 1 → "Done!" → "Wrong — it was video 2."

- [ ] **Step 3: Verify SV**

```bash
open "http://localhost:8000/sv/ai-eller-manniska/#test-video"
```

Same checks in Swedish.

- [ ] **Step 4: Wait for Johan's "kör"**

- [ ] **Step 5: Commit Phase E (after "kör")**

```bash
git add assets/js/ai-or-human.js ai-or-human/index.html sv/ai-eller-manniska/index.html
git commit -m "$(cat <<'EOF'
feat(ai-or-human): Test 3 — video placeholders + single-choice quiz

Three video tiles with placeholder overlay (data-src empty). Radio
group, submit gated by selection. data-correct-video=0 returns a
pending message until Johan supplies the answer.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Phase F — Difficulty rating + telemetry + privacy

**Goal:** Add the optional 1–6 rating widget under each test, send anonymous data to a Google Sheet via Apps Script, update the privacy page, document the Apps Script setup for Johan.

### Task F1: Add rating markup to all three sections (EN)

**Files:**
- Modify: `ai-or-human/index.html`

- [ ] **Step 1: Append rating block inside each `<section data-test="…">`**

Place this **inside** each test section, after the `<p class="quiz-feedback">` line. Three identical copies (one per test); only the difference is which section they sit in.

```html
<div class="rating" data-rating hidden>
  <p class="rating__heading">Was it easy or hard to spot the AI-generated content?</p>
  <p class="rating__hint">Optional — your vote is stored anonymously. <a href="/privacy/">Read more</a>.</p>
  <div class="rating__scale">
    <span class="rating__endlabel">Very easy</span>
    <button type="button" class="rating__btn" data-rating-btn="1" aria-pressed="false">1</button>
    <button type="button" class="rating__btn" data-rating-btn="2" aria-pressed="false">2</button>
    <button type="button" class="rating__btn" data-rating-btn="3" aria-pressed="false">3</button>
    <button type="button" class="rating__btn" data-rating-btn="4" aria-pressed="false">4</button>
    <button type="button" class="rating__btn" data-rating-btn="5" aria-pressed="false">5</button>
    <button type="button" class="rating__btn" data-rating-btn="6" aria-pressed="false">6</button>
    <span class="rating__endlabel">Very hard</span>
  </div>
</div>
```

### Task F2: Add rating markup (SV)

**Files:**
- Modify: `sv/ai-eller-manniska/index.html`

- [ ] **Step 1: Mirror with substitutions**

- Heading: `Var det lätt eller svårt att se vilket innehåll som var AI-genererat?`
- Hint: `Helt valfritt — din röst sparas anonymt. <a href="/privacy/">Läs mer</a>.` (Note: there is no SV privacy page yet — link goes to the EN page. A SV privacy page is out of scope for this plan; revisit if Johan wants to author one.)
- End labels: `Väldigt lätt`, `Väldigt svårt`

### Task F3: Wire `revealRating` + `initRating` + telemetry

**Files:**
- Modify: `assets/js/ai-or-human.js`

- [ ] **Step 1: Replace the placeholder `revealRating` and add the rating logic**

Replace the existing placeholder `revealRating` stub with this implementation, and add an `initRating` function:

```js
// ───── Rating widget + telemetry ─────

function getTestKey(rootEl) {
  return rootEl.dataset.test; // "text" | "image" | "video"
}

function getLastScore(rootEl) {
  // Pulled from the test's score state if available.
  // For simplicity we read the rendered feedback text — JS code that triggered
  // reveal already updated it. We extract digits as the score representation.
  const fb = rootEl.querySelector('[data-quiz-feedback]');
  if (!fb || fb.hidden) return { user: null, total: null };
  const text = fb.textContent || '';
  // Match patterns like "X of Y" or "X av Y".
  const m = text.match(/(\d+)\s*(?:of|av)\s*(\d+)/i);
  if (m) return { user: parseInt(m[1], 10), total: parseInt(m[2], 10) };
  // Test 3 returns "Correct!" / "Wrong …": treat as 1/1 or 0/1.
  if (/correct|rätt(?!\s*var)/i.test(text)) return { user: 1, total: 1 };
  if (/wrong|fel/i.test(text)) return { user: 0, total: 1 };
  return { user: null, total: null };
}

function postTelemetry(payload) {
  if (!TELEMETRY_URL) return;
  // Use text/plain body to avoid CORS preflight on Apps Script.
  fetch(TELEMETRY_URL, {
    method: 'POST',
    mode: 'no-cors',
    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
    body: JSON.stringify(payload)
  }).catch(() => { /* fire-and-forget */ });
}

function revealRating(rootEl) {
  const ratingEl = rootEl.querySelector('[data-rating]');
  if (!ratingEl) return;
  const key = getTestKey(rootEl);
  // If already rated this session, leave hidden.
  try {
    if (sessionStorage.getItem('aiOrHuman.rated.' + key)) return;
  } catch (_) { /* ignore storage errors */ }
  ratingEl.hidden = false;
  initRating(rootEl);
}

function initRating(rootEl) {
  const ratingEl = rootEl.querySelector('[data-rating]');
  if (!ratingEl || ratingEl.dataset.wired === '1') return;
  ratingEl.dataset.wired = '1';

  const buttons = Array.from(ratingEl.querySelectorAll('[data-rating-btn]'));
  const hint = ratingEl.querySelector('.rating__hint');
  const lang = (document.documentElement.lang || 'en').slice(0, 2);
  const thanks = lang === 'sv' ? 'Tack!' : 'Thanks!';

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      const rating = parseInt(btn.dataset.ratingBtn, 10);
      const key = getTestKey(rootEl);
      buttons.forEach(b => {
        b.disabled = true;
        b.setAttribute('aria-pressed', b === btn ? 'true' : 'false');
      });
      hint.textContent = thanks;
      try { sessionStorage.setItem('aiOrHuman.rated.' + key, '1'); } catch (_) {}

      const score = getLastScore(rootEl);
      postTelemetry({
        ts: new Date().toISOString(),
        lang: lang,
        test: key,
        rating: rating,
        userScore: score.user,
        totalScore: score.total
      });
    });
  });
}
```

- [ ] **Step 2: Verify the JS file is internally consistent**

```bash
node -c assets/js/ai-or-human.js
```

Expected: no output (syntax OK). If error, fix and re-check.

### Task F4: Update the EN privacy page

**Files:**
- Modify: `privacy/index.html`

(SV privacy page does not exist on the site — out of scope for this plan. The SV rating widget links to the EN privacy page. If Johan wants a SV privacy page later, that's a separate task.)

- [ ] **Step 1: Add a paragraph to the EN privacy page**

In `privacy/index.html`, find the main `<article>` or last text section and append:

```html
<h2>Difficulty ratings on /ai-or-human/</h2>
<p>If you choose to rate the difficulty of any test on the <a href="/ai-or-human/">AI or human?</a> page (1–6 scale, fully optional), your rating, the language version of the page, the test you rated, and your score on that test are sent anonymously to a Google Sheet owned by Johan. No cookies, no IP addresses, no user agent, and no session ID are stored. The rating is used only to understand how difficult visitors find the exercises in aggregate.</p>
```

### Task F5: Document Apps Script setup for Johan

**Files:**
- Create: `docs/internal/ai-or-human-apps-script-setup.md`

- [ ] **Step 1: Write the setup doc**

```markdown
# AI or human? — Apps Script setup

One-time setup so the difficulty ratings on /ai-or-human/ end up in a
Google Sheet you own.

## 1. Create the Sheet

1. Go to https://sheets.new
2. Title it: "AI or human — difficulty ratings"
3. In row 1, add headers: `timestamp | lang | test | rating | user_score | total_score`
4. Copy the Sheet ID from the URL (the long string between `/d/` and `/edit`).

## 2. Create the Apps Script

1. From the Sheet: Tools → Apps Script
2. Replace the default code with:

```js
const SHEET_ID = 'PASTE_SHEET_ID_HERE';

function doPost(e) {
  const data = JSON.parse(e.postData.contents);
  const sheet = SpreadsheetApp.openById(SHEET_ID).getActiveSheet();
  sheet.appendRow([
    new Date(data.ts),
    data.lang,
    data.test,
    data.rating,
    data.userScore,
    data.totalScore
  ]);
  return ContentService.createTextOutput(JSON.stringify({ ok: true }))
    .setMimeType(ContentService.MimeType.JSON);
}
```

3. Replace `PASTE_SHEET_ID_HERE` with the ID you copied above.
4. Click the disk icon to save.

## 3. Deploy as Web App

1. Click "Deploy" → "New deployment"
2. Click the gear icon → choose "Web app"
3. Description: "AI or human ratings"
4. Execute as: **Me**
5. Who has access: **Anyone**
6. Click "Deploy"
7. Authorize access when prompted (Google warns because the script writes to your Sheet — that's expected).
8. Copy the **Web app URL** that's displayed.

## 4. Wire the URL into the site

Open `assets/js/ai-or-human.js`. At the top:

```js
const TELEMETRY_URL = ''; // ← paste your Web app URL here as a string
```

Change the empty string to your URL, e.g.:

```js
const TELEMETRY_URL = 'https://script.google.com/macros/s/AKfycbx.../exec';
```

Commit, push, and ratings will start landing in your Sheet.

## Test it

After deploying, open the site, complete a test, click a rating. Check the Sheet — a new row should appear within a few seconds.

## Privacy notes

The Web app's execution log shows requests by default. To disable per-request logging:
1. In Apps Script, click the gear → "Project settings"
2. Uncheck "Show 'appsscript.json' manifest file in editor" if shown
3. The execution log can also be cleared periodically.

No IPs are stored in the Sheet itself.
```

### Task F6: Phase F preview gate

- [ ] **Step 1: Verify rating widget reveal (EN)**

```bash
open "http://localhost:8000/ai-or-human/"
```

For each test:
- Complete the test (submit).
- Rating widget should reveal below the score.
- Click a rating button → button highlights, all buttons disable, "Thanks!" replaces the hint.
- Reload the page → complete the same test again → rating widget should NOT re-appear (sessionStorage gate).

- [ ] **Step 2: Verify SV**

```bash
open "http://localhost:8000/sv/ai-eller-manniska/"
```

Same checks; copy in Swedish.

- [ ] **Step 3: Verify telemetry no-ops with empty URL**

In DevTools Network tab, complete a test and rate — confirm no POST request to any external URL is made (since `TELEMETRY_URL` is `''`).

- [ ] **Step 4: Verify privacy page links work**

Click the "Read more" / "Läs mer" link in the rating hint — both should navigate to the privacy page.

- [ ] **Step 5: Wait for Johan's "kör"**

- [ ] **Step 6: Commit Phase F (after "kör")**

```bash
git add assets/css/components.css assets/js/ai-or-human.js \
        ai-or-human/index.html sv/ai-eller-manniska/index.html \
        privacy/index.html \
        docs/internal/ai-or-human-apps-script-setup.md
git commit -m "$(cat <<'EOF'
feat(ai-or-human): optional 1-6 difficulty rating + Apps Script telemetry

Per-test rating widget reveals after submit. Anonymous POST to a
Johan-owned Google Sheet via Apps Script. TELEMETRY_URL empty by
default — UI still confirms with "Tack!", no network call. Privacy
pages updated. Setup doc for Johan in docs/internal/.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Phase G — Final QA + handoff

### Task G1: Mobile responsive check

- [ ] **Step 1: Open the EN page in iPhone preset (Safari Develop menu or Chrome devtools)**

Verify at 375px wide:
- Hero text is readable, no horizontal scroll.
- Test 1 cards stack to single column.
- Test 2 image scales to width; checkboxes wrap to 2 rows.
- Test 3 video tiles stack to single column.
- Rating buttons remain tappable (≥44px target after CSS scale-down).
- Nav burger toggles on tap.

- [ ] **Step 2: Repeat for SV**

### Task G2: Accessibility check

- [ ] **Step 1: Keyboard navigation**

Tab through the EN page. Verify:
- All checkboxes, radios, buttons reachable.
- "Show answers" button focusable when enabled, skipped when disabled.
- Rating buttons reachable.
- Focus ring visible on each.

- [ ] **Step 2: Screen reader smoke**

Use VoiceOver (Cmd+F5 on macOS). Verify:
- Score lines announced via `aria-live="polite"`.
- Buttons have meaningful text.
- Image has descriptive alt.

### Task G3: Cross-language verification

- [ ] **Step 1: Switch language each direction**

Click EN→SV in the lang switcher. Land on `/sv/ai-eller-manniska/`. Click back. Land on `/ai-or-human/`.

### Task G4: Final grep sweep

- [ ] **Step 1: No stale references**

```bash
grep -rln "notebooklm-styles\|notebooklm-stilar" \
  --include="*.html" --include="*.json" --include="*.js" --include="*.xml" --include="*.txt" --include="*.css" \
  | grep -v ^notebooklm-styles/ | grep -v ^sv/notebooklm-stilar/
```

Expected: zero matches.

```bash
grep -rln "TODO" ai-or-human/ sv/ai-eller-manniska/
```

Expected: only the two ipsum-placeholder comments awaiting Johan's text.

### Task G5: Final commit + handoff

- [ ] **Step 1: Confirm all phases committed**

```bash
git log --oneline -10
```

Expected: visible commits for Phases A through F.

- [ ] **Step 2: Send Johan the Apps Script setup doc path**

Tell Johan: "When you have 10 minutes free, follow `docs/internal/ai-or-human-apps-script-setup.md` to set up the Sheet. Send me the Web app URL and I'll paste it into `assets/js/ai-or-human.js`."

- [ ] **Step 3: Note the still-pending items**

In a wrap-up message:
- Johan to write his own Topic A and Topic B texts (replacing the two ipsum placeholders).
- Johan to find and add 3 video files; once added, set `data-correct-video` to the right number.
- Johan to deploy the Apps Script and provide the URL.

---

## Self-review summary

- Spec coverage: All sections of `2026-04-26-ai-or-human-design.md` map to a task: §3 (Phase A), §4.1 (Phase B), §4.2 (Phase C), §4.3 (Phase D), §4.4 (Phase E), §4.5 + §4.6 (Phase F), §7 (Phase B + Phase A), §9 acceptance criteria 1–11 covered across phases.
- No placeholders in the plan: all code is concrete; the only literal placeholders are the two ipsum bodies (intentional, documented).
- Type/method consistency: `flipCard`, `revealRating`, `initRating`, `getTestKey`, `getLastScore`, `postTelemetry` — names consistent across phases. `data-test` attribute values (`text`/`image`/`video`) consistent. `data-quiz-*` attributes consistent.
- Workflow: every commit is gated by Johan's "kör" per the preview-then-commit memory.
