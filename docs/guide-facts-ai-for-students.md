# Påståendeinventering — ai-for-students-guiden (educators-rundan)

**Rundan:** elevguiden görs om till en guide för engelskspråkiga educators — samma ämne
(elevers AI-användning i klassrummet), uttalad läsare. Task 1 av 16 (denna fil) är
rundans arbetsorder: ingen senare uppgift skriver en mening i guiden förrän den finns.
Spec: `docs/superpowers/specs/2026-10-14-ai-for-students-educators-design.md`, inklusive
§1-amendemanget (sidantalet är 22 sidor, inte 16 — specens eget tal var fel, mätt ur
`pdftotext` med formfeed, inte ur `grep -c 'class="page"'`).
**Upprättad:** 2026-10-14
**Faktakontrollerad:** inte ännu. Denna fil är skelettet — Task 2–5 fyller källkolumnen
och verdikten (forskningscitaten mot primärkälla, produktlandskapet mot källa eller
korsref, regleringen mot Apple-inventeringens A33–A39).

Ytorna: **EW** `_unpublished/guides/ai-for-students/index.html` · **EP**
`_unpublished/exports/ai-for-students-print-a4-en.html`.

**Tre skillnader mot syskoninventeringarna (Claude, Copilot, Gemini, Apple Intelligence),
och de står här med avsikt:**

1. **Ingen QS-kolumn.** Guiden har ingen quick-start och ingen ska byggas — Johans beslut
   2026-10-14 (specen §1). De fyra syskonguiderna har en kolumn för den ytan; den här
   inventeringen har bara EW och EP.
2. **De svenska ytorna är frysta och har inga poster.** `ai-for-elever-print-a4-sv.html`
   och `ai-for-elever-sv.pdf` ska komma ut byte-identiska med sina nuvarande versioner —
   Johans beslut 2026-10-14. Att engelskt och svenskt därmed divergerar i sak är beslutat,
   inte upptäckt, och ingen uppgift rättar den svenska ytan.
3. **Ingen innehållsförteckning finns**, så ingen post kan hänga på ett TOC-nummer.
   Specen föreslår att det ska förbli så (§7) — en guide på 22 sidor behöver ingen, och
   en TOC med hårdkodade sidnummer är programmets svåraste fälla vid ompaginering.

## Sidkartan (ärvd från specens §1-amendemang, mätt 2026-10-14)

Mätt ur den renderade PDF:en med `pdftotext`, tecken per sida, blanktecken kollapsade
men aldrig borttagna. Detta är rundans referens för ompaginering — Task 14 mäter mot
den.

| sida | innehåll | tkn |
|---|---|---|
| 1 | omslaget | 281 |
| 2 | Introduction — "The question isn't technical" | 2432 |
| 3 | **Part 1-avdelare** — "Learning is the point" | 712 |
| 4 | "If the tool elevates learning" — **OECD *Unlocking High-Quality Teaching*** | 1774 |
| 5 | WISE-ramverket | 1740 |
| 6 | "Challenging thinking, or replacing it" — **Wang & Fan, Kosmyna, Lee** | 2320 |
| 7 | **Part 2-avdelare** | 257 |
| 8 | "Teacher knowledge isn't a bonus" — **UNESCO-ramverket** | 1521 |
| 9 | källkritik, bias, hallucinationer | 1784 |
| 10 | "Teachers don't need to know the tech better" | 1696 |
| 11 | **GDPR och AI Act** | 2483 |
| 12 | **GDPR i praktiken / motsvarande regler annorstädes** | 1099 |
| 13 | **Part 3-avdelare** | 237 |
| 14 | 1:1-eran — **PISA 2015, Carter 2017, Zheng 2016, Unos Uno** | 2575 |
| 15 | **The visibility gap** — hela produktlandskapet | 2402 |
| 16 | klassrumshantering | 1688 |
| 17 | **Part 4-avdelare** | 184 |
| 18 | checklistan: pedagogik, förutsättningar | 951 |
| 19 | checklistan: tillsyn, uppföljning | 1330 |
| 20 | FAQ, första halvan | 2270 |
| 21 | FAQ, andra halvan — **AI Act-svaret, DPIA-svaret** | 2140 |
| 22 | slutcitatet och licensbandet | 730 |

