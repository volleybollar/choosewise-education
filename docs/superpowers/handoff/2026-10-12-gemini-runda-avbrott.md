# Gemini-rundan: var den står när chatten tog slut

**Skriven 2026-10-12** när kontextfönstret tog slut mitt i rundan. **LÄS DEN HÄR FÖRST** vid fortsättning, sedan planen.

## Var arbetet ligger

| | |
|---|---|
| Worktree | `.worktrees/gemini-guide-international` (skapad med `git worktree add`, `.worktrees/` är gitignorerad) |
| Gren | `feat/gemini-guide-international`, avstamp `main` = `e2282b7` |
| Plan | `docs/superpowers/plans/2026-10-12-gemini-guide-international.md` — **bindande, och rättad 14 gånger under rundan** |
| Spec | `docs/superpowers/specs/2026-10-12-gemini-guide-international-design.md` — mergad in i grenen från PR #39 |
| Inventering | `docs/guide-facts-gemini.md` — **50 poster**, 87 vaktrader |
| Ledger | `.superpowers/sdd/2026-10-12-gemini-guide-international/progress.md` — **varje ruling, i ordning** |
| Uppgiftsrapporter | samma katalog, `task-*-report.md` |

**Johans 31 ocommittade filer ligger i huvudkopian och har aldrig rörts.** Worktreen är isolerad.

## Läget

**Klara och granskade: Task 1, 2, 3, 4, 4B, 4C, 5, 6, 7, 8, 9, 10+11, 12, 13, 14, 15.**

**Task 16 (bildgranskning + genomläsning): implementerad som `1c4e30d`, granskningen DISPATCHAD MEN DESS UTFALL ÄR OKÄNT** — chatten tog slut innan den rapporterade. **Dispatcha om granskningen** mot `review-73eac3d..1c4e30d.diff`; dess brief står i ledgern.

**Task 17 (slutkontroll, överlämning, PR): INTE PÅBÖRJAD.** Medvetet — hellre ogjord än halvgjord.

**Svit:** `794 passed, 1 failed` med `--ignore=scripts/tests/test_prompt_pdf_parity.py`. Det enda felet är `test_brand_mark.py::test_the_page_count_is_what_we_think` (199 sidor mot hårdkodat 198) — **preexisterande, kom med blogg-mergen PR #40, faller likadant på `main`, inte rundans och inte rundans att laga.** Med paritetsfilen inne tillkommer dess elva miljöberoende fel (`/tmp/pdf-parity-before/` töms av macOS).

**Leveransen:** `_unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf` (**44 sidor**) och `gemini-notebook-quick-start-en.pdf` (2 sidor). Ingenting publicerat.

## Vad rundan faktiskt rättade, utöver den planerade omriktningen

1. **Google döpte om NotebookLM till Gemini Notebook 2026-07-16** — tre månader efter guidens datumstämpel. 205 förekomster, titeln, filnamnen. Johans beslut: allt, även filnamnen.
2. **Licensomläggningen pekade åt fel håll om pengar.** Premium kräver `Google AI Pro for Education` à $15/användare/månad; guiden sa att det ingick i Education Plus.
3. **Fem fel i AI Act-kapitlet**, varav det allvarligaste sa att högriskskyldigheterna gäller sedan augusti 2026 — bilaga III-högrisk för utbildning gäller från **2 december 2027**. Guiden talade om för rektorer att de redan var bundna.
4. **Matt Miller-citatet finns inte hos Matt Miller.** Ersatt med en verifierad rad, attributionen kvar.
5. **Byggarens sidfot bar det gamla namnet på 43 av 44 sidor** — hårdkodad i Python, osynlig för varje HTML-vakt, upptäckt först när PDF:en lästes.
6. **Åtta av tio sidnummer i innehållsförteckningen var fel.** Nu `3 5 8 13 20 23 27 30 32 41`, vaktade.
7. **Quick-starten sa "40-page premium PDF" om en 44-sidig guide.**

## Johans öppna beslut

1. **Tre passager står dubblerat** — Miller-citatet (s 6, 10), "the two sides stay complementary" (s 6, 18), Eric Curts/`edugems.ai` (tre gånger från s 14). Alla preexisterande. Avduplicering är ett redaktionellt pass på hans text.
2. **"pre-market obligations"** (bonuskapitlet): förhandsbedömningsplikterna faller på *leverantören*; en skola som driftsätter bär deployer-plikter. Preexisterande, och att rätta kräver en källa ingen verifierat.
3. **Titeln** är `Gemini & Gemini Notebook for teachers and school leaders`. Klumpig men ärlig. Omslagets eyebrow stammar: `Gemini · Gemini Notebook for education`.

## Skulden till publiceringsrundan — ETT jobb, inte fem

- `scripts/build-seo-meta.py` rad 51, 57, 75 (rad 75 är PAIR_MAP, som spec §1 förbjöd rundan att röra)
- `_unpublished/README.md` rad 26, 59, 63, 148 — rad 26:s källsökväg är **bruten**
- nio `notebooklm`-strängar i webbytans tillgångsattribut, osynliga för ytvakten
- **Och den är inte valfri:** quick-starten *trycker* `choosewise.education / guides / gemini-notebook` för läsaren, så publiceringsrundan måste använda den sökvägen.

## Gör detta FÖRST i nästa guides runda

**TOC-vaktens ankare för Del 1 och Del 2 bär produktnamnet.** Namnbytet bröt dem, lagningen satte in det nya namnet, sprödheten är återinförd. Apple Intelligence-rundan **kopierar** filen som mall. Byt till ankare utan produktnamn, pris eller datum innan dess.

Och: `pdf_body_text.py`:s `PLAYWRIGHT_FOOTERS` är handkopierad ur byggarnas `jobs`-listor i stället för härledd — exakt den inaktualitet som lät sidfoten bära det gamla namnet. Att härleda den live stänger luckan för varje `footer_template`-guide.

## Lärdomar som gäller bakåt

- **Prosa bor inte bara i HTML.** Byggskript och sidfotsmallar bär text ingen ytvakt läser.
- **En vakt som väljer nästa guides namn som sentinel går sönder när den guiden kommer.** `test_an_unknown_guide_is_a_loud_error` använde `"gemini"`; den ärvdes från Copilot-rundan.
- **För en `borttaget`-rad är en längre sträng som innehåller en kortare förbjuden strikt svagare.** På `aktiv`-sidan är det omvänt.
- **Fyra ord kan aldrig bli bara förbudsrader i den här guiden:** `Sweden`/`Swedish` (det källbelagda exemplet), `GDPR` (promptplatshållaren), `April 2026` (daterade produktpåståenden), `NotebookLM` (citerade titlar).
- **Mät sidlängder genom att KOLLAPSA blanktecken, inte ta bort dem.** Den buggen gav fel siffror två gånger.
