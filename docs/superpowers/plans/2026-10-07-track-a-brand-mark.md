# Spår A — märket, faviconen och Skool-tillgångarna

> **För agentiska arbetare:** OBLIGATORISK UNDERSKILL: använd superpowers:subagent-driven-development för att genomföra planen uppgift för uppgift. Stegen använder kryssrutor (`- [ ]`).

**Mål:** Choosewise får ett märke — nålen genom ringen — som favicon, Skool-logga, Skool-omslag, LinkedIn-tillgångar och på de 12 delningskorten, allt härlett ur en enda källa och bevisat med test.

**Arkitektur:** Två SVG-källfiler bär geometrin. Allt annat genereras ur dem av ett skript: faviconer, PNG-tillgångar, og-kort. Faviconlänkarna når sidorna genom `build-seo-meta.py`, som redan injicerar ett block i varje `<head>` — ett skript att ändra i stället för 199 filer. En vakt jämför banddata i varje märkesbärande SVG mot källan, så att ingen yta kan få en egen teckning.

**Teknikstack:** Playwright (Chromium) för SVG→PNG via lokal server, Pillow för `.ico`, pytest. `/usr/bin/python3` (3.9.6) är **enda** interpretern med pytest, playwright och Pillow.

**Spec:** `docs/superpowers/specs/2026-10-07-choosewise-brand-mark-design.md`

**Gren:** `feat/blueprint-track-a-mark` (finns, specen är committad där)

## Globala villkor

Kopierade ordagrant ur specen. Varje uppgifts krav omfattar det här avsnittet.

- **Geometrin är bindande.** 64×64-ruta. Ring: centrum 32,32, radie **21**, linjebredd **2,5**, `fill="none"`. Nål norr: `M32 6 L37.5 32 L26.5 32 Z`. Nål söder: `M32 58 L37.5 32 L26.5 32 Z`. Nålsöga: centrum 32,32, radie **2,6**, fylld med **bottnens färg**.
- **Två färglägen, inga fler.** Mot mörkt: ring `#FBFAF8`, norr `#E8C9A8`, söder `#FBFAF8`, nålsöga `#0B3A6F`. Mot ljust: ring `#0B3A6F`, norr `#C2793A`, söder `#0B3A6F`, nålsöga `#FBFAF8`.
- **Kopparn mot blått är `#E8C9A8`.** `#C2793A` når bara 3,0:1 mot `#0B3A6F`. Regeln bröts fem gånger i våg 1.
- **Minsta storlek 16 px. Frizon: 11 enheter** i 64-rutan.
- **Sajtens header rörs inte.** Ordmärket står kvar som ren text.
- **Guidomslagen rörs inte här.** Regeln dokumenteras, våg 2a tillämpar den.
- **`git add -A` används aldrig.** Repot har ett trettiotal ocommittade ändringar som hör till Johan. `docs/` är gitignorerad — spec och plan läggs till med `git add -f`.
- **`/usr/bin/python3` i varje kommando.** Inte `python3`.

## Granskningsfokus

Fem fall specen förutsätter men som ingen uppgifts tester annars når. Var och en har fått sitt test i den uppgift som äger koden.

1. **Dolda guidsidor.** `build_seo_block` returnerar tidigt för `HIDDEN_PATHS` med bara en `noindex`-tagg. Byggs faviconlänkarna efter den returen får sex guidsidor per språk ingen favicon. → Uppgift 4 testar en sida ur `HIDDEN_PATHS` uttryckligen.
2. **Sidor utan `<head>`.** Fyra publicerade filer är partialer. `inject_head` returnerar dem orörda, och vakten måste räkna 199 av 203 utan att kalla de fyra för fel. → Uppgift 4.
3. **Transparent favicon mot mörkt flikgränssnitt.** Märket utan botten försvinner i mörkt läge. Alla tre faviconfilerna ska ha varumärkesblå botten. → Uppgift 3 mäter en pixel mitt på vänsterkanten, som ligger på bottnen; hörnen är genomskinliga i en rundad ruta och duger inte som mätpunkt.
4. **`.ico` med bara en storlek.** Pillow skriver gärna en enda bild om `sizes` utelämnas, och då skalar äldre webbläsare 32 ned till 16 med dåligt resultat. → Uppgift 3 testar att filen innehåller både 16 och 32.
5. **og-kort som ändras i SVG men inte i PNG.** og-taggarna pekar på PNG. Ett kort vars SVG fått märket men vars PNG är gammal ser oförändrat ut för varje delad länk. → Uppgift 5 jämför märkets närvaro i PNG-pixlarna, inte bara i SVG-källan.

---

## Filstruktur

**Skapas:**
- `assets/images/brand/mark-on-dark.svg`, `assets/images/brand/mark-on-light.svg` — geometrins enda källa
- `scripts/build-brand-assets.py` — genererar faviconer och PNG-tillgångar ur källorna
- `scripts/tests/test_brand_mark.py` — de fyra vakterna
- `favicon.svg`, `favicon.ico`, `apple-touch-icon.png` — repots rot
- `assets/images/brand/skool/logo.png`, `cover.svg`, `cover.png`
- `assets/images/brand/linkedin/page-logo.png`, `page-banner.svg`, `page-banner.png`, `personal-banner.svg`, `personal-banner.png`

