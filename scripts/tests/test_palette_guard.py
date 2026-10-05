"""Crestioras palett och typsnitt får aldrig finnas i publicerade filer.

Crestiora Books är en anonym utgivare. choosewise.education är Johans
namngivna sajt. Delar de visuellt uttryck går varumärkena att koppla ihop.
Spec §3.

Uppgift 8 lägger till sajtens helhetsvakt: gammal palett (LEGACY_FORBIDDEN)
och förbjudna typsnittsfamiljer (FORBIDDEN_FONT_FAMILIES).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brandguard import ROOT, published_files  # noqa: E402

CRESTIORA_FORBIDDEN = [
    "1B2733",          # navy
    "C8A86B",          # mässing
    "F6F3EE",          # grädde
    "2E4057",          # slate
    "Playfair Display",
    # Decimal spellings av samma fyra hex-värden. scan() matchar bokstavligt
    # (ingen regex), så dessa täcker bara den exakta mellanslags-formatteringen
    # "rgba(R, G, B" som filerna faktiskt använder — inte varje whitespace-
    # variant. Medvetet val: scan() delas med Task 8:s LEGACY_FORBIDDEN, och
    # att göra den regex-baserad för whitespace-okänslighet hör inte till
    # den här uppgiften.
    "rgba(26, 39, 51",   # navy, decimal
    "rgb(26, 39, 51",
    "rgba(200, 168, 107",  # mässing, decimal
    "rgb(200, 168, 107",
    "rgba(246, 243, 238",  # grädde, decimal
    "rgb(246, 243, 238",
    "rgba(46, 64, 87",   # slate, decimal
    "rgb(46, 64, 87",
]


def scan(forbidden):
    """Returnera {relativ sökväg: [träffade värden]} för publicerade filer."""
    hits = {}
    for path in published_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        found = [f for f in forbidden if f.lower() in text.lower()]
        if found:
            hits[str(path.relative_to(ROOT))] = found
    return hits


def test_no_crestiora_values_in_published_files():
    hits = scan(CRESTIORA_FORBIDDEN)
    assert hits == {}, (
        "Crestioras varumärke läcker in på Johans namngivna sajt:\n"
        + "\n".join(f"  {k}: {v}" for k, v in sorted(hits.items()))
    )


# ───────────────────────────────────────────────────────────────────────
# Uppgift 8: hela sajtens vakt mot den gamla paletten.
# ───────────────────────────────────────────────────────────────────────

LEGACY_FORBIDDEN = [
    "2d5a3f",   # skogsgrön
    "c66b3d",   # terrakotta
    "faf7f2",   # gammal grädde
    "f2ede2",   # gammal tan
    # "Fraunces" och "Work Sans" hör INTE hemma här som bara substrängar:
    # scan() matchar var som helst i filen, och båda namnen förekommer
    # legitimt som exempel-typsnitt i brödtext (presentation-skills/module-2,
    # en lektion om typografival — "Garamond, Fraunces, Times" osv). Det är
    # inte ett varumärkesläckage, det är innehåll, och innehåll ändras
    # aldrig. De två namnen vaktas istället kontextmedvetet nedan
    # (FORBIDDEN_FONT_FAMILIES), tillsammans med Inter och Playfair
    # Display, som en riktig font-family-deklaration — inte en bar
    # delsträng.
]


def test_no_legacy_palette_in_published_files():
    hits = scan(LEGACY_FORBIDDEN)
    assert hits == {}, (
        "Gammal palett kvar:\n"
        + "\n".join(f"  {k}: {v}" for k, v in sorted(hits.items()))
    )


def test_page_local_css_uses_tokens_not_hex():
    """Granskningsfokus 5: sidlokal CSS gick runt tokens förut."""
    page_local = [
        ROOT / "guides/claude/styles.css",
        ROOT / "sv/guider/claude/styles.css",
        ROOT / "visual-codes/visual-codes.css",
    ]
    offenders = {}
    for path in page_local:
        found = re.findall(r"#[0-9a-fA-F]{3,8}\b", path.read_text(encoding="utf-8"))
        if found:
            offenders[path.name] = sorted(set(found))
    assert offenders == {}, f"Sidlokal CSS hårdkodar färg: {offenders}"


NON_TOKEN_HEX_FORBIDDEN = [
    # Hittad av uppgift 8:s sveep, inte en retirerad varumärkesfärg (hör
    # därför inte hemma i LEGACY_FORBIDDEN) — en grön "BEST"-badge som
    # aldrig blev en token. Som text på ett vitt kort mäter #5C8A6D
    # 3,95:1, under WCAG AA-golvet 4,5:1: en tillgänglighetsbugg utöver
    # paletten. guides/claude/index.html och sv/guider/claude/index.html.
    "5C8A6D",
]


def test_no_known_non_token_hex_in_published_files():
    hits = scan(NON_TOKEN_HEX_FORBIDDEN)
    assert hits == {}, (
        "Icke-token hex kvar (upptäckt under uppgift 8:s sveep):\n"
        + "\n".join(f"  {k}: {v}" for k, v in sorted(hits.items()))
    )


def test_generated_pages_carry_no_palette():
    """De ~150 genererade sidorna ska ärva allt från delad CSS."""
    samples = [
        ROOT / "prompts/teachers/index.html",
        ROOT / "sv/promptar/larare/index.html",
    ]
    for path in samples:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        assert not re.search(r"#[0-9a-fA-F]{6}\b", text), f"{path.name} bär färgvärden"


# ───────────────────────────────────────────────────────────────────────
# Font-familjer: brevet nämner inte detta, men uppgiften kräver det.
#
# Fraunces och Work Sans är den gamla identiteten. Inter och Playfair
# Display hör till Crestiora — en anonym syskonbrand den här sajten
# aldrig får gå att visuellt koppla ihop med (spec §3).
#
# Matchar på font-family-kontext, inte bar delsträng: en naiv
# delsträngskontroll ger falska träffar på ord som "Interrogate" i
# Evidence Toolkit-sidornas text (bekräftat: 180 träffar för ordstammen
# "interrogat*" i spårade filer). Mönstret kräver att namnet står som ett
# eget ord direkt efter "font-family:" eller "font-family=" (SVG).
# ───────────────────────────────────────────────────────────────────────

FORBIDDEN_FONT_FAMILIES = ["Fraunces", "Work Sans", "Inter", "Playfair Display"]

FONT_FAMILY_PATTERN = re.compile(
    r'font-family\s*[:=]\s*["\']?[^;"\'>]*\b('
    + "|".join(re.escape(name) for name in FORBIDDEN_FONT_FAMILIES)
    + r")\b",
    re.IGNORECASE,
)


def scan_font_families():
    """Returnera {relativ sökväg: [träffade typsnittsnamn]} för publicerade
    filer där ett förbjudet namn förekommer i en riktig font-family-
    deklaration."""
    hits = {}
    for path in published_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        found = sorted(set(FONT_FAMILY_PATTERN.findall(text)))
        if found:
            hits[str(path.relative_to(ROOT))] = found
    return hits


def test_no_forbidden_font_families_declared():
    hits = scan_font_families()
    assert hits == {}, (
        "Förbjudet typsnitt i en font-family-deklaration:\n"
        + "\n".join(f"  {k}: {v}" for k, v in sorted(hits.items()))
    )


def test_font_family_pattern_ignores_prose():
    """Mönstret ska inte triggas av ord som råkar innehålla ett förbjudet
    namn som delsträng ("Interrogate" innehåller "Inter", "International"
    likaså) — bara en verklig font-family-deklaration räknas."""
    assert not FONT_FAMILY_PATTERN.search(
        "Evidence you can interrogate in your own chatbot."
    )
    assert not FONT_FAMILY_PATTERN.search(
        "An internationally recognised typeface."
    )
    assert FONT_FAMILY_PATTERN.search('font-family: "Fraunces", Georgia, serif;')
    assert FONT_FAMILY_PATTERN.search("font-family='Work Sans', sans-serif")
    assert FONT_FAMILY_PATTERN.search('font-family="Hanken Grotesk, Inter, sans-serif"')
    assert FONT_FAMILY_PATTERN.search("font-family:Playfair Display,serif")
