# Påståendeinventering — Gemini- och NotebookLM-guiden

**Rundan:** Gemini/NotebookLM-guiden, internationell omriktning. Spec: `docs/superpowers/specs/2026-10-12-gemini-guide-international-design.md`
**Upprättad:** 2026-10-12
**Faktakontrollerad:** (Task 4)

Varje volatilt faktapåstående i de **engelska** ytorna, med alla sina
förekomster. De svenska ytorna ingår inte i rundan (spec §1) och har därför
inga poster.

Ytorna: **EW** `_unpublished/guides/gemini-notebook/index.html` · **EP**
`_unpublished/exports/gemini-notebook-print-a4-en.html` · **QS**
`_unpublished/exports/gemini-notebook-quick-start-en.html`

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

**Fyra poster hämtar sitt belägg ur en annan inventering.** AI Act-fakta är
redan verifierade i `docs/guide-facts-claude.md` post **P13** (källa:
Europeiska kommissionen, `digital-strategy.ec.europa.eu`, läst 2026-10-08).
Där P13 räcker står `korsref P13` i källkolumnen och ingen ny hämtning görs —
det var hela skälet att AI Act fick stanna (spec §3). I Task 4 gäller det **G25, G26,
G27 och G48** — den fjärde tillagd här, eftersom briefens tabell listade fyra värden att
rätta men P13 bär ett femte fel (se Task 4:s observationer).

## Poster

Utfallen är `stämmer`, `fel: <rätt värde>` och `obelagt: <vad källan säger i
stället>`. **Varje utfallscell inleds med sin token**, så att kolumnen går att
skanna utan att läsa resonemanget.

`fel` har två betydelser, ärvda från Copilot-inventeringen och de får inte
läsas som samma sak. `fel: <rätt värde>` betyder att en hämtad källa säger
något annat än ytan. `fel (omfång)` betyder att påståendet inte är sakligt
osant men ligger utanför det omfång rundan valde (spec §3) — **ingen källa
motsäger det, och den som letar efter en sådan letar förgäves.**

**G50 är tillagd i Task 9** på koordinatorns ruling: åldersrutans medlemsstatsresonemang, en andra instans av G28/G29:s klass som ingen förekomstmätning fångade. **G01–G34 är de kända posterna ur Task 3-briefen; två av dem bar en felaktig
radpekare i briefens tabell och är rättade här (G08, G14 — se Observationer).
G35–G47 är nya poster som steg 2–3:s mätning och en genomläsning av båda
huvudytorna lade till. G48 och G49 är tillagda i Task 4 och kunde inte hittas av en
förekomstmätning — G48 är ett femte AI Act-fel som bara en läsning mot P13 avslöjar,
G49 är Googles omdöpning av NotebookLM till Gemini Notebook den 16 juli 2026.**

