# Blueprint — överlämning

**Senast uppdaterad:** 2026-10-09
**LÄS FÖRST** vid fortsättning. Specen är den bindande auktoriteten, planerna argumenterar från den.

---

## Var allt står just nu

| Del | Läge |
|---|---|
| **Våg 1** — sajtens färg och typografi | **MERGAD** som `851c9f5`, live på choosewise.education |
| **Spår A** — märket, favicon, Skool | **PR #29 öppen**, gren `feat/blueprint-track-a-mark`, 15 commits, ej mergad |
| **Våg 2a** — guidernas tryckmallar | **MERGAD** 2026-10-08, PR #30, merge-commit `a67a47a` (72 filer, +5977/-4577). Gate för våg 2b. |
| **Våg 2b** — guidernas innehåll | **MERGAD OCH LIVE** 2026-10-08. 44 commits på `main` (HEAD `d33a014`), pushade till origin, Pages-bygget grönt och live-sajten verifierad: åtta nya markörer på den engelska guidesidan, fyra på den svenska, **noll gamla**. Alla fyra PDF:er svarar 200 och innehåller det nya. Svit 484 passed, 0 skipped. Grenen och worktreen är borttagna. Historiken blev **linjär (fast-forward)** — till skillnad från våg 1 och 2a finns ingen merge-commit som namnger vågen; den är commits `86076ce..d33a014`. |
| Diagram- och social-exporterna | Inte påbörjad, Johans beslut: egen runda |
| Visual Codes Vol. 1–3 | Inte påbörjad, **ingen plan äger den** |

**Arbetskopian står nu på `main`.** Johan har fortfarande **26 ocommittade filer** under `exports/` och `assets/pdfs/wise/` — hans eget attributionssvep. De ska aldrig commitas av det här arbetet och överlevde hela våg 2b orörda, eftersom rundan kördes i en isolerad worktree. Bekräftat vid leverans: ingen commit i vågen rör `exports/wise`, `exports/ratt` eller `assets/pdfs/wise`.

**Fem screenshot-filer är nya sedan 2026-10-08.** Johan fotade om `screenshot-memory-settings.png` och `screenshot-projects-sidebar.png` från sitt eget Max-konto efter att slutgranskningen upptäckt att de gamla motsade texten (se Fällor nedan). Båda ligger i två identiska kopior, en per språkkatalog.

---

## Nästa steg, i ordning

1. **FÖRBUDSVAKTEN.** Johans beslut 2026-10-09: nästa runda bygger den. Egen sektion nedan med allt som behövs för att börja. Den ska finnas **före** nästa guide, för varje ny guide återanvänder mönstret och ärver annars samma blinda fläck.
2. **Johan mergar PR #29** när han sett den. Faviconen landar på 198 sidor i samma stund den mergas. (#30 — våg 2a — är redan mergad, se tabellen ovan.)
3. **De fyra återstående guiderna (Copilot, Gemini/NotebookLM, Apple Intelligence, elevguiden), bara på engelska.** Samma mönster som Claude-guiden: en inventering i `docs/guide-facts-claude.md`:s form, fakta kontrollerade mot namngiven källa, fyra ytor stämda av mot varandra. Våg 2b lämnar både mallen och ett vaktlager (nedan) som nästa runda bör återanvända — och en känd brist i det vaktlagret som är värd att stänga innan dess, se nedan.
4. **Diagram- och social-exporterna.** Åtta mallar plus SVG, PNG och PDF för WISE och RÄTT. Johans beslut 2026-10-06: egen runda, gärna ihop med märket. Sju av åtta bär hans ocommittade ändringar — han bör commita svepet först.
5. **Visual Codes Vol. 1–3** i `~/Projekt/Choosewise/visual-codes-pdf/`, utanför repot. Specen §8 räknar dem till våg 2; varken 2a:s eller 2b:s plan nämner dem. Tredje kopian av paletten.
6. **NotebookLM-dokumentet** — se "Känt trasigt" nedan.

---

## Öppna beslut som väntar på Johan

