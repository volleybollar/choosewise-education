"""Färg bor i tokens.css. Ingen annanstans i assets/css/."""
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brandguard import ROOT, published_files  # noqa: E402

CSS_DIR = ROOT / "assets/css"

HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")


def shared_stylesheets():
    return sorted(p for p in CSS_DIR.glob("*.css") if p.name != "tokens.css")


# Uppgift 4: de två vakterna nedan (ytkoppar-som-text och fokustoken) körde
# bara mot assets/css/*.css. Det gapet gömde Blockerare 3 (visual-codes.css)
# och bidrog till Blockerare 2 (guides/claude/styles.css) — sidlokal CSS
# som aldrig korsade en vakt. Samma breddning som hex-vakten i
# test_palette_guard.py redan fått: all publicerad CSS, utom tokens.css
# självt (som äger de faktiska hex-värdena bakom varje token).
def published_stylesheets():
    tokens_css = ROOT / "assets/css/tokens.css"
    return sorted(p for p in published_files((".css",)) if p != tokens_css)


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
# across pages.css/components.css, 5 of which were `border-color:` only.
#
# Uppgift 4 (breddning till all publicerad CSS) hittade samma problem i en
# annan form: `(?<!border-)(?<!background-)` bara utesluter de exakta
# 7/11-teckensprefixen "border-" och "background-" omedelbart före "color:".
# guides/claude/styles.css (sidlokal, aldrig skannad förut) har både
# `text-decoration-color: var(--color-highlight);` (en understrykningslinje
# — grafik, inte text) och `border-bottom-color: var(--color-highlight);`
# (en kantlinje) — ingen av dem matchar de gamla lookbehindsen eftersom
# prefixen är "-decoration-" respektive "-bottom-", inte "border-"/
# "background-". Båda är legitima (texten själv står i --color-text /
# --color-highlight-ink på samma rader). Lösningen är generell i stället för
# fler specialfall: "color:" räknas bara som en riktig textfärg-deklaration
# om den INTE är en sammansatt *-color-egenskap, dvs den får inte föregås av
# ett bindestreck. Bekräftat: ger samma träffar som förut på de äkta
# fallen (visual-codes.css) och noll nya falska positiva.
HIGHLIGHT_AS_TEXT = re.compile(r"(?<!-)color:\s*var\(--color-highlight\)\s*[;}]")


@pytest.mark.parametrize(
    "path", published_stylesheets(), ids=lambda p: str(p.relative_to(ROOT))
)
def test_surface_copper_is_never_used_as_text(path):
    """Spec §4 regel 2: --color-highlight är en yta, aldrig text.
    Som textfärg faller den på varje yta sajten har (3,1-4,3:1)."""
    text = path.read_text(encoding="utf-8")
    hits = [
        i + 1
        for i, line in enumerate(text.splitlines())
        if HIGHLIGHT_AS_TEXT.search(line)
    ]
    assert hits == [], f"{path.relative_to(ROOT)} använder ytkoppar som textfärg på rad {hits}"


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
    :focus/:focus-visible-regel — numera i ALL publicerad CSS (uppgift 4),
    inte bara assets/css/*.css. Blockerare 2 (den osynliga fokusringen på
    .cta-band i guides/claude/styles.css) existerade just för att den
    filen aldrig korsade den här vakten."""
    text = "\n".join(p.read_text(encoding="utf-8") for p in published_stylesheets())
    bodies = _focus_rule_bodies(text)
    assert "var(--color-focus-on-dark)" in bodies, (
        "ingen :focus-regel i publicerad css använder "
        "--color-focus-on-dark — tokenen riskerar att bli obrukad igen"
    )
    assert "var(--color-focus)" in bodies, (
        "ingen :focus-regel i publicerad css använder --color-focus"
    )
