# Apple Intelligence-guiden, runda 2: skriv om — implementationsplan

> **För agentiska arbetare:** OBLIGATORISK SUB-SKILL: använd
> `superpowers:subagent-driven-development` (rekommenderas) eller
> `superpowers:executing-plans` för att köra planen uppgift för uppgift. Stegen använder
> checkbox-syntax (`- [ ]`).

**Mål:** Gör Apple Intelligence-guiden sann mot verkligheten i oktober 2026 — med de sex
funktionerna kvar och ett tydligt EU-förbehåll där Apple spärrar dem — rikta om inramningen
internationellt, ge Del 3 ett kort AI Act-avsnitt, och leverera två omrenderade engelska PDF:er.

**Arkitektur:** Inventeringen `docs/guide-facts-apple-intelligence.md` är arbetsordern: 32 poster
med primärkälla och verdikt, varav **9 föråldrade och 7 falska** ska rättas. Varje
innehållsuppgift rättar sin del av guiden **på båda engelska ytorna** och uppdaterar **sina egna
inventeringsrader** i samma commit. Omrenderingen stänger rundan; vaktlistorna töms sist.

**Teknikstack:** Python 3.9.6 via `/usr/bin/python3` — **enda interpretern** med pytest,
playwright och Pillow. `pdftotext` (poppler) för PDF-text. Inga nya beroenden.

**Spec:** `docs/superpowers/specs/2026-10-14-apple-intelligence-guide-update-design.md` —
**läs §5 och dess två amendemang först.** Amendemang II bär Johans två bindande beslut.

**Runda 1:** mergad som `1fea250`. Dess plan och ledger:
`docs/superpowers/plans/2026-10-14-apple-intelligence-round-1.md` respektive
`~/Desktop/choosewise-apple-runda-1/`.

## Globala villkor

- **Varje innehållsändring görs på BÅDA engelska ytorna.** `EP` =
  `_unpublished/exports/apple-intelligence-print-a4-en.html` (print, 25 sidor), `EW` =
  `_unpublished/guides/apple-intelligence/index.html` (webb). Ytkonsistensvakten jämför print mot
  webb **per språk** för varje värde inventeringen pekar på — en rättelse i bara en yta gör
  sviten röd. Ytorna skiljer sig ~40 % i formulering med avsikt; leta upp motsvarande passage,
  skriv inte över den ena med den andras text.
- **De exakta värdena står i inventeringen, ordagrant citerade ur Apples egna sidor.** Hämta dem
  därifrån — härled dem inte på nytt, och hitta aldrig på ett värde. Varje post bär källa med
  hämtdatum.
- **Johans beslut (spec §5, amendemang II):** de sex funktionerna i Del 2 **stannar**, med ett
  tydligt EU-förbehåll **där läsaren möter funktionen** — inte bara samlat på ett ställe. Den
  svenska **quick-startens** avslutning städas med samma kirurgi som den engelska fick; de
  svenska **guideytorna** står kvar frysta.
- **Interpretern är `/usr/bin/python3`.** Hela sviten:
  `/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py`
  Utgångsläge på `main` `1fea250`: **840 passed / 0 failed**. Talet ska aldrig sjunka och noll
  failed är kravet. Den undantagna filens 11 fel är miljöberoende (facit i
  `/tmp/pdf-parity-before/`, som macOS tömmer) och inte rundans.
- **`apple-intelligence-guide-sv.pdf` ska komma ut byte-identisk.** Guidebyggaren renderar EN och
  SV i samma körning, och **byggaren är inte deterministisk för svenska** — omrendering ger en
  byte-ändrad SV-fil med identisk text. `git checkout --` på den svenska filen efter varje
  rendering, och `untouched`-vakten fäller den som committar den ändrad.
- **`docs/` är gitignorerad.** Ändringar i inventeringen committas med `git add -f`.
- **Ingenting publiceras.** Bara `_unpublished/`, `docs/`, `scripts/` och `exports/` får ändras.
- **Guidens titel står:** `Apple Intelligence` / *for teachers and school leaders*. Byggarens
  sidfot bär samma sträng och är ren — verifiera, men räkna inte med att behöva ändra den.

## Granskningsfokus

1. **En rättelse i bara en yta.** Ytkonsistensvakten läser bara de värden inventeringen pekar
   på, så en rättelse som missar EW blir röd först om posten har en `aktiv`-rad — och tyst annars.
   Pinnas i varje innehållsuppgift: sista steget kör inventeringskontrollen över båda ytorna.
2. **En inventeringsrad som inte flyttas med texten.** `Siri 2.0` är en `aktiv`-rad i dag; skrivs
   texten om utan att raden flyttas till `borttaget` blir vakten röd på `finns_ingenstans` — och
   läggs den nya formuleringen in utan `aktiv`-rad står rättelsen ovaktad. Pinnas i varje
   innehållsuppgift: raderna uppdateras i samma commit som texten.
3. **EU-förbehållet som bara står på ett ställe.** Johans beslut säger uttryckligen att en lärare
   som läser Siri-avsnittet inte ska behöva Del 3 för att veta att funktionen inte finns på hens
   iPad. Pinnas i Task 5 och 6 med en mätning: varje funktionsavsnitt som Apple spärrar bär
   förbehållet i sin egen löptext.
4. **Sidbrytningen som flyttar TOC:ns nummer.** Rundan lägger till text (EU-förbehåll, AI
   Act-avsnitt, A32:s betalnivå). Lärdomen från Gemini: luften på en sida mättes till 9,5 mm, och
   ett stycke till hade flyttat förteckningens sista nummer utan att någon märkte det förrän
   omrenderingen. Pinnas i Task 13, och varje innehållsuppgift som lägger till mer än ett stycke
   mäter sidan **före** den skriver.
5. **Sidfoten och quick-starten är text ingen ytvakt läser.** `pdf_body_text.PLAYWRIGHT_FOOTERS`
   är handkopierad ur byggarens `jobs`, och quick-starten står utanför ytkonsistensvakten med
   avsikt. Pinnas i Task 11: båda läses manuellt mot den renderade PDF:en.

---

### Task 1: Den svenska quick-startens kirurgi

Oberoende av resten av rundan och kan mergas först. Johans beslut, spec §5 amendemang II.

**Filer:**
- Ändra: `_unpublished/exports/apple-intelligence-quick-start-sv.html` (rad 190–193)
- Renderas om: `_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf`
- Ändra: `scripts/tests/test_guide_delivery.py` (`untouched` för `apple-intelligence`)
- Ändra: `scripts/tests/test_capture_guide_baseline.py` (`RECAPTURED_THIS_ROUND`)
- Skrivs av facitskriptet: `scripts/tests/fixtures/guide-pdf-baseline.json` och kroppstextfacit
- Får inte ändras: `_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-en.pdf`

**Gränssnitt:**
- Konsumerar: inget.
- Producerar: en svensk quick-start utan pekare, och en `untouched`-lista som bara bär
  guide-PDF:en.

- [ ] **Steg 1: Mät båda pekarna i den levererade svenska PDF:en**

```bash
/usr/bin/python3 -c "
import sys,re; sys.path.insert(0,'scripts')
from tests import pdf_fingerprint as fp
flat=re.sub(r'\s+',' ',fp.extract(fp.ROOT/'_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf'))
for n in ['25-sidiga','från samma sida','G U I D E R']:
    print(repr(n), flat.count(n))"
```
Förväntat: tre tal större än noll. Adressen står **spärrad** i PDF:en, som den engelska gjorde.

- [ ] **Steg 2: Skriv om avslutningen**

Ersätt rad 190–193 i `apple-intelligence-quick-start-sv.html`:

