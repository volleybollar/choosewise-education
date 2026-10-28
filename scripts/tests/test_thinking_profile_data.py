"""Vakter för datafilen till Thinking Profile (thinking-profile/ladders-en.json).

Filen är enda källan för sidan, planeringsprompten och båda PDF:erna.
Klustrens id, namn och beskrivningar läses från thinking-moves/moves-en.json
och partyperna från side-by-side/pairs-en.json; de kopieras inte hit.
Spec: docs/superpowers/specs/2026-10-28-thinking-profile-design.md.
"""
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "thinking-profile/ladders-en.json"
MOVES = ROOT / "thinking-moves/moves-en.json"
PAIRS = ROOT / "side-by-side/pairs-en.json"

TOOLS = {"thinking-moves", "flawed-answer", "side-by-side"}
CAUSES_STEPS = [
    "I name one cause and one effect.",
    "I build a chain: A leads to B leads to C.",
    "I find a loop: C affects A again, or a delay or a side effect.",
    "I use the loop to predict what happens if one part changes, and say how sure I am.",
]
NOT_GRADED = "The ladder is for students' own self-check. It is never graded."
HONESTY = ("The ladders are Choosewise's own, built on the logic of the SOLO taxonomy. "
           "They have not been tested in research.")
REGULATING_RULE = ("Students rate the ladder on the Think back part at the end of each task, "
                   "not on the task answer.")
QUESTIONS = ["Which step did my answer reach?", "What in my answer shows it?", "My next step"]


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def moves():
    return json.loads(MOVES.read_text(encoding="utf-8"))


def pairs():
    return json.loads(PAIRS.read_text(encoding="utf-8"))


def _evidence_empty():
    # Evidensen fylls i Task 2; till dess hoppas de vakterna över.
    try:
        return not data()["evidence"]
    except (OSError, KeyError, ValueError):
        return False


needs_evidence = pytest.mark.skipif(_evidence_empty(), reason="evidence fylls i Task 2")


def test_six_ladders_in_cluster_order():
    ids = [ladder["cluster"] for ladder in data()["ladders"]]
    assert ids == [c["id"] for c in moves()["clusters"]]


def test_four_nonempty_steps_with_shows():
    for ladder in data()["ladders"]:
        assert ladder["in_class"].strip(), ladder["cluster"]
        assert len(ladder["steps"]) == 4, ladder["cluster"]
        for step in ladder["steps"]:
            assert step["text"].strip() and step["shows"].strip(), (ladder["cluster"], step)
            # Elevspråk i första person (spec: "I name one cause …").
            assert step["text"].startswith("I "), (ladder["cluster"], step["text"])


def test_causes_steps_match_spec():
    causes = next(lad for lad in data()["ladders"] if lad["cluster"] == "causes")
    assert [s["text"] for s in causes["steps"]] == CAUSES_STEPS


def test_task_refs_exist():
    move_ids = {m["id"] for m in moves()["moves"]}
    pair_ids = {p["id"] for p in pairs()["pairs"]}
    for ladder in data()["ladders"]:
        assert ladder["tasks"], ladder["cluster"]
        for task in ladder["tasks"]:
            assert task["tool"] in TOOLS, task
            if task["tool"] == "thinking-moves":
                assert task["id"] in move_ids, task
            elif task["tool"] == "side-by-side" and "id" in task:
                assert task["id"] in pair_ids, task
            elif task["tool"] == "flawed-answer":
                assert "id" not in task, task


def test_every_move_is_preferred_somewhere():
    # Varje drag hör till exakt sitt eget klusters trappa (spec-tabellen),
    # och Flawed Answer/Side by Side till Evaluating/Comparing.
    ladders = data()["ladders"]
    for move in moves()["moves"]:
        holders = [lad["cluster"] for lad in ladders
                   if {"tool": "thinking-moves", "id": move["id"]} in lad["tasks"]]
        assert holders == [move["cluster"]], (move["id"], holders)
    for tool, cluster in (("flawed-answer", "evaluating"), ("side-by-side", "comparing")):
        holders = [lad["cluster"] for lad in ladders
                   if any(t["tool"] == tool for t in lad["tasks"])]
        assert holders == [cluster], (tool, holders)


def test_icons_exist():
    for ladder in data()["ladders"]:
        icon = ladder["icon"]
        assert icon.startswith("/thinking-moves/icons/") and icon.endswith(".svg"), icon
        assert (ROOT / icon.lstrip("/")).is_file(), icon


def test_fixed_sentences():
    d = data()
    assert d["not_graded"] == NOT_GRADED
    assert d["honesty"] == HONESTY
    assert d["regulating_rule"] == REGULATING_RULE
    assert d["self_check"]["questions"] == QUESTIONS


def test_intro_and_rules_filled():
    d = data()
    for key in ("what", "why_unit", "retell"):
        assert d["intro"][key].strip(), key
    assert d["rules"] and all(r.strip() for r in d["rules"])


