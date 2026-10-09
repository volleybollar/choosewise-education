# Blueprint våg 2a — guidernas tryckmallar

> **För agentiska arbetare:** OBLIGATORISK UNDERSKILL: använd superpowers:subagent-driven-development (rekommenderas) eller superpowers:executing-plans för att genomföra planen uppgift för uppgift. Stegen använder kryssrutor (`- [ ]`).

**Mål:** De 27 tryckmallarna bakom guidernas 23 PDF:er byter till Blueprint — delad `exports/_guide-print.css`, självhostade typsnitt, noll Crestiora-värden — utan att ett enda ord i någon PDF ändras.

**Arkitektur:** Mallarna delar inte layout, så de delar inte layoutregler. En delad stilmall bär **tokens, typsnitt, A4-bas och de två underfamiljer som faktiskt är strukturlika** (licenssidorna 13 av 14 klasser gemensamma, quick starts 20 av 46). De tolv A4-guiderna har 130 klasser varav **en** är gemensam — de behåller sina layoutregler lokalt och hämtar bara färg och typsnitt ur de delade variablerna. Varje PDF:s textinnehåll låses med ett sidvis teckenfingeravtryck före första stilraden ändras.

**Teknikstack:** Playwright (Chromium) för rendering, pypdf för ihopsättning, pdftotext för textextraktion, pytest. `/usr/bin/python3` (3.9.6) är **enda** interpretern med pytest och playwright — Homebrews 3.14 saknar båda.

**Spec:** `docs/superpowers/specs/2026-10-05-choosewise-visual-identity-design.md` (§8 "Våg 2 — guiderna", §9 "Fällor")

**Föregående:** `docs/blueprint-handoff.md` (våg 1, mergad som `851c9f5`)

---

## Avgränsning

**Ingår:** 27 mallar → 23 PDF:er.

| Underfamilj | Mallar | Gemensamma klasser | Strategi |
|---|---|---|---|
| Licenssidor | 4 | 13 av 14 | Full delad layout i `_guide-print.css` |
| Quick starts | 10 | 20 av 46 | Delad kärna + lokala tillägg |
| A4-guider | 12 | 1 av 130 | Endast tokens och typsnitt delas, layout stannar lokalt |
| NLM-140 | 1 (genererad) | — | Ändras i `exports/build-nlm-prompts-en.py`, aldrig i HTML:en |

**Ingår inte:** diagram- och social-exporterna (`print-a4.html`, `wise-print-a4.html`, `*-linkedin-1200x1200.html`, `*-presentation-1920x1080.html`, `*-text-1200x1200.html` och deras SVG/PNG/PDF). Johans beslut 2026-10-05: egen runda senare, gärna ihop med spår A. Sju av de åtta bär dessutom hans ocommittade attributionssvep just nu.

**Ingår inte:** steg 2b (innehållets aktualitet). Egen plan efter den här.

## Globala villkor

Kopierade ordagrant ur specen och våg 1:s loggbok. Varje uppgifts krav omfattar det här avsnittet.

- **Paletten.** `--color-bg` `#FBFAF8` · `--color-bg-alt` `#EFF2F6` · `--color-text` `#0C1A2E` · `--color-text-soft` `#4E5A68` · `--color-text-muted` `#656F7B` · `--color-border` `#DDE3EA` · `--color-accent` `#0B3A6F` · `--color-deep` `#07284D` · `--color-dark-bg` `#0B3A6F` · `--color-dark-text` `#EFF2F6`.
- **Kopparn har tre värden och rollerna blandas aldrig.** `--color-highlight` `#C2793A` i **ytor och grafik, aldrig text**. `--color-highlight-ink` `#9C5A24` för **kopparfärgad text på ljus botten**. `--color-highlight-on-dark` `#E8C9A8` för **kopparfärgad text på mörkt band**. Regeln bröts fem gånger i våg 1 av olika arbetare som rimligt antog att ett värde räckte.
- **`--color-accent` och `--color-dark-bg` delar värdet `#0B3A6F`.** Accent som förgrund mot mörkt band ger 1,00:1 — osynligt. Fällan slog till två gånger i våg 1. Text på mörkt band tar `--color-dark-text` eller `--color-highlight-on-dark`.
- **Viktskalan:** display 300, rubrik 400, brödtext 400, betoning 500. **Inget utanför skalan.** Mallarnas nuvarande 600 och 700 går båda till **500**. 800/900 (Playfair Black) går till **400**.
- **Typsnitt:** Hanken Grotesk är enda typsnittet. Instrument Serif enbart i citat. Inga anrop till `fonts.googleapis.com` — alla mallar har två sådana `<link>` idag och de ska bort.
- **Innehållet är oförändrat.** Inte ett ord, en rubrik, en URL eller ett filnamn. Verifieras med sidvis teckenfingeravtryck.
- **`git add -A` används aldrig.** Repot har ~29 ocommittade poster som tillhör Johan. Filer väljs medvetet vid varje commit.
- **Arbetsflöde:** feature-branch och PR med merge-commit, inte squash.
- **Interpreter:** `/usr/bin/python3` i varje kommando. Inte `python3`.

## Granskningsfokus

Fem indataklasser specen förutsätter men ingen uppgifts tester annars når. Varje rad har fått sitt test inlagt i den uppgift som äger koden.

1. **Offline-rendering.** Mallarna hämtar typsnitt från Google idag. Renderas de utan nät faller Chromium tillbaka på systemsnitt, raderna bryts om och fingeravtrycket ändras av fel skäl. → Uppgift 2 mäter reproducerbarheten *före* någon stiländring, så skillnaden syns när den uppstår och inte när den upptäcks.
2. **Svenska tecken.** å ä ö och typografiska citattecken måste överleva typsnittsbytet. Faller renderaren tillbaka bryts radbrytningen tyst. → Uppgift 2:s fingeravtryck är en teckenmultimängd och fångar varje förlorat tecken.
3. **Innehållsfärger i NLM-dokumentet.** 228 av dess 332 hexkoder står i prompttexten ("accent color (#7FA1C3)") och är innehåll, inte krom. En svepande ersättning förstör dokumentet. → Uppgift 7 har ett test som räknar innehållshexarna före och efter.
4. **Mörka omslag.** Sex guider har mörkt omslag där build-skriptet ritar en egen sidfot i vitt. Byter omslaget bottenfärg utan att sidfoten följer med blir den osynlig. → Uppgift 6 mäter kontrasten i omslagssidfoten per guide.
5. **De fjorton opublicerade PDF:erna ligger i `_unpublished/`,** men skripten skriver till `assets/pdfs/guides/`. Körs ett skript som det står idag publiceras en opublicerad guide av misstag. → Uppgift 1 har ett test som binder varje skripts utdatasökväg till var PDF:en faktiskt ligger i git.

---

## Filstruktur

**Skapas:**
- `exports/_guide-print.css` — tokens, @font-face, A4-bas, licenslayout, quick start-kärna. Enda källan för guidernas färg och typsnitt.
- `scripts/tests/pdf_fingerprint.py` — delad hjälpmodul: `extract`, `pages`, `fingerprint`. Vanlig modul, inte testfil.
- `scripts/tests/fixtures/guide-pdf-baseline.json` — facit: per PDF, per sida, en sha256 av fingeravtrycket.
- `scripts/tests/test_build_scripts.py` — vaktar att varje build-skripts in- och utdata finns där skriptet påstår.
- `scripts/tests/test_guide_pdf_parity.py` — vaktar att de 23 PDF:ernas text är oförändrad.
- `scripts/tests/test_guide_print_css.py` — vaktar paletten, kopparrollerna, vikterna och typsnitten i guidfamiljen.
- `exports/build-guide-pdfs.py` — kör de tolv guidbyggarna i ordning. En kommandorad i stället för tolv.

**Ändras:**
- 7 build-skript i `exports/` (sökvägar)
- 26 HTML-mallar (13 i `exports/`, 14 i `_unpublished/exports/`, minus den genererade NLM-filen)
- `exports/build-nlm-prompts-en.py` (kromfärger för HTML, PDF och docx)
- `scripts/tests/test_prompt_pdf_parity.py` (importerar den nya hjälpmodulen i stället för egna kopior)

