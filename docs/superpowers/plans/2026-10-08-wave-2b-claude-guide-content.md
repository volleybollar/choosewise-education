# Våg 2b — Claude-guidens innehåll: implementationsplan

> **För agentiska arbetare:** OBLIGATORISK SUB-SKILL: använd superpowers:subagent-driven-development (rekommenderad) eller superpowers:executing-plans för att genomföra planen uppgift för uppgift. Stegen är kryssrutor (`- [ ]`) för spårning.

**Mål:** Claude-guiden, EN + SV, blir faktamässigt sann per oktober 2026, bär Johans röst på svenska, och levereras som andra upplagan med fyra ytor som är överens.

**Arkitektur:** En numrerad påståendeinventering är ryggraden. Allt inventeras och kontrolleras före en grind (PR #30 mergas); därefter redigeras de fyra ytorna, PDF:erna renderas om och fixturerna omfångas selektivt. Ett femte vaktlager läser inventeringen och påstår att webbytan och printytan är överens inom varje språk.

**Teknikstack:** `/usr/bin/python3` (3.9.6 — enda interpretern med pytest, playwright och Pillow), pytest, Playwright för PDF-rendering, `pdftohtml`/`pdffonts` via `scripts/tests/pdf_fingerprint.py`.

**Spec:** `docs/superpowers/specs/2026-10-08-wave-2b-claude-guide-content-design.md`

## Globala villkor

- **`git add -A` används aldrig.** Repot har alltid ~26 ocommittade filer under `exports/` och `assets/pdfs/wise/` som tillhör Johan. Namnge varje fil i varje `git add`.
- **`git checkout --` körs aldrig på en katalog.** Det raderade två av Johans filer i våg 2a. Kopiera undan och återställ med `cp`.
- **Interpretern är `/usr/bin/python3`** (3.9.6). Ingen `dict | dict`-syntax; använd `{**a, **b}`. `list[str]`-annoteringar kräver `from __future__ import annotations`.
- **Paletten rörs inte.** Våg 1 och 2a äger färg och typografi. Den här rundan ändrar bara text.
- **Koppar blir aldrig text.** Gäller om en textändring tvingar fram en stilrättning: `--color-highlight-ink` (#9C5A24) på ljus yta, `--color-highlight-on-dark` (#E8C9A8) på mörk.
- **Svenska är inte översatt engelska.** CLAUDE.md §3. Nyskrivna svenska avsnitt skrivs på svenska i Johans röst via `voice`-skillen, aldrig översatta från den engelska omskrivningen. `voice-humanizer` körs inte — den kräver uttrycklig begäran och den har inte getts.
- **Upplagan är "andra upplagan, oktober 2026"** / "Second edition, October 2026". Exakt den formuleringen, på varje av de fjorton förekomsterna.
- **Varje faktapost bär källa OCH datum OCH vilken källa.** Anthropics dokumentationssida motsäger annonseringen; en bock räcker inte.
- **De fyra opublicerade guiderna rörs inte.** Inte heller `build-nlm-prompts-en.py`, presentationsteknik-guiderna, Visual Codes, eller sajtens övriga 202 sidor.

## Granskningsfokus

Fem fel som specen förutsätter men som ingen uppgifts tester annars skulle fånga. Varje rad har fått sitt test inlagt i den uppgift som äger koden.

1. **Någon kör omfångningen med `--force` i stället för `--only`** och nollställer tyst facit för de arton PDF:er rundan aldrig öppnat. → Task 4, `test_force_cannot_silently_reset_unrelated_entries`.
2. **En sträng i vaktblocket finns på ingen av ytorna** (stavfel i inventeringen) och rapporteras som innehållsfel, så redaktören letar på fel ställe. → Task 5, `test_checker_separates_typo_from_missing_on_one_surface`.
3. **Typografisk skillnad mellan ytorna** — hårt mellanslag, tankstreck mot bindestreck — gör vakten röd utan att något är fel. → Task 5, `test_comparison_normalises_whitespace_and_dashes`.
4. **Ett påstående tas bort ur guiden men står kvar i vaktblocket** och vakten blir röd för alltid utan att säga att inventeringen är inaktuell. → Task 5, `test_rows_marked_borttaget_are_skipped`.
5. **Dollarpriset rättas men kronpriset inte**, eller tvärtom — vakten är per språk och ser aldrig att de hänger ihop. → Task 5, `test_derived_rows_require_their_source_row_to_be_resolved`.

---

# FÖRE GRINDEN — ingen av guidens ytor rörs

## Task 1: Inventeringens skelett och dess parser

**Filer:**
- Skapa: `docs/guide-facts-claude.md`
- Skapa: `scripts/tests/factinventory.py`
- Test: `scripts/tests/test_factinventory.py`

**Gränssnitt:**
- Förbrukar: inget.
- Producerar: `factinventory.load() -> list[Row]` där `Row` är en `NamedTuple` med fälten `id: str`, `lang: str`, `value: str`, `status: str`. `factinventory.INVENTORY: Path`. Task 5 läser dessa.

Vaktblocket är det enda testet läser. Resten av inventeringen är prosa och tabeller för människor.

- [ ] **Steg 1: Skriv det misslyckade testet**

```python
# scripts/tests/test_factinventory.py
"""Vaktblocket i inventeringen måste gå att läsa maskinellt.

Ett markdown-dokument som parsas på fri text är sprött. Blocket är
därför en avgränsad fence med ett fast kolumnformat, och det här
testet är det som håller formatet ärligt.
"""
from __future__ import annotations

import textwrap

from . import factinventory


def test_parses_id_lang_value_and_status(tmp_path):
    doc = tmp_path / "inv.md"
    doc.write_text(textwrap.dedent("""\
        # Inventering

        Prosa som inte ska läsas.

        ```guard
        P01 | en | Pricing accurate as of October 2026 | aktiv
        P01 | sv | Priserna stämmer per oktober 2026 | aktiv
        P09 | en | Cowork is a tab inside Claude Desktop | borttaget
        ```

        Mer prosa.
        """), encoding="utf-8")
    rows = factinventory.load(doc)
    assert [r.id for r in rows] == ["P01", "P01", "P09"]
    assert [r.lang for r in rows] == ["en", "sv", "en"]
    assert rows[1].value == "Priserna stämmer per oktober 2026"
    assert rows[2].status == "borttaget"


def test_ignores_prose_that_looks_like_a_row(tmp_path):
    doc = tmp_path / "inv.md"
    doc.write_text(textwrap.dedent("""\
        Utanför blocket står en tabellrad: P99 | en | lurendrejeri | aktiv

        ```guard
        P01 | en | riktig rad | aktiv
        ```
        """), encoding="utf-8")
    rows = factinventory.load(doc)
    assert len(rows) == 1
    assert rows[0].id == "P01"


def test_rejects_a_row_with_the_wrong_column_count(tmp_path):
    doc = tmp_path / "inv.md"
    doc.write_text("```guard\nP01 | en | saknar status\n```\n", encoding="utf-8")
    try:
        factinventory.load(doc)
    except ValueError as exc:
        assert "P01" in str(exc)
    else:
        raise AssertionError("en rad med tre kolumner ska avvisas, inte tolkas")
```

- [ ] **Steg 2: Kör testet och se att det misslyckas**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_factinventory.py -v`
Förväntat: FAIL, `ImportError` eller `ModuleNotFoundError: factinventory`.

- [ ] **Steg 3: Skriv den minsta implementationen**

```python
# scripts/tests/factinventory.py
"""Läser vaktblocket ur påståendeinventeringen.

Inventeringen är ett dokument för människor. Blocket mellan ```guard
och ``` är den enda delen som läses maskinellt, så att vakten och
källloggen är samma fil och inte två listor att hålla i synk.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "docs" / "guide-facts-claude.md"

_BLOCK = re.compile(r"^```guard\s*$(.*?)^```\s*$", re.M | re.S)
_STATUSES = {"aktiv", "borttaget"}


class Row(NamedTuple):
    id: str
    lang: str
    value: str
    status: str


def load(path: Path = None) -> list:
    text = (path or INVENTORY).read_text(encoding="utf-8")
    rows = []
    for block in _BLOCK.findall(text):
        for line in block.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) != 4:
                raise ValueError(
                    f"raden {parts[0] if parts else line!r} har {len(parts)} kolumner, "
                    "formatet är: id | språk | värde | status"
                )
            ident, lang, value, status = parts
            if status not in _STATUSES:
                raise ValueError(f"{ident}: okänd status {status!r}, väntade {_STATUSES}")
            rows.append(Row(ident, lang, value, status))
    return rows
```

- [ ] **Steg 4: Kör testet och se att det går igenom**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_factinventory.py -v`
Förväntat: PASS, tre tester.

- [ ] **Steg 5: Lägg inventeringens skelett**

Skapa `docs/guide-facts-claude.md` med rubrikerna och ett tomt vaktblock. Posterna fylls i Task 2.

```markdown
# Påståendeinventering — Claude-guiden

**Rundan:** Blueprint våg 2b. Spec: `docs/superpowers/specs/2026-10-08-wave-2b-claude-guide-content-design.md`
**Upprättad:** 2026-10-08

Varje volatilt faktapåstående i guiden, med alla sina förekomster över de
fyra ytorna. En post är inte klar förrän alla fyra är bockade.

Ytorna: **EW** `guides/claude/index.html` · **SW** `sv/guider/claude/index.html`
· **EP** `exports/claude-print-a4-en.html` · **SP** `exports/claude-print-a4-sv.html`

## Poster

| id | påstående idag | typ | omfång | EW | SW | EP | SP | källa + datum | utfall |
|---|---|---|---|---|---|---|---|---|---|

## Frågor som kräver inloggat konto

Johan betar av. Ja/nej-frågor, inte utredningsuppdrag.

| id | frågan | svar |
|---|---|---|

## Vaktblock

Läses av `scripts/tests/test_guide_surface_consistency.py`. En rad per
bevakat värde: `id | språk | exakt sträng | status`. Status `borttaget`
hoppas över — använd den när ett påstående utgått ur guiden i stället för
att radera raden, så historiken står kvar.

```guard
```
```

- [ ] **Steg 6: Commit**

```bash
git add -f docs/guide-facts-claude.md
git add scripts/tests/factinventory.py scripts/tests/test_factinventory.py
git commit -m "feat(2b): inventeringens skelett och maskinläsbara vaktblock"
```

---

## Task 2: Fyll inventeringen med varje volatilt påstående

**Filer:**
- Modifiera: `docs/guide-facts-claude.md`

**Gränssnitt:**
- Förbrukar: inventeringens skelett från Task 1.
- Producerar: en ifylld posttabell. Vaktblocket fylls först i Task 8, när de slutliga strängarna finns.

Ingen redigering av guiden i den här uppgiften. Bara inventering.

- [ ] **Steg 1: Hitta kandidaterna maskinellt**

Kör i reporoten och spara utfallet som arbetsunderlag:

```bash
for f in guides/claude/index.html sv/guider/claude/index.html \
         exports/claude-print-a4-en.html exports/claude-print-a4-sv.html; do
  echo "=== $f ==="
  sed -e 's/<[^>]*>/ /g' "$f" \
  | grep -nE '\$[0-9]|[0-9]+ ?kr|Free|Pro|Max|Team|Enterprise|Sonnet|Opus|Haiku|Cowork|Claude Code|Artifacts|Projects|Styles|Memory|Custom Skills|MCP|Connectors|April 2026|april 2026|First edition|GDPR|AI Act|ChatGPT|custom GPTs' \
  | sed 's/  */ /g'
done
```

- [ ] **Steg 2: Skriv en post per påstående**

Typerna är: `pris`, `nivå`, `modellnamn`, `funktionsnamn`, `gränssnitt`, `regelverk`, `konkurrent`, `datum`, `härlett värde`.

Omfånget säger om påståendet gäller båda språken eller bara ett. **Ett pris i kronor är inte samma värde som ett pris i dollar** — de blir två poster, och den svenska posten märks `härlett värde` med en hänvisning till dollarposten i utfallskolumnen.

Posterna som är kända sedan förarbetet och som MÅSTE finnas med:

| id | påstående | typ | not |
|---|---|---|---|
| — | Free $0 / Pro ~$20 / Max $100+ | pris | EN; plantabellen |
| — | Free 0 kr / Pro ca 200 kr / Max ca 1 000 kr+ | härlett värde | SV; hänger på dollarposten OCH kursen |
| — | "omräknade från Anthropics dollarpriser" | pris | SV; om Anthropic numera säljer i kronor är hela ramen fel, inte bara siffran — egen post, avgörs FÖRE prisposterna |
| — | "Chat (Sonnet)" på Free | modellnamn | ofastställt, se Task 3 |
| — | "tillgång till Opus" på Pro | modellnamn | ofastställt, se Task 3 |
| — | Cowork är en flik i Claude Desktop | gränssnitt | avgjort: falskt, se specens §13 |
| — | Cowork är Desktop-exklusivt | gränssnitt | avgjort: falskt |
| — | Cowork arbetar på din dator | gränssnitt | avgjort: falskt — träffar GDPR-avsnittet |
| — | "conversations may be used for model training by default" | gränssnitt | kräver inloggning |
| — | Projects är enklare än ChatGPTs custom GPTs | konkurrent | **ersätts**, inte beläggs — Johans beslut, specens §14 |
| — | EU AI Act, datum och skolors skyldigheter | regelverk | augusti 2026 har passerat |
| — | "First edition, April 2026" ×14 | datum | se specens §7 för exakta rader |
| — | Claude Docs och Claude Slides saknas i Artifacts-avsnittet | funktionsnamn | tillägg, inte rättning |

- [ ] **Steg 3: Fyll kolumnen för frågor som kräver inloggning**

Allt som ingen publicerad sida kan svara på. Formulera som ja/nej. Exempel på formen: "Står `Settings → Privacy` kvar där guiden säger, och är träningsvalet fortfarande på som standard? Ja/nej + skärmbild."

- [ ] **Steg 4: Kontrollera att varje post har alla fyra förekomster**

Varje post ska ha rad- eller avsnittshänvisning i EW, SW, EP och SP, eller ett uttryckligt `—` där påståendet inte finns på den ytan. Ett tomt fält är ett ofullständigt inventeringsarbete, inte ett `—`.

Kör som grovkontroll att inget uppenbart missats:

```bash
/usr/bin/python3 - <<'PY'
import re
rows = open('docs/guide-facts-claude.md', encoding='utf-8').read()
body = rows.split('## Poster')[1].split('## Frågor')[0]
data = [l for l in body.splitlines() if l.startswith('|') and not set(l) <= set('|-: ')]
print(f"poster: {len(data)-1}")
tomma = [l for l in data[1:] if '|  |' in l.replace('| |', '|  |')]
print(f"rader med tomt fält: {len(tomma)}")
for l in tomma[:5]: print(' ', l[:110])
PY
```

- [ ] **Steg 5: Commit**

```bash
git add -f docs/guide-facts-claude.md
git commit -m "docs(2b): inventeringen ifylld — varje volatilt påstående med sina fyra förekomster"
```

---

## Task 3: Kontrollera varje post mot officiella källor

**Filer:**
- Modifiera: `docs/guide-facts-claude.md`

**Gränssnitt:**
- Förbrukar: posttabellen från Task 2.
- Producerar: varje post har källa, kontrolldatum och utfall. Listan med inloggningsfrågor är färdig att ge Johan.

- [ ] **Steg 1: Kontrollera prisramen före prissiffrorna**

Avgör först: säljer Anthropic i kronor till satt pris, eller räknas dollarpriset om? Svaret avgör om den svenska fotnoten ska skrivas om eller bara få nya siffror. Källa: Anthropics prissida, läst med svensk marknad vald om sidan erbjuder det.

- [ ] **Steg 2: Kontrollera modellnamnen ordagrant**

Specens §14 flaggar att release notes antyder nya versioner men att uppgiften kom via en sammanfattande hämtning. **Läs sidan ordagrant** innan något skrivs. Ingen modellversion går in i guiden på andrahandsuppgift.

- [ ] **Steg 3: Kontrollera resterande poster**

Officiella källor: anthropic.com, prissidan, dokumentationen, supportartiklarna. Sekundärkällor duger inte för pris, nivå eller modellnamn.

Varje post får **källa, datum och vilken källa**. Anthropics dokumentationssida beskrev 2026-10-08 fortfarande Cowork som Desktop-lokalt medan annonseringen sade moln — när källor står mot varandra noteras båda och den nyare vinner, med noteringen att de skiljer sig.

- [ ] **Steg 4: Hantera det som ingen källa kan belägga**

Skriv om påståendet så att det inte längre hänger på faktumet, eller ta bort det. Markera utfallet `omskrivet` eller `borttaget`. **Gissa inte.**

- [ ] **Steg 5: Lämna inloggningslistan till Johan**

Ge honom listan ur inventeringens andra tabell. Vänta in svaren innan Task 8 börjar — en post som kräver inloggning och saknar svar får inte redigeras på gissning.

- [ ] **Steg 6: Commit**

```bash
git add -f docs/guide-facts-claude.md
git commit -m "docs(2b): faktakontrollen klar — källa, datum och utfall per post"
```

---

## Task 4: Selektiv fixturomfångning

**Filer:**
- Modifiera: `scripts/tests/fixtures/capture_guide_baseline.py`
- Test: `scripts/tests/test_capture_guide_baseline.py`

**Gränssnitt:**
- Förbrukar: `pdf_fingerprint.capture`, `pdf_fingerprint.BASELINE`, `pdf_body_text.BASELINE`.
- Producerar: `capture_guide_baseline.merge_baseline(existing: dict, updates: dict) -> dict` och ett `--only REL`-argument som kan anges flera gånger.

Skriptet fångar idag alla 22 PDF:er i ett svep och vägrar skriva över utan `--force`. Rundan rör fyra nycklar. En `--force`-körning skulle tyst omfånga de arton PDF:er rundan aldrig öppnat.

- [ ] **Steg 1: Skriv de misslyckade testerna**

```python
# scripts/tests/test_capture_guide_baseline.py
"""Omfångningen måste gå att rikta.

Våg 2b rör fyra av 22 nycklar. Skriptets docstring säger själv att en
--force-körning efter en ändring är liktydig med att slå av
paritetsvakten; den här filen gör det omöjligt att göra det av misstag.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from . import pdf_fingerprint as fp

_SPEC = importlib.util.spec_from_file_location(
    "capture_guide_baseline",
    Path(__file__).parent / "fixtures" / "capture_guide_baseline.py",
)

CLAUDE = [
    "assets/pdfs/guides/claude-guide-en.pdf",
    "assets/pdfs/guides/claude-guide-sv.pdf",
    "assets/pdfs/guides/claude-quick-start-en.pdf",
    "assets/pdfs/guides/claude-quick-start-sv.pdf",
]


def _module():
    mod = importlib.util.module_from_spec(_SPEC)
    mod.__name__ = "capture_guide_baseline"
    _SPEC.loader.exec_module(mod)
    return mod


def test_merge_baseline_replaces_only_named_keys():
    mod = _module()
    existing = {"a.pdf": {"pages": ["x"]}, "b.pdf": {"pages": ["y"]}}
    merged = mod.merge_baseline(existing, {"a.pdf": {"pages": ["NY"]}})
    assert merged["a.pdf"] == {"pages": ["NY"]}
    assert merged["b.pdf"] == {"pages": ["y"]}, "orörd nyckel ändrades"
    assert sorted(merged) == ["a.pdf", "b.pdf"], "nyckeluppsättningen ändrades"


def test_merge_baseline_refuses_an_unknown_key():
    mod = _module()
    with pytest.raises(KeyError):
        mod.merge_baseline({"a.pdf": {}}, {"okänd.pdf": {}})


def test_force_cannot_silently_reset_unrelated_entries():
    """Granskningsfokus 1: de arton PDF:er rundan inte öppnat ska stå still.

    Facit på disk måste fortfarande täcka exakt 22 nycklar, och de
    arton som inte är Claudes ska vara oförändrade mot det committade
    läget. Testet jämför mot git, inte mot sig självt.
    """
    import json, subprocess
    committed = json.loads(subprocess.run(
        ["git", "show", f"HEAD:{fp.BASELINE.relative_to(fp.ROOT)}"],
        capture_output=True, text=True, check=True, cwd=fp.ROOT).stdout)
    current = json.loads(fp.BASELINE.read_text(encoding="utf-8"))
    assert sorted(current) == sorted(fp.GUIDE_PDFS), "nyckeluppsättningen ändrades"
    for rel in fp.GUIDE_PDFS:
        if rel in CLAUDE:
            continue
        assert current[rel] == committed[rel], f"{rel} omfångades utan att röras"
```

- [ ] **Steg 2: Kör testerna och se att de misslyckas**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_capture_guide_baseline.py -v`
Förväntat: FAIL, `AttributeError: module 'capture_guide_baseline' has no attribute 'merge_baseline'`. Det tredje testet går igenom redan nu — det är avsiktligt, det vaktar ett tillstånd som ska förbli sant.

- [ ] **Steg 3: Skriv implementationen**

Ersätt `capture_guide_baseline.py` med:

```python
"""Fångar facit för de 22 guide-PDF:erna.

Körs den om efter en stiländring skriver den över facit med det nya
läget och paritetstestet slutar betyda något. Den vägrar därför skriva
över ett befintligt facit om inte --force anges.

--only RELATIV/SOKVAG riktar omfångningen mot namngivna PDF:er och
lämnar övriga nycklar exakt som de står. Det är det enda sättet att
omfånga en delmängd utan att slå av vakten för resten.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pdf_body_text as bt  # noqa: E402
import pdf_fingerprint as fp  # noqa: E402


def merge_baseline(existing: dict, updates: dict) -> dict:
    """Byter ut de namngivna nycklarna och lämnar resten orörda."""
    unknown = set(updates) - set(existing)
    if unknown:
        raise KeyError(f"okända nycklar: {sorted(unknown)}")
    return {**existing, **updates}


def _only_from_argv(argv: list) -> list:
    out = []
    for i, arg in enumerate(argv):
        if arg == "--only" and i + 1 < len(argv):
            out.append(argv[i + 1])
    return out


def main(argv: list) -> int:
    force = "--force" in argv
    only = _only_from_argv(argv)

    if only:
        unknown = [r for r in only if r not in fp.GUIDE_PDFS]
        if unknown:
            return _fail(f"--only fick okända sökvägar: {unknown}")
        targets = only
    else:
        if fp.BASELINE.exists() and not force:
            return _fail(
                f"{fp.BASELINE} finns redan. Kör med --only för en delmängd, "
                "eller --force bara om du MENAR att slänga hela facit — efter "
                "en ändring är det liktydigt med att slå av paritetsvakten."
            )
        targets = fp.GUIDE_PDFS

    page_updates, body_updates = {}, {}
    for rel in targets:
        path = fp.ROOT / rel
        if not path.exists():
            return _fail(f"saknas: {rel}")
        entry = fp.capture(path)
        page_updates[rel] = entry
        body_updates[rel] = bt.capture(rel)
        print(f"{len(entry['pages']):3} sidor  {len(entry['images']):2} bilder  {rel}")

    _write(fp.BASELINE, page_updates, only)
    _write(bt.BASELINE, body_updates, only)
    print(f"\nfacit skrivet: {len(targets)} PDF:er{' (delmängd)' if only else ''}")
    return 0


def _write(path: Path, updates: dict, selective: bool) -> None:
    if selective and path.exists():
        data = merge_baseline(json.loads(path.read_text(encoding="utf-8")), updates)
    else:
        data = updates
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _fail(msg: str) -> int:
    print(msg, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

- [ ] **Steg 4: Kör testerna och se att de går igenom**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_capture_guide_baseline.py -v`
Förväntat: PASS, tre tester.

- [ ] **Steg 5: Bevisa att vakten kan fallera**

Fälla 2 i överlämningen: ett test som inte kan bli rött är inget test. Bryt den med flit:

```bash
/usr/bin/python3 - <<'PY'
import json, pathlib
p = pathlib.Path('scripts/tests/fixtures/guide-pdf-baseline.json')
d = json.loads(p.read_text()); orig = p.read_text()
rel = 'assets/pdfs/presentation-skills-guide-en.pdf'
d[rel]['pages'][0] = 'SABOTAGE'
p.write_text(json.dumps(d, indent=2, sort_keys=True) + "\n")
print("saboterade", rel)
PY
/usr/bin/python3 -m pytest scripts/tests/test_capture_guide_baseline.py::test_force_cannot_silently_reset_unrelated_entries -v
```
Förväntat: FAIL med "omfångades utan att röras". Återställ sedan:
```bash
git checkout -- scripts/tests/fixtures/guide-pdf-baseline.json
```
(Här är `git checkout --` säkert: en namngiven fil, inte en katalog.)

- [ ] **Steg 6: Commit**

```bash
git add scripts/tests/fixtures/capture_guide_baseline.py scripts/tests/test_capture_guide_baseline.py
git commit -m "feat(2b): --only på fixturomfångningen, så en delmängd inte slår av vakten"
```

---

## Task 5: Det femte vaktlagret — ytorna är överens

**Filer:**
- Skapa: `scripts/tests/surfacecheck.py`
- Skapa: `scripts/tests/test_guide_surface_consistency.py`

**Gränssnitt:**
- Förbrukar: `factinventory.load()`, `factinventory.Row` från Task 1.
- Producerar: `surfacecheck.normalise(text: str) -> str` och `surfacecheck.check(rows, surfaces) -> list` som ger en lista av `Problem(id, lang, kind, detail)` där `kind` är `"saknas_på_en_yta"` eller `"finns_ingenstans"`.

Våg 2a:s fyra lager vaktar varje PDF mot den HTML den byggdes ur. Ingen vaktar webbytan mot printytan. **Konsistensen är per språk** — den svenska guiden prissätter i kronor med avsikt.

- [ ] **Steg 1: Skriv de misslyckade testerna**

```python
# scripts/tests/test_guide_surface_consistency.py
"""Webbytan och printytan ska vara överens om de volatila värdena.

Per språk, inte mellan språk: den svenska guiden prissätter i kronor
med avsikt, och en vakt som krävde samma värde över språkgränsen vore
röd från första dagen och alltså värdelös.

Vakten jämför bara de värden inventeringen pekar ut. Ytorna skiljer sig
40 % i formulering med avsikt; ordagrann likhet vore fel krav.
"""
from __future__ import annotations

import pytest

from . import factinventory, surfacecheck
from .factinventory import Row


def test_comparison_normalises_whitespace_and_dashes():
    """Granskningsfokus 3: typografi får inte göra vakten falskt röd."""
    assert surfacecheck.normalise("~$20 / mo") == surfacecheck.normalise("~$20 / mo")
    assert surfacecheck.normalise("april–2026") == surfacecheck.normalise("april-2026")
    assert surfacecheck.normalise("a  b\n c") == surfacecheck.normalise("a b c")


def test_reports_a_value_missing_from_one_surface():
    rows = [Row("P01", "en", "Second edition", "aktiv")]
    surfaces = {("en", "web"): "Second edition, October 2026", ("en", "print"): "First edition"}
    problems = surfacecheck.check(rows, surfaces)
    assert [p.kind for p in problems] == ["saknas_på_en_yta"]
    assert "print" in problems[0].detail


def test_checker_separates_typo_from_missing_on_one_surface():
    """Granskningsfokus 2: en sträng som finns ingenstans är ett stavfel
    i inventeringen, inte ett innehållsfel — annars letar redaktören fel."""
    rows = [Row("P02", "en", "Tredje upplagan", "aktiv")]
    surfaces = {("en", "web"): "Second edition", ("en", "print"): "Second edition"}
    problems = surfacecheck.check(rows, surfaces)
    assert [p.kind for p in problems] == ["finns_ingenstans"]


def test_rows_marked_borttaget_are_skipped():
    """Granskningsfokus 4: ett utgånget påstående ska inte göra vakten
    röd för alltid."""
    rows = [Row("P03", "en", "Cowork is a tab inside Claude Desktop", "borttaget")]
    surfaces = {("en", "web"): "", ("en", "print"): ""}
    assert surfacecheck.check(rows, surfaces) == []


def test_derived_rows_require_their_source_row_to_be_resolved():
    """Granskningsfokus 5: kronpriset hänger på dollarpriset. Finns en
    svensk rad för ett id, måste den engelska för samma id också finnas,
    annars kan den ena rättas utan den andra."""
    rows = [Row("P04", "sv", "ca 200 kr / mån", "aktiv")]
    surfaces = {("sv", "web"): "ca 200 kr / mån", ("sv", "print"): "ca 200 kr / mån"}
    problems = surfacecheck.check(rows, surfaces)
    assert any(p.kind == "saknar_motpart" for p in problems)


def test_the_real_inventory_parses_and_the_real_surfaces_agree():
    rows = [r for r in factinventory.load() if r.status == "aktiv"]
    if not rows:
        pytest.skip("vaktblocket är tomt — fylls i Task 8")
    problems = surfacecheck.check(rows, surfacecheck.read_surfaces())
    assert not problems, "\n".join(
        f"{p.id} [{p.lang}] {p.kind}: {p.detail}" for p in problems)
```

- [ ] **Steg 2: Kör testerna och se att de misslyckas**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -v`
Förväntat: FAIL, `ModuleNotFoundError: surfacecheck`.

- [ ] **Steg 3: Skriv implementationen**

```python
# scripts/tests/surfacecheck.py
"""Jämför guidens webbyta med dess printyta, inom ett språk.

PDF:en renderas ur print-filen, inte ur webbsidan, och de två har redan
40 % egen formulering. Ingen av våg 2a:s vakter ser skillnaden. Den här
modulen jämför bara de värden inventeringen pekar ut.
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[2]

SURFACES = {
    ("en", "web"):   "guides/claude/index.html",
    ("en", "print"): "exports/claude-print-a4-en.html",
    ("sv", "web"):   "sv/guider/claude/index.html",
    ("sv", "print"): "exports/claude-print-a4-sv.html",
}

_TAG = re.compile(r"<[^>]+>")
_SCRIPT = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)
_DASHES = dict.fromkeys(map(ord, "‐‑‒–—−"), "-")


class Problem(NamedTuple):
    id: str
    lang: str
    kind: str
    detail: str


def normalise(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).translate(_DASHES)
    return re.sub(r"\s+", " ", text).strip()


def read_surfaces(root: Path = ROOT) -> dict:
    out = {}
    for key, rel in SURFACES.items():
        raw = (root / rel).read_text(encoding="utf-8")
        out[key] = normalise(_TAG.sub(" ", _SCRIPT.sub(" ", raw)))
    return out


def check(rows, surfaces: dict) -> list:
    problems = []
    langs_by_id = {}
    for row in rows:
        if row.status != "aktiv":
            continue
        langs_by_id.setdefault(row.id, set()).add(row.lang)

    for row in rows:
        if row.status != "aktiv":
            continue
        needle = normalise(row.value)
        hits = {
            where: needle in normalise(surfaces.get((row.lang, where), ""))
            for where in ("web", "print")
        }
        if not any(hits.values()):
            problems.append(Problem(
                row.id, row.lang, "finns_ingenstans",
                f"{row.value!r} finns varken på webbytan eller printytan — "
                "sannolikt ett stavfel i inventeringen, inte ett innehållsfel"))
        elif not all(hits.values()):
            missing = [w for w, ok in hits.items() if not ok][0]
            problems.append(Problem(
                row.id, row.lang, "saknas_på_en_yta",
                f"{row.value!r} saknas på {missing}ytan"))

        if row.lang == "sv" and "en" not in langs_by_id.get(row.id, set()):
            problems.append(Problem(
                row.id, row.lang, "saknar_motpart",
                "svensk rad utan engelsk motpart — kronvärdet hänger på "
                "dollarvärdet och får inte rättas ensamt"))
    return problems
```

- [ ] **Steg 4: Kör testerna och se att de går igenom**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -v`
Förväntat: PASS. Det sista testet hoppas över (`skip`) tills vaktblocket fyllts i Task 8.

- [ ] **Steg 5: Bevisa att vakten kan fallera mot verkliga filer**

```bash
cp guides/claude/index.html /tmp/ew-backup.html
/usr/bin/python3 - <<'PY'
import pathlib
p = pathlib.Path('guides/claude/index.html')
t = p.read_text(encoding='utf-8')
assert 'April 2026' in t
p.write_text(t.replace('April 2026', 'Mars 2026', 1), encoding='utf-8')
print("ändrade ett värde på EN BARA webbytan")
PY
```
Lägg tillfälligt in `P00 | en | Pricing accurate as of April 2026 | aktiv` i vaktblocket, kör testet, och se `saknas_på_en_yta`. Återställ sedan — med `cp`, aldrig `git checkout --` på en katalog:
```bash
cp /tmp/ew-backup.html guides/claude/index.html && rm /tmp/ew-backup.html
```
Ta bort testraden ur vaktblocket.

- [ ] **Steg 6: Commit**

```bash
git add scripts/tests/surfacecheck.py scripts/tests/test_guide_surface_consistency.py
git commit -m "feat(2b): femte vaktlagret — webbytan mot printytan, per språk"
```

---

## Task 6: Hela sviten grön före grinden

**Filer:** inga ändras.

- [ ] **Steg 1: Kör hela sviten**

Kör: `/usr/bin/python3 -m pytest scripts/tests/ -q`
Förväntat: PASS. Våg 2a:s svit var 470 tester; den här rundan har lagt till tio.

- [ ] **Steg 2: Kontrollera att inget av Johans arbete rörts**

```bash
git status --short | grep -vE '^\?\? ' | grep -vE 'docs/|scripts/tests/'
```
Förväntat: tomt. Allt annat ändrat är Johans och ska inte ha rörts.

---

# ⟨ GRIND ⟩

**Redigeringen börjar INTE förrän Johan mergat PR #30.** Grenen behöver den delade `_guide-print.css`. Kontrollera innan Task 7:

```bash
gh pr view 30 --json state,mergedAt
```
Är `state` inte `MERGED`: stanna och säg till Johan. Redigera ingen yta före det — de 18 PDF:erna i #30 är binära och konflikterna är dyra.

Öppna sedan grinden:

```bash
git fetch origin && git rebase origin/main
/usr/bin/python3 -m pytest scripts/tests/ -q   # ska fortfarande vara grön efter rebase
```

---

# EFTER GRINDEN — de fyra ytorna redigeras

## Task 7: Skriv om de två bärande avsnitten, engelska

**Filer:**
- Modifiera: `guides/claude/index.html` — "Understanding the Claude ecosystem", del 3 "Cowork — agentic workflows without the terminal"
- Modifiera: `exports/claude-print-a4-en.html` — motsvarande avsnitt plus "A school leader's Cowork example"

**Gränssnitt:**
- Förbrukar: inventeringens Cowork-poster från Task 3.
- Producerar: engelsk text som Task 10 skriver en svensk motsvarighet till — **inte** översätter.

Ramen byts från "fyra platser du går till" till "ett Claude som gör olika saker beroende på vad du ber om". 101 omnämnanden över fyra ytor; de två engelska tas här.

- [ ] **Steg 1: Skriv om ekosystemavsnittet i `guides/claude/index.html`**

Avsnittet delar idag världen i Chat / Cowork / Code / Mobile. Efter sammanslagningen finns inte den uppdelningen. Den nya ramen beskriver vad Claude gör — svarar, eller tar sig an en uppgift — och var det går att nå: webb, desktop, mobil, Chrome-sidopanel, plus Claude Code för den som arbetar i terminal.

**Utrullningen måste hanteras i texten.** Sammanslagningen har nått Pro och Max; Team och Free följer. Skriv så att texten är sann oavsett vilket läge läsaren ser, i stället för att beskriva ett av dem.

- [ ] **Steg 2: Skriv om del 3**

"När ska jag välja Cowork framför Chat" är ett val som inte längre finns. Avsnittet blir ett avsnitt om agentiskt arbete: vad det är, när det lönar sig, och vad som ändras i ansvar och datahantering när Claude tar flera steg utan att stanna. Exemplen i avsnittet — de uppgifter som annars vore tre, fem eller tio kedjade prompter — håller och ska behållas; det är ramen runt dem som byts.

- [ ] **Steg 3: Rätta GDPR-avsnittet för molnkörningen**

Guiden använder lokal körning som ett dataargument mot EU-läsare. Arbetet körs nu på Anthropics servrar i en isolerad miljö. Det är en uppgift som påverkar vad en skola får göra, så den ska stå tydligt och inte gömmas i en bisats.

- [ ] **Steg 4: Spegla till `exports/claude-print-a4-en.html`**

Print-ytan har egen formulering — av 435 meningar är 260 identiska. **Skriv om den på dess egna villkor**, klistra inte in webbtexten. Print-ytan har dessutom "A school leader's Cowork example" som webbytan saknar.

- [ ] **Steg 5: Kontrollera att inga gamla påståenden står kvar**

```bash
grep -nE 'inside Claude Desktop|Desktop only|on your (own )?computer|a tab inside' \
  guides/claude/index.html exports/claude-print-a4-en.html
```
Förväntat: inga träffar som beskriver Cowork som en plats eller som lokalt körd.

- [ ] **Steg 6: Commit**

```bash
git add guides/claude/index.html exports/claude-print-a4-en.html
git commit -m "content(2b): skriv om ekosystem- och Cowork-avsnitten på engelska efter sammanslagningen"
```

---

## Task 8: Faktarättningarna på de engelska ytorna, och vaktblocket

**Filer:**
- Modifiera: `guides/claude/index.html`, `exports/claude-print-a4-en.html`
- Modifiera: `docs/guide-facts-claude.md` (vaktblocket och EW/EP-bockarna)

- [ ] **Steg 1: Rätta post för post**

Gå inventeringen uppifrån. För varje post med utfall `ändrat`: rätta på EW och EP, bocka båda. En post är inte klar förrän båda är bockade.

- [ ] **Steg 2: Ersätt ChatGPT-jämförelsen**

Johans beslut: custom GPTs håller på att försvinna, så påståendet blir fel oavsett formulering. Skriv ett påstående om vad Projects **gör** — bestående kontext över samtal — utan att jämföra med en konkurrentfunktion.

- [ ] **Steg 3: Lägg till Claude Docs och Claude Slides**

Lanserade 2026-09-16 som nya artifact-typer på alla planer. Hör in i Artifacts-avsnittet som "väsentligt nytt", inte som en rättning.

- [ ] **Steg 4: Fyll vaktblocket**

En rad per bevakat värde, `id | språk | exakt sträng | status`, med strängarna som de nu står. Poster som utgått får status `borttaget` i stället för att raderas.

- [ ] **Steg 5: Kör femte vaktlagret skarpt**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -v`
Förväntat: `test_the_real_inventory_parses_and_the_real_surfaces_agree` går nu igenom i stället för att hoppas över. Är den röd: endera ytan saknar en rättning, eller så är en sträng i blocket felstavad — felmeddelandet säger vilket.

- [ ] **Steg 6: Commit**

```bash
git add guides/claude/index.html exports/claude-print-a4-en.html
git add -f docs/guide-facts-claude.md
git commit -m "content(2b): faktarättningar på de engelska ytorna, vaktblocket fyllt"
```

---

## Task 9: Andra upplagan — fjorton datumstämplar i sex filer

**Filer:**
- Modifiera: `exports/claude-print-a4-en.html` (rad 690, 701, 848, 1577), `exports/claude-print-a4-sv.html` (fyra motsvarande), `guides/claude/index.html` (159, 1057), `sv/guider/claude/index.html` (159, 1057), `exports/claude-guide-license-en.html`, `exports/claude-guide-license-sv.html`

Quick start-filerna bär inget datum och rörs inte här.

- [ ] **Steg 1: Byt alla fjorton**

"First edition, April 2026" → "Second edition, October 2026". "Pricing accurate as of April 2026" → "Pricing accurate as of October 2026". Svenska motsvarigheter: "andra upplagan, oktober 2026", "Priserna stämmer per oktober 2026". Licensfilernas "choosewise.education · April 2026" → "· October 2026" / "· oktober 2026".

Säljer Anthropic numera i kronor till satt pris (avgjort i Task 3), skrivs den svenska fotnotens "omräknade från Anthropics dollarpriser" om här — inte bara siffran.

- [ ] **Steg 2: Kontrollera att inget står kvar**

```bash
grep -rniE 'april 2026|first edition|första upplagan' \
  guides/claude/index.html sv/guider/claude/index.html \
  exports/claude-print-a4-en.html exports/claude-print-a4-sv.html \
  exports/claude-guide-license-en.html exports/claude-guide-license-sv.html
```
Förväntat: inga träffar. Före ändringen var det fjorton.

- [ ] **Steg 3: Kontrollera att det inte står tre olika månader**

```bash
grep -rhoiE '(october|oktober) 2026' guides/claude/index.html sv/guider/claude/index.html \
  exports/claude-print-a4-*.html exports/claude-guide-license-*.html | sort | uniq -c
```
Förväntat: bara "October 2026" och "oktober 2026", inga andra månader.

- [ ] **Steg 4: Commit**

```bash
git add guides/claude/index.html sv/guider/claude/index.html \
        exports/claude-print-a4-en.html exports/claude-print-a4-sv.html \
        exports/claude-guide-license-en.html exports/claude-guide-license-sv.html
git commit -m "content(2b): andra upplagan, oktober 2026 — fjorton stämplar i sex filer"
```

---

## Task 10: De omskrivna avsnitten på svenska, i Johans röst

**Filer:**
- Modifiera: `sv/guider/claude/index.html`, `exports/claude-print-a4-sv.html`

**Gränssnitt:**
- Förbrukar: de engelska omskrivningarna från Task 7 som sakunderlag.
- Producerar: svensk text som Task 12:s röstpass inte behöver rädda.

- [ ] **Steg 1: Åberopa `voice`-skillen**

CLAUDE.md §7. Johans beslut 2026-10-08: texten ska bära hans röst. Läs skillens innehåll — den utvecklas, lita inte på minnet av den.

- [ ] **Steg 2: Skriv avsnitten på svenska**

**Översätt inte Task 7:s engelska text.** Hela anledningen till att `sv/guider/claude/index.html:292` innehåller "när det körs inne i en" är att någon översatte i stället för att skriva. Använd den engelska texten som sakunderlag — vilka påståenden som ska göras — och skriv sedan avsnittet på svenska.

- [ ] **Steg 3: Skriv print-ytans version på dess egna villkor**

Samma regel. SP-ytan har egen formulering, och print-versionen har ett avsnitt till.

- [ ] **Steg 4: Läs igenom mot ribban**

CLAUDE.md §3: skulle en svensk skolchef märka att texten är skriven av en AI eller översatt? Särskilt: genus på substantiv som bär över från engelska pronomen, och engelska sammansättningar med bindestreck.

- [ ] **Steg 5: Commit**

```bash
git add sv/guider/claude/index.html exports/claude-print-a4-sv.html
git commit -m "content(2b): ekosystem- och Cowork-avsnitten skrivna på svenska i Johans röst"
```

---

## Task 11: Faktarättningarna på de svenska ytorna

**Filer:**
- Modifiera: `sv/guider/claude/index.html`, `exports/claude-print-a4-sv.html`
- Modifiera: `docs/guide-facts-claude.md` (SW/SP-bockarna och de svenska vaktraderna)

- [ ] **Steg 1: Rätta post för post, och håll kronorna ihop med dollarn**

Varje svensk post med typen `härlett värde` hänger på sin engelska motpart. Rätta aldrig kronvärdet utan att dollarvärdet är avgjort — vakten i Task 5 blir röd med `saknar_motpart` om bara den ena finns, men den ser inte om kursen är fel.

- [ ] **Steg 2: Lägg de svenska raderna i vaktblocket**

- [ ] **Steg 3: Kör femte vaktlagret**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -v`
Förväntat: PASS, nu med både engelska och svenska rader aktiva.

- [ ] **Steg 4: Commit**

```bash
git add sv/guider/claude/index.html exports/claude-print-a4-sv.html
git add -f docs/guide-facts-claude.md
git commit -m "content(2b): faktarättningar på de svenska ytorna"
```

---

## Task 12: Röstpasset över hela den svenska guiden

**Filer:**
- Modifiera: `sv/guider/claude/index.html`, `exports/claude-print-a4-sv.html`

Hela guiden läses, inte bara de stycken som ändrats. Rytmfel syns bara när texten läses som en sammanhängande svensk text.

- [ ] **Steg 1: Åtgärda de fem belagda ställena**

| Rad | Felet | Rättningen |
|---|---|---|
| `:292` | "när det körs **inne i en**" | genusfel ur engelskans "inside one" — det heter *inne i ett* (ett Projekt) |
| `:292` | "kompetent-men-blekt" | engelsk sammansättning; skriv om på svenska |
| `:748` | "problemet policyn **adresserar**" | anglicismen CLAUDE.md §3 tar som exempel |
| `:794` | "Policyn ska **adressera**" | samma |
| `:62`, `:77`, `:292` | negativ parallellism tre gånger | översatt engelsk rytm och ett AI-tell |

Radnumren gäller filen som den stod 2026-10-08 och kan ha flyttat av tidigare uppgifter. Sök på strängen, inte på radnumret.

- [ ] **Steg 2: Prioritera promptbiblioteket**

Det är den text som lämnar guiden och hamnar i någon annans chattfönster. `:748` och `:794` står båda där.

- [ ] **Steg 3: Läs hela guiden i ett svep**

Leta efter: anglicismer, genusfel som bär över från engelska pronomen, negativ parallellism, engelska sammansättningar med bindestreck, och meningar vars rytm är engelsk även om orden är svenska.

- [ ] **Steg 4: Samma pass på print-ytan**

SP-ytan har 40 % egen formulering och måste läsas för sig.

- [ ] **Steg 5: Kontrollera att inga kända anglicismer står kvar**

```bash
grep -rniE 'adresserar|adressera|spendera tid|göra skillnad|inne i en\b' \
  sv/guider/claude/index.html exports/claude-print-a4-sv.html
```
Förväntat: inga träffar.

- [ ] **Steg 6: Kör femte vaktlagret igen**

Röstpasset kan ha ändrat en sträng som står i vaktblocket. Kör: `/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -v`. Är den röd på `saknas_på_en_yta`: uppdatera både ytan och blocket, inte bara blocket.

- [ ] **Steg 7: Commit**

```bash
git add sv/guider/claude/index.html exports/claude-print-a4-sv.html
git add -f docs/guide-facts-claude.md
git commit -m "content(2b): röstpass över hela den svenska guiden"
```

---

## Task 13: Quick start-filerna

**Filer:**
- Modifiera: `exports/claude-quick-start-en.html`, `exports/claude-quick-start-sv.html`

Quick start bär inga pris- eller modellpåståenden och inget datum. Den bär påståenden om inloggning och gratiskonto, plus DÅLIG/BÄTTRE/BÄST-raden.

- [ ] **Steg 1: Kontrollera de få påståenden som finns**

```bash
sed -e 's/<[^>]*>/ /g' exports/claude-quick-start-en.html \
  | grep -nE 'sign (in|up)|Google|Apple|free personal account|claude\.ai'
```
Stäm av mot inventeringens poster om konto och inloggning.

- [ ] **Steg 2: Rätta det som blivit fel, i båda språk**

- [ ] **Steg 3: Commit**

```bash
git add exports/claude-quick-start-en.html exports/claude-quick-start-sv.html
git commit -m "content(2b): quick start — konto- och inloggningspåståenden"
```

---

## Task 14: Rendera om de fyra PDF:erna

**Filer:**
- Modifiera: `assets/pdfs/guides/claude-guide-{en,sv}.pdf`, `assets/pdfs/guides/claude-quick-start-{en,sv}.pdf`

- [ ] **Steg 1: Rendera**

```bash
/usr/bin/python3 exports/build-claude-pdf.py
/usr/bin/python3 exports/build-claude-quickstart-pdf.py
```

- [ ] **Steg 2: Kontrollera att bara de fyra rörts**

```bash
git status --short -- assets/pdfs/
```
Förväntat: exakt fyra ändrade filer under `assets/pdfs/guides/`. Rörs `assets/pdfs/wise/` har Johans arbete påverkats — stanna.

- [ ] **Steg 3: Titta på en renderad sida**

Fälla 3 i överlämningen: fingeravtryck på text är blinda för bilder. En omrendering i våg 2a tappade åtta fotografier medan varje textkontroll passerade.

```bash
pdftoppm -png -r 60 -f 1 -l 2 assets/pdfs/guides/claude-guide-en.pdf /tmp/claude-en
pdftoppm -png -r 60 -f 1 -l 2 assets/pdfs/guides/claude-guide-sv.pdf /tmp/claude-sv
ls /tmp/claude-*.png
```
Öppna bilderna och se efter att omslaget och första uppslaget har sina bilder kvar.

- [ ] **Steg 4: Commit**

```bash
git add assets/pdfs/guides/claude-guide-en.pdf assets/pdfs/guides/claude-guide-sv.pdf \
        assets/pdfs/guides/claude-quick-start-en.pdf assets/pdfs/guides/claude-quick-start-sv.pdf
git commit -m "build(2b): rendera om Claude-guidens fyra PDF:er ur det nya innehållet"
```

---

## Task 15: Selektiv fixturomfångning

**Filer:**
- Modifiera: `scripts/tests/fixtures/guide-pdf-baseline.json`, `scripts/tests/fixtures/guide-pdf-body-baseline.json`

- [ ] **Steg 1: Omfånga bara de fyra**

```bash
/usr/bin/python3 scripts/tests/fixtures/capture_guide_baseline.py \
  --only assets/pdfs/guides/claude-guide-en.pdf \
  --only assets/pdfs/guides/claude-guide-sv.pdf \
  --only assets/pdfs/guides/claude-quick-start-en.pdf \
  --only assets/pdfs/guides/claude-quick-start-sv.pdf
```

- [ ] **Steg 2: Verifiera att diffen rör exakt fyra nycklar**

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
PY
```
Förväntat: fyra ändrade nycklar per fil, alla under `assets/pdfs/guides/claude-`. Något annat: stanna och ta reda på varför.

- [ ] **Steg 3: Kör paritets- och innehållsvakterna**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_guide_pdf_parity.py scripts/tests/test_guide_pdf_body_text.py scripts/tests/test_capture_guide_baseline.py -v`
Förväntat: PASS. `test_force_cannot_silently_reset_unrelated_entries` jämför nu mot HEAD före den här uppgiftens commit — kör den före commit, inte efter.

- [ ] **Steg 4: Commit**

```bash
git add scripts/tests/fixtures/guide-pdf-baseline.json scripts/tests/fixtures/guide-pdf-body-baseline.json
git commit -m "test(2b): omfånga facit för de fyra Claude-PDF:erna, övriga arton orörda"
```

---

## Task 16: Slutkontroll

**Filer:** `assets/` och sidmetadata kan ändras av `build-seo-meta.py`.

- [ ] **Steg 1: Kör hela sviten**

Kör: `/usr/bin/python3 -m pytest scripts/tests/ -q`
Förväntat: PASS, allt.

- [ ] **Steg 2: Kör `build-seo-meta.py` medvetet**

```bash
/usr/bin/python3 scripts/build-seo-meta.py
git status --short -- '*.html' | head -20
```
Skriptet bumpar "Last updated" ur commitdatum. Här är det korrekt — innehållet HAR ändrats. Men kontrollera att bara guidens sidor fick nytt datum, inte sidor vars innehåll inte rörts.

- [ ] **Steg 3: Gå igenom specens verifieringstabell**

Specens §12. Varje rad ska gå att bocka:

```bash
# upplagan konsekvent
grep -rniE 'april 2026|first edition' guides/claude/index.html sv/guider/claude/index.html \
  exports/claude-print-a4-*.html exports/claude-guide-license-*.html | wc -l   # ska vara 0
# fyra PDF:er, inga fler
git diff --name-only origin/main...HEAD -- assets/pdfs/ | wc -l                # ska vara 4
# anglicismer
grep -rniE 'adresserar|adressera|inne i en\b' sv/guider/claude/index.html \
  exports/claude-print-a4-sv.html | wc -l                                      # ska vara 0
```

- [ ] **Steg 4: Kontrollera att Johans arbete är orört**

```bash
git diff --name-only origin/main...HEAD | grep -E '^(exports/wise|exports/ratt|assets/pdfs/wise)' | wc -l
```
Förväntat: 0. Rör grenen någon av Johans filer har något gått fel.

- [ ] **Steg 5: Uppdatera programmets överlämning**

`docs/blueprint-handoff.md`: flytta våg 2b från "inte påbörjad" till sitt nya läge, notera att det femte vaktlagret finns och vad det äger, och att `capture_guide_baseline.py` nu har `--only`. Lägg till landningssidornas "fem guider"-överdrift under det som står öppet.

- [ ] **Steg 6: Commit och öppna PR**

```bash
git add -f docs/blueprint-handoff.md docs/guide-facts-claude.md
git commit -m "docs(2b): uppdatera överlämningen efter våg 2b"
git push -u origin feat/blueprint-wave-2b-claude-content
```
