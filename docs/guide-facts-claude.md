# Påståendeinventering — Claude-guiden

**Rundan:** Blueprint våg 2b. Spec: `docs/superpowers/specs/2026-10-08-wave-2b-claude-guide-content-design.md`
**Upprättad:** 2026-10-08

Varje volatilt faktapåstående i guiden, med alla sina förekomster över de
fyra ytorna. En post är inte klar förrän alla fyra är bockade.

Ytorna: **EW** `guides/claude/index.html` · **SW** `sv/guider/claude/index.html`
· **EP** `exports/claude-print-a4-en.html` · **SP** `exports/claude-print-a4-sv.html`

## Poster

Status för denna tabell: **inventerad, inte faktakontrollerad.** Källa+datum
och utfall är ifyllda bara för de poster som redan var avgjorda i specen
(Cowork §13, ChatGPT §14, upplagan §7, Claude Docs/Slides §14). Resten bär
placeholdern "Ej kontrollerat – Task 3" i väntan på nästa uppgift. Platser
anges som radnummer där påståendet står ordagrant; ett intervall betyder att
flera rader i samma stycke/avsnitt hör till samma påstående. `—` betyder att
påståendet inte finns alls på den ytan.

| id | påstående idag | typ | omfång | EW | SW | EP | SP | källa + datum | utfall |
|---|---|---|---|---|---|---|---|---|---|
| P01 | Plantabellens priser: Free $0 / Pro ~$20 per mo / Max $100+ per mo | pris | EN | 140–159 (tabell + fotnot) | — | 829–848 | — | Ej kontrollerat – Task 3 | Ej kontrollerat – Task 3 |
| P02 | Plantabellens priser: Free 0 kr / Pro ca 200 kr per mån / Max ca 1 000 kr+ per mån | härlett värde | SV | — | 140–159 (tabell + fotnot) | — | 829–848 | Hänger på P01 (dollarpris) OCH växelkursen — båda måste kontrolleras innan denna post rättas | Ej kontrollerat – Task 3 |
| P03 | Fotnotens ram: "Priserna stämmer per april 2026 och är omräknade från Anthropics dollarpriser" | pris | SV | — | 159 | — | 848 | Avgörs FÖRE P02: säljer Anthropic numera i kronor till satt pris? Då är hela ramen fel, inte bara siffran | Ej kontrollerat – Task 3 |
| P04 | "Chat (Sonnet)" i plantabellen under Free, plus upprepningar: "the free tier gives you access to/you get Claude Sonnet" i ekosystem-, recap- och FAQ-styckena | modellnamn | båda | 117, 143, 180, 974 | 117, 143, 180, 974 | 806, 832, 870 (ingen FAQ i print) | 806, 832, 870 | Ofastställt — release notes antyder Sonnet 4.5/5.x men är inte ordagrant läst. Ingen källa godtas förrän sidan läses direkt, se spec §14 | Ej kontrollerat – Task 3 |
| P05 | "tillgång till Opus" / "access to Opus" i plantabellen under Pro | modellnamn | båda | 149 | 149 | 838 | 838 | Ofastställt, samma krav som P04 — direktläst källa innan något skrivs | Ej kontrollerat – Task 3 |
| P06 | Cowork framställs som en egen plats/flik i Claude Desktop: hero-undertexten "Chat · Cowork · Code", ekosystemdiagrammets fyra rutor, "Cowork sits as a tab inside Claude Desktop", Del 3-rubriken, samt bildplatshållaren screenshot-cowork-tab.png ("Claude Desktop showing the Cowork tab") | gränssnitt | båda | 45 (hero), 95–113 (diagram, inkl. "NEW 2026"-märket), 119–120, 416–417, 420 (bildplatshållare) | 45, 95–113, 119–120, 416–417, 420 | 723 (TOC "Cowork · Skills · Claude Code"), 787–790 (diagram), 808–809, 1146–1147, 1150 (bild) | 723, 787–790, 808–809, 1146–1147, 1150 | claude.com/resources/articles/cowork-is-now-claude, annonserat 2026-09-16 — kontrollerat 2026-10-08, se spec §13 | Avgjort falskt: Cowork och chat slås samman till ett Claude, ingen egen flik. Skrivs om enligt väg 2 (spec §13–14), inte en radrättning — se Task 7 |
| P07 | Cowork beskrivs som Desktop-exklusivt: diagrammets "PAID ONLY"-märke, rubrikens "(paid)", "it also happens to be where Cowork lives on paid plans", FAQ:ns "(paid Desktop only)" | gränssnitt | båda | 103 (diagram), 119, 186, 1002 (FAQ) | 103, 119, 186, 1002 | 787 (diagram), 808, 876 (ingen FAQ i print) | 787, 808, 876 | support.claude.com/.../get-started-with-claude-cowork — kontrollerat 2026-10-08, se spec §13 | Avgjort falskt: webb, desktop och mobil, plus Chrome-sidopanel. Skrivs om enligt väg 2 — se Task 7 |
| P08 | Cowork sägs kräva "paid plans"/"betalda planer" utan att ange vilka — Pro, Max, Team och Enterprise särskiljs inte | gränssnitt | båda | 119–120, 149, 416–417 | 119–120, 149, 416–417 | 808–809, 838, 1146–1147 | 808–809, 838, 1146–1147 | Samma två källor som P06/P07, spec §13 | Pro och Max har sammanslagningen nu, Team och Free får den "soon" enligt källorna — texten måste antingen ange detta per plan eller skrivas så att den inte hänger på utrullningsläget. Skrivs om enligt väg 2 |
| P09 | "Cowork, Claude Code, and MCP integrations can reach into your filesystem, your email, your cloud storage" — bygger på att Cowork körs lokalt på din dator; träffar GDPR-resonemanget om var data bearbetas | gränssnitt | båda | 488 | 488 | 1237 | 1237 | support.claude.com/.../release-notes — fjärrkörning i beta sedan 2026-07-07, kontrollerat 2026-10-08, se spec §13 | Avgjort falskt för Cowork-delen: uppgifter körs i Anthropics moln, i en isolerad miljö, inte på lärarens dator. Meningen buntar ihop Cowork med Claude Code (som fortfarande är lokalt) — bara Cowork-delen är fel. GDPR-avsnittet rättas för molnkörningen, väg 2 |
| P10 | Det citerade Anthropic-stycket om Coworks arkitektur: "Claude Cowork uses the same agentic architecture that powers Claude Code, now accessible within Claude Desktop and without opening the terminal..." | gränssnitt | båda | 120, 417 | 120, 417 | 809, 1147 | 809, 1147 | claude.com/docs/cowork/overview beskriver 2026-10-08 fortfarande Cowork som "within Claude Desktop" / "Works directly on your computer" — alltså samma (föråldrade) ram som citatet, medan annonseringen och supportartikeln säger sammanslagning och moln. Källorna är inte överens med varandra, se spec §13 | Citatet är sannolikt hämtat från den sida som själv ligger efter. Skrivs om tillsammans med P06, inte citerat ordagrant längre — se Task 7 |
| P11 | "On individual plans, your conversations may be used for model training by default. Open Settings → Privacy..." samt checklistpunkten "We have reviewed Claude's privacy settings, including the opt-out for model training" | gränssnitt | båda | 161–163, 559 | 161–163, 559 | 851–852, 1323 | 851–852, 1323 | Kräver inloggning — se Q1 i frågelistan nedan | Väntar på Johans inloggade svar innan redigering, se Task 3 steg 5 |
| P12 | "Claude's Projects feature is simpler than ChatGPT's custom GPTs, which most teachers find easier to adopt" | konkurrent | båda | 979 (fråga), 981 (svar) | 979, 981 | — (ingen FAQ i print) | — | Johans beslut 2026-10-08, spec §14 — ingen källbeläggningsfråga | **Ersätts, inte beläggs.** Custom GPTs är på väg bort, så jämförelsen blir fel oavsett formulering. Skrivs om till ett påstående om vad Projects gör, utan jämförelse |
| P13 | EU AI Act-avsnittet i sin helhet: ikraftträdande 2024, infasning "through 2026 and beyond", riskdiagrammet (Unacceptable/High/Limited/Minimal), de fyra risknivåbeskrivningarna, checklistpunkten om risknivåer, FAQ:ns kortsvar | regelverk | båda | 505 (ingress), 521–549 (rubrik, stycke, diagram, fyra nivåer), 561 (checklista), 1028–1030 (FAQ) | 505, 521–549, 561, 1028–1030 | 1254 (ingress), 1273–1311 (rubrik, stycke, diagram, fyra nivåer), 1325 (checklista) | 1254, 1273–1311, 1325 | Ej kontrollerat – Task 3 | Augusti 2026 har passerat sedan guiden skrevs — infasningsläget för skolors skyldigheter behöver kontrolleras mot EU-kommissionens eget tidsschema, inte bara mot "2026 and beyond" |
| P14 | Upplaga/datumstämpeln: "Edition: First edition, April 2026" / "Pricing accurate as of April 2026" / "Updated April 2026" / kolofonens "First edition · April 2026 · © Johan Lindström" (och motsvarande svenska) | datum | båda | 159, 1057 | 159, 1057 | 690, 701, 848, 1577 | 690, 701, 848, 1577 | Johans beslut 2026-10-08, spec §7 | Blir "Second edition, October 2026" / "Andra upplagan, oktober 2026" på alla 12 förekomster inom dessa fyra ytor. **Observera:** ytterligare 2 förekomster finns i `exports/claude-guide-license-{en,sv}.html`, vilka ligger utanför denna inventerings fyra ytor (se Task 1) och hanteras separat av Task 9 |
| P15 | Artifacts-avsnittet räknar upp outputformat (Word, PDF, PowerPoint, Excel, text, HTML, Markdown) utan att nämna Claude Docs eller Claude Slides | funktionsnamn | båda | 322–324 | 322–324 | 1036–1038 | 1036–1038 | Lanserade 2026-09-16, alla planer, enligt spec §14 | **Tillägg, inte rättning.** Claude Docs och Claude Slides läggs till som väsentligt nytt i Artifacts-avsnittet |
| P16 | Rubriken "Custom Skills — your reusable teaching agents" (brödtexten använder sedan bara "Skills"/"the Skill") | funktionsnamn | båda | 436 | 436 | 1171 | 1171 | Ej kontrollerat – Task 3 | Ej kontrollerat – Task 3: kontrollera om Anthropics nuvarande produktnamn fortfarande är "Skills" (ev. "Agent Skills") och om prefixet "Custom" hör hemma i rubriken |
| P17 | Rekommendationen av Gareth Mannings GitHub-repo "claude-education-skills" som startpunkt för färdiga Skills | funktionsnamn | båda | 441 | 441 | 1181, 1571 (källförteckningen) | 1181, 1571 | Ej kontrollerat – Task 3 | Ej kontrollerat – Task 3: verifiera att repot fortfarande är aktivt på github.com/GarethManning/claude-education-skills innan omrendering |
| P18 | Omslagstaggen "Claude for Education" (EN-print) och källförteckningens "the Claude for Education and Cowork announcements" | funktionsnamn | båda | — | — | 675 (omslag), 1568 (källförteckning) | 1568 (bara källförteckningen — omslaget använder i stället "Claude inom skolsektorn") | Ej kontrollerat – Task 3 | Ej kontrollerat – Task 3: verifiera att "Claude for Education" fortfarande är Anthropics officiella programnamn |
| P19 | "Cowork, Claude Code, and MCP integrations" — termen "MCP-integrationer" för funktionen att koppla filsystem/e-post/molnlagring till Claude | funktionsnamn | båda | 488 | 488 | 1237 | 1237 | Ej kontrollerat – Task 3, låg prioritet | Ej kontrollerat – Task 3: kontrollera om Anthropics användarvända namn numera är "Connectors" snarare än "MCP" för icke-tekniska läsare |

