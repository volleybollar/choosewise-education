"""Designkontraktet för Blueprint-paletten, kodat som test.

Varje påstående här kommer från docs/superpowers/specs/
2026-10-05-choosewise-visual-identity-design.md §4 och §5.
Ändras ett värde i specen ska det ändras här i samma commit.
"""
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brandguard import ROOT, published_files  # noqa: E402

TOKENS = ROOT / "assets/css/tokens.css"


def parse_tokens(path: Path = TOKENS) -> dict[str, str]:
    """Plocka ut varje --namn: värde; ur :root-blocket."""
    text = path.read_text(encoding="utf-8")
    root_text = text.split("@media", 1)[0]
    return {
        m.group(1): m.group(2).strip()
        for m in re.finditer(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", root_text)
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
    "--color-highlight-on-dark": "#E8C9A8",
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


EXPECTED_WEIGHTS = {
    "--weight-display": "300",
    "--weight-heading": "400",
    "--weight-body": "400",
    "--weight-emphasis": "500",
}


@pytest.mark.parametrize("name,value", EXPECTED_WEIGHTS.items())
def test_weight_token_has_spec_value(name, value):
    tokens = parse_tokens()
    assert name in tokens, f"{name} saknas i tokens.css"
    assert tokens[name] == value


def test_display_weight_is_never_bold():
    """Spec §5: den lätta display-vikten bär hela riktningen."""
    tokens = parse_tokens()
    assert int(tokens["--weight-display"]) <= 300


# Granskningsfokus (fix-rond, uppgift 6): den ursprungliga versionen av
# den här vakten letade efter de bokstavliga strängarna "var(--weight-
# display)" och "var(--weight-heading)" NÅGONSTANS i base.css/pages.css —
# den kan inte se om en rubrik faktiskt använder dem, och den öppnade
# aldrig components.css, som bar 25 deklarationer på vikt 600 eller 700,
# inklusive .nav__brand (sajtens ordmärke, display-typsnitt, på varje
# sida). Fjärde testet i det här projektet som inte kan fela på det det
# påstår sig vakta. Ersatt: läs varje font-weight-deklaration i all
# publicerad CSS och fäll den om värdet inte är 300, 400 eller 500 —
# skalan specen faktiskt definierar (§5). Siffervärden som 300/400/500
# räknas, liksom var(--weight-*) (som redan är låsta till skalan av
# test_weight_token_has_spec_value ovan); allt annat numeriskt — 600, 700,
# osv — fälls. @font-face-radens "font-weight: 300 600;" (variabel-
# typsnittets kapacitetsintervall, inte en tillämpad vikt) matchar inte
# mönstret, eftersom intervallformen aldrig följs direkt av ";" eller "}".
FONT_WEIGHT_DECLARATION = re.compile(r"font-weight:\s*(\d{3})\s*[;}]")
ALLOWED_WEIGHTS = {"300", "400", "500"}


def published_stylesheets():
    return sorted(p for p in published_files((".css",)) if p != TOKENS)


@pytest.mark.parametrize(
    "path", published_stylesheets(), ids=lambda p: str(p.relative_to(ROOT))
)
def test_font_weight_values_stay_on_the_scale(path):
    """Spec §5: display/heading/body/emphasis är 300/400/500 — aldrig fetare.
    Läser den faktiska deklarationen i stället för att leta efter en
    tokensträng någonstans i filen (se not ovan)."""
    text = path.read_text(encoding="utf-8")
    offenders = [
        (i + 1, m.group(1))
        for i, line in enumerate(text.splitlines())
        for m in FONT_WEIGHT_DECLARATION.finditer(line)
        if m.group(1) not in ALLOWED_WEIGHTS
    ]
    assert offenders == [], (
        f"{path.relative_to(ROOT)} har font-weight utanför skalan "
        f"(300/400/500) på rad:värde {offenders}"
    )


# (förgrund, bakgrund, minsta kontrast, vad det är)
TEXT_PAIRS = [
    ("--color-text", "--color-bg", 4.5, "bläck på papper"),
    ("--color-text-soft", "--color-bg", 4.5, "brödtext på papper"),
    ("--color-text-muted", "--color-bg", 4.5, "metadata på papper"),
    ("--color-accent", "--color-bg", 4.5, "länk och rubrik på papper"),
    ("--color-highlight-ink", "--color-bg", 4.5, "kopparetikett på papper"),
    ("--color-highlight-on-dark", "--color-dark-bg", 4.5, "koppartext på mörkt band"),
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


def test_shadow_focus_is_opaque_and_token_based():
    """Task 10, fix round 2: --shadow-focus used to be
    rgba(11,58,111,0.28) — 28% alpha composites to roughly the colour of
    whatever it sits on, so the ring was invisible on every surface, not
    only dark ones. test_focus_ring_is_visible_against_dark_band (above)
    only compares --color-focus-on-dark to --color-dark-bg as raw
    values; it cannot see that the ring itself was translucent, and
    test_css_discipline.py's focus-rule guard can't either —
    shared_stylesheets() explicitly excludes tokens.css, where
    --shadow-focus is defined. This is the one test that actually reads
    it. Proven to fail red against the old rgba(...,0.28) value, green
    against the fix."""
    tokens = parse_tokens()
    shadow = tokens["--shadow-focus"]
    assert "rgba(" not in shadow, (
        f"--shadow-focus är transparent igen ({shadow}) — en halvgenomskinlig "
        "ring komposit:ar till nästan samma färg som ytan den ligger på "
        "och blir osynlig, oavsett vilken yta"
    )
    assert "var(--color-focus)" in shadow, (
        f"--shadow-focus bygger inte längre på tokenen --color-focus: {shadow}"
    )
