# Apple Intelligence-guiden, runda 1: mät och vakta — implementationsplan

> **För agentiska arbetare:** OBLIGATORISK SUB-SKILL: använd
> `superpowers:subagent-driven-development` (rekommenderas) eller
> `superpowers:executing-plans` för att köra planen uppgift för uppgift. Stegen använder
> checkbox-syntax (`- [ ]`).

**Mål:** Kartlägg Apple Intelligence-guiden i de fyra vaktlagren, skriv dess
påståendeinventering som en mätning av dagens guide, städa Crestioras typsnitt ur båda
webbytorna och ta bort quick-startens döda adress — utan att röra guidens prosa.

**Arkitektur:** Inga vakter ändras, fem kartor fylls. Två förberedelser görs **före**
kartläggningen, eftersom de rör filer kartläggningen annars kopierar sprött eller spränger.
Ordningen är tvingande på tre ställen: inventeringen före ytkartan (`test_every_guide_has_an_inventory_file`),
den döda adressen före leveranskartan (annars är förbudslistan röd vid införandet), och
sentinelbytet före TOC-kartan (annars faller `test_an_unknown_guide_is_a_loud_error`).

**Teknikstack:** Python 3.9.6 via `/usr/bin/python3` — **enda interpretern** med pytest,
playwright och Pillow. `pdftotext` (poppler) för PDF-text. Inga nya beroenden.

**Spec:** `docs/superpowers/specs/2026-10-14-apple-intelligence-guide-update-design.md`

## Globala villkor

- **Guidenyckeln är `apple-intelligence`** i alla fem kartor. Inventeringsfilen heter därför
  `docs/guide-facts-apple-intelligence.md` — skuldlistan namnger den redan.
- **Guidens prosa rörs inte i runda 1.** Undantag: quick-startens avslutning (Task 3).
- **De svenska PDF:erna ska komma ut byte-identiska** mot merge-basen. Båda byggarna renderar
  EN *och* SV i samma körning.
- **Ingenting publiceras.** Bara `_unpublished/`, `docs/`, `scripts/` och `exports/` får ändras.
- **Sviten körs med `test_prompt_pdf_parity.py` undantagen:**
  `/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py`
  Baslinje på `main` `fae8983`: **808 passed**. Filens 11 fel är miljöberoende (facit i
  `/tmp/pdf-parity-before/`, som macOS tömmer) och är inte rundans.
- **Varje ny vaktrad ska bevisas röd** genom att brytas med flit — i en **engångsworktree**,
  aldrig i arbetsträdet du sedan mäter i.
- **`docs/` är gitignorerad.** Nya filer under `docs/` måste läggas till med `git add -f`.

## Granskningsfokus

1. **En vakt som mäter ingenting är grön.** En tom `anchors`-lista ger noll parametriseringar.
   Pinnas i Task 6 av den befintliga `test_every_guide_in_the_toc_map_has_anchors_for_every_row`,
   som måste ses röd mot en tom lista innan den räknas som skydd.
2. **SV-PDF:erna skrivs av byggaren varje gång EN renderas om.** En orörd yta kan alltså smyga in
   i leveransen som en omrenderad fil. Pinnas i Task 3 med byte-jämförelse mot merge-basen.
3. **En inventeringsrad som bara står på en yta gör vakten röd.** `IMY` är mätt till EP:1 / EW:0 —
   den divergensen finns redan. Pinnas i Task 4: varje `aktiv`-rad körs genom
   `surfacecheck.check` mot båda ytorna innan den skrivs in.
4. **`pdftotext` spärrar versaler.** Den döda adressen står som
   `/ G U I D E S / A P P L E - I N T E L L I G E N C E` i den renderade filen; en förbudssträng
   skriven som URL matchar aldrig. Pinnas i Task 7 med strängen mätt i `_flat()`-form.
5. **En sentinel som är nästa guides namn är programmerad att gå sönder.** Pinnas i Task 1:
   assertionen vänds mot `config_for`:s kända nycklar i stället för två hårdkodade strängar.

---

### Task 1: Av-sprödade TOC-ankare och en sentinel som överlever tillväxt

**Filer:**
- Ändra: `scripts/tests/test_guide_toc.py` (ankare i `GUIDE_TOC`, rad 46–52 och 64–90; sentineltestet rad 131–138)

**Gränssnitt:**
- Konsumerar: inget.
- Producerar: `GUIDE_TOC` med ankare fria från produktnamn, pris och datum, så att Task 6 kan
  kopiera mönstret i stället för sprödheten.

