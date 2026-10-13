# Blueprint — överlämning

**Senast uppdaterad:** 2026-10-13 (Copilot-guiden MERGAD som `26c661a`; **Gemini-guiden LEVERERAD på gren med `origin/main` inmergad, svit helt grön, PR ej öppnad**)
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
| **Gemini Notebook** — andra av de fyra | **LEVERERAD PÅ GREN 2026-10-13.** Gren `feat/gemini-guide-international`, worktree `.worktrees/gemini-guide-international`, avstamp `main` = `e2282b7`, med `origin/main` (`aee4117`) inmergad 2026-10-13. **Tjugo uppgifter** — planens nitton `## Task`-rubriker plus Task 16B — körda i **nitton dispatcher** (Task 10 och 11 batchades i en), alla granskade. Leverans: `_unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf` (**44 sidor**) och `gemini-notebook-quick-start-en.pdf` (2 sidor), till Skool-communityt. **Ingenting publicerat på sajten.** Svit **796 passed, 0 failed, 0 skipped, 0 xfailed, 0 xpassed** med `test_prompt_pdf_parity.py` undantagen — **helt grön.** Grenen rapporterade länge ett rött `test_brand_mark.py::test_the_page_count_is_what_we_think` (199 mot 198) som preexisterande; `main` hade då redan lagat det i `aee4117`, och mergen hämtade in fixen. **Grenen är inte pushad och ingen PR är öppnad** — det görs efter Johans besked. **Specens PR #39 mergas före eller tillsammans med rundans PR**: planen argumenterar från specen, och en mergad plan utan mergad spec lämnar en hängande korsreferens. Se **"Gemini-guiden — vad rundan lämnar"** nedan. |
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
3b. ~~**GEMINI-GUIDEN — specen är godkänd, planen är nästa steg.**~~ **LEVERERAD PÅ GREN 2026-10-13.** Tjugo uppgifter (planens nitton plus Task 16B) körda på `feat/gemini-guide-international` i nitton dispatcher, alla granskade. **Vad rundan levererade:** två engelska PDF:er byggda ur rättat innehåll (`gemini-notebook-guide-en.pdf`, 44 sidor, och `gemini-notebook-quick-start-en.pdf`), den svenska inramningen generaliserad, GDPR på artikelnivå ersatt av en jurisdiktionsneutral ruta i huvudflödet, AI Act kvar och **rättad på fem punkter** mot Claude-inventeringens post P13, bonuskapitlets skylt skärpt, en inventering på **50 poster** med **87 vaktrader** i `docs/guide-facts-gemini.md`, och **två vaktlager generaliserade** (TOC-vakten och leveransvakten) i stället för kopierade. **Plus det ingen plan förutsåg:** Google hade döpt om NotebookLM till **Gemini Notebook** 2026-07-16, tre månader efter guidens datumstämpel — 205 förekomster, titeln, den tryckta URL:en och filnamnen, Johans beslut vid grinden. **Nästa steg:** Johan läser, sedan pushas grenen och PR:en öppnas; specens PR #39 mergas före eller med den. Läs **"Gemini-guiden — vad rundan lämnar"** nedan före nästa guide.

3c. **GUIDESIDORNAS LÖFTEN PÅ SAJTEN — egen gren, egen PR.** Johans omfångsbeslut 2026-10-13: guiderna distribueras via **Skool**, inte via sajten, och inga svenska guider utöver Claude och presentationsteknik. `guides/index.html` och `sv/guider/index.html` är **publicerade** och lovar i löptext guider om Copilot, Gemini & NotebookLM, Apple Intelligence och elevguiden som "in preparation" / "under arbete" — **det löftet ska bort.** Båda nämner dessutom inte presentationsteknik, som stannar, och båda är daterade 27 april 2026. **Hör inte på Gemini-grenen:** dess PR-text säger att ingenting publiceras, och det ska den fortsätta göra. Detaljerna i **"⚑ OMFÅNGSBESLUTET 2026-10-13"** nedan.

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
- ~~**De svenska Copilot- OCH Gemini-ytorna** — ska de hämta in de engelska?~~ **AVGJORT 2026-10-13: nej.** Johans omfångsbeslut: **inga svenska guider utöver Claude och presentationsteknik**, och guiderna distribueras via **Skool** i stället för via sajten. De svenska Copilot- och Gemini-ytorna (`copilot-print-a4-sv.html`, `copilot-quick-start-sv.html`, `_unpublished/sv/guider/copilot/`; `gemini-notebooklm-print-a4-sv.html`, `gemini-notebooklm-quick-start-sv.html`, `_unpublished/sv/guider/gemini-notebooklm/`) står kvar **frysta, permanent**, med juni- respektive aprilfakta. **De två språken divergerar i sak med avsikt.** Deras PDF:er är byte-identiska mot före sin runda och vaktas av `test_guide_delivery.py`. **Beslutet stänger samtidigt Gemini-fallets tre följdfrågor:** de svenska filnamnen stannar, den svenska quick-startens "39-sidiga" når ingen läsare, och axeletiketten behöver nu bara lagas på **två engelska ytor** i stället för fyra. Detaljerna i **"⚑ OMFÅNGSBESLUTET 2026-10-13"** nedan.
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

**Gemini-guidens kända trasiga står samlat i sitt eget avsnitt.** Tre fynd rundan medvetet inte åtgärdade (bl a en osynlig axeletikett på alla fyra ytor), Johans redaktionella pass 2026-10-13 som stängde tre av de tidigare sex, tre kända luckor, och namnbytets kvarvarande skuld med radnummer — allt i **"Gemini-guiden — vad rundan lämnar"** nedan. Ingen av dem är ny med rundan; alla är preexisterande och alla har sin motivering utskriven.

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

**Det svenska divergensläget är ett känt läge, inte en upptäckt som väntar på nästa person.** `_unpublished/exports/copilot-print-a4-sv.html`, `copilot-quick-start-sv.html` och `_unpublished/sv/guider/copilot/` står kvar med junifakta och svensk inramning — spec §5, Johans beslut 2026-10-08: rundan rör bara de engelska ytorna. Deras PDF:er är byte-identiska mot innan rundan. De engelska och svenska Copilot-ytorna **divergerar därför i sak, avsiktligt** — inte bara i formulering, som Claude-guidens båda språk gör, utan i vilka fakta som står där (Microsofts namnbyten, se nedan, finns bara på de engelska ytorna). `surfacecheck.GUIDE_SURFACES["copilot"]` fortsätter kartlägga de svenska ytorna — de FINNS, 404 publikt som allt i `_unpublished/` — så en framtida svensk vaktrad jämförs mot dem och inte mot ingenting. Men ingen `aktiv`/`borttaget`-rad i vaktblocket pekar på dem i dag. **Och sedan Johans omfångsbeslut 2026-10-13 är läget permanent:** inga svenska guider utöver Claude och presentationsteknik, så de svenska Copilot-ytorna hämtar aldrig in de engelska. Se **"⚑ OMFÅNGSBESLUTET 2026-10-13"** i Gemini-avsnittet nedan.

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

**Status.** Gren `feat/gemini-guide-international`, avstamp `main` = `e2282b7`, med
`origin/main` (`aee4117`) inmergad 2026-10-13. **Tjugo uppgifter** — planens nitton
`## Task`-rubriker plus Task 16B — körda i **nitton dispatcher** (Task 10 och 11 batchades i
en), alla granskade. Leverans:
`_unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf` (**44 sidor**) och
`gemini-notebook-quick-start-en.pdf` (2 sidor), till Skool-communityt. **Ingenting publicerat
på sajten.** Svit **796 passed / 0 failed / 0 skipped / 0 xfailed / 0 xpassed** med
`test_prompt_pdf_parity.py` undantagen — **helt grön. Grenen är inte pushad.** Specens
**PR #39 mergas före eller tillsammans med** rundans PR — planen argumenterar från specen.

