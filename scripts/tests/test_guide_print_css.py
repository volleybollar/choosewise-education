# scripts/tests/test_guide_print_css.py
"""Guidernas delade stilmall ska bära Blueprint och inget annat.

Kopparns tre roller blandades fem gånger i våg 1. Reglerna nedan är
skrivna för att bli röda på just det, inte bara på att värdena finns.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from . import brandguard

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
# .page--familj-klass. Markörerna nedan (SCOPE-GUARD:BEGIN/END <namn>)
# avgränsar varje sådant block — INKLUSIVE bas-blocket (:root … strong,b),
# som är det enda undantaget från scope-kravet eftersom dess jobb är att
# gälla överallt. De är fristående från de beskrivande rubrikkommentarerna
# ("── Licenssidan ──" osv) med flit: en omskriven rubrik ska inte kunna
# göra att vakten tyst slutar kontrollera ett block.
#
# Re-review hittade två hål i en första version av den här vakten:
#   1. Ett HELT NYTT block utan egna markörer (t.ex. en framtida uppgift 6
#      som lägger till `.page--a4-foo { … }` utan SCOPE-GUARD-kommentarer)
#      kom igenom obemärkt, eftersom vakten bara läste INNANFÖR befintliga
#      markörer — den frågade "är det som står mellan markörerna scopat?"
#      i stället för "finns det något UTANFÖR markörerna?". Fixat genom
#      test_every_selector_lies_inside_a_marked_region, som maskerar bort
#      allt täckt innehåll och kräver att inget en selektor blir kvar.
#   2. Scope-kontrollen var en delsträngskontroll (`scope_class not in
#      selector`), så `.page--license-note` såg ut att "innehålla"
#      `.page--license` trots att det är ett helt annat, längre klassnamn.
#      Fixat med en strukturell regex (gränsbevakad lookahead) i
#      _selector_has_scope.

SCOPE_GUARD_RE = re.compile(
    r"/\*\s*SCOPE-GUARD:BEGIN\s+(?P<name>[\w-]+)\s*\*/(?P<body>.*?)"
    r"/\*\s*SCOPE-GUARD:END\s+(?P=name)\s*\*/",
    re.S,
)

# Varje region i filen idag. "base" är den delade grunden (:root, @font-face,
# @page, *, html, body, .page, strong/b) och är undantagen scope-kravet —
# att gälla överallt ÄR dess jobb. page--license och page--quickstart är de
# enda två underfamiljerna. A4-guiderna (uppgift 6) delar bara tokens/
# typsnitt/.page härifrån, inte en klassvokabulär (se kommentaren överst i
# filen) — de ska alltså INTE få ett eget SCOPE-GUARD-block. Om de någon
# gång gör det, uppdatera den här mängden medvetet; vakten ska inte tyst
# acceptera fler eller färre regioner än så här.
EXPECTED_REGIONS = {"base", "page--license", "page--quickstart"}
SCOPE_EXEMPT_REGIONS = {"base"}


def _strip_comments(text: str) -> str:
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


def _blank(text: str, start: int, end: int) -> str:
    """Replace text[start:end] with spaces (newlines kept) so positions and
    line numbers in the rest of the string stay valid."""
    masked = "".join(ch if ch == "\n" else " " for ch in text[start:end])
    return text[:start] + masked + text[end:]


def _blank_comments(text: str) -> str:
    def repl(m: re.Match) -> str:
        return "".join(ch if ch == "\n" else " " for ch in m.group(0))
    return re.sub(r"/\*.*?\*/", repl, text, flags=re.S)


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


def _selector_has_scope(selector: str, family: str) -> bool:
    """Structural check, not a substring check: `.page--license` must appear
    as its own class token. `.page--license`, `.page--license.page1` and
    `.page--license .title` all match; `.page--license-note` must not —
    the character right after the family name must not continue a word/
    hyphen, or it is a different, longer class name wearing our prefix."""
    pattern = re.compile(rf"\.{re.escape(family)}(?![\w-])")
    return bool(pattern.search(selector))


def test_scope_guard_markers_exist_and_cover_the_expected_regions():
    """Red-proof for the guards below: without this check, deleting or
    renaming a SCOPE-GUARD marker would make the other two guards scan zero
    selectors for that region and pass vacuously — a guard that quietly
    covers nothing. This test fails loudly instead."""
    found = {m.group("name") for m in SCOPE_GUARD_RE.finditer(css())}
    assert found == EXPECTED_REGIONS, (
        f"SCOPE-GUARD-block hittades för {sorted(found)}, förväntade "
        f"{sorted(EXPECTED_REGIONS)}. En borttagen, felstavad eller "
        "obalanserad BEGIN/END-markör gör att regionen slutar skyddas."
    )
    begins = len(re.findall(r"/\*\s*SCOPE-GUARD:BEGIN\s+[\w-]+\s*\*/", css()))
    ends = len(re.findall(r"/\*\s*SCOPE-GUARD:END\s+[\w-]+\s*\*/", css()))
    assert begins == ends == len(EXPECTED_REGIONS), \
        f"obalanserade SCOPE-GUARD-markörer: {begins} BEGIN, {ends} END"


def test_every_selector_lies_inside_a_marked_region():
    """Gap 1 (re-review): a wholly new rule written outside every
    SCOPE-GUARD region — exactly what a future task adding a third
    sub-family without its own markers would do — must fail here, naming
    the selector and the line it's on. Masks out everything that IS inside
    a known region (markers included) and every comment, then asserts
    nothing that looks like a selector remains in what's left.

    Red-proof: append `.page--a4-foo { padding: 10mm; }` anywhere after the
    last SCOPE-GUARD:END marker and this test fails, naming it and its
    line; remove it and it is green again."""
    text = css()
    masked = text
    for match in SCOPE_GUARD_RE.finditer(text):
        masked = _blank(masked, match.start(), match.end())
    masked = _blank_comments(masked)

    violations = []
    for sel_match in re.finditer(r"([^{}]+)\{", masked):
        chunk = sel_match.group(1)
        chunk_start = sel_match.start(1)
        offset = 0
        for part in chunk.split(","):
            local = part.strip()
            if local:
                abs_pos = chunk_start + offset + part.find(local)
                line = text.count("\n", 0, abs_pos) + 1
                violations.append(f"line {line}: {local!r}")
            offset += len(part) + 1  # +1 for the comma separator
    assert not violations, (
        "Selektorer utanför alla SCOPE-GUARD-regioner (ett nytt block utan "
        f"egna markörer smyger förbi scopningen): {violations}"
    )


def test_every_selector_in_a_scoped_region_structurally_carries_its_page_scope():
    """Gap 2 (re-review): the per-selector check must be structural, not a
    substring test — `.page--license-note` is a different, longer class
    name and must not be accepted as "containing" `.page--license`.

    Every selector between a non-exempt region's SCOPE-GUARD markers must
    include that region's own `.page--xxx` class — as an ancestor
    (`.page--quickstart .foo`), or, for a class that sits on the very same
    element as the scope class (`.page1`/`.page2`, alongside
    `.page--quickstart` on one <div>), compounded directly
    (`.page--quickstart.page1`). `base` is exempt — applying everywhere is
    its job.

    Red-proof: add `.page--license-note { color: red; }` anywhere inside
    the page--license block and this test fails naming it; remove it and
    it is green again. (A bare `.foo` with no `.page--` prefix at all is
    also caught — same failure, simpler case.)"""
    violations = []
    for match in SCOPE_GUARD_RE.finditer(css()):
        family = match.group("name")
        if family in SCOPE_EXEMPT_REGIONS:
            continue
        for selector in _selectors_in_block(match.group("body")):
            if not _selector_has_scope(selector, family):
                violations.append(f"{family}: {selector!r}")
    assert not violations, (
        "Dessa selektorer saknar sitt eget .page--scope som ett strukturellt "
        f"klasstoken (inte bara som delsträng): {violations}"
    )


# ── Guidfamiljens egna mallar (uppgift 8) ─────────────────────────────────
#
# Allt ovanför det här stycket vaktar DEN DELADE STILMALLEN
# (exports/_guide-print.css) — en enda fil. Det här stycket vaktar de 26
# HANDSKRIVNA MALLARNA själva: deras inline <style>-block och markup.
# published_files() (brandguard.py) utesluter hela exports/, vilket var
# rätt så länge mallarna låg utanför arbetet — nu ligger de inne, och utan
# den här vakten kan nästa redigering smyga tillbaka Playfair eller en
# Crestiora-färg i en mall utan att ett enda test blir rött.
#
# Det här dubblerar inte de andra vakterna:
#   - test_guide_asset_paths.py kontrollerar bildvägar, inte palett/typsnitt.
#   - test_guide_pdf_font_weights.py läser inbäddade typsnittsNAMN i
#     RENDRADE PDF:er (pdffonts) — det fångar vikter som kommer från HTML
#     utan någon CSS-deklaration alls (se not nedan). Vakterna här läser
#     mallarnas KÄLLTEXT och fångar bara det som faktiskt står i en
#     font-weight- eller font-family-deklaration. De två lagren täcker
#     olika saker med samma avsikt; ingen av dem kan ersätta den andra.
#   - test_guide_pdf_parity.py / test_guide_pdf_body_text.py vaktar
#     INNEHÅLLET (ord, rubriker), inte paletten eller typsnitten.
#
# Vikter-från-HTML-utan-CSS (uppgift 4:s fynd): en ostylad <strong> renderas
# i webbläsarens nativa 700, vilket det rörliga typsnittet klämmer till 600
# — ett viktbrott utan en enda font-weight-deklaration någonstans. Det
# globala `strong, b { font-weight: 500; }` i _guide-print.css täcker det
# scenariot i dag. test_no_font_weight_outside_the_scale_in_templates
# nedan kan alltså inte se den klassen av fel — den läser bara
# font-weight-token i mallarnas KÄLLTEXT. Det är render-nivå-vakten
# (test_guide_pdf_font_weights.py) som äger det fallet; den här vakten äger
# bara det som uttryckligen står skrivet i en mall.

TEMPLATES = list(brandguard.guide_templates())


def test_the_glob_finds_every_template():
    """26 handskrivna mallar. Faller globbet ihop tyst vaktar resten
    ingenting — värdet är verifierat mot det faktiska filsystemet, inte
    bara ihoptänkt (se uppgift 8:s rapport)."""
    assert len(TEMPLATES) == 26, [p.name for p in TEMPLATES]


@pytest.mark.parametrize("path", TEMPLATES, ids=lambda p: p.name)
def test_no_old_palette_in_the_templates(path):
    text = path.read_text(encoding="utf-8")
    for value in CRESTIORA + OLD_CHOOSEWISE:
        assert value.lower() not in text.lower(), f"{path.name} bär {value}"


@pytest.mark.parametrize("path", TEMPLATES, ids=lambda p: p.name)
def test_no_external_font_calls(path):
    assert "fonts.googleapis.com" not in path.read_text(encoding="utf-8")


@pytest.mark.parametrize("path", TEMPLATES, ids=lambda p: p.name)
def test_only_blueprint_typefaces_in_font_family_context(path):
    """Matcha i font-family-kontext. Sajten undervisar om design och nämner
    typsnittsnamn i brödtext (t.ex. presentation-skills/module-2: "Fraunces,
    Times) can feel heavier…") — en vakt utan kontext slår larm på sin egen
    undervisning. Genom att bara läsa inuti font-family:-deklarationer
    träffar vakten verklig CSS-användning, aldrig prosa som nämner ett
    typsnittsnamn i förbigående.

    Värdeklassen stänger vid \"/' lika väl som vid ;/} (uppgift 9:s fynd):
    utan det skulle en framtida inline-stil utan avslutande semikolon
    ("style=\"font-family:var(--font-quote)\"", där attributet avslutas av
    citattecknet, inte ett semikolon) fånga in all text efter sig — ända
    till nästa ; eller } någonstans senare i filen — och ett sammanträffande
    typsnittsnamn i den texten skulle då larma på en fullt godkänd
    deklaration. Det valfria ledande citattecknet konsumeras separat så att
    en citerad deklaration som font-family: 'Playfair Display' ändå fångas."""
    families = re.findall(r"font-family:\s*[\"']?([^;}\"'>]+)", path.read_text(encoding="utf-8"))
    banned = [f for f in families
              if re.search(r"Playfair|Fraunces|Work Sans|\bInter\b", f)]
    assert not banned, f"{path.name}: {banned}"


@pytest.mark.parametrize("path", TEMPLATES, ids=lambda p: p.name)
def test_no_font_weight_outside_the_scale_in_templates(path):
    """Käll-nivå-syskon till test_no_font_weight_outside_the_scale ovan,
    men för mallarnas egna inline-stilar i stället för den delade filen.
    Täcker inte HTML-utan-CSS-fallet (se styckeskommentaren ovan) — det
    äger render-nivå-vakten i test_guide_pdf_font_weights.py."""
    weights = re.findall(r"font-weight:\s*(\d{3})", path.read_text(encoding="utf-8"))
    outside = sorted({w for w in weights if w not in {"300", "400", "500"}})
    assert not outside, f"{path.name}: vikter utanför skalan {outside}"
