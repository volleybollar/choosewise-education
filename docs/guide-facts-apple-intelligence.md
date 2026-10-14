# Påståendeinventering — Apple Intelligence-guiden

**Rundan:** Apple Intelligence-guiden. Runda 1 mätte och vaktade; runda 2 (Task 2–12)
skrev om guiden och färdigställer den här inventeringen. Spec:
`docs/superpowers/specs/2026-10-14-apple-intelligence-guide-update-design.md`
**Upprättad:** 2026-10-14
**Faktakontrollerad:** 2026-10-14

Ytorna: **EW** `_unpublished/guides/apple-intelligence/index.html` · **EP**
`_unpublished/exports/apple-intelligence-print-a4-en.html` · **QS**
`_unpublished/exports/apple-intelligence-quick-start-en.html`

QS står utanför ytkonsistensvakten med avsikt — quick-starten har egen, kortare
formulering, och kravet "ordagrant på alla ytor" vore rött från dag ett. Den bevakas i
stället av förekomstkolumnen här och av leveransvakten
(`scripts/tests/test_guide_delivery.py`).

Varje volatilt faktapåstående i de **engelska** ytorna, med alla sina förekomster. De
svenska ytorna ingår inte i rundan och har därför inga poster.

Inventeringen mätte ursprungligen **guiden som den stod 2026-10-14** (runda 1, mät och
vakta) och var inte en beskrivning av den omskrivna guiden. Efter runda 2:s Task 2–11
beskriver den i stället **den omskrivna guiden**: varje post bär fortfarande ett
**verdikt**, men verdiktkolumnen bär nu också vad runda 2 gjorde med posten.

- `står` — verifierat sant mot primärkälla 2026-10-14; ingen ändring behövdes
- `föråldrat` — var sant i april 2026, är det inte längre; cellens text säger vad runda 2 gjorde åt det
- `falskt` — var fel redan då; cellens text säger vad runda 2 gjorde åt det
- `obelagt` — ingen hämtbar primärkälla säger något om påståendet; cellens text säger vad runda 2 gjorde åt det
- `rättat` — ett tidigare `föråldrat`- eller `falskt`-värde är ersatt med ett nytt, källbelagt värde
- `lagt till` — guiden saknade uppgiften helt; den är tillagd i runda 2

Verdikten var runda 2:s arbetsorder och är nu dess facit. Källkolumnen bär
**primärkälla** (apple.com, support.apple.com, security.apple.com, Apples eget
pressmaterial) med hämtdatum; en sekundärkälla räcker aldrig till `står`.

## Hur källorna läses

Varje Apple-sida hämtas som rå HTML och läses ordagrant; texten extraheras lokalt ur
markupen. Där en sidas brödtext inte följer med i konverteringen hämtas den med `curl`
och läses ur HTML:en i stället — det gäller Apples User Guide-sidor, vars innehåll ligger
bakom en navigationsskal som annars är det enda som kommer med. Ingen sida sammanfattas
av ett annat modellanrop som enda belägg, och en sammanfattning är aldrig källa till ett
värde.

**Ett undantag, och det är markerat:** post **A16** behöver veta vad Apples egen sida sa i
**april 2026**, inte bara i dag. Där läses en Wayback-kopia av `support.apple.com`
(capture 2026-04-17) — alltså Apples eget sidinnehåll, arkiverat. Den är markerad
`arkiverad primärkälla` i källkolumnen så att läsaren ser skillnaden. Ingen annan post
vilar på arkivet.

**Leadsen var inte fakta, och ett av dem höll inte.** Kontrollern gav tre spår att pröva.
Mätt mot Apples egna sidor 2026-10-14:

1. **iOS 27 släpptes 14 september 2026** — **belagt.** Apple Newsroom, 2026-09-14.
2. **Assistenten heter Siri AI och är byggd med Google Gemini** — **belagt.** Apple
   Newsroom, ordagrant: "custom-built in collaboration with Google and its Gemini models".
3. **Ett Extensions-system låter användaren välja ChatGPT, Claude eller Gemini** —
   **halvt fel.** Extensions finns och är Apples eget ord (`Settings → Siri → Set Up
   Extensions`), men **ChatGPT är den enda leverantören Apple dokumenterar som valbar
   extension.** Claude och Gemini förekommer i Apples **utvecklar**material, inte i
   användargränssnittet: "Developers can also easily leverage models of their choice, like
   Claude and Gemini, or those from any other provider that implements the new language
   model protocol" (Apple Newsroom 2026-06-08, om ramverk för appbyggare). Att läsa det
   som ett val i Inställningar vore att skriva in ett fel i en omskriven guide. Se **A11**
   och **A17**.

## Ytdivergenser — fem mätta fall utan vaktrad

Vakten kräver att en `aktiv`-rad står **ordagrant på båda** engelska ytorna. Fem mätta
påståenden gör det inte, och får därför ingen rad. De står här i stället, som
observationer runda 2 ärver:

| värde | EW | EP | vad divergensen är |
|---|---|---|---|
| `IMY` | 0 | 1 | EP har ett helt stycke, "A word on the Swedish context", med Integritetsskyddsmyndigheten och dess skolvägledning. EW har inget motsvarande. Printytan bär alltså den enda nationella myndighetsreferensen i hela guiden, och webbläsaren ser den aldrig. Det är den största sakdivergensen mellan ytorna. |
| `Swedish Data Protection Authority (IMY)` | 0 | 1 | samma stycke, hela frasen |
| `Siri & Apple Intelligence → ChatGPT Extension` | 1 | 0 | EW:s FAQ ger en inställningsväg som EP inte ger. Vägen är dessutom föråldrad — se **A30** |
| `Every path to ChatGPT shows a confirmation screen before sending` | 0 | 1 | EP:s uppslag "Where each feature runs" bär en absolut formulering som EW inte har. Den är dessutom falsk — se **A31** |
| `Updated April 2026` / `Johan Lindström, April 2026` | 2 / 0 | 0 / 1 | samma datumstämpel i två olika formuleringar. Den bara ytan de delar är den nakna strängen `April 2026` (3/3), och **den** är vaktens ankare — se **A13** |

**IMY-divergensen (de två första raderna ovan) är löst av Runda 2 Task 4.** EP:s
"A word on the Swedish context"-stycke med Integritetsskyddsmyndigheten är omskrivet till
en nationsneutral ruta ("What depends on where you teach") i samma `processing-callout`-
form som guidens övriga rutor; samma rubrik och poäng finns nu även på EW, som tidigare
helt saknade stycket. Båda ytorna mäter `0` på `IMY` och på frasen
`Swedish Data Protection Authority (IMY)` sedan omskrivningen — se Task 4:s rapport för
exakt ordalydelse på båda ytorna. Raderna står kvar i tabellen som historik över
divergensen som var; de beskriver inte längre guidens nuläge.

## Poster

Förekomstkolumnerna är mätta 2026-10-14 mot vaktens egen normalisering
(`surfacecheck.normalise`), inte mot rå HTML.

