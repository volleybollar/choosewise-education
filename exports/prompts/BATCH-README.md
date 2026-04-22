# Prompt Library — Batch pipeline

End-to-end pipeline that turns 65 source PDFs on `~/Desktop/Promptar för rebranding/`
into a choosewise.education-branded prompt library: cover-branded PDFs, landing
pages, filterable library index — all in Swedish and English.

## What's already shipped

- **Pilot for `1 Lärare`** (manually crafted, since superseded by the generator)
- **All 65 SV PDFs** rendered and placed at `/assets/pdfs/prompts/`
- **All 65 SV landing pages** under `/sv/promptar/<slug>/`
- **Swedish library index** at `/sv/promptar/` with filter pills
- **English library index** at `/prompts/` — every pack shown, non-translated ones
  in "Coming soon" state until the translation step runs

## What's NOT yet done

- **English translation** — the pipeline is built (`translate-prompts.py`) but
  needs `ANTHROPIC_API_KEY` to run. See "Next steps" below.
- **`56 AI i undervisningen`** — source folder only has a Pages template, no
  finished PDF. Get the source PDF onto disk or delete the manifest entry.
- **Megapromptar `61`, `62`, `63`** — extracted as one flat list of 15/15/13
  prompts. The original docs have a very different structure (bullets, example
  input/output, not just a flat prompt list). The pilot renders them OK as
  simple prompt lists, but you may want a custom template for richer layout.
- **Smoke test on SV pages** — I generated and rendered them but didn't
  open-and-eyeball every cover. Worth a spot-check in the browser before
  deploying.

---

## Decisions locked in the manifest

File: [`manifest.py`](manifest.py)

### Naming
| SV concept | EN label | Notes |
|---|---|---|
| `Gymnasiet` | `Upper Secondary` | OECD/EU standard term for ages 16–19 |
| `HKK` | `Home Economics` | |
| `Slöjd` | `Crafts` | |
| `IDH` (Idrott och hälsa) | `PE` (Physical Education) | |
| `SO` (Samhällsorienterande ämnen) | `Social Studies` | Umbrella term |
| `Samhällskunskap` | `Social Studies` | |
| `NO` (Naturorienterande ämnen) | `Science (General)` | |
| `Naturkunskap` | `Science` | |
| `Religion` | `Religious Studies` | |
| `Modersmål` | (skipped — SV only) | Swedish curriculum-specific |
| `Svenska` / `SVA` | (skipped — SV only) | Only taught in Sweden |
| `Läs- och skrivinlärning` | (skipped — SV only) | |

### Cover pattern
- **Eyebrow** on grundskola packs: `For <Audience>` (e.g. `For Teachers`)
- **Eyebrow** on gymnasium packs: `For Teachers · Ages 16–19` (age included so
  international audiences understand)
- **Title**: `Prompts for <Subject> Teachers · Upper Secondary.` for gymnasium
- **Vol. number** = pack's position in `PACKS` (1–66) — gives the library a
  numbered-collection feel