**Om det röda testet grenen länge rapporterade — en lärdom värd mer än felet.** Rundan sprang på
`test_brand_mark.py::test_the_page_count_is_what_we_think` (199 sidor mot hårdkodat 198) i Task
1 och klassade det riktigt som preexisterande: det kom med blogg-mergen, grenens diff rör
varken testet eller en publicerad sida, och det föll likadant på `main` **vid den mätningen**.
Varje efterföljande uppgift ärvde klassningen och läste sitt utfall som "mina gröna plus det här
ena röda" — i sexton uppgifter. **Men `main` lagade felet i `aee4117` samma eftermiddag**, och
ingen uppgift mätte om det, eftersom ingen hade skäl att: en ruling från Task 1 är en avgjord
fråga. Slutkontrollen upprepade formuleringen "faller likadant på `main`" i fyra dokument utan
att hämta `origin` först. **Lärdomen: ett preexisterande fel är ett påstående om `main`, och
`main` rör sig. Hämta `origin` och mät om det i slutkontrollen, inte bara i den uppgift som
hittade det.** Mergen gör nu att grenen levererar en helt grön svit.

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
8. **Friskrivningen sa "This chapter" under en DEL-rubrik.** *"I am not a lawyer. This chapter
   gives a starting point"* stod under `<h2>Scale & Lead</h2>`, som är en del, inte ett kapitel
   → **"This part"**. Den andra förekomsten, inne i bonuskapitlet, står kvar orörd eftersom
   "chapter" är riktigt där. Ett ord, på båda engelska ytorna (`af69689`).
9. **Promptbibliotekets rubrik täckte bara halva sitt innehåll.** *"A starter library of Gemini
   prompts"* mot en förteckning som säger "Gemini **and Gemini Notebook**" och en ingress som
   uttryckligen pekar ut Gemini Notebook-specifika prompter → rubriken säger nu båda
   produkterna (`af69689`).

**Punkt 8 och 9 är värda en metanotering:** båda hittades i genomläsningen *efter* att allt
innehåll var klart, båda är enordsstora, och båda låg bara i en gitignorerad uppgiftsrapport
tills en granskning räddade dem. **Ett fynd som bara står i `.superpowers/` är ett fynd som dör
med worktreen.** Det är skälet varje oåtgärdat fynd i rundan skrevs in i en spårad fil.

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

### ⚑ OMFÅNGSBESLUTET 2026-10-13: guiderna distribueras via Skool, inte via sajten

**Johans beslut 2026-10-13.** Guidesidorna ska **inte finnas kvar på choosewise** — bortsett
från **Claude-guiden och presentationsteknik**, som stannar. De färdiga PDF:erna flyttas in i
**Skool** när communityt skapas. Alltså: **inga svenska guider utöver Claude och
presentationsteknik**, och **ingenting ska hänvisa till AI-guidesidor på sajten**.

**Konsekvensen är nästan noll i filsystemet, och det är mätt**, inte antaget: med
`brandguard.published_files()` har de fyra icke-Claude-guiderna **aldrig varit publicerade**
(allt ligger under `_unpublished/`), och **ingen publicerad sida länkar till någon av dem**. Det
finns alltså inget att ta ner. Men beslutet gör flera saker i den här överlämningen osanna, och
de står rättade nedan.

**(a) Publiceringsskulden är AVBLÅST.** Hela jobbet under "Namnbytet, och den skuld det lämnar"
nedan — `build-seo-meta.py` 51/57/75, `_unpublished/README.md` 26/59/60/63/148, `PAIR_MAP` och
`guides-en.json` — beskrev en **publicering som inte blir av**. Radnumren står kvar där **som
historik**, så att nästa läsare ser vad som en gång var planerat och varför det ströks, men
**jobbet ska inte göras.** Formuleringen att skulden "inte är valfri" är struken: den var tvingad
av en publicering, och tvånget föll med den. Detsamma gäller de **nitton `notebooklm`-strängarna
i tillgångssökvägarna** — de spelar bara roll om ytorna publiceras, vilket de inte ska, så de
står kvar med avsikt.

**(b) Det svenska divergensläget är AVGJORT.** Inga svenska guider utöver Claude och
presentationsteknik. De svenska Copilot- och Gemini-ytorna står kvar **frysta, permanent**, och
de två språken divergerar i sak **med avsikt**. Det är inte längre en öppen fråga som väntar på
Johan. **Och det stänger tre följdfrågor** som den här överlämningen listar som öppna:

1. **De svenska filnamnen** (`gemini-notebooklm-*`) — stannar. Det fanns aldrig något att byta
   dem till, och nu finns det ingen publicering som kunde kräva det.
2. **Den svenska quick-startens "39-sidiga" om en 42-sidig svensk guide** — står kvar. Ytan
   distribueras inte, så felet når ingen läsare.
3. **Den osynliga axeletiketten `RISK →`** — behöver nu bara lagas på **de två engelska
   ytorna**, inte på alla fyra samtidigt. **Den är alltså billigare än den här överlämningen
   påstår på två ställen.** Se fyndlistan nedan, som är rättad.

**(c) Webbytorna BEHÅLLS — och här är varför, så att ingen undrar eller publicerar dem av
misstag.** `_unpublished/guides/<namn>/index.html` står kvar, men **deras enda kvarvarande
funktion är att vara andra halvan i ytkonsistensvakten**: vakten jämför print mot webb per
språk, och utan webbytan har den ingenting att jämföra mot. **De är interna kontrollkopior, inte
sidor som ska publiceras.** Skälet att betala för dem: vakten har fångat **verklig divergens
flera gånger** under den här och Copilot-rundan, och den är dyr att återskapa om ytan slängs.
**Den som städar i `_unpublished/guides/` ska läsa den här raden först.**

**(d) Tre döda adresser i tryck — en lagad, en till Apple-rundan, en som står kvar med avsikt.**
En quick-start som trycker en sökväg till en sida som aldrig kommer att finnas skickar läsaren
mot en 404:

| fil | vad den trycker | status |
|---|---|---|
| `_unpublished/exports/gemini-notebook-quick-start-en.html` | `choosewise.education / guides / gemini-notebook` (rad 319) **och** underrubrikens `the full guide is at choosewise.education` (rad 181) | **BÅDA BORTTAGNA 2026-10-13** (Task 21). Avslutningsraden säger nu att guiden följer med i communityt och underrubriken att den fulla guiden tar vid — båda utan adress, så de åldras inte och binder ingen Skool-URL |
| `_unpublished/exports/apple-intelligence-quick-start-en.html` | `choosewise.education / guides / apple-intelligence` | **Apple-rundans FÖRSTA uppgift.** Samma fel, samma fix |
| `_unpublished/exports/gemini-notebooklm-quick-start-sv.html` | `choosewise.education / sv / guider / gemini-notebooklm` | **Rörs inte.** Den svenska ytan är fryst och distribueras inte, så adressen når ingen läsare — men den ska stå skriven, inte glömmas |

Copilots quick-start trycker **ingen** sökväg (bara varumärkessträngen `choosewise.education`);
den lagades i sin egen runda och är redan rätt.

**Och underrubriken bar samma osanning utan sökväg — LAGAD 2026-10-13 i samma runda.**
`_unpublished/exports/gemini-notebook-quick-start-en.html` **rad 181** sa *"the full guide is at
choosewise.education"*: samma påstående som den borttagna sökvägen, bara utan sökväg, och
**läsarsynligare** eftersom den står i underrubriken på sidan 1. Den säger nu
*"the full guide takes it from there"* — vad guiden **är** i förhållande till quick-starten,
inte **var** den finns. **Mätt i den levererade PDF:en: `choosewise.education` står exakt två
gånger, en per sida, och båda är sidfotsmärket.** Noll pekare kvar.

**Varumärkessträngarna i de två sidfötterna (rad 244 och 328) ska stå** och är orörda: de är
avsändarmärket, inte en pekare — sajten finns och är Johans oavsett hur guiden distribueras.

**Mätt åt Apple-rundan och åt den svenska ytan, utan att röra någon av dem (2026-10-13):**

| fil | underrubriken | tryckt sökväg |
|---|---|---|
| `apple-intelligence-quick-start-en.html` | **ren** — rad 94 säger `iPad-first, privacy-aware, takes 10 minutes to learn.` och nämner ingen adress | **rad 195**, `choosewise.education / guides / apple-intelligence` |
| `gemini-notebooklm-quick-start-sv.html` (fryst) | **bär samma påstående** — rad 181: `En komprimerad första timme med Gemini och NotebookLM — hela guiden finns på choosewise.education.` | **rad 319**, `choosewise.education / sv / guider / gemini-notebooklm` |
| `copilot-quick-start-en.html` | **ren** | **ingen** — rad 195 är bara varumärkessträngen `choosewise.education`; lagad i sin egen runda |

