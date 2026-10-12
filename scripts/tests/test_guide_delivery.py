"""Leveransen är de engelska PDF:erna, inte HTML:en de renderas ur.

Varje annan vakt i rundan läser HTML. Rättas HTML:en utan att PDF:erna
renderas om går hela sviten grön medan filen som går till Skool
fortfarande bär den svenska inramningen. Den här vakten läser det som
levereras.

Den täcker också quick-starten, som med avsikt står utanför
ytkonsistensvakten (spec §5) och annars inte bevakas av något som läser
dess innehåll.

Förbudslistan är PER GUIDE. Copilot-rundan valde väg A rakt av och kan
därför förbjuda "Sweden", "Swedish" och "GDPR" bart. Gemini-rundan kan
inte: ett källbelagt svenskt praktikexempel stannar (spec §9 tillåter
det uttryckligen), och en promptmall innehåller ordet GDPR som
platshållare läsaren själv fyller i. En delad lista vore en vakt som
styr innehållet i stället för att vakta det.
"""
from __future__ import annotations

import hashlib
import re
import subprocess

import pytest

from . import pdf_fingerprint as fp

GUIDE_DELIVERY = {
    "copilot": {
        "pdfs": (
            "_unpublished/assets/pdfs/guides/copilot-guide-en.pdf",
            "_unpublished/assets/pdfs/guides/copilot-quick-start-en.pdf",
        ),
        # Oförändrad ur test_copilot_delivery.py.
        "forbidden": (
            "Swedish", "Sweden", "Skolverket", "IMY", "Schrems", "GDPR",
            "April 2026", "kr 350",
        ),
        "untouched": (),
    },
    "gemini": {
        "pdfs": (
            "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-en.pdf",
            "_unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-en.pdf",
        ),
        # Inramningen och den artikelnivå-GDPR spec §3 väljer bort, sträng
        # för sträng. Inget bart "Sweden"/"Swedish" och inget bart "GDPR":
        # se modulens docstring. Och inget bart "April 2026" — sju
        # meningar bär datumet som ett DATERAT PRODUKTPÅSTÅENDE ("Since 8
        # April 2026 the two tools sync bidirectionally"), och de står
        # eller faller på sin källa, inte på rundans datumstämpel. De två
        # STÄMPLARNA bevakas i stället var och en på sin plats, av
        # test_geminis_cover_and_closing_carry_the_rounds_date nedan.
        "forbidden": (
            "Skolverket", "IMY", "Schrems",
            "Swedish schools",
            "Swedish and other EU languages",
            "Sweden, as of April 2026",
            "Sweden is a notable example",
            "GDPR fundamentals",
            "Standard GDPR discipline",
            "carrying GDPR risk",
            "the GDPR and the EU AI Act",
            "Article 6(1)(e)",
            "Article 30",
            "national data protection authority",
            "Every EU member state has one",
            "phases in through 2026 and beyond",
            "Limited risk",
            "I have a full-time job",
        ),
        # Spec §1: de svenska ytorna ska komma ut byte-identiska. Båda
        # byggarna renderar EN *och* SV i samma körning, så de skrivs
        # varje gång de engelska renderas om.
        "untouched": (
            "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-sv.pdf",
            "_unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-sv.pdf",
        ),
    },
}

GUIDES = tuple(GUIDE_DELIVERY)

# Röd till Task 13 har renderat om PDF:erna. Mängden är PER PDF, inte per
# guide: quick-starten bär INGEN av de arton förbudssträngarna redan i dag
# (mätt 2026-10-12 — den har varken svensk inramning eller juridisk text),
# så en xfail på den vore en strikt XPASS, alltså röd av fel skäl. Samma
# form som XFAIL_UNTIL_RECOUNTED i test_guide_toc.py: (guide, identitet).
XFAIL_UNTIL_RERENDERED = {
    ("gemini", "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-en.pdf"),
}


def delivery_for(guide: str) -> dict:
    try:
        return GUIDE_DELIVERY[guide]
    except KeyError:
        raise KeyError(
            f"okänd guide {guide!r}, kända: {sorted(GUIDE_DELIVERY)}"
        ) from None


def _flat(rel: str) -> str:
    """pdftotext -layout bryter rader mitt i meningar; en sträng som
    'Swedish schools' står med radbrytning emellan i den renderade
    filen. Platta till allt blankt till ett mellanslag innan sökning."""
    return re.sub(r"\s+", " ", fp.extract(fp.ROOT / rel))


def _merge_base() -> str:
    """Grenens avstamp från `main`. Jämförelsepunkten måste ligga före
    rundan: på `HEAD` vore vakten en snubbeltråd i arbetsträdet, och en
    gång committad skada skulle passera för alltid."""
    return subprocess.run(
        ["git", "merge-base", "main", "HEAD"],
        capture_output=True, text=True, check=True, cwd=fp.ROOT).stdout.strip()