**Ändras:**
- `scripts/build-seo-meta.py` — faviconlänkarna i `<head>`
- `assets/images/brand/og/*.svg` — 12 kort får märket
- `assets/images/brand/og/*.png` — renderas om

---

## Uppgift 1: Märket som källa

**Filer:**
- Skapa: `assets/images/brand/mark-on-dark.svg`, `assets/images/brand/mark-on-light.svg`
- Skapa: `scripts/tests/test_brand_mark.py`

**Gränssnitt:**
- Producerar: två SVG-filer med `viewBox="0 0 64 64"`, transparent botten, fyra element var i ordningen ring, nål-söder, nål-norr, nålsöga.
- Konsumeras av: uppgift 2, 3 och 5, som alla läser banddata ur de här filerna.

- [ ] **Steg 1: Skriv vakten som ska bli röd**

```python
# scripts/tests/test_brand_mark.py
"""Märket har en enda källa, och den källan har bindande mått.

Geometrin valdes efter mätning vid 16 och 32 pixlar. Ändras ett mått på
känsla faller läsbarheten i just de storlekar märket används mest, och
det syns inte i stort format. Därför är måtten testade och inte bara
beskrivna.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DARK = ROOT / "assets/images/brand/mark-on-dark.svg"
LIGHT = ROOT / "assets/images/brand/mark-on-light.svg"

NEEDLE_NORTH = "M32 6 L37.5 32 L26.5 32 Z"
NEEDLE_SOUTH = "M32 58 L37.5 32 L26.5 32 Z"

STATES = {
    DARK:  {"ring": "#FBFAF8", "north": "#E8C9A8", "south": "#FBFAF8", "eye": "#0B3A6F"},
    LIGHT: {"ring": "#0B3A6F", "north": "#C2793A", "south": "#0B3A6F", "eye": "#FBFAF8"},
}


@pytest.mark.parametrize("path", list(STATES), ids=lambda p: p.name)
def test_viewbox_is_the_64_grid(path: Path):
    assert 'viewBox="0 0 64 64"' in path.read_text(encoding="utf-8")


@pytest.mark.parametrize("path", list(STATES), ids=lambda p: p.name)
def test_ring_geometry(path: Path):
    text = path.read_text(encoding="utf-8")
    ring = re.search(r'<circle[^>]*r="21"[^>]*>', text)
    assert ring, "ringen med radie 21 saknas"
    assert 'stroke-width="2.5"' in ring.group(0)
    assert 'fill="none"' in ring.group(0)
    assert 'cx="32"' in ring.group(0) and 'cy="32"' in ring.group(0)


@pytest.mark.parametrize("path", list(STATES), ids=lambda p: p.name)
def test_both_needle_halves_are_exact(path: Path):
    text = path.read_text(encoding="utf-8")
    for d in (NEEDLE_NORTH, NEEDLE_SOUTH):
        assert f'd="{d}"' in text, f"nålhalvan {d} saknas eller har ändrade mått"


@pytest.mark.parametrize("path", list(STATES), ids=lambda p: p.name)
def test_needle_eye_takes_the_ground_colour(path: Path):
    """Nålsögat är ett HÅL i nålen. Får det nålens färg försvinner det."""
    text = path.read_text(encoding="utf-8")
    eye = re.search(r'<circle[^>]*r="2\.6"[^>]*>', text)
    assert eye, "nålsögat med radie 2,6 saknas"
    assert STATES[path]["eye"] in eye.group(0)


@pytest.mark.parametrize("path", list(STATES), ids=lambda p: p.name)
def test_only_the_four_palette_values(path: Path):
    allowed = {"#FBFAF8", "#0B3A6F", "#E8C9A8", "#C2793A"}
    found = {m.upper() for m in re.findall(r"#[0-9a-fA-F]{6}", path.read_text(encoding="utf-8"))}
    assert found <= allowed, f"främmande färger: {sorted(found - allowed)}"


def test_the_two_states_share_one_geometry():
    """Skillnaden mellan filerna får vara färg och ingenting annat."""
    def skeleton(p: Path) -> str:
        return re.sub(r'(fill|stroke)="#[0-9a-fA-F]{6}"', r'\1="X"',
                      p.read_text(encoding="utf-8"))
    assert skeleton(DARK) == skeleton(LIGHT)
```

- [ ] **Steg 2: Kör vakten och se den falla**

```bash
cd /Users/johan/Projekt/Choosewise/choosewise-education
/usr/bin/python3 -m pytest scripts/tests/test_brand_mark.py -q
```

Förväntat: alla fel med `FileNotFoundError` — källfilerna finns inte än.

- [ ] **Steg 3: Skriv de två källfilerna**