- **Paletten saknar en larmfärg.** Har nu tvingat fram kompromiss tre gånger: EU AI Act-pyramidens "Unacceptable", "Watch Out"-rutan, och quick startens DÅLIG/BÄTTRE/BÄST-rad där prickarna går grå → koppar → blå och inte läses som en progression. Ett enda nytt token löser alla tre.
- **Instrument Serif används utanför citat.** Specen §2 binder det till citat, men den delade stilmallen sätter även underrubriker, signaturer och footerns varumärkessträng i kursiv serif — för att mallarna hade Playfair italic där. Medvetet oförändrat i våg 2a; motiveringen står bara i en CSS-kommentar och borde vara ett registrerat beslut.
- **Evidence Toolkits band** "kring" vs "över": 1,54:1. Palettak sedan våg 1, inte ett förbiseende.
- **Sajtens header** bär inget märke. Spår A:s spec säger nej idag; frågan kan tas när tecknet setts i bruk.
- **Choosewise på LinkedIn:** egen sida eller Johans profil? Spår A levererar båda måtten tills det avgjorts.

---

## Känt trasigt eller begränsat

**NotebookLM-dokumentet går inte att bygga om.** `exports/build-nlm-prompts-en.py:30` läser `/tmp/nlm-prompts-en-chunk{1..4}.json`. Filerna finns inte och har aldrig committats. Enda kopiorna av innehållet är den committade HTML:en, PDF:en och docx-filen. Dokumentet **utgick ur våg 2a** av det skälet och står kvar i Crestiora-palett med Playfair. Att laga byggaren — återskapa datan, eller skriva om den att läsa den committade HTML:en som källa — är ett eget jobb. Specens §10.7 "inga Crestiora-värden i publicerade filer" är alltså inte bokstavligt sant efter merge.

**Sidfötterna sätts i Helvetica, inte Hanken Grotesk.** Playwrights `footer_template` renderas i en isolerad kontext som inte når självhostade typsnitt. Hanken Grotesk deklareras men löser inte ut. Verifierat per glyf med `pdftohtml -xml`. Att nå dit kräver typsnittet som data-URI i sidfotsmallen — eget jobb. Det som åtgärdades var det allvarliga: tidigare stod `'Inter'` där, vilket gav Times-Roman på 2,37–3,32:1.

**Tio av 22 PDF:er är inte byte-identiska vid omrendering.** Skillnaden är Chromiums `CreationDate`/`ModDate`. En omrendering visar alltså alltid tio ändrade filer i `git status` även när ingenting ändrats. Innehållet är idempotent, verifierat på alla fyra vaktlager.

**Landningssidornas "fem guider"-överdrift.** `guides/index.html` och `sv/guider/index.html` räknar upp fem guider (Copilot, Gemini/NotebookLM, Apple Intelligence, Claude, elevguiden) som att de går att hämta. `guides-en.json`/`guides-sv.json` har bara Claude som `available` — de fyra andra är opublicerade. Noterat i våg 2b:s spec som ett känt fel **utanför rundans omfång**: Johan avgjorde 2026-10-08 att "webbsidorna" i den rundan syftade på guidens egna två sidor, inte landningssidorna. Felet är alltså kvar med flit, inte missat. Extra skäl att inte glömma det: den svenska sidans stycke är i en kommentar uttryckligen skrivet för att svarsmotorer (ChatGPT m fl) ska kunna extrahera det fristående — överdriften matas alltså vidare till AI-sök också. Rimligen åtgärdas det när nästa guide publiceras och uppräkningen ändå måste stämma.

**~~En oprecis mening om AI-förordningens datum~~ — RÄTTAD 2026-10-08.** Slutgranskningen av hela grenen klassade den som Critical, inte som en oprecision: stycket motsade sig självt ("became applicable on 2 August 2026" mot "One duty is already in force since 2 February 2025") och underdrev vad som binder en skola idag. Den rättades på alla fyra ytor i en enda ändring, precis som Ruling 15 föreskrev. Texten nedan står kvar som historik över varför den parkerades.

**Historik:** EU-avsnittet säger "En skyldighet gäller redan, och har gjort det sedan den 2 februari 2025: AI-kunnighet" ("One duty is already in force, and has been since 2 February 2025: AI literacy" på engelska). Det är oprecist: det datumet var också när förbuden mot oacceptabel risk började gälla, inte bara AI-kunnighetsskyldigheten — meningen får det att låta som om AI-kunnighet är den enda skyldighet som gäller idag. Meningen är densamma (i sak) i `guides/claude/index.html:518`, `exports/claude-print-a4-en.html:1269`, `sv/guider/claude/index.html:520` och `exports/claude-print-a4-sv.html:1269`. Våg 2b:s ledger (Ruling 15) parkerade den medvetet till en senare rättning i stället för att fixa den på svenska ensamt — att rätta bara en yta hade skapat precis den fyrytedivergens rundans hela disciplin finns till för att förhindra. **Rättas i en egen, liten ändring som träffar alla fyra ytor samtidigt**, inte i förbifarten under nästa guides runda.

