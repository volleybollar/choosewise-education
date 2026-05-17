# Evidence Toolkit — Design

**Status:** approved 2026-05-17
**Owner:** Johan Lindström
**Surface:** choosewise.education (English)
**Spec author:** brainstorming session, May 17 2026

---

## 1. Summary

A growing, domain-by-domain reference page on `choosewise.education` that lets teachers and school leaders see which teaching interventions have the biggest evidence-based effect on learning — with every effect size cross-referenced to a named, independent meta-analysis, and with a built-in prompt builder that turns any educational claim into a critical-evaluation prompt for ChatGPT, Claude, or any chatbot.

The toolkit uses **Gareth Manning's open Claude Education Skills catalogue** as its skill spine, but does not rely on Manning's evidence labels alone. Each card carries an **independently sourced effect size** (months of progress + Cohen's d), an **implementation cost** indicator, and a **transparent source line**. Where Manning has no independent meta-analytic backing, that absence is shown openly rather than hidden.

This page is the choosewise.education answer to the question *"how do I know which teaching practices actually work?"* — and to the related question *"how do I know if the evidence claim I just heard is real?"*

---

## 2. Goals

1. Help teachers identify which teaching interventions have the largest evidence-based effect on learning.
2. Solve the verification problem at the level of the page itself: every claim has a named, citable source, and any claim can be independently interrogated via the prompt builder.
3. Position choosewise.education as a credible, independent voice on teaching evidence — neither selling a method nor uncritically passing on Manning's labels.
4. Create a publication cadence (each new domain = a shippable launch + blog post + LinkedIn material).
5. Give school leaders a usable signal on whether an intervention is straightforward or a larger undertaking to introduce.

## 3. Non-goals

- **No monetary cost ratings.** EEF's UK £-data is the only structured source and it is UK-specific. We link to it instead.
- **No age-group or subject filters in v1.** Manning's data does not carry these reliably.
- **No vendor/product recommendations.** This is research, not procurement.
- **No social/comment layer.** Static, source-cited content only.
- **No Swedish version in v1.** English-only at launch; SV may follow.

---

## 4. Audience

Primary: working teachers and school leaders making professional judgments about teaching practice. Reads English. Some research literacy but not researchers themselves.

Secondary: EdTech consultants, instructional coaches, journalists writing about education evidence. They want the academic precision (Cohen's d, named meta-analyses) that the primary audience can ignore.

The page must work for both — teacher reads "+5 months progress" and gets it; consultant reads "d=0.60 (Latimier et al. 2021)" and gets the sourcing.

---

## 5. Information architecture

### URLs

| Path | Page |
|---|---|
| `/evidence/` | Hub page — overview, structure, list of domains, prompt builder |
| `/evidence/memory/` | Domain page — Memory & Learning Science (v1 launch) |
| `/evidence/<domain-slug>/` | Future domain pages (one per Manning domain) |

### Navigation

Top-level menu item **"Evidence Toolkit"** placed between *The WISE Framework* and *AI or human?* in `assets/partials/header-en.html`:

```
The WISE Framework | Evidence Toolkit | AI or human? | Prompts | Presentation Skills | Infographic Styles | Blog | About
```

### Hub page composition (`/evidence/`)

1. Hero with eyebrow, H1, lede paragraph.
2. **"How this toolkit is organised"** block — 3 numbered steps that make the structure immediately visible:
   1. Pick a domain
   2. Browse interventions ranked by effect size
   3. Interrogate any claim using the prompt builder
3. **Domains list** — cards for each Manning domain with one of three statuses: *Available now* (green left border), *Coming next*, or *Planned* (grey, lower opacity).
4. **"Why domain-by-domain?"** explainer note — defends depth over breadth.
5. **Standalone prompt builder** at the bottom.
6. Sources & further reading block.

### Domain page composition (`/evidence/<domain>/`)

1. **Domain header** block:
   - Breadcrumb: `Evidence Toolkit › <Domain name>`
   - H2 with domain name + green pill badge showing `N interventions`
   - Domain description (1–2 sentences)
   - Meta-pills: `Avg. effect`, `Strongest evidence`, `Last reviewed`
2. **Disclaimer** (yellow caveat block) — see §9.
3. **Toolbar**: search input + sort selector + tag filter row.
4. **Card grid** — one card per skill, see §8.
5. **Standalone prompt builder** — see §11.
6. **Sources & further reading** block including EEF Toolkit link.

---

## 6. Data model

Each skill is one record. v1 source spine is Manning's `registry.json`, extended with the fields below. Data lives in a single JSON file per domain (e.g. `/evidence/data/memory.json`) and is loaded by the page at render time.

```json
{
  "id": "memory-learning-science/spaced-practice-scheduler",
  "manning_name": "Spaced Practice Scheduler",
  "display_title": "Spaced Practice Scheduler",
  "domain_id": "memory-learning-science",
  "description": "Schedule retrieval intervals across a unit so learning is distributed, not massed.",
  "tags": ["spaced", "retrieval"],

  "effect_months": 5,
  "effect_months_source": "EEF Toolkit — Spaced learning strand",
  "effect_months_year": 2021,

  "effect_d": 0.60,
  "effect_d_source": "Latimier, Peyre & Ramus",
  "effect_d_journal": "Educational Psychology Review",
  "effect_d_year": 2021,

  "implementation_cost": "low",
  "implementation_cost_rationale": "Requires re-sequencing existing practice; no new materials or training.",

  "manning_label": "strong",
  "manning_url": "https://github.com/GarethManning/claude-education-skills/blob/main/skills/memory-learning-science/spaced-practice-scheduler/SKILL.md",

  "verification_status": "verified",
  "last_reviewed": "2026-05-17"
}
```

### Field rules

- `effect_months` and `effect_d` may be `null` when no quality source exists. The card then shows "no EEF strand" or "no independent meta-analysis found" instead of a number — never a fabricated figure.
- `implementation_cost` is one of `low | medium | high`. Editorial judgment, with `_rationale` always populated.
- `verification_status` is one of `verified | partial | unverified`. `verified` requires both a named meta-analysis AND an EEF strand. `partial` is one or the other. `unverified` is Manning label only.
- Sources lead with the most recent quality study (≤5 years preferred), with EEF as cross-reference where available.

---

## 7. Visual & brand fit

The page uses the existing choosewise.education design system (`assets/css/tokens.css`, `base.css`, `components.css`, `pages.css`). New patterns added to `components.css` rather than introducing a new CSS bundle.

Key palette additions (semantic tokens):
- `--effect-months`: teal (`#0f766e`) — for months-of-progress numbers (numeric reference colour)
- `--effect-d`: violet (`#6d28d9`) — for Cohen's d numbers (numeric reference colour)
- `--impl-low`: green (`#065f46` on `#d1fae5`)
- `--impl-med`: amber (`#92400e` on `#fef3c7`)
- `--impl-high`: red (`#b91c1c` on `#fee2e2`)
- `--disclaimer-bg`: `#fffbeb` with `#d97706` left border (yellow caveat block)
- `--prompt-builder-bg`: `#0f172a` (dark slate, matches site dark surfaces)

**Effect-size calibration palette** (muted earth tones — deliberately not bright traffic-light colours, so the page reads as *calibration* not *verdict*):
- `--band-below`: white text on `#b45309` (warm umber) — for "below typical schooling effect"
- `--band-around`: white text on `#1e40af` (deep blue) — for "around typical schooling effect"
- `--band-above`: white text on `#15803d` (forest green) — for "above typical schooling effect"

Typography follows existing choosewise tokens — Fraunces/Georgia for headlines, system sans for body.

---

## 8. Skill card

Each card contains, top to bottom:

1. **Domain label** (small uppercase, faint grey).
2. **Skill title** (Georgia, semibold).
3. **One-sentence description**.
4. **Metric block** — three columns in a single neutral panel:
   - `+N months progress` — shown as a coloured pill using the calibration palette (see §7 and §8a)
   - `d = 0.NN` — shown as a coloured pill using the same calibration palette
   - `Low / Medium / High` pill labelled "Implementation"
   - Source byline under each metric in muted grey (no colour)
5. **Source line** — primary source + year tag + EEF cross-reference + year tag.
6. **Footer row** — Manning tags on the left, **"Interrogate →"** action link on the right.

### 8a. Effect-size colour banding

Months of progress and Cohen's d are both colour-coded using three bands. The same band is applied to both metrics so the card reads consistently.

| Band | Months | Cohen's d | Token | Meaning |
|---|---|---|---|---|
| Below typical | ≤ +2 | < 0.30 | `--band-below` (umber) | Below Hattie's hinge point of d ≈ 0.40 |
| Around typical | +3 to +4 | 0.30–0.59 | `--band-around` (deep blue) | Around the average effect of a year of schooling |
| Above typical | ≥ +5 | ≥ 0.60 | `--band-above` (forest green) | Clearly above the typical schooling effect |

When the two metrics disagree on band (e.g. EEF says +3 months, the meta-analysis reports d=0.62), each pill takes its own band — that disagreement is informative and should be visible, not hidden by forcing a consensus.

When a metric is missing (`null`), its pill shows the no-data marker in neutral grey instead of a band colour.

Cards with missing data show explicit placeholders (`est. — no EEF strand`, `no independent meta-analysis found`) rather than hiding the absence.

---

## 9. Disclaimer block (canonical text)

Sits above the card grid on every domain page. Yellow caveat styling.

**Title:** *How to read these numbers*

1. **"Months of progress"** is a teacher-friendly shorthand from the EEF Toolkit. It is *not* directly comparable across studies — different meta-analyses use different baselines, age groups, and outcome measures. Treat it as a magnitude indicator, not a precise prediction.

2. **Cohen's d** is the standardised effect size used in the original meta-analyses. d ≈ 0.40 is Hattie's "hinge point" — the average effect of a year of schooling. Higher = larger relative effect, but context matters more than the number.

3. **Effect sizes are averages.** A skill that shows large average effects can still produce small or negative effects in a specific classroom. Use these as a starting point for professional judgment, not a substitute for it.

4. **Sources are dated.** Where multiple meta-analyses exist, we lead with the most recent quality study and cross-reference EEF where available.

5. **Implementation cost (Low / Medium / High)** is a practical signal — not an exact science — of what your school needs to invest in teacher time, training, and structural changes to actually run the intervention well. It is the editorial team's reading of what the intervention typically requires in practice. Use it to gauge whether something is straightforward to introduce or a larger undertaking — not as a budget figure.

6. **Some interventions are also priced in £ (UK)** by the EEF Toolkit. For monetary cost data, see the [EEF Teaching & Learning Toolkit](https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit).

7. **Colour bands signal calibration, not value.** An intervention in the "below typical" band is not "bad" — it means the intervention's average effect is below the typical effect of a year of schooling. That can still be appropriate for specific contexts the average does not capture. Use the colours as a calibration aid, not a verdict.

---

## 10. Filters & sort

### In v1
- **Sort by effect size** (default, descending — biggest moves on top).
- **Sort alphabetically** (secondary option).
- **Search** by name, description, or tag.
- **Filter by tag** — uses Manning's existing tag set per domain.

### Deliberately not in v1
- Age-group filter (Manning data unreliable).
- Teacher-time filter (Manning's `teacher_time` is self-reported, low signal).
- Disagreement flag (interesting but no clear v1 user).
- Monetary cost filter (off-mission; deferred to EEF link).

All filtering is client-side. No backend; static page served from the existing choosewise.education GitHub Pages setup.

---

## 11. Prompt builder

### Per-card entry point
Every card has an `Interrogate →` link in the footer. Clicking opens a modal pre-filled with a prompt specific to that skill (skill name, claim, primary source, year). User clicks **Copy** → pastes into any chatbot.

### Standalone entry point
Bottom of every domain page (and the hub page). A textarea labelled *"Interrogate any educational claim"* — user types a free-text claim, clicks **Build prompt**, gets the same template populated with the claim.

Both entry points share the same prompt template (§12).

### Thinking-mode hint
Inside the modal, above the prompt textarea, an amber-highlighted hint reads:

> 💡 **For best results, enable your chatbot's reasoning / thinking mode before pasting** — Claude's "Extended thinking", ChatGPT's "Think" mode, or Gemini's "Thinking" / 2.5 Pro reasoning. The prompt is more demanding than a typical Q&A and benefits from slower deliberation.

The prompt template itself also includes a `// Reasoning` instruction block (see §12) so that models running in thinking mode know to invoke their reasoning capacity, and models without an explicit mode at least know slow deliberation is wanted.

### Behaviour
- Pure client-side. No outbound API calls. No tracking of which prompts are generated.
- Copy-to-clipboard uses the standard `navigator.clipboard.writeText`.
- No "open in ChatGPT" button — chatbot-agnostic by design.

---

## 12. Prompt template (canonical content)

The prompt copied to the clipboard:

```
// Context
You are a research-literate education advisor speaking with a working
teacher. Your job is to help them think critically, not to give them a
pre-baked answer.

// The claim being checked
"<claim text>"
Source on the page: <primary source string, when available>.

// What I need you to do
1. Walk through the published research on this claim — what has actually
   been studied, by whom, and how rigorously the studies were designed.
2. Separate well-replicated findings from solid designs from one-off
   studies, underpowered samples, or contested results.
3. Name the conditions that weaken the evidence — narrow populations,
   short follow-ups, measurement quirks, missing replications.
4. Call out the gap between what the research actually shows and how the
   intervention is typically marketed, simplified, or oversold in CPD
   sessions, books, or social media.
5. Land on a practical takeaway a thoughtful teacher could defend in a
   staff meeting — neither a hype line nor a defensive hedge.
6. Cite specific, named meta-analyses or systematic reviews — by author,
   year, and journal. If you don't have a real citation, say so
   explicitly rather than inventing one.
7. Note any boundary conditions: subject, age group, country, school
   type, or context where the intervention works much better or much
   worse.
8. Distinguish the construct from the label — explain what the term
   actually means in the research vs. how it's used in popular
   discourse.
9. Flag publication bias, conflict-of-interest concerns, or vendor-funded
   research where relevant.
10. Suggest one or two stronger or comparable alternatives the teacher
    could also consider.
11. Discuss cost-effectiveness — both monetary (where data exists) and
    implementation cost (teacher time, training, structural change). Note
    where the intervention is most or least cost-effective.
12. End with a concrete picture of what this would look like in a real
    classroom next Monday — and what would NOT count as this intervention
    even if it's labelled that way.

// Output format
Use a structured response that is easy for a busy teacher to scan.
Specifically:

**Bottom line** (one sentence)
**Evidence strength** (with named sources)
**What the research actually supports**
**What it does NOT support**
**Boundary conditions**
**Common myths or exaggerations**
**Cost & implementation reality**
**On Monday in the classroom**
**Alternatives worth considering**
**Suggested follow-up reading**

// Tone
Plain professional English. Define jargon when first used. Speak to an
experienced teacher, not a researcher. If you are uncertain, say so.

// Reasoning
If you can use extended thinking or step-by-step reasoning mode for
this analysis, please do so. The questions above require careful
evaluation, not a fast first-pass answer.
```

**Anti-hallucination guardrail:** Instruction 6 is load-bearing — without it, LLMs reliably invent plausible-sounding meta-analyses. Do not weaken it.

**Response sections** are 10 (one added: *Cost & implementation reality*) to match the new instruction 11.

---

## 13. Implementation cost methodology

Each skill is rated **Low / Medium / High** by the editorial team (Johan + collaborator if any). Criteria:

- **Low** — runs inside existing lessons, no new materials needed, no training required beyond reading the SKILL.md. Examples: spaced practice scheduling, retrieval practice.
- **Medium** — needs new teacher prep, minor training, or materials creation. Examples: dual coding (requires visual asset preparation), structured discussion protocols.
- **High** — needs school-level commitment: timetable change, sustained CPD, role changes, or systemic restructuring. Examples: cross-age tutoring programmes, mastery learning across departments.

`implementation_cost_rationale` field on each record holds the 1-sentence justification. This is the editorial team's read, transparently labelled as such in the disclaimer.

---

## 14. Verification approach — the central question

The page's editorial position on *"how do we know Manning's claims are correct"*:

1. **We don't trust Manning's labels alone.** Every effect size on the page comes from an independently cited, named meta-analysis — not from Manning's strong/moderate/emerging tags.
2. **Where Manning has no independent backing, we say so.** The card shows the gap rather than papering over it.
3. **The reader can verify any claim themselves.** The prompt builder turns any card into a structured critical-evaluation prompt for any chatbot, with explicit anti-hallucination instructions.
4. **Sources are dated.** Every source carries a year tag visible on the card. Old sources are not hidden — the reader judges currency.

The page is therefore not "Manning's catalogue republished" — it is "Manning's catalogue used as a skill discovery layer, with an independent evidence layer added and the verification problem structurally addressed."

---

## 14a. Integration with the WISE Framework

Evidence Toolkit is the **S — Select the right tool** step of the existing WISE Framework on `/wise/`. The two surfaces are linked bidirectionally so a reader on either page understands how they relate.

### Forward link — on the Evidence Toolkit hub (`/evidence/`)

- **Hero eyebrow** reads: `Evidence Toolkit · The S in WISE`
- **Lede paragraph** (after the H1) includes a sentence: *"The Evidence Toolkit is the **S — Select the right tool** step of the [WISE Framework](/wise/). Once you've weighed the learning goal (W) and inspected what the subject calls for (I), this is where you select the teaching move with the strongest evidence base for your context. Then you evaluate the outcome (E) — and run the cycle again."*

### Back link — on the WISE page (`/wise/`)

Inside the existing **S — Select the right tool** step block (both Teacher and School Leader variants), add a short closing sentence with a link to `/evidence/`:

> *The [Evidence Toolkit](/evidence/) gives you a ranked, source-cited menu of teaching moves with the largest evidence-based effects — sorted by effect size, with implementation cost noted, and with a built-in prompt builder for interrogating any claim.*

### Not doing
Per-card WISE micro-markers were considered and rejected — every Evidence Toolkit card sits in the same WISE step, so a per-card "S" badge adds visual noise without per-card information. The integration belongs at section level, not on every card.

---

## 15. Rollout plan

| Phase | Domain | Skills | Status |
|---|---|---|---|
| v1 launch | Memory & Learning Science | 8 | Build now |
| v1.1 | Feedback & Formative Assessment | ~13 | Next |
| v1.2 | Explicit Instruction | 5 | Then |
| v1.3 | Self-Regulated Learning | 5 | Then |
| v1.4 | Questioning & Discussion | 4 | Then |
| later | remaining Manning domains | balance | TBD |

Each new domain ships as: data file + blog post on choosewise.education + LinkedIn announcement. New domain pages slot into the hub's domain list with status changing from "Coming next" / "Planned" to "Available now".

---

## 16. Source attribution policy

- **Primary citation per card** = the most recent quality meta-analysis or systematic review (≤5 years preferred when available).
- **Cross-reference** = EEF Toolkit strand where one maps.
- **Year tag** visible on every source line so reader can judge currency.
- **No invented citations.** If we cannot name a real source for an effect figure, the field stays `null` and the card shows the absence.
- **Manning attribution** preserved on the hub page sources block and in the README. CC BY-SA 4.0 honoured.

---

## 17. Build & integration notes

- Static HTML/CSS/vanilla JS — matches Johan's stated stack preference.
- Reuse existing `data-include` partial system for header/footer.
- Reuse existing CSS token system; add semantic tokens for the new effect/cost colours.
- Data files: one JSON per domain in `/evidence/data/<domain>.json`.
- Hub and domain pages each have their own `index.html` under `/evidence/` and `/evidence/<domain>/`.
- Cards are **pre-rendered into the static HTML at build time** (small Python script reads JSON → emits card markup), so the page is SEO-indexable and readable without JavaScript. JavaScript is only required for filtering, sorting, search, and the prompt builder.
- **Existing files to edit** (besides creating new `/evidence/` content):
  - `assets/partials/header-en.html` — insert the "Evidence Toolkit" nav item between "The WISE Framework" and "AI or human?"
  - `wise/index.html` — add the back-link sentence inside both `S — Select the right tool` step blocks (Teacher variant and School Leader variant)
  - `assets/css/components.css` — add the new effect-band colour tokens and pill styles
- Comment HTML/CSS/JS so Johan can modify it himself (per CLAUDE.md).

---

## 18. Open questions / explicit deferrals

- **Swedish version** — deferred. EN-only at launch. SV mirror later under `/sv/evidens/` if traffic warrants.
- **Exact set of 8 Memory skills** — selected from Manning's 8-skill `memory-learning-science` domain; final list confirmed during data preparation.
- **Editorial team for implementation-cost ratings** — Johan is the starting editorial voice; collaborator review noted but not required.
- **Schema versioning** — initial JSON schema is v1; explicit `schema_version` field reserved for later.

---

## 19. Acceptance criteria

This design is implementation-ready when:

- [ ] `/evidence/` hub page renders with structure-explainer block, domain cards (Memory live, others "Planned/Coming"), prompt builder, sources block.
- [ ] `/evidence/memory/` renders with domain header, disclaimer, toolbar, 8 skill cards with metric blocks, prompt builder, sources block.
- [ ] Every card shows months + d + implementation cost OR an explicit no-data marker.
- [ ] Every card cites a named source with a year tag.
- [ ] Per-card "Interrogate →" opens a modal with the populated prompt and a copy-to-clipboard button.
- [ ] Modal shows the amber thinking-mode hint above the prompt textarea.
- [ ] Prompt template contains both the `// Reasoning` block and instruction 11 on cost-effectiveness.
- [ ] Standalone prompt builder accepts free-text and produces the same template via the same modal.
- [ ] Header menu shows "Evidence Toolkit" between "The WISE Framework" and "AI or human?".
- [ ] Evidence Toolkit hub eyebrow reads "Evidence Toolkit · The S in WISE" and lede links to /wise/.
- [ ] /wise/ page's "S — Select the right tool" blocks (both Teacher and School Leader) include a back-link sentence to /evidence/.
- [ ] Effect-size pills are colour-banded using the muted earth-tone calibration palette, with thresholds applied to both months and Cohen's d.
- [ ] Disclaimer above cards includes point 7 explaining that colour bands are calibration, not value.
- [ ] Cards are present in the static HTML (pre-rendered from JSON at build time) so the page is readable and SEO-indexable without JavaScript.
- [ ] All English copy reads cleanly in choosewise.education's existing voice.
