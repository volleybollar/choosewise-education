# Gemini-rundan: var den står när chatten tog slut

> ## ⛔ ÖVERSPELAD — HISTORIK, INTE ETT AKTUELLT LÄGE
>
> **Rundan är färdig.** Den här filen skrevs mitt i den, när kontextfönstret tog slut, och
> beskriver ett läge som inte längre finns. Den står kvar för att visa **hur** rundan
> återupptogs, inte **var** den står.
>
> **➡️ Läs `docs/blueprint-handoff.md` i stället.** Allt levande ur den här filen bor där nu:
> Johans öppna beslut, publiceringsskulden, "gör detta först i nästa runda", de fem
> lärdomarna, och de två siffror som inte ska ärvas.
>
> **Vad som hände efter att den här filen skrevs:**
> 1. Task 16:s granskning hade **redan rapporterat** innan chatten tog slut — ingen omdispatch
>    behövdes. Den godkände uppgiften.
> 2. **Task 16B** åtgärdade R7 och R8 (commit `af69689`) och lade till vaktraden för
>    quick-startens sidantalspåstående.
> 3. **Task 17** gjorde slutkontrollen och skrev överlämningen. Svit **795 passed / 1 failed**
>    (det preexisterande sidantalet), 0 skipped / 0 xfailed / 0 xpassed.
>
> Varje mening nedan som blev falsk av det är rättad **på plats**, med sin rättelse i fetstil,
> i stället för att bara motsägas här uppe. Filen ska inte säga något som inte är sant.

**Skriven 2026-10-12** när kontextfönstret tog slut mitt i rundan. **LÄS DEN HÄR FÖRST** vid fortsättning, sedan planen. — *Överspelat: läs `docs/blueprint-handoff.md` först.*

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

**Klara och granskade: Task 1, 2, 3, 4, 4B, 4C, 5, 6, 7, 8, 9, 10+11, 12, 13, 14, 15.** — **RÄTTAT: plus Task 16, 16B och 17. Alla sjutton är klara och granskade.**

~~**Task 16 (bildgranskning + genomläsning): implementerad som `1c4e30d`, granskningen DISPATCHAD MEN DESS UTFALL ÄR OKÄNT** — chatten tog slut innan den rapporterade. **Dispatcha om granskningen** mot `review-73eac3d..1c4e30d.diff`; dess brief står i ledgern.~~
**RÄTTAT: granskningen HADE rapporterat.** Den godkände uppgiften (`Task 16: complete` i ledgern). **Ingen omdispatch behövdes, och instruktionen ovan ska inte följas.**

~~**Task 17 (slutkontroll, överlämning, PR): INTE PÅBÖRJAD.** Medvetet — hellre ogjord än halvgjord.~~
**RÄTTAT: Task 16B och Task 17 är UTFÖRDA.** Task 16B åtgärdade R7/R8 och vaktade quick-startens sidtal (`af69689`); Task 17 gjorde slutkontrollen, skrev `docs/blueprint-handoff.md` och ett PR-utkast. **Grenen är inte pushad och ingen PR är öppnad** — det görs efter Johans besked.

~~**Svit:** `794 passed, 1 failed`~~ **RÄTTAT: `795 passed, 1 failed`** (Task 16B:s nya vaktrad) med `--ignore=scripts/tests/test_prompt_pdf_parity.py`. Det enda felet är `test_brand_mark.py::test_the_page_count_is_what_we_think` (199 sidor mot hårdkodat 198) — **preexisterande, kom med blogg-mergen PR #40, faller likadant på `main`, inte rundans och inte rundans att laga.** Med paritetsfilen inne tillkommer dess elva miljöberoende fel (`/tmp/pdf-parity-before/` töms av macOS).

**Leveransen:** `_unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf` (**44 sidor**) och `gemini-notebook-quick-start-en.pdf` (2 sidor). Ingenting publicerat.

## Vad rundan faktiskt rättade, utöver den planerade omriktningen

