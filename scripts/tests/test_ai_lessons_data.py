"""Vakter för innehållet i AI-lektionerna för elever (Skool kurs 5–6).

Spåret och varje lektion är JSON i den dolda mappen; sidorna och elev-PDF:en
byggs från dem. Testerna låser formen och specens hårda regler: högst 40
minuter, varje steg enskilt/par/alla, ingen förmänskligande formulering från
oss, daterade åldersgränser, läsarnoten och användningsraden ordagrant.
Spec: docs/superpowers/specs/2026-11-11-ai-lessons-for-students-design.md.
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLUG = "ai-lessons-younger-3c514a93"
TRACK = ROOT / SLUG / "track-en.json"

MODES = {"Individual", "Pairs", "All"}
AI_USES = {"none", "teacher-demo", "students"}
BLOCK_KINDS = {"text", "table", "slips", "checklist", "tickets"}
READER_NOTE = ("Readers outside Sweden should verify their own national regulations. "
               "AI in education is evolving quickly and country rules differ significantly.")
USE_RIGHTS = ("For members of the Choosewise community: use these materials with your own students, "
              "share them with colleagues at your school, and adapt or translate them for your own teaching. "
              "Please don't republish or sell them.")
ANTHRO = re.compile(
    r"\b(AI|it|the (chat)?bot|the machine|the model|chatbots?|machines?|models?)\s+"
    r"(thinks?|understands?|knows?|wants?|feels?|believes?)\b", re.I)
TOKENS = re.compile(r"[a-z']+|\.")


def track():
    return json.loads(TRACK.read_text(encoding="utf-8"))


def lessons():
    return [json.loads((ROOT / SLUG / entry["id"] / "lesson-en.json").read_text(encoding="utf-8"))
            for entry in track()["lessons"]]


def teacher_text(lesson):
    """Allt vi själva skriver till läraren (inte elevernas typiska svar)."""
    out = list(lesson["goals"]) + [k["meaning"] for k in lesson["key_words"]]
    out += list(lesson["before"]) + [lesson["simpler"], lesson["harder"], lesson["language_swap"]]
    out += list(lesson["background"])
    for s in lesson["steps"]:
        out += [s["do"], s.get("say", ""), s.get("fallback", "")]
    return out


def statements(text):
    """Meningar som inte är frågor. Frågor till eleverna får provocera fram
    "maskinen vet" med flit; det vi själva påstår får det inte."""
    for sentence in re.split(r"(?<=[.!?])[\"'”’)]*\s+", text):
        if not sentence.rstrip(" \"'”’)").endswith("?"):
            yield sentence


def test_track_lists_existing_lessons():
    bands = {b["id"] for b in track()["bands"]}
    for entry, lesson in zip(track()["lessons"], lessons()):
        assert entry["band"] in bands, entry["id"]
        assert (lesson["id"], lesson["band"], lesson["number"]) == (entry["id"], entry["band"], entry["number"])


def test_minutes_add_up_and_stay_within_40():
    for lesson in lessons():
        assert sum(s["minutes"] for s in lesson["steps"]) == lesson["minutes"] <= 40, lesson["id"]


def test_every_step_has_a_mode():
    for lesson in lessons():
        for s in lesson["steps"]:
            assert s["mode"] in MODES, (lesson["id"], s["title"])


def test_ai_use_is_known():
    for lesson in lessons():
        assert lesson["ai_use"] in AI_USES, lesson["id"]


def test_demo_step_has_fallback():
    for lesson in lessons():
        demos = [s for s in lesson["steps"] if s.get("demo")]
        if lesson["ai_use"] == "teacher-demo":
            assert len(demos) == 1, lesson["id"]
            assert demos[0].get("fallback", "").strip(), lesson["id"]
            assert 2 <= len(demos[0].get("prompts", [])) <= 3, lesson["id"]
        else:
            assert not demos, lesson["id"]


def test_no_anthropomorphic_wording():
    assert ANTHRO.search("The chatbot knows the answer.")  # vakten själv biter
    for lesson in lessons():
        for text in teacher_text(lesson):
            for sentence in statements(text):
                assert not ANTHRO.search(sentence), (lesson["id"], sentence)


def test_text_lessons_explain_language_swap():
    for lesson in lessons():
        if lesson["uses_text"]:
            assert lesson["language_swap"].strip(), lesson["id"]


def _next_words(lesson):
    toks = TOKENS.findall(lesson["training_text"].lower())
    return {w: Counter(toks[i + 1] for i, t in enumerate(toks[:-1]) if t == w) for w in lesson["starting_words"]}


def test_starting_words_repeat_with_variety():
    for lesson in lessons():
        if not lesson["uses_text"]:
            continue
        for word, after in _next_words(lesson).items():
            assert sum(after.values()) >= 2, (lesson["id"], word)
            assert len(after) >= 2, (lesson["id"], word, dict(after))


def test_one_slip_page_holds_every_cup():
    """En kopp per startord, en lapp per streck: sidan med lappar måste räcka
    till ordet med flest streck."""
    for lesson in lessons():
        if not lesson["uses_text"]:
            continue
        slips = [b["count"] for p in lesson["student_pdf"]["pages"] for b in p["blocks"] if b["kind"] == "slips"]
        most = max(sum(after.values()) for after in _next_words(lesson).values())
        assert slips and max(slips) >= most, (lesson["id"], slips, most)


def test_training_text_is_short():
    for lesson in lessons():
        if lesson["uses_text"]:
            words = [t for t in TOKENS.findall(lesson["training_text"].lower()) if t != "."]
            assert 60 <= len(words) <= 120, (lesson["id"], len(words))


def test_tools_have_dated_age_limits():
    limits = track()["age_limits"]
    assert limits["checked"] == "2026-11-11"
    assert {"chatgpt", "gemini", "copilot", "claude"} <= set(limits["tools"])
    for tid, tool in limits["tools"].items():
        assert tool["name"] and tool["min_age"] and "note" in tool, tid
    for lesson in lessons():
        assert set(lesson["tools"]) <= set(limits["tools"]), lesson["id"]


def test_reader_note_and_use_rights_verbatim():
    assert track()["reader_note"] == READER_NOTE
    assert track()["use_rights"] == USE_RIGHTS


def test_frameworks_name_both():
    assert [f["name"] for f in track()["frameworks"]] == ["AILit", "AI4K12"]
    for lesson in lessons():
        assert set(lesson["frameworks"]) == {"AILit", "AI4K12"}, lesson["id"]


def test_skool_text_links_the_lesson():
    for lesson in lessons():
        url = f"https://choosewise.education/{SLUG}/{lesson['id']}/"
        assert url in lesson["skool_text"], lesson["id"]


def test_student_pdf_has_four_pages_of_known_blocks():
    for lesson in lessons():
        pages = lesson["student_pdf"]["pages"]
        assert len(pages) == 4, lesson["id"]
        for page in pages:
            assert page["title"] and page["instruction"], (lesson["id"], page.get("title"))
            for block in page["blocks"]:
                assert block["kind"] in BLOCK_KINDS, (lesson["id"], block["kind"])
