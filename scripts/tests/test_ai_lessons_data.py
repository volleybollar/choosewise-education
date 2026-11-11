"""Vakter för innehållet i AI-lektionerna för elever (Skool kurs 5–6).

Spåret och varje lektion är JSON i den dolda mappen; sidorna och elev-PDF:en
byggs från dem. Testerna låser formen och specens hårda regler: högst 40
minuter, varje steg enskilt/par/alla, ingen förmänskligande formulering från
oss, daterade åldersgränser, läsarnoten och användningsraden ordagrant.
Spec: docs/superpowers/specs/2026-11-11-ai-lessons-for-students-design.md.
"""
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
YOUNGER = "ai-lessons-younger-3c514a93"
OLDER = "ai-lessons-older-319cf15d"

MODES = {"Individual", "Pairs", "All"}
AI_USES = {"none", "teacher-demo", "students"}
BLOCK_KINDS = {"text", "table", "slips", "checklist", "tickets", "cards", "mat", "image"}
READER_NOTE = ("Readers outside Sweden should verify their own national regulations. "
               "AI in education is evolving quickly and country rules differ significantly.")
USE_RIGHTS = ("For members of the Choosewise community: use these materials with your own students, "
              "share them with colleagues at your school, and adapt or translate them for your own teaching. "
              "Please don't republish or sell them.")
ANTHRO = re.compile(
    r"\b(AI|it|the (chat)?bot|the machine|the model|chatbots?|machines?|models?)\s+"
    r"(thinks?|understands?|knows?|wants?|feels?|believes?)\b", re.I)
# Ord som ger maskinen ett inre liv även utan subjekt framför ("train them to
# admit when they are unsure"). Granskningen 2026-11-11 hittade dem.
MENTAL = re.compile(r"\b(admits?|unsure|decides?|pretends?)\b", re.I)
TOKENS = re.compile(r"[a-z']+|\.")


