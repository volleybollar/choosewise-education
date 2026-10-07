# Spår A — märket, faviconen och Skool-tillgångarna

**Datum:** 2026-10-07
**Status:** utkast för Johans granskning
**Bygger på:** `docs/superpowers/specs/2026-10-05-choosewise-visual-identity-design.md` (§"Spår A"), våg 1 mergad som `851c9f5`
**Nästa steg efter godkännande:** implementationsplan via writing-plans

---

## 1. Varför

choosewise.education har idag **varken logotyp eller favicon**. Sajten klarar sig på ett textordmärke, men två saker gör att det inte räcker längre:

**Skool.** Communityn startar under namnet **Choosewise** med underrubriken **AI & EdTech for Educators**. Skool låter dig styra tre ytor — logotyp, favicon och omslagsbild 1400×790 — och inget annat. De tre bär hela den visuella igenkänningen mellan sajt och community.

**Flikraden.** En sida utan favicon visar webbläsarens tomma standardikon. Det är den vanligaste förekomsten av varumärket överhuvudtaget, och den är idag tom.

Gruppnamnet är ett medvetet avsteg från augustiresearchen, som rekommenderade "WISE Educators — AI & EdTech Decisions" för att Skools interna sök är ordbaserad. Johans skäl: medlemmarna kommer från LinkedIn och Facebook-grupper, inte från sök inne i Skool, och educators håller inte till på Skool av sig själva. Varumärket väger då tyngre än sökbarheten, och de sökbara orden tas tillbaka i underrubriken.

## 2. Vad märket är

**Nålen genom ringen.** En kompassnål som är längre än sitt instrument och bryter cirkeln.

Formen valdes bland sex kandidater efter mätning i rätt storlek, inte efter tycke. Avgörande:

- Den behåller sin karaktär i **båda** pixelfallen — äkta 16 px och 32 px.
- Den har ingen formkollision. Alternativet "avvikelsen" (nål som pekar vid sidan av ett norrmärke) var den rikaste idén men läser sig som **Safaris egen ikon** vid 32 px, vilket är en olycklig krock för ett tecken vars vanligaste hemvist är en webbläsarflik. Kompassrosen med fyra uddar är AI-produkternas generera-symbol; med åtta uddar och grundare insvängning överlevde den små storlekar, men förblev en stjärna.
- Den säger något som går att uppfatta på en halv sekund: **omdömet ryms inte i instrumentet.** Det är samma påstående som "är det fler verktyg eller bättre omdöme som behövs?".

WISE-cirkeln är inte med. Johans beslut 2026-10-07: cirkeln förblir ett diagram inne på sajten, inte ett varumärkestecken. Fyra bokstavsnoder på en ring är oläsbara i de storlekar ett märke måste klara.

### Geometri

Allt ritas i en **64×64-ruta**. Måtten är bindande — det är de som gjorde formen läsbar.

| Element | Värde |
|---|---|
| Ring | cirkel, centrum 32,32, radie **21**, linjebredd **2,5**, ingen fyllning |
| Nål, norr | triangel `M32 6 L37.5 32 L26.5 32 Z` |
| Nål, söder | triangel `M32 58 L37.5 32 L26.5 32 Z` |
| Nålsöga | cirkel, centrum 32,32, radie **2,6**, fylld med **bottnens färg** |

Nålspetsarna ligger 26 enheter från mitten. Skools runda beskärning tar 32, så marginalen är sex enheter. I det första utkastet låg spetsarna på 29 och snuddade kanten.

Nålsögat är ett **hål i nålen**, inte en prick ovanpå. Det ska alltid ha samma färg som ytan märket ligger på.

### De två färglägena

Märket finns i exakt två skick. Inga fler.

| | Mot mörkt (`#0B3A6F` eller mörkare) | Mot ljust (`#FBFAF8`, `#EFF2F6`) |
|---|---|---|
| Ring | `#FBFAF8` | `#0B3A6F` |
| Nål, norr | `#E8C9A8` | `#C2793A` |
| Nål, söder | `#FBFAF8` | `#0B3A6F` |
| Nålsöga | `#0B3A6F` | `#FBFAF8` |

Kopparn mot blått är `#E8C9A8` och inte `#C2793A`. `#C2793A` når bara **3,0:1** mot `#0B3A6F` och slocknar i små storlekar. Det är samma regel som gäller kopparfärgad text, av samma skäl: `--color-highlight` är ytfärg på ljus botten, `--color-highlight-on-dark` är det som syns mot mörkt.