```html
  <div class="closing">
    <div class="msg">Vill du ha djup? Hela <em>Apple Intelligence-guiden</em> följer med den
      här snabbstarten i communityt.</div>
  </div>
```

Samma kirurgi som den engelska fick i runda 1: ingen URL, ingen platshållare, och
sidantalspåståendet försvinner med meningen. `<div class="url">` tas bort helt. **Rör ingenting
annat i filen** — resten av den svenska prosan är fryst.

- [ ] **Steg 3: Rendera om och återställ den engelska**

```bash
/usr/bin/python3 exports/build-apple-intelligence-quickstart-pdf.py
git status --short _unpublished/assets/pdfs/guides/
```
Byggaren renderar båda språken. Står den **engelska** quick-starten som ändrad är det byggarens
icke-determinism, inte din ändring — återställ den:
`git checkout -- _unpublished/assets/pdfs/guides/apple-intelligence-quick-start-en.pdf`
Verifiera därefter att bara den svenska filen står som ändrad.

- [ ] **Steg 4: Mät att pekarna är borta**

Kör kommandot från steg 1 igen. Förväntat: `0 0 0`.

- [ ] **Steg 5: Ta den svenska quick-starten ur `untouched`**

I `scripts/tests/test_guide_delivery.py`, `GUIDE_DELIVERY["apple-intelligence"]["untouched"]`:
lämna kvar guide-PDF:en, ta bort quick-start-raden, och skriv skälet intill:

```python
        # Quick-starten lämnade listan i runda 2 Task 1: Johans beslut
        # 2026-10-14 (spec §5 amendemang II) var att den svenska
        # avslutningen städas med samma kirurgi som den engelska fick, så
        # filen ÄR ändrad med avsikt. Guide-PDF:en står kvar — de svenska
        # guideytornas prosa är fortsatt fryst.
        "untouched": (
            "_unpublished/assets/pdfs/guides/apple-intelligence-guide-sv.pdf",
        ),
```

- [ ] **Steg 6: Se facitvakten röd, och omfånga exakt den filen**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_pdf_parity.py -q
```
Förväntat: FAIL för `apple-intelligence-quick-start-sv.pdf`.

```bash
/usr/bin/python3 scripts/tests/fixtures/capture_guide_baseline.py \
  --only _unpublished/assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf
```
**Kör aldrig med `--force`** — efter en ändring är det liktydigt med att stänga av
paritetsvakten för alla 22 nycklarna.

- [ ] **Steg 7: Fyll `RECAPTURED_THIS_ROUND`**

Listan töms, den fylls inte på. Runda 1:s post (`apple-intelligence-quick-start-en.pdf`) är
mergad och ska bort:

```python
RECAPTURED_THIS_ROUND = [
    # Runda 2 Task 1, 2026-10-14: den svenska quick-starten renderades om när
    # dess två pekare till en sida som aldrig publiceras togs bort (Johans
    # beslut, spec §5 amendemang II). Guide-PDF:erna och den engelska
    # quick-starten rördes INTE i den här uppgiften.
    "_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf",
]
```

- [ ] **Steg 8: Kör hela sviten och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
git add _unpublished/exports/apple-intelligence-quick-start-sv.html \
        _unpublished/assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf \
        scripts/tests/test_guide_delivery.py scripts/tests/test_capture_guide_baseline.py \
        scripts/tests/fixtures/
git commit -m "fix(apple): samma kirurgi på den svenska quick-starten som den engelska fick"
```
Förväntat: 840 passed, noll failed.

---

### Task 2: Del 1 — hårdvaran, lagringen och den döda hjälplänken

**Filer:**
- Ändra: `_unpublished/exports/apple-intelligence-print-a4-en.html` (sidorna 3–4, rad ~607–653)
- Ändra: `_unpublished/guides/apple-intelligence/index.html` (motsvarande passager)
- Ändra: `docs/guide-facts-apple-intelligence.md` (posterna A01–A03, A19, A23, A24)

**Gränssnitt:**
- Konsumerar: inget.
- Producerar: rättade hårdvaru- och lagringsvärden som Task 10:s FAQ-svar återanvänder.

**Fem rättelser, alla med exakt värde i sin inventeringspost:**

| post | guiden säger | verdikt och rätt värde |
|---|---|---|
| A03 | `iPad Pro or iPad Air from 2021` | **falskt** — iPad Air med M1 är 5:e generationen, **2022**. iPad Pro-halvan är rätt |
| A19 | `roughly 4 GB on-device model` | **föråldrat** — Apple anger **upp till 8 GB**, och **upp till 14 GB** på nyare hårdvara. Det är diskutrymme, inte en modellfil |
| A24 | `the full iPhone 16 and 17 lines are supported` | **föråldrat** — listan är `iPhone 16 models or later, iPhone 15 Pro, iPhone 15 Pro Max, iPhone Air` |
| A23 | `support.apple.com/apple-intelligence` | **falskt, och falskt redan i april** — 404. Ersätt med en länk som svarar 200 |
| A01, A02 | `M1 chip or later`, `iPhone 15 Pro` | **står** — rör dem inte |

- [ ] **Steg 1: Läs posterna och hämta de exakta värdena**

```bash
grep -n "^| A01 \|^| A02 \|^| A03 \|^| A19 \|^| A23 \|^| A24 " docs/guide-facts-apple-intelligence.md
```
Varje cell bär Apples ordagranna formulering med källa och hämtdatum. **Använd den — härled
inget.** Står en siffra i källcitatet men inte i verdiktet är källcitatet det som gäller.

- [ ] **Steg 2: Rätta de fem värdena i EP**

Sidorna 3–4. Bevara meningarnas form och längd så långt det går — en rättelse som gör stycket
tre rader längre flyttar sidbrytningen, och det kostar i Task 13.

- [ ] **Steg 3: Rätta samma fem värden i EW**

```bash
grep -n "2021\|4 GB\|iPhone 16 and 17\|support.apple.com/apple-intelligence" \
  _unpublished/guides/apple-intelligence/index.html
```
EW formulerar passagerna annorlunda med avsikt. Rätta **värdet**, inte formuleringen.

- [ ] **Steg 4: Flytta inventeringsraderna**

För varje rättad post: sätt den gamla `aktiv`-raden till `borttaget` och lägg en ny `aktiv`-rad
med det nya värdet, i en grupp som bär uppgiftens namn:

```
# Runda 2 Task 2 — hårdvaran, lagringen, hjälplänken
A03 | en | iPad Pro or iPad Air from 2021 | borttaget
A03 | en | <det nya värdet, ordagrant som det nu står på BÅDA ytorna> | aktiv
```
Uppdatera också postens verdikt i tabellen till `rättat i runda 2 Task 2` med en rad om vad som
står nu. **Lägg aldrig en `aktiv`-rad som bara står på en yta** — det är `saknas_på_en_yta`.

- [ ] **Steg 5: Kör inventeringskontrollen över båda ytorna**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q
```
Förväntat: PASS. Faller något på `saknas_på_en_yta` har en rättelse missat EW; på
`finns_ingenstans` är en rads värde inte det som faktiskt står; på `återinfört` står ett struket
värde kvar någonstans.

- [ ] **Steg 6: Kör hela sviten och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
git add -f docs/guide-facts-apple-intelligence.md
git add _unpublished/exports/apple-intelligence-print-a4-en.html \
        _unpublished/guides/apple-intelligence/index.html
git commit -m "fix(apple): Del 1 — hårdvaruåret, lagringskravet, iPhone-listan, hjälplänken"
```

---

### Task 3: Del 1 — de tre bearbetningsvägarna i sin nya form

