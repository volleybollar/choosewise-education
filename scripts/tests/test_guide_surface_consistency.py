"""Webbytan och printytan ska vara överens om de volatila värdena.

Per språk, inte mellan språk: den svenska guiden prissätter i kronor
med avsikt, och en vakt som krävde samma värde över språkgränsen vore
röd från första dagen och alltså värdelös.

Vakten jämför bara de värden inventeringen pekar ut. Ytorna skiljer sig
40 % i formulering med avsikt; ordagrann likhet vore fel krav.
"""
from __future__ import annotations

import pytest

from . import factinventory, surfacecheck
from .factinventory import Row


def test_comparison_normalises_whitespace_and_dashes():
    """Granskningsfokus 3: typografi får inte göra vakten falskt röd."""
    assert surfacecheck.normalise("~$20\u00a0/ mo") == surfacecheck.normalise("~$20 / mo")
    assert surfacecheck.normalise("april–2026") == surfacecheck.normalise("april-2026")
    assert surfacecheck.normalise("a  b\n c") == surfacecheck.normalise("a b c")


def test_reports_a_value_missing_from_one_surface():
    rows = [Row("P01", "en", "Second edition", "aktiv")]
    surfaces = {("en", "web"): "Second edition, October 2026", ("en", "print"): "First edition"}
    problems = surfacecheck.check(rows, surfaces)
    assert [p.kind for p in problems] == ["saknas_på_en_yta"]
    assert "print" in problems[0].detail


def test_checker_separates_typo_from_missing_on_one_surface():
    """Granskningsfokus 2: en sträng som finns ingenstans är ett stavfel
    i inventeringen, inte ett innehållsfel — annars letar redaktören fel."""
    rows = [Row("P02", "en", "Tredje upplagan", "aktiv")]
    surfaces = {("en", "web"): "Second edition", ("en", "print"): "Second edition"}
    problems = surfacecheck.check(rows, surfaces)
    assert [p.kind for p in problems] == ["finns_ingenstans"]


def test_a_removed_claim_that_stays_removed_is_green():
    """Granskningsfokus 4: ett utgånget påstående ska inte göra vakten
    röd för alltid. `borttaget` kräver frånvaro, inte tystnad."""
    rows = [Row("P03", "en", "Cowork is a tab inside Claude Desktop", "borttaget")]
    surfaces = {("en", "web"): "Cowork is a way of working", ("en", "print"): ""}
    assert surfacecheck.check(rows, surfaces) == []


def test_a_removed_claim_written_back_in_turns_the_guard_red():
    """Förbudsvakten själv. Hålet våg 2b lämnade: varje rad letade efter
    det korrekta påståendet och var tyst om huruvida det felaktiga också
    stod där. En redaktör som skrev tillbaka ett struket påstående mötte
    inget motstånd alls."""
    rows = [Row("P22", "en", "extended thinking", "borttaget")]
    surfaces = {("en", "web"): "Pro adds extended thinking", ("en", "print"): ""}
    problems = surfacecheck.check(rows, surfaces)
    assert [p.kind for p in problems] == ["återinfört"]
    assert "web" in problems[0].detail


def test_a_reintroduced_claim_names_every_surface_it_stands_on():
    """Felmeddelandet ska säga var strängen står, inte bara att den gör
    det — annars får redaktören leta på fyra ytor."""
    value = "Cowork sits as a tab inside Claude Desktop"
    rows = [Row("P06", "en", value, "borttaget")]
    surfaces = {("en", "web"): value, ("en", "print"): value}
    problems = surfacecheck.check(rows, surfaces)
    assert [p.kind for p in problems] == ["återinfört"]
    assert "webbytan" in problems[0].detail and "printytan" in problems[0].detail