- [ ] **Steg 1: Kör ankarvakten och se den grön i utgångsläget**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_toc.py -q
```
Förväntat: PASS. Detta är jämförelsepunkten — ankarbytet får inte ändra ett enda sidnummer.

- [ ] **Steg 2: Byt de fem spröda ankarna**

Alla fem ersättningar är verifierade 2026-10-14 mot respektive levererad PDF: var och en
träffar på exakt **en** sida, och det är avsnittets startsida.

I `GUIDE_TOC["copilot"]["anchors"]`:

```python
        "About this guide": "share any adaptations under the same license",
```

I `GUIDE_TOC["gemini"]["anchors"]`:

```python
            "Part 1 · Getting Started":
                "you will have five concrete things to try this week",
            "Part 2 · Working Smarter":
                "it is time to stop starting from scratch",
            "Part 4 · Google Workspace for Education":
                "what teachers need to know (briefly) and what school leaders need to decide (at length)",
            "FAQ":
                "Common questions",
```

Ersätt kommentarerna som förklarar de gamla ankarens namnbyten med en rad som säger varför de
nya är valda: *ankare får inte bära produktnamn, pris eller datum — de bryts då av nästa runda
som rör just det, och ett brutet ankare ser ut som ett fel sidnummer.*

- [ ] **Steg 3: Kör vakten och se att numren står kvar**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_toc.py -q
```
Förväntat: PASS, lika många tester som i steg 1.

- [ ] **Steg 4: Skriv om sentineltestet**

Ersätt `test_an_unknown_guide_is_a_loud_error` (rad 131–138):

```python
def test_an_unknown_guide_is_a_loud_error():
    """En guide som inte finns i kartan får inte ge en tom konfiguration
    — då vaktar vakten ingenting och är grön för det.

    Sentinelen får ALDRIG vara nästa guides namn. Den här raden sa
    `apple-intelligence` ända fram till Apple-rundan, och var alltså
    programmerad att gå sönder i samma stund guiden kartlades — samma
    anti-mönster som Task 12 rev ut ur test_guide_surface_consistency.py,
    där sentinelen var "gemini". En vakt som bryts av att systemet växer
    som avsett blir avstängd, inte lagad.
    """
    with pytest.raises(KeyError) as exc:
        config_for("ingen-sådan-guide")
    for known in GUIDE_TOC:
        assert known in str(exc.value)
```

- [ ] **Steg 5: Bevisa att sentinelvakten fortfarande fångar det den ska**

I en engångsworktree, lägg till `"ingen-sådan-guide": {}` i `GUIDE_TOC` och kör testet.
Förväntat: FAIL på `pytest.raises` — vakten ser att ett okänt namn plötsligt är känt.
Riv worktreen; rör inte arbetsträdet.

```bash
git worktree add /tmp/apple-probe-1 HEAD && cd /tmp/apple-probe-1
# bryt, kör, läs utfallet, gå tillbaka
cd - && git worktree remove --force /tmp/apple-probe-1
```

- [ ] **Steg 6: Kör hela sviten**

```bash
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
```
Förväntat: 808 passed.

- [ ] **Steg 7: Committa**

```bash
git add scripts/tests/test_guide_toc.py
git commit -m "test(toc): ankare utan produktnamn, och en sentinel som tål att systemet växer"
```

---

### Task 2: Crestioras typsnitt ur båda Apple-webbytorna

**Filer:**
- Ändra: `_unpublished/guides/apple-intelligence/index.html` (rad 37–39)
- Ändra: `_unpublished/guides/apple-intelligence/styles.css` (rad 23–24)
- Ändra: `_unpublished/sv/guider/apple-intelligence/index.html` (rad 16–18)
- Ändra: `_unpublished/sv/guider/apple-intelligence/styles.css` (rad 23–24)
- Ändra: `scripts/tests/test_fonts.py` (`GUIDE_WEB_SURFACES`)

**Gränssnitt:**
- Konsumerar: inget.
- Producerar: två webbytor som ärver Blueprint ur `/assets/css/tokens.css`, och fyra nya rader i
  `GUIDE_WEB_SURFACES`.

- [ ] **Steg 1: Se vakten röd innan ytorna städas**

Lägg till de fyra sökvägarna i `GUIDE_WEB_SURFACES` **först**:

```python
GUIDE_WEB_SURFACES = (
    "guides/claude/index.html",
    "guides/claude/styles.css",
    "_unpublished/guides/copilot/index.html",
    "_unpublished/guides/copilot/styles.css",
    "_unpublished/guides/gemini-notebook/index.html",
    "_unpublished/guides/gemini-notebook/styles.css",
    # Apple är den första guiden vars SVENSKA webbyta också står här.
    # Frysningen av de svenska ytorna gäller prosan, inte CSS-hygienen:
    # ett typsnittsbyte ändrar noll tecken normaliserad text och syns
    # därför inte i ytkonsistensvakten. Copilots och Geminis svenska
    # ytor bär kvar sina Crestiora-typsnitt och är fortsatt skuld.
    "_unpublished/guides/apple-intelligence/index.html",
    "_unpublished/guides/apple-intelligence/styles.css",
    "_unpublished/sv/guider/apple-intelligence/index.html",
    "_unpublished/sv/guider/apple-intelligence/styles.css",
)
```