| id | påstående idag | typ | EW | EP | QS | källa + datum | utfall |
|---|---|---|---|---|---|---|---|
| G01 | Datumstämpeln "April 2026" — omslagets attributrad (EP) och webbytans nedladdningsfot "Updated April 2026." (EW) | datumstämpel | 1220 | 486 | — | ytorna själva, EP:486 (omslagets attributrad) och EW:1229 — nu EW:1220, och texten lyder nu "Updated October 2026.", mätt 2026-10-12 | **fel: oktober 2026.** Stämpeln är sex månader gammal och kan per definition inte bära det som hänt sedan dess — namnbytet NotebookLM→Gemini Notebook (16 juli 2026, G49), Classroom för alla åldrar (10 augusti 2026, G16) och licensomläggningen till Google AI Pro for Education (G12). Datumet måste sättas om i samma commit som sakändringarna, annars daterar guiden sig själv till före sina egna rättelser — **BOKFÖRT i Task 9 (2026-10-12):** åtgärden gjordes i Task 5 (`714bda0`-raden i loggen, "datumstämplarna till oktober") men cellen saknade notering. Båda stämplarna bär nu oktober 2026; `grep "April 2026"` ger noll träffar på stämpelraderna. Inga stämplar är redigerade i Task 9. |
| G02 | Avslutningens signatur "— Johan Lindström, April 2026" | datumstämpel | — | 1617 | — | ytan själv, EP:1623 — nu EP:1617 — mätt 2026-10-12 | **fel: oktober 2026.** Samma som G01. Signaturraden och omslagsraden måste bära samma datum — de står i dag på samma månad och får inte glida isär — **BOKFÖRT i Task 9 (2026-10-12):** samma som G01 — signaturraden sattes om i Task 5 och noteringen saknades bara. Orörd här. |
| G03 | "Since 8 April 2026 the two tools sync bidirectionally" — det daterade produktpåståendet, samt dess odaterade varianter ("Since April 2026 …") | funktion | 97, 115, 127, 128, 209, 348, 1135 | 610, 628, 640, 641, 719, 847, 1540 | — | blog.google `/innovation-and-ai/products/gemini-app/notebooks-gemini-notebooklm/` → **200**, `article:published_time 2026-04-08`, läst ordagrant 2026-10-12; support.google.com/gemininotebook/answer/17003757 → **200** | **stämmer** på datum och på själva synkroniseringen. Googles post är publicerad 8 april 2026 och säger ordagrant "Notebooks sync across the Gemini app and NotebookLM"; hjälpsidan säger "Notebooks you create in Gemini Notebook will now automatically appear in Gemini's navigation" och "Changes sync across apps". — **fel: produktnamnet** (se G49). — **fel: "anything you create in one surface is visible and editable in the other"** (EP:640/EW:130, EW-raden nu 127). Googles egen sida säger motsatsen på två punkter, ordagrant: "All shared notebooks created in Gemini Notebook, even ones you own, will not be visible in Gemini" och "Gemini will not have the ability to generate items from the Gemini Notebook Studio panel. This includes … Audio Overviews, Video Overviews, Infographics, Slide Deck … These features are only available in Gemini Notebook." Rätt värde: synken gäller notebooken och dess källor, inte Studio-artefakterna, och inte delade notebooks. — **obelagt: panelens placering** ("sitting between 'My stuff' and 'Gems'") — ingen hämtad sida beskriver sidopanelens ordning — **ÅTGÄRDAT i Task 9 (2026-10-12):** datumet står kvar på **alla** förekomster, både de daterade och de odaterade (EP 610, 628, 640, 719, 847, 1538; EW 97, 115, 127, 209, 348, 1133) — inledande token var `stämmer`, och 8 april 2026 är belagt. De två andra tokenen är åtgärdade: satsen "anything you create in one surface is visible and editable in the other" (EP:640/EW:127) och dess dubblett "both surfaces editable" (EP:847/EW:348) säger nu vad källan bär — notebooken och dess källor synkar, delade notebooks syns inte i Gemini, och Studio-artefakterna kan bara skapas i Gemini Notebook. Den obelagda sidopanelsordningen ("sitting between 'My stuff' and 'Gems'") är borta; hjälpsidans egen formulering (notebooks "appear in Gemini's navigation") står i stället. |
| G04 | Innehållsförteckningens tio sidnummer (3, 5, 8, 13, 20, 24, 28, 32, 34, 40) | datumstämpel | — | 502, 509, 516, 523, 530, 537, 544, 551, 558, 565 | — | ingen hämtbar källa; mätt mot ytan själv 2026-10-12 — EP har 13 `class="page"`-omslag (cover + toc + 10 + closing) medan innehållsförteckningen namnger sidor upp till 40. Inget PDF-facit finns i repot (`find -iname "*facit*"` gav noll) | **obelagt (ytartefakt): sidnumren kan inte beläggas mot HTML-ytan.** De är artefakter av den paginerade PDF-renderingen och hör till `test_guide_pdf_parity.py` / `pdf_body_text.py`, inte till den här inventeringen. Ingen källa motsäger dem — de är okontrollerade, inte felaktiga. Ska verifieras mot en renderad PDF efter att texten ändrats, eftersom varje sakändring i Task 5–9 flyttar brytningarna |
| G05 | `Workspace for Education` som namn och licensinnehåll (24 träffar vardera på EW/EP) | produktnamn | passim (22) | passim (22) | 187 | support.google.com/gemininotebook/answer/16337734 → **200**, ordagrant: "For Workspace and Workspace for Education users, Gemini Notebook is now a core service"; edu.google.com/intl/ALL_us/ai/gemini-for-education/ → **200**, ordagrant: "Gemini for Education is also included in all Google Workspace for Education editions free of charge" — båda lästa 2026-10-12 | **stämmer** — `Workspace for Education` är Googles aktuella namn och sidan räknar upp editionerna (Education Fundamentals, Education Standard, Education Plus, Teaching and Learning add-on). — **fel: licensinnehållet**, se G12. Namnet står kvar; det guiden säger att licensen *ger* är omlagt — **ÅTGÄRDAT i Task 9 (2026-10-12) via G12:** namnet `Workspace for Education` är orört, enligt inledande token. Det licensen *ger* är omskrivet — se G12:s notering. |
| G06 | `Gems` — asymmetrisk EP 25 / EW 24 | produktnamn | passim (22) | passim (24) | — | edu.google.com/intl/ALL_us/ai/gemini-for-education/ → **200**, ordagrant: "Build and use custom AI experts for any topic with Gems"; support.google.com/gemini/answer/13594961 → **200**, ordagrant: "Manage Gems and Skills in the Gems Manager and Skills Manager"; www.edugems.ai → **200**, ordagrant: "Note: Google has announced that Gems will be transitioning to Skills." — samtliga lästa 2026-10-12 | **stämmer** — `Gems` är fortfarande ett namngivet, aktuellt Google-begrepp och står i Gemini for Educations egen funktionslista. — **obelagt: namnet är på väg bort.** Googles egen hjälpsida parar nu Gems med **Skills** ("Gems Manager and Skills Manager"), och Eric Curts, vars bibliotek guiden pekar på, skriver att "Gems will be transitioning to Skills" och konverterar sitt eget bibliotek. **Ingen hämtbar Google-sida anger ett avvecklingsdatum** — påståendet är alltså inte falskt i dag, men det är guidens näst mest färskvarubetonade produktnamn efter G49, och 25 EP-/24 EW-förekomster hänger på det — **INGEN ÅTGÄRD i Task 9 (2026-10-12), med avsikt.** Inledande token är `stämmer` och ingen hämtbar Google-sida anger ett avvecklingsdatum, så `Gems` står kvar på varje förekomst. Den andra tokenen (`obelagt`: namnet är på väg bort) bär ingen siffra och inget datum att stryka — den belagda Gems→Skills-annonseringen är i stället skriven **en gång**, där biblioteket presenteras (se G45). Asymmetrin är mätt om i Task 9: **EP 24 / EW 23** efter G43:s omskrivning (före: 25/24), alltså samma differens — den förklaras av EP:s två TOC-rader mot EW:s skärmdumps-alt-text, och är en formuleringsskillnad, inte en sakdivergens. Se Observationer. |
| G07 | `Canvas` som namngiven funktion | produktnamn | passim (18) | passim (19) | — | support.google.com/gemini/answer/16047321 → **200**, rubrik ordagrant: "Create docs, apps & more with Canvas"; edu.google.com/intl/ALL_us/ai/gemini-for-education/ → **200**: "Write, code, and create - all in one interactive space with Gemini Canvas" — lästa 2026-10-12 | **stämmer** — Canvas är en namngiven, aktuell funktion och ingår i Gemini for Educations kostnadsfria nivå. Notera att edu-sidan skriver **"Gemini Canvas"** där guiden skriver "Canvas"; ingen sakskillnad, men om Task 9 vill matcha Googles skrivning finns den belagd här |
| G08 | `Deep Research` som "multi-step agent/research agent" — **briefens platsangivelse "EP 1416 m fl" pekade fel (EP1416 är ett ovidkommande prompt-kort); rätt rad är 807/633** | funktion | 120, 304 | 633, 807 | 299 | support.google.com/gemini/answer/15719111 → **200**, rubrik ordagrant: "Use Deep Research in Gemini Apps"; edu.google.com/intl/ALL_us/ai/gemini-for-education/ → **200**: "Generate comprehensive reports with limited access to Deep Research" — lästa 2026-10-12 | **stämmer** på namnet och på beskrivningen "multi-step research agent that plans, searches, and produces cited reports" — hjälpsidan och edu-sidan bär båda delarna. — **fel: backbone-påståendet** (EP:807/EW:307, EW-raden nu 304). Guiden säger att Deep Research "runs on the Gemini 3 Pro backbone with a one-million-token context window". Kontextfönstret är rätt för Gemini 3 Pro (belagt i G37), men **ingen hämtad sida säger att Deep Research kör på Gemini 3 Pro**, och modellfamiljen har gått vidare (Gemini 3.5, 19 maj 2026; 3.8 Flash, 28 september 2026 — se G37). Rätt skrivning namnger ingen modellversion — **ÅTGÄRDAT i Task 9 (2026-10-12):** backbone-satsen är borta på båda ytorna (EP:807/EW:304). Kapaciteten stannar, utan modellnamn och utan siffra: "Its context window is long enough to hold several long sources in mind at once and cross-reference them." Namnet `Deep Research` och beskrivningen "multi-step research agent" är orörda, enligt inledande token. |
| G09 | `Audio Overview` — asymmetrisk EP 10 / EW 11 — plus de fyra formaten och "added September 2025" | funktion | 124, 127, 218, 219, 257, 329, 330, 381, 402, 421, 568, 1192 | 637, 640, 728, 729, 764, 830, 831, 878, 896, 915, 1056, 1597 | 279, 280, 281, 295 | support.google.com/gemininotebook/answer/16212820 → **200**, läst ordagrant 2026-10-12: "Deep Dive (default) … The Brief … The Critique … The Debate"; blog.google `/innovation-and-ai/models-and-research/google-labs/notebooklm-student-features/` → **200**, `published_time 2025-09-08`, ordagrant: "Audio Overviews now include Brief, Critique, and Debate formats for diverse perspectives on sources"; support.google.com/gemini/answer/16047373 → **200** | **stämmer** — de fyra formaten står ordagrant hos Google, i samma ordning som guiden listar dem, och "added September 2025" är exakt rätt: Googles post är daterad **8 september 2025**. Det är tillsammans med G19 och G38 den bäst belagda posten i tabellen. — **fel: NotebookLM-exklusiviteten.** Audio Overviews finns nu även i Gemini-appen: support.google.com/gemini/answer/16047373, ordagrant "You can create podcast-style conversations from documents, slides, NotebookLM notebooks, and Deep Research reports with Audio Overviews in Gemini Apps". Att rama in funktionen som NotebookLM-sidig är inte längre rätt. — **fel: produktnamnet**, se G49. Gäller också QS:279–281, 295 — **ÅTGÄRDAT i Task 9 (2026-10-12):** de fyra formaten och "added September 2025" är **orörda** — inledande token är `stämmer` och datumet är exakt. Exklusivitetsinramningen är rättad: Audio Overviews-avsnittet (EP:831/EW:330) säger nu att Google också beskriver dem i Gemini-apparna, från dokument, slides, notebooks och Deep Research-rapporter. Produktnamnet var redan åtgärdat i Task 4C. Asymmetrin är mätt om: **EW 13 / EP 12** efter Task 9:s tillägg (före: 11/10), alltså samma differens — den är EW:s skärmdumps-alt-text (`alt="Gemini Notebook Audio Overview"`), en formuleringsskillnad. Se Observationer. |
| G10 | Interaktivt läge för Audio Overview "still in beta" / "currently in beta" | funktion | **påståendet borta ur ytan** (beta-etiketten struken i Task 9, `fea3f8d`; de två meningarna om interaktivt läge står kvar utan den på EW:219 och EW:330) | **påståendet borta ur ytan** (samma, EP:729 och EP:831) | — | support.google.com/gemininotebook/answer/16212820 → **200**, avsnittet "Learn about interactive mode", läst ordagrant 2026-10-12 | **obelagt: Google kallar den inte beta.** Sidan beskriver interaktivt läge utan betamärkning — "You can join a conversation and interact with the AI hosts in Audio Overview", med en enda förbehållsrad: "**Important:** The interactive mode experience is currently available only in English." Rätt värde: *finns bara på engelska*. Det är en användbar begränsning att skriva i stället för "still in beta" — särskilt i en internationell guide, där just språkbegränsningen är det läsaren behöver veta — **ÅTGÄRDAT i Task 9 (2026-10-12):** båda betamärkningarna är borta (EP 729 "currently in beta", EP 831 "still in beta"; EW 219, 330) och ersatta av det cellen anger som rätt värde — interaktivt läge finns bara på engelska, vilket är den uppgift en internationell läsare behöver. `grep -c "in beta"` ger nu **0** på båda engelska ytorna. Ingen jakt på en betamärkning gjordes. |
| G11 | `Video Overview` som endast NotebookLM-sidig | funktion | passim (8) | passim (8) | 280, 314 | support.google.com/gemininotebook/answer/16454555 → **200**; support.google.com/gemininotebook/answer/17003757 → **200**, ordagrant: "These features are only available in Gemini Notebook" — lästa ordagrant 2026-10-12 | **stämmer** på exklusiviteten — Googles egen sida säger uttryckligen att Studio-artefakterna, Video Overviews inkluderade, bara kan skapas i Gemini Notebook och inte i Gemini-appen. — **fel: elevexemplet** (EP:640/EW:130, EW-raden nu 127). Guiden skriver "A student can upload her class notes in Gemini, generate a **cinematic** Video Overview of them in NotebookLM"; Googles sida säger ordagrant "**Cinematic Overviews are only available to users ages 18+**". Exemplet kan inte vara en skolelev. — **fel: formatlistan har bytts.** Nu gäller **Cinematic / Explainer / Short**, och Visual Style-väljaren är "only for 18+ users, excluding Cinematic and Short". **Källkonflikt:** ditchthattextbook.com/notebooklm/ (200) skriver fortfarande "the format (explainer video or brief video)" — den sidan är överspelad, Googles vinner. Gäller också QS:280 — **ÅTGÄRDAT i Task 9 (2026-10-12):** formatlistan är nu **Explainer / Short / Cinematic** (EP:834/EW:333), och Cinematics 18+-spärr står uttryckligen i brödtexten. Elevexemplet (EP:640/EW:127) genererar en **Explainer** Video Overview i stället för en Cinematic — en skolelev kan inte göra den senare. QS:280 rättad på samma punkt ("Cinematic Video Overviews" → "Video Overviews (the Cinematic format is 18+)"). Exklusiviteten är orörd, enligt inledande token. |
| G12 | De två licensvägarna: `Education Plus` och `Teaching & Learning add-on` | licens | 480, 481 | 971, 972 | — | edu.google.com/intl/ALL_us/ai/gemini-for-education/ → **200**, prisavsnittet läst ordagrant 2026-10-12; support.google.com/gemininotebook/answer/16337734 → **200**; workspaceupdates.googleblog.com/2026/04/expanded-notebooklm-capabilities-for-Education-Plus-and-Teaching-and-Learning-add-on-customers.html → **200**. Briefens två namngivna edu-sidor gick **inte** att läsa: edu.google.com/workspace-for-education/editions/ → **404** och /workspace-for-education/gemini/ → **404**, liksom fem andra `edu.google.com/workspace-for-education/`-former; bara `/intl/ALL_us/ai/gemini-for-education/` svarade 200 | **fel: `Gemini for Education` (no cost, ingår i alla Workspace for Education-editioner) + `Google AI Pro for Education` ($15,00/användare/månad vid ettårsåtagande, listpris $20,00, $24,00 vid månadsfakturering).** Googles egen sida, ordagrant: "Gemini for Education is available for free as a standalone app by signing up for Google for Education Fundamentals and enabling only the Gemini app. Gemini for Education is also included in all Google Workspace for Education editions free of charge." Premiumvägen heter numera "**ADD-ON TO YOUR WORKSPACE EDITION / Google AI Pro for Education**", och Education Plus köper bara en rabatt på den: "25% discount for Education Plus customers on purchases of 50-999 licenses". **Guidens mening på EP:970 är därmed omvänd mot källan (licensstycket ligger efter omläggningen på EP:971–972/EW:480–481)** — den säger att premium-Gemini-i-Workspace "launched in February 2026 to these two license types **at no additional cost** for license holders", medan Google i dag tar betalt för just det. — **Vad som stannar:** båda editionerna finns kvar (hjälpsidan listar "Education Plus" och "Teaching and Learning add-on" som egen nivå) och ger fortfarande högre Gemini Notebook-gränser utan extra kostnad (Workspace Updates, utrullning 6 april 2026, ordagrant "at no additional cost"). Det är **Workspace-apparnas** premium som flyttat bakom ett betalt tillägg, inte editionerna som försvunnit. Notera också Googles stavning "Teaching **and** Learning add-on" mot guidens "Teaching & Learning add-on" — **ÅTGÄRDAT i Task 9 (2026-10-12), i ett eget commit.** Rubriken är "What is free, and what you pay for" och stycket är tre: (1) `Gemini for Education` är kostnadsfri, ingår i varje Workspace for Education-edition och finns som fristående app för kvalificerade institutioner; Core Gemini AI i Classroom är gratis på samma sätt. (2) Premium i Workspace-apparna kräver tillägget `Google AI Pro for Education`, **$15,00/användare/månad vid ettårsåtagande**, mot ett överstruket $20,00, eller **$24,00 vid månadsfakturering** — och stycket skriver uttryckligen ut rabattrelationen: **$15,00 ÄR redan 25 %-priset** (25 % av $20,00 är exakt $15,00), så en budget får inte dra av ytterligare en fjärdedel. (3) Education Plus och Teaching & Learning finns kvar och bär fortfarande Gemini Notebooks utökade gränser utan extra kostnad. **Förekomstkolumnen under-räknade:** det omvända påståendet stod på **sju** rader per huvudyta, inte en — EP 632, 644, 662, 959, 970, 1531, 1567 (EW 119, 131, 152, 468, 479, 1126, 1162). Alla sju pekar nu på rätt tillägg. |
| G13 | `NotebookLM Enterprise` på Google Cloud med EU-residens; Workspace-versionens residens | dataresidens | **påståendet borta ur ytan** (hela `NotebookLM Enterprise`-meningen struken i Task 6, `85bf305`/`1da9016`-spåret; ersatt av residensstycket på EW:484) | **påståendet borta ur ytan** (samma, ersättningen på EP:975) | — | fem URL-former prövade 2026-10-12, **samtliga misslyckade**: cloud.google.com/agentspace/notebooklm-enterprise/docs/overview → **404**; /agentspace/docs/notebooklm-enterprise-overview → **404**; /gemini-enterprise/notebooklm-enterprise/docs/overview → **404**; /gemini-enterprise/docs/notebooklm-overview → **404**; /notebooklm-enterprise/docs/overview → **200 men mjuk 404** ("404. Page Not Found … The requested URL … was not found on this server") | **obelagt: 404 × 5.** Det finns ingen hämtbar Google Cloud-sida för "NotebookLM Enterprise", och EU-residensuppgiften har därmed ingen läsbar källa. Det hänger ihop med G49: produkten är omdöpt, och enterprise-kunder nås i dag genom **Gemini Enterprise** — blog.google/.../gemini-3-5/ (200) skriver ordagrant "For enterprises in Gemini Enterprise Agent Platform and **Gemini Enterprise**", och blog.google/.../gemini-3/ (200) "For enterprises in Vertex AI and **Gemini Enterprise**". Ingen av dem namnger "NotebookLM Enterprise". — **Vad som stannar:** postens andra halva — att Workspace for Education-versionens residensåtagande "is not as clearly documented in public materials and needs to be confirmed via your school's Data Processing Agreement" — **stämmer** och är den säkra formuleringen. Min hämtning är själva belägget: fem Google-URL:er och ingen läsbar residensuppgift. — **ÅTGÄRDAT i Task 6 (2026-10-12):** huvudflödets förekomst (EP:973/EW:485) skrevs om — produktnamnet och residenslöftet gick, den sourcade halvan stannade ("Data residency commitments are not always clearly documented in public materials, and need to be confirmed via your school's Data Processing Agreement"). Bonuskapitlets dubblett var kvar efter Task 6 och var Task 7:s ansvar — **den är nu också borta** (`b7fe693`): EP:1024/EW:535 bär i dag AI Act-kapitlets fyradatumsmening, inte residenspåståendet, och `NotebookLM Enterprise` står noll gånger på båda engelska ytorna (mätt i Task 12). |
| G14 | `Gemini for Education` som licensnamn — **briefens rader (EP968/EW480) var tomrader, av fel med ett steg; rätt rader är rubriken och checklistraden** | produktnamn | 313, 470, 479, 513 | 814, 961, 970, 1004 | — | edu.google.com/intl/ALL_us/ai/gemini-for-education/ → **200**, läst ordagrant 2026-10-12: rubriken "Gemini for Education", "Transform teaching and learning with Gemini for Education", och sektionen "STANDALONE APPLICATION / Gemini for Education / No cost / for qualifying institutions" | **stämmer** — `Gemini for Education` är Googles aktuella, namngivna produkt. — **fel: vad namnet betecknar.** Guiden använder det som namnet på en **licens man håller** ("The Gemini for Education license", EP:969; "Our school has confirmed which Gemini for Education license (if any) we hold", EP:1001). Hos Google är det namnet på den **kostnadsfria** nivån som ingår i alla Workspace for Education-editioner — en skola kan inte sakna den. Checklistraden på EP:1001 ställer alltså en fråga som inte längre har ett "nej" som svar. Rätt fråga är om skolan håller `Google AI Pro for Education` (G12) — **ÅTGÄRDAT i Task 9 (2026-10-12):** namnet står kvar (inledande token), men inte som namnet på en licens man kan sakna. Rubriken "The Gemini for Education license" (EP:969/EW:478) är ersatt, och checklistraden (nu EP:1004/EW:513) frågar om skolan håller det **betalda** tillägget `Google AI Pro for Education`, med påpekandet att `Gemini for Education` ingår utan kostnad. Frågan har därmed ett svar som kan bli "nej". |
| G15 | Utrullningsordningen "AI Ultra, Pro, and Plus subscribers; the free tier follows" | licens | 128, 348 | 641, 847 | — | blog.google `/innovation-and-ai/products/gemini-app/notebooks-gemini-notebooklm/` → **200**, `published_time 2026-04-08`, läst ordagrant 2026-10-12 | **stämmer** på utrullningsordningen — ordagrant: "Google AI Ultra, Pro, and Plus subscribers on the web will get access this week, with expanded access coming soon", och i sammanfattningsraden "Google AI Ultra, Pro, and Plus subscribers get notebooks this week on the web". Ordningen Ultra → Pro → Plus är Googles egen. — **obelagt: "the free tier follows".** Posten säger bara "expanded access coming soon"; **ingen hämtad sida namnger den fria nivån**. Meningen är dessutom överspelad av sin egen framgång: funktionen står nu i allmän hjälpdokumentation (support.google.com/gemininotebook/answer/17003757, 200) utan någon nivåspärr alls. En utrullningsordning från april 2026 är inte en uppgift en läsare i oktober 2026 behöver — **ÅTGÄRDAT i Task 9 (2026-10-12):** utrullningsordningen Ultra → Pro → Plus står kvar (inledande token `stämmer`, Googles egen ordning), men "the free tier follows in the weeks after" är borta på båda förekomsterna (EP 641, 847; EW 128, 348) — ingen hämtad sida namnger den fria nivån. Meningen stod dessutom i presens om en utrullning från april 2026 och är satt i preteritum, med Googles eget "expanded access" som fortsättning. **EW:s `onerror`-platshållare (EW:351) följde med i tempus** — det är den enda `AI Ultra`-asymmetrin, och om prosan satts i preteritum men inte platshållaren hade ytorna börjat säga olika saker om samma utrullning. |
| G16 | Åldersgolven: Gemini Live 18+, premium-Workspace-funktioner 18+, NotebookLM 13+ — samlad lista över alla formuleringar, inte bara förstaträffen | åldersgräns | 135, 496 | 648, 987 | 314 | fem källor, alla lästa ordagrant 2026-10-12: support.google.com/gemini/answer/13278668 → **200**; support.google.com/gemini/answer/15274899 (Gemini Live) → **200**; support.google.com/gemininotebook/answer/16213268 → **200**; edu.google.com/intl/ALL_us/ai/gemini-for-education/ → **200**; workspaceupdates.googleblog.com/2026/08/gemini-in-google-classroom-is-expanding-to-users-of-all-ages-with-contextualized-Gemini-starter-prompts-for-students.html → **200** | **fel på alla tre golv.** (1) **Gemini:** "You must be 13 (or the applicable age in your country) or over to use Gemini with a personal **or school** Google Account and 18 or over to use Gemini with a **work** account" — 18-årsgränsen gäller arbetskonton, inte skolkonton. (2) **Gemini Live:** sidans "What you need"-lista bär **båda** raderna — "Be over 13 (or the applicable age in your country)" **och** "Be 18 or over" — inuti en `gkms-context-selector`, alltså två kontotypsvarianter. Sidan **etablerar inget 18+-golv**, och edu-sidan listar dessutom Gemini Live inne i den **kostnadsfria** Gemini for Education-nivån ("Have free-flowing voice conversations on the go with Gemini Live"). Guidens "Gemini Live is 18+ only — a teacher tool, not a classroom one" (EP:961) har alltså ingen källa; meningen är struken i Task 9 och står noll gånger på båda ytorna. (3) **Gemini Notebook:** "available in browser to all users **above the age of consent (or applicable in your country)**" — inget platt 13+, och **ingenting** om strängare innehållspolicy under 18. (4) Och den tyngsta: sedan **10 augusti 2026** gäller "Gemini in Classroom will also be made available to **K-12 and higher education students of all ages**". Guidens slutsats "Hands-on student use below 18 is therefore constrained" är därmed fel i sin kärna. — **De 18+-spärrar som faktiskt är belagda är smalare än guidens:** Cinematic Video Overviews och Visual Style-väljaren (G11), och "Certain NotebookLM features are only available to 18+ users" (Workspace Updates, april 2026) utan att namnge vilka. Under 18 får "a distinct product experience with extra guardrails and AI literacy resources" — en annan upplevelse, inte en stängd dörr. — **Källkonflikt, noterad:** ditchthattextbook.com/notebooklm/ (200) skriver "According to Google's help page, NotebookLM is available to all users 13+ through the browser … Content policies are stricter for users under 18 years old" — det är ordagrant guidens mening och sannolikt dess ursprung. Den är den **äldre** läsningen; Googles egen aktuella sida säger inte längre så. Primärkällan och den nyare vinner. Gäller också QS:314 — **ÅTGÄRDAT i Task 9 (2026-10-12):** alla åtta förekomster per huvudyta plus QS:314. Rätt värden skrivna: Gemini 13+ (eller landets ålder) på personligt **och** skolkonto, 18+ på arbetskonto; Gemini Live utan blankt 18+-golv och inne i den kostnadsfria nivån; Gemini Notebook "above the age of consent"; och Gemini in Classroom för **alla åldrar** sedan augusti 2026, med en egen under-18-upplevelse. Slutsatsen "Hands-on student use below 18 is therefore constrained" är borta. De 18+-spärrar som faktiskt är belagda står kvar som de smala spärrar de är (Cinematic Video Overviews, G11, plus Googles onamngivna "certain features"). Guidens hållning att läraren är primäranvändare står kvar som ett *val*, inte som en följd av ett golv. |
| G17 | Granulära per-app-toggles "rolling out through 2026" — **förekomstkolumnerna utökade i Task 9: frasen stod på ett andra ställe, Classroom-avsnittets elevvända funktionslista (EP:990/EW:499), som ingen av mätningarna listade** | funktion | **påståendet borta ur ytan** ("rolling out through 2026" och "Granular per-app toggles" strukna i Task 9, `fea3f8d`; ersatta av hänvisningen till Admin-konsolen på EW:508) | **påståendet borta ur ytan** (samma, ersättningen på EP:999) | — | ingen hämtbar källa för per-app-toggles eller 2026-fönstret, prövat mot edu.google.com/intl/ALL_us/ai/gemini-for-education/ (200), support.google.com/gemini/answer/14620100 (200) och workspaceupdates-posterna; admin-spärren däremot belagd: workspaceupdates (utrullning 6 april 2026) → **200**, ordagrant "NotebookLM is ON by default and can be disabled at the domain, OU, or group level", och workspaceupdates (10 augusti 2026) → **200**, "controlled using the Gemini in Classroom control" — lästa 2026-10-12 | **obelagt: ingen hämtad sida nämner granulära per-app-toggles eller "rolling out through 2026".** Vad som däremot är belagt och **stämmer**: styrning på domän-, OU- och gruppnivå, och att NotebookLM/Gemini Notebook är admin-spärrat på samma sätt — guidens sista mening i posten är alltså rätt. Det Google faktiskt dokumenterar som OU-mekanik är dessutom något annat än per-app: "If you would like to disable Gemini in Google Classroom for users who are under 18 years old, you can create an OU with only those users and turn off access for that OU only." Rätt skrivning behåller domän/OU/grupp och stryker både per-app-exemplet och årtalet — **ÅTGÄRDAT i Task 9 (2026-10-12), på båda ställena.** Per-app-exemplet och årtalet är borta ur admin-stycket (EP:985/EW:494), som nu bär den OU-mekanik Google faktiskt dokumenterar. **Och koordinatorns ruling 2026-10-12: "rolling out through 2026" i Classroom-avsnittet (EP:990/EW:499) är den här postens påstående på ett andra ställe, inte ett nytt påstående** — ett obelagt årtalsfönster, samma fras, samma utfall. Satsen säger nu "Student-facing features **being added** include …": funktionerna beskrivs, utrullningsfönstret inte. `grep -c "rolling out through 2026"` ger **0** på båda engelska ytorna. Task 9:s första rapport förde upp den som ett påstående utan post; det var fel — den hade en post, den här — **ÅTGÄRDAT i Task 9 (2026-10-12):** per-app-exemplet och årtalet är borta (EP:985/EW:494). Domän/OU/grupp-spärren står kvar, nu med den OU-mekanik Google faktiskt dokumenterar: en OU med bara under-18-användare, avstängd för den OU:n. Att Gemini Notebook är på som standard och kan stängas av på domän-, OU- eller gruppnivå står också, enligt cellens `stämmer`-halva. |
| G18 | Google Classroom AI-funktioner "free with all Workspace for Education accounts" | licens | 499 | 990 | — | blog.google `/products-and-platforms/products/education/classroom-ai-features/` → **200**, `published_time 2025-06-30`, läst ordagrant 2026-10-12; edu.google.com/intl/ALL_us/ai/gemini-for-education/ → **200**; workspaceupdates (10 augusti 2026) → **200**, "Availability / Education: Fundamentals, Standard, and Plus" | **stämmer** — Googles egen post, ordagrant: "Google is providing Gemini in Classroom to **all educators with Google Workspace for Education accounts at no cost**. This includes over 30 new AI tools…" Bekräftat från två oberoende håll: edu-sidans "included in all Google Workspace for Education editions free of charge" och Workspace Updates-postens tillgänglighetsrad som räknar in Fundamentals och Standard, inte bara Plus. Lärarsidans funktionslista på EP:990/EW:499 (lektionsplanering, quiz till Forms, rubriker, förslagsfeedback som läraren måste godkänna) stämmer likaså mot källan. — Attributionen "confirmed at BETT 2026" är en annan sak, se G35 |
| G19 | "I have built 140 such styles" + pekaren till style-biblioteket — **utökad med tre förekomster briefen inte listade** ("Johan's 140 NotebookLM styles", "The 140 styles connection", TOC-raden) | URL | 322, 341, 342, 593, 598, 602, 673 | 548, 823, 842, 843, 1084, 1088, 1158 | — | choosewise.education/infographic-styles/ → **200**, sidtitel ordagrant "140 Visual styles for infographics"; choosewise.education/infographic-styles/styles-en.json → **200**, **exakt 140 poster**, räknade lokalt 2026-10-12 (`json.load` → `len() == 140`, identiskt med repots egen `infographic-styles/styles-en.json`) | **stämmer** — den enda siffran i hela guiden som en hämtad källa bekräftar på siffran. 140 är 140. Pekaren `choosewise.education/infographic-styles/` svarar 200 och är alltså ingen död länk. — **Notering för Task 9, inte ett utfall:** landningssidans egen ingress säger fortfarande "styles for infographics in NotebookLM", så namnbytet (G49) landar även där. Den sidan är inte en av rundans tre ytor och ska inte ändras här, men den som rättar guiden utan att rätta länkmålet skapar en ny divergens — **OMMÄTT i Task 9 (2026-10-12):** `curl -o /dev/null -w '%{http_code}'` ger **200** på både `choosewise.education/infographic-styles/` och `choosewise.education/assets/pdfs/nlm-140-prompts-en.pdf`. **Inget 404, alltså inget fynd**, och siffran 140 är orörd på alla sex/fem förekomster. Noteringen om landningssidans egen ingress ("styles for infographics in NotebookLM") kvarstår som en uppgift utanför rundans tre ytor. |
| G20 | Matt Miller-citatet "a personal tutor that only knows what you teach" (Ditch That Textbook, januari 2026) | citat | 123, 209, 336, 1199 | 636, 719, 837, 1604 | — | ditchthattextbook.com/notebooklm/ → **200**, hela sidan läst ordagrant 2026-10-12. Strängarna "personal tutor" och "only knows what you teach" förekommer **noll gånger** i den hämtade HTML:en (`grep -ic` → 0 för båda) | **obelagt: citatet finns inte ordagrant hos Matt Miller.** Ett citationstecken är ett löfte om ordalydelse (briefens steg 4), och löftet infrias inte. Vad sidan faktiskt bär, och som kunde ersätta citatet: "It becomes an instant expert on the documents you give it", och Millers återgivning av Googles egen formulering "your personalized AI research assistant". — **Attributionen är också obelagd:** "Ditch That Textbook, **January 2026**" — den hämtade sidan visar inget januaridatum och skriver om chatten att den "is powered by **Gemini 1.5 Pro**, Google's most capable model (as of publication of this post)", vilket daterar delar av texten långt före januari 2026. En närliggande formulering ("It only knows what you teach it") finns på chrmbook.com, inte hos Miller — och en tredjepartssida är inte källa till ett citat som tillskrivs någon annan — **ÅTGÄRDAT i Task 9 (2026-10-12), steg 3B.** Alla fyra förekomsterna (EP 636, 719; EW 123, 209) bär nu den rad granskaren verifierade ordagrant på just Millers sida: *"It becomes an instant expert on the documents you give it."* Attributionen till Matt Miller och Ditch That Textbook är kvar. **Ramen bär `Gemini Notebook`**, och eftersom ramen var G49:s fyra återstående förekomster av det gamla namnet i guidens egen röst är **G49:s överlevandelista nu noll**. Dateringen "January 2026" är borta: cellen anger att dateringen följer källan, och den hämtade sidan bär inget januaridatum. |
| G21 | Säfström/Folkebrant-exemplet, Fristadsskolan i Eskilstuna, Pedagog Eskilstuna februari 2026 — källbelagt, **utökad med en tredje förekomst per yta ("Extra example…") som briefen inte listade**; **stannar — Johans beslut vid grinden 2026-10-12** | inramning | 220, 330, 402 | 730, 831, 896 | — | pedagog.eskilstuna.se `/pedagog-eskilstuna/inspiration-fran-vara-verksamheter/sa-anvander-vi-notebooklm-i-so-undervisningen-pa-hogstadiet` → **200**, daterad **4 februari 2026** på sidan, läst ordagrant 2026-10-12 | **stämmer** — källan bär varje led guiden påstår, ordagrant: "SO-lärarna Viktor Säfström och David Folkebrant" på "Fristadsskolans högstadium"; "Skapa korta ljudöversikter. **1–2 minuter** per begrepp eller moment fungerar väl på högstadiet"; "Elever använder till exempel **amhariska och olika varianter av arabiskan** och upplever att stödet håller"; "notebooks skapas av dem och delas vidare till eleverna, oftast via **Google Classroom**". Datumet 4 februari 2026 bekräftar inventeringens "februari 2026" och guidens "early 2026". — **En detalj står inte i källan:** "for **newly-arrived** students". Artikeln säger att elever *vill ha* amhariska eller arabiska varianter och hör skillnaden; ordet nyanländ förekommer inte. **ÅTGÄRDAT i Task 8 (2026-10-12):** halvsatsen är omskriven på alla sex ställen (EW 220, 330, 402; EP 730, 831, 896) till en formulering källan bär — elever som vill ha varianterna, inte "nyanlända" som kategori. — **Johans beslut vid grinden 2026-10-12: exemplet STANNAR.** Det är guidens enda namngivna, källbelagda klassrumsexempel på 42 sidor, och spec §9 tillåter uttryckligen "ett medvetet, motiverat exempel med en post i inventeringen". **Det är därför leveransvaktens förbudslista för den här guiden inte kan innehålla ett bart `Sweden` eller `Swedish`** (granskningsfokus 1, se `test_geminis_forbidden_list_does_not_ban_what_the_spec_keeps` i `scripts/tests/test_guide_delivery.py`) — till skillnad från Copilot-guiden, som valde väg A rakt av och kan förbjuda båda orden bart |
| G22 | "Output in languages beyond English" — **generaliserat i Task 8**, tidigare "including Swedish and other EU languages" som språkexempel | inramning | 330 | 831 | — | support.google.com/gemininotebook/answer/16213268 → **200**, avsnittet "Supported countries & languages"; support.google.com/gemininotebook/answer/16261963 → **200**, läst ordagrant 2026-10-12: "Gemini Notebook is currently available in **80+ languages**", och språklistan namnger **Swedish** (rad 81), **Amharic** och **Arabic (Colloquial Egyptian)** | **stämmer** — flerspråkig utmatning är dokumenterad på Googles egen sida, svenska står namngivet i listan, och sidan anger 80+ språk. Samma lista belägger dessutom G21:s amhariska och arabiska. Guidens förbehåll "though quality varies by language; generate a test clip before relying on it" är dessutom precis det Google själv signalerar om Audio Overview ("The interactive mode experience is currently available only in English", och Cinematic Video Overviews "only support English"). — **fel (omfång):** att nämna svenska **först** i en internationell guide är ett omfångsval, inte ett sakfel. **Ingen källa motsäger det, och den som letar efter en sådan letar förgäves.** Ägarens beslut vid grinden — **ÅTGÄRDAT i Task 8 (2026-10-12):** uppräkningen "including Swedish and other EU languages" är borttagen på båda ytorna (EW:330, EP:831); meningen säger nu bara "Output in languages beyond English works well, though quality varies by language". Dateringen "as of April 2026" i samma mening är också borttagen — ingen hämtad källa gav ett datum för språkstödet (se källcellen ovan), och utan ett datum att belägga mot går stämpeln, enligt samma princip som G28 |
| G23 | Huvudflödets juridikpassage "Data residency, GDPR, and national context" | regelverk | 483–489 (rubrik + ruta, post-Task 6) | 974–980 (post-Task 6) | — | sammansatt: residensdelen → se G13 (404 × 5); Sverige-parentesen → se G29 (mätt på ytorna); tillsynsmyndighetsdelen → www.edpb.europa.eu → **200**, läst 2026-10-12 | **stämmer** (flertoken, av konstruktion) på "National supervisory authorities. Every EU member state has one, and you should know yours by name" — EDPB:s egen sida etablerar arkitekturen med nationella tillsynsmyndigheter, och formuleringen är redan landneutral, vilket är exakt vad rundan vill. — **obelagt** på EU-residensuppgiften (G13). — **fel (omfång)** på Sverige-parentesen (G29). Passagen kan alltså inte få ett enda utfall: tre meningar, tre olika svar, och de måste redigeras var för sig. — **ÅTGÄRDAT i Task 6 (2026-10-12):** rubriken bytt till "Data residency, and what depends on where you are"; residensmeningen omskriven per G13; GDPR-artikelmeningen och tillsynsmyndighetsmeningen (med Sverige-parentesen, G29) ersatta av ett inledande stycke plus jurisdiktionsrutan (`callout callout--watch`) — ingen av dem namnger längre en lag eller myndighet. Detta var en **omfångsborttagning** av den sant landneutrala tillsynsmyndighetsmeningen, inte en sakkorrigering: meningen var redan korrekt, den beskriver bara en EU-specifik institutionell arkitektur som en läsare utanför EU inte kan agera på |
| G24 | Bonuskapitlets GDPR-halva: ingressen och hela avsnittet "GDPR fundamentals for schools using AI" | regelverk | **påståendet borta ur ytan** för GDPR-avsnittet (hela "GDPR fundamentals for schools using AI" struket i Task 7, `ed5e1fc`-spåret); bonuskapitlets kvarvarande praktikregel står på EW:531 | **påståendet borta ur ytan** för GDPR-avsnittet; praktikregeln på EP:1020 | — | eur-lex.europa.eu svarade **HTTP 202 med 0 byte** på fem URL-former (CELEX HTML, konsoliderad HTML, TXT, PDF, ELI) och publications.europa.eu Cellar svarade **400/406** — förordningstexten är inte hämtbar med `curl` härifrån. En officiell EU-sida svarade: www.edpb.europa.eu, "Position Paper on the derogations from the obligation to maintain records of processing activities pursuant to **Article 30(5) GDPR**" → **200**, titeln läst ordagrant 2026-10-12 | **stämmer** på de två bärande leden: controller/processor-uppdelningen ("Your school is the data controller; Google is the processor") och att **artikel 30 är registerföringsartikeln** — EDPB:s egen dokumenttitel namnger "the obligation to maintain records of processing activities pursuant to Article 30(5) GDPR", ordagrant. — **obelagt (hämtningsfel): EUR-Lex 202/0 byte på fem URL-former** på artikel 6(1)(e) "public task" som rättslig grund och på artikel 30:s fältlista (syften, kategorier, mottagare, tredjelandsöverföringar, lagringstider). **Detta är ett hämtningsfel, inte en motsägelse — ingen källa jag läst säger något annat.** Flaggat för grinden: det är sedan länge avgjorda GDPR-bestämmelser, och att stryka artikelnumren ur kapitlet skulle göra det sämre, inte säkrare. Vill ägaren ha dem belagda krävs en hämtningsväg som EUR-Lex inte stänger — det är en av de tre siffergrupper som är värd en andra källhämtning — **ÅTGÄRDAT i Task 7 (2026-10-12):** hela avsnittet "GDPR fundamentals for schools using AI" med sina sju stycken är borta på båda engelska ytorna (EP f.d. 1019–1026, EW f.d. 530–537), och kapitelingressen namnger bara AI Act:en. Två led följde **inte** med i badvattnet: dataresidensen står kvar i huvudflödet (G13, nu EP:975/EW:484) och den praktiska regeln om skoldomänkonto är **flyttad** till ett eget stycke direkt efter ingressen — men utan sin tredje mening, som bar G33:s term `records of processing`. Checklistans Article 30-punkt gick samma väg. `grep -c GDPR` ger nu **1** per engelsk yta: promptmallens platshållare (G30) |
| G25 | AI Act-ingressens "entered into force on 1 August 2024 and phases in through 2026 and beyond" | regelverk | 534 | 1023 | — | `korsref P13` (Europeiska kommissionen, `digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai`, läst ordagrant 2026-10-08). Ingen ny hämtning gjord, enligt spec §3 | **fel: förordningen blev tillämplig 2 augusti 2026.** Ikraftträdandet **stämmer** (1 augusti 2024) och ändras inte — noterat uttryckligen så att det inte stryks tyst (inventeringens regel 2). Men "phases in through 2026 and beyond" är överspelat: P13 bär kommissionens ordalydelse "The AI Act entered into force on 1 August 2024 and **became applicable on 2 August 2026**, with some exceptions" — ett datum som passerat när guiden läses. "Education is explicitly in scope" **stämmer** likaså: kommissionen räknar "AI solutions used in education institutions, that may determine the access to education … (e.g. scoring of exams)" som högrisk — **ÅTGÄRDAT i Task 7 (2026-10-12):** ingressen säger nu "entered into force on 1 August 2024 and **became applicable on 2 August 2026**" på båda engelska ytorna (nu EP:1023, EW:534). "phases in through 2026 and beyond" står inte kvar någonstans. Ikraftträdandet och "Education is explicitly in scope" är orörda, enligt den här cellens egen anvisning |
| G26 | Risknivåernas fyra namn: Minimal risk / Limited risk / High risk / Prohibited — pyramiden och brödtexten (EW-brödtexten lokaliserad: 576–579), plus **FAQ:ns nionde förekomst per yta, tillagd i Task 7:s fixrunda 2** (EW 1187/nu 1176, EP 1589/nu 1581: *”You are in the minimal-risk tier”*) | regelverk | 543, 548, 553, 558, 564, 568–571, 1178 | 1032, 1037, 1042, 1047, 1052, 1056–1059, 1583 | — | `korsref P13`; samt den publicerade Claude-guiden `exports/claude-print-a4-en.html:1276–1306`, som redan bär de fyra rättade nivånamnen | **fel: Unacceptable risk / High risk / Transparency risk / Minimal or no risk.** Tre av guidens fyra namn är fel. "Limited risk" → **Transparency risk**; "Minimal risk" → **Minimal or no risk**; "Prohibited" → **Unacceptable risk**. Bara "High risk" **stämmer**. P13 bär kommissionens ordalydelse: "The AI Act defines 4 levels of risk for AI systems: Unacceptable risk / High risk / Transparency risk / Minimal or no risk". **De två guiderna får inte säga olika saker om samma förordning** — Claude-guiden ships redan med de rättade fyra, så det är Gemini-guiden som ska följa efter, på åtta rader per yta (pyramiden 1037/1042/1047/1052 och brödtexten 1061–1064 på EP; 551/556/561/566 och 576–579 på EW — efter rundans redigeringar: pyramiden 1032/1037/1042/1047 och brödtexten 1056–1059 på EP, 543/548/553/558 och 568–571 på EW). Och brödtexten måste följa namnet: EP:1062 — nu EP:1057 — beskriver redan transparens som "the operative word at this tier", vilket gör namnbytet till en rättelse som texten själv ber om — **ÅTGÄRDAT i Task 7 (2026-10-12):** de fyra namnen är `Unacceptable risk` / `High risk` / `Transparency risk` / `Minimal or no risk` på **båda** engelska ytorna, på fyra ställen var: pyramidens `<text>`, dess HTML-kommentar, diagramtexten och brödtextens `<strong>`-led. Diagramtexten sa också "sit in Minimal or Limited" och säger nu "sit in the bottom two tiers, Minimal or no risk and Transparency risk". Argumenten följde namnen: transparensstycket stod redan rätt, och "banned outright" hör till `Unacceptable risk`. **Etiketterna mättes i webbläsare med Hanken Grotesk inläst** (`getComputedTextLength`): den bredaste, `Unacceptable risk`, slutar vid 232 i en `<rect>` som går 80–600, och det minsta avståndet till den högerställda etiketten på samma rad är 118 enheter. Ingen kollision. — **FIXRUNDA 2 (2026-10-12):** en **nionde** förekomst per yta låg utanför den här cellens ursprungliga ställelista: FAQ:ns svar på *”What does the EU AI Act actually require of me?”* sa *”You are in the **minimal-risk tier**”* (EP:1581, EW:1176; den rättade satsen står nu på EP:1583, EW:1178). Guiden namngav därmed samma nivå på två sätt — exakt den defekt som rättades i diagramtexten. Satsen säger nu *”You are in the **Minimal or no risk** tier, and standard data-protection discipline applies.”* Nivånamnen står nu alltså på **nio** ställen per yta, inte åtta, och alla nio bär den rättade taxonomin |
| G27 | Artikel 4-påståendena: "has applied since 2 February 2025", "in force since 2 February 2025", "applies since February 2025" samt de odaterade variantraderna — **briefen gav bara EP-rader; EW-motsvarigheterna saknades helt och är tillagda här** | regelverk | 81, 397, 418, 535, 536, 581, 994, 1178 | 596, 891, 912, 1024, 1025, 1069, 1424, 1583 | — | `korsref P13` | **stämmer** — P13 bär kommissionens ordalydelse: "prohibited AI practices and **AI literacy obligations entered into application from 2 February 2025**". Alla tre varianter i guiden ("has applied since", "in force since", "applies since February 2025") är korrekta, och ingen av de sju EW-raderna eller sju EP-raderna behöver ändras. Noterat uttryckligen, eftersom en post som stämmer aldrig stryks tyst (inventeringens regel 2) — och eftersom artikel 4 är det enda AI Act-påstående i guiden som håller oförändrat. **Men meningen det står i gör det inte:** se G48 |
| G28 | "A country that is among those that have not yet issued detailed national guidance finds the EU AI Act the dominant framework for its schools until that changes" — **omskriven i Task 8**, tidigare "Sweden, as of April 2026, is among the countries that have not… the dominant framework for Swedish schools" | inramning | 537 | 1026 | — | ingen källa hämtad — påståendet är ett omfångsval, inte en faktauppgift att pröva | **fel (omfång).** Ingen hämtad källa motsäger att Sverige saknar detaljerad nationell AI-vägledning för skolan, och **den som letar efter en sådan letar förgäves** — det är inventeringens egen definition av `fel (omfång)`. Påståendet ligger utanför det omfång rundan valde (spec §3). Ägarens beslut vid grinden, beslut 1. Observera att meningens andra halva — "which makes the EU AI Act the dominant framework for Swedish schools" — bär samma omfångsfråga och faller med samma beslut — **ÅTGÄRDAT i Task 8 (2026-10-12):** meningen är omskriven på båda ytorna (nu EW:537, EP:1026). Argumentet — att Aktens betydelse varierar med om landet publicerat egen nationell vägledning — står kvar, jurisdiktionsneutralt; namnet "Sweden"/"Swedish" och dateringen "as of April 2026" är borta. Ny lydelse: "A country that is among those that have *not* yet issued detailed national guidance finds the EU AI Act the dominant framework for its schools until that changes." |
| G29 | "others (Sweden is a notable example, as of April 2026) have not yet" — **stod bara på EP; EW 491 bekräftat utan Sverige-parentesen** — **meningen finns inte längre, borttagen i Task 6** | inramning | **borttagen i Task 6** (stod på 491, ingick i tillsynsmyndighetsstycket som G23's ÅTGÄRDAT-notering beskriver; ersatt av stycket "Where your data is stored and processed matters…" + callouten "What depends on where you are", nu EW:483–489, mätt om i Task 12) | **borttagen i Task 6** (stod på 979; samma ersättning, nu EP:974–980, mätt om i Task 12) | — | ytorna själva, mätt 2026-10-12 — meningen fanns på EP:979 och EW:491 vid mättillfället | **fel (omfång)** — samma grund som G28. Plus en **mätt ytdivergens, inte en hypotetisk:** printytan bar parentesen "(Sweden is a notable example, as of April 2026)", webbytans motsvarande mening gjorde det inte. Notera också att EP:979 i samma andetag namngav "(UK, France, Germany, the Netherlands)" som länder *med* vägledning, medan bonuskapitlets lead-in — nu EP:1026 — namnger "(including France, Germany, and the Netherlands)" — två listor av samma slag, olika långa, båda obelagda. — **ÅTGÄRDAT i Task 6 (2026-10-12):** hela meningen med Sverige-parentesen är borttagen i sin helhet på båda ytorna, tillsammans med tillsynsmyndighetsstycket den stod i, och ersatt av det nya inledande stycket plus jurisdiktionsrutan. Ytdivergensen den här posten mätte finns därför inte längre att observera — båda ytorna säger numera samma sak, vilket är noll ord om Sverige. **Posten står kvar trots att förekomsten är borta:** ett fynd som åtgärdats ska kunna spåras till uppgiften som åtgärdade det, av samma skäl som ett fynd utan åtgärd aldrig stryks tyst |
| G30 | Promptmallens platshållare "[e.g. GDPR + EU AI Act + your national school-governance law]" — stannar, spec §3 | regelverk | 906 | 1351 | — | ytorna själva, EP:1357 och EW:915 — nu EP:1351 och EW:906; förordningsnamnen i sig täcks av G25–G27 och `korsref P13` | **stämmer** — båda namngivna regelverken är verkliga och rätt benämnda, och "your national school-governance law" är redan landneutral, alltså exakt den form en internationell guide behöver. Platshållaren ber läsaren fylla i sitt eget lands ram; den påstår ingenting om vilket land det är. — **Omfångsfrågan är inte min.** Om GDPR-platshållaren stannar är ägarens beslut vid grinden. **Inget i källmaterialet talar mot att den stannar:** GDPR gäller varje EU-medlemsstat, och en internationell guide för europeiska skolor har mer nytta av att nämna den än av att tiga om den |
| G31 | "I have a full-time job and run this work alongside it" | författarfakta | **påståendet borta ur ytan** (meningen struken i Task 10, `346a8c3`; förväntansraden står nu på EW:1200) | **påståendet borta ur ytan** (samma, EP:1605) | — | ägarens egen uppgift, inte en webbsida: `/Users/johan/CLAUDE.md` §1 och projektminnets post `johan-lamnat-advania.md` — Johan lämnade Advania Skolpartner i **augusti 2026** och är sedan dess egen konsult som fakturerar genom JL Skolutveckling AB. Läst 2026-10-12 | **fel: han har inte längre en heltidsanställning.** Meningen "I have a full-time job and run this work alongside it" var sann när guiden stämplades april 2026 och är inte sann i oktober 2026. Det är en **författaruppgift, inte en produktuppgift** — och den är därför den enda posten i tabellen där rätt värde inte kan hämtas, bara bekräftas av ägaren. **Flaggat: skriv inte om den här meningen utan Johans eget besked om hur han vill formulera förbehållet nu.** Förbehållets *funktion* — att dämpa förväntan på svarstider — kan vara värd att behålla även när grunden ändrats. — **ÅTGÄRDAT i Task 10 (2026-10-12): Johans eget besked kom** ("ändra påståendet om mig som inte längre är sant"), och meningen är skriven om på båda ytorna. Före: "I have a full-time job and run this work alongside it, which means I can't always handle urgent or tight-turnaround queries." Efter: "This work runs alongside my consulting, so I cannot always take on urgent or tight-turnaround queries." Förbehållets funktion — svarstidsförväntan, pekningen mot admin/DPO/resurserna ovan — står oförändrad; bara anställningspåståendet är borta. Inget nytt påstående om Johans situation utöver "detta arbete löper vid sidan av mina uppdrag" tillkommer. `grep -c "full-time job"` ger **0** på EP och EW |
| G32 | Avslutningens CTA: "you can also reach out through my website (link in the footer)" | inramning | 1200 | 1605 | — | ytorna själva, EP:1611 och EW:1209 — nu EP:1605 och EW:1200; EW:1229 — nu EW:1220 — bär foten med datumstämpeln, mätt 2026-10-12 | **stämmer** på mekaniken för webbytan — en fot finns, och "link in the footer" går att följa där. — **obelagt för printytan.** En tryckt A4-PDF har ingen klickbar fot, och formuleringen ber en papperläsare klicka. Det är inget sakfel och ingen källa motsäger det; det är en **ytobundenhet** i en mening som står ordagrant lika på båda ytorna. Rätt skrivning för print namnger adressen i stället för att peka på en fot — **SKJUTEN TILL NÄSTA UPPGIFT av Task 9 (2026-10-12), med skäl.** Tokenen `obelagt` är okvalificerad och posten faller därmed inom Task 9:s regel — men förekomsten är **samma `<p>` som G31:s författarförbehåll** (nu EP:1605/EW:1200), och G31 är uttryckligen nästa uppgifts, eftersom rätt värde där bara kan komma från Johan själv. Att skriva om halva stycket här hade tvingat nästa uppgift att redigera en mening Task 9 just rört, i en passage vars ton ägaren ska bestämma. Anvisningen står oförändrad: rätt skrivning för printytan namnger adressen i stället för att peka på en klickbar fot. — **Task 10 (2026-10-12): mekaniken bekräftad, printfixen INTE gjord — skrivs upp som öppen skuld.** Avsändarneutraliteten och rätt varumärke kontrollerades och håller: EW:s delade sidfotspartial (`assets/partials/footer-en.html`) och EP:s egen sidfot/avslutning (EP:485, EP:1618) pekar båda på `choosewise.education`, och meningen säljer inte Johans tid. Men Task 10:s egna uppdrag — bekräftat i både task-10-brief.md och uppdragsbeskrivningen — bad bara om den kontrollen, inte om att namnge adressen i stället för "link in the footer" på printytan. **Anvisningen i den här cellen är alltså fortfarande inte utförd**, trots att Task 9:s rapport sköt den hit uttryckligen av det skälet. Den lämnas omedvetet öppen om ingen läser cellen: skrivs därför in här som en skuld för nästa uppgift som redigerar den här ytans avslutning, snarare än att jag åtgärdar den utan uppdrag. |
| G33 | Del 3: "Update the school's records of processing (GDPR, a European regulation — Article 30)" | regelverk | 427 | 921 | — | www.edpb.europa.eu, "Position Paper on the derogations from the obligation to maintain records of processing activities pursuant to **Article 30(5) GDPR**" → **200**, titeln läst ordagrant 2026-10-12; EUR-Lex **202/0 byte** för artikeltexten (se G24) | **stämmer** — artikel 30 är registerföringsartikeln, belagt ur EDPB:s egen dokumenttitel. Och den parentetiska glosan "(GDPR, **a European regulation** — Article 30)" är precis den internationella inramning rundan vill ha: den förklarar vad GDPR är för en läsare utanför EU i stället för att förutsätta det. **Behåll glosan.** Det är rundans bästa befintliga exempel på hur en EU-referens kan stå i en internationell guide utan att läsa som svensk inramning. — **ÖVERKÖRD av ägaren i Task 6 (2026-10-12): glosan går.** Tre skäl: (1) spec §3 namnger Article 30 explicit i sin borttagningslista, och specen är den bindande auktoriteten; (2) "Article 30" står i leveransvaktens förbjudna-strängar-lista (byggd ur samma spec), så att behålla den hade lämnat en vakt permanent röd; (3) jurisdiktionsrutan som installeras i huvudflödets juridikpassage (G23) bär glosans funktion redan jurisdiktionsneutralt ("your data-protection regime decides … what you must document") — att behålla artikelnumret bredvid rutan hade varit redundant. Meningen är omskriven till "Update the school's own record of which personal data these tools process." — artikelnivån går, rådet (vad som ska uppdateras) stannar |
| G34 | Del 3: "You are personally carrying GDPR risk that belongs with your organisation" | regelverk | 440 | 934 | — | ingen källa hämtad — påståendet bär ingen siffra, inget datum och inget produktnamn | **stämmer (ej volatil).** "You are personally carrying GDPR risk that belongs with your organisation" är ett argument om ansvarsfördelning, inte en faktauppgift som kan bli gammal. Det följer direkt av controller/processor-uppdelningen i G24, som **stämmer**. — **ÄNDRAD i Task 6 (2026-10-12), trots `stämmer`:** regelverksnamnet går, varningen stannar — "carrying GDPR risk" → "carrying a data-protection risk". Skälet är inte att påståendet var fel, utan att strängen "carrying GDPR risk" står i leveransvaktens förbjudna-strängar-lista; "a data-protection risk that belongs with your organisation" bär samma skärpa utan att namnge förordningen. Hela stycket är ett av guidens viktigaste råd (konsumentkonton i skolarbete) och har inte tappat kraft |
| G35 | "confirmed at BETT 2026" — beläggskälla för "Core Gemini AI in Classroom … free for all Workspace for Education accounts" | datumstämpel | **påståendet borta ur ytan** (BETT-attributionen struken i Task 6, `1da9016`) | **påståendet borta ur ytan** (samma) | — | blog.google `/products-and-platforms/products/education/bett-2026-gemini-classroom-updates/` → **200**, `published_time **2026-01-21**`, läst ordagrant 2026-10-12; blog.google `/products-and-platforms/products/education/classroom-ai-features/` → **200**, `published_time **2025-06-30**` | **stämmer** på sakuppgiften — Core Gemini AI i Classroom är gratis för alla Workspace for Education-konton (se G18, belagt på tre sidor). — **fel: attributionen.** BETT 2026 bekräftade det inte. BETT-posten *refererar bakåt* till "Building on the **30+ no-cost AI tools launched last year**" och annonserar i övrigt helt andra saker (standardtaggning, ljud- och videoinspelning i Classroom, ny startsida). Den sida som faktiskt annonserar gratisstatusen är Googles post från **30 juni 2025**: "Google is providing Gemini in Classroom to all educators with Google Workspace for Education accounts at no cost." Rätt värde: attribuera till juni 2025-annonseringen, eller stryk evenemangsnamnet — det senare är att föredra i en guide som ska hålla, eftersom ett mässnamn daterar texten varje gång mässan går av stapeln igen — **ÅTGÄRDAT i Task 9 (2026-10-12):** "(confirmed at BETT 2026)" är struket på båda förekomsterna per yta (EP 644, 662; EW 131, 152). Cellens två alternativ var att attribuera till juni 2025-annonseringen eller att stryka evenemangsnamnet, med det senare som det föredragna — och det är det som gjorts. Sakuppgiften (gratis för alla Workspace for Education-konton) står kvar, belagd via G18. |
| G36 | "As of BETT 2026, the 'learning standards tagging' feature in Classroom supports the UK, Australia, Canada, Japan, Brazil, Mexico, and Italy" — landlista | funktion | 501 | 992 | — | blog.google `/products-and-platforms/products/education/bett-2026-gemini-classroom-updates/` → **200**, 2026-01-21; och **den nyare och avgörande källan** workspaceupdates.googleblog.com `/2026/05/keep-track-of-student-progress-with-learning-standards-and-skills-in-Google-Classroom.html` → **200**, utrullning "started on **May 27, 2026**" — båda lästa ordagrant 2026-10-12 | **fel: United States, Canada, United Kingdom, Brazil, Japan, Mexico, Italy, Australia.** Workspace Updates skriver ordagrant: "Learning standards are available in the **United States**, Canada, United Kingdom, Brazil, Japan, Mexico, Italy, and Australia." Guidens lista **saknar USA**, och inramningen "As of BETT 2026" är överspelad på två sätt: Italien är inte längre "soon" utan tillgängligt, och funktionen har lämnat pilotstadiet och rullats ut sedan 27 maj 2026. — **Källkonflikt, och den är intern:** BETT-posten motsäger **sig själv**. En passage säger "Pilot participants will have access to learning standards from the UK, Australia, Canada, Japan, Brazil, Mexico, and soon Italy" (ingen USA); en annan passage på samma sida säger "learning standards from the **US**, UK, Australia, Canada, Japan, Brazil, Mexico, and soon Italy". Att två Google-passager på samma sida är oense är i sig ett resultat, och det är skälet att lita på majkällan. — **Guidens slutsats blir också fel i sin riktning:** "Teachers in unsupported countries will need to map … manually" stämmer fortfarande som princip, men listan är åtta länder lång och växande ("Classroom has a growing list of standards already available and periodically brings in new ones from the Satchel Rosetta Exchange"), vilket är en mer användbar sak att säga till en internationell läsare än en fryst lista — **ÅTGÄRDAT i Task 9 (2026-10-12):** listan är nu Googles åtta, med USA: United States, Canada, United Kingdom, Brazil, Japan, Mexico, Italy, Australia. "As of BETT 2026" är borta, utrullningen från **maj 2026** står i stället för pilotstadiet, och listans växande karakter står med — det är den mer användbara uppgiften för en internationell läsare. Slutsatsen om manuell mappning stannar, med en uppmaning att läsa Googles aktuella lista i stället för guidens. |
| G37 | `Gemini 3 Pro` som flaggskeppsmodell, "launched 18 November 2025", en-miljon-tokens kontextfönster, samt de kopplade omnämnandena `Gemini 3 Flash` och `Gemini 3 Pro with Deep Think` | produktnamn | **påståendet borta ur ytan** för `Gemini 3 Pro`, backbone-meningen och kontextfönstret (strukna i Task 6, `1b32062`); `Gemini 3 Deep Think` står kvar på EW:1164 | **påståendet borta ur ytan** för samma tre; `Gemini 3 Deep Think` på EP:1569 | — | fyra Google-poster, alla lästa ordagrant 2026-10-12: blog.google `/products-and-platforms/products/gemini/gemini-3/` → **200**, `datePublished 2025-11-18T16:00:00+00:00`; blog.google `/products-and-platforms/products/gemini/gemini-3-flash-gemini-app/` → **200**, `published_time **2025-12-17**`; blog.google `/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/` → **200**, `published_time **2026-05-19**`; blog.google `/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-flash-developers/` → **200**, `published_time **2026-09-28**`. deepmind.google/models/gemini/pro/ svarade 200 men renderar sitt innehåll med JS — **0 byte text efter extraktion**, alltså inte läsbar och inte använd | **fel: Gemini 3 Pro är inte längre flaggskeppet** — men posten bär fyra halveringstider i en mening, så läs delarna var för sig. (a) **"launched 18 November 2025" → stämmer**, exakt: Googles post är daterad 2025-11-18. (b) **En-miljon-tokens kontextfönster → stämmer**, ordagrant: "…and **1 million-token context window**". (c) **"The current flagship model is Gemini 3 Pro" → fel.** Gemini 3 Pro släpptes "in preview" och är inte längre flaggskeppet: **Gemini 3.5** annonserades 19 maj 2026 ("we're introducing Gemini 3.5, our latest family of models"), dess 3.5 Flash slog redan **Gemini 3.1 Pro** på kodnings- och agentbänkar, 3.5 Pro rullade ut månaden efter, och **Gemini 3.8 Flash** är daterad 28 september 2026. (d) **"Gemini 3 Flash-level access" på fria nivån → fel.** Gemini 3 Flash blev gratis standardmodell 17 december 2025, men appens fria modell har följt familjen vidare. (e) **"Gemini 3 Pro with Deep Think" → fel: `Gemini 3 Deep Think`.** Google namnger det som ett eget läge, inte en Pro-variant: "We're also introducing **Gemini 3 Deep Think** — our enhanced reasoning mode". — **Rätt skrivning namnger ingen versionssiffra.** Det här är guidens mest färskvarubetonade påstående: fem delpåståenden, tre fel, och de blir fel igen inom månader om de ersätts med dagens siffror i stället för med en formulering som inte daterar sig — **ÅTGÄRDAT i Task 9 (2026-10-12):** **ingen versionssiffra står kvar i brödtexten.** (a)/(b) Släppdatumet 18 november 2025 och en-miljon-tokens-fönstret stämmer, men bara som egenskaper hos en modell som inte längre är flaggskeppet, så de följde namnet ut; "a long context window and strong multimodal reasoning" står kvar utan siffra (EP:632/EW:119). (c) "The current flagship model is Gemini 3 Pro" är ersatt av en formulering som pekar läsaren på modellväljaren i appen. (d) "Gemini 3 Flash-level access" på fria nivån → "Google's standard model for free accounts" (nu EP:1533/EW:1128). (e) "Gemini 3 Pro with Deep Think" → **`Gemini 3 Deep Think`**, Googles eget namn på läget, inte en Pro-variant (EP:1569/EW:1164). — **RÄTTAT i fixrunda 2 (2026-10-12): den här cellen sa först att läget skrevs "utan versionssiffran" och att `grep "Gemini 3 "` ger noll träffar på båda ytorna. Båda leden är överspelade av koordinatorns ruling 4 i fixrunda 1**, som slog fast att den generella regeln ("rätt skrivning namnger ingen versionssiffra") gäller **siffror källan inte bär** — och det här namnet bär den, eftersom cellens eget rätta värde är `Gemini 3 Deep Think`. Ytan bär därför namnet i sin helhet, och **`grep -c "Gemini 3 "` ger 1 per huvudyta, inte 0**; det är den enda versionssiffran som står kvar i brödtexten, och den står där med källa. Delarna (a)–(d) är oförändrade. **Samma defekt som redan rättades en gång i G48:** en cell som beskriver ytan fel är värre än en cell som inte beskriver den, eftersom nästa runda läser cellen och inte filen. |
| G38 | `Nano Banana 2` — Googles bildmodell, "Released 26 February 2026", alias `Gemini 3.1 Flash Image`, ersätter `Nano Banana Pro`, kapacitet (upp till fem subjekt/fjorton objekt, 512px–4K) | produktnamn | 120, 317, 318, 322, 1128 | 633, 818, 819, 823, 1533 | — | blog.google `/innovation-and-ai/technology/ai/nano-banana-2/` → **200**, `published_time **2026-02-26**`; blog.google `/innovation-and-ai/technology/developers-tools/build-with-nano-banana-2/` → **200**, samma datum; båda lästa ordagrant 2026-10-12. Samt deepmind.google/models/gemini-image/flash/ → **200**, vars **sidtitel är "Nano Banana 2.1"** | **stämmer** på fyra av fem delar och **fel** på den femte — tabellens tätaste post, och cellen bär båda tokenen, inte ett samlat omdöme. (a) **"Released 26 February 2026" → stämmer**: båda Google-posterna är daterade 2026-02-26. (b) **Aliaset `Gemini 3.1 Flash Image` → stämmer**, ordagrant: "Introducing **Nano Banana 2 (Gemini 3.1 Flash Image)**, our latest state-of-the-art image model". (c) **Föregångaren `Nano Banana Pro` → stämmer**, ordagrant: "Nano Banana 2 will **replace Nano Banana Pro** across the Fast, Thinking and Pro models". Nyans guiden missar: "Google AI Pro and Ultra subscribers will **keep access to Nano Banana Pro** for specialized tasks by regenerating images via the three-dot menu" — den ersätts som standard, den dras inte in. (d) **Kapaciteten → stämmer**, ordagrant: "Maintain character resemblance of up to **five characters** and the fidelity of up to **14 objects** in a single workflow" och "resolutions **from 512px to 4K**". Guiden skriver "subjects" där Google skriver "characters" — oskadligt. Även de två kvalitativa leden håller: "web-grounded rendering of specific subjects" mot "powered by real-time information and images from web search to more accurately render specific subjects", och "genuinely precise text rendering" mot "**Precision text rendering** and translation". (e) **Den del som gått sönder → fel: "the default image generator in the Gemini app".** Google DeepMinds aktuella bildmodellsida heter **Nano Banana 2.1**, och en "Nano Banana 2 Lite" finns därutöver. Nano Banana 2 är inte längre den nyaste, och "default" är därmed osäkert. Samma lärdom som G37: skriv funktionen, inte versionsnumret — **ÅTGÄRDAT i Task 9 (2026-10-12):** de fyra `stämmer`-delarna är **orörda** (släppdatum 26 februari 2026, aliaset `Gemini 3.1 Flash Image`, föregångaren `Nano Banana Pro`, kapacitetssiffrorna). Den femte, "the default image generator in the Gemini app", är ersatt av Googles egen ordalydelse om vad som ersattes — "across the Fast, Thinking and Pro models" — plus den nyans cellen pekar ut: Pro- och Ultra-abonnenter behåller tillgången till Nano Banana Pro. Meningen säger nu uttryckligen att versionsnumret är ett rörligt mål, vilket är cellens egen lärdom. |
| G39 | "The newer Learning Guide format (added September 2025) runs in tutoring mode" | funktion | 339 | 840 | — | blog.google `/innovation-and-ai/models-and-research/google-labs/notebooklm-student-features/` → **200**, `published_time **2025-09-08**`, läst ordagrant 2026-10-12 | **stämmer** — båda leden ordagrant: "The new '**Learning Guide**' offers **personalized tutoring** within NotebookLM", i en post daterad 8 september 2025. Samma post belägger G09:s tre nya ljudformat, vilket gör "added September 2025" konsekvent på båda ställen i guiden. — **fel: produktnamnet** i den omgivande meningen, se G49. Och notera att samma post bär fler format som guiden inte nämner (flashcards, quizzes, upgraded reports, public notebooks) — inget att rätta, bara att veta att källan är rikare än påståendet |
| G40 | TOC-underrubriken "Eleven common questions answered" (FAQ-antal) | datumstämpel | — | 562 | — | ytan själv: `_unpublished/exports/gemini-notebooklm-print-a4-en.html`, räknat 2026-10-12 — exakt **11** block med `class="faq-item"` (och 11 vardera av `faq-item__q` / `faq-item__a`) | **stämmer** — elva frågor, elva svar, och rubriken säger elva. Räkneposterna G40 och G41 är de två i tabellen som en framtida redigering kan göra falska utan att någon märker det: om Task 5–9 lägger till eller tar bort en fråga måste TOC-underrubriken följa med — **KONTROLLERAD EFTER Task 9:s redigeringar (2026-10-12):** fortfarande exakt **11** `faq-item`-block på EP, och TOC-underrubriken säger elva. Task 9 lade inte till och tog inte bort någon fråga — bara innehåll inuti tre befintliga svar (fria nivån, uppgraderingsfrågan, Gem-frågan). |
| G41 | Rubriken "Five classroom workflows that compound" | datumstämpel | 353 | 850 | — | ytan själv, EP: rubriken på rad 850 och de numrerade arbetsflödena på rad 853, 856, 859, 862, 865 — räknat 2026-10-12 | **stämmer** — exakt fem numrerade arbetsflöden under rubriken "Five classroom workflows that compound". Samma varning som G40: siffran i rubriken är bara sann så länge ingen rör listan. Notera för Task 9 att guiden har **tre** numrerade serier av det här slaget (EP:724–739 fem snabbflöden, EP:853–865 de fem som rubriken räknar, EP:1178–1296 nio promptkort — radnumren mätta före Task 9; rubriken och dess fem flöden ligger kvar på EP:850 respektive 853–865) — bara den mellersta har en siffra i rubriken, och det är bara den som kan bli fel — **KONTROLLERAD EFTER Task 9:s redigeringar (2026-10-12):** fortfarande exakt **fem** numrerade arbetsflöden under rubriken. Oförändrad. |
| G42 | "Your practical compliance checklist" — nio-punktslistan i bonuskapitlet (DPIA, DPA, dataresidens, sekretessinställningar, Article 30-journalföring, AI Act-riskklassning, DPO, Article 4-kadens, larmkanal) — bär bonuskapitlets **fjärde** `Article 30`-förekomst, som annars inte täcks av G23/G24/G33 | regelverk | 573, 575–582 | 1061, 1063–1070 | — | punkt för punkt: artikel 30 → www.edpb.europa.eu → **200** (se G33); AI Act-riskklassningen → `korsref P13` (se G26); artikel 4-kadensen → `korsref P13` (se G27); dataresidensen → **404 × 5** (se G13); DPIA, DPA, sekretessinställningar, DPO och larmkanal bär ingen volatil uppgift | **stämmer** på sju av nio punkter. — **fel** på riskklassningspunkten (nu EP:1067/EW:579 "We have classified our intended uses against the EU AI Act risk tiers" och nu EP:1068/EW:580 "any use that approaches the **High-risk** tier"): nivånamnen måste bli de fyra rättade ur G26, annars säger checklistan och pyramiden olika saker på samma sida. — **obelagt** på dataresidenspunkten (nu EP:1065/EW:577), som ärver G13:s 404. — **Det här är posten som bär bonuskapitlets fjärde `Article 30`-förekomst** (EP:1072 — **punkten finns inte längre**: Task 7 bytte den mot Article 4-kadensen, nu EP:1069/EW:581, och `Article 30` står noll gånger på båda engelska ytorna). Vid sidan av G23, G24 och G33. **Alla fyra måste ändras i samma commit** — ändras tre av dem står den fjärde kvar och motsäger de andra, och ingen vakt fångar det förrän Task 12 — **KONTROLLERAD i Task 9 (2026-10-12), ingen åtgärd:** riskklassningspunktens nivånamn rättades i Task 7 (`High risk` var redan det enda rätta av de fyra), och dataresidenspunkten ärver G13:s `obelagt`, som Task 6 och 7 åtgärdade. Inget i posten rörs av Task 9. |
| G43 | Alice Keeler-citatet om Gems: "generic AI that understands nothing about your classroom" | citat | 280, 1199 | 785, 1604 | — | alicekeeler.com/2025/07/23/ai-sucks-at-student-engagement/ → **200**, läst ordagrant 2026-10-12; samt alicekeeler.com/2026/06/06/what-are-google-gemini-gems/ → **200** och alicekeeler.com/2026/06/06/ditch-magic-school-use-gems-instead/ → **200** — ingen av de tre innehåller guidens citerade fras | **stämmer** på parafrasen, **obelagt** på citatet — ett delat utfall. **stämmer** på parafrasen: guidens "a generic AI tool cannot understand the nuances of your classroom or the principles of effective pedagogy" ligger nästan ordagrant på hennes egen mening — "You cannot expect a generic tool to understand the nuances of your classroom or the principles of effective pedagogy." Det är korrekt återgivet och kan stå. — **obelagt: den citerade frasen** "generic AI that understands nothing about your classroom". Strängen finns **ingenstans** på hennes sajt; det är guidens egen formulering inom citationstecken. Antingen stryks tecknen eller byts frasen mot hennes verkliga ord, som guiden redan har i meningen före. — **fel: attributionen.** Meningen kommer ur ett inlägg om elevengagemang (23 juli 2025), inte ur någon som "writing about why she loves the concept of Gems". Hennes två Gems-inlägg (båda 6 juni 2026) innehåller den inte — **ÅTGÄRDAT i Task 9 (2026-10-12):** parafrasen står nu som det citat den i praktiken var, ordagrant hennes: *"You cannot expect a generic tool to understand the nuances of your classroom or the principles of effective pedagogy."* Den citerade frasen "generic AI that understands nothing about your classroom", som inte finns någonstans på hennes sajt, är borta tillsammans med sina citationstecken. Attributionen är rättad: meningen kommer ur ett inlägg om elevengagemang, inte ur något om Gems. (EP:785/EW:280.) |
| G44 | Kasey Bell-citaten: "a podcast for your commute" och "a deeply embedded teaching assistant directly within your workflow" | citat | 306, 424, 1199 | 809, 918, 1604 | — | shakeuplearning.libsyn.com/notebooklm-your-new-teaching-assistant → **200**, avsnitt **#252**, daterat **Jul 7, 2026**; shakeuplearning.com/blog/author/kaseybell/ → **200**; shakeuplearning.com/blog/ → **200** — samtliga lästa ordagrant 2026-10-12. Varken "a podcast for your commute" eller "a deeply embedded teaching assistant directly within your workflow" förekommer på någon av dem, och riktade sökningar hittade ingen sida där hon säger något av det | **obelagt: inget av de två citaten finns ordagrant.** Båda står inom citationstecken och inget av dem går att belägga — samma regel som fällde G20. Vad som **är** belagt: hennes avsnitt #252 heter "**NotebookLM: Your New Teaching Assistant**" och är daterat 7 juli 2026, och hennes blogginlägg samma dag heter "NotebookLM: Your New AI Teaching Assistant". Idén är hennes; orden är inte. Rätt åtgärd: byt de två citaten mot hennes verkliga rubrik, eller stryk citationstecknen och behåll resonemanget som guidens eget — **ÅTGÄRDAT i Task 9 (2026-10-12):** inget av de två obelagda citaten står kvar. EP:809/EW:306 behåller resonemanget som guidens eget, utan citationstecken och utan attribution ("a podcast for your commute, in effect"). EP:918/EW:424 bär i stället hennes verkliga, verifierbara rubrik: Shake Up Learning, avsnitt 252, "NotebookLM: Your New Teaching Assistant", juli 2026. **Rubriken behåller det gamla produktnamnet med avsikt** — ett citat som "rättas" är inte längre ett citat, och G49:s källcell säger uttryckligen att citerade rubriker inte ska skrivas om. Det är den enda `NotebookLM`-förekomsten per huvudyta efter Task 9, och den är ett citat, inte en överlevare i guidens röst. Avsnittsnumret skrivs **utan brädgård** ("episode 252"), eftersom `test_templates_have_zero_hardcoded_hex` matchar `#[0-9a-fA-F]{3,8}` och läste "#252" som en hårdkodad hexfärg. |
| G45 | Eric Curts och `edugems.ai` — "roughly 200 ready-to-use Gems"/"about 200 free education Gems", "growing every month" | produktnamn | 284, 415, 1171 | 789, 909, 1576 | — | www.edugems.ai → **200** (edugems.ai omdirigerar dit), hela sidan läst ordagrant 2026-10-12; antalet räknat lokalt ur den hämtade HTML:en | **stämmer** på Eric Curts och på att edugems.ai är ett fritt Gem-bibliotek för lärare — sidan namnger honom ("Edu💎Gems - by Eric Curts", ericcurts@gmail.com) och "a growing collection of pre-made prompts ('Gems') for educators to use with Google Gemini". **stämmer** även på "growing every month": sidan har ett eget "📢 Newest EduGems"-avsnitt och Curts skriver "I will also continue to add many more prompts to the site". — **obelagt: siten publicerar ingen siffra.** Ingen räkning står någonstans på sidan, och en lokal räkning av distinkta Gem-namn i den hämtade HTML:en ger **≈168** (176 unika ankartexter inklusive navigation). "Roughly 200" / "around 200" överskattar alltså, med en siffra källan själv inte påstår. Rätt skrivning anger inget antal — biblioteket växer, och varje siffra blir fel i båda riktningarna över tid. — **fel: Gems blir Skills.** Sidans egen banner, ordagrant: "**Note: Google has announced that Gems will be transitioning to Skills.** Over the next few months I will be converting all of the EduGems on this site to Skills. Everyone will continue to be able to use all of the prompts on this site as Gems (through this school year), as Skills (going forward), and always as copyable prompts." Biblioteket guiden pekar på byggs om under ett annat produktnamn. Se G06 — **ÅTGÄRDAT i Task 9 (2026-10-12):** **inget antal står kvar.** "roughly 200" (EP:789/EW:284), "around 200" (EP:909/EW:415) och "about 200" (EP:1574/EW:1169, nu EP:1576/EW:1171) är alla ersatta av "a free, growing library/collection" — siten publicerar ingen siffra och en lokal räkning gav ≈168, så varje tal vore guidens eget. Eric Curts, biblioteket och "growing" står kvar, enligt de två `stämmer`-tokenen. Och Gems→Skills-övergången, belagd ordagrant på sidans banner, är skriven **en gång**, där biblioteket presenteras: Google har annonserat övergången och Curts konverterar sitt bibliotek, men prompterna fungerar oavsett. Se G06. |
| G46 | Googles fyra inbyggda mall-Gems i Classroom: "Study partner, Quiz me, Brainstorm partner, Real-world connector" | produktnamn | 284, 415 | 789, 909 | — | blog.google `/products-and-platforms/products/education/classroom-ai-features/` → **200**, `published_time 2025-06-30`, läst ordagrant 2026-10-12 | **stämmer** — alla fyra namnen ordagrant och i samma ordning som guiden har dem: "Classroom will include four Gems templates to help educators get started: **Study partner, Quiz me, Brainstorm partner and Real-world connector**." — **Förbehåll för Task 9:** källan är en **framtidsformulerad** post från juni 2025 ("will include"), och ingen senare hämtad sida bekräftar att de fyra fortfarande levereras. Tillsammans med G06/G45:s Gems→Skills-övergång gör det namnen osäkra på medellång sikt. De är rätt i dag; de är inte rätt för evigt |
| G47 | Vidareläsningens namnlista över lärarbloggare/podcastare: "Matt Miller, Monica Burns, Kasey Bell, Eric Curts, Alice Keeler, Tony Vincent, Jake Miller" | citat | 1199 | 1604 | — | fyra av sju namn belagda med sidor hämtade i den här uppgiften, lästa 2026-10-12: Matt Miller (ditchthattextbook.com/notebooklm/ → **200**), Kasey Bell (shakeuplearning.libsyn.com → **200**), Eric Curts (www.edugems.ai → **200**), Alice Keeler (alicekeeler.com → **200**). Monica Burns, Tony Vincent och Jake Miller **inte hämtade**. Länkarna: support.google.com/gemini → **200**; support.google.com/notebooklm → **301 → support.google.com/gemininotebook/ → 200** | **stämmer** — båda hjälpsidespekarna löser ut och svarar 200, till skillnad från Copilot-rundans quick-start som pekade mot en 404. Fyra av sju namn är belagda med sidor som hämtades i den här uppgiften. — **fel: pekaren bär det gamla namnet.** Guiden trycker "support.google.com/notebooklm", som omdirigerar till ett hjälpcenter med titeln "**Gemini Notebook Help**". *Länken* fungerar — Google skriver uttryckligen "Automatic redirects will ensure existing shared notebooks and user links continue to work" — men den tryckta strängen är det avlagda varumärket. Se G49. — **obelagt (ej kontrollerad)** för de tre namn jag inte hämtade: inte betvivlade, bara inte kontrollerade här — **KONTROLLERAD i Task 9 (2026-10-12), ingen åtgärd:** den tryckta hjälpsides-URL:en bär sedan Task 4C `support.google.com/gemininotebook`, alltså dit värden 301:ar. Namnlistan är orörd, och `obelagt (ej kontrollerad)` är en **kvalificerad** token som enligt vokabulärtabellen inte utlöser omskrivning. |
| G48 | **NY POST (Task 4).** AI Act-ingressens andra datummening: "On 2 August 2026, general applicability begins, transparency rules apply, and most high-risk obligations take effect" — det femte AI Act-felet, som varken Task 3:s inventering eller briefens tabell täckte | regelverk | 535 | 1024 | — | `korsref P13` | **fel: bara transparensskyldigheterna gäller från 2 augusti 2026.** Meningen säger "On 2 August 2026, general applicability begins, transparency rules apply, and **most high-risk obligations take effect**". P13 bär kommissionens ordalydelse: "The **transparency rules** of the AI Act will come into effect in August 2026", medan "the rules for **high-risk** use cases in certain sensitive areas (**Annex III**) have been extended to **2 December 2027** as a result of … the AI Omnibus", och produktinbyggd högrisk "apply from 2 August 2028". **Annex III omfattar uttryckligen utbildning**, så satsen är fel i precis den riktning som skadar en skolläsare mest: den säger att högriskregimen redan binder dem, när bilaga III-fristen är 2 december 2027. — **Rätt skrivning, i den ordningen:** förbuden och AI-kunnigheten sedan 2 februari 2025; transparensskyldigheterna sedan 2 augusti 2026; bilaga III-högrisken från 2 december 2027. Samma tre datum, samma ordning, som den publicerade Claude-guidens ingress redan använder — **ÅTGÄRDAT i Task 7 (2026-10-12):** meningen är omskriven i Gemini-guidens egen röst, i den ordning den här cellen föreskriver: förbuden och AI-kunnigheten sedan 2 februari 2025, transparensskyldigheterna sedan 2 augusti 2026, bilaga III-högrisken (utbildning) från 2 december 2027, produktinbyggd högrisk från 2 augusti 2028. Den säger uttryckligen att bara två av de fyra dateringarna binder läsaren i dag. **Två av stycket tre sakled delar ordalydelse med syskonguiden, ordagrant, och det är avsiktligt — rättat i Task 7:s fixrunda 2 (2026-10-12), där den första formuleringen av den här noteringen hävdade motsatsen.** Transparensmeningen (*”The transparency obligations have applied since the Act itself became applicable[,] on 2 August 2026”*) är identisk med `exports/claude-print-a4-en.html:1269` så när som på ett inskjutet kommatecken, och bilaga III-satsen (*”through the AI Omnibus, the Annex III uses that cover education apply from 2 December 2027, and high-risk systems built into products from 2 August 2028”*, 24 ord) är ordagrant densamma. Briefens steg 4 bad om det motsatta; **koordinatorn överkörde sin egen instruktion vid granskningen av fixrunda 1**, med skälet att två guider av samma författare som bär en uppsättning rättsliga dateringar bör formulera dem likadant: en läsare som jämför de två guiderna ska inte hitta en skenbar skillnad där det inte finns en verklig. Det som ändras är alltså bara revisionsanteckningen, inte prosan — men den ändringen är nödvändig, eftersom den här cellen är rundans auktoritet och sa senare uppgifter motsatsen till vad filerna visar. **Resten av stycket är Gemini-guidens eget:** ingressmeningen (*”Four dates matter, and only two of them bind you yet”*), 2025-meningen och slutet (*”The tier that reaches furthest into school work … Use the time.”*) har ingen motsvarighet i Claude-guiden, som i stället skriver *”Most of it already applies to you”* och *”Read that as runway, not as exemption.”* |
| G49 | **NY POST (Task 4).** Produktnamnet `NotebookLM` i guidens egen prosa — 94 förekomster på EW, 97 på EP, 14 på QS, plus den tryckta hjälpsides-URL:en på EP:1610/EW:1208. Googles omdöpning till `Gemini Notebook` (16 juli 2026) ligger efter guidens datumstämpel och kunde därför inte fångas av Task 3 | produktnamn | passim (94 → 1) | passim (97 → 1) | passim (14 → 0) | workspaceupdates.googleblog.com `/2026/07/notebooklm-now-gemini-notebook.html` → **200**, daterad **July 16, 2026**, läst ordagrant 2026-10-12; blog.google `/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/` → **200**, `published_time **2026-07-16**`; bekräftat på ytterligare sex Google-sidor hämtade i dag: workspace.google.com/solutions/ai/ → **200** (briefens egen namngivna källa — **18 förekomster av "Gemini Notebook", 0 av "NotebookLM"**, mätt i både den svenska och den engelska `/intl/en/`-renderingen), support.google.com/notebooklm/ → **301 → support.google.com/gemininotebook/** (hjälpcentrets titel: "Gemini Notebook Help"), notebooklm.google.com → **301 → notebook.google.com**, notebooklm.google → **301 → notebook.google** (sidtitel "Gemini Notebook \| AI Research Tool & Thinking Partner"), edu.google.com/intl/ALL_us/ai/gemini-for-education/ → **200**, och workspaceupdates-posten 2026-08-10 → **200**, som genomgående skriver "Gemini Notebook" | **fel: produkten heter `Gemini Notebook`.** Google, ordagrant: "**We're renaming NotebookLM to Gemini Notebook.** While it remains a standalone product focused on being your premier research tool, the new name reflects how it will evolve to do more across the Google ecosystem." Utrullning från **16 juli 2026**. — **Omfattningen:** `NotebookLM` förekommer **94 gånger på EW, 97 på EP och 14 på QS** — 205 förekomster över tre ytor, plus guidens namn på filnivå och i den tryckta URL:en på EP:1604/EW:1199 (G47). Det är rundans **enskilt mest omfattande sakfel**, och det är inget som kan rättas post för post: det är ett namnbyte genom hela dokumentet. — **Varför guiden inte kan ha fångat det:** guiden är stämplad april 2026 (G01) och namnbytet kom i juli. Det är själva skälet att datumstämpeln måste flyttas i samma commit som namnet. — **Vad som mildrar:** Googles automatiska omdirigeringar håller alla gamla länkar vid liv, så ingen läsare landar på en 404; och "NotebookLM" är fortfarande det namn tredjepartskällorna använder (Pedagog Eskilstuna, Ditch That Textbook, Kasey Bells avsnitt #252, choosewise.educations egen styles-sida), så citerade rubriker och källhänvisningar ska **inte** skrivas om. Rätt åtgärd skiljer alltså guidens egen prosa från citerat material. — **Posten är tillagd i Task 4** (se Observationer); den fanns inte i Task 3:s inventering, eftersom steg 3 mätte förekomster och inte prövade namnet mot källan — **ÅTGÄRDAT i Task 4C (2026-10-12):** guidens egen röst skriver `Gemini Notebook` på alla tre engelska ytorna. Före → efter: **EW 94 → 4, EP 97 → 4, QS 14 → 0.** Titeln är `Gemini &amp; Gemini Notebook for teachers and school leaders` (EP:5, EP:462, EW:6, EW:8, EW:49; QS:5, QS:176, QS:243, QS:252, QS:328 bär quick-startens motsvarighet). Den tryckta hjälpsides-URL:en är satt till `support.google.com/gemininotebook` (EP:1604, EW:1199) och produktdomänen `notebooklm.google.com` till `notebook.google.com` (EP:661, EW:151, QS:194) — båda dit värdarna **301:ar**, inte dit de pekade. — **Kortformen `Notebook` användes inte**, och det är ett medvetet val: guiden använder redan `Notebook`/`Notebooks` om *artefakten* (28 + 10 förekomster bara på EP), så kortformen hade läst som notisboken och inte som produkten. `Gemini Notebook` står därför i sin helhet överallt, också i de 24 + 7 meningar som nu säger ”Gemini and Gemini Notebook” respektive ”Gemini or Gemini Notebook” — samma form som Johans titelbeslut vid grinden. — **De fyra överlevande förekomsterna (ursprungligen åtta; två strukna av Task 6 och två av Task 7, båda 2026-10-12 — se nedan), alla provisoriska.** Ingen av dem är permanent, och listan är skriven så att en läsare kan se vilken uppgift som tar bort var och en. **(1) Millerramen, fyra förekomster:** EP:636 (kol 300), EP:719 (kol 69), EW:126/nu EW:123 (kol 302), EW:212/nu EW:209 (kol 71) — samma mening på båda ytorna, *”Matt Miller … NotebookLM is «a personal tutor that only knows what you teach»”*. Ramen (`NotebookLM is`) står **utanför** citattecknen och är alltså guidens röst, men namnet bytte inte här, eftersom hela konstruktionen går: **G20** är `obelagt` — citatet står inte på Millers sida, som svarade 200 och bär varken ”personal tutor” eller ”only knows what you teach” — och meningen ersätts med den rad som verifierades där (”It becomes an instant expert on the documents you give it.”), med attributionen kvar. **Elimineras av Task 9**, som skriver `Gemini Notebook` i den nya ramen. **(2) `NotebookLM Enterprise`, var fyra förekomster, nu noll:** ~~EP:973~~, ~~EP:1023 (nu EP:1024)~~, ~~EW:485~~, ~~EW:537 (nu EW:535)~~. Namnet **återställdes** till det gamla i Task 4C:s fix-commit efter koordinatorns ruling: `Gemini Notebook Enterprise` är ett namn ingen källa bär, och `Gemini Enterprise` hade varit värre — **G13** är `obelagt`, med fem 404:or på det gamla namnet och EU-residenslöftet *inte* klart dokumenterat i offentligt material, så ett nytt namn hade satt en påhittad bärare på ett obelagt påstående. De fyra **delade sig på två uppgifter**, och att namna fel är värre än att inte namna: **EP:973 och EW:485 eliminerade av Task 6 (2026-10-12)** — huvudflödets residenspassage (EP 972–979, EW 484–491; efter samma commit EP 972–980, EW 481–489) skrevs om, uppgiftens tabell lät meningen *stanna* ”bara om Task 4 gav `fel` eller `obelagt`”, och Task 4 gav `obelagt`, så den skrevs om och produktnamnet gick med det konkreta löftet. **EP:1023/nu EP:1024 och EW:537/nu EW:535 eliminerade av Task 7 (2026-10-12)** — bonuskapitlets GDPR-avsnitt är borta i sin helhet, och residensmeningen med det: den var en dubblett av huvudflödets, som efter Task 6 bär samma produktfakta jurisdiktionsneutralt. Kvar i båda fallen blir den belagda halvan (”not as clearly documented in public materials — confirm via your DPA”). — **Regeln detta etablerar, som nästa runda ärver:** *ett namnbyte hittar aldrig på ett namn för ett påstående som inventeringen märkt `fel` eller `obelagt`. Det lämnar den gamla strängen, och den uppgift som äger påståendet byter hela meningen.* Ett produktnamn som bär ett obelagt påstående är ett påstående i produktnamnets kläder. — QS bär varken citat eller Enterprise-mening och har därför **noll** överlevande; summan är **fyra** (ursprungligen åtta, två strukna av Task 6 och två av Task 7), inte noll, och ett nollvärde hade betytt att både citatet och ett obelagt påstående skrivits om. Det är den listan Task 12 gör vaktrader av — `NotebookLM` får aldrig bli en förbjuden sträng i den här guiden, lika lite som `Sweden` (G21) eller `GDPR` (G30), men **fyra uppräknade förekomster (ursprungligen åtta) som var och en har en utgångsuppgift** går att vakta exakt — och alla fyra ägs nu av Task 9. — **En vakt följde med:** `scripts/tests/test_guide_toc.py` hårdkodade TOC-raden ”Understanding Gemini and NotebookLM” som nyckel och bytte i samma commit till ”Understanding Gemini and Gemini Notebook”. Dess **ankarvärden** för Part 1 och Part 2 bär fortfarande `NotebookLM` med avsikt: de är ankare i den **ännu inte omrenderade** PDF:en och ska bytas först när filen renderats om (Task 14) — **ÅTGÄRDAT i Task 9 (2026-10-12): överlevandelistan är noll.** Millerramen — de fyra sista förekomsterna av `NotebookLM` i guidens **egen röst** (EP 636, 719; EW 123, 209) — är omskriven enligt G20 och bär `Gemini Notebook`. Räkningen i guidens egen prosa är därmed **EW 94 → 0, EP 97 → 0, QS 14 → 0**. Kvar står **en (1) förekomst per huvudyta, och den är ett citat:** Kasey Bells avsnittsrubrik "NotebookLM: Your New Teaching Assistant" (EP:918/EW:424), ny i Task 9 som den **belagda** ersättaren för G44:s två obelagda citat. Den tillhör samma kategori som Pedagog Eskilstuna, Ditch That Textbook och choosewise.educations styles-sida — citerat material som cellen uttryckligen säger att namnbytet **inte** ska röra — och är alltså inte en överlevare i den här listans mening. **För Task 12:s vaktrader:** antalet i guidens egen röst är noll och kan vaktas som sådant, men `NotebookLM` kan fortfarande inte bli en förbjuden sträng — den citerade rubriken skulle göra en sådan vakt permanent röd, exakt som `Sweden` (G21) och `GDPR` (G30) inte kan förbjudas bart. |
| G50 | **NY POST (Task 9, koordinatorns ruling 2026-10-12).** Åldersrutans medlemsstatsresonemang: "and in several EU member states, national guidance goes further still (some require head-teacher approval, or prohibit independent student use of generative AI during instruction)" — **en andra instans av exakt det resonemang G28 och G29 var**, och den enda som ligger i guidens internationella huvudflöde i stället för i det EU-skopade bonuskapitlet. Varken Task 3:s eller Task 4:s förekomstmätning fångade den, eftersom ingen av dem mätte på `member state` | inramning | **påståendet borta ur ytan** (medlemsstatsresonemanget omformulerat i Task 9, `eac0163`; den generaliserade texten står på EW:135) | **påståendet borta ur ytan** (samma, EP:648) | — | **ingen källa hämtad, och ingen är skyldig** — påståendet är ett omfångsval, inte en faktauppgift att pröva. Spec §3:s borttagningslista namnger klassen ordagrant: "resonemanget om vilka medlemsstater som publicerat nationell vägledning" | **fel (omfång).** Samma klassificering och samma skäl som G28 och G29: **ingen hämtad källa motsäger** att nationell vägledning går längre i flera EU-medlemsstater, **och den som letar efter en sådan letar förgäves** — satsen ligger utanför det omfång rundan valde (spec §3). Det är inventeringens egen definition av tokenen, och den är hela skälet att **ingen hämtning är skyldig här**. — **Varför den är en defekt där G28:s omskrivna mening inte är det:** åldersrutan står i Del 0, guidens internationella huvudflöde, och förutsätter en EU-läsare utan att säga det. Bonuskapitlet säger det: dess lede (EP:1019/EW:530) deklarerar "If you teach or lead a school in an EU member state" — en EU-skopning Task 8 installerade med avsikt. En EU-referens i ett deklarerat EU-kapitel är inramning; samma referens i huvudflödet är ett antagande om läsaren. — **ÅTGÄRDAT i Task 9 (2026-10-12):** satsen säger nu "Local rules can go further than Google's floors — requiring head-teacher approval before deployment, say, or prohibiting independent student use of generative AI during instruction", och slutmeningen syftar på den försiktigheten i stället för på en medlemsstatsöversikt. **Kraften är behållen och poängen är densamma** — det som begränsar elevanvändning är läsarens egen jurisdiktion och admin-konsol, vilket står i samma stycke — men parentesens två exempel står nu som exempel på *vad lokala regler kan kräva*, inte som en räkning av vilka som kräver det. — **Ingen leveransvaktsrad var röd, och det är värt att skriva ut:** koordinatorn mätte samtliga planerade förbudsrader mot printytan 2026-10-12 (`Every EU member state has one`, `Standard GDPR discipline`, `Article 6(1)(e)`, `Article 30`, `Swedish schools`, `Sweden, as of April 2026`, `minimal-risk tier`, `most high-risk obligations take effect`) och **alla gav noll**; den enda icke-noll är `I have a full-time job`, som är G31:s och nästa uppgifts. Posten finns alltså för specens skull, inte för en vakts. Task 9:s första rapport hävdade motsatsen och är rättad. — **Granskad i samma svep och behållen, två stycken:** (1) huvudflödets student­åtkomstmening (nu EP:987/EW:496, "National guidance on student AI use varies: some countries require head-teacher approval…") namnger **ingen** stat och inget block och har samma jurisdiktionsneutrala form som G28:s godkända omskrivning — den **stannar**. (2) Bonuskapitlets lead-in (EP:1026/EW:537, "Several EU member states have published detailed national AI-in-schools guidance…; others have not") ligger inne i **G28:s egen förekomst**, är omskriven i Task 8 och godkänd vid grinden, och står i det deklarerat EU-skopade kapitlet — den **stannar** och ägs inte av den här posten. |

## Utfallsräkningen

**50 poster** (47 ur Task 3, plus **G48** och **G49** tillagda i Task 4 och **G50** i Task 9 — se Observationer).
Räknat på varje cells **inledande** token, som är den tabellen ska gå att skanna på:

| token | antal | poster |
|---|---|---|
| `stämmer` | **30** | G03, G05, G06, G07, G08, G09, G11, G14, G15, G18, G19, G21, G22, G23, G24, G30, G32, G33, G34, G35, G38, G39, G40, G41, G42, G43, G45, G46, G47 (+ G13:s och G17:s andra token) |
| `fel` | **14** | G01, G02, G12, G16, G25, G26, G28, G29, G31, G36, G37, G48, G49, G50 — varav **G28, G29 och G50 är `fel (omfång)`**, alltså inte sakligt osanna |
| `obelagt` | **6** | G04 (`ytartefakt`), G10, G13, G17, G20, G44 — plus G24:s (`hämtningsfel`) och G47:s (`ej kontrollerad`) andra token |

**Det sakligt osanna är alltså 11 poster**, inte 14: G28, G29 och G50 ligger utanför rundans
omfång och väntar på ägarens beslut, inte på en källa.

**Kvalifikatorerna i parentes är en del av tokenen och ska läsas med den** — samma grepp som
`fel (omfång)` och `stämmer (ej volatil)` redan använder, så att den som skannar kolumnen
ser *varför* en post är obelagd utan att läsa resonemanget. `obelagt` utan kvalifikator
betyder att en **hämtad** källa säger något annat än ytan; de tre kvalificerade betyder
något annat än så:

| kvalifikator | betyder | åtgärd |
|---|---|---|
| `obelagt (ytartefakt)` | värdet kommer inte från någon källa — det är en produkt av ytans egen rendering | räkna om mot den renderade PDF:en (Task 14), hämta ingenting |
| `obelagt (hämtningsfel)` | källan gick inte att läsa; **ingen källa motsäger påståendet** | skriv **inte** om påståendet på denna grund — hämta om, eller låt det stå |
| `obelagt (ej kontrollerad)` | inte prövad i den här uppgiften; varken belagd eller betvivlad | kontrollera om den ska bära vikt, annars lämna |
| `fel (omfång)` | sakligt sann men utanför rundans omfång; **ingen källa motsäger den** | ägarens beslut, inte en källfråga |
| `stämmer (ej volatil)` | bär ingen siffra, inget datum, inget produktnamn — kan inte bli gammal | ingen åtgärd |

**Bara `obelagt` utan kvalifikator utlöser regeln "skriv om påståendet utan siffra".** De
tre kvalificerade gör det inte, och det är hela skälet att kvalifikatorn står i tokenen och
inte bara i resonemanget: en senare uppgift skannar cellen, inte rapporten.

### Poster som bär en andra token längre in i cellen

Tjugofyra av 49 celler bär mer än ett utfall. Det är inte slarv — flera poster bundlar
flera delpåståenden, och en post som kollapsas till ett omdöme ljuger om minst ett av dem.

| post | inledande | ytterligare | vad den andra tokenen gäller |
|---|---|---|---|
| G03 | stämmer | fel, fel, obelagt | produktnamnet (G49); "visible and editable in the other"; sidopanelens placering |
| G05 | stämmer | fel | licensinnehållet (G12) — namnet står kvar, innehållet är omlagt |
| G06 | stämmer | obelagt | Gems→Skills-övergången, utan hämtbart avvecklingsdatum |
| G08 | stämmer | fel | "runs on the Gemini 3 Pro backbone" |
| G09 | stämmer | fel, fel | Audio Overviews finns nu även i Gemini-appen; produktnamnet |
| G11 | stämmer | fel, fel | Cinematic är 18+, så elevexemplet faller; formatlistan har bytts |
| G13 | obelagt | stämmer | residensuppgiften är obelagd, men "not as clearly documented" stämmer |
| G14 | stämmer | fel | namnet betecknar numera den kostnadsfria nivån, inte en licens man håller |
| G15 | stämmer | obelagt | "the free tier follows" |
| G17 | obelagt | stämmer | per-app-toggles obelagda, domän/OU/grupp-spärren stämmer |
| G22 | stämmer | fel (omfång) | att nämna svenska först är ett omfångsval |
| G23 | stämmer | obelagt, fel | tre meningar, tre svar: tillsyn / residens / Sverige-parentesen |
| G24 | stämmer | obelagt | artikel 6(1)(e) och artikel 30:s fältlista — EUR-Lex 202/0 byte |
| G25 | fel | stämmer, stämmer | ikraftträdandet 1 aug 2024 och "education is explicitly in scope" ändras inte |
| G26 | fel | stämmer | "High risk" är det enda av de fyra namnen som är rätt |
| G32 | stämmer | obelagt | "link in the footer" fungerar inte på en tryckt A4-PDF |
| G34 | stämmer | stämmer | ej volatil — ingen siffra, inget datum, inget produktnamn |
| G35 | stämmer | fel | sakuppgiften stämmer, attributionen till BETT 2026 gör det inte |
| G38 | stämmer | fel | fyra delfakta rätt, "default image generator" överspelat av Nano Banana 2.1 |
| G39 | stämmer | fel | datum och tutoring-läge rätt, produktnamnet i meningen fel |
| G42 | stämmer | fel, obelagt | sju av nio punkter håller; riskklassningen fel, residensen obelagd |
| G43 | stämmer | obelagt ×2, stämmer, fel | parafrasen rätt, det citerade ur luften, attributionen fel |
| G45 | stämmer | stämmer, obelagt, fel | Curts och "växer" rätt; "roughly 200" obelagt; Gems→Skills |
| G47 | stämmer | fel, obelagt | länkarna löser ut, men den tryckta strängen bär det avlagda namnet |

### Konflikter mellan källor

**Fem, och tre av dem är Google mot Google** (1, 2 och 5). Att två Google-sidor säger
olika saker är i sig ett resultat, och det står i respektive cell. *Räkningen stod på
"fyra, och tre av dem" fram till fixrunda 2 (2026-10-12) — konflikt 5 lades till i
Task 9 utan att rubriken följde med. En felaktig räkning i auktoritetsdokumentet är
ett felaktigt faktum om rundan, inte en formuleringsfråga.*

1. **BETT-posten mot sig själv (G36).** Samma sida,
   `blog.google/.../bett-2026-gemini-classroom-updates/`, säger på ett ställe "learning
   standards from the UK, Australia, Canada, Japan, Brazil, Mexico, and soon Italy" och på
   ett annat "learning standards from the **US**, UK, Australia, Canada, Japan, Brazil,
   Mexico, and soon Italy". Löst med den nyare Workspace Updates-posten (utrullning 27 maj
   2026), som räknar åtta länder med USA inkluderat.
2. **Gemini Live-sidan mot sig själv (G16).** `support.google.com/gemini/answer/15274899`
   bär i sin "What you need"-lista **både** "Be over 13 (or the applicable age in your
   country)" **och** "Be 18 or over", inuti en `gkms-context-selector` — två
   kontotypsvarianter som den extraherade texten plattar ihop. Sidan etablerar därför
   *inget* åldersgolv på egen hand; inloggningssidan (13+ personligt/skola, 18+ arbete) gör det.
3. **Ditch That Textbook mot Googles aktuella hjälpsida (G16).** Miller skriver
   "According to Google's help page, NotebookLM is available to all users 13+ through the
   browser … Content policies are stricter for users under 18 years old" — ordagrant guidens
   mening, och sannolikt dess ursprung. Googles egen sida säger i dag "above the age of
   consent (or applicable in your country)" och ingenting om strängare policy under 18. Den
   nyare primärkällan vinner, och skillnaden noteras.
4. **Ditch That Textbook mot Googles Video Overview-sida (G11).** Miller: "the format
   (explainer video or brief video)". Google i dag: **Cinematic / Explainer / Short**, med
   Cinematic låst till 18+. Samma mönster: en i övrigt bra tredjepartskälla har inte följt med.

5. **Googles Studio-panel mot Googles Gemini Apps-sida (ny, funnen i Task 9).**
   `support.google.com/gemininotebook/answer/17003757` säger ordagrant att Gemini
   **inte** kan generera Studio-artefakter — "Audio Overviews, Video Overviews,
   Infographics, Slide Deck … These features are only available in Gemini Notebook"
   (G03, G11). `support.google.com/gemini/answer/16047373` säger samtidigt att man
   skapar "podcast-style conversations … with Audio Overviews in Gemini Apps" (G09).
   Båda är hämtade, båda är Googles egna, och **båda utfallen skrevs in i guiden av
   Task 9** — vilket gjorde motsägelsen till guidens egen innan den upptäcktes i
   självgranskningen. **Koordinatorns ruling 2026-10-12: prosan får inte
   vila på den förening Task 9 först skrev.** Första försöket förklarade *varför*
   sidorna skiljer sig — att en synkad notebooks Studio inte är Gemini Apps' egen
   funktion — och det är en mekanismförklaring ingen hämtad sida gör. Guiden
   refererar nu i stället **vad varje sida säger, med sidan angiven**, konstaterar
   att de inte är överens, och ger läsaren ett handgrepp (pröva ytan du är på,
   fall tillbaka på den andra). Det är mindre prydligt och det är sant. **Den
   oförenade motsägelsen är därmed inventeringens, inte guidens**, och den är
   fortfarande värd en andra hämtning: det är den **tredje**
   Google-mot-Google-konflikten i rundan (1, 2 och 5), av fem konflikter totalt.
   *Stod "den fjärde" fram till fixrunda 2 (2026-10-12).*

**En skillnad som inte är en konflikt men liknar en:** tredjepartskällorna
(Pedagog Eskilstuna, Ditch That Textbook, Kasey Bells avsnitt #252, choosewise.educations
egen styles-sida) skriver alla fortfarande "NotebookLM". De har inte fel — de citerar och
daterar sig själva. Det är guidens **egen prosa** som ska byta namn (G49), inte citerat
material.

## Observationer utanför posterna

**Quick-start-ytan (QS) bär noll av de arton strängar leveransvakten
förbjuder** (mätt 2026-10-12, Steg 2: `Swedish\|Sweden\|Skolverket\|IMY\|GDPR\|
Schrems\|DPIA\|Article [0-9]\|data protection authority\|supervisory\|member
state\|April 2026` gav noll träffar i
`_unpublished/exports/gemini-notebook-quick-start-en.html`). **Sökvägen rättad i
fixrunda 2 (2026-10-12), och det är en rättelse av en *färskvara*, inte av en
mätning: sökvägen var korrekt när mätningen gjordes.** Task 4 kördes före
namnbytesuppgiften, och filen döptes om till `gemini-notebook-…` i Task 4B efteråt,
varför den citerade sökvägen pekade på en fil som inte längre finns — ett `grep`
mot den hade gett "noll träffar" av fel skäl. Granskaren har mätt om samtliga
arton strängar mot den verkliga filen och **alla är noll**, så slutsatsen står.
Lärdomen: en mätning som citerar en sökväg måste läsas om efter varje uppgift som
flyttar filer. Till skillnad
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

### Task 4:s observationer

**Två poster är tillagda i Task 4, och de hade inte kunnat hittas av Task 3.**
**G48** är det femte AI Act-felet: meningen på EP:1029/EW:543 säger att "most high-risk
obligations take effect" 2 augusti 2026, medan P13 belägger att bara
transparensskyldigheterna gör det och att bilaga III-högrisken — där utbildning uttryckligen
ingår — är framflyttad till 2 december 2027. Task 3 inventerade förekomster; den prövade
inte meningarna mot P13, och briefens tabell listade fyra värden, inte fem.
**G49** är produktnamnet: Google döpte om `NotebookLM` till `Gemini Notebook` den
**16 juli 2026**, tre månader efter guidens datumstämpel. 205 förekomster över tre ytor.
Ingen förekomstmätning kan upptäcka ett namnbyte — bara en hämtning kan.

**Briefens två namngivna edu-källor svarar 404, och det är ett resultat.**
`edu.google.com/workspace-for-education/editions/` och
`edu.google.com/workspace-for-education/gemini/` gav båda **404**, liksom fem andra former
av samma sökväg (`/intl/en/`, `/intl/en_us/`, `/workspace-for-education/`,
`/workspace-for-education/products/`, `/workspace-for-education/products/gemini/`). Hela
den sökvägsgrenen är borta. Den sida som bär licensuppgifterna i dag ligger på
`edu.google.com/intl/ALL_us/ai/gemini-for-education/` (**200**), hittad via sökning och
sedan hämtad som rå HTML. Briefens övriga fyra källor svarade: `workspace.google.com/solutions/ai/`
**200**, `support.google.com/notebooklm/` **301 → gemininotebook/ 200**,
`support.google.com/gemini/` **200**, och NotebookLM Enterprise-dokumentationen **404**.

**EUR-Lex går inte att läsa med `curl` härifrån.** Fem URL-former gav **HTTP 202 med 0 byte**
(CELEX HTML, konsoliderad HTML, TXT, PDF, ELI) och publications.europa.eus Cellar gav
**400/406**. Det sätter G24:s artikel 6(1)(e) och artikel 30:s fältlista på `obelagt` — men
**som hämtningsfel, inte som motsägelse.** Ingen källa jag läste säger något annat, och
artikel 30 är ändå belagd på sitt namn och sin innebörd genom EDPB:s egen dokumenttitel
(**200**). Den som vill ha de återstående GDPR-detaljerna belagda behöver en hämtningsväg
EUR-Lex inte stänger; det är ett av tre ställen där en andra källhämtning vore värd något.

**Tre produktnamn är i rörelse samtidigt, och de rör sig i samma riktning.**
`NotebookLM` → `Gemini Notebook` (gjort, 16 juli 2026, G49). `Gems` → `Skills` (annonserat,
utan datum, G06/G45). `NotebookLM Enterprise` → upplöst i `Gemini Enterprise` (G13:s 404).
Guiden bygger alltså sin produktvokabulär på tre namn som Google samlar in under
Gemini-paraplyet. Det är inte tre separata fel att rätta var för sig — det är ett mönster, och
den skrivning som håller längst namnger funktionen och inte varumärket där det går.

**Fyra versionsnummer åldras snabbare än guiden.** Gemini 3 Pro (18 nov 2025) →
Gemini 3 Flash (17 dec 2025) → Gemini 3.1 Pro → **Gemini 3.5** (19 maj 2026) → 3.5 Pro
(juni 2026) → **Gemini 3.8 Flash** (28 sep 2026). Och på bildsidan: Nano Banana (aug 2025)
→ Nano Banana Pro (nov 2025) → **Nano Banana 2** (26 feb 2026) → **Nano Banana 2.1**.
Guiden namnger fyra av dessa och binder sig därmed till ett fönster på några månader.
G37 och G38 bär båda samma lärdom: **delfakta med datum håller (släppdatum, kontextfönster,
kapacitetssiffror), superlativ håller inte** ("current flagship", "the default image
generator", "Flash-level access" på fria nivån).

**Åldersgränserna har rört sig åt motsatt håll mot vad guiden varnar för.** Guidens
genomgående hållning är att elevanvändning under 18 är spärrad. Sedan **10 augusti 2026**
gäller Gemini in Classroom "K-12 and higher education students **of all ages**", under-18
får "a distinct product experience with extra guardrails and AI literacy resources", och de
18+-spärrar som faktiskt är dokumenterade är smala (Cinematic Video Overviews,
Visual Style-väljaren, "certain NotebookLM features"). Det är den rättelse som ändrar mest
för en läsare: från "det går inte" till "det går, med en annan upplevelse och en
admin-inställning".

**Och licensvägen är omlagd, inte bara omformulerad.** Guiden säger att premium-Gemini i
Workspace-apparna kommer **utan extra kostnad** till Education Plus och Teaching & Learning
add-on. Googles egen prissida säger i dag att `Gemini for Education` är kostnadsfri och
ingår i alla editioner, medan full tillgång till Gemini i Workspace-apparna kräver
`Google AI Pro for Education` — **$15,00/användare/månad** vid ettårsåtagande, och Education
Plus köper bara **25 % rabatt** på den. Guidens mening är alltså omvänd mot källan, i en
riktning som kostar pengar för den som planerar budget på den.

**Vad som inte behöver åtgärdas, men inte får missas som "förbisett":** G27 (artikel 4 sedan
2 februari 2025) stämmer på samtliga fjorton rader och ändras inte. G19 (140 stilar) är den
enda siffran i guiden som en hämtad källa bekräftar på siffran — 140 poster i
`styles-en.json`, räknade. G40 (elva FAQ-frågor) och G41 (fem arbetsflöden) stämmer mot
ytan själv och är de två poster en senare redigering kan göra falska utan att någon märker
det. G46 (de fyra mall-Gems) stämmer ordagrant, men står på en framtidsformulerad post från
juni 2025 och hänger på att `Gems` överlever G06.

### Task 9:s observationer

**De tre asymmetrierna är formuleringsskillnader, inte sakliga divergenser — mätta
om 2026-10-12, före redigeringen.** Task 3:s förklaring håller, och den egna
mätningen visar *var* skillnaden sitter:

| namn | EP / EW före | enhet | var skillnaden sitter | utfall |
|---|---|---|---|---|
| `Gems` | 25 / 24 | förekomster | EP har två TOC-rader som namnger Gems ("Gems, Canvas, Deep Research, Studio, workflows" och "Shared Notebooks, shared Gems, PD pathways"); EW har en skärmdump med `alt="Gemini Gems panel"` som EP saknar. Netto +1 för EP | **formuleringsskillnad** — ingen åtgärd |
| `Audio Overview` | 10 / 11 | förekomster | EW har en skärmdump med `alt="Gemini Notebook Audio Overview"`; printytan har ingen motsvarighet | **formuleringsskillnad** — ingen åtgärd |
| `AI Ultra` | 5 / 6 | förekomster (= rader) | EW:s `onerror`-platshållare (EW:351) bär texten "Google is releasing it first to AI Ultra, Pro, and Plus subscribers" | **formuleringsskillnad** — men platshållaren bär ett G15-påstående och följde därför prosans tempusrättelse, se G15 |

Ingen av de tre säger något om produkten som den andra ytan motsäger — skillnaden är
att EP har en innehållsförteckning och EW har skärmbilder. Differenserna är
dessutom **intakta efter Task 9 och efter fixrunda 1**, vilket i sig bekräftar
diagnosen: Task 9 ändrade brödtext på båda ytorna symmetriskt, och differensen
rörde sig inte.

**Enheten måste stå, annars går siffrorna inte att reproducera.** Alla tal i
tabellen ovan är **förekomster**, mätta med
`grep -o "<sträng>" <fil> | wc -l`. Radtal, mätta med `grep -c`, är andra tal för
samma text. Facit efter fixrunda 1, båda enheterna, mätt 2026-10-12:

| sträng | förekomster EP / EW | rader EP / EW | delta |
|---|---|---|---|
| `Gems` | 24 / 23 | 19 / 18 | +1 EP i båda enheterna |
| `Audio Overview` | 14 / 15 | 12 / 13 | +1 EW i båda enheterna |
| `AI Ultra` | 5 / 6 | 5 / 6 | +1 EW i båda enheterna |

**Och en varning som är hela skälet till att tabellen står här:** fram till
fixrunda 2 sa det här stycket "`Audio Overview` 12/13" om läget efter Task 9. Det
var ett *förekomsttal*, korrekt när det skrevs, men överspelat av ruling 5, som
lade till ett omnämnande av Audio Overviews per yta — förekomsterna är nu 14/15.
Att 12/13 **också** är dagens radtal är ett sammanträffande, och precis det
sammanträffande som gör en enhetslös siffra oläsbar: en läsare som reproducerar
"12/13" med `grep -c` får rätt svar på fel fråga. Deltat är ±1 i **båda**
enheterna, så diagnosen *formuleringsskillnad* håller oavsett vilken man mäter.

**Tre påståenden var först rapporterade som postlösa. Koordinatorns ruling
2026-10-12 avgjorde alla tre, och ingen av dem var postlös på det sätt rapporten
hävdade** — vilket är en lärdom i sig: "saknar post" är en slutsats som ska prövas
mot specen och mot de andra posternas klasser, inte dras av att nyckelordet inte
står i någon förekomstkolumn.

1. **"in several EU member states, national guidance goes further still"**
   (EP:648/EW:135, åldersrutan) — **en ny post, G50, `fel (omfång)`.** Spec §3:s
   borttagningslista namnger klassen ordagrant, och det är samma resonemang som
   G28 och G29 bar. Alltså ingen hämtning skyldig, bara ett omfångsbeslut som
   redan var fattat. Åtgärdad; se G50.
2. **"Student-facing features rolling out through 2026"** (EP:990/EW:499) — **inte
   en ny post: G17:s påstående på ett andra ställe.** En fras, två platser, ett
   utfall. G17:s förekomstkolumner är utökade och båda ställena är åtgärdade.
3. **"15–25 minutes of classroom-ready audio"** (QS:295) — **står kvar, och det är
   ett medvetet beslut på posten.** Det är en praktikers tidsuppskattning, inte ett
   leverantörspåstående, och en guide skriven ur tio år i klassrum är berättigad
   till sina egna uppskattningar. **Ingen källa ska letas, och siffran ska inte
   tas bort.** Den står här i stället för att vara något ingen tittade på.
   Skillnaden mot de siffror rundan strök (G37:s kontextfönster, G45:s ≈200 Gems,
   G12:s priser) är att de påstod något om *Googles produkt*; den här påstår
   något om *författarens erfarenhet av att använda den*.

**Ett produkt-UI-påstående, sett och bedömt som mindre (koordinatorns ruling 5 i
fixrunda 2).** G37:s omskrivning på EP:632/EW:119 slutar "…so any version number
printed in a guide dates the guide rather than informing you — **check the model
picker in the app instead**". Den sista satsen är ett påstående om Gemini-appens
gränssnitt, och **ingen post citerar en källa för att det finns en modellväljare
där**. Den står kvar, på ruling: risken är låg och en läsare verifierar den i tio
sekunder, till skillnad från ett pris eller ett datum. Men i en runda vars enda
absoluta regel är *en post per faktamening* förtjänar den en rad här, av samma
skäl som quick-startens tidsuppskattning: **ett omdöme på posten är inte samma
sak som något ingen tittade på.** Om den någon gång ska bära vikt — eller om
Google döper om väljaren — behöver den en egen post.

**Task 9:s egen räkning av tillämpade poster, med auktoriteten i tabellen.**
Inventeringen bär **21** celler märkta `ÅTGÄRDAT i Task 9`: G03, G05, G08, G09,
G10, G11, G12, G14, G15, G16, G17, G20, G35, G36, G37, G38, G43, G44, G45, G49,
G50. Task 9:s rapport sa först **19**, och tre av de tjugoen är av ett annat slag
än de övriga arton, vilket är varför räkningarna gick isär: **G05** bär en
korsreferens till G12 snarare än en egen redigering, **G49** bär bokföring
(överlevandelistan till noll) snarare än ett rättat värde, och **G50** skapades
och åtgärdades i fixrunda 1 och fanns inte när rapporten skrevs. **Siffran som
gäller är tabellens: 21.** En rapport som räknar annat än auktoritetsdokumentet
är en andra sanning, och rundan har bara en.

**Två posters förekomstkolumn under-räknade, och bara en strängsökning visade det.**
G12 listade EP:970/EW:482, men det omvända licenspåståendet stod på **sju** rader
per huvudyta (EP 632, 644, 662, 959, 970, 1531, 1567). G16 listade åtta rader per
yta, och alla åtta fanns. Lärdomen är G49:s i miniatyr: en post som bär ett
*påstående* snarare än en *sträng* kan inte lokaliseras av en förekomstmätning på
postens eget nyckelord — den måste läsas fram.

**En vakt fångade en falsk hexfärg, och den hade rätt.**
`test_templates_have_zero_hardcoded_hex` matchar `#[0-9a-fA-F]{3,8}\b`, och G44:s
nya, belagda attribution skrev Kasey Bells avsnittsnummer som "#252" — tre
hexsiffror efter en brädgård. Vakten rördes inte; avsnittsnumret skrivs utan
brädgård, och "episode 252" är lika verifierbart. Värt att veta för varje framtida
uppgift som skriver ett avsnitts-, paragraf- eller utgåvenummer i en mall.

**URL-kontrollen gav inget fynd.** Båda pekarna i G19 svarar fortfarande **200**,
fyra dagar efter spec §2:s mätning.

### Task 10:s observationer

**G31 skriven om på Johans eget besked, G32 oförändrad men bekräftad.** Se
G31:s och G32:s egna celler ovan för före/efter och källhänvisning. Ett öppet
fynd lämnas i G32:s cell: anvisningen där ("rätt skrivning för printytan
namnger adressen i stället för att peka på en klickbar fot") uttryckligen sköts
till den här uppgiften av Task 9:s rapport, men Task 10:s eget uppdrag bad bara
om en kontroll av avsändarneutralitet och varumärke — inte om den namngivna
adressfixen. Fixen är alltså fortfarande inte gjord; den står kvar som en
öppen punkt för nästa uppgift som redigerar avslutningsstycket, snarare än att
jag utför en redigering ingen av mina två uppdragsbeskrivningar bad om.

### Task 11:s observationer

**Quick-starten (QS) kontrollerades påstående för påstående mot inventeringens
Task 9-rättade värden, 2026-10-12, och behövde ingen ytterligare ändring.**
Samtliga sex produktpåståenden (`Workspace for Education` ×1, `Deep Research`
×1, `Audio Overview` ×4, `Video Overview` — två förekomster, inte en: QS:280
och QS:314, brevets "×1" var en undertäckning) kontrollerades mot sin post:

| QS-rad | påstående | post | utfall |
|---|---|---|---|
| 187 | "If your school runs Google Workspace for Education, use that domain account instead" | G05 | Rör bara kontotypen, inte vad licensen *ger* (G05:s `fel`-del, rättad i G12). Ingen ändring |
| 280 | "podcast-style Audio Overviews, and Video Overviews (the Cinematic format is 18+)" | G09, G11 | Redan i Task 9:s rättade form — QS:280 är uttryckligen namngiven i G11:s ÅTGÄRDAT-anteckning som rättad punkt ("Cinematic Video Overviews" → "Video Overviews (the Cinematic format is 18+)"). Ingen ändring |
| 281 | "Audio Overview of a unit plan + two readings" | G09 | Gör inget NotebookLM-exklusivitets- eller produktnamnspåstående — G09:s båda `fel`-delar gäller inte den här raden. Ingen ändring |
| 295 | "Click Audio Overview. 15–25 minutes of classroom-ready audio" | G09 (Audio Overview) + egen observation (15–25 min) | Audio Overview-namnet orört och rätt; tidsuppskattningen är redan G09-oberoende och redan beslutad att stå (se Task 9:s observationer, punkt 3). Ingen ändring |
| 299 | "Run Deep Research on a topic … Background reading … in fifteen minutes instead of an afternoon — with inline citations" | G08 | Namnet och beskrivningen stämmer; G08:s `fel`-del gäller bara backbone-modellpåståendet ("Gemini 3 Pro"), som QS aldrig gjorde. Ingen ändring |
| 314 | "13 or over … for Gemini on a personal or school account, 18 or over on a work account, and Gemini Notebook in a browser from your country's age of consent" | G16 | Redan i Task 9:s rättade form — QS:314 är uttryckligen namngiven i G16:s ÅTGÄRDAT-anteckning. Ingen ändring |

`Gems` och `Canvas` förekommer noll gånger i QS (kontrollerat med `grep -n`) —
ingenting att stämma av där. **Ingen rad i tabellen ovan krävde en redigering**,
och ingen commit gjordes för Task 11.

**Två punkter kontrollerade och lämnade som de var, med skäl:**

1. **QS:319, "choosewise.education / guides / gemini-notebook".** Briefens
   egen mätning citerar den äldre sökvägen (`…/gemini-notebooklm`); filen
   bär redan den aktuella (`…/gemini-notebook`) — ett tecken på att briefen
   skrevs före ett namnbytessteg som redan passerat filen. Sökvägen är
   ägarens avsiktliga val (ruling 2026-10-12): den **stannar**, även om den
   svarar 404 i dag (`curl` bekräftar **404** på båda formerna 2026-10-12) —
   guiden är opublicerad, spec §1 tillåter ingen publicering den här rundan,
   och adressen blir giltig när den publiceras. `scripts/build-seo-meta.py`
   och `_unpublished/README.md` fortsätter ange den gamla sökvägen; den
   motsättningen är en registrerad skuld för publiceringsrundan, inte något
   Task 11 rättar.
2. **QS:295, "15–25 minutes of classroom-ready audio".** Redan beslutad och
   noterad i Task 9:s observationer (punkt 3): en praktikers egen
   tidsuppskattning, inte ett leverantörspåstående om Google-produkten. Ingen
   källa söks, siffran rörs inte.

### Task 12:s förekomstsvep

Förekomstkolumnerna (EW/EP/QS) i posttabellen ovan är **ommätta mot de
slutliga ytorna** i Task 12 — 79 celler i 50 poster ändrades. Numren i
Task 3:s och Task 4:s mätningar hade glidit vid varje innehållsuppgift,
och tre granskningar rapporterade samma klass av fynd: en post pekade på
en annan posts text. De tre kända fallen (G13, G28, G29) var inte de
enda.

**Nio poster bär nu `påståendet borta ur ytan` i stället för ett
nummer**, med den uppgift som tog meningen namngiven: G10 (beta-etiketten),
G13 (`NotebookLM Enterprise`), G17 (per-app-togglarnas utrullningsdatum),
G24 (hela GDPR-avsnittet), G31 (heltidstjänsten), G35
(BETT-attributionen), G37 (`Gemini 3 Pro` och kontextfönstret), G50
(medlemsstatsresonemanget) — plus G29, som redan stod så. Ett gammalt
nummer hade i varje fall pekat på någon annans text.

**Tre asymmetrier är mätta och står kvar med avsikt:** `Gems` EP 24 / EW
22, `Canvas` EP 19 / EW 18 och `Workspace for Education` 22/22 (var
24/24). Print bär innehållsförteckning och promptkort som webbytan inte
har; asymmetrin är en ytskillnad, inte ett sakfel.

**Ett befintligt tabellfel är noterat men orört:** G49:s källcell bär ett
oescapat `|`, vilket ger raden nio datakolumner i stället för åtta och
förskjuter dess rendering. Kolumn 4–6 ligger ändå rätt. Rättningen hör
till källkolumnen, inte till det här svepet.

## Vaktblock

```guard
# Engelska ytorna: EW `_unpublished/guides/gemini-notebook/index.html` (web)
# + EP `_unpublished/exports/gemini-notebook-print-a4-en.html` (print).
# QS står utanför vakten med avsikt (spec §5) och bevakas av
# scripts/tests/test_guide_delivery.py.
#
# Varje rad nedan är MÄTT mot båda ytorna i Task 12 med vaktens egen
# normalisering, inte ärvd från planen och inte greppad: `aktiv` står
# ordagrant på båda, `borttaget` på ingen. Grupperna bär den uppgift som
# gjorde rättningen, så nästa rundas läsare inte behöver gå till
# posttabellen för att veta vem som strök vad.
#
# TVÅ SEMANTIKREGLER som gäller när rader läggs till här:
#  1. `borttaget`: en LÄNGRE sträng som innehåller en kortare förbjuden
#     sträng är strikt SVAGARE än den korta — en återinföring träffar
#     alltid den korta raden först. Lägg alltså aldrig till en lång
#     förbudsrad "som extra skydd" kring en kort som redan står här.
#     (Task 12 hade en sådan rad för G42:s RoPA-punkt och tog bort den:
#     dess värde innehöll `Article 30`, som redan är en G24-rad.)
#  2. `aktiv`: där gäller det omvända. En kort ankarrad på själva värdet
#     överlever en legitim omformulering av den långa meningen, vilket
#     den långa raden inte gör. Därför står `2 December 2027` kvar vid
#     sidan av Annex III-meningen, och `Gemini Notebook` vid sidan av
#     G49:s fyra fras-rader.
#
# INGEN BAR "April 2026"-RAD, och inget bart "Sweden"/"Swedish"/"GDPR"/
# "NotebookLM". Åtta meningar bär datumet som daterat PRODUKTpåstående
# (G03), ordet Sweden står två gånger per yta i det källbelagda
# praktikexemplet (G21), GDPR en gång per yta i promptmallens
# platshållare (G30) och NotebookLM en gång per yta i Kasey Bells
# avsnittstitel (G44) — en citattitel som rättas är inte längre ett citat.
# En borttaget-rad på någon av de bara strängarna vore röd för innehåll
# rundan har beslutat att behålla. Stämplarna bevakas i stället av
# test_geminis_cover_and_closing_carry_the_rounds_date.

# Task 5 — datumstämplarna (`714ba0f`)
G01 | en | October 2026 | aktiv
G02 | en | Johan Lindström, April 2026 | borttaget
# G02 får ingen aktiv-rad: den nya signaturen står bara i PRINT
# (avslutningssidan, EP:1617) och har ingen motsvarighet på webbytan, så
# en aktiv-rad vore `saknas_på_en_yta` från första sekunden. Den bevakas
# av leveransvakten, som läser PDF:en.

# Task 5 — namnbytet NotebookLM → Gemini Notebook (G49, `025fb45`),
# rundans största ändring: 94 → 1 förekomst på EW, 97 → 1 på EP. Den enda
# kvarvarande är Bells avsnittstitel. Raderna fångar namnbytet via FRASER
# ur guidens egen röst, aldrig via det bara produktnamnet.
G49 | en | Gemini Notebook | aktiv
G49 | en | notebooklm.google.com | borttaget
G49 | en | Gemini and NotebookLM are tools. You are the teacher. | borttaget
G49 | en | Gemini and Gemini Notebook are tools. You are the teacher. | aktiv
G49 | en | support.google.com/gemininotebook | aktiv

# Task 6 — huvudflödets juridikpassage, ersatt av jurisdiktionsrutan
# (`6d4958b`), OCH Del 3:s två artikelled
G33 | en | a European regulation | borttaget
G33 | en | records of processing | borttaget
G33 | en | own record of which personal data these tools process | aktiv
G34 | en | carrying GDPR risk | borttaget
G34 | en | data-protection risk that belongs with your organisation | aktiv
G29 | en | Sweden is a notable example | borttaget
G23 | en | Data residency, GDPR, and national context | borttaget
G23 | en | Standard GDPR discipline | borttaget
G23 | en | Every EU member state has one | borttaget
G23 | en | Readers outside the EU should verify the privacy framework | borttaget
G23 | en | What depends on where you are | aktiv

# Task 7 — bonuskapitlet (`b7fe693`, `b5a0e1d`)
# G13: påståendet att NotebookLM Enterprise på Google Cloud ger
# EU-residens är borta i sin helhet — produkten heter inte så längre och
# residensen var obelagd. Aktiv-raden är den formulering som ersatte den.
G13 | en | NotebookLM Enterprise | borttaget
G13 | en | Data residency commitments are not always clearly documented | aktiv
G24 | en | GDPR fundamentals | borttaget
G24 | en | Article 6(1)(e) | borttaget
G24 | en | Article 30 | borttaget
# `Article 30`-raden ovan täcker ÄVEN bonuskapitlets RoPA-checklistpunkt
# ("Our records of processing (Article 30) reflect routine AI use"), som
# Task 7 bytte mot Article 4-kadensen. Se semantikregel 1: en egen rad på
# den längre punkten hade varit strikt svagare, inte extra skydd.
G25 | en | phases in through 2026 and beyond | borttaget
G25 | en | became applicable on 2 August 2026 | aktiv
G26 | en | Limited risk | borttaget
G26 | en | minimal-risk tier | borttaget
# G26: "Prohibited" med stor bokstav står i dag noll gånger på båda
# ytorna (Task 7 döpte om den kommenterade pyramiden, så den falska
# tryggheten i `_TAG`-sväljningen är borta). "The prohibited practices"
# och "required, allowed, prohibited" är legitima gemena förekomster;
# surfacecheck.normalise gör ingen gemenkonvertering, så raden är säker i
# dag — men den är inte säker mot en framtida skiftlägesokänslig svep.
G26 | en | Prohibited | borttaget
G26 | en | Minimal or no risk | aktiv
G26 | en | Transparency risk | aktiv
G26 | en | Unacceptable risk | aktiv
# G48 — rundans mest skadliga fel, och det enda av AI Act-felen som utan
# de här raderna kunde skrivas tillbaka av ett senare städsvep.
# Meningen sa att högriskskyldigheterna gäller sedan 2 augusti 2026;
# bilaga III-högrisk, som uttryckligen omfattar utbildning, gäller från
# 2 december 2027.
G48 | en | most high-risk obligations take effect | borttaget
G48 | en | general applicability begins, transparency rules apply | borttaget
G48 | en | 2 December 2027 | aktiv
G48 | en | Annex III uses that cover education apply from 2 December 2027 | aktiv
# G27: Artikel 4-datumet stod rätt men i en mening som blandade in
# högriskfelet. Den omskrivna fyradatumsmeningen får sin egen rad.
G27 | en | On 2 February 2025, the prohibited practices took effect | borttaget
G27 | en | The prohibited practices and the AI literacy obligations in Article 4 have applied since 2 February 2025 | aktiv

# Task 8 — inramningen generaliserad (`38a646c`)
G22 | en | Swedish and other EU languages | borttaget
G28 | en | Swedish schools | borttaget
G28 | en | Sweden, as of April 2026 | borttaget
G28 | en | yet issued detailed national guidance | aktiv
# G29 står under Task 6 ovan: dess mening ligger i den passage Task 6
# ersätter, inte i Task 8:s två jurisdiktionsexempel.
# G21: praktikexemplet STANNAR, och de två aktiv-raderna är det som
# hindrar ett senare städarsvep från att ta bort det utan att något
# blir rött. Motiveringen står i posten.
G21 | en | Fristadsskolan | aktiv
G21 | en | Pedagog Eskilstuna | aktiv

# Task 9 — licensomläggningen (G12, G14; `85bf305`, `1da9016`).
# Teaching & Learning-tillägget och Education Plus STÅR KVAR på båda
# ytorna med avsikt — de buntar Gemini Notebooks utökade gränser. En
# borttaget-rad på deras namn vore röd. Det som är struket är den gamla
# INRAMNINGEN: två licensvägar som gav premium-Gemini-i-Workspace utan
# extra kostnad, under rubriken "The Gemini for Education license".
G12 | en | Two relevant licensing paths exist | borttaget
G12 | en | Google now sells that as a paid add-on to your Workspace edition, called Google AI Pro for Education | aktiv
G12 | en | Gemini for Education itself is included at no cost | aktiv
G14 | en | The Gemini for Education license | borttaget
G14 | en | What is free, and what you pay for | aktiv

# Task 9 — modell- och versionsnamnen ut ur brödtexten (G37, G38;
# `1b32062`)
G37 | en | It runs on the Gemini 3 Pro backbone | borttaget
G37 | en | Gemini 3 Pro with Deep Think | borttaget
G37 | en | Gemini 3 Deep Think, Google's enhanced reasoning mode | aktiv
G38 | en | Nano Banana Pro as the default image generator | borttaget
G38 | en | it replaced Nano Banana Pro across the Fast, Thinking, and Pro models | aktiv

# Task 9 — åldersgolven (G16; `1da9016`). De tre förbudsraderna är de tre
# gamla golv som rättades; de två aktiv-raderna är de belagda som ersatte
# dem.
G16 | en | Gemini Live is 18+ only | borttaget
G16 | en | NotebookLM is available to users 13+ in a browser | borttaget
G16 | en | Teen Gemini (13+) | borttaget
G16 | en | 13 or over (or the applicable age in your country) | aktiv
G16 | en | above the age of consent in their country | aktiv

# Task 9 — de obelagda citaten ut, de belagda in (G20, G43, G44;
# `2b88167`). Ett citat som rättas är inte längre ett citat, så de
# belagda ersättningarna får varsin aktiv-rad.
G20 | en | a personal tutor that only knows what you teach | borttaget
G43 | en | a generic AI tool cannot understand | borttaget
G43 | en | You cannot expect a generic tool to understand the nuances | aktiv
G44 | en | Kasey Bell frames the shift well | borttaget
G44 | en | Kasey Bell named the shift in the title | aktiv

# Task 9 — antalet Gems (G45; `2b88167`). Siffran var obelagd och står nu
# ingenstans. Båda förbudsraderna behövs: de två meningarna står i olika
# delar och ett svep kunde återställa den ena utan den andra.
G45 | en | roughly 200 ready-to-use Gems | borttaget
G45 | en | around 200 free education Gems | borttaget
G45 | en | a free, growing library of ready-to-use Gems | aktiv

# Task 9 — BETT-attributionen (G35; `1da9016`) och landlistan (G36;
# `2b88167`)
G35 | en | confirmed at BETT 2026 | borttaget
G36 | en | As of BETT 2026 | borttaget
G36 | en | began rolling out in May 2026 | aktiv
G36 | en | eight countries, and the list is growing | aktiv

# Task 9 — Audio Overview-konflikten REFERERAD i stället för förenad
# (G09; koordinatorns ruling, `eac0163`). Första passet förenade Googles
# två motstridiga sidor på sin egen tolkning och blev avvisat: de ska
# refereras båda, med motsägelsen namngiven. Den hedgande meningen ser ut
# som skräp för ett städsvep, och tas den bort återvänder det felaktiga
# exklusivitetsramverket utan att något blir rött. Aktiv-raden är
# hedgens egen slutsats.
G09 | en | The two do not agree; check which route your account actually offers | aktiv

# Task 9 — det interaktiva lägets beta-etikett (G10; `fea3f8d`)
G10 | en | An interactive mode (still in beta) | borttaget
G10 | en | currently in beta | borttaget
G10 | en | available in English only | aktiv

# Task 9 — utrullningsdatumen (G17; `fea3f8d`, `eac0163`). "Rullar ut
# genom 2026" var obelagt och är borta i sin helhet. INGEN aktiv-rad är
# möjlig: det som ersatte påståendet är en generisk hänvisning till
# Admin-konsolen, inte ett nytt datum. En aktiv-rad på den hade bevakat
# brasklappen, inte rättningen.
G17 | en | Granular per-app toggles | borttaget
G17 | en | are rolling out through 2026 | borttaget

# Task 9 — synkens omfång (G03; `fea3f8d`). Själva datumet 8 april 2026
# är belagt och står kvar; fel var omfånget och den obelagda
# panelplaceringen.
G03 | en | anything you create in one surface is visible and editable in the other | borttaget
G03 | en | both surfaces editable | borttaget
G03 | en | sitting between "My stuff" and "Gems" | borttaget
G03 | en | appear in Gemini's navigation | aktiv

# Task 9 — Video Overview-formaten (G11; `fea3f8d`)
G11 | en | The newer Cinematic Video Overview | borttaget
G11 | en | Explainer, Short, and Cinematic | aktiv
G11 | en | Cinematic Video Overviews are 18+ | aktiv

# Task 9 — medlemsstatsresonemanget i åldersrutan (G50; `eac0163`), en
# andra instans av exakt det G28 och G29 var, och den enda i det
# internationella huvudflödet. OBS: "some countries require head-teacher
# approval" står KVAR två gånger per yta och är legitimt — det
# generaliserade resonemanget, inte det EU-skopade. Förbudsraden träffar
# därför medlemsstatsformuleringen.
G50 | en | in several EU member states, national guidance goes further still | borttaget
G50 | en | Local rules can go further than Google's floors | aktiv

# Task 10 — författarens egen inaktuella mening (`346a8c3`)
G31 | en | I have a full-time job | borttaget

# G30: promptmallens platshållare stannar (spec §3) — raden finns för
# att den inte ska städas bort av misstag.
G30 | en | your national school-governance law | aktiv
```