| id | påstående i guiden | EW | EP | QS | primärkälla + hämtdatum | verdikt |
|---|---|---|---|---|---|---|
| A01 | `M1 chip or later` — hårdvarugolvet för iPad och Mac | 2 | 1 | — | support.apple.com/en-us/121115 (publ. 2026-09-14) → **200**, ordagrant: "iPad models with M1 or later, Mac with M1 or later"; apple.com/apple-intelligence/ → **200**, enhetslistan: "iPad Pro (M1 and later), iPad Air (M1 and later) … MacBook Air (M1 and later)" — båda lästa 2026-10-14 | **står.** M1-golvet är oförändrat genom tre OS-generationer och är guidens bäst belagda hårdvarupåstående. Notera att Apple numera skriver golvet per modellfamilj, inte som "M1 chip or later" i löptext — ingen sakskillnad |
| A02 | `iPhone 15 Pro` — det lägsta stödda iPhone-steget | 2 | 3 | — | support.apple.com/en-us/121115 → **200**, ordagrant: "iPhone 16 models or later, iPhone 15 Pro, iPhone 15 Pro Max, iPhone Air"; support.apple.com ChatGPT-guiden → **200**, ordagrant: "available on an Apple Intelligence-enabled iPhone 15 Pro, iPhone 15 Pro Max, or iPhone 16 model or later" — lästa 2026-10-14 | **står.** iPhone 15 Pro är fortfarande golvet, och guidens notering att "The standard iPhone 15 is not" stämmer: Apples lista tar bara Pro-modellerna ur 15-serien. Se **A24** för listans övre ände, som däremot inte står |
| A03 | `iPad Pro or iPad Air from 2021` — årtalet på M1-iPadarna | 1 | 1 | — | support.apple.com/en-us/108043 ("Identify your iPad model") → **200**, ordagrant: "iPad Air (5th generation)" — **2022**; support.apple.com/en-us/111887 (iPad Air 5:e gen, tekniska data) → **200**, chip: Apple M1; apple.com/newsroom/2022/03/apple-introduces-the-most-powerful-and-versatile-ipad-air-ever/ → **200** — samtliga lästa 2026-10-14 | **rättat i runda 2 Task 2.** Guiden skriver nu, ordagrant likadant på EW och EP: "an iPad Pro from 2021 onwards, or an iPad Air from 2022 onwards". Bakgrund: M1-iPad Pro kom i april 2021, men M1-iPad Air är iPad Air (5:e generationen) och introducerades i **mars 2022** — Apples egen modellsida daterar den till 2022 och Apples pressmeddelande är från mars 2022. Den gamla formuleringen "iPad Pro or iPad Air from 2021" lade ett år fel på den ena av de två modellerna, och det var inte harmlöst: en skolchef som inventerar fordonsparken efter årtal räknade bort rätt maskiner |
| A04 | `Private Cloud Compute` — mellanskiktet i guidens tre-nivåmodell | 15 | 18 | 1 | apple.com/apple-intelligence/ → **200**, PCC namngivet i funktionslistan; security.apple.com/blog/private-cloud-compute/ → **200** (publ. 2024-06-10); security.apple.com/documentation/private-cloud-compute/ → **200** — lästa 2026-10-14 | **står.** PCC är kvar som namngiven arkitektur, och Apples nyare material bär samma löfte ordagrant: "When Private Cloud Compute is handling users' requests, their personal data is not stored nor made accessible to Apple or anyone else" (Newsroom 2026-09-14). Det är guidens näst mest förekommande värde och det håller. Se **A25** för den europeiska regionuppgiften, som inte gör det |
| A05 | `Writing Tools` — funktionsnamnet | 15 | 19 | 3 | apple.com/apple-intelligence/ → **200**, `Writing Tools` står i funktionslistan 2026-10-14 | **står (öppen EU-fråga).** Namnet är oförändrat. Notera att Apples egna funktionsuppräkning för 27.0 nu också listar "Automatic proofreading" och "Personalized Smart Reply in Mail" som egna rader vid sidan av Writing Tools — guiden beskriver alltså en mindre yta än den som finns, men inget den beskriver har bytt namn. **Öppen fråga, flyttad hit från A06:** DMA-sidan räknar upp "integrated tools for writing" bland det EU-användare på iOS och iPadOS inte får. Om det syftar på guidens `Writing Tools` eller bara på Siri AI:s egen skrivintegration **går inte att avgöra ur den hämtade texten**. Posten bär därför i dag inget EU-förbehåll, och frågan är runda 2:s att avgöra — faller `Writing Tools` under spärren är det guidens mest förekommande funktionsnamn (34 förekomster) som behöver ett. Se **A06** för hela resonemanget |
| A06 | `Visual Intelligence` — funktionsnamnet | 9 | 14 | 1 | apple.com/apple-intelligence/ → **200**, `Visual Intelligence` står i funktionslistan; Apple Newsroom 2026-06-08 → **200**, Visual Intelligence beskrivs som integrerad "across platforms with Siri AI"; apple.com/newsroom/2026/06/due-to-dma-siri-ai-delayed-in-eu-for-ios-27-and-ipados-27/ → **200** (curl), ordagrant: "users in the EU will not have access to Siri AI and its advanced capabilities — including the new dedicated app to revisit conversations, **an expanded Visual Intelligence experience**, integrated tools for writing, Siri mode in Camera on iOS, and other Siri AI capabilities announced at WWDC26" — samtliga lästa 2026-10-14 | **står (EU-förbehåll saknas)** på namnet — funktionen finns kvar och heter samma sak. **Men EU-delen är inte obelagd, den är belagd mot guiden:** DMA-sidan räknar ordagrant upp "an expanded Visual Intelligence experience" bland det EU-användare på iOS och iPadOS **inte** får. Guiden ger Visual Intelligence fyra klassrumsexempel och en kameradriven arbetsgång på iPad utan något EU-förbehåll, och Apple har skrivit ut svaret. Vad som är oklart — och det är en avgränsningsfråga, inte en källfråga — är hur mycket av den *grundläggande* Visual Intelligence som fanns före Siri AI som står kvar för en EU-användare; Apple spärrar det "expanded" lagret och säger inget om basfunktionen. **Runda 2 ska avgöra:** bär guidens Visual Intelligence-avsnitt bas- eller det expanderade lagret? Fyra exempel av fem läser som bas (översätt, identifiera, sammanfatta en skylt), vilket talar för att avsnittet mest står kvar — men det måste bära ett EU-förbehåll, inte inget. **Öppen fråga som rör A05:** samma Apple-mening räknar också upp "integrated tools for writing". Om det syftar på guidens `Writing Tools` (A05, verdikt `står`, 34 förekomster) eller bara på Siri AI:s egen skrivintegration **går inte att avgöra ur den hämtade texten**, och A05 bär därför i dag inget EU-förbehåll alls. Frågan är runda 2:s att avgöra och får inte tystas: faller `Writing Tools` under spärren är det guidens mest förekommande funktionsnamn som behöver ett förbehåll |
| A07 | `Mail categorisation` — funktionen och dess fyra kategorier | 9 | 10 | 1 | support.apple.com/guide/iphone/use-categories-iphfe4a36baf/ios → **200**, ordagrant: "Primary: Find personal messages and time-sensitive information. Transactions: Keep track of your confirmations, receipts, and shipping notices. Updates: Catch up on news, newsletters, and social updates. Promotions: Browse your coupon and sales emails." — läst 2026-10-14 | **står (delvis obelagt)** på sak: funktionen finns och de fyra kategorierna heter exakt vad guiden säger (`Primary, Transactions, Updates, and Promotions`, EW 1 / EP 1). Två noteringar. **Apples eget ord är "categories" / "categorize"** — sidans rubrik är "Automatically categorize incoming emails in Mail"; "Mail categorisation" är guidens brittiska substantivering, inte ett Apple-produktnamn. Och **obelagt: "Entirely on-device … no email content is sent to Apple servers".** Apples sida säger ingenting om var kategoriseringen körs, och nämner inte Apple Intelligence som krav; den enda inskränkning den skriver är "(not available in all countries or regions)". Guiden kallar detta "one of the features with the cleanest privacy profile in the entire Apple Intelligence suite" — det är en slutsats utan hämtbart belägg, i ett kapitel som handlar om DPIA. Se **A21** för inställningsvägen |
| A08 | `Image Playground` — funktionsnamnet | 1 | 3 | — | apple.com/apple-intelligence/ → **200**, `Image Playground` i funktionslistan; support.apple.com/en-us/121115 → **200**, ordagrant: "Reimagined Image Playground" — lästa 2026-10-14 | **står** på namnet. Apple kallar den i dag "the reimagined Image Playground" och listar den bland de funktioner som uttryckligen **är** tillgängliga i EU. Se **A22** — stilpåståendet står inte |
| A09 | `Genmoji` — funktionsnamnet | 1 | 3 | — | apple.com/apple-intelligence/ → **200**, `Genmoji` i funktionslistan; Apple Newsroom 2026-06-08 → **200**, Genmoji beskrivs med kvalitetsförbättringar där användaren kan "describe the changes they want to make" — lästa 2026-10-14 | **står.** Namnet och funktionen är oförändrade; det guiden skriver om låg klassrumsnytta är ett omdöme, inte ett faktapåstående, och faller utanför inventeringen |
| A10 | `Siri 2.0` — namnet på assistenten | 3 | 7 | 1 | apple.com/apple-intelligence/ → **200**: "Introducing Siri AI. Truly helpful. Truly yours."; apple.com/newsroom/2026/09/siri-ai-a-profoundly-more-capable-and-personal-assistant-is-here/ → **200** (2026-09-14); support.apple.com/en-us/127893 → **200** (publ. 2026-09-22): "Siri AI (Beta) … an entirely new version of Siri powered by the next generation of Apple Intelligence"; support.apple.com/en-us/121115 → **200**: "Apple Intelligence also powers an entirely new version of Siri: Siri AI." — samtliga lästa 2026-10-14. `grep -i "Siri 2.0"` ger **noll** träffar i den hämtade HTML:en från alla fyra sidorna | **falskt: Apple har inte och har aldrig haft en produkt som heter `Siri 2.0`.** Apple versionsnumrerar inte Siri. Fyra hämtade Apple-sidor namnger assistenten, och ingen av dem använder strängen; namnet i dag är **Siri AI**, släppt 14 september 2026 med 27.0-generationen. `Siri 2.0` är en sekundärkällas kortform som guiden lyft in som om den vore ett produktnamn, och den står på tio ställen i de engelska ytorna plus en gång i quick-starten — den näst dyraste rättelsen i runda 2 efter **A15**. Rätt värde: `Siri AI`, med reservationen att den är i beta och att EU-läget gör namnet värdelöst för en svensk läsare utan den uppgiften intill |
| A11 | `ChatGPT` — och inramningen att ChatGPT är den enda externa vägen | 27 | 39 | 1 | support.apple.com/guide/iphone/use-chatgpt-with-apple-intelligence-iph00fd3c8c2/ios → **200**, ordagrant: "You can allow Apple Intelligence to work with ChatGPT from OpenAI" och "If you're using Siri AI (Beta), tap Set Up Extensions, tap ChatGPT, then turn on Use Extension"; `grep -i "Gemini\|Claude\|Anthropic"` på samma hämtade sida ger **noll** träffar — läst 2026-10-14 | **står** på exklusiviteten, mot förväntan. ChatGPT finns kvar, är fortfarande opt-in, och är **den enda leverantör Apple dokumenterar som valbar extension** — Apples egen Extensions-sida nämner varken Claude, Gemini eller Anthropic. Kontrollerns lead om ett treval i Inställningar är alltså inte belagt; Claude och Gemini hör till Apples utvecklarramverk (se huvudet, lead 3). **Men inramningen håller ändå inte**, av ett annat skäl än det förväntade: se **A17**. Att 39 EP-förekomster hänger på rätt sida av den skillnaden är vad som gör posten dyr |
| A12 | `OpenAI` — motparten i ChatGPT-vägen | 12 | 11 | 1 | support.apple.com ChatGPT-guiden → **200**, ordagrant: "ChatGPT from OpenAI" och "For more information, see OpenAI Terms of Use"; "The ChatGPT extension is available only in regions where the ChatGPT app and service are available. Refer to OpenAI for ChatGPT availability." — läst 2026-10-14 | **står.** OpenAI är fortfarande motparten, Apple hänvisar fortfarande till OpenAI:s egna villkor för just den vägen, och guidens GDPR-resonemang om en tredjepartsmottagare utanför Apples DPA har alltså kvar sin grund. Åldersgränsen i samma stycke har den inte — se **A16** |
| A13 | `April 2026` — datumstämpeln, i tre förekomster per yta | 3 | 3 | — | ytorna själva, mätta 2026-10-14; iOS 27-släppet 2026-09-14 (Apple Newsroom → **200**) | **rättat i runda 2 Task 11.** Stämpeln är satt om till `October 2026` på båda ytorna, i samma tre förekomster (omslaget/hero, löptexten om hårdvarugolvet, avslutningens signatur) och i samma commit som sakändringarna i Task 2–10 redan gjort — ingen av de tre formuleringarna är omskriven, bara den nakna strängen. Alla tre A-text-föregångare (Siri AI, EU-spärren, lagringstaket, hårdvarulistan) som gjorde den gamla stämpeln `föråldrat` är rättade av tidigare uppgifter i den här rundan; stämpeln följer nu efter, inte före |
| A14 | `Data Protection Impact Assessment` — den juridiska termen | 1 | 1 | — | ingen Apple-hämtning behövs eller gjord; termen är GDPR artikel 35 och inte ett produktpåstående | **står.** Juridisk term, inte Apple-fakta, och oförändrad. Raden finns i vaktblocket för att termen inte ska städas bort av misstag när kapitlet skrivs om |
| A15 | `Siri 2.0's fully localised voice responses` — och löftet att svensk Siri "keep[s] improving through 2026" | 1 | 1 | — | apple.com/newsroom/2026/06/due-to-dma-siri-ai-delayed-in-eu-for-ios-27-and-ipados-27/ → **200**, ordagrant: "users in the EU will not have access to Siri AI" på "iOS 27 and iPadOS 27" och watchOS 27, medan "EU users will be able to access Siri AI on macOS 27 and visionOS 27", och "there is currently no timeline for Siri AI's availability in the EU on iOS and iPadOS"; Apple Newsroom 2026-09-14 → **200**: "Siri AI will not be available initially in the EU on iOS, iPadOS, and watchOS. Features that rely on Siri AI will also not be available in the EU."; support.apple.com ChatGPT-guiden → **200**: "Available in English to start. Siri AI will not initially be available in the EU on iOS."; apple.com/newsroom/2026/09/major-updates-for-apples-software-platforms-are-now-available/ → **200**, ordagrant: "Siri AI is now rolling out as a beta in English, with support for French, Japanese, Korean, Portuguese, and Spanish coming in October." — samtliga lästa 2026-10-14 | **föråldrat, och det är rundans viktigaste fynd.** Guiden ger en svensk lärare ett vänteläge: funktionen finns, svenskan blir bättre under 2026. Verkligheten sedan 14 september 2026 är att Siri AI **inte finns alls** på iOS och iPadOS i EU, att Apple anger DMA som skäl, att det inte finns någon tidplan, och att Siri AI dessutom börjar på **engelska**. **Svenska står inte i Apples namngivna språkvåg heller:** oktoberlistan är franska, japanska, koreanska, portugisiska och spanska. Guiden lovar alltså förbättrad svensk Siri på en tidslinje där Apple varken har lovat svenska eller EU-tillgång. Guidens hela Del 2 §2 — fem klassrumsexempel på en iPad — beskriver en funktion en svensk lärare med en skol-iPad inte kan få. Och eftersom Apple skriver "Features that rely on Siri AI will also not be available in the EU" sprider spärren sig till varje funktion guiden hänger på Siri. Att en guide för svenska skolor saknar den uppgiften är mer läsarskadligt än något enskilt felaktigt årtal i tabellen. Ankaret `Siri 2.0's fully localised voice responses` bär posten eftersom det är den enda meningsdel där båda ytorna lovar samma sak ordagrant |
| A16 | `requires the user to be 18 or over` — åldersgränsen för ChatGPT-vägen | 1 | 1 | — | support.apple.com/guide/iphone/use-chatgpt-with-apple-intelligence-iph00fd3c8c2/ios → **200**, ordagrant 2026-10-14: "Note: You must be at least 13 years old or the minimum age required in your country to consent to use ChatGPT." — och **arkiverad primärkälla**: samma Apple-sida, Wayback-capture **2026-04-17**, ordagrant samma mening: "You must be at least 13 years old or the minimum age required in your country to consent to use ChatGPT." | **falskt — och falskt redan i april 2026.** Apple har satt gränsen vid **13 år** (eller landets minimiålder), inte 18, både i dag och i en arkiverad kopia från två dagar efter guidens stämpelmånads mitt. Det är det enda stället där inventeringen går till arkivet, just för att skilja `falskt` från `föråldrat`, och skillnaden spelar roll: `föråldrat` hade betytt "Apple har sänkt gränsen", vilket inte hänt. Felet går åt den farliga riktningen — guiden säger till en skolledare att ChatGPT-vägen är vuxenspärrad och att åldern därför sköter sig själv, när Apples egen spärr släpper in en trettonåring. Det underminerar guidens egen slutsats i Del 3, som är rätt av fel skäl: ChatGPT-integrationen ska stängas av på skol-iPads, men därför att den inte är åldersspärrad på ett sätt som skyddar en elev, inte därför att den är |
| A17 | `three distinct places your request can be processed` — guidens tre-nivåmodell (on-device / PCC / ChatGPT) | 1 | 1 | — | apple.com/newsroom/2026/09/siri-ai-a-profoundly-more-capable-and-personal-assistant-is-here/ → **200**, ordagrant: Siri AI är "custom-built in collaboration with Google and its Gemini models for deeply integrated Apple Intelligence experiences"; apple.com/newsroom/2026/06/apple-intelligence-brings-powerful-ai-capabilities-into-everyday-experiences/ → **200** (2026-06-08), samma formulering: "custom-built in collaboration with Google and its Gemini models" — lästa 2026-10-14 | **föråldrat.** Modellen är guidens pedagogiska ryggrad och den kan inte längre uttrycka systemet. Google och dess Gemini-modeller är enligt Apples eget pressmaterial med i att bygga själva assistenten — alltså inne i nivå 1 och 2, inte som en fjärde opt-in-nivå vid sidan av ChatGPT. Guidens tre nivåer låter en läsare dra slutsatsen att den enda externa parten är den man själv knackar på, och det är inte längre sant. Notera att detta **inte** är leadets Extensions-påstående: det är en annan och allvarligare sak. En rättelse måste namnge Google som Apples samarbetspartner för Siri AI och hålla den skild från ChatGPT-extensionen, som fortfarande är opt-in och fortfarande är OpenAI:s (se **A11**, **A12**) |
| A18 | `always shows a confirmation screen before sending` — bekräftelsesteget i ChatGPT-vägen | 1 | 1 | — | support.apple.com/guide/iphone/use-chatgpt-with-apple-intelligence-iph00fd3c8c2/ios → **200**, ordagrant, under rubriken "Send requests to ChatGPT without confirming": "You can choose to let Siri send requests to ChatGPT automatically without asking. Go to the Settings app on your iPhone. Tap Siri. Below Extensions, tap ChatGPT. Turn off Confirm Requests." — läst 2026-10-14. **Arkiverad primärkälla för aprilläget:** samma Apple-sida, Wayback-capture **2026-04-17**, bär samma avstängning ordagrant — rubriken "Send requests to ChatGPT without confirming" och inställningen "Turn off Confirm ChatGPT Requests" (Apple har sedan kortat namnet till `Confirm Requests`) | **falskt — och falskt redan i april 2026.** Avstängningen fanns i Apples egen dokumentation när guiden stämplades; bara inställningens namn har kortats sedan dess. Det är därför `falskt` och inte `föråldrat`: Apple har inte *tagit bort* ett garanterat bekräftelsesteg, det har aldrig varit garanterat. Apple dokumenterar en egen inställning, `Confirm Requests`, vars hela syfte är att ta bort bekräftelsesteget: med den av skickar Siri förfrågningar till ChatGPT **utan att fråga**. Guidens absoluta formuleringar — "always shows a confirmation screen", "nothing is forwarded without the user accepting it" (1/1), "Anything that touches ChatGPT … requires an explicit tap" — är därmed inte sanna som generell utsaga, utan bara som beskrivning av standardläget. Det är ett fel i guidens mest integritetskritiska stycke: en skolledare som läser att samtycket är arkitektoniskt garanterat ser ingen anledning att låsa inställningen via MDM. Apple tillägger att just den avstängningen **inte** är möjlig under Siri AI ("This option isn't available if you're using Siri AI"), vilket gör rätt värde tvådelat och beroende av vilken Siri enheten kör — och på iOS i EU är det inte Siri AI (se **A15**) |
| A19 | `roughly 4 GB on-device model` — nedladdningens och diskutrymmets storlek | 1 | 1 | — | support.apple.com/en-us/121115 → **200** (publ. 2026-09-14), ordagrant: "Up to 14 GB of storage on device for iPhone 17 Pro, iPhone 17 Pro Max, iPhone Air, iPad models with M4 and later and at least 12GB of unified memory, Mac models with M3 and later and at least 12GB of unified memory, and Apple Vision Pro (M5)" och "Up to 8 GB of storage for other Apple Intelligence-enabled iPhone, iPad, Mac, and Apple Vision Pro models" — läst 2026-10-14 | **rättat i runda 2 Task 2, omrättat i Fixrunda 1.** Guiden skriver nu, ordagrant likadant på EW och EP: "up to 8 GB on most supported iPads, or up to 14 GB on iPad models with M4 or later and at least 12 GB of unified memory" (iPad-stycket), "up to 8 GB of free disk space on most supported Macs, or up to 14 GB on Mac models with M3 or later and at least 12 GB of unified memory" (Mac-stycket) och "up to 8 GB on most models, or up to 14 GB on iPhone 17 Pro, iPhone 17 Pro Max, and iPhone Air" (iPhone-stycket) — Apples egen tvådelade tak-formulering, inte ett intervall. Fixrunda 1: Task 2:s första lagning skrev "8 to 14 GB … depending on your hardware", vilket granskningen fångade som **Critical** — "Up to 8 GB" / "Up to 14 GB" är båda tak, och "8 to 14 GB" läses som ett golv (minst 8 GB), fel i samma riktning som det ursprungliga felet. Lagat genom att citera Apples två tak explicit, med de modeller som skiljer dem åt, i stället för att komprimera till ett intervall. Bakgrund: den allra första siffran 4 GB hade fördubblats till fyrdubblats mot Apples egna "Up to 8 GB … Up to 14 GB" (källa i kolumnen till vänster). Guiden gav den tre gånger per yta i tre formuleringar — `roughly 4 GB on-device model` (1/1), `about 4 GB of free disk space` (1/1), `the same 4 GB footprint` (1/1) — och byggde en praktisk instruktion på den ("thirty to sixty minutes" på skol-WiFi). En IT-ansvarig som planerade en utrullning efter 4 GB per enhet planerade fel med minst en faktor två |
| A20 | `Settings → Notifications → Summarise Previews` — inställningsvägen för notissammanfattningar | 2 | 2 | — | support.apple.com/guide/iphone/summarize-notifications-reduce-interruptions-iph1fbe7d2b9/ios → **200**, ordagrant: "Go to the Settings app on your iPhone. Tap Notifications. Tap Summarize Notifications, turn on Summarize Notifications, then tap Choose Notifications to Summarize."; `grep -i "Summarise Previews\|Summarize Previews"` på den hämtade sidan ger **noll** träffar — läst 2026-10-14. **Arkiverad primärkälla för aprilläget:** samma Apple-sida, Wayback-capture **2026-04-17** — `Summarize Notifications` står där 4 gånger som inställningsnamn, och `Summarize Previews` / `Summarise Previews` ger **noll** träffar även i aprilkopian | **falskt — och falskt redan i april 2026.** Apples inställning heter `Summarize Notifications`, med undermenyn `Choose Notifications to Summarize`, och den hette så redan när guiden stämplades. Guiden ger alltså en väg som aldrig har funnits, två gånger per yta. En lärare som följer instruktionen hittar ingen sådan post. *(Ett tidigare utkast av den här cellen förklarade felet som en sammanblandning med inställningen `Show Previews`. Den förklaringen är struken: strängen ger **noll** träffar på både dagens och aprils version av Apples sida, och en obelagd förklaring av ett belagt fel hör inte i en inventering. Felets ursprung är okänt; att vägen inte finns är mätt.)* |
| A21 | `Settings → Mail → Categorisation` — inställningsvägen för att stänga av Mail-kategorier | 2 | 2 | — | support.apple.com/guide/iphone/use-categories-iphfe4a36baf/ios → **200**, ordagrant under "Turn off categories": "Go to the Mail app on your iPhone. In an inbox, tap at the top of the screen, then choose List View." — läst 2026-10-14 | **föråldrat.** Avstängningen bor inte i Inställningar utan i Mail-appen själv, och läget heter `List View`, inte "the flat-list view". Guiden ger vägen två gånger per yta, en gång i Del 2 och en gång i FAQ:n, och FAQ-förekomsten bär dessutom guidens rekommenderade utrullningsprofil ("Mail categorisation off") — alltså en konfigurationsrekommendation med en väg som inte går att följa |
| A22 | `three visual styles` — Image Playgrounds stilutbud (`Animation, Illustration, and Sketch`, 1/1) | 1 | 1 | — | support.apple.com/en-us/121115 → **200**, ordagrant: "generating images in virtually any style" och "Reimagined Image Playground"; support.apple.com/guide/iphone/create-original-images-iph0063238b5/ios (iOS 27) → **200**, ordagrant: "Choose a style: Tap the Style button, then choose an Apple Intelligence style (like **Any Style or Illustration**) or tap **ChatGPT** to describe the style you want" och "If you choose Any Style, you can describe the style you want as part of your image description" — lästa 2026-10-14 | **föråldrat: utbudet är inte längre tre, och det är inte längre en sluten lista.** Apples egen iOS 27-sida namnger `Any Style` och `Illustration` som exempel, lägger till ett fritextläge där användaren beskriver stilen själv, och ger **ChatGPT som eget stilval inne i Image Playground**. `Animation` och `Sketch` namnges inte på sidan. Två konsekvenser för runda 2. Ordet `three` är fel, och `virtually any style` med fotorealism har en annan riskprofil i ett klassrum än tre tydligt stiliserade lägen — guidens avfärdande av funktionen som "narrow" klassrumsrelevans vilar på det gamla utbudet. Och **ChatGPT-vägen in i Image Playground finns inte i guiden**: EP:s snabbreferens placerar Image Playground under "Private Cloud Compute by default" utan någon ChatGPT-väg, vilket är precis den sorts tyst tredjepartsöverföring guidens Del 3 är skriven för att fånga |
| A23 | `support.apple.com/apple-intelligence` — den URL guiden skickar läsaren till för hjälp | 1 | 1 | — | `curl -sL` mot `https://support.apple.com/apple-intelligence` → **404**, mätt 2026-10-14. Kontrollhämtningar samma dag: `https://support.apple.com/en-us/121115` → **200**, `https://security.apple.com/` → **200**, `https://www.apple.com/apple-intelligence/` → **200**. **Arkivbelägg för aprilläget:** Wayback CDX-sökning på `support.apple.com/apple-intelligence` för 2025–2026 ger **noll captures** — ingen arkivrobot har någonsin fått ett svar värt att spara från den adressen | **rättat i runda 2 Task 2.** Guiden pekar nu på `support.apple.com/en-us/121115`, ordagrant likadant på EW och EP, i stället för den döda adressen. Bakgrund: Arkivet har inte en enda capture av den gamla URL:en under två år, vilket är vad man ser av en adress som aldrig har svarat; jämför att samma arkiv har aprilkopior av de tre andra Apple-sidor inventeringen hämtar. Det var därför `falskt` och inte `föråldrat`: länken hade inte ruttnat, den hade aldrig fungerat. Guidens avsnitt "Where do I get help if something goes wrong?" inledde med en Apple-URL som inte svarade. Den stod en gång per yta, i den sektion läsaren söker upp när något gått fel, och var den enda posten i inventeringen där felet mättes med en statuskod i stället för läst som text. Ersättaren är hämtad med 200 samma dag som mätningen: `support.apple.com/en-us/121115` för systemkrav och tillgänglighet; `security.apple.com` för PCC-arkitekturen rörs inte (den stod redan rätt — se **A26**) |
| A24 | `the full iPhone 16 and 17 lines are supported` — listans övre ände | 1 | 1 | — | support.apple.com/en-us/121115 → **200** (publ. 2026-09-14): "iPhone 16 models or later, iPhone 15 Pro, iPhone 15 Pro Max, iPhone Air, iPad mini (A17 Pro), MacBook Neo (A18 Pro), iPad models with M1 or later, Mac with M1 or later"; apple.com/apple-intelligence/ → **200**, enhetslistan ordagrant: "iPhone Duo (A20 Pro), iPhone 18 Pro Max (A20 Pro), iPhone 18 Pro (A20 Pro), iPhone 17 Pro Max (A19 Pro), iPhone 17 Pro (A19 Pro), iPhone Air (A19 Pro), iPhone 17 (A19), iPhone 17e (A19), iPhone 16 Pro Max (A18 Pro) …" — lästa 2026-10-14 | **rättat i runda 2 Task 2.** Guiden skriver nu, ordagrant likadant på EW och EP: "only iPhone 16 models or later, iPhone 15 Pro, iPhone 15 Pro Max, and iPhone Air are supported" — Apples egen formulering "iPhone 16 models or later" föråldras inte på samma sätt som en uppräkning av enskilda linjer. Bakgrund: den gamla listan slutade två hårdvarugenerationer för tidigt. Apples egen uppräkning 2026-10-14 bar `iPhone 18 Pro`, `iPhone 18 Pro Max`, `iPhone Duo`, `iPhone Air`, `iPhone 17e` och `iPhone 16e` utöver guidens två linjer, plus `MacBook Neo (A18 Pro)` på Mac-sidan — en Mac som inte är Apple-silicon i guidens mening ("any machine with Apple-silicon (M1 or later)") utan bär ett A-serie-chip, vilket gjorde guidens Mac-regel otillräcklig som urskiljning. Till skillnad från **A03** var detta inget sakfel i april 2026; det var en lista som inte hölls uppdaterad |
| A25 | `Apple operates PCC regions in Europe` | 1 | 1 | — | security.apple.com/blog/private-cloud-compute/ → **200** (publ. 2024-06-10), läst ordagrant 2026-10-14 — **ingen geografisk uppgift över huvud taget** på sidan; security.apple.com/documentation/private-cloud-compute/ → **200**; support.apple.com/en-us/121115 → **200** — ingen av dem nämner PCC-regioner eller Europa | **obelagt.** Tre hämtade Apple-sidor om PCC och tillgänglighet säger ingenting om var PCC-noderna står. Guiden hedgar redan själv i samma mening ("verify current regional availability with your procurement contact before relying on it in a DPIA"), och hedgen är rätt instinkt — men påståendet som hedgas har ingen hämtbar källa, och det står i det kapitel som ska bära en DPIA. En uppgift om dataresidens som inte går att belägga ska inte stå med siffra eller världsdel. Det här är samma klass av fel som Gemini-inventeringens **G13** |
| A26 | `The full technical whitepaper sits at security.apple.com` — och `a technical whitepaper on the PCC architecture` (1/1) | 1 | 1 | — | security.apple.com/documentation/private-cloud-compute/ → **200**, mätt 2026-10-14; security.apple.com/blog/private-cloud-compute/ → **200**, publ. 2024-06-10 | **står** på platsangivelsen: `security.apple.com` svarar, och PCC-dokumentationen ligger där. Notera för runda 2 att **blogginlägget självt inte länkar någon whitepaper** — det skriver "The rest of this post is an initial technical overview of Private Cloud Compute, to be followed by a deep dive after PCC becomes available in beta" — så den djupare dokumentationen ligger under `/documentation/private-cloud-compute/`, inte i blogginlägget guiden pekar mot. Guiden hamnar rätt, men på en vagare adress än den kunde ge |
| A27 | `Apple ships Apple Intelligence features monthly` — kadensen bakom rekommendationen om terminsvis genomgång | 1 | 1 | — | apple.com/newsroom/2026/09/major-updates-for-apples-software-platforms-are-now-available/ → **200**, läst ordagrant 2026-10-14: "UPDATE September 14, 2026" och "The new features start rolling out today across iOS 27, iPadOS 27, macOS 27, watchOS 27, visionOS 27, and tvOS 27" — **ingen kadensutfästelse någonstans på sidan**; support.apple.com/en-us/121115 → **200** och Apple Newsroom 2026-06-08 → **200**, inte heller de utfäster en månads- eller kvartalskadens | **obelagt.** Ingen hämtad Apple-sida lovar månatliga funktionssläpp. Vad sidorna faktiskt visar är ett samlat 27.0-släpp den 14 september 2026 med efterföljande vågor — och den enda daterade vågen Apple namnger är språkvågen i **A15**. Påståendet är inte motsagt av någon källa — ingen sida säger "inte månadsvis" — men det bär en rekommendation (terminsvis genomgång av konfigurationen) som är klok oavsett kadens. Rätt skrivning behåller rekommendationen och tar bort frekvensen. Samma gäller den närliggande meningen `Language support has expanded quarterly since launch` (EW 2 / EP 1 på `quarterly`), som ingen hämtad sida belägger |
| A28 | `stateless computation` — Apples term för att förfrågningsdata kastas | 1 | 1 | — | security.apple.com/blog/private-cloud-compute/ → **200**, läst ordagrant 2026-10-14: Apple använder termen "stateless computation" och skriver "Personal data leaves no trace in the PCC system"; sidan bekräftar också att serverprogramvaran görs loggbar och inspekterbar för oberoende forskare | **står.** Både termen och de två egenskaper guiden hänger på den — kastad förfrågningsdata och publicerad, granskningsbar serverbild — är Apples egna formuleringar, och Newsroom 2026-09-14 upprepar löftet för 27.0-generationen. Det är guidens starkaste tekniska avsnitt och det behöver ingen rättelse. Raden finns i vaktblocket för att termen inte ska försvinna när PCC-kapitlet skrivs om |
| A29 | `Summaries are on by default` — notissammanfattningarnas utgångsläge | 1 | 1 | — | support.apple.com/guide/iphone/summarize-notifications-reduce-interruptions-iph1fbe7d2b9/ios → **200**, läst ordagrant 2026-10-14: instruktionen lyder "Tap Summarize Notifications, **turn on** Summarize Notifications, then tap Choose Notifications to Summarize", och sidan har ett eget avsnitt "Turn notification summaries on or off" | **obelagt, och sannolikt fel riktning.** Apples egen instruktion börjar med att användaren slår **på** funktionen och sedan väljer vilka appar som ska omfattas — ingen hämtad sida säger att sammanfattningar är på som standard "for most app categories". Jag skriver `obelagt` och inte `falskt` därför att Apples sida beskriver hur man ställer in funktionen, inte vad utgångsläget är efter en uppdatering; ingen hämtbar sida uttalar sig om defaulten. För en skolutrullning pekar felet ändå åt ett praktiskt håll: guiden säger "To fine-tune …" där Apples flöde säger "turn on" |
| A30 | `Siri & Apple Intelligence → ChatGPT Extension` — inställningsvägen för ChatGPT-spärren | 1 | **0** | — | support.apple.com ChatGPT-guiden → **200**, nuvarande väg ordagrant: "Go to the Settings app on your iPhone. Tap Siri. Tap ChatGPT, tap Set Up …" och, under Siri AI: "tap Set Up Extensions, tap ChatGPT, then turn on Use Extension"; **arkiverad primärkälla** (Wayback-capture 2026-04-17 av samma sida) gav aprilvägen ordagrant: "Tap Apple Intelligence & Siri. Below Extensions, tap ChatGPT, then tap Set Up." | **föråldrat — och EW-exklusivt, alltså ingen vaktrad.** Guidens väg var rätt i april 2026: den arkiverade kopian bekräftar att menyn då hette `Apple Intelligence & Siri` med `Extensions` under sig. I dag är ingången `Settings → Siri`. Två saker för runda 2: ordet **`Extensions` är Apples eget och har varit det hela tiden** — guidens "ChatGPT Extension" är alltså inte en felstavad gissning utan Apples terminologi, vilket gör leadets Extensions-nyhet mindre ny än den såg ut (se huvudet, lead 3) — och vägen står bara på webbytan, så en rättelse som bara träffar EW lämnar EP utan motsvarande instruktion över huvud taget |
| A31 | `Every path to ChatGPT shows a confirmation screen before sending` | **0** | 1 | — | samma källa som **A18**: support.apple.com ChatGPT-guiden → **200**, "Turn off Confirm Requests" — läst 2026-10-14; **samma arkiverade aprilbelägg som A18** (Wayback-capture 2026-04-17: "Send requests to ChatGPT without confirming … Turn off Confirm ChatGPT Requests") | **falskt — falskt redan i april 2026, och EP-exklusivt, alltså ingen vaktrad.** Samma fel som **A18**, men i sin absoluta form ("Every path") och bara på printytan, i uppslaget "Where each feature runs" som är tänkt som guidens snabbreferens. Printläsaren får alltså den starkaste och mest felaktiga formuleringen av guidens integritetslöfte, och webbläsaren får den inte. Att rätta **A18** utan att rätta den här raden lämnar felet kvar i PDF:en |
| A32 | **saknas i guiden:** daglig användningsgräns och kommande betalnivå | 1 | 1 | 0 | support.apple.com/en-us/121115 → **200**, ordagrant 2026-10-14: "Certain Apple Intelligence features that rely on server-side models are subject to daily usage limits, including but not limited to Siri AI, Intelligent Photo Editing Tools, Image Playground, and AFM 3 Cloud models in Shortcuts. Daily limits may vary by feature, request complexity, system demand, system policies, and other factors. **Expanded access to such features will be available for a fee in the future.**" | **lagt till i runda 2 Task 10.** Guiden byggde hela sitt säljargument på att Apple Intelligence är gratis och ingår i enheten — "You do not need to sign into anything new" (den meningen själv är orörd, ligger utanför FAQ:n och alltså utanför Task 10:s sidspann) — och nämnde ingen gräns och ingen avgift. FAQ-svaret "Does my iPad support Apple Intelligence?" bär nu, ordagrant olika men sakligt identiskt per yta, att flera serverburna funktioner (Siri AI, Intelligent Photo Editing Tools, Image Playground, AFM 3 cloud-modeller i Shortcuts) har en daglig användningsgräns, och att Apple har sagt att utökad åtkomst till dem kommer kosta i framtiden, utan angivet datum. Ingen tidplan påstås — bara att en avgiftsnivå är annonserad. Bakgrund: för en skolchef som planerar en utrullning till hundra klassrums-iPads är det en upphandlingsfråga, inte en detalj, och den fanns inte i guiden alls före den här uppgiften |
| A33 | **saknades i guiden:** AI Act-avsnittets tillämplighetsdatum, `2 August 2026` | 1 | 1 | — | `korsref P13` (`docs/guide-facts-claude.md`) — kommissionens ordalydelse "entered into force on 1 August 2024 and became applicable on 2 August 2026". Samma datum redan rättat i Gemini-guiden (G25/G48). Ingen ny hämtning | **lagt till.** I Task 8: avsnittet "A short word on the EU AI Act" fanns inte i guiden före den här uppgiften; det här är det första av avsnittets två AI Act-datum |
| A34 | **saknades i guiden:** Annex III-högriskens startdatum för utbildning, `2 December 2027` | 1 | 2 | — | `korsref P13` — "the rules for high-risk use cases in certain sensitive areas (Annex III) have been extended to 2 December 2027 as a result of … the AI Omnibus". Samma datum i G48 | **lagt till.** I Task 8: Annex III omfattar uttryckligen utbildning (P13, G51 bilaga III punkt 3). EP-förekomsten är 2 därför att avsnittets andra stycke, tillagt i Fixrunda 1, återupprepar datumet ("From 2 December 2027, what a school would carry …") |
| A35 | **saknades i guiden:** de tre korrekta risknivånamnen `Unacceptable risk` / `Transparency risk` / `Minimal or no risk` | 1/1/1 | 1/1/1 | — | `korsref P13` — "The AI Act defines 4 levels of risk for AI systems: Unacceptable risk / High risk / Transparency risk / Minimal or no risk"; samma tre namn redan rättade i Gemini-guiden (G26) | **lagt till.** I Task 8: avsnittet namnger ingen av de tre föråldrade varianterna (`Limited risk`, `Minimal risk`, `Prohibited`) som stod i Gemini-guiden innan G26 rättade dem. `High risk` står också i löptexten men bär ingen egen rad — det är inte ett namn som stått fel i någon syskonguide |
| A36 | **saknades i guiden:** `Article 16` — förhandsplikternas hemvist (leverantörens, inte skolans) | 1 | 1 | — | `korsref G51` (`docs/guide-facts-gemini.md`) — artificialintelligenceact.eu, artikel 16, hämtad ordagrant 2026-10-13 | **lagt till.** I Task 8: avsnittet lägger inga av art. 9–15/17/43/48/49.1 på skolan; de nämns bara som "the provider's" |
| A37 | **saknades i guiden:** artikel 26-listan — driftsättarens plikter (instruktioner, tillsyn, loggar under skolans kontroll, information före driftsättning, underrättelse) | 1 | 1 | — | `korsref G51` — samma källa (artikel 26), hämtad ordagrant 2026-10-13 | **lagt till.** I Task 8, ordagrant G51:s egen tre gånger reviderade formulering: 26.6:s förbehåll ("the logs it controls", inte "the system's logs") och `which includes` i stället för ett kolon som lovar en sluten lista (artikel 26 har sju punkter, avsnittet nämner fem). Minor-fynd i Fixrunda 1 lade till "of the AI Act" vid första omnämnandet, för att skilja från GDPR:s artikel 4(2) i samma Del 3 |
| A38 | **saknades i guiden:** artikel 27 — konsekvensbedömning före första driftsättning, oavsett kommunal eller fristående skola | 1 | 1 | — | `korsref G51` — samma källa (artikel 27, bilaga III punkt 3) | **lagt till.** I Task 8, och skriver uttryckligen INTE "a body governed by public law" (sant för en kommunal skola, falskt för en friskola) utan "whether the school is publicly run or an independent provider of a public service" — samma fix G51:s andra granskningsrunda låste fast |
| A39 | **saknades i guiden:** artikel 4 — AI-kunnighetsplikten gäller sedan `2 February 2025`, oavsett risknivå | 2/2 | 2/2 | — | `korsref G27` (`docs/guide-facts-gemini.md`) — vaktrad "The prohibited practices and the AI literacy obligations in Article 4 have applied since 2 February 2025"; samma datum i P13 ("AI literacy obligations entered into application from 2 February 2025") | **lagt till.** I Fixrunda 1, efter granskningens Fynd 2. Avsnittets första utkast nämnde bara en plikt som ännu inte gäller (Annex III, 2 december 2027) och gav därmed en skolledare intrycket att ingenting binder än — artikel 4 är den enda AI Act-plikt som faktiskt gäller i dag, och P13:s egen cell pekade uttryckligen ut den som en uppgift "Task 8 bör väga in". **Task 9:** förekomsten på båda ytorna höjd 1/1 → 2/2 — samma tre ankare återanvänds i Fem policybeslut (beslut 3, staff guideline), som nu binder ihop den redan levande plikten med vad skolan ska göra nu. Ingen ny forskning, inga nya ankare |

