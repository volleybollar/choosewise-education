# Ny visuell identitet för choosewise.education

**Datum:** 2026-10-05
**Status:** Design godkänd av Johan. Implementationsplan ej skriven — nästa plan omfattar enbart våg 1.
**Omfattar:** grafiskt uttryck — färg, typografi, form. **Inte** innehåll, texter, URL:er eller sidstruktur.

---

## 1. Syfte

Johan bygger ett engelskspråkigt Skool-community under Choosewise-varumärket. Sajten och communityt ska kännas som samma avsändare. Dagens uttryck (grädde, skogsgrön, terrakotta, Fraunces + Work Sans) byts mot ett nytt som Johan valt fram mot två referenser: ElevenLabs lugna, ljusa minimalism och den blå/bronsa paletten på crestiorabooks.com/play.html.

Framgång mäts som: en besökare som kommer från Skool till sajten, eller tvärtom, ska inte behöva fundera på om det är samma avsändare — och sajten ska vara minst lika läsbar som idag på sina 189 publicerade sidor.

## 2. Fattade beslut

Alla fattade av Johan 2026-10-05 efter visuell genomgång.

| Beslut | Val | Avfärdat |
|---|---|---|
| Grundläge | Ljus bas med mörka helbreddsband | Helmörk sajt; ljus/mörk växlare |
| Palett | "Blueprint" — blått som varumärke, koppar som enda varma ton | "Paper & Ink" (nästan svartvit); "Atelier" (varm petrol) |
| Avstånd till Crestiora | Egen blå + egen koppar, eget typsnittspar | Återanvända Crestioras navy/mässing |
| Typsnitt | Hanken Grotesk 300/400/500 | Geist; Manrope + Inter |
| Serif | Instrument Serif, enbart i citat och WISE-definitioner | Ingen serif alls |
| Radavstånd rubriker | 1.16 som grundvärde, alla språk | 1.07 (för tajt för å/ä/ö) |
| PDF-omfång våg 1 | De 124 prompt-PDF:erna | Alla 151 på en gång; inga alls |
| Märke/favicon/Skool | Eget spår **efter** att färg och typografi är satta | Samtidigt med våg 1 |
| Guideinnehåll | Uppdateras i våg 2, i eget steg efter mallbytet | Samtidigt med mallbytet |

## 3. Hård begränsning: avstånd till Crestiora

Crestiora Books är anonymt. Johans namn får aldrig kopplas dit, och choosewise.education är hans synliga avsändare. Crestiora kör navy `#1B2733`, mässing `#C8A86B`, grädde `#F6F3EE`, Playfair Display + Inter.

**Inget av de värdena, och inget av de typsnitten, får användas på choosewise.education.** Paletten nedan är medvetet konstruerad för att ligga i samma temperatur utan att dela ett enda värde: mättad kobolt i stället för avmättad skiffer, koppar (rödare, mörkare) i stället för mässing (gulare, ljusare), humanistisk grotesk i stället för hög-kontrastserif.

**Kopplingen finns redan, och den är publicerad.** Verifierat 2026-10-05:

| Fil | Förekomster |
|---|---|
| `guides/claude/index.html` | 34 — i inbäddade SVG-diagram, med `font-family="Playfair Display, serif"` |
| `sv/guider/claude/index.html` | 34 — samma |
| `guides/claude/styles.css` | `#1B2733`, `#C8A86B`, `#F6F3EE`, `#2E4057` |
| `sv/guider/claude/styles.css` | samma |
| `sv/blog/posts/tva-grona-rutor-av-sextio.html` | `#1B2733`, `#F6F3EE` |

Claude-guiden nås från huvudmenyn. Det är alltså inte en bortglömd fil utan en av sajtens mest framskjutna sidor — satt i Crestioras exakta palett och display-typsnitt, på en sajt där Johan är namngiven avsändare. **Städningen av dessa fem filer är obligatorisk i våg 1, inte valfri.**

Samma regel gäller i våg 2: nio av dagens export-mallar kör också Crestioras navy, mässing och Playfair. De ska bort.

## 4. Färgtokens

Ersätter blocket `/* ───── Colors ───── */` i `assets/css/tokens.css`.

