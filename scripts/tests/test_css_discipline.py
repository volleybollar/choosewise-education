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


# NOTE: --color-focus-on-dark existed in tokens.css, with its own
# passing contrast test, for an entire wave before anyone noticed it was
# never consumed — a token that only exists in the tin, not on the wall.
# test_tokens.py's checks are all pure token-value arithmetic; none of
# them can see whether a token is wired into a real declaration. This
# guard reads actual rule bodies instead: for every selector that
# mentions :focus or :focus-visible in the shared stylesheets, grab its
# declaration block up to the next "}" (good enough — none of this
# codebase's focus rules are themselves nested inside another block) and
# assert both focus tokens appear in at least one of them, literally.
FOCUS_SELECTOR = re.compile(r":focus(?:-visible)?[^{]*\{")


def _focus_rule_bodies(text: str) -> str:
    bodies = []
    for m in FOCUS_SELECTOR.finditer(text):
        end = text.find("}", m.end())
        if end != -1:
            bodies.append(text[m.end() : end])
    return " ".join(bodies)


def test_focus_tokens_are_consumed_by_a_real_focus_rule():
    """Granskningsfokus 1 (task 10, fix round 1): en osynlig fokusring
    kom igenom trots grön testsvit eftersom ingenting mätte om
    --color-focus-on-dark faktiskt användes någonstans. Båda
    fokustokens måste nu förekomma, bokstavligen, i minst en
    :focus/:focus-visible-regel i de delade stilmallarna."""
    text = "\n".join(p.read_text(encoding="utf-8") for p in shared_stylesheets())
    bodies = _focus_rule_bodies(text)
    assert "var(--color-focus-on-dark)" in bodies, (
        "ingen :focus-regel i de delade css-filerna använder "
        "--color-focus-on-dark — tokenen riskerar att bli obrukad igen"
    )
    assert "var(--color-focus)" in bodies, (
        "ingen :focus-regel i de delade css-filerna använder --color-focus"
    )
