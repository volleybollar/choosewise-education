# Apple Intelligence Guide — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a pedagogically transparent Apple Intelligence guide (EN + SV web pages, full PDFs, Quick Start handouts) positioned on the GDPR / on-device-privacy angle, following the established Claude/Gemini guide pattern.

**Architecture:** Copy Claude guide as structural template; swap accent color to graphite `#3E4A57`; adapt 4-part IA to 3-part IA (Kom igång, Arbeta smartare, GDPR-fördelen); iPad-first examples; 6 core features. Build EN → SV → PDFs → Quick Starts → integration. No custom JavaScript beyond what Claude already has (sticky nav, FAQ toggle, copy prompts).

**Tech Stack:** Vanilla HTML/CSS/JS (no build step for web); Playwright + pypdf for PDF generation; MailerLite gate for full-PDF downloads (same pattern as Claude/Gemini).

**Spec:** [docs/superpowers/specs/2026-04-19-apple-intelligence-guide-design.md](../specs/2026-04-19-apple-intelligence-guide-design.md)

---

## File Structure

**Files to create:**
- `guides/apple-intelligence/index.html` — EN web guide (~900 lines)
- `guides/apple-intelligence/styles.css` — adapted from Claude styles + new graphite accent (~700 lines)
- `guides/apple-intelligence/script.js` — copied from Claude (141 lines, unchanged)
- `sv/guider/apple-intelligence/index.html` — SV web guide
- `sv/guider/apple-intelligence/styles.css` — mirrors EN
- `sv/guider/apple-intelligence/script.js` — mirrors EN
- `exports/apple-intelligence-print-a4-en.html` — EN print source (~600 lines)
- `exports/apple-intelligence-print-a4-sv.html` — SV print source
- `exports/apple-intelligence-quick-start-en.html` — EN 2-page handout (~450 lines)
- `exports/apple-intelligence-quick-start-sv.html` — SV 2-page handout
- `exports/build-apple-intelligence-pdf.py` — Playwright builder for full PDFs
- `exports/build-apple-intelligence-quickstart-pdf.py` — Playwright builder for Quick Starts
- `assets/images/guide-covers/apple.svg` — cover card SVG (~100 lines)
- `assets/pdfs/guides/apple-intelligence-guide-en.pdf` — generated, committed
- `assets/pdfs/guides/apple-intelligence-guide-sv.pdf` — generated, committed
- `assets/pdfs/guides/apple-intelligence-quick-start-en.pdf` — generated, committed
- `assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf` — generated, committed

**Files to modify:**
- `guides/guides-en.json` — flip `apple-intelligence` entry from `"status": "coming-soon"` to `"status": "available"`
- `sv/guider/guides-sv.json` — same

**Decision on images:** Claude and Gemini guides use JPG cover + part-opener images. For Apple MVP, **use pure typographic hero sections** (no photos, gradient background + bold type) to avoid image-sourcing blocker. Real Nano-Banana-generated images can be added in a follow-up task.

---

## Phase 0 — Setup

### Task 0.1: Create directory structure

**Files:** directories only, no code yet

- [ ] **Step 1: Create EN guide directory**

```bash
mkdir -p "guides/apple-intelligence/assets"
```

- [ ] **Step 2: Create SV guide directory**

```bash
mkdir -p "sv/guider/apple-intelligence/assets"
```

- [ ] **Step 3: Verify**

```bash
ls -la guides/apple-intelligence/ sv/guider/apple-intelligence/
```

Expected: two empty directories + `assets/` subdirectory in each.

- [ ] **Step 4: No commit yet** (empty dirs, commit after Task 0.2)

---

### Task 0.2: Create placeholder cover SVG

**Files:**
- Create: `assets/images/guide-covers/apple.svg`

- [ ] **Step 1: Inspect existing covers for consistency**

```bash
ls assets/images/guide-covers/
cat assets/images/guide-covers/claude.svg | head -40
```

Note: Copy the structural pattern (viewBox, background rect, typography).

- [ ] **Step 2: Write `assets/images/guide-covers/apple.svg`**

600×400 viewBox SVG with:
- Background: gradient from graphite `#3E4A57` to near-black `#1A1A1F`
- Accent stroke line (brass `#C8A86B`, 2px, horizontal at y=240)
- Eyebrow text: `AI IN EDUCATION` (white, Inter, 10pt, 2pt letter-spacing, uppercase, positioned y=80, centered)
- Title (two lines): `Apple Intelligence` on first line, `for teachers` on second — Playfair Display, 38pt white, centered, y=180 and y=220
- Small subtitle below stroke: `private by design` in italic serif, y=280
- Corner attribution: `choosewise.education` bottom right, Inter 9pt uppercase 2pt letter-spacing, brass color

Follow the exact structural pattern in `claude.svg` — same `<defs>` gradient syntax, same `<g>` grouping.

- [ ] **Step 3: Verify SVG renders**

Open in browser:
```bash
open assets/images/guide-covers/apple.svg
```

Expected: readable title, graphite gradient, brass accent line.

- [ ] **Step 4: Commit**

```bash
git add assets/images/guide-covers/apple.svg guides/apple-intelligence/ sv/guider/apple-intelligence/
git commit -m "scaffold: Apple Intelligence guide directories + cover SVG"
```

---

## Phase 1 — EN Web Guide

### Task 1.1: Scaffold HTML skeleton

**Files:**
- Create: `guides/apple-intelligence/index.html`
- Reference: `guides/claude/index.html` (copy structure)

- [ ] **Step 1: Copy Claude HTML as starting skeleton**

```bash
cp guides/claude/index.html guides/apple-intelligence/index.html
```

- [ ] **Step 2: Open the file and modify lines 1-50 (head + brand nav)**

Update:
- `<title>` → `Apple Intelligence for teachers and school leaders — Johan Lindström`
- `<meta name="description">` → `How Apple Intelligence works, what stays on your device, and what it means for Swedish schools. A pedagogically transparent guide.`
- Canonical URL → `https://choosewise.education/guides/apple-intelligence/`
- Open Graph image → `/assets/images/guide-covers/apple.svg`
- OG title → `Apple Intelligence for teachers and school leaders`
- Keep `<link rel="stylesheet" href="styles.css">` (will adapt CSS in Task 1.8)

- [ ] **Step 3: Clear body content**

Replace everything inside `<div class="jl-page">` with `<!-- CONTENT -->` placeholder. Keep:
- Top nav partial include: `<div data-include="/assets/partials/header-en.html"></div>`
- Bottom footer partial include: `<div data-include="/assets/partials/footer-en.html"></div>`
- Script references at bottom: `include.js` and `mailerlite-gate.js`
- The `<div class="jl-page">` wrapper itself

- [ ] **Step 4: Verify file opens in browser without errors**

Start a local server:
```bash
python3 -m http.server 8080 --directory "/Users/johan/Projekt/JLSU/Ny JLSU hemsida" &
```

Open `http://localhost:8080/guides/apple-intelligence/`. Expected: blank page with header + footer partials visible, no JS errors in console.

- [ ] **Step 5: Commit**

```bash
git add guides/apple-intelligence/index.html
git commit -m "scaffold: Apple Intelligence EN skeleton (head + partials)"
```

---

### Task 1.2: Write hero + anchor nav

**Files:**
- Modify: `guides/apple-intelligence/index.html` (replace `<!-- CONTENT -->` placeholder)

- [ ] **Step 1: Insert hero section**

Replace `<!-- CONTENT -->` with hero HTML matching Claude's structural pattern (see `guides/claude/index.html:54-120` for reference):