Forskningscitaten sitter på fyra sidor (4, 6, 8, 14), produktlandskapet på en (15), och
läsaretiketten `teachers and school leaders` står på EN plats i PDF:ens sidkarta:
omslaget. Stoppvillkoret är **ingen sida under 400 tecken utom omslaget och de fyra
avdelningssidorna** (s3, s7, s13, s17 — korta med avsikt).

## Verdikttaxonomin (ärvd från Apple-inventeringen efter omklassificeringen 2026-10-14)

- `står` — verifierat sant mot primärkälla; ingen ändring behövs
- `föråldrat` — var sant i april 2026 (guidens egen datumstämpel), är det inte längre
- `falskt` — var fel redan då
- `obelagt` — ingen hämtbar primärkälla säger något om påståendet
- `rättat` — ett tidigare `föråldrat`- eller `falskt`-värde är ersatt med ett nytt,
  källbelagt värde
- `struket` — ett `obelagt` påstående är struket **utan ersättning**: inget nytt
  källbelagt värde finns att peka på, så posten blir inte `rättat`
- `lagt till` — guiden saknade påståendet helt; det är tillagt i den här rundan

**Ingen post i den här filen bär ännu något av dessa ord.** Verdiktkolumnen är tom på
alla rader — det är Task 2–5:s jobb, inte Task 1:s. En tom cell här betyder "inte
klassificerad än", inte "står".

## Två regler, ärvda ordagrant

1. **En faktamening utan post i inventeringen får inte skrivas.**
2. **Ett fynd som inte behöver ändras stryks aldrig tyst** — det står kvar i tabellen
   med en motivering.

## En tredje regel, den här rundans egen (granskningsfokus 3)

**Ett `aktiv`-ankare är det kortaste värde som bär påståendet — ett tal, ett namn, en
tidskriftstitel — aldrig hela satsen.** På `borttaget`-sidan gäller motsatsen: en lång
sträng som innehåller en kort förbjuden är strikt svagare än den korta, eftersom en
återinföring träffar den korta först. Den här regeln styr vilket värde en framtida
`aktiv`/`borttaget`-rad ska bära när Task 2–7 fyller vaktblocket — den styr inte
måttkolumnerna nedan, som mäter exakt den sträng brevets steg 1 angav.

## Poster

Förekomstkolumnerna (EW, EP) är mätta 2026-10-14 med rå `grep -c` mot källfilerna,
enligt brevets steg 1 — inte mot en normaliserare, eftersom ingen sådan ännu finns
inkopplad för den här guiden (`surfacecheck.GUIDE_SURFACES` fylls av en senare uppgift,
se spec §7). Källkolumnen lämnas tom på varje rad — Task 2–5 fyller den. Samtliga 26
kandidater nedan har minst en förekomst på båda ytorna; ingen kandidat föll bort som
`saknas_på_en_yta` (0 på en yta) i mätningen.

**En kandidat utöver brevets 25 är tillagd här** — se "Omslaget och läsartilltalet" är
inte den; se noten under Produktlandskapet (S21). Det är en avvikelse från "mät exakt
de 25 strängarna" och den är markerad som osäker i rapporten.

### Omslaget och läsartilltalet

Två kandidater som inte är forskningscitat, produktpåståenden eller reglering — de
hör till §2 punkt 3 (datumstämpeln, samma klass som Apples A13) och §3 (läsartilltalet,
som rundan ska skärpa till `educators`). De får ett eget block i stället för att tvingas
in i någon av de tre klasserna från spec §6, eftersom ingen av dem passar där.

| id | påstående i guiden | EW | EP | primärkälla + hämtdatum | verdikt |
|---|---|---|---|---|---|
| S01 | `teachers and school leaders` — läsaretiketten. På EP står den en gång, i omslagets underrubrik ("for teachers and school leaders who want to choose tools with judgement, not hype"). På EW står den tre gånger: `og:description`, `<p class="lede">` (samma formulering som EP:s underrubrik) och en tredje gång i ett stycke om WISE-ramverkets egna "separate versions for teachers and school leaders" — den tredje förekomsten talar om WISE-ramverket, inte om den här guidens läsare, och är en annan sorts påstående trots den identiska strängen. |  3 |  1 |  |  |
| S02 | `Updated April 2026` — datumstämpeln. EP bär den två gånger (omslagets fot, radens `<span>Updated April 2026</span>`, och avslutningssidans sidfot `Johan Lindström · choosewise.education · Updated April 2026`). EW bär den en gång (`<p class="cta-fineprint">Updated April 2026.</p>`). |  1 |  2 |  |  |