### Regler för bruk

- **Minsta storlek:** 16 px. Under det används inte märket alls.
- **Frizon:** en nålbredd — 11 enheter i 64-rutan, alltså 17 % av märkets bredd — runt om.
- **Aldrig:** omfärgat utanför de två skicken, roterat, lutat, med skugga eller kontur, ihoptryckt, eller satt mot en botten som varken är papper eller varumärkesblå.
- **Sajtens header rörs inte.** Ordmärket står kvar som ren text. Johans beslut: headern är redan avvägd, och ett märke där är ett eget beslut som går att ta när tecknet setts i bruk.

## 3. Ytor och leverabler

Allt härleds ur **en** källa. Det är inte en stilfråga — det är villkoret för att märket ska se likadant ut överallt, och det ska gå att bevisa med ett test.

### Källfiler

| Fil | Innehåll |
|---|---|
| `assets/images/brand/mark-on-dark.svg` | märket i mörkt läge, 64×64, transparent botten |
| `assets/images/brand/mark-on-light.svg` | märket i ljust läge, 64×64, transparent botten |

### Favicon

| Fil | Storlek | Varför |
|---|---|---|
| `favicon.svg` | vektor | moderna webbläsare; skarp i alla storlekar |
| `favicon.ico` | 16 + 32 | äldre webbläsare, som inte läser SVG-favicon |
| `apple-touch-icon.png` | 180×180 | hemskärm på iPhone och iPad |

Alla tre är **märket på varumärkesblå botten** med hörnradie 22 %, inte märket fritt. En transparent favicon försvinner mot mörkt flikgränssnitt.

### Skool

| Fil | Storlek |
|---|---|
| `assets/images/brand/skool/logo.png` | 1024×1024, blå botten |
| `assets/images/brand/skool/cover.png` (+ `.svg`) | 1400×790 |

Omslaget: mörk blå botten, märket uppe till vänster, **Choosewise** i Hanken Grotesk 300, underrubriken **AI & EdTech for Educators** i vikt 400 och `#E8C9A8`, samt kopparbandet nederst — samma band som sajtens footer, vilket är det som binder ytorna ihop.

### LinkedIn

| Fil | Storlek |
|---|---|
| `assets/images/brand/linkedin/page-logo.png` | 300×300 |
| `assets/images/brand/linkedin/page-banner.png` | 1128×191 |
| `assets/images/brand/linkedin/personal-banner.png` | 1584×396 |

Båda bannermåtten levereras eftersom det inte är avgjort om Choosewise ska ha en egen LinkedIn-sida eller leva på Johans profil. Den personliga bannern håller vänstra tredjedelen fri från text där LinkedIn lägger profilbilden.

### og-korten

De 12 befintliga delningskorten i `assets/images/brand/og/` får märket uppe till vänster. Korten har **mörk botten** — en övertoning från `#07284D` till `#0B3A6F` — så märket tar sitt **mörka** skick. SVG:erna uppdateras och PNG:erna renderas om med `scripts/render-og-pngs.py`, som redan finns sedan våg 1 och startar en lokal server så att de självhostade typsnitten laddas.

### Guidernas omslag

Omslagets utformning **bestäms här** och **tillämpas i våg 2a**. Märket sitter uppe till vänster och litet: på ett guidomslag är titeln avsändaren och märket bara signaturen. Sex guider har mörkt omslag, resten ljust; båda skicken är definierade ovan.

Uppdelningen är avsiktlig. Våg 2a rör varenda tryckmall ändå, och att låta spår A öppna samma filer skulle betyda att två grenar skriver i samma rader.

## 4. Hur faviconen når 198 sidor

`scripts/build-seo-meta.py` injicerar redan ett block i varje sidas `<head>` mellan `<!-- seo:start -->` och `<!-- seo:end -->`, och täcker 198 av repots 203 publicerade HTML-filer: 203 spårade HTML-filer, minus `scripts/test-course.html` (en verktygsfixtur, inte en sida), minus de fyra partialerna utan `<head>` = 198. Räkna inte om det på nytt — det är den uträkningen, varje gång.

Det betyder **ett skript att ändra, inte 198 filer**, och att en ny sida får faviconen automatiskt nästa gång skriptet körs.

De fyra filerna utan `<head>` är partialer som inkluderas i andra sidor. De ska inte ha favicon och ska inte räknas som misslyckanden.