```html
<!-- ═══════════════════════════════════════════════════ -->
<!--                       HERO                           -->
<!-- ═══════════════════════════════════════════════════ -->
<section class="hero">
  <div class="hero__inner">
    <p class="eyebrow">AI in Education · Practical Guide</p>
    <h1>Apple Intelligence for teachers and school leaders</h1>
    <p class="lede">A practical, GDPR-aware guide to the AI features built into your iPad, Mac, and iPhone — what stays on the device, what doesn't, and what that means for classroom work.</p>

    <div class="hero__meta">
      <span class="meta-chip">Updated April 2026</span>
      <span class="meta-chip">iPad-first examples</span>
      <span class="meta-chip">25-page PDF</span>
    </div>

    <div class="hero__ctas">
      <a class="button button--primary" href="#part-1">Start reading</a>
      <a class="button button--secondary" href="#download">Download PDF</a>
    </div>
  </div>
</section>

<!-- ═══════════════════════════════════════════════════ -->
<!--                    ANCHOR NAV                        -->
<!-- ═══════════════════════════════════════════════════ -->
<nav class="anchor-nav" id="anchorNav" aria-label="On this page">
  <div class="anchor-nav__inner">
    <ul class="anchor-nav__list">
      <li><a href="#part-1" data-section="part-1">Get started</a></li>
      <li><a href="#part-2" data-section="part-2">Work smarter</a></li>
      <li><a href="#part-3" data-section="part-3">The GDPR angle</a></li>
      <li><a href="#faq" data-section="faq">FAQ</a></li>
      <li><a href="#download" data-section="download">Download PDF</a></li>
    </ul>
  </div>
</nav>
```

- [ ] **Step 2: Reload browser, verify hero appears**

Expected: eyebrow, H1, lede, 3 meta chips, 2 CTAs. Anchor nav not yet visible (requires CSS + scroll-trigger in Task 1.9).

- [ ] **Step 3: Commit**

```bash
git add guides/apple-intelligence/index.html
git commit -m "content: Apple Intelligence EN — hero + anchor nav"
```

---

### Task 1.3: Write Part 1 — Get started + Private Cloud Compute

**Files:**
- Modify: `guides/apple-intelligence/index.html`

- [ ] **Step 1: Add Part 1 section**

Append after the `<nav>` element. Structure (fill in prose during writing):

```html
<!-- ═══════════════════════════════════════════════════ -->
<!--                     PART 1                           -->
<!-- ═══════════════════════════════════════════════════ -->
<section class="section section--surface" id="part-1">
  <div class="section__inner">
    <p class="part-label">Part 1</p>
    <h2>Get started</h2>
    <p class="part-lede">What runs Apple Intelligence, what it can actually do today, and — the important bit — how Apple's "on-device" claim actually works when you look closely.</p>

    <!-- 1.1 Hardware + language support -->
    <h3 id="p1-hardware">Which devices run Apple Intelligence</h3>
    <p>[CONTENT: 2-3 paragraphs covering: iPad M1+ / Mac M-series / iPhone 15 Pro+; Swedish language support status as of April 2026; how to check if your device supports it (Settings → Apple Intelligence); age-gate note: 18+ for some features, see Section 3 for details]</p>

    <!-- 1.2 First setup -->
    <h3 id="p1-setup">Turning it on (iPad-first)</h3>
    <p>[CONTENT: Step-by-step. Settings → Apple Intelligence → Join Waitlist / Enable. Time to download (~4 GB). Note that Macs show it in System Settings. iPhone variant in a sidenote.]</p>

    <!-- 1.3 Private Cloud Compute explainer -->
    <h3 id="p1-pcc">Private Cloud Compute — what it actually is</h3>
    <div class="explainer-box">
      <p class="explainer-box__title">The distinction that matters</p>
      <p>[CONTENT: Clarify the three tiers:
        (1) On-device — most Writing Tools ops, simple Siri
        (2) Private Cloud Compute — longer/complex requests, encrypted, Apple cannot inspect, verifiable via Apple's published server images
        (3) ChatGPT — opt-in, different privacy model, text leaves Apple's ecosystem
      3-4 paragraphs. Include a small table or visual that distinguishes these.]</p>
    </div>

    <!-- 1.4 Värt att veta -->
    <aside class="sidenote">
      <p class="sidenote__title">Worth knowing (but outside this guide's scope)</p>
      <p>[CONTENT: 2-3 sentences per item on Image Playground, Genmoji, Clean Up in Photos. Why they're not in Part 2: creative tools that students will explore themselves; pedagogical value is narrow; privacy profile is the same as Writing Tools so the analysis in Part 3 applies.]</p>
    </aside>
  </div>
</section>
```

- [ ] **Step 2: Write the actual prose** for each `[CONTENT: ...]` block

Target: ~1000-1200 words total for Part 1. Tone: pedagogically transparent. Cite Apple's own security documentation (security.apple.com/docs/private-cloud-compute.pdf) for Private Cloud Compute claims, not marketing copy.

**Writing guidance for Private Cloud Compute section specifically:**
- Explain "stateless computation" — Apple servers don't retain request data after the response
- Explain "verifiable" — Apple publishes the server software images; security researchers can audit
- Do not overclaim: acknowledge that "Apple cannot inspect" is a trust assertion that depends on Apple's implementation being what they say it is
- Compare concretely: a Writing Tools rewrite on iPad → usually on-device; a long-form summary of a 10-page policy doc → Private Cloud Compute

- [ ] **Step 3: Verify in browser**

Reload `http://localhost:8080/guides/apple-intelligence/`. Expected: Part 1 header + 4 subsections render (may look unstyled in places — CSS comes in Task 1.8).

- [ ] **Step 4: Commit**

```bash
git add guides/apple-intelligence/index.html
git commit -m "content: Apple Intelligence EN — Part 1 (Get started + PCC explainer)"
```

---

### Task 1.4: Write Part 2 — Work smarter (6 features)

**Files:**
- Modify: `guides/apple-intelligence/index.html`

- [ ] **Step 1: Add Part 2 section scaffold**

```html
<!-- ═══════════════════════════════════════════════════ -->
<!--                     PART 2                           -->
<!-- ═══════════════════════════════════════════════════ -->
<section class="section" id="part-2">
  <div class="section__inner">
    <p class="part-label">Part 2</p>
    <h2>Work smarter</h2>
    <p class="part-lede">Six features that change day-to-day teaching work, with practical examples from real classrooms and a clear note on where each one processes your data.</p>

    <!-- Feature sections here (one per feature) -->
  </div>
</section>
```

- [ ] **Step 2: Write each of the 6 feature sub-sections**

Each feature follows this template (repeat 6 times):

```html
<article class="feature-card" id="p2-writing-tools">
  <h3>1. Writing Tools</h3>
  <p class="feature-card__what">[WHAT IT DOES: 1 paragraph, 40-60 words]</p>

  <h4>Classroom examples</h4>
  <ul class="example-list">
    <li><strong>[Scenario label]:</strong> [2-3 sentence description, iPad-first]</li>
    <li>[3-5 examples per feature]</li>
  </ul>

  <div class="processing-callout">
    <p class="processing-callout__title">Where it runs</p>
    <p>[1-2 sentences: on-device / Private Cloud Compute / ChatGPT-opt-in breakdown for THIS feature]</p>
  </div>

  <h4>How to start</h4>
  <ol class="steps">
    <li>[Numbered iPad steps]</li>
    <li>[...]</li>
  </ol>

  <p class="feature-card__mac-note"><strong>On Mac:</strong> [1 sentence if genuinely different, otherwise omit this line]</p>
</article>
```

**The 6 features (in order):**
1. **Writing Tools** — rewrite, proofread, summarize. Examples: assessment comments, parent emails, lesson plans. Where it runs: mostly on-device; longer documents trigger PCC.
2. **Siri 2.0** — schedule-aware, on-device actions. Examples: "open my planning notes for Week 12", "what's the next parent meeting?". Where it runs: all on-device unless asking for ChatGPT pass-through.
3. **Mail categorization + Priority** — Primary / Transactions / Updates / Promotions. Examples: sort 80 parent emails after a field trip announcement. Where it runs: on-device.
4. **Notification summaries** — summarize stacks of notifications. Examples: dawn check of 60 school-hours notifications on iPad. Where it runs: on-device.
5. **Notes + Image Wand** — sketch-to-image. Examples: rough circle + label → clean whiteboard-ready diagram; handout illustrations. Where it runs: Private Cloud Compute for rendering.
6. **Visual Intelligence** — camera context. Examples: point at a Swedish sign to translate; point at a textbook page to get summary. Where it runs: on-device for basic; PCC for summary; ChatGPT if user opts in for deeper questions.