**Filer:**
- Ändra: `_unpublished/exports/apple-intelligence-print-a4-en.html` (sidorna 5–8, rad ~654–741)
- Ändra: `_unpublished/guides/apple-intelligence/index.html` (motsvarande passager)
- Ändra: `docs/guide-facts-apple-intelligence.md` (A17, A25, A27, A28, A04, A26)

**Gränssnitt:**
- Konsumerar: Task 2:s rättade hårdvarubild.
- Producerar: den bearbetningsmodell Del 3 bygger sin integritetsanalys på (Task 7 och 9).

**Vad som ska ändras, och vad som uttryckligen inte ska det:**

| post | verdikt | vad uppgiften gör |
|---|---|---|
| A17 | **föråldrat** — guidens `three distinct places your request can be processed` | Modellen står kvar som tre vägar, men den tredje beskrivs rätt: Apple bygger assistenten *"in collaboration with Google and its Gemini models"*, och Gemini sitter alltså **inne i** Siri AI, inte som ett val vid sidan av. ChatGPT är fortfarande den **enda** leverantör Apple dokumenterar som valbar extension (A11 `står`) |
| A25 | **obelagt** — `Apple operates PCC regions in Europe` | Påståendet **stryks**. PCC-sidan bär ingen geografisk uppgift över huvud taget. Ersätt inte med ett annat geografiskt påstående — skriv om stycket utan det |
| A27 | **obelagt** — `Apple ships Apple Intelligence features monthly` | Kadensen går inte att belägga. Skriv om rekommendationen om terminsvis genomgång så att den inte vilar på en kadens |
| A29 | **obelagt, och sannolikt fel riktning** — `Summaries are on by default` | Hör till Task 6 (notissammanfattningarna), inte hit |
| A04, A26, A28 | **står** | Rör dem inte. `Private Cloud Compute`, whitepaper-hänvisningen och `stateless computation` är verifierade |

**Johans beslut gäller här:** spec §5:s ursprungliga formulering att Del 1 byggs om kring "vald
extern leverantör via Extensions" är **struken av amendemang I** — det är inte vad Apple har
byggt. Bygg inte stycket kring ett leverantörsval.

- [ ] **Steg 1: Mät sidornas luft innan du skriver**

```bash
/usr/bin/python3 -c "
import sys; sys.path.insert(0,'scripts')
from tests import pdf_fingerprint as fp
pages = fp.pages(fp.extract(fp.ROOT/'_unpublished/assets/pdfs/guides/apple-intelligence-guide-en.pdf'))
for n in (5,6,7,8):
    print(n, len(pages[n-1].split()), 'ord')"
```
Skriv ner talen i rapporten. Växer en sida med mer än ett stycke, mät om efter Task 13:s
rendering — det är den mätningen som avgör om TOC:ns nummer flyttar.

- [ ] **Steg 2: Skriv om tredje vägen i EP, sidorna 5–8**

Behåll rubrikerna och styckeindelningen. A17:s källcitat står i inventeringen.

- [ ] **Steg 3: Stryk A25:s och skriv om A27:s påstående i EP**

- [ ] **Steg 4: Gör samma tre ändringar i EW**

```bash
grep -n "three distinct places\|PCC regions in Europe\|features monthly" \
  _unpublished/guides/apple-intelligence/index.html
```

- [ ] **Steg 5: Flytta inventeringsraderna för A17, A25 och A27**

Grupp: `# Runda 2 Task 3 — de tre bearbetningsvägarna`. A25 och A27 får `borttaget`-rader **utan**
nya `aktiv`-rader: påståendena försvinner, de ersätts inte.

- [ ] **Steg 6: Kör inventeringskontrollen, hela sviten, och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
git add -f docs/guide-facts-apple-intelligence.md
git add _unpublished/exports/apple-intelligence-print-a4-en.html \
        _unpublished/guides/apple-intelligence/index.html
git commit -m "fix(apple): Del 1 — tredje bearbetningsvägen, och två obelagda påståenden ut"
```

---

### Task 4: Internationaliseringen — IMY, svenska skolor, 1:1 och språkfrågan

**Filer:**
- Ändra: `_unpublished/exports/apple-intelligence-print-a4-en.html` (sidorna 3, 7, 19, 24 och omslaget)
- Ändra: `_unpublished/guides/apple-intelligence/index.html` (motsvarande passager)
- Ändra: `docs/guide-facts-apple-intelligence.md` (A15:s språkhalva)

**Gränssnitt:**
- Konsumerar: inget.
- Producerar: en inramning utan nationella referenser, vilket Task 14:s förbudslista vaktar.

**Fem passager, mätta 2026-10-14 (EP-förekomster):**

| var | vad som står | vad som ska stå |
|---|---|---|
| omslagets ingress | `why that matters in a Swedish school context` | en formulering utan nationell referens |
| sidan 3 | `The practical point for Swedish schools: the iPads most commonly found in 1:1 programmes` | generellt om de iPad-flottor skolor faktiskt har |
| sidan 3 | `Swedish became available during 2025 alongside the other main European languages` | se A15 nedan — språkstatus är inte bara en inramningsfråga |
| sidan 7 | `A word on the Swedish context` + IMY-stycket (`The Swedish Data Protection Authority (IMY) has published guidance…`) | en jurisdiktionsruta i Gemini-guidens form: EU/EES-generell, utan namngiven nationell myndighet |
| sidorna 9 och 15 | klassrumsexemplen: `Proofreading Swedish: works on Swedish text…` och `point at a paragraph in a Swedish geography textbook` | exempel utan nationell referens, med samma pedagogiska poäng — ett språk läsaren undervisar i, inte ett namngivet |
| sidan 24 (FAQ) | `Is Apple Intelligence available in Swedish?` + svaret | se Task 10 |

**Del 2:s klassrumsexempel hör hit, inte till Task 6.** Task 6 rättar funktionernas fakta; de två
exemplen är inramning och tas här, så att mätningen i steg 5 kan kräva noll nationella referenser
utanför FAQ:n. Missas de blir Task 10:s steg 4 rött — det kräver noll `Swedish` på båda ytorna.

**A15 är inte en inramningsfråga utan rundans tyngsta fynd** och tillhör Task 5. Här rättas bara
den del av språkstycket som är inramning; löftet att svensk Siri `keep[s] improving through 2026`
hör till Siri-avsnittet.

- [ ] **Steg 1: Mät alla förekomster på båda ytorna**

```bash
/usr/bin/python3 -c "
import sys,re,html,pathlib; sys.path.insert(0,'scripts')
from tests import surfacecheck
def text(rel):
    s=(surfacecheck.ROOT/rel).read_text(encoding='utf-8')
    s=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S)
    return surfacecheck.normalise(html.unescape(re.sub(r'<[^>]+>',' ',s)))
for rel in ['_unpublished/exports/apple-intelligence-print-a4-en.html',
            '_unpublished/guides/apple-intelligence/index.html']:
    t=text(rel); print(rel)
    for k in ['Swedish','Sweden','IMY','1:1','Swedish school']:
        print(f'   {k!r}: {t.count(surfacecheck.normalise(k))}')"
```
Skriv talen i rapporten. De är före-bilden Task 14 jämför mot.

- [ ] **Steg 2: Läs Gemini-guidens jurisdiktionsruta som form**

```bash
grep -n -A12 "If you teach or lead a school in an EU member state" \
  _unpublished/exports/gemini-notebook-print-a4-en.html | head -20
