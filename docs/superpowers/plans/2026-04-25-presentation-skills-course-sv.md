# Presentationsteknik — SV-kurs implementation plan (Steg 1)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Launch the complete Swedish-language interactive presentation-skills course at `https://choosewise.education/sv/presentationsteknik/` — 7 modules, 5 deep-dives, working state-persistence, fully responsive, integrated with the existing site chrome.

**Architecture:** Static HTML/CSS/JS matching the rest of choosewise.education. New CSS components added to existing `assets/css/components.css`. New JS modules in `assets/js/` for course state and exercises. Module pages share a single template that varies only in content. Slide images from Johan's Keynote (selected ~25–40) are placed under `assets/images/presentation-skills/slides/`. State persists in `localStorage` per language; no server, no accounts.

**Tech Stack:** HTML5, CSS3 (existing tokens.css/base.css/components.css/pages.css), vanilla JavaScript (ES modules), Web Audio API (module 6 recording exercise), `python3 -m http.server` for preview, browser DevTools + Playwright MCP for visual verification.

**Out of scope (will get separate plans later):**
- Steg 2: SV-PDF (built after course is complete)
- Steg 3: EN-kurs (translation + localization)
- Steg 4: EN-PDF

---

## Plan structure

This plan has 11 parts. Parts 1–3 build the foundation and the canonical module. Parts 4–9 build modules 2–7 + their deep-dives following the canonical module's template. Parts 10–11 handle slide assets and final integration.

**Spec reference:** `docs/superpowers/specs/2026-04-25-presentation-skills-course-design.md`

---

## File structure that this plan creates

```
sv/presentationsteknik/
├── index.html                                # Översiktsvy (replaces placeholder)
├── modul-1/index.html                        # Varför presentationsteknik?
├── modul-2/
│   ├── index.html                            # Designa diabilder — grunderna
│   └── fordjupning/index.html                # Färgteori + typografi djup
├── modul-3/
│   ├── index.html                            # När diabilden krockar med dig
│   └── fordjupning/index.html                # 12 makeover-exempel
├── modul-4/
│   ├── index.html                            # Framförandet — närvaro i rummet
│   └── fordjupning/index.html                # Närvaro + scenrutiner
├── modul-5/
│   ├── index.html                            # Digitala presentationer
│   └── fordjupning/index.html                # Kamera + plattformar
├── modul-6/
│   ├── index.html                            # Röst, kropp och språk
│   └── fordjupning/index.html                # 19 vanliga svaga punkter
└── modul-7/index.html                        # Din checklista

assets/css/
├── components.css                            # MODIFIED: add course-progress, module-card,
│                                              # exercise, deepdive-cta, module-topbar,
│                                              # module-nav components
└── pages.css                                 # MODIFIED: add module-page, module-hero,
                                                # module-section, course-overview rules

assets/js/
├── course-progress.js                        # NEW: state mgmt + topbar updates
├── course-exercises.js                       # NEW: textarea reflection persistence
└── course-recording.js                       # NEW: Web Audio API for modul 6 övning

assets/images/presentation-skills/slides/
└── (Johan exports slide PNGs without Advania branding here)

scripts/
└── test-course.html                          # NEW: in-browser smoke tests for JS

sitemap.xml                                   # MODIFIED: add 12 new SV URLs
sv/index.html                                 # MODIFIED: add Presentationsteknik section
```

---

## Verification pattern

This codebase has no test framework. We "test" using:

1. **For HTML/CSS changes:** Spin up `python3 -m http.server 8765` from the site root, navigate to the page, check visually + via DevTools + Playwright screenshots at three widths (mobile 375px, tablet 768px, laptop 1440px).
2. **For JS modules:** A standalone `scripts/test-course.html` page exercises the JS in the browser. Each test calls a function and uses `console.assert()` + visible green/red status indicators on the page. Open in browser, see green checkmarks.
3. **For end-to-end:** Walk through the full course as a user — start at översiktsvy, complete modul 1 övning, click forward, refresh, verify state persists, etc.

After each task: visual verification + commit. Memory pattern: spin up preview, show Johan, wait for "kör" before commit.

---

# PART 1 — Foundation: directory structure + CSS components + JS modules

## Task 1: Create directory structure for the SV course

**Files:**
- Create: `sv/presentationsteknik/modul-1/`
- Create: `sv/presentationsteknik/modul-2/`, `sv/presentationsteknik/modul-2/fordjupning/`
- Create: `sv/presentationsteknik/modul-3/`, `sv/presentationsteknik/modul-3/fordjupning/`
- Create: `sv/presentationsteknik/modul-4/`, `sv/presentationsteknik/modul-4/fordjupning/`
- Create: `sv/presentationsteknik/modul-5/`, `sv/presentationsteknik/modul-5/fordjupning/`
- Create: `sv/presentationsteknik/modul-6/`, `sv/presentationsteknik/modul-6/fordjupning/`
- Create: `sv/presentationsteknik/modul-7/`
- Create: `assets/images/presentation-skills/slides/`

- [ ] **Step 1: Create all directories**

```bash
cd "Ny JLSU hemsida"
mkdir -p sv/presentationsteknik/modul-{1,7}
mkdir -p sv/presentationsteknik/modul-{2,3,4,5,6}/fordjupning
mkdir -p assets/images/presentation-skills/slides
```

- [ ] **Step 2: Verify**

```bash
find sv/presentationsteknik -type d | sort
```

Expected output: 13 directory paths printed (root + 7 module dirs + 5 fördjupning dirs).

- [ ] **Step 3: Commit**

```bash
git add sv/presentationsteknik/ assets/images/presentation-skills/
git commit -m "chore(presentationsteknik): scaffold directory structure for SV course"
```

---

## Task 2: Add `.module-topbar` + `.course-progress` CSS components

**Files:**
- Modify: `assets/css/components.css` (append to end)

The sticky topbar appears on all module + fördjupning pages. The bigger numbered stege (28px) appears on the översiktsvy. Both share the same color tokens but differ in size.

- [ ] **Step 1: Append the components to `components.css`**

Open `assets/css/components.css` and append:

```css

/* ───── Course progress (überpresentationsteknik) ─────
   Två varianter:
   1. .course-progress: stor numrerad stege på översiktsvyn (28px).
   2. .module-topbar:   sticky bar på modul + fördjupningssidor (24px).

   Färgkodning:
   - default (ej startad)            : grå border, --color-text-soft text
   - --done                          : forest green bakgrund + dark text
   - --current (aria-current="page") : terracotta + soft glow */

/* === Sticky topbar (på modul + fördjupningssidor) === */
.module-topbar {
  position: sticky;
  top: var(--nav-height, 60px);
  z-index: 10;
  background: var(--color-bg-blur);
  backdrop-filter: saturate(150%) blur(16px);
  -webkit-backdrop-filter: saturate(150%) blur(16px);
  border-bottom: 1px solid var(--color-border);
  padding: var(--space-3) 0;
}
.module-topbar__inner {
  max-width: var(--content-max);
  margin-inline: auto;
  padding-inline: var(--space-5);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  font-size: 0.875rem;
}
.module-topbar__crumb { color: var(--color-text-soft); }
.module-topbar__crumb a {
  color: var(--color-accent);
  text-decoration: none;
}
.module-topbar__crumb a:hover { text-decoration: underline; }

.module-topbar__progress {
  display: flex;
  align-items: center;
  gap: 0;
}

/* === Stora steget (översiktsvy) === */
.course-progress {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-4) 0;
  flex-wrap: wrap;
  justify-content: center;
}
.course-progress__step {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

/* === Gemensamma cirklar (storleksvarianter) === */
.course-progress__dot,
.module-topbar__progress-dot {
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-family: var(--font-display);
  font-weight: 500;
  border: 1.5px solid var(--color-border);
  color: var(--color-text-soft);
  background: var(--color-bg);
  text-decoration: none;
  transition: transform var(--dur-fast) var(--ease-out),
              border-color var(--dur-fast) var(--ease-out);
  flex-shrink: 0;
}
.course-progress__dot {           /* stor — översikt */
  width: 28px; height: 28px;
  font-size: 0.85rem;
}
.module-topbar__progress-dot {    /* mindre — sticky topbar */
  width: 24px; height: 24px;
  font-size: 0.75rem;
}

/* Hover-state (klickbara) */
.course-progress__dot:hover,
.module-topbar__progress-dot:hover {
  transform: scale(1.1);
  border-color: var(--color-accent);
}

/* "Klar"-state */
.course-progress__dot--done,
.module-topbar__progress-dot--done {
  background: var(--color-accent);
  border-color: var(--color-accent);
  color: var(--color-dark-text);
}

/* "Du är här"-state */
.course-progress__dot--current,
.module-topbar__progress-dot--current {
  background: var(--color-highlight);
  border-color: var(--color-highlight);
  color: var(--color-dark-text);
}
.course-progress__dot--current { box-shadow: 0 0 0 4px rgba(198, 107, 61, 0.15); }
.module-topbar__progress-dot--current { box-shadow: 0 0 0 3px rgba(198, 107, 61, 0.15); }

/* Linjer mellan cirklarna */
.course-progress__line {
  width: 28px; height: 1.5px;
  background: var(--color-border);
}
.module-topbar__progress-line {
  width: 18px; height: 1.5px;
  background: var(--color-border);
  flex-shrink: 0;
}
.course-progress__line--done,
.module-topbar__progress-line--done {
  background: var(--color-accent);
}

/* Mobil-anpassning av sticky topbar */
@media (max-width: 720px) {
  .module-topbar__progress-line { display: none; }
  .module-topbar__progress { gap: 4px; }
  .module-topbar__progress-dot {
    width: 22px; height: 22px;
    font-size: 0.7rem;
  }
}

/* Reduced motion: stäng av glow-puls om den läggs till senare */
@media (prefers-reduced-motion: reduce) {
  .course-progress__dot--current,
  .module-topbar__progress-dot--current { animation: none !important; }
}
```

- [ ] **Step 2: Verify CSS validates**

```bash
cd "Ny JLSU hemsida"
npx --yes csstree-validator assets/css/components.css 2>&1 | tail -5
```

Expected: no errors (or only warnings unrelated to new code).

- [ ] **Step 3: Commit**

```bash
git add assets/css/components.css
git commit -m "feat(css): add course-progress + module-topbar components for presentationsteknik"
```

---

## Task 3: Add `.module-card` + `.module-grid` components

**Files:**
- Modify: `assets/css/components.css` (append)

- [ ] **Step 1: Append to components.css**

```css

/* ───── Course module cards (översiktsvy grid) ───── */
.module-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--space-5);
  margin-top: var(--space-6);
}

.module-card {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  padding: var(--space-5);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md, 8px);
  background: var(--color-bg);
  text-decoration: none;
  color: inherit;
  transition: transform var(--dur-fast) var(--ease-out),
              box-shadow var(--dur-fast) var(--ease-out),
              border-color var(--dur-fast) var(--ease-out);
}
.module-card:hover {
  transform: translateY(-2px);
  border-color: var(--color-accent);
  box-shadow: var(--shadow-md);
}
.module-card--current {
  border-color: var(--color-highlight);
  box-shadow: 0 0 0 1px var(--color-highlight);
}
.module-card--done { background: var(--color-bg-alt); }

.module-card__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
}
.module-card__num {
  font-family: var(--font-display);
  font-size: 2.25rem;
  font-weight: 400;
  color: var(--color-text-soft);
  line-height: 1;
}
.module-card--done .module-card__num,
.module-card--current .module-card__num { color: var(--color-accent); }

.module-card__status {
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--color-text-soft);
}
.module-card__status--done    { color: var(--color-accent); }
.module-card__status--current { color: var(--color-highlight); }

.module-card__title {
  font-family: var(--font-display);
  font-size: 1.35rem;
  font-weight: 500;
  line-height: 1.25;
  margin: 0;
}
.module-card__desc {
  font-size: 0.95rem;
  color: var(--color-text-soft);
  line-height: 1.5;
  margin: 0;
}

.module-card__meta {
  display: flex;
  gap: var(--space-4);
  align-items: center;
  margin-top: auto;
  padding-top: var(--space-3);
  font-size: 0.85rem;
  color: var(--color-text-soft);
  border-top: 1px solid var(--color-border);
}
.module-card__meta-item {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}
.module-card__deepdive-tag {
  color: var(--color-highlight);
  font-weight: 500;
}
```

