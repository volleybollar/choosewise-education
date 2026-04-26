# AI or human? — Design Spec

**Date:** 2026-04-26
**Author:** Johan Lindström + Claude
**Status:** Approved for implementation planning
**Site:** choosewise.education

---

## 1. Goal

Add an interactive page where visitors test whether they can distinguish AI-generated content from human-created content across three modalities: text, image, and video. The page is published in both English (root) and Swedish (`/sv/`) following the site's existing bilingual mirror pattern.

A secondary goal: rename and reorder the primary navigation to introduce the new page and clarify that the existing "NotebookLM Styles" page is best described as "Infographic Styles".

---

## 2. Scope

### In scope
- New page `/ai-or-human/` (EN) and `/sv/ai-eller-manniska/` (SV).
- Three interactive tests on each page (texts, images, videos — videos as placeholders).
- Optional 1–6 difficulty rating widget per test, with anonymous data collection to a Johan-owned Google Sheet via Apps Script.
- Primary nav reorder + label change for "NotebookLM Styles" → "Infographic Styles" / "Infografik-stilar".
- URL change for the styles page: `/notebooklm-styles/` → `/infographic-styles/`, `/sv/notebooklm-stilar/` → `/sv/infografik-stilar/`, with meta-refresh redirect shims at the old paths.
- All internal references updated (footer, header, sitemap, llms.txt, blog posts, guides, exports, scripts).
- SEO hygiene: canonical, hreflang, JSON-LD, OG tags for the new page.
- Privacy page update covering the difficulty-rating data collection.

