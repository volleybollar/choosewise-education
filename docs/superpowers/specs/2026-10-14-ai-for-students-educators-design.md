# Elevguiden: samma ämne, uttalad läsare — educators på engelska

**Status:** utkast 2026-10-14, väntar Johans godkännande. Nästa steg efter godkännande
är en implementationsplan.
**Gäller:** den sista av de fyra guiderna i serien. Copilot var pilot (PR #38, mergad
2026-10-11), Gemini levererad 2026-10-13, Apple Intelligence 2026-10-14 inklusive
ägarens redaktionella pass och omklassificeringen. **Copilot-rundan är fortfarande
mallen för arbetsgången, men inte för arbetets innehåll** — se §3 och §6.

---

## 1. Vad som ska levereras, och vad som inte ska det

> **AMENDEMANG 2026-10-14, före planen.** Ett värde i specen är fel och rättas här; specen
> står i övrigt oförändrad som bindande auktoritet.
>
> | specen säger | mätt | varför specen hade fel |
> |---|---|---|
> | guiden är **16 sidor** (§1 rad 57, §2:s ytkarta, §3:s stoppvillkor, §6:s omfång, §7:s TOC-resonemang) | **22 renderade sidor** | `grep -c 'class="page"'` ger 16, men räknar varken omslaget eller de fyra `class="page part-divider"`-sidorna. Källan har 20 page-divar plus omslag = 21, och en div spiller till två renderade sidor. **Talet som räknas är PDF:ens, mätt med `pdftotext` och formfeed.** |
> | stoppvillkoret *"ingen sida under 400 tecken utom omslaget"* (§3) | **undantar omslaget OCH de fyra avdelningssidorna** | tre avdelningssidor ligger redan under gränsen i dag — s7 257 tecken, s13 237, s17 184 — och är korta med avsikt. Villkoret som det stod hade varit rött från första sekunden. |
>
> **Sidkartan, mätt ur den renderade PDF:en 2026-10-14** (tecken per sida med kollapsade
> blanktecken, aldrig borttagna):
>
> | sida | innehåll | tkn |
> |---|---|---|
> | 1 | omslaget | 281 |
> | 2 | Introduction — "The question isn't technical" | 2432 |
> | 3 | **Part 1-avdelare** — "Learning is the point" | 712 |
> | 4 | "If the tool elevates learning" — **OECD *Unlocking High-Quality Teaching*** | 1774 |
> | 5 | WISE-ramverket | 1740 |
> | 6 | "Challenging thinking, or replacing it" — **Wang & Fan, Kosmyna, Lee** | 2320 |
> | 7 | **Part 2-avdelare** | 257 |
> | 8 | "Teacher knowledge isn't a bonus" — **UNESCO-ramverket** | 1521 |
> | 9 | källkritik, bias, hallucinationer | 1784 |
> | 10 | "Teachers don't need to know the tech better" | 1696 |
> | 11 | **GDPR och AI Act** | 2483 |
> | 12 | **GDPR i praktiken / motsvarande regler annorstädes** | 1099 |
> | 13 | **Part 3-avdelare** | 237 |
> | 14 | 1:1-eran — **PISA 2015, Carter 2017, Zheng 2016, Unos Uno** | 2575 |
> | 15 | **The visibility gap** — hela produktlandskapet | 2402 |
> | 16 | klassrumshantering | 1688 |
> | 17 | **Part 4-avdelare** | 184 |
> | 18 | checklistan: pedagogik, förutsättningar | 951 |
> | 19 | checklistan: tillsyn, uppföljning | 1330 |
> | 20 | FAQ, första halvan | 2270 |
> | 21 | FAQ, andra halvan — **AI Act-svaret, DPIA-svaret** | 2140 |
> | 22 | slutcitatet och licensbandet | 730 |
>
> **Forskningscitaten sitter på fyra sidor (4, 6, 8, 14), produktlandskapet på en (15), och
> läsaretiketten `teachers and school leaders` står på EN plats: omslaget.** Det är mätt, och
> det gör rundan mindre än specen antog.


