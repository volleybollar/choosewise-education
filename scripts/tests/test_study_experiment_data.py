"""Vakter för datafilen till The Study Experiment (/study-experiment/).

Datafilen är sidans, resultatvyns och PDF-kitets enda källa. Upplägget är
beslutat i specen: två lektioner med en veckas mellanrum, två grupper som
läser om och testar sig i omvänd ordning (motviktat), prediktionslappen och
poänglappen, och ingen personuppgift någonstans. Ändra inte dem här utan att
specen ändras först. Evidenstexterna är granskade mot källorna i slutgranskningen
2026-11-13. Testerna kontrollerar bara att källorna finns och har rätt form, inte vad
texterna säger, så en ändrad evidenstext måste läsas mot sin källa av en människa.
Spec: docs/superpowers/specs/2026-11-13-study-experiment-design.md.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "study-experiment/experiment-en.json"
MOVES = ROOT / "study-moves/moves-en.json"

LESSONS = ("lesson1", "lesson2")


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_two_lessons_with_steps():
    d = data()
    for key in LESSONS:
        lesson = d[key]
        assert lesson["intro"].strip(), key
        assert len(lesson["steps"]) >= 4, key
        for step in lesson["steps"]:
            assert step["text"].strip(), (key, step)
            # Minuter är ett heltal, eller None för ett steg utan egen tid.
            assert step["minutes"] is None or (
                isinstance(step["minutes"], int) and not isinstance(step["minutes"], bool)
            ), (key, step)


def test_lesson_minutes_add_up():
    d = data()
    for key in LESSONS:
        total = sum(s["minutes"] or 0 for s in d[key]["steps"])
        assert total <= d["minutes"][key], (key, total)


def test_group_cards_are_counterbalanced():
    cards = data()["group_cards"]
    assert [c["group"] for c in cards] == [1, 2]
    # Grupp 1 läser Text A två gånger, grupp 2 läser Text B två gånger.
    assert any("Read Text A again" in s for s in cards[0]["steps"])
    assert any("Read Text B again" in s for s in cards[1]["steps"])
    # Motvikten åt andra hållet: grupp 1 skriver från minnet efter Text B och läser
    # den inte om, grupp 2 skriver efter Text A och läser den inte om. Annars läser
    # någon grupp samma text två gånger i båda sätten, och experimentet säger ingenting.
    write = [[s for s in c["steps"] if "Write down everything you remember" in s] for c in cards]
    assert len(write[0]) == 1 and "Turn Text B over" in write[0][0]
    assert len(write[1]) == 1 and "Turn Text A over" in write[1][0]
    assert not any("Read Text B again" in s for s in cards[0]["steps"])
    assert not any("Read Text A again" in s for s in cards[1]["steps"])
    for c in cards:
        text = " ".join(c["steps"])
        assert "Text A" in text and "Text B" in text, c["group"]


def test_prediction_slip_has_three_options():
    slip = data()["prediction_slip"]
    assert slip["question"].strip()
    options = slip["options"]
    assert len(options) == 3
    # De tre kategorierna i ordning: läste två gånger, testade sig, ungefär lika.
    for option, word in zip(options, ("twice", "tested", "same")):
        assert word in option, (word, option)


def test_score_slip_two_lines():
    d = data()
    lines = d["score_slip"]["lines"]
    assert len(lines) == 2
    assert "twice" in lines[0]
    assert "tested" in lines[1]
    for line in lines:
        assert f"of {d['questions_per_text']}" in line, line


def test_discussion_and_even_result():
    d = data()
    assert len(d["discussion"]) >= 4
    assert all(q.strip() for q in d["discussion"])
    even = d["even_result"]
    assert even["title"].strip() and even["text"].strip()
    assert "one class" in even["text"].lower()


def test_explain_has_three_points():
    points = data()["explain"]["points"]
    assert len(points) == 3
    assert all(p.strip() for p in points)
    # Tredje punkten är motvikten: halva klassen testade sig på A, halva på B.
    assert "Text A" in points[2] and "Text B" in points[2]


def test_testing_steps_include_checking():
    # Att skriva från minnet räcker inte; steget efter måste vara att kontrollera.
    for card in data()["group_cards"]:
        steps = card["steps"]
        idx = [i for i, s in enumerate(steps) if "Write down everything you remember" in s]
        assert len(idx) == 1, card["group"]
        assert idx[0] + 1 < len(steps), card["group"]
        assert "mark what you missed" in steps[idx[0] + 1], card["group"]


def test_score_slip_has_check_box():
    d = data()
    check = d["score_slip"]["check"]
    assert check.strip() and "during the week" in check
    assert d["expect"].strip()


def test_every_source_https():
    # Listan får inte vara tom: då skulle loopen nedan godkänna ingenting.
    assert data()["evidence"]
    for i, item in enumerate(data()["evidence"]):
        assert item["text"].strip(), i
        assert item["sources"], i
        for s in item["sources"]:
            assert s["text"].strip() and s["url"].startswith("https://"), (i, s)


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


def _slip_texts(d):
    slip, score = d["prediction_slip"], d["score_slip"]
    return [slip["question"], *slip["options"], *score["lines"], score["check"]]


def test_no_personal_fields():
    # Experimentet är anonymt: inget fält och ingen lapp får be om namn eller e-post.
    d = data()
    for key in _keys(d):
        assert "name" not in key.lower(), key
        assert "email" not in key.lower(), key
    for text in _slip_texts(d):
        assert "name" not in text.lower(), text
