# Påståendeinventering — Copilot-guiden

**Rundan:** Copilot-guiden, internationell omriktning. Spec: `docs/superpowers/specs/2026-10-09-copilot-guide-international-design.md`
**Upprättad:** 2026-10-09
**Faktakontrollerad:** (Task 4)

Varje volatilt faktapåstående i de **engelska** ytorna, med alla sina
förekomster. De svenska ytorna ingår inte i rundan (spec §5) och har därför
inga poster.

Ytorna: **EW** `_unpublished/guides/copilot/index.html` · **EP**
`_unpublished/exports/copilot-print-a4-en.html` · **QS**
`_unpublished/exports/copilot-quick-start-en.html`

**QS står utanför ytkonsistensvakten** — avsiktligt, spec §7: quick-starten är
en tredje yta med egen, kortare formulering, och kravet "ordagrant på alla
ytor" vore rött från dag ett och därmed värdelöst. Den bevakas i stället av
förekomstkolumnen här, av PDF-facit, och av leveransvakten
(`scripts/tests/test_copilot_delivery.py`).

## Hur källorna läses

Varje sida hämtas som rå HTML och läses ordagrant; texten extraheras lokalt ur
markupen. Ingen sida sammanfattas av ett annat modellanrop, och en
sammanfattning är aldrig källa till ett värde. Där källor går emot varandra
står båda, och den nyare vinner — med noteringen att de skiljer sig.

## Poster

(Task 3 fyller tabellen, Task 4 kolumnerna källa och utfall.)