```
Kopiera **formen**, inte texten: Apple-guidens ruta handlar om integritet och PCC, inte om AI
Act (det kommer i Task 8).

- [ ] **Steg 3: Skriv om de fyra passagerna i EP**

- [ ] **Steg 4: Skriv om samma fyra i EW**

- [ ] **Steg 5: Mät om — noll `Sweden`, noll `Swedish`, noll `IMY`**

Kör skriptet från steg 1. Förväntat: noll på alla fem nycklar **utom** där Task 10:s FAQ-svar
ännu står kvar. Står något kvar utanför FAQ:n: lista det i rapporten.

- [ ] **Steg 6: Kör inventeringskontrollen, hela sviten, och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
git add _unpublished/exports/apple-intelligence-print-a4-en.html \
        _unpublished/guides/apple-intelligence/index.html
git commit -m "fix(apple): internationell inramning — IMY-stycket, svenska skolor, 1:1-flottorna"
```

---

### Task 5: Del 2 — Siri-avsnittet: namnet, och EU-spärren

Rundans tyngsta uppgift. Läs Johans beslut i spec §5 amendemang II innan du skriver.

**Filer:**
- Ändra: `_unpublished/exports/apple-intelligence-print-a4-en.html` (sidorna 10–11, rad ~772–832)
- Ändra: `_unpublished/guides/apple-intelligence/index.html` (motsvarande passager)
- Ändra: `docs/guide-facts-apple-intelligence.md` (A10, A15)

**Gränssnitt:**
- Konsumerar: Task 3:s bearbetningsmodell.
- Producerar: EU-förbehållets formulering, som Task 6 återanvänder för de funktioner Apple
  spärrar.

**Två poster, och den andra är rundans viktigaste fynd:**

| post | verdikt | vad uppgiften gör |
|---|---|---|
| A10 | **falskt** — `Siri 2.0` är ett namn **Apple aldrig använt**. Noll träffar på apple.com; assistenten heter **Siri AI** | Byt namnet överallt: 3 förekomster i EW, 7 i EP. Avsnittsrubriken bär det också |
| A15 | **föråldrat, och rundans viktigaste fynd** — `Siri 2.0's fully localised voice responses` och löftet att svensk Siri `keep[s] improving through 2026` | **Siri AI är inte tillgänglig i EU** på iOS och iPadOS sedan 2026-09-14, med DMA som angivet skäl och **ingen tidplan**. Apple räknar själv upp vad EU-användare inte får: den nya appen för att återvända till konversationer, *"an expanded Visual Intelligence experience"*, *"integrated tools for writing"* och Siri mode i kameran |

**Johans beslut:** funktionen stannar i guiden, med ett tydligt EU-förbehåll **i avsnittets egen
löptext**. En lärare som läser Siri-avsnittet ska inte behöva Del 3 för att veta att funktionen
inte finns på hens iPad. Skriv förbehållet så att det säger tre saker: att Apple har spärrat
funktionen i EU, att skälet Apple anger är DMA, och att det inte finns någon tidplan.

- [ ] **Steg 1: Mät avsnittets luft och alla namnförekomster**

```bash
grep -c "Siri 2.0" _unpublished/exports/apple-intelligence-print-a4-en.html
grep -c "Siri 2.0" _unpublished/guides/apple-intelligence/index.html
/usr/bin/python3 -c "
import sys; sys.path.insert(0,'scripts')
from tests import pdf_fingerprint as fp
pages = fp.pages(fp.extract(fp.ROOT/'_unpublished/assets/pdfs/guides/apple-intelligence-guide-en.pdf'))
for n in (10,11):
    print(n, len(pages[n-1].split()), 'ord')"
```
Förväntat: 7 respektive 3 förekomster. Avviker talen: stanna och rapportera.

- [ ] **Steg 2: Läs A15:s källcitat ordagrant**

```bash
grep -n "^| A15 " docs/guide-facts-apple-intelligence.md
```
Cellen bär Apples egen uppräkning. Citera den inte rakt av i guiden — formulera för en lärare,
men säg inget källan inte säger. Särskilt: skriv **inte** att funktionen "kommer senare".

- [ ] **Steg 3: Byt namnet i EP och EW**

Alla tio förekomster. Kontrollera att avsnittsrubriken och TOC-underraden inte bär det gamla
namnet — TOC-underraden står på sidan 2 och är inte en del av avsnittet.

- [ ] **Steg 4: Skriv EU-förbehållet i avsnittets löptext, på båda ytorna**

- [ ] **Steg 5: Flytta inventeringsraderna**

```
# Runda 2 Task 5 — Siri AI: namnet och EU-spärren
A10 | en | Siri 2.0 | borttaget
A10 | en | Siri AI | aktiv
A15 | en | <den gamla formuleringen om lokaliserade svar> | borttaget
A15 | en | <en kort, ordagrann sträng ur det nya EU-förbehållet> | aktiv
```
**`Siri 2.0` som `borttaget`-rad är rundans starkaste enskilda vaktrad** — den gör det omöjligt
att skriva tillbaka namnet någonstans på de engelska ytorna utan att sviten blir röd.

- [ ] **Steg 6: Kör inventeringskontrollen, hela sviten, och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
git add -f docs/guide-facts-apple-intelligence.md
git add _unpublished/exports/apple-intelligence-print-a4-en.html \
        _unpublished/guides/apple-intelligence/index.html
git commit -m "fix(apple): Siri AI, och EU-spärren där läsaren möter funktionen"
```

---

### Task 6: Del 2 — de fem övriga funktionerna

**Filer:**
- Ändra: `_unpublished/exports/apple-intelligence-print-a4-en.html` (sidorna 9, 12–16)
- Ändra: `_unpublished/guides/apple-intelligence/index.html` (motsvarande passager)
- Ändra: `docs/guide-facts-apple-intelligence.md` (A05, A06, A07, A08, A09, A20, A21, A22, A29)

**Gränssnitt:**
- Konsumerar: Task 5:s formulering av EU-förbehållet.
- Producerar: rättade inställningsvägar som Task 10:s FAQ återanvänder.

| post | verdikt | vad uppgiften gör |
|---|---|---|
| A05 | **står (öppen EU-fråga)** — `Writing Tools` | Namnet står. Apples EU-uppräkning nämner *"integrated tools for writing"*, och om det syftar på guidens `Writing Tools` eller på Siri AI:s skrivintegration går **inte** att avgöra ur källan. Skriv förbehållet som det osäkra det är — påstå ingen av tolkningarna |
| A06 | **står (EU-förbehåll saknas)** — `Visual Intelligence` | Namnet står, men Apple spärrar det **utvidgade** lagret i EU. Skilj det grundläggande från det utvidgade; cellen bär ordalydelsen |
| A20 | **falskt, och falskt redan i april** — `Settings → Notifications → Summarise Previews` | Vägen finns inte. Rätt väg står i cellen (`Summarize Notifications` → `Choose Notifications to Summarize`) |
| A21 | **föråldrat** — `Settings → Mail → Categorisation` | Rätt väg och rätt rubriktext står i cellen |
| A22 | **föråldrat** — `three visual styles` i Image Playground | Utbudet är inte längre tre och inte längre en sluten lista. Cellen bär Apples formulering |
| A29 | **obelagt, och sannolikt fel riktning** — `Summaries are on by default` | Påstå inte utgångsläget. Skriv om så att läsaren får veta var inställningen finns i stället |
| A07 | **står (delvis obelagt)** — `Mail categorisation` och dess fyra kategorier | Kategorierna står. Det obelagda ledet är att kategoriseringen sker *"entirely on-device"* — en DPIA-bärande delfråga. Ta bort eller villkora det ledet; påstå det inte |
| A08, A09 | **står** | `Image Playground` och `Genmoji` är verifierade namn — rör dem inte |

- [ ] **Steg 1: Läs de nio posternas källceller**

```bash
grep -n "^| A05 \|^| A06 \|^| A07 \|^| A08 \|^| A09 \|^| A20 \|^| A21 \|^| A22 \|^| A29 " \
  docs/guide-facts-apple-intelligence.md