**En föräldralös bild.** `guides/claude/assets/screenshot-cowork-tab.png` och sin svenska kopia `sv/guider/claude/assets/screenshot-cowork-tab.png` refereras inte längre av något — Cowork-avsnittets omskrivning (Task 7, väg 2) tog bort platshållaren som pekade på den. Filerna ligger kvar på disk. Ofarligt — ingen sida länkar en trasig bild — men värt att städa bort nästa gång någon är inne i de katalogerna.

---

## Vad som vaktar vad

Fem lager. De fyra första byggdes i våg 2a; det femte i våg 2b. Ändra inget utan att veta vilket lager som äger frågan.

| Lager | Fil | Äger |
|---|---|---|
| Sidvist textfingeravtryck | `scripts/tests/test_guide_pdf_parity.py` | att ingen text flyttar sig inom eller mellan sidor |
| Dokumentnivåinvariant | `scripts/tests/test_guide_pdf_body_text.py` | att inget innehåll försvinner — kromet strippas, så ompaginering kan inte röra det |
| Renderingsvakt | `scripts/tests/test_guide_pdf_font_weights.py` | att ingen PDF bäddar in ett typsnitt över viktskalan, även när vikten kommer ur HTML och inte CSS |
| Statiska mallvakter | `test_guide_print_css.py`, `test_guide_asset_paths.py`, `test_build_scripts.py` | källan: palett, typsnitt i `font-family`-kontext, vikter, sökvägar, och att varje väljare i den delade stilmallen ligger i en SCOPE-GUARD-region med sin `.page--`-scope |
| **Ytkonsistens (nytt i våg 2b)** | `scripts/tests/test_guide_surface_consistency.py` + `scripts/tests/factinventory.py` + vaktblocket i `docs/guide-facts-claude.md` | att webb och print, på båda språken, säger samma sak om varje volatilt sakpåstående — inte bara att ingen text flyttat sig, utan att **innehållet** stämmer mellan de fyra ytorna |

**Facit ligger i `scripts/tests/fixtures/`.** Fånga aldrig om det för att få grönt. Fånga om det bara när innehållet ändrats med avsikt, och verifiera då att bara de avsedda posterna rör sig. **`scripts/tests/fixtures/capture_guide_baseline.py` tar nu en `--only RELATIV/SÖKVÄG`-flagga** (en eller flera gånger) som riktar omfångningen mot namngivna PDF:er och lämnar alla andra nycklar i de två facit-filerna exakt som de står. Den finns för att en runda som bara redigerat fyra av tjugotvå PDF:er annars tvingas välja mellan att fånga om allt (och tyst slå av vakten för de arton orörda) eller att handredigera JSON-facit för hand. `--only` gör det möjliga: fånga precis det som faktiskt ändrats.

**Ytkonsistenslagrets kända begränsning — läs innan den återanvänds på nästa guide.** Vaktblocket kan bara påstå att en exakt sträng **finns** på en yta, aldrig att den **saknas**. Ett strukit eller felaktigt påstående som skrivs tillbaka in i texten av misstag fångas alltså inte — ingen rad blir röd, eftersom raden bara letar efter det korrekta påståendet och är tyst om huruvida det felaktiga också står där. Det är en egenskap hos `surfacecheck.py` som byggd, bekräftad oberoende av en granskare under våg 2b, inte ett missat formuleringsfel. Att stänga hålet kräver en **ny radtyp** i vaktblocket — något i stil med `förbjudet`, en sträng som INTE får finnas — vilket är nytt omfång och inte gjort i den här rundan. Värt att bygga **innan** de fyra återstående guiderna tas, eftersom varje ny guide kommer att återanvända det här mönstret och ärva samma blinda fläck.

