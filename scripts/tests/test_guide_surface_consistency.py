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
    assert surfacecheck.normalise("~$20 / mo") == surfacecheck.normalise("~$20 / mo")
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


def test_rows_marked_borttaget_are_skipped():
    """Granskningsfokus 4: ett utgånget påstående ska inte göra vakten
    röd för alltid."""
    rows = [Row("P03", "en", "Cowork is a tab inside Claude Desktop", "borttaget")]
    surfaces = {("en", "web"): "", ("en", "print"): ""}
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


def test_the_real_inventory_parses_and_the_real_surfaces_agree():
    rows = [r for r in factinventory.load() if r.status == "aktiv"]
    if not rows:
        pytest.skip("vaktblocket är tomt — fylls i Task 8")
    problems = surfacecheck.check(rows, surfacecheck.read_surfaces())
    assert not problems, "\n".join(
        f"{p.id} [{p.lang}] {p.kind}: {p.detail}" for p in problems)
