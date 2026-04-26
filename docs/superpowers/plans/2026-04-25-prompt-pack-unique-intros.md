# Plan: unique-per-pack intro text on prompt-pack landing pages (Option B)

**Date drafted:** 2026-04-25
**Status:** Approved approach (Option B), execution deferred
**Goal:** Escape Google's boilerplate-classification of the new ~150-word intro and give each prompt-pack page a genuine SEO + AI-citation footprint.

---

## Why Option B (unique sentence per pack), not A or C

- **Option A — only variables (`{count}`, `{audience_lower}`):** The 150-word intro becomes site-wide boilerplate. Google ignores it as main content; AI engines treat all 60 packs as "equally relevant" and cite none specifically. Net SEO/AI lift: low.
- **Option B — 1–2 unique sentences per pack inside an otherwise shared frame:** Cheap (3–4 h drafting per language). High lift — each page has a genuinely unique core that establishes its specific topical authority.
- **Option C — fully unique intro per pack:** 10–15 h drafting per language, marginal lift over B. Diminishing returns.

## The 4-paragraph hero structure

```
P1 — Lede (dynamic per pack)
  "{count} färdiga AI-chattpromptar {audience_lower} — fria att ladda ner, anpassa och dela."
  EN: "{count} ready-to-use AI chat prompts {audience_lower} — free to download, adapt, and share."

P2 — Shared bio (identical on every pack)
  SV: "Promptarna är framtagna av mig, Johan Lindström. Med en gedigen bakgrund som lärare
       vet jag vad som skiljer en allmän AI-prompt på internet från en som faktiskt fungerar
       i klassrummet. En generell prompt tar inte hänsyn till åldersgrupp, läroplan eller
       hur en lärares vardag ser ut. Det gör de här. Varje prompt är skriven med ett tydligt
       syfte — du fyller bara i hakparenteserna med din egen kontext för att få ut något
       användbart."
  EN: "The prompts are written by me, Johan Lindström. With a solid background as a teacher,
       I know what separates a generic AI prompt from one that actually works in a classroom.
       A generic prompt doesn't account for age group, curriculum, or what a teacher's day
       actually looks like. These do. Every prompt is written with a clear purpose — you just
       fill in the bracketed placeholders with your own context to get something useful out."

P3 — UNIQUE PER PACK (the work-to-do — see drafting below)
  1–2 sentences (~30–50 words) that reference what makes THIS specific pack relevant for
  THIS specific audience. Examples below.

P4 — Shared "for whom" (identical on every pack)
  SV: "Promptarna är framför allt till för dig som ännu inte är så van vid att prompta —
       du får färdiga mallar att utgå från och göra till dina egna. Är du redan en van
       AI-användare kan du använda dem som idébank, eller analysera
       <a href="/sv/promptar/megapromptar-1/">megapromptarna</a> för att se hur de är
       uppbyggda och lära dig mönstret bakom."
  EN: "The prompts are aimed mainly at those of you who aren't yet comfortable with prompting
       — you get ready-made templates to start from and adapt. If you're already an
       experienced AI user, treat them as an idea bank, or study the
       <a href="/prompts/megaprompts-1/">megaprompts</a> to see how they're built and learn
       the structure behind them."
```

## Tone and content of the unique P3 sentences

- **Empathetic + practical**, not promotional. Reference the audience's *actual* daily challenges, not abstract value props.
- 1–2 sentences, ~30–50 words.
- May briefly tie in Johan's lived experience ("Tidsbristen är något jag mött…") when natural.
- Avoid keyword-stuffing — write like a human who knows the role.

### Three sample sentences (SV) to anchor the tone

**tidsutnyttjande:**
> "Tidsbristen är något jag mött både som lärare och som skolledare. Promptarna här handlar om att vinna tillbaka timmar på rättning, planering och möten — utan att tappa kvalitet."

**rektorer:**
> "Som rektor jonglerar du beslut som spänner över pedagogik, ekonomi och personal samtidigt. Promptarna i det här paketet är skrivna för just den verkligheten — ofta i situationer där du behöver formulera dig snabbt utan att kompromissa med precisionen."

**ikt-pedagoger:**
> "IKT-pedagoger sitter ofta i skärningen mellan teknik, pedagogik och förändringsarbete. Promptarna i det här paketet stöttar både konkret klassrumsanvändning och de strategiska samtalen med kollegium och ledning."

## CSS already in place (uncommitted, supports the new structure)

```css
/* assets/css/pages.css */
.page-hero .lede + .prose,
.page-hero .prose + .prose { margin-top: var(--space-4); max-width: none; }
```

## Workflow when executing

1. **Draft 60 unique sentences per language** (Claude does first pass): walk through every pack in `exports/prompts/manifest.py`, read sample prompts in the data file to understand what the pack actually does, then draft 1–2 sentences per pack. Output as a single markdown file with one section per pack so Johan can review/edit fast.
2. **Johan reviews/edits.** He knows roles better than I do — expect ~30% rewriting.
3. **Integrate into the template.** Two options:
   - **A:** Add a `unique_intro_sv` / `unique_intro_en` field to each pack's data JSON and render in template.
   - **B:** Keep them in the manifest.py with the rest of the pack metadata.
   Recommend (B) — manifest is already where pack metadata lives and avoids touching 118 JSON files.
4. **Update `exports/prompts/generate-pages.py`** templates (lines 71 SV / 128 EN) to include the new P3 paragraph between the shared P2 and shared P4.
5. **Run `python3 exports/prompts/generate-pages.py`** — regenerates all ~118 prompt-pack landing pages.
6. **Single commit** for the manifest update + template change + regenerated pages.

## Current state (uncommitted on disk)

Two preview pages have v2 intro text already (post-Johan-feedback shortening of bio):
- `sv/promptar/tidsutnyttjande/index.html`
- `prompts/time-management/index.html`

Both currently use the **shared frame only — no unique P3** (they jump straight from P2 to P4). When executing rollout, the unique P3 will be inserted into these two pages just like the others.

The CSS rule above is also uncommitted in `assets/css/pages.css`.

## Things to confirm before drafting

- Should the unique sentence sometimes reference Johan's lived experience ("som lärare har jag…") or always stay focused on the audience? My default: lived-experience hook is OK in ~20% of packs where it adds credibility, neutral focus on the audience for the rest.
- Megaprompt link — keep `/sv/promptar/megapromptar-1/` and `/prompts/megaprompts-1/` as the link target? Or link to a megaprompt index/listing if one exists?
- Tone calibration: drafts in Swedish should run through Johan's voice DNA (skill `voice` in `~/.claude/skills/voice` if relevant). EN can be more neutral.

## Resume command when ready

> "Run Option B from the prompt-pack unique-intros plan."

I'll read this doc, draft the 60 sentences per language, hand them over for review, and execute steps 3–6 once approved.