| Token | Värde | Roll | Kontrast mot papper |
|---|---|---|---|
| `--color-bg` | `#FBFAF8` | papper, grundyta | — |
| `--color-bg-alt` | `#EFF2F6` | svalt sektionsband | — |
| `--color-text` | `#0C1A2E` | bläck, blåsvart | 16,7:1 |
| `--color-text-soft` | `#4E5A68` | brödtext | 6,7:1 |
| `--color-text-muted` | `#656F7B` | metadata, bildtext | 4,9:1 |
| `--color-border` | `#DDE3EA` | hårlinje | — |
| `--color-border-strong` | `#C3CFDC` | ram på ghost-knapp | — |
| `--color-accent` | `#0B3A6F` | rubriker, länkar, primärknapp, band | 10,9:1 |
| `--color-accent-hover` | `#082C55` | hover | — |
| `--color-deep` | `#07284D` | footer och hero, ett steg djupare än bandet | — |
| `--color-highlight` | `#C2793A` | koppar i **ytor och grafik** | — |
| `--color-highlight-ink` | `#9C5A24` | koppar i **text på ljus yta** | 5,2:1 |
| `--color-highlight-on-dark` | `#E8C9A8` | koppar i **text på mörkt band** | 7,2:1 mot bandet |
| `--color-dark-bg` | `#0B3A6F` | mörkt band | — |
| `--color-dark-text` | `#EFF2F6` | text på mörkt band | 10,1:1 |
| `--color-focus` | `#0B3A6F` | fokusring på papper | 10,9:1 |
| `--color-focus-on-dark` | `#E8C9A8` | fokusring på mörkt band | 7,4:1 mot bandet |

**Fem tillgänglighetsregler som följer av mätningen, och som inte får brytas:**

1. `--color-text-muted` är `#656F7B`, inte den ljusare nyans som visades i mockupen. Den ljusare låg på 2,9:1 och klarade inte AA för brödtext.
2. **Koppar har tre tokens, och rollerna får aldrig blandas.** `--color-highlight` (`#C2793A`) används i ytor, linjer och grafik — **aldrig i text**. Kopparfärgad text på ljus yta tar `--color-highlight-ink` (`#9C5A24`, 5,2:1 mot papper, 4,8:1 mot sektionsbandet). Kopparfärgad text på mörkt band tar `--color-highlight-on-dark` (`#E8C9A8`, 7,2:1). `--color-highlight` som textfärg faller på **varje** yta sajten har: 3,3:1 mot papper, 3,1:1 mot sektionsbandet, 3,3:1 mot det mörka bandet, 4,3:1 mot footern. Mätt 2026-10-05.
3. **Kopparknappar har mörk text** (`--color-text` på `--color-highlight`, 5,1:1). Vit text på koppar ger 3,4:1 och är inte tillåtet.
4. **Fokusringen har två värden.** `--color-focus` är samma blå som det mörka bandet, så en ring i den färgen blir osynlig mot bandet och tangentbordsnavigering slutar synas i CTA-sektionerna. Mot mörk botten används `--color-focus-on-dark` (`#E8C9A8`, ljus koppar).

5. **`--color-accent` och `--color-dark-bg` har samma värde (`#0B3A6F`) men olika roller.** Det är avsiktligt — bandet ÄR varumärkesfärgen — men det är också en fälla: en bokstavlig mappning av en mörk källfärg till `--color-accent` på en yta som redan är `--color-dark-bg` ger 1,00:1, alltså osynlig text. Fällan har slagit till två gånger under våg 1 (fokusringen, och WISE-bokstäverna i hero). **På mörk botten gäller: text tar `--color-dark-text`, kopparaccent tar `--color-highlight-on-dark`, fokus tar `--color-focus-on-dark`.** `--color-accent` används aldrig som förgrund mot ett mörkt band.

Dessa fem är inte smakfrågor. Publiken är skolor, och tillgänglighet är en trovärdighetsfråga i den sektorn.

### Skuggor

ElevenLabs-riktningen lyfter ingenting. `--shadow-md` och `--shadow-lg` skalas ned till nära platta; höjd markeras med 1 px hårlinje i stället. `--shadow-focus` byts till `0 0 0 3px rgba(11,58,111,0.28)`.

### Radie