def test_a_removed_row_needs_no_counterpart_in_the_other_language():
    """`saknar_motpart` finns för att kronvärdet inte får rättas utan
    dollarvärdet. En struken sträng bär ingen sådan koppling, och en
    svensk förbudsrad utan engelsk syskonrad är helt legitim."""
    rows = [Row("P12", "sv", "enklare än ChatGPT:s custom GPTs", "borttaget")]
    surfaces = {("sv", "web"): "", ("sv", "print"): ""}
    assert surfacecheck.check(rows, surfaces) == []


def test_derived_rows_require_their_source_row_to_be_resolved():
    """Granskningsfokus 5: kronpriset hänger på dollarpriset. Finns en
    svensk rad för ett id, måste den engelska för samma id också finnas,
    annars kan den ena rättas utan den andra."""
    rows = [Row("P04", "sv", "ca 200 kr / mån", "aktiv")]
    surfaces = {("sv", "web"): "ca 200 kr / mån", ("sv", "print"): "ca 200 kr / mån"}
    problems = surfacecheck.check(rows, surfaces)
    assert any(p.kind == "saknar_motpart" for p in problems)


def test_an_english_only_row_needs_no_swedish_counterpart():
    """Granskningsfokus 5, andra riktningen: ett engelskt påstående får
    sakna svensk motsvarighet helt legitimt — bara kronvärdet hänger på
    dollarvärdet och får inte rättas ensamt, inte tvärtom."""
    rows = [Row("P05", "en", "Second edition", "aktiv")]
    surfaces = {("en", "web"): "Second edition", ("en", "print"): "Second edition"}
    problems = surfacecheck.check(rows, surfaces)
    assert not any(p.kind == "saknar_motpart" for p in problems)


def test_comparison_unescapes_html_entities():
    """Granskningsfokus 1: Copilots rubriker bär `&amp;`. En vaktrad
    skriven som läsaren ser den ska matcha markupen, inte tvingas skriva
    om sig till entiteten."""
    assert surfacecheck.normalise("Compliance &amp; licensing") == \
           surfacecheck.normalise("Compliance & licensing")
    assert surfacecheck.normalise("13&nbsp;+") == surfacecheck.normalise("13 +")


def test_an_unknown_guide_is_a_loud_error():
    """Granskningsfokus 4: en guide som inte finns får inte ge en tom
    ytkarta — då vaktar vakten ingenting och är grön för det."""
    # Namnet måste vara ett som aldrig kan bli en guide. Här stod
    # `gemini` fram till Task 12 — ett sentinelvärde som slutade vakta
    # någonting i samma sekund som Gemini lades in i kartan, och i
    # stället gjorde testet rött. Felet ska dessutom räkna upp de kända
    # guiderna, så att det berättar vad som fanns att välja på.
    absent = "ingen-sådan-guide"
    with pytest.raises(KeyError) as exc:
        surfacecheck.surfaces_for(absent)
    assert all(g in str(exc.value) for g in surfacecheck.GUIDES)

    with pytest.raises(KeyError) as inv_exc:
        factinventory.inventory_path(absent)
    assert all(g in str(inv_exc.value) for g in surfacecheck.GUIDES)


@pytest.mark.parametrize("guide", surfacecheck.GUIDES)
def test_every_guide_has_an_inventory_file(guide):
    """Granskningsfokus 4, andra halvan: en guide i ytkartan utan
    inventering kan aldrig få en vaktrad, och vakten vore tyst om det."""
    assert factinventory.inventory_path(guide).exists()


@pytest.mark.parametrize("guide", surfacecheck.GUIDES)
def test_every_guide_surface_file_exists(guide):
    for (lang, where), rel in surfacecheck.surfaces_for(guide).items():
        assert (surfacecheck.ROOT / rel).is_file(), f"{guide} {lang}/{where}: {rel} saknas"


# Guider vars fyra ytor ligger under _unpublished/, som Pages inte
# serverar. Claude är publicerad; de andra tre tas i sina egna rundor.
UNPUBLISHED_GUIDES = ("copilot", "gemini")