Target: ~200-250 words per feature, 1200-1500 words total for Part 2.

- [ ] **Step 3: Verify in browser**

Expected: 6 feature articles stack vertically, each with heading, examples list, processing callout, steps.

- [ ] **Step 4: Commit**

```bash
git add guides/apple-intelligence/index.html
git commit -m "content: Apple Intelligence EN — Part 2 (6 features with processing callouts)"
```

---

### Task 1.5: Write Part 3 — The GDPR angle

**Files:**
- Modify: `guides/apple-intelligence/index.html`

- [ ] **Step 1: Add Part 3 section**

```html
<!-- ═══════════════════════════════════════════════════ -->
<!--                     PART 3                           -->
<!-- ═══════════════════════════════════════════════════ -->
<section class="section section--surface" id="part-3">
  <div class="section__inner">
    <p class="part-label">Part 3</p>
    <h2>The GDPR angle — in practice</h2>
    <p class="part-lede">Why on-device processing matters under Swedish and EU data protection law, where Apple's privacy story holds up, and the one place it breaks.</p>

    <h3 id="p3-stays">What stays on your device</h3>
    <p>[CONTENT: ~200 words. Concrete list: Writing Tools for short text, basic Siri, Mail categorization, Notification summaries. Why this matters under GDPR: Art. 4 definition of processing; if data never leaves the device, it's harder to argue a data transfer or third-party processor is involved.]</p>

    <h3 id="p3-pcc-use">When Private Cloud Compute is used</h3>
    <p>[CONTENT: ~250 words. Triggers: complex Writing Tools, long-form summaries, image generation, some visual-intelligence queries. What happens: encrypted to Apple servers, processed, discarded. Apple's stateless architecture and audit story. Honest note: this is still a data transfer to Apple. It has stronger legal/technical guarantees than a typical SaaS API call, but it IS processing by a third party. Schools should address this in their DPIA.]</p>

    <h3 id="p3-chatgpt">The ChatGPT exception</h3>
    <div class="warning-box">
      <p class="warning-box__title">This is where the on-device promise breaks</p>
      <p>[CONTENT: ~250 words. When the user opts in to ChatGPT integration: text/images are sent to OpenAI. Apple anonymizes the request but OpenAI receives actual content. Different privacy posture entirely: US-based processor, Schrems II concerns for EU data, OpenAI's training-data opt-out. Practical recommendation: disable ChatGPT integration on school-issued iPads by default via MDM; train staff to recognize the ChatGPT-prompt dialog.]</p>
    </div>

    <h3 id="p3-student-data">What this means for student data</h3>
    <p>[CONTENT: ~200 words. De-identify before any AI interaction. Distinction between teacher-work data (planning, parent emails without student names) and student data (names, grades, SEN plans). Even on-device processing of student names can be problematic if the device is shared or backed up to iCloud. The conservative rule: if the document would be sensitive in a cloud service, treat Apple Intelligence interactions with the same discipline.]</p>

    <h3 id="p3-policy">Five policy decisions for your school</h3>
    <ol class="policy-list">
      <li>[CONTENT: Numbered list of 5 concrete decisions. Examples: MDM profile for ChatGPT opt-in default, staff training on the three processing tiers, DPIA update, acceptable-use language, backup/iCloud considerations.]</li>
    </ol>
  </div>
</section>
```

- [ ] **Step 2: Write the actual prose**

Target: ~1100-1400 words for Part 3. This is the signature section — the one that justifies the guide's existence. Extra care on accuracy, cite Apple's PCC whitepaper and refer to GDPR articles by number.

- [ ] **Step 3: Verify in browser**

- [ ] **Step 4: Commit**

```bash
git add guides/apple-intelligence/index.html
git commit -m "content: Apple Intelligence EN — Part 3 (GDPR angle, signature section)"
```

---

### Task 1.6: Write FAQ section

**Files:**
- Modify: `guides/apple-intelligence/index.html`

- [ ] **Step 1: Add FAQ section using Claude guide's `<details class="faq-item">` pattern**

Reference: `guides/claude/index.html:940-1040` for exact FAQ markup.

```html
<!-- ═══════════════════════════════════════════════════ -->
<!--                       FAQ                            -->
<!-- ═══════════════════════════════════════════════════ -->
<section class="section" id="faq">
  <div class="section__inner">
    <p class="part-label">FAQ</p>
    <h2>Questions teachers ask</h2>

    <details class="faq-item">
      <summary>Does my iPad support Apple Intelligence?</summary>
      <div class="faq-body">
        <p>[CONTENT: 80-120 words per FAQ]</p>
      </div>
    </details>

    <!-- Repeat for 10 FAQ items total -->
  </div>
</section>
```

**The 10 FAQ questions (write prose for each):**
1. Does my iPad support Apple Intelligence?
2. Is Apple Intelligence available in Swedish?
3. Should I turn on the ChatGPT integration?
4. Can I use Apple Intelligence with student data?
5. How does this compare to Claude or Gemini?
6. What about Apple Intelligence on my personal iPhone — is that relevant for school use?
7. Does Apple Intelligence "train on my data"?
8. Is Apple Intelligence covered by my school's existing data processor agreement with Apple?
9. Can I turn off specific features (e.g., Mail categorization) while keeping Writing Tools?
10. Where do I get help if something goes wrong?

- [ ] **Step 2: Verify in browser** — click summary, check body reveals

- [ ] **Step 3: Commit**

```bash
git add guides/apple-intelligence/index.html
git commit -m "content: Apple Intelligence EN — FAQ (10 questions)"
```

---

### Task 1.7: Add CTA band + license band + footer

**Files:**
- Modify: `guides/apple-intelligence/index.html`

- [ ] **Step 1: Add CTA band (reference `guides/claude/index.html:1040-1060`)**

```html
<!-- ═══════════════════════════════════════════════════ -->
<!--                  DARK CTA BAND                       -->
<!-- ═══════════════════════════════════════════════════ -->
<section class="cta-band" id="download">
  <h2>Take the guide with you</h2>
  <p>Download the portable PDF — same content, premium layout, perfect for offline reading or sharing with your staff.</p>
  <div class="cta-stack">
    <button class="button button--primary" data-gate="apple-intelligence-guide-en" data-gate-pdf="/assets/pdfs/guides/apple-intelligence-guide-en.pdf">
      Download the Guide (PDF)
    </button>
    <a class="button button--on-dark" href="/assets/pdfs/guides/apple-intelligence-quick-start-en.pdf" download>
      Download the Quick Start (2 pages)
    </a>
  </div>
  <p class="cta-fineprint">Updated April 2026.</p>
</section>
```

- [ ] **Step 2: Add license band (identical structure to Claude/Gemini)**

```html
<!-- ═══════════════════════════════════════════════════ -->
<!--                   LICENSE BAND                       -->
<!-- ═══════════════════════════════════════════════════ -->
<section class="license-band" aria-label="License">
  <div class="license-inner">
    <p class="license-title">License</p>
    <p class="license-body">
      <strong>This work is licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="noopener">CC BY-NC-SA 4.0</a>.</strong>
      You may copy, share, and adapt this material for non-commercial purposes, provided you credit Johan Lindström and share any adaptations under the same license.
    </p>
  </div>
</section>
```

- [ ] **Step 3: Add footer**