**Leveransen är EN PDF på engelska**, avsedd för Skool-communityt:

- `_unpublished/assets/pdfs/guides/ai-for-students-en.pdf` (16 sidor i dag)

**Ingen quick-start. Johans beslut 2026-10-14.** De fyra andra guiderna har en; den
här ska inte ha det. Tre följder, skrivna ut så att ingen uppgift bygger en ändå:

- guidens leveranspost i `GUIDE_DELIVERY` bär **en** PDF, inte två;
- det finns **inget sidantalspåstående** att vakta, och alltså ingen post i
  `NO_PAGE_CLAIM` — den dicten är tom och ska förbli det (se Apple-sektionen i
  överlämningen: rör den inte);
- förbudslistan läser **en** PDF, vilket gör varje förbjuden sträng billigare att mäta
  och svårare att missa.

**Ingenting publiceras på choosewise.education i den här rundan.** Samma ram som de
tre föregående: guiden stannar i `_unpublished/`, som Pages inte serverar. Inga poster
i `guides-en.json`, ingen `PAIR_MAP`, ingen sitemap, inga og-kort.

**De svenska ytorna fryses. Johans beslut 2026-10-14.** Samma hantering som Apples
svenska guideytor: `_unpublished/exports/ai-for-elever-print-a4-sv.html` och
`_unpublished/assets/pdfs/guides/ai-for-elever-sv.pdf` ska komma ut **byte-identiska**,
får ingen påståendeinventering och ingen vaktrad, och ingen uppgift rättar dem. Att
engelskt och svenskt därmed divergerar i sak är ett **beslutat** läge, inte en
upptäckt — och det ska stå i överlämningen när rundan är klar.

**Målgruppen är `educators` med engelska som språk. Johans beslut 2026-10-14.** Inte
elever. Ämnet är fortfarande elevernas AI-användning i klassrummet; det är **läsaren**
som är beslutad. Design och innehåll ska anpassas efter den läsaren.

---

## 2. Utgångsläget, mätt 2026-10-14 och inte antaget

| Yta | Skick |
|---|---|
| `_unpublished/exports/ai-for-students-print-a4-en.html` | 635 rader, **16 sidor** (`class="page"`-räkning). Använder **redan** `exports/_guide-print.css` och har ett Blueprint-omslag med eyebrow, titel, underrubrik, byline |
| `_unpublished/guides/ai-for-students/index.html` | 486 rader. Bär **Crestioras typsnitt**: ett Google Fonts-`<link>` med `Playfair Display` + `Inter` på rad 34 |
| `_unpublished/exports/ai-for-elever-print-a4-sv.html` | fryst, rörs inte |

**Fyra mätta förutsättningar, och tre av dem är arbete:**

1. **Guiden är REDAN skriven till läraren.** Rubrikerna är "Should students use AI in
   class?", "GDPR and the EU AI Act — what teachers need to know", "Teacher knowledge
   isn't a bonus — it's a prerequisite", "Teachers don't need to know the tech better
   than students", "Checklist: Should students use AI in this lesson?". Omslagets
   underrubrik säger redan *"for teachers and school leaders"*. **Namnet "elevguiden"
   är intern kortform och vilseleder** — `ai-for-students` beskriver ämnet, inte
   läsaren. En plan som utgår från "skriv om från elev till lärare" planerar fel
   arbete; se §3.
2. **Printlayouten är redan Blueprint. Webbytan är inte det.** Skulden är ensidig och
   ligger på webbytan: typsnitten ovan. Det är den **enda** guide-webbytan under
   `_unpublished/guides/` som fortfarande bär dem, och skälet till att den står utanför
   `test_fonts.GUIDE_WEB_SURFACES`.