Knappar och taggar `999px` (piller). Kort `16px`. Inputs `4px`. Nuvarande `--radius-*`-tokens behålls som namn, värdena justeras.

## 5. Typografitokens

| Token | Värde |
|---|---|
| `--font-display` | `'Hanken Grotesk', -apple-system, 'Helvetica Neue', sans-serif` |
| `--font-body` | samma som display |
| `--font-quote` | `'Instrument Serif', Georgia, serif` — **ny** |
| `--font-mono` | oförändrad |

- **Vikter:** display 300, h2/h3 400, brödtext 400, knappar och betoning 500. Display sätts aldrig i fet vikt — det är hela riktningens poäng.
- **Teckenavstånd:** display −0.032em, h2 −0.02em, brödtext 0, versalsatta etiketter +0.15em.
- **Radavstånd:** `--lh-tight` ändras från 1.1 till **1.16**. Gäller alla språk. Skälet är att Å, Ä och Ö i låg vikt kommer för nära raden ovanför vid tajtare värde; ett enda värde för båda språken är mindre bräckligt än ett svenskt undantag som glöms bort.
- Den flytande `clamp()`-skalan behålls oförändrad. Det är vikten som ändras, inte storlekarna.

Båda typsnitten är under OFL och självhostas i `assets/fonts/` precis som Fraunces och Work Sans gör idag. Inga anrop till Google Fonts från den publicerade sajten — integritetskravet i dagens `fonts.css` gäller fortsatt.

**Kravet är redan brutet idag.** Fyra publicerade sidor hämtar typsnitt direkt från `fonts.googleapis.com`: `guides/claude/index.html`, `sv/guider/claude/index.html`, `wise-framework.html` och `ratt-modellen.html`. Det innebär att besökarnas IP-adresser i praktiken delas med Google på just de sidorna, trots att resten av sajten självhostar för att undvika det. De fyra anropen tas bort i våg 1.

**Filformaten skiljer sig** (verifierat mot Google Fonts 2026-10-05):

- **Hanken Grotesk** är variabel, `font-weight: 300 600` i en enda fil. Täcker alla tre vikter vi använder.
- **Instrument Serif** är **inte** variabel. Den finns bara i vikt 400, som två statiska filer — rak och kursiv. Båda behövs; citaten sätts i kursiv.

Latin-subsetet räcker för svenska (å, ä, ö ligger i U+0000–00FF), men latin-ext laddas också för säkerhets skull.

## 6. Användningsregler

Utan dessa blir resultatet en omfärgad gammal sajt, inte en ny design.

1. **Färg förekommer på få ställen.** Blått: rubriker, länkar, primärknappar, mörka band. Koppar: etiketter, linjer, den enda knappen på mörk botten. Allt annat är bläck, papper och hårlinje.
2. **Höjd görs med hårlinjer, inte skuggor.** Kort får 1 px ram, inte skugga.
3. **Serifen finns på exakt ett ställe:** citat och WISE-definitioner. Den är förbjuden i rubriker, kort, navigation och knappar. Bryts regeln tappar den sin verkan.
4. **Display är ljus och tajt, brödtext är normal och öppen.** Ingen fet display.

## 7. Innehållsbärande färg: WISE

WISE-diagrammets färgsättning är inte dekor. Sajten säger uttryckligen: *"Notice that the third step is coloured differently. That's deliberate."* W, I och E är reflekterande steg; S är beslutsögonblicket.

Semantiken överlever bytet: **W/I/E blir blå, S blir koppar.** Men diagrammet är ritat som konturcirklar med en bokstav inuti, och de två delarna tar olika token:

| Del | Token | Varför |
|---|---|---|
| Cirkelns kontur, W/I/E | `--color-accent` | grafik |
| Bokstaven, W/I/E | `--color-accent` | text, 10,9:1 mot papper |
| Cirkelns kontur, beslutssteget | `--color-highlight` | grafik — ytkoppar är tillåten här |
| Bokstaven, beslutssteget | `--color-highlight-ink` | **text**, 5,2:1. Ytkoppar ger 3,3:1 och är förbjuden som text |

Att låta bokstaven ärva konturens token är den uppenbara genvägen och den faller på kontrast. Gäller `assets/images/brand/wise-framework.svg`, hero-animationen på startsidan och WISE-sidan i båda språkversioner.

