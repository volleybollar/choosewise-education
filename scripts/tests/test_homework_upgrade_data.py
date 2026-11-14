"""Vakter för datafilen till Homework Upgrade (/homework-upgrade-1f0cd17c/).

Datafilen är sidans och promptbyggarens enda källa för text som varierar per
mönster. Ordning, etiketter och formuleringarna om AI är beslutade i specen
(docs/superpowers/specs/2026-11-14-homework-upgrade-design.md) — ändra dem inte
här utan att specen ändras först.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLUG = "homework-upgrade-1f0cd17c"
DATA_PATH = ROOT / SLUG / "upgrade-en.json"
COUNTDOWN_PATH = ROOT / "test-countdown/countdown-en.json"

# Läses en gång: filen ändras inte under en testkörning.
DATA = json.loads(DATA_PATH.read_text(encoding="utf-8"))
PATTERNS = DATA["patterns"]

ORDER = ["read-close-write", "answer-from-memory", "self-test-cards", "bring-back",
         "example-then-twin", "mixed-set", "explain-it", "ask-why", "draw-it",
         "plan-at-home", "fix-your-mistakes", "guess-first"]
GROUPS = ["reading", "facts", "problems", "concepts", "writing", "marked", "new-topic"]
# Etikett per mönsternummer (specens tabell).
LABELS = {1: "strong", 2: "strong", 3: "strong", 4: "strong", 5: "strong", 6: "promising",
          7: "promising", 8: "promising", 9: "promising", 10: "choosewise", 11: "strong",
          12: "promising"}


def all_strings(node):
    """Varje textsträng i JSON-trädet, på alla djup."""
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from all_strings(value)
    elif isinstance(node, list):
        for value in node:
            yield from all_strings(value)


def test_twelve_patterns_in_order():
    assert [p["id"] for p in PATTERNS] == ORDER
    assert [p["number"] for p in PATTERNS] == list(range(1, 13))


def test_groups_in_order_and_used():
    assert [g["id"] for g in DATA["groups"]] == GROUPS
    positions = []
    for p in PATTERNS:
        assert p["group"] in GROUPS, p["id"]
        positions.append(GROUPS.index(p["group"]))
    # Mönstren står grupperade i gruppernas ordning.
    assert positions == sorted(positions)


def test_labels_match_spec():
    assert set(DATA["labels"]) == {"strong", "promising", "choosewise"}
    for p in PATTERNS:
        assert p["label"] == LABELS[p["number"]], p["id"]


def test_every_pattern_complete():
    for p in PATTERNS:
        for key in ("name", "instead", "check", "why", "tip", "chatbot", "brief"):
            assert isinstance(p[key], str) and p[key].strip(), (p["id"], key)
        assert len(p["steps"]) == 3, p["id"]
        assert all(s.strip() for s in p["steps"]), p["id"]
        assert len(p["sources"]) >= 1, p["id"]


def test_sources_are_https():
    urls = [s["url"] for p in PATTERNS for s in p["sources"]]
    urls += [s["url"] for item in DATA["evidence"] for s in item["sources"]]
    assert urls
    for url in urls:
        assert url.startswith("https://"), url


def test_example_is_complete():
    ex = DATA["example"]
    assert ex["pattern"] in ORDER
    assert len(ex["homework"]) == 2
    assert len(ex["upgrade"]) == 6
    assert len(ex["ai_risk"]) == 2
    assert len(ex["check"]) == 3
    for item in ex["check"]:
        assert item["q"].strip() and item["a"].strip()


def test_check_and_students():
    assert len(DATA["check"]["steps"]) == 5
    assert len(DATA["students"]["text"]) == 4


def test_evidence_has_six_items_with_sources():
    assert len(DATA["evidence"]) == 6
    for item in DATA["evidence"]:
        assert item["title"].strip() and item["text"].strip()
        assert len(item["sources"]) >= 1, item["title"]


def test_age_rules_match_test_countdown():
    countdown = json.loads(COUNTDOWN_PATH.read_text(encoding="utf-8"))
    assert DATA["age_rules"] == countdown["age_rules"]
    assert DATA["age_rules_date"] == countdown["age_rules_date"]


def test_never_promises_ai_proof():
    """Sidan lovar aldrig läxor som tål AI. "AI-proof" får bara stå i meningen
    "No homework is AI-proof" (skiftlägeskänsligt)."""
    sentence = "No homework is AI-proof"
    for text in all_strings(DATA):
        start = text.find("AI-proof")
        while start != -1:
            begin = start - len("No homework is ")
            assert begin >= 0 and text[begin:start + len("AI-proof")] == sentence, text
            start = text.find("AI-proof", start + 1)
