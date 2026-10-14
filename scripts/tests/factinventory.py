"""Läser vaktblocket ur påståendeinventeringen.

Inventeringen är ett dokument för människor. Blocket mellan ```guard
och ``` är den enda delen som läses maskinellt, så att vakten och
källloggen är samma fil och inte två listor att hålla i synk.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[2]
INVENTORIES = {
    "claude":  ROOT / "docs" / "guide-facts-claude.md",
    "copilot": ROOT / "docs" / "guide-facts-copilot.md",
    "gemini":  ROOT / "docs" / "guide-facts-gemini.md",
    "apple-intelligence": ROOT / "docs" / "guide-facts-apple-intelligence.md",
}


def inventory_path(guide: str) -> Path:
    try:
        return INVENTORIES[guide]
    except KeyError:
        raise KeyError(
            f"okänd guide {guide!r}, kända: {sorted(INVENTORIES)}"
        ) from None


_BLOCK = re.compile(r"^```guard\s*$(.*?)^```\s*$", re.M | re.S)
_STATUSES = {"aktiv", "borttaget"}


class Row(NamedTuple):
    id: str
    lang: str
    value: str
    status: str


def load(path: Path) -> list:
    text = path.read_text(encoding="utf-8")
    rows = []
    for block in _BLOCK.findall(text):
        for line in block.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) != 4:
                raise ValueError(
                    f"raden {parts[0] if parts else line!r} har {len(parts)} kolumner, "
                    "formatet är: id | språk | värde | status"
                )
            ident, lang, value, status = parts
            if status not in _STATUSES:
                raise ValueError(f"{ident}: okänd status {status!r}, väntade {_STATUSES}")
            rows.append(Row(ident, lang, value, status))
    return rows
