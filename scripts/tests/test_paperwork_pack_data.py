"""Vakter för datafilen till Paperwork Pack (/paperwork-pack-f388fd9f/).

Datafilen är sidans och Word-mallarnas enda källa för text. Avsnitt, mallar,
prompter, landsrader, forskningspunkter och etiketter är beslutade i specen
(docs/superpowers/specs/2026-11-23-paperwork-pack-design.md, del C) — ändra dem
inte här utan att specen ändras först.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLUG = "paperwork-pack-f388fd9f"
DATA_PATH = ROOT / SLUG / "paperwork-en.json"
LADDER_PATH = ROOT / "quality-ladder-ec1c2f8c/ladder-en.json"

KEYS = {"labels", "hero", "sections", "evidence", "care"}
SECTION_IDS = ["pp-meetings", "pp-admin", "pp-parents"]
LESSONS = [5, 7, 10]
TEMPLATE_IDS = {
    "pp-meetings": ["meeting-protocol", "information-note", "skill-pairing"],
    "pp-admin": ["cut-first-checklist", "letter-template"],
    "pp-parents": ["messages-home"],
}
PROMPT_IDS = {
    "pp-meetings": ["P1", "P2"],
    "pp-admin": ["P3", "P4"],
    "pp-parents": ["P5", "P6", "P7"],
}
REUSED = {"P1": "lesson 5", "P3": "lesson 7", "P5": "lesson 10"}

# Prompterna ur kurslektionerna 5, 7 och 10 i AI OS
# (brands/choosewise/skool/skool-setup.md, §7.8), ordagrant utan indrag.
# De kallprovades 2026-11-17 och får inte ändras på sidan.
COURSE_P1 = (
    "Our team of [number] teachers of [subject or year group] has [length] minutes to work on "
    "one problem in our teaching: [the problem]. Write an agenda with times: what each of us "
    "brings (a task, a test item or a count from an exit ticket), how we look at it together, "
    "the one change we will each try in class, and when and how we check the result at the next "
    "meeting. Do not ask me about individual students or colleagues."
)
COURSE_P3 = (
    "I am a teacher at a [primary or secondary] school. Write a one-page template for a document "
    "I write again and again: [the document, for example a letter to parents about a trip]. Put "
    "every name, date, grade and personal detail in square brackets as a placeholder. Start with "
    "one line saying who it is for and what they need to do. Keep it short and plain. Do not ask "
    "me for names or details about students."
)
COURSE_P5 = (
    "I teach [subject] to [age or year group]. Write three message templates to parents or "
    "guardians, each under 60 words and in plain language: one about missing work, one about an "
    "upcoming test, and one about something done well with one thing to work on. Use square "
    "brackets for every name, date, number and detail, for example [first name], [date] and "
    "[topic]. End each message with one question the family can ask at home. Do not ask me about "
    "individual students."
)

# Landsraderna, ordagrant som i lektion 7 och 10 (specen C2, punkt 4 och 5).
COUNTRY_ADMIN = ("Rules differ between countries. Check what applies where you work before you "
                 "stop keeping a record or change what you document.")
COUNTRY_PARENTS = ("Rules differ between countries. Check what applies where you work before you "
                   "send messages home, store parents' contact details or translate for families.")

# Forskningspunkterna i specens ordning (C4): rubrik och etikett.
EVIDENCE = [
    ("Meetings about one problem, quality over hours", "promising"),
    ("Pairing on a skill", "promising"),
    ("Content matters more than format", None),
    ("Cut first", "framework"),
    ("Messages about learning", "promising"),
    ("Short absence letters", "promising"),
    ("AI for these tasks", None),
]
# Ett nyckelord per riskpunkt, i specens ordning (C5).
CARE_KEYWORDS = ["wrong", "one page", "too many", "translat", "one problem"]
# De tre tabellblocken (mall, rubrik): kolumnrubriker i "columns", tomma rader i "rows".
TABLE_BLOCKS = {
    ("meeting-protocol", "Decision log"),
    ("cut-first-checklist", "Our recurring documents"),
    ("messages-home", "Term plan"),
}
MESSAGE_HEADINGS =["Missing work", "An upcoming test", "Something done well", "Absence"]
BLAME_WORDS = ["fail", "concern", "worried", "must", "unacceptable"]
BANNED = ["leverage", "empower", "game-changer", "seamless", "unlock", "cutting-edge", "!"]


def data():
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


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


def section(section_id):
    return next(s for s in data()["sections"] if s["id"] == section_id)


def template(template_id):
    for s in data()["sections"]:
        for t in s["templates"]:
            if t["id"] == template_id:
                return t
    raise KeyError(template_id)


def prompts():
    return {p["id"]: p for s in data()["sections"] for p in s["prompts"]}


def message_blocks():
    blocks = template("messages-home")["blocks"]
    return {b["heading"]: " ".join(b["lines"]) for b in blocks[:4]}


def test_top_level_keys():
    assert set(data()) == KEYS


def test_sections_order_and_lessons():
    sections = data()["sections"]
    assert [s["id"] for s in sections] == SECTION_IDS
    assert [s["lesson"] for s in sections] == LESSONS


def test_template_ids_and_files():
    for s in data()["sections"]:
        assert [t["id"] for t in s["templates"]] == TEMPLATE_IDS[s["id"]]
        for t in s["templates"]:
            assert t["file"] == t["id"] + ".docx"
            assert t["title"] and t["intro"] and t["blocks"]
            for block in t["blocks"]:
                # Tabellblock har tomma rader i "lines"; alla andra block har text.
                assert block["heading"] and (block["lines"] or block.get("columns"))
                assert isinstance(block["box"], bool)


def test_prompt_ids():
    for s in data()["sections"]:
        assert [p["id"] for p in s["prompts"]] == PROMPT_IDS[s["id"]]
    for pid, p in prompts().items():
        assert p["title"] and p["body"]
        assert p["reused_from"] == REUSED.get(pid), pid


def test_reused_prompts_match_course():
    p = prompts()
    assert p["P1"]["body"] == COURSE_P1
    assert p["P3"]["body"] == COURSE_P3
    assert p["P5"]["body"] == COURSE_P5


def test_prompt_bodies_have_no_privacy_line():
    # Sidans hjälpfunktion lägger integritetsraden först; den får inte stå två gånger.
    for pid, p in prompts().items():
        assert "Do not include student names" not in p["body"], pid


def test_new_prompts_refuse_names():
    p = prompts()
    for pid in ("P2", "P4", "P6", "P7"):
        last_sentence = p[pid]["body"].rstrip().split(". ")[-1]
        assert "Do not ask" in last_sentence, (pid, last_sentence)
        assert "names" in last_sentence and "students" in last_sentence, (pid, last_sentence)
        assert "colleagues" in last_sentence, (pid, last_sentence)


def test_p6_p7_keep_brackets():
    p = prompts()
    for pid in ("P6", "P7"):
        assert "square bracket" in p[pid]["body"], pid
        assert "unchanged" in p[pid]["body"], pid


def test_message_word_limits():
    messages = message_blocks()
    assert list(messages) == MESSAGE_HEADINGS
    for heading, text in messages.items():
        assert len(text.split()) < 60, (heading, len(text.split()))
    assert len(messages["Absence"].split()) < 50


def test_only_the_four_messages_have_a_copy_button():
    # "copy": true ger blocket en egen kopieringsknapp på sidan: bara de fyra meddelandena hem.
    flagged = [(t["id"], b["heading"]) for s in data()["sections"] for t in s["templates"]
               for b in t["blocks"] if b.get("copy")]
    assert flagged == [("messages-home", h) for h in MESSAGE_HEADINGS]


def test_absence_has_no_blame_words():
    text = message_blocks()["Absence"].lower()
    for word in BLAME_WORDS:
        assert word not in text, word


def test_country_lines():
    assert section("pp-meetings")["country_line"] is None
    assert section("pp-admin")["country_line"] == COUNTRY_ADMIN
    assert section("pp-parents")["country_line"] == COUNTRY_PARENTS


def test_evidence_labels():
    evidence = data()["evidence"]
    assert [(e["title"], e["label"]) for e in evidence] == EVIDENCE
    for item in evidence:
        assert item["text"]
        if item["label"] is not None:
            assert item["sources"], item["title"]
        for source in item["sources"]:
            assert source["text"]
            assert source["url"].startswith("https://"), source


def test_labels_match_quality_ladder():
    ladder = json.loads(LADDER_PATH.read_text(encoding="utf-8"))
    assert data()["labels"] == ladder["labels"]


def test_care_points():
    care = data()["care"]
    assert len(care) == len(CARE_KEYWORDS)
    for item, keyword in zip(care, CARE_KEYWORDS):
        assert item["risk"] and item["what_we_do"]
        text = (item["risk"] + " " + item["what_we_do"]).lower()
        assert keyword in text, (keyword, item)


def test_banned_words():
    for text in all_strings(data()):
        lowered = text.lower()
        for word in BANNED:
            assert word not in lowered, (word, text)


def test_no_unbracketed_personal_data():
    # Texterna som går hem till familjer: varje datum, tal och detalj är en platshållare.
    for template_id in ("messages-home", "letter-template"):
        for block in template(template_id)["blocks"]:
            for line in block["lines"]:
                outside = re.sub(r"\[[^\]]*\]", "", line)
                assert not re.search(r"\d", outside), (template_id, line)


def test_table_blocks():
    # Tabeller är egna fält (columns + rows), aldrig rader med " | " i texten.
    tables = {}
    for s in data()["sections"]:
        for t in s["templates"]:
            for block in t["blocks"]:
                assert not any(" | " in line for line in block["lines"]), (t["id"], block)
                if "columns" in block:
                    tables[(t["id"], block["heading"])] = block
                else:
                    assert "rows" not in block, (t["id"], block)
    assert set(tables) == TABLE_BLOCKS
    for key, block in tables.items():
        assert len(block["columns"]) >= 2, key
        assert all(block["columns"]), key
        assert isinstance(block["rows"], int) and block["rows"] >= 1, key
        assert block["lines"] == [], key
    for text in all_strings(data()):
        assert " | " not in text, text


def test_feedback_policy_link():
    links = section("pp-admin")["links"]
    assert any(link["href"] == "/quality-ladder-ec1c2f8c/#ql-policy" and link["text"]
               for link in links)
