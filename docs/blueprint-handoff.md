# Blueprint — överlämning

**Senast uppdaterad:** 2026-10-07
**LÄS FÖRST** vid fortsättning. Specen är den bindande auktoriteten, planerna argumenterar från den.

---

## Var allt står just nu

| Del | Läge |
|---|---|
| **Våg 1** — sajtens färg och typografi | **MERGAD** som `851c9f5`, live på choosewise.education |
| **Spår A** — märket, favicon, Skool | **PR #29 öppen**, gren `feat/blueprint-track-a-mark`, 15 commits, ej mergad |
| **Våg 2a** — guidernas tryckmallar | **PR #30 öppen**, gren `feat/blueprint-wave-2a-guides`, 23 commits, svit 470, ej mergad |
| **Våg 2b** — guidernas innehåll | Inte påbörjad |
| Diagram- och social-exporterna | Inte påbörjad, Johans beslut: egen runda |
| Visual Codes Vol. 1–3 | Inte påbörjad, **ingen plan äger den** |

**Arbetskopian står på `feat/blueprint-wave-2a-guides`.** Johan har ~26 ocommittade filer under `exports/` och `assets/pdfs/wise/` som är hans eget attributionssvep. De ska aldrig commitas av det här arbetet.

De två öppna PR:erna rör inte varandra och kan mergas i valfri ordning.

---

## Nästa steg, i ordning

1. **Johan mergar PR #29 och #30** när han sett dem. Faviconen landar på 198 sidor i samma stund #29 mergas; #30 byter ut 22 guide-PDF:er varav 9 är publicerade.
2. **Våg 2b — guidernas innehåll.** Fem guider i två språk, 10 sidor och 18 PDF:er, skrivna i april 2026. Varje faktapåstående ska kontrolleras mot verkligheten i båda språken. Specen §8 kallar detta en del av leveransen, inte en senare ambition, eftersom guiderna ska ligga som medlemsvärde i Skool. **Ingen plan finns än.**
3. **Diagram- och social-exporterna.** Åtta mallar plus SVG, PNG och PDF för WISE och RÄTT. Johans beslut 2026-10-06: egen runda, gärna ihop med märket. Sju av åtta bär hans ocommittade ändringar — han bör commita svepet först.
4. **Visual Codes Vol. 1–3** i `~/Projekt/Choosewise/visual-codes-pdf/`, utanför repot. Specen §8 räknar dem till våg 2; varken 2a:s eller 2b:s plan nämner dem. Tredje kopian av paletten.
5. **NotebookLM-dokumentet** — se "Känt trasigt" nedan.

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

---

## Vad som vaktar vad

Fyra lager, byggda i våg 2a. Ändra inget utan att veta vilket lager som äger frågan.

| Lager | Fil | Äger |
|---|---|---|
| Sidvist textfingeravtryck | `scripts/tests/test_guide_pdf_parity.py` | att ingen text flyttar sig inom eller mellan sidor |
| Dokumentnivåinvariant | `scripts/tests/test_guide_pdf_body_text.py` | att inget innehåll försvinner — kromet strippas, så ompaginering kan inte röra det |
| Renderingsvakt | `scripts/tests/test_guide_pdf_font_weights.py` | att ingen PDF bäddar in ett typsnitt över viktskalan, även när vikten kommer ur HTML och inte CSS |
| Statiska mallvakter | `test_guide_print_css.py`, `test_guide_asset_paths.py`, `test_build_scripts.py` | källan: palett, typsnitt i `font-family`-kontext, vikter, sökvägar, och att varje väljare i den delade stilmallen ligger i en SCOPE-GUARD-region med sin `.page--`-scope |

**Facit ligger i `scripts/tests/fixtures/`.** Fånga aldrig om det för att få grönt. Fånga om det bara när innehållet ändrats med avsikt, och verifiera då att bara de avsedda posterna rör sig.

---

## Fällor som kostat tid i det här programmet

1. **En kontrastsiffra härledd ur deklarerad CSS är inte bevisad.** Chromiums print-economy-läge ändrade tyst färger i sidfotskontexten: en siffra mätt till 10,63:1 renderade i verkligheten 4,57:1 tills `print-color-adjust: exact` lades till. Pixelmät i den renderade filen. Gäller bakåt mot våg 1 och spår A.
2. **Fråga alltid: skulle det här testet bli rött om felet kom tillbaka?** Våg 1 sköt fyra tester som inte kunde fallera. Våg 2a hittade flera till — en tom parametrisering, en vakt som bara läste mellan markörer, en delsträngsmatchning. Bryt vakten med flit och se den bli röd innan du litar på den.
3. **Fingeravtryck på text är blinda för bilder.** En omrendering tappade åtta fotografier medan varje textkontroll passerade. Titta på en renderad sida.
4. **`git checkout --` på en KATALOG raderar andras ocommittade arbete.** Hände i våg 2a och kostade två av Johans filer, som gick att återskapa av tur. Namnge alltid filer du själv ändrat; kopiera undan och återställ med `cp`.
5. **`git add -A` används aldrig.** Repot har alltid ett trettiotal ocommittade filer som tillhör Johan.
6. **`build-seo-meta.py` bumpar "Last updated"** ur git-commitdatum. En körning som bara skulle lägga till länkar sätter nytt datum på sidor vars innehåll inte rörts.
7. **Generatorer äger sina filer.** `build-og-images.py` skriver om de tolv delningskorten ur en mall; en handredigering där raderas tyst vid nästa körning. Lägg ändringen i generatorn.
8. **Sajten undervisar om design** och nämner typsnittsnamn i brödtext. Vakter måste matcha i `font-family`-kontext.
9. **`/usr/bin/python3` (3.9.6) är enda interpretern** med pytest, playwright och Pillow.

---

## Dokument

- Spec våg 1 och 2: `docs/superpowers/specs/2026-10-05-choosewise-visual-identity-design.md`
- Spec spår A: `docs/superpowers/specs/2026-10-07-choosewise-brand-mark-design.md`
- Plan spår A: `docs/superpowers/plans/2026-10-07-track-a-brand-mark.md`
- Plan våg 2a: `docs/superpowers/plans/2026-10-05-visual-identity-wave-2a-guides.md`
- Märkets bruksregler: `docs/brand-mark-usage.md`
- Beslutsloggar och PR-texter: `~/Desktop/choosewise-spar-a-forslag/`
- PDF:erna att titta på: `~/Desktop/choosewise-guider-vag2a/` (kopior — kan vara inaktuella)
