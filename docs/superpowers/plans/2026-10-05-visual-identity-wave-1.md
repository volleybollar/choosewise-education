# Visuell identitet våg 1 — implementationsplan

> **För agentiska arbetare:** OBLIGATORISK UNDERSKILL: använd superpowers:subagent-driven-development (rekommenderas) eller superpowers:executing-plans för att genomföra planen uppgift för uppgift. Stegen använder kryssrutor (`- [ ]`) för avprickning.

**Mål:** Byta choosewise.educations grafiska uttryck till Blueprint-paletten och Hanken Grotesk, städa bort Crestioras palett och Google Fonts-anropen från de publicerade filerna, och rendera om de 124 prompt-PDF:erna i den nya stilen — utan att ändra en enda mening innehåll.

**Arkitektur:** All färg och typografi bor i `assets/css/tokens.css`. Allt annat konsumerar tokens. Arbetet är därför: (1) skriv testerna som kodar designkontraktet, (2) byt tokens, (3) jaga rätt på allt som går runt tokens — hårdkodade värden i `components.css`, i sidlokal CSS, i inbäddade SVG-diagram och i SVG-filer — tills guard-testerna är gröna. De ~150 genererade sidorna rörs inte: de bär noll färgvärden och ärver allt från delad CSS.

**Teknikstack:** Rak HTML/CSS, inga byggsteg på sajten. Python 3 med pytest för tester (följer `scripts/tests/test_build_evidence_cards.py`). Playwright för PDF-rendering och skärmbilder. `pdftotext` för innehållsjämförelse.

**Spec:** `docs/superpowers/specs/2026-10-05-choosewise-visual-identity-design.md`

**Branch:** `feat/visual-identity-blueprint` finns redan, med specen committad som `4c44580`.

## Globala villkor

- **Förbjudna värden i publicerade filer, utan undantag:** `#1B2733`, `#C8A86B`, `#F6F3EE`, `#2E4057`, `Playfair Display`. Det är Crestioras palett och typsnitt, och Crestiora är anonymt. Spec §3.
- **Förbjudna värden efter uppgift 8:** `#2d5a3f`, `#c66b3d`, `#faf7f2`, `#f2ede2`, `Fraunces`, `Work Sans`. Gammal palett.
- **Inga anrop till `fonts.googleapis.com` eller `fonts.gstatic.com`** från publicerade filer. Spec §5.
- **All text som renderas mot sin bakgrund ska nå minst 4,5:1** enligt WCAG 2.1 AA. Spec §4.
- **"Publicerade filer"** betyder allt utanför `.git/`, `exports/`, `_unpublished/`, `docs/`, `.superpowers/`, `.playwright-mcp/`. Den definitionen används identiskt i varje test.
- **`git add -A` används aldrig.** Repot har 21 ocommittade ändringar som inte hör hit. Varje commit listar sina filer explicit.
- **Innehåll ändras inte.** Ingen mening, rubrik, URL eller filnamn rörs. Bara färg, typsnitt, form.
- **`/usr/bin/python3` (3.9.6) är den enda interpreter som har `pytest` och `playwright`.** Homebrews `python3` (3.14) saknar båda. Varje test- och renderingskommando i planen använder därför `/usr/bin/python3` explicit.
- **Förhandsvisning körs alltid på ny port** — `include.js` hämtar `header-*.html` separat och Safari cachar hårt.

## Granskningsfokus

Fem saker specen förutsätter men som ingen uppgifts huvudtest fångar. Varje rad har fått ett test i den uppgift som äger koden.

1. **Fokusringen försvinner mot mörka band.** `--color-focus` är samma blå som `--color-dark-bg`. En tangentbordsanvändare tappar all fokusmarkering i CTA- och footer-sektionerna. → test i uppgift 1.
2. **Svenska tecken i PDF efter typsnittsbytet.** Prompt-PDF:erna renderas av Playwright; om Hanken Grotesk inte är nåbar för renderaren faller texten tillbaka på ett systemsnitt och å/ä/ö kan bryta radbrytningen. → test i uppgift 9.
3. **Kopparknapparnas textfärg.** Vit text på koppar ger 3,4:1 och är inte tillåtet, men är den vana man griper till. → test i uppgift 1.
4. **`prefers-reduced-motion` slutar respekteras** om `--dur-*`-blocket råkar skrivas över när tokens byts. → test i uppgift 1.
5. **Sidlokal CSS går runt tokens.** `guides/claude/styles.css` och dess svenska tvilling har 161 `var()`-anrop men också 15 hårdkodade värden. Samma mönster kan uppstå igen. → test i uppgift 8.

---

### Uppgift 1: Designkontraktet som test, och de nya tokenen

**Filer:**
- Skapa: `scripts/tests/test_tokens.py`
- Ändra: `assets/css/tokens.css` (färgblock rad 8–33, typografiblock rad 35–40, `--lh-tight`, skuggor, radier)

**Gränssnitt:**
- Konsumerar: inget.
- Producerar: `parse_tokens(path)` och `contrast(hex_a, hex_b)` i `scripts/tests/test_tokens.py`. Ingen senare uppgift importerar dem — de hör till den här filens egna påståenden.

- [ ] **Steg 1: Skriv det fallerande testet**

Skapa `scripts/tests/test_tokens.py`:

```python
"""Designkontraktet för Blueprint-paletten, kodat som test.

Varje påstående här kommer från docs/superpowers/specs/
2026-10-05-choosewise-visual-identity-design.md §4 och §5.
Ändras ett värde i specen ska det ändras här i samma commit.
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TOKENS = ROOT / "assets/css/tokens.css"


def parse_tokens(path: Path = TOKENS) -> dict[str, str]:
    """Plocka ut varje --namn: värde; ur :root-blocket."""
    text = path.read_text(encoding="utf-8")
    return {
        m.group(1): m.group(2).strip()
        for m in re.finditer(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", text)
    }


def _channel(c: int) -> float:
    s = c / 255
    return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4


def _luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def contrast(a: str, b: str) -> float:
    la, lb = _luminance(a), _luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


EXPECTED_COLOURS = {
    "--color-bg": "#FBFAF8",
    "--color-bg-alt": "#EFF2F6",
    "--color-text": "#0C1A2E",
    "--color-text-soft": "#4E5A68",
    "--color-text-muted": "#656F7B",
    "--color-border": "#DDE3EA",
    "--color-border-strong": "#C3CFDC",
    "--color-accent": "#0B3A6F",
    "--color-accent-hover": "#082C55",
    "--color-deep": "#07284D",
    "--color-highlight": "#C2793A",
    "--color-highlight-ink": "#9C5A24",
    "--color-dark-bg": "#0B3A6F",
    "--color-dark-text": "#EFF2F6",
    "--color-focus": "#0B3A6F",
    "--color-focus-on-dark": "#E8C9A8",
}


@pytest.mark.parametrize("name,value", EXPECTED_COLOURS.items())
def test_colour_token_has_spec_value(name, value):
    tokens = parse_tokens()
    assert name in tokens, f"{name} saknas i tokens.css"
    assert tokens[name].upper() == value.upper()


# (förgrund, bakgrund, minsta kontrast, vad det är)
TEXT_PAIRS = [
    ("--color-text", "--color-bg", 4.5, "bläck på papper"),
    ("--color-text-soft", "--color-bg", 4.5, "brödtext på papper"),
    ("--color-text-muted", "--color-bg", 4.5, "metadata på papper"),
    ("--color-accent", "--color-bg", 4.5, "länk och rubrik på papper"),
    ("--color-highlight-ink", "--color-bg", 4.5, "kopparetikett på papper"),
    ("--color-dark-text", "--color-dark-bg", 4.5, "text på mörkt band"),
    ("--color-text", "--color-highlight", 4.5, "text på kopparknapp"),
    ("--color-focus-on-dark", "--color-dark-bg", 3.0, "fokusring på mörkt band"),
    ("--color-focus", "--color-bg", 3.0, "fokusring på papper"),
]


@pytest.mark.parametrize("fg,bg,minimum,label", TEXT_PAIRS)
def test_contrast_meets_wcag(fg, bg, minimum, label):
    tokens = parse_tokens()
    ratio = contrast(tokens[fg], tokens[bg])
    assert ratio >= minimum, f"{label}: {ratio:.2f}:1, kräver {minimum}:1"


def test_focus_ring_is_visible_against_dark_band():
    """Granskningsfokus 1: en fokusring i bandets egen färg är osynlig."""
    tokens = parse_tokens()
    assert tokens["--color-focus-on-dark"] != tokens["--color-dark-bg"]


def test_copper_button_text_is_not_white():
    """Granskningsfokus 3: vit text på koppar ger 3,4:1."""
    tokens = parse_tokens()
    assert contrast("#FFFFFF", tokens["--color-highlight"]) < 4.5
    assert contrast(tokens["--color-text"], tokens["--color-highlight"]) >= 4.5


def test_heading_line_height_allows_swedish_diacritics():
    tokens = parse_tokens()
    assert float(tokens["--lh-tight"]) >= 1.16


def test_font_tokens_name_the_new_families():
    tokens = parse_tokens()
    assert "Hanken Grotesk" in tokens["--font-display"]
    assert "Hanken Grotesk" in tokens["--font-body"]
    assert "Instrument Serif" in tokens["--font-quote"]


def test_old_fonts_are_gone_from_tokens():
    tokens = parse_tokens()
    joined = " ".join(tokens.values())
    assert "Fraunces" not in joined
    assert "Work Sans" not in joined


def test_reduced_motion_block_survives():
    """Granskningsfokus 4: motion-tokens får inte tappas vid omskrivningen."""
    text = TOKENS.read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in text
    assert re.search(r"--dur-fast:\s*0ms", text)
```

- [ ] **Steg 2: Kör testet och se att det fallerar**

```bash
cd /Users/johan/Projekt/Choosewise/choosewise-education
/usr/bin/python3 -m pytest scripts/tests/test_tokens.py -v
```

Förväntat: FAIL. `--color-bg` har värdet `#faf7f2`, `--color-focus-on-dark` saknas helt, `--lh-tight` är `1.1`, `--font-display` namnger Fraunces.

- [ ] **Steg 3: Skriv de nya tokenen**

Ersätt färgblocket i `assets/css/tokens.css` (allt från `/* ───── Colors ───── */` till och med raden före `/* ───── Typography ───── */`):

```css
/* ───── Colors — Blueprint, spec §4 ───── */
--color-bg:           #FBFAF8;  /* papper */
--color-bg-alt:       #EFF2F6;  /* svalt sektionsband */
--color-text:         #0C1A2E;  /* bläck, blåsvart */
--color-text-soft:    #4E5A68;  /* brödtext */
--color-text-muted:   #656F7B;  /* metadata — 4,9:1, rör inte */
--color-border:       #DDE3EA;
--color-border-strong:#C3CFDC;

--color-accent:       #0B3A6F;  /* varumärkesblå */
--color-accent-hover: #082C55;
--color-deep:         #07284D;  /* footer, hero */

/* Koppar har två värden. Ytor och grafik tar --color-highlight.
   All kopparfärgad TEXT tar --color-highlight-ink (5,2:1). */
--color-highlight:     #C2793A;
--color-highlight-ink: #9C5A24;
--color-highlight-hover: #A9642C;

--color-dark-bg:      #0B3A6F;
--color-dark-text:    #EFF2F6;

/* Fokusringen har två värden: den blå är osynlig mot det blå bandet. */
--color-focus:         #0B3A6F;
--color-focus-on-dark: #E8C9A8;

--color-bg-blur:       rgba(251, 250, 248, 0.85);
--color-border-subtle: rgba(239, 242, 246, 0.12);

/* Kopieringsknappar — var en egen blå, nu samma som varumärkesfärgen */
--color-copy:       #0B3A6F;
--color-copy-hover: #082C55;
```

Ersätt typsnittsraderna:

```css
--font-display: 'Hanken Grotesk', -apple-system, 'Helvetica Neue', sans-serif;
--font-body:    'Hanken Grotesk', -apple-system, 'Helvetica Neue', sans-serif;
--font-quote:   'Instrument Serif', Georgia, 'Times New Roman', serif;
--font-mono:    'SF Mono', Menlo, Monaco, monospace;
```

Ändra `--lh-tight` från `1.1` till `1.16`, och `--tracking-tight` från `-0.02em` till `-0.032em`.

Platta ut skuggorna och ändra fokusringen:

```css
--shadow-sm: 0 1px 2px rgba(12,26,46,0.04);
--shadow-md: 0 1px 3px rgba(12,26,46,0.05);
--shadow-lg: 0 2px 8px rgba(12,26,46,0.06);
--shadow-focus: 0 0 0 3px rgba(11,58,111,0.28);
```

Ändra `--radius-md` från `8px` till `12px` och `--radius-lg` från `16px` till `16px` (oförändrad). `--radius-sm` och `--radius-pill` står kvar.

Rör inte `@media (prefers-reduced-motion: reduce)`-blocket.