## Utfallsräkningen

**39 poster** — de ursprungliga 32 (briefens fjorton, A01–A14, plus **18** som runda 1:s
egen mätning lade till, A15–A32) och **7** som Task 8 lade till (A33–A39: Del 3:s nya AI
Act-avsnitt samt artikel 4-posten dess Fixrunda 1 lade till). Efter runda 2:s Task 2–11
beskriver samtliga 39 **den omskrivna guiden**: verdiktkolumnen bär klassificeringen och,
för varje post runda 2 har rört, vad som gjordes med den. Räknat på varje cells
**inledande** token, som är den tabellen ska gå att skanna på:

| token | antal | poster |
|---|---|---|
| `står` | **13** | A01, A02, A04, A08, A09, A11, A12, A14, A26, A28 (10 okvalificerade) samt **A05 `står (öppen EU-fråga)`**, **A06 `står (EU-förbehåll saknas)`** och **A07 `står (delvis obelagt)`** (3 kvalificerade) |
| `föråldrat` | **5** | A15, A17, A21, A22, A30 |
| `falskt` | **5** | A10, A16, A18, A20, A31 |
| `obelagt` | **3** | A25, A27, A29 |
| `rättat` | **5** | A03, A13, A19, A23, A24 — ett tidigare `föråldrat`- eller `falskt`-värde bytt mot ett nytt, källbelagt värde |
| `lagt till` | **8** | A32 (Task 10, den dagliga användningsgränsen) samt A33–A39 (Task 8:s AI Act-avsnitt och Fixrunda 1:s artikel 4-post) — ingen av de åtta en rättelse av en tidigare fel sträng, utan en uppgift guiden saknade helt |