```

- [ ] **Steg 2: Mät luften på sidorna 9 och 12–16**

Samma skript som Task 3 steg 1, för sidorna 9, 12, 13, 14, 15, 16. Skriv ner talen.

- [ ] **Steg 3: Rätta de sju posterna i EP**

- [ ] **Steg 4: Rätta samma sju i EW**

- [ ] **Steg 5: Mät att EU-förbehållet står där läsaren möter funktionen**

```bash
/usr/bin/python3 -c "
import sys,re,html,pathlib; sys.path.insert(0,'scripts')
from tests import surfacecheck
s=(surfacecheck.ROOT/'_unpublished/exports/apple-intelligence-print-a4-en.html').read_text(encoding='utf-8')
for m in re.finditer(r'(?is)<h3[^>]*>(.*?)</h3>(.*?)(?=<h3|\Z)', s):
    rub=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',m.group(1)))).strip()
    kropp=html.unescape(re.sub(r'<[^>]+>',' ',m.group(2)))
    if any(k in rub for k in ('Siri','Visual Intelligence','Writing Tools')):
        print(f'{rub[:40]:42} EU-ord i avsnittet: {\"EU\" in kropp}')"
```
Förväntat: `True` för varje avsnitt vars funktion Apple spärrar. `False` betyder att förbehållet
bara står samlat någon annanstans, vilket Johans beslut uttryckligen avvisar.

- [ ] **Steg 6: Flytta inventeringsraderna**

Grupp: `# Runda 2 Task 6 — de fem övriga funktionerna`. A29 och A07:s on-device-led får
`borttaget`-rader utan nya `aktiv`-rader.

- [ ] **Steg 7: Kör inventeringskontrollen, hela sviten, och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
git add -f docs/guide-facts-apple-intelligence.md
git add _unpublished/exports/apple-intelligence-print-a4-en.html \
        _unpublished/guides/apple-intelligence/index.html
git commit -m "fix(apple): Del 2 — inställningsvägar, stilutbud, och EU-förbehåll per funktion"
```

---

### Task 7: Del 3 — ChatGPT-vägen

**Filer:**
- Ändra: `_unpublished/exports/apple-intelligence-print-a4-en.html` (sidan 21, rad ~1072–1091)
- Ändra: `_unpublished/guides/apple-intelligence/index.html` (motsvarande passage)
- Ändra: `docs/guide-facts-apple-intelligence.md` (A11, A12, A16, A18, A30, A31)

**Gränssnitt:**
- Konsumerar: Task 3:s bearbetningsmodell.
- Producerar: den faktabild Task 9:s policybeslut vilar på.

**Den goda nyheten först:** A11 och A12 är **`står`**. ChatGPT är fortfarande den enda leverantör
Apple dokumenterar som valbar extension, och OpenAI är fortfarande motparten. Del 3:s bärande
analys — att den externa vägen är den plats där integritetsberättelsen brister — håller alltså.
Det som inte håller är **tre detaljer om hur vägen fungerar**, och alla tre gör guidens
integritetslöfte starkare än Apples dokumentation:

| post | verdikt | rätt värde |
|---|---|---|
| A16 | **falskt — och falskt redan i april 2026** — `requires the user to be 18 or over` | Apple säger **13** år |
| A18 | **falskt — och falskt redan i april 2026** — `always shows a confirmation screen before sending` | Bekräftelsen är inte obligatorisk: inställningen `Turn off Confirm Requests` fanns redan i april |
| A31 | **falskt — och EP-exklusivt** — `Every path to ChatGPT shows a confirmation screen before sending` | Samma sak, samma källa. Raden har ingen vaktrad eftersom strängen bara står i EP |
| A30 | **föråldrat — och EW-exklusivt** — `Siri & Apple Intelligence → ChatGPT Extension` | Nuvarande väg står i cellen |

**Det här är den klass av fel rundan finns för.** En skolledare som läser att bekräftelsen alltid
visas fattar ett annat beslut än en som vet att den kan stängas av. Skriv rättelsen så att den
säger vad en skola behöver göra: att inställningen finns, och att den kan stängas av.

- [ ] **Steg 1: Läs de sex posternas källceller**

- [ ] **Steg 2: Rätta åldersgränsen och bekräftelsesteget i EP**

- [ ] **Steg 3: Rätta inställningsvägen i EW och bekräftelsesteget där**

Observera asymmetrin: A30 står bara i EW, A31 bara i EP. Båda ska rättas, var och en på sin yta,
och ingen av dem får en `aktiv`-rad som kräver båda ytorna.

- [ ] **Steg 4: Flytta inventeringsraderna**

Grupp: `# Runda 2 Task 7 — ChatGPT-vägen`. A16 och A18 får `borttaget` + ny `aktiv`.
A30 och A31 får **ingen** `aktiv`-rad — de är enytiga, och en sådan rad vore
`saknas_på_en_yta` från första sekunden. Skriv skälet i en kommentar intill.

- [ ] **Steg 5: Kör inventeringskontrollen, hela sviten, och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
git add -f docs/guide-facts-apple-intelligence.md
git add _unpublished/exports/apple-intelligence-print-a4-en.html \
        _unpublished/guides/apple-intelligence/index.html
git commit -m "fix(apple): ChatGPT-vägen — 13 år, och en bekräftelse som kan stängas av"
```

---

### Task 8: Del 3 — AI Act-avsnittet

**Filer:**
- Ändra: `_unpublished/exports/apple-intelligence-print-a4-en.html` (nytt avsnitt i Del 3, efter sidan 22)
- Ändra: `_unpublished/guides/apple-intelligence/index.html` (motsvarande avsnitt)
- Ändra: `docs/guide-facts-apple-intelligence.md` (nya poster)

**Gränssnitt:**
- Konsumerar: Task 7:s faktabild.
- Producerar: det regelavsnitt Task 9:s policybeslut hänvisar till.

**Avsnittet ärver Gemini-rundans källbelagda allokering — ingen ny research.** Hämta värdena ur
`docs/guide-facts-claude.md` post **P13** och `docs/guide-facts-gemini.md` posterna **G25, G26,
G27, G48, G51**. Där de räcker står `korsref` i källkolumnen och ingen ny hämtning görs.

**Vad avsnittet ska bära, och inte mer:**

- Riskbenämningarna som de faktiskt heter: `Unacceptable risk`, `Transparency risk`,
  `Minimal or no risk`. **Inte** `Limited risk`, **inte** `Minimal risk`, **inte** `Prohibited`.
- Att AI Act blev tillämplig **2 augusti 2026**, och att bilaga III-högrisk för **utbildning**
  gäller från **2 december 2027** — inte från 2026.
- Driftsättarens plikter enligt **art. 26**: instruktionerna (26.1), mänsklig tillsyn med
  kompetens, utbildning, befogenhet och stöd (26.2), de loggar skolan **styr** i minst sex
  månader (26.6), information till personal och deras företrädare före driftsättning (26.7),
  information till de berörda (26.11).
- **Art. 27:** konsekvensbedömning före första driftsättning.

**Två fel Gemini-rundan gjorde i miniatyr när den rättade samma sak — gör dem inte igen:**
1. Skriv **inte** att skolan ska "behålla systemets loggar i sex månader" utan 26.6:s förbehåll
   om driftsättarens kontroll. För ett molnsystem ligger merparten av loggarna hos leverantören.
2. Skriv **inte** att en skola är "a body governed by public law". Det är sant för en kommunal
   skola och **falskt för en friskola**.

Och: förhandsplikterna (art. 9–15, 17, 43, 48, 49.1) är **leverantörens**, inte skolans. Lägg dem
inte på en driftsättande skola.

- [ ] **Steg 1: Läs de fem korsrefererade posterna**

```bash
grep -n "^| P13 " docs/guide-facts-claude.md
grep -n "^| G25 \|^| G26 \|^| G27 \|^| G48 \|^| G51 " docs/guide-facts-gemini.md
```

- [ ] **Steg 2: Mät Del 3:s sista sidors luft innan du skriver**

Samma skript som Task 3 steg 1, för sidorna 19–23. **Avsnittet är ett tillägg, inte en
ersättning** — det kommer att flytta sidbrytningar, och Task 13 räknar om numren. Skriv ner
talen så att tillväxten går att mäta.

- [ ] **Steg 3: Skriv avsnittet i EP**

Kort. Guiden är en integritetsguide, inte en regelguide — spec §5 säger *kort avsnitt i Del 3*,
inte eget kapitel.

- [ ] **Steg 4: Skriv motsvarande avsnitt i EW**

- [ ] **Steg 5: Lägg nya inventeringsposter**

En post per volatilt värde avsnittet bär (datumen, riskbenämningarna, artikelnumren), med
`korsref P13` eller `korsref G51` i källkolumnen. Varje ny `aktiv`-rad ska stå ordagrant på båda
ytorna.

- [ ] **Steg 6: Kör inventeringskontrollen, hela sviten, och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
git add -f docs/guide-facts-apple-intelligence.md
git add _unpublished/exports/apple-intelligence-print-a4-en.html \
        _unpublished/guides/apple-intelligence/index.html
git commit -m "feat(apple): kort AI Act-avsnitt i Del 3, med driftsättarens plikter"
```