- [ ] **Steg 4: Kör testet och se att det går igenom**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_tokens.py -v
```

Förväntat: PASS, alla.

- [ ] **Steg 5: Commit**

```bash
git add scripts/tests/test_tokens.py assets/css/tokens.css
git commit -m "feat(tokens): Blueprint palette and Hanken Grotesk type tokens"
```

---

### Uppgift 2: Självhostade typsnitt, och bort med Google Fonts-anropen

**Filer:**
- Skapa: `assets/fonts/hanken-grotesk/HankenGrotesk-VariableFont.woff2`
- Skapa: `assets/fonts/instrument-serif/InstrumentSerif-Regular.woff2`
- Skapa: `assets/fonts/instrument-serif/InstrumentSerif-Italic.woff2`
- Skapa: `scripts/tests/brandguard.py`
- Skapa: `scripts/tests/test_fonts.py`
- Ändra: `assets/css/fonts.css`
- Ändra: `guides/claude/index.html`, `sv/guider/claude/index.html`, `wise-framework.html`, `ratt-modellen.html` — ta bort `<link>`-raderna till Google Fonts

**Gränssnitt:**
- Konsumerar: `--font-display`, `--font-body`, `--font-quote` från uppgift 1.
- Producerar: `scripts/tests/brandguard.py` med `ROOT`, `PUBLISHED_EXCLUDE` och `published_files(suffixes)`. Uppgift 4 och 8 importerar den.

**Varför en egen hjälpmodul:** `scripts/tests/` innehåller `__init__.py` och är alltså ett paket, så `import test_fonts` fungerar inte mellan testfiler. Hjälparna bor i en vanlig modul som varje testfil når via samma `sys.path`-mönster som `test_build_evidence_cards.py` redan använder.

- [ ] **Steg 1: Skriv det fallerande testet**

Skapa först hjälpmodulen `scripts/tests/brandguard.py`:

```python
"""Delade hjälpare för varumärkestesterna.

Vanlig modul, inte testfil — scripts/tests/ är ett paket, så testfiler
kan inte importera varandra direkt.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parents[2]

# Samma definition av "publicerad fil" i varje test i sviten.
PUBLISHED_EXCLUDE = {
    ".git", "exports", "_unpublished", "docs",
    ".superpowers", ".playwright-mcp", "node_modules", "__pycache__",
}


def published_files(
    suffixes: tuple[str, ...] = (".html", ".css", ".js", ".svg"),
) -> Iterator[Path]:
    """Alla filer som faktiskt serveras av GitHub Pages."""
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in suffixes:
            continue
        if PUBLISHED_EXCLUDE & set(path.relative_to(ROOT).parts):
            continue
        yield path
```

Skapa sedan `scripts/tests/test_fonts.py`:

```python
"""Typsnitten ska vara självhostade. Inga anrop till Google."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brandguard import ROOT, published_files  # noqa: E402

EXPECTED_FONT_FILES = [
    "assets/fonts/hanken-grotesk/HankenGrotesk-VariableFont.woff2",
    "assets/fonts/instrument-serif/InstrumentSerif-Regular.woff2",
    "assets/fonts/instrument-serif/InstrumentSerif-Italic.woff2",
]


@pytest.mark.parametrize("rel", EXPECTED_FONT_FILES)
def test_font_file_is_self_hosted(rel):
    path = ROOT / rel
    assert path.exists(), f"{rel} saknas"
    assert path.stat().st_size > 10_000, f"{rel} ser trunkerad ut"


def test_fontface_declares_both_families():
    css = (ROOT / "assets/css/fonts.css").read_text(encoding="utf-8")
    assert "Hanken Grotesk" in css
    assert "Instrument Serif" in css
    assert "Fraunces" not in css
    assert "Work Sans" not in css


def test_hanken_covers_the_weights_we_use():
    css = (ROOT / "assets/css/fonts.css").read_text(encoding="utf-8")
    assert "font-weight: 300 600" in css


def test_no_published_file_calls_google_fonts():
    offenders = []
    for path in published_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "fonts.googleapis.com" in text or "fonts.gstatic.com" in text:
            offenders.append(str(path.relative_to(ROOT)))
    assert offenders == [], f"Hämtar typsnitt från Google: {offenders}"
```

- [ ] **Steg 2: Kör testet och se att det fallerar**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_fonts.py -v
```

Förväntat: FAIL. Typsnittsfilerna saknas, `fonts.css` namnger Fraunces, och fyra sidor anropar Google.

- [ ] **Steg 3: Ladda ned typsnitten och skriv om fonts.css**

```bash
cd /Users/johan/Projekt/Choosewise/choosewise-education
mkdir -p assets/fonts/hanken-grotesk assets/fonts/instrument-serif
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36'

# Hanken Grotesk, variabel 300–600, latin + latin-ext i en fil
curl -s -A "$UA" "https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300..600&display=swap" \
  | grep -A4 '/\* latin \*/' | grep -oE 'https://[^)]+\.woff2' | head -1 \
  | xargs curl -s -o assets/fonts/hanken-grotesk/HankenGrotesk-VariableFont.woff2

# Instrument Serif — statisk, rak + kursiv
curl -s -A "$UA" "https://fonts.googleapis.com/css2?family=Instrument+Serif&display=swap" \
  | grep -A4 '/\* latin \*/' | grep -oE 'https://[^)]+\.woff2' | head -1 \
  | xargs curl -s -o assets/fonts/instrument-serif/InstrumentSerif-Regular.woff2
curl -s -A "$UA" "https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@1&display=swap" \
  | grep -A4 '/\* latin \*/' | grep -oE 'https://[^)]+\.woff2' | head -1 \
  | xargs curl -s -o assets/fonts/instrument-serif/InstrumentSerif-Italic.woff2

ls -la assets/fonts/hanken-grotesk assets/fonts/instrument-serif
```

Kontrollera att varje fil är större än 10 kB. Är någon på 0 byte har Google ändrat sitt CSS-format — hämta då URL:en för hand ur svaret på `curl` ovan.

Ersätt hela innehållet i `assets/css/fonts.css`:

```css
/* Självhostade typsnitt — integritet och prestanda.
   Inga anrop till Google från den publicerade sajten. */

@font-face {
  font-family: 'Hanken Grotesk';
  src: url('../fonts/hanken-grotesk/HankenGrotesk-VariableFont.woff2') format('woff2');
  font-weight: 300 600;
  font-style: normal;
  font-display: swap;
}

/* Instrument Serif är inte variabel — vikt 400, två statiska filer. */
@font-face {
  font-family: 'Instrument Serif';
  src: url('../fonts/instrument-serif/InstrumentSerif-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Instrument Serif';
  src: url('../fonts/instrument-serif/InstrumentSerif-Italic.woff2') format('woff2');
  font-weight: 400;
  font-style: italic;
  font-display: swap;
}
```

Ta bort Google Fonts-anropen ur de fyra sidorna. Hitta dem med:

```bash
grep -n "fonts.googleapis.com\|fonts.gstatic.com\|preconnect" \
  guides/claude/index.html sv/guider/claude/index.html \
  wise-framework.html ratt-modellen.html
```

Radera `<link rel="preconnect" ...>`- och `<link ... fonts.googleapis.com ...>`-raderna i varje fil. Lägg inget i stället — sidorna ärver `fonts.css` via sitt vanliga stilmallsanrop.

- [ ] **Steg 4: Kör testet och se att det går igenom**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_fonts.py -v
```

Förväntat: PASS, alla.

- [ ] **Steg 5: Commit**

```bash
git add assets/fonts/hanken-grotesk assets/fonts/instrument-serif \
        assets/css/fonts.css scripts/tests/test_fonts.py scripts/tests/brandguard.py \
        guides/claude/index.html sv/guider/claude/index.html \
        wise-framework.html ratt-modellen.html
git commit -m "feat(fonts): self-host Hanken Grotesk and Instrument Serif, drop Google Fonts calls"
```

---

### Uppgift 3: Tokenisera components.css

**Filer:**
- Skapa: `scripts/tests/test_css_discipline.py`
- Ändra: `assets/css/components.css` (127 hårdkodade värden)
- Ändra: `assets/css/pages.css` rad 313 (`color: #fff` på kopparfärgad bakgrund)