1. **Google döpte om NotebookLM till Gemini Notebook 2026-07-16** — tre månader efter guidens datumstämpel. 205 förekomster, titeln, filnamnen. Johans beslut: allt, även filnamnen.
2. **Licensomläggningen pekade åt fel håll om pengar.** Premium kräver `Google AI Pro for Education` à $15/användare/månad; guiden sa att det ingick i Education Plus.
3. **Fem fel i AI Act-kapitlet**, varav det allvarligaste sa att högriskskyldigheterna gäller sedan augusti 2026 — bilaga III-högrisk för utbildning gäller från **2 december 2027**. Guiden talade om för rektorer att de redan var bundna.
4. **Matt Miller-citatet finns inte hos Matt Miller.** Ersatt med en verifierad rad, attributionen kvar.
5. **Byggarens sidfot bar det gamla namnet på 43 av 44 sidor** — hårdkodad i Python, osynlig för varje HTML-vakt, upptäckt först när PDF:en lästes.
6. **Åtta av tio sidnummer i innehållsförteckningen var fel.** Nu `3 5 8 13 20 23 27 30 32 41`, vaktade.
7. **Quick-starten sa "40-page premium PDF" om en 44-sidig guide.**

## Genomläsningens fynd som INTE stod i överlämningen — räddade hit 2026-10-12

Granskningen av Task 16 fann att fyra fynd bara låg i `task-16-report.md`, och `.superpowers/`
är gitignorerad: de hade dött med worktreen. **Två är verifierade av granskaren som verkliga,
läsarvända och enordsstora:**

> **RÄTTAT: R7 och R8 är ÅTGÄRDADE i Task 16B, commit `af69689`.** Båda på båda engelska
> ytorna, guiden omrenderad och facit omfångat selektivt med `--only`. De står kvar nedan som
> beskrivning av vad felen var, inte som öppna fynd. **R5 och R6 är fortfarande oåtgärdade** —
> de är Johans beslut och står i `docs/blueprint-handoff.md`.

1. **R7 — fel ord i friskrivningen. ÅTGÄRDAD (`af69689`): `This chapter` → `This part`.** Den andra förekomsten, inne i bonuskapitlet, står kvar orörd eftersom "chapter" är riktigt där. `gemini-notebook-print-a4-en.html:929` säger *"I am not a
   lawyer. **This chapter** gives a starting point"* — men stycket står under `<h2>Scale &
   Lead</h2>` (rad 890), som är en **del**, inte ett kapitel. Samma friskrivning på rad 1075
   ligger inne i bonuskapitlet, där "this chapter" är riktigt. **Ett ord.**
2. **R8 — rubrik mot förteckning. ÅTGÄRDAD (`af69689`).** Rubriken på rad 1166 var *"A starter library of Gemini
   prompts"*; förteckningens underrad på rad 555 säger *"25 starter prompts for Gemini and
   Gemini Notebook"*. Promptbiblioteket täcker båda produkterna. **Rubriken säger nu "A starter
   library of Gemini and Gemini Notebook prompts", på båda ytorna.**
3. **R5** — Säfström/Folkebrant-exemplet förekommer **tre** gånger (utöver de tre duplikat som
   redan står nedan).
4. **R6** — författaren omtalas både som "Johan" och som "I" i samma dokument.

~~**Dessutom, ur granskningen:** inget vaktar quick-startens "44-page"-påstående. Numret som just
hittades fel genom läsning kan bli fel igen på exakt samma sätt, tyst. En rad räcker.~~
**RÄTTAT: vaktat sedan Task 16B.**
`test_guide_delivery.py::test_every_quick_starts_page_count_claim_matches_its_rendered_main_guide`
jämför det tryckta talet mot huvudguidens **härledda** sidantal, i stället för att hårdkoda
det. Vakten täcker Copilot också.

**Och två siffror att inte ärva:** pyramidens trängsta luft är **120 enheter**, inte ~17 —
granskaren mätte om den oberoende ur den levererade PDF:en vid 200 dpi och landade inom en halv
enhet. Och guiden växte **42 → 44** sidor denna runda, inte 38 → 44; talet 38 står fel i två
rapporter.

## Johans öppna beslut

> **Fortfarande öppna, och de står nu i `docs/blueprint-handoff.md` tillsammans med R5 och R6
> (Fristadsskolan tre gånger, och "Johan" mot "I"), som inte stod här när den här filen
> skrevs.** Besluta dem där, inte här.

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