@pytest.mark.parametrize("guide", UNPUBLISHED_GUIDES)
def test_unpublished_guides_surfaces_are_under_unpublished(guide):
    """Granskningsfokus 5 i Copilot-rundan, nu för två guider: pekar
    kartan på `guides/<guide>/` läser vakten en fil som inte finns —
    eller en dag den fel."""
    rels = list(surfacecheck.surfaces_for(guide).values())
    assert len(rels) == 4
    assert all(rel.startswith("_unpublished/") for rel in rels), rels


def test_every_unpublished_guide_is_in_the_surface_map():
    """Listan ovan får inte glida ifrån ytkartan. En guide som läggs i
    kartan men inte här tappar sin sökvägsvakt tyst."""
    assert set(UNPUBLISHED_GUIDES) <= set(surfacecheck.GUIDES)
    assert "claude" not in UNPUBLISHED_GUIDES


@pytest.mark.parametrize("guide", surfacecheck.GUIDES)
def test_every_guides_guard_block_is_not_empty(guide):
    """Ett tömt vaktblock gör de tre vakterna nedan grönt av fel skäl.

    De tre läser raderna och påstår något om varje — med noll rader
    passerar de utan att vakta något. Den här raden är det som gör ett
    tömt block rött, och den gäller varje guide i ytkartan: en vakt som
    bara skyddade Claudes block lämnade Copilots tömbart.
    """
    rows = factinventory.load(factinventory.inventory_path(guide))
    assert [r for r in rows if r.status == "borttaget"], f"{guide}: inga borttaget-rader"
    assert [r for r in rows if r.status == "aktiv"], f"{guide}: inga aktiv-rader"


def _rows(guide: str, status: str) -> list:
    return [r for r in factinventory.load(factinventory.inventory_path(guide))
            if r.status == status]


@pytest.mark.parametrize("guide", surfacecheck.GUIDES)
def test_the_real_inventory_parses_and_the_real_surfaces_agree(guide):
    rows = _rows(guide, "aktiv")
    problems = surfacecheck.check(rows, surfacecheck.read_surfaces(guide))
    assert not problems, "\n".join(
        f"{p.id} [{p.lang}] {p.kind}: {p.detail}" for p in problems)


@pytest.mark.parametrize("guide", surfacecheck.GUIDES)
def test_the_real_forbidden_list_is_absent_from_the_real_surfaces(guide):
    rows = _rows(guide, "borttaget")
    problems = surfacecheck.check(rows, surfacecheck.read_surfaces(guide))
    assert not problems, "\n".join(
        f"{p.id} [{p.lang}] {p.kind}: {p.detail}" for p in problems)


@pytest.mark.parametrize("guide", surfacecheck.GUIDES)
def test_the_real_forbidden_list_would_catch_a_reintroduction(guide):
    """Fälla 2: en vakt som inte setts bli röd vaktar ingenting. Här
    skrivs ett verkligt struket påstående tillbaka i en kopia av den
    verkliga engelska webbytan, och bara det id:t ska bli rött.

    Offret är den kortaste engelska förbudsraden, inte ett hårdkodat id —
    annars måste varje ny guide redigera testet. Precondition-assert:en
    håller valet ärligt, för innehåller offrets värde en annan förbudsrad
    blir två id:n röda och likhetsjämförelsen vore fel krav."""
    rows = [r for r in _rows(guide, "borttaget") if r.lang == "en"]
    victim = min(rows, key=lambda r: len(r.value))
    needle = surfacecheck.normalise(victim.value)
    assert not [r for r in rows
                if r.id != victim.id
                and surfacecheck.normalise(r.value) in needle], \
        f"{victim.id}:s värde innehåller en annan förbudsrad — välj ett annat offer"

    surfaces = dict(surfacecheck.read_surfaces(guide))
    surfaces[("en", "web")] += " " + victim.value
    problems = surfacecheck.check(rows, surfaces)
    assert [(p.id, p.lang, p.kind) for p in problems] == \
           [(victim.id, "en", "återinfört")]