- [ ] **Step 2: Commit**

```bash
git add assets/css/components.css
git commit -m "feat(css): add module-card grid for presentationsteknik overview"
```

---

## Task 4: Add `.exercise` + `.deepdive-cta` + `.module-nav` + `.module-figure` components

**Files:**
- Modify: `assets/css/components.css` (append)

- [ ] **Step 1: Append to components.css**

```css

/* ───── Course exercise block (interaktiv övning på modulsidor) ───── */
.exercise {
  background: var(--color-bg-alt);
  border-left: 3px solid var(--color-accent);
  padding: var(--space-5);
  border-radius: 0 var(--radius-md, 8px) var(--radius-md, 8px) 0;
  margin-block: var(--space-5);
}
.exercise__label {
  font-size: 0.75rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-accent);
  font-weight: 600;
  margin-bottom: var(--space-2);
}
.exercise__prompt {
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 500;
  margin-bottom: var(--space-4);
}
.exercise__textarea {
  width: 100%;
  min-height: 100px;
  padding: var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font: inherit;
  resize: vertical;
  background: var(--color-bg);
}
.exercise__hint {
  font-size: 0.85rem;
  color: var(--color-text-soft);
  margin-top: var(--space-2);
}
.exercise__btn { margin-top: var(--space-3); }
.exercise__feedback {
  margin-top: var(--space-3);
  font-size: 0.875rem;
  color: var(--color-accent);
  font-style: italic;
  min-height: 1.2em;
}

/* ───── Deep-dive CTA (länkblock i slutet av modulen) ───── */
.deepdive-cta {
  margin-block: var(--space-7);
  padding: var(--space-6);
  border: 1px solid var(--color-highlight);
  border-radius: var(--radius-md, 8px);
  background: linear-gradient(135deg,
    rgba(198, 107, 61, 0.05) 0%,
    rgba(198, 107, 61, 0.10) 100%);
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: var(--space-5);
  align-items: center;
  text-decoration: none;
  color: inherit;
  transition: transform var(--dur-fast) var(--ease-out);
}
.deepdive-cta:hover { transform: translateY(-1px); }
.deepdive-cta__icon {
  font-size: 2rem;
  color: var(--color-highlight);
}
.deepdive-cta__title {
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 500;
  margin: 0 0 var(--space-2) 0;
  color: var(--color-text);
}
.deepdive-cta__desc {
  color: var(--color-text-soft);
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0;
}
.deepdive-cta__arrow {
  color: var(--color-highlight);
  font-weight: 500;
}
@media (max-width: 720px) {
  .deepdive-cta {
    grid-template-columns: 1fr;
    text-align: left;
  }
  .deepdive-cta__icon { font-size: 1.5rem; }
}

/* ───── Module prev/next navigation (slut på modulsidan) ───── */
.module-nav {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
  padding-block: var(--space-7);
  margin-top: var(--space-6);
  border-top: 1px solid var(--color-border);
}
.module-nav__link {
  padding: var(--space-4);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md, 8px);
  text-decoration: none;
  color: inherit;
  transition: border-color var(--dur-fast) var(--ease-out);
}
.module-nav__link:hover { border-color: var(--color-accent); }
.module-nav__direction {
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--color-text-soft);
  margin-bottom: var(--space-2);
}
.module-nav__title {
  font-family: var(--font-display);
  font-size: 1.05rem;
  font-weight: 500;
}
.module-nav__link--next { text-align: right; }
@media (max-width: 720px) {
  .module-nav { grid-template-columns: 1fr; }
}

/* ───── Module figure (slide-bilder + caption i innehåll) ───── */
.module-figure {
  margin-block: var(--space-5);
  border-radius: var(--radius-md, 8px);
  overflow: hidden;
  box-shadow: var(--shadow-md);
}
.module-figure img {
  width: 100%;
  height: auto;
  display: block;
}
.module-figure figcaption {
  padding: var(--space-3) var(--space-4);
  background: var(--color-bg-alt);
  font-size: 0.875rem;
  color: var(--color-text-soft);
}
```

- [ ] **Step 2: Commit**

```bash
git add assets/css/components.css
git commit -m "feat(css): add exercise, deepdive-cta, module-nav, module-figure components"
```

---

## Task 5: Add `.module-page` + `.module-hero` + `.module-section` page layout

**Files:**
- Modify: `assets/css/pages.css` (append)

- [ ] **Step 1: Append to pages.css**

```css

/* ───── Presentationsteknik / Presentation Skills course pages ───── */

/* === Modulsida-layout (modul + fördjupning) === */
.module-page {
  max-width: 760px;
  margin-inline: auto;
  padding-inline: var(--space-5);
}

.module-hero { padding-block: var(--space-7) var(--space-5); }
.module-hero__eyebrow {
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  color: var(--color-text-soft);
  text-transform: uppercase;
  margin-bottom: var(--space-3);
}
.module-hero__eyebrow strong {
  color: var(--color-accent);
  font-weight: 500;
}
.module-hero h1 { margin-bottom: var(--space-4); }
.module-hero__lede {
  font-size: 1.2rem;
  color: var(--color-text-soft);
  line-height: 1.55;
  max-width: 60ch;
}

.module-section {
  padding-block: var(--space-6);
  border-top: 1px solid var(--color-border);
}
.module-section h2 {
  font-size: 1.5rem;
  margin-bottom: var(--space-4);
}
.module-section p {
  max-width: 60ch;
  line-height: 1.65;
}
.module-section p + p { margin-top: var(--space-4); }
```

- [ ] **Step 2: Commit**

```bash
git add assets/css/pages.css
git commit -m "feat(css): add module-page layout for presentationsteknik"
```

---

## Task 6: Implement `course-progress.js` (state management)

**Files:**
- Create: `assets/js/course-progress.js`

This module manages the per-language progress state (which modules are done / current / not-started) in `localStorage` and exposes helpers that page templates can call to render the correct state.

- [ ] **Step 1: Create the file**

```js
// course-progress.js
// Manages course progression state (presentationsteknik).
//
// localStorage keys (one set per language):
//   presentationsteknik-sv-progress       → JSON array of 7 statuses
//                                           ("done" | "current" | "not-started")
//   presentationsteknik-sv-mod{N}-{slug}  → individual exercise answers
//                                           (handled by course-exercises.js)
//
// API:
//   CourseProgress.init(lang)
//   CourseProgress.getStatus(modIndex)         → "done"|"current"|"not-started"
//   CourseProgress.setCurrent(modIndex)        → marks others "done" up to N-1
//   CourseProgress.markDone(modIndex)
//   CourseProgress.reset()
//   CourseProgress.renderTopbar(containerEl, currentMod)
//   CourseProgress.renderOverview(containerEl, currentMod)

(function (global) {
  const TOTAL_MODULES = 7;
  let LANG = 'sv';
  let STORAGE_KEY = 'presentationsteknik-sv-progress';

  const MODULE_TITLES = {
    sv: [
      'Varför presentationsteknik?',
      'Designa diabilder — grunderna',
      'När diabilden krockar med dig',
      'Framförandet — närvaro i rummet',
      'Digitala presentationer',
      'Röst, kropp och språk',
      'Din checklista',
    ],
  };

  const MODULE_URLS = {
    sv: [
      '/sv/presentationsteknik/modul-1/',
      '/sv/presentationsteknik/modul-2/',
      '/sv/presentationsteknik/modul-3/',
      '/sv/presentationsteknik/modul-4/',
      '/sv/presentationsteknik/modul-5/',
      '/sv/presentationsteknik/modul-6/',
      '/sv/presentationsteknik/modul-7/',
    ],
  };

  function defaultProgress() {
    return Array(TOTAL_MODULES).fill('not-started');
  }

  function load() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return defaultProgress();
      const parsed = JSON.parse(raw);
      if (!Array.isArray(parsed) || parsed.length !== TOTAL_MODULES) {
        return defaultProgress();
      }
      return parsed;
    } catch {
      return defaultProgress();
    }
  }

  function save(state) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch { /* localStorage might be disabled — silently no-op */ }
  }

  const CourseProgress = {
    init(lang) {
      LANG = lang || 'sv';
      STORAGE_KEY = `presentationsteknik-${LANG}-progress`;
    },

    getState() { return load(); },

    getStatus(modIndex) {
      const state = load();
      return state[modIndex - 1] || 'not-started';
    },

    setCurrent(modIndex) {
      const state = defaultProgress();
      for (let i = 0; i < modIndex - 1; i++) state[i] = 'done';
      state[modIndex - 1] = 'current';
      save(state);
    },

    markDone(modIndex) {
      const state = load();
      state[modIndex - 1] = 'done';
      save(state);
    },

    reset() {
      try { localStorage.removeItem(STORAGE_KEY); } catch { }
    },

    /* Renders inside an element with class "module-topbar__progress".
       currentMod = which module is "you are here" on this page. */
    renderTopbar(containerEl, currentMod) {
      const state = load();
      // mark currentMod as current in storage if not already
      if (state[currentMod - 1] !== 'done') {
        state[currentMod - 1] = 'current';
        save(state);
      }
      const titles = MODULE_TITLES[LANG];
      const urls = MODULE_URLS[LANG];
      containerEl.innerHTML = '';
      for (let i = 0; i < TOTAL_MODULES; i++) {
        const mod = i + 1;
        const status = (mod === currentMod) ? 'current' : state[i];
        const dot = document.createElement('a');
        dot.className = 'module-topbar__progress-dot';
        if (status === 'done') dot.classList.add('module-topbar__progress-dot--done');
        if (status === 'current') {
          dot.classList.add('module-topbar__progress-dot--current');
          dot.setAttribute('aria-current', 'page');
        }
        dot.href = urls[i];
        dot.title = `Modul ${mod} — ${titles[i]}`;
        dot.textContent = mod;
        containerEl.appendChild(dot);

        if (i < TOTAL_MODULES - 1) {
          const line = document.createElement('span');
          line.className = 'module-topbar__progress-line';
          if (status === 'done') line.classList.add('module-topbar__progress-line--done');
          containerEl.appendChild(line);
        }
      }
    },

    /* Renders the bigger 28px progressionsstege on översiktsvyn.
       containerEl has class "course-progress". */
    renderOverview(containerEl, currentMod) {
      const state = load();
      const titles = MODULE_TITLES[LANG];
      const urls = MODULE_URLS[LANG];
      containerEl.innerHTML = '';
      for (let i = 0; i < TOTAL_MODULES; i++) {
        const mod = i + 1;
        const status = state[i];

        const step = document.createElement('div');
        step.className = 'course-progress__step';

        const dot = document.createElement('a');
        dot.className = 'course-progress__dot';
        if (status === 'done') dot.classList.add('course-progress__dot--done');
        if (status === 'current') dot.classList.add('course-progress__dot--current');
        dot.href = urls[i];
        dot.title = `Modul ${mod} — ${titles[i]}`;
        dot.textContent = mod;
        step.appendChild(dot);
        containerEl.appendChild(step);

        if (i < TOTAL_MODULES - 1) {
          const line = document.createElement('span');
          line.className = 'course-progress__line';
          if (status === 'done') line.classList.add('course-progress__line--done');
          containerEl.appendChild(line);
        }
      }
    },
  };

  global.CourseProgress = CourseProgress;
})(window);
```

- [ ] **Step 2: Commit**

