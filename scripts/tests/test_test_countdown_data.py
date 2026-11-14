"""Vakter för datafilen till Test Countdown (/test-countdown/).

Datafilen är sidans enda källa för den statiska texten: hur man testar sig
själv, varför planen ser ut som den gör, noterna för kort och långt avstånd,
lärartexterna, forskningen och åldersreglerna. Planens egna regler och texter
ligger i assets/js/test-countdown.js och vaktas av egna tester. Ändra inte
innehållet här utan att specen ändras först. Evidenstexterna är granskade mot
källorna; testerna kontrollerar bara att källorna finns och har rätt form, inte
vad texterna säger, så en ändrad evidenstext måste läsas mot sin källa av en
människa. Inget fält får be om namn eller e-post: planen är anonym.
Spec: docs/superpowers/specs/2026-11-14-test-countdown-design.md.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "test-countdown/countdown-en.json"
MOVES = ROOT / "study-moves/moves-en.json"


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_how_to_has_four_steps():
    d = data()
    how = d["how_to"]
    assert how["title"].strip()
    steps = how["steps"]
    assert len(steps) == 4
    assert all(s.strip() for s in steps)
    # Första steget är att stänga boken, tredje att kontrollera mot anteckningarna.
    assert "close" in steps[0].lower()
    assert "check" in steps[2].lower()
    assert d["feels_harder"].strip()
    assert d["sensible"].strip()


def test_why_has_five_points():
    why = data()["why"]
    assert why["title"].strip() and why["intro"].strip()
    points = why["points"]
    assert len(points) == 5
    assert all(p.strip() for p in points)
    # Sömnen och övningsprovet är två av skälen bakom planens form.
    assert any("sleep" in p.lower() for p in points)
    assert any("practice test" in p.lower() for p in points)


def test_notes():
    d = data()
    for key in ("short_note", "share", "no_ai", "student_ai"):
        assert d[key].strip(), key
    # Planen börjar högst tre veckor före provet, och noten säger det.
    assert "three weeks" in d["capped_note"]
    # Elev-AI nämns bara för elever från 13 år.
    assert "13" in d["student_ai"]


def test_every_source_https():
    evidence = data()["evidence"]
    # Listan får inte vara tom eller för kort: då skulle loopen nedan godkänna för lite.
    assert len(evidence) >= 4
    for i, item in enumerate(evidence):
        assert item["text"].strip(), i
        assert len(item["sources"]) >= 1, i
        for s in item["sources"]:
            assert s["text"].strip(), (i, s)
            assert s["url"].startswith("https://"), (i, s)


def test_age_rules_match_study_moves():
    # Åldersreglerna ska aldrig glida isär från Study Moves; där granskas de.
    d = data()
    moves = json.loads(MOVES.read_text(encoding="utf-8"))
    assert d["age_rules"] == moves["age_rules"]
    assert d["age_rules_date"] == moves["age_rules_date"]


def _keys(obj):
    """Alla nycklar i ett JSON-objekt, på alla nivåer."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from _keys(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _keys(v)


def test_no_personal_fields():
    # Planen är anonym: inget fält får be om namn eller e-post.
    keys = list(_keys(data()))
    assert keys  # en tom lista skulle godkänna allt
    for key in keys:
        assert "name" not in key.lower(), key
        assert "email" not in key.lower(), key