**Apple har alltså halva problemet, inte hela: en sökväg, ingen underrubrikspekare.** Den
svenska Gemini-ytan har **båda**, precis som den engelska hade — men den är fryst och
distribueras inte, så den rörs inte. Copilot är ren på båda punkter och är mallen.

**(d2) `_unpublished/README.md` är märkt som avblåst, i filen själv.** Runbooken beskriver
publiceringsjobbet steg för steg, och den som öppnar den direkt läste tidigare en instruktion
som inte gäller — överlämningen skyddade bara den som läste överlämningen först. **En
varningsruta ligger nu högst upp i filen**, före brödtexten: beslutet, datumet, att guiderna
distribueras via Skool, och en pekare hit. **Runbookens instruktionsrader är orörda med avsikt**
— de är historiken, och de är fortfarande riktiga om beslutet någon gång vänder. En avblåst
instruktion som skrivs om till något annat går inte att återställa.

**(e) En sajtändring som INTE hör på den här grenen, men som är nästa steg.**
`guides/index.html` och `sv/guider/index.html` är **publicerade** och lovar i löptext guider om
Copilot, Gemini & NotebookLM, Apple Intelligence och elevguiden som "in preparation" /
"under arbete". **Det löftet ska bort.** Båda nämner dessutom **inte** presentationsteknik, som
stannar, och båda är daterade **27 april 2026**. Det kräver **egen gren och egen PR**: den här
grenens PR-text säger att ingenting publiceras, och det ska den fortsätta göra.

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

**(b) Skulden är AVBLÅST — Johans omfångsbeslut 2026-10-13 (se avsnittet ovan).** Den här
listan beskrev **ett jobb i publiceringsrundan**, och den publiceringen blir inte av: guiderna
distribueras via Skool. **Radnumren står kvar som historik**, så att nästa läsare ser vad som en
gång var planerat och varför det ströks — men **jobbet ska inte göras.** Allt nedan är alltså
dokumentation av ett avblåst jobb, inte en uppgift. Tre ställen, som var överens med varandra
till och med Task 17 men inte efter Task 18 — se rad 60:

- `scripts/build-seo-meta.py` rad **51, 57 och 75** — rad 75 är `PAIR_MAP`, som spec §1
  uttryckligen förbjöd rundan att röra.
- `_unpublished/README.md` rad **26, 59, 60, 63 och 148** — publiceringsrunbookens engelska
  block. **Rad 26:s källsökväg är i dag bruten**, eftersom filerna flyttat. **Och rad 60 är
  sedan Task 18 (2026-10-13) osann i sak, inte bara i sökväg:** den bär
  `"title": "Gemini & NotebookLM for teachers and school leaders"` och annonserar alltså en
  titel guiden **inte längre bär** — den heter nu `Gemini & Gemini Notebook for educators`
  (se Johans redaktionella pass nedan). Publiceringsrundan som inte tar rad 60 publicerar
  indexkortet med fel titel. Den lagades inte i Task 18 med avsikt: raden bär **också** det
  pensionerade produktnamnet och den gamla sökvägen `/guides/gemini-notebooklm/`, alltså precis
  det id- och sökvägsval spec §1 reserverade bort från rundan, och en halv rättning hade gjort
  runbooken osammanhängande på samma sätt som rad 26.
- Nio `notebooklm`-strängar i webbytans **tillgångssökvägar** (nedan).

**Varför den inte lagades här:** rad 26 går inte att rätta ensam utan att runbooken blir
osammanhängande ("flytta `gemini-notebook` till `guides/gemini-notebooklm`"), och att rätta
hela blocket betyder att **välja guidens publicerade sökväg och id** — vilket är precis vad
`PAIR_MAP` äger och spec §1 reserverar. En halv rättning hade gjort de två filerna oense.
Publiceringsrundan hade bytt destinationssökvägen på båda ställena plus i `guides-en.json`
samtidigt — **den rundan blir inte av, så bytet sker inte.** **De svenska raderna i `_unpublished/README.md` — 32 (`git mv … sv/guider/gemini-notebooklm`), 96 (`"id": "gemini-notebooklm"`) och 100 (`"url": "/sv/guider/gemini-notebooklm/"`) — är fortfarande riktiga och ska inte röras**, eftersom den svenska ytan behåller sitt namn. Samma gäller `build-seo-meta.py:57`, som är `HIDDEN_PATHS`-postens svenska halva. Av de tre `build-seo-meta.py`-raderna är det alltså **51** (`HIDDEN_PATHS`, engelska) och **75:s nyckel** (`PAIR_MAP`, vars värde är den svenska sökvägen och stannar) som ska byta.

**(b2) ~~Skulden är inte längre valfri, och leveransen avgör frågan.~~ FÖRFALLEN 2026-10-13.**
Argumentet löd: quick-starten **trycker** guidens publicerade adress
`choosewise.education / guides / gemini-notebook` för läsaren, de levererade PDF:erna är därför
i omlopp med adressen **i tryck**, och publiceringsrundan **måste** alltså använda
`/guides/gemini-notebook/`. **Båda leden föll samma dag:** omfångsbeslutet tog bort
publiceringen, och Task 21 tog bort den tryckta adressen ur quick-starten. Kvar står bara
lärdomen, som är värd att behålla: **en guide som trycker en adress binder konfigurationen** —
så den som sätter en adress i tryck ska veta att hen just har fattat ett infrastrukturbeslut.
Nästa gång: tryck ingen adress som inte redan finns.

**(c) `NotebookLM` kan aldrig bli en förbudsrad i den här guiden.** Citaten bär ordet
legitimt — en citattitel som "rättas" är inte längre ett citat. Vakten vaktar därför Task 4C:s
**uppräknade överlevande förekomster**, inte det bara produktnamnet. Samma gäller tre andra
ord: `Sweden`/`Swedish` (praktikexemplet), `GDPR` (promptmallens platshållare) och
`April 2026` (åtta daterade produktpåståenden). Står utskrivet i vaktblockets huvud.

**(d) NITTON `notebooklm`-strängar lever kvar i de engelska ytornas TILLGÅNGSSÖKVÄGAR OCH
KLASSNAMN — på alla tre ytor, inte bara webbytan.** Räknade per yta 2026-10-13:

| yta | antal | rader | vad de är |
|---|---|---|---|
| `_unpublished/guides/gemini-notebook/index.html` (EW) | **9** | 351 | `assets/screenshot-notebooklm-in-gemini.png` — **filen finns dessutom inte i katalogen**; trasig före rundan, ingen post äger den |
| | | 607, 615, 623, 631, 639, 647, 655, 663 | `/assets/notebooklm-images/style-*.webp` |
| `_unpublished/exports/gemini-notebook-print-a4-en.html` (EP) | **8** | 1093, 1101, 1109, 1117, 1125, 1133, 1141, 1149 | `../../assets/notebooklm-images/style-*.webp` — samma publicerade katalog, relativ i stället för rotad |
| `_unpublished/exports/gemini-notebook-quick-start-en.html` (QS) | **2** | 57, 193 | CSS-klassen `.tool-card.notebooklm` plus dess enda användning — triviala, men de räknas |
| **summa** | **19** | | |

**Sexton** av de nitton är bildsökvägar mot samma publicerade katalog, `assets/notebooklm-images/`
(åtta per yta, rotade på webbytan och relativa i printytan). Katalogen bär **420 filer** och
finns på riktigt. **Det är alltså katalognamnet som är den egentliga posten, inte de sexton
referenserna** — döps katalogen om följer alla sexton i en sed. De tre övriga är en egen sak var:
EW:350:s trasiga skärmdumpssökväg (rad 351 fram till Task 18) och quick-startens två CSS-rader.

De sitter **inuti attribut** (eller i ett CSS-klassnamn). `surfacecheck._TAG` strippar attribut,
så ytkonsistensvakten kan aldrig se dem, och ingen runda har rört dem. De hörde i samma jobb som
(b) — **och faller därmed med det: de står kvar med avsikt.** En tillgångssökväg spelar bara roll
om ytan publiceras, och ytorna ska inte publiceras (omfångsbeslutet ovan). Uppräkningen nedan
står kvar som karta, för den dag någon ändå döper om katalogen. **Skrivet ut per yta med sökväg här så att nästa läsare inte tror att namnbytet var
fullständigt i filsystemet bara för att det var fullständigt i prosan** — och **inte** bara för
webbytan, vilket var den första versionen av den här punkten och lämnade läsaren med knappt
hälften.

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

