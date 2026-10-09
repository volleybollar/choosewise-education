# Copilot-guiden, aktuell och internationell: implementationsplan

> **För agentiska arbetare:** OBLIGATORISK SUB-SKILL: använd superpowers:subagent-driven-development (rekommenderad) eller superpowers:executing-plans för att genomföra planen uppgift för uppgift. Stegen är kryssrutor (`- [ ]`) för spårning.

**Mål:** De två engelska Copilot-PDF:erna levereras till Skool-communityt, faktamässigt sanna per oktober 2026 och skrivna för en engelskspråkig skolvärld i stället för en svensk — utan att något publiceras på sajten.

**Arkitektur:** Samma ryggrad som våg 2b. En numrerad påståendeinventering (`docs/guide-facts-copilot.md`) upprättas och faktakontrolleras **innan** en enda guideyta rörs. Vaktlagret från våg 2b görs guide-agnostiskt så att samma vakt bevakar både Claude och Copilot. Därefter redigeras de två engelska ytorna parvis — aldrig en i taget — PDF:erna renderas om, och facit omfångas selektivt med `--only`.

**Teknikstack:** `/usr/bin/python3` (3.9.6 — enda interpretern med pytest, playwright och Pillow), pytest, Playwright för PDF-rendering, `pdftotext`/`pdftoppm` (poppler) för textextraktion och sidbilder.

**Spec:** `docs/superpowers/specs/2026-10-09-copilot-guide-international-design.md`

**Gren:** `feat/copilot-guide-international`, från `main` (HEAD `61a4b07`, svit **752 passed, 0 skipped** på 55 s — verifierat 2026-10-09 innan planen skrevs).

---

## Globala villkor

- **`git add -A` används aldrig.** Repot har ~30 ocommittade filer under `exports/` och `assets/pdfs/wise/` som tillhör Johan. Namnge varje fil i varje `git add`.
- **`git checkout --` körs aldrig på en katalog.** Det raderade två av Johans filer i våg 2a. På **namngiven fil** är det tillåtet och används i Task 10 för att återställa de två svenska PDF:erna.
- **Interpretern är `/usr/bin/python3`** (3.9.6). Ingen `dict | dict`; använd `{**a, **b}`. `list[str]` i annoteringar kräver `from __future__ import annotations`.
- **Ingenting publiceras.** Inga poster i `guides-en.json`, ingen PAIR_MAP, ingen sitemap, inga og-kort, landningssidans *"in preparation"* står kvar. Allt arbete ligger under `_unpublished/`, plus testfiler, inventeringen och överlämningen.
- **De svenska ytorna rörs inte.** `_unpublished/exports/copilot-print-a4-sv.html`, `_unpublished/exports/copilot-quick-start-sv.html` och `_unpublished/sv/guider/copilot/` lämnas som de står, och deras PDF:er ska vara **byte-identiska** när rundan är klar.
- **Layouten rörs inte.** Omslaget behåller sitt navyformat och sina tre piller, sidfoten sin vänsterställning. Endast text ändras — plus att webbsidans `reader-responsibility-note` byter till den befintliga `processing-callout`-komponenten, vilket inte är en ny stil utan en komponent som redan används sex gånger på samma sida.
- **Paletten och typografin rörs inte.** Enda typografiändringen är att Google Fonts-raderna och de två `--font-*`-överskrivningarna tas bort, så att sidan ärver Blueprints `tokens.css` i stället för Crestioras Playfair/Inter.
- **En faktamening utan post i inventeringen får inte skrivas.** Ärvs från våg 2b, gäller utan undantag.
- **Ett fynd som inte behöver ändras stryks aldrig tyst.** Det står kvar i tabellen med en motivering.
- **Varje post bär källa, hämtdatum och vilken källa.** Rå HTML och lokal textextraktion; en sammanfattning är aldrig källa till ett värde.
- **Inga enskilda lagar eller myndigheter namnges** i de engelska ytorna — det är gränsen mellan väg A och väg C. "Data controller" används som allmän yrkesterm, inte som hänvisning till en namngiven förordning. GDPR, Schrems II, EU Data Boundary, Skolverket och IMY ut ur brödtexten. **Undantag:** "EU Data Boundary" är ett *produktnamn* hos Microsoft; där det måste nämnas som produktfunktion (data residency) är det tillåtet, men aldrig som rättslig analys. Varje sådan förekomst får en post i inventeringen med motiveringen utskriven.
- **CTA:n pekar på choosewise.education, inte på svensk konsultverksamhet.** Johans engelskspråkiga hatt är choosewise.education (CLAUDE.md §2). Meningen *"I offer consulting for schools, primarily in Sweden."* stryks och ersätts enligt Task 7. **Antagande som Johan får korrigera när han läser planen:** CTA:n säljer inte Johans tid i den här guiden, den pekar läsaren till choosewise.education och till communityt.
- **Quick-starten står utanför ytkonsistensvakten** — avsiktligt, enligt spec §7. Den bevakas i stället av inventeringens förekomstkolumn, av PDF-vakterna, och av leveransvakten i Task 2.
- **Sifferutfallen i stegen är räknade, inte mätta.** De utgår från `main`:s 752 och de tester planen lägger till; lägger du till ett test till räknar du om. Det som är bindande är **0 skipped och 0 xfailed i Task 14**, och att inget test-id från `main` har försvunnit.
- **Prosa som beror på en källa skrivs inte i planen.** Där formuleringen är avgjord — omslaget, jurisdiktionsrutan, CTA:n, quick-startens sista mening — står den ordagrant här. Där meningen bär ett faktavärde står i stället vad den ska säga och vilken post som belägger den, eftersom en förskriven faktamening vore ett värde utan källa, och spec §6:s första regel förbjuder exakt det.
- **Tio av 22 PDF:er är inte byte-identiska vid omrendering.** Skillnaden är Chromiums `CreationDate`/`ModDate`. En omrendering visar alltid ändrade filer även när innehållet är oförändrat — det är inte ett fynd.

### Rättelse av specen, inskriven med avsikt

Spec §2 svarar **"Nej — noll `toc-page-num`"** på frågan om innehållsförteckningen har hårdkodade sidnummer. **Det är fel.** Mätningen letade efter Claude-guidens klassnamn. Copilots print har sex hårdkodade sidnummer i klassen `toc__page` (`exports/copilot-print-a4-en.html` rad 607–657), **och en av dem är redan fel i dag:** innehållsförteckningen säger att FAQ:n står på sidan 23, men i den renderade PDF:en står den på 24 (verifierat med `pdftotext -f 24 -l 24` 2026-10-09; sidan 23 är "Five policy decisions"). Fällan gäller alltså den här rundan, och Task 11 äger den.

---

## Granskningsfokus

Fem fel som specen förutsätter men som ingen uppgifts tester annars skulle fånga. Varje rad har fått sitt test inlagt i den uppgift som äger koden.

1. **HTML-entiteter gör vakten falskt röd.** Copilots rubriker innehåller `&amp;` ("Compliance &amp; licensing"). En vaktrad skriven med `&` jämförs i dag mot markupens `&amp;` och blir röd utan att något är fel — eller, värre, en redaktör skriver om raden till `&amp;` och vakten slutar beskriva det läsaren ser. → Task 1, `test_comparison_unescapes_html_entities`.
2. **PDF:en är leveransen, men varje vakt läser HTML.** Rättas HTML:en utan att PDF:en renderas om går hela sviten grön medan filen som går till Skool fortfarande säger "Swedish schools" och "April 2026". → Task 2, `test_the_delivered_pdfs_carry_no_swedish_framing`.
3. **Quick-starten står utanför ytvakten och kan tappas tyst.** Den är en tredje yta utan motpart; inget i våg 2b:s vaktlager ser den. → Task 2, `test_the_quick_start_pdf_is_part_of_the_delivery_guard`.
4. **En okänd guide ger en tyst grön vakt.** Skrivs `read_surfaces("gemini")` eller en inventering som inte finns, ska det bli ett högljutt fel med de kända guiderna namngivna — inte en tom ytkarta som inte kan hitta något fel. → Task 1, `test_an_unknown_guide_is_a_loud_error` och `test_every_guide_has_an_inventory_file`.
5. **Ytkartan pekar på en publicerad fil för en opublicerad guide.** Copilots fyra ytor ligger under `_unpublished/`; en felskriven sökväg mot `guides/copilot/` skulle läsa en fil som inte finns eller, om den en dag publiceras, den fel. → Task 1, `test_copilot_surfaces_are_the_unpublished_ones`.

---

## Filstruktur

| Fil | Ansvar | Uppgift |
|---|---|---|
| `scripts/tests/surfacecheck.py` | ytkartan per guide, normalisering | Task 1 |
| `scripts/tests/factinventory.py` | inventeringssökväg per guide, parsern | Task 1 |
| `scripts/tests/test_guide_surface_consistency.py` | ytvakten, nu parametriserad över guiderna | Task 1 |
| `scripts/tests/test_copilot_delivery.py` | **ny** — leveransvakten: de två engelska PDF:erna är fria från svenskramning | Task 2 |
| `docs/guide-facts-copilot.md` | **ny** — påståendeinventeringen med vaktblocket | Task 1 (skelett), 3 (poster), 4 (fakta), 10 (vaktrader) |
| `_unpublished/exports/copilot-print-a4-en.html` | källan till huvud-PDF:en — den egentliga leveransen | Task 5–9, 11 |
| `_unpublished/guides/copilot/index.html` | webbytan, hålls i sak synkad med printytan | Task 5–9 |
| `_unpublished/guides/copilot/styles.css` | typsnittsöverskrivningarna tas bort | Task 5 |
| `_unpublished/exports/copilot-quick-start-en.html` | källan till quick-start-PDF:en, går också till Skool | Task 9 |
| `_unpublished/assets/pdfs/guides/copilot-guide-en.pdf` | leverans | Task 10, 11 |
| `_unpublished/assets/pdfs/guides/copilot-quick-start-en.pdf` | leverans | Task 10 |
| `scripts/tests/fixtures/guide-pdf-baseline.json` | facit per sida, två nycklar omfångas | Task 12 |
| `scripts/tests/fixtures/guide-pdf-body-baseline.json` | facit per dokument, två nycklar omfångas | Task 12 |
| `docs/blueprint-handoff.md` | programöverlämningen, inklusive det svenska divergensläget | Task 13 |

