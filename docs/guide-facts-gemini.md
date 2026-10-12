# Påståendeinventering — Gemini- och NotebookLM-guiden

**Rundan:** Gemini/NotebookLM-guiden, internationell omriktning. Spec: `docs/superpowers/specs/2026-10-12-gemini-guide-international-design.md`
**Upprättad:** 2026-10-12
**Faktakontrollerad:** (Task 4)

Varje volatilt faktapåstående i de **engelska** ytorna, med alla sina
förekomster. De svenska ytorna ingår inte i rundan (spec §1) och har därför
inga poster.

Ytorna: **EW** `_unpublished/guides/gemini-notebooklm/index.html` · **EP**
`_unpublished/exports/gemini-notebooklm-print-a4-en.html` · **QS**
`_unpublished/exports/gemini-notebooklm-quick-start-en.html`

**QS står utanför ytkonsistensvakten** — avsiktligt, spec §5: quick-starten är
en tredje yta med egen, kortare formulering, och kravet "ordagrant på alla
ytor" vore rött från dag ett och därmed värdelöst. Den bevakas i stället av
förekomstkolumnen här, av PDF-facit, och av leveransvakten
(`scripts/tests/test_guide_delivery.py`).

## Hur källorna läses

Varje sida hämtas som rå HTML och läses ordagrant; texten extraheras lokalt ur
markupen. Ingen sida sammanfattas av ett annat modellanrop, och en
sammanfattning är aldrig källa till ett värde. Där källor går emot varandra
står båda, och den nyare vinner — med noteringen att de skiljer sig.

**Googles sidor kan svara 403 mot `curl`**, precis som Microsofts
marknadsföringssidor gjorde i förra rundan. Ett påstående utan hämtbar källa
blir `obelagt` och skrivs om utan siffra — det får inte bli `stämmer` på en
sida ingen kunde läsa.

**Två poster hämtar sitt belägg ur en annan inventering.** AI Act-fakta är
redan verifierade i `docs/guide-facts-claude.md` post **P13** (källa:
Europeiska kommissionen, `digital-strategy.ec.europa.eu`, läst 2026-10-08).
Där P13 räcker står `korsref P13` i källkolumnen och ingen ny hämtning görs —
det var hela skälet att AI Act fick stanna (spec §3).

## Poster

Utfallen är `stämmer`, `fel: <rätt värde>` och `obelagt: <vad källan säger i
stället>`. **Varje utfallscell inleds med sin token**, så att kolumnen går att
skanna utan att läsa resonemanget.

`fel` har två betydelser, ärvda från Copilot-inventeringen och de får inte
läsas som samma sak. `fel: <rätt värde>` betyder att en hämtad källa säger
något annat än ytan. `fel (omfång)` betyder att påståendet inte är sakligt
osant men ligger utanför det omfång rundan valde (spec §3) — **ingen källa
motsäger det, och den som letar efter en sådan letar förgäves.**

**G01–G34 är de kända posterna ur Task 3-briefen; två av dem bar en felaktig
radpekare i briefens tabell och är rättade här (G08, G14 — se Observationer).
G35–G47 är nya poster som steg 2–3:s mätning och en genomläsning av båda
huvudytorna lade till.**