| id | påstående idag | typ | EW | EP | QS | källa + datum | utfall |
|---|---|---|---|---|---|---|---|
| C01 | SKU-tabellens fyra produktnamn och fyrdelade struktur: "Copilot (free web)", "Copilot Chat (with work/school account)", "Copilot Pro", "Microsoft 365 Copilot" | produktnamn | 94–129 (tabellen; namnen på rad 105, 111, 117, 123); omskrivna i Licensing-avsnittet 409–414 och sidenote 166 | 692–727 (tabell 1; namnen på 703, 709, 715, 721) och 1166–1196 (tabell 2; namnen på 1176, 1181, 1186, 1191); sammanfattningen 823–825 | — (ingen SKU-tabell, bara funktionslistan) | | |
| C02 | Priset "~kr 350/user/mo" / "kr 350 per user per month" för Microsoft 365 Copilot | pris | 126, 414, 448 | 724, 1055, 1193, 1198, 1235, 1254 | — | | |
| C03 | "Commercial Data Protection" (CDP) som namn, definition och omfång — tre kontraktspåståenden plus tre ärliga kvalifikationer | produktnamn | 7, 9, 14, 83, 131, 145–159 (hela förklaringsrutan "The distinction that matters"), 190, 203, 233, 380, 411, 413, 448 | 590, 653, 669, 683, 767–778 (förklaringsruta 1), 788–800 (förklaringsruta 2, "What CDP is not"), 1050, 1094, 1115, 1261 | 106 (bara förkortningen "CDP"; namnet skrivs inte ut) | | |
| C04 | Åldersgolvet "13" (EW) / "13+" (EP) för Copilot med arbets-/skolkonto | åldersgräns | 420, 422 | 1094, 1209, 1211, 1217 | — | | |
| C05 | URL:en copilot.microsoft.com som den fria konsumentytan | URL | 91, 105, 158, 203, 398, 399, 411, 448, 455, 483, 490 | 665, 703, 729, 1060 | 190 | | |
| C06 | URL:en learn.microsoft.com som hjälpkälla för CDP/EU Data Boundary-dokumentation | URL | 504 (skriver ut namnet "Microsoft Learn portal", ingen literal URL) | 1310 (literal URL "learn.microsoft.com/copilot") | — | | |
| C07 | "EU Data Boundary" som produktfunktion (data residency) och dess täckningsgrad ("most"/"overwhelming majority") | funktion | 154, 156, 380, 402, 403, 405, 428, 490, 504 | 633, 653, 775, 797, 799, 1094, 1144, 1146, 1148, 1231, 1237 | — | | |
| C08 | De sex funktionernas namn i del 2: Copilot Chat, Copilot in Word, Copilot in Outlook, Copilot in Teams, Copilot in PowerPoint, Copilot Pages | funktion | 189, 219, 249, 279, 309, 339 | 850, 884, 920, 953, 988, 1021 | 105, 112, 119, 126, 133, 140 | | |
| C09 | Datumstämpeln "April 2026" / "Updated April 2026" | datumstämpel | 49, 156, 422, 525 | 602, 671, 1217, 1324 | 190 | | |
| C10 | Omslagets rubriktext "A practical guide for Swedish schools" | inramning | — (hero-ledet rad 46 nämner inte Sverige) | 590 | — | | |
| C11 | FAQ-posten "Is Copilot available in Swedish?" | inramning | 460–463 | 1266–1269 | — | | |
| C12 | Skolverket-exemplen i prompterna (läroplansdokument-exemplet och staff-guideline-exemplet) | inramning | 196 | 857, 1233 | — | | |
| C13 | "Swedish-English parallel version" / student-vänlig "Swedish rewrite" i exemplen (Word och PowerPoint) | inramning | 228, 316 | 892, 995 | — | | |
| C14 | Den rättsliga analysen: GDPR-artiklar (6, 9), Schrems II, DPIA-resonemang, SCC/EU-US Data Privacy Framework | inramning | 152, 154, 380, 387–394, 401–405, 428, 469, 490, 504 | 771, 773, 775, 777, 789–799, 1094, 1115–1119, 1144–1156, 1213, 1217, 1231, 1261, 1275, 1296, 1310 | — | | |
| C15 | Reader-responsibility-noten med Sverige, Skolverket, IMY och de fyra namngivna länderna (UK, Frankrike, Tyskland, Nederländerna) | inramning | 422, 469, 504 | 671, 1217 | — | | |
| C16 | Avslutningens CTA: "I offer consulting for schools, primarily in Sweden." | inramning | 504 | — (motsvarande FAQ/closing nämner inte Sverige) | — | | |
| C17 | Innehållsförteckningens sex sidnummer | datumstämpel | — | 617, 623, 629, 635, 641, 647 | — | | |
| C18 | EP:s Copilot Chat-exempel "Tone-rewriting a parent email" nämner "a parent with Swedish as a second language"; EW:s motsvarande exempel gör det inte | inramning | — (motsvarande exempel rad 197 nämner inte Swedish) | 858 | — | | |
| C19 | URL:en copilot.cloud.microsoft som den CDP-skyddade arbets-/skolkontovägen | URL | 91, 138, 140, 150, 190, 208, 358, 398, 399, 448 | 744, 752, 830, 877, 1063 | — | | |
| C20 | De namngivna adminverktygen "Microsoft Entra" och "Copilot Control System" för att styra funktionsåtkomst | produktnamn | 497 | — (motsvarande FAQ-svar rad 1301–1304 namnger ingetdera) | — | | |
| C21 | Det citerade adminfunktionsnamnet "Access Protection for Copilot" (blockering av konsumentdomänen) | produktnamn | 399 | — (motsvarande stycke rad 1132 namnger ingen specifik kontroll) | — | | |
| C22 | EP:s Teams-processing-callout nämner "In Sweden, recording human voice without consent is a GDPR concern"; EW:s motsvarande callout gör det inte | inramning | — (motsvarande callout rad 293 nämner inte Sverige/GDPR) | 977 | — | | |
| C23 | "Copilot Studio" som produktnamn (lågkodsmiljön för agenter, nämnd men utanför guidens scope; även nämnd i EW:s svenska-FAQ och EP:s connector-stycke) | produktnamn | 165, 462 | 795, 817 | — | | |
| C24 | "New Outlook for Mac" / "Legacy Outlook" som produktnamn i Outlook-funktionens Mac-not | produktnamn | 274 | — (EP saknar per-funktion Mac-noter helt) | — | | |
| C25 | Antalet FAQ-frågor, uttryckt som "Nine questions teachers ask" (TOC) / "Nine of the questions..." (FAQ-ledet) | datumstämpel | — (rubriken "Questions teachers ask" anger inget antal) | 639, 1247 | — | | |
| C26 | Den enstaka hänvisningen till "alignment with the EU AI Act" i "Where do I get help"-FAQ:n | inramning | 504 | — | — | | |

### Anmärkningar till enskilda poster