---

# FÖRE GRINDEN — ingen guideyta rörs

## Task 1: Vaktlagret blir guide-agnostiskt

**Filer:**
- Modifiera: `scripts/tests/surfacecheck.py`
- Modifiera: `scripts/tests/factinventory.py`
- Modifiera: `scripts/tests/test_guide_surface_consistency.py`
- Skapa: `docs/guide-facts-copilot.md` (skelett med tomt vaktblock)
- Test: `scripts/tests/test_guide_surface_consistency.py`, `scripts/tests/test_factinventory.py`

**Gränssnitt:**
- Förbrukar: `factinventory.Row` (oförändrad NamedTuple: `id`, `lang`, `value`, `status`), `surfacecheck.check(rows, surfaces)` (oförändrad), `surfacecheck.normalise(text)`.
- Producerar:
  - `surfacecheck.GUIDE_SURFACES: dict[str, dict[tuple[str, str], str]]` — nyckel `"claude"` / `"copilot"`, värde den gamla `SURFACES`-formen.
  - `surfacecheck.GUIDES: tuple[str, ...]` — `("claude", "copilot")`, det testerna parametriserar över.
  - `surfacecheck.surfaces_for(guide: str) -> dict` — höjer `KeyError` med kända guider namngivna.
  - `surfacecheck.read_surfaces(guide: str, root: Path = ROOT) -> dict` — **`guide` är obligatorisk**, inget Claude-standardvärde.
  - `factinventory.INVENTORIES: dict[str, Path]` och `factinventory.inventory_path(guide: str) -> Path`.
  - `factinventory.load(path: Path) -> list[Row]` — **`path` är obligatorisk**; `INVENTORY`-konstanten tas bort.

Det gamla `SURFACES` och `INVENTORY` försvinner. Båda var hårdkodade till Claude, och ett standardvärde som pekar på en guide är precis den hårdkodning den här uppgiften tar bort.

- [ ] **Steg 1: Skriv de misslyckade testerna**

Lägg till i `scripts/tests/test_guide_surface_consistency.py` (de befintliga tolv testerna står kvar; de fem sista ändras i steg 5):

```python
def test_comparison_unescapes_html_entities():
    """Granskningsfokus 1: Copilots rubriker bär `&amp;`. En vaktrad
    skriven som läsaren ser den ska matcha markupen, inte tvingas skriva
    om sig till entiteten."""
    assert surfacecheck.normalise("Compliance &amp; licensing") == \
           surfacecheck.normalise("Compliance & licensing")
    assert surfacecheck.normalise("13&nbsp;+") == surfacecheck.normalise("13 +")


def test_an_unknown_guide_is_a_loud_error():
    """Granskningsfokus 4: en guide som inte finns får inte ge en tom
    ytkarta — då vaktar vakten ingenting och är grön för det."""
    with pytest.raises(KeyError) as exc:
        surfacecheck.surfaces_for("gemini")
    assert "claude" in str(exc.value) and "copilot" in str(exc.value)

    with pytest.raises(KeyError) as inv_exc:
        factinventory.inventory_path("gemini")
    assert "claude" in str(inv_exc.value) and "copilot" in str(inv_exc.value)


@pytest.mark.parametrize("guide", surfacecheck.GUIDES)
def test_every_guide_has_an_inventory_file(guide):
    """Granskningsfokus 4, andra halvan: en guide i ytkartan utan
    inventering kan aldrig få en vaktrad, och vakten vore tyst om det."""
    assert factinventory.inventory_path(guide).exists()


@pytest.mark.parametrize("guide", surfacecheck.GUIDES)
def test_every_guide_surface_file_exists(guide):
    for (lang, where), rel in surfacecheck.surfaces_for(guide).items():
        assert (surfacecheck.ROOT / rel).is_file(), f"{guide} {lang}/{where}: {rel} saknas"


def test_copilot_surfaces_are_the_unpublished_ones():
    """Granskningsfokus 5: Copilot ligger i `_unpublished/`, som Pages
    inte serverar. Pekar kartan på `guides/copilot/` läser vakten en fil
    som inte finns — eller en dag den fel."""
    rels = list(surfacecheck.surfaces_for("copilot").values())
    assert len(rels) == 4
    assert all(rel.startswith("_unpublished/") for rel in rels), rels


def test_claudes_forbidden_list_is_not_empty():
    """De parametriserade vakterna nedan hoppar över en guide vars
    vaktblock är tomt, så att Copilot kan vara tom fram till Task 10.
    Claudes block är fyllt sedan våg 2b och får inte tömmas i skydd av
    den skip:en."""
    rows = factinventory.load(factinventory.inventory_path("claude"))
    assert [r for r in rows if r.status == "borttaget"]
```

- [ ] **Steg 2: Kör dem och se dem misslyckas**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -v`
Förväntat: FAIL — `AttributeError: module 'surfacecheck' has no attribute 'GUIDES'` vid insamlingen (parametriseringen läses vid import, så hela filen faller). Det är rätt sorts rött: kartan finns inte än.

- [ ] **Steg 3: Gör `surfacecheck` guide-agnostisk**

```python
# scripts/tests/surfacecheck.py — ersätt SURFACES-blocket
import html

GUIDE_SURFACES = {
    "claude": {
        ("en", "web"):   "guides/claude/index.html",
        ("en", "print"): "exports/claude-print-a4-en.html",
        ("sv", "web"):   "sv/guider/claude/index.html",
        ("sv", "print"): "exports/claude-print-a4-sv.html",
    },
    # Copilot ligger under _unpublished/ — GitHub Pages serverar inte
    # kataloger som börjar med understreck, verifierat 2026-10-09 (404 på
    # alla fyra utkastkataloger). De svenska ytorna står med i kartan fast
    # rundan inte rör dem: de FINNS, och en svensk vaktrad ska jämföras mot
    # dem och inte mot ingenting. Att de divergerar i sak från de engelska
    # är ett känt läge (spec §5), inte något vakten ska dölja.
    "copilot": {
        ("en", "web"):   "_unpublished/guides/copilot/index.html",
        ("en", "print"): "_unpublished/exports/copilot-print-a4-en.html",
        ("sv", "web"):   "_unpublished/sv/guider/copilot/index.html",
        ("sv", "print"): "_unpublished/exports/copilot-print-a4-sv.html",
    },
}
GUIDES = tuple(GUIDE_SURFACES)


def surfaces_for(guide: str) -> dict:
    try:
        return GUIDE_SURFACES[guide]
    except KeyError:
        raise KeyError(
            f"okänd guide {guide!r}, kända: {sorted(GUIDE_SURFACES)}"
        ) from None
```

Och i `normalise`, före dash-översättningen — entiteterna först, annars översätts `&ndash;` aldrig till ett streck som sedan blir bindestreck:

```python
def normalise(text: str) -> str:
    text = html.unescape(text)
    text = unicodedata.normalize("NFKC", text).translate(_DASHES)
    return re.sub(r"\s+", " ", text).strip()
```

`read_surfaces` tar guiden:

```python
def read_surfaces(guide: str, root: Path = ROOT) -> dict:
    out = {}
    for key, rel in surfaces_for(guide).items():
        raw = (root / rel).read_text(encoding="utf-8")
        out[key] = normalise(_TAG.sub(" ", _SCRIPT.sub(" ", raw)))
    return out
```

- [ ] **Steg 4: Gör `factinventory` guide-agnostisk**

```python
# scripts/tests/factinventory.py — ersätt INVENTORY-konstanten
INVENTORIES = {
    "claude":  ROOT / "docs" / "guide-facts-claude.md",
    "copilot": ROOT / "docs" / "guide-facts-copilot.md",
}


def inventory_path(guide: str) -> Path:
    try:
        return INVENTORIES[guide]
    except KeyError:
        raise KeyError(
            f"okänd guide {guide!r}, kända: {sorted(INVENTORIES)}"
        ) from None
```

och signaturen:

```python
def load(path: Path) -> list:
    text = path.read_text(encoding="utf-8")
```

Resten av `load` är oförändrad.

- [ ] **Steg 5: Parametrisera de tre "verkliga" testerna**

Ersätt de tre sista testerna i `test_guide_surface_consistency.py` med dessa. Notera att `load()` nu kräver en sökväg på alla tre ställen.

```python
def _rows(guide: str, status: str) -> list:
    return [r for r in factinventory.load(factinventory.inventory_path(guide))
            if r.status == status]


@pytest.mark.parametrize("guide", surfacecheck.GUIDES)
def test_the_real_inventory_parses_and_the_real_surfaces_agree(guide):
    rows = _rows(guide, "aktiv")
    if not rows:
        pytest.skip(f"{guide}: vaktblocket har inga aktiv-rader — fylls i Task 10")
    problems = surfacecheck.check(rows, surfacecheck.read_surfaces(guide))
    assert not problems, "\n".join(
        f"{p.id} [{p.lang}] {p.kind}: {p.detail}" for p in problems)


@pytest.mark.parametrize("guide", surfacecheck.GUIDES)
def test_the_real_forbidden_list_is_absent_from_the_real_surfaces(guide):
    rows = _rows(guide, "borttaget")
    if not rows:
        pytest.skip(f"{guide}: vaktblocket har inga borttaget-rader — fylls i Task 10")
    problems = surfacecheck.check(rows, surfacecheck.read_surfaces(guide))
    assert not problems, "\n".join(
        f"{p.id} [{p.lang}] {p.kind}: {p.detail}" for p in problems)