| id | påstående idag | typ | EW | EP | QS | källa + datum | utfall |
|---|---|---|---|---|---|---|---|
| G01 | Datumstämpeln "April 2026" — omslagets attributrad (EP) och webbytans nedladdningsfot "Updated April 2026." (EW) | datumstämpel | 1229 | 486 | — | | |
| G02 | Avslutningens signatur "— Johan Lindström, April 2026" | datumstämpel | — | 1623 | — | | |
| G03 | "Since 8 April 2026 the two tools sync bidirectionally" — det daterade produktpåståendet, samt dess odaterade varianter ("Since April 2026 …") | funktion | 100, 118, 130, 351, 1144 | 610, 628, 640, 719, 847, 1546 | — | | |
| G04 | Innehållsförteckningens tio sidnummer (3, 5, 8, 13, 20, 24, 28, 32, 34, 40) | datumstämpel | — | 502, 509, 516, 523, 530, 537, 544, 551, 558, 565 | — | | |
| G05 | `Workspace for Education` som namn och licensinnehåll (24 träffar vardera på EW/EP) | produktnamn | passim (24) | passim (24) | 187 | | |
| G06 | `Gems` — asymmetrisk EP 25 / EW 24 | produktnamn | passim (24) | passim (25) | — | | |
| G07 | `Canvas` som namngiven funktion | produktnamn | passim (19) | passim (19) | — | | |
| G08 | `Deep Research` som "multi-step agent/research agent" — **briefens platsangivelse "EP 1416 m fl" pekade fel (EP1416 är ett ovidkommande prompt-kort); rätt rad är 807/633** | funktion | 123, 307 | 633, 807 | 299 | | |
| G09 | `Audio Overview` — asymmetrisk EP 10 / EW 11 — plus de fyra formaten och "added September 2025" | funktion | 127, 221, 222, 260, 332, 347, 384, 405, 424, 576, 1201 | 637, 728, 729, 764, 830, 878, 896, 915, 1061, 1603 | 279, 280, 281, 295 | | |
| G10 | Interaktivt läge för Audio Overview "still in beta" / "currently in beta" | funktion | 222, 333 | 729, 831 | — | | |
| G11 | `Video Overview` som endast NotebookLM-sidig | funktion | passim (8) | passim (8) | 280 | | |
| G12 | De två licensvägarna: `Education Plus` och `Teaching & Learning add-on` | licens | 482 | 970 | — | | |
| G13 | `NotebookLM Enterprise` på Google Cloud med EU-residens; Workspace-versionens residens | dataresidens | 485, 537 | 973, 1023 | — | | |
| G14 | `Gemini for Education` som licensnamn — **briefens rader (EP968/EW480) var tomrader, av fel med ett steg; rätt rader är rubriken och checklistraden** | produktnamn | 481, 513 | 969, 1001 | — | | |
| G15 | Utrullningsordningen "AI Ultra, Pro, and Plus subscribers; the free tier follows" | licens | 351 | 847 | — | | |
| G16 | Åldersgolven: Gemini Live 18+, premium-Workspace-funktioner 18+, NotebookLM 13+ — samlad lista över alla formuleringar, inte bara förstaträffen | åldersgräns | 134, 138, 155, 316, 318, 471, 473, 496 | 644, 648, 662, 814, 816, 959, 961, 984 | 314 | | |
| G17 | Granulära per-app-toggles "rolling out through 2026" | funktion | 494 | 982 | — | | |
| G18 | Google Classroom AI-funktioner "free with all Workspace for Education accounts" | licens | 499 | 987 | — | | |
| G19 | "I have built 140 such styles" + pekaren till style-biblioteket — **utökad med tre förekomster briefen inte listade** ("Johan's 140 NotebookLM styles", "The 140 styles connection", TOC-raden) | URL | 325, 344–345, 607, 611, 615–682 | 548, 823, 842–843, 1090, 1094, 1164 | — | | |
| G20 | Matt Miller-citatet "a personal tutor that only knows what you teach" (Ditch That Textbook, januari 2026) | citat | 126, 212 | 636, 719 | — | | |
| G21 | Säfström/Folkebrant-exemplet, Fristadsskolan i Eskilstuna, Pedagog Eskilstuna februari 2026 — källbelagt, **utökad med en tredje förekomst per yta ("Extra example…") som briefen inte listade**; stanna/ta bort avgörs efter Task 4 | inramning | 223, 333, 405 | 730, 831, 896 | — | | |
| G22 | "including Swedish and other EU languages" som språkexempel | inramning | 333 | 831 | — | | |
| G23 | Huvudflödets juridikpassage "Data residency, GDPR, and national context" | regelverk | 484–491 | 972–979 | — | | |
| G24 | Bonuskapitlets GDPR-halva: ingressen och hela avsnittet "GDPR fundamentals for schools using AI" | regelverk | 530, 532–539 | 1016, 1018–1025 | — | | |
| G25 | AI Act-ingressens "entered into force on 1 August 2024 and phases in through 2026 and beyond" | regelverk | 542 | 1028 | — | | |
| G26 | Risknivåernas fyra namn: Minimal risk / Limited risk / High risk / Prohibited — pyramiden och brödtexten (EW-brödtexten lokaliserad: 576–579) | regelverk | 551, 556, 561, 566, 576, 577, 578, 579 | 1037, 1042, 1047, 1052, 1061, 1062, 1063, 1064 | — | | |
| G27 | Artikel 4-påståendena: "has applied since 2 February 2025", "in force since 2 February 2025", "applies since February 2025" samt de odaterade variantraderna — **briefen gav bara EP-rader; EW-motsvarigheterna saknades helt och är tillagda här** | regelverk | 84, 421, 449, 543, 590, 1003, 1187 | 596, 912, 940, 1029, 1075, 1430, 1589 | — | | |
| G28 | "Sweden, as of April 2026, is among the countries that have not… the dominant framework for Swedish schools" | inramning | 545 | 1031 | — | | |
| G29 | "others (Sweden is a notable example, as of April 2026) have not yet" — **står bara på EP; EW 491 bekräftat utan Sverige-parentesen** | inramning | 491 | 979 | — | | |
| G30 | Promptmallens platshållare "[e.g. GDPR + EU AI Act + your national school-governance law]" — stannar, spec §3 | regelverk | 915 | 1357 | — | | |
| G31 | "I have a full-time job and run this work alongside it" | författarfakta | 1209 | 1611 | — | | |
| G32 | Avslutningens CTA: "you can also reach out through my website (link in the footer)" | inramning | 1209 | 1611 | — | | |
| G33 | Del 3: "Update the school's records of processing (GDPR, a European regulation — Article 30)" | regelverk | 430 | 921 | — | | |
| G34 | Del 3: "You are personally carrying GDPR risk that belongs with your organisation" | regelverk | 443 | 934 | — | | |
| G35 | "confirmed at BETT 2026" — beläggskälla för "Core Gemini AI in Classroom … free for all Workspace for Education accounts" | datumstämpel | 134, 155 | 644, 662 | — | | |
| G36 | "As of BETT 2026, the 'learning standards tagging' feature in Classroom supports the UK, Australia, Canada, Japan, Brazil, Mexico, and Italy" — landlista | funktion | 501 | 989 | — | | |
| G37 | `Gemini 3 Pro` som flaggskeppsmodell, "launched 18 November 2025", en-miljon-tokens kontextfönster, samt de kopplade omnämnandena `Gemini 3 Flash` och `Gemini 3 Pro with Deep Think` | produktnamn | 122, 307, 1137, 1173 | 632, 807, 1539, 1575 | — | | |
| G38 | `Nano Banana 2` — Googles bildmodell, "Released 26 February 2026", alias `Gemini 3.1 Flash Image`, ersätter `Nano Banana Pro`, kapacitet (upp till fem subjekt/fjorton objekt, 512px–4K) | produktnamn | 123, 320–321, 325, 1137 | 633, 818–819, 823, 1539 | — | | |
| G39 | "The newer Learning Guide format (added September 2025) runs in tutoring mode" | funktion | 342 | 840 | — | | |
| G40 | TOC-underrubriken "Eleven common questions answered" (FAQ-antal) | datumstämpel | — | 561–562 | — | | |
| G41 | Rubriken "Five classroom workflows that compound" | datumstämpel | 356 | 850 | — | | |
| G42 | "Your practical compliance checklist" — nio-punktslistan i bonuskapitlet (DPIA, DPA, dataresidens, sekretessinställningar, Article 30-journalföring, AI Act-riskklassning, DPO, Article 4-kadens, larmkanal) — bär bonuskapitlets **fjärde** `Article 30`-förekomst, som annars inte täcks av G23/G24/G33 | regelverk | 581, 583–591 | 1066, 1068–1076 | — | | |
| G43 | Alice Keeler-citatet om Gems: "generic AI that understands nothing about your classroom" | citat | 283 | 785 | — | | |
| G44 | Kasey Bell-citaten: "a podcast for your commute" och "a deeply embedded teaching assistant directly within your workflow" | citat | 309, 427 | 809, 918 | — | | |
| G45 | Eric Curts och `edugems.ai` — "roughly 200 ready-to-use Gems"/"about 200 free education Gems", "growing every month" | produktnamn | 287, 418, 1180 | 789, 909, 1582 | — | | |
| G46 | Googles fyra inbyggda mall-Gems i Classroom: "Study partner, Quiz me, Brainstorm partner, Real-world connector" | produktnamn | 287, 418 | 789, 909 | — | | |
| G47 | Vidareläsningens namnlista över lärarbloggare/podcastare: "Matt Miller, Monica Burns, Kasey Bell, Eric Curts, Alice Keeler, Tony Vincent, Jake Miller" | citat | 1208 | 1610 | — | | |

