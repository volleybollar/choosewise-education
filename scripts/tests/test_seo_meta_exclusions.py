"""Sitemapen får aldrig peka in i en git-worktree.

EXCLUDE_DIR_PARTS listade .git men inte .worktrees. Eftersom build-seo-meta.py
går över filsystemet med rglob och inte över git-indexet, svepte den in varje
HTML-fil i .worktrees/<gren>/ — skrev om dem (vilket smutsar den öppna PR:ens
arbetskopia) och la ut dem som publika URL:er i sitemap.xml. Felet syns först
när en sökmotor följer https://choosewise.education/.worktrees/... och får 404.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _seo_module():
    spec = importlib.util.spec_from_file_location(
        "build_seo_meta", ROOT / "scripts/build-seo-meta.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_worktree_pages_are_excluded():
    """Vägen måste stängas på segmentet, inte på en enskild grennamnssträng —
    nästa worktree heter något annat."""
    seo = _seo_module()
    assert seo.is_excluded(".worktrees/gemini-guide-international/about/index.html")
    assert seo.is_excluded(".worktrees/nagon-framtida-gren/blog/index.html")


def test_a_normal_page_is_still_processed():
    """Motprov: vakten ska stänga worktrees, inte sajten."""
    seo = _seo_module()
    assert not seo.is_excluded("about/index.html")
    assert not seo.is_excluded("blog/posts/gpts-and-gems-retires.html")


def test_sitemap_lists_no_worktree_urls():
    """Vakten på artefakten som faktiskt når läsare."""
    sitemap = (ROOT / "sitemap.xml").read_text()
    assert ".worktrees" not in sitemap