3. **Båda engelska ytorna bär `Updated April 2026`** — printytan två gånger (en i
   sidfoten), webbytan en gång. Samma klass som Apples A13 och Geminis datumstämpel.
4. **Webbytan lovar en nedladdning som inte finns.** CTA-blocket säger *"Download the
   portable PDF — same content, premium layout, perfect for offline reading or for
   sharing with colleagues"* och knappen är en `<button>Download the guide (PDF)</button>`
   **utan href och utan handler**. Exakt samma felklass som Apples struckna *"download
   the 25-page premium PDF from the same page"*, och den hör på förbudslistan när den
   är borta.

**En ytdivergens finns redan innan rundan börjar:** printytan bär rubriken *"GDPR in
practice (EU) / equivalent data protection rules elsewhere"*, webbytan saknar den.
Rundan ska mäta divergensen i sin helhet, inte anta att den är den enda.

### Vad guiden står i och vad den står utanför

| Karta | Läge |
|---|---|
| `pdf_fingerprint.UNPUBLISHED_GUIDE_PDFS` | **inne** — båda PDF:erna |
| `pdf_body_text` dokumentkarta | **inne** — båda PDF:erna |
| `test_guide_pdf_font_weights` | **inne** — båda PDF:erna |
| `test_build_scripts` / `test_guide_asset_paths` | **inne** — `build-ai-for-elever-pdf.py` |
| `surfacecheck.GUIDE_SURFACES` | **utanför** |
| `factinventory.INVENTORIES` | **utanför** — `docs/guide-facts-ai-for-students.md` finns inte |
| `GUIDE_DELIVERY` (förbudslistan) | **utanför** |
| `GUIDE_TOC` | **utanför** — guiden har ingen innehållsförteckning |
| `test_fonts.GUIDE_WEB_SURFACES` | **utanför** — se punkt 2 |
| `UNMAPPED_GUIDE_SURFACES` | **enda posten** — se §7 |

### Vad som INTE är ett problem här

- **Inga nationella referenser.** `Sweden`, `Swedish`, `Skolverket` och `IMY` ger noll
  träffar på båda engelska ytorna. Internationaliseringen som kostade tre rundor på de
  andra guiderna är i allt väsentligt redan gjord i den här.
- **AI Act-avsnittet är redan jurisdiktionsramat** — *"If you are in the EU … If you
  are outside the EU"*, med FERPA, delstatsregler och UK GDPR nämnda. Ramen står; det
  är **sakinnehållet** inuti den som ska mätas (§6, klass 3).
- **Printlayouten.** Rörs inte, annat än där §4 ändrar omslagets text.

---

## 3. Vald väg: rundan skärper läsaren, den byter den inte

Beslutet "educators" ska inte läsas som ett läsarbyte. Det är en **precisering** av en
läsare guiden redan har, och skillnaden avgör rundans storlek.

Vad "anpassad till educators med engelska som språk" betyder konkret, och det är tre
krav som går att mäta:

1. **Läsaren ska vara samma person hela vägen.** Varje passage som talar till någon
   annan än en educator — till eleven, till "skolan" som abstraktion, eller till en
   svensk läsare med svensk kontext — mäts fram och skrivs om. **Mätningen görs innan
   något skrivs**, och varje förekomst får en rad i inventeringens ytkolumn.
2. **Ordet `educators` ska bära läsartilltalet där ett ord behövs**, i stället för
   `teachers and school leaders`. Samma avvikelse som Gemini-guiden redan gör
   medvetet, och av samma skäl: sajtens underrubrik är *AI & Digitalization for
   Educators*.
3. **Ingen passage får förutsätta svensk skolkontext.** Mätt: det finns ingen i dag.
   Kravet står kvar som en vakt mot att rundan själv inför en när den skriver om.

**Vad rundan inte ska göra:** inte skriva om guidens pedagogiska tes, inte byta
WISE-ramverket, inte flytta kapitel, och inte bygga ut guiden. Sidantalet 16 är ett
**stoppvillkor**, inte ett mål: rundans rättelser får göra guiden längre bara där en
källa kräver fler ord, och en sida får inte hamna under 400 tecken utom omslaget.

