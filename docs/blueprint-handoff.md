# Blueprint — överlämning

**Senast uppdaterad:** 2026-10-12 (Copilot-guiden MERGAD som `26c661a`; **Gemini-guiden LEVERERAD på gren, PR ej öppnad**)
**LÄS FÖRST** vid fortsättning. Specen är den bindande auktoriteten, planerna argumenterar från den.

---

## Var allt står just nu

| Del | Läge |
|---|---|
| **Våg 1** — sajtens färg och typografi | **MERGAD** som `851c9f5`, live på choosewise.education |
| **Spår A** — märket, favicon, Skool | **PR #29 öppen**, gren `feat/blueprint-track-a-mark`. Omarbetad 2026-10-09 efter Johans beslut: `main` inmergad (noll konflikter), underrubriken ändrad, og-korten utan märket. Svit 743. |
| **Våg 2a** — guidernas tryckmallar | **MERGAD** 2026-10-08, PR #30, merge-commit `a67a47a` (72 filer, +5977/-4577). Gate för våg 2b. |
| **Våg 2b** — guidernas innehåll | **MERGAD OCH LIVE** 2026-10-08. 44 commits på `main` (HEAD `d33a014`), pushade till origin, Pages-bygget grönt och live-sajten verifierad: åtta nya markörer på den engelska guidesidan, fyra på den svenska, **noll gamla**. Alla fyra PDF:er svarar 200 och innehåller det nya. Svit 484 passed, 0 skipped. Grenen och worktreen är borttagna. Historiken blev **linjär (fast-forward)** — till skillnad från våg 1 och 2a finns ingen merge-commit som namnger vågen; den är commits `86076ce..d33a014`. |
| **Copilot-guiden** — första av de fyra | **MERGAD 2026-10-11** som merge-commit `26c661a` (PR #38, 28 commits). Grenen och worktreen borttagna. Leveransen: två engelska PDF:er i `_unpublished/assets/pdfs/guides/`, ingenting publicerat. Svit 757 passed (plus elva miljöberoende fel, se nedan). |
| **Gemini Notebook** — andra av de fyra | **LEVERERAD PÅ GREN 2026-10-12.** Gren `feat/gemini-guide-international`, worktree `.worktrees/gemini-guide-international`, avstamp `main` = `e2282b7`. Sjutton uppgifter (1–16B plus 17), alla granskade. Leverans: `_unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf` (**44 sidor**) och `gemini-notebook-quick-start-en.pdf` (2 sidor), till Skool-communityt. **Ingenting publicerat på sajten.** Svit **795 passed, 1 failed, 0 skipped, 0 xfailed, 0 xpassed** med `test_prompt_pdf_parity.py` undantagen — det enda felet är det preexisterande `test_brand_mark.py::test_the_page_count_is_what_we_think` (199 mot 198), som kom med blogg-mergen PR #40 och faller likadant på `main`. **Grenen är inte pushad och ingen PR är öppnad** — det görs efter Johans besked. **Specens PR #39 mergas före eller tillsammans med rundans PR**: planen argumenterar från specen, och en mergad plan utan mergad spec lämnar en hängande korsreferens. Se **"Gemini-guiden — vad rundan lämnar"** nedan. |
| Diagram- och social-exporterna | Inte påbörjad, Johans beslut: egen runda |
| Visual Codes Vol. 1–3 | Inte påbörjad, **ingen plan äger den** |

**Arbetskopian står nu på `main`.** Johan har fortfarande **26 ocommittade filer** under `exports/` och `assets/pdfs/wise/` — hans eget attributionssvep. De ska aldrig commitas av det här arbetet och överlevde hela våg 2b orörda, eftersom rundan kördes i en isolerad worktree. Bekräftat vid leverans: ingen commit i vågen rör `exports/wise`, `exports/ratt` eller `assets/pdfs/wise`.

**Fem screenshot-filer är nya sedan 2026-10-08.** Johan fotade om `screenshot-memory-settings.png` och `screenshot-projects-sidebar.png` från sitt eget Max-konto efter att slutgranskningen upptäckt att de gamla motsade texten (se Fällor nedan). Båda ligger i två identiska kopior, en per språkkatalog.

---

## Nästa steg, i ordning

1. **~~FÖRBUDSVAKTEN~~ — BYGGD 2026-10-09.** Klar och grön före nästa guide, precis som avsett. Se egen sektion nedan för vad den gör och hur en ny guide använder den. **PR #31 öppen**, gren `feat/blueprint-forbidden-guard`, 3 commits, svit 489. Arbetskopian står på grenen.
2. **Johan mergar PR #29** när han sett den. Faviconen landar på 198 sidor i samma stund den mergas — sajten har noll favicon-taggar i dag, så det är jordgloben som byts ut, inte ett märke som byts mot ett annat. **Symbolens omfång är beskuret 2026-10-09:** Skool, LinkedIn-sidan och faviconen, men **inte** og-delningskorten och inte sajtens header. (#30 — våg 2a — är redan mergad, se tabellen ovan.)
3. ~~**COPILOT-GUIDEN — specen är godkänd, planen är nästa steg.**~~ **LEVERERAD 2026-10-10.** Fjorton uppgifter körda på `feat/copilot-guide-international` (28 commits), **PR #38** öppen och väntar på Johans slutgranskning + push. Läs `docs/superpowers/specs/2026-10-09-copilot-guide-international-design.md` för vad som avgjordes 2026-10-09; läs sektionen **"Copilot-guiden — vad rundan lämnar"** nedan för vad rundan faktiskt levererade, vad vaktlagret nu äger, det svenska divergensläget och vad som medvetet inte åtgärdades. Copilot var pilot; de tre andra guiderna (Gemini/NotebookLM, Apple Intelligence, elevguiden) tas i egna rundor med den här som mall.

4. ~~**De fyra återstående guiderna**, bara på engelska.~~ Ersatt av punkt 3 — en guide i taget, Johans beslut 2026-10-09. Den ursprungliga formuleringen: Samma mönster som Claude-guiden: en inventering i `docs/guide-facts-claude.md`:s form, fakta kontrollerade mot namngiven källa, fyra ytor stämda av mot varandra. Våg 2b lämnar både mallen och ett vaktlager (nedan) som nästa runda bör återanvända, och vaktlagrets kända brist är stängd sedan 2026-10-09 — mönstret kan nu kopieras rakt av utan att ärva en blind fläck.
3b. ~~**GEMINI-GUIDEN — specen är godkänd, planen är nästa steg.**~~ **LEVERERAD PÅ GREN 2026-10-12.** Sjutton uppgifter körda på `feat/gemini-guide-international`, alla granskade. **Vad rundan levererade:** två engelska PDF:er byggda ur rättat innehåll (`gemini-notebook-guide-en.pdf`, 44 sidor, och `gemini-notebook-quick-start-en.pdf`), den svenska inramningen generaliserad, GDPR på artikelnivå ersatt av en jurisdiktionsneutral ruta i huvudflödet, AI Act kvar och **rättad på fyra punkter** mot Claude-inventeringens post P13, bonuskapitlets skylt skärpt, en inventering på **50 poster** med **87 vaktrader** i `docs/guide-facts-gemini.md`, och **två vaktlager generaliserade** (TOC-vakten och leveransvakten) i stället för kopierade. **Plus det ingen plan förutsåg:** Google hade döpt om NotebookLM till **Gemini Notebook** 2026-07-16, tre månader efter guidens datumstämpel — 205 förekomster, titeln, den tryckta URL:en och filnamnen, Johans beslut vid grinden. **Nästa steg:** Johan läser, sedan pushas grenen och PR:en öppnas; specens PR #39 mergas före eller med den. Läs **"Gemini-guiden — vad rundan lämnar"** nedan före nästa guide.

4. **Diagram- och social-exporterna.** Åtta mallar plus SVG, PNG och PDF för WISE och RÄTT. Johans beslut 2026-10-06: egen runda, gärna ihop med märket. Sju av åtta bär hans ocommittade ändringar — han bör commita svepet först.
5. **Visual Codes Vol. 1–3** i `~/Projekt/Choosewise/visual-codes-pdf/`, utanför repot. Specen §8 räknar dem till våg 2; varken 2a:s eller 2b:s plan nämner dem. Tredje kopian av paletten.
6. **NotebookLM-dokumentet** — se "Känt trasigt" nedan.

---

## Öppna beslut som väntar på Johan

- **Paletten saknar en larmfärg.** Har nu tvingat fram kompromiss tre gånger: EU AI Act-pyramidens "Unacceptable", "Watch Out"-rutan, och quick startens DÅLIG/BÄTTRE/BÄST-rad där prickarna går grå → koppar → blå och inte läses som en progression. Ett enda nytt token löser alla tre.
- **Instrument Serif används utanför citat.** Specen §2 binder det till citat, men den delade stilmallen sätter även underrubriker, signaturer och footerns varumärkessträng i kursiv serif — för att mallarna hade Playfair italic där. Medvetet oförändrat i våg 2a; motiveringen står bara i en CSS-kommentar och borde vara ett registrerat beslut.
- **Evidence Toolkits band** "kring" vs "över": 1,54:1. Palettak sedan våg 1, inte ett förbiseende.
- **Sajtens header** bär inget märke. Spår A:s spec säger nej idag; frågan kan tas när tecknet setts i bruk.
- ~~**Choosewise på LinkedIn:** egen sida eller Johans profil?~~ **AVGJORT 2026-10-09: egen sida.** Den personliga bannern används inte — Johans profil behåller sin egen avsändare. Sidan skapas nu för att säkra namnet, men posterna fortsätter från profilen tills Skool öppnar. Båda måtten ligger kvar committade.
- **De tre återstående guiderna** (Gemini/NotebookLM, Apple Intelligence, elevguiden) tas i egna rundor, en guide i taget, med Copilot-rundan som mall. Vaktlagret är redan guide-agnostiskt (se "Copilot-guiden — vad rundan lämnar" nedan) — nästa runda fyller två dict:ar och skriver en inventering, den behöver inte ändra vakten själv.
- **De svenska Copilot- OCH Gemini-ytorna** står kvar med gamla fakta och svensk inramning, och **frågan är densamma för båda.** Copilot: `_unpublished/exports/copilot-print-a4-sv.html`, `copilot-quick-start-sv.html`, `_unpublished/sv/guider/copilot/` — junifakta. Gemini: `_unpublished/exports/gemini-notebooklm-print-a4-sv.html`, `gemini-notebooklm-quick-start-sv.html`, `_unpublished/sv/guider/gemini-notebooklm/` — **aprilfakta, och de säger fortfarande NotebookLM.** Båda guidernas svenska PDF:er är byte-identiska mot före sin runda (mätt med md5 mot bascommiten, och vaktat av `test_guide_delivery.py`). **De två språken divergerar nu i sak, inte bara i formulering** — det är ett känt, avsiktligt läge, inte en upptäckt som väntar. Om och när de svenska ytorna ska hämta in de engelska är Johans beslut, inte avgjort än. **Gemini-fallet bär dessutom tre följdfrågor** som avgörs i samma svep: de svenska filnamnen (`gemini-notebooklm-*`, se namnbytet nedan), den svenska quick-startens "39-sidiga" om en 42-sidig svensk guide, och den osynliga axeletiketten som bara kan lagas på alla fyra ytor samtidigt.
- **Fyra frågor i Gemini-guiden väntar på Johan, inte på en källa** — alla preexisterande, alla med detaljer och sidnummer i "Gemini-guiden — vad rundan lämnar" nedan: **(1)** tre passager står dubblerat och en fjärde (Fristadsskolan) står tre gånger — avduplicering är ett redaktionellt pass på hans egen text, inte en faktarättelse; **(2)** författaren omtalas både som "Johan" och som "I" i samma dokument; **(3)** bonuskapitlets "pre-market obligations" lägger plikter på skolan som i huvudsak faller på *leverantören* — att rätta det kräver en källa ingen hämtat; **(4)** titeln `Gemini & Gemini Notebook for teachers and school leaders` och omslagets eyebrow `Gemini · Gemini Notebook for education`, som stammar.
- **Tre beslut ur Gemini-rundan som Johan bör veta att han tog**, så att nästa guide inte tar dem om: **(1)** namnbytet NotebookLM → Gemini Notebook omfattar **allt, även filnamnen** (inte bara prosa och titel); **(2)** det källbelagda svenska praktikexemplet (Fristadsskolan i Eskilstuna) **stannar** i den internationella guiden, med en post och en utskriven motivering; **(3)** bonuskapitlet tar in **emotion recognition** i utbildningsinstitutioner och kommissionens egen högriskformulering om tillträde till utbildning, men **inte förbud 9** (nudification-appar) — kapitlet stannar vid "vad gäller dina verktyg och din skola".

---

## Känt trasigt eller begränsat

**NotebookLM-dokumentet går inte att bygga om.** `exports/build-nlm-prompts-en.py:30` läser `/tmp/nlm-prompts-en-chunk{1..4}.json`. Filerna finns inte och har aldrig committats. Enda kopiorna av innehållet är den committade HTML:en, PDF:en och docx-filen. Dokumentet **utgick ur våg 2a** av det skälet och står kvar i Crestiora-palett med Playfair. Att laga byggaren — återskapa datan, eller skriva om den att läsa den committade HTML:en som källa — är ett eget jobb. Specens §10.7 "inga Crestiora-värden i publicerade filer" är alltså inte bokstavligt sant efter merge.

**Sidfötterna sätts i Helvetica, inte Hanken Grotesk.** Playwrights `footer_template` renderas i en isolerad kontext som inte når självhostade typsnitt. Hanken Grotesk deklareras men löser inte ut. Verifierat per glyf med `pdftohtml -xml`. Att nå dit kräver typsnittet som data-URI i sidfotsmallen — eget jobb. Det som åtgärdades var det allvarliga: tidigare stod `'Inter'` där, vilket gav Times-Roman på 2,37–3,32:1.

**Tio av 22 PDF:er är inte byte-identiska vid omrendering.** Skillnaden är Chromiums `CreationDate`/`ModDate`. En omrendering visar alltså alltid tio ändrade filer i `git status` även när ingenting ändrats. Innehållet är idempotent, verifierat på alla fyra vaktlager.

**Landningssidornas "fem guider"-överdrift.** `guides/index.html` och `sv/guider/index.html` räknar upp fem guider (Copilot, Gemini/NotebookLM, Apple Intelligence, Claude, elevguiden) som att de går att hämta. `guides-en.json`/`guides-sv.json` har bara Claude som `available` — de fyra andra är opublicerade. Noterat i våg 2b:s spec som ett känt fel **utanför rundans omfång**: Johan avgjorde 2026-10-08 att "webbsidorna" i den rundan syftade på guidens egna två sidor, inte landningssidorna. Felet är alltså kvar med flit, inte missat. Extra skäl att inte glömma det: den svenska sidans stycke är i en kommentar uttryckligen skrivet för att svarsmotorer (ChatGPT m fl) ska kunna extrahera det fristående — överdriften matas alltså vidare till AI-sök också. Rimligen åtgärdas det när nästa guide publiceras och uppräkningen ändå måste stämma.

**~~En oprecis mening om AI-förordningens datum~~ — RÄTTAD 2026-10-08.** Slutgranskningen av hela grenen klassade den som Critical, inte som en oprecision: stycket motsade sig självt ("became applicable on 2 August 2026" mot "One duty is already in force since 2 February 2025") och underdrev vad som binder en skola idag. Den rättades på alla fyra ytor i en enda ändring, precis som Ruling 15 föreskrev. Texten nedan står kvar som historik över varför den parkerades.

**Historik:** EU-avsnittet säger "En skyldighet gäller redan, och har gjort det sedan den 2 februari 2025: AI-kunnighet" ("One duty is already in force, and has been since 2 February 2025: AI literacy" på engelska). Det är oprecist: det datumet var också när förbuden mot oacceptabel risk började gälla, inte bara AI-kunnighetsskyldigheten — meningen får det att låta som om AI-kunnighet är den enda skyldighet som gäller idag. Meningen är densamma (i sak) i `guides/claude/index.html:518`, `exports/claude-print-a4-en.html:1269`, `sv/guider/claude/index.html:520` och `exports/claude-print-a4-sv.html:1269`. Våg 2b:s ledger (Ruling 15) parkerade den medvetet till en senare rättning i stället för att fixa den på svenska ensamt — att rätta bara en yta hade skapat precis den fyrytedivergens rundans hela disciplin finns till för att förhindra. **Rättas i en egen, liten ändring som träffar alla fyra ytor samtidigt**, inte i förbifarten under nästa guides runda.

**En föräldralös bild.** `guides/claude/assets/screenshot-cowork-tab.png` och sin svenska kopia `sv/guider/claude/assets/screenshot-cowork-tab.png` refereras inte längre av något — Cowork-avsnittets omskrivning (Task 7, väg 2) tog bort platshållaren som pekade på den. Filerna ligger kvar på disk. Ofarligt — ingen sida länkar en trasig bild — men värt att städa bort nästa gång någon är inne i de katalogerna.

**`test_prompt_pdf_parity.py`:s elva fel är miljöberoende, inte Copilot-rundans.** Facit för fem prompt-PDF:er (`teachers-en`, `principals-en`, `matematik-sv`, `larare-sv`, `skolchefer-sv`) ligger i `/tmp/pdf-parity-before/`, ett maskinlokalt scratch-facit som testets egen docstring dokumenterar och som macOS tömde vid midnatt 2026-10-10. Verifierat, inte antaget, i Task 14: samma elva fel reproducerar på `main` i huvudkopian, och Copilot-rundan ändrar noll prompt-PDF:er. **Eget, litet jobb:** lägg facit där git ser det, eller låt testet skippa högljutt när katalogen är tom i stället för att falla rött utan motivering varje gång klockan slår midnatt.

**Ungefär trettio platskolumner i `docs/guide-facts-copilot.md`:s EW-kolumn ligger nu fel med ett.** Radnumren för webbytan (`_unpublished/guides/copilot/index.html`) fixerades i Task 4/8, men commit `16bd50f` senare i rundan lade till en nettorad i samma fil (74 insättningar mot 73 raderingar) utan att platskolumnen räknades om. EP-kolumnen (print) är opåverkad — samma commit var nettonoll där (104 mot 104). **Ofarligt för vakten:** `surfacecheck`/`factinventory` matchar strängar, aldrig radnummer — felet syns bara för en människa som läser cellen. Rättas när någon redan är inne i tabellen av ett annat skäl.

**Gemini-guidens kända trasiga står samlat i sitt eget avsnitt.** Sex fynd rundan medvetet inte åtgärdade (bl a en osynlig axeletikett på alla fyra ytor och fyra dubblerade passager), tre kända luckor, och namnbytets kvarvarande skuld med radnummer — allt i **"Gemini-guiden — vad rundan lämnar"** nedan. Ingen av dem är ny med rundan; alla är preexisterande och alla har sin motivering utskriven.

**Webbytans ankar-id:n `p1-edp`/`p3-edp` skiljer sig nu från den svenska spegelns `p1-cdp`/`p3-cdp`.** Namnbytet Commercial Data Protection → Enterprise data protection (se faktafynden nedan) följde med in i den engelska sidans id-strängar; den svenska filen rördes inte (spec §5) och behöll `cdp`. **Noll inkommande länkar** till något av de fyra id:na, verifierat. Värt att veta innan någon länkar till ett specifikt avsnitt i någon av guiderna.

---

## Vad som vaktar vad

Fem lager. De fyra första byggdes i våg 2a; det femte i våg 2b. Två till — leveransvakten och innehållsförteckningsvakten — tillkom i Copilot-rundan 2026-10-10 och **blev guide-agnostiska i Gemini-rundan 2026-10-12**. Ändra inget utan att veta vilket lager som äger frågan.

**Fyra av lagren är i dag guide-agnostiska, och det är den viktigaste meningen i det här avsnittet för nästa guide:** ytkonsistensvakten, inventeringen, TOC-vakten och leveransvakten tar alla en guide som argument. **Nästa guide fyller fyra kartor och skriver en inventering. Den behöver inte ändra en enda vakt.** Vilka fyra kartor, och vad var och en kräver, står i "Gemini-guiden — vad rundan lämnar" nedan.

| Lager | Fil | Äger |
|---|---|---|
| **Rendering i webbläsare (nytt 2026-10-09)** | `scripts/tests/test_responsive_overflow.py` | att ingen Evidence-sida scrollar i sidled vid 320/390/768/1024 px, och att bandpillret inte spricker ut i fem rader. Sviten var helt statisk före det, vilket är exakt varför överflödsregressionen gick igenom |
| Sidvist textfingeravtryck | `scripts/tests/test_guide_pdf_parity.py` | att ingen text flyttar sig inom eller mellan sidor |
| Dokumentnivåinvariant | `scripts/tests/test_guide_pdf_body_text.py` | att inget innehåll försvinner — kromet strippas, så ompaginering kan inte röra det |
| Renderingsvakt | `scripts/tests/test_guide_pdf_font_weights.py` | att ingen PDF bäddar in ett typsnitt över viktskalan, även när vikten kommer ur HTML och inte CSS |
| Statiska mallvakter | `test_guide_print_css.py`, `test_guide_asset_paths.py`, `test_build_scripts.py` | källan: palett, typsnitt i `font-family`-kontext, vikter, sökvägar, och att varje väljare i den delade stilmallen ligger i en SCOPE-GUARD-region med sin `.page--`-scope |
| **Ytkonsistens (nytt i våg 2b, guide-agnostiskt sedan Copilot-rundan)** | `scripts/tests/test_guide_surface_consistency.py` + `scripts/tests/factinventory.py` + vaktblocket i `docs/guide-facts-claude.md`/`docs/guide-facts-copilot.md`/`docs/guide-facts-gemini.md` | att webb och print, på båda språken, säger samma sak om varje volatilt sakpåstående — inte bara att ingen text flyttat sig, utan att **innehållet** stämmer mellan de fyra ytorna. **Sedan 2026-10-09 åt båda hållen:** `aktiv` kräver att strängen finns på båda ytorna, `borttaget` att den inte finns på någon av dem. **Sedan 2026-10-10 guide-agnostiskt:** `surfacecheck.GUIDE_SURFACES`/`GUIDES`/`surfaces_for()` och `factinventory.INVENTORIES`/`inventory_path()` tar en guide som argument i stället för att vara hårdkodade till Claude |
| **Leveransvakt (Copilot-rundan, guide-agnostisk sedan Gemini-rundan)** | `scripts/tests/test_guide_delivery.py` (hette `test_copilot_delivery.py`) | att de **levererade PDF:erna** — inklusive quick-starten, som med avsikt står utanför ytkonsistensvakten — saknar **sin egen guides** lista förbjudna strängar. Läser PDF:en, inte HTML:en den renderas ur. Äger dessutom tre Gemini-specifika frågor: att de svenska PDF:erna är byte-identiska mot bascommiten, att stämplarna bär rundans datum, och **att varje quick-starts tryckta sidantalspåstående stämmer mot sin huvudguides härledda sidantal** (nytt i Task 16B, täcker Copilot också) |
| **Innehållsförteckningsvakt (Copilot-rundan, guide-agnostisk sedan Gemini-rundan)** | `scripts/tests/test_guide_toc.py` (hette `test_copilot_toc.py`) | att förteckningens hårdkodade sidnummer (klass `toc__page`) stämmer mot var avsnitten faktiskt börjar i den renderade PDF:en — Copilots sex och Geminis tio. Täcker **inte** Claude-guidens femton; varför står i filens docstring |

**Facit ligger i `scripts/tests/fixtures/`.** Fånga aldrig om det för att få grönt. Fånga om det bara när innehållet ändrats med avsikt, och verifiera då att bara de avsedda posterna rör sig. **`scripts/tests/fixtures/capture_guide_baseline.py` tar nu en `--only RELATIV/SÖKVÄG`-flagga** (en eller flera gånger) som riktar omfångningen mot namngivna PDF:er och lämnar alla andra nycklar i de två facit-filerna exakt som de står. Den finns för att en runda som bara redigerat fyra av tjugotvå PDF:er annars tvingas välja mellan att fånga om allt (och tyst slå av vakten för de arton orörda) eller att handredigera JSON-facit för hand. `--only` gör det möjliga: fånga precis det som faktiskt ändrats. **`RECAPTURED_THIS_ROUND` i `scripts/tests/test_capture_guide_baseline.py` (döpt om från `CLAUDE`) måste tömmas och fyllas om i varje ny runda — aldrig tilläggas.** Se "Copilot-guiden — vad rundan lämnar" nedan för varför det är en hård regel och inte en rekommendation.

**~~Ytkonsistenslagrets kända begränsning~~ — STÄNGD 2026-10-09 av förbudsvakten.** Vaktblocket kunde bara påstå att en exakt sträng **finns** på en yta, aldrig att den **saknas** — ett struket påstående som skrevs tillbaka mötte inget motstånd. Hålet är stängt: `borttaget` betyder nu **får inte finnas**, och samma lager äger båda riktningarna. Egen sektion nedan.

**Påståendeinventeringen är rundans auktoritet, och mallen för nästa fyra.** `docs/guide-facts-claude.md` är inte ett arbetsdokument som kan kastas efter leverans — det är källloggen specens §8 kräver, och det är **facit** som guidetexten svarar mot, inte tvärtom (se våg 2b-specens Ruling 12-liknande princip: hittas en förekomst som inte behöver ändras ska den stå kvar i tabellen med en motivering, inte strykas tyst). Samma struktur — en post per volatilt påstående, fyra ytors förekomster, typ, omfång, källa+datum, utfallstoken, plus ett separat vaktblock — återanvändes rakt av för Copilot (`docs/guide-facts-copilot.md`) och är mallen för Gemini/NotebookLM-, Apple Intelligence- och elevguiden.

---

## Förbudsvakten — BYGGD 2026-10-09

**Hålet som är stängt.** `surfacecheck.check()` kunde bara påstå att en exakt sträng **finns** på en yta. Varje rad letade efter det korrekta påståendet och var tyst om huruvida det felaktiga också stod där. Ett struket felaktigt påstående som skrevs tillbaka av misstag fångades alltså inte av någonting — sviten förblev grön.

**Johans beslut 2026-10-09:** ingen ny statustoken. **`borttaget` betyder nu "får inte finnas"** i stället för "hoppa över". Skälet är att datan redan var rätt — de 36 `borttaget`-raderna i vaktblocket *är* förbudslistan, och alla 36 verifierades frånvarande från alla fyra ytorna innan semantiken byttes. Noll textändringar krävdes för att aktivera dem. Alternativet, en egen `förbjudet`-token, hade krävt att samma 36 rader skrevs om för att vakten skulle vakta något alls, och lämnat två tokens som i praktiken betydde samma sak i all befintlig data. **Dyker ett behov av en rad som är ren historik upp, läggs den token till då** — den finns inte i dag, med flit.

**Vad vakten gör.** För varje `borttaget`-rad påstår `check()` att strängen **inte** står på någon av språkets två ytor. Träffas den blir problemtypen **`återinfört`** — egen typ, så felmeddelandet säger vad som faktiskt hänt i stället för att låna en av de tre befintliga, och det namnger vilken yta eller vilka ytor strängen står på. `aktiv`-radernas beteende är oförändrat, och `saknar_motpart` gäller fortfarande bara `aktiv` (en struken sträng bär ingen språkkoppling).

**Verifierat så här, inte bara med gröna tester.** Två strukna påståenden — P06:s Cowork-mening och P24:s `5–20× usage` — skrevs tillbaka i den **verkliga** `guides/claude/index.html` och vakten blev röd på båda, med rätt id och rätt yta. Filen återställdes med `cp` från en kopia, aldrig med `git checkout` (fälla 4). Ett av testerna gör samma sak i minnet mot verklig inventering och verkliga ytor, så fälla 2 är stängd i sviten själv: `test_the_real_forbidden_list_would_catch_a_reintroduction`.

**Svit 484 → 489.** Sex nya tester, ett omdöpt: `test_rows_marked_borttaget_are_skipped` hette fel efter semantikbytet och heter nu `test_a_removed_claim_that_stays_removed_is_green` — och dess ytor är inte längre tomma strängar, för en tom yta kan inte skilja "frånvarande" från "vakten tittar inte".

**Rörda filer:** `scripts/tests/surfacecheck.py` (13 rader), `scripts/tests/test_guide_surface_consistency.py`, `docs/guide-facts-claude.md` (statusens innebörd på tre ställen, plus daterade uppdateringar i P22 och P25 vars celler uttryckligen skrev ut begränsningen som nu är borta — de står kvar med motivering, aldrig strukna tyst). **`factinventory.py` rördes inte** — `_STATUSES` är oförändrad, vilket är hela poängen med beslutet.

**Så gör nästa guide.** Kopiera vaktblockets mönster rakt av. En `aktiv` rad per volatilt påstående som ska stå på båda ytorna, och **en `borttaget`-rad för varje påstående rundan stryker eller rättar** — den sistnämnda är inte längre bara historik, den är det enda som hindrar att rättningen tas tillbaka. Kontrollera särskilt att en `borttaget`-sträng inte är en delsträng av legitim text: ordet "Cowork" står kvar överallt i Claude-guiden som laglig övergångstext, medan hela meningen "Cowork sits as a tab inside Claude Desktop" är förbjuden. Det är skillnaden mellan en vakt som fungerar och en som är röd från dag ett.

---

## Copilot-guiden — vad rundan lämnar (2026-10-10)

**Status.** Gren `feat/copilot-guide-international`, 28 commits, **PR #38**. Leverans: `_unpublished/assets/pdfs/guides/copilot-guide-en.pdf` och `copilot-quick-start-en.pdf`, byggda ur rättat innehåll med Blueprint-layout, till Skool-communityt. **Ingenting publicerat på sajten.** Svit: **757 passed, 0 failed, 0 skipped, 0 xfailed** med `scripts/tests/test_prompt_pdf_parity.py` undantagen — den filens 11 fel är miljöberoende (se "Känt trasigt eller begränsat").

**Det svenska divergensläget är ett känt läge, inte en upptäckt som väntar på nästa person.** `_unpublished/exports/copilot-print-a4-sv.html`, `copilot-quick-start-sv.html` och `_unpublished/sv/guider/copilot/` står kvar med junifakta och svensk inramning — spec §5, Johans beslut 2026-10-08: rundan rör bara de engelska ytorna. Deras PDF:er är byte-identiska mot innan rundan. De engelska och svenska Copilot-ytorna **divergerar därför i sak, avsiktligt** — inte bara i formulering, som Claude-guidens båda språk gör, utan i vilka fakta som står där (Microsofts namnbyten, se nedan, finns bara på de engelska ytorna). `surfacecheck.GUIDE_SURFACES["copilot"]` fortsätter kartlägga de svenska ytorna — de FINNS, 404 publikt som allt i `_unpublished/` — så en framtida svensk vaktrad jämförs mot dem och inte mot ingenting. Men ingen `aktiv`/`borttaget`-rad i vaktblocket pekar på dem i dag.

**Vaktlagret är nu guide-agnostiskt.** `surfacecheck.py` bar tidigare ett enda `SURFACES`-dict, hårdkodat till Claude; det är nu `GUIDE_SURFACES` (en guide → dess fyra ytor) plus `GUIDES = tuple(GUIDE_SURFACES)` och `surfaces_for(guide)`, som slår upp en guide eller kastar `KeyError` med de kända namnen i meddelandet. `factinventory.py` bar tidigare en enda hårdkodad sökväg; det är nu `INVENTORIES` (en guide → dess `docs/guide-facts-*.md`) plus `inventory_path(guide)`, och `load()` kräver numera en sökväg som argument i stället för att gissa en. **Nästa guide läggs till genom att fylla två dict:ar och skriva en inventering** — ingen ändring i vakten själv.

**Två nya vakter, byggda för Copilot men generella** (se tabellrader ovan under "Vad som vaktar vad"): `test_copilot_delivery.py` läser de levererade PDF:erna själva, inte HTML:en de renderas ur, och täcker quick-starten som med avsikt står utanför ytkonsistensvakten (spec §7). `test_copilot_toc.py` jämför innehållsförteckningens hårdkodade sidnummer mot var avsnitten faktiskt börjar i den renderade PDF:en.

**En konvention nästa runda MÅSTE följa.** `RECAPTURED_THIS_ROUND` i `scripts/tests/test_capture_guide_baseline.py` (döpt om från `CLAUDE`) listar de PDF:er **den pågående rundan** legitimt renderat om och därför fått omfånga. Den ska **tömmas och fyllas om i varje ny runda — aldrig tilläggas.** Föregående rundas poster stod kvar i listan när Copilot-rundan började, vilket är exakt varför en tyst Claude-omrendering inte skulle ha märkts: en lista som bara växer slutar vakta något.

**Rättelse av specens §2.** Specen påstod att guiden hade **noll** hårdkodade sidnummer i innehållsförteckningen ("Claude-guiden hade 18, varav 13 blev fel i våg 2b. Den fällan gäller inte här"). Mätningen letade efter klassen `toc-page-num` — Claude-guidens klassnamn. Copilot-guiden bär **sex** sidnummer, i klassen `toc__page`, och ett av dem (FAQ-raden) **var redan fel innan rundan började.** Nästa guide mäter på sin egen mallklass, inte på Claude-guidens.

**Tre fynd, medvetet inte åtgärdade** — se "Känt trasigt eller begränsat" för detaljerna: de elva miljöberoende testfelen och `/tmp`-facitet bakom dem, ungefär trettio platskolumner i `docs/guide-facts-copilot.md`:s EW-kolumn som nu ligger fel med ett (en senare commit lade till en rad), och ankar-id:na `p1-edp`/`p3-edp` som nu skiljer sig från den svenska spegelns `p1-cdp`/`p3-cdp`.

**Tre faktafynd som gäller de tre återstående guiderna också**, inte bara Copilot — alla tre dokumenterade med källa och hämtdatum i `docs/guide-facts-copilot.md`:

1. Microsoft har döpt om **Commercial Data Protection till Enterprise data protection (EDP)** (C03/C05/C19).
2. **Microsoft 365 Copilot heter nu Microsoft Copilot** (liksom Chat-varianten) — men licenser visar fortfarande de gamla namnen under en övergångsperiod (C01/C08/C27).
3. Guidens sätt att skilja den skyddade ytan från konsumentytan **på adressen är fel.** Det är kontot som avgör, inte värdnamnet — ett privat Microsoft-konto når samma `copilot.cloud.microsoft`, och Microsoft avråder uttryckligen från att blockera det värdnamnet (C05/C19/C21).

---

## Gemini-guiden — vad rundan lämnar (2026-10-12)

Skriven för en läsare som inte var med. Vad som står var, vad som är känt trasigt, vilket
vaktlager som äger vilken fråga, och vad Johan ska besluta.

**Status.** Gren `feat/gemini-guide-international`, avstamp `main` = `e2282b7`, sjutton
uppgifter (1–16B plus slutkontrollen), alla granskade. Leverans:
`_unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf` (**44 sidor**) och
`gemini-notebook-quick-start-en.pdf` (2 sidor), till Skool-communityt. **Ingenting publicerat
på sajten.** Svit **795 passed / 1 failed / 0 skipped / 0 xfailed / 0 xpassed** med
`test_prompt_pdf_parity.py` undantagen; det enda felet är det preexisterande
`test_brand_mark.py::test_the_page_count_is_what_we_think` (199 mot 198, kom med blogg-mergen
PR #40, faller likadant på `main`). **Grenen är inte pushad.** Specens **PR #39 mergas före
eller tillsammans med** rundans PR — planen argumenterar från specen.

### Dokumenten, i läsordning

| | |
|---|---|
| Spec | `docs/superpowers/specs/2026-10-12-gemini-guide-international-design.md` — bindande auktoritet |
| Plan | `docs/superpowers/plans/2026-10-12-gemini-guide-international.md` — **rättad 14 gånger under rundan**; dess tal är hypoteser, inte mätningar |
| Inventering | `docs/guide-facts-gemini.md` — **50 poster, 87 vaktrader.** Rundans auktoritet: texten svarar mot den, inte tvärtom |
| Avbrottsfilen | `docs/superpowers/handoff/2026-10-12-gemini-runda-avbrott.md` — **ÖVERSPELAD, står kvar som historik.** Allt levande ur den står här i stället |

Ledgern och uppgiftsrapporterna låg i worktreens `.superpowers/` och följer inte med
leveransen — `.superpowers/` är gitignorerad, precis som våg 2b:s ledger försvann. Allt som
överlever rundan står därför här.

### Vad rundan rättade, utöver den planerade omriktningen

1. **Google döpte om NotebookLM till Gemini Notebook 2026-07-16** — tre månader efter guidens
   datumstämpel, och ingenting i specen kände det. 205 förekomster, titeln, den tryckta
   URL:en, filnamnen. Verifierat mot Googles egen Workspace Updates-post plus fyra 301:or
   (`notebooklm.google.com` → `notebook.google.com`, `support.google.com/notebooklm/` →
   `/gemininotebook/`).
2. **Licensomläggningen pekade åt fel håll om pengar.** Premium kräver `Google AI Pro for
   Education` à $15/användare/månad; guiden sa att det ingick i Education Plus.
3. **Fem fel i AI Act-kapitlet**, varav det allvarligaste sa att högriskskyldigheterna gäller
   sedan augusti 2026 — bilaga III-högrisk, som uttryckligen omfattar utbildning, gäller från
   **2 december 2027**. Guiden talade om för rektorer att de redan var bundna.
4. **Matt Miller-citatet finns inte hos Matt Miller.** Ersatt med en rad som *var* verifierad
   på den sida agenten faktiskt hämtade; attributionen kvar.
5. **Byggarens löpande sidfot bar det gamla namnet på 43 av 44 sidor.** Hårdkodad i Python
   (`exports/build-gemini-notebook-pdf.py:61`), alltså osynlig för varje HTML-läsande vakt,
   och upptäckt först när `test_guide_pdf_body_text` läste den renderade filen.
6. **Åtta av tio sidnummer i innehållsförteckningen var fel.** Nu `3 5 8 13 20 23 27 30 32 41`,
   och vaktade. (Rolig detalj: bara fem behövde ändras — rundans prosatillväxt gjorde tre av
   de felaktiga numren rätta av sig själv.)
7. **Quick-starten sa "40-page premium PDF" om en 44-sidig guide.** Hittat genom läsning, och
   det var fel även före rundan (guiden var 42 sidor då). Nu rättat **och vaktat**.

### Vaktlagret: fyra guide-agnostiska lager plus en femte vaktrad

**Nästa guide fyller fyra kartor och skriver en inventering. Den behöver inte ändra någon
vakt.** Det är skillnaden mot Copilot-rundan, som fick generalisera två lager, och mot
våg 2b, som hårdkodade allt till Claude.

| vad som fylls | var | vad raden kräver |
|---|---|---|
| **1. `surfacecheck.GUIDE_SURFACES`** | `scripts/tests/surfacecheck.py` | guidens **fyra ytor** (EN web, EN print, SV web, SV print). Kartlägg de svenska även om rundan inte rör dem — en framtida svensk vaktrad ska jämföras mot dem och inte mot ingenting. `GUIDES` och `surfaces_for()` härleds; en okänd guide ger `KeyError` med de kända namnen i meddelandet |
| **2. `factinventory.INVENTORIES`** | `scripts/tests/factinventory.py` | sökvägen till guidens `docs/guide-facts-<namn>.md`. `inventory_path(guide)` slår upp den; `load()` kräver en sökväg som argument och gissar aldrig |
| **3. TOC-kartan** | `scripts/tests/test_guide_toc.py` | en rad per förteckningsnummer: rubriken, det tryckta numret, **och ett ankare** — en textsträng som bara står på avsnittets startsida. `test_every_guide_in_the_toc_map_has_anchors_for_every_row` finns för att en tom `anchors` annars ger en **tyst grön** vakt (tom parametrisering = grön). **Läs ankarvarningen nedan innan du kopierar filen** |
| **4. Förbudslistan** | `scripts/tests/test_guide_delivery.py` | **en lista per guide, aldrig delad.** Copilots lista förbjuder `Sweden`, `Swedish` och `GDPR` rakt av; Geminis kan inte, eftersom båda orden står kvar legitimt. En delad lista hade gjort den billigaste vägen till grönt att **stryka innehåll vakten inte har någon åsikt om** — alltså en vakt som styr innehållet i stället för att vakta det. `test_each_guides_forbidden_list_is_its_own` håller dem åtskilda |

**Femte vaktraden, ny i Task 16B:**
`test_guide_delivery.py::test_every_quick_starts_page_count_claim_matches_its_rendered_main_guide`
jämför varje quick-starts **tryckta** sidantalspåstående (`44-page`) mot huvudguidens
**härledda** sidantal. Numret hittades fel genom läsning och vaktades av ingenting. Vakten
täcker Copilot också, från dag ett.

**Och en vaktlärdom som gäller bakåt:** `test_an_unknown_guide_is_a_loud_error` använde
strängen `"gemini"` som sentinel — den var alltså programmerad att gå sönder i samma stund
Gemini lades i kartan, vilket är precis vad den här rundan gjorde. Den ärvdes från
Copilot-rundan, som valde **nästa guides namn** som sentinel. Omskriven till ett namn som
aldrig kan bli en guide, med en assertion mot `surfacecheck.GUIDES`. **En vakt som bryts av
att systemet växer som avsett är en vakt som garanterat blir avstängd i stället för lagad.**

### Två konventioner nästa runda ska följa

**Tre listor töms i slutet av varje runda — aldrig tilläggs.** `RECAPTURED_THIS_ROUND` i
`scripts/tests/test_capture_guide_baseline.py` var redan en hård regel (se Copilot-avsnittet
ovan); Gemini-rundan lade till två av samma art:

- **`XFAIL_UNTIL_RECOUNTED`** i `scripts/tests/test_guide_toc.py` — de TOC-nummer som är kända
  fel fram till rundan renderar om och räknar om. Töms när numren är rätta (Gemini: Task 14).
- **`XFAIL_UNTIL_RERENDERED`** i `scripts/tests/test_guide_delivery.py` — **per PDF, inte per
  guide.** De levererade PDF:er som ännu bär förbjudet innehåll därför att källan är rättad men
  filen inte omrenderad. Töms vid omrenderingen (Gemini: Task 13).

Båda är **strikta** xfail. Det är avsiktligt: en icke-strikt markering tar bort hela poängen
(en vakt som inte kan bli röd av fel skäl), och strikt är också varför `XFAIL_UNTIL_RERENDERED`
måste vara per PDF — quick-starten var ren från början, och en per-guide-markering hade gjort
den till en XPASS.

**Och en lista som fylls i stället för att tömmas:** `test_fonts.GUIDE_WEB_SURFACES` tar in en
guides webbyta när den städats. Gemini lades till i Task 5; Copilot och Claude står redan där.
`_unpublished/guides/apple-intelligence/` och `_unpublished/guides/ai-for-students/` står
**inte** där, eftersom de ännu bär Crestioras typsnitt — se de kända luckorna nedan.

### Namnbytet, och den skuld det lämnar

**Vad som bytte namn.** Prosan i de engelska ytorna (205 förekomster), titeln, den tryckta
URL:en, byggskriptets sidfot, filnamnen och facitnycklarna. **Johans beslut 2026-10-12: allt,
även filnamnen.** `NotebookLM` står nu **en gång per engelsk yta** — Kasey Bells avsnittstitel
i Shake Up Learning #252 — och noll gånger i guidens egen röst.

**(a) De svenska filnamnen behåller `gemini-notebooklm-*` med avsikt.** Deras innehåll säger
fortfarande NotebookLM (aprilfakta, utanför rundans omfång per spec §1), och ett namnbyte där
hade gjort **filnamnet osant om innehållet**. Femton spårade filer bär prefixet; alla femton är
svenska. Följden är att `test_the_swedish_gemini_pdfs_are_untouched_since_the_merge_base`
fungerar oförändrat, eftersom dess merge-base-uppslagning sker på oförändrade sökvägar.

**(b) Skulden är ETT jobb, inte flera, och den hör i publiceringsrundan.** Tre ställen, som i
dag är **överens med varandra**:

- `scripts/build-seo-meta.py` rad **51, 57 och 75** — rad 75 är `PAIR_MAP`, som spec §1
  uttryckligen förbjöd rundan att röra.
- `_unpublished/README.md` rad **26, 59, 63 och 148** — publiceringsrunbookens engelska block.
  **Rad 26:s källsökväg är i dag bruten**, eftersom filerna flyttat.
- Nio `notebooklm`-strängar i webbytans **tillgångssökvägar** (nedan).

**Varför den inte lagades här:** rad 26 går inte att rätta ensam utan att runbooken blir
osammanhängande ("flytta `gemini-notebook` till `guides/gemini-notebooklm`"), och att rätta
hela blocket betyder att **välja guidens publicerade sökväg och id** — vilket är precis vad
`PAIR_MAP` äger och spec §1 reserverar. En halv rättning hade gjort de två filerna oense.
Publiceringsrundan byter destinationssökvägen på båda ställena plus i `guides-en.json`
samtidigt. **De svenska raderna (`build-seo-meta.py` 32, 96, 100) är fortfarande riktiga och
ska inte röras.**

**(b2) Skulden är inte längre valfri, och leveransen avgör frågan.** Quick-starten **trycker
guidens publicerade adress för läsaren**: `choosewise.education / guides / gemini-notebook`. De
levererade PDF:erna är alltså i omlopp med den adressen **i tryck**, vilket betyder att
publiceringsrundan **måste** använda `/guides/gemini-notebook/`. Den har inget val kvar.
Alternativet hade varit att låta quick-starten trycka den gamla sökvägen för att hålla den
överens med konfigurationen — men då trycker guiden en adress som bär det **pensionerade
produktnamnet**, vilket motsäger hela namnbytet. Det här är alltså inte "en inkonsekvens att
rätta någon gång": **frågan är avgjord av leveransen, och konfigurationen är den som ska flytta.**

**(c) `NotebookLM` kan aldrig bli en förbudsrad i den här guiden.** Citaten bär ordet
legitimt — en citattitel som "rättas" är inte längre ett citat. Vakten vaktar därför Task 4C:s
**uppräknade överlevande förekomster**, inte det bara produktnamnet. Samma gäller tre andra
ord: `Sweden`/`Swedish` (praktikexemplet), `GDPR` (promptmallens platshållare) och
`April 2026` (åtta daterade produktpåståenden). Står utskrivet i vaktblockets huvud.

**(d) Nio `notebooklm`-strängar lever kvar i webbytans TILLGÅNGSSÖKVÄGAR.** I
`_unpublished/guides/gemini-notebook/index.html`:

- rad 351: `assets/screenshot-notebooklm-in-gemini.png` (filen finns dessutom inte i
  katalogen — trasig före rundan, ingen post äger den)
- rad 607, 615, 623, 631, 639, 647, 655, 663: `/assets/notebooklm-images/style-*.webp`

De sitter **inuti attribut**. `surfacecheck._TAG` strippar attribut, så ytkonsistensvakten kan
aldrig se dem, och ingen runda har rört dem. De hör i samma jobb som (b). **Skrivet ut med
sökväg här så att nästa läsare inte tror att namnbytet var fullständigt i filsystemet bara för
att det var fullständigt i prosan.**

### Gör detta FÖRST i nästa guides runda — innan den kopierar vaktfilen

**`scripts/tests/test_guide_toc.py`:s ankare för Del 1 och Del 2 bär produktnamnet**
(`"If you have never opened Gemini or Gemini Notebook, start here"`). Namnbytet bröt dem i sin
gamla form; de lagades genom att sätta in det **nya** namnet — och därmed är **samma sprödhet
återinförd**. Nästa namnbyte bryter dem igen, på exakt samma sätt, och kostar exakt samma
utredning. Värre: eftersom båda raderna stod som xfail såg ett **brutet ankare** ut precis som
ett **fel sidnummer**, och bara steg 1:s ankaromverifiering skilde dem.

**Byt till ankare utan produktnamn, pris eller datum.** Två rader till i samma riskklass är
obrutna i dag: Del 4:s `"Many schools run Google Workspace for Education"` och FAQ:ns
`"Is the free tier enough?"`.

**Skälet att göra det först:** Apple Intelligence-rundan kommer att **kopiera** den här filen
som mall, och ett sprött mönster som kopieras sprider sig.

### En förbättring nästa runda bör göra — inte en lucka

**`scripts/tests/pdf_body_text.py`:s `PLAYWRIGHT_FOOTERS` är handkopierad** ur byggarnas
`jobs`-listor i stället för härledd ur dem. Det är exakt den klass av inaktualitet som lät
byggarens sidfot bära det pensionerade produktnamnet på 43 sidor genom hela rundan. Modulens
egen docstring dokumenterar handkopieringen som **avsiktligt mönster för alla
`footer_template`-guider** (apple-intelligence, copilot och ai-for-elever bär samma), så att
härleda den live stänger luckan för **varje** guide, inte bara den här. Tvärgående
refaktorering; hörde inte i den här rundans fillista.

### Sex fynd ur genomläsningen som rundan medvetet INTE åtgärdade

Alla sex är **preexisterande**. Att de står här och inte i en uppgift är ett beslut, inte ett
förbiseende — ett fynd som inte åtgärdas skrivs ut, aldrig stryks tyst.

1. **Figurens axeletikett `RISK →` renderas ingenstans.** En rotate-transform placerar den på
   x = −60, utanför `viewBox`. Felet finns på **alla fyra ytor**, inklusive de svenska — och
   just därför lagades det inte: en korrekt lagning rör de frusna svenska ytorna och ändrar
   deras PDF-byte, vilket spec §1 förbjuder. **Nästa runda kan laga alla fyra i en commit.**
   Figurens fyra nivåer är etiketterade ändå, så förlusten är axelns riktningspil.
2. **Tre passager står dubblerat.** Matt Miller-citatet två gånger (sidorna 6 och 10), "the two
   sides stay complementary" två gånger (6 och 18), och Eric Curts/`edugems.ai`-stycket **tre**
   gånger (från sidan 14). Rundans enda bidrag är att två nästan identiska slutmeningar blev
   *exakt* identiska, när en faktauppgift förenade "AI Ultra" och "Google AI Ultra" mot samma
   verifierade källa — alltså en **förbättring i noggrannhet som ökade ekot**. Att avduplicera
   är ett redaktionellt pass på Johans egen text, inte en faktarättelse. **Johans beslut.**
3. **Säfström/Folkebrant-exemplet (Fristadsskolan) förekommer tre gånger**, utöver de tre
   passagerna ovan. Samma redaktionella pass. **Johans beslut.**
4. **Författaren omtalas både som "Johan" och som "I"** i samma dokument. **Johans beslut.**
5. **Den svenska quick-starten säger "39-sidiga" om en 42-sidig svensk guide.** Preexisterande,
   på en frusen yta. Samma jobb som de svenska filnamnen.
6. **`capture_guide_baseline.py` rapporterar 45 sidor för en 44-sidig PDF.** **Inget defekt:**
   `pdf_fingerprint.pages()` delar på sidbrytningstecken och ger en avslutande tom post
   (verifierat: 43 poster för den 42-sidiga versionen, 45 för den 44-sidiga). Skriptets
   utskriftssträng är en kosmetisk felmärkning, inte en felräkning.

**Och en sjunde, som är Johans beslut men inte ett läsfynd:** bonuskapitlet säger att högrisk
medför "formal pre-market obligations: risk assessment, dataset quality management, logging,
documentation". **Förhandsbedömningsplikterna faller huvudsakligen på LEVERANTÖREN**; en skola
som driftsätter bär i stället deployer-plikter. Preexisterande, orört av rundan, och att rätta
det kräver en källa ingen verifierat — att skriva det utan post hade brutit rundans enda
oeftergivliga regel.

### Tre kända luckor

1. **Claude-guidens femton TOC-nummer står ovaktade.** `test_guide_toc.py` tar inte in dem;
   varför står i filens docstring. De två andra guiderna är vaktade.
2. **`_unpublished/guides/apple-intelligence/` och `_unpublished/guides/ai-for-students/` bär
   fortfarande Crestioras typsnitt**, inklusive inline-`font-family`-attribut i SVG. De står
   därför inte i `test_fonts.GUIDE_WEB_SURFACES`. Städas i sina egna rundor.
3. **Quick-startens pekare till guidens egen adress svarar 404 så länge guiden är
   opublicerad.** Medvetet, inte missat — ingenting i den här rundan publiceras.

### Fem rättelser till specen, så att nästa guide mäter på rätt saker

1. **Webbytans typsnittsfel var tre gånger större än specen sa.** Utöver tre `<link>`-rader och
   tre `--font-*`-överskrivningar bar webbytan **sjutton inline-`font-family`-attribut i
   SVG-`<text>`-element** (sex `Playfair Display`, elva `Inter`). Ett inline-attribut vinner
   över varje `:root`-token, så felet går **inte** att se i en CSS-granskning. Copilots båda
   ytor hade noll sådana attribut — fällan var ny. Vaktas nu av
   `test_the_guide_web_surfaces_have_no_crestiora_fonts`.
2. **"AI Act stannar" betyder inte "AI Act är orörd".** Specen sa att AI Act-fakta *redan är
   belagda* i Claude-inventeringens post P13. Det stämde — och **fyra av dem var belagda som
   felaktiga**, med rättningen redan levererad i den publicerade Claude-guiden:
   ikraftträdandeformuleringen ("phases in through 2026 and beyond" → **became applicable on 2
   August 2026**), högriskfristen (augusti 2026 → **2 december 2027**), och två av de fyra
   risknivånamnen ("Limited risk" → **Transparency risk**, "Minimal risk" → **Minimal or no
   risk**; den fjärde, "Prohibited" → **Unacceptable risk**, av samma skäl). En korsreferens
   till P13, ingen ny källdomän.
3. **Den svenska inramningen innehöll ett källbelagt svenskt praktikexempel**, inte bara
   inramning: Fristadsskolan i Eskilstuna, publicerat på Pedagog Eskilstuna. Det stannar — och
   **därför kan Gemini-guidens förbudslista inte innehålla ett bart `Sweden` eller `Swedish`**,
   som Copilots gör. Det är skälet förbudslistorna är per guide.
4. **Ett påstående om Johan själv var inte längre sant.** *"I have a full-time job and run this
   work alongside it"* — han lämnade Advania i augusti 2026. Meningen stod inte i Claude- eller
   Copilot-guidens engelska ytor; den var den här guidens egen. Omskriven så att
   **förväntningen på svarstid** behålls utan påståendet om en anställning.
5. **Produktnamnens antal skiljde sig mellan de två engelska ytorna.** Tre asymmetrier (`Gems`
   25/24, `Audio Overview` 10/11, `AI Ultra` 5/6). **Antalet är ingen fälla — asymmetrin är**,
   eftersom den betyder att ytorna redan säger olika saker om samma produkt. Varje asymmetri
   lästes i sitt sammanhang; alla visade sig vara struktur eller formulering (t ex bar
   printytans förteckning en underrad webben inte har). **Lärdomen: ett förekomsttal ska läsas,
   inte lagas.**

### Två siffror att INTE ärva ur rundans rapporter

- **Pyramidens trängsta luft är 120 enheter, inte ~17.** Den tidigare uppskattningen var
  pessimistisk med en faktor sju. Oberoende ommätt av två mätare ur den levererade PDF:en vid
  200–300 dpi, som landade inom en halv enhet av varandra. Ingen etikett går utanför sin rect.
- **Guiden växte 42 → 44 sidor denna runda, inte 38 → 44.** Talet 38 står fel i två
  uppgiftsrapporter.

### En sak att laga när någon ändå är inne i inventeringen

`docs/guide-facts-gemini.md:113` säger korrekt **50 poster**, och tokenräkningens tre tal
(30 + 14 + 6 = 50) är rätta — men **uppräkningarna** inne i raderna listar tillsammans bara 49
id:n: **G27 står i ingen av dem** (den hör i `stämmer`, vars uppräkning har 29 poster mot sitt
eget tal 30). Underrubriken på rad 145 säger därför *"Tjugofyra av 49 celler"* och ärver samma
ofullständighet. Två tecken att rätta. **Levererat värde är rätt; det är recordet som är fel,
och det är recordet nästa runda läser.**

---

## Evidence-sidornas mobilöverflöd — LÖST 2026-10-09

**Det var en regression från Evidence-fixen samma dag, inte ett gammalt fel.** Överlämningen och minnet sa att överflödet fanns före fixen; mätning mot `8af79cd` visade **noll överflöd** på alla kontrollerade sidor. Efter fixen stack 15 av 15 domänsidor ut, upp till 161 px vid 320 px och 117 px vid 1024 px.

**Rotorsaken var `white-space: nowrap` på `.band-none`.** Den lades till för att hindra "no EEF strand" att brytas till två rader vid 12 px — och gjorde därmed rutnätskolumnens min-content till hela frasens bredd. `grid-template-columns: 1fr 1fr 1fr` är `minmax(auto, 1fr)` och kan **aldrig** krympa under min-content, så dokumentet blev bredare än fönstret. Isolerat genom att backa en regel i taget: nowrap ensam stod för 91 av 91 px vid 390 px, medan textstorlekarna stod för 14.

**Tre ändringar, en per orsak:** nowrap borttagen; `@container (max-width: 420px)` staplar metric-blocket när **kortet** är smalt (inte när fönstret är det — vid 1024 px rymdes tre kort per rad och kolumnerna blev ~87 px, så en mobilbrytpunkt hade missat fallet); och `.et-card-grid` fick `minmax(min(360px, 100%), 1fr)` — `min()` för de sista 4 px vid 320 px, och 360 i stället för 300 så korten blir breda nog att behålla metric-blocket side-by-side på desktop. **Johans beslut:** hellre två bredare kort per rad vid 1024 px än tre smala med staplat metric-block.

**Lärdomen:** 743 statiska tester såg ingenting. Bredd finns först när webbläsaren räknat. Det är samma lärdom som fälla 3 (fingeravtryck på text är blinda för bilder) i en ny förklädnad — och skälet till att vaktlagret ovan nu har en renderingsrad.

**Kvar, orört:** `/blog/` sticker ut 24 px vid 320 px (`.blog-grid` kräver `minmax(320px, 1fr)`). Samma klass av fel, utanför den här rundans omfång. Evidence har dessutom kvar `side-tab` 32, `all-caps-body` 29 och `flat-type-hierarchy` 15 från impeccable-körningen.

---

## Överflöd i sidled — hela sajten, 2026-10-09

**Alla 203 publicerade sidor mättes vid 320 px. 19 hade överflöd; alla är åtgärdade.** Evidence (15 sidor) var en regression från samma dags fix, se avsnittet ovan. Bloggen (5) och resten (14) hade fyra återkommande orsaker:

| Orsak | Åtgärd |
|---|---|
| Rutnät med fast minbredd — `minmax(320px, 1fr)` i en 272 px innehållsyta | `minmax(min(320px, 100%), 1fr)` på `.blog-grid`, `.styles-grid`, `.module-grid`, `.et-card-grid` |
| Långa obrytbara ord — `choosewise.education`, `skolmåltidspersonal`, nakna URL:er i källistor | `overflow-wrap: break-word` på `body`. Det fanns **ingen** sådan regel på sajten före detta |
| Rubrikens golv — `--fs-display` har golvet 2.25rem, och det binder ända upp till 600 px | `.post__header h1` får samma kurva med golvet 1.65rem |
| Tabeller bredare än spalten | Scroll på en omslutande låda, aldrig på tabellen |

**Tabellfällan är värd att läsa innan någon rör en tabell igen.** Första försöket var `table { display: block; overflow-x: auto }` i base.css. Sviten blev grön — men guidernas egen `styles.css` har `.jl-page table { overflow: hidden }` för att klippa de rundade hörnen, och vann på specificitet. Tabellen slutade spränga sidan **genom att klippas**, och två kolumner blev oåtkomliga på telefon. Överflödsvakten kunde inte se skillnaden: klippt innehåll mäter noll. Därav en egen vakt — *en tabell som är bredare än sin spalt måste gå att scrolla, aldrig klippas*.

Andra försöket var `min-width` på tabellen. Det gör **lådan** bred, inte innehållet, så sidan svämmade över igen. Scrollen måste ligga på en omslutande `.table-scroll`, med `min-width: 560px` på tabellen inuti. Utan den minbredden klämts kolumnerna ihop till ett par ord per rad och raderna blev **838 px höga i stället för 216**.

**Vakten är inte uttömmande.** `scripts/tests/test_responsive_overflow.py` täcker 35 sidor — Evidence, bloggen och de sidor sweepen pekade ut. Alla 203 går inte att ha i sviten: det tar över tre minuter. Kör sweepen för hand när en ny mall tillkommer:

```python
# /usr/bin/python3, från repots rot. Serverar lokalt, mäter alla publicerade
# sidor vid 320 px och skriver ut dem som scrollar i sidled.
import sys, http.server, socketserver, threading, functools
sys.path.insert(0, "scripts")
from tests import brandguard
from playwright.sync_api import sync_playwright

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
class Server(socketserver.TCPServer): allow_reuse_address = True

srv = Server(("127.0.0.1", 0), functools.partial(Quiet, directory="."))
threading.Thread(target=srv.serve_forever, daemon=True).start()
port = srv.server_address[1]

urls = set()
for f in brandguard.published_files((".html",)):
    rel = f.relative_to(brandguard.ROOT).as_posix()
    urls.add("" if rel == "index.html" else rel[:-10] if rel.endswith("/index.html") else rel)

with sync_playwright() as pw:
    b = pw.chromium.launch()
    page = b.new_page(viewport={"width": 320, "height": 700})
    for u in sorted(urls):
        page.goto(f"http://127.0.0.1:{port}/{u}", wait_until="domcontentloaded")
        page.wait_for_timeout(120)
        over = page.evaluate(
            "()=>document.documentElement.scrollWidth-document.documentElement.clientWidth")
        if over > 0:
            print(f"+{over:4d}px  /{u}")
    b.close()
srv.shutdown()
```

**Och hur man hittar boven när en sida svämmar över.** Två sonder, inte en — jag gick vilse på båda:

- *Vilket element bryter ut ur sin förälder?* `r.right > clientWidth && parentRect.right <= clientWidth && förälderns overflow-x === "visible"`. Utan föräldervillkoret pekar den på barn som bara ärvt en bred förälder — `IMG`, `A.nav__link`.
- *Vilket element är bredare än sin egen låda?* `el.scrollWidth > el.clientWidth`. Det är den som hittar långa ord och tabeller, och den första sonden ser dem inte.

Ett filter som sållar bort breda element för att slippa fullbreddsbehållare dolde boven helt på inläggssidorna: sonden returnerade ingenting alls.

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

12. **Prosa bor inte bara i HTML.** Byggskript och `footer_template`-mallar bär text som ingen ytvakt läser. Gemini-rundans sidfot bar det pensionerade produktnamnet på 43 av 44 sidor, hårdkodad i Python, och upptäcktes först när den **renderade PDF:en** lästes. En fillista som äger "sökvägar" och en som äger "HTML-ytor" har ett glapp mellan sig, och sidfotstiteln bodde där.

13. **Mät sidlängder genom att KOLLAPSA blanktecken, inte ta bort dem.** Den buggen gav fel siffror två gånger i Gemini-rundan och sköt två sidor under en diagnostisk gräns de klarade med marginal. Och ett diagnostiskt tal är inte ett bindande villkor: gränsen 700 tecken hade en sida **åtta** tecken över sig, medan det bindande villkoret (400) klarades med marginal.

14. **För en `borttaget`-rad är en längre sträng som innehåller en kortare förbjuden strikt SVAGARE än den korta** — en återinföring träffar alltid den korta raden först, så en lång rad "som extra skydd" skyddar inget. På `aktiv`-sidan är det omvänt: en kort ankarrad på själva värdet överlever en legitim omformulering av den långa meningen. Båda reglerna står nu i vaktblockets huvud i `docs/guide-facts-gemini.md`, där nästa runda kopierar dem.

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
- Spec Copilot-guiden: `docs/superpowers/specs/2026-10-09-copilot-guide-international-design.md`
- Plan Copilot-guiden: `docs/superpowers/plans/2026-10-09-copilot-guide-international.md` (fjorton uppgifter) — uppgiftsbrev och -rapporter i `.superpowers/sdd/2026-10-09-copilot-guide-international/`
- Påståendeinventeringen, Copilot-guidens facit: `docs/guide-facts-copilot.md`
- PR Copilot-guiden: #38, gren `feat/copilot-guide-international`
- Spec Gemini-guiden: `docs/superpowers/specs/2026-10-12-gemini-guide-international-design.md` (**PR #39**, gren `docs/gemini-guide-spec` — mergas före eller med rundans PR)
- Plan Gemini-guiden: `docs/superpowers/plans/2026-10-12-gemini-guide-international.md` (sjutton uppgifter, grinden efter uppgift 4) — **rättad 14 gånger under körningen; dess tal är hypoteser och ska mätas, aldrig citeras**
- Påståendeinventeringen, Gemini-guidens facit: `docs/guide-facts-gemini.md` (50 poster, 87 vaktrader)
- Gemini-rundans avbrottsfil: `docs/superpowers/handoff/2026-10-12-gemini-runda-avbrott.md` — **ÖVERSPELAD, historik.** Allt levande ur den står i "Gemini-guiden — vad rundan lämnar" ovan
- **Gemini-rundans ledger och uppgiftsrapporter finns inte kvar efter leverans.** Samma skäl som våg 2b:s: de låg i worktreens `.superpowers/`, som är gitignorerad. De 60+ rulings som togs under körningen är inarbetade i det här dokumentet där de överlever rundan
- Gren Gemini-guiden: `feat/gemini-guide-international` — **inte pushad, ingen PR öppnad 2026-10-12**
- Märkets bruksregler: `docs/brand-mark-usage.md`
- Beslutsloggar och PR-texter: `~/Desktop/choosewise-spar-a-forslag/`
- PDF:erna att titta på: `~/Desktop/choosewise-guider-vag2a/` (kopior — kan vara inaktuella)