## 8. Omfattning

### Rörs inte

Innehåll, texter, URL:er, sidstruktur, navigation, de ~100 Visual Codes-bilderna, de tre videorna på "AI or human?", och de JSON-datafiler som promptbiblioteket genereras ur.

### Våg 1 — sajten och promptbiblioteket

| Steg | Omfattning | Verifiering |
|---|---|---|
| `tokens.css`, `fonts.css` | 2 filer; nya typsnitt självhostade | Sajten laddar utan nätverksanrop till fonts.googleapis.com |
| `components.css` | 127 hårdkodade färger (slate/blå/violett/bärnsten) tokeniseras | `grep -oE '#[0-9a-fA-F]{3,8}' assets/css/` ger träffar enbart i `tokens.css` |
| 5 sidor med egen `<style>` | `wise-framework.html`, `ratt-modellen.html` (båda föräldralösa — se §9.7), `sv/blog/posts/tva-grona-rutor-av-sextio.html`, `presentation-skills/module-6/deep-dive/`, `sv/presentationsteknik/modul-6/fordjupning/` | Före/efter-skärmbild per sida i 3 bredder |
| 3 sidlokala CSS-filer | `guides/claude/styles.css`, `sv/guider/claude/styles.css` (Crestioras palett — se §3), `visual-codes/visual-codes.css` | Inga Crestiora-värden kvar; sidorna renderar oförändrat i layout |
| Claude-guidens inbäddade SVG | 34 förekomster per språkversion i `guides/claude/index.html` och `sv/guider/claude/index.html` | `grep` på Crestiora-värden ger noll träffar i publicerade filer |
| ~150 genererade sidor | **inget arbete** — de bär noll färgvärden och ärver allt från delad CSS (verifierat 2026-10-05) | Stickprov: `grep` på färg/typsnitt i en genererad promptsida ger noll träffar |
| 27 SVG:er + hero-animationen | handarbete | Okulär kontroll i EN och SV |
| 12 og-kort | SVG uppdateras, **PNG-renderingen skriptas** i stället för att göras för hand | Delningsförhandsvisning testad skarpt efter publicering |
| 124 prompt-PDF:er | `exports/prompts/_prompt-print.css` + `build-prompts-pdf.py` | 5 stickprov: omslag, sidbrytningar och sidnummer intakta |

Prompt-PDF:erna är billiga just för att hela serien har **en** delad stilmall och en idempotent batch på ~50 sekunder. Det är därför de ligger i våg 1.

### Spår A — märke, favicon, Skool-tillgångar

Startar **efter** att våg 1:s färg och typografi är satta.

Sajten har idag varken logotyp eller favicon — bara ordmärket satt i text. Det fungerar på webben men inte i Skool, som kräver logotyp, favicon och omslagsbild i 1400×790. Just de tre ytorna är de enda Skool låter oss styra, så de bär hela igenkänningen mellan sajt och community.

Leverans: ett enkelt märke byggt på WISE-cirkeln som redan finns, i blått och koppar, som ger favicon, Skool-logga och omslagsbild ur samma källa.

### Våg 2 — guiderna

Eget jobb efter våg 1 och spår A. **Två steg, inte ett.**

**Syftet med guiderna styr ambitionsnivån:** de ska ligga som nedladdningar i Skool-communityt. Claude-guiden finns dessutom publicerad på sajten. Det betyder att guide-PDF:erna är medlemsvärde, inte bara marknadsföringsmaterial — de läses av någon som betalat eller registrerat sig, och de är ett av få ställen där sajtens och communityts formspråk möts i samma dokument. Därför ingår samtliga guider, publicerade som opublicerade, och därför är innehållets aktualitet (steg 2b) en del av leveransen och inte en senare ambition.

**2a — gemensam mall, innehållet orört.** De 23 fristående print-mallarna i `exports/` bär idag var sin inbakad palett, cirka 1 000 hårdkodade färgvärden totalt, varav nio filer kör Crestioras navy/mässing/Playfair. De bryts ut till en delad `_guide-print.css` efter samma mönster som `_prompt-print.css`. Guide-PDF:erna renderas om.
*Verifiering: den extraherade texten ur varje PDF är identisk före och efter. Bara färg och typsnitt skiljer.*