@pytest.mark.parametrize("guide", surfacecheck.GUIDES)
def test_the_real_forbidden_list_would_catch_a_reintroduction(guide):
    """Fälla 2: en vakt som inte setts bli röd vaktar ingenting. Här
    skrivs ett verkligt struket påstående tillbaka i en kopia av den
    verkliga engelska webbytan, och bara det id:t ska bli rött.

    Offret är den kortaste engelska förbudsraden, inte ett hårdkodat id —
    annars måste varje ny guide redigera testet. Precondition-assert:en
    håller valet ärligt, för innehåller offrets värde en annan förbudsrad
    blir två id:n röda och likhetsjämförelsen vore fel krav."""
    rows = [r for r in _rows(guide, "borttaget") if r.lang == "en"]
    if not rows:
        pytest.skip(f"{guide}: inga engelska borttaget-rader — fylls i Task 10")
    victim = min(rows, key=lambda r: len(r.value))
    needle = surfacecheck.normalise(victim.value)
    assert not [r for r in rows
                if r.id != victim.id
                and surfacecheck.normalise(r.value) in needle], \
        f"{victim.id}:s värde innehåller en annan förbudsrad — välj ett annat offer"

    surfaces = dict(surfacecheck.read_surfaces(guide))
    surfaces[("en", "web")] += " " + victim.value
    problems = surfacecheck.check(rows, surfaces)
    assert [(p.id, p.lang, p.kind) for p in problems] == \
           [(victim.id, "en", "återinfört")]
```

- [ ] **Steg 6: Skapa inventeringens skelett**

```bash
cat > docs/guide-facts-copilot.md <<'DOC'
# Påståendeinventering — Copilot-guiden

**Rundan:** Copilot-guiden, internationell omriktning. Spec: `docs/superpowers/specs/2026-10-09-copilot-guide-international-design.md`
**Upprättad:** 2026-10-09
**Faktakontrollerad:** (Task 4)

Varje volatilt faktapåstående i de **engelska** ytorna, med alla sina
förekomster. De svenska ytorna ingår inte i rundan (spec §5) och har därför
inga poster.

Ytorna: **EW** `_unpublished/guides/copilot/index.html` · **EP**
`_unpublished/exports/copilot-print-a4-en.html` · **QS**
`_unpublished/exports/copilot-quick-start-en.html`

**QS står utanför ytkonsistensvakten** — avsiktligt, spec §7: quick-starten är
en tredje yta med egen, kortare formulering, och kravet "ordagrant på alla
ytor" vore rött från dag ett och därmed värdelöst. Den bevakas i stället av
förekomstkolumnen här, av PDF-facit, och av leveransvakten
(`scripts/tests/test_copilot_delivery.py`).

## Hur källorna läses

Varje sida hämtas som rå HTML och läses ordagrant; texten extraheras lokalt ur
markupen. Ingen sida sammanfattas av ett annat modellanrop, och en
sammanfattning är aldrig källa till ett värde. Där källor går emot varandra
står båda, och den nyare vinner — med noteringen att de skiljer sig.

## Poster

(Task 3 fyller tabellen, Task 4 kolumnerna källa och utfall.)

| id | påstående idag | typ | EW | EP | QS | källa + datum | utfall |
|---|---|---|---|---|---|---|---|

## Observationer utanför posterna

(Task 4.)

## Vaktblock

Semantiken är den som gäller sedan 2026-10-09: `aktiv` kräver att strängen står
ordagrant på **båda** de engelska guideytorna (EW + EP), `borttaget` att den
**inte** står på någon av dem. Varje påstående rundan stryker eller rättar får
en `borttaget`-rad — den är det enda som hindrar att rättningen tas tillbaka.

```guard
# Fylls i Task 10. Tills blocket har rader hoppar de parametriserade
# vakterna över copilot, och Task 13 kräver 0 skipped i sviten — så ett
# tomt block kan inte överleva rundan.
```
DOC
```

- [ ] **Steg 7: Kör testerna och se dem passera**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py scripts/tests/test_factinventory.py -v`
Förväntat: PASS. Copilots tre parametriseringar står som SKIPPED med "fylls i Task 10"; Claudes tre som PASSED.

- [ ] **Steg 8: Jämför insamlade test-id:n mot `main`**

Fälla 1 i spec §8: `str.replace` utan `count` tog bort tre vakter i stället för en 2026-10-09, och sviten förblev grön. Parametrisering byter namn på tester — därför jämförs listorna, inte antalen.

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py \
  --collect-only -q | sed '/^$/,$d' | sort > /tmp/ids-now.txt
# -u krävs: docs/guide-facts-copilot.md är ospårad i det här läget och
# en stash utan -u vägrar med "did not match any file known to git".
# Sökvägarna är avgränsade till scripts/tests/ och inventeringen —
# Johans ocommittade filer ligger i exports/ och assets/ och rörs inte.
git stash push -u -- scripts/tests/ docs/guide-facts-copilot.md
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py \
  --collect-only -q | sed '/^$/,$d' | sort > /tmp/ids-main.txt
git stash pop
git stash list   # ska vara tom — blev den inte det, poppa innan du går vidare
diff /tmp/ids-main.txt /tmp/ids-now.txt
```
Förväntat: varje rad i `ids-main.txt` har en motsvarighet i `ids-now.txt` — de tre "verkliga" testerna som `[claude]`-varianter, de nio övriga oförändrade, plus de sex nya. **Inget `main`-id får ha försvunnit utan att dess `[claude]`-variant finns.** Saknas ett: en vakt har tappats, stanna.

- [ ] **Steg 9: Kör hela sviten**

Kör: `/usr/bin/python3 -m pytest scripts/tests/ -q`
Förväntat: **760 passed, 3 skipped** (752 + 8 nya insamlade + 3 nya parametriseringar, varav Copilots tre hoppas över).

- [ ] **Steg 10: Commit**

```bash
git add scripts/tests/surfacecheck.py scripts/tests/factinventory.py \
        scripts/tests/test_guide_surface_consistency.py
git add -f docs/guide-facts-copilot.md   # docs/ är gitignorerad, -f krävs
git commit -m "test(copilot): ytvakten och inventeringen blir guide-agnostiska"
```

---

## Task 2: Leveransvakten — PDF:erna, inte HTML:en

**Filer:**
- Skapa: `scripts/tests/test_copilot_delivery.py`

**Gränssnitt:**
- Förbrukar: `scripts/tests/pdf_fingerprint.py` — `fp.ROOT`, `fp.extract(path) -> str` (pdftotext `-layout` över hela filen), `fp.UNPUBLISHED_GUIDE_PDFS`.
- Producerar: inget andra uppgifter läser.

Varje vakt rundan ärver läser HTML. Leveransen är två PDF:er. Rättas HTML:en och glöms renderingen är allt grönt medan filen som går till Skool fortfarande säger "Swedish schools". Den här vakten läser de två filerna som faktiskt levereras.

**Vakten är röd från den stund den skrivs till Task 10 har renderat om.** Det är avsiktligt och det är poängen: den beskriver leveransen, och leveransen är fel just nu. Uppgiften avslutas med den **xfail-markerad mot en namngiven uppgift**, och Task 10 tar bort markeringen. En vakt som skrivs efter renderingen hade aldrig setts bli röd på det den vaktar.

- [ ] **Steg 1: Skriv vakten**

```python
# scripts/tests/test_copilot_delivery.py
"""Leveransen är de två engelska PDF:erna, inte HTML:en de renderas ur.

Varje annan vakt i rundan läser HTML. Rättas HTML:en utan att PDF:erna
renderas om går hela sviten grön medan filen som går till Skool
fortfarande bär den svenska inramningen. Den här vakten läser det som
levereras.

Den täcker också quick-starten, som med avsikt står utanför
ytkonsistensvakten (spec §7) och annars inte bevakas av något som läser
dess innehåll.
"""
from __future__ import annotations

import re

import pytest

from . import pdf_fingerprint as fp

DELIVERED = (
    "_unpublished/assets/pdfs/guides/copilot-guide-en.pdf",
    "_unpublished/assets/pdfs/guides/copilot-quick-start-en.pdf",
)

# Strängar som inte får stå i de engelska PDF:erna när rundan är klar.
# "Swedish"/"Sweden" täcker inramningen, "Skolverket"/"IMY" myndigheterna,
# "Schrems"/"GDPR" den rättsliga analysen väg A tar bort, "April 2026"
# datumstämpeln och "kr 350" SEK-priset i den engelska SKU-tabellen.
FORBIDDEN = (
    "Swedish", "Sweden", "Skolverket", "IMY", "Schrems", "GDPR",
    "April 2026", "kr 350",
)


def _flat(rel: str) -> str:
    """pdftotext -layout bryter rader mitt i meningar; en sträng som
    'Swedish schools' står med radbrytning emellan i den renderade
    filen. Platta till allt blankt till ett mellanslag innan sökning."""
    return re.sub(r"\s+", " ", fp.extract(fp.ROOT / rel))


@pytest.mark.parametrize("rel", DELIVERED)
@pytest.mark.xfail(reason="röd till Task 10 har renderat om PDF:erna", strict=True)
def test_the_delivered_pdfs_carry_no_swedish_framing(rel):
    """Granskningsfokus 2."""
    flat = _flat(rel)
    found = [needle for needle in FORBIDDEN if needle in flat]
    assert found == [], f"{rel} bär kvar: {found}"


def test_the_quick_start_pdf_is_part_of_the_delivery_guard():
    """Granskningsfokus 3: quick-starten står utanför ytvakten med
    avsikt. Faller den också ur den här vakten bevakas dess innehåll av
    ingenting alls."""
    assert any("quick-start" in rel for rel in DELIVERED)
    for rel in DELIVERED:
        assert rel in fp.UNPUBLISHED_GUIDE_PDFS, f"{rel} står inte i facitlistan"
```

- [ ] **Steg 2: Kör och se att den är röd på rätt sätt**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_copilot_delivery.py -v`
Förväntat: `test_the_quick_start_pdf_is_part_of_the_delivery_guard` PASSED, de två parametriseringarna XFAIL. **Läs utfallet, bocka inte blint:** `strict=True` betyder att en XPASS är ett fel. Får du XPASS står inte strängarna i PDF:en — då har du antingen fel filsökväg eller en extraktion som inte ger text, och vakten vaktar ingenting. Kontrollera i så fall med `pdftotext -f 1 -l 1 _unpublished/assets/pdfs/guides/copilot-guide-en.pdf - | head` att texten faktiskt kommer ut.