## Frågor som kräver inloggat konto

Johan betar av. Ja/nej-frågor, inte utredningsuppdrag.

| id | frågan | svar |
|---|---|---|
| Q1 | Står `Settings → Privacy` kvar där guiden säger (rad 161–163/559 EW·SW, 851–852/1323 EP·SP), och är träningsvalet ("conversations may be used for model training by default") fortfarande på som standard på individuella planer? Ja/nej + skärmbild. | – |
| Q2 | Finns Memory-avsnittet kvar under Inställningar så som guiden beskriver (rad 346 EW/SW), och fungerar aktiveringen och granskningen av sparade minnen som beskrivet? Guiden väntar redan på en skärmbild (`screenshot-memory-settings.png`). Ja/nej + skärmbild. | – |
| Q3 | Finns någon kvarvarande "Cowork"-ingång (flik, knapp, slash-kommando) i Claude Desktop-gränssnittet i dag, efter sammanslagningen med Chat — och vad ska ersätta bildplatshållaren `screenshot-cowork-tab.png`? Ja/nej + skärmbild av det faktiska gränssnittet. | – |
| Q4 | Visar kontots plan-/modellväljare på en gratisplan i dag literally "Claude Sonnet" utan versionsnummer, eller ett annat namn (t.ex. en versionssiffra)? Ja/nej + skärmbild. | – |
| Q5 | Visar gränssnittet fortfarande "unlimited Projects" (eller motsvarande, utan angivet tak) på en Pro-plan, eller har ett numeriskt tak införts? Ja/nej + skärmbild. | – |

## Vaktblock

Läses av `scripts/tests/test_guide_surface_consistency.py`. En rad per
bevakat värde: `id | språk | exakt sträng | status`. Status `borttaget`
hoppas över — använd den när ett påstående utgått ur guiden i stället för
att radera raden, så historiken står kvar.

```guard
```