---

## 4. Titeln och omslaget

**Johans beslut 2026-10-14: titeln får avvika från systerguidernas, därför att den här
guiden är annorlunda.** Specens förslag, att godkännas med specen:

- **Titeln behålls som en fråga:** `Should students use AI in class?` En fråga är
  guidens hela tes — svaret är "det beror på, och det är ditt beslut" — och den är en
  bättre hook än en målgruppsetikett. Systerguidernas `… for teachers and school
  leaders` följs alltså inte, och det är avsiktligt.
- **Läsaren namnges i underrubriken**, där den redan står: `for teachers and school
  leaders` → `for educators`, i linje med §3 krav 2.
- **Eyebrow `Pedagogical decision guide` står kvar.** Den säger vad dokumentet är och
  gör titelns fråga läsbar som en guide och inte som en blogpost.

Byline och licensband rörs inte. Datumstämpeln ersätts enligt §6.

---

## 5. Ytor

| Yta | Roll |
|---|---|
| `_unpublished/exports/ai-for-students-print-a4-en.html` | källan till PDF:en — den egentliga leveransen |
| `_unpublished/guides/ai-for-students/index.html` | webbsidan, publiceras inte men ingår |
| `_unpublished/exports/ai-for-elever-print-a4-sv.html` | **fryst**, byte-identisk ut |

Webbsidan ingår fast den inte publiceras, av samma skäl som i de tre föregående
rundorna: lämnas den orörd divergerar den från print med varje faktarättning, och nästa
gång någon tar upp guiden för publicering är de två osynkade på exakt de meningar som
var känsligast. Den har dessutom två egna fel som bara finns där — typsnitten och den
döda nedladdningsknappen.

---

## 6. Inventeringen — `docs/guide-facts-ai-for-students.md`

Formen ärvs från `docs/guide-facts-apple-intelligence.md`, som är den mest utvecklade:
en post per volatilt påstående, förekomster per yta, källa med hämtdatum, verdikt ur
taxonomin, plus vaktblocket med `aktiv`/`borttaget`-rader. **Taxonomin ärvs som den
står efter omklassificeringen 2026-10-14, `struket` inkluderat.**

Båda reglerna ärvs utan undantag:

1. **En faktamening utan post i inventeringen får inte skrivas.**
2. **Ett fynd som inte behöver ändras stryks aldrig tyst** — det står kvar i tabellen
   med en motivering.

**Den här guidens volatilitet ligger INTE i produktnamn.** Den ligger i tre klasser,
och den första har redan fällt en syskonguide.

### Klass 1 — forskningscitaten. Nio namngivna, och de är guidens bärande belägg

| # | Citat som det står i guiden | Vad som måste verifieras |
|---|---|---|
| 1 | OECD, *Unlocking High-Quality Teaching*, april 2025 | att rapporten finns, dess månad, **"150 classrooms across 40 countries"**, och det ordagranna citatet |
| 2 | Wang & Fan, *Computers & Education*, 2025 meta-analys, **69 studier** | tidskrift, år, antalet studier, och att slutsatsen är den guiden drar |
| 3 | Kosmyna et al., MIT Media Lab 2025, EEG | **"up to 55 percent lower brain connectivity"** — talet, måttet och förbehållet |
| 4 | Lee et al., Microsoft Research, CHI 2025, **319 knowledge workers** | antalet deltagare och slutsatsens riktning |
| 5 | UNESCO, *AI Competency Framework for Teachers*, 2024 | titel och år |
| 6 | OECD PISA, *Students, Computers and Learning*, 2015 | titeln, året, och att "digital paradox" är rapportens fynd och inte en sekundärkällas etikett |
| 7 | Carter, Greenberg & Walker, 2017, RCT vid US Military Academy | **`0.18 standard deviations`** — talet, måttet och riktningen |
| 8 | Zheng et al., *Review of Educational Research*, 2016 | tidskrift, år, och villkoret ("bara där lärare integrerade pedagogiskt") |
| 9 | Grönlund et al., Örebro, Unos Uno 2011–2014, **~20 skolor i 11 kommuner** | talen, åren, och slutsatserna guiden hänger på |

