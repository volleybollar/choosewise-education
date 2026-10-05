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


# NOTE: the originally proposed pattern was `r"color:\s*var\(--color-highlight\)\s*[;}]"`.
# That over-matches: "color:" is a substring of "border-color:" and "background-color:",
# so it also flagged pure `border-color: var(--color-highlight);` declarations, which are
# correct as-is (surfaces/borders are exactly what --color-highlight is for). Confirmed by
# running both patterns side by side against the real files: the naive one hit 17 lines
# across pages.css/components.css, 5 of which were `border-color:` only. The lookbehinds
# below exclude those while still matching every real `color:` (and `color:` immediately
# after another declaration on the same line, e.g. `border-color: ...; color: ...;`).
HIGHLIGHT_AS_TEXT = re.compile(
    r"(?<!border-)(?<!background-)color:\s*var\(--color-highlight\)\s*[;}]"
)


@pytest.mark.parametrize("path", shared_stylesheets(), ids=lambda p: p.name)
def test_surface_copper_is_never_used_as_text(path):
    """Spec §4 regel 2: --color-highlight är en yta, aldrig text.
    Som textfärg faller den på varje yta sajten har (3,1-4,3:1)."""
    text = path.read_text(encoding="utf-8")
    hits = [
        i + 1
        for i, line in enumerate(text.splitlines())
        if HIGHLIGHT_AS_TEXT.search(line)
    ]
    assert hits == [], f"{path.name} använder ytkoppar som textfärg på rad {hits}"
