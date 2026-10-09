"""Märket har en enda källa, och den källan har bindande mått.

Geometrin valdes efter mätning vid 16 och 32 pixlar. Ändras ett mått på
känsla faller läsbarheten i just de storlekar märket används mest, och
det syns inte i stort format. Därför är måtten testade och inte bara
beskrivna.
"""
from __future__ import annotations

import importlib.util
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


def test_favicon_ico_keeps_the_rounded_transparent_corner():
    """favicon.svg/.ico live inside browser tab chrome, so their 22 % rounded
    corners are genuinely transparent by design — that chrome shows through.
    The true corner pixel sits outside the rounded radius and is
    transparent, so the probe sits mid-edge instead, which is on the
    brand-blue fill. (apple-touch-icon.png is the opposite case — see
    test_apple_touch_icon_has_opaque_square_corners below.)
    """
    with Image.open(FAVICON_ICO) as im:
        im.size = (32, 32)
        im.load()
        frame = im.convert("RGBA")
    r, g, b, a = frame.getpixel((2, frame.height // 2))
    assert a == 255, "bottnen vid kanten är genomskinlig"
    assert (r, g, b) == (0x0B, 0x3A, 0x6F), f"fel bottenfärg: {(r, g, b)}"
    corner_a = frame.getpixel((0, 0))[3]
    assert corner_a == 0, "hörnet förväntas vara genomskinligt (rundad ruta)"
    assert "#0B3A6F" in FAVICON_SVG.read_text(encoding="utf-8")


def test_apple_touch_icon_has_opaque_square_corners():
    """iOS applies its own squircle mask and composites transparency over
    BLACK, so a rounded, transparent-cornered touch icon gets dark corners
    on the home screen. apple-touch-icon.png is therefore a square, fully
    opaque tile (radius 0) — unlike favicon.svg/.ico above, its true
    corners must carry the brand ground, not transparency.
    """
    im = Image.open(APPLE_TOUCH).convert("RGBA")
    for x, y in ((0, 0), (im.width - 1, im.height - 1)):
        r, g, b, a = im.getpixel((x, y))
        assert a == 255, f"hörnet ({x},{y}) är genomskinligt"
        assert (r, g, b) == (0x0B, 0x3A, 0x6F), f"fel bottenfärg i hörnet: {(r, g, b)}"


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
OG_DEFAULT = ROOT / "assets/images/brand/og-default.svg"

# The twelve section cards plus og-default.svg — the file the site-wide
# og:image tag actually points at. It is not one of the twelve (see
# test_there_are_twelve_og_cards below, which must keep counting exactly
# that) but it gets the mark too, so it needs the same two guards.
ALL_OG_CARDS = OG_SVGS + [OG_DEFAULT]


def test_there_are_twelve_og_cards():
    assert len(OG_SVGS) == 12, [p.name for p in OG_SVGS]


@pytest.mark.parametrize("svg", ALL_OG_CARDS, ids=lambda p: p.name)
def test_no_og_card_carries_the_mark(svg):
    """Johans beslut 2026-10-09: symbolen hör primärt till Skool-communityt.
    og-korten är de stora bilderna folk ser när sajten delas — det är där
    märket hade blivit "överallt". Korten bär ordmärket och inget mer.

    Parametriseringen kan inte gå tom: test_there_are_twelve_og_cards
    räknar källan."""
    text = svg.read_text(encoding="utf-8")
    for d in (NEEDLE_NORTH, NEEDLE_SOUTH):
        assert f'd="{d}"' not in text, f"{svg.name} bär märket"


# scripts/build-og-images.py has a hyphen in its name too, so it's loaded
# from its file path the same way it loads build-brand-assets.py itself.
_spec = importlib.util.spec_from_file_location(
    "build_og_images", ROOT / "scripts/build-og-images.py")
_build_og_images = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_build_og_images)


def test_the_og_generator_does_not_stamp_the_mark():
    """Generatorn äger korten (fälla 7) — en handredigering där raderas
    tyst vid nästa körning. Det är alltså HÄR ett återinförande måste
    fångas, innan någon kör skriptet och skriver över de committade
    korten."""
    source = (ROOT / "scripts/build-og-images.py").read_text(encoding="utf-8")
    for d in (NEEDLE_NORTH, NEEDLE_SOUTH):
        assert f'd="{d}"' not in source, \
            "build-og-images.py stämplar märket på delningskorten igen"
    assert "mark_markup" not in source, \
        "build-og-images.py importerar märkets banor ur build-brand-assets.py igen"


# LinkedIns egen spec, hämtad 2026-10-09 från hjälpsidan "Image
# specifications for your LinkedIn Pages and Career Pages": loggan
# rekommenderas 400×400 (minst 268×268), omslaget 1512×256. De tidigare
# måtten 300×300 och 1128×191 var en äldre spec — 300 ligger över
# minimum men under rekommendationen och blir mjuk på retinaskärmar.
# 1512/256 är exakt samma proportion som 1128/191, så bannern är skalad
# rakt av och inte omdesignad.
EXPECTED_SIZES = {
    "skool/logo.png": (1024, 1024),
    "skool/cover.png": (1400, 790),
    "linkedin/page-logo.png": (400, 400),
    "linkedin/page-banner.png": (1512, 256),
    "linkedin/personal-banner.png": (1584, 396),
}


@pytest.mark.parametrize("rel,size", EXPECTED_SIZES.items())
def test_asset_exists_with_exact_size(rel, size):
    path = ROOT / "assets/images/brand" / rel
    assert path.exists(), f"{rel} saknas"
    assert Image.open(path).size == size


@pytest.mark.parametrize("rel", ["skool/cover.svg", "linkedin/personal-banner.svg"])
def test_generated_card_carries_the_marks_own_paths(rel):
    text = (ROOT / "assets/images/brand" / rel).read_text(encoding="utf-8")
    for d in (NEEDLE_NORTH, NEEDLE_SOUTH):
        assert f'd="{d}"' in text, f"{rel} har en egen teckning av nålen"


# --- Guard A: the two SVG-less tiles --------------------------------------
#
# skool/logo.png and linkedin/page-logo.png come straight out of
# tile_svg() with no companion .svg on disk, so only their pixel
# dimensions were guarded (test_asset_exists_with_exact_size above). A
# regression that stripped the mark but kept the canvas size would ship a
# blank blue square as the Skool logo with every other guard green.
#
# tile_svg() centres the mark at _MARK_INNER_FRACTION of the tile (inner =
# size * _MARK_INNER_FRACTION) and maps the mark's own 0..64 viewBox onto
# that inner square. Imported from the generator itself, the same way
# TEMPLATE is imported from build-og-images.py above — a copy of the
# fraction here would go stale the moment tile_svg() changes it.
#
# The north needle (M32 6 L37.5 32 L26.5 32 Z) narrows to a point at y=6 and
# widens towards y=32; the box below is inset from all three of its
# edges across that y-range in the 64-grid, so mapping it through the
# same scale/offset keeps it inside the needle at any tile size the
# generator produces — it is derived from the geometry, not fitted to
# today's output.
_spec_bba = importlib.util.spec_from_file_location(
    "build_brand_assets", ROOT / "scripts/build-brand-assets.py")
_build_brand_assets = importlib.util.module_from_spec(_spec_bba)
_spec_bba.loader.exec_module(_build_brand_assets)

_MARK_INNER_FRACTION = _build_brand_assets._MARK_INNER_FRACTION
_NORTH_NEEDLE_SAFE_BOX = (30.5, 14, 33.5, 30)  # x0, y0, x1, y1 in the 64-grid


def _mark_sample_box(tile_size: int) -> tuple[int, int, int, int]:
    inner = tile_size * _MARK_INNER_FRACTION
    off = (tile_size - inner) / 2
    scale = inner / 64
    x0, y0, x1, y1 = _NORTH_NEEDLE_SAFE_BOX
    return (
        round(off + x0 * scale), round(off + y0 * scale),
        round(off + x1 * scale), round(off + y1 * scale),
    )


@pytest.mark.parametrize("rel", ["skool/logo.png", "linkedin/page-logo.png"])
def test_svg_less_tiles_carry_the_marks_copper(rel):
    """No .svg to text-match against, so this opens the PNG itself and
    looks for the mark's copper in the region the north needle actually
    occupies — the same technique test_the_png_was_rendered_after_the_svg
    uses for the og cards."""
    path = ROOT / "assets/images/brand" / rel
    im = Image.open(path).convert("RGB")
    box = _mark_sample_box(im.size[0])
    colours = im.crop(box).getcolors(im.size[0] * im.size[1]) or []
    assert any(c == (0xE8, 0xC9, 0xA8) for _, c in colours), (
        f"{rel}: no copper in the north-needle region {box} — mark missing?")


# --- Guard B: the font path ------------------------------------------------
#
# The three generated card SVGs declare an @font-face whose src url
# points at the self-hosted Hanken Grotesk file. A mistyped or stale
# path renders the card in a system fallback without failing loudly.
# This catches a wrong or stale path; it does not catch a font that
# exists but fails to load in time at render — that needs a browser,
# and a browser-driven document.fonts.check test would trade this
# sub-second static suite for one with the flakiness that brings.
_FONT_URL = re.compile(r'url\("?([^")]+?)"?\)')


@pytest.mark.parametrize("rel", ["skool/cover.svg", "linkedin/page-banner.svg",
                                 "linkedin/personal-banner.svg"])
def test_generated_card_font_path_exists(rel):
    text = (ROOT / "assets/images/brand" / rel).read_text(encoding="utf-8")
    match = _FONT_URL.search(text)
    assert match, f"{rel}: no @font-face src url found"
    font_path = ROOT / match.group(1).lstrip("/")
    assert font_path.exists(), f"{rel}: font path {match.group(1)} does not exist"


SUBTITLE = "AI &amp; Digitalization for Educators"
OLD_SUBTITLE = "AI &amp; EdTech for Educators"


@pytest.mark.parametrize("rel", ["skool/cover.svg", "linkedin/page-banner.svg",
                                 "linkedin/personal-banner.svg"])
def test_the_subtitle_is_the_decided_one(rel):
    """Johans beslut 2026-10-09. `digitalization` följer sajtens egen
    -ize-konvention (382 förekomster mot 18 för -isation), och versalt D
    matchar `Educators` på samma rad — gement bröt rytmen vid 42 px."""
    text = (ROOT / "assets/images/brand" / rel).read_text(encoding="utf-8")
    assert SUBTITLE in text, f"{rel} saknar den beslutade underrubriken"
    assert OLD_SUBTITLE not in text, f"{rel} bär kvar den gamla underrubriken"


def test_the_generator_owns_the_subtitle():
    """Fälla 7: en handredigering i en genererad SVG raderas tyst vid
    nästa körning. Strängen måste stå i generatorn, inte bara i filerna."""
    source = (ROOT / "scripts/build-brand-assets.py").read_text(encoding="utf-8")
    assert SUBTITLE in source
    assert OLD_SUBTITLE not in source


LINKEDIN_BANNER = "linkedin/page-banner.svg"
BANNER_W = 1512


def test_the_linkedin_page_banner_carries_no_mark():
    """Johans beslut 2026-10-09, alternativ B.

    Företagssidans logga lägger sig över omslagets nedre vänstra hörn —
    specen påstod motsatsen och hade fel. Märket på omslaget hamnade
    alltså dels i skymundan, dels dubbelt, eftersom avataren är samma
    märke. Omslaget bär nu ordmärket ensamt.
    """
    text = (ROOT / "assets/images/brand" / LINKEDIN_BANNER).read_text(encoding="utf-8")
    for d in (NEEDLE_NORTH, NEEDLE_SOUTH):
        assert f'd="{d}"' not in text, "märket är tillbaka på LinkedIn-omslaget"


def test_the_linkedin_page_banner_text_is_centred():
    """Mobilen beskär omslaget mot mitten, så lockupen måste ligga där.

    Centreringen görs med text-anchor och inte med ett handräknat x —
    annars hamnar den fel så fort ordmärket eller underrubriken ändras.
    """
    text = (ROOT / "assets/images/brand" / LINKEDIN_BANNER).read_text(encoding="utf-8")
    assert text.count('text-anchor="middle"') == 2, "båda raderna ska vara centrerade"
    assert f'x="{BANNER_W // 2}"' in text, "texten ska sitta i omslagets mitt"