**Och i samma fil, av exakt samma skäl: TOC-vaktens sentinel är `apple-intelligence` — alltså
nästa guides namn.** `scripts/tests/test_guide_toc.py:133-138`:

```python
def test_an_unknown_guide_is_a_loud_error():
    with pytest.raises(KeyError) as exc:
        config_for("apple-intelligence")
    assert "copilot" in str(exc.value) and "gemini" in str(exc.value)
```

Det är **samma anti-mönster som Task 12 rev ut** ur `test_guide_surface_consistency.py`, där
sentinel var `"gemini"` och alltså var programmerad att gå sönder i samma sekund Gemini lades i
kartan. Den vakten använder nu `"ingen-sådan-guide"`, med skälet utskrivet i en kommentar — men
TOC-vakten, som byggdes i **samma runda**, återinförde mönstret med nästa guides namn.

Kostnaden är lägre än ankarsprödhetens: felet blir **högljutt** (testet faller på
`pytest.raises`, inte tyst grönt) och assertionen på `"copilot"`/`"gemini"` faller också, så det
är omöjligt att missa. Men det hör ändå här, intill ankarna, eftersom **det är Apple
Intelligence-rundan själv som bryter det, i den fil den just kopierat.** Byt till ett namn som
aldrig kan bli en guide, och assertera mot `config_for`:s kända nycklar i stället för mot två
hårdkodade strängar.

### En förbättring nästa runda bör göra — inte en lucka

**`scripts/tests/pdf_body_text.py`:s `PLAYWRIGHT_FOOTERS` är handkopierad** ur byggarnas
`jobs`-listor i stället för härledd ur dem. Det är exakt den klass av inaktualitet som lät
byggarens sidfot bära det pensionerade produktnamnet på 43 sidor genom hela rundan. Modulens
egen docstring dokumenterar handkopieringen som **avsiktligt mönster för alla
`footer_template`-guider** (apple-intelligence, copilot och ai-for-elever bär samma), så att
härleda den live stänger luckan för **varje** guide, inte bara den här. Tvärgående
refaktorering; hörde inte i den här rundans fillista.

### Johans redaktionella pass (Task 18, 2026-10-13) — titeln, rösten, dubbleringarna

**Tre** av de fynd som stod uppskjutna nedan är **stängda på Johans beslut 2026-10-13** — de
tre dubblerade passagerna (c), Fristadsskolan-exemplet (d) och `Johan` mot `I` (b). Räkna talet
mot den uppräkningen, de tre bokstäverna i föregående mening: listan över uppskjutna fynd gick
från sex poster till tre genom att precis de tre lyftes ut.
**Titelbytet (a) var aldrig ett uppskjutet fynd** och räknas alltså inte in här. De tre står
inte längre öppna, och nästa runda ska inte "rätta" tillbaka något av det här.

**(a) Titeln heter nu `Gemini & Gemini Notebook for educators`.** Sju ställen: EP rad 5
(`<title>`) och 462 (`<h1>`), EW rad 6 (`<title>`, suffixet `— Johan Lindström` kvar), 8
(`og:title`) och 49 (`<h1>`), `exports/build-gemini-notebook-pdf.py` rad 61 (löpande sidfot,
HTML-escapad `&amp;`) och `scripts/tests/pdf_body_text.py` rad 85 (speglad literal, oescapat
`&`). Byggarens rad 66 — det svenska jobbets sidfot — står orörd, och de svenska PDF:erna är
byte-identiska med bascommiten.

**Quick-starten följde efter på Johans beslut 2026-10-13** (Task 19), så att de två engelska
ytorna inte annonserar olika publik: `_unpublished/exports/gemini-notebook-quick-start-en.html`
rad **5** (`<title>… Quick Start — for educators`, tankstrecket behållet) och rad **176**
(`<span class="eyebrow">… Quick Start · for educators`, mittpunkten behållen). Det var filens
**enda** två förekomster av `for teachers`. **Ingen speglad literal att uppdatera:**
quick-start-byggaren har ingen `footer_template` utan en `.page-footer`-div i HTML:en, så
sidfoten parsas live ur mallen via `PAGE_FOOTER_TEMPLATES` — `PLAYWRIGHT_FOOTERS` rör inte
quick-starten och ska inte göra det. Quick-startens tryckta `44-page` rör **huvudguiden**, inte
sig själv, och står oförändrat.

**AVVIKELSEN ÄR AVSIKTLIG.** Systerguiderna heter `… for teachers and school leaders`
(apple-intelligence, copilot). Gemini avviker nu från familjen, på Johans beslut, och i linje
med sajtens egen underrubrik `AI & Digitalization for Educators`. **Den som tar in nästa guide
ska inte läsa avvikelsen som ett slarvfel och harmonisera bort den.**

**(b) Författaren omtalas konsekvent som `I`.** De två tredjepersonsmeningarna i prosan är
omskrivna: EP 823 → **822** / EW 322 → **321** (`Johan's 140 Gemini Notebook styles` → `My 140
Gemini Notebook styles`) och EP 843 → **842** / EW 342 → **341** (`Johan has built a library of
140 styles` → `I have built a library of 140 styles`). **De åtta kvarvarande `Johan`-förekomsterna på EP är inte prosa och
ska stå:** omslagets byline, signaturen, kolofonen, licensraden, etiketterna `Johan's Note`
(två) och `A note from Johan`, samt en CSS-kommentar. **En etikett är en skylt, inte prosa.**

**(c) De tre dubblerade passagerna är avdublicerade, och ägarskapet står här.**

| passage | ÄGER den | avdublicerad |
|---|---|---|
| Matt Miller-citatet ("becomes an instant expert on the documents you give it") | **sidan 6** (EP 636 / EW 123, orörda) | sidan 10 (EP 719 / EW 209, oförskjutna) — citatmeningen borttagen, styckets egen poäng (att det mesta lärare behöver ligger mellan de två verktygen) står kvar ordagrant |
| "the two sides stay complementary" + webbsök/Video Overviews + April 2026-lanseringen till Ultra/Pro/Plus | **sidan 6** (EP 641 / EW 128, orörda) | sidan 18:s integrationsruta (EP 847 → **846** / EW 348 → **347**) — de två upprepande slutmeningarna borttagna; rutan slutar nu på sin egen poäng ("You get a grounded answer **and** a creative classroom resource in one interaction") |
| Eric Curts / `edugems.ai`-beskrivningen med sitt förbehåll | **sidan 14** (EP 789 → **788** / EW 284 → **283**) | sidan 21 (EP 909 → **908** / EW 415 → **414**) — raden är nu en korsreferens: "The edugems.ai library covered in Part 2 is as good a starting point for a department as it is for one teacher." Sidan 42:s korta resursrad (EP 1576 → **1575** / EW 1171 → **1170**) står kvar, den hör i en resurssammanställning |

**Inget nytt påstående infördes**, och inget citat tillskrevs någon. Sidan 6 äger
Miller-citatet i exakt den ordalydelse granskaren verifierade mot `ditchthattextbook.com`
(se G20); sidan 10 har inget citat alls i stället för ett nytt.

**(d) Säfströms/Folkebrants Fristadsskolan-exempel gick från tre till två förekomster per yta.**
Borttagen är **sidan 11**:s `Extra example:` under "2 · Generate a podcast from your unit plan"
(EP 730 / EW 220). **Kvar står:** sidan 16:s `The anchor example worth knowing` i
Audio Overviews-avsnittet (EP 831 → **830** / EW 330 → **329**) och sidan 20:s
avdelningsvinkel (EP 896 → **895** / EW 402 → **401**).
 Skälet: "Five quick wins"-avsnittet har
andra konkreta exempel (Year 7-geografiläraren under punkt 1, policyjämförelsen under punkt 4),
medan Audio Overviews-avsnittet skulle ha tappat sitt **enda namngivna klassrumsexempel** —
och sidan 11:s förekomst var dessutom inramad som en bisats, inte som avsnittets ankare.
G21:s två vaktrader (`Fristadsskolan`, `Pedagog Eskilstuna`) är mätta efteråt: **två
förekomster var per yta, båda strängarna på båda ytorna.** Ordet `Sweden` står **oförändrat två
gånger per yta** — sidan 11:s förekomst bar det inte — så vaktblockets kommentar i
`docs/guide-facts-gemini.md` stämmer fortfarande och är inte rörd.