- [ ] **Steg 3: Kör hela sviten**

Kör: `/usr/bin/python3 -m pytest scripts/tests/ -q`
Förväntat: 761 passed, 3 skipped, 2 xfailed.

- [ ] **Steg 4: Commit**

```bash
git add scripts/tests/test_copilot_delivery.py
git commit -m "test(copilot): leveransvakten läser PDF:erna, inte HTML:en"
```

---

## Task 3: Inventera varje volatilt påstående

**Filer:**
- Modifiera: `docs/guide-facts-copilot.md` (postabellen)

Ingen källa läses här och ingen yta redigeras. Uppgiften är att hitta och lokalisera varje påstående som kan ha åldrats eller som bär svensk inramning, med radnummer per yta. Ett påstående som inte står i tabellen får inte skrivas om senare.

- [ ] **Steg 1: Mät inramningen**

```bash
cd /Users/johan/Projekt/Choosewise/choosewise-education
for f in _unpublished/guides/copilot/index.html \
         _unpublished/exports/copilot-print-a4-en.html \
         _unpublished/exports/copilot-quick-start-en.html; do
  echo "=== $f"
  grep -nE "Swedish|Sweden|Skolverket|IMY|GDPR|Schrems|EU Data Boundary|April 2026|kr ?[0-9]" "$f" | cut -c1-120
done
```
Varje träff hör till antingen en post (ett påstående som ska rättas) eller en omriktning (en formulering som ska skrivas om). Båda listas.

- [ ] **Steg 2: Mät produktfakta**

Särskilt misstänkta enligt spec §6, eftersom Microsoft bytt namn och paketering flera gånger sedan juni:

```bash
grep -nE "Microsoft 365 Copilot|Copilot Pro|Copilot Chat|Copilot Studio|Copilot Pages|Commercial Data Protection|CDP|copilot\.microsoft\.com|learn\.microsoft\.com|admin cent|13\+|age floor|license|licence" \
  _unpublished/exports/copilot-print-a4-en.html | cut -c1-120
```

- [ ] **Steg 3: Skriv tabellen**

En rad per påstående, id `C01`, `C02`, … Kolumnerna är `id | påstående idag | typ | EW | EP | QS | källa + datum | utfall`. `typ` är en av `produktnamn`, `pris`, `funktion`, `URL`, `åldersgräns`, `inramning`, `datumstämpel`. Platser är radnummer; `—` betyder att påståendet inte står på den ytan. Lämna `källa + datum` och `utfall` tomma — Task 4 äger dem.

Dessa är kända från planeringen och **ska** finnas med (fler tillkommer):

| id | påstående | typ | plats |
|---|---|---|---|
| C01 | SKU-tabellens fyra produktnamn: "Copilot (free web)", "Copilot Chat (with work/school account)", "Copilot Pro", "Microsoft 365 Copilot" | produktnamn | EP 689–732, EW ~110–130 |
| C02 | Priset "~kr 350/user/mo" i den **engelska** SKU-tabellen | pris | EP 724, 1193, 1198, 1254; EW 126 |
| C03 | "Commercial Data Protection" som namn och omfång | produktnamn | EP 767–781, EW 145–156, QS 95 |
| C04 | Åldersgolvet "13+" för arbets-/skolkonto | åldersgräns | EP 1208, EW ~410 |
| C05 | URL:en `copilot.microsoft.com` som konsumentytan | URL | EP 689–732, 1254; QS 190 |
| C06 | URL:en `learn.microsoft.com/copilot` som hjälpkälla | URL | EP 1310, EW 504 |
| C07 | "EU Data Boundary" som produktfunktion (data residency) | funktion | EP 633, 797, 1144–1156; EW 154, 401–405 |
| C08 | De sex funktionerna i del 2 och deras namn ("Copilot Pages" m fl) | funktion | EP 850–1040, EW ~200–330, QS 99–120 |
| C09 | Datumstämpeln "April 2026" | datumstämpel | EP 602, 1324; EW 49, 525 |
| C10 | Omslagets "A practical guide for Swedish schools" | inramning | EP 590 |
| C11 | FAQ-posten "Is Copilot available in Swedish?" | inramning | EP 1266–1271, EW 460–463 |
| C12 | Skolverket-exemplen i prompterna | inramning | EP 857, 1233; EW 196 |
| C13 | "Swedish-English parallel version" / "Swedish rewrite" | inramning | EP 892, 995; EW 228, 316 |
| C14 | Den rättsliga analysen (GDPR, Schrems II, DPIA-meningarna) | inramning | EP 789–799, 1115–1156; EW 152–156, 380–405 |
| C15 | Reader-responsibility-noten med Sverige, Skolverket, IMY och fyra namngivna länder | inramning | EP 1217, EW 422 |
| C16 | Avslutningens CTA: "I offer consulting for schools, primarily in Sweden." | inramning | EW 504 |
| C17 | Innehållsförteckningens sex sidnummer | datumstämpel | EP 607–657 |

- [ ] **Steg 4: Kontrollera att varje radnummer stämmer**

```bash
/usr/bin/python3 - <<'PY'
import re
from pathlib import Path
root = Path(".")
# Klistra in (fil, rad, en kort sträng ur påståendet) för varje post och se
# att strängen verkligen står på den raden. En felpekande post skickar
# Task 5–9 till fel stycke.
checks = [
    ("_unpublished/exports/copilot-print-a4-en.html", 590, "Swedish schools"),
    ("_unpublished/exports/copilot-print-a4-en.html", 724, "kr 350"),
    ("_unpublished/guides/copilot/index.html", 422, "Readers outside Sweden"),
]
for rel, line, needle in checks:
    text = (root / rel).read_text(encoding="utf-8").splitlines()[line - 1]
    print(("OK  " if needle in text else "FEL "), rel, line, needle)
PY
```
Förväntat: OK på varje rad. Utöka listan till samtliga poster.

- [ ] **Steg 5: Commit**

```bash
git add -f docs/guide-facts-copilot.md
git commit -m "docs(copilot): inventera guidens volatila påståenden"
```

---

## Task 4: Faktakontrollera varje post mot namngiven källa

**Filer:**
- Modifiera: `docs/guide-facts-copilot.md` (kolumnerna `källa + datum` och `utfall`, plus "Observationer utanför posterna")

Ingen yta redigeras. Varje post får en källa med hämtdatum och ett utfall: **stämmer**, **fel** (med det rätta värdet), eller **obelagt** (källan säger inte det guiden säger).

- [ ] **Steg 1: Hämta källorna som rå HTML**

Sidorna läses ordagrant, inte sammanfattade. En sammanfattning får aldrig vara källa till ett värde — den har tidigare i detta projekt förvanskat versionsnummer.

```bash
mkdir -p /tmp/copilot-sources
# Microsofts egna sidor är källan för produkt, licens, pris och funktion.
# Hämta de sidor posterna pekar på, en fil per URL, och extrahera text lokalt.
curl -sS -A "Mozilla/5.0" "https://www.microsoft.com/en-us/microsoft-365/copilot/" \
  -o /tmp/copilot-sources/copilot-home.html
curl -sS -A "Mozilla/5.0" "https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-overview" \
  -o /tmp/copilot-sources/learn-overview.html
/usr/bin/python3 - <<'PY'
import re, pathlib
for p in sorted(pathlib.Path("/tmp/copilot-sources").glob("*.html")):
    raw = p.read_text(encoding="utf-8", errors="ignore")
    raw = re.sub(r"<(script|style)\b.*?</\1>", " ", raw, flags=re.S | re.I)
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw))
    print("=" * 70); print(p.name, len(text)); print(text[:4000])
PY
```
Går en sida inte att hämta (403, inloggning, JS-rendering) står det i källkolumnen, och påståendet behandlas som **obelagt** — det presenteras aldrig som fastställt. Det är spec §3:s motivering som avgör: varje påstående ska gå att belägga med en källa Johan kan stå för.

- [ ] **Steg 2: Avgör varje post**

Fyll `källa + datum` med URL, hämtdatum och **det ordagranna citatet** som bär värdet. Fyll `utfall` med **stämmer** / **fel: <rätt värde>** / **obelagt: <vad källan säger i stället>**.

Särskilt att avgöra:
- **C02, priset.** Den engelska SKU-tabellen prissätter i SEK. Det är inte bara ett fel värde, det är fel valuta för en engelskspråkig läsekrets. Rätt värde är Microsofts eget listpris i USD per användare och månad, med noteringen att EDU-avtal och Volume Licensing avviker. Står priset inte ordagrant på en hämtbar sida blir posten **obelagt**, och då skrivs cellen om till en formulering utan siffra (Task 8 äger hur).
- **C04, åldersgolvet.** Microsofts eget minimum, inte en nationell regel. Namnge inget land.
- **C07, EU Data Boundary.** Får stå som produktfunktion (var data lagras och behandlas), aldrig som rättslig analys. Motiveringen skrivs ut i utfallskolumnen.

- [ ] **Steg 3: Skriv "Observationer utanför posterna"**

Allt faktakontrollen stötte på som inte är en post: funktioner guiden inte nämner, namnbyten som inte rör någon mening i guiden, sidor som flyttat. De står där så att Task 5–9 vet att de finns och inte tror att de förbisetts. Att täcka dem är nytt omfång.

- [ ] **Steg 4: Kontrollera att inget påstående står utan utfall**

```bash
/usr/bin/python3 - <<'PY'
import re, pathlib
rows = [l for l in pathlib.Path("docs/guide-facts-copilot.md")
        .read_text(encoding="utf-8").splitlines()
        if re.match(r"^\| C\d\d ", l)]
print(f"{len(rows)} poster")
tom = [l.split("|")[1].strip() for l in rows if not l.rstrip().rstrip("|").split("|")[-1].strip()]
assert not tom, f"poster utan utfall: {tom}"
print("varje post har ett utfall")
PY
```

- [ ] **Steg 5: Commit**