**Tre regler för klassen, och de är inte förhandlingsbara:**

- **Primärkällan är studien eller rapporten själv**, hämtad och läst samma dag — inte
  en sammanfattning, inte en nyhetsartikel om den, inte ett pressmeddelande.
- **Varje siffra läses ordagrant ur källan.** `55 percent`, `69 studies`, `319`, `150
  classrooms across 40 countries`, `11 municipalities` — ett tal som inte går att läsa
  ur primärkällan **tas bort**, det skrivs inte om till ett annat tal.
- **Ett citat kontrolleras mot sin egen källa.** Gemini-rundan citerade Matt Miller
  ordagrant; citatet fanns inte, och lösningen blev att **ta bort attributionen, inte
  skriva om den**. Samma utfall gäller här: en studie som inte går att belägga lämnar
  guiden, och påståendet den bar får stå på egna ben eller falla.

**Klass 1 är också den enda platsen där den här guiden kan ta skada i en annan riktning
än de andra fyra.** En felaktig inställningsväg kostar läsaren en minut. En uppfunnen
studie i en guide som säljs till skolledare kostar guidens auktoritet, och Johans.

### Klass 2 — produktlandskapet i "The visibility gap"

Avsnittet bär sex påståenden om marknaden, alla från april 2026:

- *"The largest chatbots in K-12 classrooms today are Gemini (Google) and ChatGPT
  (OpenAI)"* — en marknadsandelsutsaga utan källa;
- *"Copilot is built on ChatGPT"* — var en förenkling redan då och är sannolikt fel nu;
- *"Apple Intelligence uses ChatGPT for the functions that go beyond the device"* —
  **korsref A11/A12** i Apple-inventeringen, verdikt `står`, verifierat 2026-10-14;
- *"K-12-specific products include Khanmigo, MagicSchool, and ChatGPT for Teachers"* —
  tre produktnamn, varav minst ett har bytt namn eller paketering sedan april;
- **den bärande utsagan:** *"What the majority of these tools share, according to what's
  publicly advertised, is that they do not give teachers a clear aggregated view of
  which questions students in a class have asked"* — hedgad, men hela avsnittets poäng
  vilar på den, och den är den mest sannolikt föråldrade i guiden;
- *"teachers suddenly have the instruments the 1:1 researchers were calling for back in
  2014"* — hänger på föregående.

**Rundan ärver tre färdiga inventeringar** (`guide-facts-copilot.md`,
`guide-facts-gemini.md`, `guide-facts-apple-intelligence.md`) med verifierade poster om
exakt dessa produkter. `korsref` är redan en etablerad konvention i inventeringarna och
ska användas i stället för att hämta om samma källa — men **bara för poster vars
verdikt är `står` eller `rättat`**, aldrig för en post som själv är `obelagt`.

**Faller den bärande utsagan** — om de stora verktygen i dag ger läraren en aggregerad
klassvy — så faller avsnittets slutsats, och det är ett innehållsbeslut för Johan, inte
en formulering för en uppgift. Grinden ligger där: **mät först, rapportera, invänta
beslut.**

### Klass 3 — GDPR och AI Act

Avsnittet skrevs i april 2026 och föregår allt de tre senare rundorna verifierade.
**Mät det mot de färdiga posterna**, inte mot en ny hämtning: Apple-inventeringens
A33–A39 bär AI Act:s datum, artikel 4:s AI-kunnighetsplikt (gäller sedan 2 februari
2025), artikel 16 mot artikel 26, artikel 27, och Annex III-tidpunkten **2 december
2027** efter AI Omnibus.