---

## Innan uppgift 1: grenen

```bash
cd /Users/johan/Projekt/Choosewise/choosewise-education
git checkout main && git pull --ff-only
git checkout -b feat/blueprint-wave-2a-guides
```

Repot har ~29 ocommittade poster som tillhör Johan och ska följa med orörda över grenbytet. Ingen av dem rör guidfamiljen — kontrollera med `git status --short | grep -E "quick-start|print-a4|license|nlm"` (förväntat: tomt) innan du börjar.

---

## Uppgift 1: Läk de sju build-skriptens sökvägar

De fjorton mallarna för Gemini/NotebookLM, Copilot, Apple Intelligence och AI för elever flyttades till `_unpublished/exports/` i commit `430f6d0`. Skripten följde inte med. De går inte att köra idag, och om de gick skulle de skriva de opublicerade PDF:erna till den publicerade katalogen.

**Filer:**
- Ändra: `exports/build-ai-for-elever-pdf.py`, `exports/build-apple-intelligence-pdf.py`, `exports/build-apple-intelligence-quickstart-pdf.py`, `exports/build-copilot-pdf.py`, `exports/build-copilot-quickstart-pdf.py`, `exports/build-gemini-notebooklm-pdf.py`, `exports/build-gemini-quickstart-pdf.py`
- Skapa: `scripts/tests/test_build_scripts.py`

**Gränssnitt:**
- Producerar: tolv körbara build-skript i `exports/`, var och en med in- och utdatasökvägar som pekar på filer som finns.

- [ ] **Steg 1: Skriv det test som ska bli rött**

```python
# scripts/tests/test_build_scripts.py
"""Build-skripten ska peka på filer som finns.

De fjorton opublicerade guidmallarna flyttades till _unpublished/exports/
i 430f6d0 men skripten följde inte med. Testet fångar både att indata
saknas och att utdata skrivs till fel katalog — ett skript som skriver en
opublicerad guide till assets/pdfs/guides/ publicerar den av misstag.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = sorted((ROOT / "exports").glob("build-*.py"))

HTML_REF = re.compile(r'["\']([\w./-]*exports/[\w.-]+\.html)["\']')
PDF_REF = re.compile(r'["\']([\w./-]*(?:assets/pdfs|_unpublished)[\w./-]*\.pdf)["\']')


def _tracked_pdfs() -> set[str]:
    out = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "*.pdf"],
        capture_output=True, text=True, check=True,
    ).stdout.split()
    return set(out)


@pytest.mark.parametrize("script", SCRIPTS, ids=lambda p: p.name)
def test_every_html_input_exists(script: Path):
    missing = [r for r in sorted(set(HTML_REF.findall(script.read_text(encoding="utf-8"))))
               if not (ROOT / r).exists()]
    assert not missing, f"{script.name} pekar på HTML som inte finns: {missing}"


@pytest.mark.parametrize("script", SCRIPTS, ids=lambda p: p.name)
def test_every_pdf_output_matches_where_the_pdf_lives(script: Path):
    """Utdatasökvägen ska vara där PDF:en faktiskt ligger i git.

    En opublicerad guide som skrivs till assets/pdfs/guides/ hamnar i
    nästa commit som publicerad.
    """
    tracked = _tracked_pdfs()
    wrong = []
    for ref in sorted(set(PDF_REF.findall(script.read_text(encoding="utf-8")))):
        if ref in tracked:
            continue
        name = Path(ref).name
        elsewhere = [t for t in tracked if Path(t).name == name]
        if elsewhere:
            wrong.append(f"{ref} -> ligger i själva verket på {elsewhere[0]}")
    assert not wrong, f"{script.name} skriver till fel katalog: {wrong}"
```

- [ ] **Steg 2: Kör testet och se det falla**

```bash
cd /Users/johan/Projekt/Choosewise/choosewise-education
/usr/bin/python3 -m pytest scripts/tests/test_build_scripts.py -q
```

Förväntat: 14 fel. Sju skript faller på `test_every_html_input_exists` (fjorton saknade mallar) och samma sju på `test_every_pdf_output_matches_where_the_pdf_lives` (fjorton PDF:er som i själva verket ligger under `_unpublished/assets/pdfs/guides/`).

- [ ] **Steg 3: Rätta sökvägarna i de sju skripten**

Varje skript bygger sökvägar som `root / "exports/<namn>.html"` och `root / "assets/pdfs/guides/<namn>.pdf"`, där `root = Path(__file__).parent.parent`. Byt prefixet i båda leden:

```bash
cd /Users/johan/Projekt/Choosewise/choosewise-education
for s in build-ai-for-elever-pdf build-apple-intelligence-pdf \
         build-apple-intelligence-quickstart-pdf build-copilot-pdf \
         build-copilot-quickstart-pdf build-gemini-notebooklm-pdf \
         build-gemini-quickstart-pdf; do
  /usr/bin/sed -i '' \
    -e 's|"exports/|"_unpublished/exports/|g' \
    -e 's|"assets/pdfs/guides/|"_unpublished/assets/pdfs/guides/|g' \
    "exports/$s.py"
done
```

Läs igenom varje ändrad rad efteråt. Skripten har även docstrings som nämner sökvägarna — rätta dem för hand, `sed`-raden ovan träffar bara strängar i kod eftersom docstringarna saknar citattecken runt sökvägen.

- [ ] **Steg 4: Kör testet och se det bli grönt**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_build_scripts.py -q
```

Förväntat: alla gröna.

- [ ] **Steg 5: Kör hela sviten**

```bash
/usr/bin/python3 -m pytest scripts/tests/ -q
```

Förväntat: 110 tidigare + de nya, alla gröna.

- [ ] **Steg 6: Commit**

```bash
git add scripts/tests/test_build_scripts.py exports/build-ai-for-elever-pdf.py \
  exports/build-apple-intelligence-pdf.py exports/build-apple-intelligence-quickstart-pdf.py \
  exports/build-copilot-pdf.py exports/build-copilot-quickstart-pdf.py \
  exports/build-gemini-notebooklm-pdf.py exports/build-gemini-quickstart-pdf.py
git commit -m "fix(exports): point the parked guide builders at _unpublished"
```

---

## Uppgift 2: Fingeravtryck, samlad byggare och reproducerbarhetsgrind

Innan en enda stilrad ändras måste två saker vara sanna: vi har facit på vad PDF:erna säger idag, och verktygskedjan kan återskapa dagens PDF:er ur oförändrade mallar. Utan det andra beviset mäter paritetstestet ingenting — det går inte att skilja en stilregression från en renderingsskillnad.

**Filer:**
- Skapa: `scripts/tests/pdf_fingerprint.py`, `scripts/tests/fixtures/guide-pdf-baseline.json`, `scripts/tests/test_guide_pdf_parity.py`, `exports/build-guide-pdfs.py`
- Ändra: `scripts/tests/test_prompt_pdf_parity.py`

**Gränssnitt:**
- Producerar: `pdf_fingerprint.extract(pdf: Path) -> str`, `pdf_fingerprint.pages(text: str) -> list[str]`, `pdf_fingerprint.fingerprint(page: str) -> str` (sha256-hex av sidans teckenmultimängd), `pdf_fingerprint.GUIDE_PDFS: list[str]` (de 23 sökvägarna, repo-relativa).
- Konsumeras av: uppgift 4, 5, 6 och 7, som alla kör `test_guide_pdf_parity.py` efter omrendering.

- [ ] **Steg 1: Skriv hjälpmodulen**

```python
# scripts/tests/pdf_fingerprint.py
"""Sidvis textfingeravtryck för PDF-paritet.

Vanlig modul, inte testfil — scripts/tests/ är ett paket, så testfiler
kan inte importera varandra direkt.

Fingeravtrycket är en teckenmultimängd PER SIDA. Varför inte ordlistan:
pdftotext tokeniserar spärrade versaler oförutsägbart ("PROMPT LIBRARY"
blir "P R O M P T L I B R A RY"), vilket gör ordjämförelser känsliga för
hur verktyget råkar dela upp text i stället för för om texten ändrats.

Känd begränsning: multimängden är blind för omkastning INOM en sida. Två
meningar som byter plats på samma sida ger samma avtryck. Den som flyttar
innehåll måste alltså titta själv — avtrycket vaktar mot att omstylingen
tappar eller lägger till tecken, inte mot medveten omredigering.
"""
from __future__ import annotations