**En fälla i skriptet:** `build_seo_block` returnerar tidigt för sökvägarna i `HIDDEN_PATHS` och skickar då bara en `noindex`-tagg — ingen canonical, ingen JSON-LD. Läggs faviconlänkarna i den vanliga grenen får de dolda guidsidorna ingen favicon. Länkarna ska därför byggas **före** den tidiga returen och ingå i båda grenarna.

## 5. Vakter

Utan tester kan nästa ändring tyst införa en andra teckning av märket. Fyra vakter:

1. **En enda källa.** Varje SVG som bär märket innehåller exakt de banor som står i §2. Ett test jämför banddata mot källfilerna och blir rött om någon ritat om nålen på en enskild yta.
2. **Paletten.** Mark-filerna och de genererade tillgångarna innehåller bara de fyra värden som anges i §2 — `#FBFAF8`, `#0B3A6F`, `#E8C9A8`, `#C2793A`. Inga Crestiora-värden, ingen gammal grön.
3. **Faviconen når varje sida.** Varje publicerad HTML-fil med `<head>` innehåller de tre faviconlänkarna. Testet räknar 198 (se §4) och blir rött om injektionen missar en fil.
4. **Filerna finns och har rätt mått.** `favicon.ico` innehåller 16 och 32, `apple-touch-icon.png` är 180×180, Skool-omslaget är exakt 1400×790.

Varje vakt ska prövas mot sitt eget felfall innan den godkänns — i våg 1 visade sig fyra tester inte kunna bli röda på det de påstod sig vakta.

## 6. Definition av klart

1. Märket finns som två källfiler och varje annan tillgång är härledd ur dem, bevisat av vakt 1.
2. `favicon.svg`, `favicon.ico` och `apple-touch-icon.png` ligger i repots rot och visas i flikraden på en lokalt serverad sida.
3. Faviconen syns på alla 198 sidor med `<head>`, i både EN och SV.
4. Skool-loggan och omslaget 1400×790 finns som PNG, och omslaget är granskat i Skools egen beskärning.
5. LinkedIn-tillgångarna finns i alla tre måtten.
6. De 12 og-korten har märket, och **PNG:erna är omrenderade**, inte bara SVG:erna.
7. Guidomslagets utformning är dokumenterad så att våg 2a kan tillämpa den utan nya beslut.
8. Testsviten är grön, de fyra nya vakterna inräknade, och var och en har prövats mot sitt felfall.
9. PR mergad och Pages-bygget verifierat skarpt, med faviconen kontrollerad på den publicerade sajten.

## 7. Fällor

1. **`build-seo-meta.py` bumpar "Last updated"** ur git-commitdatum på varje sida den rör. En körning som bara lägger till faviconlänkar sätter nytt datum på 198 sidor. Kontrollera vad skriptet rör och återställ orelaterade sidor före push.
2. **Två og-skript, olika uppgifter.** `build-og-images.py` genererar SVG; `render-og-pngs.py` renderar SVG till PNG via en lokal server. og-taggarna pekar på PNG, så en ändring som bara rör SVG syns inte när någon delar en länk. Kör alltid båda, i den ordningen.
3. **Förhandsvisning körs alltid på ny port.** Safari cachar hårt, och favicon är det webbläsare cachar allra hårdast — en gammal ikon kan sitta kvar långt efter att filen bytts.
4. **`git add -A` används aldrig.** Repot har ett trettiotal ocommittade ändringar som hör till Johan.
5. **`/usr/bin/python3` är enda interpretern** med pytest och playwright. Homebrews 3.14 saknar båda.
6. **Kopparns tre roller blandas aldrig.** Regeln bröts fem gånger i våg 1 av olika arbetare som rimligt antog att ett värde räckte.

## 8. Vad som inte ingår

- **Sajtens header.** Ordmärket står kvar som ren text.
- **Våg 2a:s tryckmallar.** Guidomslagets utformning bestäms här, tillämpas där.
- **Diagram- och social-exporterna** (WISE/RÄTT). Egen runda, Johans beslut 2026-10-06.
- **Skool-gruppens innehåll och struktur.** Det här är tillgångarna, inte lanseringen.

## 9. Öppna frågor

Ingen som blockerar. En som Johan får avgöra när han ser tecknet i bruk: om sajtens header ska få märket vid sidan av ordmärket. Specen säger nej idag.
