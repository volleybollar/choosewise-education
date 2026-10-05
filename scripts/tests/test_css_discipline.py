"""Färg bor i tokens.css. Ingen annanstans i assets/css/."""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CSS_DIR = ROOT / "assets/css"

HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")


def shared_stylesheets():
    return sorted(p for p in CSS_DIR.glob("*.css") if p.name != "tokens.css")


@pytest.mark.parametrize("path", shared_stylesheets(), ids=lambda p: p.name)
def test_no_hardcoded_hex_outside_tokens(path):
    found = HEX.findall(path.read_text(encoding="utf-8"))
    assert found == [], (
        f"{path.name} har {len(found)} hårdkodade färger: {sorted(set(found))[:8]}"
    )