**Alla radnummer ovan är skrivna `före → efter`.** Borttagningen av EP 730 / EW 220 flyttade
varje rad efter den ett steg upp på respektive yta; titelraderna (EP 5, 462; EW 6, 8, 49) ligger
före brytpunkten och står kvar.

**Pagineringen rörde sig inte.** Guiden är fortfarande **44 sidor**, och förteckningens tio
sidnummer är oförändrade (`3 5 8 13 20 23 27 30 32 41`) — mätta mot den omrenderade PDF:en,
varje ankare på sin kartlagda sida. Quick-startens tryckta `44-page` stämmer därför också
fortfarande. `XFAIL_UNTIL_RECOUNTED` och `XFAIL_UNTIL_RERENDERED` är tomma och lämnas tomma.

**Posttabellens radnummer i `docs/guide-facts-gemini.md` är nu ett steg efter på EP från rad 730
och på EW från rad 220** (G20:s och G21:s kolumner, plus G19:s). Posttabellen läses aldrig
maskinellt (`factinventory.load()` läser bara vaktblocket), så ingen vakt är röd för det — men
den som läser tabellen som karta ska veta att den pekar en rad fel efter borttagningen. Hör i
samma svep som G49:s oescapade pipe och G27-aritmetiken.

**Och två postceller är nu inaktuella i SAK, inte bara i radnummer.** Båda beskriver ett läge
som inte längre gäller, och båda står kvar orörda — Task 18 fick inte röra någon postrad eller
vaktrad, och en halv rättning av en cell vars utfallstext bär hela rundans resonemang är värre
än en cell man vet är daterad:

- **`docs/guide-facts-gemini.md:88` (G21)** säger `utökad med en tredje förekomst per yta
  ("Extra example…") som briefen inte listade` och listar tre platser per yta
  (`220, 330, 402` / `730, 831, 896`). **Efter Task 18 finns två**: `329, 401` på EW och
  `830, 895` på EP. Beslutet att behålla exemplet står kvar och gäller — det är **antalet** som
  är inaktuellt, inte beslutet. Vaktraderna `G21 | en | Fristadsskolan | aktiv` och
  `G21 | en | Pedagog Eskilstuna | aktiv` är mätta mot de två kvarvarande och håller.
- **`docs/guide-facts-gemini.md:116` (G49)** trycker fortfarande den **gamla titeln** som
  gällande i sin beskrivning av namnbytet. Titeln är sedan 2026-10-13
  `Gemini & Gemini Notebook for educators`.

**Den som nästa gång ändå är inne i posttabellen** tar de två cellerna, radnummerskiftet, G49:s
oescapade pipe och G27-aritmetiken i ett svep — det är samma jobb.

**(e) En fjärde dubblering — AVGJORD, inte uppskjuten. Johans beslut 2026-10-13: båda står.**
**Classrooms fyra mall-Gems räknas upp två gånger**, med samma fyra namn (Study partner,
Quiz me, Brainstorm partner, Real-world connector), på sidan 14 (EP 788 / EW 283) och sidan 21
(EP 908 / EW 414). Dubbleringen hittades i Task 18 och lades fram för Johan. **Hans skäl att
behålla båda:** sidan 21 sitter i ett avsnitt om **delade Gems för arbetslag**, så vinkeln är en
annan; fyra namn är kort; och en läsare som hoppar in på sidan 21 får dem direkt utan att
bläddra tillbaka.

**Det här är alltså inte ett olöst fynd, och nästa runda ska inte "rätta" det.** Skillnaden mot
de tre stängda ovan är bara utfallet: där blev beslutet *ta bort*, här blev det *behåll*. Båda
meningarna står oförändrade och ska stå.

### Tre fynd ur genomläsningen som rundan medvetet INTE åtgärdade

Alla tre är **preexisterande**. Att de står här och inte i en uppgift är ett beslut, inte ett
förbiseende — ett fynd som inte åtgärdas skrivs ut, aldrig stryks tyst.

1. **Figurens axeletikett `RISK →` renderas ingenstans.** En rotate-transform placerar den på
   x = −60, utanför `viewBox`. Felet finns på **alla fyra ytor**, inklusive de svenska.
   Figurens fyra nivåer är etiketterade ändå, så förlusten är axelns riktningspil.

   **Skälet att skjuta upp den, omskrivet 2026-10-13 — det gamla skälet höll inte.** Fram till
   slutgranskningen stod här att *"en korrekt lagning rör de frusna svenska ytorna och ändrar
   deras PDF-byte, vilket spec §1 förbjuder"*. **Det är fel.** En fix på bara de **två engelska**
   ytorna lämnar de svenska bytena orörda, och de engelska PDF:erna renderas om ändå i varje
   runda som rör innehåll. **Den är alltså billig: två ytor, en commit, ingen spec-konflikt.**

   **Beslutet att skjuta upp står ändå**, men på sitt riktiga skäl: det är en **kosmetisk
   figuretikett i ett dokument vars fyra nivåer redan är etiketterade**, och den låg utanför
   varje uppgifts fillista.

   **Och efter omfångsbeslutet 2026-10-13 är den ännu billigare än raden ovan säger:** det
   finns inget kommande svep som tar de svenska ytorna, för de är frysta permanent och
   distribueras inte. **Jobbet är därför bara de två engelska ytorna — en commit — och det är
   hela jobbet, inte halva.** Att "laga alla fyra samtidigt" är inte längre det prydligaste
   alternativet; det är ett alternativ som inte finns. **Tro inte att en billig fix är
   förbjuden.**
2. **Den svenska quick-starten säger "39-sidiga" om en 42-sidig svensk guide.** Preexisterande,
   på en frusen yta. **Efter omfångsbeslutet 2026-10-13 står den kvar permanent:** ytan
   distribueras inte och når ingen läsare, så det finns inget jobb kvar att vänta på — "samma
   jobb som de svenska filnamnen" var det, och det jobbet är avblåst.
3. **`capture_guide_baseline.py` rapporterar 45 sidor för en 44-sidig PDF.** **Inget defekt:**
   `pdf_fingerprint.pages()` delar på sidbrytningstecken och ger en avslutande tom post
   (verifierat: 43 poster för den 42-sidiga versionen, 45 för den 44-sidiga). Skriptets
   utskriftssträng är en kosmetisk felmärkning, inte en felräkning.

### Två fynd av samma slag, ur slutkontrollen och helgranskningen

Inte ur genomläsningen, alltså inte med i de tre ovan — men samma kategori: preexisterande,
läsarsynliga i liten skala, och medvetet lämnade med utskriven åtgärd.

**1. Ett av AI Act:s fyra datum är inte fetat medan de tre andra är.** Meningen *"Four dates
matter, and only two of them bind you yet"* bär `<strong>` på `2 February 2025`,
`2 August 2026` och `2 December 2027` — men **`2 August 2028` står bart**, så en skummande
rektor räknar tre datum i en mening som säger fyra. **Exakt åtgärd, en tagg per yta:**

| yta | rad | ändring |
|---|---|---|
| `_unpublished/exports/gemini-notebook-print-a4-en.html` | 1023 | `from 2 August 2028` → `from <strong>2 August 2028</strong>` |
| `_unpublished/guides/gemini-notebook/index.html` | 534 | samma |

(Radnumren var 1024 och 535 fram till Task 18; borttagningen av EP 730 / EW 220 flyttade dem ett steg upp.)

**Lämnad med avsikt:** enda åtgärden rör den **levererade PDF:en** och kostar en omrendering
plus en selektiv facitomfångning — oproportionerligt för ett `<strong>`.
**Publiceringsrundan renderar om ändå och kan ta den gratis då.**

**2. `docs/guide-facts-gemini.md`:s postrad för `G49` har tio pipes där de 49 andra har nio.**
En **oescapad `|` i källkolumnen** delar den i två fält, så kolumnerna glider ett steg från
källan och framåt. Preexisterande — bekräftat genom att köra samma pipe-räkning mot
`git show HEAD:`, identisk form där. **Ofarligt för vakten, men inte av det skäl man först
gissar:** `factinventory.load()` läser **bara vaktblocket**, aldrig posttabellen (se modulens
docstring), så ingen vakt har någonsin tittat på den raden — samma strukturella sak som den
tredje vaktluckan ovan. En **människa** som läser tabellen ser däremot en kolumn glida.
**Hör i samma svep som G27-aritmetiken:** nästa gång någon ändå är inne i tabellen, escapa
pipen.