```bash
git add assets/js/course-progress.js
git commit -m "feat(js): add course-progress module for presentationsteknik state"
```

---

## Task 7: Implement `course-exercises.js` (textarea reflection persistence)

**Files:**
- Create: `assets/js/course-exercises.js`

Wires up any `<form data-exercise="key">` element on a page so that the textarea inside it auto-saves to `localStorage` and loads on page-load.

- [ ] **Step 1: Create the file**

```js
// course-exercises.js
// Auto-saves any <form data-exercise="<key>"> textarea answer to localStorage.
//
// Markup expected:
//   <form data-exercise="modul-1-varfor" class="exercise__form">
//     <textarea class="exercise__textarea" name="answer" required></textarea>
//     <button type="submit" class="btn btn--primary">Spara</button>
//     <p class="exercise__feedback" aria-live="polite"></p>
//   </form>
//
// Behavior:
//   - On load: textarea pre-filled if a saved value exists in localStorage.
//   - On submit: persist value, show "Sparat ✓" in __feedback for 4s.
//   - storage key: `presentationsteknik-${lang}-exercise-${key}`
//                  (lang detected from <html lang> attribute)

(function (global) {
  function getLang() {
    return (document.documentElement.lang || 'sv').slice(0, 2);
  }

  function storageKeyFor(exerciseKey) {
    return `presentationsteknik-${getLang()}-exercise-${exerciseKey}`;
  }

  function init() {
    const forms = document.querySelectorAll('form[data-exercise]');
    forms.forEach((form) => {
      const key = form.dataset.exercise;
      const textarea = form.querySelector('textarea');
      const feedback = form.querySelector('.exercise__feedback');
      if (!textarea) return;

      // Load existing answer
      try {
        const saved = localStorage.getItem(storageKeyFor(key));
        if (saved) textarea.value = saved;
      } catch { /* localStorage disabled */ }

      form.addEventListener('submit', (e) => {
        e.preventDefault();
        try {
          localStorage.setItem(storageKeyFor(key), textarea.value);
          if (feedback) {
            feedback.textContent = 'Sparat ✓';
            setTimeout(() => { feedback.textContent = ''; }, 4000);
          }
        } catch {
          if (feedback) feedback.textContent = 'Kunde inte spara (localStorage avstängd)';
        }
      });
    });
  }

  // Auto-init when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  global.CourseExercises = { init };
})(window);
```

- [ ] **Step 2: Commit**

```bash
git add assets/js/course-exercises.js
git commit -m "feat(js): add course-exercises module for textarea reflection persistence"
```

---

## Task 8: Add `scripts/test-course.html` smoke tests

**Files:**
- Create: `scripts/test-course.html`

Standalone test page for the two JS modules. Open in browser, see green checkmarks for all tests.

- [ ] **Step 1: Create the test page**

```html
<!DOCTYPE html>
<html lang="sv">
<head>
  <meta charset="UTF-8">
  <title>Course JS — smoke tests</title>
  <style>
    body { font-family: -apple-system, sans-serif; padding: 2rem; max-width: 700px; margin: auto; }
    .test { padding: 0.5rem; border-bottom: 1px solid #eee; }
    .pass { color: green; } .fail { color: red; font-weight: 600; }
    h1 { font-size: 1.4rem; }
    button { padding: 0.5rem 1rem; margin-top: 1rem; }
  </style>
</head>
<body>
  <h1>Course JS — smoke tests</h1>
  <p>Detta exekverar både <code>course-progress.js</code> och <code>course-exercises.js</code>.</p>
  <div id="results"></div>
  <button onclick="localStorage.clear(); location.reload();">Reset all storage + rerun</button>

  <!-- Hidden test fixtures -->
  <div id="topbar-container" class="module-topbar__progress" style="display:none"></div>
  <div id="overview-container" class="course-progress" style="display:none"></div>
  <form data-exercise="test-key" style="display:none">
    <textarea>initial</textarea>
    <button type="submit">save</button>
    <p class="exercise__feedback"></p>
  </form>

  <script src="../assets/js/course-progress.js"></script>
  <script src="../assets/js/course-exercises.js"></script>
  <script>
    const results = document.getElementById('results');
    function test(name, fn) {
      const div = document.createElement('div');
      div.className = 'test';
      try {
        fn();
        div.innerHTML = `<span class="pass">✓</span> ${name}`;
      } catch (e) {
        div.innerHTML = `<span class="fail">✗</span> ${name}<br><small>${e.message}</small>`;
      }
      results.appendChild(div);
    }
    function assert(cond, msg) { if (!cond) throw new Error(msg || 'assertion failed'); }

    // === CourseProgress tests ===
    localStorage.clear();
    CourseProgress.init('sv');

    test('default state is 7 × not-started', () => {
      const state = CourseProgress.getState();
      assert(state.length === 7, 'length 7');
      assert(state.every(s => s === 'not-started'), 'all not-started');
    });

    test('setCurrent(3) → modules 1,2 done; 3 current; 4-7 not-started', () => {
      CourseProgress.setCurrent(3);
      const s = CourseProgress.getState();
      assert(s[0] === 'done' && s[1] === 'done', 'first two done');
      assert(s[2] === 'current', 'third current');
      assert(s.slice(3).every(x => x === 'not-started'), '4-7 not-started');
    });

    test('markDone(3) → module 3 becomes done', () => {
      CourseProgress.markDone(3);
      assert(CourseProgress.getStatus(3) === 'done');
    });

    test('reset() clears progress', () => {
      CourseProgress.reset();
      assert(CourseProgress.getState().every(s => s === 'not-started'));
    });

    test('renderTopbar produces 7 dots + 6 lines', () => {
      const container = document.getElementById('topbar-container');
      CourseProgress.setCurrent(2);
      CourseProgress.renderTopbar(container, 2);
      const dots = container.querySelectorAll('.module-topbar__progress-dot');
      const lines = container.querySelectorAll('.module-topbar__progress-line');
      assert(dots.length === 7, `expected 7 dots, got ${dots.length}`);
      assert(lines.length === 6, `expected 6 lines, got ${lines.length}`);
      assert(dots[1].classList.contains('module-topbar__progress-dot--current'),
        'modul 2 dot has current class');
      assert(dots[1].getAttribute('aria-current') === 'page', 'modul 2 has aria-current');
    });

    test('renderOverview produces 7 dots + 6 lines', () => {
      const container = document.getElementById('overview-container');
      CourseProgress.renderOverview(container, 2);
      assert(container.querySelectorAll('.course-progress__dot').length === 7);
      assert(container.querySelectorAll('.course-progress__line').length === 6);
    });

    // === CourseExercises tests ===
    test('exercise form pre-loads stored answer', () => {
      localStorage.setItem('presentationsteknik-sv-exercise-test-key', 'preloaded');
      // Re-init to trigger load
      CourseExercises.init();
      const ta = document.querySelector('form[data-exercise="test-key"] textarea');
      assert(ta.value === 'preloaded', `expected 'preloaded', got '${ta.value}'`);
    });

    test('exercise form persists on submit', () => {
      const form = document.querySelector('form[data-exercise="test-key"]');
      const ta = form.querySelector('textarea');
      ta.value = 'newvalue';
      form.dispatchEvent(new Event('submit'));
      const stored = localStorage.getItem('presentationsteknik-sv-exercise-test-key');
      assert(stored === 'newvalue', `expected 'newvalue', got '${stored}'`);
    });

    localStorage.clear();
  </script>
</body>
</html>
```

- [ ] **Step 2: Run the tests**

```bash
cd "Ny JLSU hemsida"
python3 -m http.server 8765 > /tmp/preview.log 2>&1 &
open http://localhost:8765/scripts/test-course.html
```

Expected: page loads with 8 green checkmarks (✓), no red ✗.

- [ ] **Step 3: Stop preview server**

```bash
lsof -ti:8765 | xargs kill -9 2>/dev/null
```

- [ ] **Step 4: Commit**

```bash
git add scripts/test-course.html
git commit -m "test(presentationsteknik): add course JS smoke tests"
```

---

# PART 2 — Översiktsvy (production)

## Task 9: Replace placeholder with the real översiktsvy

**Files:**
- Modify: `sv/presentationsteknik/index.html` (currently a placeholder; full rewrite)

This is the grid landing page. It includes the big 28px progress stege at top + 7 module cards. State (which is current, which are done) is read from `localStorage` and rendered by `course-progress.js`.

- [ ] **Step 1: Replace `sv/presentationsteknik/index.html` with full content**