```bash
/usr/bin/python3 -m pytest scripts/tests/test_fonts.py -q
```
Förväntat: **4 failed** — `index.html` bär `fonts.googleapis.com`/`fonts.gstatic.com`/`Playfair`,
`styles.css` bär `Playfair` och `'Inter'`. Det här är vakten som bevisar sig själv.

- [ ] **Steg 2: Stryk de tre länkraderna i båda `index.html`**

Ta bort exakt dessa tre rader (EN rad 37–39, SV rad 16–18) och ingenting annat:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

Kvar står de fem lokala arken (`fonts.css`, `tokens.css`, `base.css`, `components.css`,
`styles.css`) — samma uppsättning som den städade Gemini-ytan bär på rad 31–35.

- [ ] **Steg 3: Stryk de två tokenöverskrivningarna i båda `styles.css`**

Rad 23–24 i var fil:

```css
  --font-display: 'Playfair Display', Georgia, serif;
  --font-body:    'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
```

`--font-mono` på rad 25 är neutral och **stannar**. De 16 `font-family: var(--font-*)`-raderna
längre ned är tokenanvändning och rörs inte — de pekar nu på Blueprint i stället för Crestiora.

- [ ] **Steg 4: Kör typsnittsvakten**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_fonts.py -q
```
Förväntat: PASS, noll Crestiora-strängar i de fyra filerna.

- [ ] **Steg 5: Kontrollera att ytornas text inte rört sig**

```bash
git diff --stat _unpublished/guides/apple-intelligence/ _unpublished/sv/guider/apple-intelligence/
```
Förväntat: exakt 4 filer, 10 borttagna rader, 0 tillagda. Rör diffen någon annan rad är det ett
fel — ytkonsistensvakten läser samma filer i Task 5.

- [ ] **Steg 6: Kör hela sviten och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
git add scripts/tests/test_fonts.py _unpublished/guides/apple-intelligence/ _unpublished/sv/guider/apple-intelligence/
git commit -m "style(apple): bort med Crestioras typsnitt ur båda webbytorna, in i typsnittsvakten"
```
Förväntat: 808 passed före commit.

---

### Task 3: Den döda adressen ut ur quick-starten, och PDF:en omrenderad

**Filer:**
- Ändra: `_unpublished/exports/apple-intelligence-quick-start-en.html` (rad 193–196)
- Renderas om: `_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-en.pdf`
- Ändra: `scripts/tests/test_capture_guide_baseline.py` (`RECAPTURED_THIS_ROUND`)
- Skrivs av facitskriptet: `scripts/tests/fixtures/guide-pdf-baseline.json` och kroppstextfacit
- Får inte ändras: `_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf`

**Gränssnitt:**
- Konsumerar: inget.
- Producerar: en levererad EN-quick-start utan båda pekarna — förutsättningen för Task 7:s
  förbudslista.

- [ ] **Steg 1: Mät båda pekarna i den levererade PDF:en**

```bash
/usr/bin/python3 -c "
import sys,pathlib,re; sys.path.insert(0,'scripts')
from tests import pdf_fingerprint as fp
flat=re.sub(r'\s+',' ',fp.extract(fp.ROOT/'_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-en.pdf'))
for n in ['from the same page','/ G U I D E S / A P P L E','download the 25-page premium PDF']:
    print(n, flat.count(n))"
```
Förväntat: `1 1 1`. Adressen står **spärrad** i PDF:en — därav mellanrummen.

- [ ] **Steg 2: Skriv om avslutningen**

Ersätt rad 193–196 i HTML:en:

```html
  <div class="closing">
    <div class="msg">Want depth? The full <em>Apple Intelligence Guide</em> comes with this
      quick start in the community.</div>
  </div>
```

Johans beslut 2026-10-13: **ingen URL och ingen platshållare.** `<div class="url">` tas bort
helt, och prosans *"from the same page"* försvinner med meningen — den var en andra pekare till
samma sida som aldrig kommer att finnas.

- [ ] **Steg 3: Rendera om**

```bash
/usr/bin/python3 exports/build-apple-intelligence-quickstart-pdf.py
```
Byggaren renderar EN **och** SV i samma körning (`jobs`, rad 10–15).

- [ ] **Steg 4: Verifiera att den svenska PDF:en är byte-identisk**

```bash
git status --short _unpublished/assets/pdfs/guides/
```
Förväntat: **bara** `apple-intelligence-quick-start-en.pdf` ändrad.