**Påståendeinventeringen är rundans auktoritet, och mallen för nästa fyra.** `docs/guide-facts-claude.md` är inte ett arbetsdokument som kan kastas efter leverans — det är källloggen specens §8 kräver, och det är **facit** som guidetexten svarar mot, inte tvärtom (se våg 2b-specens Ruling 12-liknande princip: hittas en förekomst som inte behöver ändras ska den stå kvar i tabellen med en motivering, inte strykas tyst). Samma struktur — en post per volatilt påstående, fyra ytors förekomster, typ, omfång, källa+datum, utfallstoken, plus ett separat vaktblock — är tänkt att återanvändas rakt av för Copilot-, Gemini/NotebookLM-, Apple Intelligence- och elevguiden.

---

## Förbudsvakten — nästa runda, och allt som behövs för att börja

**Problemet.** `surfacecheck.check()` kan bara påstå att en exakt sträng **finns** på en yta. Varje aktiv rad letar efter det korrekta påståendet och är tyst om huruvida det felaktiga också står där. Ett struket felaktigt påstående som skrivs tillbaka av misstag fångas alltså inte av någonting — sviten förblir grön. Bekräftat oberoende av en granskare: det är en egenskap hos modulen som byggd, inte en missad formulering.

**Varför det hastar.** Mönstret ska återanvändas på fyra guider till. Byggs vakten efteråt ärver alla fyra den blinda fläcken först.

**Datan finns redan.** Vaktblocket i `docs/guide-facts-claude.md` har **36 rader med status `borttaget`** — varenda sträng som medvetet togs ur texten under våg 2b. Det ÄR förbudslistan. Idag hoppas de raderna bara över.

**Vad som ska byggas.**

1. En ny statustoken, förslagsvis `förbjudet`, eller att `borttaget` börjar betyda "får inte finnas" i stället för "hoppa över". Det senare är gratis i datan men ändrar innebörden av 36 befintliga rader — väg det mot att en `borttaget`-rad idag också används som ren historik.
2. `surfacecheck.check()` får en gren som för varje sådan rad påstår att strängen **inte** finns på någon av språkets två ytor, med en egen problemtyp — i stil med `återinfört` — så felmeddelandet säger vad som faktiskt hänt i stället för att låna en av de tre befintliga.
3. Tester som pinnar beteendet, inklusive ett som **bryter vakten med flit** och ser den bli röd. Det är fälla 2 i den här listan och våg 2b fick två fixrundor just på tester som inte kunde fallera.

**Filer:** `scripts/tests/surfacecheck.py` (~6 rader), `scripts/tests/factinventory.py` (statusuppsättningen `_STATUSES`), `scripts/tests/test_guide_surface_consistency.py`, och vaktblockets preambel i `docs/guide-facts-claude.md`.

**En konkret återinföringsrisk att testa mot:** ordet "Cowork" står kvar överallt i guiden som legitim övergångstext. En redaktör som under utrullningen skriver tillbaka ett Cowork-stycke möter idag inget motstånd alls.

---

## Fällor som kostat tid i det här programmet

1. **En kontrastsiffra härledd ur deklarerad CSS är inte bevisad.** Chromiums print-economy-läge ändrade tyst färger i sidfotskontexten: en siffra mätt till 10,63:1 renderade i verkligheten 4,57:1 tills `print-color-adjust: exact` lades till. Pixelmät i den renderade filen. Gäller bakåt mot våg 1 och spår A.
2. **Fråga alltid: skulle det här testet bli rött om felet kom tillbaka?** Våg 1 sköt fyra tester som inte kunde fallera. Våg 2a hittade flera till — en tom parametrisering, en vakt som bara läste mellan markörer, en delsträngsmatchning. Bryt vakten med flit och se den bli röd innan du litar på den.
3. **Fingeravtryck på text är blinda för bilder.** En omrendering tappade åtta fotografier medan varje textkontroll passerade. Titta på en renderad sida.
4. **`git checkout --` på en KATALOG raderar andras ocommittade arbete.** Hände i våg 2a och kostade två av Johans filer, som gick att återskapa av tur. Namnge alltid filer du själv ändrat; kopiera undan och återställ med `cp`.
5. **`git add -A` används aldrig.** Repot har alltid ett trettiotal ocommittade filer som tillhör Johan.
6. **`build-seo-meta.py` bumpar "Last updated"** ur git-commitdatum. En körning som bara skulle lägga till länkar sätter nytt datum på sidor vars innehåll inte rörts. **Konkret i våg 2b:s slutkontroll:** en medveten körning (innehållet hade faktiskt ändrats) stämplade om 12 helt orelaterade sidor — `about/index.html`, tre blogginlägg, `guides/index.html`, `prompts/index.html` och sex till — med gamla backlog-datum (2026-05-17 till 2026-10-05) som inte har med rundan att göra, samtidigt som den **inte** rörde de två sidor rundan faktiskt ändrat (de bär ingen `last-updated`-markör alls). Alla 12 reverterades med namngiven `git checkout --` per fil innan commit. Kör skriptet, men läs varje diff — "innehållet har ändrats den här rundan" gör inte automatiskt körningen träffsäker.
7. **Generatorer äger sina filer.** `build-og-images.py` skriver om de tolv delningskorten ur en mall; en handredigering där raderas tyst vid nästa körning. Lägg ändringen i generatorn.
8. **Sajten undervisar om design** och nämner typsnittsnamn i brödtext. Vakter måste matcha i `font-family`-kontext.
9. **`/usr/bin/python3` (3.9.6) är enda interpretern** med pytest, playwright och Pillow.