```html
<!DOCTYPE html>
<html lang="sv">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Presentationsteknik — choosewise.education</title>
  <meta name="description" content="En interaktiv kurs i presentationsteknik för lärare, skolledare och alla som håller presentationer. Sju moduler, fritt nedladdningsbar sammanfattning.">
  <meta property="og:title" content="Presentationsteknik — choosewise.education">
  <meta property="og:description" content="En interaktiv kurs i presentationsteknik för lärare, skolledare och alla som håller presentationer.">
  <meta property="og:image" content="/assets/images/brand/og-default.svg">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://choosewise.education/sv/presentationsteknik/">
  <link rel="stylesheet" href="/assets/css/fonts.css">
  <link rel="stylesheet" href="/assets/css/tokens.css">
  <link rel="stylesheet" href="/assets/css/base.css">
  <link rel="stylesheet" href="/assets/css/components.css">
  <link rel="stylesheet" href="/assets/css/pages.css">
</head>
<body>
  <div data-include="/assets/partials/header-sv.html"></div>

  <main>
    <!-- Sidans hero: eyebrow + h1 + lede, samma mönster som RÄTT-modellen,
         AI-Guider, etc. -->
    <section class="page-hero container">
      <span class="eyebrow" data-reveal>Presentationsteknik</span>
      <h1 data-reveal>Sju moduler som flyttar din presentationsteknik framåt.</h1>
      <p class="lede" data-reveal>Från varför, via diabilder och framförande, till röst och kropp. Gå hela kursen i ordning, eller hoppa direkt in i den del du behöver. Allt sparas lokalt i din webbläsare — inga konton, ingen e-post, inga spår.</p>
    </section>

    <!-- Stora progress-stegen — fylls i av course-progress.js -->
    <section class="container" style="padding-top: var(--space-4); padding-bottom: var(--space-4);">
      <nav class="course-progress" id="course-overview-progress" aria-label="Kursprogression"></nav>
    </section>

    <!-- Modulkort i grid -->
    <section class="container section">
      <div class="module-grid">

        <a class="module-card" data-mod="1" href="/sv/presentationsteknik/modul-1/">
          <div class="module-card__head">
            <span class="module-card__num">01</span>
            <span class="module-card__status" data-status></span>
          </div>
          <h2 class="module-card__title">Varför presentationsteknik?</h2>
          <p class="module-card__desc">Sineks Golden Circle, ditt varför, logik vs känslor — fundamentet som allt annat vilar på.</p>
          <div class="module-card__meta">
            <span class="module-card__meta-item">⏱ 5 min</span>
          </div>
        </a>

        <a class="module-card" data-mod="2" href="/sv/presentationsteknik/modul-2/">
          <div class="module-card__head">
            <span class="module-card__num">02</span>
            <span class="module-card__status" data-status></span>
          </div>
          <h2 class="module-card__title">Designa diabilder — grunderna</h2>
          <p class="module-card__desc">Ett budskap per slide, max 6 objekt, färg, typografi, blickstyrning. Reglerna som gör all skillnad.</p>
          <div class="module-card__meta">
            <span class="module-card__meta-item">⏱ 10 min</span>
            <span class="module-card__meta-item module-card__deepdive-tag">+ Fördjupning</span>
          </div>
        </a>

        <a class="module-card" data-mod="3" href="/sv/presentationsteknik/modul-3/">
          <div class="module-card__head">
            <span class="module-card__num">03</span>
            <span class="module-card__status" data-status></span>
          </div>
          <h2 class="module-card__title">När diabilden krockar med dig</h2>
          <p class="module-card__desc">Texttunga slides, punktlistor, tabeller, mallar, animeringar — och vad du gör istället.</p>
          <div class="module-card__meta">
            <span class="module-card__meta-item">⏱ 8 min</span>
            <span class="module-card__meta-item module-card__deepdive-tag">+ Fördjupning</span>
          </div>
        </a>

        <a class="module-card" data-mod="4" href="/sv/presentationsteknik/modul-4/">
          <div class="module-card__head">
            <span class="module-card__num">04</span>
            <span class="module-card__status" data-status></span>
          </div>
          <h2 class="module-card__title">Framförandet — närvaro i rummet</h2>
          <p class="module-card__desc">Blicken, pausen, utfyllnadsljud, props, berättelser. Hur du blir personen i rummet.</p>
          <div class="module-card__meta">
            <span class="module-card__meta-item">⏱ 10 min</span>
            <span class="module-card__meta-item module-card__deepdive-tag">+ Fördjupning</span>
          </div>
        </a>

        <a class="module-card" data-mod="5" href="/sv/presentationsteknik/modul-5/">
          <div class="module-card__head">
            <span class="module-card__num">05</span>
            <span class="module-card__status" data-status></span>
          </div>
          <h2 class="module-card__title">Digitala presentationer</h2>
          <p class="module-card__desc">Vad är annorlunda när du presenterar via skärm? Kamera, ljud, ögonkontakt, pausstrategi.</p>
          <div class="module-card__meta">
            <span class="module-card__meta-item">⏱ 8 min</span>
            <span class="module-card__meta-item module-card__deepdive-tag">+ Fördjupning</span>
          </div>
        </a>

        <a class="module-card" data-mod="6" href="/sv/presentationsteknik/modul-6/">
          <div class="module-card__head">
            <span class="module-card__num">06</span>
            <span class="module-card__status" data-status></span>
          </div>
          <h2 class="module-card__title">Röst, kropp och språk</h2>
          <p class="module-card__desc">Träningsmetaforen, essensen av kropp, röst och retorik. För dig som vill längre.</p>
          <div class="module-card__meta">
            <span class="module-card__meta-item">⏱ 12 min</span>
            <span class="module-card__meta-item module-card__deepdive-tag">+ Fördjupning</span>
          </div>
        </a>

        <a class="module-card" data-mod="7" href="/sv/presentationsteknik/modul-7/">
          <div class="module-card__head">
            <span class="module-card__num">07</span>
            <span class="module-card__status" data-status></span>
          </div>
          <h2 class="module-card__title">Din checklista</h2>
          <p class="module-card__desc">Sammanfattning, reflektion och nedladdningsbar PDF-sammanfattning av kursen.</p>
          <div class="module-card__meta">
            <span class="module-card__meta-item">⏱ 5 min</span>
          </div>
        </a>

      </div>
    </section>
  </main>

  <div data-include="/assets/partials/footer-sv.html"></div>

  <script defer src="/assets/js/include.js"></script>
  <script defer src="/assets/js/scroll-reveals.js"></script>
  <script defer src="/assets/js/course-progress.js"></script>
  <script defer>
    // Wait for course-progress.js + DOM ready
    document.addEventListener('DOMContentLoaded', () => {
      CourseProgress.init('sv');
      CourseProgress.renderOverview(
        document.getElementById('course-overview-progress'),
        null  // ingen modul är "current" från översikten
      );
      // Sätt status på varje modulkort
      const state = CourseProgress.getState();
      document.querySelectorAll('.module-card[data-mod]').forEach(card => {
        const mod = parseInt(card.dataset.mod, 10);
        const status = state[mod - 1] || 'not-started';
        const statusEl = card.querySelector('[data-status]');
        if (status === 'done') {
          card.classList.add('module-card--done');
          statusEl.classList.add('module-card__status--done');
          statusEl.textContent = '✓ Klar';
        } else if (status === 'current') {
          card.classList.add('module-card--current');
          statusEl.classList.add('module-card__status--current');
          statusEl.textContent = '● Pågår';
        } else {
          statusEl.textContent = 'Ej startad';
        }
      });
    });
  </script>
</body>
</html>
```

- [ ] **Step 2: Verify in preview**

```bash
cd "Ny JLSU hemsida"
python3 -m http.server 8765 > /tmp/preview.log 2>&1 &
open http://localhost:8765/sv/presentationsteknik/
```