import hashlib
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PUBLISHED_GUIDE_PDFS = [
    "assets/pdfs/guides/claude-guide-en.pdf",
    "assets/pdfs/guides/claude-guide-sv.pdf",
    "assets/pdfs/guides/claude-quick-start-en.pdf",
    "assets/pdfs/guides/claude-quick-start-sv.pdf",
    "assets/pdfs/presentation-skills-guide-en.pdf",
    "assets/pdfs/presentationsteknik-guide-sv.pdf",
    "assets/pdfs/presentation-skills-summary-en.pdf",
    "assets/pdfs/presentationsteknik-sammanfattning-sv.pdf",
    "assets/pdfs/nlm-140-prompts-en.pdf",
]

UNPUBLISHED_GUIDE_PDFS = [
    "_unpublished/assets/pdfs/guides/ai-for-elever-sv.pdf",
    "_unpublished/assets/pdfs/guides/ai-for-students-en.pdf",
    "_unpublished/assets/pdfs/guides/apple-intelligence-guide-en.pdf",
    "_unpublished/assets/pdfs/guides/apple-intelligence-guide-sv.pdf",
    "_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-en.pdf",
    "_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf",
    "_unpublished/assets/pdfs/guides/copilot-guide-en.pdf",
    "_unpublished/assets/pdfs/guides/copilot-guide-sv.pdf",
    "_unpublished/assets/pdfs/guides/copilot-quick-start-en.pdf",
    "_unpublished/assets/pdfs/guides/copilot-quick-start-sv.pdf",
    "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-en.pdf",
    "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-sv.pdf",
    "_unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-en.pdf",
    "_unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-sv.pdf",
]

GUIDE_PDFS = PUBLISHED_GUIDE_PDFS + UNPUBLISHED_GUIDE_PDFS

BASELINE = Path(__file__).parent / "fixtures" / "guide-pdf-baseline.json"


def extract(pdf: Path) -> str:
    return subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"],
        capture_output=True, text=True, check=True,
    ).stdout


def pages(text: str) -> list[str]:
    return text.split("\f")


def fingerprint(page: str) -> str:
    counts = Counter("".join(page.split()))
    canonical = "".join(f"{ch}{counts[ch]}" for ch in sorted(counts))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def fingerprints(pdf: Path) -> list[str]:
    return [fingerprint(p) for p in pages(extract(pdf))]
```

- [ ] **Steg 2: Skriv skriptet som fångar facit**

```python
# scripts/tests/fixtures/capture_guide_baseline.py
"""Fångar facit för de 23 guide-PDF:erna. Körs EN gång, före stilbytet.

Körs den igen efter en stiländring skriver den över facit med det nya
läget och paritetstestet slutar betyda något. Den vägrar därför skriva
över en befintlig fixtur om inte --force anges.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pdf_fingerprint as fp  # noqa: E402

force = "--force" in sys.argv
if fp.BASELINE.exists() and not force:
    sys.exit(f"{fp.BASELINE} finns redan. Kör med --force bara om du MENAR att "
             "slänga facit — efter en stiländring är det liktydigt med att "
             "slå av paritetsvakten.")

data = {}
for rel in fp.GUIDE_PDFS:
    path = fp.ROOT / rel
    if not path.exists():
        sys.exit(f"saknas: {rel}")
    data[rel] = fp.fingerprints(path)
    print(f"{len(data[rel]):3} sidor  {rel}")

fp.BASELINE.parent.mkdir(parents=True, exist_ok=True)
fp.BASELINE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"\nfacit skrivet: {fp.BASELINE} ({len(data)} PDF:er)")
```

- [ ] **Steg 3: Fånga facit från de committade PDF:erna**

```bash
cd /Users/johan/Projekt/Choosewise/choosewise-education
git status --short assets/pdfs _unpublished/assets/pdfs
```

Förväntat: `assets/pdfs/wise/*.pdf` kan vara ändrade (Johans svep, utanför den här planen). **Ingen av de 23 guide-PDF:erna får vara ändrad** — facit ska tas från det som ligger i git. Är någon av dem smutsig: stanna och fråga Johan.

```bash
/usr/bin/python3 scripts/tests/fixtures/capture_guide_baseline.py
```

Förväntat: 23 rader med sidantal, sedan `facit skrivet`.

- [ ] **Steg 4: Skriv paritetstestet**

```python
# scripts/tests/test_guide_pdf_parity.py
"""Omstylingen får inte ändra ett ord i guide-PDF:erna.

Facit ligger committat i fixtures/guide-pdf-baseline.json och togs från
PDF:erna som de såg ut före stilbytet. Ett rött test här betyder antingen
att texten faktiskt flyttat sig, eller att renderaren bytt typsnitt mitt i
(svenska tecken som faller tillbaka på ett systemsnitt bryter raderna).
Båda ska stoppa arbetet.
"""
from __future__ import annotations

import json

import pytest

from . import pdf_fingerprint as fp

BASELINE = json.loads(fp.BASELINE.read_text(encoding="utf-8"))


@pytest.mark.parametrize("rel", fp.GUIDE_PDFS)
def test_text_is_unchanged(rel: str):
    path = fp.ROOT / rel
    assert path.exists(), f"{rel} saknas"
    before = BASELINE[rel]
    after = fp.fingerprints(path)
    assert len(after) == len(before), (
        f"{rel}: {len(before)} sidor före, {len(after)} efter — sidbrytningen flyttade sig"
    )
    moved = [i + 1 for i, (b, a) in enumerate(zip(before, after)) if b != a]
    assert not moved, f"{rel}: texten ändrad på sida {moved}"


def test_baseline_covers_every_guide_pdf():
    """Facit ska inte tappa en PDF tyst."""
    assert sorted(BASELINE) == sorted(fp.GUIDE_PDFS)


def test_fingerprint_catches_a_single_character_change():
    """Beviset att vakten kan bli röd på det den vaktar."""
    assert fp.fingerprint("Hanken Grotesk") != fp.fingerprint("Hanken Grotesl")


def test_fingerprint_ignores_whitespace_only_differences():
    """Spärrad text tokeniseras olika av pdftotext utan att innehållet rört sig."""
    assert fp.fingerprint("P R O M P T") == fp.fingerprint("PROMPT")
```

- [ ] **Steg 5: Kör paritetstestet mot de orörda PDF:erna**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_pdf_parity.py -q
```

Förväntat: alla gröna (facit togs just från samma filer).

- [ ] **Steg 6: Skriv den samlade byggaren**

```python
#!/usr/bin/env python3
# exports/build-guide-pdfs.py
"""Kör alla guidbyggare i ordning. Tolv skript, en kommandorad.

  /usr/bin/python3 exports/build-guide-pdfs.py           # alla
  /usr/bin/python3 exports/build-guide-pdfs.py claude    # bara de som matchar

Skriptet bygger inget själv — det startar de befintliga byggarna, så att
omrendering efter en stiländring är ett steg och inte tolv.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
BUILDERS = [
    "build-claude-pdf.py",
    "build-claude-quickstart-pdf.py",
    "build-presentationsteknik-pdf.py",
    "build-presentationsteknik-quickstart-pdf.py",
    "build-nlm-prompts-en.py",
    "build-gemini-notebooklm-pdf.py",
    "build-gemini-quickstart-pdf.py",
    "build-copilot-pdf.py",
    "build-copilot-quickstart-pdf.py",
    "build-apple-intelligence-pdf.py",
    "build-apple-intelligence-quickstart-pdf.py",
    "build-ai-for-elever-pdf.py",
]

needle = sys.argv[1] if len(sys.argv) > 1 else ""
selected = [b for b in BUILDERS if needle in b]
if not selected:
    sys.exit(f"inget byggskript matchar {needle!r}")

failed = []
for name in selected:
    print(f"\n=== {name} ===", flush=True)
    result = subprocess.run([sys.executable, str(HERE / name)])
    if result.returncode != 0:
        failed.append(name)

