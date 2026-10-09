"""Omfångningen måste gå att rikta.

Våg 2b rör fyra av 22 nycklar. Skriptets docstring säger själv att en
--force-körning efter en ändring är liktydig med att slå av
paritetsvakten; den här filen gör det omöjligt att göra det av misstag.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from . import pdf_body_text as bt
from . import pdf_fingerprint as fp

_SPEC = importlib.util.spec_from_file_location(
    "capture_guide_baseline",
    Path(__file__).parent / "fixtures" / "capture_guide_baseline.py",
)

CLAUDE = [
    "assets/pdfs/guides/claude-guide-en.pdf",
    "assets/pdfs/guides/claude-guide-sv.pdf",
    "assets/pdfs/guides/claude-quick-start-en.pdf",
    "assets/pdfs/guides/claude-quick-start-sv.pdf",
]


def _module():
    mod = importlib.util.module_from_spec(_SPEC)
    mod.__name__ = "capture_guide_baseline"
    _SPEC.loader.exec_module(mod)
    return mod


def test_merge_baseline_replaces_only_named_keys():
    mod = _module()
    existing = {"a.pdf": {"pages": ["x"]}, "b.pdf": {"pages": ["y"]}}
    merged = mod.merge_baseline(existing, {"a.pdf": {"pages": ["NY"]}})
    assert merged["a.pdf"] == {"pages": ["NY"]}
    assert merged["b.pdf"] == {"pages": ["y"]}, "orörd nyckel ändrades"
    assert sorted(merged) == ["a.pdf", "b.pdf"], "nyckeluppsättningen ändrades"


def test_merge_baseline_refuses_an_unknown_key():
    mod = _module()
    with pytest.raises(KeyError):
        mod.merge_baseline({"a.pdf": {}}, {"okänd.pdf": {}})


def test_force_cannot_silently_reset_unrelated_entries():
    """Granskningsfokus 1: de arton PDF:er rundan inte öppnat ska stå still.

    Facit på disk måste fortfarande täcka exakt 22 nycklar, och de
    arton som inte är Claudes ska vara oförändrade mot det committade
    läget. Testet jämför mot git, inte mot sig självt.
    """
    import json, subprocess
    committed = json.loads(subprocess.run(
        ["git", "show", f"HEAD:{fp.BASELINE.relative_to(fp.ROOT)}"],
        capture_output=True, text=True, check=True, cwd=fp.ROOT).stdout)
    current = json.loads(fp.BASELINE.read_text(encoding="utf-8"))
    assert sorted(current) == sorted(fp.GUIDE_PDFS), "nyckeluppsättningen ändrades"
    for rel in fp.GUIDE_PDFS:
        if rel in CLAUDE:
            continue
        assert current[rel] == committed[rel], f"{rel} omfångades utan att röras"


def test_force_cannot_silently_reset_unrelated_body_entries():
    """Samma granskningsfokus, men för kroppstextfacit.

    De två faciten skrivs av samma `_write`/`merge_baseline`-väg i dag,
    men inget hindrar en framtida ändring från att grena isär de två
    skrivvägarna — och då fångar sidfingeravtryckets test ovan ingenting
    på kroppstextsidan. Den här kopian finns så att en sådan gren inte
    kan tysta regressionen: `bt.BASELINE` måste täcka exakt 22 nycklar,
    och de arton som inte är Claudes ska vara oförändrade mot det
    committade läget. Testet jämför mot git, inte mot sig självt.
    """
    import json, subprocess
    committed = json.loads(subprocess.run(
        ["git", "show", f"HEAD:{bt.BASELINE.relative_to(fp.ROOT)}"],
        capture_output=True, text=True, check=True, cwd=fp.ROOT).stdout)
    current = json.loads(bt.BASELINE.read_text(encoding="utf-8"))
    assert sorted(current) == sorted(fp.GUIDE_PDFS), "nyckeluppsättningen ändrades"
    for rel in fp.GUIDE_PDFS:
        if rel in CLAUDE:
            continue
        assert current[rel] == committed[rel], f"{rel} omfångades utan att röras"
