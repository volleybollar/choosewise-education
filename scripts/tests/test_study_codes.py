"""Vakter för sidan Visual codes for studying (/visual-codes/study/).

Datafilen är sidans enda källa: varje kort, varje kopieringsknapp och varje
bild byggs från den. Viktigast är att tilläggsmeningen på varje kort är exakt
den som gav bilden — annars ljuger sidan.
"""
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "visual-codes/study"
DATA = PAGE / "codes-study-en.json"
# Testmappen ligger utanför repot. Saknas den hoppas jämförelsen med
# prompterna över — på en annan maskin finns den inte.
SOURCE = Path.home() / "Projekt/Choosewise/visual-codes-study-test"

ORDER = ["test-yourself", "explain-it", "see-the-whole",
         "follow-the-sequence", "remember-and-compare", "doesnt-work-yet"]
STATUSES = {"works", "partial", "fails"}
USES = {"print", "wall", "digital"}
HERO_IMAGES = ["hero-cheatsheet", "hero-quizmate", "feynman-codeonly"]


def all_codes():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    return [(s, c) for s in data["sections"] for c in s["codes"]]


def test_sections_in_the_agreed_order():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    assert [s["id"] for s in data["sections"]] == ORDER


def test_every_code_has_required_fields():
    slugs = []
    for _, c in all_codes():
        assert c["code"].startswith("/"), c["code"]
        assert re.fullmatch(r"[a-z0-9-]+", c["slug"]), c["slug"]
        assert c["status"] in STATUSES, c["code"]
        assert set(c["uses"]) <= USES, c["code"]
        assert c["description"].strip() and c["subject"].strip(), c["code"]
        slugs.append(c["slug"])
    assert len(slugs) == len(set(slugs)), "slug måste vara unik"


def test_part_1_codes_all_carry_an_addition():
    """Övningskoderna fungerar bara med tilläggsmeningen — utan den skrev
    modellen ut svaren. Ett kort i del 1 utan Add-rad vore ett tomt löfte."""
    for s, c in all_codes():
        if s["part"] == 1:
            assert c.get("addition"), c["code"]


def test_fails_only_in_the_doesnt_work_box():
    for s, c in all_codes():
        assert (c["status"] == "fails") == (s["id"] == "doesnt-work-yet"), c["code"]


def test_every_image_exists_in_both_sizes():
    slugs = [c["slug"] for _, c in all_codes()] + HERO_IMAGES
    for slug in slugs:
        for name in (f"{slug}.webp", f"{slug}-512w.webp"):
            assert (PAGE / "images" / name).exists(), name


@pytest.mark.skipif(not SOURCE.exists(), reason="testmappen finns bara på Johans dator")
def test_addition_is_exactly_what_was_sent():
    """Prompten som skickades ligger bredvid varje bild som .txt:
    '<kod> <ämne>. Make it an image. <tillägg>'."""
    for _, c in all_codes():
        sent = (SOURCE / c["source"]).with_suffix(".txt").read_text().strip()
        expected = f"{c['code']} {c['subject']}. Make it an image."
        if c.get("addition"):
            expected += " " + c["addition"]
        assert sent == expected, c["code"]