Summan 13 + 5 + 5 + 3 + 5 + 8 = **39**, oförändrat mot postantalet.

**Kvalifikatorerna i parentes är en del av tokenen och ska läsas med den** — samma grepp som
systerinventeringens `fel (omfång)` och `obelagt (ytartefakt)`. De finns därför att en
kvalifikatorlös `står` i de tre kvalificerade cellerna hade ljugit för den som gör precis
vad briefen säger att man ska kunna göra: skanna kolumnen utan att läsa resonemanget.
(**A32 bar tidigare `föråldrat (genom frånvaro)` som ledande token — det var runda 1:s
siffror. Task 10 lade till uppgiften och bytte posten till `lagt till`, så den fjärde
ledande kvalifikatorn finns inte längre. `föråldrat (genom frånvaro)` lever kvar, men bara
som A22:s andra token — se tabellen nedan.**)

| kvalifikator | betyder | åtgärd i runda 2 |
|---|---|---|
| `står (delvis obelagt)` | värdet står, men en **delfråga i samma cell saknar hämtbar källa** — och i A07:s fall är delfrågan DPIA-bärande | behandla delfrågan som `obelagt`: skriv om den utan tvärsäker formulering, hämta eller hedga |
| `står (EU-förbehåll saknas)` | värdet står, men Apple spärrar funktionen eller ett lager av den i EU och guiden saknar förbehållet | lägg till förbehållet; namnet behöver ingen rättelse |
| `står (öppen EU-fråga)` | värdet står; **om** EU-spärren träffar det går inte att avgöra ur hämtad text | avgör frågan först, förbehållet sedan — ingen gissning |
| `föråldrat (genom frånvaro)` | guiden påstod inget fel, den **saknade** en uppgift Apple har publicerat — i dag bara A22:s andra token | lägg till uppgiften; ingen vaktrad är möjlig (0/0) |

