"""Vakter för datafilen till Lesson Lens (/lesson-lens/).

Datafilen är sidans, promptbyggarens och PDF:ens enda källa. Ordning,
etiketter och Formative check som start är beslutade av Johan 2026-10-29 —
ändra dem inte här utan att specen ändras först.
Spec: docs/superpowers/specs/2026-10-29-lesson-lens-design.md.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "lesson-lens/lenses-en.json"
TM_DATA = ROOT / "thinking-moves/moves-en.json"

ORDER = ["retrieval-practice", "spacing", "cognitive-load", "dual-coding", "formative-check",
         "feedback", "explicit-instruction", "metacognition", "dialogic-discussion",
         "belonging", "thinking-depth", "trade-off"]
LABELS = {"retrieval-practice": "strong", "spacing": "strong", "cognitive-load": "strong",
          "dual-coding": "promising", "formative-check": "strong", "feedback": "strong",
          "explicit-instruction": "strong", "metacognition": "strong",
          "dialogic-discussion": "promising", "belonging": "promising",
          "thinking-depth": "framework", "trade-off": "choosewise"}
# Första länken till Evidence Toolkit per lins (specens tabell). Dual coding och
# thinking depth väljer byggaren själv, men länken måste finnas.
TOOLKIT = {"retrieval-practice": "/evidence/memory/", "spacing": "/evidence/memory/",
           "cognitive-load": "/evidence/explicit-instruction/",
           "formative-check": "/evidence/feedback/",
           "feedback": "/evidence/feedback/", "explicit-instruction": "/evidence/explicit-instruction/",
           "metacognition": "/evidence/self-regulated-learning/",
           "dialogic-discussion": "/evidence/questioning-discussion/",
           "belonging": "/evidence/wellbeing-motivation-agency/"}
MATHS_SCIENCE = {"Maths", "Physics", "Chemistry", "Biology", "Science"}


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def lenses():
    return data()["lenses"]


def test_lenses_in_agreed_order():
    assert [l["id"] for l in lenses()] == ORDER
    assert [l["number"] for l in lenses()] == list(range(1, 13))


def test_default_lens_is_formative_check():
    assert data()["default_lens"] == "formative-check"


def test_labels_match_spec():
    assert {l["id"]: l["label"] for l in lenses()} == LABELS


def test_four_labels_defined():
    labels = data()["labels"]
    assert set(labels) == {"strong", "promising", "framework", "choosewise"}
    for key in labels:
        assert labels[key]["name"] and labels[key]["definition"]
    assert labels["choosewise"]["definition"] == "Choosewise's own question, not a research finding."


def test_choosewise_label_only_on_trade_off():
    assert [l["id"] for l in lenses() if l["label"] == "choosewise"] == ["trade-off"]


def test_toolkit_links_exist():
    for l in lenses():
        assert l["toolkit"], l["id"]
        for link in l["toolkit"]:
            assert link["text"], l["id"]
            assert (ROOT / link["href"].strip("/") / "index.html").exists(), link["href"]
        if l["id"] in TOOLKIT:
            assert l["toolkit"][0]["href"] == TOOLKIT[l["id"]], l["id"]
    trade = next(l for l in lenses() if l["id"] == "trade-off")
    assert [t["href"] for t in trade["toolkit"]] == ["/evidence/ai-learning-science/", "/wise/"]


def test_complete_example_per_lens():
    for l in lenses():
        ex = l["example"]
        assert ex["subject"], l["id"]
        assert 6 <= ex["grade"] <= 12, l["id"]
        assert 4 <= len(ex["lesson"]) <= 6, l["id"]
        assert all(line.strip() for line in ex["lesson"]), l["id"]
        assert 1 <= len(ex["upgrade"]) <= 2, l["id"]
        for field in ("keep", "nudge", "check"):
            assert ex[field].strip(), (l["id"], field)
        assert ex["nudge"] == "None" or ex["nudge"].rstrip().endswith("?"), l["id"]


def test_subjects_spread():
    subjects = [l["example"]["subject"] for l in lenses()]
    assert len(set(subjects)) >= 8
    assert max(subjects.count(s) for s in subjects) <= 2
    assert sum(s in MATHS_SCIENCE for s in subjects) <= 6
    assert len({l["example"]["grade"] for l in lenses()}) >= 5


def test_trade_off_brief_covers_lessons_without_ai():
    brief = next(l for l in lenses() if l["id"] == "trade-off")["prompt_brief"]
    assert "hand over to AI" in brief
    assert "even if the lesson has no AI" in brief


def test_every_lens_has_brief_and_evidence():
    for l in lenses():
        assert l["name"] and l["one_liner"] and l["prompt_brief"] and l["evidence"], l["id"]


def test_every_source_has_https_url():
    for l in lenses():
        for s in l["sources"]:
            assert s["text"] and s["url"].startswith("https://"), l["id"]


def test_research_lenses_have_sources():
    for l in lenses():
        if l["label"] != "choosewise":
            assert l["sources"], l["id"]


def test_age_rules_match_thinking_moves():
    tm = json.loads(TM_DATA.read_text(encoding="utf-8"))
    assert data()["age_rules"] == tm["age_rules"]