```html
<footer class="footer">
  <p>© 2026 Johan Lindström · Free to share with attribution.<br>
  <a href="https://choosewise.education">Visit the main site</a> · <a href="https://www.linkedin.com/in/johan-lindstr%C3%B6m-b290a85/">Follow on LinkedIn</a></p>
</footer>
```

- [ ] **Step 4: Verify in browser** — all three bands render, download buttons visible

- [ ] **Step 5: Commit**

```bash
git add guides/apple-intelligence/index.html
git commit -m "content: Apple Intelligence EN — CTA band + license band + footer"
```

---

### Task 1.8: Adapt styles.css with graphite accent

**Files:**
- Create: `guides/apple-intelligence/styles.css`
- Reference: `guides/claude/styles.css`

- [ ] **Step 1: Copy Claude styles as baseline**

```bash
cp guides/claude/styles.css guides/apple-intelligence/styles.css
```

- [ ] **Step 2: Update the `:root` token block (lines 1-30 of Claude styles)**

Change these values only:

```css
:root {
  /* ── Color tokens ── */
  --color-primary:    #1B2733;   /* deep navy — unchanged, site consistency */
  --color-primary-2:  #3E4A57;   /* NEW: soft graphite, Apple guide accent */
  --color-accent:     #C8A86B;   /* antique brass — unchanged */
  --color-accent-2:   #A8B3BE;   /* NEW: cool silver, used sparingly for Apple-specific UI metaphors */
  --color-surface:    #F6F3EE;   /* cream — unchanged */
  --color-surface-2:  #EEEBE5;   /* slightly darker cream for callouts */
  --color-text:       #1A1A1F;   /* near-black — unchanged */
  --color-text-light: #6B7280;   /* cool gray — unchanged */

  /* keep existing spacing + typography tokens unchanged */
  --space-1: 8px;
  --space-2: 16px;
  --space-3: 24px;
  --space-4: 32px;
  --space-5: 48px;

  --font-serif: 'Playfair Display', Georgia, serif;
  --font-sans: 'Inter', -apple-system, sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;
}
```

- [ ] **Step 3: Swap instances of `var(--color-primary)` → `var(--color-primary-2)` in 3 places only**

Do NOT globally replace. Only replace in:
- `.hero` background-gradient (subtle shift)
- `.cta-band` background-gradient
- `.part-label` text color

Every other use of `--color-primary` (nav, links, buttons) stays navy for site consistency.

- [ ] **Step 4: Add new CSS blocks for Apple-specific components**

Append to end of `guides/apple-intelligence/styles.css`:

```css
/* ═══════════════════════════════════════════════════
   APPLE GUIDE — SPECIFIC COMPONENTS
   ═══════════════════════════════════════════════════ */

/* Processing callout (used on each feature card in Part 2) */
.jl-page .processing-callout {
  background: var(--color-surface-2);
  border-left: 3px solid var(--color-primary-2);
  padding: var(--space-2) var(--space-3);
  margin: var(--space-3) 0;
  border-radius: 2px;
}
.jl-page .processing-callout__title {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-primary-2);
  margin: 0 0 var(--space-1);
}
.jl-page .processing-callout p:last-child {
  margin: 0;
  font-size: 14px;
  color: var(--color-text);
}

/* Explainer box (used for Private Cloud Compute in Part 1) */
.jl-page .explainer-box {
  background: var(--color-surface);
  border: 1px solid rgba(27, 39, 51, 0.08);
  padding: var(--space-4);
  margin: var(--space-4) 0;
  border-radius: 4px;
}
.jl-page .explainer-box__title {
  font-family: var(--font-serif);
  font-size: 18px;
  color: var(--color-primary);
  margin: 0 0 var(--space-2);
}

/* Warning box (used for ChatGPT exception in Part 3) */
.jl-page .warning-box {
  background: #FBF6E9;
  border-left: 4px solid var(--color-accent);
  padding: var(--space-3);
  margin: var(--space-3) 0;
  border-radius: 2px;
}
.jl-page .warning-box__title {
  font-weight: 600;
  color: var(--color-primary);
  margin: 0 0 var(--space-1);
  font-size: 15px;
}

/* Feature card (used in Part 2) */
.jl-page .feature-card {
  padding: var(--space-4) 0;
  border-bottom: 1px solid rgba(27, 39, 51, 0.08);
}
.jl-page .feature-card:last-child { border-bottom: none; }
.jl-page .feature-card__what {
  font-size: 16px;
  color: var(--color-text);
  margin: var(--space-1) 0 var(--space-3);
}
.jl-page .feature-card__mac-note {
  font-size: 13px;
  color: var(--color-text-light);
  margin-top: var(--space-2);
  font-style: italic;
}

/* Policy list (numbered) */
.jl-page .policy-list {
  counter-reset: policy;
  list-style: none;
  padding: 0;
}
.jl-page .policy-list li {
  counter-increment: policy;
  position: relative;
  padding-left: 40px;
  margin-bottom: var(--space-2);
}
.jl-page .policy-list li::before {
  content: counter(policy);
  position: absolute;
  left: 0;
  top: 0;
  width: 28px;
  height: 28px;
  background: var(--color-primary-2);
  color: white;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 13px;
}

/* Sidenote (used for "Värt att veta" in Part 1) */
.jl-page .sidenote {
  border-left: 2px solid var(--color-text-light);
  padding: 0 var(--space-3);
  margin: var(--space-4) 0;
  color: var(--color-text-light);
  font-size: 14px;
}
.jl-page .sidenote__title {
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 var(--space-1);
  font-size: 13px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
```

- [ ] **Step 5: Verify in browser**

Reload. Expected: hero has subtle graphite shift, feature cards render, processing callouts and explainer boxes styled.

- [ ] **Step 6: Commit**

```bash
git add guides/apple-intelligence/styles.css
git commit -m "style: Apple Intelligence EN — adapt Claude styles with graphite accent + new components"
```

---

### Task 1.9: Copy script.js from Claude

**Files:**
- Create: `guides/apple-intelligence/script.js`

- [ ] **Step 1: Copy**

```bash
cp guides/claude/script.js guides/apple-intelligence/script.js
```

- [ ] **Step 2: Update the `sectionIds` array inside the file**