**Två av kvalifikatorerna är spärrar, inte dekoration.** `står (delvis obelagt)` på **A07**
får inte läsas som att Mail-kategoriseringens on-device-påstående är belagt — det är det
inte, och det står i DPIA-kapitlet. `står (EU-förbehåll saknas)` på **A06** får inte läsas
som att Visual Intelligence-avsnittet är klart — Apple har skrivit ut EU-svaret och guiden
bär det inte.

### Poster som bär en andra token längre in i cellen

Åtta av 39 celler bär mer än ett utfall (oförändrat sedan runda 1 — ingen av de åtta
`lagt till`-cellerna bär mer än en token, och detsamma gäller de fem `rättat`-cellerna).
Det är inte slarv: flera poster bundlar ett
produktnamn med ett påstående om funktionen, och en post som kollapsas till ett omdöme
ljuger om minst ett av dem. **Tabellen finns för att den som skannar den inledande kolumnen
ska kunna se vilka celler hen inte får lita på oläst.**

| post | inledande | ytterligare | vad den andra tokenen gäller |
|---|---|---|---|
| **A07** | står (delvis obelagt) | **obelagt** | "Entirely on-device … no email content is sent to Apple servers" och "cleanest privacy profile" — Apples sida säger ingenting om var kategoriseringen körs. **DPIA-bärande**, och den enskilt viktigaste raden i den här tabellen |
| **A06** | står (EU-förbehåll saknas) | **föråldrat** + öppen fråga | DMA-sidan namnger "an expanded Visual Intelligence experience" bland det EU-användare inte får; guiden ger fyra klassrumsexempel utan förbehåll. Öppna frågan: bär guidens avsnitt bas- eller det expanderade lagret? |
| **A05** | står (öppen EU-fråga) | öppen fråga | "integrated tools for writing" i samma Apple-mening — oklart om det är guidens `Writing Tools`. 34 förekomster hänger på svaret |
| **A11** | står | **föråldrat** | exklusiviteten står (ChatGPT är enda dokumenterade valbara extension), men tre-nivåinramningen håller inte — se **A17**. Det är två motsatta svar i en cell och får inte slås ihop |
| **A22** | föråldrat | **föråldrat (genom frånvaro)** | `three` är fel **och** ChatGPT-stilvalet inne i Image Playground finns inte i guiden alls |
| **A08** | står | → **A22** | namnet `Image Playground` står; stilpåståendet i samma stycke gör det inte |
| **A26** | står | precisering | adressen står, men PCC-djupdokumentationen ligger under `/documentation/private-cloud-compute/`, inte i blogginlägget guiden pekar mot |
| **A12** | står | → **A16** | `OpenAI` står som motpart; åldersgränsen i samma stycke är falsk |

**A09, A14, A28 och A29 bär bara en token var** och är därför säkra att läsa ur kolumnen —
det är värt att säga uttryckligen, eftersom resten av tabellen inte är det.

## Observationer runda 2 ärver

**1. Den dyraste rättelsen är inte ett ord, det är ett kapitel.** `Siri 2.0` (A10) står på
tio ställen och är ett namnbyte — mekaniskt. `Siri AI`:s EU-spärr (A15) är en sakuppgift
som gör guidens Del 2 §2, dess fem klassrumsexempel och quick-startens punkt 3 obrukbara
för målgruppen. Ett sök-och-ersätt från `Siri 2.0` till `Siri AI` utan A15 gör guiden
**sämre**: den skulle då bära Apples aktuella namn på en funktion läsaren inte kan få, och
därmed se färsk ut medan den är fel.

**2. Tre fel pekar åt samma håll: integritetslöftet är starkare i guiden än hos Apple.**
A16 (13 år, inte 18), A18 och A31 (bekräftelsesteget kan stängas av), A07 (on-device-
påståendet om Mail saknar belägg) och A25 (PCC-regioner i Europa, obelagt). Varje enskilt
fel är litet. Tillsammans ger de en skolledare en tryggare bild än Apples egen
dokumentation bär, och det är den läsargrupp Del 3 är skriven för. Runda 2 bör läsa de fem
posterna som en grupp, inte som fem rader.

**3. Guidens instruktioner föråldras snabbare än dess resonemang.** A20, A21 och A30 är
alla inställningsvägar, och alla tre är fel eller flyttade. Guidens analysavsnitt (PCC,
GDPR-resonemanget, tre-nivåpedagogiken som idé) står sig betydligt bättre än dess
"How to start"-listor. Det är ett argument för att runda 2 skriver vägarna kortare och mer
beskrivande, inte för att den skriver dem noggrannare.

**4. IMY-stycket är printexklusivt och är guidens enda nationella myndighetsreferens.**
EP bär "A word on the Swedish context" med Integritetsskyddsmyndigheten; EW bär inget
motsvarande. En guide som säljs på att vara skriven för svenska skolor har alltså sin
svenska myndighetsförankring bara i PDF:en. Ingen vaktrad är möjlig förrän ytorna möts
(EP 1 / EW 0), och det är ett innehållsbeslut, inte en vaktfråga.

**5. Två av kontrollerns tre leads höll, det tredje höll halvt — och halvan som föll var
den intressanta.** Att Extensions finns var redan sant i april 2026 (A30, arkivet). Att
Claude och Gemini skulle vara valbara där är inte belagt av någon Apple-sida; de hör till
utvecklarramverket. Men medan leadet letade efter Gemini i Inställningar satt Gemini redan
inne i assistenten (A17). Den som skriver runda 2 utifrån leadet i stället för utifrån
källorna skulle ha skrivit in ett fel och missat det riktiga.

**6. Tre poster saknar vaktrad med avsikt** — A30 (EW 1 / EP 0), A31 (EP 1 / EW 0) och
IMY-divergensen (EP 1 / EW 0). Ingen av dem är glömd; var och en är mätt och står i
Ytdivergenser eller i sin egen postrad. En framtida runda som "städar" dem in i
vaktblocket gör den röd. (**A32 stod här före runda 2 Task 10** — den var 0/0 och alltså
i samma läge som dessa tre. Task 10 lade till uppgiften i FAQ:n på båda ytorna och gav den
två egna `aktiv`-rader i vaktblocket; den hör därför inte längre till den här gruppen. Se
Task 10:s kommentarblock i Vaktblocket.)

## Vaktblocket

```guard
# Engelska ytorna: EW `_unpublished/guides/apple-intelligence/index.html` (web)
# + EP `_unpublished/exports/apple-intelligence-print-a4-en.html` (print).
# QS står utanför vakten med avsikt och bevakas av test_guide_delivery.py.
#
# Varje rad är MÄTT mot båda ytorna med vaktens egen normalisering:
# `aktiv` står ordagrant på båda, `borttaget` på ingen. Ingen rad är ärvd
# från planen utan att mätas om.
#
# INGEN RAD PÅ `IMY`: EP:1 / EW:0, alltså `saknas_på_en_yta` från start.
# Divergensen står i prosan ovan och är runda 2:s sak. Samma skäl gäller
# A30 (EW:1 / EP:0) och A31 (EP:1 / EW:0) — de har postrader men ingen
# vaktrad, med avsikt. A32 stod här som (0/0) till och med Task 9; Task 10
# lade till uppgiften och gav den två `aktiv`-rader längst ner i blocket.
A01 | en | M1 chip or later | aktiv
A02 | en | iPhone 15 Pro | aktiv
A03 | en | iPad Pro or iPad Air from 2021 | borttaget
A04 | en | Private Cloud Compute | aktiv
A05 | en | Writing Tools | aktiv
A06 | en | Visual Intelligence | aktiv
A07 | en | Mail categorisation | aktiv
A08 | en | Image Playground | aktiv
A09 | en | Genmoji | aktiv
A10 | en | Siri 2.0 | borttaget
A11 | en | ChatGPT | aktiv
A12 | en | OpenAI | aktiv
A13 | en | April 2026 | borttaget
A14 | en | Data Protection Impact Assessment | aktiv
# Raderna ovan är mätta på BÅDA engelska ytorna 2026-10-14 och är
# `aktiv` därför att de står där i dag — inte därför att de är sanna.
# Verdikten (står/föråldrat/falskt/obelagt) bor i posttabellen; vaktblocket
# mäter bara förekomst. Runda 2 flyttar de föråldrade till `borttaget`.

# Posterna nedan är den här rundans egen mätning, utöver planens fjorton.
# Varje värde är verifierat 1:1 eller mer på båda engelska ytorna med
# samma normalisering innan raden skrevs in.
#
# A13:s tre datumförekomster bär tre olika formuleringar, och två av dem
# står på bara en yta (`Updated April 2026` EW:2/EP:0 och
# `Johan Lindström, April 2026` EP:1/EW:0). Därför är ankaret den nakna
# strängen `April 2026` (3/3) och inte någon av de två långa.
A15 | en | Siri 2.0's fully localised voice responses | borttaget
A16 | en | requires the user to be 18 or over | borttaget
A17 | en | three distinct places your request can be processed | aktiv
A18 | en | always shows a confirmation screen before sending | borttaget
A18 | en | nothing is forwarded without the user accepting it | borttaget
A19 | en | roughly 4 GB on-device model | borttaget
A19 | en | about 4 GB of free disk space | borttaget
A19 | en | the same 4 GB footprint | borttaget
A20 | en | Settings → Notifications → Summarise Previews | borttaget
A21 | en | Settings → Mail → Categorisation | borttaget
A22 | en | three visual styles | borttaget
A22 | en | Animation, Illustration, and Sketch | borttaget
A23 | en | support.apple.com/apple-intelligence | borttaget
A24 | en | the full iPhone 16 and 17 lines are supported | borttaget
A25 | en | Apple operates PCC regions in Europe | borttaget
A26 | en | The full technical whitepaper sits at security.apple.com | aktiv
A26 | en | a technical whitepaper on the PCC architecture | aktiv
A27 | en | Apple ships Apple Intelligence features monthly | borttaget
A28 | en | stateless computation | aktiv
A29 | en | Summaries are on by default | borttaget
# A19 och A26 har tre respektive två rader därför att samma påstående
# står i flera formuleringar per yta. En rättelse som bara träffar den
# första lämnar de andra kvar, och ingenting blir rött — det är precis
# det felet de extra raderna finns för att fånga.
#
# A14, A28 och A07 är `står`-poster. Deras rader är INTE förbudsvakter
# utan bevarandevakter: de ska stå kvar efter runda 2, och raden finns
# för att de inte ska städas bort när kapitlet runt dem skrivs om.

# Runda 2 Task 2 — hårdvaran, lagringen, hjälplänken
# De fyra posterna ovan (A03, A19, A24, A23) är flyttade till `borttaget`
# här och ersatta med de nya värdena nedan, mätta ordagrant på BÅDA
# engelska ytorna 2026-10-14 efter rättelsen.
A03 | en | iPad Pro from 2021 onwards, or an iPad Air from 2022 onwards | aktiv
A19 | en | 8 to 14 GB of on-device storage, depending on your hardware | borttaget
A19 | en | 8 to 14 GB of free disk space, depending on your hardware | borttaget
A19 | en | the same storage range | borttaget
A23 | en | support.apple.com/en-us/121115 | aktiv
A24 | en | iPhone 16 models or later, iPhone 15 Pro, iPhone 15 Pro Max, and iPhone Air are supported | aktiv

# Fixrunda 1 på Task 2 — A19 skrevs först om som ett intervall ("8 to
# 14 GB … depending on your hardware"), vilket läsaren kan missförstå
# som ett golv (minst 8 GB). Apples egna två tak ("up to 8 GB" /
# "up to 14 GB") är tak, inte golv — en äldre enhet kan klara sig med
# mindre. De tre raderna ovan är därför flyttade till `borttaget` igen,
# och ersatta med Apples tvådelade formulering nedan.
A19 | en | up to 8 GB on most supported iPads, or up to 14 GB on iPad models with M4 or later and at least 12 GB of unified memory | aktiv
A19 | en | up to 8 GB of free disk space on most supported Macs, or up to 14 GB on Mac models with M3 or later and at least 12 GB of unified memory | aktiv
A19 | en | up to 8 GB on most models, or up to 14 GB on iPhone 17 Pro, iPhone 17 Pro Max, and iPhone Air | aktiv

# Runda 2 Task 3 — de tre bearbetningsvägarna
# A17: modellen står kvar som tre vägar (strängen nedan är orörd och
# fortsatt `aktiv` — den beskriver var en förfrågan BEHANDLAS, och den
# är fortfarande sann). Det som var `föråldrat` var den underförstådda
# bilden att den tredje vägen är den enda externa parten. Två nya
# meningar, mätta ordagrant på BÅDA engelska ytorna, fäller den bilden:
# Google/Gemini sitter inne i steg 1–2 (Apples egen formulering), och
# ChatGPT namnges uttryckligen som den enda leverantören man VÄLJER.
# (Den ursprungliga raden för "three distinct places …" står redan
# ovan i vaktblockets första del, oförändrad — den dupliceras inte här.)
A17 | en | in collaboration with Google and its Gemini models | aktiv
A17 | en | the one external provider Apple documents as something a user actually chooses to turn on | aktiv

# A25 och A27: obelagda påståenden strukna, utan ersättning. Ingen ny
# `aktiv`-rad för någon av dem — påståendena ska bara vara borta, inte
# bytta mot något annat. Raderna själva (ursprungligen `aktiv`, bland
# planens fjorton ovan) är flyttade till `borttaget` i samma rad de
# redan stod på, enligt samma mönster som A03/A19/A23/A24 i Task 2.

# Runda 2 Task 4 — internationaliseringen (ingen ny vaktrad av detta avsnitt)
# Sidan 3:s språkstycke bar två problem i samma mening: en nationell
# referens (`Swedish became available during 2025 alongside the other
# main European languages`) och samma obelagda kadens som A27
# (`Language support has expanded quarterly since launch`, EW 2 / EP 1
# på `quarterly` — se A27:s notkolumn ovan). Båda är skrivna om till
# generell, kadensfri inramning på BÅDA ytorna. Detta föregriper INTE
# A15: Siris faktiska språkläge (`Siri 2.0's fully localised voice
# responses … keep improving through 2026`, FAQ-stycket) rörs inte här
# — det är Task 5:s fynd och tas i FAQ-svaret om `Is Apple Intelligence
# available in Swedish?`, som står kvar oförändrat på båda ytorna.
# IMY-stycket (se Ytdivergenser ovan, nu löst) bar samma mönster: dess
# "Apple ships features monthly" är en egen, kortare sträng än A27:s
# vaktrad och fångas inte av den — frekvensen är ändå borttagen i
# omskrivningen, utan ersättning, enligt samma princip som A27.
# En ytterligare förekomst låg utanför briefens tabell men inom samma
# nycklar (`1:1`) och är rättad här för att nå noll: EP:s FAQ-svar på
# "Does my iPad qualify" bar `1:1 fleet iPads` (ingen egen post ovan
# att flytta till `borttaget`) och är nu `school-fleet iPads`, samma
# ordval EW redan använde. Ingen av de tre (quarterly-meningen,
# IMY-rutans kortfras, 1:1 fleet iPads) är en post i tabellen ovan; de
# är rena inramningsrättelser, inte sakrättelser, och kräver därför
# ingen ny `aktiv`/`borttaget`-rad.
#
# Fixrunda 1 — EW:s FAQ-svar på "Where do I get help" bar också
# `I offer consulting for schools, primarily in Sweden.` Jag strök
# `primarily in Sweden` i den första versionen av den här rättningen;
# granskningen fällde det som ett Important, och koordinatorns ruling
# återställde meningen ORDAGRANT. Skälet går längre än formalia: frasen
# är ett sakpåstående om GUIDEFÖRFATTARENS egen verksamhet, inte om
# läsarens jurisdiktion — internationaliseringens poäng är att läsaren
# inte ska behöva vara svensk, inte att författaren ska framställas som
# verksam överallt. Att stryka kvalifikatorn hade LAGT TILL ett
# obelagt påstående ("jag erbjuder konsultation för skolor",
# okvalificerat) i stället för att ta bort ett. Meningen står alltså
# kvar, ordagrant, på EW rad ~480 (`_unpublished/guides/apple-
# intelligence/index.html`, FAQ-svaret "Where do I get help if
# something goes wrong?"). **Den här raden är skälet till att Task 14
# inte kan förbjuda bart `Sweden` eller `Swedish` i sin förbudslista**
# — en sådan regel skulle slå mot en korrekt, källbelagd uppgift om en
# verklig person. Förbudslistan måste i stället förbjuda FRASER (t.ex.
# `Swedish school context`, `Swedish Data Protection Authority`,
# `1:1 programmes` i elevnärmande inramning) på samma sätt som
# gemini-notebook-guidens förbudslista redan gör, eftersom dess egen
# källbelagda praktikexempel också bär ordet `Sweden`/`Swedish`.