@needs_evidence
def test_labels_used_are_defined():
    used = {e["label"] for e in data()["evidence"]}
    assert used <= set(moves()["labels"]) - {"note"}


@needs_evidence
def test_every_source_has_https_url():
    sources = [s for e in data()["evidence"] for s in e["sources"]]
    assert sources
    for s in sources:
        assert s["text"].strip() and s["url"].startswith("https://"), s


# --- Genomarbetat exempel och evidens (Task 2) ---

# Fälten i de riktiga byggarna (thinking-moves/index.html, side-by-side/index.html),
# utan "(optional)". Exemplets inputs skrivs "Fält: värde".
BUILDER_FIELDS = {
    "thinking-moves": {"Thinking move", "Subject", "Grade", "What is the lesson about?",
                       "What do students already know?"},
    "side-by-side": {"Pair type", "How hard should the difference be to see?", "Subject",
                     "Grade", "What is the lesson about?", "What do students already know?"},
}
BUILDER_GRADES = {"thinking-moves": {"8", "9", "10", "11", "12"},
                  "side-by-side": {"7", "8", "9", "10", "11", "12"}}
URL_PARAM = {"thinking-moves": "move", "flawed-answer": "flaw", "side-by-side": "pair"}


def builder_url(tool, task_id):
    # Samma härledning som i Task 1: /<verktyg>/?<param>=<id>.
    return "/{}/?{}={}".format(tool, URL_PARAM[tool], task_id)


def _causes_tasks():
    causes = next(lad for lad in data()["ladders"] if lad["cluster"] == "causes")
    return causes["tasks"]


def test_example_obeys_task_rules():
    ex = data()["example"]
    assert (ex["subject"], ex["grade"], ex["weeks"], ex["topic"], ex["cluster"]) == (
        "Biology", 8, 6, "Ecosystems", "causes")
    assert ex["thread"].strip() and ex["tell_students"].strip()
    plan = ex["plan"]
    assert 4 <= len(plan) <= 6
    weeks = [p["week"] for p in plan]
    assert weeks == sorted(weeks) and all(1 <= w <= ex["weeks"] for w in weeks)
    causes = _causes_tasks()
    from_causes = [p for p in plan if {"tool": p["tool"], "id": p["task"]} in causes]
    assert 2 * len(from_causes) >= len(plan)
    by_week = {p["week"]: (p["tool"], p["task"]) for p in plan}
    assert by_week.get(2) == ("thinking-moves", "map-the-loop")
    assert by_week.get(4) == ("thinking-moves", "best-explanation")
    assert by_week.get(5) == ("side-by-side", "one-change")
    steps = [p["step"] for p in plan]
    assert all(s in (1, 2, 3, 4) for s in steps)
    assert steps == sorted(steps) and steps[-1] == 4
    for p in plan:
        assert p["what"].strip(), p
        assert p["url"] == builder_url(p["tool"], p["task"]), p


def test_example_inputs_fit_builder():
    move_names = {m["id"]: m["name"] for m in moves()["moves"]}
    pair_names = {p["id"]: p["name"] for p in pairs()["pairs"]}
    level_names = {lv["name"] for lv in pairs()["levels"]}
    ex = data()["example"]
    for p in ex["plan"]:
        fields = dict(i.split(": ", 1) for i in p["inputs"])
        assert set(fields) <= BUILDER_FIELDS[p["tool"]], p["inputs"]
        assert fields["Subject"] == ex["subject"]
        assert fields["Grade"] == str(ex["grade"]) in BUILDER_GRADES[p["tool"]]
        assert fields["What is the lesson about?"].strip()
        assert len(fields["What is the lesson about?"]) <= 400
        if p["tool"] == "thinking-moves":
            assert fields["Thinking move"] == move_names[p["task"]], p
        else:
            assert fields["Pair type"] == pair_names[p["task"]], p
            assert fields["How hard should the difference be to see?"] in level_names


def test_example_students_differ_in_step():
    ex = data()["example"]
    students = ex["students"]
    assert len(students) == 2
    assert ex["students_note"].startswith("Fictional examples")
    plan_tasks = {p["task"] for p in ex["plan"]}
    for s in students:
        for key in ("name", "answer", "shows", "next"):
            assert s[key].strip(), (s["name"], key)
        assert s["task"] in plan_tasks, s["task"]
        assert s["step"] in (1, 2, 3, 4)
    assert students[0]["name"] != students[1]["name"]
    assert students[0]["step"] != students[1]["step"]


def test_evidence_has_ladder_framework_entry():
    entries = [e for e in data()["evidence"] if e["label"] == "framework"]
    assert len(entries) == 1
    assert HONESTY in entries[0]["text"]


def test_no_solo_as_evidence():
    # SOLO är grunden för trapporna, inte bevis för att de fungerar.
    evidence = data()["evidence"]
    assert evidence
    for e in evidence:
        if e["label"] in ("strong", "promising"):
            blob = e["text"] + " ".join(s["text"] for s in e["sources"])
            assert "Biggs" not in blob and "SOLO" not in blob, e["claim"]