**Gränssnitt:**
- Konsumerar: tokennamnen från uppgift 1.
- Producerar: inget som senare uppgifter importerar.

- [ ] **Steg 1: Skriv det fallerande testet**

Skapa `scripts/tests/test_css_discipline.py`:

```python
"""Färg bor i tokens.css. Ingen annanstans i assets/css/."""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CSS_DIR = ROOT / "assets/css"

HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")


def shared_stylesheets():
    return sorted(p for p in CSS_DIR.glob("*.css") if p.name != "tokens.css")


@pytest.mark.parametrize("path", shared_stylesheets(), ids=lambda p: p.name)
def test_no_hardcoded_hex_outside_tokens(path):
    found = HEX.findall(path.read_text(encoding="utf-8"))
    assert found == [], (
        f"{path.name} har {len(found)} hårdkodade färger: {sorted(set(found))[:8]}"
    )
```

- [ ] **Steg 2: Kör testet och se att det fallerar**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_css_discipline.py -v
```

Förväntat: FAIL på **två** filer — `components.css` med 127 värden, och `pages.css` med ett. `base.css` passerar redan.

Den enda träffen i `pages.css` sitter på rad 313 och är inte bara ett hårdkodat värde, utan ett brott mot spec §4 regel 3:

```css
.prompt-filter.is-active {
  background: var(--color-highlight);
  color: #fff;            /* vit på koppar = 3,4:1, otillåtet */
  border-color: var(--color-highlight);
}
```

Det är det aktiva filterpillret på promptsidan. Byt `#fff` mot `var(--color-text)` — mörk text på koppar ger 5,1:1.

- [ ] **Steg 3: Byt de hårdkodade värdena mot tokens**

Lista dem grupperade så arbetet blir mekaniskt:

```bash
grep -noE '#[0-9a-fA-F]{3,8}\b' assets/css/components.css | sort -t: -k2 | uniq -c -f0
```

Översättningstabell. Värdena till vänster är den Tailwind-aktiga paletten som smugit sig in; höger sida är det token som bär samma roll:

| Hårdkodat | Ersätts med |
|---|---|
| `#fff`, `#ffffff` | `var(--color-bg)` |
| `#fafaf7` | `var(--color-bg)` |
| `#f1f5f9`, `#f5f3ff`, `#fef3c7` | `var(--color-bg-alt)` |
| `#0f172a`, `#000` | `var(--color-text)` |
| `#475569`, `#64748b` | `var(--color-text-soft)` |
| `#94a3b8`, `#cbd5e1` | `var(--color-text-muted)` |
| `#e5e7eb` | `var(--color-border)` |
| `#1e3a8a`, `#6d28d9`, `#5b21b6`, `#ddd6fe` | `var(--color-accent)` |
| `#15803d` | `var(--color-accent)` |
| `#92400e`, `#78350f`, `#b8423a` | `var(--color-highlight-ink)` |

Varje rad som sätter färg på **text** ska landa på `--color-text`, `--color-text-soft`, `--color-text-muted`, `--color-accent` eller `--color-highlight-ink` — aldrig på `--color-highlight`, som är till för ytor.

De nio `rgba()`-anropen i filen lämnas som de är om de är genomskinliga svarta eller vita skuggor; bär de färg byts de mot motsvarande token med `color-mix()` eller mot `--color-border-subtle`.