# Runda 2 Task 5 — Siri AI: namnet och EU-spärren
# A10: `Siri 2.0` ströks på alla elva förekomster på de engelska ytorna
# (EP 7 + EW 4, varav en vardera var en HTML-kommentar — `<!-- 2.2 Siri
# 2.0 -->` i EW och två versal-kommentarer i EP, `SIRI 2.0 OPENER` /
# `SIRI 2.0 CONT.` — briefens mätning (7/3) var en förekomst för låg på
# EW eftersom den bara räknade synlig text; grep -c räknar matchande
# RADER och fångar kommentaren). Alla elva är bytta till `Siri AI`,
# kommentarer inkluderat, så `finns_ingenstans` gäller ordagrant —
# **för de två vaktade ytorna.** `_unpublished/exports/apple-
# intelligence-quick-start-en.html:112` bär fortfarande `Siri 2.0` och
# ligger UTANFÖR `surfacecheck.GUIDE_SURFACES` (quick-starten vaktas
# inte av ytkonsistensvakten, bara av `test_guide_delivery.py`).
# A10:s postrad (`docs/guide-facts-apple-intelligence.md` rad 102)
# räknar den förekomsten i sin faktakolumn; vaktraden gör det inte.
# Quick-starten rörs inte av Task 5 — en senare uppgift äger den.
A10 | en | Siri AI | aktiv
#
# A15: den gamla meningen (`Siri 2.0's fully localised voice responses
# … keep improving through 2026`) fanns bara på ett ställe per yta —
# FAQ-svaret "Is Apple Intelligence available in Swedish?" — inte i
# Siri-avsnittet självt (vars "Where it runs"-ruta bara beskriver
# bearbetningsväg, inte språkstatus). Dokfilens egen not under Task 4
# ovan pekar hit: "det är Task 5:s fynd". Båda ytornas FAQ-svar är
# omskrivna så löftet är borta, inte bara namnbytt — ett sök-och-ersätt
# som bara döpt om `Siri 2.0` till `Siri AI` hade lämnat lögnen kvar
# med nytt namn. EU-förbehållet står själv i Siri-avsnittets egen
# löptext (ny `processing-callout`-ruta på båda ytorna, direkt efter
# inledningsstycket, före klassrumsexemplen) OCH som en kort hänvisning
# i FAQ-svaret. Ankaret nedan är den enda fras som står ordagrant
# likadan på alla tre ställena (Siri-avsnittet EP, Siri-avsnittet EW,
# FAQ-svaret båda ytorna): `the EU's Digital Markets Act`. De tre
# sakuppgifterna (spärrad i EU, DMA angivet skäl, ingen tidplan) står i
# samtliga fyra passager; ingen av dem skriver att funktionen "kommer
# senare" eller antyder en tidplan.
A15 | en | the EU's Digital Markets Act | aktiv

# Runda 2 Task 6 — de fem övriga funktionerna
# A20, A21, A22 och A29: de fyra raderna ovan (bland planens "utöver
# fjorton") är flyttade till `borttaget` i samma rad de redan stod på,
# enligt samma mönster som A03/A19/A23/A24/A25/A27 tidigare. A29 får
# ingen ersättande `aktiv`-rad alls — kapitlet pekar nu bara till var
# inställningen bor, utan att påstå ett utgångsläge, så det finns inget
# nytt sakpåstående att ankra. A20, A21 och A22 får ersättande
# `aktiv`-rader nedan, mätta ordagrant på BÅDA engelska ytorna
# 2026-10-14 efter rättelsen (Notification summaries-kapitlet och
# FAQ-svaret för A20; Mail-kapitlet och FAQ-svaret för A21; "Worth
# knowing"-stycket för A22).
A20 | en | Settings → Notifications → Summarize Notifications | aktiv
A20 | en | Choose Notifications to Summarize | aktiv
A21 | en | List View | aktiv
A22 | en | Any Style | aktiv
A22 | en | Illustration | aktiv
#
# A07: `Mail categorisation` själv (radet ovan i planens fjorton) är
# oförändrad och förblir `aktiv` — namnet och de fyra kategorierna
# står kvar, obestritt. Det obelagda ledet var bara på-enheten-påståendet
# och den superlativa slutsatsen som hängde på det; båda är strukna ur
# "Where it runs · Mail categorisation"-rutan på båda ytorna, utan
# ersättande sakpåstående om VAR kategoriseringen körs — rutan säger nu
# att det är obekräftat, vilket inte är ett nytt påstående att ankra.
A07 | en | no email content is sent to Apple servers | borttaget
A07 | en | cleanest privacy profile in the entire Apple Intelligence suite | borttaget
#
# FIXRUNDA 1 — GRANSKNINGSFYND 2 (Important), koordinatorns ruling: INTE ett
# bredare ankare här (det skulle göra sviten röd över en uppgiftsgräns — Del
# 3 ägs av nästa uppgift, och ett sådant ankare gör varje mellanliggande
# "noll failed" meningslöst). I stället en synlig notis, mätt 2026-10-14:
#
# Frasen `Mail categorisation and notification summaries are entirely
# on-device` står ORDAGRANT en gång per yta: EP sida 19 (Part 3, stycket
# under "What stays on your device") och EW samma avsnitt (id `p3-stays`).
# Det är **1/1**, inte koordinatorns preliminära "2 i EP, 1 i EW" — verifierat
# med `grep -c` mot den exakta strängen på båda ytorna och rapporterat så i
# Task 6:s fixrapport, Fixrunda 1.
#
# SAMMA SAKUPPGIFT står en gång till, i ANNAN ordalydelse, på BÅDA ytorna:
# Part 1:s "1. On-device processing"-stycke (EP sida 5, EW samma avsnitt, id
# `p1-pcc`) räknar "Mail categorisation" bland det som "run[s] entirely on
# the iPad, Mac, or iPhone … Nothing leaves the device." Den meningen ligger
# i Task 3:s sidspann (5–8) men var INTE bland Task 3:s nio poster (A04,
# A17, A25, A26, A27, A28) — den är orörd sedan runda 2 startade och bär nu
# samma motsägelse mot Del 2:s "unconfirmed"-hållning som sidan 19.
#
# Ingen av de två platserna fångas av A07:s `borttaget`-rader ovan — de
# ankrar bara de två STRUKNA superlativfraserna ur Del 2:s egen ruta, inte
# dessa två kvarstående påståenden. Vakten är alltså grön utan att vaka
# motsägelsen, känt och avsiktligt enligt ruling ovan.
#
# NÄSTA UPPGIFT (Del 3) ÄGER BÅDA PLATSERNA: rätta sida 19 OCH Part 1:s
# "On-device processing"-stycke (som ligger geografiskt i Task 3:s sidspann
# men aldrig rättades av Task 3, eftersom A07 inte var dess post) i samma
# svep, och sätt ett bredare `aktiv`→`borttaget`-ankare som täcker BÅDA
# ordalydelserna. En enda sammansatt sträng räcker sannolikt inte: `Mail
# categorisation … entirely on-device` (granskarens förslag) fångar sida
# 19:s fras men INTE Part 1:s ("Mail categorisation, and Notification
# summaries" i en uppräkning, följt långt senare av den separata meningen
# "Nothing leaves the device.") — troligen krävs TVÅ ankare, ett per
# ordalydelse, snarare än ett som läser över menings- och styckegränsen.
# Oavsett lösning: ankaret/ankarna får INTE träffa den legitima
# notis-rutan (`index.html:289`, "Entirely on-device — no notification
# content leaves the iPad") — annan ordalydelse, utan `Mail categorisation`,
# och ska stå kvar oförändrad.
#
# A05 och A06 är inga förbudsvakter i vanlig mening — de ankrar ny text
# som INTE fanns i guiden förut (cellerna säger uttryckligen att
# posterna i dag bär inget EU-förbehåll alls). Ankaret är i båda fallen
# Apples egen citerade fras ur DMA-sidan, vald därför att den är den
# enda delen av de två nya styckena (Writing Tools respektive Visual
# Intelligence, ~40 % olika formulerade per yta enligt husstilen) som
# står ordagrant lika på EP och EW.
#
# A05: frågan är och förblir OBESVARAD ur källan — raden ankrar bara
# att den öppna frågan själv står i guiden, inte ett svar på den. Ingen
# av tolkningarna (Writing Tools / Siris egen skrivintegration) påstås.
A05 | en | integrated tools for writing | aktiv
#
# A06: Visual Intelligence-kapitlet skiljer nu uttryckligen det
# grundläggande lagret (oberört) från det "expanded" lagret (spärrat i
# EU, Apples egen formulering, ingen publicerad tidplan).
A06 | en | an expanded Visual Intelligence experience | aktiv
#
# Kontrollerns tillägg — sidorna 17 och 18 (EP): EP:s "A week in the
# classroom, composed"-stycke (sidan 17) sålde Siri AI:s
# lektionsplans-hämtning utan förbehåll, två sidor efter att
# förbehållet infördes i Siri-avsnittet (sidan 10). Meningen bär nu en
# kort hänvisning ("not on an EU iPad, where Siri AI remains blocked —
# see the Siri AI entry earlier in this Part") i stället för hela
# förbehållet igen. Ingen ny vaktrad: hänvisningen återanvänder inga nya
# sakuppgifter, bara en pekare till Siri-avsnittets redan ankrade
# `the EU's Digital Markets Act` (A15). EW har ingen motsvarande
# sammanfattande sida — dess Siri-exempel (inklusive samma
# lektionsplans-hämtning) står redan under Siri-avsnittets egen
# `Not available in the EU`-ruta, så ingen ändring behövdes där.