### Forskningscitaten (spec §6 klass 1) — nio citat, sexton ankare

Primärkällan är studien eller rapporten själv, hämtad och läst samma dag — aldrig en
sammanfattning eller ett pressmeddelande om den. Ett tal som inte går att läsa ur
primärkällan tas bort, det skrivs inte om till ett annat tal. Ett citat som inte går att
belägga mot sin egen källa lämnar guiden; attributionen tas bort, den skrivs inte om.

| id | påstående i guiden | EW | EP | primärkälla + hämtdatum | verdikt |
|---|---|---|---|---|---|
| S03 | `Unlocking High-Quality Teaching` — OECD-rapportens titel, april 2025, citerad med nyckelfyndet om lärarkvalitet |  1 |  1 | oecd.org/en/publications/unlocking-high-quality-teaching_f5b82176-en.html → **403** direkt (OECD blockerar bot-UA); Wayback-capture 2026-10-09 → **200**, ordagrant 2026-10-14: "In an era defined by rapid innovation and constant change, it is tempting to focus on the latest trends or technologies that promise transformative change. However, refining existing teaching practices by closely examining the current realities of classrooms can be a powerful – and even potentially safer – approach to addressing stagnating student achievement, as seen across PISA participating countries." Publicerad **3 april 2025**. Rapportens egen slutsats, ordagrant: "no other factor within schools has a greater impact on students' academic success and overall achievement than the quality of teaching." | **står.** Titeln, utgivningsmånaden (april 2025) och det långa citatet är ordagrant belagda — guidens citat är en trogen men tyst avkortad delmängd av källans mening (källan fortsätter ", as seen across PISA participating countries" efter "stagnating student achievement"; ingen ordskillnad i den del som faktiskt citeras, ingen ellips markerar klippet). Slutsatsen att inget skolinternt påverkar elevresultat mer än undervisningens kvalitet är rapportens egen formulering, inte guidens tolkning. Se **S04** för talen 150/40, som INTE står som skrivna. |
| S04 | `150 classrooms` — OECD-rapportens urval, ordagrant "150 classrooms across 40 countries" |  1 |  1 | Samma sida som S03 (Wayback-capture 2026-10-09) → **200**, ordagrant 2026-10-14: "It also has built on the qualitative insights of more than 150 schools from 40 countries to better understand the complex realities of implementing these practices in day-to-day teaching." Källan skriver **150 skolor** i 40 länder, inte "150 classrooms across 40 countries" som guiden skriver. | **falskt.** Talen 150 och 40 är rätt, men enheten är fel: rapporten är grundad på **150 skolor**, inte 150 klassrum — "schools" och "classrooms" är inte utbytbara i en rapport som själv handlar om skillnaden mellan skolnivå och lektionsnivå. Det är exakt den farliga klassen fynd: ett tal som ser rätt ut men bär fel ord. |
| S05 | `Wang &amp; Fan` — meta-analysens författarnamn, *Computers &amp; Education*, 2025 |  1 |  1 | nature.com/articles/s41599-025-04787-y → **200** (hämtad med webbläsar-UA; samma URL gav 403 mot ett vanligt verktygsanrop), ordagrant 2026-10-14: sidans egen rubrik bär nu prefixet "RETRACTED ARTICLE:"; sidans metadata anger tidskriften som "humanities and social sciences communications", volym 12(1); brödtexten: "This article was retracted on 22 April 2026." nature.com/articles/s41599-026-07310-z (Retraction Note) → **200**, ordagrant: "The Editor has decided to retract this article due to concerns relating to discrepancies in the meta-analysis. ... Taken together, the identified issues undermine the Editor's confidence in the validity of the analysis and the conclusions drawn from it. The authors have not responded to correspondence regarding this retraction." | **falskt.** Författarnamnen Wang & Fan stämmer, men tidskriften gör inte — artikeln stod i *Humanities and Social Sciences Communications*, inte i *Computers & Education*, som aldrig har publicerat den. Allvarligare: artikeln är **indragen (retracted) 2026-04-22**, av redaktören själv, på grund av "discrepancies in the meta-analysis" som undergräver förtroendet för analysen och dess slutsatser — författarna har inte svarat på förfrågan. Att hänga ett guide-stycke på en indragen studie är den farligaste sortens fynd i den här rundan. Se **S06** för studieantalet, också fel, och notera att guidens tredje utfall "motivation" inte är ett av metaanalysens egna tre utfallsmått (se S06-raden för detaljen). |
| S06 | `69 studies` — antalet studier i Wang &amp; Fan-metaanalysen |  1 |  1 | Samma artikel som S05 → **200**, ordagrant 2026-10-14: "This study aimed to assess the effectiveness of ChatGPT in improving students' learning performance, learning perception, and higher-order thinking through a meta-analysis of **51 research studies** published between November 2022 and February 2025." och: "Table 3 presents the 72 effects obtained from the coding of the 51 studies..." Källan skriver 51 studier (72 effektstorlekar ur dem), inte 69. | **falskt.** Metaanalysen omfattar **51 studier**, inte 69 — och artikeln är dessutom indragen (se S05): två oberoende skäl att stryka påståendet, inte bara rätta talet. Ett tredje: källans egna tre utfallsmått är "learning performance, learning perception, and higher-order thinking" — guidens tredje ord "motivation" förekommer i artikeln bara som ett delfynd i en annan, citerad understudie (Niloy et al.), inte som ett av Wang & Fan-metaanalysens egna tre mått. Guidens "performance, motivation and higher-order thinking" är alltså inte källans egna tre utfall, trots formuleringen "the three outcomes are the meta-analysis's own" som brevet bad om att kontrollera. |
| S07 | `Kosmyna` — MIT Media Lab EEG-studien (Kosmyna et al., 2025) |  1 |  1 | arxiv.org/abs/2506.08872 → **200**, ordagrant 2026-10-14: titel "Your Brain on ChatGPT: Accumulation of Cognitive Debt when Using an AI Assistant for Essay Writing Task", "by Nataliya Kosmyna and 7 other authors", inlämnad "[v1] Tue, 10 Jun 2025". Fulltexten (arxiv.org/pdf/2506.08872) märker sig själv, sidfot på varje sida: "Preprint, under review" — inte kollegialt granskad ännu. | **står** på namn, institution (MIT Media Lab, synligt i inlämningsloggens avsändaradress) och år (2025). **Förbehåll som guiden saknar, se S08:** studien är fortfarande en preprint under granskning, inte en publicerad peer review-artikel. |
| S08 | `55 percent` — "up to 55 percent lower brain connectivity" i Kosmyna et al. |  1 |  1 | arxiv.org/pdf/2506.08872 (fulltext, s. 145) → **200**, ordagrant 2026-10-14: "The LLM group showed the least extensive connectivity, with up to 55% reduced total dDTF magnitude compared to the Brain-Only group in low-frequency semantic and monitoring networks." Urval, ordagrant ur abstractet: "A total of 54 participants took part in Sessions 1-3, with 18 completing session 4." Varaktighet, ordagrant: "Over four months, LLM users consistently underperformed at neural, linguistic, and behavioral levels." | **står** på talet självt — 55 procent är exakt vad källan skriver, för måttet total dDTF-anslutning i lågfrekventa semantiska/övervakande nätverk jämfört med Brain-Only-gruppen; guidens "lower brain connectivity" är en förenkling av det måttet men ingen felaktig siffra. **Två förbehåll guiden bär utan markering:** urvalet är litet (54 deltagare i sessionerna 1–3, bara 18 i den fjärde) och studien är en preprint under granskning, inte en publicerad artikel (se S07) — guiden skriver talet som ett etablerat, oförbehållet faktum. |
| S09 | `Lee et al` — Microsoft Research-studien, CHI 2025 |  1 |  1 | microsoft.com/en-us/research/wp-content/uploads/2025/01/lee_2025_ai_critical_thinking_survey.pdf → **200** (hämtad via webbläsarläsning; samma URL 403:ar mot ett vanligt verktygsanrop), ordagrant 2026-10-14: "The definitive version was published in CHI 2025, https://doi.org/10.1145/3706598.3713778." Författare enligt samma pdf: Hana Lee m.fl. (Lee, Sarkar, Tankelevitch, Drosos, Rintel, Banks m.fl.), Microsoft Research. | **står.** Microsoft Research är avsändaren, CHI 2025 är konferensen (DOI 10.1145/3706598.3713778), och Lee är försteförfattare — guidens attribution håller. |
| S10 | `319 knowledge workers` — antalet deltagare i Lee et al. |  1 |  1 | Samma pdf som S09 → **200**, ordagrant 2026-10-14: "We survey 319 knowledge workers to investigate 1) when and how knowledge workers perceive the enaction of critical thinking when using GenAI, and 2) when and why GenAI affects their effort to do so." Nyckelfyndet, ordagrant: "confidence in GenAI is associated with less critical thinking, while higher self-confidence is associated with more critical thinking." | **står.** 319 är rätt, och riktningen i guidens påstående — hög tillit till AI går ihop med mindre kritiskt tänkande — är studiens egen slutsats, ordagrant. |
| S11 | `AI Competency Framework` — UNESCO:s ramverkstitel, 2024 (*AI Competency Framework for Teachers*) |  1 |  1 |  |  |
| S12 | `Students, Computers and Learning` — OECD PISA-rapportens titel, 2015 |  1 |  1 |  |  |
| S13 | `digital paradox` — PISA-rapportens fynd, återgivet som etikett. Att termen är rapportens egen, inte en sekundärkällas, är en av de saker som ska verifieras |  1 |  1 |  |  |
| S14 | `Carter, Greenberg` — RCT vid US Military Academy, 2017 (Carter, Greenberg & Walker) |  1 |  1 |  |  |
| S15 | `0.18 standard deviations` — effektstorleken i Carter, Greenberg & Walker |  1 |  1 |  |  |
| S16 | `Zheng et al` — meta-analysen i *Review of Educational Research*, 2016 |  1 |  1 |  |  |
| S17 | `Unos Uno` — Grönlund et al., Örebro universitet, 2011–2014 |  1 |  1 |  |  |
| S18 | `11 municipalities` — Unos Uno-studiens omfång, ordagrant "roughly 20 schools in 11 municipalities" |  1 |  1 |  |  |