```bash
git add -f docs/guide-facts-copilot.md
git commit -m "docs(copilot): faktakontrollera varje post mot namngiven källa"
```

---

# ⟨ GRIND ⟩

**Ingen guideyta redigeras förrän:**

- [ ] `docs/guide-facts-copilot.md` har en post per volatilt påstående, var och en med källa, hämtdatum och utfall.
- [ ] `/usr/bin/python3 -m pytest scripts/tests/ -q` ger 761 passed, 3 skipped, 2 xfailed.
- [ ] Inget under `exports/`, `assets/pdfs/wise/` eller någon svensk yta är ändrat: `git status --short | grep -vE "^ M (docs/|scripts/)"` ska bara visa Johans redan ocommittade filer.

---

# EFTER GRINDEN — de två engelska ytorna redigeras

Varje uppgift härifrån redigerar **båda** engelska guideytorna i samma commit. Aldrig en i taget: det är den divergens vakten finns till för att förhindra, och en halv rättning är svårare att hitta än ingen.

## Task 5: Omslaget, datumstämplarna och typsnitten

**Filer:**
- Modifiera: `_unpublished/exports/copilot-print-a4-en.html` (rad 590, 602, 663, 1324)
- Modifiera: `_unpublished/guides/copilot/index.html` (rad 7, 9, 14, 16–18, 49, 525)
- Modifiera: `_unpublished/guides/copilot/styles.css` (rad 23–24)

- [ ] **Steg 1: Omslaget och stämplarna i printytan**

Rad 590 — hela raden ersätts:

```html
    <p class="cover__lede">A practical guide for schools running Microsoft 365 — which Copilot you're actually using, what Commercial Data Protection gives you, and the six features worth building into the teaching week.</p>
```

Rad 602: `April 2026` → `October 2026`.
Rad 1324: `— Johan Lindström, April 2026` → `— Johan Lindström, October 2026`.
Rad 663 — inledningens lede, "Most Swedish schools" → "Most schools":

```html
  <p class="lede">Most schools already run their entire admin stack on Microsoft 365. Copilot is the AI that lives inside that stack. The question isn't whether to adopt it — it's whether to use it the way your tenant already protects, or the consumer way that does not.</p>
```

- [ ] **Steg 2: Samma stämplar i webbytan**

Rad 7, 9 och 14 — de tre metabeskrivningarna. Byt `what the licensing maze means for Swedish schools.` till `what the licensing maze means for a school budget.` i alla tre (de är i dag ordagrant lika, och ska förbli det).
Rad 49: `Updated April 2026` → `Updated October 2026`.
Rad 525: `Updated April 2026.` → `Updated October 2026.`

- [ ] **Steg 3: Google Fonts ut, Blueprint ärvs**

Ta bort rad 16–18 i `_unpublished/guides/copilot/index.html`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

Playfair Display och Inter är **Crestioras** typsnitt (CLAUDE.md §2), inte Choosewises. Raderna hämtar dem från Google, vilket sajtens egen vakt förbjuder för publicerade filer (`test_fonts.py::test_no_published_file_calls_google_fonts` — `_unpublished/` är uteslutet ur den, så den fångar inte det här).

Ta bort rad 23–24 i `_unpublished/guides/copilot/styles.css`:

```css
  --font-display: 'Playfair Display', Georgia, serif;
  --font-body:    'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
```

Länken till `/assets/css/tokens.css` ligger kvar i `<head>` och sätter `--font-display` och `--font-body` till `'Hanken Grotesk'`. Den publicerade Claude-guidens `styles.css` deklarerar inga `--font-*` alls — det är mönstret som följs. Tas bara `<link>`-raderna bort men inte överskrivningarna faller sidan tillbaka på Georgia och systemsans, vilket ser ut som ett fel men inte är Blueprint.

- [ ] **Steg 4: Kontrollera att inget "April 2026" eller Playfair står kvar**

```bash
grep -nE "April 2026|Playfair|fonts\.googleapis|Swedish schools" \
  _unpublished/exports/copilot-print-a4-en.html \
  _unpublished/guides/copilot/index.html \
  _unpublished/guides/copilot/styles.css
```
Förväntat: ingen träff.

- [ ] **Steg 5: Kör sviten**

Kör: `/usr/bin/python3 -m pytest scripts/tests/ -q`
Förväntat: oförändrat 761 passed, 3 skipped, 2 xfailed. Ingen vakt läser de här raderna än — vaktraderna skrivs i Task 10.

- [ ] **Steg 6: Commit**

```bash
git add _unpublished/exports/copilot-print-a4-en.html \
        _unpublished/guides/copilot/index.html \
        _unpublished/guides/copilot/styles.css
git commit -m "content(copilot): omslaget, oktoberstämpeln och Blueprints typografi"
```

---

## Task 6: Del 3 — neutral kärna och jurisdiktionsrutan

**Filer:**
- Modifiera: `_unpublished/exports/copilot-print-a4-en.html` (rad 633, 789–799, 1094, 1108, 1115–1121, 1144–1156, 1208–1220, 1231–1237)
- Modifiera: `_unpublished/guides/copilot/index.html` (rad 152–156, 380, 394, 401–405, 422, 428–431)

Det här är rundans tyngsta uppgift och väg A:s kärna: Sverige och den rättsliga analysen ut ur brödtexten, kvar står vad Microsoft **avtalsmässigt** utfäster i en skoltenant, vad CDP gör och inte gör, och vilka inställningar en administratör styr. Därefter en kort ruta som säger att var läsaren bor avgör resten.

**Varje faktamening som skrivs här måste ha en post i inventeringen.** Har den ingen: öppna posten först, med källa och datum, eller skriv inte meningen.

- [ ] **Steg 1: Del 3:s ingångar**

Printytan rad 1108 — part-opener-leden:

```html
      <p class="part-opener__lede">What Commercial Data Protection commits Microsoft to inside a school tenant, how licensing actually lands in a school budget, and the five decisions worth taking before a staff rollout.</p>
```

Webbytan rad 380 — motsvarande led:

```html
        <p class="part-opener__lede">What Commercial Data Protection actually buys you inside your tenant, where your data is processed, and the five policy decisions worth making before a broader rollout.</p>
```

Printytan rad 633 — innehållsförteckningens underrad:

```html
        <span class="toc__sub">CDP, where data is processed, student data, five policy decisions</span>
```

- [ ] **Steg 2: "Where your data is processed" ersätter Schrems-sidan**

Printytan rad 1144–1156 (PAGE 20). Eyebrow blir `Part 3 · Where your data is processed`, rubriken `Where the processing happens`. Brödtexten skrivs om till tre stycken som alla är belagda i inventeringen:

1. Vad Microsoft utfäster om var data lagras och behandlas för en tenant (C07, produktfunktion — "EU Data Boundary" får nämnas som funktionens namn, aldrig som rättslig analys).
2. Vad administratören kan se och välja i tenanten, och var det står.
3. Vad som **inte** följer av det: att var läsaren bor avgör vilket regelverk som gäller, med hänvisning till rutan.

Samma omskrivning på webbytan rad 401–405; rubriken `<h3 id="p3-boundary">` byter text till `Where your data is processed` men **behåller sitt id** — ankaret kan vara länkat från sidans egen innehållsnavigering och från utskrifter läsaren redan har.

Printytan rad 797 och 799 ("The EU Data Boundary story." och "Schrems II stays in the picture.") ersätts av ett stycke: **"Where the data is processed."** Samma innehåll som punkt 1 ovan, kortare, och utan rättslig analys. Webbytan rad 154 och 156 på samma sätt.

Printytan rad 1117 och 1119, webbytan rad 394: behåll poängen att skolan är data controller och att CDP inte ändrar det. Stryk DPIA-resonemanget om underleverantörskedja och tredjelandsöverföring — det är jurisdiktionsbundet.

- [ ] **Steg 3: Jurisdiktionsrutan, med bestämt innehåll**

Spec §3: rutans innehåll är bestämt, inte fritt. Den slår fast att skolan är personuppgiftsansvarig och att Copilot inte ändrar det, att vilket regelverk som gäller beror på jurisdiktion, och den namnger **tre kategorier läsaren ska kontrollera lokalt**. Inga enskilda lagar eller myndigheter.

Printytan rad 1217 — hela `processing-callout`-rutan ersätts:

```html
  <div class="processing-callout">
    <p class="processing-callout__title">What depends on where you are</p>
    <p>Three things in this part are set where you work, not by the product. <strong>Your data-protection regime</strong> decides what lawful basis you need before processing student data, and what you must document. <strong>Your rules on student age and consent</strong> decide who may use Copilot at all, and who signs for it — Microsoft's own age floor is a minimum, not a permission slip. <strong>Your school's procurement and approval route</strong> decides who signs the agreement and who must be consulted first.</p>
    <p>What does not depend on where you are: your school remains the data controller for its students' data, and using Copilot does not transfer that responsibility to Microsoft. Check the three above locally before you rely on any specific rule in this part.</p>
  </div>
```

Webbytan rad 422 — `reader-responsibility-note` ersätts av samma ruta i `processing-callout`, som sidan redan använder sex gånger. Klassen `reader-responsibility-note` har **ingen CSS-regel någon**stans (kontrollerat 2026-10-09 i `styles.css` och `assets/css/*.css`) — noten renderas i dag som brödtext medan printytans motsvarighet är en ruta. Bytet är alltså ingen ny stil utan en rättning av att webbytan tappat komponenten.

```html
    <div class="processing-callout">
      <p class="processing-callout__title">What depends on where you are</p>
      <p>Three things in this part are set where you work, not by the product. <strong>Your data-protection regime</strong> decides what lawful basis you need before processing student data, and what you must document. <strong>Your rules on student age and consent</strong> decide who may use Copilot at all, and who signs for it — Microsoft's own age floor is a minimum, not a permission slip. <strong>Your school's procurement and approval route</strong> decides who signs the agreement and who must be consulted first.</p>
      <p>What does not depend on where you are: your school remains the data controller for its students' data, and using Copilot does not transfer that responsibility to Microsoft. Check the three above locally before you rely on any specific rule in this part.</p>
    </div>
```