### ⚠️ NÄSTA RUNDAS FÖRSTA INNEHÅLLSUPPGIFT: `pre-market obligations`

**Det enda öppna fyndet som är läsarskadligt, och det ska inte vara svårt att hitta.** Därför
står det i sin egen rubrik och inte som en fotnot bland de uppskjutna.

Bonuskapitlet (print 1056) säger att högrisk medför *"formal pre-market obligations: risk
assessment, dataset quality management, logging, documentation"*.
**Förhandsbedömningsplikterna faller huvudsakligen på LEVERANTÖREN**; en skola som bara
**driftsätter** ett system bär i stället deployer-plikter — ett annat och mindre krävande
åtagande.

**Varför det är värre än de andra uppskjutna fynden:** det lägger leverantörens plikter på
läsaren, i en PDF som säljs till skolledare, i det kapitel som finns till för att säga vad som
binder dem. Samma felriktning som rundans allvarligaste fynd (G48, som sa att
högriskskyldigheterna redan gällde) — och det här är den enda av den klassen som står kvar.

**Varför rundan inte rättade det:** preexisterande, orört av rundan, och en korrekt rättning
kräver en källa ingen verifierat. Att skriva en rättslig distinktion utan post i inventeringen
hade brutit rundans enda oeftergivliga regel. **Det är alltså en hämtning som behövs, inte ett
omdöme** — och med den hämtningen gjord är rättelsen en mening på två ytor.

### Tre kända luckor

1. **Claude-guidens femton TOC-nummer står ovaktade.** `test_guide_toc.py` tar inte in dem;
   varför står i filens docstring. De två andra guiderna är vaktade.
2. **`_unpublished/guides/apple-intelligence/` och `_unpublished/guides/ai-for-students/` bär
   fortfarande Crestioras typsnitt**, inklusive inline-`font-family`-attribut i SVG. De står
   därför inte i `test_fonts.GUIDE_WEB_SURFACES`. Städas i sina egna rundor.
3. ~~**Quick-startens pekare till guidens egen adress svarar 404 så länge guiden är
   opublicerad.**~~ **STÄNGD 2026-10-13 (Task 21): pekaren är borttagen.** Omfångsbeslutet gjorde
   404:an permanent i stället för tillfällig — sidan kommer aldrig att finnas — så adressen är
   struken ur quick-starten i stället för att vänta på en publicering. Avslutningsraden säger nu
   att guiden följer med i communityt, utan adress. Apple Intelligences quick-start bär **samma
   fel olagat**; se omfångsbeslutets punkt (d).

### Fem rättelser till specen, så att nästa guide mäter på rätt saker

1. **Webbytans typsnittsfel var tre gånger större än specen sa.** Utöver tre `<link>`-rader och
   tre `--font-*`-överskrivningar bar webbytan **sjutton inline-`font-family`-attribut i
   SVG-`<text>`-element** (sex `Playfair Display`, elva `Inter`). Ett inline-attribut vinner
   över varje `:root`-token, så felet går **inte** att se i en CSS-granskning. Copilots båda
   ytor hade noll sådana attribut — fällan var ny. Vaktas nu av
   `test_the_guide_web_surfaces_have_no_crestiora_fonts`.
2. **"AI Act stannar" betyder inte "AI Act är orörd".** Specen sa att AI Act-fakta *redan är
   belagda* i Claude-inventeringens post P13. Det stämde — och **FEM av dem var belagda som
   felaktiga**, med rättningen redan levererad i den publicerade Claude-guiden:

   | # | post | stod i Gemini-guiden | P13:s belagda värde |
   |---|---|---|---|
   | 1 | G25 | "phases in through 2026 and beyond" | **became applicable on 2 August 2026** |
   | 2 | G48 | högriskskyldigheterna gäller sedan 2 augusti 2026 | bilaga III-högrisk, som uttryckligen omfattar utbildning, gäller från **2 december 2027** |
   | 3 | G26 | "Prohibited" | **Unacceptable risk** |
   | 4 | G26 | "Limited risk" | **Transparency risk** |
   | 5 | G26 | "Minimal risk" | **Minimal or no risk** |

   **Rad 3–5 är tre av de fyra risknivånamnen** — bara `High risk` var redan rätt. En
   korsreferens till P13, ingen ny källdomän.

   **Talet är fem, inte fyra.** "Fyra" är specens inramning och stod i två av det här
   dokumentets rader fram till slutgranskningen, intill en uppräkning som räknade fem.
   Inventeringen avgör: G25 bär en rättelse, G48 en, G26 **tre**. Det är **fjärde instansen av
   felklassen "ett tal i prosa intill tabellen det räknar"** — och den mest konsekvensbärande,
   eftersom det är den rättelseklass som säger skolledare vad som binder dem.

   **Om du räknar om nivånamnen i ytan: skriv ut vilken bas du mäter på.** Rå HTML-grep ger
   `Unacceptable risk` 3, `Transparency risk` 4, `Minimal or no risk` 5, `High risk` 4;
   **taggstrippad text ger 2 / 3 / 4 / 3.** Skillnaden är exakt ett per namn och kommer från
   pyramidens HTML-kommentar, som bär den gamla taxonomin i sin förklaring. **Båda talen är
   rätta på sin bas** — de pensionerade namnen står på **0** i båda. Ett tal utan sin bas blir
   nästa läsares "fel".
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

### Den tredje vaktluckan: TOC-underraderna är strukturellt ovaktbara

Rundan betalade för två vaktluckor och hittade en tredje i slutgranskningen. **Alla tre har
samma form: text som bor där inget av vaktlagren tittar.**

| # | luckan | vad den kostade |
|---|---|---|
| 1 | **prosa i Python** — byggarens `footer_template` | det pensionerade produktnamnet på 43 av 44 sidor, osynligt för varje HTML-läsande vakt |
| 2 | **en summa i prosa intill tabellen den räknar** — inventeringens utfallsräkning | fyra tal som tystnade när G50 tillkom; fjärde instansen hittad i slutkontrollen |
| 3 | **innehållsförteckningens underrader** (ny, oåtgärdad) | ingenting ännu — men se nedan |

**Luckan.** `scripts/tests/test_guide_toc.py:100`:s radregex kastar uttryckligen bort
`<span class="toc__sub">`, så de tio underradernas **text** jämförs aldrig mot någonting.
TOC-vakten läser rubrik och sidnummer; underraden är inte med.

**Och ytkonsistensvakten kan inte ta över.** Underraderna finns **bara på printytan** — tio
`toc__sub`-element i EP och **noll** i EW (`grep -c` ger EP 11, varav en är CSS-väljaren) — och
`surfacecheck`:s `aktiv`-semantik kräver att
strängen står på **båda** ytorna. En `aktiv`-rad på en underrad vore alltså
**permanent `saknas_på_en_yta`** — röd från första sekunden, för innehåll som är korrekt.

**Varför den är seg: det är inte en glömd rad, det är att de två vaktlagren utesluter varandra
på just de raderna.** TOC-vakten ser raden men inte dess text; ytvakten kan se text men bara
text som står på två ytor. Att stänga luckan kräver antingen att TOC-vakten börjar jämföra
underradstext mot ett facit, eller att ytvakten får en enytessemantik — båda är vaktarbete, och
rundans beslut är att nästa guide inte ska behöva ändra någon vakt.

**Vad som står oskyddat i dag.** Två underrader bär **självräkningar** om dokumentet:

| underrad | påstår | mätt i EP | |
|---|---|---|---|
| Prompts | *"**25** starter prompts for Gemini and Gemini Notebook"* | **25** `prompt-card`-element | ✅ sant |
| The Styles Library | *"**Eight** curated entry points from **140** Gemini Notebook styles"* | **8** `style-card`-element | ✅ sant |

**Båda är sanna i dag** — men ingen av dem har en post i inventeringen, medan **samma klass av
påstående har det**: G40 vaktar FAQ:ns elva frågor, G41 Del 2:s fem arbetsflöden. Och rundan
rättade bonuskapitlets underrad **för hand** (Task 7, när kapitlets skylt skärptes), vilket är
precis vad man gör när ingen vakt finns. **Det är alltså en inkonsekvens i inventeringen, inte
bara i vaktlagret:** två självräkningar om dokumentet står utan post därför att vakten inte
kunde bära dem, inte därför att någon bedömde dem ovolatila.

