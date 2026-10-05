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