### Produktlandskapet (spec §6 klass 2) — "The visibility gap"

Sex påståenden i specen, mätta som åtta kandidater eftersom ett av påståendena namnger
tre produkter var för sig och ett har en egen primärkälla redan i en syskoninventering.

| id | påstående i guiden | EW | EP | primärkälla + hämtdatum | verdikt |
|---|---|---|---|---|---|
| S19 | `largest chatbots` — "The largest chatbots in K-12 classrooms today are Gemini (Google) and ChatGPT (OpenAI)" — en marknadsandelsutsaga utan källa i guiden |  1 |  1 |  |  |
| S20 | `Copilot is built on` — "Copilot is built on ChatGPT" — var en förenkling redan i april 2026 enligt specen, sannolikt fel nu |  1 |  1 |  |  |
| S21 | `beyond the device` — "Apple Intelligence uses ChatGPT for the functions that go beyond the device". **Ankaret är kortat till denna fras** (regel 3) i stället för hela meningen. **Not om avvikelsen:** den här kandidaten stod inte i brevets steg-1-skript (de 25 angivna strängarna); den är tillagd här därför att specens §6 klass 2 räknar upp meningen som ett av sina sex påståenden och ger den redan ett korsref-svar (`Apple-inventeringens A11/A12, verdikt `står`, verifierat 2026-10-14`), och regel 1 ("en faktamening utan post får inte skrivas") gäller lika mycket för en mening brevets skript råkade utelämna. Mätt precis som övriga kandidater: `grep -c "beyond the device"` |  1 |  1 |  |  |
| S22 | `Khanmigo` — K-12-specifikt produktnamn |  1 |  1 |  |  |
| S23 | `MagicSchool` — K-12-specifikt produktnamn |  1 |  1 |  |  |
| S24 | `ChatGPT for Teachers` — K-12-specifikt produktnamn |  1 |  1 |  |  |
| S25 | `aggregated view` — den bärande utsagan: "they do not give teachers a clear aggregated view of which questions students in a class have asked". Faller den, faller avsnittets slutsats — innehållsbeslut för Johan, inte en formulering för en uppgift (spec §6) |  1 |  1 |  |  |
| S26 | `back in 2014` — "teachers suddenly have the instruments the 1:1 researchers were calling for back in 2014", hänger på S25 |  1 |  1 |  |  |