print()
if failed:
    sys.exit("misslyckades: " + ", ".join(failed))
print(f"klart: {len(selected)} byggskript")
```

- [ ] **Steg 7: Reproducerbarhetsgrinden — rendera om allt ur OFÖRÄNDRADE mallar**

Det här är uppgiftens egentliga poäng. Ingen mall har ändrats än, så PDF:erna ska komma ut identiska.

```bash
cd /Users/johan/Projekt/Choosewise/choosewise-education
/usr/bin/python3 exports/build-guide-pdfs.py
/usr/bin/python3 -m pytest scripts/tests/test_guide_pdf_parity.py -q
```

Förväntat: grönt. **Blir det rött: stanna.** Det betyder att verktygskedjan inte återskapar dagens PDF:er, och då kan paritetstestet inte skilja en stilregression från en renderingsskillnad senare. Troligaste orsaken är att mallarna hämtar typsnitt från `fonts.googleapis.com` och att nätet eller Googles svar skiljer sig mellan körningarna. Dokumentera vilka PDF:er som rör sig och hur mycket, och ta det till Johan innan arbetet fortsätter — en mall vars text rör sig redan vid en nollställd omrendering kan inte vaktas av paritetstestet och måste granskas okulärt i stället.

```bash
git checkout -- assets/pdfs _unpublished/assets/pdfs   # kasta omrenderingen, facit står kvar
```

- [ ] **Steg 8: Låt prompttestet använda samma hjälpmodul**

`scripts/tests/test_prompt_pdf_parity.py` har egna kopior av `extract`, `_pages` och `_fingerprint`. Ersätt dem med import från `pdf_fingerprint`. Behåll dess `/tmp`-baserade facit och dess egna tester — bara dubbletterna försvinner.

```python
from . import pdf_fingerprint as fp

extract = fp.extract
_pages = fp.pages
_fingerprint = fp.fingerprint
```

- [ ] **Steg 9: Kör hela sviten**

```bash
/usr/bin/python3 -m pytest scripts/tests/ -q
```

Förväntat: allt grönt. Prompttestets egna tester kan hoppas över om `/tmp/pdf-parity-before` saknas — det är dess dokumenterade beteende och inte ett fel.

- [ ] **Steg 10: Commit**

```bash
git add scripts/tests/pdf_fingerprint.py scripts/tests/test_guide_pdf_parity.py \
  scripts/tests/test_prompt_pdf_parity.py scripts/tests/fixtures/ exports/build-guide-pdfs.py