10. **Innehållsförteckningens sidnummer är hårdkodade och ingen vakt ser dem.** Våg 2b:s egen ompaginering (45 → 46 sidor i ett mellanläge) gjorde 13 av 15 rader fel i BÅDA guide-PDF:erna, och ingen av de fem vakterna märkte något — de jämför PDF mot sin källa, aldrig innehållsförteckningens `toc-page-num`-literaler mot de faktiskt renderade sidorna. Slutgranskningen fångade det genom att rendera dokumentet och leta upp varje kapitel. **Varje runda som rör innehåll paginerar om.** Räkna om numren mot den renderade PDF:en som allra sista steg, och sök i **dokumentordning** — en naiv första träff matchar innehållsförteckningens egen text på sidan 3, och två rader matchar dessutom på fel senare sida. En vakt i de befintligas form vore billig och skulle skydda varje kommande guide.

11. **Bilder är en femte yta, och ingen behandlade dem som en.** Sexton textgranskningar missade att `screenshot-memory-settings.png` visade två reglage under Capabilities medan den omskrivna texten intill sa tre i ett eget avsnitt — och att dess sidomeny visade en Cowork-post i en guide byggd kring att Cowork inte längre är en plats. Inventeringens post listade styckets rad men inte bildens. **Lista bildens rad som en egen förekomst i inventeringen**, och titta på varje figur som sitter intill text rundan ändrat.

---

## Dokument

- Spec våg 1 och 2: `docs/superpowers/specs/2026-10-05-choosewise-visual-identity-design.md`
- Spec spår A: `docs/superpowers/specs/2026-10-07-choosewise-brand-mark-design.md`
- Spec våg 2b: `docs/superpowers/specs/2026-10-08-wave-2b-claude-guide-content-design.md` — §12 har verifieringstabellen, §13–14 Cowork-vägvalet
- Plan spår A: `docs/superpowers/plans/2026-10-07-track-a-brand-mark.md`
- Plan våg 2a: `docs/superpowers/plans/2026-10-05-visual-identity-wave-2a-guides.md`
- Plan våg 2b: `docs/superpowers/plans/2026-10-08-wave-2b-claude-guide-content.md` — sexton uppgifter med grinden efter uppgift 6
- **Våg 2b:s ledger finns inte kvar.** Den låg i worktreen `.worktrees/wave-2b/.superpowers/` och försvann när arbetsytan togs bort vid leverans, enligt processen. De arton rulings som togs under körningen redovisades för Johan i chatten; de som överlever rundan är inarbetade i det här dokumentet som principer — framför allt att inventeringen är auktoriteten texten svarar mot (ett fynd som inte behöver ändras står kvar i tabellen med en motivering, aldrig struket tyst), och att en faktamening utan post i inventeringen inte får skrivas.
- Påståendeinventeringen, Claude-guidens facit och mall för nästa fyra: `docs/guide-facts-claude.md`
- Märkets bruksregler: `docs/brand-mark-usage.md`
- Beslutsloggar och PR-texter: `~/Desktop/choosewise-spar-a-forslag/`
- PDF:erna att titta på: `~/Desktop/choosewise-guider-vag2a/` (kopior — kan vara inaktuella)