- [ ] **Steg 4: Kör testet och se att det går igenom**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_css_discipline.py -v
```

Förväntat: PASS för alla fyra stilmallar.

- [ ] **Steg 5: Commit**

```bash
git add assets/css/components.css assets/css/pages.css scripts/tests/test_css_discipline.py
git commit -m "refactor(css): tokenise hardcoded colours, fix white-on-copper filter pill"
```

---

### Uppgift 4: Ut med Crestioras palett ur de publicerade filerna

Det här är uppgiften som stänger anonymitetsrisken i spec §3. Den går före all annan kosmetik.

**Filer:**
- Skapa: `scripts/tests/test_palette_guard.py`
- Ändra: `guides/claude/index.html` (34 förekomster i inbäddade SVG)
- Ändra: `sv/guider/claude/index.html` (34 förekomster)
- Ändra: `guides/claude/styles.css` (15 värden)
- Ändra: `sv/guider/claude/styles.css` (15 värden)
- Ändra: `sv/blog/posts/tva-grona-rutor-av-sextio.html` (2 värden)

**Gränssnitt:**
- Konsumerar: `ROOT` och `published_files` från `scripts/tests/brandguard.py` (uppgift 2).
- Producerar: `CRESTIORA_FORBIDDEN` och `scan(forbidden)` i `scripts/tests/test_palette_guard.py`. Uppgift 8 lägger till `LEGACY_FORBIDDEN` i samma fil.

- [ ] **Steg 1: Skriv det fallerande testet**

Skapa `scripts/tests/test_palette_guard.py`:

```python
"""Crestioras palett och typsnitt får aldrig finnas i publicerade filer.

Crestiora Books är en anonym utgivare. choosewise.education är Johans
namngivna sajt. Delar de visuellt uttryck går varumärkena att koppla ihop.
Spec §3.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brandguard import ROOT, published_files  # noqa: E402

CRESTIORA_FORBIDDEN = [
    "1B2733",          # navy
    "C8A86B",          # mässing
    "F6F3EE",          # grädde
    "2E4057",          # slate
    "Playfair Display",
]


def scan(forbidden):
    """Returnera {relativ sökväg: [träffade värden]} för publicerade filer."""
    hits = {}
    for path in published_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        found = [f for f in forbidden if f.lower() in text.lower()]
        if found:
            hits[str(path.relative_to(ROOT))] = found
    return hits


def test_no_crestiora_values_in_published_files():
    hits = scan(CRESTIORA_FORBIDDEN)
    assert hits == {}, (
        "Crestioras varumärke läcker in på Johans namngivna sajt:\n"
        + "\n".join(f"  {k}: {v}" for k, v in sorted(hits.items()))
    )
```

- [ ] **Steg 2: Kör testet och se att det fallerar**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_palette_guard.py -v
```

Förväntat: FAIL med fem filer listade.

- [ ] **Steg 3: Byt värdena**

`guides/claude/styles.css` och `sv/guider/claude/styles.css` — samma ändring i båda:

| Crestiora | Ersätts med |
|---|---|
| `#1B2733` | `var(--color-text)` om det är text, `var(--color-accent)` om det är en yta |
| `#2E4057` | `var(--color-accent)` |
| `#C8A86B` | `var(--color-highlight)` för ytor, `var(--color-highlight-ink)` för text |
| `#F6F3EE` | `var(--color-bg-alt)` |
| `#E8E4DC` | `var(--color-border)` |
| `#B8553F` | `var(--color-highlight-ink)` |
| `#6B7280` | `var(--color-text-muted)` |
| `#D1D5DB` | `var(--color-border)` |
| `#FFFFFF`, `#FDFCFA`, `#FAFBFC`, `#FFF8F4` | `var(--color-bg)` |

`guides/claude/index.html` och `sv/guider/claude/index.html` — de 34 förekomsterna sitter i inbäddade `<svg>`-diagram med `fill=` och `stroke=`. SVG-attribut kan ta `var()` när de står i samma dokument, så:

```html
<!-- före -->
<rect x="200" y="60" width="130" height="130" rx="10" fill="#1B2733"/>
<text ... font-family="Playfair Display, serif" font-weight="700" fill="#1B2733">Chat</text>

<!-- efter -->
<rect x="200" y="60" width="130" height="130" rx="10" fill="var(--color-accent)"/>
<text ... font-family="var(--font-display)" font-weight="300" fill="var(--color-accent)">Chat</text>
```

Varje `font-family="Playfair Display, serif"` byts mot `font-family="var(--font-display)"`, och `font-weight="700"` mot `font-weight="300"` på rubrikliknande text i diagrammen — annars bryts regeln om att display aldrig sätts fet (spec §6.4).

`sv/blog/posts/tva-grona-rutor-av-sextio.html` — rad 98: `#1B2733` → `var(--color-text)`, `#F6F3EE` → `var(--color-bg-alt)`.

- [ ] **Steg 4: Kör testet och se att det går igenom**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_palette_guard.py -v
```

Förväntat: PASS.

- [ ] **Steg 5: Kontrollera att diagrammen fortfarande renderar**

```bash
python3 -m http.server 8771 --directory . &
sleep 1
open "http://localhost:8771/guides/claude/"
open "http://localhost:8771/sv/guider/claude/"
```

Titta särskilt på diagrammen med Chat/Cowork/Code-rutorna. Rutorna ska vara blå, etiketterna kopparfärgade, rubriktexten ljus. Stäng servern med `kill %1` när du är klar. Ny port varje gång — cachen ljuger annars.

- [ ] **Steg 6: Commit**

```bash
git add scripts/tests/test_palette_guard.py \
        guides/claude/index.html guides/claude/styles.css \
        sv/guider/claude/index.html sv/guider/claude/styles.css \
        sv/blog/posts/tva-grona-rutor-av-sextio.html
git commit -m "fix(brand): remove Crestiora's palette and Playfair from published pages"
```

---

### Uppgift 5: De handunderhållna sidorna

**Filer:**
- Ändra: `index.html`, `sv/index.html`
- Ändra: `wise/index.html`, `sv/ratt/index.html`
- Ändra: `presentation-skills/module-6/deep-dive/index.html`, `sv/presentationsteknik/modul-6/fordjupning/index.html`
- Ändra: `wise-framework.html`, `ratt-modellen.html` (föräldralösa — stylas om, raderas **inte**, spec §9.7)
- Ändra: `visual-codes/visual-codes.css` (2 värden)

**Gränssnitt:**
- Konsumerar: tokennamnen från uppgift 1.
- Producerar: inget.

- [ ] **Steg 1: Lista exakt vad som ska bytas**

```bash
for f in index.html sv/index.html wise/index.html sv/ratt/index.html \
         presentation-skills/module-6/deep-dive/index.html \
         sv/presentationsteknik/modul-6/fordjupning/index.html \
         wise-framework.html ratt-modellen.html visual-codes/visual-codes.css; do
  echo "── $f"
  grep -noE '#[0-9a-fA-F]{3,8}\b|Fraunces|Work Sans' "$f" | head -20
done
```

- [ ] **Steg 2: Byt värdena**

Samma översättning som i uppgift 3. De gamla värdena mappar så här:

| Gammalt | Ersätts med |
|---|---|
| `#faf7f2` | `var(--color-bg)` |
| `#f2ede2` | `var(--color-bg-alt)` |
| `#1a1a18` | `var(--color-text)` |
| `#6b6b65` | `var(--color-text-soft)` |
| `#2d5a3f` | `var(--color-accent)` |
| `#c66b3d` | `var(--color-highlight-ink)` om text, `var(--color-highlight)` om yta |
| `#e8e2d5` | `var(--color-border)` |
| `Fraunces` | `var(--font-display)` |
| `Work Sans` | `var(--font-body)` |

**WISE-färgerna bär innehåll** (spec §7): i WISE-diagrammet ska W, I och E bli `var(--color-accent)` och S bli `var(--color-highlight)`. Det gäller `wise/index.html`, `sv/ratt/index.html` och de två föräldralösa rotfilerna. Blanda inte ihop dem — texten på sidan förklarar uttryckligen att det tredje steget har avvikande färg.

- [ ] **Steg 3: Kontrollera varje sida i webbläsaren**

```bash
python3 -m http.server 8772 --directory . &
sleep 1
for u in "" "sv/" "wise/" "sv/ratt/" \
         "presentation-skills/module-6/deep-dive/" \
         "sv/presentationsteknik/modul-6/fordjupning/" \
         "wise-framework.html" "ratt-modellen.html" "visual-codes/"; do
  open "http://localhost:8772/$u"
done
```

Förväntat: ingen grön eller terrakotta yta kvar. WISE-cirkeln har tre blå steg och ett kopparfärgat. Stäng med `kill %1`.

- [ ] **Steg 4: Commit**

```bash
git add index.html sv/index.html wise/index.html sv/ratt/index.html \
        presentation-skills/module-6/deep-dive/index.html \
        sv/presentationsteknik/modul-6/fordjupning/index.html \
        wise-framework.html ratt-modellen.html visual-codes/visual-codes.css
git commit -m "feat(pages): restyle hand-maintained pages to Blueprint tokens"
```

---

### Uppgift 6: SVG-tillgångarna

**Filer:**
- Ändra: `assets/images/brand/wise-framework.svg`
- Ändra: `assets/images/brand/og-default.svg`
- Ändra: `assets/images/brand/portrait-placeholder.svg`
- Ändra: `assets/images/hero-video/ambient-poster.svg`
- Ändra: `assets/images/guide-covers/*.svg` (6 filer)
- Ändra: `assets/images/prompt-covers/teacher-questioning.svg`
- Ändra: `visual-codes/images/placeholder-after.svg`

**Gränssnitt:**
- Konsumerar: färgvärdena från uppgift 1. Fristående SVG-filer kan inte läsa `var()` från sajtens CSS — här skrivs **hex-värdena rakt ut**.
- Producerar: inget.

- [ ] **Steg 1: Lista värdena per fil**

```bash
for f in assets/images/brand/wise-framework.svg \
         assets/images/brand/og-default.svg \
         assets/images/brand/portrait-placeholder.svg \
         assets/images/hero-video/ambient-poster.svg \
         assets/images/guide-covers/*.svg \
         assets/images/prompt-covers/*.svg \
         visual-codes/images/placeholder-after.svg; do
  echo "── $f"; grep -oE '#[0-9a-fA-F]{3,6}' "$f" | sort | uniq -c
done
```

- [ ] **Steg 2: Byt värdena**

Fristående SVG saknar tillgång till sajtens tokens, så här skrivs värdena ut:

| Gammalt | Nytt |
|---|---|
| `#faf7f2`, `#f7f4ec` | `#FBFAF8` |
| `#f2ede2` | `#EFF2F6` |
| `#1a1a18`, `#1e1e1c` | `#0C1A2E` |
| `#5a5a57`, `#6b6b65` | `#4E5A68` |
| `#a5a59f` | `#656F7B` |
| `#2d5a3f` | `#0B3A6F` |
| `#c66b3d` | `#C2793A` |
| `#e8e2d5` | `#DDE3EA` |

I `wise-framework.svg`: de elva förekomsterna av `#2d5a3f` hör till W, I och E och blir `#0B3A6F`. De två `#c66b3d` hör till S och blir `#C2793A`. Kontrollera mot sidan att det är rätt bokstav som får koppar — färgen bär innehåll.

Byt också varje `font-family` som nämner Fraunces eller Work Sans mot `Hanken Grotesk, sans-serif`, och sänk `font-weight` på rubriktext från 700 till 300.

- [ ] **Steg 3: Kontrollera att varje SVG fortfarande är giltig och ser rätt ut**

```bash
for f in assets/images/brand/*.svg assets/images/guide-covers/*.svg \
         assets/images/prompt-covers/*.svg assets/images/hero-video/*.svg; do
  python3 -c "import xml.etree.ElementTree as E,sys; E.parse(sys.argv[1]); print('ok', sys.argv[1])" "$f"
done
open assets/images/brand/wise-framework.svg
```

Förväntat: `ok` för varje fil, och WISE-diagrammet visar tre blå steg och ett kopparfärgat.

- [ ] **Steg 4: Commit**

```bash
git add assets/images/brand/wise-framework.svg \
        assets/images/brand/og-default.svg \
        assets/images/brand/portrait-placeholder.svg \
        assets/images/hero-video/ambient-poster.svg \
        assets/images/guide-covers assets/images/prompt-covers \
        visual-codes/images/placeholder-after.svg
git commit -m "feat(svg): restyle brand and cover artwork to Blueprint palette"
```

---

### Uppgift 7: og-korten, och ett skript för PNG-steget

PNG-renderingen görs för hand idag. Det är den punkt som mest sannolikt glöms bort, eftersom felet syns först när någon delar en länk. Den automatiseras här.

**Filer:**
- Ändra: `scripts/build-og-images.py` (paletten sitter i `SECTIONS` och `TEMPLATE`)
- Skapa: `scripts/render-og-pngs.py`
- Ändra: `assets/images/brand/og/*.svg` (12, genereras)
- Ändra: `assets/images/brand/og/*.png` (12, renderas)

**Gränssnitt:**
- Konsumerar: färgvärdena från uppgift 1.
- Producerar: `scripts/render-og-pngs.py` körs som `python3 scripts/render-og-pngs.py` och renderar varje SVG i `assets/images/brand/og/` till PNG i 1200×630.

- [ ] **Steg 1: Byt paletten i generatorn**

I `scripts/build-og-images.py`: byt varje `accent_hex` i `SECTIONS` från `#2d5a3f` till `#0B3A6F` och från `#c66b3d` till `#C2793A`. I `TEMPLATE`: byt gradientens `stop-color="#1a1a18"` till `#07284D`, och varje typsnittsnamn från Fraunces/Work Sans till `Hanken Grotesk`.

- [ ] **Steg 2: Skriv PNG-renderaren**

Skapa `scripts/render-og-pngs.py`:

```python
#!/usr/bin/env python3
"""Rendera varje og-SVG till PNG i 1200×630.