**Den kända felklassen, och den ska letas aktivt:** att framställa högriskskyldigheter
som bindande i dag, eller att lägga **leverantörens** förhandsplikter på skolan. Det
felet har nu fällts i tre dokument — G48 i Gemini-rundan, Geminis bonuskapitels
`pre-market obligations` (fortfarande öppet), och Apples A36/A37. Guidens mening *"Both
apply, both are the teacher's and the school authority's responsibility, and neither
can be postponed"* är precis den formulering som bär risken och ska mätas först.

### Omfång

Guiden är 16 sidor — hälften av Geminis 44 — men citattät. **Vänta 25–35 poster**, med
tyngdpunkten i klass 1 och 2. Copilots 27 är rimlig jämförelsepunkt, inte Apples 39.

---

## 7. Kodarbetet — rundan stänger ett vaktlager

**Inget nytt vaktlager ska byggas.** Allt är guide-agnostiskt sedan Copilot-, Gemini-
och Apple-rundorna. Rundan fyller fyra kartor och **river en**:

| Åtgärd | Var |
|---|---|
| fyll en rad | `surfacecheck.GUIDE_SURFACES` |
| fyll en rad | `factinventory.INVENTORIES` |
| fyll en post, **en** PDF | `GUIDE_DELIVERY` i `test_guide_delivery.py` |
| fyll webbytans sökväg | `test_fonts.GUIDE_WEB_SURFACES` |
| **töm OCH STRYK** | `UNMAPPED_GUIDE_SURFACES` i `test_guide_surface_consistency.py` |
| töm och fyll om med en PDF | `RECAPTURED_THIS_ROUND` i `test_capture_guide_baseline.py` |

**Strykningen är ett krav, inte en städning.** Listans eget huvud säger det: *"Är den
tom ska både listan och dess två vakter strykas — de vaktar ingenting då."* Elevguiden
är dess enda post. Rundan ska alltså ta bort `UNMAPPED_GUIDE_SURFACES` och de två
tester som läser den, Det är `test_every_unpublished_guide_web_surface_is_accounted_for`
(som läser listan som undantag) och `test_the_debt_list_cannot_rot` (som finns till bara
för listan) — den första skrivs om så att den mäter mot `GUIDE_SURFACES` enbart, den
andra stryks helt. **Gör det sist**, efter att ytan är inne i
`GUIDE_SURFACES` och sviten är grön, och mät insamlade test-id:n mot `main` i samma
svep — två tester försvinner, och det ska synas som avsikt och inte som ett tapp.

**Förbudslistan** får guidens egna strängar. Minst dessa, mätta på noll i den
renderade PDF:en innan de skrivs in: `Download the portable PDF`,
`Download the guide (PDF)`, `same content, premium layout`, `April 2026`. Regeln från
Apple-rundan gäller: **en lång sträng som innehåller en kort förbjuden är strikt
svagare än den korta** — ankra på det korta värdet.

**Ingen innehållsförteckning, och därmed ingen post i `GUIDE_TOC`.** Specens förslag,
att godkännas med specen: en guide på 16 sidor behöver ingen, och utan en håller rundan
programmets svåraste fälla helt utanför sig — innehållsförteckningens hårdkodade
sidnummer, som felat i två rundor och som varje ompaginering bryter. Vill Johan ha
paritet med systerguiderna i stället är det ett medvetet tillägg: då fylls `GUIDE_TOC`
med mall, PDF och **ett ankare per rad**, taget ur brödtext eller `<h3>` — aldrig ur en
spärrad etikett, eftersom `pdftotext` spärrar versaler oförutsägbart.

---

## 8. Verifiering