---

### Task 9: Del 3 — studentdata och de fem policybesluten

**Filer:**
- Ändra: `_unpublished/exports/apple-intelligence-print-a4-en.html` (sidorna 22–23)
- Ändra: `_unpublished/guides/apple-intelligence/index.html` (motsvarande passager)
- Ändra: `docs/guide-facts-apple-intelligence.md` (A14 oförändrad, eventuella nya poster)

**Gränssnitt:**
- Konsumerar: Task 5:s EU-förbehåll, Task 7:s rättade ChatGPT-fakta, Task 8:s AI Act-avsnitt.
- Producerar: guidens slutsatser, som Task 11:s quick-start sammanfattar.

De fem policybesluten är guidens takeaway. Efter Task 5, 7 och 8 vilar tre av dem på fakta som
flyttat sig: bekräftelsesteget kan stängas av, åldersgränsen är 13 år, och EU-läsaren kan inte få
Siri AI. **A14 (`Data Protection Impact Assessment`) står** — det är GDPR artikel 35, inte
Apple-fakta.

- [ ] **Steg 1: Läs de fem besluten som de står i dag**

```bash
sed -n '/PAGE 23 — FIVE POLICY DECISIONS/,/PAGE 24/p' \
  _unpublished/exports/apple-intelligence-print-a4-en.html
```

- [ ] **Steg 2: Skriv om de beslut vars premiss flyttat sig, i EP**

Rör inte de beslut som fortfarande håller. En omskrivning som inte behövs kostar sidutrymme och
flyttar nummer.

- [ ] **Steg 3: Gör samma ändringar i EW**

- [ ] **Steg 4: Kör inventeringskontrollen, hela sviten, och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
git add -f docs/guide-facts-apple-intelligence.md
git add _unpublished/exports/apple-intelligence-print-a4-en.html \
        _unpublished/guides/apple-intelligence/index.html
git commit -m "fix(apple): policybesluten mot den nya faktabilden"
```

---

### Task 10: FAQ

**Filer:**
- Ändra: `_unpublished/exports/apple-intelligence-print-a4-en.html` (sidan 24, rad ~1137–1219)
- Ändra: `_unpublished/guides/apple-intelligence/index.html` (motsvarande passage)
- Ändra: `docs/guide-facts-apple-intelligence.md` (A32, plus de poster FAQ-svaren bär)

**Gränssnitt:**
- Konsumerar: Task 2:s hårdvarusvar, Task 6:s inställningsvägar, Task 5:s EU-förbehåll.
- Producerar: inget senare uppgifter läser.

FAQ:n bär tio frågor och är den sida som samlar flest värden ur andra uppgifter. Tre saker ska
hända:

1. **Internationaliseringen slutförs:** frågan `Is Apple Intelligence available in Swedish?`
   skrivs om generellt för icke-engelska språk, och svaret får inte påstå en tidplan.
2. **De värden andra uppgifter rättat följer med** — hårdvarusvaret (Task 2), inställningsvägarna
   (Task 6), Siri AI och EU-spärren (Task 5). FAQ:n är den vanligaste platsen för ett värde som
   rättats överallt utom här.
3. **A32, `föråldrat (genom frånvaro)`:** guiden säger ingenting om att serverbaserade funktioner
   har en **daglig användningsgräns** och att utökad åtkomst *"will be available for a fee in the
   future"*. Lägg till det — en skolledare som planerar en utrullning behöver veta det.

- [ ] **Steg 1: Lista FAQ:ns tio frågor och vilka poster var och en bär**

- [ ] **Steg 2: Skriv om de berörda svaren i EP**

- [ ] **Steg 3: Skriv om samma svar i EW**

- [ ] **Steg 4: Mät att inget nationellt begrepp står kvar någonstans**

```bash
/usr/bin/python3 -c "
import sys,re,html; sys.path.insert(0,'scripts')
from tests import surfacecheck
for rel in ['_unpublished/exports/apple-intelligence-print-a4-en.html',
            '_unpublished/guides/apple-intelligence/index.html']:
    s=(surfacecheck.ROOT/rel).read_text(encoding='utf-8')
    t=surfacecheck.normalise(html.unescape(re.sub(r'<[^>]+>',' ',s)))
    print(rel, {k: t.count(k) for k in ('Sweden','Swedish','IMY','Siri 2.0')})"
```
Förväntat: noll på alla fyra, på båda ytorna. **Det här är kvittot Task 14:s förbudslista vilar
på.**

- [ ] **Steg 5: Flytta inventeringsraderna och lägg A32:s nya poster**

- [ ] **Steg 6: Kör inventeringskontrollen, hela sviten, och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
git add -f docs/guide-facts-apple-intelligence.md
git add _unpublished/exports/apple-intelligence-print-a4-en.html \
        _unpublished/guides/apple-intelligence/index.html
git commit -m "fix(apple): FAQ — språkfrågan, de rättade värdena, och användningsgränsen"
```

---

### Task 11: Omslaget, sidfoten, datumstämpeln och den engelska quick-starten

**Filer:**
- Ändra: `_unpublished/exports/apple-intelligence-print-a4-en.html` (sidorna 1, 2, 25)
- Ändra: `_unpublished/guides/apple-intelligence/index.html` (omslag och avslutning)
- Ändra: `_unpublished/exports/apple-intelligence-quick-start-en.html`
- Läs (ändra bara om den bär fel text): `exports/build-apple-intelligence-pdf.py`
- Ändra: `docs/guide-facts-apple-intelligence.md` (A13)

**Gränssnitt:**
- Konsumerar: allt innehåll från Task 2–10.
- Producerar: de ytor Task 13 renderar om.