Står den svenska som ändrad: jämför den mot merge-basen och återställ den —
`git checkout -- _unpublished/assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf` — och
skriv in i ledgern att byggaren inte är deterministisk för SV. Committa den aldrig ändrad: Task
7:s `untouched`-rad jämför bytes mot merge-basen och är röd för en omrenderad orörd yta.

- [ ] **Steg 5: Mät att båda pekarna är borta**

Kör kommandot från steg 1 igen. Förväntat: `0 0 0`.

- [ ] **Steg 6: Se PDF-facit bli rött — och förstå varför**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_pdf_parity.py -q
```
Förväntat: FAIL för `apple-intelligence-quick-start-en.pdf`. Apples fyra PDF:er står i
`pdf_fingerprint.GUIDE_PDFS` och har facit sedan tidigare; en omrendering som inte omfångas är
per definition en paritetsregression. Det här steget får inte hoppas över: ser du inte rött här
har omrenderingen i steg 3 inte gett någon faktisk ändring.

- [ ] **Steg 7: Omfånga EXAKT den omrenderade filen**

```bash
/usr/bin/python3 scripts/tests/fixtures/capture_guide_baseline.py   --only _unpublished/assets/pdfs/guides/apple-intelligence-quick-start-en.pdf
```
`--only` är det enda sättet att omfånga en delmängd utan att slå av vakten för de övriga 21
nycklarna. **Kör aldrig med `--force`** — en `--force`-körning efter en ändring är liktydig med
att stänga av paritetsvakten, och skriptets egen docstring säger det.

- [ ] **Steg 8: Töm och fyll om `RECAPTURED_THIS_ROUND`**

Listan bär i dag en post från premarket-rundan (`gemini-notebook-guide-en.pdf`). Den **töms**,
den fylls inte på — en lista som bara växer slutar vakta något.

```python
RECAPTURED_THIS_ROUND = [
    # Apple-rundan 1, 2026-10-14: quick-starten renderades om när de två
    # pekarna till en sida som aldrig publiceras togs bort. Huvudguiden
    # rördes INTE — prosan står still i runda 1 — så dess tre facitnycklar
    # ska stå under vakten, inte i undantaget.
    "_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-en.pdf",
]
```

- [ ] **Steg 9: Kör facitvakterna**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_capture_guide_baseline.py scripts/tests/test_guide_pdf_parity.py -q
```
Förväntat: PASS. Faller `test_force_cannot_silently_reset_unrelated_entries` har omfångningen
träffat fler nycklar än den namngivna — återställ båda JSON-faciten med
`git checkout -- scripts/tests/fixtures/` och kör om steg 7 med rätt `--only`.

- [ ] **Steg 10: Kör hela sviten och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
git add _unpublished/exports/apple-intelligence-quick-start-en.html         _unpublished/assets/pdfs/guides/apple-intelligence-quick-start-en.pdf         scripts/tests/test_capture_guide_baseline.py scripts/tests/fixtures/
git commit -m "fix(apple): ta bort quick-startens två pekare till en sida som aldrig publiceras"
```
Förväntat: 808 passed.

---

### Task 4: Påståendeinventeringen — en mätning av dagens guide

**Filer:**
- Skapa: `docs/guide-facts-apple-intelligence.md`
- Ändra: `scripts/tests/factinventory.py` (`INVENTORIES`)

**Gränssnitt:**
- Konsumerar: inget.
- Producerar: `factinventory.inventory_path("apple-intelligence")` → filen ovan, och ett
  `guard`-block vars rader Task 5:s ytkonsistensvakt läser. Radformen är
  `ID | språk | värde | status`, där status är `aktiv` eller `borttaget`.

- [ ] **Steg 1: Lägg in sökvägen och se vakten röd**

```python
INVENTORIES = {
    "claude":  ROOT / "docs" / "guide-facts-claude.md",
    "copilot": ROOT / "docs" / "guide-facts-copilot.md",
    "gemini":  ROOT / "docs" / "guide-facts-gemini.md",
    "apple-intelligence": ROOT / "docs" / "guide-facts-apple-intelligence.md",
}
```

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q
```
Förväntat: PASS ännu — `test_every_guide_has_an_inventory_file` parametriseras över
`surfacecheck.GUIDES`, och Apple står inte där förrän Task 5. Sökvägen läggs in här för att
Task 5 ska kunna kartlägga utan att samma commit gör två saker.

- [ ] **Steg 2: Skriv inventeringens huvud**

Följ `docs/guide-facts-gemini.md`:s form. Huvudet ska namnge ytorna och säga vad rundan mäter:

```markdown
# Påståendeinventering — Apple Intelligence-guiden

**Rundan:** Apple Intelligence-guiden, runda 1 (mät och vakta). Spec:
`docs/superpowers/specs/2026-10-14-apple-intelligence-guide-update-design.md`
**Upprättad:** 2026-10-14
**Faktakontrollerad:** 2026-10-14

Ytorna: **EW** `_unpublished/guides/apple-intelligence/index.html` · **EP**
`_unpublished/exports/apple-intelligence-print-a4-en.html` · **QS**
`_unpublished/exports/apple-intelligence-quick-start-en.html`

QS står utanför ytkonsistensvakten med avsikt — quick-starten har egen, kortare
formulering, och kravet "ordagrant på alla ytor" vore rött från dag ett.

Inventeringen är skriven som en **mätning av guiden som den står 2026-10-14**, inte som
en beskrivning av den omskrivna guiden. Varje post bär därför ett **verdikt**:

- `står` — verifierat sant mot primärkälla 2026-10-14
- `föråldrat` — var sant i april 2026, är det inte längre
- `falskt` — var fel redan då

Verdikten är runda 2:s arbetsorder. Källkolumnen bär **primärkälla** (apple.com,
support.apple.com) med hämtdatum; en sekundärkälla räcker aldrig till `står`.
```

- [ ] **Steg 3: Skriv posttabellen**

En rad per volatilt påstående, med id (`A01`, `A02`, …), var det står (EW/EP/QS med antal),
värdet, verdiktet och källan. Utgå från guidens volatila kärna, mätt 2026-10-14:

| id | värde | EW | EP | att verifiera mot primärkälla |
|---|---|---|---|---|
| A01 | `M1 chip or later` | 2 | 1 | Apples systemkrav för Apple Intelligence |
| A02 | `iPhone 15 Pro` | 2 | 3 | samma |
| A03 | `iPad Pro or iPad Air from 2021` | 1 | 1 | samma |
| A04 | `Private Cloud Compute` | 15 | 18 | Apples PCC-sida |
| A05 | `Writing Tools` | 15 | 19 | funktionsnamn i aktuell OS-version |
| A06 | `Visual Intelligence` | 9 | 14 | samma |
| A07 | `Mail categorisation` | 9 | 10 | samma |
| A08 | `Image Playground` | 1 | 3 | samma |
| A09 | `Genmoji` | 1 | 3 | samma |
| A10 | `Siri 2.0` | 3 | 7 | **namnet är pensionerat** — verifiera vad assistenten heter i dag |
| A11 | `ChatGPT` | 27 | 39 | om ChatGPT fortfarande är den enda externa vägen |
| A12 | `OpenAI` | 12 | 11 | samma |
| A13 | `April 2026` | 3 | 3 | stämpeln, inte ett produktpåstående |
| A14 | `Data Protection Impact Assessment` | 1 | 1 | står (juridisk term, inte produktfakta) |

**`IMY` får ingen `aktiv`-rad.** Den är mätt till EP:1 / EW:0 — ytorna divergerar redan där, och
en `aktiv`-rad vore `saknas_på_en_yta` från första sekunden. Skriv in divergensen i prosan i
stället, som en observation runda 2 ärver.

Lägg till de poster mätningen hittar utöver tabellen ovan. Tabellen är golvet, inte taket.

- [ ] **Steg 4: Skriv `guard`-blocket**

```
```guard
# Engelska ytorna: EW `_unpublished/guides/apple-intelligence/index.html` (web)
# + EP `_unpublished/exports/apple-intelligence-print-a4-en.html` (print).
# QS står utanför vakten med avsikt och bevakas av test_guide_delivery.py.
#
# Varje rad är MÄTT mot båda ytorna med vaktens egen normalisering:
# `aktiv` står ordagrant på båda, `borttaget` på ingen. Ingen rad är ärvd
# från planen utan att mätas om.
#
# INGEN RAD PÅ `IMY`: EP:1 / EW:0, alltså `saknas_på_en_yta` från start.
# Divergensen står i prosan ovan och är runda 2:s sak.
A01 | en | M1 chip or later | aktiv
A02 | en | iPhone 15 Pro | aktiv
A03 | en | iPad Pro or iPad Air from 2021 | aktiv
A04 | en | Private Cloud Compute | aktiv
A05 | en | Writing Tools | aktiv
A06 | en | Visual Intelligence | aktiv
A07 | en | Mail categorisation | aktiv
A08 | en | Image Playground | aktiv
A09 | en | Genmoji | aktiv
A10 | en | Siri 2.0 | aktiv
A11 | en | ChatGPT | aktiv
A12 | en | OpenAI | aktiv
A13 | en | April 2026 | aktiv
A14 | en | Data Protection Impact Assessment | aktiv
# Raderna ovan är mätta på BÅDA engelska ytorna 2026-10-14 och är
# `aktiv` därför att de står där i dag — inte därför att de är sanna.
# Verdikten (står/föråldrat/falskt) bor i posttabellen; vaktblocket
# mäter bara förekomst. Runda 2 flyttar de föråldrade till `borttaget`.
```
```