### Regleringen (spec §6 klass 3) — GDPR och AI Act

**Inga rader i den här rundan av Task 1.** Brevets steg-1-skript mätte inte mot den här
klassen — den mäts enligt specen "mot de färdiga posterna", dvs. mot Apple-inventeringens
redan verifierade A33–A39 (AI Act:s datum, artikel 4:s AI-kunnighetsplikt, artikel 16 mot
artikel 26, artikel 27, Annex III-tidpunkten 2 december 2027), inte mot en ny hämtning.
Den posten och dess korsref-rader skrivs av en senare uppgift (spec pekar mot Task 6,
som läser GDPR/AI Act-avsnittet). **Det en senare uppgift ska mäta först**, enligt
specen: meningen *"Both apply, both are the teacher's and the school authority's
responsibility, and neither can be postponed"* — samma felklass som har fällts i tre
andra dokument (Gemini G48, Geminis `pre-market obligations`, Apples A36/A37): att lägga
leverantörens förhandsplikter på skolan, eller framställa högriskskyldigheter som
bindande i dag.

Denna tomhet är **inte** regel 2:s "stryks aldrig tyst" i andra bemärkelsen — det finns
inget fynd att redovisa än, bara en känd plats där ett fynd kommer att höra hemma.

## Utfallsräkningen

