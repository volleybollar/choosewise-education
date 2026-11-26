"""Vakter för datafilen till Ideas first (/ideas-first-778ba230/).

Datafilen är sidans och teambladets enda källa för exemplet, de fyra stegen,
kontrollerna och följdprompten, teamrutinen, forskningen, varningarna och länkarna.
Texter som specen kallar bindande (docs/superpowers/specs/2026-11-26-ideas-first-design.md,
del B) prövas ordagrant här — ändra dem inte utan att specen ändras först.

Siffrorna kommer från kurslektion 11 (~/Projekt/Choosewise/skool/skool-setup.md §7.8)
och forskningsfilen 2026-11-14-teacher-tasks-evidence.md §7.

Sidan skrivs på amerikansk engelska (lektion 11 har "defence", sidan "defense").
Ordagranna citat och källtitlar står kvar som de publicerades.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLUG = "ideas-first-778ba230"
DATA_PATH = ROOT / SLUG / "ideas-en.json"
LADDER_PATH = ROOT / "quality-ladder-ec1c2f8c/ladder-en.json"

KEYS = {"labels", "hero", "how", "choose", "team", "evidence", "care", "next"}
OUR_SUGGESTION = "our suggestion, not a research finding"
# Påståendet om lärare är alltid avgränsat till studierna om idéer: EEF-försöket
# i forskningsdelen är gjort med lärare, men mätte tid, inte variation.
NOT_TEACHERS = "None of the studies on ideas is of teachers planning lessons"
CHECKS = [
    "Are the eight really different, or one activity in eight wordings? Ask again for the kind "
    "that is missing.",
    "Does the idea you chose serve the goal, and is the subject content right?",
    "What did you change? If you cannot say, you took the AI's idea, not your own.",
]
FOLLOW_UP = ("Several of these are the same kind of activity. Give me four more, each of a kind "
             "that is missing from the list above, not a new version of one already there. "
             "Same rules: one or two sentences each, the format in brackets, no ranking.")
SOURCE_URLS = {
    "https://doi.org/10.1126/sciadv.adn5290",
    "https://doi.org/10.48550/arXiv.2505.17241",
    "https://doi.org/10.1145/3635636.3656204",
    "https://doi.org/10.1145/3613904.3642919",
    "https://scale.stanford.edu/ai/repository/chatgpt-lesson-preparation-teacher-choices-trial-"
    "evaluation-report",
}
NEXT_HREFS = ["/what-teachers-do-354716b7/", "/pedagogy-compass-59ecb8db/",
              "/unit-studio-541ebd12/", "/prompts/teachers/", "/free/prompts/",
              "https://www.skool.com/choosewise-7103"]
CARE_KEYWORDS = ["eight wordings", "subject content", "first idea", "department", "identifiable"]
# Brittisk stavning som inte får stå på sidan (utom i citat och källtitlar).
BRITISH = re.compile(r"\b(behaviour\w*|colour\w*|programme|practis\w*|organis\w*|recognis\w*"
                     r"|labelled|centre|pupils?|maths|defence)\b", re.IGNORECASE)
# Brittiska ord som inte är stavning men ändå ska hållas utanför (utom i citat och källtitlar).
BRITISH_WORDS = ["primary school", "attainers", "tick off"]
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


def test_top_level_keys():
    assert set(data()) == KEYS


def test_labels_match_quality_ladder():
    ladder = json.loads(LADDER_PATH.read_text(encoding="utf-8"))
    assert data()["labels"] == ladder["labels"]


def test_hero():
    hero = data()["hero"]
    assert hero["title"] == "What it looks like"
    assert [r["term"] for r in hero["rows"]] == [
        "Goal", "Your ideas first", "From the AI, three of the eight", "Your choice and change"]
    texts = " ".join(r["text"] for r in hero["rows"]).lower()
    for phrase in ["towns grew up beside rivers", "a map of local rivers and towns", "role-play",
                   "card sort", "defense", "two hundred years apart", "your own town"]:
        assert phrase in texts, phrase
    assert "our example" in hero["note"].lower()
    assert "Grade 8 geography" in hero["note"]
    assert hero["closing"] == ("The AI widened the options; the choice and the local maps "
                               "are yours.")


def test_how():
    how = data()["how"]
    steps = how["steps"]
    assert len(steps) == 4
    assert "two or three" in steps[0] and "before you ask" in steps[0]
    for word in ["format", "context", "challenge", "the best idea"]:
        assert word in steps[1], word
    assert "change" in steps[2]
    assert "team" in steps[3] and "before anyone uses AI" in steps[3]
    assert how["label"] == "framework"
    assert how["note"] == ("The four steps are our reading of the studies below. "
                           + NOT_TEACHERS + ".")


def test_choose():
    choose = data()["choose"]
    assert "without AI" in choose["intro"]
    assert choose["checks"] == CHECKS
    assert choose["follow_up"] == FOLLOW_UP
    ways = [w.lower() for w in choose["ways"]]
    assert len(ways) == 3
    for way, word in zip(ways, ["local", "combine", "challenge"]):
        assert word in way, (word, way)
    assert choose["ways_note"] == "(" + OUR_SUGGESTION + ")"


def test_team():
    team = data()["team"]
    assert "same AI lesson" in team["intro"]
    routine = team["routine"]
    assert len(routine) == 5
    assert "alone" in routine[1] and "before anyone uses AI" in routine[1]
    assert "Our team" in routine[3]
    assert OUR_SUGGESTION in team["routine_note"]


def test_team_sheet():
    sheet = data()["team"]["sheet"]
    assert sheet["title"] == "Ideas first: team sheet"
    assert sheet["header"] == ["Subject", "Grade", "Goal", "Date"]
    assert sheet["note"] == "Only the ideas go into AI, never the names on this sheet."
    assert sheet["routine_heading"].strip()
    assert len(sheet["routine"]) == 5
    for line in sheet["routine"]:
        assert len(line) <= 80, line
    assert sheet["before_ai"]["heading"] == "Ideas before AI"
    assert sheet["before_ai"]["columns"] == ["Who", "Ideas"]
    assert sheet["before_ai"]["rows"] >= 6
    assert sheet["from_ai"]["heading"] == "From the AI: worth a closer look"
    assert sheet["from_ai"]["hint"].strip()
    assert sheet["chose"]["heading"] == "What we chose and changed"
    assert sheet["chose"]["columns"] == ["Who", "Chose", "Changed"]
    assert sheet["chose"]["rows"] >= 3


def test_evidence():
    ev = data()["evidence"]
    assert NOT_TEACHERS in ev["lede"]
    assert "measured time, not variety" in ev["lede"]
    assert ev["label"] == "promising"
    items = ev["items"]
    assert [i["label"] for i in items] == [None, None, None, None, None, "framework"]
    for item in items:
        assert item["title"].strip() and item["text"].strip()
    for phrase in ["less creative writers", "more similar"]:
        assert phrase in items[0]["text"], phrase
    for phrase in ["28 studies", "8,214", "(0.27, a small effect)", "(−0.86, a large drop)",
                   "−0.05", "preprint"]:
        assert phrase in items[1]["text"], phrase
    for phrase in ["36 participants", "felt less responsible for the ideas they generated"]:
        assert phrase in items[2]["text"], phrase
    for phrase in ["60 participants", "fixation"]:
        assert phrase in items[3]["text"], phrase
    for phrase in ["56.2", "81.5", "31%", "did not appear to be affected"]:
        assert phrase in items[4]["text"], phrase
    # Storleken på EEF-försöket kommer från en sammanfattning: står den med ska det synas.
    if "259" in items[4]["text"]:
        assert "summary" in items[4]["text"]
    urls = {s["url"] for i in items for s in i["sources"]}
    assert urls == SOURCE_URLS
    for item in items:
        for source in item["sources"]:
            assert source["text"].strip() and source["url"].startswith("https://")


def test_care():
    care = data()["care"]
    assert len(care) == 5
    for item, word in zip(care, CARE_KEYWORDS):
        assert word in item["risk"].lower(), (word, item["risk"])
        assert item["what_we_do"].strip()


def test_next():
    items = data()["next"]
    assert [i["href"] for i in items] == NEXT_HREFS
    prompts = items[3]["text"]
    assert "25" in prompts and "36" in prompts
    for item in items:
        assert item["text"].strip()


def test_american_spelling():
    for s in all_strings(data(), skip_sources=True):
        hits = BRITISH.findall(QUOTED.sub("", s))
        assert not hits, (hits, s)


def test_british_vocabulary():
    for s in all_strings(data(), skip_sources=True):
        text = QUOTED.sub("", s).lower()
        for word in BRITISH_WORDS:
            assert word not in text, (word, s)


def test_banned_words():
    for s in all_strings(data()):
        for word in BANNED:
            assert word not in s.lower(), (word, s)