Gjordes tidigare för hand i webbläsare. Det glömdes bort, och felet
syns först när någon delar en länk på LinkedIn. Nu är det ett kommando.

Kräver en lokal server så att självhostade typsnitt laddas — file://
ger fallback-snitt och fel radbrytning.
"""
from __future__ import annotations

import http.server
import socketserver
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OG_DIR = ROOT / "assets/images/brand/og"
PORT = 8799


def serve() -> socketserver.TCPServer:
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(
        *a, directory=str(ROOT), **kw
    )
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def main() -> None:
    httpd = serve()
    svgs = sorted(OG_DIR.glob("*.svg"))
    if not svgs:
        raise SystemExit("Inga SVG-filer i assets/images/brand/og/")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1200, "height": 630}, device_scale_factor=1
        )
        for svg in svgs:
            rel = svg.relative_to(ROOT)
            page.goto(f"http://127.0.0.1:{PORT}/{rel}", wait_until="networkidle")
            page.wait_for_timeout(300)  # låt typsnitten sätta sig
            out = svg.with_suffix(".png")
            page.screenshot(path=str(out))
            print(f"renderade {out.relative_to(ROOT)}")
        browser.close()

    httpd.shutdown()


if __name__ == "__main__":
    main()
```

- [ ] **Steg 3: Kör båda skripten**

```bash
python3 scripts/build-og-images.py
/usr/bin/python3 scripts/render-og-pngs.py
```

Förväntat: 12 rader `renderade assets/images/brand/og/<namn>.png`.

- [ ] **Steg 4: Kontrollera resultatet**

```bash
python3 -c "
from pathlib import Path
import struct
for p in sorted(Path('assets/images/brand/og').glob('*.png')):
    w, h = struct.unpack('>II', p.read_bytes()[16:24])
    assert (w, h) == (1200, 630), f'{p.name} är {w}×{h}'
    print(f'{p.name}: {w}×{h}, {p.stat().st_size // 1024} kB')
"
open assets/images/brand/og/wise-en.png assets/images/brand/og/prompts-sv.png
```

Förväntat: alla 12 är 1200×630, och korten visar blå gradient med kopparfärgad accent och Hanken Grotesk — inte Fraunces.

- [ ] **Steg 5: Commit**

```bash
git add scripts/build-og-images.py scripts/render-og-pngs.py assets/images/brand/og
git commit -m "feat(og): restyle share cards and script the PNG render step"
```

---

### Uppgift 8: Hela sajten grön

**Filer:**
- Ändra: `scripts/tests/test_palette_guard.py` (lägg till den gamla palettens vakt)
- Ändra: vad vakten än hittar

**Gränssnitt:**
- Konsumerar: `scan` från uppgift 4, `published_files` från uppgift 2, `parse_tokens` från uppgift 1.
- Producerar: inget.

- [ ] **Steg 1: Skriv det fallerande testet**

Lägg till i `scripts/tests/test_palette_guard.py`:

```python
LEGACY_FORBIDDEN = [
    "2d5a3f",   # skogsgrön
    "c66b3d",   # terrakotta
    "faf7f2",   # gammal grädde
    "f2ede2",   # gammal tan
    "Fraunces",
    "Work Sans",
]


def test_no_legacy_palette_in_published_files():
    hits = scan(LEGACY_FORBIDDEN)
    assert hits == {}, (
        "Gammal palett kvar:\n"
        + "\n".join(f"  {k}: {v}" for k, v in sorted(hits.items()))
    )


def test_page_local_css_uses_tokens_not_hex():
    """Granskningsfokus 5: sidlokal CSS gick runt tokens förut."""
    import re

    from brandguard import ROOT

    page_local = [
        ROOT / "guides/claude/styles.css",
        ROOT / "sv/guider/claude/styles.css",
        ROOT / "visual-codes/visual-codes.css",
    ]
    offenders = {}
    for path in page_local:
        found = re.findall(r"#[0-9a-fA-F]{3,8}\b", path.read_text(encoding="utf-8"))
        if found:
            offenders[path.name] = sorted(set(found))
    assert offenders == {}, f"Sidlokal CSS hårdkodar färg: {offenders}"


def test_generated_pages_carry_no_palette():
    """De ~150 genererade sidorna ska ärva allt från delad CSS."""
    import re

    from brandguard import ROOT

    samples = [
        ROOT / "prompts/teachers/index.html",
        ROOT / "sv/promptar/larare/index.html",
    ]
    for path in samples:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        assert not re.search(r"#[0-9a-fA-F]{6}\b", text), f"{path.name} bär färgvärden"
```

- [ ] **Steg 2: Kör hela sviten och se vad som är kvar**

```bash
/usr/bin/python3 -m pytest scripts/tests/ -v
```

Förväntat: `test_no_legacy_palette_in_published_files` fallerar och listar de filer uppgift 5–7 inte fångade.

- [ ] **Steg 3: Åtgärda det vakten hittar**

Använd samma översättningstabell som i uppgift 5. Lägg inget nytt till i den förbjudna listan — hittar vakten något oväntat, byt värdet, ändra inte testet.

- [ ] **Steg 4: Kör hela sviten igen**

```bash
/usr/bin/python3 -m pytest scripts/tests/ -v
```

Förväntat: PASS, hela sviten.

- [ ] **Steg 5: Commit**

```bash
git add scripts/tests/test_palette_guard.py
git commit -m "test(brand): guard the whole site against the legacy palette"
```

---

### Uppgift 9: Prompt-PDF:erna

**Filer:**
- Skapa: `scripts/tests/test_prompt_pdf_parity.py`
- Ändra: `exports/prompts/_prompt-print.css`
- Ändra: `assets/pdfs/prompts/*.pdf` (124, renderas om)

**Gränssnitt:**
- Konsumerar: färgvärdena från uppgift 1, typsnittsfilerna från uppgift 2.
- Producerar: inget.

- [ ] **Steg 1: Spara textfacit före ändringen**

```bash
mkdir -p /tmp/pdf-parity-before
for f in teachers-en principals-en mathematics-sv larare-sv skolchefer-sv; do
  pdftotext -layout "assets/pdfs/prompts/$f.pdf" "/tmp/pdf-parity-before/$f.txt"
done
ls -la /tmp/pdf-parity-before/
```

Innehållet får inte ändras av en omstyling. De fem filerna är facit.

- [ ] **Steg 2: Skriv det fallerande testet**

Skapa `scripts/tests/test_prompt_pdf_parity.py`:

```python
"""Omstylingen får inte ändra ett ord i prompt-PDF:erna.