### Out of scope
- Backend persistence of test results (no scoring history, no leaderboards).
- Login or analytics tracking of test answers.
- Generating real AI content for the texts (Claude writes 2 in Johan's voice; the other 2 are ipsum to be replaced later).
- Sourcing the videos (placeholders only — Johan provides mp4 files later).

---

## 3. Navigation changes

### 3.1 New menu order (EN, file: `assets/partials/header-en.html`)
1. The WISE Framework (`/wise/`)
2. AI Guides (`/guides/`)
3. **AI or human?** (`/ai-or-human/`) — NEW
4. Prompts (`/prompts/`)
5. Presentation Skills (`/presentation-skills/`)
6. Infographic Styles (`/infographic-styles/`) — RENAMED + URL CHANGED
7. Blog (`/blog/`)
8. About (`/about/`)

### 3.2 New menu order (SV, file: `assets/partials/header-sv.html`)
1. RÄTT-modellen (`/sv/ratt/`)
2. Guider (`/sv/guider/`)
3. **AI eller människa?** (`/sv/ai-eller-manniska/`) — NEW (note: uses "?" with capital A)
4. Promptar (`/sv/promptar/`)
5. Presentationsteknik (`/sv/presentationsteknik/`)
6. Infografik-stilar (`/sv/infografik-stilar/`) — RENAMED + URL CHANGED
7. Blogg (`/sv/blog/`)
8. Om (`/sv/om/`)

### 3.3 URL change for the styles page

The page currently at `/notebooklm-styles/` and `/sv/notebooklm-stilar/` is renamed and moved.

- New canonical URLs: `/infographic-styles/` and `/sv/infografik-stilar/`.
- Old paths must keep returning HTTP 200 (GitHub Pages cannot serve 301s) but redirect via `<meta http-equiv="refresh">` and a `<link rel="canonical">` pointing at the new URL. A visible link fallback is included for clients that do not honor the meta refresh.
- All site-internal references to the old paths must be updated to the new paths (see §7).

---

## 4. Page architecture

### 4.1 Hero (top of page)
Pattern matches existing pages (e.g. WISE, Guides):
- `eyebrow` (e.g. "Test yourself" / "Testa dig själv")
- `<h1>` matching the menu label exactly: "AI or human?" / "AI eller människa?"
- Lede paragraph (Swedish original supplied by Johan; EN is a translation):

> SV: "I takt med den snabba teknikutvecklingen blir det allt svårare att se skillnad på text, bild och video som är AI-genererad och text/bild och video som inte är det. Jag tänker inte på massproducerad AI-slop, utan det som genereras av människor som har kompetens att skapa kvalitativt innehåll. På den här sidan har jag skapat några enkla övningar där du kan testa om du kan se vad som är AI-genererat och vad som inte är det."
>
> EN: "As technology advances rapidly, it gets harder and harder to tell AI-generated text, images, and video apart from content that is not. I'm not thinking about mass-produced AI slop, but the kind of output produced by people who know how to create quality content with these tools. On this page I've put together a few short exercises where you can test whether you can see what's AI-generated and what's not."

### 4.2 Test 1 — Texts (2×2 grid)

**Section heading:** "Test 1 — Text" / "Test 1 — Texts"
**Question:** "Vilka två texter är AI-genererade?" / "Which two texts are AI-generated?"

**Layout:**
- 2×2 grid of flipcards. Same-topic pair = same row; cards stack to a single column on mobile.
- Row 1 (Topic A — "Lärares användning av AI som verktyg för att effektivisera sitt arbete"): one AI-style text + one ipsum placeholder. Position within the row randomized per page load.
- Row 2 (Topic B — "Skolans roll i samhället"): one AI-style text + one ipsum placeholder. Position within the row randomized per page load.
- Each text is 100–150 words.

**Card content:**
- Front: full text body (visible without flipping) + a single checkbox/toggle "AI-genererad" / "AI-generated".
- Back: large badge/label "AI-genererad" / "Inte AI-genererad" (or English equivalents) plus a short explanation line ("Skriven av Johan", "Genererad av en AI-modell" etc.).

**Interaction model — Hybrid (option C from brainstorming):**
1. Initial state: cards are NOT flippable. Checkboxes are interactive. User may select up to 2.
2. If user attempts to select a 3rd checkbox, the new selection is accepted and the oldest is silently deselected (max 2 enforced via JS).
3. "Visa svar" / "Show answers" button is disabled until exactly 2 are selected; enabled when exactly 2 are selected.
4. On click: the cards become flippable (clicking flips), score is calculated and rendered ("Du fick X av 2 rätt. Klicka på korten för att se vilka som är AI-genererade.").
5. "Nollställ" / "Reset" button: clears checkboxes, hides score, flips all cards back to front, re-locks flipping. Also re-randomizes card positions within each row.

**Texts Claude writes (in Johan's voice, see CLAUDE.md):**
- Topic A AI-style: ~120 words on teachers using AI to streamline their work — written in Johan's voice but with subtle AI tells (slight over-structure, balanced both-sides hedging, tidy parallel constructions).
- Topic B AI-style: ~120 words on schools' role in society — same approach.
- Both ipsum placeholders use the standard `Lorem ipsum…` pattern, ~120 words, with a `<!-- TODO: replace with Johan's text -->` comment.

### 4.3 Test 2 — Images

**Section heading:** "Test 2 — Bilder" / "Test 2 — Images"
**Lead text** (above image): "9 bilder. En del är AI-genererade och en del är inte det. Din uppgift är att kryssa i de som du tror är AI-genererade." / EN equivalent.

**Image:**
- File: `/assets/images/ai-or-human/photo-grid.jpg` (sourced from `~/Desktop/AI eller digitalt fotografi.jpeg`, optimized to ~85% JPEG quality, max 1600px wide, target ≤300 KB).
- Wrapped in a `.image-frame` container: light border (`var(--color-border)`), `--radius-md` corners, `--shadow-md`, internal padding `--space-3`.
- Single asset for both languages (the image itself contains no text).

**Controls below image:**
- Row of 9 numbered checkboxes 1–9, evenly spaced, with the number as the visible label.
- A "Klar!" / "Done!" button (always enabled — no minimum selection required).
- A "Nollställ" / "Reset" button (text-link style).

**Answer key (hardcoded as `data-correct-not-ai="1,6,8"` on the test container):**
- Not AI: 1, 6, 8
- AI-generated: 2, 3, 4, 5, 7, 9
- Verifies hint 2: each row and each column contains exactly one non-AI image (Row 1: 1, Row 2: 6, Row 3: 8; Col 1: 1, Col 2: 8, Col 3: 6).

**Scoring:**
- For each of the 9 numbers, user is correct if their checkbox state matches the actual AI/non-AI state. Score = number of correct cells out of 9.
- Feedback line: "Du fick X av 9 rätt." / "You got X of 9 right."

**Hints (below score, two flipcards in 16:9 default aspect):**
- Hint 1 — Front: "Ledtråd 1" / "Hint 1". Back: "Det finns 6 st AI-genererade bilder." / "Six of the images are AI-generated."
- Hint 2 — Front: "Ledtråd 2" / "Hint 2". Back: "I varje kolumn finns en bild som inte är AI-genererad. I varje rad finns en bild som inte är AI-genererad." / EN equivalent.

**Reset behavior:**
- Clears all 9 checkboxes.
- Hides score.
- Flips both hints back to front.

### 4.4 Test 3 — Videos

**Section heading:** "Test 3 — Video" / "Test 3 — Videos"
**Lead text:** "Tre videos. En är AI-genererad och två är det inte. Vilken tror du är AI-genererad?" / EN equivalent.

**Layout:**
- 3 video tiles side-by-side on desktop, stacked on mobile.
- Each tile: a numbered label (1, 2, 3) above an empty `<video controls>` element. A semi-transparent overlay reads "Video kommer snart" / "Video coming soon" until a real `src` is supplied.
- Hardcoded `data-src=""` on each `<video>` — Johan replaces with a real path later.

**Controls:**
- 3 radio buttons (group; only one selectable): "1", "2", "3".
- "Klar!" / "Done!" button (disabled until one is selected).
- "Nollställ" / "Reset" button.

**Answer key:**
- Stored as `data-correct-video="0"` on the test container, where `0` means "not yet defined" (so a click on Klar before videos are added returns a neutral message: "Lägger till facit när videorna är på plats.").
- When videos are added, Johan changes the value to `1`, `2`, or `3`.

**Scoring:**
- 0 or 1 right. Feedback "Rätt!" / "Correct!" or "Fel — det var video X." / "Wrong — it was video X." (only after `data-correct-video` is non-zero).

### 4.5 Difficulty rating widget (all three tests)

After the score line of each test, a small optional widget invites the user to rate how hard the test felt.

**Layout:**
- Heading line: "Var det lätt eller svårt att se vilket innehåll som var AI-genererat?" / "Was it easy or hard to spot the AI-generated content?"
- Sub-line: "Helt valfritt — din röst sparas anonymt." / "Optional — your vote is stored anonymously."
- A row of 6 round buttons labeled `1` through `6`, with end-labels "Väldigt lätt" (left) / "Very easy" and "Väldigt svårt" (right) / "Very hard".
- After click: buttons disable, the chosen one highlights, a "Tack!" / "Thanks!" line replaces the sub-line.

**Visibility:**
- Hidden until the user has submitted that test (`#test-N-score` becomes visible). The rating widget reveals at the same time.
- Resetting the test does NOT re-open the widget if a rating was already submitted in this session — one rating per test per session.

**State:**
- Tracked per test in `sessionStorage` under keys `aiOrHuman.rated.text|image|video` (truthy = already rated).

### 4.6 Telemetry — difficulty rating storage

**Approach:** Google Apps Script Web App writing to a Google Sheet owned by Johan.

**Why:** Free, no third-party data processor, privacy-respecting (no cookies, no IP logging), simple to read and analyze in the Sheet UI or Looker Studio.

**Endpoint configuration:**
- The Web App URL is stored as a constant at the top of `assets/js/ai-or-human.js`:
  ```js
  const TELEMETRY_URL = ''; // Apps Script Web App URL — set when Sheet is configured
  ```
- If `TELEMETRY_URL` is the empty string (e.g. before Johan provides his URL or in a forked environment), the rating widget submits silently and shows the Tack-confirmation but performs no network request.

**Payload (POST, JSON, `Content-Type: text/plain` to avoid CORS preflight):**
```json
{
  "ts": "2026-04-26T14:32:11.000Z",
  "lang": "sv",
  "test": "text",
  "rating": 4,
  "score": "1/2",
  "userScore": 1,
  "totalScore": 2
}
```

**Apps Script (Johan installs):**
```js
const SHEET_ID = '<johan-pastes-id>';

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
  return ContentService.createTextOutput(JSON.stringify({ok: true}))
    .setMimeType(ContentService.MimeType.JSON);
}
```

**Sheet header row (Johan creates manually once):**
`timestamp | lang | test | rating | user_score | total_score`

**Privacy notes:**
- No IP addresses, no user-agent, no cookies, no session IDs are sent or stored.
- Apps Script's own request log can be disabled via the script settings; recommended.
- The widget's privacy line links to `/privacy/` (EN) / `/sv/privacy/` (SV) for full disclosure.

**Failure handling:**
- The fetch is fire-and-forget (`.catch(() => {})`).
- The "Tack!" confirmation appears immediately on click, regardless of network outcome.
- This is acceptable because the data is non-essential and a missed submission is fine.

**Setup checklist for Johan (executed before merge to production):**
1. Create a Google Sheet titled "AI or human — difficulty ratings" with the header row above.
2. Tools → Apps Script → paste the script, set `SHEET_ID` to the Sheet ID.
3. Deploy → New deployment → Type: Web app → Execute as: Me → Who has access: Anyone.
4. Copy the deployment URL.
5. Send the URL to Claude (or paste into `assets/js/ai-or-human.js` directly).

---

## 5. Components and styling

### 5.1 Reuse
- `.flipcard`, `.flipcard__inner`, `.flipcard__face`, `.flipcard__front`, `.flipcard__back` — existing in `components.css`. Used by Test 2 hints and (with a variant) by Test 1 cards.
- `.btn`, `.eyebrow`, `.lede`, `.section`, `.container` — existing.

### 5.2 New CSS additions (in `assets/css/components.css`)

```css
/* Text-card variant for Test 1 — taller, no aspect-ratio lock */
.flipcard--text { aspect-ratio: auto; min-height: 18rem; }
.flipcard--text .flipcard__face { padding: var(--space-5); justify-content: space-between; }
.flipcard--text .flipcard__body { font-size: var(--fs-body); line-height: var(--lh-normal); }
.flipcard--text .flipcard__choice { /* checkbox row at bottom of front */ }

/* Quiz-shared utilities */
.quiz-section { margin-top: var(--space-9); }
.quiz-section__heading { /* matches .section__title */ }
.quiz-section__lead { /* matches .lede width */ max-width: var(--content-text-max); }
.quiz-grid--2x2 { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-5); }
.quiz-grid--3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-5); }
.quiz-controls { display: flex; flex-wrap: wrap; gap: var(--space-4); align-items: center; margin-top: var(--space-5); }
.quiz-options { display: flex; flex-wrap: wrap; gap: var(--space-3); }
.quiz-option { /* checkbox+label pair */ }
.quiz-feedback { margin-top: var(--space-4); font-family: var(--font-display); font-size: var(--fs-h3); }
.quiz-feedback[hidden] { display: none; }
.quiz-reset { /* text-link styled button */ background: none; border: 0; color: var(--color-accent); cursor: pointer; text-decoration: underline; }

/* Image-frame for Test 2 photo */
.image-frame { padding: var(--space-3); border: 1px solid var(--color-border); border-radius: var(--radius-md); box-shadow: var(--shadow-md); background: var(--color-bg); }
.image-frame img { display: block; width: 100%; height: auto; border-radius: var(--radius-sm); }

/* Video tile for Test 3 */
.video-tile { position: relative; aspect-ratio: 16/9; background: var(--color-bg-alt); border-radius: var(--radius-md); overflow: hidden; }
.video-tile__placeholder { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-family: var(--font-display); color: var(--color-text-soft); }
.video-tile__label { /* "1" "2" "3" small badge top-left */ }

/* Difficulty rating widget */
.rating { margin-top: var(--space-5); padding: var(--space-4) 0; border-top: 1px solid var(--color-border); }
.rating[hidden] { display: none; }
.rating__heading { font-family: var(--font-display); font-size: var(--fs-body); margin: 0 0 var(--space-2); }
.rating__hint { font-size: var(--fs-small); color: var(--color-text-soft); margin: 0 0 var(--space-3); }
.rating__scale { display: flex; gap: var(--space-2); align-items: center; flex-wrap: wrap; }
.rating__endlabel { font-size: var(--fs-small); color: var(--color-text-soft); }
.rating__btn { width: 2.5rem; height: 2.5rem; border-radius: 50%; border: 1px solid var(--color-border); background: var(--color-bg); cursor: pointer; font-family: var(--font-body); font-weight: 500; transition: all 0.2s; }
.rating__btn:hover:not(:disabled) { border-color: var(--color-accent); }
.rating__btn[aria-pressed="true"] { background: var(--color-accent); color: var(--color-dark-text); border-color: var(--color-accent); }
.rating__btn:disabled { cursor: default; opacity: 0.6; }
.rating__btn[aria-pressed="true"]:disabled { opacity: 1; }

/* Mobile breakpoints */
@media (max-width: 720px) {
  .quiz-grid--2x2 { grid-template-columns: 1fr; }
  .quiz-grid--3 { grid-template-columns: 1fr; }
  .rating__scale { gap: var(--space-1); }
  .rating__btn { width: 2.25rem; height: 2.25rem; }
}
```

### 5.3 JavaScript

**File:** `assets/js/ai-or-human.js`

Single script tag included from both language pages. Self-contained (no globals). Reads language from `document.documentElement.lang`. Uses `data-` attributes on test containers to find facit and behavior.

**Public surface:** none — IIFE, runs on `DOMContentLoaded`.

**Internal modules (within the IIFE):**
- `initTextTest(rootEl)` — handles selection cap, randomization, submit, score, reset, flip-locking.
- `initImageTest(rootEl)` — handles checkbox state, score against `data-correct-not-ai`, reset incl. flipping hints back.
- `initVideoTest(rootEl)` — handles radio state, score against `data-correct-video`, reset.
- `initRating(testRootEl, testKey)` — wires up the difficulty widget, sessionStorage gate, and POST to `TELEMETRY_URL`.
- A small shared utility `flipCard(cardEl, toState)` that toggles `is-flipped` class and respects the per-test "locked" state.

**Strings:**
- Hard-coded UI strings live in the HTML (already language-specific via the EN/SV mirror). The JS reads the rendered button labels rather than carrying its own translations.
- Score-line templates live in `data-` attributes on each test container, e.g. `data-feedback-template="Du fick {score} av {total} rätt."`. JS does the `{score}` / `{total}` substitution. This keeps all user-facing strings in the per-language HTML.

---

## 6. Files to create or modify

### 6.1 New files
- `ai-or-human/index.html` — EN page.
- `sv/ai-eller-manniska/index.html` — SV page.
- `infographic-styles/index.html` — moved from `notebooklm-styles/index.html`, with paths updated.
- `sv/infografik-stilar/index.html` — moved from `sv/notebooklm-stilar/index.html`, with paths updated.
- `assets/js/ai-or-human.js` — shared script.
- `assets/images/ai-or-human/photo-grid.jpg` — optimized image.

### 6.2 Modified files
- `assets/partials/header-en.html` — reorder + rename + new item.
- `assets/partials/header-sv.html` — same.
- `assets/partials/footer-en.html` — update NLM link → Infographic Styles.
- `assets/partials/footer-sv.html` — same.
- `assets/css/components.css` — add quiz styles, flipcard--text variant, image-frame, video-tile, rating widget.
- `sitemap.xml` — add new URLs (`/ai-or-human/`, `/sv/ai-eller-manniska/`, `/infographic-styles/`, `/sv/infografik-stilar/`); update old NLM entries to point to new URLs.
- `llms.txt` — replace NLM URLs, add new test page.
- `privacy/index.html` (and SV equivalent) — short paragraph disclosing the difficulty-rating data collection.
- `notebooklm-styles/index.html` — replaced with redirect shim.
- `sv/notebooklm-stilar/index.html` — replaced with redirect shim.
- `blog/posts/why-i-built-choosewise-education.html` — update internal link.
- `sv/blog/posts/varfor-jag-byggt-choosewise-education.html` — update internal link.
- `guides/gemini-notebooklm/index.html` — update internal link.
- `sv/guider/gemini-notebooklm/index.html` — update internal link.
- `exports/gemini-notebooklm-print-a4-en.html` — update internal link if any.
- `exports/gemini-notebooklm-print-a4-sv.html` — same.
- `scripts/parse-nlm-html.js` — update any path constants.

### 6.3 Redirect shim template

Used at `notebooklm-styles/index.html` and `sv/notebooklm-stilar/index.html`. Minimal HTML, no nav, no analytics.

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

---

## 7. SEO

- New pages get `<link rel="canonical">` to themselves and `<link rel="alternate" hreflang>` for the other language + `x-default`.
- New pages get `<meta property="og:image">` pointing at a suitable OG card. For the AI-or-human page, reuse an existing brand OG card if no custom one is requested in this iteration. Note this as a follow-up if a custom card is wanted.
- JSON-LD: minimal `WebPage` block matching the existing pattern; no FAQ schema unless content warrants it (it doesn't, in this iteration).
- `data-modified` / "Last updated" stamp matches the site's existing pattern.

---

## 8. Risks and mitigations

| Risk | Mitigation |
|---|---|
| URL change for Infographic Styles breaks external backlinks | Meta-refresh redirect shim + canonical at the old paths. |
| Search engines lose ranking on the renamed page | Canonical on the shim transfers signals; sitemap and llms.txt updated; link from new page back to old slug not needed. |
| Test 1 "AI in Johan's voice" texts feel obvious as AI | Texts go through Johan's review before merge. Spec marks them as iterative. |
| Test 3 video facit not yet known | `data-correct-video="0"` returns a neutral "not yet" message. Johan flips the value when videos land. |
| Mobile layout cramped on Test 2 (9 checkboxes + image) | Checkboxes wrap to two rows; tested at 360px width. |
| Per-load randomization confuses users who reload mid-test | Acceptable — reload is interpreted as a deliberate restart. Documented in script comments. |
| Apps Script Web App URL is a hard-coded constant in JS — anyone could spam it | Apps Script has built-in rate limits per origin; a malicious flood would just produce noise in the Sheet that Johan can filter out. Acceptable for this data type. |
| `TELEMETRY_URL` not set yet at first deploy | Widget submits silently and shows Tack-confirmation; no network call attempted. Implementation merges fine without the URL. |

---

## 9. Acceptance criteria

The implementation is complete when:

1. The new page renders correctly at `/ai-or-human/` and `/sv/ai-eller-manniska/` on the local preview server.
2. All three tests behave per §4: selection limits, score computation, reset, randomization (Test 1).
3. Nav reorder and rename are reflected in both `header-en.html` and `header-sv.html`.
4. Both Infographic Styles pages live at the new URLs and the old paths redirect via meta-refresh.
5. All 15 internal references (per §6.2) are updated and verified by `grep`.
6. `sitemap.xml` and `llms.txt` reflect the changes.
7. Mobile layout (≤720px) does not horizontally overflow on any of the three tests.
8. Manual smoke test confirms: tab-key keyboard nav works, all checkboxes/radios are reachable, score is announced visibly (and ideally via `aria-live`).
9. Johan reviews the two AI-style texts in Test 1 and approves them (or returns notes).
10. Difficulty rating widget appears below each test's score line, accepts one rating, persists state in `sessionStorage`, and posts to `TELEMETRY_URL` (if set). With `TELEMETRY_URL` empty, widget still works UI-side but performs no network call.
11. `/privacy/` (and SV equivalent) discloses the difficulty-rating collection.
