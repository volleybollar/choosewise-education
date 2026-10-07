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