**Billigaste halvmesyren, om nästa runda vill en:** ge de två underraderna poster i
inventeringen med `aktiv`-rader på **printytan via leveransvakten** (`test_guide_delivery.py`
läser PDF:en och har ingen tvåytesregel) i stället för via ytkonsistensvakten. Det är samma
grepp som quick-startens sidantalspåstående fick i Task 16B.

### Fjärde instansen av samma felklass — och den här gången i auktoritetsdokumentet självt

**Rättad i slutkontrollen.** `docs/guide-facts-gemini.md`:s utfallsräkning påstod korrekt
**50 poster** med tre rätta delsummor (30 + 14 + 6), men **uppräkningarna** inne i raderna
listade tillsammans bara 49 id:n — **G27 stod i ingen av dem** — och underrubriken till
andra-token-tabellen ärvde nämnaren som *"Tjugofyra av 49 celler"*. G27 är `stämmer` och står nu
i den raden; nämnaren säger 50. Verifierat med `comm` mot postlistan (tom symmetrisk skillnad)
och med en delsummekontroll (varje rad påstått = uppräknat, uppräkningen disjunkt och komplett).

**Lärdomen är klassen, inte talet.** Det här var rundans **fjärde** fall av samma sak: G48:s
revisionsnotis, G37:s notis och G13:s cell sa alla något om en yta som inte längre stämde, och
alla tre rättades i sina egna uppgifter. Det fjärde satt i **inventeringen självt** och hittades
först i slutkontrollen, när ingen uppgift längre ägde filen.

**Vad som gör klassen seg: ett tal som står i prosa intill tabellen det räknar har ingen vakt
som kan se när tabellen växer.** `factinventory.py` läser postradernas *struktur* och blir röd om
en rad går sönder — men en summa, en nämnare eller en uppräkning i löpande text är för vakten
bara text. G50 tillkom i Task 9 och tre tal runtom den blev tysta i samma sekund. **Varje gång
en post läggs till i en inventering ska uppräkningarna räknas om, och helst mätas i stället för
läsas** (`comm` mellan postlistan och uppräkningen tar tre sekunder och kan inte ha fel).

---

## Hygienrundan 2026-10-13 — datumets självreferens, och fyra ytor utan synlig funktion

Gren `fix/seo-date-selfreference`, tre commits, avstamp `main` = `4547f4d`. Svit **805 passed,
0 failed, 0 skipped, 0 xfailed, 0 xpassed** med `test_prompt_pdf_parity.py` undantagen (dess 11
fel är de miljöberoende). Båda jobben var samma sak: **en invariant som bara levde i ett
dokument, flyttad in i en vakt.**

### (1) `build-seo-meta.py` läste sitt eget utdata — STÄNGT

`git_lastmod()` tog datumet för senaste commit som rörde filen. Men skriptet **skriver** det
datumet in i filen — i `page-last-updated`-blockets `<time>`, i JSON-LD:s `"dateModified"` och i
sitemapens `<lastmod>`. Att skriva stämpeln är alltså en ändring av filen, och nästa körning
läste sitt **eget förra utdata** som om innehållet ändrats. Verifierat ordagrant: commit
`9c6390c` ändrade `about/index.html` på fyra rader, och alla fyra bar ett datumfält.

**Det är fälla 6 nedan, och den är nu stängd i koden i stället för i en varning.**

**Sprängvidden var 13 filer, inte 6.** Mätt genom att köra skriptets egen per-fil-logik över
alla 195 filer i scope med gammal och ny `git_lastmod` och jämföra utfallet: utan fixen hade en
körning 2026-10-13 skrivit `2026-10-13` på `about/`, `prompts/`, `wise/`, `notebooklm-styles/`,
deras fyra svenska motparter, och **fem blogginlägg** — de sista har ingen synlig stämpel men
bär `dateModified` i sitt `Article`-schema, vilket är varför en inventering som bara tittar på
section landings med synligt block räknar fel. Med fixen: **0 filer.**

`git_lastmod()` går nu bakåt genom filens commits och stannar vid den första som säger något om
innehållet. En commit hoppas över när skriptets egna rader sorterats bort ur diffen och resten
är lika på båda sidor — se "Regressionen i (3)" nedan för varför det blev en restjämförelse och
inte ett krav på datummarkörer. Fallbacken på mtime och sedan dagens datum är orörd. Vakten är
`scripts/tests/test_seo_lastmod.py`, som bygger riktiga git-repon i temporära kataloger: fem
tester, varav två är över-hoppningsprov som fäller en spärr som hoppar över för mycket. Varje
vakt sågs röd mot den implementation den skulle fånga innan den litades på.

**Kostnad: en full körning går från ~5,0 s till ~12,2 s** (`git log` plus ett `git show` per
fil). **Ingen cache byggd** — en cache måste invalideras på HEAD och vore mer kod än fixen.

**Sitemapens sexton evidence-rader gick `2026-10-09 → 2026-10-08`** i samma körning: `ae6dd1e`
är en **merge-commit** och ger tom diff, så det sanna datumet är `63b33ba`, 2026-10-08.

### (2) De fyra guide-webbytorna är interna kontrollkopior — nu synligt i filerna

`_unpublished/guides/{ai-for-students,apple-intelligence,copilot,gemini-notebook}/index.html`
behålls **bara** för att vara andra halvan i ytkonsistensvakten. Guiderna distribueras via
Skool, inte via sajten, så de publiceras aldrig. Fram till nu stod det skyddet bara i punkt (c)
ovan, och en städrunda som läste filträdet såg fyra opublicerade HTML-sidor utan funktion.

**Två vakter i `scripts/tests/test_guide_surface_consistency.py`.**
`test_every_unpublished_guide_web_surface_is_accounted_for` läser **filträdet** och kräver att
varje `_unpublished/guides/*/index.html` står antingen i `surfacecheck.GUIDE_SURFACES` eller på
`UNMAPPED_GUIDE_SURFACES`. `test_the_debt_list_cannot_rot` fäller tre ruttnings-riktningar: en
post vars fil försvunnit, en post som samtidigt står i ytkartan (skulden betald men posten
kvar), och en post utan skäl. Båda sågs röda med flit — en femte katalog fällde den första,
och alla tre riktningarna den andra.

**`UNMAPPED_GUIDE_SURFACES` är en SKULD SOM SKA TÖMMAS, inte en parkering.**
`apple-intelligence` och `ai-for-students` står där för att de ännu saknar påståendeinventering;
utan den kan ingen vaktrad peka på ytan, och en post i ytkartan utan inventering är en tyst vakt
som `test_every_guide_has_an_inventory_file` redan förbjuder. **Varje guides egen runda
kartlägger sin yta, flyttar den härifrån in i ytkartan, och listan krymper. Är listan tom ska
både den och dess två vakter strykas** — de vaktar ingenting då.

**Och en banner i toppen av alla fyra filerna**, så att den som städar läser filen och inte
överlämningen. Den ligger mellan doctype och `<html`, utanför `<body>`-flödet, och har **inget
`>` i kommentarens innehåll** — avslutande `-->` bär förstås ett, och det är just det som ska
vara det första `>`:et, för `surfacecheck._TAG` (`<[^>]+>`) matchar fram till det. Står det ett
`>` inuti klipps kommentaren där, och resten blir läsbar text i den normaliserade ytan. Mätt, inte antaget: de normaliserade
ytorna är oförändrade **på tecknet** (copilot en 46 978 / sv 42 871, gemini en 93 029 /
sv 91 307, delta 0) och vaktraderna lika många och lika gröna (copilot 10 aktiv / 22 borttaget,
gemini 39 / 52, noll problem). Ingen PDF och ingen printyta rördes.

### (3) `/infographic-styles/` och `/sv/infografik-stilar/` är nu section landings

