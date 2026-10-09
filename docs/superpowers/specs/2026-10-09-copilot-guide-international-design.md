# Copilot-guiden: aktuell, och riktad mot en engelskspråkig skolvärld

**Status:** godkänd design 2026-10-09. Nästa steg är en implementationsplan.
**Gäller:** den första av de fyra återstående guiderna. Copilot är pilot; de tre
andra tas i egna rundor med den här som mall.

---

## 1. Vad som ska levereras, och vad som inte ska det

**Leveransen är två PDF:er på engelska**, avsedda för Skool-communityt:

- `_unpublished/assets/pdfs/guides/copilot-guide-en.pdf`
- `_unpublished/assets/pdfs/guides/copilot-quick-start-en.pdf`

**Ingenting publiceras på choosewise.education i den här rundan.** Guiden stannar
i `_unpublished/`, som GitHub Pages inte serverar — verifierat 2026-10-09: alla
fyra utkastkataloger svarar 404. Hela publiceringskedjan är därför utanför
omfånget: inga poster i `guides-en.json`, ingen PAIR_MAP, ingen sitemap, inga
og-kort, och landningssidans *"in preparation"* står kvar som den är.

Johans beslut 2026-10-09, ordagrant: *"PDF:erna ska in i Skool-communityt, så de
ska inte publiceras någonstans nu."*

### Målgruppen är inte svensk

Johans korrigering samma dag: *"målgruppen i Skool-communityt blir den
engelskspråkiga delen av skolvärlden, inte specifikt Sverige."*

Det är en innehållsförutsättning, inte en språkfråga. Utkastet är svenskramat på
djupet och det styr hela del 3.

---

## 2. Utgångsläget, mätt och inte antaget

Utkastet är från **2026-06-28** — före Blueprint (5 okt), före tryckmallarnas
konvertering (7 okt) och före Claude-innehållets faktarunda (8 okt).

| Fråga | Svar |
|---|---|
| Är tryckmallen Blueprint? | **Ja.** Våg 2a konverterade alla 14 opublicerade mallar till `_guide-print.css`. Verifierat genom att rendera PDF-sidor och jämföra mot Claude-guiden: samma färger, samma rubrikskala, samma callout-ruta med kopparlinje, samma Instrument Serif i kursiv. |
| Har webbsidan rätt typografi? | **Nej.** Alla fyra utkast laddar **Playfair Display och Inter från Google Fonts** — Crestioras typsnitt. Den publicerade Claude-guiden laddar varken eller. |
| Ärver sidorna Blueprint-färgerna? | Ja, 91 `var(--color-*)` i `styles.css`. Det är typografin som sitter kvar, inte paletten. |
| Finns innehållsförteckning med hårdkodade sidnummer? | **Nej** — noll `toc-page-num`. Claude-guiden hade 18, varav 13 blev fel i våg 2b. Den fällan gäller inte här. |
| Är PDF:erna vaktade? | **Ja.** Alla fyra copilot-PDF:er ligger i både `guide-pdf-baseline.json` och `guide-pdf-body-baseline.json` (22 nycklar totalt). |
| Finns byggare? | Ja: `exports/build-copilot-pdf.py` och `exports/build-copilot-quickstart-pdf.py`. |
| Bilder i tryckmallen | 3 |
| Quick-startens storlek | 211 rader |

### Svenskramningen, inventerad

Mätt i webbutkastet: 15 × "Swedish", 4 × "Sweden", 4 × "Skolverket", 3 × "GDPR".
Det är inte ord att byta ut, det är resonemang att skriva om:

- En hel FAQ-post: *"Is Copilot available in Swedish?"* med fyra meningar om
  svensk språkkvalitet och utrullningsordning.
- Prompts som förutsätter svensk kontext: Skolverket-dokument som exempel,
  svensk-engelska lappar till vårdnadshavare, "student-accessible Swedish
  rewrite".
- Ett stycke om att *"Sweden in particular lacks a unified national AI-in-school
  guidance document as of April 2026"*, med Skolverket och IMY namngivna.
- Avslutningen: *"I offer consulting for schools, primarily in Sweden."*
- Hela del 3 byggd på GDPR, EU Data Boundary och Schrems II.

Omslaget bär dessutom två fel i klartext: *"A practical guide for **Swedish
schools**"* och datumstämpeln *"April 2026"*.

---

## 3. Vald väg: neutral kärna, en tydligt märkt regional del