```xml
<!-- assets/images/brand/mark-on-dark.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64"
     role="img" aria-label="Choosewise">
  <!-- Nålen genom ringen. Måtten är bindande: de valdes efter mätning
       vid 16 och 32 pixlar. Nålsögat är ett HÅL i nålen och har därför
       bottnens färg, inte nålens. -->
  <circle cx="32" cy="32" r="21" fill="none" stroke="#FBFAF8" stroke-width="2.5"/>
  <path d="M32 58 L37.5 32 L26.5 32 Z" fill="#FBFAF8"/>
  <path d="M32 6 L37.5 32 L26.5 32 Z" fill="#E8C9A8"/>
  <circle cx="32" cy="32" r="2.6" fill="#0B3A6F"/>
</svg>
```

```xml
<!-- assets/images/brand/mark-on-light.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64"
     role="img" aria-label="Choosewise">
  <circle cx="32" cy="32" r="21" fill="none" stroke="#0B3A6F" stroke-width="2.5"/>
  <path d="M32 58 L37.5 32 L26.5 32 Z" fill="#0B3A6F"/>
  <path d="M32 6 L37.5 32 L26.5 32 Z" fill="#C2793A"/>
  <circle cx="32" cy="32" r="2.6" fill="#FBFAF8"/>
</svg>
```

- [ ] **Steg 4: Kör vakten och se den bli grön**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_brand_mark.py -q
```

- [ ] **Steg 5: Bevisa att vakten kan bli röd**

```bash
/usr/bin/sed -i '' 's/r="21"/r="24"/' assets/images/brand/mark-on-dark.svg
/usr/bin/python3 -m pytest scripts/tests/test_brand_mark.py -q -k ring
git checkout -- assets/images/brand/mark-on-dark.svg
```

Förväntat: rött på `test_ring_geometry`, grönt igen efter återställningen. I våg 1 kunde fyra tester inte falla på det de påstod sig vakta — det här steget är billigare än att upptäcka samma sak i efterhand.

- [ ] **Steg 6: Commit**

```bash
git add assets/images/brand/mark-on-dark.svg assets/images/brand/mark-on-light.svg \
  scripts/tests/test_brand_mark.py
git commit -m "feat(brand): add the Choosewise mark as two source files"
```

---

## Uppgift 2: Generatorn

Ett skript som gör varje tillgång ur källorna. Skälet att det är ett skript och inte handarbete: specen kräver att allt kommer ur samma teckning, och ett skript kan inte glömma det.

**Filer:**
- Skapa: `scripts/build-brand-assets.py`

**Gränssnitt:**
- Producerar: `build_brand_assets.mark_markup(state: str) -> str` som returnerar märkets fyra element som SVG-sträng, läst ur källfilen och inte skriven på nytt. Funktionerna `tile_svg(size, radius_pct)`, `render_png(svg_text, w, h, out)`.
- Konsumeras av: uppgift 3 och 5.

- [ ] **Steg 1: Skriv skriptet**

```python
#!/usr/bin/env python3
# scripts/build-brand-assets.py
"""Genererar varje varumärkestillgång ur de två källfilerna.

Varför ett skript: specen kräver att favicon, Skool-logga, omslag och
LinkedIn-tillgångar kommer ur SAMMA teckning. Handarbete glömmer det
förr eller senare; ett skript som läser källan kan inte.

Rendering kräver en lokal server — file:// ger fallback-typsnitt och fel
radbrytning. Samma skäl som i render-og-pngs.py.

Kör:  /usr/bin/python3 scripts/build-brand-assets.py
"""
from __future__ import annotations

import http.server
import re
import socketserver
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "assets/images/brand"
PORT = 8801

BLUE = "#0B3A6F"
CREAM = "#FBFAF8"
COPPER_DK = "#E8C9A8"

# Märkets element plockas UT ur källfilen, aldrig skrivna på nytt här.
# Skriver man dem två gånger har man två sanningar.
_INNER = re.compile(r"<svg[^>]*>(.*)</svg>", re.S)


def mark_markup(state: str) -> str:
    """state: 'dark' eller 'light'."""
    src = BRAND / f"mark-on-{state}.svg"
    body = _INNER.search(src.read_text(encoding="utf-8")).group(1)
    # Kommentarer ur källan följer inte med in i genererade filer.
    return re.sub(r"<!--.*?-->", "", body, flags=re.S).strip()


def tile_svg(size: int, radius_pct: float = 22.0, state: str = "dark") -> str:
    """Märket på varumärkesblå botten med rundade hörn.

    Botten är inte dekoration: en transparent favicon försvinner mot
    mörkt flikgränssnitt.
    """
    r = size * radius_pct / 100
    inner = size * 0.62          # märket upptar 62 % av rutan
    off = (size - inner) / 2     # frizonen runt om
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 {size} {size}">'
        f'<rect width="{size}" height="{size}" rx="{r:.2f}" fill="{BLUE}"/>'
        f'<svg x="{off:.2f}" y="{off:.2f}" width="{inner:.2f}" height="{inner:.2f}" '
        f'viewBox="0 0 64 64">{mark_markup(state)}</svg>'
        f'</svg>'
    )


