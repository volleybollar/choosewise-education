# Gemini- och NotebookLM-guiden: aktuell, och riktad mot en engelskspråkig skolvärld

**Status:** godkänd design 2026-10-12. Nästa steg är en implementationsplan.
**Gäller:** den andra av de fyra guiderna. Copilot var pilot (PR #38, mergad
2026-10-11 som `26c661a`) och är mallen. Apple Intelligence och elevguiden tas
i egna rundor efter den här.

---

## 1. Vad som ska levereras, och vad som inte ska det

> **AMENDEMANG 2026-10-13, efter körningen.** Två värden i det här avsnittet är överspelade av
> ägarbeslut under rundan. Specen står i övrigt oförändrad som bindande auktoritet.
>
> | § 1 säger | levererat | beslut |
> |---|---|---|
> | `gemini-notebooklm-guide-en.pdf` / `gemini-notebooklm-quick-start-en.pdf` | **`gemini-notebook-guide-en.pdf`** / **`gemini-notebook-quick-start-en.pdf`** | **Johan, 2026-10-12** vid grinden efter Task 4: Google döpte om NotebookLM till Gemini Notebook 2026-07-16 (post G49), och namnbytet omfattar **allt, även filnamnen**. De **svenska** filnamnen behåller `gemini-notebooklm-*` med avsikt — deras innehåll säger fortfarande NotebookLM. |
> | huvudguiden **42 sidor** | **44 sidor** | **Controllern, Task 13:** rundans rättelser är längre än det de ersatte (licensstycket, den nya jurisdiktionsrutan, AI Act:s fyra datum, namnbytets fem tecken per förekomst över ~200). Strukturen verifierad frisk. Stoppvillkoret omformulerat till 41–44 sidor **och** ingen sida under 400 tecken utom omslaget. |
>
> Rulingarna i sin helhet stod i rundans ledger, som låg i den gitignorerade worktreen och inte
> överlevde leveransen. **Där de nu står: `docs/blueprint-handoff.md`**, avsnittet
> *"Gemini-guiden — vad rundan lämnar"*. Samma avsnitt bär de **fem** rättelser till den här
> specen som mätningen tvingade fram.

**Leveransen är två PDF:er på engelska**, avsedda för Skool-communityt:

- `_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-en.pdf` (42 sidor) — *se amendemanget: `gemini-notebook-guide-en.pdf`, 44 sidor*
- `_unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-en.pdf` (2 sidor) — *se amendemanget: `gemini-notebook-quick-start-en.pdf`*

**Ingenting publiceras på choosewise.education i den här rundan.** Samma frame
som Copilot: guiden stannar i `_unpublished/`, som Pages inte serverar. Inga
poster i `guides-en.json`, ingen PAIR_MAP, ingen sitemap, inga og-kort.

**De svenska ytorna rörs inte** och ska komma ut byte-identiska:
`_unpublished/exports/gemini-notebooklm-print-a4-sv.html`,
`gemini-notebooklm-quick-start-sv.html` och
`_unpublished/sv/guider/gemini-notebooklm/`. Följden — att engelskt och svenskt
divergerar i sak — är ett känt läge, inte en upptäckt.

---

## 2. Utgångsläget, mätt 2026-10-12 och inte antaget

Guiden är **inte** Copilot i liten skala. Den är nästan dubbelt så stor, dess
svenska inramning är nästan obefintlig, och dess juridik sitter i ett eget
skyltat kapitel i stället för invävd i brödtexten.

| | Copilot (förra rundan) | Gemini/NotebookLM |
|---|---|---|
| Printytan | 1 333 rader, 25 sidor | **1 636 rader, 42 sidor** |
| PDF-storlek | 6,5 MB | **9,6 MB** |
| Bilder i mallen | 3 | **8** |
| "Swedish" / "Sweden" | 15 / 4 | **2 / 3** |
| Skolverket, IMY, Schrems | 4 / 3 / 7 | **0 / 0 / 0** |
| GDPR | 3 | **11 på webbytan, 12 i print** |
| Hårdkodade sidnummer | 6 | **10** |
| Datumstämplar | 4 | **2** (plus nio daterade *produktpåståenden*) |
| Pris i fel valuta | 5 förekomster i SEK | **inga** |

**Tryckmallen är Blueprint** — den laddar `exports/_guide-print.css`, precis som
Copilots. Våg 2a konverterade även den här.

