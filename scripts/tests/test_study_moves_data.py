"""Vakter för datafilen till Study Moves (/study-moves/).

Datafilen är sidans, promptbyggarens och PDF:ens enda källa. Ordningen på
de tio dragen, de sex målen och Test yourself som start är beslutade i
specen — ändra dem inte här utan att specen ändras först. Evidenstexter,
källor och åldersregler granskas fortfarande, så testerna kontrollerar
bara att de finns och har rätt form, inte vad de säger.
Spec: docs/superpowers/specs/2026-11-12-study-moves-design.md.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "study-moves/moves-en.json"

ORDER = ["test-yourself", "spread-it-out", "mix-it-up", "explain-it-simply", "ask-why",
         "draw-it", "find-an-example", "study-a-solved-example", "fix-your-mistakes", "guess-first"]
# Målen och deras drag, i specens ordning (tabellen "The six goals").
GOALS = {"remember": ["test-yourself", "spread-it-out"], "tell-apart": ["mix-it-up"],
         "understand": ["explain-it-simply", "ask-why", "draw-it", "find-an-example"],
         "solve": ["study-a-solved-example", "mix-it-up"], "fix": ["fix-your-mistakes"],
         "start": ["guess-first"]}
TEXT_FIELDS = ("name", "research_name", "one_liner", "feels", "watch_out", "evidence")


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def moves():
    return data()["moves"]


def test_moves_in_agreed_order():
    assert [m["id"] for m in moves()] == ORDER
    assert [m["number"] for m in moves()] == list(range(1, 11))


def test_default_move_is_test_yourself():
    assert data()["default_move"] == "test-yourself"


def test_goals_match_spec():
    goals = data()["goals"]
    assert [g["id"] for g in goals] == list(GOALS)
    for g in goals:
        assert g["moves"] == GOALS[g["id"]], g["id"]
        assert g["name"].strip() and g["description"].strip(), g["id"]


def test_move_goals_mirror_goal_lists():
    # Målen står på två ställen (i målet och i draget); de måste säga samma sak.
    goals = data()["goals"]
    for m in moves():
        listed_in = [g["id"] for g in goals if m["id"] in g["moves"]]
        assert sorted(m["goals"]) == sorted(listed_in), m["id"]


def test_every_move_has_a_goal():
    in_goals = {mid for g in data()["goals"] for mid in g["moves"]}
    for m in moves():
        assert m["id"] in in_goals, m["id"]


def test_labels_defined():
    labels = data()["labels"]
    assert set(labels) == {"strong", "promising", "framework"}
    for key in labels:
        assert labels[key]["name"].strip() and labels[key]["definition"].strip(), key
    for m in moves():
        assert m["label"] in labels, m["id"]


def test_steps_three_or_four():
    for m in moves():
        assert 3 <= len(m["steps"]) <= 4, m["id"]
        assert all(isinstance(s, str) and s.strip() for s in m["steps"]), m["id"]


def test_examples_spread():
    subjects = []
    for m in moves():
        ex = m["example"]
        assert isinstance(ex["grade"], int) and 7 <= ex["grade"] <= 12, m["id"]
        assert ex["subject"].strip() and ex["text"].strip(), m["id"]
        subjects.append(ex["subject"])
    assert len(set(subjects)) >= 7
    assert max(subjects.count(s) for s in subjects) <= 2


def test_texts_present():
    for m in moves():
        for field in TEXT_FIELDS:
            assert isinstance(m[field], str) and m[field].strip(), (m["id"], field)
        for who in ("teacher_ai", "student_ai"):
            for part in ("card", "brief"):
                assert m[who][part].strip(), (m["id"], who, part)


def test_top_level_texts_present():
    d = data()
    assert d["eighty_twenty"].strip()
    assert d["classroom_note"].strip()
    assert d["age_rules_date"].strip()
    assert d["feels_harder"]["text"].strip()
    for s in d["feels_harder"]["sources"]:
        assert s["text"].strip() and s["url"].startswith("https://"), s


def test_every_source_https():
    for m in moves():
        assert m["sources"], m["id"]
        for s in m["sources"]:
            assert s["text"].strip() and s["url"].startswith("https://"), m["id"]


def test_toolkit_links_exist():
    for m in moves():
        assert m["toolkit"], m["id"]
        assert isinstance(m["related"], list), m["id"]
        for link in m["toolkit"] + m["related"]:
            assert link["text"].strip(), m["id"]
            assert (ROOT / link["href"].strip("/") / "index.html").exists(), (m["id"], link["href"])


def _related(move_id):
    m = next(m for m in moves() if m["id"] == move_id)
    return [r["href"] for r in m["related"]]


def test_test_yourself_links_retrieval_rhythm():
    assert "/retrieval-rhythm/" in _related("test-yourself")


def test_draw_it_links_study_codes():
    assert "/visual-codes/study/" in _related("draw-it")


def test_student_briefs_never_hand_over_answers():
    # Antimål i specen: AI:n får aldrig göra elevens arbete.
    for m in moves():
        brief = m["student_ai"]["brief"].lower()
        assert "give me the answer" not in brief, m["id"]
        assert "write my" not in brief, m["id"]


def test_age_rules_cover_four_tools():
    rules = data()["age_rules"]
    assert [r["tool"] for r in rules] == ["Copilot Chat", "Gemini for Education", "ChatGPT", "Claude"]
    for r in rules:
        assert r["rule"].strip(), r["tool"]


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
    # Inget fält får be om personuppgifter. Dragets eget namn ("name") och
    # forskningsnamnet ("research_name") är dragets, inte elevens, och
    # undantas; alla andra nycklar med "name" eller "email" är förbjudna.
    for m in moves():
        for key in _keys(m):
            assert "email" not in key.lower(), (m["id"], key)
            if key not in ("name", "research_name"):
                assert "name" not in key.lower(), (m["id"], key)