def serve() -> socketserver.TCPServer:
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(
        *a, directory=str(ROOT), **kw)
    try:
        httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    except OSError as exc:
        raise SystemExit(
            f"Kunde inte binda 127.0.0.1:{PORT} ({exc}). Troligen en kvarglömd "
            f"server — kör `lsof -i :{PORT}`, avsluta processen, eller ändra PORT.")
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def render_png(page, svg_text: str, w: int, h: int, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    page.set_viewport_size({"width": w, "height": h})
    page.set_content(
        f'<body style="margin:0">{svg_text}</body>',
        wait_until="load")
    page.wait_for_timeout(220)   # typsnittet ska hinna in innan bilden tas
    page.screenshot(path=str(out), omit_background=True)
```

- [ ] **Steg 2: Kontrollera att märket plockas ur källan och inte skrivs om**

```bash
cd /Users/johan/Projekt/Choosewise/choosewise-education
/usr/bin/python3 -c "
import sys; sys.path.insert(0,'scripts')
import importlib.util
spec = importlib.util.spec_from_file_location('bba','scripts/build-brand-assets.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(m.mark_markup('dark'))
"
```

Förväntat: de fyra elementen med `r=\"21\"`, båda nålhalvorna och nålsögat — ordagrant som i källfilen.

- [ ] **Steg 3: Commit**

```bash
git add scripts/build-brand-assets.py
git commit -m "feat(brand): add the asset generator that reads the mark from source"
```

---

## Uppgift 3: Faviconerna

**Filer:**
- Ändra: `scripts/build-brand-assets.py` (favicondelen)
- Skapa: `favicon.svg`, `favicon.ico`, `apple-touch-icon.png` i repots rot
- Ändra: `scripts/tests/test_brand_mark.py` (vakt 3 och 4)

**Gränssnitt:**
- Konsumerar: `tile_svg` och `render_png` från uppgift 2.
- Producerar: tre filer i repots rot.

- [ ] **Steg 1: Lägg till favicondelen i generatorn**

```python
def build_favicons(page) -> None:
    """Tre filer: SVG för moderna webbläsare, .ico för äldre, PNG för hemskärm."""
    (ROOT / "favicon.svg").write_text(tile_svg(64), encoding="utf-8")

    render_png(page, tile_svg(180), 180, 180, ROOT / "apple-touch-icon.png")

    # .ico ska innehålla BÅDE 16 och 32. Utelämnas sizes skriver Pillow en
    # enda bild, och äldre webbläsare skalar då 32 ned till 16 själva med
    # dåligt resultat.
    render_png(page, tile_svg(32), 32, 32, ROOT / "_ico32.png")
    img = Image.open(ROOT / "_ico32.png").convert("RGBA")
    img.save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32)])
    (ROOT / "_ico32.png").unlink()
```

- [ ] **Steg 2: Skriv vakterna**

Lägg till i `scripts/tests/test_brand_mark.py`:

```python
from PIL import Image

FAVICON_SVG = ROOT / "favicon.svg"
FAVICON_ICO = ROOT / "favicon.ico"
APPLE_TOUCH = ROOT / "apple-touch-icon.png"


def test_favicon_files_exist():
    for f in (FAVICON_SVG, FAVICON_ICO, APPLE_TOUCH):
        assert f.exists(), f"{f.name} saknas"


def test_apple_touch_icon_is_180_square():
    assert Image.open(APPLE_TOUCH).size == (180, 180)


def test_ico_carries_both_sizes():
    """En .ico med bara en storlek låter webbläsaren skala ned 32 till 16."""
    with Image.open(FAVICON_ICO) as im:
        sizes = set(im.info.get("sizes", ()))
    assert {(16, 16), (32, 32)} <= sizes, f"ico innehåller {sorted(sizes)}"


def test_favicons_have_the_brand_ground_not_transparency():
    """Ett märke utan botten försvinner mot mörkt flikgränssnitt.

    Hörnpixeln ligger utanför hörnradien och är alltså genomskinlig i en
    rundad ruta — mätpunkten är därför mitt på vänsterkanten, som ligger
    på bottnen.
    """
    im = Image.open(APPLE_TOUCH).convert("RGBA")
    r, g, b, a = im.getpixel((2, im.height // 2))
    assert a == 255, "bottnen är genomskinlig"
    assert (r, g, b) == (0x0B, 0x3A, 0x6F), f"fel bottenfärg: {(r, g, b)}"
    assert "#0B3A6F" in FAVICON_SVG.read_text(encoding="utf-8")
```

- [ ] **Steg 3: Kör generatorn**

```bash
cd /Users/johan/Projekt/Choosewise/choosewise-education
/usr/bin/python3 scripts/build-brand-assets.py
/usr/bin/python3 -m pytest scripts/tests/test_brand_mark.py -q
```

- [ ] **Steg 4: Titta på faviconen i verklig storlek**

```bash
/usr/bin/python3 -m http.server 8802 >/dev/null 2>&1 &
open http://localhost:8802/
```

Granska flikraden i både ljust och mörkt systemläge. Stäng servern efteråt. Safari cachar faviconer hårt — använd en ny port om en gammal ikon sitter kvar.

- [ ] **Steg 5: Commit**

```bash
git add favicon.svg favicon.ico apple-touch-icon.png scripts/build-brand-assets.py \
  scripts/tests/test_brand_mark.py
git commit -m "feat(brand): generate the favicon in all three formats"
```

---

## Uppgift 4: Faviconen når varje sida

**Filer:**
- Ändra: `scripts/build-seo-meta.py`
- Ändra: `scripts/tests/test_brand_mark.py`

**Gränssnitt:**
- Producerar: tre `<link>`-rader i varje sidas seo-block.

`build_seo_block` returnerar **tidigt** för sökvägarna i `HIDDEN_PATHS` och skickar då bara en `noindex`-tagg. Faviconlänkarna måste byggas före den returen, annars får sex guidsidor per språk ingen favicon.

- [ ] **Steg 1: Skriv vakten som ska bli röd**

```python
import subprocess
from . import brandguard

FAVICON_LINKS = (
    '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
    '<link rel="icon" href="/favicon.ico" sizes="32x32">',
    '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
)

PAGES = [p for p in brandguard.published_files((".html",))
         if "<head" in p.read_text(encoding="utf-8", errors="replace")]


def test_the_page_count_is_what_we_think():
    """199 av 203. Faller globbet ihop vaktar resten ingenting."""
    assert len(PAGES) == 199, len(PAGES)


@pytest.mark.parametrize("path", PAGES, ids=lambda p: str(p.relative_to(ROOT)))
def test_every_page_links_the_favicon(path):
    text = path.read_text(encoding="utf-8")
    missing = [l for l in FAVICON_LINKS if l not in text]
    assert not missing, f"{path.relative_to(ROOT)} saknar {missing}"


def test_hidden_pages_get_the_favicon_too():
    """build_seo_block returnerar tidigt för HIDDEN_PATHS med bara en
    noindex-tagg. Byggs länkarna efter den returen får guidsidorna ingen."""
    hidden = ROOT / "guides/claude/index.html"
    text = hidden.read_text(encoding="utf-8")
    assert "noindex" in text, "testet pekar på fel sida — den här är inte dold"
    for link in FAVICON_LINKS:
        assert link in text, f"dold sida saknar {link}"
```

- [ ] **Steg 2: Kör och se den falla**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_brand_mark.py -q -k favicon
```

Förväntat: 199 fel på länkarna plus det dolda fallet.

- [ ] **Steg 3: Lägg länkarna i seo-blocket, före den tidiga returen**

I `scripts/build-seo-meta.py`, i `build_seo_block`:

```python
def build_seo_block(canonical_path: str, lang: str, html: str,
                    last_modified: str) -> str:
    # Faviconen gäller varje sida, även de dolda. Raderna byggs därför
    # FÖRE den tidiga returen för HIDDEN_PATHS — läggs de efter får de
    # sex guidsidorna per språk ingen favicon.
    favicon = [
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
        '<link rel="icon" href="/favicon.ico" sizes="32x32">',
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
    ]
    if canonical_path in HIDDEN_PATHS:
        return "\n".join([SEO_MARK_START,
                          '<meta name="robots" content="noindex,nofollow">',
                          *favicon,
                          SEO_MARK_END])
    canonical_url = BASE_URL + canonical_path
    lines = [SEO_MARK_START, f'<link rel="canonical" href="{canonical_url}">', *favicon]
    ...
```

- [ ] **Steg 4: Kör skriptet och kontrollera vad det rörde**

```bash
/usr/bin/python3 scripts/build-seo-meta.py
git diff --stat | tail -3
```

**`build-seo-meta.py` bumpar "Last updated"** ur git-commitdatum. Kontrollera att inga sidor fått nytt datum av en körning som bara skulle lägga till tre länkar:

```bash
git diff -U0 | grep -E "^[+-].*(page-last-updated|dateModified)" | head -20
```

Finns sådana rader: återställ dem innan commit. De hör inte till det här arbetet.

- [ ] **Steg 5: Kör vakten och se den bli grön**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_brand_mark.py -q
```

- [ ] **Steg 6: Commit**

```bash
git add scripts/build-seo-meta.py scripts/tests/test_brand_mark.py
git add $(git diff --name-only -- '*.html')
git commit -m "feat(brand): link the favicon from every page, hidden ones included"
```

---

## Uppgift 5: og-korten

De 12 korten har **mörk botten** — en övertoning från `#07284D` till `#0B3A6F` — så märket tar sitt **mörka** skick. og-taggarna pekar på PNG, så SVG-ändringen räcker inte.

**Filer:**
- Ändra: `assets/images/brand/og/*.svg` (12 filer), `assets/images/brand/og-default.svg`
- Ändra: `assets/images/brand/og/*.png` (renderas om)
- Ändra: `scripts/tests/test_brand_mark.py`

- [ ] **Steg 1: Skriv vakten**

```python
OG_DIR = ROOT / "assets/images/brand/og"
OG_SVGS = sorted(OG_DIR.glob("*.svg"))


def test_there_are_twelve_og_cards():
    assert len(OG_SVGS) == 12, [p.name for p in OG_SVGS]


@pytest.mark.parametrize("svg", OG_SVGS, ids=lambda p: p.name)
def test_every_og_card_carries_the_mark(svg):
    """Samma banddata som källan — inte en egen teckning av nålen."""
    text = svg.read_text(encoding="utf-8")
    for d in (NEEDLE_NORTH, NEEDLE_SOUTH):
        assert f'd="{d}"' in text, f"{svg.name} saknar nålen"
    assert "#E8C9A8" in text, f"{svg.name}: norrspetsen ska vara ljus koppar mot mörkt"


@pytest.mark.parametrize("svg", OG_SVGS, ids=lambda p: p.name)
def test_the_png_was_rendered_after_the_svg(svg):
    """og-taggarna pekar på PNG. En SVG med märket och en gammal PNG ser
    oförändrad ut för varje delad länk, och felet upptäcks aldrig."""
    png = svg.with_suffix(".png")
    assert png.exists(), f"{png.name} saknas"
    im = Image.open(png).convert("RGB")
    assert im.size == (1200, 630)
    # Märket sitter uppe till vänster. Finns ljus koppar i den rutan har
    # PNG:en renderats om efter att märket lades in.
    box = im.crop((60, 50, 200, 190)).getcolors(140 * 140) or []
    assert any(c == (0xE8, 0xC9, 0xA8) for _, c in box), \
        f"{png.name} saknar märkets koppar — PNG:en är inte omrenderad"
```

- [ ] **Steg 2: Kör och se den falla**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_brand_mark.py -q -k og
```

- [ ] **Steg 3: Lägg märket i de 12 korten plus standardkortet**

Infoga direkt efter bottenrektangeln i varje `assets/images/brand/og/*.svg` och i `og-default.svg`:

```xml
  <!-- Märket, hämtat ur assets/images/brand/mark-on-dark.svg. Ändras det
       där ska det ändras här — vakten i test_brand_mark.py jämför banorna. -->
  <svg x="80" y="64" width="112" height="112" viewBox="0 0 64 64">
    <circle cx="32" cy="32" r="21" fill="none" stroke="#FBFAF8" stroke-width="2.5"/>
    <path d="M32 58 L37.5 32 L26.5 32 Z" fill="#FBFAF8"/>
    <path d="M32 6 L37.5 32 L26.5 32 Z" fill="#E8C9A8"/>
    <circle cx="32" cy="32" r="2.6" fill="#0B3A6F"/>
  </svg>
```

Kontrollera i varje kort att märket inte krockar med texten — rubrikerna börjar på olika höjd. Flytta texten, aldrig märket.

- [ ] **Steg 4: Rendera om PNG:erna**

```bash
/usr/bin/python3 scripts/render-og-pngs.py
/usr/bin/python3 -m pytest scripts/tests/test_brand_mark.py -q -k og
```

- [ ] **Steg 5: Titta på två kort**

```bash
open assets/images/brand/og/wise-en.png assets/images/brand/og/prompts-sv.png
```

- [ ] **Steg 6: Commit**

```bash
git add assets/images/brand/og/ assets/images/brand/og-default.svg \
  scripts/tests/test_brand_mark.py
git commit -m "feat(brand): put the mark on the twelve share cards"
```

---

## Uppgift 6: Skool- och LinkedIn-tillgångarna

**Filer:**
- Ändra: `scripts/build-brand-assets.py`
- Skapa: `assets/images/brand/skool/logo.png`, `cover.svg`, `cover.png`
- Skapa: `assets/images/brand/linkedin/page-logo.png`, `page-banner.svg`, `page-banner.png`, `personal-banner.svg`, `personal-banner.png`
- Ändra: `scripts/tests/test_brand_mark.py`

- [ ] **Steg 1: Lägg till tillgångarna i generatorn**

```python
def card_svg(w: int, h: int, mark_size: int, mark_x: int, mark_y: int,
             title: str | None, subtitle: str | None,
             title_pt: int, sub_pt: int, text_x: int,
             title_y: int, sub_y: int, band: int) -> str:
    """Mörkt kort med märket, rubrik, underrubrik och kopparbandet nederst.

    Bandet är samma band som sajtens footer. Det är det som binder
    Skool och LinkedIn till sajten visuellt.
    """
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}">',
        '<style>@font-face{font-family:"Hanken Grotesk";'
        'src:url("/assets/fonts/hanken-grotesk/HankenGrotesk-VariableFont.woff2") '
        'format("woff2");font-weight:300 600}</style>',
        f'<rect width="{w}" height="{h}" fill="{BLUE}"/>',
        f'<rect y="{h - band}" width="{w}" height="{band}" fill="#C2793A"/>',
        f'<svg x="{mark_x}" y="{mark_y}" width="{mark_size}" height="{mark_size}" '
        f'viewBox="0 0 64 64">{mark_markup("dark")}</svg>',
    ]
    if title:
        parts.append(
            f'<text x="{text_x}" y="{title_y}" font-family="Hanken Grotesk, sans-serif" '
            f'font-size="{title_pt}" font-weight="300" fill="{CREAM}" '
            f'letter-spacing="-2">{title}</text>')
    if subtitle:
        parts.append(
            f'<text x="{text_x}" y="{sub_y}" font-family="Hanken Grotesk, sans-serif" '
            f'font-size="{sub_pt}" font-weight="400" fill="{COPPER_DK}" '
            f'letter-spacing="1.6">{subtitle}</text>')
    parts.append("</svg>")
    return "".join(parts)


TITLE = "Choosewise"
SUBTITLE = "AI &amp; EdTech for Educators"


def build_skool(page) -> None:
    out = BRAND / "skool"
    render_png(page, tile_svg(1024, radius_pct=0), 1024, 1024, out / "logo.png")
    cover = card_svg(1400, 790, 168, 112, 150, TITLE, SUBTITLE,
                     104, 42, 112, 438, 512, 24)
    (out / "cover.svg").write_text(cover, encoding="utf-8")
    render_png(page, cover, 1400, 790, out / "cover.png")


def build_linkedin(page) -> None:
    out = BRAND / "linkedin"
    render_png(page, tile_svg(300, radius_pct=0), 300, 300, out / "page-logo.png")

    page_banner = card_svg(1128, 191, 88, 56, 46, TITLE, SUBTITLE,
                           46, 21, 176, 94, 130, 8)
    (out / "page-banner.svg").write_text(page_banner, encoding="utf-8")
    render_png(page, page_banner, 1128, 191, out / "page-banner.png")

    # Den personliga bannern: LinkedIn lägger profilbilden över vänstra
    # delen, så märket och texten börjar längre in än på sidbannern.
    personal = card_svg(1584, 396, 120, 90, 138, TITLE, SUBTITLE,
                        62, 28, 248, 196, 246, 12)
    (out / "personal-banner.svg").write_text(personal, encoding="utf-8")
    render_png(page, personal, 1584, 396, out / "personal-banner.png")


def main() -> None:
    httpd = serve()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(device_scale_factor=1)
            build_favicons(page)
            build_skool(page)
            build_linkedin(page)
            browser.close()
    finally:
        httpd.shutdown()
    print("klart")


if __name__ == "__main__":
    main()
```

- [ ] **Steg 2: Skriv vakten**

```python
EXPECTED_SIZES = {
    "skool/logo.png": (1024, 1024),
    "skool/cover.png": (1400, 790),
    "linkedin/page-logo.png": (300, 300),
    "linkedin/page-banner.png": (1128, 191),
    "linkedin/personal-banner.png": (1584, 396),
}


@pytest.mark.parametrize("rel,size", EXPECTED_SIZES.items())
def test_asset_exists_with_exact_size(rel, size):
    path = ROOT / "assets/images/brand" / rel
    assert path.exists(), f"{rel} saknas"
    assert Image.open(path).size == size


@pytest.mark.parametrize("rel", ["skool/cover.svg", "linkedin/page-banner.svg",
                                 "linkedin/personal-banner.svg"])
def test_generated_card_carries_the_marks_own_paths(rel):
    text = (ROOT / "assets/images/brand" / rel).read_text(encoding="utf-8")
    for d in (NEEDLE_NORTH, NEEDLE_SOUTH):
        assert f'd="{d}"' in text, f"{rel} har en egen teckning av nålen"
```

- [ ] **Steg 3: Kör generatorn och vakten**

```bash
/usr/bin/python3 scripts/build-brand-assets.py
/usr/bin/python3 -m pytest scripts/tests/test_brand_mark.py -q
```

- [ ] **Steg 4: Granska i Skools egen beskärning**

```bash
open assets/images/brand/skool/logo.png assets/images/brand/skool/cover.png \
     assets/images/brand/linkedin/personal-banner.png
```

Skool beskär loggan **rund**. Kontrollera att nålspetsarna har marginal till kanten — de ligger 26 enheter från mitten i 64-rutan mot beskärningens 32, men mät i bilden och lita inte på räkningen.

- [ ] **Steg 5: Commit**

```bash
git add scripts/build-brand-assets.py assets/images/brand/skool/ \
  assets/images/brand/linkedin/ scripts/tests/test_brand_mark.py
git commit -m "feat(brand): generate the Skool and LinkedIn assets"
```

---

## Uppgift 7: Guidomslagets regel, och PR

Spår A levererar **regeln** för guidomslagen; våg 2a tillämpar den. Det som skrivs här är det våg 2a läser.

**Filer:**
- Skapa: `docs/brand-mark-usage.md`

- [ ] **Steg 1: Skriv bruksanvisningen**

```markdown
# Choosewise-märket — så används det

**Källan:** `assets/images/brand/mark-on-dark.svg` och `mark-on-light.svg`.
Allt annat genereras ur dem av `scripts/build-brand-assets.py`. Rita aldrig
märket på nytt i en enskild fil — vakten i `scripts/tests/test_brand_mark.py`
jämför banddata och blir röd.

## Geometri — bindande

Allt i en 64×64-ruta. Måtten valdes efter mätning vid 16 och 32 pixlar.

| Element | Värde |
|---|---|
| Ring | centrum 32,32 · radie 21 · linjebredd 2,5 · `fill="none"` |
| Nål, norr | `M32 6 L37.5 32 L26.5 32 Z` |
| Nål, söder | `M32 58 L37.5 32 L26.5 32 Z` |
| Nålsöga | centrum 32,32 · radie 2,6 · **bottnens färg** |

Nålsögat är ett hål i nålen, inte en prick ovanpå.

## Två färglägen, inga fler

| | Mot mörkt | Mot ljust |
|---|---|---|
| Ring | `#FBFAF8` | `#0B3A6F` |
| Nål, norr | `#E8C9A8` | `#C2793A` |
| Nål, söder | `#FBFAF8` | `#0B3A6F` |
| Nålsöga | `#0B3A6F` | `#FBFAF8` |

Kopparn mot blått är `#E8C9A8`. `#C2793A` når bara 3,0:1 mot `#0B3A6F`
och slocknar i små storlekar.

## Regler

- Minsta storlek **16 px**. Under det används märket inte alls.
- Frizon **11 enheter** i 64-rutan, alltså 17 % av bredden, runt om.
- Aldrig omfärgat utanför de två lägena, roterat, lutat, med skugga eller
  kontur, ihoptryckt, eller mot en botten som varken är papper eller
  varumärkesblå.
- Sajtens header bär inget märke. Ordmärket står som ren text.

## Guidomslag — regeln våg 2a tillämpar

Märket sitter **uppe till vänster**, 34 enheter brett på ett A4 (210×297),
med 24 enheters marginal från vänsterkant och topp. Mörkt omslag tar det
mörka läget, ljust omslag det ljusa.

Märket är litet med flit: på ett guidomslag är titeln avsändaren och
märket bara signaturen. Under titeln går kopparlinjen, och under den
`CHOOSEWISE.EDUCATION` spärrat — i `#E8C9A8` mot mörkt, `#9C5A24` mot
ljust.
```

- [ ] **Steg 2: Hela sviten**

```bash
cd /Users/johan/Projekt/Choosewise/choosewise-education
/usr/bin/python3 -m pytest scripts/tests/ -q
```

Förväntat: våg 1:s 110 plus spår A:s nya, alla gröna.

- [ ] **Steg 3: Kontrollera att inget orelaterat följer med**

```bash
git status --short | grep -vE "favicon|apple-touch|assets/images/brand|scripts/|docs/" | head -20
```

Förväntat: bara Johans egna ocommittade filer, som ska lämnas i fred.

- [ ] **Steg 4: Push och PR**

```bash
git add -f docs/brand-mark-usage.md
git commit -m "docs(brand): write the mark usage rules wave 2a will apply"
git push -u origin feat/blueprint-track-a-mark
gh pr create --base main --title "Spår A: märket, faviconen och Skool-tillgångarna" --body "$(cat <<'EOF'
Choosewise får ett märke: nålen genom ringen, vald bland sex kandidater
efter mätning vid 16 och 32 pixlar.

Två SVG-källfiler bär geometrin. Allt annat genereras ur dem av
`scripts/build-brand-assets.py` — faviconerna i tre format, Skool-loggan
och omslaget 1400×790, LinkedIn i tre mått. De 12 delningskorten får
märket och PNG:erna är omrenderade.

Faviconen når sidorna genom `build-seo-meta.py`, som redan injicerar ett
block i varje `<head>`. Länkarna byggs före den tidiga returen för
`HIDDEN_PATHS`, så även de dolda guidsidorna får dem.

Fyra vakter, var och en prövad mot sitt eget felfall: geometrin, paletten,
att faviconen når alla 199 sidor, och att varje tillgång bär märkets egna
banor i stället för en egen teckning.

Utanför: sajtens header (ordmärket står kvar som text) och guidernas
omslag, vars regel dokumenteras här och tillämpas i våg 2a.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Steg 5: Visa Johan innan merge**

Samma ordning som i våg 1: han ser bilderna innan något publiceras. Faviconen syns på varje sida på sajten.

---

## Vad som inte ingår

- **Sajtens header.** Ordmärket står kvar som ren text. Johans beslut; frågan kan tas när tecknet setts i bruk.
- **Guidernas omslag.** Regeln skrivs här, tillämpas i våg 2a.
- **Diagram- och social-exporterna** (WISE/RÄTT). Egen runda.
- **Skool-gruppens innehåll och lansering.** Det här är tillgångarna.
