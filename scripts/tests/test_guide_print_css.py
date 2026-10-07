# scripts/tests/test_guide_print_css.py
"""Guidernas delade stilmall ska bära Blueprint och inget annat.

Kopparns tre roller blandades fem gånger i våg 1. Reglerna nedan är
skrivna för att bli röda på just det, inte bara på att värdena finns.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CSS = ROOT / "exports" / "_guide-print.css"

CRESTIORA = ["#1B2733", "#C8A86B", "#F6F3EE"]
OLD_CHOOSEWISE = ["#2d5a3f", "#f7f4ec", "#1e1e1c"]
BLUEPRINT = {
    "--color-bg": "#FBFAF8", "--color-bg-alt": "#EFF2F6",
    "--color-text": "#0C1A2E", "--color-text-soft": "#4E5A68",
    "--color-text-muted": "#656F7B", "--color-border": "#DDE3EA",
    "--color-accent": "#0B3A6F", "--color-deep": "#07284D",
    "--color-highlight": "#C2793A", "--color-highlight-ink": "#9C5A24",
    "--color-highlight-on-dark": "#E8C9A8",
    "--color-dark-bg": "#0B3A6F", "--color-dark-text": "#EFF2F6",
}


def css() -> str:
    return CSS.read_text(encoding="utf-8")


def test_every_blueprint_token_is_defined_with_the_right_value():
    text = css()
    for token, value in BLUEPRINT.items():
        assert re.search(rf"{re.escape(token)}\s*:\s*{value}\s*;", text, re.I), \
            f"{token} saknas eller har fel värde (ska vara {value})"


def test_no_old_palette_values_anywhere():
    text = css()
    for value in CRESTIORA + OLD_CHOOSEWISE:
        assert value.lower() not in text.lower(), f"{value} lever kvar i den delade mallen"


def test_hex_colours_appear_only_in_the_root_block():
    """Varje färg ska komma ur en variabel. Undantaget är :root självt och
    @font-face, som inte har färger alls."""
    text = css()
    root = re.search(r":root\s*\{.*?\}", text, re.S)
    assert root, ":root-blocket saknas"
    outside = text[: root.start()] + text[root.end():]
    stray = re.findall(r"#[0-9a-fA-F]{3,8}\b", outside)
    assert not stray, f"hårdkodade färger utanför :root: {sorted(set(stray))}"


def test_fonts_are_self_hosted():
    text = css()
    assert "fonts.googleapis.com" not in text
    assert "assets/fonts/hanken-grotesk/HankenGrotesk-VariableFont.woff2" in text
    for rel in re.findall(r"url\('([^']+)'\)", text):
        assert (CSS.parent / rel).resolve().exists(), f"typsnittsfilen saknas: {rel}"


def _without_font_face_blocks(text: str) -> str:
    """@font-face describes what the font FILE supports, not how a weight
    is used — a variable font's range (e.g. `300 600`) is correct there
    and must not be read as a usage. Strip those blocks before scanning
    for actual weight usages."""
    return re.sub(r"@font-face\s*\{[^}]*\}", "", text, flags=re.S)


def test_no_font_weight_outside_the_scale():
    """Display 300, rubrik 400, brödtext 400, betoning 500. Inget annat.

    Only usages count (outside @font-face). A usage must resolve to the
    scale: 300, 400, 500, or the keyword `normal` (= 400). `bold`,
    `bolder`, `lighter` and any numeric value outside the scale are
    violations — including a second number in a multi-value declaration.
    """
    text = _without_font_face_blocks(css())
    allowed_numeric = {"300", "400", "500"}
    violations = []
    for declaration in re.findall(r"font-weight:\s*([^;]+);", text):
        for token in declaration.split():
            if token == "normal" or token in allowed_numeric:
                continue
            violations.append(token)
    assert not violations, \
        f"vikter utanför skalan (utanför @font-face): {sorted(set(violations))}"


def test_font_face_variable_range_is_exempt_from_the_scale():
    """The scale guard above must not reach into @font-face — the Hanken
    Grotesk variable range `300 600` describes the file, not a usage,
    and must stay untouched by tasks 4-6."""
    assert re.search(r"font-weight:\s*300\s+600\s*;", css()), \
        "Hanken Grotesk @font-face-intervallet 300 600 saknas eller har ändrats"


def test_copper_is_never_used_as_text_colour():
    """--color-highlight är ytfärg. Kopparfärgad text tar -ink eller -on-dark.

    Regeln bröts fem gånger i våg 1 av arbetare som antog att ett värde
    räckte, så vakten läser varje color-deklaration och inte bara filen.
    """
    bad = [m for m in re.findall(r"(?<!-)color:\s*var\(([^)]+)\)", css())
           if m.strip() == "--color-highlight"]
    assert not bad, "--color-highlight används som textfärg; ta --color-highlight-ink " \
                    "på ljus botten eller --color-highlight-on-dark på mörkt band"


# ── Sub-family scoping guard ──────────────────────────────────────────────
#
# Task 5's review: licensblockets bara `.eyebrow { margin-bottom: 18pt }`
# (ett generiskt, oscopat klassnamn) läckte in i varje quick start-masthead,
# eftersom `.masthead .eyebrow` aldrig satte sin egen margin — CSS kaskadar
# per EGENSKAP, inte per regel, så en helt orelaterad bar-selektor längre
# ner i filen vinner ändå på den enda egenskap den ensam deklarerar. Samma
# fälla väntade i licensblockets återstående tolv bara selektorer (.title,
# .body, .subtitle, .link, .signature, .terms, .divider, …) — och alla tolv
# A4-guider som uppgift 6 ska koppla till den här filen använder redan
# .eyebrow eller .signature.
#
# Lösningen: varje regel i ett underfamilj-block ska bära sin egen
# .page--familj-klass. Markörerna nedan (SCOPE-GUARD:BEGIN/END <familj>)
# avgränsar varje sådant block i CSS-källan. De är fristående från de
# beskrivande rubrikkommentarerna ("── Licenssidan ──" osv) med flit: en
# omskriven rubrik ska inte kunna göra att vakten tyst slutar kontrollera
# ett block. Om en markör saknas eller är felstavad upptäcker
# test_scope_guard_markers_exist_and_cover_the_expected_families det
# (exakt mängdjämförelse, inte "minst noll träffar").

SCOPE_GUARD_RE = re.compile(
    r"/\*\s*SCOPE-GUARD:BEGIN\s+(?P<name>[\w-]+)\s*\*/(?P<body>.*?)"
    r"/\*\s*SCOPE-GUARD:END\s+(?P=name)\s*\*/",
    re.S,
)

# De enda två underfamiljerna i den här filen idag. A4-guiderna (uppgift 6)
# delar bara tokens/typsnitt/.page härifrån, inte en klassvokabulär (se
# kommentaren överst i filen) — de ska alltså INTE få ett eget SCOPE-GUARD-
# block. Om de någon gång gör det, uppdatera den här mängden medvetet;
# vakten ska inte tyst acceptera fler eller färre block än så här.
EXPECTED_SCOPED_FAMILIES = {"page--license", "page--quickstart"}


def _strip_comments(text: str) -> str:
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


def _selectors_in_block(block: str) -> list[str]:
    """Every selector-list text (what precedes each `{`) inside one block,
    comments stripped, split on top-level commas into individual selectors."""
    clean = _strip_comments(block)
    out = []
    for match in re.finditer(r"([^{}]+)\{", clean):
        for part in match.group(1).split(","):
            part = part.strip()
            if part:
                out.append(part)
    return out


def test_scope_guard_markers_exist_and_cover_the_expected_families():
    """Red-proof for the guard below: without this check, deleting or
    renaming a SCOPE-GUARD marker would make
    test_every_selector_in_a_subfamily_block_carries_its_page_scope scan
    zero selectors for that family and pass vacuously — a guard that quietly
    covers nothing. This test fails loudly instead."""
    found = {m.group("name") for m in SCOPE_GUARD_RE.finditer(css())}
    assert found == EXPECTED_SCOPED_FAMILIES, (
        f"SCOPE-GUARD-block hittades för {sorted(found)}, förväntade "
        f"{sorted(EXPECTED_SCOPED_FAMILIES)}. En borttagen, felstavad eller "
        "obalanserad BEGIN/END-markör gör att blocket slutar skyddas."
    )
    begins = len(re.findall(r"/\*\s*SCOPE-GUARD:BEGIN\s+[\w-]+\s*\*/", css()))
    ends = len(re.findall(r"/\*\s*SCOPE-GUARD:END\s+[\w-]+\s*\*/", css()))
    assert begins == ends == len(EXPECTED_SCOPED_FAMILIES), \
        f"obalanserade SCOPE-GUARD-markörer: {begins} BEGIN, {ends} END"


def test_every_selector_in_a_subfamily_block_carries_its_page_scope():
    """Every selector between a family's SCOPE-GUARD markers must include
    that family's own `.page--xxx` class — as an ancestor (`.page--quickstart
    .foo`), or, for a class that sits on the very same element as the scope
    class (`.page1`/`.page2`, alongside `.page--quickstart` on one <div>),
    compounded directly (`.page--quickstart.page1`).

    Red-proof (run by hand, not kept as a test — a real regression would
    defeat its own guard): add `.foo { color: red; }` anywhere inside the
    page--license block and this test fails naming `page--license: '.foo'`;
    remove it and it is green again. This is exactly the shape of the bug
    the reviewer found (.eyebrow without a .page--license prefix)."""
    violations = []
    for match in SCOPE_GUARD_RE.finditer(css()):
        family = match.group("name")
        scope_class = f".{family}"
        for selector in _selectors_in_block(match.group("body")):
            if scope_class not in selector:
                violations.append(f"{family}: {selector!r}")
    assert not violations, (
        "Dessa selektorer saknar sitt eget .page--scope och kan läcka till "
        f"andra underfamiljer: {violations}"
    )
