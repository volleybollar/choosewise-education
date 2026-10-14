"""Jämför guidens webbyta med dess printyta, inom ett språk.

PDF:en renderas ur print-filen, inte ur webbsidan, och de två har redan
40 % egen formulering. Ingen av våg 2a:s vakter ser skillnaden. Den här
modulen jämför bara de värden inventeringen pekar ut.

Två motsatta lägen, styrda av radens status: `aktiv` kräver att strängen
står på båda ytorna, `borttaget` att den inte står på någon av dem. Det
senare är förbudsvakten — utan den kan ett struket påstående skrivas
tillbaka utan att något blir rött.
"""
from __future__ import annotations

import html
import re
import unicodedata
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[2]

GUIDE_SURFACES = {
    "claude": {
        ("en", "web"):   "guides/claude/index.html",
        ("en", "print"): "exports/claude-print-a4-en.html",
        ("sv", "web"):   "sv/guider/claude/index.html",
        ("sv", "print"): "exports/claude-print-a4-sv.html",
    },
    # Copilot ligger under _unpublished/ — GitHub Pages serverar inte
    # kataloger som börjar med understreck, verifierat 2026-10-09 (404 på
    # alla fyra utkastkataloger). De svenska ytorna står med i kartan fast
    # rundan inte rör dem: de FINNS, och en svensk vaktrad ska jämföras mot
    # dem och inte mot ingenting. Att de divergerar i sak från de engelska
    # är ett känt läge (spec §5), inte något vakten ska dölja.
    "copilot": {
        ("en", "web"):   "_unpublished/guides/copilot/index.html",
        ("en", "print"): "_unpublished/exports/copilot-print-a4-en.html",
        ("sv", "web"):   "_unpublished/sv/guider/copilot/index.html",
        ("sv", "print"): "_unpublished/exports/copilot-print-a4-sv.html",
    },
    # Gemini-guiden ligger under _unpublished/ av samma skäl som Copilot:
    # GitHub Pages serverar inte kataloger som börjar med understreck. De
    # svenska ytorna står med i kartan fast rundan inte rör dem — de FINNS,
    # och en svensk vaktrad ska jämföras mot dem och inte mot ingenting. Att
    # de divergerar i sak från de engelska är ett känt läge (spec §1), inte
    # något vakten ska dölja.
    "gemini": {
        ("en", "web"):   "_unpublished/guides/gemini-notebook/index.html",
        ("en", "print"): "_unpublished/exports/gemini-notebook-print-a4-en.html",
        ("sv", "web"):   "_unpublished/sv/guider/gemini-notebooklm/index.html",
        ("sv", "print"): "_unpublished/exports/gemini-notebooklm-print-a4-sv.html",
    },
    # Apple Intelligence ligger under _unpublished/ av samma skäl som
    # Copilot och Gemini: GitHub Pages serverar inte kataloger som börjar
    # med understreck. De svenska ytorna står med fast runda 1 bara rör
    # deras typsnitt — de FINNS, och en svensk vaktrad ska jämföras mot
    # dem och inte mot ingenting. Att de divergerar i sak från de engelska
    # efter runda 2 är ett känt läge (spec §1), inte något vakten ska dölja.
    "apple-intelligence": {
        ("en", "web"):   "_unpublished/guides/apple-intelligence/index.html",
        ("en", "print"): "_unpublished/exports/apple-intelligence-print-a4-en.html",
        ("sv", "web"):   "_unpublished/sv/guider/apple-intelligence/index.html",
        ("sv", "print"): "_unpublished/exports/apple-intelligence-print-a4-sv.html",
    },
}
GUIDES = tuple(GUIDE_SURFACES)


def surfaces_for(guide: str) -> dict:
    try:
        return GUIDE_SURFACES[guide]
    except KeyError:
        raise KeyError(
            f"okänd guide {guide!r}, kända: {sorted(GUIDE_SURFACES)}"
        ) from None


_TAG = re.compile(r"<[^>]+>")
_SCRIPT = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)
_DASHES = dict.fromkeys(map(ord, "‐‑‒–—−"), "-")
_SURFACE_NAMES = {"web": "webbytan", "print": "printytan"}


class Problem(NamedTuple):
    id: str
    lang: str
    kind: str
    detail: str


def normalise(text: str) -> str:
    text = html.unescape(text)
    text = unicodedata.normalize("NFKC", text).translate(_DASHES)
    return re.sub(r"\s+", " ", text).strip()


def read_surfaces(guide: str, root: Path = ROOT) -> dict:
    out = {}
    for key, rel in surfaces_for(guide).items():
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
        needle = normalise(row.value)
        hits = {
            where: needle in normalise(surfaces.get((row.lang, where), ""))
            for where in ("web", "print")
        }

        if row.status == "borttaget":
            standing = [where for where, ok in hits.items() if ok]
            if standing:
                problems.append(Problem(
                    row.id, row.lang, "återinfört",
                    f"{row.value!r} är struket ur guiden men står på "
                    + " och ".join(_SURFACE_NAMES[where] for where in standing)))
            continue

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
