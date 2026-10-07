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
from PIL import Image

from . import brandguard

ROOT = Path(__file__).resolve().parents[2]
DARK = ROOT / "assets/images/brand/mark-on-dark.svg"
LIGHT = ROOT / "assets/images/brand/mark-on-light.svg"

FAVICON_SVG = ROOT / "favicon.svg"
FAVICON_ICO = ROOT / "favicon.ico"
APPLE_TOUCH = ROOT / "apple-touch-icon.png"

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
def test_ring_stroke_colour(path: Path):
    """Ringens stroke måste matcha sitt färgläge."""
    text = path.read_text(encoding="utf-8")
    ring = re.search(r'<circle[^>]*r="21"[^>]*>', text)
    assert ring, "ringen med radie 21 saknas"
    assert f'stroke="{STATES[path]["ring"]}"' in ring.group(0)


@pytest.mark.parametrize("path", list(STATES), ids=lambda p: p.name)
def test_north_needle_fill_colour(path: Path):
    """Nålens norra del måste ha rätt färg för sitt läge."""
    text = path.read_text(encoding="utf-8")
    north = re.search(rf'<path[^>]*d="{NEEDLE_NORTH}"[^>]*>', text)
    assert north, f"nålen norr {NEEDLE_NORTH} saknas"
    assert f'fill="{STATES[path]["north"]}"' in north.group(0)


@pytest.mark.parametrize("path", list(STATES), ids=lambda p: p.name)
def test_south_needle_fill_colour(path: Path):
    """Nålens södra del måste ha rätt färg för sitt läge."""
    text = path.read_text(encoding="utf-8")
    south = re.search(rf'<path[^>]*d="{NEEDLE_SOUTH}"[^>]*>', text)
    assert south, f"nålen söder {NEEDLE_SOUTH} saknas"
    assert f'fill="{STATES[path]["south"]}"' in south.group(0)


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
        text = p.read_text(encoding="utf-8")
        # Strip XML comments before normalising colours
        text = re.sub(r'  <!--.*?-->\n', '', text, flags=re.DOTALL)
        return re.sub(r'(fill|stroke)="#[0-9a-fA-F]{6}"', r'\1="X"', text)
    assert skeleton(DARK) == skeleton(LIGHT)


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


FAVICON_LINKS = (
    '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
    '<link rel="icon" href="/favicon.ico" sizes="32x32">',
    '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
)

PAGES = [p for p in brandguard.published_files((".html",))
         if "<head" in p.read_text(encoding="utf-8", errors="replace")
         and "scripts" not in p.relative_to(ROOT).parts]


def test_the_page_count_is_what_we_think():
    """198 av 203. scripts/ är verktygsfixturer, inte sidor — en ny fil
    där ska inte kunna ändra talet tyst. Faller globbet ihop vaktar
    resten ingenting."""
    assert len(PAGES) == 198, len(PAGES)


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