- **C01/C03 överlappar delvis**: C01 äger SKU-tabellernas identitet och struktur; C03 äger CDP som namngivet begrepp. Samma rader (t.ex. EW 411, 413) bär båda påståendena eftersom tabellraden namnger en SKU *och* säger om den har CDP.
- **C03/C14 överlappar delvis**: EP 771–777 (förklaringsruta 1) definierar CDP:s tre kontraktspåståenden, varav ett ("DPA", "controller") redan är juridiskt språk. C14 äger specifikt de GDPR-artikelhänvisningarna, Schrems II-resonemanget och DPIA-formuleringarna; C03 äger CDP-definitionen som sådan. Vid omskrivning enligt rundans väg (CDP kvar, juridisk analys bort) måste båda posterna läsas tillsammans för samma stycken.
- **C07/C14 överlappar delvis**: EW 401–405 och EP 1144–1156 blandar "EU Data Boundary som funktion" (C07, ska kunna överleva) med Schrems II-resonemang (C14, ska bort enligt rundans väg). Samma radintervall står under båda id:n med denna not.
- **C04:** ordvalet skiljer mellan ytorna redan idag — EW skriver bara "13", EP skriver "13+". Det är en befintlig ytinkonsekvens, inte en produkt för Task 4 att välja mellan utan ett observandum för Task 5.
- **C06:** samma hjälpkälla beskrivs med olika precision per yta — EW namnger bara "the Microsoft Learn portal" (inget URL), EP skriver ut "learn.microsoft.com/copilot". En rättning av URL:en (om den har bytt) träffar bara EP ordagrant; EW:s formulering kräver en egen bedömning.
- **C17:** sidnumren är en direkt konsekvens av innehållsmängden i varje del. Eftersom rundans väg krymper del 3 (juridisk analys bort, ersatt av en kort ruta) kommer sidnumren med stor sannolikhet att behöva räknas om även om inget annat i TOC-posten ändras i sak.
- **C25:** medtagen enligt samma logik som C17 — ett uttryckligt antal i löptext som blir fel om FAQ-listan krymper eller växer när C11/C15 redigeras. Lägre säkerhet än C17, men riskerar att bli en obevakad regression om den inte finns med.
- **C26:** en enda, ospecifik mening utan datum eller nivåer (jämför med Claude-guidens utförliga EU AI Act-avsnitt). Tas med för fullständighetens skull, men kan mycket väl landa på "kräver ingen ändring" i Task 4 eftersom den inte påstår något kontrollerbart.

## Observationer utanför posterna

(Task 4.)

Sådant som övervägdes men **inte** gavs en egen post, med skäl:

- **"Four SKUs" / "four different products" / "six features" / "five policy decisions"** — upprepade räkneord i löptext (EW 90, 92, 181, 380, 409, 425; EP 653, 690, 825, 843, 1094, 1108, 1164, 1226; QS 93, 99) som bara återspeglar innehåll som redan är poster (C01, C08) eller som är rent redaktionellt (listlängder satta av författaren, inte av Microsoft eller av svensk inramning). De ändras automatiskt om C01/C08:s underliggande innehåll ändras, och behöver därför ingen egen bevakning.
- **Jämförelser med Claude, Gemini och Apple Intelligence** (EW 474–476; EP 791, 1046, 1073, 1280–1282) — nämns utan versionsnummer, pris eller specifika sakuppgifter om de andra produkterna. Inget kontrollerbart påstående om en tredje produkt att rätta; själva jämförelsens poäng (Copilot är starkast i Microsoft-stacken, svagare för öppet tänkande) är Johans redaktionella ställningstagande, inte ett faktapåstående om Claude/Gemini/Apple.
- **"Intune, Jamf, Mosyle" som exempel på MDM-leverantörer** (EW 504) — generisk branschreferens, ingen specifik produktversion eller prisuppgift som kan ha åldrats.
- **Tidsuppskattningar** ("thirty minutes it takes to configure", EW 399; "A 30-minute standing calendar entry", EW 431/EP 1237) — redaktionella uppskattningar, inte Microsoft-fakta.

## Vaktblock

Semantiken är den som gäller sedan 2026-10-09: `aktiv` kräver att strängen
står ordagrant på **båda** de engelska guideytorna (EW + EP), `borttaget` att
den **inte** står på någon av dem. Varje påstående rundan stryker eller rättar
får en `borttaget`-rad — den är det enda som hindrar att rättningen tas
tillbaka.

```guard
# Fylls i Task 10. Tills blocket har rader hoppar de parametriserade
# vakterna över copilot, och Task 13 kräver 0 skipped i sviten — så ett
# tomt block kan inte överleva rundan.
```
