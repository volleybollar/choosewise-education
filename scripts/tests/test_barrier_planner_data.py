"""Vakter för datafilen till Barrier Planner (/barrier-planner-1c25533d/).

Datafilen är sidans och Word-filernas enda källa för korten, exemplen, blanketten,
listan över populära men obelagda anpassningar, forskningen och varningarna. Texter
som specen kallar bindande (docs/superpowers/specs/2026-11-25-barrier-planner-design.md,
del B) prövas ordagrant här — ändra dem inte utan att specen ändras först.

Sidan skrivs på amerikansk engelska. Ordagranna citat ("pupils" hos EEF) och
källtitlar ("coloured", "behavioural") står kvar som de publicerades.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLUG = "barrier-planner-1c25533d"
DATA_PATH = ROOT / SLUG / "planner-en.json"
LADDER_PATH = ROOT / "quality-ladder-ec1c2f8c/ladder-en.json"

KEYS = {"labels", "hero", "how", "barriers_intro", "cards", "adapt", "record", "unsupported",
        "evidence", "care"}
CARD_IDS = ["getting-started", "multi-step", "reading-load", "writing", "attention", "changes",
            "not-alone", "language"]
BARRIERS = {
    "getting-started": "Doesn't get started on the task",
    "multi-step": "Loses track of instructions with several steps",
    "reading-load": "Reading a long text takes all their energy",
    "writing": "Starts written tasks but doesn't finish them",
    "attention": "Loses focus during independent work or in noise",
    "changes": "Finds changes and unstructured time hard",
    "not-alone": "Can do it with you, but not alone",
    "language": "Is still learning the language of instruction",
}
COMPASS = "/pedagogy-compass-59ecb8db/"
CARD_LINKS = {
    "getting-started": COMPASS + "#problem-dont-start",
    "multi-step": COMPASS + "#problem-overload",
    "reading-load": "#bp-adapt",
    "writing": "/quality-ladder-ec1c2f8c/",
    "attention": None,
    "changes": None,
    "not-alone": COMPASS + "#problem-not-alone",
    "language": "#bp-adapt",
}
OUR_SUGGESTION = "(our suggestion, not a research finding)"
UNSUPPORTED_IN_MOVES = ["overlay", "dyslexia font", "fidget", "extra time", "easier worksheet",
                        "less work"]
WARNING = ("This form never goes through AI. Fill it in by hand or in your school's system "
           "for records.")
COUNTRY_LINE = ("Rules differ between countries. Check what applies where you work before you "
                "decide, record or share support for a student.")
UNSUPPORTED_TITLES = ["Colored overlays and tinted lenses", "Dyslexia fonts",
                      "Fidget spinners as an attention aid", "Extra time as a classroom support",
                      "Less work as the default accommodation",
                      "Matching teaching to a diagnosis category"]
# Etikett per forskningspunkt, i specens ordning (avsnitt B9).
EVIDENCE_LABELS = ["framework", "strong", "promising", "promising", "promising", "strong",
                   "promising", "promising", "framework"]
CARE_KEYWORDS = ["identifiable", "unsupported", "never go away", "definitions", "whole story"]
# Brittisk stavning som inte får stå på sidan (utom i citat och källtitlar).
BRITISH = re.compile(r"\b(behaviour\w*|colour\w*|programme|practis\w*|organis\w*|recognis\w*"
                     r"|labelled|centre|pupils?|maths)\b", re.IGNORECASE)
QUOTED = re.compile(r'"[^"]*"|“[^”]*”')
BANNED = ["leverage", "empower", "game-changer", "seamless", "unlock", "cutting-edge",
          "ai-proof", "low effect", "doesn't work", "does not work", "!"]


def data():
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def all_strings(node, skip_sources=False):
    """Varje textsträng i JSON-trädet, på alla djup. Med skip_sources hoppas
    källornas titlar över (de står som de publicerades)."""
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for key, value in node.items():
            if skip_sources and key == "sources":
                continue
            yield from all_strings(value, skip_sources)
    elif isinstance(node, list):
        for value in node:
            yield from all_strings(value, skip_sources)


def card(cid):
    return next(c for c in data()["cards"] if c["id"] == cid)


def card_text(c):
    return " ".join(all_strings(c, skip_sources=True))


def test_top_level_keys():
    assert set(data()) == KEYS


def test_labels_match_quality_ladder():
    ladder = json.loads(LADDER_PATH.read_text(encoding="utf-8"))
    assert data()["labels"] == ladder["labels"]


def test_card_ids_and_barriers():
    cards = data()["cards"]
    assert [c["id"] for c in cards] == CARD_IDS
    for c in cards:
        assert c["barrier"] == BARRIERS[c["id"]], c["id"]


def test_card_shape():
    for c in data()["cards"]:
        assert 2 <= len(c["signs"]) <= 3, c["id"]
        assert 2 <= len(c["whole_class"]) <= 3, c["id"]
        assert 1 <= len(c["targeted"]) <= 2, c["id"]
        for move in c["whole_class"] + c["targeted"]:
            assert move["short"].strip(), c["id"]
            assert len(move["short"]) <= 140, (c["id"], move["short"])
            assert "(" not in move["short"], (c["id"], move["short"])
            assert move["label"] in (None, "strong", "promising", "framework", "choosewise")
        assert c["review"].startswith("Do they") and c["review"].endswith("?"), c["id"]
        assert c["label"] == "framework", c["id"]
        assert c["sources"], c["id"]
        assert all(s["url"].startswith("https://") for s in c["sources"]), c["id"]


def test_card_links():
    for c in data()["cards"]:
        href = c["link"]["href"] if c["link"] else None
        assert href == CARD_LINKS[c["id"]], c["id"]


def test_card_numbers():
    assert "0.51" in card_text(card("getting-started"))
    reading = card_text(card("reading-load"))
    assert "0.39" in reading and "0.35" in reading
    assert "8 months" in card_text(card("not-alone"))
    assert "60" in " ".join(card("attention")["not_this"])


def test_not_this():
    def nt(cid):
        return " ".join(card(cid)["not_this"]).lower()
    assert "less work" in nt("getting-started")
    assert "less work" in nt("writing")
    assert "overlays" in nt("reading-load") and "dyslexia fonts" in nt("reading-load")
    assert "fidget spinners" in nt("attention")
    assert "stripping" in nt("language")


def test_no_unsupported_recommendation():
    for c in data()["cards"]:
        for move in c["whole_class"] + c["targeted"]:
            for text in (move["text"].lower(), move["short"].lower()):
                for term in UNSUPPORTED_IN_MOVES:
                    assert term not in text, (c["id"], term)


def test_our_suggestion_marked():
    for cid in ("getting-started", "writing"):
        assert any(OUR_SUGGESTION in m["text"] for m in card(cid)["targeted"]), cid
    assert any("we have found no study" in m["text"].lower() for m in card("attention")["targeted"])


def test_binding_texts():
    d = data()
    assert d["record"]["warning"] == WARNING
    assert d["record"]["header"] == ["Student or class", "Date", "Who took part"]
    assert d["record"]["country_line"] == COUNTRY_LINE
    assert d["barriers_intro"]["privacy"] == "Describe the task and the barrier, never the student."
    assert d["adapt"]["check"] == ("Check every definition and bracketed explanation; this is "
                                   "where errors slip in.")


def test_binding_intent_texts():
    d = data()
    assert len(d["how"]) == 3
    assert "not who it happens to" in d["how"][0]
    # Specen B3 skriver "whole-class moves"; planen sa "whole class" (regel i liggaren).
    assert "whole-class" in d["how"][1]
    assert "take away" in d["how"][2] and "date" in d["how"][2]
    assert "Two students with the same diagnosis" in d["barriers_intro"]["diagnosis"]


def test_hero():
    hero = data()["hero"]
    assert hero["title"] == "What a plan looks like"
    assert [r["term"] for r in hero["rows"]] == ["The barrier", "For the whole class", "Targeted",
                                                 "Review in three weeks"]


def test_record_shape():
    rec = data()["record"]
    assert rec["measure_columns"] == ["What we do", "Who does it", "From when", "What we look for"]
    assert rec["outcomes"] == ["Keep", "Change", "Stop"]
    assert rec["outcome_rows"] == ["Measure 1", "Measure 2", "Measure 3"]
    assert len(rec["review_questions"]) == 5
    assert len(rec["eef_questions"]) == 3
    assert [b["kind"] for b in rec["blocks"]] == ["box", "box", "measures", "line", "outcomes"]
    fields = rec["header"] + [b["heading"] for b in rec["blocks"]] + rec["measure_columns"]
    for field in fields:
        for word in ("diagnos", "medical", "health"):
            assert word not in field.lower(), field


def test_unsupported():
    u = data()["unsupported"]
    assert [i["title"] for i in u["items"]] == UNSUPPORTED_TITLES
    for item in u["items"]:
        assert item["research"].strip() and item["instead"].strip()
        assert not item["instead"].lower().startswith("instead")
    assert "open question" in u["movement_note"]


def test_evidence():
    ev = data()["evidence"]
    assert ev["lede"].strip()
    items = ev["items"]
    assert [i["label"] for i in items] == EVIDENCE_LABELS
    assert ("less helpful for teaching and learning than determining the pupils' educational needs"
            in items[0]["text"])
    assert "8 months" in items[1]["text"] and "0.51" in items[1]["text"]
    assert "0.35" in items[2]["text"]
    assert "0.39" in items[5]["text"]
    for item in items:
        assert item["sources"], item["title"]
        assert all(s["url"].startswith("https://") for s in item["sources"]), item["title"]


def test_care():
    care = data()["care"]
    assert len(care) == 5
    for item, keyword in zip(care, CARE_KEYWORDS):
        assert keyword in item["risk"].lower(), (item["risk"], keyword)


def test_american_spelling():
    for s in all_strings(data(), skip_sources=True):
        hits = BRITISH.findall(QUOTED.sub("", s))
        assert not hits, (hits, s)


def test_banned_words():
    for s in all_strings(data()):
        for word in BANNED:
            assert word not in s.lower(), (word, s)