# Runda 2 Task 7 — ChatGPT-vägen
# A16 och A18: de tre raderna ovan (bland planens fjorton/utöver-fjorton)
# är flyttade till `borttaget` i samma rad de redan stod på, enligt samma
# mönster som tidigare uppgifter. Ersättande `aktiv`-rader nedan, mätta
# ordagrant på BÅDA engelska ytorna 2026-10-14 efter rättelsen.
#
# A16: `18 or over` är bytt mot Apples egen ålder (`at least 13 years
# old or the minimum age required in your country`). Samma mening,
# ordagrant likadan, på EP (sida 4, Setup) och EW (avsnitt p1-setup).
A16 | en | requires the user to be at least 13 | aktiv
#
# A18 hade två skilda förekomster, en per stycke, och båda var falska på
# samma sätt: "always"/"nothing is forwarded without" läser bekräftelsen
# som arkitektoniskt garanterad. Apples egen `Confirm Requests`-inställning
# (Settings → Siri → ChatGPT) stänger av just den skärmen, och fanns redan
# i april 2026 (se A18:s källcell).
#
# FIXRUNDA 1 (Critical, granskningen): mitt första försök bytte den
# obetingade formuleringen mot en annan obetingad formulering — "Apple
# also documents a setting that turns that confirmation off" — utan
# källcellens eget förbehåll: "This option isn't available if you're
# using Siri AI." I just den rutan som uttryckligen handlar om Siri AI
# (förekomst 1 nedan) var det alltså sakligt fel i precis motsatt
# riktning av det ursprungliga felet. Felets rot var briefens instruktion
# ("att inställningen finns, och att den kan stängas av") — en riktig
# sammanfattning av HÄLFTEN av källan, skriven som om den vore hela. Båda
# de obetingade raderna som denna fixrunda skrev in är därför flyttade
# till `borttaget` nedan, och ersatta av EN delad, tvådelad formulering
# som står ordagrant likadan på BÅDA förekomster och BÅDA ytorna:
A18 | en | shows a confirmation screen before sending by default | borttaget
A18 | en | turns this confirmation off | borttaget
A18 | en | that option isn't available when using Siri AI itself, so for Siri AI specifically the confirmation can't be disabled | aktiv
#
# Förekomst 1 — "Where it runs · Siri AI"-rutan (EP sida 11, EW samma
# kort): bekräftelsen visas, kan stängas av för klassisk Siri, men INTE
# under Siri AI — den exakta funktion rutan beskriver.
#
# Förekomst 2 — Del 3:s "This is where the on-device promise breaks"-ruta
# (EP sida 21, EW p3-chatgpt), guidens mest integritetskritiska stycke:
# samma tvådelade sanning, plus den praktiska slutsatsen att vilket läge
# som gäller beror på vilken Siri enheten kör — en skola ska inte anta
# det strängare av de två utan att kontrollera.
#
# A30 och A31 är rättade i samma commit, men får AVSIKTLIGT ingen ny
# aktiv-rad — de är enytiga (A30 bara EW, A31 bara EP), och en vaktrad som
# kräver ordagrann träff på BÅDA ytorna vore `saknas_på_en_yta` från första
# sekunden, exakt det Ytdivergenser-avsnittet ovan redan varnar för (samma
# skäl som IMY). A30:s gamla sträng (`Siri &amp; Apple Intelligence →
# ChatGPT Extension`, EW:488) är bytt mot `Settings → Siri → ChatGPT
# Extension` — dagens väg, inte den som gällde i april 2026. A31:s gamla
# mening (`Every path to ChatGPT shows a confirmation screen before
# sending`, EP:1012, "At a glance"-rutan) är omskriven till samma sakläge
# som A18: tappet är alltid ett uttryckligt tryck, men skärmen som följer
# är en standard, inte en garanti.
#
# FIXRUNDA 1 (Important, samma granskning): A31:s första omskrivning bar
# samma brist som A18:s Critical-fynd — obetingad ("Apple documents a
# setting that turns it off"), utan Siri AI-förbehållet. Eftersom A31
# sitter i EP:s "At a glance"-ruta och alltså är en global sanning om hela
# guiden (inte bara om Del 3:s uttalade EU-läsare), är den nu rättad till
# samma tvådelade sanning som A18, i egen, kortare ordalydelse (ingen delad
# vaktrad, eftersom A31 inte har en). Ingen av A30/A31-raderna flyttas till
# `borttaget` — det fanns aldrig en vaktrad för dem att flytta.
#
# A07: de två bredare ankarna kontrollern efterfrågade, ett per
# ordalydelse. Båda fångar BARA Mail-kategoriseringens på-enheten-påstående
# (den DPIA-bärande motsägelsen mot Del 2:s "unconfirmed"-hållning), inte
# den legitima notis-rutan om notissammanfattningar (`index.html:289`,
# "Entirely on-device — no notification content leaves the iPad" — ingen
# `Mail categorisation` i den strängen) och inte Del 2:s redan hedgade
# Mail-mening (`apple-intelligence-print-a4-en.html:863`, "Don't assume
# this one is entirely on-device; Apple hasn't confirmed it either way" —
# ingen av de två nya ankarna står i den meningen). Provade mot båda före
# commit, se rapporten.
#
# Ankare 1 — Del 3:s "What stays on your device" (EP sida 19, EW p3-stays),
# ordagrant likadan på båda ytorna innan rättelsen:
A07 | en | Mail categorisation and notification summaries are entirely on-device | borttaget
#
# Ankare 2 — Del 1:s "1. On-device processing"-stycke (EP sida 5, EW
# p1-pcc), en annan ordalydelse än ankare 1 och därför en egen rad —
# `entirely on-device` finns inte i den här meningen, bara "Nothing
# leaves the device":
A07 | en | Mail categorisation, and Notification summaries. Nothing leaves the device. | borttaget

# Runda 2 Task 8 — Del 3: ett nytt avsnitt om EU:s AI-förordning (guiden bar
# noll om AI Act innan den här uppgiften; sex nya id:n, A33–A38 i det första
# svepet, A39 tillagd i Fixrunda 1 — se den gruppen nedan). Ingen ny research — avsnittet ärver
# källbelagd allokering från två systerinventeringar: docs/guide-facts-
# claude.md P13 (Europeiska kommissionen, digital-strategy.ec.europa.eu/en/
# policies/regulatory-framework-ai, läst ordagrant 2026-10-08) och
# docs/guide-facts-gemini.md G25/G26/G27/G48/G51 (G51 i sin tur:
# artificialintelligenceact.eu, artikelsidorna, hämtade ordagrant
# 2026-10-13). Alla sex rader mätta ordagrant på BÅDA engelska ytorna
# 2026-10-14, efter avsnittet skrevs in på EP sida 23 (ny) och EW p3-ai-act.
A33 | en | 2 August 2026 | aktiv
A34 | en | 2 December 2027 | aktiv
A35 | en | Unacceptable risk | aktiv
A35 | en | Transparency risk | aktiv
A35 | en | Minimal or no risk | aktiv
A36 | en | Article 16 | aktiv
A37 | en | Article 26 of the AI Act, which includes: follow the instructions for use, assign human oversight to staff with the competence, training, authority and support to exercise it, retain the logs it controls for at least six months, inform staff and their representatives before putting it to work, and tell the people subject to it that it is in use. | aktiv
A38 | en | Article 27 adds a fundamental-rights impact assessment before first deployment, and it applies whether the school is publicly run or an independent provider of a public service. | aktiv
#
# A33/A34 — korsref P13: kommissionens egen ordalydelse "became applicable on
# 2 August 2026" och "the rules for high-risk use cases in certain sensitive
# areas (Annex III) have been extended to 2 December 2027 as a result of …
# the AI Omnibus". Annex III omfattar uttryckligen utbildning. Samma två
# datum, redan rättade i Gemini-guiden under G25/G48.
#
# A35 — korsref P13 (kommissionens ordalydelse: "Unacceptable risk / High
# risk / Transparency risk / Minimal or no risk") och G26 (samma tre namn,
# redan rättade i Gemini-guiden efter att ha stått som `Limited risk`,
# `Minimal risk` och `Prohibited`). Avsnittet namnger INGEN av de tre
# felaktiga varianterna. `High risk` står också i löptexten men får ingen
# egen rad: det är inte ett namn som stått fel i någon syskonguide, och
# det är inte i briefens lista över riskbenämningar att vakta.
#
# A36/A37/A38 — korsref G51 (artificialintelligenceact.eu, artikel 16, 26
# och 27, hämtade ordagrant 2026-10-13; samma allokering G51:s tre
# granskningsrundor låste fast för en syskonguide). A37 återanvänder G51:s
# slutgiltiga formulering av artikel 26-listan ORDAGRANT, inklusive 26.6:s
# förbehåll ("the logs it controls", inte "the system's logs") och
# `which includes` i stället för ett kolon som lovar en sluten lista. A38
# återanvänder G51:s rättade artikel 27-formulering och skriver uttryckligen
# INTE `a body governed by public law` — det var sant för en kommunal skola
# och falskt för en friskola, G51:s andra granskningsrundas fynd. Delad
# ordalydelse mellan syskonguider för juridiskt precisa satser är avsiktlig
# praxis, inte en miss — se G48:s egen not om samma mönster.
#
# Avsnittet påstår INGENSTANS att Apple Intelligence självt är ett
# högrisksystem enligt bilaga III: det beror på hur systemet används, inte
# på produkten, och ingen av de tre inventeringarna avgör frågan — se
# avsnittets sista stycke på båda ytorna. Förhandsplikterna (art. 9–15, 17,
# 43, 48, 49.1 via art. 16(a)) läggs inte på skolan i avsnittet; de är
# leverantörens (A36).

# Fixrunda 1 på Task 8 — granskningens två Important och tre Minor.
#
# FYND 1 (Important): A33–A38 saknade postrader i ## Poster, och
# Utfallsräkningen sa fortfarande "32 poster". Åtgärdat i tabellen ovan
# (A33–A39 är nu egna rader, med `korsref P13`/`korsref G51`/`korsref G27` i
# källkolumnen) och i Utfallsräkningens rubrik och tokentabell (ny `lagt
# till`-rad, 7 poster). Ingen ändring i vaktblocket krävdes av det fyndet —
# spårbarheten där var redan korrekt, bara fel ställe.
#
# FYND 2 (Important, koordinatorns ruling): artikel 4 saknades — den enda
# AI Act-plikt som binder en skola redan i dag (AI-kunnighet, sedan
# 2 februari 2025, oavsett risknivå). En ny mening på varje yta, i samma
# stycke som "is not due yet"/"isn't due yet", före Annex III-meningen.
# Ny post A39, korsref G27 (`docs/guide-facts-gemini.md`, vaktrad "The
# prohibited practices and the AI literacy obligations in Article 4 have
# applied since 2 February 2025") och P13 (samma datum, kommissionens egen
# ordalydelse "AI literacy obligations entered into application from
# 2 February 2025"). Tre guard-rader, mätta ordagrant på BÅDA ytorna:
A39 | en | 2 February 2025 | aktiv
A39 | en | Article 4 of the AI Act's AI-literacy | aktiv
A39 | en | every school that deploys an AI system | aktiv
#
# Den sista raden ankrar den risknivåoberoende träffbilden ("regardless of
# risk tier" / "oavsett risknivå") som koordinatorns ruling krävde — samma
# fras står ordagrant i båda ytornas artikel 4-mening, trots att meningarna
# i övrigt är ~40 % olika formulerade.
#
# MINOR 3: EP:1138 hade ett tankstreck som aldrig slöt ("… Commission's own
# examples." i stället för "… examples — the obligations …"), vilket
# avslutade meningen vid den inskjutna satsen i stället för att återvända
# till huvudsatsen. EW gjorde det redan rätt. EP lagd i EW:s form — ingen
# ny vaktrad, det är en interpunktionsfix, inget nytt sakvärde.
#
# MINOR 4: "What a school carries, as the deployer, is Article 26" stod i
# presens, ett stycke efter "is not due yet"/"isn't due yet" — vilket läser
# som att artikel 26-plikterna redan gäller, trots att Annex III-utlösaren
# för utbildning inte gör det förrän 2 december 2027. Tillagt på båda
# ytorna: "From 2 December 2027, what a school would carry, as the
# deployer, is …" (EP) / "From 2 December 2027, what would fall to a
# school as the deployer is …" (EW) — samma tre ord koordinatorn efterfrågade,
# och samma datum som A34 redan ankrar (EP:s förekomst av `2 December 2027`
# är därför nu 2, se A34:s postrad).
#
# MINOR 5: "Article 26" bytt till "Article 26 of the AI Act" vid första (och
# enda) omnämnandet på båda ytorna, eftersom samma Del 3 använder
# `Article 4(2)` om GDPR ("What stays on your device"-sidan) och ett naket
# artikelnummer i guidens enda rättsliga avsnitt annars är tvetydigt. A37:s
# guard-rad ovan är uppdaterad till den nya, längre strängen i samma
# commit — ingen gammal rad lämnad kvar att bli `återinfört`-fälld.
#
# Samma tvetydighet gäller i princip "Article 4" (GDPR har också en
# artikel 4), så A39:s nya mening skriver självmant "Article 4 of the AI
# Act" också — inte beordrat av granskningen, men samma princip tillämpad
# på en mening som skrevs i samma svep. Flaggat i fixrapporten för
# kontrollören att ogilla om den anses gå utanför fyndets omfång.
#
# EJ åtgärdat, enligt uttrycklig instruktion: artikel 26-meningens
# skannbarhet (granskarens Minor 6 — vaktraden kräver G51:s ordalydelse
# ordagrant, en omskrivning skulle kräva en ny vaktrad och en ny
# överenskommelse om vad som ankras) och "six pages"-talet (Minor 7 — ägs
# av Task 13:s omrendering).