- [ ] **Steg 5: Verifiera varje rad mot båda ytorna innan den skrivs in**

```bash
/usr/bin/python3 -c "
import sys,re,html,pathlib; sys.path.insert(0,'scripts')
from tests import surfacecheck, factinventory
def text(rel):
    s=(surfacecheck.ROOT/rel).read_text(encoding='utf-8')
    s=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S)
    return surfacecheck.normalise(html.unescape(re.sub(r'<[^>]+>',' ',s)))
rows=factinventory.load(factinventory.inventory_path('apple-intelligence'))
surfaces={('en','web'):text('_unpublished/guides/apple-intelligence/index.html'),
          ('en','print'):text('_unpublished/exports/apple-intelligence-print-a4-en.html')}
for p in surfacecheck.check(rows, surfaces): print(p.kind, p.detail)"
```
Förväntat: ingen utskrift. Varje rad som skriver ut `saknas_på_en_yta` eller `finns_ingenstans`
ska **tas bort eller rättas**, aldrig lämnas kvar — Task 5 gör den röd annars.

- [ ] **Steg 6: Committa**

```bash
git add -f docs/guide-facts-apple-intelligence.md
git add scripts/tests/factinventory.py
git commit -m "docs(apple): påståendeinventering som mätning av dagens guide, med verdikt per post"
```

---

### Task 5: Ytkartan, den opublicerade listan och skuldlistan — i samma commit

**Filer:**
- Ändra: `scripts/tests/surfacecheck.py` (`GUIDE_SURFACES`)
- Ändra: `scripts/tests/test_guide_surface_consistency.py` (`UNPUBLISHED_GUIDES`, `UNMAPPED_GUIDE_SURFACES`)

**Gränssnitt:**
- Konsumerar: `factinventory.inventory_path("apple-intelligence")` från Task 4.
- Producerar: `surfacecheck.surfaces_for("apple-intelligence")` → fyra ytor, och
  `surfacecheck.GUIDES` med fyra namn — vilket Task 6 och 7 inte behöver, men Task 8:s filsvep gör.

**De tre ändringarna hör ihop och ska göras tillsammans.** Kartläggs Apple utan att
`UNPUBLISHED_GUIDES` fylls blir `test_every_unpublished_guide_is_in_the_surface_map` röd
(mängden härleds ur kartan och jämförs med **set-likhet**). Kartläggs den utan att skuldlistan
töms blir `test_the_debt_list_cannot_rot` röd (en post som står både på listan och i kartan är
en betald skuld som ser obetald ut).

- [ ] **Steg 1: Lägg Apple i ytkartan**

```python
    # Apple Intelligence ligger under _unpublished/ av samma skäl som
    # Copilot och Gemini: GitHub Pages serverar inte kataloger som börjar
    # med understreck. De svenska ytorna står med fast runda 1 bara rör
    # deras typsnitt — de FINNS, och en svensk vaktrad ska jämföras mot
    # dem och inte mot ingenting. Att de divergerar i sak från de engelska
    # efter runda 2 är ett känt läge (spec §1), inte något vakten ska dölja.
    "apple-intelligence": {
        ("en", "web"):   "_unpublished/guides/apple-intelligence/index.html",
        ("en", "print"): "_unpublished/exports/apple-intelligence-print-a4-en.html",
        ("sv", "web"):   "_unpublished/sv/guider/apple-intelligence/index.html",
        ("sv", "print"): "_unpublished/exports/apple-intelligence-print-a4-sv.html",
    },
```

- [ ] **Steg 2: Fyll den opublicerade listan och töm skuldlistan**

```python
UNPUBLISHED_GUIDES = ("copilot", "gemini", "apple-intelligence")
```

Ta bort hela posten `"_unpublished/guides/apple-intelligence/index.html": "…"` ur
`UNMAPPED_GUIDE_SURFACES`. Kvar står elevguiden ensam — behåll dess skäl ordagrant, men stryk
ledet *"samma skäl som apple-intelligence"* och skriv ut skälet i egen rätt, annars pekar
listan på en post som inte finns.