**2b — innehållet uppdateras.** Claude-guiden (publicerad, EN + SV) plus de fyra opublicerade: Gemini/NotebookLM, Copilot, Apple Intelligence, AI för elever — samtliga i två språk. 10 guidesidor, 18 PDF:er. Guiderna skrevs i april 2026 och modellerna har förändrats sedan dess; varje faktapåstående ska kontrolleras mot verkligheten i båda språken.
*Verifiering: varje uppdaterat påstående har en kontrollerad källa. Svensk text läses mot kvalitetsribban i CLAUDE.md §3.*

Skälet till uppdelningen: om en PDF går sönder ska det gå att se om det var mallen eller texten. Stegen kan följa direkt på varandra — uppdelningen kostar ingen väntetid, bara en extra commit.

**Visual Codes Vol. 1–3** (`~/Projekt/Choosewise/visual-codes-pdf/`, utanför repot) har en tredje kopia av paletten och ingår i våg 2. Utan dem står tre PDF:er kvar i grönt och terrakotta medan allt annat bytt.

## 9. Fällor som ska byggas in i planen

Alla är dokumenterade i tidigare sessioner och har kostat tid förut.

1. **`build-seo-meta.py` bumpar "Last updated"** ur git-commitdatum. En sajtbred omstylingscommit sätter nytt datum på varje sida, även de vars innehåll inte rörts. Kontrollera vad skriptet rör och återställ orelaterade sidor före push.
2. **Cachen ljuger.** `include.js` hämtar `header-*.html` separat, och Safari cachar srcset hårt. Förhandsvisning körs alltid på **ny port**.
3. **`git add -A` används aldrig.** Repot har ett trettiotal ocommittade ändringar som inte hör till det här arbetet, och `docs/` samt `.superpowers/` är gitignorerade. Filer väljs medvetet vid varje commit.
4. **og-bildernas PNG-steg är manuellt idag.** Det är den punkt som mest sannolikt glöms bort, eftersom felet syns först när någon delar en länk. Skriptas i våg 1.
5. **`p, li { max-width: 40rem }`** i `base.css` slår mot sidor med egen layout. Sidlokal CSS är accepterad på den här sajten — ändra inte den globala regeln.
6. **Arbetsflöde:** feature-branch och PR med merge-commit, inte squash.
7. **Två föräldralösa filer i repots rot.** `wise-framework.html` och `ratt-modellen.html` saknas i `sitemap.xml` och länkas inte från någon sida — de är kvar sedan innan `/wise/` och `/sv/ratt/` fanns. GitHub Pages serverar dem ändå. De stylas om tillsammans med resten (de är publikt nåbara och ska inte stå kvar i gammal palett), men **de raderas inte** i det här arbetet. Att avgöra om de ska bort är ett eget beslut för Johan.

## 10. Definition av klart — våg 1

1. `grep` hittar inga hårdkodade färger utanför `tokens.css` i `assets/css/`.
2. Alla sidor i de 12 og-korten har omrenderade PNG:er, och skriptet som gör det ligger i `scripts/`.
3. Före/efter-skärmbilder finns för 12 representativa sidor i 3 bredder, i båda språkversioner.
4. Kontrastmätning av de färgpar som används i text ger minst 4,5:1.
5. Fem prompt-PDF:er stickprovade: omslag, sidbrytningar, sidnummer och svenska tecken intakta.
6. Sajten laddar utan externa typsnittsanrop.
7. Inget av Crestioras värden (`#1B2733`, `#C8A86B`, `#F6F3EE`, Playfair Display) förekommer i publicerade filer.
8. PR mergad till `main`, GitHub Pages-bygget verifierat skarpt.

## 11. Ingen temaväxlare

Det blir en rak ersättning, inte ett nytt tema vid sidan av det gamla. Skälet: dubbla teman betyder dubbel underhållsbörda på en sajt Johan ska kunna ändra själv, och alla 189 sidor skulle behöva fungera i båda lägena. Den nya stilen blir default i samma stund som PR:en mergas.

## 12. Öppna frågor

Inga kvar. Frågan om de opublicerade guiderna är besvarad: samtliga fem guider ingår i våg 2, eftersom alla ska finnas som nedladdningar i Skool-communityt (se §8, våg 2).