De två bar ett **föräldralöst** `page-last-updated`-block, fruset på `2026-04-24`: de togs ur
`SECTION_LANDINGS` vid omdöpningen `4ceaf43` (*refactor(nav): rename NotebookLM Styles →
Infographic Styles*, 2026-04-26): katalogen bytte namn och tog blocket med sig, medan
`SECTION_LANDINGS` behöll den gamla nyckeln `/notebooklm-styles/`. **`/infographic-styles/` har
alltså aldrig stått i listan** — `git show 252a374:scripts/build-seo-meta.py` visar den gamla
nyckeln men inte den nya, och stämpeln `2026-04-24` är äldre än omdöpningen, vilket stämmer med
den bilden. Skriptet skriver blocket bara för section landings — så det
varken uppdaterades eller togs bort. Johans beslut 2026-10-13: lägg in dem igen, med
`CollectionPage` som systrarna. Blocket **adopterades på plats** via sina markörer (ett block
per fil efteråt, inte två) och visar nu `2026-10-07`. Renderat och granskat vid 1280 px och
320 px: stämpeln sitter där `/prompts/` och `/sv/promptar/` har sin, med samma hårfina linje
över, samma centrering och samma 17 px — och **noll överflöd**, mätt med
`documentElement.scrollWidth - clientWidth`, samma metod som `test_responsive_overflow.py`.

### Regressionen i (3), och varför spärren ser ut som den gör

**Jobb 3 återskapade jobb 1:s bugg på exakt de två sidor det stämplade**, och granskningen
fångade det. Spärrens första version krävde en datummarkör på **varje** ändrad rad. Det håller
bara när utdatat ändrar ett datum*värde* — då bär både den borttagna och den tillagda raden
markören. När de två sidorna blev section landings ändrade utdatat **form**: JSON-LD:n fick en
helt ny `CollectionPage`-entitet, så den **borttagna** raden bar ingen markör alls, `all(...)`
föll, och commiten räknades som innehåll. Nästa körning hade stämplat om båda sidorna till
körningens datum, tyst.

**Spärren jämför nu rester i stället för att inspektera rader:** skriptets egna rader sorteras
bort på båda sidor av diffen, och det som blir kvar jämförs. Är resterna lika har commiten bara
flyttat runt det skriptet självt skrev — vilket täcker både värde- och formändring, och ger den
tomma diffen (merge, lägesbyte) på köpet. **Frågan är inte vad som står på raden utan vem som
skrev den.**

**Vad som INTE sorteras bort, och varför det är ett medvetet val:** bara de tre datumbärande
raderna (JSON-LD-blocket, last-updated-blockets aside, sitemapens `<lastmod>`). Markörparen samt
favicon-, canonical- och hreflang-raderna är också genererade, men de bär inget datum — och
`0890841`, som lade favicon på 190 filer, **är** det sanna "senast ändrat" för åtta sidor
(2026-10-07). Mätt: sorteras även de bort faller **171 av 195 sidor** tillbaka till julidatum.
Spärren ska stänga datumets självreferens, inte omdefiniera vad en innehållsändring är.

**Mätt över hela historiken efter fixen:** 1829 commit/fil-par, 221 överhoppade, och **noll** av
dem hade en icke-genererad rad ändrad. Över-hoppningsprovet åt andra hållet håller också —
`0890841`, `63b33ba`, `e1d3a4a` på `index.html` och `252a374` räknas alla som innehåll, trots att
de rör datum- eller JSON-LD-rader.

### ⚑ KVARVARANDE SKULD: `notebooklm-styles` bär det pensionerade produktnamnet

**Namngiven här för att den annars dör med rundans rapport.** Sökvägarna:

| sökväg | vad den är |
|---|---|
| `notebooklm-styles/index.html` | **omdirigeringsstubb**, `noindex`, `meta refresh` till `/infographic-styles/` |
| `sv/notebooklm-stilar/index.html` | samma, till `/sv/infografik-stilar/` |

Innehållet har alltså **redan** flyttat till `infographic-styles`; det som står kvar är de två
stubbarna och namnet i publika sökvägar. **Togs inte i hygienrundan — Johans beslut 2026-10-13:
eget ärende.** Skälet: ett namnbyte rör publicerade sökvägar, `PAIR_MAP`, og-kort, sitemap och
inkommande länkar, och kräver omdirigeringar. Båda stubbarna står i `SECTION_LANDINGS` och i
sitemapen (8 rader var för `notebooklm` respektive `infographic`), och båda får
`CollectionPage`-schema med `dateModified` trots att de är `noindex`-stubbar utan `</main>` —
de får därför inget synligt block, vilket är varför ingen dubblett uppstod. **Två påståenden om
sidan som inte är sanna, och de hör med när ärendet tas:** en omdirigeringsstubb är ingen
`CollectionPage`, och den ska rimligen inte stå i sitemapen alls — ändå har `notebooklm` åtta
rader där, lika många som `infographic`. Preexisterande, inte infört av hygienrundan.

### Fynd rapporterade men inte åtgärdade

**`docs/guide-facts-copilot.md`:s EW-radnummer glider 21 rader till.** Fynd 3 i Copilot-rundan
säger att ungefär trettio platskolumner redan ligger fel med ett efter `16bd50f`. Bannern lägger
**21 rader** (`git diff --numstat` ger `21 0` för alla fyra) i toppen av webbytan, så de ligger
nu fel med **22** — och motsvarande kolumner för
`gemini-notebook` likaså. **Ofarligt för vakten:** `surfacecheck` och `factinventory` matchar
**strängar, aldrig radnummer**; felet syns bara för en människa som läser cellen. **Behandla
EW-kolumnens radnummer i båda inventeringarna som ungefärliga**, inte exakta, tills någon är
inne i tabellen av annat skäl och räknar om dem.

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
6. **STÄNGT 2026-10-13 — `build-seo-meta.py` bumpade "Last updated"** ur git-commitdatum. **Självreferensen är lagad och vaktad** (`scripts/tests/test_seo_lastmod.py`): skriptet sorterar nu bort sina egna rader ur diffen och jämför resten, så både ändrat datum*värde* och ändrad *form* räknas som skriptets utdata. **Beviset är idempotens, inte en enstaka körning:** från rent träd efter fixen ger `build-seo-meta.py` `head updates: 0` och tomt `git status`. Rubriken sattes en gång för tidigt — den stod STÄNGT efter commit 2, medan commit 3 fortfarande fällde på formfallet. Nu är den faktiskt stängd. Historiken nedan står kvar som förklaring till varför sidor bär datum som inte stämmer med sitt innehåll, och **läs fortfarande varje diff** — fixen tar bort självreferensen, inte behovet av att titta. En körning som bara skulle lägga till länkar sätter nytt datum på sidor vars innehåll inte rörts. **Konkret i våg 2b:s slutkontroll:** en medveten körning (innehållet hade faktiskt ändrats) stämplade om 12 helt orelaterade sidor — `about/index.html`, tre blogginlägg, `guides/index.html`, `prompts/index.html` och sex till — med gamla backlog-datum (2026-05-17 till 2026-10-05) som inte har med rundan att göra, samtidigt som den **inte** rörde de två sidor rundan faktiskt ändrat (de bär ingen `last-updated`-markör alls). Alla 12 reverterades med namngiven `git checkout --` per fil innan commit. Kör skriptet, men läs varje diff — "innehållet har ändrats den här rundan" gör inte automatiskt körningen träffsäker.
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
- Plan Gemini-guiden: `docs/superpowers/plans/2026-10-12-gemini-guide-international.md` (nitton `## Task`-rubriker, grinden efter uppgift 4; Task 16B tillkom under körningen och har ingen rubrik i planen) — **rättad 14 gånger under körningen; dess tal är hypoteser och ska mätas, aldrig citeras**
- Påståendeinventeringen, Gemini-guidens facit: `docs/guide-facts-gemini.md` (50 poster, 87 vaktrader)
- Gemini-rundans avbrottsfil: `docs/superpowers/handoff/2026-10-12-gemini-runda-avbrott.md` — **ÖVERSPELAD, historik.** Allt levande ur den står i "Gemini-guiden — vad rundan lämnar" ovan
- **Gemini-rundans ledger och uppgiftsrapporter finns inte kvar efter leverans.** Samma skäl som våg 2b:s: de låg i worktreens `.superpowers/`, som är gitignorerad. De 60+ rulings som togs under körningen är inarbetade i det här dokumentet där de överlever rundan
- Gren Gemini-guiden: `feat/gemini-guide-international` — **inte pushad, ingen PR öppnad 2026-10-12**
- Märkets bruksregler: `docs/brand-mark-usage.md`
- Beslutsloggar och PR-texter: `~/Desktop/choosewise-spar-a-forslag/`
- PDF:erna att titta på: `~/Desktop/choosewise-guider-vag2a/` (kopior — kan vara inaktuella)