def _delivery_cases():
    for guide, cfg in GUIDE_DELIVERY.items():
        for rel in cfg["pdfs"]:
            marks = ([pytest.mark.xfail(
                        strict=True,
                        reason="röd till Task 13 har renderat om PDF:erna")]
                     if (guide, rel) in XFAIL_UNTIL_RERENDERED else [])
            yield pytest.param(guide, rel, marks=marks, id=f"{guide}:{rel.rsplit('/', 1)[-1]}")


@pytest.mark.parametrize("guide,rel", list(_delivery_cases()))
def test_the_delivered_pdfs_carry_no_abandoned_claim(guide, rel):
    flat = _flat(rel)
    found = [needle for needle in delivery_for(guide)["forbidden"] if needle in flat]
    assert found == [], f"{rel} bär kvar: {found}"


@pytest.mark.parametrize("guide", GUIDES)
def test_the_quick_start_pdf_is_part_of_the_delivery_guard(guide):
    """Quick-starten står utanför ytvakten med avsikt. Faller den också
    ur den här vakten bevakas dess innehåll av ingenting alls."""
    pdfs = delivery_for(guide)["pdfs"]
    assert any("quick-start" in rel for rel in pdfs), guide
    for rel in pdfs:
        assert rel in fp.UNPUBLISHED_GUIDE_PDFS, f"{rel} står inte i facitlistan"


@pytest.mark.parametrize("guide", GUIDES)
def test_each_guides_forbidden_list_is_its_own(guide):
    """Granskningsfokus 1: listan får inte bli delad igen. En guide utan
    egna strängar är en guide vars vakt någon har slagit ihop."""
    cfg = delivery_for(guide)
    assert cfg["forbidden"], f"{guide}: tom förbudslista"
    others = {needle for other, c in GUIDE_DELIVERY.items() if other != guide
              for needle in c["forbidden"]}
    assert set(cfg["forbidden"]) - others, (
        f"{guide}: varje förbjuden sträng delas med en annan guide — "
        "listan har slagits ihop och vaktar inte den här guidens beslut")


def test_geminis_forbidden_list_does_not_ban_what_the_spec_keeps():
    """Granskningsfokus 1, andra halvan. Två saker STANNAR i Gemini-
    guiden och en kopierad Copilot-lista hade förbjudit båda: det
    källbelagda Fristadsskolan-exemplet (spec §9: medvetet, motiverat
    exempel med en post) och promptmallens GDPR-platshållare (spec §3).
    En bar sträng här skulle göra vakten röd för rätt innehåll."""
    forbidden = delivery_for("gemini")["forbidden"]
    for kept in ("Sweden", "Swedish", "GDPR", "EU AI Act", "Article 4"):
        assert kept not in forbidden, (
            f"{kept!r} är en bar sträng i Geminis förbudslista — "
            "den träffar innehåll rundan har beslutat att behålla")


@pytest.mark.xfail(strict=True, reason="röd till Task 13 har renderat om PDF:erna")
def test_geminis_cover_and_closing_carry_the_rounds_date():
    """Datumstämplarna, var och en på sin plats.

    En bar förbudsrad på "April 2026" går inte för den här guiden (se
    kommentaren i kartan), så omslaget kontrolleras som SIDA 1 och
    avslutningen genom signaturens hela sträng. Det är de två ställen där
    datumet är en stämpel på dokumentet och inte ett påstående om en
    produkt.
    """
    main = "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-en.pdf"
    cover = re.sub(r"\s+", " ", fp.pages(fp.extract(fp.ROOT / main))[0])
    assert "October 2026" in cover, "omslaget bär inte rundans datum"
    assert "April 2026" not in cover, "omslaget bär kvar den gamla stämpeln"
    flat = _flat(main)
    assert "Johan Lindström, October 2026" in flat
    assert "Johan Lindström, April 2026" not in flat


@pytest.mark.parametrize(
    "rel", GUIDE_DELIVERY["gemini"]["untouched"],
    ids=lambda rel: rel.rsplit("/", 1)[-1])
def test_the_swedish_gemini_pdfs_are_untouched_since_the_merge_base(rel):
    """Granskningsfokus 5: båda byggarna renderar EN *och* SV utan
    språkargument, så de svenska filerna skrivs varje gång de engelska
    renderas om. Återställs de slarvigt är INNEHÅLLSfacit ändå
    oförändrat — fingeravtrycket är detsamma, bara `CreationDate` har
    rört sig — och hela sviten går grön medan två filer ligger ändrade.
    Den här vakten jämför bytes mot bascommiten, inte innehåll."""
    committed = subprocess.run(
        ["git", "show", f"{_merge_base()}:{rel}"],
        capture_output=True, check=True, cwd=fp.ROOT).stdout
    assert hashlib.sha256(committed).hexdigest() == \
           hashlib.sha256((fp.ROOT / rel).read_bytes()).hexdigest(), \
           f"{rel} är inte byte-identisk med bascommiten — spec §1"