**26 poster, verdikt tomt på samtliga.** Ingen klassificering är gjord i den här
uppgiften. Tabellen räknar poster per block, inte per verdikt-token, eftersom ingen
token är satt än — nästa uppgifts utfallsräkning ersätter den här med en som räknar
riktiga tokens.

| block | poster | id-spann |
|---|---|---|
| Omslaget och läsartilltalet | 2 | S01–S02 |
| Forskningscitaten (klass 1) | 16 | S03–S18 |
| Produktlandskapet (klass 2) | 8 | S19–S26 |
| Regleringen (klass 3) | 0 (ännu) | — |

Summan 2 + 16 + 8 + 0 = **26**, lika med postantalet ovan.

## Vaktblocket

```guard
# Engelska ytorna: EW `_unpublished/guides/ai-for-students/index.html` (web)
# + EP `_unpublished/exports/ai-for-students-print-a4-en.html` (print).
# Ingen QS — guiden har ingen quick-start (Johans beslut 2026-10-14). De svenska
# ytorna är frysta och ingår inte i rundan; de får aldrig en rad här.
#
# BLOCKET ÄR TOMT MED AVSIKT. Guiden står ännu inte i någon vaktkarta
# (`surfacecheck.GUIDE_SURFACES` fylls av en senare uppgift, se spec §7), och
# `test_every_guides_guard_block_is_not_empty` kräver minst en `aktiv`- och minst
# en `borttaget`-rad i samma stund guiden kommer in i kartan. Inga sådana rader
# finns förrän innehållet är rättat — att skriva in rader nu, innan Task 2–7 har
# mätt och rättat påståendena, hade gissat utfallet i stället för att mäta det.
#
# När en senare uppgift fyller blocket: varje `aktiv`-rad ska bära det KORTASTE
# värde som bär påståendet (ett tal, ett namn, en tidskriftstitel) — aldrig hela
# satsen (se regel 3 i huvudet ovan). En rad krävs ordagrant på BÅDA engelska
# ytorna för `aktiv`; en kandidat som bara träffar en yta får ingen rad, bara en
# notering i prosan (samma hantering som Apples IMY-divergens).
```

