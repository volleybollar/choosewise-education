# Påståendeinventering — ai-for-students-guiden (educators-rundan)

**Rundan:** elevguiden görs om till en guide för engelskspråkiga educators — samma ämne
(elevers AI-användning i klassrummet), uttalad läsare. Task 1 av 16 (denna fil) är
rundans arbetsorder: ingen senare uppgift skriver en mening i guiden förrän den finns.
Spec: `docs/superpowers/specs/2026-10-14-ai-for-students-educators-design.md`, inklusive
§1-amendemanget (sidantalet är 22 sidor, inte 16 — specens eget tal var fel, mätt ur
`pdftotext` med formfeed, inte ur `grep -c 'class="page"'`).
**Upprättad:** 2026-10-14
**Faktakontrollerad:** ja, klar. Task 2–5 fyllde källkolumnen och verdikten
(forskningscitaten mot primärkälla, produktlandskapet mot källa eller korsref,
regleringen mot Apple-inventeringens A33–A39); Task 7–13 skrev om guidens prosa efter
dem; **fixvågen 2026-10-15** lade rundans sista sju poster (S38–S44) efter
helgranskningen och räknade om utfallstabellen maskinellt. Varje rad bär ett verdikt
och en källa. De tre Task 1-meningar som sa motsatsen (den här raden, "Ingen post i den
här filen bär ännu något av dessa ord" i taxonomiavsnittet och "Resten av blocket fylls
av senare uppgifter" i vaktblockets slut) var sanna när de skrevs och blev osanna av
rundans eget arbete — de är städade av fixvågen, inte strukna tyst.

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

## Sidkartan (uppdaterad av fixvågen 2026-10-15 efter omrendering — ersätter Task 14:s mätning, som i sin tur ersatte specens §1-amendemang)

Mätt ur den renderade PDF:en med `pdftotext`, tecken per sida, blanktecken kollapsade
men aldrig borttagna. **Fortfarande 22 sidor** efter fixvågens innehållsändringar —
ingen avdelningssida har flyttat (3, 7, 13, 17 är desamma före och efter, i alla tre
mätningar). Detta är NÄSTA rundas referens för ompaginering.

`tkn (Task 14)` är läget när Task 14 renderade om, alltså talen i den förra versionen av
det här avsnittet; `tkn (fixvågen)` är läget efter helgranskningens rättelser. Fem sidor
ändrades, och varje ändring spåras till ett granskningsfynd:

- sida 4: 1771 → 1772 tkn — **M7**, ellipsen i OECD-citatet (+1 tecken)
- sida 12: 1099 → 1175 tkn, **+7 %** — **I7**, GDPR-punkten omskriven utan produktnamn
- sida 14: 2336 → 2365 tkn — **I1**, `translated from the Swedish` tillagt vid
  Grönlund-citatet
- sida 15: 3022 → 2949 tkn, **−2 %** — **C1** (attributionen borta, rubriken `Where to
  start`) och **I2** (rubriken omskriven); sidan är fortfarande guidens tyngsta
- sida 20: 2270 → 2233 tkn — **C1**, FAQ-svarets attribution borta

Totalt 33 740 → 33 736 tecken: rundan tog bort två obelagda attributioner och lade till
en översättningsmärkning, en ellips och en längre GDPR-formulering, och det jämnade ut
sig nästan exakt.

| sida | innehåll | tkn (Task 14) | tkn (fixvågen) |
|---|---|---|---|
| 1 | omslaget (datumstämpeln struken, S02) | 257 | 257 |
| 2 | Introduction — "The question isn't technical" | 2432 | 2432 |
| 3 | **Part 1-avdelare** — "Learning is the point" | 712 | 712 |
| 4 | "If the tool elevates learning" — **OECD *Unlocking High-Quality Teaching*** (citatet nu elliderat, S03/M7) | 1771 | 1772 |
| 5 | WISE-ramverket | 1740 | 1740 |
| 6 | "Challenging thinking, or replacing it" — **Deng et al., Kosmyna, Lee** | 2435 | 2435 |
| 7 | **Part 2-avdelare** | 257 | 257 |
| 8 | "Teacher knowledge isn't a bonus" — **UNESCO-ramverket** | 1521 | 1521 |
| 9 | källkritik, bias, hallucinationer | 1784 | 1784 |
| 10 | "Teachers don't need to know the tech better" | 1696 | 1696 |
| 11 | **GDPR och AI Act** | 2874 | 2874 |
| 12 | **GDPR i praktiken** — punkten om biträdesavtal omskriven utan produktnamn (S42/I7) | 1099 | 1175 |
| 13 | **Part 3-avdelare** | 237 | 237 |
| 14 | 1:1-eran — **PISA 2015, Carter 2017, Unos Uno**; Grönlund-citatet märkt som översättning (S39/I1) | 2336 | 2365 |
| 15 | **The visibility gap** — rubriken rättad (S25/I2), UNESCO/OECD-attributionen struken, rubriken "Where to start" (S38/C1) | 3022 | 2949 |
| 16 | klassrumshantering | 1688 | 1688 |
| 17 | **Part 4-avdelare** | 184 | 184 |
| 18 | checklistan: pedagogik, förutsättningar | 951 | 951 |
| 19 | checklistan: tillsyn, uppföljning | 1330 | 1330 |
| 20 | FAQ, första halvan — attributionen i "I don't know AI myself" struken (S38/C1) | 2270 | 2233 |
| 21 | FAQ, andra halvan — **AI Act-svaret, DPIA-svaret**, AI-detektorsvaret (S43/M1) | 2420 | 2420 |
| 22 | slutcitatet och licensbandet | 724 | 724 |

Forskningscitaten sitter på fyra sidor (4, 6, 8, 14), produktlandskapet på en (15), och
läsaretiketten `teachers and school leaders` står på EN plats i PDF:ens sidkarta:
omslaget. **Stoppvillkoret är kontrollerat efter omrenderingen och är grönt:** ingen sida
under 400 tecken utom omslaget och de fyra avdelningssidorna (s3, s7, s13, s17 — korta
med avsikt). Den tunnaste icke-undantagna sidan är fortfarande slutsidan, 724 tecken,
oförändrad.

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

**Varje post i den här filen bär nu ett av dessa ord.** Verdiktkolumnen var tom på alla
rader när Task 1 skrev skelettet; Task 2–5 fyllde den och fixvågen 2026-10-15 fyllde de
sista sju raderna (S38–S44). En tom cell skulle betyda "inte klassificerad än", inte
"står" — men ingen finns kvar, och räkningen i "Utfallsräkningen" nedan mäter det
maskinellt (`UTAN VERDIKT` ska vara 0).

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

**Förekomstkolumnernas konvention, EN enda, fastställd av fixvågen 2026-10-15
(granskningsfynd I5):** `EW`- och `EP`-talen är **FÖRE-värden**. De mäter postens sträng
i källfilerna som de stod i rundans **bascommit `c66ee5c`**, alltså vad rundan mötte —
inte vad den lämnade efter sig. Efter-läget mäts med ett `grep` när som helst och
behöver därför ingen kolumn; före-läget går inte att återskapa utan en commit-referens,
och det är det som gör det värt en kolumn. **Varje rad är omräknad mot `c66ee5c` i
fixvågen**, och fyra rader som bar efter-värden är rättade: S05 (`Wang &amp; Fan`,
0/0 → 1/1), S37 (`SchoolAI`, 2/2 → 1/1), S34 (Deng et al., 1/1 → 0/0 — posten är `lagt
till`, strängen fanns inte i bascommiten) samt S06 (`69 studies`, 0/0 → 1/1, som var fel
under BÅDA läsningarna: strängen stod i bascommiten och står kvar i dag, nu knuten till
S34:s nya mening).

**Enheten är rå `grep -c`** — antal matchande RADER i källfilen, inte antal förekomster,
och inte mätt mot `surfacecheck.normalise()`. **Ett dokumenterat undantag i enhet, inte i
tidpunkt:** S35 (löptextens läsartilltal) räknar ordgränsmatchningar i den renderade
löptexten, inte rader, vilket dess egen cell skriver ut — reproducerat i fixvågen mot
`c66ee5c`: `you` 42 (EW) / 37 (EP), `your` 19/18, `we` 7/9, exakt cellens tal.

**Två poster har 0 på en yta** och är därmed `saknas_på_en_yta`: S36 (Gerlich-citatet,
EW 1 / EP 0) och S44 (Discovery Education-attributionen, EW 1 / EP 0). Ingen av dem kan
få en `aktiv`-vaktrad; båda står i stället i "Ytdivergenser" nedan. Alla övriga poster
har minst en förekomst på båda ytorna i bascommiten.

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
| S03 | `Unlocking High-Quality Teaching` — OECD-rapportens titel, april 2025, citerad med nyckelfyndet om lärarkvalitet |  1 |  1 | oecd.org/en/publications/unlocking-high-quality-teaching_f5b82176-en.html → **403** direkt (OECD blockerar bot-UA); Wayback-capture 2026-10-09 → **200**, ordagrant 2026-10-14: "In an era defined by rapid innovation and constant change, it is tempting to focus on the latest trends or technologies that promise transformative change. However, refining existing teaching practices by closely examining the current realities of classrooms can be a powerful – and even potentially safer – approach to addressing stagnating student achievement, as seen across PISA participating countries." Publicerad **3 april 2025**. Rapportens egen slutsats, ordagrant: "no other factor within schools has a greater impact on students' academic success and overall achievement than the quality of teaching." | **står.** Titeln, utgivningsmånaden (april 2025) och det långa citatet är ordagrant belagda — guidens citat är en trogen men tyst avkortad delmängd av källans mening (källan fortsätter ", as seen across PISA participating countries" efter "stagnating student achievement"; ingen ordskillnad i den del som faktiskt citeras, ingen ellips markerade klippet — **rättat av fixvågen 2026-10-15, granskningsfynd M7:** citatet slutar nu `stagnating student achievement …"` på båda ytorna, så avkortningen är synlig för läsaren i stället för tyst. Ingen annan del av citatet är rörd, och inget ord är tillagt eller taget bort. Slutsatsen att inget skolinternt påverkar elevresultat mer än undervisningens kvalitet är rapportens egen formulering, inte guidens tolkning. Se **S04** för talen 150/40, som INTE står som skrivna. |
| S04 | `150 classrooms` — OECD-rapportens urval, ordagrant "150 classrooms across 40 countries" |  1 |  1 | oecd.org/en/publications/unlocking-high-quality-teaching_f5b82176-en.html (samma sida som S03; Wayback-capture 2026-10-09) → **200**, ordagrant 2026-10-14: "It also has built on the qualitative insights of more than 150 schools from 40 countries to better understand the complex realities of implementing these practices in day-to-day teaching." Källan skriver **150 skolor** i 40 länder, inte "150 classrooms across 40 countries" som guiden skriver. | **rättat.** Talen 150 och 40 var rätta, men enheten var fel: rapporten är grundad på **150 skolor**, inte 150 klassrum — "schools" och "classrooms" är inte utbytbara i en rapport som själv handlar om skillnaden mellan skolnivå och lektionsnivå. Det var exakt den farliga klassen fynd: ett tal som ser rätt ut men bär fel ord. Guidetexten är rättad på båda engelska ytorna (EP rad ~340, EW rad ~123), 2026-10-15 (Task 7): `150 classrooms across 40 countries` → `150 schools across 40 countries`. Talen 150/40 själva var redan rätt och är orörda. |
| S05 | `Wang &amp; Fan` — meta-analysens författarnamn, *Computers &amp; Education*, 2025 |  1 |  1 | nature.com/articles/s41599-025-04787-y → **200** (hämtad med webbläsar-UA; samma URL gav 403 mot ett vanligt verktygsanrop), ordagrant 2026-10-14: sidans egen rubrik bär nu prefixet "RETRACTED ARTICLE:"; sidans metadata anger tidskriften som "humanities and social sciences communications", volym 12(1); brödtexten: "This article was retracted on 22 April 2026." nature.com/articles/s41599-026-07310-z (Retraction Note) → **200**, ordagrant: "The Editor has decided to retract this article due to concerns relating to discrepancies in the meta-analysis. ... Taken together, the identified issues undermine the Editor's confidence in the validity of the analysis and the conclusions drawn from it. The authors have not responded to correspondence regarding this retraction." | **struket.** Författarnamnen Wang & Fan stämde, men tidskriften gjorde inte — artikeln stod i *Humanities and Social Sciences Communications*, inte i *Computers & Education*, som aldrig har publicerat den. Allvarligare: artikeln är **indragen (retracted) 2026-04-22**, av redaktören själv, på grund av "discrepancies in the meta-analysis" som undergräver förtroendet för analysen och dess slutsatser — författarna har inte svarat på förfrågan. Att hänga ett guide-stycke på en indragen studie är den farligaste sortens fynd i den här rundan. Attributionen `Wang & Fan` är struken ur guidetexten på båda engelska ytorna (sidan 6), 2026-10-15 (Task 7) — utan ersättning vid DENNA post: den positiva sidan av avsnittet bärs nu av en annan, egen post, **S34**, med sin egen vaktrad. Se **S06** för studieantalet, också struket. |
| S06 | `69 studies` — antalet studier i Wang &amp; Fan-metaanalysen |  1 |  1 | nature.com/articles/s41599-025-04787-y (samma artikel som S05) → **200**, ordagrant 2026-10-14: "This study aimed to assess the effectiveness of ChatGPT in improving students' learning performance, learning perception, and higher-order thinking through a meta-analysis of **51 research studies** published between November 2022 and February 2025." och: "Table 3 presents the 72 effects obtained from the coding of the 51 studies..." Källan skriver 51 studier (72 effektstorlekar ur dem), inte 69. | **struket.** Metaanalysen omfattade **51 studier**, inte 69 — och artikeln är dessutom indragen (se S05): två oberoende skäl att stryka påståendet, inte bara rätta talet. Ett tredje: källans egna tre utfallsmått var "learning performance, learning perception, and higher-order thinking" — guidens tredje ord "motivation" förekom i artikeln bara som ett delfynd i en annan, citerad understudie (Niloy et al.), inte som ett av Wang & Fan-metaanalysens egna tre mått. Guidens "performance, motivation and higher-order thinking" var alltså inte källans egna tre utfall. Hela frasen `69 studies` och attributionen till Wang & Fan är struken ur guidetexten på båda engelska ytorna (sidan 6), 2026-10-15 (Task 7). Talet 69 lever vidare i guiden, men nu korrekt knutet till **S34** (Deng et al., som oberoende av denna sammanblandning faktiskt identifierade 69 artiklar) — se S34 för kontrollen av att det inte bara är samma fel i ny form. |
| S07 | `Kosmyna` — MIT Media Lab EEG-studien (Kosmyna et al., 2025) |  1 |  1 | arxiv.org/abs/2506.08872 → **200**, ordagrant 2026-10-14: titel "Your Brain on ChatGPT: Accumulation of Cognitive Debt when Using an AI Assistant for Essay Writing Task", "by Nataliya Kosmyna and 7 other authors", inlämnad "[v1] Tue, 10 Jun 2025". Fulltexten (arxiv.org/pdf/2506.08872) märker sig själv, sidfot på varje sida: "Preprint, under review" — inte kollegialt granskad ännu. | **står** på namn, institution (MIT Media Lab, synligt i inlämningsloggens avsändaradress) och år (2025). **Förbehåll som guiden saknar, se S08:** studien är fortfarande en preprint under granskning, inte en publicerad peer review-artikel. |
| S08 | `55 percent` — "up to 55 percent lower brain connectivity" i Kosmyna et al. |  1 |  1 | arxiv.org/pdf/2506.08872 (fulltext, s. 145) → **200**, ordagrant 2026-10-14: "The LLM group showed the least extensive connectivity, with up to 55% reduced total dDTF magnitude compared to the Brain-Only group in low-frequency semantic and monitoring networks." Urval, ordagrant ur abstractet: "A total of 54 participants took part in Sessions 1-3, with 18 completing session 4." Varaktighet, ordagrant: "Over four months, LLM users consistently underperformed at neural, linguistic, and behavioral levels." | **lagt till.** Talet självt stod redan rätt — 55 procent är exakt vad källan skriver, för måttet total dDTF-anslutning i lågfrekventa semantiska/övervakande nätverk jämfört med Brain-Only-gruppen; guidens "lower brain connectivity" är en förenkling av det måttet men ingen felaktig siffra, och talet 55 percent är orört. Men guiden saknade helt **de två förbehåll** källan bär: urvalet är litet (54 deltagare i sessionerna 1–3, bara 18 i den fjärde) och studien är en preprint under granskning, inte en publicerad artikel (se S07). Dessa två förbehåll är nu skrivna in i guidetexten på båda engelska ytorna (sidan 6), 2026-10-15 (Task 7), som en parentes direkt efter `Kosmyna et al.`: "— a preprint, not yet peer-reviewed, with 54 participants and only 18 completing the fourth session". |
| S09 | `Lee et al` — Microsoft Research-studien, CHI 2025 |  1 |  1 | microsoft.com/en-us/research/wp-content/uploads/2025/01/lee_2025_ai_critical_thinking_survey.pdf → **200** (hämtad via webbläsarläsning; samma URL 403:ar mot ett vanligt verktygsanrop), ordagrant 2026-10-14: "The definitive version was published in CHI 2025, https://doi.org/10.1145/3706598.3713778." Författare enligt samma pdf: Hana Lee m.fl. (Lee, Sarkar, Tankelevitch, Drosos, Rintel, Banks m.fl.), Microsoft Research. | **står.** Microsoft Research är avsändaren, CHI 2025 är konferensen (DOI 10.1145/3706598.3713778), och Lee är försteförfattare — guidens attribution håller. |
| S10 | `319 knowledge workers` — antalet deltagare i Lee et al. |  1 |  1 | microsoft.com/en-us/research/wp-content/uploads/2025/01/lee_2025_ai_critical_thinking_survey.pdf (samma pdf som S09; URL:en upprepad av fixvågen 2026-10-15 enligt regeln att varje källcell står på egna ben, granskningsfynd M6) → **200**, ordagrant 2026-10-14: "We survey 319 knowledge workers to investigate 1) when and how knowledge workers perceive the enaction of critical thinking when using GenAI, and 2) when and why GenAI affects their effort to do so." Nyckelfyndet, ordagrant: "confidence in GenAI is associated with less critical thinking, while higher self-confidence is associated with more critical thinking." | **står.** 319 är rätt, och riktningen i guidens påstående — hög tillit till AI går ihop med mindre kritiskt tänkande — är studiens egen slutsats, ordagrant. |
| S11 | `AI Competency Framework` — UNESCO:s ramverkstitel, 2024 (*AI Competency Framework for Teachers*) |  1 |  1 | unesco.org/en/articles/ai-competency-framework-teachers → **200**, ordagrant 2026-10-14: sidrubriken "Publication AI competency framework for teachers", publiceringsdatum direkt under rubriken: "8 August 2024" (uppdaterad "16 January 2026"). Brödtexten på samma sida återger titeln i den versalform guiden använder: "The AI Competency Framework for Teachers addresses this gap by defining the knowledge, skills, and values teachers must master in the age of AI." Citeringsraden på samma sida: "Miao, Fengchun UNESCO Cukurova, Mutlu 2024". **Tillägg, Task 10 (2026-10-15), samma URL:** granskningen hämtade unesco.org/en/articles/ai-competency-framework-teachers på nytt och fann, ordagrant: "the publication outlines 15 competencies across five dimensions" — exakt den strukturdetalj guidens stycke på sidan 8 också påstår ("15 competencies across five dimensions"). Talen är alltså sanna, inte bara titeln/året; cellen belade dem inte förut. **Tillägg, fixvågen 2026-10-15 (granskningsfynd M3), primärkällan själv:** unesco-asp.dk/wp-content/uploads/2025/02/AI-Competency-framework-for-teachers_UNESCO_2024.pdf (UNESCO:s egen pdf, 52 sidor) → **200**, `pdftotext` 2026-10-15, ordagrant: "the publication outlines 15 competencies across five dimensions: Human-centred mindset, Ethics of AI, AI foundations and applications, AI pedagogy, and AI for professional learning. These competencies are categorized into three progression levels: Acquire, Deepen, and Create." Det är de FEM DIMENSIONSNAMNEN ordagrant — det som cellen tidigare inte belade. | **står.** Titeln ("AI Competency Framework for Teachers", som den faktiskt förekommer i sidans brödtext — sidrubriken själv bär gemener, "AI competency framework for teachers", men det är samma dokument) och året (2024, publicerad 8 augusti 2024) är ordagrant belagda på UNESCO:s egen sida. **Läst mot sidan 8 i Task 8 (2026-10-15):** stycket "Teacher knowledge isn't a bonus — it's a prerequisite" skriver "In 2024 UNESCO published its *AI Competency Framework for Teachers*" — exakt titel och år, ordagrant samma som denna källcell belägger. **Ingen ändring behövde göras.** Noterat uttryckligen eftersom en post som stämmer aldrig stryks tyst (inventeringens regel 2). **Rättat av Task 10 (2026-10-15):** detaljen "15 competencies across five dimensions" i samma stycke låg tidigare utanför vad den här källcellen verifierade (cellen styrkte bara titel, upphovsmän och år) — nu är den också belagd, ordagrant mot samma URL (se källcellen). Ingen ändring i guidetexten; bara citatet i inventeringens egen cell var det som saknades. **Tillägg, fixvågen 2026-10-15 (granskningsfynd M3): guidens uppräkning av de fem dimensionerna är en PARAFRAS, inte UNESCO:s rubriker.** Guiden skriver "among them a human-centred mindset, AI ethics, foundational AI understanding, AI pedagogy, and AI to support one's own learning"; UNESCO skriver "Human-centred mindset, Ethics of AI, AI foundations and applications, AI pedagogy, and AI for professional learning" (se källcellen). Tre av fem är omskrivna — "AI ethics" för "Ethics of AI", "foundational AI understanding" för "AI foundations and applications", "AI to support one's own learning" för "AI for professional learning". **Ingen ändring i guidetexten:** parafrasen är inte felaktig i sak (varje omskrivning pekar på samma dimension), guiden markerar den själv med "among them" i stället för att presentera den som citat, och specen §6 klass 1:s strykningsregel gäller citat som inte går att belägga — inte en parafras vars original nu står ordagrant i källcellen ovan. Märkningen hör i den här posten; en läsare som vill UNESCO:s egna rubriker finner dem här. |
| S12 | `Students, Computers and Learning` — OECD PISA-rapportens titel, 2015 |  1 |  1 | oecd.org/content/dam/oecd/en/publications/reports/2015/09/students-computers-and-learning_g1g57f3a/9789264239555-en.pdf → **200**, ordagrant 2026-10-14, kolofonsidans citeringsrad: "OECD (2015), Students, Computers and Learning: Making the Connection, PISA, OECD Publishing." Förordet, ordagrant: "students who use computers very frequently at school do a lot worse in most learning outcomes, even after accounting for social background and student demographics." | **står.** Titeln och året (2015) är rapportens egna (pdfinfo bekräftar 204 sidor, samma fil). Kontrollen för socioekonomisk bakgrund är rapportens egen formulering ("social background and student demographics"), inte ett tillägg från guiden. Se **S13** för termen "digital paradox", som INTE förekommer i den här texten. |
| S13 | `digital paradox` — PISA-rapportens fynd, återgivet som etikett. Att termen är rapportens egen, inte en sekundärkällas, är en av de saker som ska verifieras |  1 |  1 | oecd.org/content/dam/oecd/en/publications/reports/2015/09/students-computers-and-learning_g1g57f3a/9789264239555-en.pdf → **200**, helfilssökning 2026-10-14: strängen "paradox" (skiftlägesokänsligt) förekommer **noll gånger** i rapportens samtliga 204 sidor (`grep -c -i paradox` på den fulla `pdftotext`-utskriften → 0). Sekundärkällor använder termen om samma fynd — t ex en substack-artikel med rubriken "The Digital Paradox: Navigating the Pushback on Classroom Technology" och spansk press ("PISA y la paradoja digital", El Heraldo de México) — men ingen av dem är OECD självt. | **står.** Guiden hedgar redan korrekt: "what became known as the 'digital paradox'" påstår inte att OECD myntade termen, bara att fyndet senare fick den etiketten av andra — och det stämmer, rapporten använder aldrig ordet. Hedgen "became known as" räcker för att skilja fyndet (rapportens eget, se S12) från etiketten (en sekundärkällas). |
| S14 | `Carter, Greenberg` — RCT vid US Military Academy, 2017 (Carter, Greenberg & Walker) |  1 |  1 | doi.org/10.1016/j.econedurev.2016.12.005 → omdirigerar till sciencedirect.com/science/article/abs/pii/S0272775716303454 → **403** direkt (Elsevier blockerar bot-UA, samma mönster som OECD/Nature/Microsoft i Task 2; ingen Wayback-capture finns för den sidan, kontrollerat mot `archive.org/wayback/available`). Läst i stället via en kurssajts spegling av exakt samma publicerade artikel-PDF (people.it.tamu.edu/~w-arthur/302/Payne et al (2017) Economics of Educ Review...pdf), vars sidhuvud och artikelhistorik bekräftar att det är den publicerade versionen, inte arbetspappret: "Economics of Education Review 56 (2017) 118–132 ... The impact of computer usage on academic performance: Evidence from a randomized trial at the United States Military Academy ... Susan Payne Carter, Kyle Greenberg∗, Michael S. Walker ... Published by Elsevier Ltd." samt "Received 5 July 2016, Revised 8 December 2016, Accepted 9 December 2016, Available online 14 December 2016" → **200** (ordagrant 2026-10-14). | **står.** Författarnamnen, institutionen (United States Military Academy) och designen — "a study that prohibited computer devices in randomly selected classrooms of an introductory economics course" — är ordagrant belagda i den publicerade artikeln. Se **S15** för effektstorleken och utfallsmåttet. |
| S15 | `0.18 standard deviations` — effektstorleken i Carter, Greenberg & Walker |  1 |  1 | doi.org/10.1016/j.econedurev.2016.12.005 → omdirigerar till sciencedirect.com/science/article/abs/pii/S0272775716303454 → **403** direkt (samma blockering som S14; ingen Wayback-capture finns för sidan). Läst via samma kurssajts-spegling som S14 (people.it.tamu.edu/~w-arthur/302/Payne et al (2017) Economics of Educ Review...pdf) → **200**, ordagrant 2026-10-14, abstractet: "Average final exam scores among students assigned to classrooms that allowed computers were 0.18 standard deviations lower than exam scores of students in classrooms that prohibited computers." Kontrollerat mot arbetspappret (Blueprint Labs Discussion Paper #2016.02, maj 2016, blueprintcdn.com): dess abstract bär SAMMA tal, "18 percent of a standard deviation lower" — den siffra som skiljer sig inom arbetspappret (0.21, en okontrollerad delskattning i Tabell 3 kolumn 1, mot 0.18, den fullt kontrollerade skattningen i kolumn 4: "remains statistically significant at -0.18σ") finns inom samma dokument, inte mellan arbetspapper och publicerad version. | **står.** 0.18 standardavvikelser är exakt det publicerade abstractets eget tal, för utfallsmåttet "final exam scores" (det sammansatta provresultatet), i en design med slumpmässig tilldelning av datoranvändning per klassrum. Brevets varnade felklass (olika tal i arbetspapper kontra publicerad artikel) kontrollerades uttryckligen och inträffade inte här — båda versionerna landar på 0.18 som sin huvudsiffra. |
| S16 | `Zheng et al` — meta-analysen i *Review of Educational Research*, 2016 |  1 |  1 | journals.sagepub.com/doi/10.3102/0034654316628645 → **403** direkt (Cloudflare-utmaning mot botanrop). Wayback-capture 2026-05-05 (web.archive.org/web/20260505071154/https://journals.sagepub.com/doi/abs/10.3102/0034654316628645) → **200**, ordagrant 2026-10-14 — men visar bara abstractet bakom en uttrycklig betalvägg-markering, "Get full access to this article": "Over the past decade, the number of one-to-one laptop programs in schools has steadily increased. ... A meta-analysis of 10 studies examines the impact of laptop programs on students' academic achievement, finding significantly positive average effect sizes in English, writing, mathematics, and science." Tidskrift/volym/år bekräftat separat i ERIC:s förlagslämnade abstract (eric.ed.gov/?id=EJ1121563 → **200**, 2026-10-14): "Review of Educational Research, v86 n4 p1052-1084 Dec 2016." Fulltexten är obelagd trots sökning: OpenAlex (api.openalex.org/works/doi:10.3102/0034654316628645) → "is_oa": false, "any_repository_has_fulltext": false; Unpaywall → "oa_status": "closed"; ResearchGate och HKU Scholars Hub svarade **403**; oa.mg hade ingen PDF. Det enda ställe villkorsformuleringen faktiskt hittades var ett UCI-pressmeddelande/ScienceDaily-referat (sciencedaily.com/releases/2016/04/160426110655.htm): "can improve educational outcomes when there is teacher buy-in, suitable technical support and professional development for teachers, and appropriate implementation with the curriculum." | **struket.** Var `obelagt` för villkoret: tidskrift (*Review of Educational Research*), volym/sidor (86(4):1052–1084) och år (2016) stod belagda mot det hämtbara abstractet, men villkoret guiden hängde halva sitt argument på — "positive effects existed, but only where teachers integrated the devices pedagogically" — uttalades inte i abstractet, och fulltexten är overifierbar bakom en betalvägg utan laglig gratiskopia (se sökningen i källcellen). Den enda formulering som fångar villkoret är ett pressmeddelande/referat, och brevets regel diskvalificerar uttryckligen en sammanfattning eller ett pressmeddelande som belägg för en primärkälla. **Ägarens beslut vid rundans grind (2026-10-15), genomfört av Task 9:** hela citatet, inte bara villkoret, är struket ur guidetexten på båda engelska ytorna (sidan 14) — utan ersättning vid DENNA post. Skälet: att behålla citatet utan villkoret hade gjort påståendet starkare i FEL riktning, eftersom det enda verifierade i källan (källcellen ovan) är att metaanalysen fann POSITIVA effekter i engelska, skrivande, matematik och naturvetenskap — motsatsen till vad stycket använde citatet till. Stycket bygger en kedja ("the research record is clear and internationally consistent"); borttagningen är läst mot hela stycket, inte bara mot meningen, och de tre kvarvarande citaten på samma sida — PISA 2015 (S03/S12/S13), Carter, Greenberg & Walker 2017 (S14/S15) och Unos Uno (S17/S18), alla `står` — bär kedjan ensamma, i samma riktning, utan Zhengs hedge. Se Task 9-rapporten för hela stycket citerat efter borttagningen. |
| S17 | `Unos Uno` — Grönlund et al., Örebro universitet, 2011–2014 |  1 |  1 | diva-portal.org/smash/get/diva2:706366/FULLTEXT01.pdf (Grönlund, Åke. *Att förändra skolan med teknik: Bortom "en dator per elev"*, Örebro universitet, 2014, ISBN 978-91-7668-992-9) → **200**, ordagrant 2026-10-14, förordet: "Den här boken bygger på erfarenheterna från projektet Unos Uno som under åren 2011–2013 arbetat systematiskt med att utveckla skolan med hjälp av informations- och kommunikationsteknik (it). Ett tjugotal skolor i elva kommuner och en friskolekoncern har deltagit." Tryckår enligt kolofonsidan: 2014. | **står.** Grönlund och Örebro universitet är rapportens egna uppgifter; projektperioden 2011–2013 plus utgivningsåret 2014 täcker guidens "2011–2014" utan motsägelse. **Medveten anmärkning enligt brevet:** källan är svensk (Örebro universitet, DiVA), men guiden ramar den som "the most cited Nordic longitudinal study" — en internationellt citerbar beskrivning som inte kräver svensk läsarkontext. Posten står kvar av det skälet; den ska INTE strykas som en nationell referens i en senare runda. |
| S18 | `11 municipalities` — Unos Uno-studiens omfång, ordagrant "roughly 20 schools in 11 municipalities" |  1 |  1 | diva-portal.org/smash/get/diva2:706366/FULLTEXT01.pdf (Grönlund, Åke. *Att förändra skolan med teknik: Bortom "en dator per elev"*, Örebro universitet, 2014) → **200**, ordagrant 2026-10-14. Omfånget, samma mening som S17: "Ett tjugotal skolor i elva kommuner och en friskolekoncern har deltagit" — matchar guidens "roughly 20 schools in 11 municipalities" nästan ordagrant (guiden utelämnar bara friskolekoncernen). **Not om intern variation i källan:** på ett annat ställe i samma bok skriver författaren i stället "tio kommuner, en friskoleorganisation och SKL" — en avvikande räkning inom samma dokument; guidens tal (11) är förordets egen formulering, inte en guidekonstruktion, så det ändrar inte verdikten. Utfall 1, ordagrant: "Andelen enskilt arbete ökar generellt" (bekräftar att ensamarbetet ökade). Utfall 2, ordagrant: "Sociala medier är en mycket stor källa till distraktion vilket skapar stress hos många elever eftersom de försummar arbetet", kvantifierat senare i rapporten: "Fortfarande 2013 anger... en tredjedel av eleverna... att (framför allt) sociala medier... inverkar negativt på under[visningen]" (bekräftar att sociala medier distraherade en betydande andel elever). | **står.** Talen 20/11 och båda utfallen (ökat ensamarbete, social medier-distraktion hos en tredjedel av eleverna) är rapportens egna, ordagrant belagda. |
| S34 | **Ersättningskälla för S05/S06** — Wang & Fan-metaanalysen (indragen 2026-04-22, dessutom fel tidskrift och fel studieantal, se S05/S06) kan inte längre bära den positiva sidan i avsnittet på sidan 6 ("Challenging thinking, or replacing it"). Denna post belägger en oindragen, peer-granskad metaanalys av kontrollerade (experimentella) ChatGPT-studier som kan ersätta citatet. Task 5B lade bara källan; Task 7 (denna uppgift) har skrivit meningen och mätt EW/EP mot den — se verdiktet nedan för ordalydelsen och vaktblocket för ankaren. |  0 |  0 | doi.org/10.1016/j.compedu.2024.105224 → omdirigerar till sciencedirect.com/science/article/pii/S0360131524002380 → **403** direkt (ScienceDirect blockerar bot-UA, samma mönster som OECD/Nature/Microsoft/Elsevier tidigare i den här inventeringen; en captcha-sida bekräftades med både webbläsar-UA via curl och via r.jina.ai-proxy; `archive.org/wayback/available` och CDX-sökning gav ingen capture som visar annat än samma blockering). Läst i stället via en bitidentisk, förlagsproducerad kopia av den publicerade PDF:en: onderwijsorakel.nl/wp-content/uploads/2024/12/1-s2.0-S0360131524002380-main-1.pdf (filnamnet är ScienceDirects egen PDF-namnkonvention för just denna pii; `pdfinfo` på den hämtade filen bekräftar `Creator: Elsevier` och `Subject: Computers & Education, 227 (2025) 105224. doi:10.1016/j.compedu.2024.105224` — samma artikel som DOI:n pekar på, inte en annan version) → **200**, ordagrant 2026-10-15: "A comprehensive search across five databases identified 69 articles published between 2022 and 2024 for analysis." och: "Overall, the results showed that ChatGPT interventions significantly enhanced academic performance (g+ = 0.712), affective-motivational states (g+ = 0.881), and higher-order thinking propensities (g+ = 0.703); significantly reduced mental effort (g+ = -0.675); but did not have a significant effect on self-efficacy (g+ = 0.441)." Författare (kolofonen): Ruiqi Deng, Maoli Jiang, Xinlu Yu, Yuyan Lu, Shasha Liu, Jing Hengyi School of Education, Hangzhou Normal University. Open access under CC BY-licens, bekräftat både i artikelns egen kolofon och av Unpaywall (`api.unpaywall.org`, oa_status: hybrid, license: cc-by). Tidslinje (artikelns sidfot, ordagrant): "Received 15 August 2024; Received in revised form 9 December 2024; Accepted 11 December 2024; Available online 12 December 2024." **Retraktionsstatus aktivt kontrollerad, på tre ställen:** (1) `api.crossref.org/works/10.1016/j.compedu.2024.105224` → fälten `update-to`, `updated-by` och `relation` är alla tomma — CrossRef, som bär förlagens egna retraktionsflaggor, känner inte till någon rättelse eller indragning av artikeln. (2) Hela Retraction Watch-databasen hämtad som CSV direkt från `api.labs.crossref.org/data/retractionwatch` (det officiella dataset retractiondatabase.org bygger på, ca 25 MB, 2026-10-15) och genomsökt mot DOI:n, artikelns titel och författarnamnet "Ruiqi Deng" — noll träffar. Som kontroll av att sökmetoden faktiskt fångar en indragning gav exakt samma genomsökning en träff på den redan kända Wang & Fan-indragningen (DOI 10.1057/s41599-025-04787-y, retraherad 2026-04-22, samma institution — Jing Hengyi School of Education, Hangzhou Normal University — som denna artikels författare) — dvs. metoden hade hittat den här artikeln om den var indragen. (3) `retractionwatch.com`, sökt direkt på författarnamnen och titeln → noll träffar. Ingen retraktion, ingen "expression of concern", ingen corrigendum hittad på något av de tre ställena. | **lagt till.** Kraven 1–4 är uppfyllda: en oindragen, peer-granskad systematisk översikt och metaanalys av kontrollerade (experimentella) studier om generativ AI:s effekt på elevers lärande, hämtad i fulltext och citerad ordagrant ovan. Källan bär: 69 identifierade studier (62 meta-analyserade), och statistiskt signifikanta positiva effekter för tre utfall som tillsammans kan bära avsnittets positiva sida — academic performance (g+ = 0.712), affective-motivational states (g+ = 0.881) och higher-order thinking propensities (g+ = 0.703). Källan bär INTE "motivation" som eget, separat mått — närmast är "affective-motivational states", ett bredare begrepp som omfattar men inte är identiskt med motivation — och bär heller inte stöd för att kalla resultatet okontroversiellt: källan flaggar själv publikationsbias i två av fem utfall (academic performance, affective-motivational states) och avsaknad av power-analys som skäl till försiktig tolkning av samtliga resultat. **Task 7 (denna uppgift) har skrivit in meningen** på båda engelska ytorna (sidan 6), 2026-10-15: "A 2024 meta-analysis (Deng et al., *Computers & Education*, 69 studies identified) found/finding that ChatGPT in controlled experiments significantly improved students' academic performance, affective-motivational states and higher-order thinking." Ordet "motivation" är inte återanvänt — "affective-motivational states" står i stället, källans eget begrepp. Ingen "okontroversiell"-formulering är tillagd; publikationsbiaset och avsaknaden av poweranalys nämns inte i guidetexten (bedömt som för mycket detalj för avsnittets längd, inte som en utelämnad varning om ett sakförhållande guiden hävdar motsatsen till). |
| S36 | `correlation of -0.75` — guidens tionde forskningscitat, EW-exklusivt (sidan 6, direkt efter Lee et al.): "A Swiss study (Gerlich 2025) found a correlation of -0.75 between AI use and critical thinking among younger users." Upptäckt av Task 5B; ingen post fanns förrän nu. | 1 | 0 | mdpi.com/2075-4698/15/1/6 → **403** direkt (Akamai-kant, "Access Denied" — samma klass bot-blockering som OECD/Nature/Microsoft/ScienceDirect tidigare i den här inventeringen); läst i stället via en r.jina.ai-renderad kopia av exakt samma förlagssida (r.jina.ai/https://www.mdpi.com/2075-4698/15/1/6) → **200**, hämtad 2026-10-15: sidan visar artikelns normala "Open Access"-märke, titel "AI Tools in Society: Impacts on Cognitive Offloading and the Future of Critical Thinking", författare Michael Gerlich, avdelning "Center for Strategic Corporate Foresight and Sustainability, SBS Swiss Business School, 8302 Kloten-Zurich, Switzerland", "28 Pages" — och **ingen indragningsbanner** (jämför den indragna Wang & Fan-artikelns egen rubrikprefix "RETRACTED ARTICLE:", se S05, som syns direkt på motsvarande sida). DOI 10.3390/soc15010006, publicerad online 2025-01-03 (`api.crossref.org/works/10.3390/soc15010006`, fältet `published-online`, 2026-10-15). Fulltexten läst via en bitidentisk, förlagsproducerad PDF-spegling: traindy.io/wp-content/uploads/2025/01/2025-AI-and-Critical-Thinking.pdf → **200**, hämtad 2026-10-15 (`pdfinfo` bekräftar `Title: AI Tools in Society: Impacts on Cognitive Offloading and the Future of Critical Thinking`, `Author: Michael Gerlich`, 28 sidor; varje sidfot i den extraherade texten bär journalens egen löpande rubrik "Societies 2025, 15, 6" — samma artikel som DOI:n pekar på, inte en annan version). **Korrelationssiffran, källans egen Tabell 6, ordagrant:** "AI Tool Use ↔ Cognitive Offloading ... +0.72 ... Strong positive correlation", "AI Tool Use ↔ Critical Thinking ... −0.68 ... Strong negative correlation", "Cognitive Offloading ↔ Critical Thinking ... −0.75 ... Strong negative correlation." Brödtexten upprepar samma tre tal, ordagrant: "The correlation between AI tool use and critical thinking was found to be strongly negative (r = −0.68)..." och, i nästa stycke: "A strong negative correlation (r = −0.75) between cognitive offloading and critical thinking further supports this interpretation." **Retraktionsstatus aktivt kontrollerad, på två ställen (samma metod som S34):** (1) `api.crossref.org/works/10.3390/soc15010006` → fältet `updated-by` visar en länk av `"type": "correction"` (DOI 10.3390/soc15090252, "updated" 2025-09-10) — ingen post av typen retraction i `update-to` eller `relation`. Korrigeringens eget innehåll (ideas.repec.org/a/gam/jsoctx/v15y2025i9p252-d1746512.html → **200**, hämtad 2026-10-15, abstract ordagrant: "Error in Table [4]...") gäller Tabell 4 (ANOVA för "deep thinking activities", en dubblett av Tabell 3) — inte Tabell 6, den tabell denna post hänger på. (2) Hela Retraction Watch-databasen hämtad som CSV (`api.labs.crossref.org/data/retractionwatch`, ca 73 200 rader, 2026-10-15) och genomsökt mot DOI:n, artikeltiteln och författarnamnet "Gerlich" → noll träffar; samma dataset och metod fångade redan den kända Wang & Fan-indragningen (se S34) — dvs. metoden hade hittat den här artikeln om den var indragen. **Studiedesign, ordagrant ur källans avsnitt 3.2–3.5:** urvalet var "669 participants in the United Kingdom, of which 666 were considered valid", rekryterade "through a combination of convenience and purposive sampling" och "promoted online in the UK on different social media platforms" — ett självselekterat bekvämlighetsurval i Storbritannien, inte ett draget slumpurval. Kritiskt tänkande mättes med en "structured questionnaire ... A 6-step Likert scale", byggd på "established instruments such as the Halpern Critical Thinking Assessment (HCTA) tool and Terenzini's self-reported measures" — ett självrapporterat enkätmått, inte ett genomfört HCTA-prestationstest. Designen är tvärsnittlig: en enda enkätomgång plus semistrukturerade intervjuer med en delmängd på 50 deltagare, ingen uppföljning över tid. Åldersfyndet, ordagrant ur abstractet: "Younger participants exhibited higher dependence on AI tools and lower critical thinking scores compared to older participants" — ett separat ANOVA/gruppmedelvärde-fynd för åldersgrupperna "17–25 years (young), 26–45 years (middle-aged), and 46 years and older (older)", inte en korrelationssiffra; källan knyter aldrig −0,75 specifikt till yngre användare. | **rättat.** Källan bär tre separata korrelationer, inte en, i sin egen Tabell 6: AI-användning ↔ kritiskt tänkande är **−0,68**; AI-användning ↔ cognitive offloading är **+0,72**; cognitive offloading ↔ kritiskt tänkande är **−0,75**. Guidens mening kopplade −0,75 till fel variabelpar — den satte siffran som källan reserverar för "cognitive offloading ↔ critical thinking" på "AI use and critical thinking", vars egen siffra i källan är −0,68 (brödtexten upprepar den ordagrant: "The correlation between AI tool use and critical thinking was found to be strongly negative (r = −0.68)"). Epitetet "Swiss study" var dessutom fel om DATAN: institutionen är schweizisk (Gerlich, SBS Swiss Business School), men urvalet självt är brittiskt — "669 participants in the United Kingdom, of which 666 were considered valid", "promoted online in the UK on different social media platforms" — inte ett schweiziskt urval. Klämman "among younger users" band dessutom siffran till ett tredje, obesläktat fynd: källans enda åldersresultat är ett separat ANOVA-gruppmedelvärde ("Younger participants exhibited higher dependence on AI tools and lower critical thinking scores compared to older participants"), inte en korrelation, och källan knyter aldrig −0,68 (eller −0,75) specifikt till yngre användare. **Task 12 (2026-10-15) har rättat båda leden på EW** — meningens enda yta (se "Ytdivergenser"): `A Swiss study (Gerlich 2025) found a correlation of -0.75 between AI use and critical thinking among younger users.` → `A study (Gerlich 2025) found a correlation of -0.68 between AI use and critical thinking.` Talet är nu källans egen siffra för exakt det par meningen påstår; landsepitetet är struket helt snarare än nyanserat, eftersom brevets regel ("skriv bara det källan bär") inte ger täckning för en ny, egen omformulering som "a UK-based study"; och åldersklämman är struken eftersom den satta siffran inte längre har något åldersspecifikt fynd att hänga på. Ingen `aktiv`-vaktrad skrivs för ändringen — meningen finns bara på EW, se vaktblockets S36-kommentar. |

### Produktlandskapet (spec §6 klass 2) — "The visibility gap"

Sex påståenden i specen, mätta som åtta kandidater eftersom ett av påståendena namnger
tre produkter var för sig och ett har en egen primärkälla redan i en syskoninventering.
**S37 är tillagd av Task 9** (en nionde kandidat, utanför både brevets och specens
ursprungliga uppräkning) — se S37:s egen cell för skälet.

| id | påstående i guiden | EW | EP | primärkälla + hämtdatum | verdikt |
|---|---|---|---|---|---|
| S19 | `largest chatbots` — "The largest chatbots in K-12 classrooms today are Gemini (Google) and ChatGPT (OpenAI)" — en marknadsandelsutsaga utan källa i guiden |  1 |  1 | securly.com/aiusageinsights → **200**, hämtad 2026-10-14. Detta är **inte** en av leverantörernas egna sidor utan en skolenhets-övervakningsleverantörs egen telemetri från skolägda enheter — den enda hämtbara datakälla som hittades för K-12-andelar, vilket brevet inte förutsåg ("det gör det sannolikt inte"). Ordagrant: "**Gemini** Google 38% (872,054 Chats)" och "**ChatGPT** OpenAI 37.2% (838,344 Chats)", mot tredjeplacerade "Securly AI Chat" på 19.4%. Urval: "2.25 Million Student AI Conversations in 138 Days" över "1,454 School Districts in 39 States", period "Dec 1, 2025 - April 17, 2026", sidan daterad "May 15, 2026". **Samma leverantörs egen tidigare mätning ger motsatt ordning:** k12dive.com/spons/the-ai-visibility-gap-lessons-from-12-million-k-12-conversations/817500/ → **200**, hämtad 2026-10-14 (publicerad 2026-04-20, Securly-sponsrat innehåll, samma metodik): ordagrant "ChatGPT holds 42 percent of the market, Gemini accounts for 21 percent", urval "nearly 1.2 million student AI conversations across 1,312 districts in 39 states". Två läsningar av samma företag, fem veckor isär, är alltså oense om vilken av de två som är störst, även om båda är överens om att Gemini och ChatGPT tillsammans dominerar stort över en namngiven trea. Ingen av Google eller OpenAI publicerar själva K-12-marknadsandelar. | **rättat.** Var `obelagt` för rangordningen — inte därför att ingen källa finns (brevets gissning), utan därför att den enda hittade källan motsäger sig själv om turordningen inom samma femveckorsperiod. Att "Gemini och ChatGPT tillsammans är störst" håller i båda Securly-läsningarna; vilken av de två som är störst gör det inte, och ingen förstapartskälla ger en stabilare siffra. **Task 9 har skrivit om meningen på båda engelska ytorna (sidan 15), 2026-10-15:** `The largest chatbots in K-12 classrooms today are Gemini (Google) and ChatGPT (OpenAI)` → `Two chatbots dominate K-12 classrooms today: Gemini (Google) and ChatGPT (OpenAI)` — "dominate" håller det som är belagt (de två tillsammans är störst) utan att rangordna dem mot varandra. |
| S20 | `Copilot is built on` — "Copilot is built on ChatGPT" — var en förenkling redan i april 2026 enligt specen, sannolikt fel nu |  1 |  1 | **Korsref enligt brevet gick inte att utföra:** samtliga 27 poster (C01–C27) i `docs/guide-facts-copilot.md` genomsökta — ingen rör Copilots underliggande modell eller nämner OpenAI/GPT över huvud taget. Mätt direkt mot förstapartskällor i stället. techcommunity.microsoft.com (Microsoft Copilot Blog, "Available today: OpenAI's GPT-5.6 in Microsoft 365 Copilot", publicerad 2026-07-09) → **200**, hämtad 2026-10-14, ordagrant: "Microsoft 365 Copilot is AI built for work, where frontier models like GPT-5.6 are an important part of a broader system designed to deliver business value—bringing together Work IQ, Microsoft 365 apps, and the enterprise-grade security, compliance, and privacy customers expect from Microsoft." openai.com/index/gpt-5-6-preferred-model-microsoft-365-copilot/ → **200**, hämtad 2026-10-14, ordagrant: "GPT‑5.6 ... will become the new preferred model in Microsoft 365 Copilot ... In addition to serving the models natively, Microsoft will also access OpenAI models directly through the API." Se även samma Copilot-inventerings **C07** (redan verifierad), learn.microsoft.com/en-us/microsoft-365/copilot/microsoft-365-copilot-privacy, ordagrant: "Models provided by Anthropic as a subprocessor are currently excluded from the EU Data Boundary" — Copilot körs alltså på flera leverantörers modeller parallellt (OpenAI **och** Anthropic), inte på en enda. | **rättat.** **Omklassificerat av fixvågen 2026-10-15 (granskningsfynd I4): verdiktet stod `falskt` men cellen dokumenterade en omskrivning PÅ PLATS med ett nytt källbelagt värde, och posten bär en `aktiv`-rad på det nya värdet (`a broader system`) — taxonomins definition av `rättat`, ord för ord: "ett tidigare `föråldrat`- eller `falskt`-värde är ersatt med ett nytt, källbelagt värde". Fyra andra poster i den här filen fick `rättat` under identiska omständigheter (S01, S02, S19, S29), och S19:s cell skriver till och med ut övergången (`obelagt` → `rättat`). Ursprungsverdiktet var `falskt` och det är intakt i resonemanget nedan; det som ändras är klassificeringen av UTFALLET.** "Copilot is built on ChatGPT" blandar redan i grunden ihop ChatGPT (OpenAIs konsumentprodukt) med de GPT-modeller Copilot faktiskt hämtar via Azure OpenAI Service/API — Copilot har aldrig varit "byggt på ChatGPT" i produktmening. I dag beskriver Microsoft själv Copilot som "a broader system" där frontier-modeller som GPT-5.6 är "an important part", och samma inventerings egen C07-post visar att Anthropics modeller körs som underleverantör vid sidan av OpenAIs. Både ramen (ett enda ursprung) och produktnamnet (ChatGPT snarare än GPT-modellerna) är fel. **Task 9 har skrivit om meningen på båda engelska ytorna (sidan 15), 2026-10-15:** `Copilot is built on ChatGPT` → `Copilot is, in Microsoft's own words, "a broader system" that draws on several models — including OpenAI's GPT models and, as a subprocessor, Anthropic's — not a single ChatGPT core`. Cellen bär citaten ("a broader system", "as a subprocessor"); guidetexten återanvänder dem i stället för att hitta på en egen beskrivning. |
| S21 | `beyond the device` — "Apple Intelligence uses ChatGPT for the functions that go beyond the device". **Ankaret är kortat till denna fras** (regel 3) i stället för hela meningen. **Not om avvikelsen:** den här kandidaten stod inte i brevets steg-1-skript (de 25 angivna strängarna); den är tillagd här därför att specens §6 klass 2 räknar upp meningen som ett av sina sex påståenden och ger den redan ett korsref-svar (`Apple-inventeringens A11/A12, verdikt `står`, verifierat 2026-10-14`), och regel 1 ("en faktamening utan post får inte skrivas") gäller lika mycket för en mening brevets skript råkade utelämna. Mätt precis som övriga kandidater: `grep -c "beyond the device"` |  1 |  1 | **Korsref `guide-facts-apple-intelligence.md` A11 och A12** — bägges verdikt kontrollerat här innan korsrefen användes: båda **står**, inte `obelagt` eller `falskt`, så korsrefen är tillåten enligt regeln. A11: support.apple.com/guide/iphone/use-chatgpt-with-apple-intelligence-iph00fd3c8c2/ios → **200**, ordagrant: "You can allow Apple Intelligence to work with ChatGPT from OpenAI"; `grep -i "Gemini\\|Claude\\|Anthropic"` på samma hämtade sida ger noll träffar. A12: samma sida → **200**, ordagrant: "ChatGPT from OpenAI" och "For more information, see OpenAI Terms of Use." Båda lästa 2026-10-14 enligt Apple-inventeringen. | **står.** Apple-inventeringen har redan verifierat att ChatGPT (OpenAI) är den enda externa leverantör Apple dokumenterar som valbar extension för förfrågningar Siri inte klarar on-device — exakt det "beyond the device" hävdar. A11 noterar en annan, separat brasa (se A17: Google och dess Gemini-modeller är med och bygger själva Siri AI) men den gäller hur assistenten är konstruerad, inte vilken extern tjänst en användare kopplar på för uppgifter utanför enheten — den brasan rör inte den här guidens mening, och A17:s egen anteckning säger uttryckligen att den ska hållas skild från ChatGPT-extensionen (A11/A12). |
| S22 | `Khanmigo` — K-12-specifikt produktnamn |  1 |  1 | khanmigo.ai → **200**, ordagrant 2026-10-15 (sidtiteln och hero-ledet): "Meet Khanmigo: Khan Academy's AI-powered teaching assistant & tutor" och "Khanmigo is your always-available teaching assistant."; blog.khanacademy.org/khanmigo-features/ → **200**, ordagrant 2026-10-14 (publicerad 2023-11-29, uppdaterad 2025-03-21), rubrik: "Khanmigo Features for Teachers". Produkten finns och heter så i dag. | **står.** Namnet är oförändrat och produkten är i drift. |
| S23 | `MagicSchool` — K-12-specifikt produktnamn |  1 |  1 | magicschool.ai → **200**, ordagrant 2026-10-15 (sidtiteln och hero-ledet för lärare): "AI Platform for School Districts \| MagicSchool" och "Save time, spark creativity, and support every learner."; magicschool.ai/faq → **200**, ordagrant 2026-10-14: "Teachers decide how students use MagicSchool and can see what happens along the way." Produkten finns och heter så i dag. | **står.** Namnet är oförändrat och produkten är i drift. |
| S24 | `ChatGPT for Teachers` — K-12-specifikt produktnamn |  1 |  1 | openai.com/index/chatgpt-for-teachers/ → **200**, hämtad 2026-10-14, ordagrant rubrik/brödtext: "A free version of ChatGPT built for teachers" och "ChatGPT for Teachers is built for both educators and school leaders." Produkten finns och heter exakt så i dag. **Förbehåll som bär över till S25:** samma sida beskriver produkten enbart för "educators" och "school and district leaders" — ingen mening på sidan nämner elevkonton; det är en lärar-/personalyta, inte en elevyta. | **står.** Namnet är korrekt och produkten är i drift, med reservationen (se S25) att den enligt sin egen sida inte har elever som användare. |
| S25 | `aggregated view` (**och, från fixvågen 2026-10-15, avsnittsrubriken på sidan 15 — granskningsfynd I2**) — den bärande utsagan: "they do not give teachers a clear aggregated view of which questions students in a class have asked". Faller den, faller avsnittets slutsats — innehållsbeslut för Johan, inte en formulering för en uppgift (spec §6) |  1 |  1 | Mätt leverantör för leverantör mot var och ens egen publika dokumentation (inte jämförelseartiklar), enligt brevets steg 1–2. **Google** (Gemini for Education / Workspace for Education admin): edu.google.com/intl/ALL_us/ai/gemini-for-education/ → **200**, hämtad 2026-10-14, ordagrant: "Enterprise-grade data protection: Core Service covered under Google Workspace for Education terms. Data is not human reviewed or used to train AI models." knowledge.workspace.google.com/admin/generative-ai/review-gemini-usage-in-your-organization → **200**, hämtad 2026-10-14, ordagrant: "Review Gemini in Google Workspace apps usage information by organizational unit or group... The number of chat messages your users exchanged with Gemini... Gemini usage per feature." Funktionen är **admin**-vänd (Google Admin-konsolen), inte lärarvänd, och visar antal och trender per organisationsenhet — aldrig ämne eller innehåll i en elevfråga. **OpenAI** (ChatGPT Edu / ChatGPT for Teachers): help.openai.com/en/articles/10875114-workspace-analytics-for-chatgpt-enterprise-and-edu → **200**, hämtad 2026-10-14 (sidan anger "Updated: 2 months ago"), ordagrant: "Task insights shows aggregated patterns of work in ChatGPT by classifying conversations into broad task categories and topics. It provides workspace-level insights without exposing individual prompts, conversations, or user-level activity." Ämnesbunten, inte frågebunten, aggregering på **workspace**-nivå (inte klass-/lektionsnivå), och gäller "ChatGPT Enterprise and Edu" — inte det K-12-produktnamn guiden själv använder. openai.com/index/chatgpt-for-teachers/ → **200**, hämtad 2026-10-14, ordagrant: "ChatGPT for Teachers is built for both educators and school leaders" — produkten har enligt sin egen sida inga elevkonton alls (se S24), så det finns ingen elevfråga att aggregera i just den produkten. **Microsoft** (Copilot for Education): learn.microsoft.com/en-us/copilot/manage → **200**, hämtad 2026-10-14 (sidans "ms.date": 2026-10-12), ordagrant: "The Microsoft Copilot Chat usage dashboard provides insights into active usage of Copilot Chat. Admins can generate reports on total active users, average daily active users, total prompts submitted and average prompts per user, and active users of Copilot Chat in specific apps." microsoft.com/en-us/education/products/copilot-in-education → **200**, hämtad 2026-10-14: nämner "Copilot Dashboard" (adoption/sentiment) och "Education Insights"-kort som flaggar elever vars "activity patterns have changed" — inga av dessa beskriver en vy över frågornas innehåll eller ämne, bara antal och mönsterflaggor, och uttryckligen admin-vänt. **Khan Academy** (Khanmigo Teacher Tools): blog.khanacademy.org/khanmigo-features/ → **200**, hämtad 2026-10-14 (publicerad 2023-11-29, uppdaterad 2025-03-21), ordagrant: "Summarize Student Chat History: Gain insights from compiled summaries of student Khanmigo chats (available exclusively to teachers rostered in a Khan Academy Districts partner district)." khanacademy.org/khan-for-educators/k4e-us-demo/xb78db74671c953a7:engage-from-preparation-to-pedagogy/xb78db74671c953a7:quick-data-checks/v/responding-to-student-chat-trends → **200**, hämtad 2026-10-14, ordagrant (den officiella lärarutbildningsvideots egen transkript): "From your class dashboard, you can choose a class and explore trending topics or flag conversations. Trending topics give you a quick snapshot of what students are asking about most often. For example, you might notice several students asking about area calculation or problem-solving over the past week... these trends give you valuable insight into what's on your students' minds." **Detta är den enda av de fem mätta leverantörerna vars egen publika dokumentation uttryckligen beskriver precis den vy guiden säger saknas** — en klassnivå-aggregering av vilka ämnen/frågor eleverna ställt till AI:n, tillgänglig för läraren, inte bara admin. **MagicSchool**: magicschool.ai/blog-posts/enterprise-feature-releases → **200**, hämtad 2026-10-14 (publicerad 2025-02-03, byline "Senior Product Marketing Manager, MagicSchool"), ordagrant: "Student Room Insights provides teachers and admins with a window into classroom activity... Access detailed usage data: For a broader view, the dashboard compiles quantitative data on tool usage and frequency. It updates hourly." magicschool.ai/faq → **200**, hämtad 2026-10-14, ordagrant: "Teachers decide how students use MagicSchool and can see what happens along the way... review students' work and AI interactions." En aggregerad vy över **vilka verktyg** och **hur ofta**, klassvis och i realtid — närmare guidens påstående än Google/Microsoft/OpenAI, men ingen av sidorna beskriver en vy över **ämnena eller innehållet** i frågorna, bara verktygsanvändning och frekvens. Gränsfall, räknas här som att INTE uppfylla "which questions." | **står, men smalt — se rapporten till Johan.** Fyra av fem mätta leverantörer (Google, Microsoft, OpenAIs namngivna K-12-produkt, och MagicSchool för frågeinnehåll specifikt) ger enligt sin egen publika dokumentation ingen aggregerad vy över elevfrågornas innehåll — det håller "majority"-formuleringen i sak, och meningens egna hedge ("according to what's publicly advertised") håller också. **Men Khan Academy/Khanmigo — ett av de tre K-12-produktnamn som räknas upp i exakt samma mening — annonserar offentligt precis den förmåga meningen säger att majoriteten saknar** (klassnivå "trending topics" och "Summarize Student Chat History", lärarvänt, inte bara admin). Det motsäger inte ordet "majority" (en av fem är inte en majoritet), men det är ett namngivet undantag i samma andetag som påståendet görs. Detta är brevets eget "minst några gör det"-spår (steg 4) — den bokstavliga satsen håller, men om den håller som LÄSARENS intryck av stycket, och om Khanmigo-undantaget bör namnges eller hedgen skärpas, var en innehållsfråga för Johan, inte en faktafråga den här uppgiften kunde avgöra. **Johans beslut vid rundans grind (2026-10-15), genomfört av Task 9 i två steg.** Första steget namngav bara Khanmigo explicit, i samma mening som majoritetspåståendet. Granskningen av det steget hittade att guiden redan bar ett ANNAT, obelagt undantagspåstående två meningar bort (SchoolAI, se **S37**) — och efter att S37 belades mot schoolai.com beslutade ägaren att namnge BÅDA. Ordalydelsen, på båda engelska ytorna (sidan 15), 2026-10-15: `...do not give teachers a clear aggregated view of which questions students in a class have asked the AI during a lesson; two vendors do: Khanmigo, which advertises a "Summarize Student Chat History" feature and a class dashboard of trending topics, and SchoolAI, whose Mission Control dashboard advertises a "Class Mastery Score" and the class's common misconceptions.` Ingen singular "the exception" används — ägarens uttryckliga krav, eftersom två oberoende leverantörer nu är namngivna. Den tredje styckesmeningen på samma sida ("Khanmigo and SchoolAI show the feature is technically possible, independently of each other...") elaborerar på båda i stället för att upprepa namngivningen separat. **ANDRA FÖREKOMSTEN — avsnittsrubriken, rättad av fixvågen 2026-10-15 (granskningsfynd I2).** Rubriken `The visibility gap — today's AI tools don't show teachers what students are asking` stod kvar oförändrad medan stycket under den namngav två leverantörer som GÖR det (Khanmigo och SchoolAI, ägarbeslut 2 respektive S37) — en motsägelse som rundans egna rättelser skapade, inte en ärvd. Rubriken är omskriven till `The visibility gap — most AI tools still don't show teachers what students are asking` på båda ytorna: `most` ersätter det underförstådda "alla" och `still` bär kvar avsnittets poäng — lärarvyn är görbar (två leverantörer bygger den) men de flesta verktygen ger den inte. Hedgen i stycket ("According to what's publicly advertised, most of these tools...") och rubriken säger nu samma sak. **Grepad i hela repot 2026-10-15:** strängen `show teachers what students are asking` förekom på exakt två ställen, EP:488 och EW:293 (båda `<h2>`), och på inga andra — ingen innehållsförteckning finns (specen §7), webbytans `anchor-nav` bär bara de fem delrubrikerna ("Part 1 · Learning is the point", "Part 2 · Prerequisites", "Part 3 · On the classroom floor", "Checklist", "FAQ") och `_unpublished/guides/ai-for-students/script.js` nämner ingen rubriktext alls (0 träffar på `visibility`, `gap` och `teachers`). Båda förekomsterna är alltså ändrade, och ingen navigations- eller innehållsyta divergerar från dem. |
| S26 | `back in 2014` — "teachers suddenly have the instruments the 1:1 researchers were calling for back in 2014", hänger på S25 |  1 |  1 | Hänger på S25 (brevets egen regel: "faller den faller den här"). Meningen är själv villkorad — "Combined with aggregated class visibility (if the vendor offers it), teachers suddenly have the instruments..." — och det villkoret är, enligt S25:s källrad, redan uppfyllt hos minst en namngiven leverantör (Khanmigo) per 2026-10-14. Ingen ny hämtning krävs utöver S25:s fem leverantörskällor, eftersom den här meningen inte själv namnger någon leverantör. | **står.** Villkoret "if the vendor offers it" är redan uppfyllt hos minst en leverantör (Khanmigo, se S25) enligt dagens publika dokumentation, så den villkorade slutsatsen är sann som skriven — den överclaimar inte på egen hand. Den hänger på S25 precis som brevet förutsåg, och landar i samma läge: formellt sant, men värt Johans uppmärksamhet av samma skäl som S25. **Läst mot den nya sidan 15 (Task 9, 2026-10-15, uppdaterad efter granskningens SchoolAI-fynd):** villkoret är nu namngivet, inte bara hypotetiskt — Khanmigo och SchoolAI står båda explicit namngivna i stycket ovanför. Meningens egen hedge ("if the vendor offers it") höll redan innan namngivningen och behöver ingen ändring; den beskriver fortfarande korrekt att instrumentet inte är universellt, bara att två leverantörer nu är namngivna i stycket intill, inte en. Ingen ändring gjord i guidetexten för den här posten. |
| S37 | `SchoolAI` — guidens undantagsclaim på sidan 15, nu: "...two vendors do: Khanmigo... and SchoolAI, whose Mission Control dashboard advertises a "Class Mastery Score" and the class's common misconceptions." Fanns i guiden redan innan den här rundan i en annan form (arv från guide-designens ursprungsspec, april 2026: "There is one notable exception in the K-12 space. SchoolAI offers an aggregated class-level dashboard...") men stod utanför både Task 1:s 25 kandidater och Task 4:s sex produktposter — ingen av rundans fem mätuppgifter mätte eller belade påståendet. Task 9:s första pass (2026-10-15) strök det utan att hämta källan (se historiken nedan); granskningen beställde en mätning innan avvikelsen dömdes. |  1 |  1 | schoolai.com/mission-control → **200**, ordagrant 2026-10-15 (hämtat av granskningen): "Class Mastery Score — See where the class stands at a glance, with common misconceptions surfaced so teachers can address them right away." och: "Mission Control shows what students are asking, how they're reasoning, and where they're stuck. For the first time, leaders and coaches can see student thinking across every classroom, every day." Samma ribba som Task 4:s mätning av de fem andra leverantörerna (S25): publikt annonserat, lärarvänt (här även leder/coacher), innehåll och inte bara antal — "what students are asking" är frågeinnehåll, inte bara verktygsanvändning eller frekvens (jämför MagicSchools gränsfall i S25). | **rättat.** Gick från `obelagt` till belagt **i samma post** — inte `struket` ersatt av en ny id, eftersom det är SAMMA påstående (SchoolAI ger en klassaggregerad vy) som nu har ett nytt, källbelagt värde i stället för inget värde alls. **Historiken, i tur och ordning:** (1) guiden bar claimet osynligt för rundans mätuppgifter (Task 1–4 täckte aldrig SchoolAI). (2) Task 9 upptäckte motsägelsen när Johans beslut om att namnge Khanmigo (S25) skulle skrivas in — en kvarlämnad, obelagd SchoolAI-mening hade gett sidan två olika "undantag" i samma stycke — och strök SchoolAI-meningen utan att hämta källan, en rimlig bedömning på den information som fanns då (ingen av rundans fem mätuppgifter hade täckt den). (3) Granskningen beställde en mätning innan avvikelsen dömdes och hämtade schoolai.com/mission-control ordagrant (källcellen ovan): SchoolAI klarar exakt den ribba Task 4 satte för de fem andra leverantörerna, tydligare än fyra av dem. (4) Ägaren beslutade att namnge BÅDA leverantörerna explicit, ingen i singular "the exception" — samma skäl som bar det ursprungliga beslutet (en läsare som själv upptäcker ett undantag tappar förtroende för kapitlet), förstärkt av att två OBEROENDE leverantörer redan löst problemet, vilket stärker kapitlets poäng att vyn är görbar och att branschen i övrigt inte prioriterar den. Guidetexten är skriven in på båda engelska ytorna (sidan 15), 2026-10-15 (Task 9, andra passet) — se Task 9-rapporten för exakt ordalydelse före/efter. |

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
| S29 | `minimal risk` — "AI use falls in the minimal risk category and the requirements are relatively light" | 1 | 1 | `korsref A35` (`docs/guide-facts-apple-intelligence.md`, verdikt `lagt till`) — kommissionens ordalydelse, ordagrant: "The AI Act defines 4 levels of risk for AI systems: Unacceptable risk / High risk / Transparency risk / Minimal or no risk" | **rättat.** Var `falskt, men lindrigt`. Aktens egen fjärde nivå heter "Minimal or no risk," inte "minimal risk" — och "minimal risk" var exakt den förkortade/föråldrade variant som A35 noterar stod fel i Gemini-guiden innan G26 rättade den (tillsammans med "Limited risk" → Transparency risk och "Prohibited" → Unacceptable risk). Skillnaden var lindrigare här än i Gemini-fallet: guiden räknade inte upp alla fyra nivåer i en formell lista eller ett diagram (bara "minimal risk" och "high risk" nämndes, i löpande text), så felet var ett enda ord ("or no" saknades) snarare än en felaktig fyrnivålista. "High risk" i samma mening var redan korrekt och är orört. **ÅTGÄRDAT i Task 8 (2026-10-15), sidan 11, båda engelska ytorna:** `minimal risk` → `Minimal or no risk`, samma rättelse som G26 redan gjorde i Gemini-guiden. Den nakna strängen `minimal risk` förekom exakt en gång per yta före rättelsen (mätt, inget legitimt kvarvarande bruk någon annanstans i guiden), så den är ett säkert `borttaget`-ankare utan undantag. **Task 10 (2026-10-15) hittade en andra, osynkroniserad förekomst av samma sakfel på sidan 21** (FAQ, "What does the EU AI Act mean for my classroom — the short answer?"): `You're in the minimal-risk category` — hyfenerad, inte med mellanslag, så Task 8:s `borttaget`-ankare ovan träffade den aldrig (se vaktblockets kommentar vid den nya raden). Rättad på båda engelska ytorna till `You're in the <em>Minimal or no risk</em> category`, samma terminologi som sidan 11. |
| S30 | `Data Protection Impact Assessment` / `GDPR Article 35` — FAQ-svaret: "Do we need a Data Protection Impact Assessment (DPIA)? ... a DPIA is often required (under GDPR Article 35 in the EU; consult equivalent rules elsewhere)" | 1 | 1 | gdpr-info.eu/art-35-gdpr/ → **200**, hämtad 2026-10-15, ordagrant artikel 35(1): "Where a type of processing in particular using new technologies, ... is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall, prior to the processing, carry out an assessment of the impact of the envisaged processing operations on the protection of personal data." Plus `korsref A38` (`docs/guide-facts-apple-intelligence.md`, verdikt `lagt till`) — artikel 27, konsekvensbedömningen för grundläggande rättigheter, som gäller "whether the school is publicly run or an independent provider of a public service," före första driftsättning av ett Annex III-högrisksystem (utbildning är punkt 3) | **lagt till** (artikel 27 fanns inte i guiden; var `står, men ofullständigt`). GDPR artikel 35 beskrivs korrekt i FAQ-svaret (sidan 21): en DPIA krävs när behandlingen sannolikt innebär hög risk för registrerades rättigheter, precis vad guiden skriver där — det ledet är orört. Men FAQ-svaret nämnde bara GDPR:s DPIA och sa ingenting om AI Act:s EGEN, separata konsekvensbedömning för grundläggande rättigheter (artikel 27, A38) — en skyldighet som gäller samma högrisksystem (Annex III, utbildning inkluderat) oavsett om skolan är kommunal eller fristående, och som inte ersätts av en GDPR-DPIA. En läsare som gör sin GDPR-DPIA och tror sig vara klar missar en andra, AI Act-specifik plikt. **ÅTGÄRDAT i Task 8 (2026-10-15) — men INTE på FAQ-svarets egen plats.** Artikel 27 är nu skriven in i guiden, i samma mening som S28:s rättelse på sidan 11 (se S28:s cell för hela ordalydelsen): "...plus Article 27's fundamental-rights impact assessment before first use, whether it is publicly run or an independent provider of a public service." **Skälet till att meningen inte landade bredvid DPIA-meningen på sidan 21, där S30 ursprungligen pekade:** Task 8:s filomfång är uttryckligen "sidorna 7–12" (brevets egen rad för filerna), och FAQ:n (sidan 21) står explicit listad i Task 10:s brief som den uppgiftens egna rad ("FAQ:ns AI Act- och DPIA-svar enligt Task 5") — Task 10:s gränssnitt säger dessutom att den konsumerar "vad Task 8 skrev på sidorna 11–12". Att skriva om FAQ-svaret här hade dubblerat eller krockat med en uppgift som redan äger den ytan. Avsnittet har alltså nu artikel 27 — kravet "guiden ska inte sakna artikel 27" är uppfyllt — men FAQ-svarets EGEN mening på sidan 21 nämner fortsatt bara artikel 35; det är en öppen tråd för Task 10, inte en halvgjord rättelse här. Flaggat i rapporten under "farhågor". **ÅTGÄRDAT i Task 10 (2026-10-15), sidan 21, båda engelska ytorna.** DPIA-svaret bär nu, direkt efter GDPR artikel 35-meningen: "The AI Act adds a separate requirement for the same high-risk systems, education included: Article 27's fundamental-rights impact assessment before first use, whether the school is publicly run or an independent provider of a public service — a GDPR DPIA does not cover it." Tråden som Task 8 lämnade öppen är därmed stängd på sin egen plats. |
| S31 | `FERPA governs student data` — "FERPA governs student data" | 1 | 1 | studentprivacy.ed.gov/faq/what-ferpa → **200**, hämtad 2026-10-15, ordagrant: "FERPA is a federal law that affords parents the right to have access to their children's education records, the right to seek to have the records amended, and the right to have some control over the disclosure of personally identifiable information from the education records" | **står.** FERPA är den federala lag som reglerar amerikanska elevers utbildningsjournaler, inklusive personligt identifierbar information — precis det påståendet hävdar, om än i en enda kort sats utan detaljer |
| S32 | `no single federal AI regulation` — "in the US there is no single federal AI regulation but state-level rules (California, Colorado and others) exist" | 1 | 1 | multistate.us/insider/2026/4/9/how-states-are-regulating-ai-in-education-this-legislative-session → **200**, hämtad 2026-10-15, ordagrant om Kalifornien: "California (CA AB 1159) – Expands and strengthens student data privacy protections, prohibits using student data to train AI," samt "134 bills related to AI in education legislation have been introduced across 31 states" (mars 2026). **Colorado, delstatens egen lagstiftningssida** (`leg.colorado.gov/bills/sb24-205` → **200**, hämtad 2026-10-15, ordagrant: "Bill Summary: On and after February 1, 2026, the act requires a developer of a high-risk artificial intelligence system (high-risk system) to use reasonable care to protect consumers from any known or reasonably foreseeable risks of algorithmic discrimination in the high-risk system." Signerad 2024-05-17, Chapter 198) — alltså en verklig, antagen delstatslag, inte bara ett förslag. Samma lagstiftningssida, efterföljaren (`leg.colorado.gov/bills/sb26-189` → **200**, hämtad 2026-10-15, ordagrant: "In 2024, the general assembly enacted Senate Bill 24-205, which created consumer protections in interactions with artificial intelligence systems. The act repeals and reenacts those provisions with new requirements regarding the use of automated decision-making technology in consequential decisions." Signerad 2026-05-14, omfattar uttryckligen beslut om "education"). **"Ingen enskild federal AI-lag" — primärkälla, inte parafras:** Congressional Research Service-rapporten R48555 (`congress.gov/crs_external_products/R/PDF/R48555/R48555.2.pdf` → **200**, hämtad 2026-10-15, daterad 2025-06-04), ordagrant: "No federal legislation establishing broad regulatory authorities for the development or use of AI or prohibitions on AI has been enacted" och "In the absence of federal AI regulations, states have been enacting their own laws." Rapporten är 16 månader gammal vid hämtningstillfället, inte en nyhet från i dag — men ingen senare federal AI-lag har hittats i sökningen som motsäger den (se delstatstabellen ovan, som i stället visar fortsatt delstatsaktivitet 2026) | **står.** Påståendet är brett och unamngivet nog att hålla trots att Colorados ursprungliga lag redan bytts ut mot en efterträdare: delstatsnivå-regler finns alltjämt, bekräftat mot delstaternas egna lagstiftningssidor i både Kalifornien (AB 1159 om elevdata) och Colorado (SB24-205 → SB26-189, den senare i kraft 2027-01-01), och ingen samlad federal AI-lag finns, bekräftat mot CRS, forskningsarmen för den amerikanska kongressen. Medveten anmärkning: en federal preemption-diskussion pågår i USA 2026, men ingen preemption har trätt i kraft — påståendet är sant per hämtdatumet, inte garanterat förbli så |
| S33 | `In the UK there is UK GDPR` — "In the UK there is UK GDPR" | 1 | 1 | ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/ → **200**, hämtad 2026-10-15, ordagrant: "The UK GDPR includes a right for individuals to have inaccurate personal data rectified, or completed if it is incomplete" — ICO (Storbritanniens tillsynsmyndighet) namnger och tillämpar "UK GDPR" som egen, gällande reglering | **står.** UK GDPR är en verklig, av ICO tillämpad reglering — Storbritanniens egen version av GDPR efter Brexit, vid sidan av Data Protection Act 2018 |

Denna fyllnad är **inte** regel 2:s "stryks aldrig tyst" i andra bemärkelsen — tomheten
i Task 1 var en känd plats där ett fynd skulle höra hemma, och nu gör det det.

### Granskningsfynden (fixvågen 2026-10-15) — sju poster helgranskningen saknade

Helgranskningen av grenen fällde ett Critical och åtta Important. Fem av fynden rörde
påståenden **utan post** i den här filen; de får sina poster här. Blocket är eget i
stället för att trängas in i de tre klasserna från spec §6, av samma skäl som
"Omslaget och läsartilltalet" är eget: de tre blockens egna ingresser räknar ut sina
kandidater (nio citat plus ett tionde, åtta plus S37, sju), och en post som smygs in i
en sådan uppräkning gör ingressen osann. Klasstillhörigheten står i stället i varje
cell. Fynden I2 (rubriken mot sitt stycke), I4 (verdiktet mot sin cell) och M7
(ellipsen) ändrade BEFINTLIGA poster — S25, S20 och S03 — och står där, inte här.

| id | påstående i guiden | EW | EP | primärkälla + hämtdatum | verdikt |
|---|---|---|---|---|---|
| S38 | `(UNESCO, OECD` — **granskningsfynd C1, spec §6 klass 1.** Attributionen bakom rådet "börja tillsammans, synligt", på två ställen per yta: sidan 15 ("Guidance from major education bodies (UNESCO, OECD, and national curriculum authorities) **converges on a practical point**: *start together, visibly*", under rubriken "What international guidance says" på EP / "What education authorities say" på EW) och FAQ:n sidan 20 ("an intermediate mode that international guidance (UNESCO, OECD) **consistently recommends**: *start together on a shared screen*"). Påståendet säger vad två namngivna internationella organ REKOMMENDERAR, hedgat med "converges"/"consistently" — alltså ett starkare påstående än en enskild studies fynd, och det enda i guiden som tillskriver ett pedagogiskt råd till en myndighet. | 2 | 2 | **Sex primärdokument hämtade, konverterade med `pdftotext` och genomsökta 2026-10-15. Alla sex på noll för det specifika rådet.** (1) UNESCO, *Guidance for generative AI in education and research* (2023), `unesco.org.uk/site/assets/files/10375/guidance_for_generative_ai_in_education_and_research.pdf` → **200**, 96 sidor (unesdoc.unesco.org gav **403** mot bot-UA, samma klass som S03:s OECD-blockering; UNESCO UK:s kopia är samma dokument, verifierat mot titelsidan "Guidance for generative AI in education and research"). Nollträffar: `shared screen`, `whole class`, `whole-class`, `projector`, `large screen`, `classroom activit`, `together with students`, `co-use`, `teacher-mediated`, `teacher mediated`, `guided use`, `model the use`, `first step`, `start together`, `visibly`, `in front of the class`, `class discussion`, `teacher supervision`, `supervised`. Enstaka träffar, alla lästa i sitt sammanhang och ingen om klassrumsbruk: `modelling` 1 ("modelling of the mother tongue or foreign language", om språkinlärning), `jointly` 1 ("jointly develop trustworthy models", om regeringar och forskningsinstitutioner), `collectively` 1 (om modellvikter), `openly` 1 (en referenstitel från The Verge), `demonstrate` 3 (om modellers begränsningar och forskningspotential). (2) UNESCO, *AI competency framework for teachers* (2024), `unesco-asp.dk/wp-content/uploads/2025/02/AI-Competency-framework-for-teachers_UNESCO_2024.pdf` → **200**, 52 sidor: samma sökordslista, samtliga **0** utom `demonstrate` 36 (kompetensbeskrivningarnas standardverb) och `supervis` 1. (3) OECD + Education International, *Opportunities, guidelines and guardrails for effective and equitable use of AI in education* (2023), `oecd.org/content/dam/oecd/en/about/projects/edu/smart-data-and-digital-technology-in-education/` (filnamnet med procentkodade blanksteg) → **200**, 17 sidor: samtliga **0** utom `jointly` 2 och `supervis` 1. (4) OECD, *Digital Education Outlook 2023*, `oecd.org/content/dam/oecd/en/publications/reports/2023/12/oecd-digital-education-outlook-2023_c827b81a/c74f03de-en.pdf` → **200**: `shared screen` 0, `whole-class` 0, `start together` 0, `visibly` 0, `large screen` 0, `teacher-mediated` 0, `guided use` 0; `whole class` 1, ordagrant "recommending how they could engage the whole class in collaborative learning activities" — en beskrivning av vad en AI-funktion för klassrumsorkestrering kan föreslå läraren, inte ett råd om att börja tillsammans; `projector` 1 (en irländsk utrustningsbidragslista), `class discussion` 1 (om formativ bedömning). (5) OECD, *Insights on the effective use of generative AI in education* (Digital Education Outlook 2025), `oecd.org/content/dam/oecd/en/about/projects/edu/smart-data-and-digital-technology-in-education/Insights_OECD Digital Education Outlook 2025.pdf` → **200**: samtliga sökord **0** utom `first step` 1 (inte om klassrumsbruk). (6) OECD, *Digital Education Outlook 2026*, `oecd.org/content/dam/oecd/en/publications/reports/2026/01/oecd-digital-education-outlook-2026_940e0dd8/062a7394-en.pdf` → **200**, 267 sidor: `shared screen` 0, `start together` 0, `whole-class` 0; `whole class` 1 (en intervju om en uppsatsanalys-dashboard i Brasilien), `visibly` 1 (om Khanmigos "double-check"-mekanism). **Fyra webbsökningar utöver dokumenten, samtliga utan träff på rådet:** UNESCO-vägledningen + `whole-class shared screen teacher-mediated use`; OECD + `whole class teacher modelling shared screen first step classroom`; `"shared screen" OR "whole class"` begränsad till `unesco.org`/`unesdoc.unesco.org`; OECD + `teachers use generative AI together with students projected screen discuss errors bias real time` begränsad till `oecd.org`. Ingen av de fyra returnerade ett dokument där UNESCO eller OECD rekommenderar helklassbruk på delad skärm som första steg. **Ett näraliggande fynd som INTE räcker:** UNESCO:s lärarramverk (källa 2) har en hel dimension som heter "AI pedagogy", och OECD (källa 6) skriver att lärare bör möta generativ AI som "an expert yet unreliable collaborator" — men ingen av dem föreskriver FORMEN (gemensamt, synligt, helklass, delad skärm, som FÖRSTA steg), och ett råd om form kan inte vila på ett råd om hållning. | **struket.** Fyndet är `obelagt` — sex hämtade primärdokument från just de två organ guiden namnger säger ingenting om att använda AI gemensamt, synligt, i helklass som första steg, och inget av dem kan därmed bära ett "converges on a practical point" eller ett "consistently recommends". Specen §6 klass 1 är bindande och dess ordalydelse är inte förhandlingsbar: *"ett citat som inte går att belägga lämnar guiden — borttaget, inte omskrivet."* **Utfall: attributionen är borta, rådet står kvar i guidens eget namn.** Sidan 15:s rubrik ("What international guidance says" / "What education authorities say") är ersatt av `Where to start` på båda ytorna och stycket inleds nu `If you take one practical step from this guide, take this one: start together, visibly`; FAQ-svaret säger `an intermediate mode this guide recommends instead`. **Rådet självt är oförändrat ord för ord** — "start together, visibly", den stora skärmen, att fel och bias diskuteras i realtid, och att rådet bär oavsett jurisdiktion därför att det inte hänger på verktyget utan på läraren. Det är god pedagogik som guiden kan äga själv, och den äger den nu. Samma utfall som Gemini-rundans Matt Miller-citat: attributionen togs bort, poängen stannade. **Sidoeffekt, medvetet:** de två gamla rubrikerna DIVERGERADE mellan ytorna (preexisterande, se "Ytdivergenser" nedan) och den nya är identisk på båda — inte en harmonisering av innehåll, utan följden av att samma felaktiga attribution måste bort på två ytor och av att en `aktiv`-vaktrad kräver ordagrann identitet. |
| S39 | `isn't a tech project` — **granskningsfynd I1, spec §6 klass 1.** Grönlund-citatet, sidan 14, presenterat ordagrant inom citattecken: "Grönlund's summary line is worth remembering: *"A school IT project isn't a tech project, it's a change project."*". Helgranskningen hämtade primärkällan och fann påståendet SANT — posten saknades, inte belägget. | 1 | 1 | `diva-portal.org/smash/get/diva2:706366/FULLTEXT01.pdf` (Grönlund, Åke. *Att förändra skolan med teknik: Bortom "en dator per elev"*, Örebro universitet, 2014, ISBN 978-91-7668-992-9) → **200**, hämtad och `pdftotext`-läst 2026-10-15. **Källan har ingen engelsk ordalydelse; den har tre svenska, alla ordagranna:** (a) förordets sammanfattning "i korthet": *"En till en" är inte ett it-projekt utan ett förändringsprojekt.* (svenska citattecken runt "En till en" i originalet); (b) kapitelrubriken med dess styckesinledning: *"1:1" är ett förändringsprojekt, inte ett it-projekt*; (c) den formulering som ligger närmast guidens generalisering från 1:1 till skol-it i stort, i rådslistan: *Kommunen måste se it i skolan som ett förändringsprojekt, inte ett teknikprojekt.* Guidens ordföljd ("isn't a tech project, it's a change project") följer (b) och (c); dess subjekt ("A school IT project") följer (c), inte (a). | **står.** Sakinnehållet är källans eget och står i tre ordagranna svenska varianter, varav en bär exakt guidens generalisering (*it i skolan ... ett förändringsprojekt, inte ett teknikprojekt*). Ingen siffra, inget år och inget namn i meningen är fel. **Men citatet är en ÖVERSÄTTNING som presenterades som ordagrant, och det är rättat av fixvågen 2026-10-15.** Bedömningen, utskriven eftersom brevet begärde den: en läsare vilseleds. Meningen står inom citattecken, kallas "Grönlund's summary line" och får inget språk angivet — en engelskspråkig skolledare läser det som Grönlunds egna ord på engelska, går för att citera dem vidare, och finner dem inte, eftersom de inte finns. Det är samma skada ett uppfunnet citat gör, med den skillnaden att sakinnehållet håller. Priset för att laga det är fyra ord. **Ordalydelsen på båda ytorna är nu:** `Grönlund's summary line is worth remembering, translated from the Swedish:` följt av citatet oförändrat. Citatets ord är orörda; bara märkningen är tillagd. (Att guidens engelska är en översättning av en svensk primärkälla gäller också S40 och S41, men de två presenteras INTE inom citattecken — de står som guidens egen återgivning av studiens fynd, kursiverade, och behöver därför ingen märkning. Skillnaden är citattecknen, inte språket.) |
| S40 | `more teacher-led time, not less` — **granskningsfynd I1, spec §6 klass 1.** Unos Uno-studiens slutsats som guiden hänger 1:1-avsnittet på, sidan 14: "the schools that improved their results with 1:1 had *more teacher-led time, not less*". Kursiverad, inte citerad. Helgranskningen fann påståendet SANT; posten saknades. | 1 | 1 | `diva-portal.org/smash/get/diva2:706366/FULLTEXT01.pdf` (samma bok som S17/S18/S39; URL:en upprepad enligt regeln att varje källcell står på egna ben) → **200**, 2026-10-15. Ordagrant, om vad som skilde de framgångsrika skolorna: *"Enskilt välorganiserat arbete ersätts av ensamarbete där eleverna tappar fokus. Andelen enskilt arbete ökar generellt. I de framgångsrika skolorna ersätts de med välorganiserat, lärarlett enskilt arbete/samarbete, i andra med ofokuserat ensamarbete."* Rådslistan, ordagrant: *"Byt ensamarbete mot lärarlett arbete enskilt och i grupp."* Och om riktningen i 1:1 som det faktiskt bedrevs, ordagrant: *"Resultatet av 1:1 – som det bedrivits hittills – är alltså (i genomsnitt) att man får mindre undervisning, om man med det menar lärarledd undervisning."* Guidens två följande meningar ("Where the teacher stepped back and let the device 'take over,' results fell. Where the teacher reinforced their own pedagogical work with the device as an aid... results improved") återger samma kontrast. | **står.** Riktningen är källans egen och står på tre ställen: de framgångsrika skolorna ersatte ofokuserat ensamarbete med *lärarlett* arbete, rådet är att byta ensamarbete mot lärarlett arbete, och 1:1 som det bedrevs gav *mindre* lärarledd undervisning. Guidens "more teacher-led time, not less" är en trogen sammanfattning, inte en vändning av fyndet. **Ingen ändring i guidetexten, och därför ingen vaktrad** (bara ett fynd som ÄNDRAS får en guardrad) — posten står här enligt regel 2, som förbjuder att ett fynd utan åtgärd stryks tyst. Den ordagranna svenska formuleringen är **inte** något guiden citerar, så ingen översättningsmärkning behövs; se S39:s sista parentes för distinktionen. |
| S41 | `weaker students were hit hardest` — **granskningsfynd I1, spec §6 klass 1.** Unos Uno-studiens fördelningsfynd, sidan 14: "...and that *weaker students were hit hardest* — precisely the students schools exist to help". Kursiverad, inte citerad. Helgranskningen fann påståendet SANT; posten saknades. | 1 | 1 | `diva-portal.org/smash/get/diva2:706366/FULLTEXT01.pdf` (samma bok som S17/S18/S39/S40) → **200**, 2026-10-15. Ordagrant ur rådsrutan "Se till att lärarnas arbetstid används för undervisning": *"För mycket ensamarbete drabbar främst de mindre starka eleverna, det vet vi med säkerhet."* (Meningen bryts av en sid- och rubrikväxling i `pdftotext`-utdraget — "För" står före sidnumret 36 och resten efter rubrikraden — ordföljden är återställd här och är entydig i pdf:ens egen layout.) Samma stycke fortsätter, ordagrant: *"Individualisering och ensamarbete är inte samma sak. Skolan ska vara en plats för socialt lärande. Enskilt lärarlett arbete bidrar till elevens lärande, ensamarbete bidrar till att eleverna tappar fokus och drivkraft."* | **står.** Fyndet är källans eget, med källans egen styrkemarkör (*det vet vi med säkerhet* — starkare än guidens oadverbierade påstående, inte svagare). Kausalkedjan guiden drar är också källans: ensamarbetet ökade i 1:1-klassrummen (S18), och för mycket ensamarbete drabbar främst de svagare eleverna. **Ingen ändring i guidetexten, och därför ingen vaktrad** — posten står här enligt regel 2. Ingen översättningsmärkning: påståendet är inte citerat, se S39. |
| S42 | `without a specific school contract` — **granskningsfynd I7, spec §6 klass 2 i ett klass 3-avsnitt.** GDPR-punktlistan på sidan 12: "Don't upload student data to AI services without first verifying that an approved data processing agreement exists for that service. **Many consumer chatbots (e.g. ChatGPT without a specific school contract) do *not* meet this bar.**" Ett namngivet produkt- OCH avtalspåstående i regleringsavsnittet, utan post — alltså en faktamening skriven i strid med regel 1. | 1 | 1 | **Mätt 2026-10-15, och primärkällan gick inte att läsa.** Samtliga förstapartsvägar till OpenAI:s egna villkor svarade **403** (Cloudflare-utmaning mot varje icke-webbläsarklient, både `curl` med webbläsar-UA och WebFetch): `openai.com/policies/data-processing-addendum/`, `openai.com/policies/feb-2024-data-processing-addendum/`, `openai.com/enterprise-privacy/`, `openai.com/chatgpt/education/`, `openai.com/index/chatgpt-for-teachers/` (samma URL som **S24** nådde 200 på 2026-10-14 — blockeringen är ny i dag) och `help.openai.com/en/articles/9853512-data-processing-addendum-dpa`. Wayback-vägen var också stängd (`archive.org/wayback/available` → **429**, `web.archive.org` otillgänglig för verktyget). **Den enda förstapartskälla som svarade:** `trust.openai.com` → **200**, 2026-10-15, som anger att OpenAI:s efterlevnadscertifieringar (SOC 2 Type 2, ISO) täcker *"API, ChatGPT Enterprise, and ChatGPT Edu services"* — konsument-ChatGPT står inte i uppräkningen. Det styrker att skolgraderade åtaganden hänger på affärs- och utbildningsprodukterna, men det är **inte** ett belägg för den avtalsutsaga guiden gjorde, och "many consumer chatbots" är dessutom en marknadsutsaga om flera namnlösa leverantörer som ingen enskild förstapartssida kan bära. **Det nya värdet är i stället hämtat ur regelverket självt**, som är den plats påståendets kärna faktiskt bor: GDPR artikel 28, `gdpr-info.eu/art-28-gdpr/` → **200**, 2026-10-15 (samma värd som Apple-inventeringen redan använder för artikel 35), ordagrant 28(1): *"Where processing is to be carried out on behalf of a controller, the controller shall use only processors providing sufficient guarantees to implement appropriate technical and organisational measures..."* och 28(3) första ledet: *"Processing by a processor shall be governed by a contract or other legal act under Union or Member State law, that is binding on the processor with regard to the controller and that sets out the subject-matter and duration of the processing..."* | **rättat.** Fyndet var `obelagt`: guiden namngav en produkt och dess avtalsläge i sitt regleringsavsnitt utan att någon hämtbar primärkälla belade det, och den enda källa som svarade i dag säger något smalare än guiden gjorde. Jag valde att **mjuka till påståendet så att det inte namnger en produkt**, inte att låta det stå med `obelagt`, av tre skäl: (1) avsnittet är regleringsavsnittet, där specen §6 klass 3 pekar ut just risken att lägga fel plikt på fel part — ett obelagt avtalspåstående om en namngiven leverantör är samma felklass en nivå ner; (2) påståendets pedagogiska arbete kräver inte produktnamnet, bara regeln; (3) regeln är belagd i primärkällan, produktens avtalsläge är det inte. **Ordalydelsen på båda ytorna är nu:** `A consumer account a teacher has signed up for personally is not covered by one: the agreement has to be the school authority's, and it has to name that specific service.` Det är artikel 28 i klartext — biträdesavtalet ingås av den personuppgiftsansvarige (skolhuvudmannen) och gäller en bestämd behandling hos ett bestämt biträde — och det säger samma praktiska sak till läraren som den gamla meningen gjorde, utan att påstå något om en leverantörs avtalsportfölj. `rättat` enligt samma mönster som **S19**, där en obelagd marknadsutsaga skrevs om på plats till ett belagt värde (`obelagt` → `rättat`). |
| S43 | `AI detectors are unreliable` — **granskningsfynd M1.** FAQ-svaret på sidan 21, om att upptäcka AI-skrivna elevtexter: "AI detectors are unreliable and should not be used as evidence." Ett tvåledat påstående utan attribution och utan post. | 1 | 1 | Weber-Wulff, D., Anohina-Naumeca, A., Bjelobaba, S., Foltýnek, T., Guerrero-Dib, J., Popoola, O., Šigut, P. och Waddington, L. (2023). *Testing of detection tools for AI-generated text*. **International Journal for Educational Integrity** 19:26, DOI `10.1007/s40979-023-00146-z`. Förlagets två URL:er (`link.springer.com/article/10.1007/s40979-023-00146-z`, `edintegrity.biomedcentral.com/articles/10.1007/s40979-023-00146-z`) kräver cookie- och idp-omdirigering för icke-webbläsarklienter (303 respektive 301 → 303), så fulltexten är läst i författarnas egen version, `arxiv.org/pdf/2306.15666` → **200**, `pdftotext` 2026-10-15 (samma studie, samma åtta författare, 12 publika verktyg plus Turnitin och PlagiarismCheck). **Led 1 — opålitligheten, ordagrant** (sammanfattningen och diskussionen): *"the available detection tools are neither accurate nor reliable and have a main bias towards classifying the output as human-written rather than detecting AI-generated text"* och *"Detection tools for AI-generated text do fail, they are neither accurate nor reliable (all scored below 80% of accuracy and only 5 over 70%)."* **Led 2 — bevisfrågan, ordagrant** (slutsatsen och diskussionen): *"This paper exposes serious limitations of the state-of-the-art AI-generated text detection tools and their unsuitability for use as evidence of academic misconduct."*, *"Reports provided by detection tools for AI-generated text cannot be used as the only basis for reporting students for cheating."* och, om varför: *"Detection tools for AI-generated text provide simple outputs ... without any possibility of verification or evidence. Therefore, a student accused of unauthorised content generation only on this basis would have no possibility for a defence."* Falskpositiv-spannet i samma studie, ordagrant: *"The probability of false positives ranged from 0% (Turnitin) to 50% (GPT Zero)."* **Institutionell bekräftelse, förstahands:** `vanderbilt.edu/brightspace/2023/08/16/guidance-on-ai-detection-and-why-were-disabling-turnitins-ai-detector/` → **200**, 2026-10-15, ordagrant: *"we do not believe that AI detection software is an effective tool that should be used"*, med skälet *"AI detectors have been found to be more likely to label text written by non-native English speakers as AI-written"*. | **står.** Båda leden är belagda ordagrant i en peer-reviewad primärstudie, och de är belagda med källans EGNA ord för precis de två saker guiden påstår: att verktygen är opålitliga ("neither accurate nor reliable") och att de inte ska användas som bevis ("unsuitability for use as evidence of academic misconduct"). Guidens mening är om något mer försiktig än källan, som också rekommenderar att verktygen inte används i akademiska sammanhang alls. **Ingen ändring i guidetexten, och därför ingen vaktrad.** Påståendet har heller ingen attribution att ta bort — det står redan i guidens eget namn, vilket är exakt det läge C1:s och M2:s påståenden fick efter sina strykningar. Posten står här enligt regel 2. |
| S44 | `Discovery Education` — **granskningsfynd M2.** Del 4:s ingress, EW-exklusiv: "Twelve questions in four categories. **Inspired by Discovery Education's "Should AI Be Used in Schools?"** but reframed for lesson-level decisions, not policy decisions." En attribution till en namngiven resurs hos en namngiven utgivare, utan post. EP:517 bar samma ingress UTAN attributionen — en preexisterande ytdivergens. | 1 | 0 | **Mätt 2026-10-15, fyra vägar, ingen träff på resursen.** (1) Webbsökning `Discovery Education "Should AI Be Used in Schools?" resource activity` → returnerade Discovery Educations egna bloggposter (`discoveryeducation.com/blog/educational-leadership/ai-in-education/` — *"The Pros and Cons of AI in Education: Benefits, Risks, and Real Examples"* — samt `.../ai-in-the-classroom/` och `.../ai-for-school-purchasing-considerations/`) men ingen resurs, lektion eller aktivitet med den titeln. Den titel som faktiskt bär orden tillhör **en annan utgivare**: `now.fordham.edu/university-news/should-ai-be-used-in-schools-weighing-the-benefits-and-risks/` (Fordham University). (2) Webbsökning `"Should AI Be Used in Schools" discoveryeducation.com` begränsad till `discoveryeducation.com` → nio träffar, samtliga bloggposter och produktsidor, ingen med titeln. (3) `bing.com/search?q="Should AI Be Used in Schools?" "Discovery Education"` → ingen Discovery Education-sida med den titeln i resultaten. (4) `html.duckduckgo.com/html/?q="Should AI Be Used in Schools" site:discoveryeducation.com` → CAPTCHA, inga resultat (mätningen räknas som **utan utfall**, inte som bekräftelse). | **struket.** Resursen går inte att belägga. Helgranskningen kunde inte bekräfta att den finns, och fyra oberoende sökvägar i fixvågen hittade den inte heller — det närmaste är en bloggpost hos Discovery Education med ett annat namn, och en artikel med nästan exakt den titeln hos en helt annan utgivare (Fordham). Samma regel som C1: en attribution som inte går att belägga lämnar guiden, och påståendet den bar får stå på egna meriter. **Utfall: attributionen är borta ur EW; checklistan står kvar oförändrad.** Ingressen lyder nu `Twelve questions in four categories. Reframed for lesson-level decisions, not policy decisions. Works as a quick check before a lesson and as the basis for collegial conversations.` **Ingen vaktrad är möjlig:** EW 1 / EP 0 redan före strykningen, alltså `saknas_på_en_yta` från start — samma hantering som S36 (Gerlich) och Apples IMY-post. Strängen kan heller inte vaktas i förbudslistan, som bara läser den levererade PDF:en (byggd ur EP, där attributionen aldrig stod). **Sidoeffekt:** EW:s ingress är nu ordagrant EP:s, så en av de EW-exklusiva meningar granskningen räknade är borta — en följd av strykningen, inte en harmonisering (se "Ytdivergenser"). |

## Ytdivergensen i sin helhet, mätt 2026-10-15 (granskningsfynd I8)

**Rundan harmoniserar INTE ytorna.** Ägarens beslut (brevet) står: guiden byggs inte ut
för att göra EW och EP identiska. Det här avsnittet är därför ett **underlag för nästa
runda**, inte en uppgiftslista — men det är mätt i sin helhet i stället för att antas,
vilket var granskningens anmärkning.

### Metoden, så att talen går att reproducera

Båda ytornas synliga text extraheras (`<script>`/`<style>`/HTML-kommentarer bort,
block-element bryts isär till egna rader FÖRE meningsdelningen så att en rubrik aldrig
klistras ihop med nästa stycke, inline-taggar bort, HTML-entiteter avkodade, typografiska
apostrofer och tankstreck normaliserade, blanktecken kollapsade). Meningar under 25
tecken räknas inte — de är etiketter och brödsmulor, inte innehåll. **Ytornas egna skal
räknas inte:** `<nav>`, `<footer>`, licensbandet och webbytans hero-banner är
navigationskrom, inte guidetext. Två meningar är "samma" om deras gemener-och-siffror
nyckel är identisk; en mening som bara finns på en yta jämförs sedan med `difflib` mot
den andra ytans meningar, och en likhet ≥ 0,60 räknas som **omskrivningspar** (samma
mening, annan längd eller annat ordval) i stället för som innehållslucka.

**Talen skiljer sig från helgranskningens 34 EW-exklusiva / 19 EP-exklusiva, och det är
metoden, inte ytorna, som skiljer** — en annan meningsdelare ger ett annat antal av
samma underliggande skillnader. Talen nedan är de som går att reproducera med metoden
ovan.

### Talen

| mätning | EW-meningar | EP-meningar | EW-exklusiva | EP-exklusiva |
|---|---|---|---|---|
| bascommit `c66ee5c` (före rundan) | 287 | 279 | **39** | **31** |
| efter fixvågen (HEAD) | 284 | 277 | **37** | **30** |

Av HEAD:s 37 + 30 exklusiva meningar är **17 omskrivningspar** (samma mening på båda
ytorna, olika ordval eller längd — EP är genomgående den avkortade), vilket lämnar
**20 rent EW-exklusiva** och **13 rent EP-exklusiva** meningar.

**Praktiskt taget allt är preexisterande.** Varje exklusiv mening vid HEAD är
återsökt i bascommiten, på sin egen yta och på den andra: 35 av 37 EW-exklusiva och 29
av 30 EP-exklusiva fanns redan vid `c66ee5c`, i samma roll. **Två undantag, båda
följder av rundans egna rättelser och ingen av dem en ny innehållslucka:**

1. **EP:s Deng-mening** (sidan 6) — `A 2024 meta-analysis (Deng et al., Computers &
   Education, 69 studies identified) found that...` mot EW:s `In one corner stands a 2024
   meta-analysis (Deng et al., ...) finding that...`. Meningen är ny (Task 7, S34), men
   divergensens FORM är ärvd: det struckna Wang & Fan-citatet (S05/S06) bar exakt samma
   par — EW:s "In one corner stands a substantial 2025 meta-analysis..." mot EP:s "A
   substantial 2025 meta-analysis...". Ersättningen ärvde alltså den gamla meningens
   ytdivergens tillsammans med dess plats.
2. **EW:s checklistingress** — `Reframed for lesson-level decisions, not policy
   decisions.` Dess längre förlaga (`Inspired by Discovery Education's "Should AI Be Used
   in Schools?" but reframed for...`) var EW-exklusiv redan i bascommiten; fixvågens
   strykning av attributionen (S44) kortade meningen men stängde inte divergensen — EP:s
   ingress saknar fortfarande ledet helt.

**En divergens är STÄNGD av fixvågen**, som bieffekt och inte som mål: sidan 15:s
underrubrik bar två olika ordalydelser (`What international guidance says` på EP,
`What education authorities say` på EW) och är nu `Where to start` på båda — följden av
att C1:s obelagda attribution måste bort på båda ytorna och av att en `aktiv`-vaktrad
kräver ordagrann identitet (se S38).

### De substantiella fallen, namngivna

**Rent EP-exklusivt — printytans avslutning (sex meningar, det största enskilda fallet):**
`A skilled teacher's most important tool is judgement.` · `AI is the most powerful tool
we've yet seen for amplifying teaching.` · `It is also the most powerful tool we've seen
for short-circuiting learning.` · `Which of the two it becomes in your classroom isn't
determined by the technology.` · `It's determined by the pedagogical choices you are
already an expert at making.` — plus baksidans tre resurslänkar (`The WISE Framework for
Education`, `Prompt library`, `Tool-specific guides`). Guidens avslutande tanke finns
alltså bara i PDF:en. Detta är raden som redan stod i den förra versionen av det här
avsnittet; mätningen bekräftar och preciserar den.

**Rent EP-exklusivt i löptexten:** `The result is that the student works harder, not
less, but with a sparring partner that raises the ceiling on the work.` (sidan 6,
slutklämmen om AI som sparringpartner — EW:s stycke slutar tidigare) och printytans
eyebrow `Pedagogical decision guide` samt `(E in WISE - Evaluate the outcome.)` som egen
rad.

**Rent EW-exklusivt, substantiellt (tio fall):** `A study (Gerlich 2025) found a
correlation of -0.68 between AI use and critical thinking.` (S36, egen rad nedan) ·
`Classical source criticism isn't obsolete; it's extended by a new category of text where
you can't ask "who said it?" but must ask "what do independent sources say?"` ·
`Detecting a hallucination isn't a specialist skill - it's checking claims.` · det tredje
exempelledet i AI-som-utmanare-stycket (`"I've drafted an op-ed, which counter-arguments
are strongest and how would I address them?"`) · `(E in WISE - Evaluate the outcome.)
Plan a concrete follow-up - a short quiz, an oral presentation, a written reflection -
where the student, without AI, has to demonstrate what they've learned.` · tre
checklist-/FAQ-utbyggnader (`If not - wait on using AI for this task until you do, or
plan the lesson so you evaluate AI responses together as a class.`, `If not - do a short
joint exercise on the large screen before the actual AI lesson.`, `If in doubt - ask your
data protection officer or IT coordinator before the lesson, not after.`) · `In the EU
this means GDPR compliance with a signed data processing agreement; outside the EU check
the equivalent rules` · `In the EU, national DPAs publish guidance; outside the EU, check
your country's privacy regulator.` · och WISE-hänvisningarna (`A full walkthrough of the
WISE framework - with separate versions for teachers and school leaders - is available
at choosewise.education/wise/.`, `It's free, shareable, and works as a reference for
individual lesson planning as well as for a school's or district's AI strategy.`, `Other
material handles that - including the practical prompt sets and tool-specific guides on
choosewise.education.`).

**Mönstret, och det är det nästa runda behöver veta:** divergensen är inte slumpmässig.
EW är den utförligare ytan i löptext, checklista och FAQ (de 17 omskrivningsparen har EP
som den avkortade i samtliga fall), medan EP har en avslutning och ett resursblock som
EW helt saknar. Ingen av de 67 exklusiva meningarna bär ett faktapåstående som saknar
post i den här filen — det är kontrollerat mot postlistan ovan — så divergensen är en
**redaktionell** skuld, inte en faktaskuld.

## Ytdivergenser — tre mätta fall utan vaktrad

Vakten (när den kopplas in för den här guiden, spec §7) kräver att en `aktiv`-rad står
**ordagrant på båda** engelska ytorna. Tre mätta fall gör det inte, och får därför ingen
rad. De står här i stället, som Apples IMY-post gör det för sin guide.

| värde | EW | EP | vad divergensen är |
|---|---|---|---|
| `correlation of -0.68` (S36, Gerlich 2025; var `-0.75` före Task 12) | 1 | 0 | EW bär hela meningen om Gerlich-studien (sidan 6, direkt efter Lee et al.); EP har ingen motsvarighet — printytans stycke om "Challenging thinking, or replacing it" slutar efter Lee et al.-meningen. Se S36 för källkontrollen och rättelsens två led (siffra + landsepitet). Meningen är EW-exklusiv både före och efter Task 12:s rättning, så ingen `aktiv`-rad är möjlig oavsett vilket värde meningen bär. |
| `GDPR in practice (EU) / equivalent data protection rules elsewhere` — rubriknivå | h3 (0 som h2) | h2 (1) | Rubrikens ORD är identiska, ordagrant, på båda ytorna (`grep` bekräftar full textmatch) — det här är INTE en sträng som saknas. Divergensen är strukturell: EP ger meningen sin egen sida med eyebrow "Regulation — continued" och en egen `<h2>`, som en jämbördig andra regleringsrubrik vid sidan av "GDPR and the EU AI Act — what teachers need to know". EW nästlar samma mening som en underordnad `<h3>` inom den enda sektionen "Regulation" (`id="p2-law"`), utan egen eyebrow. En läsare av EP möter alltså GDPR-i-praktiken som en egen huvudrubrik; en läsare av EW möter den som en underrubrik till AI Act-avsnittet. Ingen `aktiv`-rad är möjlig på rubriktexten (den är redan identisk och skulle mäta 1/1), men rubrikNIVÅN i sig divergerar och är dokumenterad här som den kända skillnaden brevet syftade på. |
| `A skilled teacher's most important tool is judgement.` + dess efterföljande stycke ("AI is the most powerful tool we've yet seen for amplifying teaching...") | 0 | 1 | EP:s baksidestext (`back-cover`) bär en avslutande rubrik och ett helt stycke som EW aldrig får någon motsvarighet till — EW:s sista innehållssektion är licensbandet rakt in i footern — CTA-bandet ("Take the guide with you") med det ouppfyllbara nedladdningslöftet är struket av Task 12 (2026-10-15), så avståndet till EP:s avslutande stycke är nu ännu kortare, inte längre. Printytans avslutande tanke ("vem som vinner eller förlorar bestäms inte av tekniken, det bestäms av det pedagogiska valet du redan är expert på") finns alltså bara i PDF:en. Detta är den av de två kända divergenserna som är en ren innehållslucka (sträng helt frånvarande), till skillnad från GDPR-rubriken ovan (sträng identisk, bara nivå/placering skiljer). Ägarens beslut (brevet) är att guiden inte byggs ut för att harmonisera ytorna — raden står kvar som dokumentation, inte som uppgift att åtgärda. |

**Rättelse av brevets egen premiss:** brevet beskriver den andra raden som att "printytans
GDPR-rubrik ... saknas på webbytan." Det stämmer inte ordagrant — rubrikens text finns på
EW, ordagrant, bara en nivå ner (`<h3>` i stället för `<h2>`) och utan egen sida/eyebrow.
Den tredje raden (det avslutande stycket) är däremot exakt den rena frånvaro brevet
beskriver. Se rapporten för samma distinktion i klartext.

## Utfallsräkningen

**44 poster.** Talen nedan är **maskinräknade**, aldrig skrivna för hand — det är
avsnittets enda regel, och den förra versionen bröt den: den påstod 36 poster
`{står 23, falskt 4, rättat 3, struket 2, lagt till 2, obelagt 2}`, en räkning som inte
gick att reproducera med dess eget skript. Helgranskningen körde skriptet och fick **37**
`{står 22, rättat 8, struket 3, lagt till 3, falskt 1, obelagt 0}`. Fixvågen 2026-10-15
reproducerade granskningens tal exakt mot den committade filen och körde sedan om
skriptet SIST, efter alla sina egna ändringar — talen nedan är den körningen.

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
→ {'rättat': 10, 'står': 26, 'struket': 5, 'lagt till': 3} summa 44
```

| verdikt | antal |
|---|---|
| står | 26 |
| rättat | 10 |
| struket | 5 |
| lagt till | 3 |
| falskt | 0 |
| obelagt | 0 |
| föråldrat | 0 |
| UTAN VERDIKT | 0 |

Summan 26+10+5+3+0+0+0+0 = **44**, lika med det totala postantalet (S01–S44). Varje
rad bär ett verdikt: `UTAN VERDIKT` är 0, och `falskt`/`obelagt`/`föråldrat` är 0 därför
att varje sådant fynd har fått ett UTFALL — rättat på plats, struket ur guiden, eller
omklassificerat när cellen visade att utfallet redan var ett annat (S20, se I4 nedan).

**Delta mot granskningens 37, rad för rad, så att varje förändring går att spåra:**

| verdikt | granskningen (37) | fixvågen (44) | vad som hände |
|---|---|---|---|
| står | 22 | 26 | **+4**: S39, S40, S41 (de tre Unos Uno-påståenden granskningen fann SANNA men utan post — I1) och S43 (AI-detektorpåståendet — M1) |
| rättat | 8 | 10 | **+2**: S42 (produktpåståendet i GDPR-punkten mjukat till och belagt mot GDPR artikel 28 — I7) och **S20**, omklassificerad från `falskt` därför att dess egen cell dokumenterade en omskrivning på plats med ett nytt källbelagt värde plus en `aktiv`-rad på det värdet (I4) |
| struket | 3 | 5 | **+2**: S38 (UNESCO/OECD-attributionen — C1) och S44 (Discovery Education-attributionen — M2). Båda följer spec §6 klass 1: attributionen går, påståendet stannar i guidens eget namn |
| lagt till | 3 | 3 | oförändrat |
| falskt | 1 | 0 | **−1**: S20:s omklassificering (I4) |
| obelagt | 0 | 0 | oförändrat — C1:s och I7:s fynd VAR `obelagt`, men båda fick ett utfall (`struket` respektive `rättat`) i samma vända, så ingen post stannar i det läget |

**Talen gäller per den commit de räknades i (fixvågens commit) och blir inaktuella igen
så snart en senare runda sätter eller ändrar en verdiktcell. Räkna om maskinellt med
skriptet ovan — ingen tabell i det här avsnittet får någonsin fyllas i för hand.**

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
# (ursprungsverdikt `falskt`: siffran -0.75 hör i källan till ett annat
# variabelpar, och "Swiss study" beskrev datan, inte bara institutionen).
# Samma princip som IMY i Apple-inventeringen: en sträng som bara står på en
# yta vaktas inte som `aktiv`, oavsett vad en framtida rättning landar på.
#
# Task 12 (2026-10-15) har rättat meningen på EW, i samma post (verdikt nu
# `rättat`, inte en ny id): -0.75 → -0.68 (källans egen siffra för paret
# guiden påstår, "AI use and critical thinking") och "A Swiss study" struket
# (urvalet är brittiskt; institutionen är schweizisk, men guiden påstod inte
# institutionen, den påstod datan). "among younger users" föll bort i samma
# svep — källan knyter aldrig sin korrelation till åldersgruppen. Fortfarande
# INGEN RAD: rättningen ändrar bara VILKET värde den EW-exklusiva meningen
# bär, inte att den förblir EW-exklusiv — se S36:s cell och raden i
# "Ytdivergenser" för ordalydelsen före/efter.
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
# Task 10 — checklistan och FAQ:n, sidorna 17–21.
#
# S29, andra förekomsten — FAQ:ns "EU AI Act — the short answer" (sidan 21)
# bar fortfarande den gamla risknivå-benämningen, men i HYFENERAD form
# (`minimal-risk`, inte `minimal risk` med mellanslag). S28/S29:s befintliga
# `borttaget`-ankare ovan (`minimal risk`, mellanslag) matchade den INTE —
# `normalise()` slår bara om Unicode-bindestreck till ASCII-hyphen, den slår
# aldrig om hyphen till mellanslag — så den stale frasen hade överlevt
# Task 8:s rättelse osynligt för vakten. Samma sakfel som S29 (Aktens fjärde
# nivå heter "Minimal or no risk"), på en andra plats guiden aldrig hade
# synkroniserat. Rättad till `<em>Minimal or no risk</em> category` på båda
# ytorna. `minimal-risk` (med bindestreck) förekom exakt en gång per yta och
# var hela felet på den platsen — inget legitimt kvarvarande bruk av just
# den hyfenerade formen — så den är ett säkert eget `borttaget`-ankare,
# skilt från S29:s ursprungliga mellanslagsankare ovan (de är olika strängar
# för `normalise()`, trots att de beskriver samma sakfel).
S29 | en | minimal-risk | borttaget
#
# S30 — tråden stängd. Task 8 skrev in artikel 27 på sidan 11 men lämnade
# FAQ-svaret om DPIA (sidan 21) med bara GDPR artikel 35 — en läsare som
# bara läser FAQ:n missade AI Act:s egen, separata konsekvensbedömning.
# Samma mening (ordagrant på båda ytorna) är nu skriven in i DPIA-svaret:
# "The AI Act adds a separate requirement for the same high-risk systems,
# education included: Article 27's fundamental-rights impact assessment
# before first use, whether the school is publicly run or an independent
# provider of a public service — a GDPR DPIA does not cover it." Ankaret är
# den korta slutklämmen, unik för just den här meningen (skiljer den från
# S28:s identiska "Article 27"-fras på sidan 11, så en framtida strykning av
# FAQ-meningen specifikt slår rött utan att en strykning av sidan 11:s mening
# gör det, och vice versa).
S30 | en | a GDPR DPIA does not cover it | aktiv
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
# S37 — granskningens fynd (2026-10-15) belade SchoolAI mot dess egen sida
# (schoolai.com/mission-control), samma ribba som de fem andra
# leverantörerna mättes mot. Ägarens beslut: namnge BÅDA leverantörerna,
# ingen i singular "the exception". `SchoolAI` är nu en skriven,
# källbelagd del av guidetexten på båda ytorna — `aktiv`, inte `borttaget`.
S37 | en | SchoolAI | aktiv
#
# ══════════════════════════════════════════════════════════════════════
# FIXVÅGEN 2026-10-15 — helgranskningens ett Critical och åtta Important.
# Blocket är inte längre "resten fylls av senare uppgifter": rundan är
# klar, och raderna nedan är de sista. Reglerna de följer är desamma —
# varje `aktiv`-rad bär det KORTASTE värde som bär påståendet (ett tal,
# ett namn, en rubrik), aldrig hela satsen (regel 3 i huvudet ovan), och
# en rad krävs ordagrant på BÅDA engelska ytorna för `aktiv`; en kandidat
# som bara träffar en yta får ingen rad, bara en notering i prosan (samma
# hantering som Apples IMY-divergens).
# ══════════════════════════════════════════════════════════════════════
#
# S38 — attributionen till UNESCO/OECD, sidorna 15 och 20 (granskningens
# Critical). Rådet står kvar ord för ord; bara attributionen är borta, se
# S38:s cell för de sex primärdokument som mättes på noll. Fyra
# `borttaget`-ankare, ett per struken ordalydelse:
#   - de TVÅ gamla underrubrikerna, som divergerade mellan ytorna (EP bar
#     "What international guidance says", EW "What education authorities
#     say" — en preexisterande ytdivergens som C1-rättelsen stänger).
#     Båda är nu 0/0, så båda kan vaktas som `borttaget`; en rad per
#     ordalydelse, eftersom en återinföring kan träffa vilken som helst
#     av dem.
#   - de två attributionssatserna, var och en unik för sin mening.
# `(UNESCO, OECD` är MEDVETET INTE ett ankare, trots att det är den
# kortaste strängen som fångade båda förekomsterna (måttkolumnen mäter
# den): ett `borttaget` på den hade varit regel 3:s undantagsfall, för
# `UNESCO` lever legitimt kvar på sidan 8 (ramverket, S11) och `OECD` på
# sidorna 4 och 14 (S03, S12/S13) — en framtida, legitim mening som
# nämner båda organen i en parentes hade slagit rött mot en attribution
# som aldrig skrevs tillbaka. Ankarna är därför de längre, distinkta
# ordalydelserna.
S38 | en | What international guidance says | borttaget
S38 | en | What education authorities say | borttaget
S38 | en | Guidance from major education bodies | borttaget
S38 | en | consistently recommends | borttaget
S38 | en | Where to start | aktiv
S38 | en | If you take one practical step from this guide | aktiv
S38 | en | an intermediate mode this guide recommends instead | aktiv
#
# S39 — Grönlund-citatet, sidan 14 (granskningens I1, första av tre).
# Citatets ord är orörda; märkningen att det är en översättning är
# tillagd. Inget är borttaget, så ingen `borttaget`-rad — bara den nya
# märkningen vaktas, och den är unik i hela guiden.
S39 | en | translated from the Swedish | aktiv
#
# S40/S41 — de två andra Unos Uno-påståendena granskningen kontrollerade
# ("more teacher-led time, not less", "weaker students were hit hardest").
# Båda `står` mot primärkällan och guidetexten är oförändrad: INGEN RAD,
# samma regel som för S03/S07/S09/S10 och S27/S31–S33 — bara ett fynd som
# ÄNDRAS får en guardrad. Posterna finns, med källcell och verdikt; det
# är regel 2 som kräver dem, inte vakten.
#
# S03 — det klippta OECD-citatet på sidan 4 (granskningens M7). Citatet
# slutade tyst före källans ", as seen across PISA participating
# countries" och har nu en ellips som visar klippet. Det är en
# prosaändring, så posten får sina första rader. Den oelliderade formen
# är en säker `borttaget`-sträng: `achievement."` (direkt citattecken
# efter punkten) kan inte matcha den nya `achievement …"`, eftersom
# `normalise()` bara slår om Unicode-bindestreck och kollapsar blanksteg
# — den infogar aldrig ett mellanslag mellan ordet och citattecknet.
S03 | en | stagnating student achievement." | borttaget
S03 | en | stagnating student achievement …" | aktiv
#
# S25, andra förekomsten — avsnittsrubriken på sidan 15 (granskningens
# I2). Rubriken sa att dagens verktyg INTE visar läraren vad eleverna
# frågar, medan stycket under den namnger två leverantörer som gör det
# (Khanmigo och SchoolAI, ägarbeslut 2 och S37). Motsägelsen var skapad
# av rundans egna rättelser, inte ärvd. Rubriken bär nu avsnittets
# faktiska poäng: lärarvyn är görbar, men de flesta verktygen ger den
# inte. `today's AI tools don't show teachers` förekom exakt en gång per
# yta och VAR hela felet — ett säkert kort ankare utan undantag. Det nya
# ankaret är avsiktligt den längre formen MED `most ... still`, eftersom
# den korta strängen `show teachers what students are asking` är gemensam
# för den gamla och den nya rubriken och därför inte kan vakta att
# rättelsen står kvar.
S25 | en | today's AI tools don't show teachers | borttaget
S25 | en | most AI tools still don't show teachers | aktiv
#
# S42 — det namngivna produkt- och avtalspåståendet i GDPR-punktlistan,
# sidan 12 (granskningens I7). Två `borttaget`-ankare, båda unika för den
# struckna satsen och båda 0/0 efter rättelsen. `ChatGPT` ensamt är INTE
# ett ankare: produkten nämns legitimt på sidorna 15 och 20 (S19, S24,
# S21) — regel 3:s undantag igen.
S42 | en | Many consumer chatbots | borttaget
S42 | en | without a specific school contract | borttaget
S42 | en | has to name that specific service | aktiv
#
# S43 — "AI detectors are unreliable and should not be used as evidence"
# (sidan 21, granskningens M1). `står` ordagrant mot Weber-Wulff m.fl.
# (2023); guidetexten är oförändrad: INGEN RAD, samma regel som S40/S41.
#
# S44 — Discovery Education-attributionen i Del 4:s ingress (granskningens
# M2), struken eftersom resursen inte går att belägga. EW 1 / EP 0 redan
# FÖRE strykningen, alltså `saknas_på_en_yta` från start: INGEN RAD, samma
# hantering som S36 (Gerlich) och Apples IMY-post. Strängen kan heller
# inte vaktas i förbudslistan, som bara läser den levererade PDF:en
# (byggd ur EP, där attributionen aldrig stod).
#
# S35 — läsartilltalet. Fixvågens enda beröring av posten är att dess
# FÖRE-värden är reproducerade (se "Poster"-ingressen, granskningens I5).
# Guidetexten är orörd och posten har aldrig haft en rad.
```

