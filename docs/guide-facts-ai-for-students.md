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
- `struket` — **ett påstående, oavsett tidigare verdikt, struket utan ersättning:**
  inget nytt källbelagt värde finns att peka på VID DEN POSTEN, så posten blir inte
  `rättat`. Definitionen är bredare än den ursprungliga ("ett `obelagt` påstående
  struket utan ersättning") — den här rundan har satt `struket` på poster som kom
  från `falskt` (S05/S06, Wang & Fan-citatet: fel tidskrift, fel studieantal, OCH
  indraget 2026-04-22), och det är rätt i sak. Utslagsgivande är inte vilket verdikt
  posten bar innan, utan att påståendet självt är borta ur guidetexten.
  **`struket` mot `rättat`, distinktionen:** `rättat` är **samma** posts värde
  korrigerat på plats — S04 (OECD-urvalet) bär fortfarande sitt eget tal, bara
  enheten är bytt `classrooms` → `schools`. `struket` är postens påstående helt
  borttaget ur guidetexten, och en eventuell ersättning lever som en **egen post**:
  Wang & Fan-citatet (S05/S06) är struket utan ersättning VID DESSA två id:n — det
  som ersätter citatets plats i stycket är S34, Deng et al., ett annat id med sin
  egen källcell och sitt eget verdikt (`lagt till`). En post märks aldrig `rättat`
  bara därför att NÅGOT fyller tomrummet den lämnade; den märks `rättat` bara om
  DEN SJÄLVA fick ett nytt, källbelagt värde.
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
tidskriftstitel — aldrig hela satsen.** På `borttaget`-sidan gäller motsatsen, men bara
VILLKORAT: en kort sträng är ett starkare ankare än en lång ENDAST så länge varje
förekomst av den korta strängen faktiskt var felet, eftersom en återinföring annars
träffar den korta strängen först. **Undantaget:** lever den korta strängen legitimt
kvar någon annanstans — ett annat påstående, ett annat dokument den citerar — måste
ankaret i stället vara den längsta sträng som bara matchar den borttagna förekomsten;
annars slår en legitim kvarvarande förekomst ut som "återinförd" mot en mening som
aldrig skrevs om. (Se vaktblockets egen kommentar vid S01 för ett konkret fall.) Den
här regeln styr vilket värde en framtida `aktiv`/`borttaget`-rad ska bära när Task 2–7
fyller vaktblocket — den styr inte måttkolumnerna nedan, som mäter exakt den sträng
brevets steg 1 angav.

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
| S01 | `teachers and school leaders` — läsaretiketten. På EP står den en gång, i omslagets underrubrik ("for teachers and school leaders who want to choose tools with judgement, not hype"). På EW står den tre gånger: `og:description`, `<p class="lede">` (samma formulering som EP:s underrubrik) och en tredje gång i ett stycke om WISE-ramverkets egna "separate versions for teachers and school leaders" — den tredje förekomsten talar om WISE-ramverket, inte om den här guidens läsare, och är en annan sorts påstående trots den identiska strängen. |  3 |  1 |   | **rättat.** Läsaretiketten i omslagets underrubrik (EP) och dess två EW-motsvarigheter (`og:description`, `<p class="lede">`) är ändrad `teachers and school leaders` → `educators` — Johans beslut 2026-10-14 (brevets §4, Task 11). Titeln (`Should students use AI in class?`) och eyebrow:n (`Pedagogical decision guide`) är orörda. EW:s tredje förekomst (WISE-ramverkets egna "separate versions for teachers and school leaders", rad ~152) talar om ett annat dokument och är medvetet lämnad orörd — därför är vaktblockets `borttaget`-ankare för den här posten den längre, distinkta ordalydelsen ur den gamla underrubriken, inte den nakna strängen; se vaktblockets egen kommentar för undantaget från regel 3. |
| S02 | `Updated April 2026` — datumstämpeln. EP bär den två gånger (omslagets fot, radens `<span>Updated April 2026</span>`, och avslutningssidans sidfot `Johan Lindström · choosewise.education · Updated April 2026`). EW bär den en gång (`<p class="cta-fineprint">Updated April 2026.</p>`). |  1 |  2 |   | **rättat.** Stämpeln är satt om från `April 2026` till `October 2026` i samtliga tre förekomster — EP:s `cover__footer`-rad (nu `<span>October 2026</span>`, utan `Updated`) och avslutningssidans licensrad (`Johan Lindström · choosewise.education · October 2026`), EW:s cta-finprint (`Updated October 2026.`, med `Updated` kvar) — samma form som syskonguiderna copilot och apple-intelligence redan bär på sina motsvarande ytor. 2026-10-15 (leveransdagen) ligger inom oktober 2026, så stämpeln är sann vid leverans. Byggaren (`exports/build-ai-for-elever-pdf.py`) bär ingen egen datumtext i `cover_footer`/`standard_footer` — bara titel och sidnummer — så den femte ytan krävde ingen ändring. |
| S35 | Löptextens läsartilltal (sidorna 2–21), Task 6: varje `you`, `your` och `we` i löptexten, läst i sitt sammanhang, och den nakna strängen `teachers and school leaders` sökt i löptexten (skilt från S01:s omslagsetikett). Rått mätt (`grep -o -i`, hela filen, utan kontext): `you` 37 (EP) / 42 (EW), `your` 18 (EP) / 19 (EW), `we` 9 (EP) / 7 (EW). Skillnaderna kommer av redan kända ytdivergenser, inte av nya fynd: EW har tre stycken EP saknar (en extra checklistfråga om att "catch bias and hallucinations", avsnittet "Take the guide with you" och CC-licensraden), och EP har ett avslutande stycke EW saknar ("AI is the most powerful tool we've yet seen for amplifying teaching..."). Samtliga 79 `you`-förekomster (37+42) och alla `your`/`we`-förekomster är lästa i sitt sammanhang (brevets steg 2); listan finns i sin helhet i Task 6-rapporten. `teachers and school leaders` förekommer 0 gånger i EP:s löptext och 1 gång i EW:s löptext (rad ~152) — samma WISE-ramverksmening S01:s vaktrad redan skyddar. |  42 |  37 |   | **står. Läsartilltalet är mätt, inte antaget, och det höll redan.** Varje `you`/`your` i löptexten talar till läraren/skolledaren som handlande part, aldrig till en elev eller till "skolan" som en person-lös abstraktion: "before you let AI into a lesson", "the students you have", "it must be you who judges", "check with your school leadership", "your jurisdiction", "ask your data protection officer". Två typer av `you`-träffar ligger utanför den bedömningen med avsikt och är inte läsartilltal: citerade exempelprompter inom citattecken ("explain why you think the reasoning is off", riktat mot AI-modellen i ett exempelyttrande, inte mot guidens läsare) och webbytans CC-licensrad ("You may copy, share and adapt... as long as you credit...", generisk licenstext för vem som än återanvänder materialet). `we` är genomgående det inkluderande "vi" om professionen/skolväsendet ("we now have to apply it", "the school system we built", "we've seen this before") — aldrig ett "vi" som talar för en elev. Den enda löptextförekomsten av `teachers and school leaders` (EW, rad ~152) beskriver WISE-ramverkets egna lärar-/skolledarversioner, inte den här guidens läsare, och är därför medvetet lämnad orörd — samma undantag som S01:s vaktrad redan dokumenterar. **Utfall: inget att rätta.** Ingen ändring är gjord i `_unpublished/exports/ai-for-students-print-a4-en.html` eller `_unpublished/guides/ai-for-students/index.html` för den här posten; de två kända ytdivergenserna som förklarar räkneskillnaden (se måttkolumnen) rör innehåll utanför läsartilltalet och lämnas till den uppgift som äger ytparitet. |

### Forskningscitaten (spec §6 klass 1) — nio citat på printytan, ett tionde EW-exklusivt

Primärkällan är studien eller rapporten själv, hämtad och läst samma dag — aldrig en
sammanfattning eller ett pressmeddelande om den. Ett tal som inte går att läsa ur
primärkällan tas bort, det skrivs inte om till ett annat tal. Ett citat som inte går att
belägga mot sin egen källa lämnar guiden; attributionen tas bort, den skrivs inte om.

**S34 är tillagd under Task 5B (ett ägarbeslut vid rundans grind, inte en del av
ursprungsplanen)** som ersättare för S05/S06: Wang & Fan-metaanalysen är indragen
(retracted 2026-04-22) och bar redan fel tidskrift och fel studieantal, så den kunde inte
längre hänga kvar som den positiva sidan i avsnittet "Challenging thinking, or replacing
it" (sidan 6) — men ägaren beslutade att citatet skulle ERSÄTTAS, inte bara tas bort, så att
avsnittets positiva sida inte föll bort och guiden inte lutade mörkare än forskningsläget
motiverar. S34 belägger en oindragen, peer-granskad metaanalys av kontrollerade studier som
kan bära den positiva sidan i stället. **Task 7 (denna uppgift) har skrivit in den nya
meningen på båda engelska ytorna och strukit Wang & Fan-citatet helt** — S05 och S06
behåller sina källceller orörda som historisk dokumentation av felet, men deras verdikt är
nu `struket` (attributionen och talet är borta ur guiden, utan ersättning VID DESSA poster
— ersättningen lever vid S34, ett eget id utanför S03–S18-spannet).

**S36 är tillagd under Task 5C**, en uppgift som inte stod i ursprungsplanen utan
tillkom när en tidigare uppgift (Task 5B) upptäckte att EW bär en mening printytan
helt saknar, direkt efter Lee et al.-citatet i samma stycke (sidan 6, "Challenging
thinking, or replacing it"): *"A Swiss study (Gerlich 2025) found a correlation of
-0.75 between AI use and critical thinking among younger users."* Ingen av rundans
fem mätuppgifter såg den, eftersom den inte finns på printytan de alla mätte mot —
den är guidens **tionde** forskningscitat, inte ett av de nio. Eftersom den bara
träffar en yta (EW 1 / EP 0) får den ingen `aktiv`-vaktrad (regeln i vaktblockets
sista stycke, samma hantering som Apples IMY-post) — divergensen står i stället i
"Ytdivergenser" nedan.

| id | påstående i guiden | EW | EP | primärkälla + hämtdatum | verdikt |
|---|---|---|---|---|---|
| S03 | `Unlocking High-Quality Teaching` — OECD-rapportens titel, april 2025, citerad med nyckelfyndet om lärarkvalitet |  1 |  1 | oecd.org/en/publications/unlocking-high-quality-teaching_f5b82176-en.html → **403** direkt (OECD blockerar bot-UA); Wayback-capture 2026-10-09 → **200**, ordagrant 2026-10-14: "In an era defined by rapid innovation and constant change, it is tempting to focus on the latest trends or technologies that promise transformative change. However, refining existing teaching practices by closely examining the current realities of classrooms can be a powerful – and even potentially safer – approach to addressing stagnating student achievement, as seen across PISA participating countries." Publicerad **3 april 2025**. Rapportens egen slutsats, ordagrant: "no other factor within schools has a greater impact on students' academic success and overall achievement than the quality of teaching." | **står.** Titeln, utgivningsmånaden (april 2025) och det långa citatet är ordagrant belagda — guidens citat är en trogen men tyst avkortad delmängd av källans mening (källan fortsätter ", as seen across PISA participating countries" efter "stagnating student achievement"; ingen ordskillnad i den del som faktiskt citeras, ingen ellips markerar klippet). Slutsatsen att inget skolinternt påverkar elevresultat mer än undervisningens kvalitet är rapportens egen formulering, inte guidens tolkning. Se **S04** för talen 150/40, som INTE står som skrivna. |
| S04 | `150 classrooms` — OECD-rapportens urval, ordagrant "150 classrooms across 40 countries" |  1 |  1 | oecd.org/en/publications/unlocking-high-quality-teaching_f5b82176-en.html (samma sida som S03; Wayback-capture 2026-10-09) → **200**, ordagrant 2026-10-14: "It also has built on the qualitative insights of more than 150 schools from 40 countries to better understand the complex realities of implementing these practices in day-to-day teaching." Källan skriver **150 skolor** i 40 länder, inte "150 classrooms across 40 countries" som guiden skriver. | **rättat.** Talen 150 och 40 var rätta, men enheten var fel: rapporten är grundad på **150 skolor**, inte 150 klassrum — "schools" och "classrooms" är inte utbytbara i en rapport som själv handlar om skillnaden mellan skolnivå och lektionsnivå. Det var exakt den farliga klassen fynd: ett tal som ser rätt ut men bär fel ord. Guidetexten är rättad på båda engelska ytorna (EP rad ~340, EW rad ~123), 2026-10-15 (Task 7): `150 classrooms across 40 countries` → `150 schools across 40 countries`. Talen 150/40 själva var redan rätt och är orörda. |
| S05 | `Wang &amp; Fan` — meta-analysens författarnamn, *Computers &amp; Education*, 2025 |  0 |  0 | nature.com/articles/s41599-025-04787-y → **200** (hämtad med webbläsar-UA; samma URL gav 403 mot ett vanligt verktygsanrop), ordagrant 2026-10-14: sidans egen rubrik bär nu prefixet "RETRACTED ARTICLE:"; sidans metadata anger tidskriften som "humanities and social sciences communications", volym 12(1); brödtexten: "This article was retracted on 22 April 2026." nature.com/articles/s41599-026-07310-z (Retraction Note) → **200**, ordagrant: "The Editor has decided to retract this article due to concerns relating to discrepancies in the meta-analysis. ... Taken together, the identified issues undermine the Editor's confidence in the validity of the analysis and the conclusions drawn from it. The authors have not responded to correspondence regarding this retraction." | **struket.** Författarnamnen Wang & Fan stämde, men tidskriften gjorde inte — artikeln stod i *Humanities and Social Sciences Communications*, inte i *Computers & Education*, som aldrig har publicerat den. Allvarligare: artikeln är **indragen (retracted) 2026-04-22**, av redaktören själv, på grund av "discrepancies in the meta-analysis" som undergräver förtroendet för analysen och dess slutsatser — författarna har inte svarat på förfrågan. Att hänga ett guide-stycke på en indragen studie är den farligaste sortens fynd i den här rundan. Attributionen `Wang & Fan` är struken ur guidetexten på båda engelska ytorna (sidan 6), 2026-10-15 (Task 7) — utan ersättning vid DENNA post: den positiva sidan av avsnittet bärs nu av en annan, egen post, **S34**, med sin egen vaktrad. Se **S06** för studieantalet, också struket. |
| S06 | `69 studies` — antalet studier i Wang &amp; Fan-metaanalysen |  0 |  0 | nature.com/articles/s41599-025-04787-y (samma artikel som S05) → **200**, ordagrant 2026-10-14: "This study aimed to assess the effectiveness of ChatGPT in improving students' learning performance, learning perception, and higher-order thinking through a meta-analysis of **51 research studies** published between November 2022 and February 2025." och: "Table 3 presents the 72 effects obtained from the coding of the 51 studies..." Källan skriver 51 studier (72 effektstorlekar ur dem), inte 69. | **struket.** Metaanalysen omfattade **51 studier**, inte 69 — och artikeln är dessutom indragen (se S05): två oberoende skäl att stryka påståendet, inte bara rätta talet. Ett tredje: källans egna tre utfallsmått var "learning performance, learning perception, and higher-order thinking" — guidens tredje ord "motivation" förekom i artikeln bara som ett delfynd i en annan, citerad understudie (Niloy et al.), inte som ett av Wang & Fan-metaanalysens egna tre mått. Guidens "performance, motivation and higher-order thinking" var alltså inte källans egna tre utfall. Hela frasen `69 studies` och attributionen till Wang & Fan är struken ur guidetexten på båda engelska ytorna (sidan 6), 2026-10-15 (Task 7). Talet 69 lever vidare i guiden, men nu korrekt knutet till **S34** (Deng et al., som oberoende av denna sammanblandning faktiskt identifierade 69 artiklar) — se S34 för kontrollen av att det inte bara är samma fel i ny form. |
| S07 | `Kosmyna` — MIT Media Lab EEG-studien (Kosmyna et al., 2025) |  1 |  1 | arxiv.org/abs/2506.08872 → **200**, ordagrant 2026-10-14: titel "Your Brain on ChatGPT: Accumulation of Cognitive Debt when Using an AI Assistant for Essay Writing Task", "by Nataliya Kosmyna and 7 other authors", inlämnad "[v1] Tue, 10 Jun 2025". Fulltexten (arxiv.org/pdf/2506.08872) märker sig själv, sidfot på varje sida: "Preprint, under review" — inte kollegialt granskad ännu. | **står** på namn, institution (MIT Media Lab, synligt i inlämningsloggens avsändaradress) och år (2025). **Förbehåll som guiden saknar, se S08:** studien är fortfarande en preprint under granskning, inte en publicerad peer review-artikel. |
| S08 | `55 percent` — "up to 55 percent lower brain connectivity" i Kosmyna et al. |  1 |  1 | arxiv.org/pdf/2506.08872 (fulltext, s. 145) → **200**, ordagrant 2026-10-14: "The LLM group showed the least extensive connectivity, with up to 55% reduced total dDTF magnitude compared to the Brain-Only group in low-frequency semantic and monitoring networks." Urval, ordagrant ur abstractet: "A total of 54 participants took part in Sessions 1-3, with 18 completing session 4." Varaktighet, ordagrant: "Over four months, LLM users consistently underperformed at neural, linguistic, and behavioral levels." | **lagt till.** Talet självt stod redan rätt — 55 procent är exakt vad källan skriver, för måttet total dDTF-anslutning i lågfrekventa semantiska/övervakande nätverk jämfört med Brain-Only-gruppen; guidens "lower brain connectivity" är en förenkling av det måttet men ingen felaktig siffra, och talet 55 percent är orört. Men guiden saknade helt **de två förbehåll** källan bär: urvalet är litet (54 deltagare i sessionerna 1–3, bara 18 i den fjärde) och studien är en preprint under granskning, inte en publicerad artikel (se S07). Dessa två förbehåll är nu skrivna in i guidetexten på båda engelska ytorna (sidan 6), 2026-10-15 (Task 7), som en parentes direkt efter `Kosmyna et al.`: "— a preprint, not yet peer-reviewed, with 54 participants and only 18 completing the fourth session". |
| S09 | `Lee et al` — Microsoft Research-studien, CHI 2025 |  1 |  1 | microsoft.com/en-us/research/wp-content/uploads/2025/01/lee_2025_ai_critical_thinking_survey.pdf → **200** (hämtad via webbläsarläsning; samma URL 403:ar mot ett vanligt verktygsanrop), ordagrant 2026-10-14: "The definitive version was published in CHI 2025, https://doi.org/10.1145/3706598.3713778." Författare enligt samma pdf: Hana Lee m.fl. (Lee, Sarkar, Tankelevitch, Drosos, Rintel, Banks m.fl.), Microsoft Research. | **står.** Microsoft Research är avsändaren, CHI 2025 är konferensen (DOI 10.1145/3706598.3713778), och Lee är försteförfattare — guidens attribution håller. |
| S10 | `319 knowledge workers` — antalet deltagare i Lee et al. |  1 |  1 | Samma pdf som S09 → **200**, ordagrant 2026-10-14: "We survey 319 knowledge workers to investigate 1) when and how knowledge workers perceive the enaction of critical thinking when using GenAI, and 2) when and why GenAI affects their effort to do so." Nyckelfyndet, ordagrant: "confidence in GenAI is associated with less critical thinking, while higher self-confidence is associated with more critical thinking." | **står.** 319 är rätt, och riktningen i guidens påstående — hög tillit till AI går ihop med mindre kritiskt tänkande — är studiens egen slutsats, ordagrant. |
| S11 | `AI Competency Framework` — UNESCO:s ramverkstitel, 2024 (*AI Competency Framework for Teachers*) |  1 |  1 | unesco.org/en/articles/ai-competency-framework-teachers → **200**, ordagrant 2026-10-14: sidrubriken "Publication AI competency framework for teachers", publiceringsdatum direkt under rubriken: "8 August 2024" (uppdaterad "16 January 2026"). Brödtexten på samma sida återger titeln i den versalform guiden använder: "The AI Competency Framework for Teachers addresses this gap by defining the knowledge, skills, and values teachers must master in the age of AI." Citeringsraden på samma sida: "Miao, Fengchun UNESCO Cukurova, Mutlu 2024". | **står.** Titeln ("AI Competency Framework for Teachers", som den faktiskt förekommer i sidans brödtext — sidrubriken själv bär gemener, "AI competency framework for teachers", men det är samma dokument) och året (2024, publicerad 8 augusti 2024) är ordagrant belagda på UNESCO:s egen sida. **Läst mot sidan 8 i Task 8 (2026-10-15):** stycket "Teacher knowledge isn't a bonus — it's a prerequisite" skriver "In 2024 UNESCO published its *AI Competency Framework for Teachers*" — exakt titel och år, ordagrant samma som denna källcell belägger. **Ingen ändring behövde göras.** Noterat uttryckligen eftersom en post som stämmer aldrig stryks tyst (inventeringens regel 2). Not: detaljen "15 competencies across five dimensions" i samma stycke ligger utanför vad den här källcellen själv verifierade (cellen styrker bara titel, upphovsmän och år) — ingen uppgift har flaggat den som fel, men den är inte oberoende kontrollerad här heller; se rapporten. |
| S12 | `Students, Computers and Learning` — OECD PISA-rapportens titel, 2015 |  1 |  1 | oecd.org/content/dam/oecd/en/publications/reports/2015/09/students-computers-and-learning_g1g57f3a/9789264239555-en.pdf → **200**, ordagrant 2026-10-14, kolofonsidans citeringsrad: "OECD (2015), Students, Computers and Learning: Making the Connection, PISA, OECD Publishing." Förordet, ordagrant: "students who use computers very frequently at school do a lot worse in most learning outcomes, even after accounting for social background and student demographics." | **står.** Titeln och året (2015) är rapportens egna (pdfinfo bekräftar 204 sidor, samma fil). Kontrollen för socioekonomisk bakgrund är rapportens egen formulering ("social background and student demographics"), inte ett tillägg från guiden. Se **S13** för termen "digital paradox", som INTE förekommer i den här texten. |
| S13 | `digital paradox` — PISA-rapportens fynd, återgivet som etikett. Att termen är rapportens egen, inte en sekundärkällas, är en av de saker som ska verifieras |  1 |  1 | oecd.org/content/dam/oecd/en/publications/reports/2015/09/students-computers-and-learning_g1g57f3a/9789264239555-en.pdf → **200**, helfilssökning 2026-10-14: strängen "paradox" (skiftlägesokänsligt) förekommer **noll gånger** i rapportens samtliga 204 sidor (`grep -c -i paradox` på den fulla `pdftotext`-utskriften → 0). Sekundärkällor använder termen om samma fynd — t ex en substack-artikel med rubriken "The Digital Paradox: Navigating the Pushback on Classroom Technology" och spansk press ("PISA y la paradoja digital", El Heraldo de México) — men ingen av dem är OECD självt. | **står.** Guiden hedgar redan korrekt: "what became known as the 'digital paradox'" påstår inte att OECD myntade termen, bara att fyndet senare fick den etiketten av andra — och det stämmer, rapporten använder aldrig ordet. Hedgen "became known as" räcker för att skilja fyndet (rapportens eget, se S12) från etiketten (en sekundärkällas). |
| S14 | `Carter, Greenberg` — RCT vid US Military Academy, 2017 (Carter, Greenberg & Walker) |  1 |  1 | doi.org/10.1016/j.econedurev.2016.12.005 → omdirigerar till sciencedirect.com/science/article/abs/pii/S0272775716303454 → **403** direkt (Elsevier blockerar bot-UA, samma mönster som OECD/Nature/Microsoft i Task 2; ingen Wayback-capture finns för den sidan, kontrollerat mot `archive.org/wayback/available`). Läst i stället via en kurssajts spegling av exakt samma publicerade artikel-PDF (people.it.tamu.edu/~w-arthur/302/Payne et al (2017) Economics of Educ Review...pdf), vars sidhuvud och artikelhistorik bekräftar att det är den publicerade versionen, inte arbetspappret: "Economics of Education Review 56 (2017) 118–132 ... The impact of computer usage on academic performance: Evidence from a randomized trial at the United States Military Academy ... Susan Payne Carter, Kyle Greenberg∗, Michael S. Walker ... Published by Elsevier Ltd." samt "Received 5 July 2016, Revised 8 December 2016, Accepted 9 December 2016, Available online 14 December 2016" → **200** (ordagrant 2026-10-14). | **står.** Författarnamnen, institutionen (United States Military Academy) och designen — "a study that prohibited computer devices in randomly selected classrooms of an introductory economics course" — är ordagrant belagda i den publicerade artikeln. Se **S15** för effektstorleken och utfallsmåttet. |
| S15 | `0.18 standard deviations` — effektstorleken i Carter, Greenberg & Walker |  1 |  1 | doi.org/10.1016/j.econedurev.2016.12.005 → omdirigerar till sciencedirect.com/science/article/abs/pii/S0272775716303454 → **403** direkt (samma blockering som S14; ingen Wayback-capture finns för sidan). Läst via samma kurssajts-spegling som S14 (people.it.tamu.edu/~w-arthur/302/Payne et al (2017) Economics of Educ Review...pdf) → **200**, ordagrant 2026-10-14, abstractet: "Average final exam scores among students assigned to classrooms that allowed computers were 0.18 standard deviations lower than exam scores of students in classrooms that prohibited computers." Kontrollerat mot arbetspappret (Blueprint Labs Discussion Paper #2016.02, maj 2016, blueprintcdn.com): dess abstract bär SAMMA tal, "18 percent of a standard deviation lower" — den siffra som skiljer sig inom arbetspappret (0.21, en okontrollerad delskattning i Tabell 3 kolumn 1, mot 0.18, den fullt kontrollerade skattningen i kolumn 4: "remains statistically significant at -0.18σ") finns inom samma dokument, inte mellan arbetspapper och publicerad version. | **står.** 0.18 standardavvikelser är exakt det publicerade abstractets eget tal, för utfallsmåttet "final exam scores" (det sammansatta provresultatet), i en design med slumpmässig tilldelning av datoranvändning per klassrum. Brevets varnade felklass (olika tal i arbetspapper kontra publicerad artikel) kontrollerades uttryckligen och inträffade inte här — båda versionerna landar på 0.18 som sin huvudsiffra. |
| S16 | `Zheng et al` — meta-analysen i *Review of Educational Research*, 2016 |  1 |  1 | journals.sagepub.com/doi/10.3102/0034654316628645 → **403** direkt (Cloudflare-utmaning mot botanrop). Wayback-capture 2026-05-05 (web.archive.org/web/20260505071154/https://journals.sagepub.com/doi/abs/10.3102/0034654316628645) → **200**, ordagrant 2026-10-14 — men visar bara abstractet bakom en uttrycklig betalvägg-markering, "Get full access to this article": "Over the past decade, the number of one-to-one laptop programs in schools has steadily increased. ... A meta-analysis of 10 studies examines the impact of laptop programs on students' academic achievement, finding significantly positive average effect sizes in English, writing, mathematics, and science." Tidskrift/volym/år bekräftat separat i ERIC:s förlagslämnade abstract (eric.ed.gov/?id=EJ1121563 → **200**, 2026-10-14): "Review of Educational Research, v86 n4 p1052-1084 Dec 2016." Fulltexten är obelagd trots sökning: OpenAlex (api.openalex.org/works/doi:10.3102/0034654316628645) → "is_oa": false, "any_repository_has_fulltext": false; Unpaywall → "oa_status": "closed"; ResearchGate och HKU Scholars Hub svarade **403**; oa.mg hade ingen PDF. Det enda ställe villkorsformuleringen faktiskt hittades var ett UCI-pressmeddelande/ScienceDaily-referat (sciencedaily.com/releases/2016/04/160426110655.htm): "can improve educational outcomes when there is teacher buy-in, suitable technical support and professional development for teachers, and appropriate implementation with the curriculum." | **struket.** Var `obelagt` för villkoret: tidskrift (*Review of Educational Research*), volym/sidor (86(4):1052–1084) och år (2016) stod belagda mot det hämtbara abstractet, men villkoret guiden hängde halva sitt argument på — "positive effects existed, but only where teachers integrated the devices pedagogically" — uttalades inte i abstractet, och fulltexten är overifierbar bakom en betalvägg utan laglig gratiskopia (se sökningen i källcellen). Den enda formulering som fångar villkoret är ett pressmeddelande/referat, och brevets regel diskvalificerar uttryckligen en sammanfattning eller ett pressmeddelande som belägg för en primärkälla. **Ägarens beslut vid rundans grind (2026-10-15), genomfört av Task 9:** hela citatet, inte bara villkoret, är struket ur guidetexten på båda engelska ytorna (sidan 14) — utan ersättning vid DENNA post. Skälet: att behålla citatet utan villkoret hade gjort påståendet starkare i FEL riktning, eftersom det enda verifierade i källan (källcellen ovan) är att metaanalysen fann POSITIVA effekter i engelska, skrivande, matematik och naturvetenskap — motsatsen till vad stycket använde citatet till. Stycket bygger en kedja ("the research record is clear and internationally consistent"); borttagningen är läst mot hela stycket, inte bara mot meningen, och de tre kvarvarande citaten på samma sida — PISA 2015 (S03/S12/S13), Carter, Greenberg & Walker 2017 (S14/S15) och Unos Uno (S17/S18), alla `står` — bär kedjan ensamma, i samma riktning, utan Zhengs hedge. Se Task 9-rapporten för hela stycket citerat efter borttagningen. |
| S17 | `Unos Uno` — Grönlund et al., Örebro universitet, 2011–2014 |  1 |  1 | diva-portal.org/smash/get/diva2:706366/FULLTEXT01.pdf (Grönlund, Åke. *Att förändra skolan med teknik: Bortom "en dator per elev"*, Örebro universitet, 2014, ISBN 978-91-7668-992-9) → **200**, ordagrant 2026-10-14, förordet: "Den här boken bygger på erfarenheterna från projektet Unos Uno som under åren 2011–2013 arbetat systematiskt med att utveckla skolan med hjälp av informations- och kommunikationsteknik (it). Ett tjugotal skolor i elva kommuner och en friskolekoncern har deltagit." Tryckår enligt kolofonsidan: 2014. | **står.** Grönlund och Örebro universitet är rapportens egna uppgifter; projektperioden 2011–2013 plus utgivningsåret 2014 täcker guidens "2011–2014" utan motsägelse. **Medveten anmärkning enligt brevet:** källan är svensk (Örebro universitet, DiVA), men guiden ramar den som "the most cited Nordic longitudinal study" — en internationellt citerbar beskrivning som inte kräver svensk läsarkontext. Posten står kvar av det skälet; den ska INTE strykas som en nationell referens i en senare runda. |
| S18 | `11 municipalities` — Unos Uno-studiens omfång, ordagrant "roughly 20 schools in 11 municipalities" |  1 |  1 | diva-portal.org/smash/get/diva2:706366/FULLTEXT01.pdf (Grönlund, Åke. *Att förändra skolan med teknik: Bortom "en dator per elev"*, Örebro universitet, 2014) → **200**, ordagrant 2026-10-14. Omfånget, samma mening som S17: "Ett tjugotal skolor i elva kommuner och en friskolekoncern har deltagit" — matchar guidens "roughly 20 schools in 11 municipalities" nästan ordagrant (guiden utelämnar bara friskolekoncernen). **Not om intern variation i källan:** på ett annat ställe i samma bok skriver författaren i stället "tio kommuner, en friskoleorganisation och SKL" — en avvikande räkning inom samma dokument; guidens tal (11) är förordets egen formulering, inte en guidekonstruktion, så det ändrar inte verdikten. Utfall 1, ordagrant: "Andelen enskilt arbete ökar generellt" (bekräftar att ensamarbetet ökade). Utfall 2, ordagrant: "Sociala medier är en mycket stor källa till distraktion vilket skapar stress hos många elever eftersom de försummar arbetet", kvantifierat senare i rapporten: "Fortfarande 2013 anger... en tredjedel av eleverna... att (framför allt) sociala medier... inverkar negativt på under[visningen]" (bekräftar att sociala medier distraherade en betydande andel elever). | **står.** Talen 20/11 och båda utfallen (ökat ensamarbete, social medier-distraktion hos en tredjedel av eleverna) är rapportens egna, ordagrant belagda. |
| S34 | **Ersättningskälla för S05/S06** — Wang & Fan-metaanalysen (indragen 2026-04-22, dessutom fel tidskrift och fel studieantal, se S05/S06) kan inte längre bära den positiva sidan i avsnittet på sidan 6 ("Challenging thinking, or replacing it"). Denna post belägger en oindragen, peer-granskad metaanalys av kontrollerade (experimentella) ChatGPT-studier som kan ersätta citatet. Task 5B lade bara källan; Task 7 (denna uppgift) har skrivit meningen och mätt EW/EP mot den — se verdiktet nedan för ordalydelsen och vaktblocket för ankaren. | 1 | 1 | doi.org/10.1016/j.compedu.2024.105224 → omdirigerar till sciencedirect.com/science/article/pii/S0360131524002380 → **403** direkt (ScienceDirect blockerar bot-UA, samma mönster som OECD/Nature/Microsoft/Elsevier tidigare i den här inventeringen; en captcha-sida bekräftades med både webbläsar-UA via curl och via r.jina.ai-proxy; `archive.org/wayback/available` och CDX-sökning gav ingen capture som visar annat än samma blockering). Läst i stället via en bitidentisk, förlagsproducerad kopia av den publicerade PDF:en: onderwijsorakel.nl/wp-content/uploads/2024/12/1-s2.0-S0360131524002380-main-1.pdf (filnamnet är ScienceDirects egen PDF-namnkonvention för just denna pii; `pdfinfo` på den hämtade filen bekräftar `Creator: Elsevier` och `Subject: Computers & Education, 227 (2025) 105224. doi:10.1016/j.compedu.2024.105224` — samma artikel som DOI:n pekar på, inte en annan version) → **200**, ordagrant 2026-10-15: "A comprehensive search across five databases identified 69 articles published between 2022 and 2024 for analysis." och: "Overall, the results showed that ChatGPT interventions significantly enhanced academic performance (g+ = 0.712), affective-motivational states (g+ = 0.881), and higher-order thinking propensities (g+ = 0.703); significantly reduced mental effort (g+ = -0.675); but did not have a significant effect on self-efficacy (g+ = 0.441)." Författare (kolofonen): Ruiqi Deng, Maoli Jiang, Xinlu Yu, Yuyan Lu, Shasha Liu, Jing Hengyi School of Education, Hangzhou Normal University. Open access under CC BY-licens, bekräftat både i artikelns egen kolofon och av Unpaywall (`api.unpaywall.org`, oa_status: hybrid, license: cc-by). Tidslinje (artikelns sidfot, ordagrant): "Received 15 August 2024; Received in revised form 9 December 2024; Accepted 11 December 2024; Available online 12 December 2024." **Retraktionsstatus aktivt kontrollerad, på tre ställen:** (1) `api.crossref.org/works/10.1016/j.compedu.2024.105224` → fälten `update-to`, `updated-by` och `relation` är alla tomma — CrossRef, som bär förlagens egna retraktionsflaggor, känner inte till någon rättelse eller indragning av artikeln. (2) Hela Retraction Watch-databasen hämtad som CSV direkt från `api.labs.crossref.org/data/retractionwatch` (det officiella dataset retractiondatabase.org bygger på, ca 25 MB, 2026-10-15) och genomsökt mot DOI:n, artikelns titel och författarnamnet "Ruiqi Deng" — noll träffar. Som kontroll av att sökmetoden faktiskt fångar en indragning gav exakt samma genomsökning en träff på den redan kända Wang & Fan-indragningen (DOI 10.1057/s41599-025-04787-y, retraherad 2026-04-22, samma institution — Jing Hengyi School of Education, Hangzhou Normal University — som denna artikels författare) — dvs. metoden hade hittat den här artikeln om den var indragen. (3) `retractionwatch.com`, sökt direkt på författarnamnen och titeln → noll träffar. Ingen retraktion, ingen "expression of concern", ingen corrigendum hittad på något av de tre ställena. | **lagt till.** Kraven 1–4 är uppfyllda: en oindragen, peer-granskad systematisk översikt och metaanalys av kontrollerade (experimentella) studier om generativ AI:s effekt på elevers lärande, hämtad i fulltext och citerad ordagrant ovan. Källan bär: 69 identifierade studier (62 meta-analyserade), och statistiskt signifikanta positiva effekter för tre utfall som tillsammans kan bära avsnittets positiva sida — academic performance (g+ = 0.712), affective-motivational states (g+ = 0.881) och higher-order thinking propensities (g+ = 0.703). Källan bär INTE "motivation" som eget, separat mått — närmast är "affective-motivational states", ett bredare begrepp som omfattar men inte är identiskt med motivation — och bär heller inte stöd för att kalla resultatet okontroversiellt: källan flaggar själv publikationsbias i två av fem utfall (academic performance, affective-motivational states) och avsaknad av power-analys som skäl till försiktig tolkning av samtliga resultat. **Task 7 (denna uppgift) har skrivit in meningen** på båda engelska ytorna (sidan 6), 2026-10-15: "A 2024 meta-analysis (Deng et al., *Computers & Education*, 69 studies identified) found/finding that ChatGPT in controlled experiments significantly improved students' academic performance, affective-motivational states and higher-order thinking." Ordet "motivation" är inte återanvänt — "affective-motivational states" står i stället, källans eget begrepp. Ingen "okontroversiell"-formulering är tillagd; publikationsbiaset och avsaknaden av poweranalys nämns inte i guidetexten (bedömt som för mycket detalj för avsnittets längd, inte som en utelämnad varning om ett sakförhållande guiden hävdar motsatsen till). |
| S36 | `correlation of -0.75` — guidens tionde forskningscitat, EW-exklusivt (sidan 6, direkt efter Lee et al.): "A Swiss study (Gerlich 2025) found a correlation of -0.75 between AI use and critical thinking among younger users." Upptäckt av Task 5B; ingen post fanns förrän nu. | 1 | 0 | mdpi.com/2075-4698/15/1/6 → **403** direkt (Akamai-kant, "Access Denied" — samma klass bot-blockering som OECD/Nature/Microsoft/ScienceDirect tidigare i den här inventeringen); läst i stället via en r.jina.ai-renderad kopia av exakt samma förlagssida (r.jina.ai/https://www.mdpi.com/2075-4698/15/1/6) → **200**, hämtad 2026-10-15: sidan visar artikelns normala "Open Access"-märke, titel "AI Tools in Society: Impacts on Cognitive Offloading and the Future of Critical Thinking", författare Michael Gerlich, avdelning "Center for Strategic Corporate Foresight and Sustainability, SBS Swiss Business School, 8302 Kloten-Zurich, Switzerland", "28 Pages" — och **ingen indragningsbanner** (jämför den indragna Wang & Fan-artikelns egen rubrikprefix "RETRACTED ARTICLE:", se S05, som syns direkt på motsvarande sida). DOI 10.3390/soc15010006, publicerad online 2025-01-03 (`api.crossref.org/works/10.3390/soc15010006`, fältet `published-online`, 2026-10-15). Fulltexten läst via en bitidentisk, förlagsproducerad PDF-spegling: traindy.io/wp-content/uploads/2025/01/2025-AI-and-Critical-Thinking.pdf → **200**, hämtad 2026-10-15 (`pdfinfo` bekräftar `Title: AI Tools in Society: Impacts on Cognitive Offloading and the Future of Critical Thinking`, `Author: Michael Gerlich`, 28 sidor; varje sidfot i den extraherade texten bär journalens egen löpande rubrik "Societies 2025, 15, 6" — samma artikel som DOI:n pekar på, inte en annan version). **Korrelationssiffran, källans egen Tabell 6, ordagrant:** "AI Tool Use ↔ Cognitive Offloading ... +0.72 ... Strong positive correlation", "AI Tool Use ↔ Critical Thinking ... −0.68 ... Strong negative correlation", "Cognitive Offloading ↔ Critical Thinking ... −0.75 ... Strong negative correlation." Brödtexten upprepar samma tre tal, ordagrant: "The correlation between AI tool use and critical thinking was found to be strongly negative (r = −0.68)..." och, i nästa stycke: "A strong negative correlation (r = −0.75) between cognitive offloading and critical thinking further supports this interpretation." **Retraktionsstatus aktivt kontrollerad, på två ställen (samma metod som S34):** (1) `api.crossref.org/works/10.3390/soc15010006` → fältet `updated-by` visar en länk av `"type": "correction"` (DOI 10.3390/soc15090252, "updated" 2025-09-10) — ingen post av typen retraction i `update-to` eller `relation`. Korrigeringens eget innehåll (ideas.repec.org/a/gam/jsoctx/v15y2025i9p252-d1746512.html → **200**, hämtad 2026-10-15, abstract ordagrant: "Error in Table [4]...") gäller Tabell 4 (ANOVA för "deep thinking activities", en dubblett av Tabell 3) — inte Tabell 6, den tabell denna post hänger på. (2) Hela Retraction Watch-databasen hämtad som CSV (`api.labs.crossref.org/data/retractionwatch`, ca 73 200 rader, 2026-10-15) och genomsökt mot DOI:n, artikeltiteln och författarnamnet "Gerlich" → noll träffar; samma dataset och metod fångade redan den kända Wang & Fan-indragningen (se S34) — dvs. metoden hade hittat den här artikeln om den var indragen. **Studiedesign, ordagrant ur källans avsnitt 3.2–3.5:** urvalet var "669 participants in the United Kingdom, of which 666 were considered valid", rekryterade "through a combination of convenience and purposive sampling" och "promoted online in the UK on different social media platforms" — ett självselekterat bekvämlighetsurval i Storbritannien, inte ett draget slumpurval. Kritiskt tänkande mättes med en "structured questionnaire ... A 6-step Likert scale", byggd på "established instruments such as the Halpern Critical Thinking Assessment (HCTA) tool and Terenzini's self-reported measures" — ett självrapporterat enkätmått, inte ett genomfört HCTA-prestationstest. Designen är tvärsnittlig: en enda enkätomgång plus semistrukturerade intervjuer med en delmängd på 50 deltagare, ingen uppföljning över tid. Åldersfyndet, ordagrant ur abstractet: "Younger participants exhibited higher dependence on AI tools and lower critical thinking scores compared to older participants" — ett separat ANOVA/gruppmedelvärde-fynd för åldersgrupperna "17–25 years (young), 26–45 years (middle-aged), and 46 years and older (older)", inte en korrelationssiffra; källan knyter aldrig −0,75 specifikt till yngre användare. | **falskt.** Källan bär tre separata korrelationer, inte en, i sin egen Tabell 6: AI-användning ↔ kritiskt tänkande är **−0,68**; AI-användning ↔ cognitive offloading är **+0,72**; cognitive offloading ↔ kritiskt tänkande är **−0,75**. Guidens mening kopplar −0,75 till fel variabelpar — den sätter siffran som källan reserverar för "cognitive offloading ↔ critical thinking" på "AI use and critical thinking", vars egen siffra i källan är −0,68. Det är inte en avrundning: det är fel tal på fel variabelpar, en strängare variant av S04:s felklass (rätt tal, fel enhet) — här är talet självt fel för det påstådda paret. Epitetet "Swiss study" är försvarbart som institutionsbeskrivning (Gerlich är knuten till SBS Swiss Business School, Kloten-Zürich), men urvalet självt är brittiskt — 669 deltagare rekryterade i Storbritannien via sociala medier, inte i Schweiz — vilket guiden inte klargör och en läsare lätt misstolkar. Studien är dessutom självrapporterad och tvärsnittlig, med ett bekvämlighetsurval rekryterat via sociala medier (samma förbehållsklass som S08 gav Kosmyna-citatet: preprint, N=54), och "among younger users" är ett separat gruppmedelvärde-fynd, inte vad −0,75 själv mäter. En korrigering finns (2025-09-10) men gäller Tabell 4 (ANOVA), inte Tabell 6, och ändrar inget av ovanstående. Meningen kan inte stå som den är skriven — se rapporten för vad källan faktiskt bär. |

### Produktlandskapet (spec §6 klass 2) — "The visibility gap"

Sex påståenden i specen, mätta som åtta kandidater eftersom ett av påståendena namnger
tre produkter var för sig och ett har en egen primärkälla redan i en syskoninventering.
**S37 är tillagd av Task 9** (en nionde kandidat, utanför både brevets och specens
ursprungliga uppräkning) — se S37:s egen cell för skälet.

| id | påstående i guiden | EW | EP | primärkälla + hämtdatum | verdikt |
|---|---|---|---|---|---|
| S19 | `largest chatbots` — "The largest chatbots in K-12 classrooms today are Gemini (Google) and ChatGPT (OpenAI)" — en marknadsandelsutsaga utan källa i guiden |  1 |  1 | securly.com/aiusageinsights → **200**, hämtad 2026-10-14. Detta är **inte** en av leverantörernas egna sidor utan en skolenhets-övervakningsleverantörs egen telemetri från skolägda enheter — den enda hämtbara datakälla som hittades för K-12-andelar, vilket brevet inte förutsåg ("det gör det sannolikt inte"). Ordagrant: "**Gemini** Google 38% (872,054 Chats)" och "**ChatGPT** OpenAI 37.2% (838,344 Chats)", mot tredjeplacerade "Securly AI Chat" på 19.4%. Urval: "2.25 Million Student AI Conversations in 138 Days" över "1,454 School Districts in 39 States", period "Dec 1, 2025 - April 17, 2026", sidan daterad "May 15, 2026". **Samma leverantörs egen tidigare mätning ger motsatt ordning:** k12dive.com/spons/the-ai-visibility-gap-lessons-from-12-million-k-12-conversations/817500/ → **200**, hämtad 2026-10-14 (publicerad 2026-04-20, Securly-sponsrat innehåll, samma metodik): ordagrant "ChatGPT holds 42 percent of the market, Gemini accounts for 21 percent", urval "nearly 1.2 million student AI conversations across 1,312 districts in 39 states". Två läsningar av samma företag, fem veckor isär, är alltså oense om vilken av de två som är störst, även om båda är överens om att Gemini och ChatGPT tillsammans dominerar stort över en namngiven trea. Ingen av Google eller OpenAI publicerar själva K-12-marknadsandelar. | **rättat.** Var `obelagt` för rangordningen — inte därför att ingen källa finns (brevets gissning), utan därför att den enda hittade källan motsäger sig själv om turordningen inom samma femveckorsperiod. Att "Gemini och ChatGPT tillsammans är störst" håller i båda Securly-läsningarna; vilken av de två som är störst gör det inte, och ingen förstapartskälla ger en stabilare siffra. **Task 9 har skrivit om meningen på båda engelska ytorna (sidan 15), 2026-10-15:** `The largest chatbots in K-12 classrooms today are Gemini (Google) and ChatGPT (OpenAI)` → `Two chatbots dominate K-12 classrooms today: Gemini (Google) and ChatGPT (OpenAI)` — "dominate" håller det som är belagt (de två tillsammans är störst) utan att rangordna dem mot varandra. |
| S20 | `Copilot is built on` — "Copilot is built on ChatGPT" — var en förenkling redan i april 2026 enligt specen, sannolikt fel nu |  1 |  1 | **Korsref enligt brevet gick inte att utföra:** samtliga 27 poster (C01–C27) i `docs/guide-facts-copilot.md` genomsökta — ingen rör Copilots underliggande modell eller nämner OpenAI/GPT över huvud taget. Mätt direkt mot förstapartskällor i stället. techcommunity.microsoft.com (Microsoft Copilot Blog, "Available today: OpenAI's GPT-5.6 in Microsoft 365 Copilot", publicerad 2026-07-09) → **200**, hämtad 2026-10-14, ordagrant: "Microsoft 365 Copilot is AI built for work, where frontier models like GPT-5.6 are an important part of a broader system designed to deliver business value—bringing together Work IQ, Microsoft 365 apps, and the enterprise-grade security, compliance, and privacy customers expect from Microsoft." openai.com/index/gpt-5-6-preferred-model-microsoft-365-copilot/ → **200**, hämtad 2026-10-14, ordagrant: "GPT‑5.6 ... will become the new preferred model in Microsoft 365 Copilot ... In addition to serving the models natively, Microsoft will also access OpenAI models directly through the API." Se även samma Copilot-inventerings **C07** (redan verifierad), learn.microsoft.com/en-us/microsoft-365/copilot/microsoft-365-copilot-privacy, ordagrant: "Models provided by Anthropic as a subprocessor are currently excluded from the EU Data Boundary" — Copilot körs alltså på flera leverantörers modeller parallellt (OpenAI **och** Anthropic), inte på en enda. | **falskt.** "Copilot is built on ChatGPT" blandar redan i grunden ihop ChatGPT (OpenAIs konsumentprodukt) med de GPT-modeller Copilot faktiskt hämtar via Azure OpenAI Service/API — Copilot har aldrig varit "byggt på ChatGPT" i produktmening. I dag beskriver Microsoft själv Copilot som "a broader system" där frontier-modeller som GPT-5.6 är "an important part", och samma inventerings egen C07-post visar att Anthropics modeller körs som underleverantör vid sidan av OpenAIs. Både ramen (ett enda ursprung) och produktnamnet (ChatGPT snarare än GPT-modellerna) är fel. **Task 9 har skrivit om meningen på båda engelska ytorna (sidan 15), 2026-10-15:** `Copilot is built on ChatGPT` → `Copilot is, in Microsoft's own words, "a broader system" that draws on several models — including OpenAI's GPT models and, as a subprocessor, Anthropic's — not a single ChatGPT core`. Cellen bär citaten ("a broader system", "as a subprocessor"); guidetexten återanvänder dem i stället för att hitta på en egen beskrivning. |
| S21 | `beyond the device` — "Apple Intelligence uses ChatGPT for the functions that go beyond the device". **Ankaret är kortat till denna fras** (regel 3) i stället för hela meningen. **Not om avvikelsen:** den här kandidaten stod inte i brevets steg-1-skript (de 25 angivna strängarna); den är tillagd här därför att specens §6 klass 2 räknar upp meningen som ett av sina sex påståenden och ger den redan ett korsref-svar (`Apple-inventeringens A11/A12, verdikt `står`, verifierat 2026-10-14`), och regel 1 ("en faktamening utan post får inte skrivas") gäller lika mycket för en mening brevets skript råkade utelämna. Mätt precis som övriga kandidater: `grep -c "beyond the device"` |  1 |  1 | **Korsref `guide-facts-apple-intelligence.md` A11 och A12** — bägges verdikt kontrollerat här innan korsrefen användes: båda **står**, inte `obelagt` eller `falskt`, så korsrefen är tillåten enligt regeln. A11: support.apple.com/guide/iphone/use-chatgpt-with-apple-intelligence-iph00fd3c8c2/ios → **200**, ordagrant: "You can allow Apple Intelligence to work with ChatGPT from OpenAI"; `grep -i "Gemini\\|Claude\\|Anthropic"` på samma hämtade sida ger noll träffar. A12: samma sida → **200**, ordagrant: "ChatGPT from OpenAI" och "For more information, see OpenAI Terms of Use." Båda lästa 2026-10-14 enligt Apple-inventeringen. | **står.** Apple-inventeringen har redan verifierat att ChatGPT (OpenAI) är den enda externa leverantör Apple dokumenterar som valbar extension för förfrågningar Siri inte klarar on-device — exakt det "beyond the device" hävdar. A11 noterar en annan, separat brasa (se A17: Google och dess Gemini-modeller är med och bygger själva Siri AI) men den gäller hur assistenten är konstruerad, inte vilken extern tjänst en användare kopplar på för uppgifter utanför enheten — den brasan rör inte den här guidens mening, och A17:s egen anteckning säger uttryckligen att den ska hållas skild från ChatGPT-extensionen (A11/A12). |
| S22 | `Khanmigo` — K-12-specifikt produktnamn |  1 |  1 | khanmigo.ai → **200**, ordagrant 2026-10-15 (sidtiteln och hero-ledet): "Meet Khanmigo: Khan Academy's AI-powered teaching assistant & tutor" och "Khanmigo is your always-available teaching assistant."; blog.khanacademy.org/khanmigo-features/ → **200**, ordagrant 2026-10-14 (publicerad 2023-11-29, uppdaterad 2025-03-21), rubrik: "Khanmigo Features for Teachers". Produkten finns och heter så i dag. | **står.** Namnet är oförändrat och produkten är i drift. |
| S23 | `MagicSchool` — K-12-specifikt produktnamn |  1 |  1 | magicschool.ai → **200**, ordagrant 2026-10-15 (sidtiteln och hero-ledet för lärare): "AI Platform for School Districts \| MagicSchool" och "Save time, spark creativity, and support every learner."; magicschool.ai/faq → **200**, ordagrant 2026-10-14: "Teachers decide how students use MagicSchool and can see what happens along the way." Produkten finns och heter så i dag. | **står.** Namnet är oförändrat och produkten är i drift. |
| S24 | `ChatGPT for Teachers` — K-12-specifikt produktnamn |  1 |  1 | openai.com/index/chatgpt-for-teachers/ → **200**, hämtad 2026-10-14, ordagrant rubrik/brödtext: "A free version of ChatGPT built for teachers" och "ChatGPT for Teachers is built for both educators and school leaders." Produkten finns och heter exakt så i dag. **Förbehåll som bär över till S25:** samma sida beskriver produkten enbart för "educators" och "school and district leaders" — ingen mening på sidan nämner elevkonton; det är en lärar-/personalyta, inte en elevyta. | **står.** Namnet är korrekt och produkten är i drift, med reservationen (se S25) att den enligt sin egen sida inte har elever som användare. |
| S25 | `aggregated view` — den bärande utsagan: "they do not give teachers a clear aggregated view of which questions students in a class have asked". Faller den, faller avsnittets slutsats — innehållsbeslut för Johan, inte en formulering för en uppgift (spec §6) |  1 |  1 | Mätt leverantör för leverantör mot var och ens egen publika dokumentation (inte jämförelseartiklar), enligt brevets steg 1–2. **Google** (Gemini for Education / Workspace for Education admin): edu.google.com/intl/ALL_us/ai/gemini-for-education/ → **200**, hämtad 2026-10-14, ordagrant: "Enterprise-grade data protection: Core Service covered under Google Workspace for Education terms. Data is not human reviewed or used to train AI models." knowledge.workspace.google.com/admin/generative-ai/review-gemini-usage-in-your-organization → **200**, hämtad 2026-10-14, ordagrant: "Review Gemini in Google Workspace apps usage information by organizational unit or group... The number of chat messages your users exchanged with Gemini... Gemini usage per feature." Funktionen är **admin**-vänd (Google Admin-konsolen), inte lärarvänd, och visar antal och trender per organisationsenhet — aldrig ämne eller innehåll i en elevfråga. **OpenAI** (ChatGPT Edu / ChatGPT for Teachers): help.openai.com/en/articles/10875114-workspace-analytics-for-chatgpt-enterprise-and-edu → **200**, hämtad 2026-10-14 (sidan anger "Updated: 2 months ago"), ordagrant: "Task insights shows aggregated patterns of work in ChatGPT by classifying conversations into broad task categories and topics. It provides workspace-level insights without exposing individual prompts, conversations, or user-level activity." Ämnesbunten, inte frågebunten, aggregering på **workspace**-nivå (inte klass-/lektionsnivå), och gäller "ChatGPT Enterprise and Edu" — inte det K-12-produktnamn guiden själv använder. openai.com/index/chatgpt-for-teachers/ → **200**, hämtad 2026-10-14, ordagrant: "ChatGPT for Teachers is built for both educators and school leaders" — produkten har enligt sin egen sida inga elevkonton alls (se S24), så det finns ingen elevfråga att aggregera i just den produkten. **Microsoft** (Copilot for Education): learn.microsoft.com/en-us/copilot/manage → **200**, hämtad 2026-10-14 (sidans "ms.date": 2026-10-12), ordagrant: "The Microsoft Copilot Chat usage dashboard provides insights into active usage of Copilot Chat. Admins can generate reports on total active users, average daily active users, total prompts submitted and average prompts per user, and active users of Copilot Chat in specific apps." microsoft.com/en-us/education/products/copilot-in-education → **200**, hämtad 2026-10-14: nämner "Copilot Dashboard" (adoption/sentiment) och "Education Insights"-kort som flaggar elever vars "activity patterns have changed" — inga av dessa beskriver en vy över frågornas innehåll eller ämne, bara antal och mönsterflaggor, och uttryckligen admin-vänt. **Khan Academy** (Khanmigo Teacher Tools): blog.khanacademy.org/khanmigo-features/ → **200**, hämtad 2026-10-14 (publicerad 2023-11-29, uppdaterad 2025-03-21), ordagrant: "Summarize Student Chat History: Gain insights from compiled summaries of student Khanmigo chats (available exclusively to teachers rostered in a Khan Academy Districts partner district)." khanacademy.org/khan-for-educators/k4e-us-demo/xb78db74671c953a7:engage-from-preparation-to-pedagogy/xb78db74671c953a7:quick-data-checks/v/responding-to-student-chat-trends → **200**, hämtad 2026-10-14, ordagrant (den officiella lärarutbildningsvideots egen transkript): "From your class dashboard, you can choose a class and explore trending topics or flag conversations. Trending topics give you a quick snapshot of what students are asking about most often. For example, you might notice several students asking about area calculation or problem-solving over the past week... these trends give you valuable insight into what's on your students' minds." **Detta är den enda av de fem mätta leverantörerna vars egen publika dokumentation uttryckligen beskriver precis den vy guiden säger saknas** — en klassnivå-aggregering av vilka ämnen/frågor eleverna ställt till AI:n, tillgänglig för läraren, inte bara admin. **MagicSchool**: magicschool.ai/blog-posts/enterprise-feature-releases → **200**, hämtad 2026-10-14 (publicerad 2025-02-03, byline "Senior Product Marketing Manager, MagicSchool"), ordagrant: "Student Room Insights provides teachers and admins with a window into classroom activity... Access detailed usage data: For a broader view, the dashboard compiles quantitative data on tool usage and frequency. It updates hourly." magicschool.ai/faq → **200**, hämtad 2026-10-14, ordagrant: "Teachers decide how students use MagicSchool and can see what happens along the way... review students' work and AI interactions." En aggregerad vy över **vilka verktyg** och **hur ofta**, klassvis och i realtid — närmare guidens påstående än Google/Microsoft/OpenAI, men ingen av sidorna beskriver en vy över **ämnena eller innehållet** i frågorna, bara verktygsanvändning och frekvens. Gränsfall, räknas här som att INTE uppfylla "which questions." | **står, men smalt — se rapporten till Johan.** Fyra av fem mätta leverantörer (Google, Microsoft, OpenAIs namngivna K-12-produkt, och MagicSchool för frågeinnehåll specifikt) ger enligt sin egen publika dokumentation ingen aggregerad vy över elevfrågornas innehåll — det håller "majority"-formuleringen i sak, och meningens egna hedge ("according to what's publicly advertised") håller också. **Men Khan Academy/Khanmigo — ett av de tre K-12-produktnamn som räknas upp i exakt samma mening — annonserar offentligt precis den förmåga meningen säger att majoriteten saknar** (klassnivå "trending topics" och "Summarize Student Chat History", lärarvänt, inte bara admin). Det motsäger inte ordet "majority" (en av fem är inte en majoritet), men det är ett namngivet undantag i samma andetag som påståendet görs. Detta är brevets eget "minst några gör det"-spår (steg 4) — den bokstavliga satsen håller, men om den håller som LÄSARENS intryck av stycket, och om Khanmigo-undantaget bör namnges eller hedgen skärpas, var en innehållsfråga för Johan, inte en faktafråga den här uppgiften kunde avgöra. **Johans beslut vid rundans grind (2026-10-15), genomfört av Task 9:** Khanmigo namnges explicit, i samma mening som majoritetspåståendet, på båda engelska ytorna (sidan 15) — `...do not give teachers a clear aggregated view of which questions students in a class have asked the AI during a lesson; Khanmigo is the exception, advertising a "Summarize Student Chat History" feature and a class dashboard of trending topics.` Den tredje styckesmeningen på samma sida ("There is one notable exception...") är omskriven i samma svep för att elaborera på Khanmigo i stället för att upprepa namngivningen separat — se **S37** för varför den meningen tidigare namngav ett annat, aldrig mätt produktnamn (SchoolAI) och varför det måste rättas här för att inte motsäga den här posten. |
| S26 | `back in 2014` — "teachers suddenly have the instruments the 1:1 researchers were calling for back in 2014", hänger på S25 |  1 |  1 | Hänger på S25 (brevets egen regel: "faller den faller den här"). Meningen är själv villkorad — "Combined with aggregated class visibility (if the vendor offers it), teachers suddenly have the instruments..." — och det villkoret är, enligt S25:s källrad, redan uppfyllt hos minst en namngiven leverantör (Khanmigo) per 2026-10-14. Ingen ny hämtning krävs utöver S25:s fem leverantörskällor, eftersom den här meningen inte själv namnger någon leverantör. | **står.** Villkoret "if the vendor offers it" är redan uppfyllt hos minst en leverantör (Khanmigo, se S25) enligt dagens publika dokumentation, så den villkorade slutsatsen är sann som skriven — den överclaimar inte på egen hand. Den hänger på S25 precis som brevet förutsåg, och landar i samma läge: formellt sant, men värt Johans uppmärksamhet av samma skäl som S25. **Läst mot den nya sidan 15 (Task 9, 2026-10-15):** villkoret är nu namngivet, inte bara hypotetiskt — Khanmigo står explicit som undantaget i stycket ovanför. Meningens egen hedge ("if the vendor offers it") höll redan innan namngivningen och behöver ingen ändring; den beskriver fortfarande korrekt att instrumentet inte är universellt, bara att minst en leverantör nu är namngiven i stycket intill. Ingen ändring gjord i guidetexten för den här posten. |
| S37 | `SchoolAI` — guidens tidigare undantagsclaim på sidan 15: "There is one notable exception in the K-12 space. SchoolAI offers an aggregated class-level dashboard that surfaces common misconceptions and recurring topics across the class." Fanns i guiden redan innan den här rundan (arv från guide-designens ursprungsspec, april 2026) men stod utanför både Task 1:s 25 kandidater och Task 4:s sex produktposter — ingen uppgift i den här rundan mätte eller belade påståendet förrän Task 9 upptäckte det vid redigeringen av samma stycke. |  1 |  1 | `docs/superpowers/specs/2026-04-23-ai-for-elever-guide-design.md`, rad 40 och 85, bekräftar att claimet var ett medvetet designval från april 2026 ("EN-version nämner SchoolAI som undantag", källa angiven som "SchoolAI dokumentation + Bloomberg-investigation 2025") — men ingen av de källorna är hämtad eller läst i DEN HÄR rundans inventering, och specraden själv är en avsiktsförklaring, inte ett ordagrant citat mot en primärkälla. Ingen hämtning är gjord mot schoolai.com eller Bloomberg-artikeln i den här uppgiften; se "farhågor" i Task 9-rapporten. | **struket.** Inte därför att påståendet nödvändigtvis är falskt — det är helt enkelt obedömt, eftersom det aldrig ingick i rundans fem mätuppgifter (Task 1–4) och alltså aldrig fick en primärkälla hämtad mot sig i DEN HÄR inventeringen. Problemet som tvingar fram strykningen är ett annat: **Johans beslut vid grinden (S25) namnger Khanmigo, explicit, som "undantaget" i samma stycke** — och en kvarlämnad SchoolAI-mening två meningar senare hade gjort sidan till sin egen motsägelse, två olika, obelagda "undantag" på samma sida. Struket utan ersättning vid DENNA post, 2026-10-15 (Task 9) — ersättningen (Khanmigo, belagd mot S25) lever vid S25, inte som en rättning av S37 självt, exakt samma mönster som S05/S06 → S34. Om SchoolAI:s egen klassvy ska tillbaka i en framtida runda är en innehållsfråga för Johan, inte en som den här uppgiften kan avgöra — den skulle i så fall kräva sin egen hämtning mot schoolai.com, inte ett antagande utifrån aprilspecens formulering. |

### Regleringen (spec §6 klass 3) — GDPR och AI Act

**Task 1 lämnade den här klassen tom med avsikt** (brevets steg-1-skript mätte inte mot
den, se föregående version av det här avsnittet). **Task 5 (denna uppgift) mäter den**,
enligt specen "mot de färdiga posterna" — dvs. mot Apple-inventeringens redan
verifierade A33–A39 (AI Act:s tillämplighetsdatum, de fyra risknivåerna, artikel 4:s
AI-kunnighetsplikt, artikel 16 mot artikel 26, artikel 27, Annex III-tidpunkten 2
december 2027), inte mot en ny hämtning av samma sak. Där guiden säger något
Apple-inventeringen inte täcker (FERPA, amerikanska delstatsregler, UK GDPR, GDPR
artikel 35) är källan en egen hämtning, med egen källcell, gjord 2026-10-15.

De tre regleringspassagerna sitter på sidorna 11 ("GDPR and the EU AI Act"), 12 ("GDPR
in practice") och 21 (FAQ:ns AI Act- och DPIA-svar). Sju kandidater identifierade, S27–S33.

**Den kända felklassen (G48, Geminis `pre-market obligations`, Apples A36/A37) är
funnen igen, i S28** — se motiveringen i den raden. **Inte i S27** (rättat vid
granskningen av den här uppgiften — se S27:s egen cell för varför "neither can be
postponed" faktiskt stämmer, och varför den tempting-men-fel läsningen ändå var värd
att skriva ner). Felet är inte en attributionsfråga här (guiden lägger ingen namngiven
leverantörsplikt på skolan, till skillnad från G51:s ursprungliga fel) utan en
tidsfråga: S28:s högriskskyldigheter beskrivs i presens, utan datum, längre ner i
samma avsnitt.

| id | påstående i guiden | EW | EP | primärkälla + hämtdatum | verdikt |
|---|---|---|---|---|---|
| S27 | `neither can be postponed` — "Both apply, both are the teacher's and the school authority's responsibility, and neither can be postponed," om EU AI Act och GDPR tillsammans | 1 | 1 | `korsref A33` (`docs/guide-facts-apple-intelligence.md`, verdikt `lagt till`) — AI Act:s tillämplighetsdatum, kommissionens ordalydelse via P13: "entered into force on 1 August 2024 and became applicable on 2 August 2026." GDPR:s tillämplighet sedan 2018 är obestridd och kräver ingen ny källa. Ingen korsref mot A34/A39 (artikel 4/Annex III) — de är inte vad meningen syftar på, se verdiktet | **står.** "Both" och "neither" syftar grammatiskt tillbaka på den NÄRMAST FÖREGÅENDE meningens två namngivna regelverk — "the EU AI Act... and the GDPR" — inte på artikel 4 kontra Annex III, som inte ens är introducerade i texten vid den här punkten: den första nämningen av "high risk" kommer först efter ett helt stycke om icke-EU-regler (FERPA, delstatsregler, UK GDPR, se S31–S33) och en ny underrubrik, "The EU AI Act — what the classification means." Läst grammatiskt, rätt: AI Act är tillämplig sedan 2 augusti 2026 (A33), GDPR sedan länge — båda regelverken gäller, och ingetdera går att välja bort. Meningen är sann som den står. **Varför den motsatta läsningen ändå frestar:** samma felklass som redan hittats i tre andra dokument (G48, Geminis pre-market-stycke, Apples A36/A37) — högriskskyldigheter framställda som bindande i dag — finns verkligen i det här avsnittet, bara längre bort i texten och i ett annat stycke (se S28: "documentation requirements... human review before a decision takes effect," skrivet i presens utan datum). En snabb läsning som hoppar förbi mellanstycket kan av misstag koppla ordet "neither" till S28:s mer konkreta, handlingsbara skyldigheter i stället för till den abstrakta "frameworks apply"-satsen det faktiskt hör till — det var den läsningen min första bedömning gjorde, och som granskningen rättade. Nästa runda: felet sitter i S28, inte här |
| S28 | `documentation requirements` — stycket om högrisk: "Then the Act speaks of high risk... Here there are documentation requirements, transparency requirements towards the student, and requirements for human review before a decision takes effect," skrivet i presens, utan datum eller förbehåll | 1 | 1 | `korsref A34` (`docs/guide-facts-apple-intelligence.md`, verdikt `lagt till`) — ordagrant: "the rules for high-risk use cases in certain sensitive areas (Annex III) have been extended to 2 December 2027 as a result of … the AI Omnibus" — Annex III omfattar uttryckligen utbildning. Plus `korsref A37` (samma fil, verdikt `lagt till`) — artikel 26, driftsättarens (skolans) fem plikter: följ bruksanvisningen, ge mänsklig tillsyn till personal med "the necessary competence, training and authority", spara "the logs it controls" i minst sex månader, informera personal och deras representanter före driftsättning, underrätta de som berörs — hämtad av G51 från artificialintelligenceact.eu 2026-10-13, ordagrant citerad i A37 | **rättat.** Var `falskt` av två skäl. **(1) Tidlöshet:** stycket beskrev högriskskyldigheterna som gällande nu ("Here there are..."), utan att nämna att Annex III-högrisken för utbildning först träder i kraft 2 december 2027 (A34). Det var en brist som INTE finns i S27 (den meningen knyter bara ihop de två regelverkens allmänna giltighet, och står kvar som `står`) — men väl här, i det här stycket, en bit längre ner i samma avsnitt. **(2) Ofullständig lista utan att säga det:** "requirements for human review before a decision takes effect" täckte bara EN av driftsättarens (skolans) fem plikter enligt artikel 26 (A37) — bruksanvisning, tillsyn, loggar, information till personal, underrättelse till berörda. Stycket nämnde ingen av de fyra andra och gav ingen signal om att listan var ofullständig (jämför G51:s rättelse "which includes:", som uttryckligen öppnar listan). "Documentation requirements" nämndes utan att säga vem som bär dem — enligt A36 är den tekniska dokumentationen (artikel 9–15 via artikel 16(a)) i grunden **leverantörens** plikt, inte skolans, men stycket stod i ett avsnitt riktat till läraren och skolledningen, vilket riskerade att läsas som att dokumentationen är deras jobb. Ingen enskild mening pekade en namngiven leverantörsplikt direkt på skolan (skillnad mot G51:s ursprungliga fel), men otydligheten pekade åt samma håll. **ÅTGÄRDAT i Task 8 (2026-10-15), sidan 11, båda engelska ytorna:** styckets sista mening ("Here there are documentation requirements...") är ersatt med en mening som skriver ut distinktionen explicit. Vad som binder skolan I DAG: Article 4's AI-literacy-plikt, sedan **2 February 2025**, oavsett risknivå. Vad som INTE binder än: själva högriskplikterna (dokumentation, transparens, mänsklig granskning) — de startar **2 December 2027**, och fram till då bärs det mesta av **leverantören under Article 16**, inte skolan (den motsatta felriktningen brevet varnade för). Från samma datum bär skolan **Article 26** som driftsättare. Ny ordalydelse (identisk på EP och EW): "These high-risk duties — documentation, transparency, human review before a decision takes effect — start on 2 December 2027, and even then most belong to the provider under Article 16, not the school. What already binds a school today, at every risk tier, is Article 4's AI-literacy duty, in force since 2 February 2025; from 2 December 2027 the school itself carries Article 26 as deployer, plus Article 27's fundamental-rights impact assessment before first use, whether it is publicly run or an independent provider of a public service." Artikel 27-ledet hör formellt till **S30** (se den posten) men är skrivet in i samma mening av utrymmesskäl — se S30:s cell för varför. |
| S29 | `minimal risk` — "AI use falls in the minimal risk category and the requirements are relatively light" | 1 | 1 | `korsref A35` (`docs/guide-facts-apple-intelligence.md`, verdikt `lagt till`) — kommissionens ordalydelse, ordagrant: "The AI Act defines 4 levels of risk for AI systems: Unacceptable risk / High risk / Transparency risk / Minimal or no risk" | **rättat.** Var `falskt, men lindrigt`. Aktens egen fjärde nivå heter "Minimal or no risk," inte "minimal risk" — och "minimal risk" var exakt den förkortade/föråldrade variant som A35 noterar stod fel i Gemini-guiden innan G26 rättade den (tillsammans med "Limited risk" → Transparency risk och "Prohibited" → Unacceptable risk). Skillnaden var lindrigare här än i Gemini-fallet: guiden räknade inte upp alla fyra nivåer i en formell lista eller ett diagram (bara "minimal risk" och "high risk" nämndes, i löpande text), så felet var ett enda ord ("or no" saknades) snarare än en felaktig fyrnivålista. "High risk" i samma mening var redan korrekt och är orört. **ÅTGÄRDAT i Task 8 (2026-10-15), sidan 11, båda engelska ytorna:** `minimal risk` → `Minimal or no risk`, samma rättelse som G26 redan gjorde i Gemini-guiden. Den nakna strängen `minimal risk` förekom exakt en gång per yta före rättelsen (mätt, inget legitimt kvarvarande bruk någon annanstans i guiden), så den är ett säkert `borttaget`-ankare utan undantag. |
| S30 | `Data Protection Impact Assessment` / `GDPR Article 35` — FAQ-svaret: "Do we need a Data Protection Impact Assessment (DPIA)? ... a DPIA is often required (under GDPR Article 35 in the EU; consult equivalent rules elsewhere)" | 1 | 1 | gdpr-info.eu/art-35-gdpr/ → **200**, hämtad 2026-10-15, ordagrant artikel 35(1): "Where a type of processing in particular using new technologies, ... is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall, prior to the processing, carry out an assessment of the impact of the envisaged processing operations on the protection of personal data." Plus `korsref A38` (`docs/guide-facts-apple-intelligence.md`, verdikt `lagt till`) — artikel 27, konsekvensbedömningen för grundläggande rättigheter, som gäller "whether the school is publicly run or an independent provider of a public service," före första driftsättning av ett Annex III-högrisksystem (utbildning är punkt 3) | **lagt till** (artikel 27 fanns inte i guiden; var `står, men ofullständigt`). GDPR artikel 35 beskrivs korrekt i FAQ-svaret (sidan 21): en DPIA krävs när behandlingen sannolikt innebär hög risk för registrerades rättigheter, precis vad guiden skriver där — det ledet är orört. Men FAQ-svaret nämnde bara GDPR:s DPIA och sa ingenting om AI Act:s EGEN, separata konsekvensbedömning för grundläggande rättigheter (artikel 27, A38) — en skyldighet som gäller samma högrisksystem (Annex III, utbildning inkluderat) oavsett om skolan är kommunal eller fristående, och som inte ersätts av en GDPR-DPIA. En läsare som gör sin GDPR-DPIA och tror sig vara klar missar en andra, AI Act-specifik plikt. **ÅTGÄRDAT i Task 8 (2026-10-15) — men INTE på FAQ-svarets egen plats.** Artikel 27 är nu skriven in i guiden, i samma mening som S28:s rättelse på sidan 11 (se S28:s cell för hela ordalydelsen): "...plus Article 27's fundamental-rights impact assessment before first use, whether it is publicly run or an independent provider of a public service." **Skälet till att meningen inte landade bredvid DPIA-meningen på sidan 21, där S30 ursprungligen pekade:** Task 8:s filomfång är uttryckligen "sidorna 7–12" (brevets egen rad för filerna), och FAQ:n (sidan 21) står explicit listad i Task 10:s brief som den uppgiftens egna rad ("FAQ:ns AI Act- och DPIA-svar enligt Task 5") — Task 10:s gränssnitt säger dessutom att den konsumerar "vad Task 8 skrev på sidorna 11–12". Att skriva om FAQ-svaret här hade dubblerat eller krockat med en uppgift som redan äger den ytan. Avsnittet har alltså nu artikel 27 — kravet "guiden ska inte sakna artikel 27" är uppfyllt — men FAQ-svarets EGEN mening på sidan 21 nämner fortsatt bara artikel 35; det är en öppen tråd för Task 10, inte en halvgjord rättelse här. Flaggat i rapporten under "farhågor". |
| S31 | `FERPA governs student data` — "FERPA governs student data" | 1 | 1 | studentprivacy.ed.gov/faq/what-ferpa → **200**, hämtad 2026-10-15, ordagrant: "FERPA is a federal law that affords parents the right to have access to their children's education records, the right to seek to have the records amended, and the right to have some control over the disclosure of personally identifiable information from the education records" | **står.** FERPA är den federala lag som reglerar amerikanska elevers utbildningsjournaler, inklusive personligt identifierbar information — precis det påståendet hävdar, om än i en enda kort sats utan detaljer |
| S32 | `no single federal AI regulation` — "in the US there is no single federal AI regulation but state-level rules (California, Colorado and others) exist" | 1 | 1 | multistate.us/insider/2026/4/9/how-states-are-regulating-ai-in-education-this-legislative-session → **200**, hämtad 2026-10-15, ordagrant om Kalifornien: "California (CA AB 1159) – Expands and strengthens student data privacy protections, prohibits using student data to train AI," samt "134 bills related to AI in education legislation have been introduced across 31 states" (mars 2026). **Colorado, delstatens egen lagstiftningssida** (`leg.colorado.gov/bills/sb24-205` → **200**, hämtad 2026-10-15, ordagrant: "Bill Summary: On and after February 1, 2026, the act requires a developer of a high-risk artificial intelligence system (high-risk system) to use reasonable care to protect consumers from any known or reasonably foreseeable risks of algorithmic discrimination in the high-risk system." Signerad 2024-05-17, Chapter 198) — alltså en verklig, antagen delstatslag, inte bara ett förslag. Samma lagstiftningssida, efterföljaren (`leg.colorado.gov/bills/sb26-189` → **200**, hämtad 2026-10-15, ordagrant: "In 2024, the general assembly enacted Senate Bill 24-205, which created consumer protections in interactions with artificial intelligence systems. The act repeals and reenacts those provisions with new requirements regarding the use of automated decision-making technology in consequential decisions." Signerad 2026-05-14, omfattar uttryckligen beslut om "education"). **"Ingen enskild federal AI-lag" — primärkälla, inte parafras:** Congressional Research Service-rapporten R48555 (`congress.gov/crs_external_products/R/PDF/R48555/R48555.2.pdf` → **200**, hämtad 2026-10-15, daterad 2025-06-04), ordagrant: "No federal legislation establishing broad regulatory authorities for the development or use of AI or prohibitions on AI has been enacted" och "In the absence of federal AI regulations, states have been enacting their own laws." Rapporten är 16 månader gammal vid hämtningstillfället, inte en nyhet från i dag — men ingen senare federal AI-lag har hittats i sökningen som motsäger den (se delstatstabellen ovan, som i stället visar fortsatt delstatsaktivitet 2026) | **står.** Påståendet är brett och unamngivet nog att hålla trots att Colorados ursprungliga lag redan bytts ut mot en efterträdare: delstatsnivå-regler finns alltjämt, bekräftat mot delstaternas egna lagstiftningssidor i både Kalifornien (AB 1159 om elevdata) och Colorado (SB24-205 → SB26-189, den senare i kraft 2027-01-01), och ingen samlad federal AI-lag finns, bekräftat mot CRS, forskningsarmen för den amerikanska kongressen. Medveten anmärkning: en federal preemption-diskussion pågår i USA 2026, men ingen preemption har trätt i kraft — påståendet är sant per hämtdatumet, inte garanterat förbli så |
| S33 | `In the UK there is UK GDPR` — "In the UK there is UK GDPR" | 1 | 1 | ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/ → **200**, hämtad 2026-10-15, ordagrant: "The UK GDPR includes a right for individuals to have inaccurate personal data rectified, or completed if it is incomplete" — ICO (Storbritanniens tillsynsmyndighet) namnger och tillämpar "UK GDPR" som egen, gällande reglering | **står.** UK GDPR är en verklig, av ICO tillämpad reglering — Storbritanniens egen version av GDPR efter Brexit, vid sidan av Data Protection Act 2018 |

Denna fyllnad är **inte** regel 2:s "stryks aldrig tyst" i andra bemärkelsen — tomheten
i Task 1 var en känd plats där ett fynd skulle höra hemma, och nu gör det det.

## Ytdivergenser — tre mätta fall utan vaktrad

Vakten (när den kopplas in för den här guiden, spec §7) kräver att en `aktiv`-rad står
**ordagrant på båda** engelska ytorna. Tre mätta fall gör det inte, och får därför ingen
rad. De står här i stället, som Apples IMY-post gör det för sin guide.

| värde | EW | EP | vad divergensen är |
|---|---|---|---|
| `correlation of -0.75` (S36, Gerlich 2025) | 1 | 0 | EW bär hela meningen om Gerlich-studien (sidan 6, direkt efter Lee et al.); EP har ingen motsvarighet — printytans stycke om "Challenging thinking, or replacing it" slutar efter Lee et al.-meningen. Se S36 för källkontrollen: siffran är dessutom felaktigt knuten (den hör till ett annat variabelpar i källan, verdikt `falskt`) — men ändringen rör en sträng som bara finns på EN yta, så ingen `aktiv`-rad är möjlig oavsett vad en framtida rättning landar på. |
| `GDPR in practice (EU) / equivalent data protection rules elsewhere` — rubriknivå | h3 (0 som h2) | h2 (1) | Rubrikens ORD är identiska, ordagrant, på båda ytorna (`grep` bekräftar full textmatch) — det här är INTE en sträng som saknas. Divergensen är strukturell: EP ger meningen sin egen sida med eyebrow "Regulation — continued" och en egen `<h2>`, som en jämbördig andra regleringsrubrik vid sidan av "GDPR and the EU AI Act — what teachers need to know". EW nästlar samma mening som en underordnad `<h3>` inom den enda sektionen "Regulation" (`id="p2-law"`), utan egen eyebrow. En läsare av EP möter alltså GDPR-i-praktiken som en egen huvudrubrik; en läsare av EW möter den som en underrubrik till AI Act-avsnittet. Ingen `aktiv`-rad är möjlig på rubriktexten (den är redan identisk och skulle mäta 1/1), men rubrikNIVÅN i sig divergerar och är dokumenterad här som den kända skillnaden brevet syftade på. |
| `A skilled teacher's most important tool is judgement.` + dess efterföljande stycke ("AI is the most powerful tool we've yet seen for amplifying teaching...") | 0 | 1 | EP:s baksidestext (`back-cover`) bär en avslutande rubrik och ett helt stycke som EW aldrig får någon motsvarighet till — EW:s sista innehållssektion är CTA-bandet ("Take the guide with you") rakt in i licensbandet och footern. Printytans avslutande tanke ("vem som vinner eller förlorar bestäms inte av tekniken, det bestäms av det pedagogiska valet du redan är expert på") finns alltså bara i PDF:en. Detta är den av de två kända divergenserna som är en ren innehållslucka (sträng helt frånvarande), till skillnad från GDPR-rubriken ovan (sträng identisk, bara nivå/placering skiljer). Ägarens beslut (brevet) är att guiden inte byggs ut för att harmonisera ytorna — raden står kvar som dokumentation, inte som uppgift att åtgärda. |

**Rättelse av brevets egen premiss:** brevet beskriver den andra raden som att "printytans
GDPR-rubrik ... saknas på webbytan." Det stämmer inte ordagrant — rubrikens text finns på
EW, ordagrant, bara en nivå ner (`<h3>` i stället för `<h2>`) och utan egen sida/eyebrow.
Den tredje raden (det avslutande stycket) är däremot exakt den rena frånvaro brevet
beskriver. Se rapporten för samma distinktion i klartext.

## Utfallsräkningen

**36 poster.** Den tidigare versionen av det här avsnittet räknade poster per block
(omslag/läsartilltal, forskningscitat, produktlandskap, reglering) och landade på 33 —
ett tal som redan var fel innan Task 7 (S35 fanns, tillagd av Task 6, och S34 ligger
utanför forskningscitat-blockets S03–S18-spann) och som Task 7 dessutom ändrar genom att
sätta nya verdikt på S04/S05/S06/S08/S34. Task 5C lägger därefter S36 (Gerlich-citatet,
EW-exklusivt, verdikt `falskt`). Den typen av tabell kräver att någon räknar blockgränser
för hand för att hålla den uppdaterad — exakt den risk brevets stoppvillkor varnar för.
Den här versionen räknar i stället **maskinellt ur verdiktkolumnens ledord**, med samma
skript som grindens egen räkning:

```
/usr/bin/python3 -c "
import re, collections
TOK=['står','föråldrat','falskt','obelagt','struket','rättat','lagt till']
c=collections.Counter()
for l in open('docs/guide-facts-ai-for-students.md'):
    if not re.match(r'^\| S\d+ \|', l): continue
    lead=[x.strip() for x in l.strip().strip('|').split('|')][-1].lstrip('*')
    c[next((t for t in TOK if lead.startswith(t)),'UTAN VERDIKT')]+=1
print(dict(c),'summa',sum(c.values()))"
→ {'rättat': 3, 'står': 23, 'struket': 2, 'lagt till': 2, 'obelagt': 2, 'falskt': 4} summa 36
```

| verdikt | antal |
|---|---|
| står | 23 |
| falskt | 4 |
| rättat | 3 |
| struket | 2 |
| lagt till | 2 |
| obelagt | 2 |
| föråldrat | 0 |
| UTAN VERDIKT | 0 |

Summan 23+4+3+2+2+2+0+0 = **36**, lika med det totala postantalet (S01–S36, där S34
ligger utanför forskningscitat-blockets ursprungliga S03–S18-spann, S35 hör till
"Omslaget och läsartilltalet" trots att den står efter S02 i tabellen, och S36 (Task 5C,
Gerlich-citatet) ligger i "Forskningscitaten" men är EW-exklusiv — se "Ytdivergenser").

**Talen ovan gäller per den commit de räknades i (denna uppgifts commit, Task 5C) och blir
inaktuella igen så snart en senare uppgift sätter eller ändrar en verdiktcell. Rundans
sista uppgift räknar om dem maskinellt en sista gång innan leverans — ingen tabell i det
här avsnittet ska någonsin fyllas i för hand.**

## Vaktblocket

```guard
# Engelska ytorna: EW `_unpublished/guides/ai-for-students/index.html` (web)
# + EP `_unpublished/exports/ai-for-students-print-a4-en.html` (print).
# Ingen QS — guiden har ingen quick-start (Johans beslut 2026-10-14). De svenska
# ytorna är frysta och ingår inte i rundan; de får aldrig en rad här.
#
# Guiden stod inte i någon vaktkarta när det här stycket skrevs
# (`surfacecheck.GUIDE_SURFACES` skulle fyllas av en senare uppgift, se spec
# §7) — **UPPDATERAT: kartan fylldes i `e9089ec`, före Task 7.**
# `surfacecheck.GUIDE_SURFACES["ai-for-students"]` bär nu alla fyra ytor, och
# `test_guide_surface_consistency.py` vaktar raderna nedan på riktigt, inte
# bara i väntan. Varje `aktiv`-rad som läggs efter `e9089ec` måste alltså
# redan vid skrivtillfället stå ordagrant på båda engelska ytorna — det är
# inte längre en framtida uppgifts problem.
# BLOCKET ÄR INTE LÄNGRE TOMT: Task 11, rundans första skrivuppgift, lade de
# två första raderna, S01 och S02 — de enda två poster i "Omslaget och
# läsartilltalet" (se tabellen ovan) som krävde en prosaändring i guiden
# snarare än bara ett verdikt.
#
# S01 — läsaretiketten. Omslagets underrubrik (EP) och dess EW-motsvarigheter
# (`og:description`, `<p class="lede">`) är ändrade `teachers and school
# leaders` → `educators`.
#
# UNDANTAGET FRÅN REGEL 3, I KLARTEXT (rättat vid granskningen, se nedan):
# "en kort sträng är strikt starkare än en lång" gäller bara SÅ LÄNGE VARJE
# FÖREKOMST av den korta strängen faktiskt var felet. EW rad ~152 ("A full
# walkthrough of the WISE framework — with separate versions for teachers
# and school leaders — is available...") bär den bara nakna strängen
# `teachers and school leaders` legitimt, om ETT ANNAT dokument
# (WISE-ramverkets egna lärar-/skolledarversioner) — den förekomsten var
# aldrig felet och ska stå kvar. Ett `borttaget`-ankare på den nakna
# strängen hade därför slagit ut som `återinfört` i samma sekund guiden
# läggs i `GUIDE_SURFACES`, mot en mening som aldrig skrevs om. Lösningen är
# INTE att korta ankaret ytterligare utan att FÖRLÄNGA det: raden nedan är
# ankrad på den distinkta ordalydelsen ur den gamla underrubriken —
# `teachers and school leaders who want to choose tools with judgement, not
# hype` — ordagrant tagen ur alla tre borttagna förekomster (EP:s
# `cover__subtitle`, EW:s `og:description` och `<p class="lede">`) och
# frånvarande ur WISE-meningen, som aldrig fortsätter med "who want to
# choose tools...". Samma felklass som `docs/guide-facts-gemini.md` G49
# dokumenterade för `NotebookLM` (en sträng kan inte vaktas som bart
# `borttaget` om en legitim förekomst kvarstår) — skillnaden här är att
# undantaget gäller ANKRINGEN av samma post, inte att posten saknar vaktrad
# helt.
S01 | en | teachers and school leaders who want to choose tools with judgement, not hype | borttaget
S01 | en | for educators | aktiv
#
# S02 — datumstämpeln, samma klass som Apples A13. Satt om från `April 2026`
# till `October 2026` i alla tre förekomster (EP:s `cover__footer` och
# `back-cover__license`, EW:s `cta-fineprint`). Den nakna strängen är
# ankaret, eftersom de två ytorna bär olika ordval runt den — `Updated` kvar
# på EW, inget prefix på EP — samma skillnad som syskonguiderna copilot och
# apple-intelligence redan landat på. Byggaren (`exports/
# build-ai-for-elever-pdf.py`) bär ingen egen datumtext och rördes inte.
S02 | en | April 2026 | borttaget
S02 | en | October 2026 | aktiv
#
# Task 7, Del 1 — de fyra forskningscitaten på sidorna 4 och 6. S03, S07,
# S09 och S10 är orörda (redan `står`, inget skäl att ändra) och får därför
# ingen rad — bara ett fynd som ÄNDRAS får en guardrad.
#
# S04 — OECD-urvalet, sidan 4. Enheten rättad `classrooms` → `schools`;
# talen 150/40 var redan rätta och är orörda. `150 classrooms across 40
# countries` har bara en förekomst i hela guiden (samma mening som S03:s
# citat) och den förekomsten VAR felet, så den korta fulla frasen är ett
# säkert `borttaget`-ankare utan undantag — ordet "classrooms" ensamt hade
# INTE varit säkert, eftersom det citerade OECD-fyndet i samma stycke
# ("the current realities of classrooms") bär samma ord legitimt.
S04 | en | 150 schools across 40 countries | aktiv
S04 | en | 150 classrooms across 40 countries | borttaget
#
# S05/S06 — Wang & Fan-citatet, sidan 6, struket helt (indragen 2026-04-22,
# fel tidskrift, fel studieantal — se källcellerna). Ingen `aktiv`-rad vid
# dessa två id:n: ersättningen lever vid S34, ett eget id, inte en
# korrigering av S05/S06 själva.
# S05:s ankare är namnet, kortast möjligt eftersom `Wang & Fan` inte har
# någon legitim kvarvarande förekomst (hela attributionen är borta).
# S06:s första ankare är `69 studies)` MED den stängande parentesen — bara
# `69 studies` hade krockat med S34:s nya, legitima `69 studies identified)`
# (siffran 69 lever vidare, nu rätt knuten till Deng et al.; se S34).
# S06:s andra ankare är den längre frasen `performance, motivation and
# higher-order thinking`, inte bara `motivation` — den nakna strängen
# `motivation` är nu en SUBSTRÄNG av `affective-motivational states` (S34:s
# nya, korrekta formulering) och skulle ha slagit ut som återinförd mot en
# mening som aldrig skrevs om. Exakt det undantag regel 3 beskriver.
S05 | en | Wang & Fan | borttaget
S06 | en | 69 studies) | borttaget
S06 | en | performance, motivation and higher-order thinking | borttaget
#
# S08 — Kosmyna-förbehållet, sidan 6. Talet `55 percent` är orört (se S07/
# S08:s källceller); bara ett förbehåll LAGT TILL, ingen `borttaget`-rad
# behövs eftersom inget togs bort.
S08 | en | not yet peer-reviewed | aktiv
S08 | en | 18 completing the fourth session | aktiv
#
# S34 — ersättningskällan, sidan 6 (Deng, Jiang, Yu, Lu & Liu, 2024).
# Tre `aktiv`-ankare: författarnamnet (den korrigerade attributionen),
# `69 studies identified` (skiljer sig avsiktligt från S06:s struket-ankare
# genom ordet "identified" — guiden påstår inte att alla 69 ingick i den
# kvantitativa syntesen, bara att de identifierades i sökningen; källan
# meta-analyserade 62), och `affective-motivational states` (källans eget
# begrepp, inte guidens gamla "motivation").
S34 | en | Deng et al. | aktiv
S34 | en | 69 studies identified | aktiv
S34 | en | affective-motivational states | aktiv
#
# S36 — Gerlich-citatet (sidan 6), tillagt av Task 5C. INGEN RAD: EW 1 / EP 0,
# alltså `saknas_på_en_yta` från start — meningen finns bara på webbytan, se
# "Ytdivergenser" ovan för divergensen och S36:s egen cell för källkontrollen
# (verdikt `falskt`: siffran -0.75 hör i källan till ett annat variabelpar).
# Samma princip som IMY i Apple-inventeringen: en sträng som bara står på en
# yta vaktas inte som `aktiv`, oavsett vad en framtida rättning landar på.
#
# Task 8 — regleringsstycket, sidan 11 ("The EU AI Act — what the
# classification means"). S27 (sidan 11, "Both apply...") och S31–S33
# (FERPA, no-single-federal-law, UK GDPR) är redan `står` och fick aldrig
# någon rad — bara ett fynd som ÄNDRAS får en guardrad, samma regel som för
# S03/S07/S09/S10. S28, S29 och S30 ÄNDRADE guidens prosa och får rader här.
#
# S28/S29 — samma stycke, samma mening, rättad i ett svep: "minimal risk" →
# "Minimal or no risk" (S29, ren terminologifix) och styckets sista sats
# omskriven för att skriva ut explicit vad som binder skolan I DAG kontra
# FRÅN ETT DATUM (S28, felklassen brevets amendemang pekade om till). Den
# nakna strängen `minimal risk` förekom en gång per yta och var hela felet
# — inget legitimt kvarvarande bruk — så den är ett säkert `borttaget`-
# ankare utan undantag (regel 3's huvudfall, inte dess undantag).
S29 | en | minimal risk | borttaget
S29 | en | Minimal or no risk | aktiv
S28 | en | 2 February 2025 | aktiv
S28 | en | Article 4 | aktiv
S28 | en | 2 December 2027 | aktiv
S28 | en | Article 16 | aktiv
S28 | en | Article 26 | aktiv
#
# S30 — Artikel 27, konsekvensbedömningen för grundläggande rättigheter.
# Guiden saknade den helt (`lagt till`, se S30:s cell för skälet till att
# ordet landade i S28:s mening på sidan 11 i stället för intill DPIA-
# meningen på sidan 21, som ligger i Task 10:s eget sidspann). Ankaret är
# artikelnumret, inte "fundamental-rights impact assessment" eller någon
# annan omskrivning — kortast möjligt enligt regel 3.
S30 | en | Article 27 | aktiv
#
# Task 9 — Del 3, sidorna 14–16: 1:1-eran och produktlandskapet.
#
# S16 — Zheng-citatet (sidan 14), struket helt, Johans beslut vid grinden
# (ägarbeslut 1). Ingen ersättning vid denna id — kedjan ("the research
# record is clear and internationally consistent") bärs nu ensam av S03/
# S12/S13 (PISA), S14/S15 (Carter) och S17/S18 (Unos Uno), alla `står` —
# stycket är läst i sin helhet efter borttagningen (se Task 9-rapporten).
# `Zheng` förekommer bara en gång i hela guiden (den struckna meningen) och
# är därför ett säkert kort ankare utan undantag — ingen annan mening
# nämner författaren.
S16 | en | Zheng | borttaget
#
# S15/S18 — de två tal som nu bär stycket utan Zhengs hedge. Värdena själva
# är orörda (bara Zheng-meningen föll), men de får sin första vaktrad i den
# här rundan eftersom de nu ensamma bär argumentet på sidan.
S15 | en | 0.18 standard deviations | aktiv
S18 | en | 11 municipalities | aktiv
#
# S19 — marknadsledarna (sidan 15), omformulerad utan rangordning (Task 4:s
# mätning, `obelagt` → `rättat`). `The largest chatbots` förekom en gång och
# var hela felet (den implicerade rangordningen); ingen legitim kvarvarande
# förekomst.
S19 | en | The largest chatbots | borttaget
S19 | en | Two chatbots dominate | aktiv
#
# S20 — Copilots modellpåstående, `falskt` enligt Task 4:s mätning mot
# förstapartskällor (korsref mot guide-facts-copilot.md gick inte att
# utföra, se källcellen). Det gamla ankaret är brevets egen ordalydelse
# (steg 6-exemplet); det nya citerar Microsofts eget uttryck.
S20 | en | Copilot is built on ChatGPT | borttaget
S20 | en | a broader system | aktiv
#
# S22–S24 — de tre K-12-produktnamnen, orörda i sak (verdikt står) och
# INTE rättade av den här uppgiften (brevets egen instruktion: "rör dem
# inte"), men de får sin första vaktrad nu eftersom stycket runt dem
# skrivs om i samma svep — namnen, inte meningarna om dem.
S22 | en | Khanmigo | aktiv
S23 | en | MagicSchool | aktiv
S24 | en | ChatGPT for Teachers | aktiv
#
# S25 — Khanmigo-undantaget, Johans beslut vid grinden (ägarbeslut 2).
# Guiden namnger nu Khanmigo explicit, i samma mening som påståendet att
# majoriteten saknar vyn, och styrker det med produktens egen
# funktionsbeteckning i stället för en guide-konstruerad beskrivning.
S25 | en | Summarize Student Chat History | aktiv
#
# S37 (NY POST, upptäckt och struken av Task 9) — "SchoolAI" var redan
# guidens undantagsclaim innan den här rundan (arv från guide-designens
# spec från april 2026), men ingen uppgift i rundan mätte eller belade den
# — den stod utanför Task 1:s 25 kandidater och Task 4:s sex produktposter.
# Med Khanmigo nu namngivet som "undantaget" (S25, ägarbeslut 2) hade en
# kvarlämnad SchoolAI-mening gjort sidan till sin egen motsägelse: två
# olika, obelagda "undantag" i samma stycke. Struken utan ersättning vid
# DENNA id — ersättningen (Khanmigo) lever vid S25, inte som en rättning av
# S37 självt. `SchoolAI` förekom en gång per yta och var hela den struckna
# meningen; inget legitimt kvarvarande bruk.
S37 | en | SchoolAI | borttaget
#
# Resten av blocket fylls av senare uppgifter, i takt med att de skriver om
# guidens prosa för S09–S14, S27, S31–S33 (resten av forskningscitaten och
# regleringen) — samma mönster som Apple-rundans A-rader. Varje ny `aktiv`-
# rad ska bära det KORTASTE värde som bär påståendet (ett tal, ett namn, en
# tidskriftstitel) — aldrig hela satsen (se regel 3 i huvudet ovan). En rad
# krävs ordagrant på BÅDA engelska ytorna för `aktiv`; en kandidat som bara
# träffar en yta får ingen rad, bara en notering i prosan (samma hantering
# som Apples IMY-divergens).
```