**Webbsidan laddar Crestioras typsnitt**, samma fel som Copilot: tre
`<link>`-rader till Google Fonts (`Playfair Display`, `Inter`) och **tre**
`--font-*`-överskrivningar i `_unpublished/guides/gemini-notebooklm/styles.css`
(rad 21–23: display, body **och** mono). Blueprints `tokens.css` är redan länkad
i samma `<head>` och sätter alla tre. Båda halvorna ska bort, annars faller
sidan tillbaka på Georgia och systemsans.

### Innehållsförteckningen är trasig, inte inaktuell

Copilot-specen påstod att den guiden inte hade hårdkodade sidnummer; den hade
sex, och ett var fel. Här är läget sämre och det är **mätt mot den renderade
PDF:en**, inte mot markupen:

| Avsnitt | Förteckningen säger | Börjar faktiskt på |
|---|---|---|
| Introduction | 3 | 3 ✓ |
| Understanding Gemini and NotebookLM | 5 | 5 ✓ |
| Part 1 · Getting Started | 8 | **7** |
| Part 2 · Working Smarter | 13 | **12** |
| Part 3 · Scale & Lead | 20 | **19** |
| Part 4 · Google Workspace for Education | 24 | **22** |
| Bonus Chapter · For EU readers | 28 | **25** |
| The Styles Library | 32 | **28** |
| Prompts | 34 | **30** |
| FAQ | 40 | **39** |

**Åtta av tio är fel, och driften växer från −1 till −4.** Det är inte en
slarvsiffra utan en förteckning som aldrig räknats om sedan kapitel växte. I en
guide där Styles Library och Prompts tillsammans är tolv sidor rent
referensmaterial — det läsaren slår upp på sidnummer — är det det mest
läsarnära felet i hela utkastet.

### Vad som INTE är ett problem här

Två saker som mätningen avfärdade, så att rundan inte letar efter dem:

- **Guidens utgående pekare lever.** Kapitlet om de 140 stilarna pekar på
  `choosewise.education/infographic-styles/` och den sidan svarar **200**, liksom
  `assets/pdfs/nlm-140-prompts-en.pdf`. Det som är känt trasigt är *byggaren* som
  regenererar promptdokumentet, inte dokumentet. Copilots quick-start skickade
  läsare till en 404; den här guiden gör det inte.
- **Ingen prissättning i fel valuta.** Guiden prissätter inte alls i SEK.

---

## 3. Vald väg: neutral kärna, och AI Act stannar som bonuskapitel

**Johans beslut 2026-10-12.** Copilot körde väg A rakt av — ingen lag och ingen
myndighet namngiven någonstans. Här blir det en variant, och skälet är att
materialet har en annan form:

Kapitlet heter i förteckningen **"Bonus Chapter · For EU readers"** och öppnar
med *"If you teach or lead a school in an EU member state"*. Det är alltså redan
skyltat och överhoppbart — inte, som Copilots del 3, guidens tyngsta del
stående som en varningsskylt för halva läsekretsen. Det var det skälet väg B
förkastades på för Copilot, och det gäller inte här.

**Det här stannar:** EU AI Act — artikel 4 om AI-kunnighet, ikraftträdandet, de
två datumen och risknivåerna. Skälet är dubbelt. Dels är det det enda regelverk
i kapitlet som riktar sig till skolan *som utbildare av sin personal*, vilket är
guidens egen läsekrets. Dels är **fakta redan belagda**: Claude-guidens
inventering från våg 2b (`docs/guide-facts-claude.md`, post P13) bär dem med
källa och hämtdatum. Att behålla dem kostar en korsreferens, inte en ny
källdomän.

**Det här går:** GDPR på artikelnivå (6(1)(e), 30), "your country's national
data protection authority", "every EU member state has one", resonemanget om
vilka medlemsstater som publicerat nationell vägledning, och DPIA som namngiven
artefakt där den är jurisdiktionsbunden. Skälet är rundans beviskrav: de kräver
nya källdomäner som ingen i den här rundan har verifierat, och spec-regeln från
Copilot gäller — **en faktamening utan post i inventeringen får inte skrivas**.

**Dataresidensen är produktfakta, inte juridik**, och behandlas som Copilots "EU
Data Boundary": den får stå där meningen säger var data lagras och behandlas,
aldrig som rättslig analys, och varje förekomst får en egen post med
motiveringen utskriven.

**GDPR står på tre ställen utanför bonuskapitlet**, och de behandlas olika:

- **Print rad 972–979, avsnittet "Data residency, GDPR, and national context"** —
  huvudflödets egen juridikpassage, med "National supervisory authorities. Every
  EU member state has one" och en svagare föregångare till jurisdiktionsrutan på
  rad 977 ("Readers outside the EU should verify…"). Det är **här rutan ska stå**:
  passagen ersätts av den, och dataresidensen stannar som produktfakta.