# Runda 2 Task 9 — Del 3: studentdata och de fem policybesluten
#
# Mätning mot de tre fakta Task 5/7/8 rättade (EU-spärren på Siri AI,
# ChatGPT-vägens 13-årsgräns, det tvådelade bekräftelsesteget): ingen av
# de fem policybesluten och inget i studentdata-sidan vilar på något av
# de tre. Besluten 1, 2, 4 och 5 samt studentdata-sidan är oförändrade —
# se rapporten för resonemanget per beslut. A14 (DPIA) rörd inte, som
# briefen krävde.
#
# Beslut 3 (staff guideline) fick ETT nytt, kort tillägg på båda ytorna:
# AI Act-avsnittets artikel 4-plikt (A39) gäller redan i dag, och
# guidelinen är den naturliga platsen bland de fem besluten för den
# kopplingen. Samma tre A39-ankare återanvänds ordagrant (`Article 4 of
# the AI Act's AI-literacy`, `every school that deploys an AI system`,
# `2 February 2025`) — ingen ny guard-rad, ingen ny forskning, och
# avsnittets fulla resonemang (fyra risknivåer, Annex III, artikel
# 26/27) upprepas inte. A39:s förekomst i huvudtabellen höjd 1/1 → 2/2.
#
# Menynamnsfrågan Task 7 lämnade (`Apple Intelligence & Siri`): mätt på
# båda ytorna, inga träffar i studentdata- eller policybeslut-sidorna.
# De fem träffarna på EP och fyra på EW ligger alla i avsnitt som rör
# HÅRDVARUKONTROLLEN (är enheten kompatibel), inte ChatGPT-spärren A30
# rättade. A30:s källa (support.apple.com ChatGPT-guiden) säger bara vad
# ChatGPT-vägens egen inställning heter i dag (`Settings → Siri`); ingen
# hämtad källa i inventeringen uttalar sig om det allmänna
# kompatibilitetsmenyns namn. Lämnat orört — ingen gissning.

# Runda 2 Task 10 — FAQ:n
#
# 1) Internationaliseringen av språkfrågan. Frågan själv (tidigare "Is
# Apple Intelligence available in Swedish?") är skriven om till en
# generell fråga om icke-engelska språk — EP: "Is Apple Intelligence
# available in my language?"; EW: "Is Apple Intelligence available in a
# language other than English?" (husstilens vanliga ~40 % variation).
# Task 5/Task 4:s givna text (se Task 4:s kommentarblock ovan: "detta
# föregriper INTE A15 ... det är Task 5:s fynd") är behandlad som given:
# Siri AI-meningen och "Verify the [current/live] language matrix ..."
# är ORÖRDA i sak, bara "for the language you teach in" infogat i den
# senare. Ingen kadens och inget vänteläge är återinfört — "Swedish
# rolled out during 2025" / "Swedish localisation rolled out during
# 2025" är en förfluten, daterad händelse, inte ett löfte om framtida
# täckning, och ingen ny frekvens eller "kommer snart"-formulering är
# tillagd.
#
# BESLUT (första svepet, ERSATT av Fixrunda 1 nedan) — `Swedish` som
# exempel, inte struket: båda ytornas nya svar behöll ordet `Swedish` EN
# gång som en uttrycklig exempelmarkering ("Swedish, for example, rolled
# out during 2025, and ..."). Granskningen fällde detta som Important:
# frågan såg internationaliserad ut i rubriken men inte i svaret — en
# läsare vars språk inte är svenska fick ingen egen datapunkt, bara en
# hänvisning till att "kolla matrisen", medan Sverige var den enda nation
# som namngavs. Koordinatorns ruling: släpp landnamnet, generalisera även
# sakinnehållet. Se Fixrunda 1 nedan för den slutgiltiga texten och
# mätningen.
#
# `Sweden` (skiljt från `Swedish`, annan sträng), orört av både första
# svepet och Fixrunda 1: den enda EW-förekomsten är Fixrunda 1 på Task
# 4:s återställda "I offer consulting for schools, primarily in
# Sweden." i FAQ-svaret "Where do I get help if something goes wrong?"
# — ett ägarbeslut om guideförfattarens egen verksamhet, inte läsarens
# jurisdiktion (se Task 4:s Fixrunda 1-kommentar ovan för hela
# resonemanget). Task 10 har INTE rört den meningen, i något svep.
#
# 2) A03:s hårdvaruår i FAQ:n. FAQ-svaret "Does my iPad support Apple
# Intelligence?" bar på EP en ANNAN formulering än A03:s vaktsträng
# ("iPad Pro and iPad Air from 2021" — "and", inte "or", och ingen egen
# vaktrad fångade den, se Task 2:s självgranskning). Samma sakfel som
# A03 (iPad Air är 2022, inte 2021). Rättad till "iPad Pro from 2021,
# iPad Air from 2022" — FAQ:ns egna, kortare register, inte ett
# ordagrant lån av A03:s vaktsträng. EW:s motsvarande svar nämnde aldrig
# ett årtal ("iPad Pro (M1 and up), iPad Air (M1 and up)") och bar
# alltså aldrig felet — ingen ändring behövdes där. Ingen ny guard-rad:
# FAQ:ns fras är och förblir en annan ordalydelse än A03:s existerande
# `aktiv`-rad, med avsikt (FAQ:ns kompakta stil), så den dupliceras inte
# här.
#
# 3) A32 — lagt till, båda ytorna, i samma FAQ-svar som punkt 2 ("Does
# my iPad support Apple Intelligence?"), som en avslutande
# budgetanmärkning efter hårdvarukontrollen. Tre sakuppgifter ur källan:
# namngivna serverburna funktioner har en daglig användningsgräns,
# gränsen kan variera, och utökad åtkomst kommer kosta i framtiden utan
# angivet datum. Ingen tidplan påstås (källan ger ingen, och svaret
# upprepar inte "i framtiden" som om det vore snart). Två ankare, mätta
# ordagrant på BÅDA engelska ytorna efter tillägget:
A32 | en | Siri AI, Intelligent Photo Editing Tools, Image Playground | aktiv
A32 | en | will come at a fee in the future | aktiv
#
# A32:s huvudtabellsrad uppdaterad (förekomst 0/0 → 1/1, verdikt
# "lagt till i runda 2 Task 10"). Observationernas punkt 6 och
# vaktblockets inledande kommentar (ovan) uppdaterade i samma commit —
# A32 räknas inte längre bland posterna utan vaktrad.
#
# Meny-namnet `Apple Intelligence & Siri` i FAQ-svar 1 och 2 är ORÖRT —
# samma avgörande som Task 9 gjorde (ingen källa i inventeringen avgör
# den allmänna kompatibilitetsmenyns namn). Ingen av de två tilläggen
# ovan (punkt 2 och 3) rör den frasen.
#
# FIXRUNDA 1 (Important, granskningen; koordinatorns ruling: genomför
# rekommendationen). Fyndet: frågan var generaliserad i rubriken men
# inte i svaret — Sverige var kvar som det enda konkreta innehållet,
# och en läsare på ett annat språk fick ingen egen datapunkt, bara en
# hänvisning till matrisen. Landnamnet är nu helt släppt och
# sakinnehållet generaliserat, enligt rulingen: svaret säger att
# språkstödet varierar per språk och fortsätter utökas, och pekar på
# Apples levande språkmatris för LÄSARENS eget språk — ingen enskild
# nation namnges längre någonstans i meningen. Siri AI-meningen om
# EU-spärren (A15) är OFÖRÄNDRAD — den är sakinnehåll, inte inramning.
# Inget sägs om NÄR något rullade ut; ingen kadens infördes.
#
# Ny text, ordagrant:
# EP: "Language support varies by language and keeps expanding — check
# Apple's live language matrix for the language you teach in before
# planning a staff rollout. Siri AI itself is a separate case: it is
# blocked in the EU on iPhone and iPad. Apple cites the EU's Digital
# Markets Act as the reason, with no published timeline — see Part 2
# for details."
# EW: "Language support varies by language and keeps expanding — check
# Apple's live language-support matrix for the language you teach in
# before planning a staff rollout. Siri AI is a separate matter: it is
# blocked in the EU on iPhone and iPad, Apple's stated reason is the
# EU's Digital Markets Act, and Apple has not published a timeline — so
# treat the Siri AI features described in Part 2 as unavailable on an
# EU iPad regardless of language."
#
# Inga guard-rader bar `Swedish`-formuleringen (kontrollerat: `grep -n
# "^A[0-9]* | en | .*Swedish" docs/guide-facts-apple-intelligence.md`
# gav noll träffar både före och efter) — A15:s enda ankare är "the
# EU's Digital Markets Act", som står oförändrat i den kvarvarande
# Siri AI-meningen. Ingen rad att flytta till `borttaget`, ingen ny rad
# att lägga till.
#
# Mätning efter fixen, med briefens eget skript:
# `{'Sweden': 0, 'Swedish': 0, 'IMY': 0, 'Siri 2.0': 0}` (EP) och
# `{'Sweden': 1, 'Swedish': 0, 'IMY': 0, 'Siri 2.0': 0}` (EW).
# `Swedish` är nu NOLL på båda ytorna — ordet finns inte längre
# någonstans i guiden. `Sweden` står kvar en gång, EW rad 500,
# "I offer consulting for schools, primarily in Sweden." — oförändrad,
# ägarbeslut (se ovan). **Underlag för Task 14:s förbudslista:** `Swedish`
# kan nu förbjudas som bart ord (ingen legitim förekomst kvar); `Sweden`
# kräver fortfarande frashantering, inte ett bart ordförbud, eftersom
# den enda kvarvarande förekomsten är en sann biografisk uppgift om
# guideförfattaren, inte en nationell generalisering av läsarens
# kontext.

# Runda 2 Task 11 — omslaget, sidfoten, datumstämpeln och quick-starten
#
# A13: `April 2026` är flyttad till `borttaget` ovan (raden som stod bland
# planens fjorton) och ersatt av `October 2026` nedan, mätt ordagrant 3/3
# på BÅDA engelska ytorna efter ett rent sök-och-ersätt (omslaget/hero,
# löptextens hårdvarustycke, avslutningens signatur — samma tre
# förekomster och samma tre formuleringar A13:s postrad redan beskriver,
# bara med det nya ordet). Stämpeln sätts om i den här commiten,
# tillsammans med hela rundans sakändringar — i enlighet med postradens
# egen regel ("aldrig före").
A13 | en | October 2026 | aktiv
#
# TOC-underraden för Del 3 (EP-exklusiv, ingen vaktrad — samma skäl som
# Ytdivergenser-avsnittets IMY-rad: EW har ingen motsvarande underrad att
# jämföra mot). "On-device, PCC, ChatGPT — and five policy decisions" bar
# inget om Task 8:s nya AI Act-avsnitt och är bytt till "On-device, PCC,
# ChatGPT, the EU AI Act — and five policy decisions". Sidnumren i samma
# `<li>` (`toc__page`) är ORÖRDA — de räknas om mot den omrenderade PDF:en
# i Task 13, enligt briefens uttryckliga instruktion.
#
# Byggarens sidfot (`exports/build-apple-intelligence-pdf.py`, `jobs`):
# titelsträngen är `"Apple Intelligence for teachers and school leaders"`,
# verifierad ordagrant mot den redan renderade PDF:en
# (`pdftotext -layout … | grep -c "for teachers and school leaders"` → 26
# träffar, en per sidfot). Ingen pensionerad sträng i sidfoten — den bär
# varken ett gammalt guidenamn, ett föråldrat firmanamn eller någon
# Advania-rest. Ingen ändring i byggaren.
#
# Quick-starten (`_unpublished/exports/apple-intelligence-quick-start-en.html`,
# utanför ytkonsistensvakten, se modulens egen notis ovan): fyra ändringar,
# var och en läst mot guiden, inte mot minnet.
#   1. `Siri 2.0` (rad 112, den sista kvarvarande förekomsten enligt A10:s
#      postrad) → `Siri AI`.
#   2. Siri AI-kortet (sida 1, kort 2) och "Ask Siri for Thursday's
#      schedule" (sida 2, uppgift 3) fick vardera en kort EU-notis — Siri
#      AI är blockerad i EU på iPhone och iPad, DMA angivet skäl, ingen
#      tidplan (samma sakuppgift som A15, ankaret "the EU's Digital
#      Markets Act" på de två vaktade ytorna). Observationernas punkt 1
#      pekar uttryckligen ut quick-startens "punkt 3" som obrukbar för en
#      EU-läsare utan den här notisen.
#   3. "Some features are 18+" (Watch out-rutan) → "ChatGPT access
#      requires the user to be at least 13 (or your country's minimum)" —
#      samma rättelse som A16 (18 var aldrig rätt; Apples egen gräns är 13
#      år eller landets minimiålder, och gäller specifikt ChatGPT-vägen,
#      inte funktioner i allmänhet).
#   4. Avslutningens mening skriven om med en sidantalsplatshållare,
#      INTE ett tal: "The full [PAGE_COUNT]-page <em>Apple Intelligence
#      Guide</em> comes with this quick start in the community." Talet är
#      inte känt förrän Task 13 renderat om PDF:erna; `[PAGE_COUNT]` är en
#      textmarkör (inga siffror) som Task 13 ersätter med det uppmätta
#      sidantalet utan att skriva om meningen i övrigt. Ordet `Guide` står
#      direkt efter markören, långt inom de 60 tecken `_PAGE_CLAIM` tillåter.
#      Ingen ny vaktrad: `test_every_quick_starts_page_count_claim_matches_
#      its_rendered_main_guide` läser den LEVERERADE pdf:en
#      (`_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-
#      en.pdf`), som den här uppgiften uttryckligen inte renderar om — PDF:en
#      bär alltså ännu ingen sifferträff, `NO_PAGE_CLAIM["apple-
#      intelligence"]` gäller oförändrat till Task 13 har renderat och kan
#      tömma den.
#
# Mail categorisation-, Notification summaries-, Writing Tools- och Visual
# Intelligence-korten är lästa mot guiden och lämnade orörda: ingen av dem
# gör ett påstående som motsäger A05 (öppen fråga, oförändrad), A06 (öppen
# fråga om Writing Tools delas), A07 (notissammanfattningar är fortfarande
# en legitim on-device-rad; Mail-kortet påstår inget om var det körs) eller
# A20–A22 (ingen av dem nämner en inställningsväg i quick-starten).
```
