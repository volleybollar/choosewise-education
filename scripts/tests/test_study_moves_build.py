"""Vakter för sidan Study Moves (/study-moves/) och dess byggskript.

Målrutorna, de tio dragkorten, etikettförklaringen, källorna och
åldersreglerna byggs från study-moves/moves-en.json av
scripts/build-study-moves.py, så att de syns utan JavaScript och kan
indexeras. Testerna läser den byggda sidan och kör byggskriptet.
Spec: docs/superpowers/specs/2026-11-12-study-moves-design.md.
"""
import importlib.util
import json
import re
import shutil
from html import escape
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "study-moves/index.html"
DATA = ROOT / "study-moves/moves-en.json"
BUILD = ROOT / "scripts/build-study-moves.py"

SECTIONS = ["sm-goals", "sm-feels", "sm-moves", "sm-builder", "sm-evidence", "sm-age", "sm-download"]


def html():
    return PAGE.read_text(encoding="utf-8")


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def load_build():
    spec = importlib.util.spec_from_file_location("build_study_moves", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def section(section_id, page=None):
    m = re.search(rf'<section[^>]*id="{section_id}".*?</section>', page or html(), re.S)
    assert m, section_id
    return m.group(0)


def cards(page=None):
    return re.findall(r'<article class="tm-move sm-move"[^>]*>.*?</article>', page or html(), re.S)


def fake_move(**over):
    move = {"id": "x", "number": 1, "name": "A <b>&</b>", "research_name": "R <i>", "goals": ["g"],
            "one_liner": "Q & A", "feels": "f", "label": "strong", "steps": ["<s>1</s>", "2", "3"],
            "example": {"subject": "S", "grade": 9, "text": "<em>t</em>"},
            "teacher_ai": {"card": "tc", "brief": "tb"}, "student_ai": {"card": "sc", "brief": "sb"},
            "watch_out": "w", "evidence": "e", "sources": [{"text": "s", "url": "https://x"}],
            "toolkit": [{"href": "/evidence/", "text": "t"}], "related": []}
    move.update(over)
    return move


FAKE_DATA = {"labels": {"strong": {"name": "Strong", "definition": "d"}},
             "goals": [{"id": "g", "name": "Goal <g>", "description": "d", "moves": ["x"]}]}


def test_card_escapes_text():
    out = load_build().render_move_card(fake_move(), FAKE_DATA)
    assert "&lt;b&gt;" in out and "<b>" not in out
    for raw in ("<i>", "<s>1</s>", "<em>t</em>", "<g>"):
        assert raw not in out, raw


def test_card_has_all_parts():
    d = data()
    page_cards = cards()
    assert len(page_cards) == len(d["moves"])
    for move, card in zip(d["moves"], page_cards):
        expected = [move["name"], move["research_name"], move["one_liner"], move["example"]["text"],
                    move["feels"], move["teacher_ai"]["card"], move["student_ai"]["card"],
                    move["watch_out"], move["evidence"], *move["steps"]]
        for text in expected:
            assert escape(text) in card, (move["id"], text)
        for s in move["sources"]:
            assert escape(s["url"]) in card, (move["id"], s["url"])
        for link in move["toolkit"] + move["related"]:
            assert f'href="{escape(link["href"])}"' in card, (move["id"], link["href"])
        for who in ("teacher", "student"):
            assert f'href="?move={move["id"]}&amp;for={who}#sm-builder"' in card, (move["id"], who)
            assert f'data-use-move="{move["id"]}" data-use-for="{who}"' in card, (move["id"], who)
        assert ">Teacher: prepare it with AI<" in card and ">Student: study with AI (13+)<" in card


def test_card_shows_label_and_goals():
    d = data()
    goal_names = {g["id"]: g["name"] for g in d["goals"]}
    for move, card in zip(d["moves"], cards()):
        name = d["labels"][move["label"]]["name"]
        assert f'class="tm-chip tm-chip--{move["label"]}">{name}<' in card, move["id"]
        assert f'<span class="tm-move__num">Move {move["number"]}</span>' in card, move["id"]
        for g in move["goals"]:
            assert escape(goal_names[g]) in card, (move["id"], g)


def test_card_links_sit_after_details():
    # Länkarna står längst ned i kortet, utanför den hopfällda delen.
    for card in cards():
        assert card.index("</details>") < card.index('<div class="sm-move__use">')


def test_goals_link_to_cards():
    d = data()
    card_ids = set(re.findall(r'<article class="tm-move sm-move" id="([^"]+)"', html()))
    hrefs = re.findall(r'href="#([^"]+)"', load_build().render_goals(d))
    assert hrefs
    for target in hrefs:
        assert target in card_ids, target


def test_goals_show_start_and_eighty_twenty():
    goals = section("sm-goals")
    assert 'id="sm-start"' in goals and "Not sure? Start here." in goals
    assert escape(data()["eighty_twenty"]) in goals


def test_build_is_idempotent(tmp_path):
    (tmp_path / "study-moves").mkdir()
    shutil.copy(PAGE, tmp_path / "study-moves/index.html")
    shutil.copy(DATA, tmp_path / "study-moves/moves-en.json")
    mod = load_build()
    mod.build(tmp_path)
    first = (tmp_path / "study-moves/index.html").read_bytes()
    mod.build(tmp_path)
    assert (tmp_path / "study-moves/index.html").read_bytes() == first


def test_page_is_built_from_current_json(tmp_path):
    # Den incheckade sidan ska vara byggd från den incheckade JSON-filen.
    (tmp_path / "study-moves").mkdir()
    shutil.copy(PAGE, tmp_path / "study-moves/index.html")
    shutil.copy(DATA, tmp_path / "study-moves/moves-en.json")
    load_build().build(tmp_path)
    assert (tmp_path / "study-moves/index.html").read_text(encoding="utf-8") == html()


def test_page_has_ten_cards():
    page = html()
    assert page.count('<article class="tm-move sm-move"') == 10
    assert len(re.findall(r'<li class="sm-goal">', section("sm-goals"))) == 6
    ids = re.findall(r'<article class="tm-move sm-move" id="([^"]+)" data-move-id="\1"', page)
    assert ids == [m["id"] for m in data()["moves"]]


def test_missing_marker_raises():
    with pytest.raises(ValueError):
        load_build()._inject("<p>no markers</p>", "moves", "x")


def test_page_states_age_rules_date():
    age = section("sm-age")
    assert f'({data()["age_rules_date"]})' in age
    assert "You never need AI to use a move." in age
    for rule in data()["age_rules"]:
        assert escape(rule["tool"]) in age and escape(rule["rule"]) in age
    for word in ("national", "school policy"):
        assert word in age, word


def test_sections_in_order():
    page = html()
    positions = [page.index(f'id="{sid}"') for sid in SECTIONS]
    assert positions == sorted(positions)


def test_evidence_section_has_legend_note_and_sources():
    evidence = section("sm-evidence")
    for label in data()["labels"].values():
        assert f">{escape(label['name'])}<" in evidence and escape(label["definition"]) in evidence
    assert escape(data()["classroom_note"]) in evidence
    for move in data()["moves"]:
        for s in move["sources"]:
            assert escape(s["url"]) in evidence, s["url"]


def test_feels_section_from_json():
    feels = section("sm-feels")
    assert escape(data()["feels_harder"]["text"]) in feels
    for s in data()["feels_harder"]["sources"]:
        assert escape(s["url"]) in feels


def test_hero_back_link_and_download():
    page = html()
    assert '<a class="tm-back" href="/study/">← Study + AI</a>' in page
    assert "Free tool · Grades 7–12" in page and "<h1>Study Moves</h1>" in page
    assert 'href="/assets/pdfs/free/study-moves-cards-en.pdf"' in section("sm-download")
    assert 'content="https://choosewise.education/assets/images/brand/og/studymoves-en.png"' in page


def test_builder_has_fields_and_defaults():
    builder = section("sm-builder")
    for el in ("sm-move", "sm-subject", "sm-grade", "sm-topic", "sm-prior", "sm-topic-label",
               "sm-prior-label", "sm-privacy", "sm-prompt", "sm-copy", "sm-hint"):
        assert f'id="{el}"' in builder, el
    assert re.search(r'<input type="radio" name="sm-who" id="sm-who-teacher" value="teacher" checked>', builder)
    assert re.search(r'<input type="radio" name="sm-who" id="sm-who-student" value="student">', builder)
    assert '<option value="9" selected>' in builder
    grades = re.findall(r'<option value="(\d+)"', re.search(r'<select[^>]*id="sm-grade".*?</select>', builder, re.S).group(0))
    assert grades == [str(g) for g in range(7, 13)]
    assert "Do not include student names or student work." in builder