### Branding (applied to every PDF)
- **Removed**: Johan Lindström's name on cover, `@Aland72` / Mastodon / X refs
- **Kept and amplified**: LinkedIn CTA on back cover ("Follow Johan Lindström
  on LinkedIn for new prompts, guides and reflections on AI in education")
- **Added**: `choosewise.education` top-left on cover, full CTA stack on back
  cover linking to `/prompts/`, `/wise/`, LinkedIn

### Categories (filter pills on library index)
- **Classroom teachers** (5) — Lärare, Lär dig nya saker, Förskola, Förskoleklass,
  Förstelärare, IKT-pedagoger
- **Subject specialists** (33) — all subject packs + gymnasium variants
- **School leaders** (3) — Rektorer, Skolchefer, Strateger
- **Support staff** (15) — Fritids, Speciallärare, Elevassistenter, SYV,
  Specialpedagoger, Sköterskor, Kuratorer, Psykologer, Vaktmästare, Måltidspersonal,
  IT-ansvariga, Bibliotekarier, Administratörer
- **Thematic** (9) — Digitala verktyg, AI i undervisningen, Ämnesövergripande,
  Utomhuspedagogik, Studier om lärande, Effektivt tidsutnyttjande, Megapromptar 1–3

---

## Pipeline

```
  source PDFs
       │  pdftotext -layout
       ▼
  extract-prompts.py ───────────► data/<slug>.json
                                       │
                                       ├── generate-html.py (SV) ──► <slug>-sv.html
                                       │
                                       ├── translate-prompts.py ──► data/<slug-en>-en.json
                                       │                                 │
                                       │                                 ▼
                                       │                          generate-html.py (EN) ──► <slug-en>-en.html
                                       │
                                       ▼
                                  generate-pages.py ──► /sv/promptar/<slug>/index.html
                                                        /prompts/<slug-en>/index.html
                                                        /sv/promptar/index.html
                                                        /prompts/index.html
                                       │
                                       ▼
                                  build-prompts-pdf.py ──► /assets/pdfs/prompts/<slug>-{sv,en}.pdf
```

Every step is **idempotent**: rerunning regenerates the same output.

---

## Files in this folder

| File | Purpose |
|---|---|
| `manifest.py` | Single source of truth: folder→slug→category→title mappings |
| `extract-prompts.py` | PDF → JSON (parses each source PDF into part/prompt structure) |
| `translate-prompts.py` | Claude API translation SV→EN, preserves bracketed placeholders |
| `generate-html.py` | JSON → branded A4-print HTML (`<slug>-sv.html`, `<slug>-en.html`) |
| `generate-pages.py` | Landing pages + library index regenerator |
| `build-prompts-pdf.py` | HTML → PDF via Playwright |
| `_prompt-print.css` | Shared CSS for all print HTMLs (cover, prompts, back page) |
| `data/*.json` | Extracted + translated pack data (one file per pack per language) |
| `<slug>-sv.html` · `<slug>-en.html` | Generated print-HTML files (input to the PDF renderer) |

---

## Next steps — to finish the English side

### 1. Install the Anthropic SDK
```bash
pip install anthropic
```

### 2. Set your API key
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Run the translator (20–30 min for all 57 translatable packs)
```bash
cd "/Users/johan/Projekt/JLSU/Ny JLSU hemsida"
python3 exports/prompts/translate-prompts.py
```

This writes `data/<slug-en>-en.json` for each translatable pack. Already-
translated packs are skipped (pass `--force` to redo them).

Expected cost: ~$3–5 total for all 57 packs on `claude-sonnet-4-6`.

### 4. Generate EN HTML files
```bash
python3 exports/prompts/generate-html.py     # regenerates both SV + EN now
```

### 5. Regenerate landing pages + library index
```bash
python3 exports/prompts/generate-pages.py
```

The EN library index will now show all translated packs as live cards (not
"Coming soon"), and each gets an individual `/prompts/<slug>/` landing page.

### 6. Render all EN PDFs
```bash
python3 exports/prompts/build-prompts-pdf.py
```

This renders every `*-en.html` (and re-renders SV for completeness).

### 7. Spot-check
Open a few random covers:
```bash
open "/Users/johan/Projekt/JLSU/Ny JLSU hemsida/assets/pdfs/prompts/physics-en.pdf"
open "/Users/johan/Projekt/JLSU/Ny JLSU hemsida/assets/pdfs/prompts/mathematics-upper-secondary-en.pdf"
open "/Users/johan/Projekt/JLSU/Ny JLSU hemsida/assets/pdfs/prompts/school-nurses-en.pdf"
```

### 8. Commit & push
```bash
cd "/Users/johan/Projekt/JLSU/Ny JLSU hemsida"
git add -u
git add prompts/ sv/promptar/ assets/pdfs/prompts/ exports/prompts/data/
git commit -m "feat(prompts): add English translations for library (57 packs)"
git push origin main
```

---

## Troubleshooting

### Extractor missed prompts in a specific pack
Check the `is_prompt()` heuristic in `extract-prompts.py`. It recognises prompts
by their opening verb (Skapa, Ge, Föreslå, …). If a pack uses an opener we
haven't seen before, add it to `IMPERATIVE_OPENERS`.

### A pack's extracted count is way off vs. cover count
Run with a single slug and inspect the JSON:
```bash
python3 exports/prompts/extract-prompts.py <slug>
cat exports/prompts/data/<slug>.json | jq '.parts[] | {title, prompts: .prompts | length}'
```

### Megapromptar render weirdly
They're flagged `special: True` in the manifest. The current renderer treats
them as simple prompt lists — which works but doesn't match the source's richer
"Create → example input/output" structure. To build a custom template, check the
source PDF:
```bash
pdftotext -layout "~/Desktop/Promptar för rebranding/Del 1-63/61 Megapromptar 1/"*.pdf | less
```

### "56 AI i undervisningen" has no PDF
Source folder only has a Pages template. Either export the finished Pages
doc to PDF and place it in the folder, or remove the pack from `manifest.py`.

---

## Pilot timing (for reference)

- Pilot (SV + EN, hand-crafted): **~15 min**
- Pipeline build: **~45 min**
- Full SV batch (extract → HTML → PDF → pages): **~50 s wall time**
- Estimated EN batch (with API): **20–30 min** (dominated by translation)

Total session wall time to get all 65 packs live in both languages (once
translation runs): **~1 hour** from this starting point.