Och de svenska tecknen måste överleva typsnittsbytet — faller
renderaren tillbaka på ett systemsnitt bryts radbrytningen.
Granskningsfokus 2.
"""
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PDF_DIR = ROOT / "assets/pdfs/prompts"
BEFORE = Path("/tmp/pdf-parity-before")

SAMPLES = ["teachers-en", "principals-en", "mathematics-sv", "larare-sv", "skolchefer-sv"]


def extract(pdf: Path) -> str:
    return subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"],
        capture_output=True, text=True, check=True,
    ).stdout


@pytest.mark.parametrize("slug", SAMPLES)
def test_content_is_unchanged(slug):
    baseline = BEFORE / f"{slug}.txt"
    if not baseline.exists():
        pytest.skip(f"Inget facit för {slug} — kör steg 1 först")
    assert extract(PDF_DIR / f"{slug}.pdf").split() == baseline.read_text().split()


@pytest.mark.parametrize("slug", ["larare-sv", "skolchefer-sv", "mathematics-sv"])
def test_swedish_characters_survive(slug):
    text = extract(PDF_DIR / f"{slug}.pdf")
    assert any(ch in text for ch in "åäöÅÄÖ"), "svenska tecken saknas helt"
    # Ett saknat snitt ger ofta ersättningstecken i stället för diakriter.
    assert "�" not in text


def test_every_pack_rendered():
    assert len(list(PDF_DIR.glob("*.pdf"))) >= 124
```

- [ ] **Steg 3: Kör testet — det ska vara grönt redan nu**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_prompt_pdf_parity.py -v
```

Förväntat: PASS. Testet beskriver det tillstånd som ska överleva ändringen, inte ett nytt beteende. Är det rött här är facit fel sparat — gå tillbaka till steg 1.

- [ ] **Steg 4: Byt paletten i den delade stilmallen**

I `exports/prompts/_prompt-print.css`, ersätt `:root`-blocket:

```css
:root {
  --color-bg:           #FBFAF8;
  --color-bg-alt:       #EFF2F6;
  --color-text:         #0C1A2E;
  --color-text-soft:    #4E5A68;
  --color-accent:       #0B3A6F;
  --color-highlight:    #C2793A;
  --color-highlight-ink:#9C5A24;
  --color-border:       #DDE3EA;
  --color-dark-bg:      #0B3A6F;
  --color-dark-text:    #EFF2F6;

  --font-display: 'Hanken Grotesk', Helvetica, sans-serif;
  --font-body:    'Hanken Grotesk', Helvetica, sans-serif;
}
```

Byt `@import` mot självhostade typsnitt — PDF-bygget ska inte heller ringa Google:

```css
@font-face {
  font-family: 'Hanken Grotesk';
  src: url('../../assets/fonts/hanken-grotesk/HankenGrotesk-VariableFont.woff2') format('woff2');
  font-weight: 300 600;
  font-style: normal;
}
```

Byt de hårdkodade värdena i `@page`-blocken: `color: #6b6b65` → `#4E5A68`, `color: #1a1a18` → `#0C1A2E`, och `font-family: 'Fraunces', Georgia, serif` → `'Hanken Grotesk', sans-serif`. Sänk rubrikvikter från 700 till 300.

- [ ] **Steg 5: Rendera om alla 124**

```bash
/usr/bin/python3 exports/prompts/build-prompts-pdf.py
```

Förväntat: ~50 sekunder, 124 filer skrivna.

- [ ] **Steg 6: Kör testet och se att det fortfarande går igenom**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_prompt_pdf_parity.py -v
```

Förväntat: PASS. Fallerar `test_content_is_unchanged` har stilbytet flyttat text — oftast en sidbrytning som hamnat annorlunda. Jämför med `diff <(pdftotext -layout assets/pdfs/prompts/larare-sv.pdf -) /tmp/pdf-parity-before/larare-sv.txt`.

- [ ] **Steg 7: Ögna fem omslag**

```bash
open assets/pdfs/prompts/teachers-en.pdf assets/pdfs/prompts/larare-sv.pdf \
     assets/pdfs/prompts/mathematics-upper-secondary-en.pdf \
     assets/pdfs/prompts/skolchefer-sv.pdf assets/pdfs/prompts/physics-en.pdf
```

Kontrollera: omslaget är blått, etiketten kopparfärgad, sidnumren står kvar nere till höger, och å/ä/ö ser rätt ut i de svenska.

- [ ] **Steg 8: Commit**

```bash
git add exports/prompts/_prompt-print.css scripts/tests/test_prompt_pdf_parity.py \
        assets/pdfs/prompts
git commit -m "feat(pdf): restyle the 124 prompt packs to Blueprint"
```

---

### Uppgift 10: Skarp kontroll och PR

**Filer:**
- Skapa: `scripts/shoot-visual-check.py`
- Ändra: `sitemap.xml` och sidor som `build-seo-meta.py` rör (selektivt)

**Gränssnitt:**
- Konsumerar: allt ovan.
- Producerar: skärmbilder i `/tmp/visual-check/`.

- [ ] **Steg 1: Skriv skärmbildsskriptet**

Skapa `scripts/shoot-visual-check.py`:

```python
#!/usr/bin/env python3
"""Skärmbilder av tolv representativa sidor i tre bredder, båda språken.