| vad | nuläge | vad uppgiften gör |
|---|---|---|
| A13, datumstämpeln | `April 2026` — tre förekomster per yta (omslag, löpande, avslutning) | **föråldrat.** Sätt om till rundans månad |
| TOC:ns underrad för Del 3 | `On-device, PCC, ChatGPT — and five policy decisions` | Nämner inte AI Act-avsnittet. Uppdatera underraden; **numren räknas om i Task 13** |
| byggarens sidfot | `"Apple Intelligence for teachers and school leaders"` i `jobs` | Verifiera mot den renderade PDF:en att strängen är ren. Den bär inget pensionerat namn i dag, men **ingen ytvakt läser den** |
| quick-startens avslutning | `The full Apple Intelligence Guide comes with this quick start in the community.` | Lägg till guidens sidantal i en formulering som **nämner guiden**, så att sidantalsvakten ser påståendet. Ingen URL, ingen platshållare — Johans beslut står |
| quick-startens innehåll | sammanfattar sex funktioner | Uppdatera de värden Task 5, 6 och 7 rättat. Quick-starten står **utanför** ytkonsistensvakten och vaktas bara av leveransvakten och av din läsning |

**Sidantalspåståendet skrivs INTE här.** Talet är inte känt förrän Task 13 renderat, och ett
påstående med fel tal är precis vad vakten finns för. Den här uppgiften skriver avslutningens
mening **utan** sidantal; Task 13 steg 3b lägger in talet när det är mätt. Formulera meningen så
att talet kan skjutas in utan att satsen skrivs om, och så att ordet `Guide` står inom 60 tecken
efter talets plats — annars ser `_PAGE_CLAIM` inte påståendet.

- [ ] **Steg 1: Mät alla tre datumstämplar per yta**

```bash
grep -c "April 2026" _unpublished/exports/apple-intelligence-print-a4-en.html
grep -c "April 2026" _unpublished/guides/apple-intelligence/index.html
```
Förväntat: 3 och 3.

- [ ] **Steg 2: Sätt om stämpeln på båda ytorna, och i quick-starten**

- [ ] **Steg 3: Uppdatera TOC:ns underrad för Del 3**

- [ ] **Steg 4: Läs byggarens sidfotssträngar mot den renderade PDF:en**

```bash
grep -n -A3 "^jobs = \[" exports/build-apple-intelligence-pdf.py
pdftotext -layout _unpublished/assets/pdfs/guides/apple-intelligence-guide-en.pdf - | grep -c "for teachers and school leaders"
```
Bär sidfoten en sträng som rundan pensionerat: rätta den i byggaren. Gör den inte det: skriv i
rapporten att du läste den och vad den sa.

- [ ] **Steg 5: Uppdatera quick-startens innehåll och avslutning**

- [ ] **Steg 6: Flytta A13:s inventeringsrader, kör sviten och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
git add -f docs/guide-facts-apple-intelligence.md
git add _unpublished/exports/ _unpublished/guides/apple-intelligence/index.html
git commit -m "fix(apple): datumstämpeln, TOC-underraden, sidfoten och quick-startens innehåll"
```

---

### Task 12: Inventeringens slutkontroll, och `MEASURE_ONLY_INVENTORIES` tömd

**Filer:**
- Ändra: `docs/guide-facts-apple-intelligence.md` (huvudet, utfallsräkningen, kvalifikatortabellen)
- Ändra: `scripts/tests/test_guide_surface_consistency.py` (`MEASURE_ONLY_INVENTORIES`)

**Gränssnitt:**
- Konsumerar: alla inventeringsrader Task 2–11 flyttat.
- Producerar: en inventering som beskriver den omskrivna guiden, inte aprilversionen.

`MEASURE_ONLY_INVENTORIES` finns därför att en inventering som bara **mäter** har noll
`borttaget`-rader. Efter Task 2–11 har Apples inventering många, och posten ska **strykas** —
`test_the_measure_only_list_cannot_rot` är röd så länge den står kvar med betald skuld.

- [ ] **Steg 1: Räkna om utfallsfördelningen**

Dokumentets `## Utfallsräkningen` räknas på varje cells **inledande** token. Räkna om den mot de
verdikt som nu står, och uppdatera kvalifikatortabellen `### Poster som bär en andra token längre
in i cellen`.

- [ ] **Steg 2: Uppdatera huvudet**

Huvudet säger att inventeringen är en mätning av guiden som den stod 2026-10-14. Skriv om det:
den beskriver nu den omskrivna guiden, och verdiktkolumnen bär vad runda 2 gjorde med varje post.

- [ ] **Steg 3: Se vakten röd, och stryk posten**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q -k measure_only
```
Förväntat: FAIL på "skulden är betald, stryk posten ur MEASURE_ONLY_INVENTORIES".

Stryk posten. Är listan tom ska **både listan och dess ruttnandevakt strykas** — en tom lista
vaktar ingenting, och `test_the_measure_only_list_cannot_rot` samlar då noll parametriseringar,
vilket är grönt utan att vakta något. Lämna en kommentar i filen om varför listan fanns, så att
nästa guides mät-och-vakta-runda inte får återuppfinna resonemanget.

- [ ] **Steg 4: Kör hela sviten och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
git add -f docs/guide-facts-apple-intelligence.md
git add scripts/tests/test_guide_surface_consistency.py
git commit -m "docs(apple): inventeringen beskriver den omskrivna guiden, mät-och-vakta-posten struken"
```

---

### Task 13: Omrenderingen — sidantal, TOC-nummer, ankare och facit

**Filer:**
- Renderas om: `apple-intelligence-guide-en.pdf`, `apple-intelligence-quick-start-en.pdf`
- Får inte ändras: `apple-intelligence-guide-sv.pdf`
- Ändra: `_unpublished/exports/apple-intelligence-print-a4-en.html` (TOC:ns nummer)
- Ändra: `scripts/tests/test_guide_toc.py` (Apples fem ankare, `XFAIL_UNTIL_RECOUNTED`)
- Ändra: `scripts/tests/test_capture_guide_baseline.py` (`RECAPTURED_THIS_ROUND`)
- Skrivs av facitskriptet: `scripts/tests/fixtures/`

**Gränssnitt:**
- Konsumerar: allt innehåll.
- Producerar: det sidantal Task 14:s förbudslista och quick-startens påstående vilar på.

- [ ] **Steg 1: Rendera om båda engelska PDF:erna**

```bash
/usr/bin/python3 exports/build-apple-intelligence-pdf.py
/usr/bin/python3 exports/build-apple-intelligence-quickstart-pdf.py
git status --short _unpublished/assets/pdfs/guides/
```
Står `apple-intelligence-guide-sv.pdf` som ändrad: `git checkout --` på den. Byggaren är inte
deterministisk för svenska, och `untouched`-vakten fäller en committad ändring.

- [ ] **Steg 2: Mät det nya sidantalet**

```bash
/usr/bin/python3 -c "
import sys; sys.path.insert(0,'scripts')
from tests import pdf_fingerprint as fp
pages = fp.pages(fp.extract(fp.ROOT/'_unpublished/assets/pdfs/guides/apple-intelligence-guide-en.pdf'))
pages = pages[:-1] if pages and pages[-1]=='' else pages
print(len(pages), 'sidor')
for i,p in enumerate(pages,1):
    n=len(p.split())
    print(f'  {i:2} {n:4} ord', '  ← mycket tunn' if n<80 else '')"
```
**Stoppvillkor:** inget sidantal är fel i sig, men **ingen sida utom omslaget får vara under 400
tecken**, och en sida som blivit nästan tom betyder att ett avsnitt brutit fel. Rapportera talet
och varje tunn sida.

- [ ] **Steg 3: Räkna om TOC:ns fem nummer i mallen**

- [ ] **Steg 3b: Skjut in sidantalet i quick-startens avslutning**