- **Print rad 541, förteckningens underrad** för bonuskapitlet ("GDPR, the EU AI
  Act, risk tiers, compliance checklist") — följer med när kapitlets skylt skärps.
- **Print rad 1357, inuti en promptmall** ("Relevant legal framework: [e.g. GDPR +
  EU AI Act + your national school-governance law]") — det är en platshållare
  läsaren själv fyller i med sitt eget regelverk, inte ett påstående guiden gör.
  Den får en post och en motivering, och utgångspunkten är att den **stannar**:
  exemplet visar formen på svaret, och att stryka det gör mallen svårare att
  använda utan att göra guiden mer sann.

**Jurisdiktionsrutan från Copilot återanvänds ordagrant i sak** — samma tre
kategorier läsaren ska kontrollera lokalt: dataskyddsregimen, reglerna om elevers
ålder och samtycke, och skolans egen upphandlings- och godkännandeväg. Inga
enskilda lagar eller myndigheter i rutan. Den står i huvudflödet enligt ovan, så
att läsare som hoppar över bonuskapitlet ändå möter den.

**Kapitlets skylt skärps:** rubriken säger i dag "For EU readers". Efter rundan
ska den säga vad kapitlet faktiskt täcker — AI Act — så att en läsare utanför EU
inte tror sig missa dataskyddsvägledning som inte längre står där.

---

## 4. Layout: rörs inte

Brödtext, rubriker, callout-rutor, färger och typografi är redan Blueprint.
Guiden behåller sitt eget omslag och sin egen sidfot.

**Tre ändringar som inte är layout:** datumstämpeln, innehållsförteckningens tio
sidnummer, och typsnittsraderna i §2. Sidnummer är innehåll, inte form.

---

## 5. Ytor

| Yta | Roll |
|---|---|
| `_unpublished/exports/gemini-notebooklm-print-a4-en.html` | källan till huvud-PDF:en — den egentliga leveransen |
| `_unpublished/exports/gemini-notebooklm-quick-start-en.html` | källan till quick-start-PDF:en, går också till Skool |
| `_unpublished/guides/gemini-notebooklm/index.html` | webbsidan, plus dess `styles.css` |

Webbsidan ingår fast den inte publiceras, av samma skäl som i Copilot-rundan:
lämnas den orörd divergerar den från print med varje faktarättning, och nästa
gång någon tar upp guiden för publicering är de två osynkade på exakt de
meningar som var känsligast.

**Quick-starten står utanför ytkonsistensvakten**, precis som Copilots, och
bevakas i stället av leveransvakten som läser PDF:erna.

---

## 6. Inventeringen

**`docs/guide-facts-gemini.md`**, byggd på Copilot-inventeringens form: en post
per volatilt påstående, med förekomster per yta, typ, källa med hämtdatum och
utfall, plus vaktblocket. Båda reglerna ärvs utan undantag:

1. **En faktamening utan post i inventeringen får inte skrivas.**
2. **Ett fynd som inte behöver ändras stryks aldrig tyst.**

Rundan väntas bli ungefär dubbelt så stor som Copilots 27 poster — guiden är 42
sidor och täcker **två produkter**.

**Särskilt misstänkta**, eftersom Google döper om och paketerar om ofta:
`Workspace for Education` (25 förekomster), `Gems` (28), `Canvas` (19),
`Deep Research` (14), `Audio Overview` (12), `Education Plus` (7),
`NotebookLM Enterprise` (2), `Gemini for Education` (2).

**Två daterade produktpåståenden** som inte är stämplar och som måste verifieras
som fakta: *"Since 8 April 2026 the two tools sync bidirectionally"* står på två
ställen (print rad 640 och 847). Ett datum i brödtext är ett påstående om när
något hände; källan måste bära det eller så går datumet.

**Ett tredjepartscitat:** Matt Miller (Ditch That Textbook, januari 2026) citeras
ordagrant. Citat kontrolleras mot sin egen källa, inte mot Google.

---

## 7. Kodarbetet

Rundans kodarbete är att **generalisera TOC-vakten**, inte att kopiera den.

`scripts/tests/test_copilot_toc.py` byggdes i Copilot-rundan med guidens namn i
filnamnet, i konstanterna och i ankarlistan. Att kopiera den till
`test_gemini_toc.py` skulle ge två filer med samma logik och två ställen att
laga — samma fel som `CLAUDE`-listan var, och den kostade en eskalering förra
rundan. Den ska i stället bli **guide-agnostisk**, med samma mönster som
`surfacecheck.GUIDE_SURFACES`: en karta från guide till mall, PDF och
ankarlista, och ett parametriserat test över guiderna.

Ytvakten och inventeringen är redan guide-agnostiska sedan Copilot-rundan;
Gemini läggs till genom att fylla `surfacecheck.GUIDE_SURFACES` och
`factinventory.INVENTORIES` med en rad var. **Leveransvakten**
(`test_copilot_delivery.py`) bör generaliseras på samma sätt när den får sin
andra guide — annars växer den till en fil per guide.

`RECAPTURED_THIS_ROUND` i `test_capture_guide_baseline.py` **töms och fylls om**
med den här rundans två PDF:er. Copilots fyra kommer ut. Konventionen står i en
kommentar ovanför konstanten sedan förra rundan.

### Känd begränsning, utskriven med avsikt

TOC-vakten kan bara kontrollera avsnitt vars startsida går att hitta med en
ankarsträng i den extraherade texten. `pdftotext` spärrar versaler oförutsägbart
("PA R T 1"), så ankaret måste tas ur brödtext eller en `<h3>`, aldrig ur en
spärrad etikett. Det är en känd fälla från Copilot-rundan och den gäller här med
tio ankare i stället för sex.

---

## 8. Verifiering

1. **Faktakontroll mot namngiven källa**, hämtad och läst samma dag — rå HTML och
   lokal textextraktion, aldrig en sammanfattning som källa till ett värde.
   Googles sidor kan svara 403 mot curl som Microsofts marknadsföringssidor
   gjorde; ett påstående utan hämtbar källa blir `obelagt` och skrivs om utan
   siffra.
2. **Omriktningen enligt §3**, inklusive att kapitlets skylt skärps.
3. **Alla tio sidnummer räknas om mot den renderade PDF:en** och vaktas.
4. **Bygg om de två engelska PDF:erna.** Båda byggarna renderar EN *och* SV i
   samma körning utan språkargument — de svenska kopieras undan och återställs
   med `cp`, aldrig `git checkout --`.
5. **Omfånga facit med `--only`** för exakt de två. `--force` är liktydigt med
   att slå av paritetsvakten för alla 22.
6. **Titta på det renderade dokumentet.** Åtta bilder, mot Copilots tre, och
   varje bild intill ändrad text granskas.
7. **Hela sviten**, plus en genomläsning av PDF:en från pärm till pärm.

### Fällor som gäller den här rundan

- **Sviten bär elva miljöberoende fel** i `test_prompt_pdf_parity.py` så länge
  `/tmp/pdf-parity-before/` är tom — macOS tömmer den vid dygnsskifte. Samma elva
  fallerar på `main`. Rundans siffror rapporteras med den filen exkluderad.
- **Mellan renderingen och facitomfångningen bär sviten fyra fel** till. Det är
  inneboende: man kan inte rendera om en PDF och behålla dess gamla fingeravtryck.
- **Jämför insamlade test-id:n mot `main`** om någon parametrisering rörs.
- **En vakt som inte setts bli röd vaktar ingenting.** Bryt varje ny vakt med
  flit och se den fallera på det den vaktar. En HTML-kommentar duger inte som
  brytning — `_TAG`-regexen slukar den.
- **`/usr/bin/python3` är enda interpretern** med pytest, playwright och Pillow.
- **`git add -A` används aldrig**, och `docs/` är gitignorerad: `git add -f`.

---

## 9. Vad som gör rundan klar

- Båda engelska PDF:erna byggda ur rättat innehåll, med Blueprint-layout.
- Inget "Sweden", "Swedish" eller namngiven myndighet kvar i de engelska ytorna
  annat än där det är ett medvetet, motiverat exempel med en post i inventeringen.
- GDPR på artikelnivå borta; AI Act kvar och korsrefererad till Claude-guidens
  verifierade poster; bonuskapitlets skylt säger vad kapitlet täcker.
- Jurisdiktionsrutan står i huvudflödet, utan namngiven lag eller myndighet.
- Varje volatilt påstående har en post i `docs/guide-facts-gemini.md` med källa
  och datum.
- Ytkonsistensvakten grön för Claude, Copilot och Gemini.
- TOC-vakten guide-agnostisk, grön för båda guiderna, och sedd röd på minst ett
  av de åtta felaktiga numren innan de rättades.
- PDF-facit omfångat med `--only`, de tjugo andra nycklarna orörda.
- Webbsidan rättad i sak och fri från Google Fonts och Crestiora-typsnitten.
- Det svenska divergensläget skrivet i överlämningen.