git commit -m "test(guides): lock the 23 guide PDFs to a committed text baseline"
```

---

## Uppgift 3: `_guide-print.css` — tokens, typsnitt och A4-bas

**Filer:**
- Skapa: `exports/_guide-print.css`
- Skapa: `scripts/tests/test_guide_print_css.py`

**Gränssnitt:**
- Producerar: `exports/_guide-print.css` med `:root`-variablerna i Globala villkor, `@font-face` för Hanken Grotesk och Instrument Serif, samt klasserna `.page`, `.page-footer`, `.page-num` som quick starts och licenssidorna delar.
- Konsumeras av: uppgift 4, 5 och 6, som länkar filen med `<link rel="stylesheet" href="_guide-print.css">` (mallarna i `exports/`) respektive `href="../../exports/_guide-print.css"` (mallarna i `_unpublished/exports/`).

Typsnittssökvägen inuti CSS:en är relativ **CSS-filens** läge, inte HTML-filens. `../assets/fonts/...` fungerar därför för båda uppsättningarna mallar. Det är skälet till att det räcker med en fil.

- [ ] **Steg 1: Skriv vakten först**

```python
# scripts/tests/test_guide_print_css.py
"""Guidernas delade stilmall ska bära Blueprint och inget annat.

Kopparns tre roller blandades fem gånger i våg 1. Reglerna nedan är
skrivna för att bli röda på just det, inte bara på att värdena finns.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CSS = ROOT / "exports" / "_guide-print.css"

CRESTIORA = ["#1B2733", "#C8A86B", "#F6F3EE"]
OLD_CHOOSEWISE = ["#2d5a3f", "#f7f4ec", "#1e1e1c"]
BLUEPRINT = {
    "--color-bg": "#FBFAF8", "--color-bg-alt": "#EFF2F6",
    "--color-text": "#0C1A2E", "--color-text-soft": "#4E5A68",
    "--color-text-muted": "#656F7B", "--color-border": "#DDE3EA",
    "--color-accent": "#0B3A6F", "--color-deep": "#07284D",
    "--color-highlight": "#C2793A", "--color-highlight-ink": "#9C5A24",
    "--color-highlight-on-dark": "#E8C9A8",
    "--color-dark-bg": "#0B3A6F", "--color-dark-text": "#EFF2F6",
}


def css() -> str:
    return CSS.read_text(encoding="utf-8")


def test_every_blueprint_token_is_defined_with_the_right_value():
    text = css()
    for token, value in BLUEPRINT.items():
        assert re.search(rf"{re.escape(token)}\s*:\s*{value}\s*;", text, re.I), \
            f"{token} saknas eller har fel värde (ska vara {value})"


def test_no_old_palette_values_anywhere():
    text = css()
    for value in CRESTIORA + OLD_CHOOSEWISE:
        assert value.lower() not in text.lower(), f"{value} lever kvar i den delade mallen"


def test_hex_colours_appear_only_in_the_root_block():
    """Varje färg ska komma ur en variabel. Undantaget är :root självt och
    @font-face, som inte har färger alls."""
    text = css()
    root = re.search(r":root\s*\{.*?\}", text, re.S)
    assert root, ":root-blocket saknas"
    outside = text[: root.start()] + text[root.end():]
    stray = re.findall(r"#[0-9a-fA-F]{3,8}\b", outside)
    assert not stray, f"hårdkodade färger utanför :root: {sorted(set(stray))}"


def test_fonts_are_self_hosted():
    text = css()
    assert "fonts.googleapis.com" not in text
    assert "assets/fonts/hanken-grotesk/HankenGrotesk-VariableFont.woff2" in text
    for rel in re.findall(r"url\('([^']+)'\)", text):
        assert (CSS.parent / rel).resolve().exists(), f"typsnittsfilen saknas: {rel}"


def test_no_font_weight_outside_the_scale():
    """Display 300, rubrik 400, brödtext 400, betoning 500. Inget annat."""
    weights = re.findall(r"font-weight:\s*(\d{3})", css())
    outside = sorted({w for w in weights if w not in {"300", "400", "500"}})
    assert not outside, f"vikter utanför skalan: {outside}"


def test_copper_is_never_used_as_text_colour():
    """--color-highlight är ytfärg. Kopparfärgad text tar -ink eller -on-dark.

    Regeln bröts fem gånger i våg 1 av arbetare som antog att ett värde
    räckte, så vakten läser varje color-deklaration och inte bara filen.
    """
    bad = [m for m in re.findall(r"(?<!-)color:\s*var\(([^)]+)\)", css())
           if m.strip() == "--color-highlight"]
    assert not bad, "--color-highlight används som textfärg; ta --color-highlight-ink " \
                    "på ljus botten eller --color-highlight-on-dark på mörkt band"
```

- [ ] **Steg 2: Kör vakten och se den falla**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_print_css.py -q
```

Förväntat: alla fel med `FileNotFoundError` — filen finns inte än.

- [ ] **Steg 3: Skriv `exports/_guide-print.css`**

Spegla `exports/prompts/_prompt-print.css` i uppbyggnad. Filen innehåller, i den här ordningen:

```css
/* ════════════════════════════════════════════════════════
   Delad A4-tryckstil för choosewise.educations guider.
   Används av licenssidorna, quick starts och A4-guiderna.
   A4-guiderna har egen layout och hämtar bara färg och
   typsnitt härifrån — deras klassvokabulär delas inte.
   ════════════════════════════════════════════════════════ */

:root {
  --color-bg:                #FBFAF8;
  --color-bg-alt:            #EFF2F6;
  --color-text:              #0C1A2E;
  --color-text-soft:         #4E5A68;
  --color-text-muted:        #656F7B;
  --color-border:            #DDE3EA;
  --color-accent:            #0B3A6F;
  --color-deep:              #07284D;

  /* Kopparn har tre värden. Ytor och grafik tar --color-highlight, aldrig text.
     Kopparfärgad TEXT tar --color-highlight-ink på ljusa ytor
     eller --color-highlight-on-dark på mörka band. */
  --color-highlight:         #C2793A;
  --color-highlight-ink:     #9C5A24;
  --color-highlight-on-dark: #E8C9A8;

  /* --color-dark-bg har SAMMA värde som --color-accent. Accent som
     förgrund mot mörkt band ger 1,00:1 — använd --color-dark-text. */
  --color-dark-bg:           #0B3A6F;
  --color-dark-text:         #EFF2F6;

  --font-display: 'Hanken Grotesk', Helvetica, sans-serif;
  --font-body:    'Hanken Grotesk', Helvetica, sans-serif;
  --font-quote:   'Instrument Serif', Georgia, serif;
}

@font-face {
  font-family: 'Hanken Grotesk';
  src: url('../assets/fonts/hanken-grotesk/HankenGrotesk-VariableFont.woff2') format('woff2');
  font-weight: 300 600;
  font-style: normal;
}
/* Instrument Serif enbart i citat. Mallarna sätter underrubriker och
   signaturer i kursiv serif idag (Playfair italic), så kursiven behövs. */
@font-face {
  font-family: 'Instrument Serif';
  src: url('../assets/fonts/instrument-serif/InstrumentSerif-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
}
@font-face {
  font-family: 'Instrument Serif';
  src: url('../assets/fonts/instrument-serif/InstrumentSerif-Italic.woff2') format('woff2');
  font-weight: 400;
  font-style: italic;
}

/* ── A4-bas, delad av alla tre underfamiljerna ── */
@page { size: A4; margin: 0; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html { background: var(--color-bg); }
body {
  font-family: var(--font-body);
  color: var(--color-text);
  background: var(--color-bg);
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
.page { width: 210mm; height: 297mm; display: flex; flex-direction: column; }

/* ── Licenssidan: 13 av 14 klasser är gemensamma mellan de fyra
      licensmallarna, så hela layouten bor här. Skrivs i uppgift 4. ── */

/* ── Quick start: 20 av 46 klasser är gemensamma mellan de tio
      quick start-mallarna. Kärnan bor här, resten lokalt. Uppgift 5. ── */
```

Sidspecifik `padding` på `.page` skiljer mellan underfamiljerna (licens 36/28 mm, quick start 18/20 mm) och sätts därför i respektive underfamiljs block, inte i basen.

- [ ] **Steg 4: Kör vakten och se den bli grön**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_print_css.py -q
```

Förväntat: alla gröna.

- [ ] **Steg 5: Commit**

```bash
git add exports/_guide-print.css scripts/tests/test_guide_print_css.py
git commit -m "feat(guides): add the shared Blueprint print stylesheet"
```

---

## Uppgift 4: Licenssidorna (4 mallar, 2 PDF:er berörs)

De fyra licensmallarna delar 13 av 14 klasser och har 15–16 hårdkodade färger var. Hela layouten flyttar till den delade filen.

**Filer:**
- Ändra: `exports/claude-guide-license-en.html`, `exports/claude-guide-license-sv.html`, `exports/presentation-skills-license-en.html`, `exports/presentationsteknik-license-sv.html`
- Ändra: `exports/_guide-print.css` (licensblocket)

**Gränssnitt:**
- Konsumerar: tokens och `.page` från uppgift 3.
- Producerar: klasserna `.eyebrow`, `.title`, `.subtitle`, `.divider`, `.body`, `.terms`, `.term-row`, `.term-label`, `.term-body`, `.link`, `.signature`, `.attribution` i `_guide-print.css`.

Licenssidan är sista sidan i `claude-guide-{en,sv}.pdf` och `presentation-skills-guide-en.pdf` / `presentationsteknik-guide-sv.pdf`. Den har ingen egen PDF.

- [ ] **Steg 1: Flytta licenslayouten till den delade filen**

Utgå från `exports/claude-guide-license-en.html`:s `<style>`-block och översätt varje färg och vikt:

| Idag | Blueprint |
|---|---|
| `color: #1A1A1F` (body) | `var(--color-text)` |
| `background: #F6F3EE` | `var(--color-bg)` |
| `.eyebrow { color: #C8A86B }` | `var(--color-highlight-ink)` — koppar som **text** på ljus botten |
| `.title { font-family: 'Playfair Display'; color: #1B2733 }` | `var(--font-display)`, `var(--color-text)` |
| `.subtitle { 'Playfair Display' italic; color: #6B7280 }` | `var(--font-quote)`, `var(--color-text-muted)` |
| `.divider { background: #C8A86B }` | `var(--color-highlight)` — koppar som **yta** |
| `.body { color: #3A3A38 }` | `var(--color-text-soft)` |
| `.body strong { color: #1B2733; font-weight: 600 }` | `var(--color-text)`, `font-weight: 500` |
| `.term-row { border-bottom: 1px solid rgba(27,39,51,0.08) }` | `1px solid var(--color-border)` |
| `.term-label { font-weight: 600; color: #1B2733 }` | `font-weight: 500`, `var(--color-text)` |
| `.link { color: #1B2733; border-bottom: 1px solid #C8A86B }` | `var(--color-accent)`, `1px solid var(--color-highlight)` |
| `.signature { 'Playfair Display' italic; color: #1B2733 }` | `var(--font-quote)`, `var(--color-text)` |
| `.attribution { color: #6B7280 }` | `var(--color-text-muted)` |

Lägg blocket under rubriken `/* ── Licenssidan ── */` i `_guide-print.css`, med `.page` -varianten `padding: 36mm 28mm; justify-content: center; text-align: center;` i en `.page--license`-klass.

- [ ] **Steg 2: Byt ut de fyra mallarnas huvuden**

I varje av de fyra filerna: ta bort de två `<link>`-raderna till `fonts.googleapis.com`, ta bort hela `<style>`-blocket, och lägg in

```html
<link rel="stylesheet" href="_guide-print.css">
```

Byt `<div class="page">` till `<div class="page page--license">`. Rör ingenting annat i markup.

- [ ] **Steg 3: Kontrollera att ingen färg blev kvar**

```bash
cd /Users/johan/Projekt/Choosewise/choosewise-education
grep -nE '#[0-9a-fA-F]{3,8}|googleapis|Playfair|Inter' \
  exports/claude-guide-license-*.html exports/presentation-skills-license-en.html \
  exports/presentationsteknik-license-sv.html
```

Förväntat: inga träffar.

- [ ] **Steg 4: Rendera om de fyra berörda PDF:erna**

```bash
/usr/bin/python3 exports/build-guide-pdfs.py claude-pdf
/usr/bin/python3 exports/build-guide-pdfs.py presentationsteknik-pdf
```

- [ ] **Steg 5: Paritet**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_pdf_parity.py -q -k "claude-guide or presentation-skills-guide or presentationsteknik-guide"
```

Förväntat: grönt. Rött betyder att texten flyttat sig — stanna och jämför sida för sida innan något annat görs.

- [ ] **Steg 6: Titta på sidan**

```bash
/usr/bin/python3 -c "
import subprocess
subprocess.run(['pdftoppm','-png','-r','110','-f','1','-l','1',
  'assets/pdfs/guides/claude-guide-en.pdf','/tmp/licens-en'])"
open /tmp/licens-en-1.png
```

Granska: kopparn ska synas som linje och ögonbryn, aldrig som brödtext. Ingen text får ligga blått mot blått.

- [ ] **Steg 7: Hela sviten och commit**

```bash
/usr/bin/python3 -m pytest scripts/tests/ -q
git add exports/_guide-print.css exports/claude-guide-license-en.html \
  exports/claude-guide-license-sv.html exports/presentation-skills-license-en.html \
  exports/presentationsteknik-license-sv.html assets/pdfs/guides/claude-guide-en.pdf \
  assets/pdfs/guides/claude-guide-sv.pdf assets/pdfs/presentation-skills-guide-en.pdf \
  assets/pdfs/presentationsteknik-guide-sv.pdf
git commit -m "feat(guides): move the licence page onto the shared stylesheet"
```

---

## Uppgift 5: Quick starts (10 mallar, 10 PDF:er)

De tio quick start-mallarna delar 20 klasser: `brand closing eyebrow idx label lede license-line masthead msg name page page-footer page-num page1 page2 section subtitle text url watchout`. De bor i den delade filen. De 26 resterande klasserna är guidespecifika och stannar i respektive mall.

**Filer:**
- Ändra: `exports/claude-quick-start-en.html`, `exports/claude-quick-start-sv.html`, `exports/presentation-skills-quick-start-en.html`, `exports/presentationsteknik-quick-start-sv.html`, `_unpublished/exports/apple-intelligence-quick-start-{en,sv}.html`, `_unpublished/exports/copilot-quick-start-{en,sv}.html`, `_unpublished/exports/gemini-notebooklm-quick-start-{en,sv}.html`
- Ändra: `exports/_guide-print.css` (quick start-kärnan)

**Gränssnitt:**
- Konsumerar: tokens och `.page` från uppgift 3.
- Producerar: de 20 delade klasserna i `_guide-print.css`, med `.page--quickstart { padding: 18mm 20mm; }`.

De fyra svenska och engelska claude/presentationsteknik-mallarna kör gammal choosewise-palett (`#1e1e1c`, `#f7f4ec`, `#2f4a3a`, Fraunces/Work Sans). De sex opublicerade kör Crestiora (`#1B2733`, `#C8A86B`, Playfair/Inter). Översätt båda till samma tokens:

| Gammal choosewise | Crestiora | Blueprint |
|---|---|---|
| `#1e1e1c` text | `#1A1A1F` / `#1B2733` | `var(--color-text)` |
| `#f7f4ec` botten | `#F6F3EE` | `var(--color-bg)` |
| `#3a3a38` brödtext | `#3A3A38` | `var(--color-text-soft)` |
| `#5a5a57` / `#a5a59f` dämpat | `#6B7280` | `var(--color-text-muted)` |
| `#2f4a3a` skogsgrön accent | `#1B2733` | `var(--color-accent)` |
| terrakotta / `#C8A86B` som yta | `#C8A86B` | `var(--color-highlight)` |
| terrakotta / `#C8A86B` som text | `#C8A86B` | `var(--color-highlight-ink)` |
| `rgba(30,30,28,0.12)` hårlinje | `rgba(27,39,51,0.08)` | `var(--color-border)` |
| `'Fraunces'` / `'Playfair Display'` | — | `var(--font-display)` |
| `'Work Sans'` / `'Inter'` | — | `var(--font-body)` |
| `font-weight: 600` | `600` | `500` |

- [ ] **Steg 1: Skriv quick start-kärnan i `_guide-print.css`**

Utgå från `exports/claude-quick-start-en.html`:s block för de 20 delade klasserna och översätt enligt tabellen. `.watchout` är rutan som i våg 1 fick skilja sig genom **form, inte kulör** — den behåller sin stapel och svaga kopparfyllning (`background` ur `--color-highlight` med låg opacitet, stapel i `--color-highlight`, etikett i `--color-highlight-ink`).

- [ ] **Steg 2: Konvertera de tio mallarna en i taget**

För varje fil: ta bort de två googleapis-`<link>`:arna, lägg in stilmallslänken, ta bort de 20 delade klassernas regler ur det lokala `<style>`-blocket, och översätt de kvarvarande lokala reglerna enligt tabellen.

Länkens sökväg skiljer:

```html
<!-- exports/*.html -->
<link rel="stylesheet" href="_guide-print.css">
<!-- _unpublished/exports/*.html -->
<link rel="stylesheet" href="../../exports/_guide-print.css">
```

- [ ] **Steg 3: Kontrollera att ingen gammal färg blev kvar**

```bash
grep -nliE '#1B2733|#C8A86B|#F6F3EE|#f7f4ec|#2f4a3a|#1e1e1c|Playfair|Fraunces|Work Sans|googleapis' \
  exports/*quick-start*.html _unpublished/exports/*quick-start*.html
```

Förväntat: inga träffar.

- [ ] **Steg 4: Rendera om och mät paritet**

```bash
/usr/bin/python3 exports/build-guide-pdfs.py quickstart
/usr/bin/python3 -m pytest scripts/tests/test_guide_pdf_parity.py -q -k "quick-start or summary or sammanfattning"
```

Förväntat: tio gröna.

- [ ] **Steg 5: Titta på en svensk och en engelsk sida**

```bash
for p in assets/pdfs/guides/claude-quick-start-sv.pdf \
         _unpublished/assets/pdfs/guides/copilot-quick-start-en.pdf; do
  /usr/bin/python3 -c "
import subprocess,sys
pdf=sys.argv[1]; out='/tmp/'+pdf.split('/')[-1][:-4]
subprocess.run(['pdftoppm','-png','-r','110','-f','1','-l','2',pdf,out])" "$p"
done
open /tmp/claude-quick-start-sv-1.png /tmp/copilot-quick-start-en-1.png
```

Granska särskilt: å ä ö i rubriker, `.watchout`-rutan, sidfotens sidnummer.

- [ ] **Steg 6: Hela sviten och commit**

```bash
/usr/bin/python3 -m pytest scripts/tests/ -q
git add exports/_guide-print.css exports/*quick-start*.html \
  _unpublished/exports/*quick-start*.html assets/pdfs/guides/claude-quick-start-*.pdf \
  assets/pdfs/presentation-skills-summary-en.pdf \
  assets/pdfs/presentationsteknik-sammanfattning-sv.pdf \
  _unpublished/assets/pdfs/guides/*quick-start*.pdf
git commit -m "feat(guides): move the ten quick starts onto the shared stylesheet"
```

---

## Uppgift 6: A4-guiderna (12 mallar, 10 PDF:er)

130 klasser, en gemensam. De här mallarna får **inte** tvingas in i en delad layout — det skulle betyda att skriva om tolv bespoke-dokument till en vokabulär ingen av dem har. De länkar den delade filen för tokens, typsnitt och A4-bas, och behåller sina egna layoutregler lokalt med färgerna hämtade ur variablerna.

**Filer:**
- Ändra: `exports/claude-print-a4-{en,sv}.html`, `exports/presentation-skills-print-a4-en.html`, `exports/presentationsteknik-print-a4-sv.html`, `_unpublished/exports/ai-for-{elever-print-a4-sv,students-print-a4-en}.html`, `_unpublished/exports/apple-intelligence-print-a4-{en,sv}.html`, `_unpublished/exports/copilot-print-a4-{en,sv}.html`, `_unpublished/exports/gemini-notebooklm-print-a4-{en,sv}.html`

**Gränssnitt:**
- Konsumerar: tokens, `@font-face` och `.page` från uppgift 3. Inga nya delade klasser produceras.

Sex av guiderna har **mörkt omslag** och renderas i två pass av sina build-skript: omslaget utan sidfot eller med vit titel, sidorna därefter med grå sidfot. Omslagets bottenfärg går till `var(--color-dark-bg)` och all text på det till `var(--color-dark-text)` eller `var(--color-highlight-on-dark)`. **Aldrig** `var(--color-accent)` som förgrund — det är samma värde som bottnen.

- [ ] **Steg 1: Konvertera en guide först och titta på den**

Börja med `exports/claude-print-a4-en.html` (63 färgförekomster, 12 unika — störst och mest representativ). Byt huvudet, översätt varje färg enligt tabellen i uppgift 5, mappa vikterna 600 och 700 till 500 och 800/900 till 400.

```bash
/usr/bin/python3 exports/build-guide-pdfs.py claude-pdf
/usr/bin/python3 -m pytest scripts/tests/test_guide_pdf_parity.py -q -k claude-guide-en
/usr/bin/python3 -c "
import subprocess
subprocess.run(['pdftoppm','-png','-r','110','-f','1','-l','4',
  'assets/pdfs/guides/claude-guide-en.pdf','/tmp/claude-a4'])"
open /tmp/claude-a4-1.png
```

Visa omslaget för Johan innan de elva andra följer samma mönster. Det är här formspråket i tryck avgörs.

- [ ] **Steg 2: Mät omslagssidfotens kontrast**

```python
# /tmp/matt-omslag.py  — körs med /usr/bin/python3
from PIL import Image
import sys

def lum(rgb):
    def c(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (c(x) for x in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)))
    return (lb + 0.05) / (la + 0.05)

img = Image.open(sys.argv[1]).convert("RGB")
w, h = img.size
# sidfotszonen: nedersta 8 % av omslaget
zone = img.crop((0, int(h * 0.92), w, h))
colours = sorted(zone.getcolors(zone.size[0] * zone.size[1]), reverse=True)[:2]
(_, bg), (_, fg) = colours[0], colours[1]
print(f"botten {bg}  text {fg}  kontrast {ratio(bg, fg):.2f}:1")
```

Kravet är minst 4,5:1. Får du 1,00:1 har accent hamnat mot mörkt band — fällan ur våg 1.

- [ ] **Steg 3: Konvertera de elva övriga**

Samma mönster. Efter varje fil: `grep` på gamla värden, rendera om den guidens PDF, kör dess paritetstest.

- [ ] **Steg 4: Kontrollera hela underfamiljen**

```bash
grep -nliE '#1B2733|#C8A86B|#F6F3EE|#f7f4ec|#2d5a3f|#1e1e1c|Playfair|Fraunces|Work Sans|googleapis' \
  exports/*print-a4*.html _unpublished/exports/*print-a4*.html
```

Förväntat: inga träffar. (`exports/print-a4.html` och `exports/wise-print-a4.html` är diagramexporterna och ligger **utanför** planen — de ska fortfarande ge träff. Kontrollera att det bara är de två.)

- [ ] **Steg 5: Rendera om allt och mät paritet på alla 23**

```bash
/usr/bin/python3 exports/build-guide-pdfs.py
/usr/bin/python3 -m pytest scripts/tests/test_guide_pdf_parity.py -q
```

Förväntat: 23 gröna (NLM är ännu oförändrad och ska också vara grön).

- [ ] **Steg 6: Commit**

```bash
/usr/bin/python3 -m pytest scripts/tests/ -q
git add exports/*print-a4-??.html exports/presentationsteknik-print-a4-sv.html \
  _unpublished/exports/*print-a4*.html assets/pdfs/guides/claude-guide-*.pdf \
  assets/pdfs/presentation-skills-guide-en.pdf assets/pdfs/presentationsteknik-guide-sv.pdf \
  _unpublished/assets/pdfs/guides/*guide*.pdf _unpublished/assets/pdfs/guides/ai-for-*.pdf
git commit -m "feat(guides): take the twelve A4 guides to Blueprint"
```

---

## Uppgift 7: NLM-140 — kromfärgerna i byggskriptet

`exports/nlm-140-prompts-en.html` är **genererad**. Ändringar i HTML-filen skrivs över nästa gång skriptet körs. Skriptet producerar tre utdata: HTML, PDF och en `.docx` med egna `RGBColor`-anrop.

Av filens 332 hexkoder är cirka 228 **innehåll** — prompttext som beskriver visuella stilar ("a primary accent color (#7FA1C3)"). En svepande ersättning förstör dokumentet.

**Filer:**
- Ändra: `exports/build-nlm-prompts-en.py` (kromfärgerna på rad ~57–254 och `RGBColor`-anropen på rad ~303–331)
- Ändra: `scripts/tests/test_guide_pdf_parity.py` (nytt test, se steg 1)

- [ ] **Steg 1: Skriv testet som skyddar innehållsfärgerna**

Lägg till i `scripts/tests/test_guide_pdf_parity.py`:

```python
import re

NLM_HTML = fp.ROOT / "exports" / "nlm-140-prompts-en.html"
# Hexkoder som står i prompttexten, inte i <style>. Räknat före stilbytet.
NLM_CONTENT_HEX_COUNT = 228


def test_nlm_content_hex_codes_survive_the_restyle():
    """De 228 hexkoderna i prompttexten är innehåll och ska stå kvar ordagrant.

    En svepande färgersättning över filen skulle byta dem mot Blueprint och
    göra 140 stilbeskrivningar osanna.
    """
    text = NLM_HTML.read_text(encoding="utf-8")
    style = re.search(r"<style>.*?</style>", text, re.S)
    assert style, "style-blocket saknas"
    body = text[: style.start()] + text[style.end():]
    found = {m.upper() for m in re.findall(r"#[0-9a-fA-F]{6}\b", body)}
    assert len(found) >= NLM_CONTENT_HEX_COUNT, (
        f"bara {len(found)} innehållshexar kvar av {NLM_CONTENT_HEX_COUNT} — "
        "en svepande ersättning har träffat prompttexten"
    )
```

Mät det verkliga talet innan du skriver in det:

```bash
/usr/bin/python3 - <<'PY'
import re
from pathlib import Path
t = Path("exports/nlm-140-prompts-en.html").read_text(encoding="utf-8")
s = re.search(r"<style>.*?</style>", t, re.S)
body = t[:s.start()] + t[s.end():]
print(len({m.upper() for m in re.findall(r"#[0-9a-fA-F]{6}\b", body)}))
PY
```

- [ ] **Steg 2: Kör testet och se det grönt mot dagens fil**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_pdf_parity.py -q -k nlm
```

- [ ] **Steg 3: Byt kromfärgerna i skriptet**

I `exports/build-nlm-prompts-en.py`, i det inbäddade `<style>`-blocket: samma tabell som uppgift 5. `#1B2733` → `var(--color-text)`, `#C8A86B` → `var(--color-highlight-ink)` där det är text och `var(--color-highlight)` där det är yta, `#3E4A57` → `var(--color-text-soft)`, `#8a8a85` → `var(--color-text-muted)`, `#F6F3EE` → `var(--color-bg)`. Lägg `<link rel="stylesheet" href="_guide-print.css">` i det genererade huvudet och ta bort googleapis-raderna.

Docx-grenen kan inte använda CSS-variabler. Byt de tre `RGBColor`-anropen till Blueprints värden direkt, med en kommentar som säger varför de står hårdkodade här:

```python
# Docx har ingen CSS. Värdena speglar _guide-print.css och måste ändras
# på båda ställena om paletten rör sig igen.
run.font.color.rgb = RGBColor(0x9C, 0x5A, 0x24)  # --color-highlight-ink
r.font.color.rgb = RGBColor(0x0C, 0x1A, 0x2E)    # --color-text
r.font.color.rgb = RGBColor(0x4E, 0x5A, 0x68)    # --color-text-soft
```

- [ ] **Steg 4: Kör skriptet och mät**

```bash
/usr/bin/python3 exports/build-nlm-prompts-en.py
/usr/bin/python3 -m pytest scripts/tests/test_guide_pdf_parity.py -q -k "nlm"
```

Förväntat: både innehållstestet och paritetstestet gröna.

- [ ] **Steg 5: Commit**

```bash
/usr/bin/python3 -m pytest scripts/tests/ -q
git add exports/build-nlm-prompts-en.py exports/nlm-140-prompts-en.html \
  exports/nlm-140-prompts-en.docx assets/pdfs/nlm-140-prompts-en.pdf \
  scripts/tests/test_guide_pdf_parity.py
git commit -m "feat(guides): take the NotebookLM 140 document to Blueprint"
```

---

## Uppgift 8: Utvidga varumärkesvakten till guidfamiljen

`brandguard.published_files()` utesluter hela `exports/`. Det var rätt i våg 1 — mallarna låg utanför. Nu ligger de inne, och utan en vakt kan nästa ändring smyga tillbaka Playfair utan att ett test blir rött.

**Filer:**
- Ändra: `scripts/tests/brandguard.py` (ny funktion, `PUBLISHED_EXCLUDE` rörs inte)
- Ändra: `scripts/tests/test_guide_print_css.py` (nya tester över hela familjen)

**Gränssnitt:**
- Producerar: `brandguard.guide_templates() -> Iterator[Path]` — de 26 handskrivna mallarna, alltså de 27 minus den genererade `nlm-140-prompts-en.html`.

- [ ] **Steg 1: Lägg till funktionen i brandguard**

```python
GUIDE_TEMPLATE_GLOBS = (
    "exports/claude-print-a4-*.html",
    "exports/claude-guide-license-*.html",
    "exports/claude-quick-start-*.html",
    "exports/presentation-skills-*.html",
    "exports/presentationsteknik-*.html",
    "_unpublished/exports/*.html",
)

# nlm-140-prompts-en.html genereras av exports/build-nlm-prompts-en.py och
# vaktas där — den räknas inte som handskriven mall.
GENERATED = {"nlm-140-prompts-en.html"}


def guide_templates() -> Iterator[Path]:
    """De handskrivna tryckmallarna bakom guide-PDF:erna (våg 2a)."""
    seen = set()
    for pattern in GUIDE_TEMPLATE_GLOBS:
        for path in sorted(ROOT.glob(pattern)):
            if path.name in GENERATED or path in seen:
                continue
            seen.add(path)
            yield path
```

- [ ] **Steg 2: Skriv vakterna**

Lägg till i `scripts/tests/test_guide_print_css.py`:

```python
from . import brandguard

TEMPLATES = list(brandguard.guide_templates())


def test_the_glob_finds_every_template():
    """26 handskrivna mallar. Faller globbet ihop tyst vaktar resten ingenting."""
    assert len(TEMPLATES) == 26, [p.name for p in TEMPLATES]


@pytest.mark.parametrize("path", TEMPLATES, ids=lambda p: p.name)
def test_no_old_palette_in_the_templates(path):
    text = path.read_text(encoding="utf-8")
    for value in CRESTIORA + OLD_CHOOSEWISE:
        assert value.lower() not in text.lower(), f"{path.name} bär {value}"


@pytest.mark.parametrize("path", TEMPLATES, ids=lambda p: p.name)
def test_no_external_font_calls(path):
    assert "fonts.googleapis.com" not in path.read_text(encoding="utf-8")


@pytest.mark.parametrize("path", TEMPLATES, ids=lambda p: p.name)
def test_only_blueprint_typefaces_in_font_family_context(path):
    """Matcha i font-family-kontext. Sajten undervisar om design och nämner
    typsnittsnamn i brödtext — en vakt utan kontext slår larm på sin egen
    undervisning."""
    families = re.findall(r"font-family:\s*([^;}]+)", path.read_text(encoding="utf-8"))
    banned = [f for f in families
              if re.search(r"Playfair|Fraunces|Work Sans|\bInter\b", f)]
    assert not banned, f"{path.name}: {banned}"


@pytest.mark.parametrize("path", TEMPLATES, ids=lambda p: p.name)
def test_no_font_weight_outside_the_scale_in_templates(path):
    weights = re.findall(r"font-weight:\s*(\d{3})", path.read_text(encoding="utf-8"))
    outside = sorted({w for w in weights if w not in {"300", "400", "500"}})
    assert not outside, f"{path.name}: vikter utanför skalan {outside}"
```

- [ ] **Steg 3: Kör och se dem gröna**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_print_css.py -q
```

Är någon röd är en mall missad i uppgift 4–6. Rätta mallen, inte testet.

- [ ] **Steg 4: Bevisa att vakten kan bli röd**

```bash
/usr/bin/sed -i '' "s/var(--font-display)/'Playfair Display', serif/" exports/claude-quick-start-en.html
/usr/bin/python3 -m pytest scripts/tests/test_guide_print_css.py -q -k claude-quick-start-en
git checkout -- exports/claude-quick-start-en.html
```

Förväntat: rött på `test_only_blueprint_typefaces_in_font_family_context`, sedan grönt igen efter återställningen. Fyra tester i våg 1 kunde inte falla på det de vaktade — det här steget är billigare än att upptäcka samma sak i efterhand.

- [ ] **Steg 5: Commit**

```bash
/usr/bin/python3 -m pytest scripts/tests/ -q
git add scripts/tests/brandguard.py scripts/tests/test_guide_print_css.py
git commit -m "test(guides): guard the 26 print templates against the old palettes"
```

---

## Uppgift 9: Slutverifiering och PR

- [ ] **Steg 1: Rendera om allt från rent läge**

```bash
cd /Users/johan/Projekt/Choosewise/choosewise-education
/usr/bin/python3 exports/build-guide-pdfs.py
git status --short assets/pdfs _unpublished/assets/pdfs
```

Förväntat: inga ändringar utöver dem som redan committats. Dyker en PDF upp som ändrad efter en omrendering utan källändring är bygget inte idempotent — notera vilken och varför.

- [ ] **Steg 2: Hela sviten**

```bash
/usr/bin/python3 -m pytest scripts/tests/ -q
```

- [ ] **Steg 3: Okulär granskning, sex uppslag**

```bash
/usr/bin/python3 - <<'PY'
import subprocess
from pathlib import Path
jobs = [
    ("assets/pdfs/guides/claude-guide-en.pdf", 1, 3),
    ("assets/pdfs/guides/claude-guide-sv.pdf", 1, 3),
    ("assets/pdfs/presentationsteknik-guide-sv.pdf", 1, 2),
    ("assets/pdfs/nlm-140-prompts-en.pdf", 1, 2),
    ("_unpublished/assets/pdfs/guides/copilot-guide-en.pdf", 1, 2),
    ("_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-sv.pdf", 1, 2),
]
out = Path("/tmp/blueprint-guider"); out.mkdir(exist_ok=True)
for pdf, first, last in jobs:
    stem = Path(pdf).stem
    subprocess.run(["pdftoppm", "-png", "-r", "110", "-f", str(first),
                    "-l", str(last), pdf, str(out / stem)], check=True)
print(f"bilder i {out}")
PY
open /tmp/blueprint-guider
```

Checklista per uppslag: koppar som text bara i `-ink` eller `-on-dark`, ingen text blått mot blått, å ä ö intakta, sidnummer och sidbrytningar på samma ställe som förut.

- [ ] **Steg 4: Kontrollera att `build-seo-meta.py` inte bumpat orelaterade sidor**

```bash
git status --short | grep -vE "exports/|assets/pdfs|scripts/tests" | head -20
```

Guidarbetet rör inga HTML-sidor på sajten. Dyker sidor upp här som inte hör till planen: återställ dem före push.

- [ ] **Steg 5: Push och PR**

```bash
git push -u origin feat/blueprint-wave-2a-guides
gh pr create --base main --title "Blueprint våg 2a: guidernas tryckmallar" --body "$(cat <<'EOF'
De 27 tryckmallarna bakom guidernas 23 PDF:er går till Blueprint. Delad
`exports/_guide-print.css` för tokens, typsnitt och de två underfamiljer som
faktiskt är strukturlika; A4-guiderna behåller sin egen layout och hämtar bara
färg och typsnitt ur variablerna.

Innehållet är oförändrat. Varje PDF:s text är låst mot ett committat sidvis
teckenfingeravtryck taget före första stilraden ändrades.

Dessutom: de sju build-skript som pekade på `exports/` efter att mallarna
flyttats till `_unpublished/` i 430f6d0 går att köra igen.

Utanför: diagram- och social-exporterna (egen runda, Johans beslut) och steg 2b
(innehållets aktualitet).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Steg 6: Visa Johan bilderna innan merge**

Samma ordning som i våg 1: han ser trycket innan något publiceras. Nio av de 23 PDF:erna ligger live på sajten.

---

## Vad som INTE ingår

- **Steg 2b** — guidernas innehåll. Fem guider i två språk, 10 sidor, 18 PDF:er, skrivna i april 2026. Egen plan.
- **Diagram- och social-exporterna** — åtta mallar plus SVG, PNG och PDF. Johans beslut: egen runda, gärna ihop med spår A.
- **Visual Codes Vol. 1–3** — `~/Projekt/Choosewise/visual-codes-pdf/`, utanför repot, tredje kopian av paletten. Specen räknar dem till våg 2; de kräver sin egen körning i den katalogen.
- **Spår A** — märke och favicon. Specen sekvenserade spår A före våg 2 just för att guidernas omslag är en av få ytor där ett märke syns stort. Görs spår A efter den här planen ritas de sex mörka omslagen om en andra gång.
