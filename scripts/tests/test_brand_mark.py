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
        text = p.read_text(encoding="utf-8")
        # Strip XML comments before normalising colours
        text = re.sub(r'  <!--.*?-->\n', '', text, flags=re.DOTALL)
        return re.sub(r'(fill|stroke)="#[0-9a-fA-F]{6}"', r'\1="X"', text)
    assert skeleton(DARK) == skeleton(LIGHT)
