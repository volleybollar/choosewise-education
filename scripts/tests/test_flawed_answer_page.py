"""Vakter för sidan Flawed Answer (/flawed-answer/).

Feltypskorten, evidensen och åldersreglerna byggs från
flawed-answer/flaws-en.json (och åldersreglerna från
thinking-moves/moves-en.json) av scripts/build-flawed-answer.py, så att de
syns utan JavaScript. Testerna läser den byggda sidan och kör byggskriptet.
Spec: docs/superpowers/specs/2026-10-28-flawed-answer-design.md.
"""
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "flawed-answer/index.html"
DATA = ROOT / "flawed-answer/flaws-en.json"
TM_DATA = ROOT / "thinking-moves/moves-en.json"
BUILD = ROOT / "scripts/build-flawed-answer.py"

ORDER = ["wrong-cause", "correlation-as-cause", "missing-step", "overgeneralisation",
         "hidden-assumption", "right-for-wrong-reason"]
SECTIONS = ["fa-builder", "fa-how", "fa-flaws", "fa-variant", "fa-evidence", "fa-age", "fa-download"]
EASIER_ONLY = "Easier to spot only: AI tools could not plant this flaw reliably at the harder level."


def html():
    return PAGE.read_text(encoding="utf-8")


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def section(section_id):
    m = re.search(rf'<section[^>]*id="{section_id}".*?</section>', html(), re.S)
    assert m, section_id
    return m.group(0)


def cards():
    return re.findall(r'<article class="tm-move fa-flaw"[^>]*>.*?</article>', html(), re.S)


def load_build():
    spec = importlib.util.spec_from_file_location("build_flawed_answer", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def esc(text):
    from html import escape
    return escape(text)


def test_six_cards_in_order():
    ids = re.findall(r'<article class="tm-move fa-flaw" id="([^"]+)" data-flaw-id="\1"', html())
    assert ids == ORDER


def test_card_shows_icon_signs_and_example_key():
    for flaw, card in zip(data()["flaws"], cards()):
        assert f'src="/flawed-answer/icons/{flaw["id"]}.svg"' in card, flaw["id"]
        for sign in flaw["telltale_signs"]:
            assert esc(sign) in card, sign
        details = re.search(r"<details.*?</details>", card, re.S).group(0)
        for key in ("question", "answer", "flaw", "fix"):
            assert esc(flaw["example"][key]) in details, (flaw["id"], key)


def test_ai_label_on_every_example():
    for card in cards():
        assert "AI-generated answer" in card


def test_build_is_idempotent():
    mod = load_build()
    mod.build(ROOT)
    first = PAGE.read_bytes()
    mod.build(ROOT)
    assert PAGE.read_bytes() == first
    assert len(cards()) == 6


def test_json_text_is_escaped():
    mod = load_build()
    flaw = {"id": "x", "number": 1, "name": "A <b>", "one_liner": "Q & A",
            "telltale_signs": ["<i>s</i>", "t"], "prompt_brief": "p", "harder_ok": True,
            "example": {"subject": "S", "grade": 8, "level": "easier", "question": "<q>",
                        "answer": "<script>x</script>", "flaw": "f", "fix": "f",
                        "why_convincing": "w", "test_it": "t", "probe": "p", "think_back": "t"}}
    out = mod.render_flaw_card(flaw, data()["levels"])
    assert "<b>" not in out and "&lt;b&gt;" in out
    assert "<script>" not in out and "<i>s</i>" not in out


def test_page_has_required_sections():
    for sid in SECTIONS:
        assert re.search(rf'<section[^>]*id="{sid}"', html()), sid


def test_evidence_labels_and_toolkit_link():
    ev = section("fa-evidence")
    assert ">Strong<" in ev and ">Thin<" in ev
    assert 'href="/evidence/"' in ev
    assert "not a single use" in ev


def test_sources_list_every_url():
    d = data()
    ev = section("fa-evidence")
    urls = [s["url"] for e in d["evidence"] for s in e["sources"]] + [s["url"] for s in d["context"]["sources"]]
    for url in urls:
        assert esc(url) in ev, url


def test_age_rules_match_thinking_moves():
    age = section("fa-age")
    for rule in json.loads(TM_DATA.read_text(encoding="utf-8"))["age_rules"]:
        assert esc(rule["rule"]) in age, rule["tool"]
    assert "national" in age and "school policy" in age


def test_easier_only_line_shown_iff_harder_ok_false():
    mod = load_build()
    for flaw, card in zip(data()["flaws"], cards()):
        assert (EASIER_ONLY in card) == (not flaw["harder_ok"]), flaw["id"]
    flaw = dict(data()["flaws"][0], harder_ok=False)
    assert EASIER_ONLY in mod.render_flaw_card(flaw, data()["levels"])


def test_download_links_both_pdfs():
    dl = section("fa-download")
    assert 'href="/assets/pdfs/free/flawed-answer-frame-en.pdf"' in dl
    assert 'href="/assets/pdfs/free/flawed-answer-cards-en.pdf"' in dl


def test_privacy_line_visible():
    assert "Do not include student names or student work" in section("fa-builder")


def test_use_links_name_their_flaw():
    for flaw, card in zip(data()["flaws"], cards()):
        assert f'href="?flaw={flaw["id"]}#fa-builder"' in card
        assert f'aria-label="Use this flaw: {esc(flaw["name"])}"' in card, flaw["id"]


def test_variant_shows_student_prompt_and_rules():
    variant = section("fa-variant")
    assert esc(data()["variant"]["student_prompt"]) in variant
    assert "approved" in variant and "age rules" in variant


def test_hero_promise_and_back_link():
    hero = re.search(r'<section class="page-hero.*?</section>', html(), re.S).group(0)
    assert 'href="/think/"' in hero
    assert "About 5 minutes to prepare, 15 minutes in class, no student devices needed" in hero
