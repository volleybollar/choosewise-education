# Ny visuell identitet för choosewise.education

**Datum:** 2026-10-05
**Status:** Design godkänd av Johan. Implementationsplan ej skriven — nästa plan omfattar enbart våg 1.
**Omfattar:** grafiskt uttryck — färg, typografi, form. **Inte** innehåll, texter, URL:er eller sidstruktur.

---

## 1. Syfte

Johan bygger ett engelskspråkigt Skool-community under Choosewise-varumärket. Sajten och communityt ska kännas som samma avsändare. Dagens uttryck (grädde, skogsgrön, terrakotta, Fraunces + Work Sans) byts mot ett nytt som Johan valt fram mot två referenser: ElevenLabs lugna, ljusa minimalism och den blå/bronsa paletten på crestiorabooks.com/play.html.

Framgång mäts som: en besökare som kommer från Skool till sajten, eller tvärtom, ska inte behöva fundera på om det är samma avsändare — och sajten ska vara minst lika läsbar som idag på sina 235 textsidor.

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

Samma regel gäller åt andra hållet i våg 2: nio av dagens export-mallar kör redan Crestioras navy, mässing och Playfair. De ska bort.

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
| `--color-highlight-ink` | `#9C5A24` | koppar i **text** | 5,2:1 |
| `--color-dark-bg` | `#0B3A6F` | mörkt band | — |
| `--color-dark-text` | `#EFF2F6` | text på mörkt band | 10,1:1 |
| `--color-focus` | `#0B3A6F` | fokusring | — |

**Tre tillgänglighetsregler som följer av mätningen, och som inte får brytas:**

1. `--color-text-muted` är `#656F7B`, inte den ljusare nyans som visades i mockupen. Den ljusare låg på 2,9:1 och klarade inte AA för brödtext.
2. **Koppar har två tokens.** `--color-highlight` (`#C2793A`) används i ytor, linjer och grafik. All kopparfärgad **text** — etiketter, versalsatta rubriker — använder `--color-highlight-ink` (`#9C5A24`, 5,2:1). Den ljusare låg på 3,3:1.
3. **Kopparknappar har mörk text** (`--color-text` på `--color-highlight`, 5,1:1). Vit text på koppar ger 3,4:1 och är inte tillåtet.

Dessa tre är inte smakfrågor. Publiken är skolor, och tillgänglighet är en trovärdighetsfråga i den sektorn.

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

Båda typsnitten är variabla, under OFL och självhostas i `assets/fonts/` precis som Fraunces och Work Sans gör idag. Inga anrop till Google Fonts från den publicerade sajten — integritetskravet i dagens `fonts.css` gäller fortsatt.

## 6. Användningsregler

Utan dessa blir resultatet en omfärgad gammal sajt, inte en ny design.

1. **Färg förekommer på få ställen.** Blått: rubriker, länkar, primärknappar, mörka band. Koppar: etiketter, linjer, den enda knappen på mörk botten. Allt annat är bläck, papper och hårlinje.
2. **Höjd görs med hårlinjer, inte skuggor.** Kort får 1 px ram, inte skugga.
3. **Serifen finns på exakt ett ställe:** citat och WISE-definitioner. Den är förbjuden i rubriker, kort, navigation och knappar. Bryts regeln tappar den sin verkan.
4. **Display är ljus och tajt, brödtext är normal och öppen.** Ingen fet display.

## 7. Innehållsbärande färg: WISE

WISE-diagrammets färgsättning är inte dekor. Sajten säger uttryckligen: *"Notice that the third step is coloured differently. That's deliberate."* W, I och E är reflekterande steg; S är beslutsögonblicket.

Semantiken överlever bytet: **W/I/E blir blå (`--color-accent`), S blir koppar (`--color-highlight`).** Gäller `assets/images/brand/wise-framework.svg`, hero-animationen på startsidan och WISE-sidan i båda språkversioner.

## 8. Omfattning

### Rörs inte

Innehåll, texter, URL:er, sidstruktur, navigation, de ~100 Visual Codes-bilderna, de tre videorna på "AI or human?", och de JSON-datafiler som promptbiblioteket genereras ur.

### Våg 1 — sajten och promptbiblioteket

| Steg | Omfattning | Verifiering |
|---|---|---|
| `tokens.css`, `fonts.css` | 2 filer; nya typsnitt självhostade | Sajten laddar utan nätverksanrop till fonts.googleapis.com |
| `components.css` | 127 hårdkodade färger (slate/blå/violett/bärnsten) tokeniseras | `grep -oE '#[0-9a-fA-F]{3,8}' assets/css/` ger träffar enbart i `tokens.css` |
| 33 sidor med egen `<style>` | genomgång en och en | Före/efter-skärmbild per sida i 3 bredder |
| ~150 genererade sidor | körs om med befintliga skript | `git diff` visar enbart färg- och typsnittsändringar |
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

Det blir en rak ersättning, inte ett nytt tema vid sidan av det gamla. Skälet: dubbla teman betyder dubbel underhållsbörda på en sajt Johan ska kunna ändra själv, och alla 235 sidor skulle behöva fungera i båda lägena. Den nya stilen blir default i samma stund som PR:en mergas.

## 12. Öppna frågor

Inga kvar. Frågan om de opublicerade guiderna är besvarad: samtliga fem guider ingår i våg 2, eftersom alla ska finnas som nedladdningar i Skool-communityt (se §8, våg 2).
