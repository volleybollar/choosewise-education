"""Vakter för sidan Lesson Lens (/lesson-lens/).

Exemplet överst och de tolv linskorten byggs från lesson-lens/lenses-en.json
av scripts/build-lesson-lens.py, så att de syns utan JavaScript och kan
indexeras. Testerna läser den byggda sidan och kör byggskriptet.
Spec: docs/superpowers/specs/2026-10-29-lesson-lens-design.md.
"""
import importlib.util
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "lesson-lens/index.html"
DATA = ROOT / "lesson-lens/lenses-en.json"
BUILD = ROOT / "scripts/build-lesson-lens.py"

ORDER = ["retrieval-practice", "spacing", "cognitive-load", "dual-coding", "formative-check",
         "feedback", "explicit-instruction", "metacognition", "dialogic-discussion",
         "belonging", "thinking-depth", "trade-off"]
SECTIONS = ["ll-builder", "ll-lenses", "ll-how", "ll-evidence", "ll-age", "ll-download"]


def html():
    return PAGE.read_text(encoding="utf-8")


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def section(section_id):
    m = re.search(rf'<section[^>]*id="{section_id}".*?</section>', html(), re.S)
    assert m, section_id
    return m.group(0)


def cards():
    return re.findall(r'<article class="tm-move ll-lens"[^>]*>.*?</article>', html(), re.S)


def load_build():
    spec = importlib.util.spec_from_file_location("build_lesson_lens", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_twelve_cards_in_order():
    ids = re.findall(r'<article class="tm-move ll-lens" id="([^"]+)" data-lens-id="\1"', html())
    assert ids == ORDER


def test_card_shows_label_chip():
    d = data()
    for lens, card in zip(d["lenses"], cards()):
        name = d["labels"][lens["label"]]["name"]
        assert re.search(rf'class="tm-chip tm-chip--{lens["label"]}">{name}<', card), lens["id"]


def test_examples_render_four_parts():
    for lens, card in zip(data()["lenses"], cards()):
        details = re.search(r"<details.*?</details>", card, re.S).group(0)
        for part in ("Lesson", "Keep", "Upgrade", "Nudge", "Check"):
            assert f">{part}<" in details, (lens["id"], part)
        for line in lens["example"]["lesson"]:
            assert escape(line) in details, (lens["id"], line)


def test_hero_shows_default_example_before_builder():
    page = html()
    m = re.search(r"<!-- hero-example:start -->(.*?)<!-- hero-example:end -->", page, re.S)
    assert m
    default = next(l for l in data()["lenses"] if l["id"] == data()["default_lens"])
    assert escape(default["example"]["keep"]) in m.group(1)
    assert page.index("<!-- hero-example:start -->") < page.index('id="ll-builder"')


def test_toolkit_links_on_cards():
    for lens, card in zip(data()["lenses"], cards()):
        for link in lens["toolkit"]:
            assert f'href="{link["href"]}"' in card, (lens["id"], link["href"])


def test_use_links_name_their_lens():
    for lens, card in zip(data()["lenses"], cards()):
        assert f'href="?lens={lens["id"]}#ll-builder"' in card
        assert f'data-use-lens="{lens["id"]}"' in card
        assert f'aria-label="Use this lens: {escape(lens["name"])}"' in card


def test_build_is_idempotent():
    mod = load_build()
    mod.build(ROOT)
    first = PAGE.read_bytes()
    mod.build(ROOT)
    assert PAGE.read_bytes() == first
    assert len(cards()) == 12


def test_page_has_required_sections():
    for sid in SECTIONS:
        assert re.search(rf'<section[^>]*id="{sid}"', html()), sid


def test_legend_has_four_labels():
    evidence = section("ll-evidence")
    for name in ("Strong", "Promising", "Framework", "Choosewise"):
        assert f">{name}<" in evidence, name


def test_evidence_section_lists_every_source():
    evidence = section("ll-evidence")
    for lens in data()["lenses"]:
        for s in lens["sources"]:
            assert escape(s["url"]) in evidence, s["url"]


def test_age_section_has_reader_note():
    text = section("ll-age")
    for word in ("Copilot Chat", "Gemini", "ChatGPT", "Claude", "national", "school policy"):
        assert word in text, word


def test_privacy_line_visible():
    assert "Do not include student names or student work" in section("ll-builder")


def test_download_links_pdf():
    assert 'href="/assets/pdfs/free/lesson-lens-cards-en.pdf"' in section("ll-download")


def test_back_link_to_hub():
    assert 'href="/pedagogy/"' in html()


def test_json_text_is_escaped():
    mod = load_build()
    lens = {"id": "x", "number": 1, "name": "A <b>", "one_liner": "Q & A", "label": "strong",
            "evidence": "e", "sources": [{"text": "s", "url": "https://x"}], "prompt_brief": "p",
            "toolkit": [{"href": "/evidence/", "text": "t"}],
            "example": {"subject": "S", "grade": 8, "lesson": ["<i>l</i>"] * 4, "keep": "k",
                        "upgrade": ["u"], "nudge": "None", "check": "c"}}
    out = mod.render_lens_card(lens, {"strong": {"name": "Strong"}})
    assert "<b>" not in out and "&lt;b&gt;" in out and "<i>l</i>" not in out
