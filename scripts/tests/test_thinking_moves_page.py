"""Vakter för sidan Thinking Moves (/thinking-moves/).

Korten och klustren byggs från thinking-moves/moves-en.json av
scripts/build-thinking-moves.py, så att de syns utan JavaScript och kan
indexeras. Testerna läser den byggda sidan och kör byggskriptet.
Spec: docs/superpowers/specs/2026-10-27-thinking-moves-design.md.
"""
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "thinking-moves/index.html"
DATA = ROOT / "thinking-moves/moves-en.json"
BUILD = ROOT / "scripts/build-thinking-moves.py"

ORDER = ["many-ways", "pick-and-justify", "check-the-claim", "argue-it", "like-what",
         "best-explanation", "strip-it-down", "estimate-it", "model-it", "then-what",
         "map-the-loop", "think-back"]
SECTIONS = ["tm-builder", "tm-moves", "tm-how", "tm-clusters", "tm-evidence", "tm-age", "tm-download"]


def html():
    return PAGE.read_text(encoding="utf-8")


def section(section_id):
    m = re.search(rf'<section[^>]*id="{section_id}".*?</section>', html(), re.S)
    assert m, section_id
    return m.group(0)


def cards():
    return re.findall(r'<article class="tm-move"[^>]*>.*?</article>', html(), re.S)


def load_build():
    spec = importlib.util.spec_from_file_location("build_thinking_moves", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_twelve_cards_in_order():
    ids = re.findall(r'<article class="tm-move" id="([^"]+)" data-move-id="\1"', html())
    assert ids == ORDER


def test_card_shows_label_and_icon():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    names = {k: v["name"] for k, v in data["labels"].items() if k != "note"}
    for move, card in zip(data["moves"], cards()):
        assert f'src="/thinking-moves/icons/{move["id"]}.svg"' in card, move["id"]
        assert re.search(rf'class="tm-chip tm-chip--{move["label"]}">{names[move["label"]]}<', card), move["id"]


def test_examples_render_all_four_parts():
    for card in cards():
        details = re.search(r"<details.*?</details>", card, re.S).group(0)
        for part in ("Task", "Look for", "Probe", "Think back"):
            assert details.count(f">{part}<") == 2, part


def test_six_clusters_render_with_modes():
    clusters = section("tm-clusters")
    assert clusters.count('class="tm-cluster"') == 6
    assert "Janusian" in clusters and "Inversion" in clusters
    assert clusters.lower().count("thin") >= 2


def test_build_is_idempotent(tmp_path):
    mod = load_build()
    mod.build(ROOT)
    first = PAGE.read_bytes()
    mod.build(ROOT)
    assert PAGE.read_bytes() == first
    assert len(cards()) == 12


def test_page_has_required_sections():
    for sid in SECTIONS:
        assert re.search(rf'<section[^>]*id="{sid}"', html()), sid


def test_evidence_section_links_toolkit():
    assert 'href="/evidence/"' in section("tm-evidence")
    assert "not a single five-minute move" in section("tm-evidence")


def test_age_section_has_reader_note():
    text = section("tm-age")
    for word in ("Copilot Chat", "Gemini", "ChatGPT", "Claude", "national", "school policy"):
        assert word in text, word


def test_privacy_line_visible():
    assert "Do not include student names or student work" in section("tm-builder")


def test_download_links_pdf():
    assert 'href="/assets/pdfs/free/thinking-moves-cards-en.pdf"' in section("tm-download")


def test_json_text_is_escaped():
    mod = load_build()
    move = {"id": "x", "number": 1, "name": "A <b>", "one_liner": "Q & A", "modes": "m",
            "cluster": "c", "label": "strong", "evidence": "e", "sources": [{"text": "s", "url": "https://x"}],
            "prompt_brief": "p", "examples": [{"subject": "S", "grade": 8, "task": "<i>t</i>",
                                                "look_for": "l", "probe": "p", "think_back": "t"}] * 2}
    out = mod.render_move_card(move, {"strong": {"name": "Strong"}})
    assert "<b>" not in out and "&lt;b&gt;" in out and "<i>t</i>" not in out


def test_every_card_carries_the_label_caveat():
    for card in cards():
        assert "not a single five-minute move" in card