Task 11 skrev meningen utan tal. Lägg in det mätta sidantalet så att formuleringen nämner
`Guide` inom 60 tecken efter talet, rendera om quick-starten (steg 1 igen), och verifiera:

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_delivery.py -q -k page_count
```
Förväntat: PASS. Faller den säger meddelandet vilket tal quick-starten trycker och vilket
guiden faktiskt har.

- [ ] **Steg 4: Verifiera om alla fem ankare mot den omrenderade PDF:en**

```bash
/usr/bin/python3 -c "
import sys; sys.path.insert(0,'scripts')
from tests import pdf_fingerprint as fp, surfacecheck
from tests.test_guide_toc import config_for, toc_rows
cfg = config_for('apple-intelligence')
pages = [surfacecheck.normalise(p) for p in fp.pages(fp.extract(fp.ROOT/cfg['pdf']))]
for titel, papperssida in toc_rows('apple-intelligence'):
    ankare = surfacecheck.normalise(cfg['anchors'][titel])
    traffar = [i+1 for i,p in enumerate(pages) if i+1 > cfg['toc_page'] and ankare in p]
    status = 'OK ' if traffar[:1] == [papperssida] else 'FEL'
    print(status, titel, '| ankaret på', traffar, '| förteckningen säger', papperssida)"
```
Rundan skriver om prosan, så flera ankare kommer att sakna träff. **Byt ankaret, inte numret** —
och välj nya ankare ur `pdftotext`-utskriften, fria från produktnamn, pris och datum. Det är
konventionen runda 1 införde, och den gäller.

- [ ] **Steg 5: Töm `XFAIL_UNTIL_RECOUNTED`**

Har du använt mängden under omräkningen ska den vara tom när numren är rätta. En mängd som bara
växer slutar vakta något.

- [ ] **Steg 6: Omfånga båda omrenderade PDF:erna, och fyll om `RECAPTURED_THIS_ROUND`**

```bash
/usr/bin/python3 scripts/tests/fixtures/capture_guide_baseline.py \
  --only _unpublished/assets/pdfs/guides/apple-intelligence-guide-en.pdf \
  --only _unpublished/assets/pdfs/guides/apple-intelligence-quick-start-en.pdf
```
**Aldrig `--force`.** `RECAPTURED_THIS_ROUND` ska efteråt bära exakt de PDF:er rundan renderat om
— Task 1:s svenska quick-start plus dessa två — och ingenting annat.

- [ ] **Steg 7: Kör hela sviten och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
git add _unpublished/exports/apple-intelligence-print-a4-en.html \
        _unpublished/assets/pdfs/guides/ scripts/tests/
git commit -m "build(apple): omrendering — nytt sidantal, omräknad förteckning, nya ankare"
```

---

### Task 14: Leveransvakten — förbudslistan fylls

**Filer:**
- Ändra: `scripts/tests/test_guide_delivery.py` (`forbidden`, `NO_PAGE_CLAIM`, `BARE_PAGE_NUMBERS`, `XFAIL_UNTIL_RERENDERED`)

**Gränssnitt:**
- Konsumerar: Task 13:s omrenderade PDF:er.
- Producerar: vakten som gör rundans rättelser oåterkalleliga.

Runda 1:s förbudslista fick bara bära strängar PDF:erna redan var fria från. Nu är rättelserna
gjorda och renderade, och listan kan bära dem — **men bara de som faktiskt är frånvarande.**

- [ ] **Steg 1: Mät varje kandidat i båda engelska PDF:erna**

```bash
/usr/bin/python3 -c "
import sys,re; sys.path.insert(0,'scripts')
from tests import pdf_fingerprint as fp
pdfs=['_unpublished/assets/pdfs/guides/apple-intelligence-guide-en.pdf',
      '_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-en.pdf']
flat={p: re.sub(r'\s+',' ',fp.extract(fp.ROOT/p)) for p in pdfs}
for n in ['Siri 2.0','Sweden','Swedish','IMY','April 2026','18 or over',
          'always shows a confirmation screen','Summarise Previews',
          'PCC regions in Europe','features monthly','three visual styles',
          'support.apple.com/apple-intelligence','iPad Air from 2021']:
    print(f'{n!r:45}', {k.rsplit('/',1)[-1]: v.count(n) for k,v in flat.items()})"
```
**Bara kandidater med noll i båda får in i listan.** En kandidat med en kvarvarande förekomst
betyder att en rättelse missats — gå tillbaka till den uppgift som ägde den, lägg inte en
`XFAIL_UNTIL_RERENDERED` över den.

- [ ] **Steg 2: Skriv listan, med en kommentar som skiljer klasserna**

Guiden bär fortfarande `GDPR` legitimt (den är en integritetsguide) och `ChatGPT`/`OpenAI`
legitimt (A11 och A12 `står`). Förbjud dem inte. Skriv i kommentaren vilka ord som medvetet
**inte** står på listan och varför — runda 1:s lista gör det, och nästa runda läser det.

- [ ] **Steg 3: Pröva `NO_PAGE_CLAIM` och `BARE_PAGE_NUMBERS`**

Skrev Task 11 ett sidantalspåstående som nämner guiden, ska `apple-intelligence` **strykas** ur
`NO_PAGE_CLAIM` — och är listan tom ska listan och dess ruttnandevakt strykas. Står
`Summarise a 5-page curriculum PDF` kvar i quick-starten ska `BARE_PAGE_NUMBERS`-posten stå kvar;
har Task 11 skrivit om stycket ska posten uppdateras eller strykas.

- [ ] **Steg 4: `XFAIL_UNTIL_RERENDERED` ska vara tom**

Mängden är per PDF. Är den inte tom när rundan är klar har en PDF inte renderats om.

- [ ] **Steg 5: Bryt vakten med flit i en engångsworktree**

Skriv tillbaka `Siri 2.0` i printytan, rendera om, kör leveransvakten. Förväntat: FAIL.
Riv worktreen; mät aldrig i ett arbetsträd du saboterat.

- [ ] **Steg 6: Kör hela sviten och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
git add scripts/tests/test_guide_delivery.py
git commit -m "test(apple): förbudslistan bär rundans rättelser"
```

---

### Task 15: Helgranskning av grenen, och underlag för Johans redaktionella pass

**Filer:** inga ändras, om granskningen inte hittar något.

- [ ] **Steg 1: Mät sviten i en ORÖRD utcheckning**

```bash
git worktree add /tmp/apple2-verify HEAD && cd /tmp/apple2-verify
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
```
Mät aldrig i arbetsträdet: en `cp`-återställning som inte bet gav en gång en laddad modul med
sabotaget kvar och ett `git status` som sa rent, och det kostade en utredning.

- [ ] **Steg 2: Filsvep och publiceringskontroll**

```bash
git diff --name-only main...HEAD | sed 's|/.*||' | sort | uniq -c
git diff --name-only main...HEAD | grep -v "^_unpublished/\|^docs/\|^scripts/\|^exports/" || echo "inget publicerat rört"
```

- [ ] **Steg 3: Verifiera att den svenska guide-PDF:en är byte-identisk**

```bash
git diff --stat $(git merge-base main HEAD) -- _unpublished/assets/pdfs/guides/apple-intelligence-guide-sv.pdf
```
Förväntat: ingen utskrift. Den svenska **quick-starten** ska däremot vara ändrad — det är Task 1.

- [ ] **Steg 4: Läs guiden som läsare, och skriv Johans beslutsunderlag**

Rapporten ska bära, i prioritetsordning: varje passage där du är osäker på om formuleringen är
Johans röst, varje ställe där EU-förbehållet kan läsas som att funktionen kommer senare, och
varje dubblering som uppstått när flera uppgifter rättat samma sak på olika ställen.
Gemini-rundans motsvarande pass hittade tre dubbleringar som ingen vakt kunde se.

- [ ] **Steg 5: Riv worktreen och rapportera**

Rapporten ska bära: svitens tal ur den orörda utcheckningen med sha, sidantalet, filsvepets
utfall, inventeringens nya fördelning, och beslutsunderlaget från steg 4. Pusha inte och öppna
ingen PR utan Johans klartecken.
