"""Jämför guidens webbyta med dess printyta, inom ett språk.

PDF:en renderas ur print-filen, inte ur webbsidan, och de två har redan
40 % egen formulering. Ingen av våg 2a:s vakter ser skillnaden. Den här
modulen jämför bara de värden inventeringen pekar ut.
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[2]

SURFACES = {
    ("en", "web"):   "guides/claude/index.html",
    ("en", "print"): "exports/claude-print-a4-en.html",
    ("sv", "web"):   "sv/guider/claude/index.html",
    ("sv", "print"): "exports/claude-print-a4-sv.html",
}

_TAG = re.compile(r"<[^>]+>")
_SCRIPT = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)
_DASHES = dict.fromkeys(map(ord, "‐‑‒–—−"), "-")


class Problem(NamedTuple):
    id: str
    lang: str
    kind: str
    detail: str


def normalise(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).translate(_DASHES)
    return re.sub(r"\s+", " ", text).strip()


def read_surfaces(root: Path = ROOT) -> dict:
    out = {}
    for key, rel in SURFACES.items():
        raw = (root / rel).read_text(encoding="utf-8")
        out[key] = normalise(_TAG.sub(" ", _SCRIPT.sub(" ", raw)))
    return out


def check(rows, surfaces: dict) -> list:
    problems = []
    langs_by_id = {}
    for row in rows:
        if row.status != "aktiv":
            continue
        langs_by_id.setdefault(row.id, set()).add(row.lang)

    for row in rows:
        if row.status != "aktiv":
            continue
        needle = normalise(row.value)
        hits = {
            where: needle in normalise(surfaces.get((row.lang, where), ""))
            for where in ("web", "print")
        }
        if not any(hits.values()):
            problems.append(Problem(
                row.id, row.lang, "finns_ingenstans",
                f"{row.value!r} finns varken på webbytan eller printytan — "
                "sannolikt ett stavfel i inventeringen, inte ett innehållsfel"))
        elif not all(hits.values()):
            missing = [w for w, ok in hits.items() if not ok][0]
            problems.append(Problem(
                row.id, row.lang, "saknas_på_en_yta",
                f"{row.value!r} saknas på {missing}ytan"))

        if row.lang == "sv" and "en" not in langs_by_id.get(row.id, set()):
            problems.append(Problem(
                row.id, row.lang, "saknar_motpart",
                "svensk rad utan engelsk motpart — kronvärdet hänger på "
                "dollarvärdet och får inte rättas ensamt"))
    return problems