Kontrollera att klassen `reader-responsibility-note` inte står kvar någonstans:

```bash
grep -rn "reader-responsibility" _unpublished/guides/copilot/ _unpublished/exports/copilot-print-a4-en.html
```
Förväntat: ingen träff.

- [ ] **Steg 4: Student access och de fem besluten**

Printytan rad 1208–1216, webbytan motsvarande: åldersgolvet står kvar som Microsofts eget minimum (C04), hänvisningen till nationella regler ersätts av en pekning till rutan. Inga länder namnges.

Printytan rad 1231 och 1237, webbytan 428 och 431: DPIA-punkten skrivs om till "document the Copilot paths in your own data-protection documentation" — behåll de tre vägarna, som är produktfakta, ta bort DPIA som namngiven artefakt där den är jurisdiktionsbunden. Punkten om termingranskning behåller sitt innehåll men tappar "EU Data Boundary coverage" som rättslig term om inventeringen inte belägger den som produktfunktion.

- [ ] **Steg 5: Kontrollera att den rättsliga inramningen är borta**

```bash
grep -ncE "GDPR|Schrems|Skolverket|IMY" \
  _unpublished/exports/copilot-print-a4-en.html \
  _unpublished/guides/copilot/index.html
grep -nE "EU Data Boundary" _unpublished/exports/copilot-print-a4-en.html \
  _unpublished/guides/copilot/index.html | cut -c1-120
```
Förväntat: `0` för den första. Varje kvarvarande "EU Data Boundary" ska gå att peka till en post i inventeringen där den står som produktfunktion med motiveringen utskriven — annars tas den bort.

- [ ] **Steg 6: Kör sviten och commit**

Kör: `/usr/bin/python3 -m pytest scripts/tests/ -q`
Förväntat: 761 passed, 3 skipped, 2 xfailed.

```bash
git add _unpublished/exports/copilot-print-a4-en.html _unpublished/guides/copilot/index.html
git commit -m "content(copilot): del 3 utan jurisdiktion, plus rutan som säger var det avgörs"
```

---

## Task 7: Prompter, FAQ och avslutningen

**Filer:**
- Modifiera: `_unpublished/exports/copilot-print-a4-en.html` (rad 857, 892, 995, 1233, 1266–1271)
- Modifiera: `_unpublished/guides/copilot/index.html` (rad 196, 228, 316, 460–463, 504)

Prompterna och FAQ:n är där den svenska inramningen är mest konkret: ett Skolverket-dokument som exempel, en svensk-engelsk lapp till vårdnadshavare, en hel FAQ-post om svensk språkkvalitet.

- [ ] **Steg 1: Prompterna**

Printytan rad 857: `a twenty-page Skolverket module or a school-improvement document` → `a twenty-page curriculum module or a school-improvement document`.
Printytan rad 892: `Parallel Swedish-English versions:` → `Parallel versions in two languages:`, och exemplet skrivs om till "the same letter in the school's language and in a family's home language".
Printytan rad 995: `a student-accessible Swedish rewrite` → `a student-accessible rewrite`.
Printytan rad 1233: Skolverket-exemplet i staff-guideline-punkten → `a generalised curriculum document`.
Webbytan rad 196: `a thirty-page Skolverket guidance document` → `a thirty-page curriculum or inspection document`.
Webbytan rad 228: `Swedish-English parallel version for EAL parents:` → `Parallel version for EAL parents:`, samma omskrivning som print.
Webbytan rad 316: `a student-accessible Swedish rewrite` → `a student-accessible rewrite`.

- [ ] **Steg 2: FAQ-posten om språk**

Printytan rad 1266–1271 och webbytan rad 460–463 är samma fråga i två formuleringar. Frågan blir:

```html
      <summary>Does Copilot work in languages other than English?</summary>
```

Svaret skrivs om till det som är sant oavsett land och **belagt i inventeringen**: vilka språk Microsoft anger stöd för på de lärarytor del 2 täcker, att nyare funktioner rullas ut på engelska först och får fler språk i senare vågor, och det praktiska tipset att be om omskrivning i rätt register när svaret blir stelt — nu med ett språkneutralt exempel i stället för den svenska promptraden. Står språklistan inte ordagrant på en hämtbar sida blir posten **obelagt**, och då säger svaret vad Microsoft dokumenterar, inte en siffra.

Printytans FAQ-ingress (rad 1247) säger "Nine of the questions" — antalet frågor ändras inte, så siffran står kvar. Kontrollera: `grep -c 'faq-item__q' _unpublished/exports/copilot-print-a4-en.html` ska ge 9.

- [ ] **Steg 3: Avslutningens CTA**

Webbytan rad 504, sista halvan. Meningen `I offer consulting for schools, primarily in Sweden.` stryks, liksom `and the still-open question of Swedish national guidance from Skolverket and IMY`. Resten av stycket (admin centre, Microsoft Learn, MDM-leverantörer) står kvar. Den nya avslutningen:

```html
        <p>Start with the Microsoft 365 admin centre's own Copilot documentation and health dashboard — the fastest source for tenant-level issues, licence assignment, and feature availability. For the technical documentation on CDP and where your data is processed, the Microsoft Learn portal publishes architecture and contract details. For school-specific questions — policy decisions, documentation, rolling out across a staffroom — the guides and write-ups at choosewise.education go further than this FAQ can. For MDM-specific configuration, your school's device-management provider (Intune, Jamf, Mosyle) will have Copilot-specific guidance and profile options.</p>
```

**Antagandet bakom raden** står i Globala villkor: guiden säljer inte Johans tid, den pekar till choosewise.education. Printytans motsvarighet (rad 1310) nämner ingen konsultverksamhet och behöver bara samma `choosewise.education`-pekning om den saknas — kontrollera raden innan du ändrar den.

- [ ] **Steg 4: Kontrollera att inramningen är borta**

```bash
grep -nE "Swedish|Sweden|Skolverket|IMY|consulting" \
  _unpublished/exports/copilot-print-a4-en.html \
  _unpublished/guides/copilot/index.html | cut -c1-140
```
Förväntat: **ingen träff.** Står något kvar ska det vara ett medvetet, motiverat exempel — och då har det en post i inventeringen med motiveringen utskriven. Annars bort.

- [ ] **Steg 5: Kör sviten och commit**

Kör: `/usr/bin/python3 -m pytest scripts/tests/ -q`
Förväntat: 761 passed, 3 skipped, 2 xfailed.

```bash
git add _unpublished/exports/copilot-print-a4-en.html _unpublished/guides/copilot/index.html
git commit -m "content(copilot): prompter, FAQ och avslutning utan svensk inramning"
```

---

## Task 8: Produktnamn, priser och URL:er enligt inventeringen

**Filer:**
- Modifiera: `_unpublished/exports/copilot-print-a4-en.html` (rad 689–732, 1055, 1163–1203, 1254, 1310)
- Modifiera: `_unpublished/guides/copilot/index.html` (rad 110–130, 414, 448, 490, 504)

Varje ändring här har sin post i inventeringen med utfall **fel** eller **obelagt**. Poster med utfall **stämmer** ändras inte — de är redan rätt och står kvar i tabellen med sin motivering.

- [ ] **Steg 1: SKU-tabellen**

Fyra produktnamn (C01) rättas till Microsofts aktuella namn per inventeringen. Priset (C02) byter från `~kr 350/user/mo` till det belagda USD-listpriset per användare och månad — på **alla fem förekomsterna**: print 724, 1193, 1198, 1254 och webb 126. Är C02 **obelagt** skrivs cellen om utan siffra, till exempel `Paid add-on, per user per month` med kostnadsmeningen i brödtexten (print 1198) omskriven till att priset sätts av Volume Licensing och EDU-avtal och ska verifieras hos återförsäljaren.

**Kontrollera med `grep -c`, inte med `str.replace` i huvudet:** fem förekomster är lätt att missa en av, och en halv prisrättning är precis det ytvakten i Task 10 finns till för.

```bash
grep -nE "kr ?350|SEK" _unpublished/exports/copilot-print-a4-en.html \
  _unpublished/guides/copilot/index.html
```
Förväntat efter ändringen: ingen träff.

- [ ] **Steg 2: Funktionsnamnen i del 2**

De sex funktionerna (C08) och deras ytor. Har Microsoft bytt namn på någon sedan juni — "Copilot Pages", "Copilot Chat", in-app-funktionerna — rättas namnet överallt det står, på båda ytorna, och den gamla strängen får en `borttaget`-rad i Task 10.

- [ ] **Steg 3: URL:erna**

C05 och C06. Varje URL i guiden ska svara utan omdirigering till något annat innehåll:

```bash
for u in https://copilot.microsoft.com https://learn.microsoft.com/copilot; do
  printf "%-45s " "$u"; curl -s -o /dev/null -w "%{http_code} -> %{redirect_url}\n" "$u"
done
```
En URL som omdirigerar till en annan sida skrivs om till sitt nya mål. En som svarar 404 tas bort eller ersätts enligt inventeringen.

- [ ] **Steg 4: Kör sviten och commit**

Kör: `/usr/bin/python3 -m pytest scripts/tests/ -q`
Förväntat: 761 passed, 3 skipped, 2 xfailed.

```bash
git add _unpublished/exports/copilot-print-a4-en.html _unpublished/guides/copilot/index.html
git commit -m "content(copilot): produktnamn, priser och URL:er per inventeringen"
```

---

## Task 9: Quick-starten

**Filer:**
- Modifiera: `_unpublished/exports/copilot-quick-start-en.html` (rad 95, 190, plus produktnamn i funktionsrutorna 99–145)

Quick-starten står utanför ytkonsistensvakten (spec §7) och har en egen, kortare formulering. Den får därför inte kopiera guidens meningar — men varje faktapåstående den bär måste vara samma fakta.

- [ ] **Steg 1: Sverige-meningen**

Rad 190, sista meningen: `Verify your country's AI-in-education rules — Sweden lacks national guidance as of April 2026.` ersätts:

