"""Vakter för bilderna på AI-lektionernas kort.

Bilderna är enstaka ikoner ur Tabler Icons (MIT), kopierade till
_unpublished/exports/ai-lessons/icons/ med licensen bredvid. De ritas in i
elev-PDF:erna, så en fil får aldrig bära skript eller länkar, och ett kort
vars ikon saknas blir ett ordkort med en ruta att rita i.
"""
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ICONS = ROOT / "_unpublished/exports/ai-lessons/icons"
BUILD = ROOT / "exports/build-ai-lessons-pdf.py"


def load_build():
    spec = importlib.util.spec_from_file_location("build_ai_lessons_pdf", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def card_icons():
    spec = importlib.util.spec_from_file_location("build_ai_lessons", ROOT / "scripts/build-ai-lessons.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for slug in mod.TRACKS:
        yield from _card_icons(slug)


def _card_icons(slug):
    track = json.loads((ROOT / slug / "track-en.json").read_text(encoding="utf-8"))
    for entry in track["lessons"]:
        lesson = json.loads((ROOT / slug / entry["id"] / "lesson-en.json").read_text(encoding="utf-8"))
        for page in lesson["student_pdf"]["pages"]:
            for block in page["blocks"]:
                for card in block.get("cards", []):
                    if card.get("icon"):
                        yield entry["id"], card["icon"]


def test_licence_file_is_there():
    text = (ICONS / "LICENSE-tabler-icons.txt").read_text(encoding="utf-8")
    assert "MIT License" in text and "Paweł Kuna" in text


def test_every_card_icon_exists():
    missing = [(lid, name) for lid, name in card_icons() if not (ICONS / f"{name}.svg").exists()]
    assert not missing, missing


def test_icons_carry_no_script():
    for svg in ICONS.glob("*.svg"):
        text = svg.read_text(encoding="utf-8")
        assert not re.search(r"<script|\son\w+\s*=|href\s*=", text, re.I), svg.name


def test_load_icon_strips_to_drawing_elements(tmp_path, monkeypatch):
    mod = load_build()
    (tmp_path / "bad.svg").write_text(
        '<svg viewBox="0 0 24 24"><script>alert(1)</script><path d="M1 1h2" onclick="x()"/>'
        '<a href="https://x"><circle cx="1" cy="1" r="1"/></a></svg>', encoding="utf-8")
    monkeypatch.setattr(mod, "ICON_DIR", tmp_path)
    out = mod.load_icon("bad")
    assert "<path" in out and "<circle" in out
    assert "script" not in out and "onclick" not in out and "href" not in out


def test_missing_icon_gives_a_draw_box():
    mod = load_build()
    assert mod.load_icon("no-such-icon") is None
    out = mod.BLOCKS["cards"]({"kind": "cards", "cards": [{"word": "x", "icon": "no-such-icon"}]})
    assert "draw it" in out