Expected: hero with eyebrow "Presentationsteknik", h1, lede; below it a 7-step grey progress stege; below it a 7-card grid where every card shows "Ej startad". Hover lifts cards. Click navigates (404 expected for now since modules don't exist yet).

- [ ] **Step 3: Mobile + tablet visual check via DevTools**

Resize to 375px and 768px. Cards should reflow to 1 col, then 2 col. No overflow.

- [ ] **Step 4: Show Johan, wait for "kör"**

- [ ] **Step 5: Commit + push**

```bash
git add sv/presentationsteknik/index.html
git commit -m "feat(presentationsteknik): build SV overview page (replaces placeholder)"
git push
lsof -ti:8765 | xargs kill -9 2>/dev/null
```

---

# PART 3 — Modul 1 (canonical module — fully built, no fördjupning)

## Task 10: Create `sv/presentationsteknik/modul-1/index.html` skeleton

**Files:**
- Create: `sv/presentationsteknik/modul-1/index.html`

This is the canonical module template that modules 2–7 will copy. Get this one right.

- [ ] **Step 1: Create the file**

```html
<!DOCTYPE html>
<html lang="sv">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Modul 1: Varför presentationsteknik? — Presentationsteknik</title>
  <meta name="description" content="Modul 1 i kursen Presentationsteknik. Sineks Golden Circle, ditt varför, logik vs känslor.">
  <meta property="og:title" content="Modul 1: Varför presentationsteknik? — choosewise.education">
  <meta property="og:description" content="Sineks Golden Circle, ditt varför, logik vs känslor.">
  <meta property="og:image" content="/assets/images/brand/og-default.svg">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://choosewise.education/sv/presentationsteknik/modul-1/">
  <link rel="stylesheet" href="/assets/css/fonts.css">
  <link rel="stylesheet" href="/assets/css/tokens.css">
  <link rel="stylesheet" href="/assets/css/base.css">
  <link rel="stylesheet" href="/assets/css/components.css">
  <link rel="stylesheet" href="/assets/css/pages.css">
</head>
<body>
  <div data-include="/assets/partials/header-sv.html"></div>

  <main>
    <!-- Sticky topbar med breadcrumb och numrerad progressionsbar -->
    <div class="module-topbar">
      <div class="module-topbar__inner">
        <div class="module-topbar__crumb">
          <a href="/sv/presentationsteknik/">Kursöversikt</a> · Modul 1 av 7
        </div>
        <nav class="module-topbar__progress" id="module-progress" aria-label="Kursprogression"></nav>
      </div>
    </div>

    <article class="module-page">

      <!-- Modulhero -->
      <header class="module-hero">
        <div class="module-hero__eyebrow"><strong>Modul 1</strong> · 5 min läsning</div>
        <h1>Varför presentationsteknik?</h1>
        <p class="module-hero__lede">Innan vi pratar om typsnitt, pauser och animeringar — pratar vi om dig. Vad är det du vill att publiken ska tänka, känna och göra när du har slutat tala? Den frågan är hela skälet till att presentationsteknik finns.</p>
      </header>

      <!-- Sektion 1: definition -->
      <section class="module-section">
        <h2>Vad är presentationsteknik?</h2>
        <p>Ordet "teknik" kommer från grekiskans <em>technē</em> — "konst, skicklighet eller hantverk". I praktiken handlar det om hur du tar något du vet, känner eller tror, och flyttar det in i en annan människas huvud så att hen tar med sig det därifrån.</p>
        <p>Det är inte bara en mjukvara du öppnar och en knapp du trycker på. Det är ett hantverk. Det går att lära sig — och det går att försämra om man inte tänker efter.</p>
      </section>

      <!-- Sektion 2: minnesövning -->
      <section class="module-section">
        <h2>Tänk på ett möte för 4–8 veckor sedan</h2>
        <p>Vad minns du? Sannolikt inte slidesen. Sannolikt inte ens orden. Du minns en känsla, en bild, en mening, eller — i värsta fall — ingenting alls.</p>
        <p>Det är en viktig signal: <strong>publiken minns inte din presentation, de minns sin upplevelse av den</strong>. Ditt jobb som presentatör är att designa den upplevelsen.</p>
      </section>

      <!-- Sektion 3: Sineks Golden Circle -->
      <section class="module-section">
        <h2>Sineks Golden Circle — börja med varför</h2>
        <p>Simon Sineks modell är enkel: människor reagerar på <em>varför</em> du gör något, inte på <em>vad</em> du gör. När du presenterar något — en idé, en produkt, en förändring — börjar du oftast på fel ställe. Du börjar med vad. Du borde börja med varför.</p>
        <p>I bilen är det enkelt att räkna upp specifikationerna: 152 hk, 0–100 på 7,2 sekunder, svart med röda säten, 248 liter lastutrymme. Det är fakta. Det är inte ett varför. Bilköpet sker när någon kopplar fakta till en känsla — och känslan kommer från varför.</p>
        <p>Samma sak gäller din nästa presentation. Vad är det du brinner för? Vad är det du tror på? Det är publikens ingång till resten.</p>
      </section>

      <!-- Sektion 4: logik vs känsla -->
      <section class="module-section">
        <h2>Logik och fakta — eller instinkter och känslor?</h2>
        <p>Beslut fattas inte av tabeller. Beslut fattas av människor som tittar på tabeller och känner något. Det betyder inte att du ska skippa fakta — det betyder att fakta är ditt verktyg för att skapa en känsla av tillit, övertygelse eller insikt.</p>
        <p>Den bästa presentationen kombinerar båda: tillräckligt med fakta för att din publik ska veta att du vet vad du pratar om, och tillräckligt med känsla för att de ska bry sig.</p>
      </section>

      <!-- Sektion 5: Övning — ditt varför -->
      <section class="module-section">
        <h2>Övning: Ditt varför</h2>

        <div class="exercise">
          <div class="exercise__label">Reflektion · 5 min</div>
          <p class="exercise__prompt">Varför jobbar du med det du gör — och varför ska någon lyssna på vad du har att säga?</p>
          <form data-exercise="modul-1-varfor" class="exercise__form">
            <textarea
              class="exercise__textarea"
              name="answer"
              placeholder="Skriv din egen kortvariant — 2–4 meningar."
              required></textarea>
            <p class="exercise__hint">Sparas lokalt i din webbläsare. Bara du ser det.</p>
            <button type="submit" class="btn btn--primary exercise__btn">Spara svar</button>
            <p class="exercise__feedback" aria-live="polite"></p>
          </form>
        </div>

        <p>Spara det här svaret. Du kommer att använda det igen när vi i senare moduler pratar om hur man förmedlar det.</p>
      </section>

      <!-- Föregående / nästa modul -->
      <nav class="module-nav" aria-label="Modulnavigation">
        <a class="module-nav__link" href="/sv/presentationsteknik/">
          <div class="module-nav__direction">← Tillbaka</div>
          <div class="module-nav__title">Kursöversikt</div>
        </a>
        <a class="module-nav__link module-nav__link--next" href="/sv/presentationsteknik/modul-2/">
          <div class="module-nav__direction">Nästa →</div>
          <div class="module-nav__title">Designa diabilder — grunderna</div>
        </a>
      </nav>

    </article>
  </main>

  <div data-include="/assets/partials/footer-sv.html"></div>

  <script defer src="/assets/js/include.js"></script>
  <script defer src="/assets/js/course-progress.js"></script>
  <script defer src="/assets/js/course-exercises.js"></script>
  <script defer>
    document.addEventListener('DOMContentLoaded', () => {
      CourseProgress.init('sv');
      CourseProgress.renderTopbar(
        document.getElementById('module-progress'),
        1  // currentMod
      );
      // Mark this module as "current" if it isn't already done
      if (CourseProgress.getStatus(1) !== 'done') {
        CourseProgress.setCurrent(1);
      }
      // When user clicks "Nästa", mark this module as done
      document.querySelector('.module-nav__link--next')?.addEventListener('click', () => {
        CourseProgress.markDone(1);
      });
    });
  </script>
</body>
</html>
```

- [ ] **Step 2: Verify in preview**

```bash
cd "Ny JLSU hemsida"
python3 -m http.server 8765 > /tmp/preview.log 2>&1 &
open http://localhost:8765/sv/presentationsteknik/modul-1/
```

Expected:
1. Sticky topbar visible with breadcrumb left, numbered progress bar right (modul 1 = terracotta circle, others grey)
2. "Modul 1 · 5 min läsning" eyebrow
3. h1 "Varför presentationsteknik?"
4. 5 sections of content
5. Övning block (yellow-tinted background, accent border-left)
6. Föregående/nästa nav at bottom
7. Click into modul 1 from översiktsvyn — modul 1 should now be "● Pågår"

- [ ] **Step 3: Test exercise persistence**

In the textarea, type "Test svar". Click "Spara svar". Page should show "Sparat ✓". Refresh page. Textarea should still contain "Test svar".

- [ ] **Step 4: Mobile check (375px width)**

Sticky topbar should stack vertically or shrink — verify breadcrumb + progress bar both visible. Module nav (prev/next) should stack to single column.

- [ ] **Step 5: Show Johan; iterate on copy if needed**

This is the **content review checkpoint** for Modul 1. Johan reads the prose and either approves or requests edits. Apply edits inline before commit.

- [ ] **Step 6: Commit + push**

```bash
git add sv/presentationsteknik/modul-1/index.html
git commit -m "feat(presentationsteknik): build modul 1 — Varför presentationsteknik?"
git push
lsof -ti:8765 | xargs kill -9 2>/dev/null
```

---

# PART 4 — Modul 2 (Designa diabilder — grunderna) + fördjupning

Modul 2 follows Modul 1's template but adds a `reveal-on-click` exercise plus a deepdive-cta. Slide images are referenced (placeholder until Part 10 exports them).

## Task 11: Build `sv/presentationsteknik/modul-2/index.html`

**Files:**
- Create: `sv/presentationsteknik/modul-2/index.html`

**Content brief (drafted in spec; finalize during execution):**
- 6 sections: ett budskap per slide; max 6 objekt; färg & kontrast; typografi; styra blicken; övning
- Slide images referenced: `/assets/images/presentation-skills/slides/slide-064-kontrast-vit.jpg` (and 3 colors), `/assets/images/presentation-skills/slides/slide-040-prickar.jpg`
- Exercise: reveal-on-click "fel slide → rätt slide" (custom JS inline)
- Deepdive CTA at bottom linking to `fordjupning/`

- [ ] **Step 1: Copy modul-1 as starting point**

```bash
cp sv/presentationsteknik/modul-1/index.html sv/presentationsteknik/modul-2/index.html
```

- [ ] **Step 2: Open the new file and update**

Update in this order:
- `<title>` → `Modul 2: Designa diabilder — grunderna — Presentationsteknik`
- og:title, og:description, og:url to match modul 2
- breadcrumb: "Modul 2 av 7"
- topbar JS init: `CourseProgress.renderTopbar(..., 2)` and `setCurrent(2)`
- markDone listener: `CourseProgress.markDone(2)`
- module-hero eyebrow: `<strong>Modul 2</strong> · 10 min läsning`
- h1: `Designa diabilder — grunderna`
- lede: `En bra slide hjälper publiken förstå dig — den tävlar inte med dig om uppmärksamhet. Det här är de fem reglerna som gör störst skillnad.`
- Replace 4 content sections with modul-2 content (provided as content brief below)
- Replace övning with reveal-on-click variant (HTML + small inline script)
- Add `<a class="deepdive-cta" href="/sv/presentationsteknik/modul-2/fordjupning/">…</a>` block before the module-nav
- Update module-nav: prev → modul-1, next → modul-3

**Content draft for the 5 main sections** (refine with Johan during execution):

```html
<!-- Sektion 1: ett budskap per slide -->
<section class="module-section">
  <h2>Ett budskap per slide</h2>
  <p>Varje slide ska bära ett budskap. Inte två. Inte ett halvt. Ett. Om du har två saker att säga, bygg två slides.</p>
  <p>Det här är inte en regel om grafisk design — det är en regel om uppmärksamhet. När en slide har två budskap måste publiken välja vilket av dem de ska följa. De är då inte med dig längre. De är hos sig själva, och försöker sortera.</p>
</section>

<!-- Sektion 2: max 6 objekt -->
<section class="module-section">
  <h2>Max sex objekt per slide</h2>
  <p>Med "objekt" menar jag allt som syns: ord, bilder, ikoner, linjer, logotyper. När antalet passerar sex tappar publiken översikten. Det blir brus, inte signal.</p>
  <p>Ett snabbt test: visa din slide för en vän i tre sekunder, dölj den, fråga vad de såg. Om svaret är vagt har sliden för många objekt.</p>
  <figure class="module-figure">
    <img src="/assets/images/presentation-skills/slides/slide-040-prickar.jpg"
         alt="Slide med 11 utspridda prickar — för många objekt att hålla i blicken samtidigt.">
    <figcaption>Tio sekunder på den här sliden räcker inte för publiken att räkna. Bygg om till färre objekt eller en grupp.</figcaption>
  </figure>
</section>

<!-- Sektion 3: färg & kontrast -->
<section class="module-section">
  <h2>Färg och kontrast</h2>
  <p>Bakgrunden styr fokus. Ljus bakgrund tar bort uppmärksamhet från dig som presentatör — publiken tittar på sliden, inte på dig. Mörk bakgrund är diskret — den glider in i bakgrunden av rummet och låter dig stå kvar i centrum.</p>
  <p>Använd få färger, och använd dem genomgående. Regnbågen är inte ett designsystem. Två accentfärger räcker långt.</p>
</section>

<!-- Sektion 4: typografi -->
<section class="module-section">
  <h2>Typografi</h2>
  <p>Stora teckenstorlekar där du vill att publiken ska titta. Små där det är referensinformation. Blanda inte storlekar inom samma "uppmärksamhetslager".</p>
  <p>Sans-serif uppfattas oftast som lättare att läsa på avstånd; serif kan kännas tyngre men ger mer karaktär. Välj en familj och håll dig till den. Behåll tydlig kontrast mellan text och bakgrund — om du tvekar är kontrasten för låg.</p>
</section>

<!-- Sektion 5: styra blicken -->
<section class="module-section">
  <h2>Styr blicken med färg</h2>
  <p>Färg kan göra ett enda ord på en slide till det enda du behöver säga. När allt är grått förutom siffran "47%" är det den siffran publiken kommer ihåg.</p>
  <p>Det här är ett kraftfullt verktyg — och det är därför det inte ska användas hela tiden. När allt är färgmarkerat är ingenting markerat.</p>
</section>
```

**Övning HTML + inline script (reveal-on-click):**

```html
<section class="module-section">
  <h2>Övning: en slide, två versioner</h2>
  <div class="exercise">
    <div class="exercise__label">Klicka för att avslöja · 1 min</div>
    <p class="exercise__prompt">Här är en typisk slide. Klicka för att se hur den hade kunnat byggas annorlunda.</p>
    <div id="reveal-slide" style="position: relative; cursor: pointer; user-select: none;">
      <img id="reveal-img"
           src="/assets/images/presentation-skills/slides/slide-modul2-fore.jpg"
           alt="Före: en slide med fyra bullet-punkter och en rubrik."
           style="width: 100%; border-radius: var(--radius-sm); display: block;">
      <div id="reveal-overlay"
           style="position: absolute; inset: 0; display: grid; place-items: center; background: rgba(26,26,24,0.55); color: var(--color-dark-text); border-radius: var(--radius-sm); transition: opacity 0.4s;">
        <span style="font-family: var(--font-display); font-size: 1.25rem;">Klicka för att se efter →</span>
      </div>
    </div>
    <button id="reveal-toggle" class="btn btn--primary exercise__btn" style="margin-top: var(--space-3);">
      Visa "efter"-versionen
    </button>
    <p class="exercise__feedback" id="reveal-feedback" aria-live="polite"></p>
  </div>
</section>
```

Add this inline script just before `</body>`-script-block (after `course-exercises.js`):

```js
<script defer>
  document.addEventListener('DOMContentLoaded', () => {
    const img = document.getElementById('reveal-img');
    const overlay = document.getElementById('reveal-overlay');
    const btn = document.getElementById('reveal-toggle');
    const feedback = document.getElementById('reveal-feedback');
    const FORE = '/assets/images/presentation-skills/slides/slide-modul2-fore.jpg';
    const EFTER = '/assets/images/presentation-skills/slides/slide-modul2-efter.jpg';
    let revealed = false;
    function toggle() {
      revealed = !revealed;
      img.src = revealed ? EFTER : FORE;
      img.alt = revealed
        ? 'Efter: samma slide men med ett enda kärnbudskap som tar fokus.'
        : 'Före: en slide med fyra bullet-punkter och en rubrik.';
      overlay.style.opacity = revealed ? '0' : '1';
      btn.textContent = revealed ? 'Tillbaka till "före"' : 'Visa "efter"-versionen';
      feedback.textContent = revealed
        ? 'Lägg märke till hur ditt öga drogs någon helt annanstans här.'
        : '';
    }
    document.getElementById('reveal-slide').addEventListener('click', toggle);
    btn.addEventListener('click', (e) => { e.preventDefault(); toggle(); });
  });
</script>
```

**Deep-dive CTA block** (placed after övningen, before module-nav):

```html
<a class="deepdive-cta" href="/sv/presentationsteknik/modul-2/fordjupning/">
  <div class="deepdive-cta__icon">↓</div>
  <div>
    <h3 class="deepdive-cta__title">Fördjupning: färgteori och typografi för presentatörer</h3>
    <p class="deepdive-cta__desc">Praktiska principer från designvärlden, översatt för dig som inte är designer men presenterar. ~7 min läsning.</p>
  </div>
  <div class="deepdive-cta__arrow">Öppna →</div>
</a>
```

- [ ] **Step 3: Verify**

```bash
python3 -m http.server 8765 > /tmp/preview.log 2>&1 &
open http://localhost:8765/sv/presentationsteknik/modul-2/
```

Page renders, topbar shows modul 2 as current, övning works (click image or button toggles between 'fore' and 'efter' image — image will be broken until Part 10 produces the slides; that's expected for now), deepdive-cta visible at bottom.

- [ ] **Step 4: Show Johan, get content approval**

- [ ] **Step 5: Commit + push**

```bash
git add sv/presentationsteknik/modul-2/index.html
git commit -m "feat(presentationsteknik): build modul 2 — Designa diabilder grunderna"
git push
lsof -ti:8765 | xargs kill -9 2>/dev/null
```

---

## Task 12: Build `sv/presentationsteknik/modul-2/fordjupning/index.html`

**Files:**
- Create: `sv/presentationsteknik/modul-2/fordjupning/index.html`

**Content brief — färgteori + typografi för presentatörer:**
- Fördjupningens scope: 5–7 sektioner, ~7 min läsning
- Sources to scrape during execution: Material Design Color Theory, Adobe color/contrast guides, Practical Typography (Matthew Butterick), Smashing Magazine articles on slide typography, Garr Reynolds (Presentation Zen)
- Topics to cover:
  1. Färgens psykologi i en presentationskontext — vad olika färger signalerar
  2. WCAG-kontrast — varför 4.5:1 är ett minimum, inte en standard
  3. Färgharmoni — komplement, analog, triad — och varför trial-and-error oftast räcker
  4. Typsnittsfamiljer — sans, serif, slab — när använda vad i en slide-kontext
  5. Hierarki via storlek + vikt + färg
  6. Avstånd (line-height, letter-spacing) på avstånd
  7. När du *ska* bryta reglerna

- [ ] **Step 1: Research best practice (web fetch / web search)**

Spend 5–10 search queries gathering current best practice. Compile a notes file at `/tmp/fordjupning-modul-2-notes.md` with quoted sources you'll cite. Show Johan the source list before drafting; let him remove sources that don't fit his voice.

- [ ] **Step 2: Copy modul-1/index.html as starting point**

```bash
cp sv/presentationsteknik/modul-1/index.html sv/presentationsteknik/modul-2/fordjupning/index.html
```

- [ ] **Step 3: Update head + topbar to mark modul 2 as "current"**

- breadcrumb: `<a href="/sv/presentationsteknik/">Kursöversikt</a> · <a href="/sv/presentationsteknik/modul-2/">Modul 2</a> · Fördjupning`
- title, og:* matching
- topbar JS: `renderTopbar(..., 2)` (still highlights modul 2 since fördjupning is "part of" modul 2)
- module-hero eyebrow: `<strong>Modul 2 · Fördjupning</strong> · 7 min läsning`
- h1: `Färgteori och typografi för presentatörer`
- lede: short paragraph framing fördjupningen as "för dig som vill grunda dina val på något starkare än magkänsla"

- [ ] **Step 4: Replace content sections with drafted fördjupningsinnehåll**

Each of the 7 sections is a `<section class="module-section">` with h2 + 2–4 paragraphs. Pull from research notes. Keep Johan's voice: auktoritativ men varm, klart men inte torrt.

- [ ] **Step 5: Remove the övning section and the deepdive-cta** (fördjupning has no further fördjupning)

- [ ] **Step 6: Update module-nav at bottom**

```html
<nav class="module-nav" aria-label="Navigation">
  <a class="module-nav__link" href="/sv/presentationsteknik/modul-2/">
    <div class="module-nav__direction">← Tillbaka</div>
    <div class="module-nav__title">Modul 2 — Designa diabilder</div>
  </a>
  <a class="module-nav__link module-nav__link--next" href="/sv/presentationsteknik/modul-3/">
    <div class="module-nav__direction">Nästa modul →</div>
    <div class="module-nav__title">När diabilden krockar med dig</div>
  </a>
</nav>
```

- [ ] **Step 7: Verify**

Preview, walk through, check topbar still works, check sticky on scroll.

- [ ] **Step 8: Show Johan, iterate on content if needed**

- [ ] **Step 9: Commit + push**

```bash
git add sv/presentationsteknik/modul-2/fordjupning/index.html
git commit -m "feat(presentationsteknik): add modul 2 fördjupning — färgteori + typografi"
git push
```

---

# PART 5 — Modul 3 (När diabilden krockar med dig) + fördjupning

## Task 13: Build `sv/presentationsteknik/modul-3/index.html`

Same template as modul 2 (copy from modul-1, adapt). Update all metadata, breadcrumb, topbar JS to modul 3.

**Content brief (5 sections):**
1. **Textmuren** — läroplans-textmuren som exempel; "publiken kan inte läsa och lyssna samtidigt"
2. **Punktlistans dilemma** — apelsiner/citroner-exemplet; "ett ord per punkt är inte information"
3. **Tabeller — bra och dåliga** — HP/Lenovo-tabellen; "tabeller på en slide som har fler än 9 celler hör hemma i ett dokument"
4. **Mallar** — slide-mallar designade för 1990-talets kontorslandskap; skipa dem
5. **Animeringar och tvådiabildsprincipen** — när rörelse hjälper, när den distraherar

**Övning:** textarea-reflektion — "Tänk på en presentation du höll senast. Vilken slide var den texttätaste?"
- Same pattern as modul 1 (`data-exercise="modul-3-textmur"`)

**Slide-figurer to reference:**
- `slide-060-laroplan-textmur.jpg`
- `slide-080-punktlistor.jpg`
- `slide-200-hp-lenovo.jpg` (or similar)
- `slide-273-tiger.jpg`

**Deep-dive CTA:** "12 makeover-exempel — riktiga slides före och efter"

**Steps:** Same pattern as Task 11 — copy modul-1, adapt content, verify, show Johan, commit + push.

- [ ] **Step 1: Copy modul-1/index.html → modul-3/index.html**
- [ ] **Step 2: Update head metadata for modul 3**
- [ ] **Step 3: Update topbar JS to renderTopbar(..., 3)**
- [ ] **Step 4: Update module-hero eyebrow + h1 + lede**

```html
<header class="module-hero">
  <div class="module-hero__eyebrow"><strong>Modul 3</strong> · 8 min läsning</div>
  <h1>När diabilden krockar med dig</h1>
  <p class="module-hero__lede">Texttunga slides, klustrade punktlistor och tabeller med åtta kolumner — det är inte bara fult. De krockar med dig som presentatör. Publiken kan inte läsa och lyssna samtidigt.</p>
</header>
```

- [ ] **Step 5: Draft and insert 5 content sections** (use brief above; fill each section with 2–4 paragraphs in Johan's voice)
- [ ] **Step 6: Insert övning with `data-exercise="modul-3-textmur"`**
- [ ] **Step 7: Insert deepdive-cta linking to `fordjupning/`**
- [ ] **Step 8: Update module-nav** (prev=modul-2, next=modul-4)
- [ ] **Step 9: Verify in preview, show Johan**
- [ ] **Step 10: Commit + push**

```bash
git add sv/presentationsteknik/modul-3/index.html
git commit -m "feat(presentationsteknik): build modul 3 — När diabilden krockar med dig"
git push
```

---

## Task 14: Build `sv/presentationsteknik/modul-3/fordjupning/index.html`

**Files:**
- Create: `sv/presentationsteknik/modul-3/fordjupning/index.html`

**Content brief — 12 makeover-exempel:**
- Each makeover is a `<section class="module-section">` with: h3 (problemnamn), short text framing the issue (1 paragraph), `<figure>` with före + efter side-by-side, short caption explaining what changed.
- Examples to cover (each ~50 words intro + image pair):
  1. Textmuren → centrerat citat
  2. Bullet-list på 8 punkter → ett kärnbudskap + ikon
  3. Tabell med 9 kolumner → 3 nyckeltal i stora siffror
  4. Slide-mall med logo + datum + sidnummer → ren slide
  5. Stock-foto-collage → en relevant bild
  6. Animation av "fly-in" från sex håll → simpel reveal
  7. Diagrammet med tre Y-axlar → ett enkelt linjediagram
  8. Tre röriga ikoner → ett enkelt diagram
  9. Bullet-text + bild + citat på samma slide → tvådiabildsprincipen (två slides)
  10. Tunn 12pt-text → 36pt nyckelord
  11. Slide med tre olika typsnitt → en familj, två vikter
  12. "Inflation, ekonomi, kostnader" rubrik → "Maten kostar 23% mer än 2021"

- [ ] **Step 1: Copy modul-1/index.html → modul-3/fordjupning/index.html**
- [ ] **Step 2: Update head metadata; topbar `renderTopbar(..., 3)`**
- [ ] **Step 3: Update breadcrumb to "Kursöversikt · Modul 3 · Fördjupning"**
- [ ] **Step 4: module-hero eyebrow `Modul 3 · Fördjupning · 10 min`, h1 "Tolv makeover-exempel"**
- [ ] **Step 5: Replace content with 12 sections** (each: h3 problemnamn, paragraf, `<figure>` med 2 bilder före/efter sida vid sida, figcaption)
- [ ] **Step 6: Remove övning + deepdive-cta**
- [ ] **Step 7: Update module-nav** (prev=modul-3, next=modul-4)
- [ ] **Step 8: Verify, show Johan**
- [ ] **Step 9: Commit + push**

```bash
git add sv/presentationsteknik/modul-3/fordjupning/index.html
git commit -m "feat(presentationsteknik): add modul 3 fördjupning — 12 makeover-exempel"
git push
```

---

# PART 6 — Modul 4 (Framförandet — närvaro i rummet) + fördjupning

## Task 15: Build `sv/presentationsteknik/modul-4/index.html`

Same pattern. **Content brief (6 sektioner, ~10 min):**
1. **Innan du börjar** — testa tekniken, belysning på, är du synlig?
2. **Stå upp** — varför stå (även om du har möjlighet att sitta)
3. **Blicken** — på publiken, inte slides; "scanning" kontra "låsa fast"
4. **Pauser** — strategiska vs ofunktionella; "öööh" som konsekvens av rädsla för tystnad
5. **Interaktion och berättelser** — frågor, props, blädderblock, whiteboard, anekdoter
6. **Undvik att läsa från sliden** — om du måste, skriv stödord i talarvyn istället

**Övning:** "Räkna utfyllnadsljud" — embed a short audio clip (60 sec, royalty-free or Johan-recorded), user counts and types result, shows actual count after.
- Use vanilla `<audio>` element + textarea + reveal-button pattern.

**Slide-figurer:** 2–3 illustrations of "stå/sitta" and "blickkontakt" (tech: SVG illustrations or photographic from Johan's deck).

**Deep-dive CTA:** "Närvaro och scenrutiner — vad du kan lära av talartränare"

- [ ] **Step 1–10:** Same pattern as Task 13 (copy modul-1, adapt). Specific exercise HTML for "räkna utfyllnadsljud":

```html
<section class="module-section">
  <h2>Övning: Räkna "öööh"</h2>
  <div class="exercise">
    <div class="exercise__label">Lyssningsövning · 2 min</div>
    <p class="exercise__prompt">Lyssna på det här klippet (60 sekunder) och räkna varje gång du hör ett "öh", "ehm" eller "liksom".</p>
    <audio controls src="/assets/audio/modul-4-utfyllnadsljud.mp3" style="width: 100%;"></audio>
    <form data-exercise="modul-4-rakna" class="exercise__form" style="margin-top: var(--space-4);">
      <label for="rakna-input" style="display: block; margin-bottom: var(--space-2);">Hur många räknade du?</label>
      <input id="rakna-input" type="number" min="0" max="100" name="answer"
             class="exercise__textarea" style="min-height: auto; max-width: 120px;" required>
      <button type="submit" class="btn btn--primary exercise__btn">Spara mitt svar</button>
      <button type="button" id="rakna-show-answer" class="btn btn--secondary" style="margin-left: var(--space-3);">
        Visa rätt svar
      </button>
      <p class="exercise__feedback" aria-live="polite"></p>
      <p id="rakna-answer" style="display: none; margin-top: var(--space-3); padding: var(--space-3); background: var(--color-bg); border-radius: var(--radius-sm);">
        Rätt antal: <strong>14</strong>. Det är högt — och presentatören är inte sämre än andra. Det här är vad publiken hör utan att tänka på det.
      </p>
    </form>
  </div>
</section>
```

Inline script for "show answer" button:

```js
document.getElementById('rakna-show-answer')?.addEventListener('click', () => {
  document.getElementById('rakna-answer').style.display = 'block';
});
```

- [ ] **Step 11: Note for Johan: produce a 60-sec audio clip with intentional "öh"-counts**

This is a Johan-blocked task. He records himself or finds a royalty-free clip. Place at `assets/audio/modul-4-utfyllnadsljud.mp3` and adjust the "rätt antal" in the answer block to match.

- [ ] **Step 12: Commit + push** (same as before)

---

## Task 16: Build `sv/presentationsteknik/modul-4/fordjupning/index.html`

**Content brief:** scrape best practice from talartränare (Toastmasters principles, Nancy Duarte, Garr Reynolds, TED Speaker Coaching). 6–8 sections, ~8 min.

Topics to cover:
- Stagecraft basics — the 3 zones of the stage
- Body anchoring — "neutral position" som hem
- Vocal variety — register, tempo, volym
- Scene rhythm — building intensity, lull, climax
- Silence as tool
- Engagement loops — hur du skapar microinteractions med publiken
- The first 30 seconds (TED-research)
- The last 30 seconds

Same task pattern as Task 12. Steps elided (copy modul-1, update meta, update topbar `renderTopbar(..., 4)`, draft content, verify, show Johan, commit + push).

---

# PART 7 — Modul 5 (Digitala presentationer) + fördjupning

## Task 17: Build `sv/presentationsteknik/modul-5/index.html`

**Content brief (6 sektioner, ~8 min):**
1. **Vad skiljer från fysiska?** — "i samma rum" vs "digitalt"; sociala signaler du tappar
2. **Tekniken** — ljud, kamera, belysning, ståbord, händer
3. **Digital ögonkontakt** — kameran, inte skärmen; placering av ansikten i kameran
4. **Mötet börjar 9.10** — varför inte 9.00; runda starttider på fem minuter sänker uppmärksamheten
5. **Pausstrategi** — pauser mellan möten är inte lyx, det är produktivitet
6. **Interaktion digitalt** — chatten, breakout rooms, polls — verktyg som inte finns "på riktigt"

**Övning:** Checklista "Ditt digitala presentationsrum" — kryssa-av-frågor (12 punkter), sparas individuellt.

```html
<section class="module-section">
  <h2>Övning: Ditt digitala presentationsrum</h2>
  <div class="exercise">
    <div class="exercise__label">Checklista · 5 min</div>
    <p class="exercise__prompt">Kryssa av det du redan har på plats. Det som är okryssat är inför nästa digitala möte.</p>
    <form data-checklist="modul-5-rum" class="exercise__form">
      <label><input type="checkbox" name="check-1"> Kameran är i ögonhöjd (inte underifrån)</label><br>
      <label><input type="checkbox" name="check-2"> Ljuset kommer framifrån, inte bakifrån</label><br>
      <label><input type="checkbox" name="check-3"> Mikrofonen är extern, inte laptop-byggd</label><br>
      <label><input type="checkbox" name="check-4"> Bakgrunden är ren (inte virtuell)</label><br>
      <label><input type="checkbox" name="check-5"> Du står upp eller sitter rakt</label><br>
      <label><input type="checkbox" name="check-6"> Du tittar i kameran när du talar, inte på deltagarna</label><br>
      <label><input type="checkbox" name="check-7"> Du har testat länken innan mötet börjar</label><br>
      <label><input type="checkbox" name="check-8"> Du börjar mötet 9.10, inte 9.00</label><br>
      <label><input type="checkbox" name="check-9"> Du hälsar deltagarna individuellt när de kommer in</label><br>
      <label><input type="checkbox" name="check-10"> Du har en interaktionsmoment varje 7–10 min</label><br>
      <label><input type="checkbox" name="check-11"> Du stänger av aviseringar på datorn</label><br>
      <label><input type="checkbox" name="check-12"> Du har vatten inom räckhåll</label><br>
      <p class="exercise__feedback" aria-live="polite"></p>
    </form>
  </div>
</section>
```

Add to `course-exercises.js` a new feature: auto-persist checkbox forms by `data-checklist`. **Update Task 7's JS to support this** — split into a separate task if needed.

Actually: for clean separation, add a new function `CourseChecklists.init()` to course-exercises.js. Modify the file:

```js
// (append to course-exercises.js)
function initChecklists() {
  const forms = document.querySelectorAll('form[data-checklist]');
  forms.forEach((form) => {
    const key = form.dataset.checklist;
    const checkboxes = form.querySelectorAll('input[type="checkbox"]');
    const storageKey = `presentationsteknik-${getLang()}-checklist-${key}`;

    // Load
    try {
      const saved = JSON.parse(localStorage.getItem(storageKey) || '{}');
      checkboxes.forEach((cb) => { cb.checked = !!saved[cb.name]; });
    } catch { }

    // Save on change
    checkboxes.forEach((cb) => {
      cb.addEventListener('change', () => {
        const state = {};
        checkboxes.forEach((c) => { state[c.name] = c.checked; });
        try { localStorage.setItem(storageKey, JSON.stringify(state)); } catch { }
      });
    });
  });
}

// Update auto-init
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => { init(); initChecklists(); });
} else {
  init(); initChecklists();
}
```

**Add tests for checklist persistence to `scripts/test-course.html`** (in same task or split).

- [ ] **Step 1–5:** Update `course-exercises.js` with checklist support; add 2 tests to test-course.html; verify all green
- [ ] **Step 6: Commit JS change separately**

```bash
git add assets/js/course-exercises.js scripts/test-course.html
git commit -m "feat(js): add checklist persistence to course-exercises"
```

- [ ] **Step 7–14:** Build modul-5/index.html same pattern as previous modules (copy modul-1, adapt)
- [ ] **Step 15: Commit modul 5 page**

```bash
git add sv/presentationsteknik/modul-5/index.html
git commit -m "feat(presentationsteknik): build modul 5 — Digitala presentationer"
git push
```

---

## Task 18: Build `sv/presentationsteknik/modul-5/fordjupning/index.html`

**Content brief — kamera + plattformar (~6 min):**
- Sources: Microsoft Teams support docs, Zoom support docs, Google Meet help, articles on hybrid meetings
- 5–6 sections:
  1. Kamera-setup — placering, höjd, vinkel, vit balans
  2. Ljud — extern mikrofon vs laptop; ljudisolering
  3. Belysning — keylight, fill, undvik bakgrundsljus
  4. Plattformsspecifikt — Teams, Zoom, Meet (en sektion per)
  5. Hybridmöten — när några är i rummet och några är digitala

Same task pattern as Task 12.

---

# PART 8 — Modul 6 (Röst, kropp, språk) + fördjupning (special: recording)

## Task 19: Implement `course-recording.js`

**Files:**
- Create: `assets/js/course-recording.js`

This module handles the inspelningsövning in modul 6. Web Audio API records 30 seconds, allows playback, doesn't upload anywhere.

- [ ] **Step 1: Create the file**

```js
// course-recording.js
// In-browser 30-sec audio recording for modul 6.
// All processing happens locally — no uploads.
//
// Markup expected:
//   <div data-recorder>
//     <button data-start>Spela in 30 sek</button>
//     <button data-stop disabled>Stoppa</button>
//     <audio data-playback controls></audio>
//     <p data-status></p>
//   </div>
//
// Fallback: if no mic permission, show file upload <input type="file" accept="audio/*">.

(function (global) {
  function init() {
    const containers = document.querySelectorAll('[data-recorder]');
    containers.forEach(setup);
  }

  function setup(container) {
    const startBtn = container.querySelector('[data-start]');
    const stopBtn = container.querySelector('[data-stop]');
    const playback = container.querySelector('[data-playback]');
    const status = container.querySelector('[data-status]');

    let mediaRecorder = null;
    let chunks = [];
    let timeoutId = null;

    function setStatus(msg) { if (status) status.textContent = msg; }

    if (!navigator.mediaDevices?.getUserMedia) {
      setStatus('Din webbläsare stödjer inte inspelning. Ladda upp en ljudfil istället nedan.');
      addFallbackUpload(container, playback);
      return;
    }

    startBtn.addEventListener('click', async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        chunks = [];
        mediaRecorder.ondataavailable = (e) => { if (e.data.size) chunks.push(e.data); };
        mediaRecorder.onstop = () => {
          const blob = new Blob(chunks, { type: 'audio/webm' });
          playback.src = URL.createObjectURL(blob);
          stream.getTracks().forEach(t => t.stop());
          setStatus('Klar. Spela upp och lyssna på utfyllnadsljud.');
        };
        mediaRecorder.start();
        startBtn.disabled = true;
        stopBtn.disabled = false;
        setStatus('Spelar in… 30 sek max.');

        timeoutId = setTimeout(() => {
          if (mediaRecorder?.state === 'recording') stopBtn.click();
        }, 30000);
      } catch (err) {
        setStatus('Kunde inte starta inspelning. Du kan ladda upp en ljudfil istället.');
        addFallbackUpload(container, playback);
      }
    });

    stopBtn.addEventListener('click', () => {
      if (mediaRecorder?.state === 'recording') mediaRecorder.stop();
      if (timeoutId) clearTimeout(timeoutId);
      startBtn.disabled = false;
      stopBtn.disabled = true;
    });
  }

  function addFallbackUpload(container, playback) {
    if (container.querySelector('input[type=file]')) return; // already added
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'audio/*';
    input.style.marginTop = '1rem';
    input.addEventListener('change', () => {
      if (input.files[0]) {
        playback.src = URL.createObjectURL(input.files[0]);
      }
    });
    container.appendChild(input);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  global.CourseRecording = { init };
})(window);
```

- [ ] **Step 2: Add a manual smoke-test page**

Create `scripts/test-recording.html` with the markup above; load `course-recording.js`; verify start/stop works in browser, fallback shows when permission denied.

- [ ] **Step 3: Commit**

```bash
git add assets/js/course-recording.js scripts/test-recording.html
git commit -m "feat(js): add course-recording for modul 6 inspelningsövning"
```

---

## Task 20: Build `sv/presentationsteknik/modul-6/index.html`

**Content brief (~12 min, 5 sektioner):**
1. **Träningsmetafor** — "Gör vi det inte på träning kommer vi inte heller att göra det på match"
2. **Kropp** — sway (1), neutral position (34); kort om varje, varför de är vanliga svaga punkter
3. **Röst** — pauser (19, 21), tempo (8–10); "tystnad är ditt verktyg"
4. **Ögon/ansikte** — generell ögonkontakt (72); "publiken vill se dina ögon, inte din profil mot slidet"
5. **Språk** — trikolon (95); 3-rytmiken som retoriskt verktyg

**Övning:** inspelningsövning (30 sek) — använder course-recording.js
- Markup matches the data-attributes from Task 19

```html
<section class="module-section">
  <h2>Övning: spela in dig själv</h2>
  <div class="exercise">
    <div class="exercise__label">Inspelningsövning · 5 min</div>
    <p class="exercise__prompt">Spela in 30 sekunder där du presenterar något du gör på jobbet. Lyssna på det. Räkna utfyllnadsljud, paus-mönster och ditt tempo.</p>
    <p class="exercise__hint" style="margin-bottom: var(--space-3);">
      All bearbetning sker lokalt i din webbläsare. Ingen uppladdning sker. Du kan stänga sidan utan att något lämnar din dator.
    </p>
    <div data-recorder>
      <button data-start type="button" class="btn btn--primary">Starta inspelning (30 sek)</button>
      <button data-stop type="button" class="btn btn--secondary" disabled>Stoppa</button>
      <p data-status style="margin-top: var(--space-3);"></p>
      <audio data-playback controls style="width: 100%; margin-top: var(--space-3);"></audio>
    </div>
  </div>
</section>
```

**Deep-dive CTA:** "Vanliga svaga punkter — 19 tekniker att börja med"

- [ ] **Step 1–11:** Same pattern as previous modules. Make sure to include `<script defer src="/assets/js/course-recording.js"></script>` in the page's script block.
- [ ] **Step 12: Commit + push**

```bash
git add sv/presentationsteknik/modul-6/index.html
git commit -m "feat(presentationsteknik): build modul 6 — Röst, kropp och språk"
git push
```

---

## Task 21: Build `sv/presentationsteknik/modul-6/fordjupning/index.html`

**Content brief — 19 vanliga svaga punkter:**

Each technique is a `<section>` with: h3 (teknikens namn + numret från Johans deck), one paragraph beskrivning, one paragraph "Vanlig fallgrop", one paragraph "Tips att börja med". ~80–120 ord per teknik.

The 19 techniques (from spec):

**Kropp:** 1. Gunga, 4. Fidget, 5. Flykt/frys
**Röst:** 8–10. Tempo, 19+21. Pauser, 25. Utfyllnadsljud, 28. Artikulation
**Position & gester:** 34. Neutral position, 44. Funktionella gester, 66. Anchoring
**Ögon & ansikte:** 72. Generell ögonkontakt, 76. Neutralt ansiktsuttryck, 83. Skratta åt sig själv
**Språk & retorik:** 88. Onödiga utfyllnadsord, 89. Negationer, 95. Trikolon, 96. Repetition av ord
**Helhet:** 105. Intensitetsövergång, 107. Närvarande och autentisk

Group them under 6 h2-rubriker (Kropp, Röst, Position & gester, Ögon & ansikte, Språk & retorik, Helhet).

- [ ] **Step 1–8:** Same task pattern as Task 12 (copy modul-1, adapt). Long content — total ~2400 words. Plan for 1–2 review rounds with Johan.
- [ ] **Step 9: Commit + push**

---

# PART 9 — Modul 7 (Din checklista)

## Task 22: Build `sv/presentationsteknik/modul-7/index.html`

**Content brief (~5 min, 4 sektioner):**
1. **Sammanfattning** — en mening per modul (7 meningar)
2. **Reflektion** — textarea: "Vad är det första du ändrar inför nästa presentation?"
3. **Ladda ner PDF** — placeholder för nu (faktisk PDF kommer i Steg 2)
4. **Tipsa om relaterade resurser** — RÄTT-modellen, AI-guider på sajten

The reflektion uses `data-exercise="modul-7-foersta-aendring"`.
The "ladda ner PDF" is a button placeholder linking to `/assets/pdfs/presentationsteknik-sammanfattning.pdf` (404 until Steg 2). Add a styled "kommer snart"-badge above the button until Steg 2 is built.

Final action: when this module is "marked done", show a celebratory text + a "Återställ progress"-link in case user wants to restart.

```html
<section class="module-section">
  <h2>Återställ kursen</h2>
  <p>Vill du köra kursen från början igen, eller rensa dina svar?</p>
  <button id="reset-course" type="button" class="btn btn--secondary">Rensa mina svar och progress</button>
  <p id="reset-feedback" aria-live="polite" style="margin-top: var(--space-3); color: var(--color-text-soft);"></p>
</section>
```

Inline script:

```js
document.getElementById('reset-course')?.addEventListener('click', () => {
  if (confirm('Säkert? All din progress och alla dina svar tas bort.')) {
    Object.keys(localStorage)
      .filter(k => k.startsWith('presentationsteknik-sv-'))
      .forEach(k => localStorage.removeItem(k));
    document.getElementById('reset-feedback').textContent = 'Klart. Refresha sidan för att börja om.';
  }
});
```

- [ ] **Step 1–10:** Same pattern. Steps elided.
- [ ] **Step 11: Commit + push**

---

# PART 10 — Slide images (Johan-blocked)

## Task 23: Johan exports slides without Advania-branding

**Files:**
- `assets/images/presentation-skills/slides/` ← Johan places exported PNGs here

**This is a Johan-task.** Specify the exact slides he needs to export, with naming conventions.

- [ ] **Step 1: I produce a list of required slides**

Markdown table at `docs/presentation-skills-slide-list.md`:

| Filename | Source slide # | Description | Used in |
|----------|----------------|-------------|---------|
| `slide-040-prickar.jpg` | Del 1 slide 40 | 11 utspridda prickar | Modul 2 §2 |
| `slide-064-kontrast-vit.jpg` | Del 1 slide 64 | Vit bakgrund, svart text | Modul 2 §3 |
| `slide-069-kontrast-svart.jpg` | Del 1 slide 69 | Svart bakgrund, vit text | Modul 2 §3 |
| `slide-060-laroplan-textmur.jpg` | Del 1 slide 60 | Läroplanstexten på svart | Modul 3 §1 |
| `slide-080-punktlistor-bra.jpg` | Del 1 slide 80 | Bullet-list "apelsiner..." | Modul 3 §2 |
| `slide-200-hp-lenovo-tabell.jpg` | Del 1 slide 200 | Tabell HP/Lenovo/Acer/Asus | Modul 3 §3 |
| `slide-269-tiger.jpg` | Del 1 slide 269 | Tiger-bilden låg upplösning | Modul 3 §5 |
| ... (extend list as we build modules) | | | |

I produce this list during the first time we draft each modul's content. List grows incrementally. Final count expected: 25–40.

- [ ] **Step 2: Johan exports from Keynote**
- Format: JPG, 1920×1080, kvalitet "Bra"
- Without Advania-loggor (use a JLSU-version of the Keynote, or temporarily hide logo layer)
- Filename convention: `slide-NNN-kort-namn.jpg`
- Place in `assets/images/presentation-skills/slides/`

- [ ] **Step 3: I optimize each slide**

```bash
cd "Ny JLSU hemsida"
node scripts/optimize-images.js assets/images/presentation-skills/slides/
```

This produces WebP variants and keeps JPG fallback. Update modul HTML to use `<picture>` if needed for responsive.

- [ ] **Step 4: Verify each modul page renders slide correctly**

Walk every modul, check no broken images.

- [ ] **Step 5: Commit**

```bash
git add assets/images/presentation-skills/ docs/presentation-skills-slide-list.md
git commit -m "assets(presentationsteknik): add curated slide images from Keynote"
git push
```

---

# PART 11 — Final integration

## Task 24: Update sitemap.xml + SV homepage

**Files:**
- Modify: `sitemap.xml` — add 12 new SV URLs
- Modify: `sv/index.html` — add a Presentationsteknik section linking to course

- [ ] **Step 1: Add to sitemap.xml** (insert in alphabetical-ish order between presentationsteknik placeholder and guider section)

Replace the existing single placeholder URL with all 12:

```xml
  <url><loc>https://choosewise.education/sv/presentationsteknik/</loc></url>
  <url><loc>https://choosewise.education/sv/presentationsteknik/modul-1/</loc></url>
  <url><loc>https://choosewise.education/sv/presentationsteknik/modul-2/</loc></url>
  <url><loc>https://choosewise.education/sv/presentationsteknik/modul-2/fordjupning/</loc></url>
  <url><loc>https://choosewise.education/sv/presentationsteknik/modul-3/</loc></url>
  <url><loc>https://choosewise.education/sv/presentationsteknik/modul-3/fordjupning/</loc></url>
  <url><loc>https://choosewise.education/sv/presentationsteknik/modul-4/</loc></url>
  <url><loc>https://choosewise.education/sv/presentationsteknik/modul-4/fordjupning/</loc></url>
  <url><loc>https://choosewise.education/sv/presentationsteknik/modul-5/</loc></url>
  <url><loc>https://choosewise.education/sv/presentationsteknik/modul-5/fordjupning/</loc></url>
  <url><loc>https://choosewise.education/sv/presentationsteknik/modul-6/</loc></url>
  <url><loc>https://choosewise.education/sv/presentationsteknik/modul-6/fordjupning/</loc></url>
  <url><loc>https://choosewise.education/sv/presentationsteknik/modul-7/</loc></url>
```

- [ ] **Step 2: Add Presentationsteknik-sektion till SV-startsidan**

Open `sv/index.html`. Mellan WISE/RÄTT-sektion och Guider-sektion, lägg till:

```html
<section class="section section--alt" data-reveal>
  <div class="container">
    <h2 class="section__title">Presentationsteknik</h2>
    <p class="section__lede">En interaktiv kurs i sju moduler för dig som vill att din publik ska minnas vad du sa — inte vad du visade. Gå hela kursen från början, eller plocka de delar du behöver.</p>
    <a class="btn btn--ghost" href="/sv/presentationsteknik/">Öppna kursen</a>
  </div>
</section>
```

(Verifiera att existerande sektion på SV-startsidan följer detta mönster — om inte, anpassa.)

- [ ] **Step 3: Verify, show Johan**

- [ ] **Step 4: Commit + push**

```bash
git add sitemap.xml sv/index.html
git commit -m "feat(presentationsteknik): wire course into sitemap + SV homepage"
git push
```

---

## Task 25: Final QA walk-through

- [ ] **Step 1: Walk every page from översikt → modul 1 → ... → modul 7 → fördjupningar**

Open browser at `/sv/presentationsteknik/` and click forward through every page. Note:
- Topbar always visible, reflects correct current modul
- Övningar work (textarea persist, checkbox persist, recording works)
- Slide images all load
- Prev/next navigation correct everywhere
- Deep-dive CTAs link correctly

- [ ] **Step 2: Mobile QA at 375px**

Use DevTools to set viewport to iPhone SE (375×667). Walk every page. Verify:
- Topbar progress bar is readable (linjerna döljs på 720px)
- Modulkort i grid blir 1 kolumn
- Module-nav stackad
- Övningar fungerar med touch

- [ ] **Step 3: Tablet QA at 768px**

Same, viewport 768. Verify 2-col grid, intermediate sizes.

- [ ] **Step 4: Lighthouse run on översiktsvyn**

```bash
npx --yes lighthouse http://localhost:8765/sv/presentationsteknik/ \
  --only-categories=performance,accessibility,best-practices,seo \
  --quiet --chrome-flags="--headless"
```

Expected: all scores ≥85, no a11y errors. If any fail, list them as fixup-tasks before moving on.

- [ ] **Step 5: All-clear commit** (only if any small fixes were needed during QA)

```bash
git add -A && git commit -m "fix(presentationsteknik): QA fixes from final walk-through"
git push
```

- [ ] **Step 6: Announce launch to Johan**

Confirm to Johan that Steg 1 is complete:
- Course live at https://choosewise.education/sv/presentationsteknik/
- Total: 13 pages (1 overview + 7 moduls + 5 fördjupningar)
- All content reviewed by Johan during execution
- localStorage state works
- Mobile + accessibility checked
- **Next:** Steg 2 (SV-PDF) gets a separate plan when Johan is ready.

---

## Self-review notes

**Spec coverage check:**

| Spec section | Where in plan |
|---|---|
| 7 modules with content | Tasks 10–22 |
| 5 deep-dives | Tasks 12, 14, 16, 18, 21 |
| Översiktsvy (grid) | Task 9 |
| Sticky topbar across all module pages | Tasks 2, 6 (CSS+JS); used in every module task |
| Mockups A approved | Task 9 produces översikt; Task 10 produces module page matching mockup C |
| Hybrid slide-image strategy | Tasks 11, 13, 15, 20 reference slides; Task 23 collects them |
| Interactive exercises (textarea, reveal, count, checklist, recording) | Tasks 10, 11, 15, 17, 19, 20 |
| localStorage state, namespaced | Tasks 6, 7 |
| Sitemap | Task 24 |
| SV homepage link | Task 24 |
| Mobile + a11y | Tasks 25 |
| Modul 6 fördjupning = 19 curated techniques | Task 21 |
| Övriga fördjupningar with web research | Tasks 12, 14, 16, 18 (each starts with research step) |
| Johan reviewer at every content task | Built into each task as "show Johan" step |

**Steg 2/3/4 not in this plan** — explicitly noted as out of scope.

**Risk: Tasks 11–22 contain "content draft" steps that depend on Johan's review.** This means execution will pause at each module for content iteration. That's intentional — it's the right granularity for Johan-the-author to drive content while engineering follows.

**Type/method consistency:** `CourseProgress.setCurrent`, `CourseProgress.markDone`, `CourseProgress.renderTopbar`, `CourseProgress.renderOverview` — all consistent across tasks. `data-exercise` attribute name consistent. `data-checklist` and `data-recorder` introduced in tasks 17 and 19 respectively, consistent with their JS modules.

**Placeholder scan:** No "TBD", "TODO", "fill in later". Content briefs are concrete (specific slides, specific topics, specific source domains). Each step that adds code shows the code.

**Plan is large but each task is bounded.** Recommended execution model: subagent-driven (Option 1 below) so we can review per-task and pause naturally at each Johan-content checkpoint.