Find the line `const sectionIds = ['part-1', 'part-2', 'part-3', 'prompts', 'download'];` (around line 32 of Claude's script.js) and change to:

```javascript
const sectionIds = ['part-1', 'part-2', 'part-3', 'faq', 'download'];
```

(Apple guide has FAQ instead of prompts section.)

- [ ] **Step 3: Add script reference to index.html**

Already present from Task 1.1 (copied from Claude). Verify the line exists near the end of index.html:

```html
<script src="script.js" defer></script>
```

- [ ] **Step 4: Verify in browser**

Scroll test: anchor nav should appear after hero scrolls out of view; clicking nav links should smooth-scroll to sections.

- [ ] **Step 5: Commit**

```bash
git add guides/apple-intelligence/script.js
git commit -m "feat: Apple Intelligence EN — anchor nav + FAQ script"
```

---

### Task 1.10: Full-page browser verification

**Files:** no code changes, verification only

- [ ] **Step 1: Open on desktop viewport (1440×900)**

Check each section:
- Hero: eyebrow, H1, lede, chips, CTAs
- Anchor nav appears on scroll
- Part 1: 4 subsections including PCC explainer and sidenote
- Part 2: 6 feature cards with processing callouts
- Part 3: 5 subsections including warning box and policy list
- FAQ: 10 collapsible items
- CTA band: 2 download buttons
- License band: CC BY-NC-SA visible
- Footer

- [ ] **Step 2: Open on iPad portrait (1024×1366)**

Check:
- Anchor nav fits horizontally without scroll (5 items)
- Feature cards don't overflow
- Processing callouts readable
- Policy list numbered circles align

- [ ] **Step 3: Open on iPhone portrait (390×844)**

Check:
- Hero H1 wraps correctly
- Anchor nav scrolls horizontally (expected behavior)
- FAQ items fit within viewport

- [ ] **Step 4: Console check**

Open DevTools Console. Expected: zero errors. (There may be 404s for Open Graph image if it's not yet rendered; that's expected until Task 7 finalization.)

- [ ] **Step 5: Commit** (only if fixes were needed)

No commit if verification passes. If issues found, fix and commit with `fix: Apple Intelligence EN — <issue>`.

---

## Phase 2 — SV Web Guide

### Task 2.1: Scaffold SV from EN

**Files:**
- Create: `sv/guider/apple-intelligence/index.html`
- Create: `sv/guider/apple-intelligence/styles.css`
- Create: `sv/guider/apple-intelligence/script.js`

- [ ] **Step 1: Copy all three EN files to SV location**

```bash
cp guides/apple-intelligence/index.html sv/guider/apple-intelligence/index.html
cp guides/apple-intelligence/styles.css sv/guider/apple-intelligence/styles.css
cp guides/apple-intelligence/script.js sv/guider/apple-intelligence/script.js
```

- [ ] **Step 2: Update `<html lang="en">` → `<html lang="sv">` and head metadata in SV index.html**

Change:
- `<title>` → `Apple Intelligence för lärare och skolledare — Johan Lindström`
- Description → `Hur Apple Intelligence fungerar, vad som stannar på enheten och vad det betyder för svenska skolor. En pedagogiskt transparent guide.`
- Canonical → `https://choosewise.education/sv/guider/apple-intelligence/`
- OG title → `Apple Intelligence för lärare och skolledare`
- Header partial → `header-sv.html` (was `header-en.html`)
- Footer partial → `footer-sv.html`

- [ ] **Step 3: Commit baseline (before translation)**

```bash
git add sv/guider/apple-intelligence/
git commit -m "scaffold: Apple Intelligence SV — copy EN structure + SV metadata"
```

---

### Task 2.2: Translate hero + anchor nav

**Files:**
- Modify: `sv/guider/apple-intelligence/index.html`

- [ ] **Step 1: Translate hero block**

Replace English copy with Swedish (natural professional Swedish — see `sv/guider/claude/index.html` for voice reference):

- `Eyebrow`: `AI i skolan · Praktisk guide`
- `H1`: `Apple Intelligence för lärare och skolledare`
- `Lede`: `En praktisk, GDPR-medveten guide till AI-funktionerna i din iPad, Mac och iPhone — vad som stannar på enheten, vad som inte gör det, och vad det betyder för arbetet i skolan.`
- Meta chips: `Uppdaterad april 2026` / `iPad-först exempel` / `25-sidig PDF`
- CTAs: `Börja läsa` / `Ladda ner PDF`

- [ ] **Step 2: Translate anchor nav labels**

- `Get started` → `Kom igång`
- `Work smarter` → `Arbeta smartare`
- `The GDPR angle` → `GDPR-fördelen`
- `FAQ` → `Vanliga frågor`
- `Download PDF` → `Ladda ner PDF`

- [ ] **Step 3: Verify** on `http://localhost:8080/sv/guider/apple-intelligence/`

- [ ] **Step 4: Commit**

```bash
git add sv/guider/apple-intelligence/index.html
git commit -m "content: Apple Intelligence SV — hero + anchor nav translated"
```

---

### Task 2.3: Translate Part 1

**Files:**
- Modify: `sv/guider/apple-intelligence/index.html`

- [ ] **Step 1: Translate Part 1 prose from EN version**

Key terminology decisions:
- "Apple Intelligence" — keep in English (product name)
- "Private Cloud Compute" — keep in English (product term), add Swedish gloss on first use: `Private Cloud Compute (Apples integritetsskyddade moln)`
- "on-device" → `på enheten`
- "Writing Tools" → keep in English (UI labels), add gloss `(skrivverktygen)` on first use
- "Siri" → `Siri`
- Section headings in Swedish:
  - `Which devices run Apple Intelligence` → `Vilka enheter kör Apple Intelligence`
  - `Turning it on (iPad-first)` → `Slå på det (iPad-först)`
  - `Private Cloud Compute — what it actually is` → `Private Cloud Compute — så fungerar det i praktiken`

Maintain the same structural HTML — only replace prose content.

- [ ] **Step 2: Verify**

- [ ] **Step 3: Commit**

```bash
git add sv/guider/apple-intelligence/index.html
git commit -m "content: Apple Intelligence SV — Part 1 translated"
```

---

### Task 2.4: Translate Part 2 (6 features)

**Files:**
- Modify: `sv/guider/apple-intelligence/index.html`

- [ ] **Step 1: Translate each of the 6 feature sections**

UI label terminology (keep English on first mention with Swedish gloss):
- Writing Tools → `Writing Tools (skrivverktyg)`
- Siri 2.0 → `Siri 2.0` (no gloss needed, same name)
- Mail categorization + Priority → `Mail-kategorisering + Priority-inkorgen`
- Notification summaries → `Notissammanfattningar`
- Notes + Image Wand → `Notes + Image Wand (bildtrollspö)`
- Visual Intelligence → `Visual Intelligence (kamera-kontext)`

Structure identical to EN. "Where it runs" → `Var beräkningen sker`. "How to start" → `Så kommer du igång`. "On Mac:" → `På Mac:`.

- [ ] **Step 2: Verify**

- [ ] **Step 3: Commit**

```bash
git add sv/guider/apple-intelligence/index.html
git commit -m "content: Apple Intelligence SV — Part 2 (6 features translated)"
```

---

### Task 2.5: Translate Part 3

**Files:**
- Modify: `sv/guider/apple-intelligence/index.html`

- [ ] **Step 1: Translate Part 3 prose**

Section headings:
- `What stays on your device` → `Vad som stannar på enheten`
- `When Private Cloud Compute is used` → `När Private Cloud Compute används`
- `The ChatGPT exception` → `ChatGPT-undantaget`
- `What this means for student data` → `Vad det betyder för elevdata`
- `Five policy decisions for your school` → `Fem policybeslut för din skola`

Warning box title: `Detta är där löftet om on-device bryts`

Reference GDPR articles by Swedish number (same as EU). When referencing Schrems II, use Swedish-language Swedish-readable phrasing.

- [ ] **Step 2: Verify**

- [ ] **Step 3: Commit**

```bash
git add sv/guider/apple-intelligence/index.html
git commit -m "content: Apple Intelligence SV — Part 3 translated (signature section)"
```

---

### Task 2.6: Translate FAQ

**Files:**
- Modify: `sv/guider/apple-intelligence/index.html`

- [ ] **Step 1: Translate all 10 FAQ items to Swedish**

Questions:
1. `Stöder min iPad Apple Intelligence?`
2. `Finns Apple Intelligence på svenska?`
3. `Ska jag slå på ChatGPT-integrationen?`
4. `Kan jag använda Apple Intelligence med elevdata?`
5. `Hur jämför det här med Claude eller Gemini?`
6. `Vad om Apple Intelligence på min privata iPhone — är det relevant för skolarbete?`
7. `Tränar Apple Intelligence på min data?`
8. `Täcks Apple Intelligence av skolans befintliga personuppgiftsbiträdesavtal med Apple?`
9. `Kan jag stänga av specifika funktioner (t.ex. Mail-kategorisering) utan att stänga av Writing Tools?`
10. `Var får jag hjälp om något går fel?`

- [ ] **Step 2: Update `sectionIds` in SV script.js to match SV anchor nav IDs** (if they differ — they shouldn't, keep English IDs for href consistency)

- [ ] **Step 3: Verify**

- [ ] **Step 4: Commit**

```bash
git add sv/guider/apple-intelligence/
git commit -m "content: Apple Intelligence SV — FAQ (10 questions translated)"
```

---

### Task 2.7: Translate CTA + license + footer

**Files:**
- Modify: `sv/guider/apple-intelligence/index.html`

- [ ] **Step 1: Translate CTA band**

- H2: `Ta guiden med dig`
- Body: `Ladda ner den portabla PDF:en — samma innehåll, premium-layout, perfekt för offline-läsning eller att dela med kollegor.`
- Primary button: `Ladda ner guiden (PDF)` + update `data-gate="apple-intelligence-guide-sv"` and `data-gate-pdf="/assets/pdfs/guides/apple-intelligence-guide-sv.pdf"`
- Secondary button: `Ladda ner Quick Start (2 sidor)` + update href to `/assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf`
- Fineprint: `Uppdaterad april 2026.`

- [ ] **Step 2: Translate license band**

Exact text (reuse Claude SV guide phrasing):

```html
<p class="license-title">Licens</p>
<p class="license-body">
  <strong>Det här verket är licensierat under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.sv" target="_blank" rel="noopener">CC BY-NC-SA 4.0</a>.</strong>
  Du får kopiera, dela och bearbeta materialet för icke-kommersiella ändamål, så länge du anger Johan Lindström som källa och behåller samma licens på eventuella bearbetningar.
</p>
```

- [ ] **Step 3: Translate footer**

```html
<p>© 2026 Johan Lindström · Får spridas fritt med angivande av författare.<br>
<a href="https://choosewise.education">Besök huvudsajten</a> · <a href="https://www.linkedin.com/in/johan-lindstr%C3%B6m-b290a85/">Följ på LinkedIn</a></p>
```

- [ ] **Step 4: Verify full SV page end-to-end**

- [ ] **Step 5: Commit**

```bash
git add sv/guider/apple-intelligence/index.html
git commit -m "content: Apple Intelligence SV — CTA + license + footer translated"
```

---

### Task 2.8: Full-page SV verification

**Files:** no code changes

- [ ] **Step 1: Side-by-side check** — open EN and SV in two browser windows

Expected: identical layout, only text differs. All IDs match (anchor nav should jump to same sections).

- [ ] **Step 2: Responsive check** on iPad + iPhone viewports

- [ ] **Step 3: Console check** — zero errors

---

## Phase 3 — EN Full PDF

### Task 3.1: Create print-a4-en.html

**Files:**
- Create: `exports/apple-intelligence-print-a4-en.html`
- Reference: `exports/gemini-notebooklm-print-a4-en.html` (copy structure)

- [ ] **Step 1: Copy Gemini print HTML as starting point**

```bash
cp exports/gemini-notebooklm-print-a4-en.html exports/apple-intelligence-print-a4-en.html
```

- [ ] **Step 2: Modify `<head>` and `<style>` block**

Update:
- `<title>` → `Apple Intelligence for teachers and school leaders`
- In the `<style>` block, find color tokens (near `--color-primary` or inline color values like `#c66b3d` which is Gemini's terracotta). Change to:
  - Primary: `#1B2733` (navy)
  - Accent: `#C8A86B` (brass) — replace all terracotta `#c66b3d` references
  - Surface: `#F6F3EE` (cream)

- [ ] **Step 3: Replace content with Apple-specific content**

This is the largest single task in the plan. Work section by section, preserving the print-HTML page structure (`<div class="page">` per printed page):

**Page 1 — Cover:**
- Eyebrow: `AI in education · Practical Guide`
- Title: `Apple Intelligence for teachers and school leaders`
- Subtitle: `A pedagogically transparent guide — what stays on your device, what doesn't, and why that matters in a Swedish school context`
- Author: `Johan Lindström · April 2026`

**Page 2 — Table of contents:**
- Part 1 — Get started (p.3-8)
- Part 2 — Work smarter (p.9-18)
- Part 3 — The GDPR angle (p.19-23)
- FAQ (p.24)
- About this guide + license (p.25)

**Pages 3-8 — Part 1:**
Adapt the web Part 1 content. Each logical section gets its own page or half-page.

**Pages 9-18 — Part 2:**
One page per feature (6 pages) + 4 pages for examples/screenshots/walk-throughs.

**Pages 19-23 — Part 3:**
Adapt Part 3 content; warning box becomes a full-width callout page.

**Page 24 — FAQ:**
Compact layout, 10 Q&A in two columns.

**Page 25 — Closing:**
Signature, license attribution (to be augmented by build script), "last updated" date.

- [ ] **Step 4: Verify HTML renders in browser at A4 print preview**

```bash
open "file:///Users/johan/Projekt/JLSU/Ny JLSU hemsida/exports/apple-intelligence-print-a4-en.html"
```

Then Cmd+P in Chrome → check page count (~25) and that no content is cut off at page boundaries.

- [ ] **Step 5: Commit**

```bash
git add exports/apple-intelligence-print-a4-en.html
git commit -m "content: Apple Intelligence EN — print-a4 HTML source"
```

---

### Task 3.2: Build script for full PDFs

**Files:**
- Create: `exports/build-apple-intelligence-pdf.py`
- Reference: `exports/build-gemini-notebooklm-pdf.py`

- [ ] **Step 1: Write build script**

```python
#!/usr/bin/env python3
"""Regenerate Apple Intelligence (EN + SV) A4 guide PDFs from print HTML."""
from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).parent.parent

def footer(title: str, page_label: str) -> str:
    return f"""
<div style="font-size: 8pt; color: #a5a59f; width: 100%; padding: 0 16mm 0 16mm;
            display: flex; justify-content: space-between; align-items: center;
            font-family: 'Inter', -apple-system, sans-serif;">
  <span>{title}</span>
  <span>{page_label} <span class="pageNumber"></span></span>
</div>
"""

jobs = [
    (
        root / "exports/apple-intelligence-print-a4-en.html",
        root / "assets/pdfs/guides/apple-intelligence-guide-en.pdf",
        footer("Apple Intelligence for teachers and school leaders", "Page"),
    ),
    (
        root / "exports/apple-intelligence-print-a4-sv.html",
        root / "assets/pdfs/guides/apple-intelligence-guide-sv.pdf",
        footer("Apple Intelligence för lärare och skolledare", "Sida"),
    ),
]

EMPTY_HEADER = "<div></div>"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    for src, dst, footer_template in jobs:
        if not src.exists():
            print(f"Skipping {dst.name} — source {src.name} not found")
            continue
        url = src.as_uri()
        print(f"Building {dst.name} from {src.name}")
        page.goto(url, wait_until="networkidle")
        page.emulate_media(media="print")
        dst.parent.mkdir(parents=True, exist_ok=True)
        page.pdf(
            path=str(dst),
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "14mm", "left": "0", "right": "0"},
            prefer_css_page_size=True,
            display_header_footer=True,
            header_template=EMPTY_HEADER,
            footer_template=footer_template,
        )
        print(f"  -> {dst.stat().st_size // 1024} KB")
    browser.close()
print("Done.")
```

- [ ] **Step 2: Run script (will skip SV since Task 4 hasn't run yet)**

```bash
python3 exports/build-apple-intelligence-pdf.py
```

Expected output: `Building apple-intelligence-guide-en.pdf from apple-intelligence-print-a4-en.html` → creates `~25 page` PDF. SV is skipped with "Skipping ... source not found".

- [ ] **Step 3: Verify page count**

```bash
python3 -c "
import pypdf
r = pypdf.PdfReader('assets/pdfs/guides/apple-intelligence-guide-en.pdf')
print(f'Pages: {len(r.pages)}')
print(f'Size: {r.pages[0].mediabox}')
"
```

Expected: ~25 pages, A4 (595x842 pt).

- [ ] **Step 4: Visual inspect PDF**

```bash
open assets/pdfs/guides/apple-intelligence-guide-en.pdf
```

Scan every page: cover, TOC, Part 1, Part 2, Part 3, FAQ, closing. Check for text overflow, orphaned headers, broken callouts.

- [ ] **Step 5: Commit**

```bash
git add exports/build-apple-intelligence-pdf.py assets/pdfs/guides/apple-intelligence-guide-en.pdf
git commit -m "feat: Apple Intelligence EN — build script + full PDF (25 pages)"
```

---

## Phase 4 — SV Full PDF

### Task 4.1: Create print-a4-sv.html

**Files:**
- Create: `exports/apple-intelligence-print-a4-sv.html`

- [ ] **Step 1: Copy EN print HTML as base**

```bash
cp exports/apple-intelligence-print-a4-en.html exports/apple-intelligence-print-a4-sv.html
```

- [ ] **Step 2: Update language and metadata**

- `<html lang="en">` → `<html lang="sv">`
- `<title>` → `Apple Intelligence för lärare och skolledare`

- [ ] **Step 3: Translate all page content**

Use same Swedish copy as the SV web guide (Task 2.3-2.7). Preserve the print-HTML page structure (don't change `<div class="page">` boundaries).

Cover eyebrow: `AI i skolan · Praktisk guide`
Cover title: `Apple Intelligence för lärare och skolledare`
Cover subtitle: `En pedagogiskt transparent guide — vad som stannar på enheten, vad som inte gör det, och varför det spelar roll i en svensk skolkontext`

TOC labels (match web guide section titles):
- Del 1 — Kom igång
- Del 2 — Arbeta smartare
- Del 3 — GDPR-fördelen
- Vanliga frågor
- Om guiden + licens

- [ ] **Step 4: Verify print preview**

- [ ] **Step 5: Commit**

```bash
git add exports/apple-intelligence-print-a4-sv.html
git commit -m "content: Apple Intelligence SV — print-a4 HTML source"
```

---

### Task 4.2: Build SV PDF

**Files:**
- No new files; reuse `exports/build-apple-intelligence-pdf.py`

- [ ] **Step 1: Run build script**

```bash
python3 exports/build-apple-intelligence-pdf.py
```

Expected: both EN and SV PDFs build.

- [ ] **Step 2: Verify page count**

```bash
python3 -c "
import pypdf
for name in ['apple-intelligence-guide-en.pdf', 'apple-intelligence-guide-sv.pdf']:
    r = pypdf.PdfReader(f'assets/pdfs/guides/{name}')
    print(f'{name}: {len(r.pages)} pages')
"
```

Both should be ~25 pages.

- [ ] **Step 3: Visual inspect SV PDF**

```bash
open assets/pdfs/guides/apple-intelligence-guide-sv.pdf
```

- [ ] **Step 4: Commit**

```bash
git add assets/pdfs/guides/apple-intelligence-guide-sv.pdf
git commit -m "feat: Apple Intelligence SV — full PDF (25 pages)"
```

---

## Phase 5 — EN Quick Start

### Task 5.1: Create EN quick-start HTML

**Files:**
- Create: `exports/apple-intelligence-quick-start-en.html`
- Reference: `exports/claude-quick-start-en.html`

- [ ] **Step 1: Copy Claude Quick Start as base**

```bash
cp exports/claude-quick-start-en.html exports/apple-intelligence-quick-start-en.html
```

- [ ] **Step 2: Update metadata**

- `<title>` → `Apple Intelligence Quick Start — for teachers`

- [ ] **Step 3: Replace content**

Preserve the 2-page A4 structure. Replace content:

**Page 1 — the 6 features in compact form:**

```html
<div class="page page1">
  <div class="masthead">
    <span class="eyebrow">Apple Intelligence Quick Start · for teachers</span>
    <span class="page-num">01 / 02</span>
  </div>

  <h1>The six Apple Intelligence features<br>that change classroom work</h1>
  <p class="subtitle">iPad-first, privacy-aware, takes 10 minutes to learn</p>
  <p class="lede">Apple Intelligence runs mostly on your device — a genuine GDPR advantage when your work involves sensitive content. These six features give you the strongest daily return. Details on what leaves the device are in Part 3 of the full guide.</p>

  <!-- Six feature mini-cards in a 2x3 grid -->
  <div class="feature-grid">
    <div class="feature-mini">
      <span class="idx">1</span>
      <h3>Writing Tools</h3>
      <p>Rewrite, proofread, summarize. Grading comments, parent emails, lesson plans. Most on-device.</p>
    </div>
    <!-- Repeat for 6 features -->
  </div>
</div>
```

**Page 2 — 5 tasks to try today + watch-out + closing:**

```html
<div class="page page2">
  <div class="masthead">
    <span class="eyebrow">5 things to try on your iPad today</span>
    <span class="page-num">02 / 02</span>
  </div>

  <h2>Try it: 5 practical tasks</h2>

  <div class="tasks">
    <!-- 5 tasks, one per feature + 1 wildcard -->
    <div class="task">
      <span class="idx">1</span>
      <div class="text"><strong>Rewrite a parent email in three tones</strong> — Writing Tools offers Friendly / Professional / Concise. Pick the one that fits, send.</div>
    </div>
    <!-- etc -->
  </div>

  <div class="watchout">
    <span class="label">● Watch out · age-gates and data</span>
    <p>Some features are 18+; verify your national rules for student-facing use. De-identify documents before Apple Intelligence processes them. Disable ChatGPT integration on school devices by default — it sends text to OpenAI and opens a different privacy conversation entirely.</p>
  </div>

  <div class="closing">
    <div class="msg">Want depth? Read the full <em>Apple Intelligence Guide</em> — or download the 25-page premium PDF from the same page.</div>
    <div class="url">choosewise.education / guides / apple-intelligence</div>
  </div>

  <div class="license-line">
    <span><strong>Licensed under CC BY-NC-SA 4.0</strong> — attribution, non-commercial, share-alike.</span>
    <span>creativecommons.org/licenses/by-nc-sa/4.0</span>
  </div>

  <div class="page-footer">
    <span>Apple Intelligence Quick Start — Johan Lindström</span>
    <span class="brand">choosewise.education</span>
    <span>Page 02 / 02</span>
  </div>
</div>
```

- [ ] **Step 4: Adapt CSS inside the `<style>` block**

Add feature-grid styles (2 columns x 3 rows):

```css
.feature-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin: 14px 0;
}
.feature-mini {
  padding: 8px 10px;
  border-left: 2px solid #3E4A57;
  background: #faf7f2;
  border-radius: 2px;
}
.feature-mini .idx {
  font-weight: 700;
  color: #3E4A57;
  font-size: 11px;
}
.feature-mini h3 {
  font-family: 'Fraunces', serif;
  font-size: 12.5px;
  margin: 2px 0 2px;
  color: #1e1e1c;
}
.feature-mini p {
  font-size: 10px;
  line-height: 1.5;
  color: #3a3a38;
  margin: 0;
}
```

- [ ] **Step 5: Verify in browser print preview** — check page count is exactly 2

- [ ] **Step 6: Commit**

```bash
git add exports/apple-intelligence-quick-start-en.html
git commit -m "content: Apple Intelligence EN — Quick Start HTML source"
```

---

### Task 5.2: Build script + EN Quick Start PDF

**Files:**
- Create: `exports/build-apple-intelligence-quickstart-pdf.py`
- Reference: `exports/build-claude-quickstart-pdf.py`

- [ ] **Step 1: Write build script**

```python
#!/usr/bin/env python3
"""Regenerate Apple Intelligence Quick Start (EN + SV) 2-page A4 PDFs."""
from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).parent.parent
jobs = [
    (root / "exports/apple-intelligence-quick-start-en.html",
     root / "assets/pdfs/guides/apple-intelligence-quick-start-en.pdf"),
    (root / "exports/apple-intelligence-quick-start-sv.html",
     root / "assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    for src, dst in jobs:
        if not src.exists():
            print(f"Skipping {dst.name} — source not found")
            continue
        url = src.as_uri()
        print(f"Building {dst.name} from {src.name}")
        page.goto(url, wait_until="networkidle")
        page.emulate_media(media="print")
        dst.parent.mkdir(parents=True, exist_ok=True)
        page.pdf(
            path=str(dst),
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
            prefer_css_page_size=True,
        )
        print(f"  -> {dst.stat().st_size // 1024} KB")
    browser.close()
print("Done.")
```

- [ ] **Step 2: Run**

```bash
python3 exports/build-apple-intelligence-quickstart-pdf.py
```

Expected: EN PDF built (~2 pages, ~400-500 KB). SV skipped.

- [ ] **Step 3: Verify page count is exactly 2**

```bash
python3 -c "
import pypdf
r = pypdf.PdfReader('assets/pdfs/guides/apple-intelligence-quick-start-en.pdf')
print(f'Pages: {len(r.pages)}')
"
```

- [ ] **Step 4: Visual inspect**

```bash
open assets/pdfs/guides/apple-intelligence-quick-start-en.pdf
```

- [ ] **Step 5: Commit**

```bash
git add exports/build-apple-intelligence-quickstart-pdf.py assets/pdfs/guides/apple-intelligence-quick-start-en.pdf
git commit -m "feat: Apple Intelligence EN — Quick Start build script + PDF (2 pages)"
```

---

## Phase 6 — SV Quick Start

### Task 6.1: Create SV Quick Start HTML + build PDF

**Files:**
- Create: `exports/apple-intelligence-quick-start-sv.html`

- [ ] **Step 1: Copy EN as base**

```bash
cp exports/apple-intelligence-quick-start-en.html exports/apple-intelligence-quick-start-sv.html
```

- [ ] **Step 2: Update lang + title**

- `<html lang="en">` → `<html lang="sv">`
- `<title>` → `Apple Intelligence Quick Start — för lärare`

- [ ] **Step 3: Translate content**

- Masthead: `Apple Intelligence Quick Start · för lärare`
- H1: `Sex Apple Intelligence-funktioner som förändrar arbetet i klassrummet`
- Subtitle: `iPad-först, integritetsmedveten, tar 10 minuter att lära sig`
- Feature mini-cards: translate each
- Page 2 heading: `Testa: 5 praktiska uppgifter att prova idag`
- Watch-out label: `● Tänk på · åldersgränser och data`
- Watch-out body: translate
- Closing msg: `Vill du ha djup? Läs hela <em>Apple Intelligence-guiden</em> — eller ladda ner den 25-sidiga premium-PDF:en från samma sida.`
- License line: `<strong>Licensierad under CC BY-NC-SA 4.0</strong> — ange källa, icke-kommersiell, samma licens.` + URL deed.sv

- [ ] **Step 4: Run build script to generate both PDFs**

```bash
python3 exports/build-apple-intelligence-quickstart-pdf.py
```

- [ ] **Step 5: Verify both quick-start PDFs exist and are 2 pages each**

```bash
python3 -c "
import pypdf
for name in ['apple-intelligence-quick-start-en.pdf', 'apple-intelligence-quick-start-sv.pdf']:
    r = pypdf.PdfReader(f'assets/pdfs/guides/{name}')
    print(f'{name}: {len(r.pages)} pages')
"
```

- [ ] **Step 6: Commit**

```bash
git add exports/apple-intelligence-quick-start-sv.html assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf
git commit -m "feat: Apple Intelligence SV — Quick Start HTML + PDF (2 pages)"
```

---

## Phase 7 — Integration

### Task 7.1: Flip guide status to available (EN)

**Files:**
- Modify: `guides/guides-en.json`

- [ ] **Step 1: Open `guides/guides-en.json` and locate the apple-intelligence entry**

It should currently have `"status": "coming-soon"`.

- [ ] **Step 2: Change to `"status": "available"`**

Also verify that the `url` field is correct (`/guides/apple-intelligence/`) and that `cover_image` points to `/assets/images/guide-covers/apple.svg`.

- [ ] **Step 3: Verify JSON is valid**

```bash
python3 -c "import json; json.load(open('guides/guides-en.json'))"
```

Expected: no error.

- [ ] **Step 4: Commit**

```bash
git add guides/guides-en.json
git commit -m "feat: flip Apple Intelligence EN guide to available"
```

---

### Task 7.2: Flip guide status to available (SV)

**Files:**
- Modify: `sv/guider/guides-sv.json`

- [ ] **Step 1: Open + change status**

Same pattern: `"status": "coming-soon"` → `"status": "available"`.

- [ ] **Step 2: Verify JSON**

```bash
python3 -c "import json; json.load(open('sv/guider/guides-sv.json'))"
```

- [ ] **Step 3: Commit**

```bash
git add sv/guider/guides-sv.json
git commit -m "feat: flip Apple Intelligence SV guide to available"
```

---

### Task 7.3: Verify guide index cards render

**Files:** no code changes, verification only

- [ ] **Step 1: Open EN guide index**

```bash
open "http://localhost:8080/guides/"
```

Expected:
- Apple Intelligence card is visible, not grayed-out ("coming soon")
- Cover SVG renders
- Click leads to `/guides/apple-intelligence/`

- [ ] **Step 2: Open SV guide index**

```bash
open "http://localhost:8080/sv/guider/"
```

Same check.

- [ ] **Step 3: Fix any card styling issues**

If the Apple card looks broken relative to Claude/Gemini cards, inspect the cover SVG for fit issues. Commit fixes as `fix: Apple Intelligence card — <issue>`.

---

### Task 7.4: End-to-end download flow test

**Files:** no code changes, verification only

- [ ] **Step 1: EN path**

1. Open `http://localhost:8080/guides/apple-intelligence/`
2. Scroll to CTA band
3. Click "Download the Guide (PDF)" → expect MailerLite gate modal
4. Enter test email → expect modal transitions to "Check your inbox" with direct download link
5. Click download link → expect PDF downloads
6. Open PDF → verify it is the latest version with license page

- [ ] **Step 2: EN Quick Start (no gate)**

1. Click "Download the Quick Start" → PDF downloads directly (no modal)
2. Open PDF → verify 2 pages, license line on page 2

- [ ] **Step 3: SV path**

Repeat both tests on `http://localhost:8080/sv/guider/apple-intelligence/`.

- [ ] **Step 4: No commit unless fixes needed**

---

### Task 7.5: Final multi-viewport check

**Files:** no code changes, verification only

- [ ] **Step 1: Test matrix**

For each of: EN web, SV web

Test viewports: 1440×900 (desktop), 1024×1366 (iPad portrait), 390×844 (iPhone 14)

Check each viewport for:
- Hero readable, no overflow
- Anchor nav usable (appears on scroll, no broken wrap)
- Part 2 feature cards legible
- Processing callouts contain content properly
- Warning box in Part 3 visible
- Policy list numbers align
- CTA band buttons stack on narrow viewports
- License band + footer readable

- [ ] **Step 2: Document any issues in a FIX list**

For each issue found, write a one-line todo. Fix and commit as separate commits with `fix: Apple Intelligence — <specific issue>`.

- [ ] **Step 3: Push to remote**

Once all issues are fixed:

```bash
git push origin main
```

---

## Self-Review (to be done before handoff)

**Spec coverage check:**
- Section 4 (Features) — Task 1.4 + 2.4 cover all 6 ✓
- Section 5 (IA) — Tasks 1.3/1.4/1.5 cover 3 parts ✓
- Section 6 (Deliverables) — 4 PDFs + 2 web + 1 SVG covered ✓
- Section 7 (Design system) — Task 1.8 implements graphite accent ✓
- Section 8 (Sources) — referenced in Task 1.3 (PCC explainer) ✓
- Section 9 (Global content rules) — referenced in Task 2.3 (age gates) ✓
- Section 10 (Alignment record) — captured ✓
- Section 13 (Implementation order) — matches Phase 1-7 ✓

**Known gaps / follow-ups (not blocking initial ship):**
- Real photos for hero/part openers — currently typographic only. Can be added as a follow-up task with Nano Banana generation.
- Apple Intelligence EU feature matrix changes monthly — add reminder to `project_upcoming_tasks.md` to re-verify every quarter.