Tre vägar vägdes. **Väg A valdes av Johan 2026-10-09.**

**A — neutral kärna plus en ärlig jurisdiktionsruta.** Sverige ut ur brödtexten.
Del 3 skrivs om till det som faktiskt är jurisdiktionsoberoende: vad Microsoft
**avtalsmässigt** utfäster i en skoltenant, vad Commercial Data Protection gör
och inte gör, och vilka inställningar en administratör styr. Därefter en kort
ruta som säger att var läsaren bor avgör resten.

**Rutans innehåll är bestämt, inte fritt:** den slår fast att skolan är
personuppgiftsansvarig och att Copilot inte ändrar det; att vilket regelverk som
gäller beror på jurisdiktion; och den namnger **tre kategorier läsaren ska
kontrollera lokalt** — dataskyddsregimen, reglerna om elevers ålder och samtycke,
och skolans egen upphandlings- och godkännandeväg. **Inga enskilda lagar eller
myndigheter namnges**, eftersom guiden då skulle påstå sig täcka jurisdiktioner
den inte verifierat. Det är gränsen mellan väg A och väg C.

**B — EU-ramad men skyltad.** Förkastad: Skool-publiken är bredast i USA, och då
står guidens tyngsta del som en varningsskylt för halva läsekretsen.

**C — full internationalisering** med FERPA, COPPA och brittisk DfE/ICO-vägledning.
Förkastad: tre nya källdomäner att verifiera mot rundans beviskrav. Våg 2b:s regel
är att en faktamening utan post i inventeringen inte får skrivas, och att hålla
den ribban för amerikansk och brittisk skoljuridik är ett eget projekt.

**Motiveringen för A**, som ska bäras genom hela rundan: varje påstående ska gå
att belägga med en källa Johan kan stå för — Microsofts egen dokumentation om vad
produkten gör och vad avtalet säger. En guide som säger *kontrollera det här hos
er* är mer användbar än en som gissar fel med auktoritet. A är dessutom billigast
att hålla aktuell, eftersom produktfakta åldras likadant för alla läsare.

---

## 4. Layout: formspråket räcker, omslaget rörs inte

Johans beslut 2026-10-09. Brödtext, rubriker, callout-rutor, färger och typografi
är redan identiska med Claude-guidens — verifierat genom rendering, inte genom
metadata. Copilot behåller sitt eget omslag (helt navy, tre piller
CHAT/WRITE/SUMMARISE) och sin egen sidfot (vänsterställd, med sidnummer).

**Två ändringar på omslaget, inga fler:** *"Swedish schools"* och *"April 2026"*.

Alternativen — att ge Copilot Claude-guidens fotoomslag, eller att bara harmonisera
sidfoten — valdes bort. Skälet är att varje guide rimligen får ha ett eget ansikte,
och att ett fotoomslag kostar en bild per guide.

---

## 5. Ytor

Tre filer rörs, alla engelska:

| Yta | Roll |
|---|---|
| `_unpublished/exports/copilot-print-a4-en.html` | källan till huvud-PDF:en — den egentliga leveransen |
| `_unpublished/exports/copilot-quick-start-en.html` | källan till quick-start-PDF:en, går också till Skool |
| `_unpublished/guides/copilot/index.html` | webbsidan, plus dess `styles.css` |

**Webbsidan ingår fast den inte publiceras.** Skälet är inte prydlighet: lämnas
den orörd divergerar den från print med varje faktarättning, och nästa gång någon
tar upp guiden för publicering är de två ytorna osynkade på exakt de meningar som
var känsligast. Det är precis den divergens våg 2b:s disciplin finns till för att
förhindra. Google Fonts-raden med Playfair och Inter tas bort i samma veva.

**De svenska ytorna rörs inte**, enligt Johans beslut 2026-10-08 att de fyra
återstående guiderna uppdateras bara på engelska. **Följden ska skrivas in som ett
känt läge, inte upptäckas senare:** `copilot-print-a4-sv.html`,
`copilot-quick-start-sv.html` och `_unpublished/sv/guider/copilot/` kommer att
divergera från de engelska i sak, och deras PDF:er står kvar med juni-fakta och
svensk inramning.

---

## 6. Inventeringen

**`docs/guide-facts-copilot.md`**, byggd på `docs/guide-facts-claude.md`:s form:
en post per volatilt påstående, med förekomster per yta, typ, omfång, **källa med
hämtdatum** och utfall. Plus vaktblocket.

Två regler ärvs från våg 2b och gäller utan undantag:

1. **En faktamening utan post i inventeringen får inte skrivas.**
2. **Ett fynd som inte behöver ändras stryks aldrig tyst** — det står kvar i
   tabellen med en motivering.

Vaktblockets semantik är den som gäller sedan 2026-10-09: `aktiv` kräver att
strängen står ordagrant på båda ytorna i språket, `borttaget` att den **inte**
står på någon av dem. Varje påstående rundan stryker eller rättar får en
`borttaget`-rad — den är det enda som hindrar att rättningen tas tillbaka.

**Särskilt misstänkta i den här guiden**, eftersom Microsoft bytt namn och
paketering flera gånger sedan juni: plannamn, licensnamn, funktionsnamn,
produkt-URL:er, och vad Commercial Data Protection heter och omfattar. Inget av
dem får stå kvar på utkastets ord.

---

## 7. Kodarbetet

`surfacecheck.SURFACES` och `factinventory.INVENTORY` är hårdkodade till Claude.
De ska bli guide-agnostiska så testet kan parametrisera över båda guiderna.

`factinventory.load()` tar redan en sökväg; bara standardvärdet är Claude.
`surfacecheck` behöver en uppsättning ytor per guide.

Allt med test först, och varje ny vakt bryts med flit och ses bli röd innan den
litas på. Det är rundans enda egentliga kodarbete.

### Känd begränsning, utskriven med avsikt

Ytkonsistensvakten jämför **webb mot print**, precis som för Claude.
**Quick-starten ingår inte** i den jämförelsen. Den är en tredje yta med egen,
avsiktligt kortare formulering, och att kräva att varje sträng står ordagrant på
alla tre vore fel krav — vakten vore röd från första dagen och därmed värdelös.

Quick-starten hanteras i stället på två sätt: inventeringen listar dess
förekomster, så rundan inte kan glömma den, och PDF-vakterna fångar oavsiktliga
ändringar i den.

---

## 8. Verifiering

1. **Faktakontroll mot namngiven källa**, hämtad och läst samma dag — inte
   sammanfattad. Samma källdisciplin som Claude-guidens inventering: rå HTML och
   lokal textextraktion där det går, aldrig en sammanfattning som källa till ett
   värde.
2. **Omriktningen enligt väg A**, inklusive avslutningens CTA.
3. **Bygg om de två engelska PDF:erna** och omfånga facit med
   `capture_guide_baseline.py --only` för exakt de två. `--force` är liktydigt med
   att slå av paritetsvakten för alla 22 och får inte användas.
4. **Titta på det renderade dokumentet.** Våg 2b granskade text sexton gånger och
   hittade tre fel först när någon öppnade PDF:en, varav en bild som motsade sin
   egen text. Tre bilder finns i mallen; varje bild intill ändrad text granskas.
5. **Hela sviten**, plus en genomläsning av PDF:en från pärm till pärm.

### Fällor som gäller den här rundan

- **Jämför insamlade test-id:n mot `main`** om någon parametrisering rörs.
  `str.replace` utan `count` tog bort tre vakter i stället för en 2026-10-09, och
  sviten förblev grön.
- **En vakt som inte setts bli röd vaktar ingenting.** Fyra gånger under
  2026-10-09 skrevs en vakt som inte kunde fallera på det den vaktade.
- **`/usr/bin/python3` är enda interpretern** med pytest, playwright och Pillow.
- **`git add -A` används aldrig.** Repot har ett trettiotal ocommittade filer som
  tillhör Johan.
- **Tio av 22 PDF:er är inte byte-identiska vid omrendering** — skillnaden är
  Chromiums `CreationDate`/`ModDate`. En omrendering visar alltid ändrade filer
  även när ingenting ändrats.

---

## 9. Vad som gör rundan klar

- Båda engelska PDF:erna byggda ur rättat innehåll, med Blueprint-layout.
- Inget "Sweden", "Swedish" eller "Skolverket" kvar i de engelska ytorna annat än
  där det är ett medvetet, motiverat exempel.
- Omslaget säger varken "Swedish schools" eller "April 2026".
- Varje volatilt påstående har en post i `docs/guide-facts-copilot.md` med källa
  och datum.
- Ytkonsistensvakten grön för både Claude och Copilot.
- PDF-facit omfångat med `--only`, de tjugo andra nycklarna orörda.
- Webbsidan rättad i sak och fri från Google Fonts.
- Det svenska divergensläget skrivet i överlämningen.