```html
    <p>Sign in with your work or school account every time. Consumer Copilot at copilot.microsoft.com is a different product under different terms — not protected by your school's data agreement. De-identify student data before any prompt. Check your own country's rules on student age, consent and data protection before a wider rollout — they differ, and the product does not decide them.</p>
```

(Resten av raden står ordagrant kvar; bara den sista meningen byts.)

- [ ] **Steg 2: Produktnamn och CDP-formuleringen**

Rad 95 (leden) och funktionsrutorna 99–145: samma produktnamn som Task 8 fastställde. Inga nya faktapåståenden — bara samma fakta i quick-startens kortare form.

- [ ] **Steg 3: Kontrollera**

```bash
grep -nE "Swedish|Sweden|April 2026|kr ?350|Skolverket" \
  _unpublished/exports/copilot-quick-start-en.html
```
Förväntat: ingen träff.

- [ ] **Steg 4: Kör sviten och commit**

Kör: `/usr/bin/python3 -m pytest scripts/tests/ -q`
Förväntat: 761 passed, 3 skipped, 2 xfailed.

```bash
git add _unpublished/exports/copilot-quick-start-en.html
git commit -m "content(copilot): quick-starten utan svensk inramning"
```

---

## Task 10: Vaktblocket — varje rättning får sin rad

**Filer:**
- Modifiera: `docs/guide-facts-copilot.md` (vaktblocket)

Nu finns rättningarna; nu skrivs raderna som hindrar att de tas tillbaka. `aktiv` kräver att strängen står ordagrant på **båda** engelska guideytorna (EW + EP). `borttaget` kräver att den inte står på någon av dem.

- [ ] **Steg 1: Skriv raderna**

En `aktiv`-rad per rättat värde som ska stå kvar, och en `borttaget`-rad per struket eller ersatt sträng. Formatet är `id | språk | värde | status`, fyra kolumner, `#` inleder kommentar.

Dessa är kända redan nu och **ska** finnas med (fler tillkommer ur Task 6–9):

```guard
# Engelska ytorna: EW `_unpublished/guides/copilot/index.html`
# + EP `_unpublished/exports/copilot-print-a4-en.html`.
# QS står utanför vakten med avsikt (spec §7) och bevakas av
# test_copilot_delivery.py.
C09 | en | October 2026 | aktiv
C09 | en | April 2026 | borttaget
C10 | en | A practical guide for schools running Microsoft 365 | aktiv
C10 | en | A practical guide for Swedish schools | borttaget
C14 | en | Schrems II | borttaget
C14 | en | GDPR | borttaget
C15 | en | What depends on where you are | aktiv
C15 | en | Readers outside Sweden | borttaget
C12 | en | Skolverket | borttaget
C02 | en | kr 350 | borttaget
C16 | en | I offer consulting for schools, primarily in Sweden | borttaget
```

**Två fällor i just det här steget.** En `aktiv`-rad vars sträng bara står på en yta ger `saknas_på_en_yta` — det betyder att Task 6–9 missade en yta, inte att raden ska skrivas om. En `aktiv`-rad som inte står någonstans ger `finns_ingenstans` och är nästan alltid ett stavfel i vaktblocket.

- [ ] **Steg 2: Kör vakten och läs varje problem**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -v`
Förväntat: PASS, och **ingen SKIPPED kvar** — Copilots tre parametriseringar ska nu köra på riktigt.

- [ ] **Steg 3: Bryt vakten med flit och se den bli röd**

Fälla 2 i spec §8: fyra gånger under 2026-10-09 skrevs en vakt som inte kunde fallera på det den vaktade. Skriv tillbaka ett struket påstående i printytan, se exakt det id:t bli rött, och återställ.

```bash
cp _unpublished/exports/copilot-print-a4-en.html /tmp/copilot-print-backup.html
printf '<!-- April 2026 -->\n' >> _unpublished/exports/copilot-print-a4-en.html
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q 2>&1 | tail -20
cp /tmp/copilot-print-backup.html _unpublished/exports/copilot-print-a4-en.html
git diff --stat -- _unpublished/exports/copilot-print-a4-en.html
```
Förväntat: `C09 [en] återinfört` i utfallet, och efter återställningen en tom `git diff --stat`. **Blir vakten inte röd vaktar den ingenting** — då står strängen inte i vaktblocket, eller normaliseringen äter den, och det ska redas ut innan uppgiften bockas. Återställningen sker med `cp` från kopian, aldrig med `git checkout --` på en katalog.

- [ ] **Steg 4: Kör hela sviten och commit**

Kör: `/usr/bin/python3 -m pytest scripts/tests/ -q`
Förväntat: 764 passed, **0 skipped**, 2 xfailed.

```bash
git add -f docs/guide-facts-copilot.md
git commit -m "test(copilot): vaktblocket — varje rättning och strykning får sin rad"
```

---

## Task 11: Rendera om de två engelska PDF:erna

**Filer:**
- Modifiera: `_unpublished/assets/pdfs/guides/copilot-guide-en.pdf`, `_unpublished/assets/pdfs/guides/copilot-quick-start-en.pdf`
- Modifiera: `scripts/tests/test_copilot_delivery.py` (xfail-markeringen tas bort)

**Båda byggarna renderar EN *och* SV.** Varken `exports/build-copilot-pdf.py` eller `exports/build-copilot-quickstart-pdf.py` tar ett språkargument, och de svenska källorna finns — så fyra filer skrivs och de två svenska måste återställas. De får inte ändras ens i `CreationDate`: spec §1 lämnar dem med junifakta, och en ändrad byte i dem skulle kräva en facitomfångning rundan inte ska göra.

- [ ] **Steg 1: Kopiera undan de svenska PDF:erna**

```bash
cd /Users/johan/Projekt/Choosewise/choosewise-education
cp _unpublished/assets/pdfs/guides/copilot-guide-sv.pdf /tmp/copilot-guide-sv.pdf
cp _unpublished/assets/pdfs/guides/copilot-quick-start-sv.pdf /tmp/copilot-quick-start-sv.pdf
```

- [ ] **Steg 2: Rendera**

```bash
/usr/bin/python3 exports/build-copilot-pdf.py
/usr/bin/python3 exports/build-copilot-quickstart-pdf.py
```

- [ ] **Steg 3: Återställ de svenska, med `cp` från kopian**

```bash
cp /tmp/copilot-guide-sv.pdf _unpublished/assets/pdfs/guides/copilot-guide-sv.pdf
cp /tmp/copilot-quick-start-sv.pdf _unpublished/assets/pdfs/guides/copilot-quick-start-sv.pdf
git status --short -- _unpublished/assets/pdfs/
```
Förväntat: **exakt två ändrade filer**, `copilot-guide-en.pdf` och `copilot-quick-start-en.pdf`. Står en svensk fil som ändrad: återställningen misslyckades, gör om steget. Står någon annan PDF som ändrad: stanna.

- [ ] **Steg 4: Ta bort xfail-markeringen och se vakten bli grön**

Ta bort de två raderna i `scripts/tests/test_copilot_delivery.py`:

```python
@pytest.mark.xfail(reason="röd till Task 10 har renderat om PDF:erna", strict=True)
```

(och importen av `pytest` står kvar — `parametrize` använder den.)

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_copilot_delivery.py -v`
Förväntat: PASS, 3 tester. Är någon röd står en förbjuden sträng kvar i den renderade filen — läs felmeddelandet, det namnger vilken.

- [ ] **Steg 5: Commit**

```bash
git add _unpublished/assets/pdfs/guides/copilot-guide-en.pdf \
        _unpublished/assets/pdfs/guides/copilot-quick-start-en.pdf \
        scripts/tests/test_copilot_delivery.py
git commit -m "build(copilot): rendera om de två engelska PDF:erna ur det rättade innehållet"
```

---

## Task 12: Innehållsförteckningen, bilderna och uppslagen

**Filer:**
- Modifiera: `_unpublished/exports/copilot-print-a4-en.html` (rad 607–657, innehållsförteckningens sidnummer)
- Modifiera: `_unpublished/assets/pdfs/guides/copilot-guide-en.pdf` (om numren ändrades)

Spec §2 svarade fel på den här frågan (se Rättelse ovan): printytan har sex hårdkodade sidnummer i `toc__page`, och FAQ:ns står redan fel i dag — 23 i förteckningen, 24 i PDF:en. Del 3 har dessutom just skrivits om, så sidflödet kan ha flyttat sig. Det här steget går efter renderingen, aldrig före.

- [ ] **Steg 1: Mät var avsnitten faktiskt börjar**

```bash
cd /Users/johan/Projekt/Choosewise/choosewise-education
pdfinfo _unpublished/assets/pdfs/guides/copilot-guide-en.pdf | grep Pages
for p in $(seq 1 30); do
  head=$(pdftotext -f $p -l $p _unpublished/assets/pdfs/guides/copilot-guide-en.pdf - 2>/dev/null | tr '\n' ' ' | cut -c1-70)
  [ -n "$head" ] && printf "%2d  %s\n" "$p" "$head"
done
```

- [ ] **Steg 2: Jämför med förteckningen**

```bash
sed -n '607,657p' _unpublished/exports/copilot-print-a4-en.html | \
  grep -E 'toc__(title|page)' | sed 's/<[^>]*>//g' | sed 's/^ *//'
```
Sex nummer: "Why this guide exists", "Part 1 · Get started", "Part 2 · Work smarter", "Part 3 · Compliance & licensing", "FAQ", "About this guide". Varje ska peka på den sida där avsnittet faktiskt börjar enligt steg 1. **Känt fel att rätta: FAQ:n.** Kontrollera alla sex, inte bara den.

- [ ] **Steg 3: Rätta numren och rendera om**

Rätta `toc__page`-värdena i `_unpublished/exports/copilot-print-a4-en.html`, kör sedan Task 11:s steg 1–3 igen (kopiera undan svenska, rendera, återställ) och mät om med steg 1. Ett tvåsiffrigt nummer som byts mot ett annat tvåsiffrigt flyttar inte sidbrytningarna, men det ska verifieras och inte antas.

- [ ] **Steg 4: Titta på det renderade dokumentet**

