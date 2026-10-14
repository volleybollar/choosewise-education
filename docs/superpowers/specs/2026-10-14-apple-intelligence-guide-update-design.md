# Apple Intelligence-guiden: aktuell mot iOS 27, vaktad, och riktad mot en engelskspråkig skolvärld

**Status:** godkänd design 2026-10-14. Nästa steg är en implementationsplan.
**Gäller:** den tredje av de fyra guiderna. Copilot var pilot (PR #38, mergad 2026-10-11),
Gemini är mallen (PR #41, mergad 2026-10-13 som `08bb8aa`). Elevguiden tas i en egen runda
efter den här.

**Rundan är delad i två leveranser med var sin PR.** Skälet står i §3.

---

## 1. Vad som ska levereras, och vad som inte ska det

**Runda 1 — mät och vakta.** Apple Intelligence-guiden kartläggs i de fyra vaktlagren, får sin
påståendeinventering, tappar Crestioras typsnitt och får sin döda adress borttagen. Guidens
prosa rörs inte. Leveransen är en omrenderad `apple-intelligence-quick-start-en.pdf` och en
inventering som säger vad i guiden som inte längre är sant.

**Runda 2 — skriv om.** Alla tre delar skrivs om mot iOS 27, inramningen blir internationell,
Del 3 får ett kort AI Act-avsnitt, och båda engelska PDF:erna renderas om.

**Ingenting publiceras på choosewise.education i någon av rundorna.** Guiden stannar i
`_unpublished/`, som GitHub Pages inte serverar. Inga poster i `guides-en.json`, ingen PAIR_MAP,
ingen sitemap, inga og-kort. Guiderna distribueras via Skool (omfångsbeslutet 2026-10-13).

**De svenska ytornas prosa rörs inte**, och de svenska PDF:erna ska komma ut byte-identiska:
`apple-intelligence-guide-sv.pdf` och `apple-intelligence-quick-start-sv.pdf`. Båda byggarna
renderar EN *och* SV i samma körning (`exports/build-apple-intelligence-pdf.py`, `jobs` rad
62–75), så de skrivs varje gång de engelska renderas om — därför står de i `untouched`.

**Undantaget från frysningen, beslutat av Johan 2026-10-14:** den svenska **webbytans** typsnitt
städas tillsammans med den engelska. Frysningen gäller prosan, inte CSS-hygienen, och ett
typsnittsbyte ändrar noll tecken normaliserad text — ytkonsistensvakten ser det inte. Följden är
att Apple blir den **första** guiden vars svenska webbyta står i `test_fonts.GUIDE_WEB_SURFACES`;
Copilots och Geminis svenska ytor bär kvar sina Crestiora-typsnitt och är fortsatt skuld.

Att engelskt och svenskt divergerar i sak efter runda 2 är ett känt läge, inte en upptäckt.

---

## 2. Utgångsläget, mätt 2026-10-14 och inte antaget

`main` = `fae8983`, rent arbetsträd, inga öppna PR:ar, en worktree. Sviten:
**808 passed / 0 failed / 0 skipped / 0 xfailed / 0 xpassed**
med `scripts/tests/test_prompt_pdf_parity.py` undantagen, mätt 2026-10-14 med `/usr/bin/python3`
(enda interpretern med pytest, playwright och Pillow). Den filens **11 fel är miljöberoende och
inte rundans**: dess facit ligger i `/tmp/pdf-parity-before/`, ett maskinlokalt scratch-facit som
macOS tömmer — katalogen fanns inte vid mätningen. Rundorna rör noll prompt-PDF:er. Att testet
faller rött i stället för att skippa högljutt när facit saknas är en känd, egen liten skuld och
hör inte till den här specen.

**Fyra ytor finns, alla under `_unpublished/`:**

| | sökväg |
|---|---|
| EN web | `_unpublished/guides/apple-intelligence/index.html` |
| EN print | `_unpublished/exports/apple-intelligence-print-a4-en.html` |
| SV web | `_unpublished/sv/guider/apple-intelligence/index.html` |
| SV print | `_unpublished/exports/apple-intelligence-print-a4-sv.html` |

**Levererat i dag:** `apple-intelligence-guide-en.pdf` 25 sidor, `-quick-start-en.pdf` 2 sidor,
plus de två svenska. Innehållet är 6 492 ord på engelska, stämplat **April 2026**.

**Apple är kartlagd i noll av fyra vaktlager.** `surfacecheck.GUIDE_SURFACES` har `claude`,
`copilot`, `gemini`. `factinventory.INVENTORIES` har samma tre. `test_guide_toc.GUIDE_TOC` har
`copilot` och `gemini`. `test_guide_delivery.GUIDE_DELIVERY` har `copilot` och `gemini`.

**Skuldlistan namnger inventeringsfilen.** `UNMAPPED_GUIDE_SURFACES` i
`test_guide_surface_consistency.py` väntar sig `docs/guide-facts-apple-intelligence.md` — alltså
med guidenyckeln `apple-intelligence`, inte `apple`. Posten stryks i samma commit som
kartläggningen: `test_the_debt_list_cannot_rot` är röd om en yta står både på listan och i
kartan.

**Och en andra lista måste fyllas samtidigt:** `UNPUBLISHED_GUIDES = ("copilot", "gemini")` i
samma fil jämförs med **set-likhet** mot en mängd som härleds ur ytkartan. Läggs Apple bara i
kartan blir `test_every_unpublished_guide_is_in_the_surface_map` röd. Detta är inte en skuld att
stryka utan en lista att fylla — motsatt riktning mot `UNMAPPED_GUIDE_SURFACES`, i samma fil.

**Typsnitten är en mindre skuld än överlämningen antyder.** Båda webbytorna använder redan
`var(--font-display)` / `var(--font-body)` / `var(--font-mono)` genomgående — de 16
`font-family`-raderna är alltså tokenanvändning, inte Crestiora. Crestiora kommer in på exakt
**sex rader per yta**: tre `<link>` i `index.html` (två preconnects + Google Fonts-arket med
`Playfair+Display` och `Inter`) och **två `--font-*`-överskrivningar** högst upp i `styles.css`
(rad 23–24) som skuggar `tokens.css`. `--font-mono` är neutral och rörs inte.

**Noll inline-`font-family` i SVG** — Geminis dyraste typsnittslager (17 attribut som vinner över
varje token och syns i ingen CSS-vakt) finns inte här. Städningen är därför: stryk de tre
länkarna och de två överskrivningarna, så ärver ytan `tokens.css` precis som den städade
Gemini-ytan gör (`_unpublished/guides/gemini-notebook/index.html` rad 31–35 bär bara de fem
lokala arken).

**Innehållsförteckningen har systerguidernas form** — `toc__title` / `toc__sub` / `toc__page`,
fem rader, sidorna 3, 9, 19, 24, 25. Den går att kartlägga rakt av.

### Fem ankare i `test_guide_toc.py` är spröda, inte fyra

Överlämningen namnger fyra. Mätningen ger fem, alla i samma riskklass — ett ankare som bär
produktnamn, pris eller datum bryts av nästa runda som rör just det:

| guide · rad | ankare | bär |
|---|---|---|
| gemini · Part 1 | `If you have never opened Gemini or Gemini Notebook, start here` | produktnamn |
| gemini · Part 2 | `returning to Gemini or Gemini Notebook for the same kind of task` | produktnamn |
| gemini · Part 4 | `Many schools run Google Workspace for Education` | produktnamn |
| gemini · FAQ | `Is the free tier enough?` | pris |
| **copilot · About this guide** | `Johan Lindström, October 2026` | **datum** |

Den femte stod inte i överlämningen. Den bryts av varje runda som sätter om Copilot-guidens
datumstämpel, och den ligger i den fil Apple-rundan kopierar som mall.

### Den döda adressen är två pekare, inte en

Överlämningen säger att Apple har "halva problemet": underrubriken är ren (verifierat — rad 93
säger `iPad-first, privacy-aware, takes 10 minutes to learn.`, ingen adress). Men avslutningen
bär **två** pekare till en sida som aldrig kommer att finnas:

```
rad 194:  <div class="msg">Want depth? Read the full <em>Apple Intelligence Guide</em> —
          or download the 25-page premium PDF from the same page.</div>
rad 195:  <div class="url">choosewise.education / guides / apple-intelligence</div>
```

`från samma sida` är en pekare i prosa och faller inte bort med `<div class="url">`. Båda ska
bort.

### Vad innehållet säger, och vad verkligheten säger

Guiden är skriven i april 2026 och bär **noll OS-versionsnummer** — inget `iOS`-nummer, inget
`iPadOS`-nummer på 6 492 ord. Det såg ut som ett hållbarhetsval. Det var det inte: guiden
beskriver en arkitektur som iOS 27 har bytt ut.

| guiden säger | leden som motsäger den |
|---|---|
| `Siri 2.0`, på separat releasespår | Siri heter **Siri AI**, egen app, släppt med iOS 27 |
| ChatGPT är den **enda** externa vägen (39 omnämnanden) | **Extensions** låter användaren välja ChatGPT, Claude eller Gemini |
| `the single place the privacy story breaks — the ChatGPT integration` | förvalet är Google-byggt; `OpenAI is a US-based processor` är inte längre guidens sanning |
| `As of April 2026` om hårdvarukraven | iOS 27 släpptes 14 september 2026 |
| 14 × `Swedish`, IMY-stycket, svensk språkstatus i FAQ | systerguiderna är omriktade internationellt |
| noll `AI Act` | Claude- och Gemini-guiderna bär den med korrekta värden |

**Leden ovan är leads, inte fakta specen välsignar.** De kommer ur websökningar
2026-10-14 mot sekundärkällor (MacRumors, Digital Trends, Qz, Business Standard). Varje påstående
verifieras mot **primärkälla** (apple.com, support.apple.com, Apples pressmaterial) i runda 1:s
inventering, med datum och länk per post. Gemini-rundans dyraste lärdom gäller här: *när du
flyttar en plikt eller ett faktum från en part till en annan, kontrollera båda ändarna.*

---

## 3. Vald väg: två rundor, inte en gren

Gemini-rundan var en gren med 78 commits som blandade vakter, research, omskrivning och
omrendering. Den gick i mål, men mergen blev en utredning i sig, och innehållets grind krävde
tre fixrundor.

Rundorna har olika natur. Infrastrukturen är **verifierbar av tester**: en karta är rätt eller
röd. Innehållet är **redaktionellt**: det kräver Johans läsning och kan inte automatiseras till
grönt. Delar vi dem får runda 1 mergas samma dag den är klar, och runda 2 börjar från ett `main`
där varje steg i omskrivningen är bevakat.

**Avvisade alternativ:** *innehållet först, vakterna sist* — det är exakt tillståndet som lät
Gemini-byggarens sidfot bära ett pensionerat produktnamn på 43 av 44 sidor genom hela rundan,
eftersom sidfoten sitter i Python och varje vakt läste HTML. *Allt i en gren* — se ovan.

---

## 4. Runda 1 — mät och vakta

### 4.1 Tre förberedelser, före kopieringen av vaktfilen

1. **Ankarna av-sprödas.** De fem raderna i tabellen i §2 byts till strängar utan produktnamn,
   pris eller datum, verifierade mot `pdftotext`-utskriften av respektive levererad PDF. Varje
   nytt ankare ska träffa **först** på den sida avsnittet faktiskt börjar på.
2. **Sentinelen byts.** `test_an_unknown_guide_is_a_loud_error` (rad 133–138) anropar
   `config_for("apple-intelligence")` — nästa guides eget namn, i den fil rundan ska kopiera.
   Den går sönder i samma stund Apple kartläggs. Byts till ett namn som aldrig kan bli en guide,
   och assertionen vänds mot `config_for`:s kända nycklar i stället för de två hårdkodade
   strängarna `"copilot"` och `"gemini"`.
3. **Typsnitten ur båda webbytorna.** Tre `<link>`-rader i `index.html` och två
   `--font-*`-överskrivningar i `styles.css` stryks per yta; ytan ärver då Blueprint ur
   `tokens.css`. Därefter läggs **fyra** sökvägar till i `test_fonts.GUIDE_WEB_SURFACES`
   (`index.html` + `styles.css` × två språk). Vakten letar efter Crestiora-strängar, så den är
   grön först när både länkarna och överskrivningarna är borta.

### 4.2 Kartläggningen — fyra vaktlager, fem filändringar, inga vaktändringar

> **AMENDEMANG 2026-10-14, efter körningen.** Rubrikens sista led, "inga vaktändringar", höll
> inte. Rundan ändrade **fyra** redan existerande guide-breda vaktfunktioner och lade **tre**
> nya deklarationer till, båda som kontrollerns rulingar på plandefekter som kartläggningen av
> Apples guide avslöjade. Specen står i övrigt oförändrad som bindande auktoritet.
>
> De fyra ändrade vaktfunktionerna, uppräknade så att talet går att kontrollera utan att läsa
> commit-diffar:
>
> 1. `test_every_guides_guard_block_is_not_empty` (c6f41f3)
> 2. `test_the_real_forbidden_list_would_catch_a_reintroduction` (c6f41f3)
> 3. `test_every_quick_starts_page_count_claim_matches_its_rendered_main_guide` (ae35fef, mönstret skärpt)
> 4. `test_the_swedish_gemini_pdfs_are_untouched_since_the_merge_base` → omdöpt och generaliserad
>    från Gemini-enbart till alla guider som `test_the_untouched_pdfs_are_byte_identical_to_the_merge_base`
>    (fixrundan dec0377..a14286f)
>
> Talet fyra är omräknat i en granskning av de faktiska commit-diffarna, inte bara påstått.
>
> | § 4.2 säger | levererat | beslut |
> |---|---|---|
> | inga vaktändringar | **Task 5A (`c6f41f3`):** `test_every_guides_guard_block_is_not_empty` och `test_the_real_forbidden_list_would_catch_a_reintroduction` ändrade; ny deklaration `MEASURE_ONLY_INVENTORIES` med ruttnandevakt | **Controllern:** Apples inventering är per design en mätning — alla kartlagda rader `aktiv`, noll `borttaget`. De två vakterna krävde minst en `borttaget`-rad per kartlagd guide, vilket hade tvingat fram en påhittad rad som påstår att en sträng strukits ur Apples prosa — något ingenting i runda 1 gör. Valt i stället: en deklarerad `MEASURE_ONLY_INVENTORIES` i husets form (skäl per post), plus en ruttnandevakt som asserterar att guiden står på listan, så en guide som tappar sina förbudsrader utan att vara deklarerad förblir röd. |
> | inga vaktändringar | **Task 7A (`ae35fef`, fixrunda `dec0377..a14286f`):** sidantalsmönstret i `test_every_quick_starts_page_count_claim_matches_its_rendered_main_guide` skärpt; ny deklaration `NO_PAGE_CLAIM` med ruttnandevakt, senare kompletterad med `BARE_PAGE_NUMBERS` och en byte-identitetsvakt generaliserad från Gemini till alla guider | **Controllern:** vakten plockade quick-startens första `\d+-page` var den än stod, och tog `Summarise a 5-page curriculum PDF` för ett påstående om guiden sedan Task 3 tagit bort guidens enda äkta sidantalspåstående. Valt: ett skärpt mönster som bara räknar ett påstående OM GUIDEN, plus `NO_PAGE_CLAIM` med ruttnandevakt. Omgranskningen fann att ruttnandevakten delade mönster med vakten den vaktade; fixrundan lade `BARE_PAGE_NUMBERS` och generaliserade byte-identitetsvakten. |
>
> Rulingarna i sin helhet, inklusive de avvisade alternativen, står i rundans ledger:
> `.superpowers/sdd/2026-10-14-apple-intelligence-round-1/progress.md`, under *"Task 5+6+7 —
> de tre återstående kartorna, batchade"*.

| lager | fil | vad som läggs till |
|---|---|---|
| ytkartan | `scripts/tests/surfacecheck.py` | `"apple-intelligence"` med fyra ytor, med kommentar om varför de svenska står med fast rundan inte rör dem |
| opublicerad-listan | `test_guide_surface_consistency.py` | `"apple-intelligence"` i `UNPUBLISHED_GUIDES`, och posten **struken** ur `UNMAPPED_GUIDE_SURFACES` |
| inventeringen | `scripts/tests/factinventory.py` | `"apple-intelligence": ROOT / "docs" / "guide-facts-apple-intelligence.md"` |
| TOC-kartan | `test_guide_toc.py` | fem rader med mall, PDF, `toc_page: 2` och fem ankare utan produktnamn, pris eller datum |
| leveransvakten | `test_guide_delivery.py` | Apples **egen** förbudslista och `untouched` med de två svenska PDF:erna |

**Förbudslistan i runda 1 får bara innehålla strängar som den levererade PDF:en redan är fri
från.** Guiden bär i dag `Swedish`, `IMY` och `April 2026` legitimt — de är sanna påståenden om
en guide som ännu inte är omskriven. Att förbjuda dem nu vore att göra billigaste vägen till
grönt att stryka innehåll, vilket är en vakt som styr innehållet i stället för att vakta det.
Internationaliseringens förbud läggs in i **runda 2**, vid omrenderingen, enligt
`XFAIL_UNTIL_RERENDERED`-konventionen.

### 4.3 Inventeringen är rundans egentliga leverans

`docs/guide-facts-apple-intelligence.md` skrivs som en **mätning av dagens guide**, inte som en
bokföring av den kommande. Varje påstående får id, språk, värde, **primärkälla med datum** och
ett verdikt:

- **står** — verifierat sant 2026-10-14
- **föråldrat** — var sant i april, är inte längre det
- **falskt** — var fel redan då

Vaktblocket (```guard-blocket som `factinventory.load()` läser) bär posterna med status `aktiv`
eller `borttaget` enligt modulens befintliga form. Prosan omkring bär verdikten och källorna.

Det gör runda 1:s grind till en **fel-lista Johan kan styra runda 2 med**. Gemini-rundan hittade
sju fel som specen inte förutsåg; här hittas de innan planen för omskrivningen skrivs.

### 4.4 Den döda adressen

Båda pekarna i §2 tas bort ur `apple-intelligence-quick-start-en.html`: ingen URL, ingen
platshållare, och prosan säger att guiden följer med i communityt. Den svenska quick-starten
rörs inte. EN-quick-starten renderas om; de svenska PDF:erna ska komma ut byte-identiska.

### 4.5 Vad som gör runda 1 klar

- Sviten grön i en **orörd utcheckning** av grenens HEAD, inte i arbetsträdet.
- Varje ny vaktrad **bevisad röd** genom att brytas med flit i en engångsworktree, och grön igen
  när den lagas. En vakt som aldrig setts röd är ett påstående.
- `apple-intelligence` i fyra kartor, struken ur skuldlistan, tillagd i `UNPUBLISHED_GUIDES`.
- Fyra nya sökvägar i `test_fonts.GUIDE_WEB_SURFACES`; noll Crestiora-strängar i båda ytorna.
- `docs/guide-facts-apple-intelligence.md` finns, med verdikt och primärkälla per post.
- `apple-intelligence-quick-start-en.pdf` omrenderad utan båda pekarna; de två svenska PDF:erna
  byte-identiska mot merge-basen.
- Filsvep över grenen: bara `_unpublished/`, `docs/`, `scripts/` och `exports/` ändrade.

---

## 5. Runda 2 — skriv om

Planen skrivs när runda 1 är mergad och inventeringen säger vad som faktiskt är fel. Designen
nedan är bindande; ordningen inuti är planens sak.

**Del 1** byggs om kring iOS 27:s krav och de tre bearbetningsvägarna i sin nya form: on-device,
Private Cloud Compute, och **vald** extern leverantör via Extensions. Hårdvarutabellen
verifieras mot Apples egna systemkrav, inte mot aprilversionen.

**Del 2** prövar sina sex funktioner mot iOS 27. Siri-appen, visual intelligence och cross-app
actions är kandidater; vilka sex som blir kvar avgörs av inventeringen och av vad en lärare
faktiskt har nytta av på en vecka. Klassrumsexemplen internationaliseras.

**Del 3** byggs om så att integritetsanalysen handlar om **leverantörsvalet** i stället för om
OpenAI som undantaget, och får ett **kort AI Act-avsnitt** som ärver Gemini-rundans källbelagda
allokering: driftsättarens art. 26-plikter (instruktionerna, mänsklig tillsyn, de loggar skolan
**styr**, information till personal och berörda), art. 27:s konsekvensbedömning, riskbenämningarna
`Unacceptable risk` / `Transparency risk` / `Minimal or no risk`, och bilaga III-högrisk för
utbildning **2 dec 2027**. De fem policybesluten skrivs om mot den nya bilden.

**FAQ** internationaliseras; språkfrågan besvaras generellt för icke-engelska språk.

**Inramningen:** IMY-stycket, `Swedish schools`, 1:1-formuleringen och omslagets
`in a Swedish school context` ut. `Siri 2.0` ut överallt. Datumstämpeln sätts om på omslaget och
i avslutningen.

**Omrenderingen stänger rundan:** sidantal, TOC-nummer, quick-startens tryckta
`25-page`-påstående (vaktat av `test_every_quick_starts_page_count_claim_matches_its_rendered_main_guide`),
förbudslistan fylls på först när PDF:en är ren, och `XFAIL_UNTIL_RECOUNTED` och
`XFAIL_UNTIL_RERENDERED` **töms** — de fylls aldrig över en rundas slut.

**Johans redaktionella pass är sista grinden**, som Gemini Task 18–20.

**Stoppvillkor för omfånget:** guiden får växa, men varje tillägg mäter sidan **före** det
skriver. Lärdomen från Gemini: luften på sidan 28 var 9,5 mm, och ett stycke till hade flyttat
TOC:ns sista nummer utan att någon märkte det förrän omrenderingen.

---

## 6. Fällor som gäller de här rundorna

1. **Pröva aldrig en vakt genom att sabotera arbetsträdet du sedan mäter i.** En `cp`-återställning
   som inte biter ger en laddad modul med sabotaget kvar och ett `git status` som säger rent.
   Använd en engångsworktree.
2. **`pdf_body_text.PLAYWRIGHT_FOOTERS` är handkopierad** ur byggarnas `jobs`-listor. Apple bär
   `footer_template`, alltså text som ingen ytvakt läser — samma lucka som lät Geminis sidfot bära
   ett pensionerat namn på 43 sidor. Sidfotens strängar läses manuellt vid omskrivningen.
3. **Ett preexisterande fel är ett påstående om `main`, och `main` rör sig.** Kör `git fetch`
   innan något kallas preexisterande.
4. **GitHubs `mergeable` kan ljuga.** Mät om lokalt i en engångsworktree innan en konflikt tros på.
5. **Grönt av fel skäl är programmets vanligaste vaktfel** — sex instanser hittills, alla hittade
   genom att bryta vakten. En vakt som bryts av att systemet växer som avsett (en sentinel med
   nästa guides namn) blir avstängd, inte lagad.

---

## 7. Utanför omfånget

- Publicering av någon Apple-yta på choosewise.education.
- De svenska ytornas **prosa**, i båda rundorna.
- Copilots och Geminis svenska webbytor, som bär kvar Crestiora-typsnitt (egen skuld, egen runda).
- Elevguiden (`ai-for-students`), som står kvar på skuldlistan med sitt eget skäl.
- Att härleda `PLAYWRIGHT_FOOTERS` live ur byggarna — tvärgående refaktorering, egen uppgift.