def _tracks():
    spec = importlib.util.spec_from_file_location("build_ai_lessons", ROOT / "scripts/build-ai-lessons.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.TRACKS


TRACKS = _tracks()


def track(slug):
    return json.loads((ROOT / slug / "track-en.json").read_text(encoding="utf-8"))


def lessons(slug=None):
    """Lektionerna i ett spår, eller i alla spår."""
    return [json.loads((ROOT / s / entry["id"] / "lesson-en.json").read_text(encoding="utf-8"))
            for s in ([slug] if slug else TRACKS) for entry in track(s)["lessons"]]


def teacher_text(lesson):
    """Allt vi själva skriver till läraren (inte elevernas typiska svar)."""
    out = list(lesson["goals"]) + [k["meaning"] for k in lesson["key_words"]]
    out += list(lesson["before"]) + list(lesson["materials"]) + [lesson["simpler"], lesson["harder"], lesson["language_swap"]]
    out += list(lesson["background"]) + [lesson["line"], lesson["age_note"], lesson["skool_text"]]
    for s in lesson["steps"]:
        out += [s["do"], s.get("say", ""), s.get("fallback", "")] + list(s.get("prompts", []))
    return out


def statements(text):
    """Meningar som inte är frågor. Frågor till eleverna får provocera fram
    "maskinen vet" med flit; det vi själva påstår får det inte. Webbadresser
    är inga formuleringar och tas bort (lektionen who-decides heter så)."""
    text = re.sub(r"https?://\S+", "", text)
    for sentence in re.split(r"(?<=[.!?])[\"'”’)]*\s+", text):
        if not sentence.rstrip(" \"'”’)").endswith("?"):
            yield sentence


def test_both_tracks_are_built():
    assert TRACKS == [YOUNGER, OLDER]
    for slug in TRACKS:
        assert (ROOT / slug / "track-en.json").exists(), slug


def test_lesson_ids_unique_within_each_track():
    """Inom ett spår blir id:t en adress. Samma id i två spår är tillåtet
    (ai-or-human finns i 9–12 och 13–15)."""
    for slug in TRACKS:
        entries = track(slug)["lessons"]
        assert len({e["id"] for e in entries}) == len(entries), slug
        for band in {e["band"] for e in entries}:
            numbers = [e["number"] for e in entries if e["band"] == band]
            assert len(set(numbers)) == len(numbers), (slug, band)


def test_track_lists_existing_lessons():
    for slug in TRACKS:
        bands = {b["id"] for b in track(slug)["bands"]}
        for entry, lesson in zip(track(slug)["lessons"], lessons(slug)):
            assert entry["band"] in bands, entry["id"]
            assert (lesson["id"], lesson["band"], lesson["number"]) == (entry["id"], entry["band"], entry["number"])


def test_every_track_has_an_ai_use_note():
    for slug in TRACKS:
        assert track(slug)["ai_use_note"].strip(), slug


def test_shared_age_rows_match_across_tracks():
    """Spår 2 har spår 1:s rader ordagrant. Ändras en åldersgräns i det ena
    spåret måste den ändras i det andra."""
    young, old = track(YOUNGER)["age_limits"], track(OLDER)["age_limits"]
    assert young["checked"] == old["checked"]
    assert set(young["tools"]) <= set(old["tools"])
    for tid in young["tools"]:
        assert young["tools"][tid] == old["tools"][tid], tid


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
    assert MENTAL.search("They train them to admit when they are unsure.")
    for lesson in lessons():
        for text in teacher_text(lesson):
            for sentence in statements(text):
                assert not ANTHRO.search(sentence), (lesson["id"], sentence)
                assert not MENTAL.search(sentence), (lesson["id"], sentence)


def test_promise_to_come_back_is_kept():
    """Steg 1 lovar eleverna att gissningarna tas upp igen. Det ska ske i ett
    tidsatt steg, inte bara i en fråga som kanske aldrig ställs."""
    for lesson in lessons():
        steps = lesson["steps"]
        for i, s in enumerate(steps):
            if "come back to it" in s.get("say", ""):
                later = " ".join(t["do"] + " " + t.get("say", "") for t in steps[i + 2:])
                assert "guesses" in later.lower(), lesson["id"]


def test_every_lesson_has_age_note_and_language_swap():
    for lesson in lessons():
        assert lesson["language_swap"].strip() and lesson["age_note"].strip(), lesson["id"]


def test_credits_are_links():
    for lesson in lessons():
        for credit in lesson["credits"]:
            assert credit["text"].strip() and credit["url"].startswith("https://"), (lesson["id"], credit)


def test_language_swap_covers_every_student_page():
    """Varje elevsida har engelska ord. Språkbytet ska säga vad läraren gör
    med var och en, inte bara med träningstexten."""
    for lesson in lessons():
        named = set()
        for m in re.finditer(r"\bpages?\s+((?:\d+(?:,\s*|\s+and\s+)?)+)", lesson["language_swap"], re.I):
            named.update(int(n) for n in re.findall(r"\d+", m.group(1)))
        assert set(range(1, len(lesson["student_pdf"]["pages"]) + 1)) <= named, (lesson["id"], named)


def test_tickets_ask_the_closing_question():
    for lesson in lessons():
        tickets = [b for p in lesson["student_pdf"]["pages"] for b in p["blocks"] if b["kind"] == "tickets"]
        assert tickets and all(t["question"] == lesson["closing_question"] for t in tickets), lesson["id"]


def _next_words(lesson):
    toks = TOKENS.findall(lesson["training_text"].lower())
    return {w: Counter(toks[i + 1] for i, t in enumerate(toks[:-1]) if t == w) for w in lesson["starting_words"]}


def test_starting_words_repeat_with_variety():
    for lesson in lessons():
        if "training_text" not in lesson:
            continue
        for word, after in _next_words(lesson).items():
            assert sum(after.values()) >= 2, (lesson["id"], word)
            assert len(after) >= 2, (lesson["id"], word, dict(after))


def test_one_slip_page_holds_every_cup():
    """En kopp per startord, en lapp per streck: sidan med lappar måste räcka
    till ordet med flest streck."""
    for lesson in lessons():
        if "training_text" not in lesson:
            continue
        slips = [b["count"] for p in lesson["student_pdf"]["pages"] for b in p["blocks"] if b["kind"] == "slips"]
        most = max(sum(after.values()) for after in _next_words(lesson).values())
        assert slips and max(slips) >= most, (lesson["id"], slips, most)


def test_training_text_is_short():
    for lesson in lessons():
        if "training_text" in lesson:
            words = [t for t in TOKENS.findall(lesson["training_text"].lower()) if t != "."]
            assert 60 <= len(words) <= 120, (lesson["id"], len(words))


def test_tools_have_dated_age_limits():
    for slug in TRACKS:
        limits = track(slug)["age_limits"]
        assert limits["checked"] == "2026-11-11"
        assert {"chatgpt", "gemini", "copilot", "claude"} <= set(limits["tools"])
        for tid, tool in limits["tools"].items():
            assert tool["name"] and tool["min_age"] and "note" in tool, tid
        for lesson in lessons(slug):
            assert set(lesson["tools"]) <= set(limits["tools"]), lesson["id"]


def test_reader_note_and_use_rights_verbatim():
    for slug in TRACKS:
        assert track(slug)["reader_note"] == READER_NOTE
        assert track(slug)["use_rights"] == USE_RIGHTS


def test_frameworks_name_both():
    for slug in TRACKS:
        assert [f["name"] for f in track(slug)["frameworks"]] == ["AILit", "AI4K12"]
    for lesson in lessons():
        assert set(lesson["frameworks"]) == {"AILit", "AI4K12"}, lesson["id"]


def test_skool_text_links_the_lesson():
    for slug in TRACKS:
        for lesson in lessons(slug):
            url = f"https://choosewise.education/{slug}/{lesson['id']}/"
            assert url in lesson["skool_text"], lesson["id"]


def test_student_pdf_has_one_to_four_pages_of_known_blocks():
    for lesson in lessons():
        pages = lesson["student_pdf"]["pages"]
        assert 1 <= len(pages) <= 4, lesson["id"]
        for page in pages:
            assert page["title"] and page["instruction"], (lesson["id"], page.get("title"))
            for block in page["blocks"]:
                assert block["kind"] in BLOCK_KINDS, (lesson["id"], block["kind"])


# ───── Lektionsspecifika vakter (planen 2026-11-11-ai-lessons-9-12) ─────

def _lesson(lid, slug=YOUNGER):
    return json.loads((ROOT / slug / lid / "lesson-en.json").read_text(encoding="utf-8"))


def _blocks(lesson, kind):
    return [b for p in lesson["student_pdf"]["pages"] for b in p["blocks"] if b["kind"] == kind]


def test_ai_or_not_sorts_sixteen_cards_on_three_columns():
    lesson = _lesson("ai-or-not")
    assert sum(len(b["cards"]) for b in _blocks(lesson, "cards")) == 16
    assert [b["headings"] for b in _blocks(lesson, "mat")] == [["Always does the same", "Finds patterns and guesses", "Not sure"]]


def test_learning_from_examples_credits_iste_and_has_a_card_to_draw():
    lesson = _lesson("learning-from-examples")
    assert any("ISTE" in c["text"] and "CC BY 4.0" in c["text"] for c in lesson["credits"])
    new = [b for b in _blocks(lesson, "cards") if b.get("heading", "").startswith("New cards")]
    assert new and any(not c.get("icon") for c in new[0]["cards"])


def test_who_does_it_fail_has_ten_training_and_eight_visitor_cards():
    lesson = _lesson("who-does-it-fail")
    blocks = _blocks(lesson, "cards")
    training = [c for b in blocks if b.get("heading", "").startswith("Training") for c in b["cards"]]
    visitors = [c for b in blocks if b.get("heading", "").startswith("Visitors") for c in b["cards"]]
    assert len(training) == 10 and len(visitors) == 8
    assert any(c.get("icon") == "disabled" for c in visitors)  # en person i rullstol, inte bara stolen
    assert all(c.get("icon") != "user" for c in training)  # bysten saknar kropp


def test_ai_or_human_uses_the_picture_grid_and_gives_the_answers():
    lesson = _lesson("ai-or-human")
    assert [b["src"] for b in _blocks(lesson, "image")] == ["assets/images/ai-or-human/photo-grid.jpg"]
    assert any("1, 6 and 8 are not AI" in text for text in teacher_text(lesson))
    assert any("video 2" in text for text in teacher_text(lesson))


def test_who_decides_has_the_grid_and_its_own_rule_starters():
    lesson = _lesson("who-decides")
    grids = [b for b in _blocks(lesson, "checklist") if isinstance(b["items"], list) and len(b["items"]) == 8]
    assert grids and grids[0]["checks"] == ["Me", "The app", "Another person", "Not sure"]
    student_words = " ".join([b["body"] for b in _blocks(lesson, "text")]
                             + [c for b in _blocks(lesson, "table") for c in b["columns"]]).lower()
    for word in ("unsure", "honest", "get help", "private"):  # IDEAL Thinkers kategorier: bara inspiration
        assert word not in student_words, word


def test_no_tool_age_note_adds_something():
    """Sidan säger redan att lektionen inte använder något AI-verktyg; åldersraden
    ska tillföra något, inte upprepa det."""
    for lesson in lessons():
        if not lesson["tools"]:
            assert "don't use any AI tool" not in lesson["age_note"], lesson["id"]


def test_learning_from_examples_keeps_the_new_cards_apart():
    """De nya korten, och tåget som saknas med flit, får inte ligga på ett ark
    som eleverna klipper innan steg 5."""
    pages = _lesson("learning-from-examples")["student_pdf"]["pages"]
    new_page = next(p for p in pages if any(b.get("heading", "").startswith("New cards") for b in p["blocks"]))
    assert sum(b["kind"] == "cards" for b in new_page["blocks"]) == 1
    others = [c["word"] for p in pages if p is not new_page for b in p["blocks"] if b["kind"] == "cards" for c in b["cards"]]
    assert "train" not in others


def test_lessons_with_a_photo_say_how_to_print_it():
    for lesson in lessons():
        if _blocks(lesson, "image"):
            assert any("colour" in line for line in lesson["before"]), lesson["id"]


def test_who_decides_tricky_messages_come_from_a_child():
    lesson = _lesson("who-decides")
    tricky = [c for b in _blocks(lesson, "cards") for c in b["cards"]]
    assert tricky and all(c["word"].startswith("A child types:") for c in tricky)


# ───── Lektionsspecifika vakter, 13–15 (planen 2026-11-11-ai-lessons-13-15) ─────

def test_why_chatbots_feel_human_marks_the_chat_in_our_own_columns():
    lesson = _lesson("why-chatbots-feel-human", OLDER)
    chats = [b for b in _blocks(lesson, "checklist")
             if b["checks"] == ["Feelings", "Flattery", "Keeps you chatting", "Replaces people"]]
    assert len(chats) == 1 and 8 <= len(chats[0]["items"]) <= 12
    words = " ".join(c for b in _blocks(lesson, "checklist") for c in b["checks"] + list(b["items"])).lower()
    for word in ("sycophancy", "simulated", "authority", "social presence"):  # Common Sense: bara inspiration
        assert word not in words, word


def test_why_chatbots_feel_human_names_the_safeguarding_routine():
    assert any("safeguarding" in line for line in _lesson("why-chatbots-feel-human", OLDER)["before"])