## Observationer utanför posterna

**Quick-start-ytan (QS) bär noll av de arton strängar leveransvakten
förbjuder** (mätt 2026-10-12, Steg 2: `Swedish\|Sweden\|Skolverket\|IMY\|GDPR\|
Schrems\|DPIA\|Article [0-9]\|data protection authority\|supervisory\|member
state\|April 2026` gav noll träffar i
`_unpublished/exports/gemini-notebooklm-quick-start-en.html`). Till skillnad
från Copilot-guidens quick-start, som pekade läsare mot en 404, har den här
quick-starten varken svensk inramning eller juridisk text att rätta. Det är
inget att åtgärda — bara att inte missa som "förbisett".

**G29 bekräftar en befintlig ytdivergens, inte en hypotetisk.** Printytans
rad 979 bär parentesen "(Sweden is a notable example, as of April 2026)";
webbytans motsvarande mening (rad 491) saknar den redan i dag. De två
engelska ytorna är alltså inte överens om en av rundans känsligaste meningar
innan någon redigering ägt rum — ett tecken på att ytorna har underhållits
olika, inte bara ett datumfel att rätta symmetriskt.

**Tre produktnamn är asymmetriska mellan EW och EP i steg 3:s mätning, och
alla tre förklaras av sidstruktur snarare än av sakligt olika innehåll:**
`Gems` (EP 25/EW 24) och `AI Ultra` (EP 5/EW 6) förklaras av att EW har en
`onerror`-skärmdumpsplaceholder (rad 354, "Google is releasing it first to
AI Ultra, Pro, and Plus subscribers") som EP saknar; `Audio Overview` (EW
11/EP 10) förklaras likadant av EW:s skärmdump-alt-text "NotebookLM Audio
Overview" (rad 347), som EP inte har en motsvarighet till. `Studio` (EP 6/EW
5) förklaras av att EP har en TOC-rad ("Gems, Canvas, Deep Research, Studio,
workflows", rad 520) som EW, utan innehållsförteckning, inte kan ha. Inget av
de fyra är en sakdivergens att rätta — det är formuleringsskillnader av
layouttyp, medtagna här så att Task 5–9 inte letar efter en bakomliggande
sakuppgift som inte finns.

**Briefens kända tabell innehöll två felaktiga radpekare**, hittade i
steg 5:s utökade kontroll och rättade i tabellen ovan: G08 (`EP 1416 m fl`
pekade mot ett ovidkommande kommunikationsprompt-kort; rätt rad är EP 807/
EW 307, med en andra förekomst på EP 633/EW 123) och G14 (`EP 968, EW 480`
var tomrader — ett steg för tidigt; rätt rader är EP 969/EW 481 för
rubriken, plus en andra förekomst på EP 1001/EW 513 som briefen inte
listade alls).

**G27 saknade EW-rader helt i briefen.** Artikel 4-daterings­påståendet
("has applied since"/"in force since"/"applies since … 2 February 2025")
finns ordagrant på webbytan också (rad 84, 421, 1187), och de tre
checklista/promptmall-varianterna har sina egna EW-motsvarigheter (449, 590,
1003). Utan dem hade Task 9 inte vetat var på webbytan rättningen skulle
landa.

## Vaktblock

```guard
# Fylls i Task 12, i samma commit som `gemini` läggs till i
# surfacecheck.GUIDE_SURFACES och factinventory.INVENTORIES.
# Till dess är blocket tomt MED AVSIKT: `test_every_guides_guard_block_is_not_empty`
# kräver både aktiv- och borttaget-rader för varje guide i ytkartan, så
# ett tomt block kan inte samexistera med en ifylld ytkarta.
```