Fälla i spec §8: våg 2b granskade text sexton gånger och hittade tre fel först när någon öppnade PDF:en, varav en bild som motsade sin egen text. Tre bilder finns i mallen — `part-1-opener.webp`, `part-2-opener.webp`, `part-3-opener.webp` — och **part 3:s bild står intill text som just skrivits om.**

```bash
pdftoppm -png -r 60 -f 1 -l 4 _unpublished/assets/pdfs/guides/copilot-guide-en.pdf /tmp/copilot-en
pdftoppm -png -r 60 -f 18 -l 24 _unpublished/assets/pdfs/guides/copilot-guide-en.pdf /tmp/copilot-en-p3
pdftoppm -png -r 60 -f 1 -l 2 _unpublished/assets/pdfs/guides/copilot-quick-start-en.pdf /tmp/copilot-qs
ls /tmp/copilot-*.png
```
Öppna bilderna och granska: omslaget säger "schools running Microsoft 365" och "October 2026"; de tre öppningsbilderna finns kvar; jurisdiktionsrutan ligger som en ruta och inte som brödtext; ingen rad har blivit änka eller spräckt sin sida; part 3:s bild motsäger inte den nya texten.

- [ ] **Steg 5: Läs PDF:en från pärm till pärm**

```bash
pdftotext -layout _unpublished/assets/pdfs/guides/copilot-guide-en.pdf /tmp/copilot-en.txt
wc -l /tmp/copilot-en.txt
```
Läs hela filen. Det är sista chansen att se en mening som blev halv när ett stycke byttes ut.

- [ ] **Steg 6: Commit**

```bash
git add _unpublished/exports/copilot-print-a4-en.html \
        _unpublished/assets/pdfs/guides/copilot-guide-en.pdf
git commit -m "fix(copilot): innehållsförteckningens sidnummer mot den renderade PDF:en"
```

---

## Task 13: Selektiv fixturomfångning

**Filer:**
- Modifiera: `scripts/tests/fixtures/guide-pdf-baseline.json`, `scripts/tests/fixtures/guide-pdf-body-baseline.json`

- [ ] **Steg 1: Omfånga bara de två**

```bash
/usr/bin/python3 scripts/tests/fixtures/capture_guide_baseline.py \
  --only _unpublished/assets/pdfs/guides/copilot-guide-en.pdf \
  --only _unpublished/assets/pdfs/guides/copilot-quick-start-en.pdf
```

**`--force` får inte användes.** Det är liktydigt med att slå av paritetsvakten för alla 22 PDF:er (spec §8).

- [ ] **Steg 2: Verifiera att diffen rör exakt två nycklar**

```bash
/usr/bin/python3 - <<'PY'
import json, subprocess
for f in ("guide-pdf-baseline.json", "guide-pdf-body-baseline.json"):
    rel = f"scripts/tests/fixtures/{f}"
    before = json.loads(subprocess.run(["git","show",f"HEAD:{rel}"],
        capture_output=True, text=True, check=True).stdout)
    after = json.loads(open(rel, encoding="utf-8").read())
    changed = sorted(k for k in after if before.get(k) != after[k])
    print(f"{f}: {len(changed)} ändrade nycklar")
    for k in changed: print("   ", k)
    assert sorted(before) == sorted(after), "nyckeluppsättningen ändrades"
    assert len(changed) == 2, "exakt två nycklar ska ha ändrats"
    assert all("copilot-" in k and k.endswith("-en.pdf") for k in changed)
PY
```
Förväntat: två ändrade nycklar per fil, båda `_unpublished/assets/pdfs/guides/copilot-*-en.pdf`. De tjugo andra orörda. Något annat: stanna och ta reda på varför — särskilt om en svensk Copilot-nyckel ändrats, för då återställdes inte SV-filerna i Task 11.

- [ ] **Steg 3: Kör paritets- och innehållsvakterna före commit**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_guide_pdf_parity.py scripts/tests/test_guide_pdf_body_text.py scripts/tests/test_capture_guide_baseline.py -v`
Förväntat: PASS. `test_force_cannot_silently_reset_unrelated_entries` jämför mot HEAD före den här uppgiftens commit — kör den före commit, inte efter.

- [ ] **Steg 4: Commit**

```bash
git add scripts/tests/fixtures/guide-pdf-baseline.json \
        scripts/tests/fixtures/guide-pdf-body-baseline.json
git commit -m "test(copilot): omfånga facit för de två engelska PDF:erna, övriga tjugo orörda"
```

---

## Task 14: Slutkontroll, överlämning och PR

- [ ] **Steg 1: Hela sviten**

Kör: `/usr/bin/python3 -m pytest scripts/tests/ -q`
Förväntat: **766 passed, 0 skipped, 0 xfailed, 0 xpassed.** Står en skip kvar är ett vaktblock tomt; står en xfail kvar sitter markeringen från Task 2 i.

- [ ] **Steg 2: Gå igenom specens §9 rad för rad**

```bash
cd /Users/johan/Projekt/Choosewise/choosewise-education
# Inget "Sweden", "Swedish", "Skolverket" kvar i de engelska ytorna
grep -rncE "Swedish|Sweden|Skolverket|IMY" \
  _unpublished/guides/copilot/index.html \
  _unpublished/exports/copilot-print-a4-en.html \
  _unpublished/exports/copilot-quick-start-en.html      # ska vara 0 på alla tre
# Omslaget säger varken "Swedish schools" eller "April 2026"
grep -nE "Swedish schools|April 2026" _unpublished/exports/copilot-print-a4-en.html | wc -l   # 0
# Webbsidan fri från Google Fonts och Crestiora-typsnitten
grep -rnE "fonts\.googleapis|Playfair|'Inter'" \
  _unpublished/guides/copilot/index.html _unpublished/guides/copilot/styles.css | wc -l       # 0
# Två PDF:er ändrade, inga fler
git diff --name-only origin/main...HEAD -- '*.pdf' | wc -l                                    # 2
# Johans filer orörda
git diff --name-only origin/main...HEAD | grep -cE '^(exports/wise|exports/ratt|assets/pdfs/wise)'   # 0
# Svenska Copilot-ytor orörda
git diff --name-only origin/main...HEAD | grep -cE 'copilot.*-sv|sv/guider/copilot'                  # 0
# Inget publiceringssteg smugit in
git diff --name-only origin/main...HEAD | grep -cE 'guides-en\.json|sitemap\.xml|PAIR_MAP|build-seo-meta'  # 0
```

- [ ] **Steg 3: Kontrollera att varje volatilt påstående har källa och datum**

```bash
grep -cE "^\| C[0-9][0-9] " docs/guide-facts-copilot.md
grep -E "^\| C[0-9][0-9] " docs/guide-facts-copilot.md | grep -cE "2026-10-"
```
Förväntat: samma tal två gånger — varje post bär ett hämtdatum i oktober 2026. Är det andra talet lägre står en post utan källa, och då är dess mening skriven utan belägg.

- [ ] **Steg 4: Uppdatera överlämningen**

`docs/blueprint-handoff.md`:
- Flytta Copilot-raden i statustabellen från "SPEC GODKÄND, inget byggt" till sitt nya läge, med PR-nummer, grennamn och sifferutfallet ur sviten.
- Skriv in **det svenska divergensläget** som ett känt läge, inte något som ska upptäckas senare: `_unpublished/exports/copilot-print-a4-sv.html`, `_unpublished/exports/copilot-quick-start-sv.html` och `_unpublished/sv/guider/copilot/` står kvar med junifakta och svensk inramning, och deras PDF:er är orörda. De engelska och svenska Copilot-ytorna divergerar därför i sak — avsiktligt, Johans beslut 2026-10-08.
- Skriv in att **vaktlagret nu är guide-agnostiskt**: `surfacecheck.GUIDE_SURFACES` + `GUIDES`, `factinventory.INVENTORIES` + `inventory_path()`, och att nästa guide läggs till genom att fylla två dict:ar och skapa en inventering.
- Skriv in **leveransvakten** (`scripts/tests/test_copilot_delivery.py`) och vad den äger: de levererade PDF:erna, inklusive quick-starten som står utanför ytvakten.
- Skriv in **rättelsen av spec §2 om innehållsförteckningen** och att FAQ-numret var fel före rundan, så att nästa guide mäter på `toc__page` och inte på Claude-guidens klassnamn.
- Lägg till under det som står öppet: **de tre återstående guiderna** (Gemini/NotebookLM, Apple Intelligence, elevguiden) tas i egna rundor med den här som mall, och **de svenska Copilot-ytorna** om de någon gång ska hämta in de engelska.

- [ ] **Steg 5: Commit och öppna PR**

```bash
git add -f docs/blueprint-handoff.md
git commit -m "docs(copilot): uppdatera överlämningen efter Copilot-rundan"
git push -u origin feat/copilot-guide-international
```

PR-texten säger: vad som levereras (två engelska PDF:er till Skool, ingenting publicerat), vilken väg som valdes och varför, vad vaktlagret nu äger, det svenska divergensläget, rättelsen av spec §2, och sifferutfallet ur sviten.

---

## Vad som gör rundan klar

Specens §9, med planens tillägg:

- [ ] Båda engelska PDF:erna byggda ur rättat innehåll, med Blueprint-layout.
- [ ] Inget "Sweden", "Swedish" eller "Skolverket" kvar i de engelska ytorna annat än där det är ett medvetet, motiverat exempel med en post i inventeringen.
- [ ] Omslaget säger varken "Swedish schools" eller "April 2026".
- [ ] Varje volatilt påstående har en post i `docs/guide-facts-copilot.md` med källa och datum.
- [ ] Ytkonsistensvakten grön för både Claude och Copilot, utan skip.
- [ ] Leveransvakten grön — och den har setts vara röd innan PDF:erna renderades om.
- [ ] PDF-facit omfångat med `--only`, de tjugo andra nycklarna orörda.
- [ ] Webbsidan rättad i sak och fri från Google Fonts och Crestioras typsnitt.
- [ ] Innehållsförteckningens sex sidnummer stämmer mot den renderade PDF:en.
- [ ] Det svenska divergensläget skrivet i överlämningen.