- [ ] **Steg 3: Kör ytvakterna**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q
```
Förväntat: PASS, med fyra nya parametriseringar (en per Apple-yta i inventeringsvakten och
konsistensvakten).

- [ ] **Steg 4: Bryt vakten med flit, i en engångsworktree**

```bash
git worktree add /tmp/apple-probe-5 HEAD && cd /tmp/apple-probe-5
```
Prova två sabotage, kör `test_guide_surface_consistency.py` efter vart och ett:
1. Lägg tillbaka Apple-posten i `UNMAPPED_GUIDE_SURFACES` → förväntat FAIL i
   `test_the_debt_list_cannot_rot` med *"står på skuldlistan OCH i ytkartan"*.
2. Ta bort `"apple-intelligence"` ur `UNPUBLISHED_GUIDES` → förväntat FAIL i
   `test_every_unpublished_guide_is_in_the_surface_map` med *"saknas"*.

```bash
cd - && git worktree remove --force /tmp/apple-probe-5
```
Går något av sabotagen **grönt** är vakten blind — skriv det i ledgern och stanna.

- [ ] **Steg 5: Kör hela sviten och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
git add scripts/tests/surfacecheck.py scripts/tests/test_guide_surface_consistency.py
git commit -m "test(apple): kartlägg fyra ytor, fyll den opublicerade listan, töm skuldlistans post"
```

---

### Task 6: TOC-kartan för Apple

**Filer:**
- Ändra: `scripts/tests/test_guide_toc.py` (`GUIDE_TOC`)

**Gränssnitt:**
- Konsumerar: Task 1:s ankarkonvention.
- Producerar: `config_for("apple-intelligence")`.

- [ ] **Steg 1: Skriv in kartan**

Alla fem ankare är verifierade 2026-10-14 mot
`_unpublished/assets/pdfs/guides/apple-intelligence-guide-en.pdf`: var och en träffar på exakt
en sida, och det är avsnittets startsida. Inget ankare bär produktnamn, pris eller datum.

```python
    # Apple Intelligence: fem rader, fem ankare, alla verifierade mot den
    # renderade PDF:en 2026-10-14. Ankarna är valda ur pdftotext-utskriften
    # och är fria från produktnamn, pris och datum — runda 2 skriver om
    # prosan och ska byta ankare EN gång, mot den omrenderade PDF:en, inte
    # jaga sprödhet den här rundan införde.
    "apple-intelligence": {
        "template": "_unpublished/exports/apple-intelligence-print-a4-en.html",
        "pdf": "_unpublished/assets/pdfs/guides/apple-intelligence-guide-en.pdf",
        "toc_page": 2,
        "anchors": {
            "Part 1 · Get started":
                "If that menu item appears at all, your device is compatible",
            "Part 2 · Work smarter":
                "it is a menu option that appears when you select text",
            "Part 3 · The GDPR angle":
                "What stays on your device",
            "FAQ":
                "Ten of the questions that come up most often",
            "About this guide":
                "You may copy, share, and adapt this material for non-commercial purposes",
        },
    },
```

- [ ] **Steg 2: Kör TOC-vakten**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_toc.py -q -k apple
```
Förväntat: 7 passed — fem sidnummerrader plus radvakten och ankarvakten.

- [ ] **Steg 3: Bevisa att en tom ankarlista blir röd**

I en engångsworktree, sätt `"anchors": {}` för Apple och kör samma kommando.
Förväntat: FAIL i `test_every_guide_in_the_toc_map_has_anchors_for_every_row` med
*"ankarlistan är tom"*. Blir det i stället **grönt med färre tester** är vakten blind —
stanna och skriv det i ledgern.

- [ ] **Steg 4: Bevisa att ett fel sidnummer blir rött**

I samma worktree, ändra FAQ-radens `<span class="toc__page">24</span>` till `23` i mallen
`_unpublished/exports/apple-intelligence-print-a4-en.html`, och kör. Förväntat: FAIL med *"förteckningen säger 23, avsnittet börjar på 24"*.
Riv worktreen.

- [ ] **Steg 5: Kör hela sviten och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
git add scripts/tests/test_guide_toc.py
git commit -m "test(apple): TOC-karta med fem verifierade ankare"
```

---

### Task 7: Leveranskartan — förbudslista och orörda ytor

**Filer:**
- Ändra: `scripts/tests/test_guide_delivery.py` (`GUIDE_DELIVERY`)

**Gränssnitt:**
- Konsumerar: Task 3:s omrenderade quick-start.
- Producerar: `delivery_for("apple-intelligence")`.

- [ ] **Steg 1: Skriv in kartan**

