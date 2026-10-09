"""Vaktblocket i inventeringen måste gå att läsa maskinellt.

Ett markdown-dokument som parsas på fri text är sprött. Blocket är
därför en avgränsad fence med ett fast kolumnformat, och det här
testet är det som håller formatet ärligt.
"""
from __future__ import annotations

import textwrap

from . import factinventory


def test_parses_id_lang_value_and_status(tmp_path):
    doc = tmp_path / "inv.md"
    doc.write_text(textwrap.dedent("""\
        # Inventering

        Prosa som inte ska läsas.

        ```guard
        P01 | en | Pricing accurate as of October 2026 | aktiv
        P01 | sv | Priserna stämmer per oktober 2026 | aktiv
        P09 | en | Cowork is a tab inside Claude Desktop | borttaget
        ```

        Mer prosa.
        """), encoding="utf-8")
    rows = factinventory.load(doc)
    assert [r.id for r in rows] == ["P01", "P01", "P09"]
    assert [r.lang for r in rows] == ["en", "sv", "en"]
    assert rows[1].value == "Priserna stämmer per oktober 2026"
    assert rows[2].status == "borttaget"


def test_ignores_prose_that_looks_like_a_row(tmp_path):
    doc = tmp_path / "inv.md"
    doc.write_text(textwrap.dedent("""\
        Utanför blocket står en tabellrad: P99 | en | lurendrejeri | aktiv

        ```guard
        P01 | en | riktig rad | aktiv
        ```
        """), encoding="utf-8")
    rows = factinventory.load(doc)
    assert len(rows) == 1
    assert rows[0].id == "P01"


def test_rejects_a_row_with_the_wrong_column_count(tmp_path):
    doc = tmp_path / "inv.md"
    doc.write_text("```guard\nP01 | en | saknar status\n```\n", encoding="utf-8")
    try:
        factinventory.load(doc)
    except ValueError as exc:
        assert "P01" in str(exc)
    else:
        raise AssertionError("en rad med tre kolumner ska avvisas, inte tolkas")