1. **Faktakontroll mot namngiven primärkälla**, hämtad och läst samma dag — rå HTML
   eller PDF och lokal textextraktion, aldrig en sammanfattning som källa till ett
   värde. Akademiska sidor svarar 403 eller kräver betalvägg oftare än Apples och
   Googles; **ett påstående utan hämtbar primärkälla blir `obelagt` och skrivs om utan
   siffra, eller `struket`**.
2. **Läsartilltalet mätt, inte bedömt:** varje förekomst av `teachers and school
   leaders`, `students` som tilltalad part, och varje du-tilltal, listad per yta innan
   något skrivs om.
3. **Ytkonsistensen mätt i sin helhet** — den kända divergensen (GDPR-rubriken) är
   sannolikt inte den enda.
4. **Bygg om PDF:en.** `build-ai-for-elever-pdf.py` renderar **EN och SV i samma
   körning utan språkargument**. Den svenska kopieras undan och återställs med `cp`,
   **aldrig** `git checkout --` på en katalog, och verifieras byte-identisk mot
   bascommiten innan leverans.
5. **Omfånga facit med `--only`** för exakt den engelska PDF:en. `--force` är
   liktydigt med att slå av paritetsvakten för alla 22.
6. **Titta på det renderade dokumentet.** Bilder intill ändrad text granskas var och
   en — fingeravtryck på text är blinda för bilder.
7. **Bryt varje ny vakt med flit** och se den bli röd på det den vaktar. En
   HTML-kommentar duger inte som brytning: `_TAG`-regexen slukar den.
8. **Hela sviten**, plus en genomläsning av PDF:en från pärm till pärm.

### Fällor som gäller den här rundan

- **Sviten bär elva miljöberoende fel** i `test_prompt_pdf_parity.py` så länge
  `/tmp/pdf-parity-before/` är tom — macOS tömmer den. Återskapa facit enligt testets
  egen instruktion; samma elva fallerar på `main`.
- **Mellan renderingen och facitomfångningen bär sviten två fel.** Det är inneboende.
- **Jämför insamlade test-id:n mot `main`** — den här rundan tar bort två tester med
  avsikt, och då duger inte "antalet ökade" som kontroll.
- **`/usr/bin/python3` är enda interpretern** med pytest, playwright och Pillow.
- **`git add -A` används aldrig**, och `docs/` är gitignorerad: `git add -f`.
- **Läs postradens motivering innan du skriver om meningen den beskriver.** Ägarens
  pass 2026-10-14 bröt en formulering vars skäl stod i motiveringscellen och inte i
  guiden.

---

## 9. Vad som gör rundan klar

- PDF:en byggd ur rättat innehåll, Blueprint-layout, **ingen quick-start byggd**.
- Varje volatilt påstående har en post i `docs/guide-facts-ai-for-students.md` med
  källa och hämtdatum — forskningscitaten mot primärkällan, produktpåståendena mot
  källa eller `korsref` till en syskoninventerings `står`/`rättat`-post.
- Ingen siffra i guiden som inte går att läsa ur sin primärkälla.
- Ingen uppfunnen eller obelagd attribution kvar — borttagen, inte omskriven.
- AI Act-avsnittet mätt mot A33–A39, utan leverantörsplikter lagda på skolan.
- Läsaren är en educator i varje passage, och `educators` bär läsartilltalet.
- Webbytan fri från Google Fonts och Crestiora-typsnitten, och fri från löftet om en
  nedladdning som inte finns.
- `Updated April 2026` borta från båda engelska ytorna.
- Ytkonsistensvakten grön för Claude, Copilot, Gemini, Apple **och** elevguiden.
- `UNMAPPED_GUIDE_SURFACES` **struken**, med sina två vakter, och test-id:n jämförda
  mot `main`.
- Förbudslistan bär guidens strängar, alla mätta på noll i den levererade PDF:en.
- PDF-facit omfångat med `--only`, de övriga nycklarna orörda.
- `ai-for-elever-sv.pdf` och den svenska printytan verifierat byte-identiska.
- Det frysta svenska läget och rundans beslut skrivna i överlämningen.