```python
    "apple-intelligence": {
        "pdfs": (
            "_unpublished/assets/pdfs/guides/apple-intelligence-guide-en.pdf",
            "_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-en.pdf",
        ),
        # Runda 1:s lista förbjuder BARA strängar de levererade PDF:erna
        # redan är fria från. Guiden bär `Swedish`, `IMY`, `Schrems` och
        # `Siri 2.0` legitimt — de är sanna påståenden om en guide som ännu
        # inte är omskriven, och att förbjuda dem nu vore att göra billigaste
        # vägen till grönt att stryka innehåll. De läggs till i runda 2, vid
        # omrenderingen.
        #
        # De tre första raderna är den döda adressen, mätt i `_flat()`-form:
        # pdftotext spärrar versaler, så URL:en står som
        # `/ G U I D E S / A P P L E - I N T E L L I G E N C E` i utskriften
        # och en needle skriven som vanlig URL hade aldrig matchat.
        "forbidden": (
            "/ G U I D E S / A P P L E",
            "from the same page",
            "download the 25-page premium PDF",
            "Skolverket",
            "NotebookLM",
            "Copilot",
        ),
        # Båda byggarna renderar EN *och* SV i samma körning, så de svenska
        # filerna skrivs varje gång de engelska renderas om. Raden jämför
        # bytes mot merge-basen.
        "untouched": (
            "_unpublished/assets/pdfs/guides/apple-intelligence-guide-sv.pdf",
            "_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf",
        ),
    },
```

- [ ] **Steg 2: Kör leveransvakten**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_delivery.py -q
```
Förväntat: PASS. Faller `test_the_delivered_pdfs_carry_no_abandoned_claim` på
`/ G U I D E S / A P P L E` är Task 3:s omrendering inte committad — gå tillbaka dit.

- [ ] **Steg 3: Bevisa att sidantalsvakten täcker Apple**

`test_every_quick_starts_page_count_claim_matches_its_rendered_main_guide` härleder talet ur den
renderade huvudguiden. Quick-starten säger `25-page` och guiden är 25 sidor i dag.

I en engångsworktree, ändra quick-startens HTML till `26-page`, rendera om och kör vakten.
Förväntat: FAIL. Riv worktreen.

- [ ] **Steg 4: Kör hela sviten och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
git add scripts/tests/test_guide_delivery.py
git commit -m "test(apple): leveranskarta med den döda adressen som förbudssträng"
```

---

### Task 8: Helgranskning av grenen

**Filer:** inga ändras, om granskningen inte hittar något.

- [ ] **Steg 1: Mät sviten i en ORÖRD utcheckning**

```bash
git worktree add /tmp/apple-verify HEAD && cd /tmp/apple-verify
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
```
Förväntat: **808 passed + de nya raderna**, 0 failed. Mät aldrig i arbetsträdet: en
`cp`-återställning som inte bet ger en laddad modul med sabotaget kvar och ett `git status` som
säger rent. Det kostade en utredning 2026-10-13.

- [ ] **Steg 2: Filsvep över grenen**

```bash
git diff --name-only main...HEAD | sed 's|/.*||' | sort | uniq -c
```
Förväntat: bara `_unpublished`, `docs`, `scripts`. Står något annat där har rundan rört sajten —
stanna och rapportera.

- [ ] **Steg 3: Kontrollera att ingenting publicerat ändrats**

```bash
git diff --name-only main...HEAD | grep -v "^_unpublished/\|^docs/\|^scripts/\|^exports/" || echo "inget publicerat rört"
```
Förväntat: `inget publicerat rört`.

- [ ] **Steg 4: Kontrollera de fyra kartorna**

```bash
/usr/bin/python3 -c "
import sys; sys.path.insert(0,'scripts')
from tests import surfacecheck, factinventory
from tests.test_guide_toc import GUIDE_TOC
from tests.test_guide_delivery import GUIDE_DELIVERY
from tests.test_guide_surface_consistency import UNPUBLISHED_GUIDES, UNMAPPED_GUIDE_SURFACES
g='apple-intelligence'
print('ytkartan      ', g in surfacecheck.GUIDES)
print('inventeringen ', g in factinventory.INVENTORIES, factinventory.inventory_path(g).exists())
print('toc-kartan    ', g in GUIDE_TOC)
print('leveransen    ', g in GUIDE_DELIVERY)
print('opublicerade  ', g in UNPUBLISHED_GUIDES)
print('skuldlistan   ', [k for k in UNMAPPED_GUIDE_SURFACES])"
```
Förväntat: fem `True`, och skuldlistan med **bara** elevguiden kvar.

- [ ] **Steg 5: Riv worktreen och kopiera ut ledgern**

```bash
cd - && git worktree remove --force /tmp/apple-verify
cp -R .superpowers/sdd/*apple* ~/Desktop/choosewise-apple-runda-1/
```
`.superpowers/` är gitignorerad och överlever inte leveransen. Gemini-rundans ledger med 86
rulings räddades på det här sättet; Copilot-rundans gjorde det inte.

- [ ] **Steg 6: Rapportera till Johan**

Rapporten ska bära: svitens tal ur den **orörda** utcheckningen, filsvepets utfall, vilka vakter
som bevisats röda och hur, inventeringens antal poster fördelade på `står` / `föråldrat` /
`falskt` — och den listan är runda 2:s arbetsorder. Pusha inte och öppna ingen PR utan Johans
klartecken.