Körs mot en lokal server på ny port — cachen ljuger annars.
"""
from __future__ import annotations

import http.server
import socketserver
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = Path("/tmp/visual-check")
PORT = 8801

PAGES = [
    ("", "home-en"), ("sv/", "home-sv"),
    ("wise/", "wise-en"), ("sv/ratt/", "wise-sv"),
    ("prompts/", "prompts-en"), ("sv/promptar/", "prompts-sv"),
    ("prompts/teachers/", "pack-en"), ("sv/promptar/larare/", "pack-sv"),
    ("guides/claude/", "guide-en"), ("sv/guider/claude/", "guide-sv"),
    ("evidence/", "evidence-en"), ("visual-codes/", "visualcodes-en"),
]
WIDTHS = [(390, "phone"), (834, "tablet"), (1440, "desktop")]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(
        *a, directory=str(ROOT), **kw
    )
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for width, wname in WIDTHS:
            page = browser.new_page(viewport={"width": width, "height": 1000})
            for path, name in PAGES:
                page.goto(f"http://127.0.0.1:{PORT}/{path}", wait_until="networkidle")
                page.wait_for_timeout(600)
                page.screenshot(path=str(OUT / f"{name}-{wname}.png"), full_page=True)
                print(f"{name}-{wname}")
            page.close()
        browser.close()
    httpd.shutdown()


if __name__ == "__main__":
    main()
```

- [ ] **Steg 2: Kör den och granska**

```bash
/usr/bin/python3 scripts/shoot-visual-check.py
open /tmp/visual-check
```

Gå igenom alla 36 bilderna. Leta efter: grön eller terrakotta som överlevt, fet display-text, rubriker där å/ä/ö nuddar raden ovanför, kort som fortfarande har skugga i stället för hårlinje, och text som tappat kontrast mot sin bakgrund.

- [ ] **Steg 3: Kontrollera fokusringen för hand**

```bash
python3 -m http.server 8802 --directory . &
sleep 1
open "http://localhost:8802/"
```

Tabba genom startsidan hela vägen ned i det mörka CTA-bandet och footern. Fokusmarkeringen ska synas tydligt på varje länk och knapp, även mot det blå bandet. Det är granskningsfokus 1 och går inte att automatisera meningsfullt. Stäng med `kill %1`.

- [ ] **Steg 4: Kör hela testsviten en sista gång**

```bash
/usr/bin/python3 -m pytest scripts/tests/ -v
```

Förväntat: PASS, allt.

- [ ] **Steg 5: Kör SEO-skriptet och återställ det som inte hör hit**

```bash
git status --porcelain > /tmp/before-seo.txt
python3 scripts/build-seo-meta.py
git status --porcelain > /tmp/after-seo.txt
diff /tmp/before-seo.txt /tmp/after-seo.txt
```

Skriptet härleder synligt "Last updated" ur git-commitdatum, så en sajtbred commit bumpar datumet även på sidor vars innehåll inte rörts. Gå igenom diffen och återställ varje sida där **bara** datumet ändrats:

```bash
git checkout -- <sökväg>
```

Behåll ändringarna i `sitemap.xml`.

- [ ] **Steg 6: Commit och PR**

```bash
git add scripts/shoot-visual-check.py sitemap.xml
git commit -m "chore(seo): refresh sitemap after the visual identity change"
git push -u origin feat/visual-identity-blueprint
gh pr create --title "Blueprint: ny visuell identitet (våg 1)" --body "$(cat <<'BODY'
Byter choosewise.educations grafiska uttryck till Blueprint-paletten och
Hanken Grotesk. Innehållet är oförändrat.

Spec: docs/superpowers/specs/2026-10-05-choosewise-visual-identity-design.md

- Nya tokens: djupblått som varumärkesfärg, koppar som enda varma ton
- Hanken Grotesk 300/400/500, Instrument Serif i citat, radavstånd 1.16
- Crestioras palett och Playfair Display borta ur publicerade filer
- Google Fonts-anropen borta från fyra sidor som läckte besökardata
- components.css tokeniserad (127 hårdkodade värden)
- og-kortens PNG-rendering är nu ett skript i stället för handarbete
- De 124 prompt-PDF:erna omrenderade, innehållet verifierat oförändrat

Våg 2 (guidernas mall och innehåll) och spåret för märke, favicon och
Skool-tillgångar ligger utanför den här PR:en.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
BODY
)"
```

**Mergas med merge-commit, inte squash** — repots konvention.

---

## Egengranskning

**Täckning mot specen:** §4 färgtokens → uppgift 1. §5 typografi och självhostning → uppgift 1 och 2. §6 användningsregler → uppgift 3, 5, 6 (vikt 300, hårlinjer, kopparnas två roller). §7 WISE-semantik → uppgift 5 och 6. §8 våg 1-tabellen → uppgift 2–9, rad för rad. §9 fällorna → uppgift 4 steg 5 (cache/ny port), uppgift 10 steg 5 (SEO-datum), varje commit listar filer (aldrig `git add -A`), uppgift 5 rör de föräldralösa filerna utan att radera dem. §10 definition av klart → uppgift 8 och 10.

**Inte täckt, medvetet:** spår A (märke, favicon, Skool-tillgångar) och våg 2 (guidernas mall och innehåll) ligger utanför den här planen enligt spec §8 och Johans beslut.

**Typkonsistens:** `ROOT` och `published_files()` bor i `scripts/tests/brandguard.py` (uppgift 2) och når uppgift 4 och 8 via `sys.path.insert` — samma mönster som `test_build_evidence_cards.py` redan använder, eftersom `scripts/tests/` är ett paket och testfiler därför inte kan importera varandra direkt. `scan()` och `CRESTIORA_FORBIDDEN` definieras i uppgift 4; uppgift 8 lägger `LEGACY_FORBIDDEN` i samma fil och behöver ingen import. `parse_tokens()` och `contrast()` stannar i uppgift 1.

**Interpretern:** varje `pytest`- och Playwright-kommando i planen anropar `/usr/bin/python3` explicit. Homebrews `python3` saknar båda paketen, så ett glömt prefix ger `No module named pytest` och inte ett rött test.
