"""Vakter för AI-lektionernas elev-PDF:er.

En PDF per lektion, 1–4 sidor. PDF:en är A4 men innehållet ska rymmas när
den skrivs ut i 100 % på US Letter, och varje sida bär sin sidfot. Källan är
genererad HTML i _unpublished/exports/ai-lessons/, byggd ur lesson-en.json.
Varje test går igenom alla lektioner i alla spår.
"""
import importlib.util
import json
import re
import subprocess
from pathlib import Path

import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "exports/build-ai-lessons-pdf.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


TRACKS = load("build_ai_lessons", ROOT / "scripts/build-ai-lessons.py").TRACKS


def track(slug):
    return json.loads((ROOT / slug / "track-en.json").read_text(encoding="utf-8"))


PAIRS = [(slug, entry["id"]) for slug in TRACKS for entry in track(slug)["lessons"]]


def lesson(slug, lid):
    return json.loads((ROOT / slug / lid / "lesson-en.json").read_text(encoding="utf-8"))


def pdf(slug, lid):
    return ROOT / slug / lid / lesson(slug, lid)["student_pdf"]["file"]


def src(slug, lid):
    return load("build_ai_lessons_pdf", BUILD).source_path(lesson(slug, lid))


def squash(text):
    return re.sub(r"\s+", "", text).lower()


def pages(path):
    return [squash(p.extract_text()) for p in PdfReader(path).pages]


def has(needle, haystack):
    return squash(needle) in haystack


@pytest.mark.parametrize("slug,lid", PAIRS)
def test_every_pdf_matches_its_page_count_and_footers(slug, lid):
    texts = pages(pdf(slug, lid))
    assert len(texts) == len(lesson(slug, lid)["student_pdf"]["pages"])
    for n, t in enumerate(texts, start=1):
        assert has(f"{n} / {len(texts)}", t) and has(lesson(slug, lid)["title"], t) and has("choosewise.education", t), n


def test_training_text_on_page_one():
    for slug, lid in PAIRS:
        if "training_text" in lesson(slug, lid):
            assert has(lesson(slug, lid)["training_text"], pages(pdf(slug, lid))[0]), lid


@pytest.mark.parametrize("slug,lid", PAIRS)
def test_use_rights_on_page_one(slug, lid):
    assert has(track(slug)["use_rights"], pages(pdf(slug, lid))[0])


@pytest.mark.parametrize("slug,lid", PAIRS)
def test_pdf_fonts_allowed_weights(slug, lid):
    out = subprocess.run(["pdffonts", str(pdf(slug, lid))], capture_output=True, text=True, check=True).stdout
    assert "HankenGrotesk" in out
    assert not re.search(r"(SemiBold|Bold|Black|Heavy)", out, re.I), out


@pytest.mark.parametrize("slug,lid", PAIRS)
def test_source_html_is_generated_from_json(slug, lid):
    build = load("build_ai_lessons", ROOT / "scripts/build-ai-lessons.py")
    t = build.load_track(ROOT, slug)
    mod = load("build_ai_lessons_pdf", BUILD)
    data = next(x for x in t["lesson_data"] if x["id"] == lid)
    assert mod.render_student_html(t, data) == src(slug, lid).read_text(encoding="utf-8")


def test_source_paths_are_unique_across_tracks():
    """ai-or-human finns i två spår; källfilerna får aldrig skriva över varandra."""
    paths = [src(slug, lid) for slug, lid in PAIRS]
    assert len(paths) == len(set(paths)), sorted(p.name for p in paths if paths.count(p) > 1)


@pytest.mark.parametrize("slug,lid", PAIRS)
def test_fits_us_letter(slug, lid, tmp_path):
    """En lärare skriver ut A4-PDF:en på US Letter i 100 %, centrerat, på en
    skrivare som inte når de yttersta 5 mm. Letter är 279,4 mm hög, så 8,8 mm
    försvinner upptill och nedtill på A4, och skrivaren tar 5 mm till; på
    bredden är Letter större. Varje ord måste ligga inom det som blir kvar."""
    out = tmp_path / "bbox.html"
    subprocess.run(["pdftotext", "-bbox", str(pdf(slug, lid)), str(out)], check=True)
    mm = 25.4 / 72
    top = (297 - 279.4) / 2 + 5
    side = max(0.0, 5 - (215.9 - 210) / 2)
    texts = re.split(r"<page ", out.read_text(encoding="utf-8"))[1:]
    assert len(texts) == len(lesson(slug, lid)["student_pdf"]["pages"])
    for n, text in enumerate(texts, start=1):
        words = re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)<', text)
        assert words, n
        for x0, y0, x1, y1, word in words:
            assert top <= float(y0) * mm and float(y1) * mm <= 297 - top, (n, word, float(y0) * mm, float(y1) * mm)
            assert side <= float(x0) * mm and float(x1) * mm <= 210 - side, (n, word)


def test_cards_have_cut_lines_and_words():
    mod = load("build_ai_lessons_pdf", BUILD)
    block = {"kind": "cards", "cards": [{"word": "bus", "icon": "bus"}, {"word": "hovercraft"}]}
    out = mod.BLOCKS["cards"](block)
    cards = re.findall(r'<div class="card">.*?</div></div>', out, re.S)
    assert len(cards) == 2
    assert "bus" in cards[0] and "<path" in cards[0]
    assert "hovercraft" in cards[1] and "draw it" in cards[1]
    css = mod.STYLE
    assert re.search(r"\.card\s*\{[^}]*dashed", css), "cards need dashed cut lines"


def test_mat_has_one_column_per_heading():
    mod = load("build_ai_lessons_pdf", BUILD)
    out = mod.BLOCKS["mat"]({"kind": "mat", "headings": ["Land", "Water", "Air"]})
    assert len(re.findall(r'class="mat__col"', out)) == 3 and "Water" in out


def test_checklist_takes_labelled_rows():
    mod = load("build_ai_lessons_pdf", BUILD)
    out = mod.BLOCKS["checklist"]({"kind": "checklist", "items": ["The next video", "The ads"], "checks": ["Me", "The app"]})
    assert "The next video" in out and out.count('class="box"') == 4


def test_table_takes_prefilled_rows():
    mod = load("build_ai_lessons_pdf", BUILD)
    out = mod.BLOCKS["table"]({"kind": "table", "columns": ["Die", "Word"], "rows": [["1, 2, 3", "cat"], ["4", ""]]})
    body = out.split("<tbody>", 1)[1]
    assert body.count("<tr>") == 2 and body.count("<td") == 4
    assert "cat" in body and "1, 2, 3" in body


def test_prefilled_tables_give_their_cells_room():
    """Förtryckta celler behöver luft och en första kolumn efter innehållet;
    annars flyter "Northside" och "Football" ihop i lektion 3."""
    mod = load("build_ai_lessons_pdf", BUILD)
    out = mod.BLOCKS["table"]({"kind": "table", "columns": ["A", "B"], "rows": [["x", ""]]})
    assert 'class="grid grid--fill grid--data"' in out
    assert re.search(r"\.grid--data td\s*\{[^}]*padding", mod.STYLE)
    # Flera tomma kolumner (lektion 5) ska dela bredden; sista kolumnen får inte låsas till 15 %.
    assert re.search(r"\.grid--data td:last-child\s*\{[^}]*width:\s*auto", mod.STYLE)
    assert "grid--data" not in mod.BLOCKS["table"]({"kind": "table", "columns": ["A"], "rows": 2})


def test_tall_tables_give_room_to_write():
    mod = load("build_ai_lessons_pdf", BUILD)
    out = mod.BLOCKS["table"]({"kind": "table", "columns": ["App", "Data"], "rows": [["A map app", ""]], "tall": True})
    assert "grid--tall" in out
    assert re.search(r"\.grid--tall td\s*\{[^}]*height:\s*18mm", mod.STYLE)
    assert "grid--tall" not in mod.BLOCKS["table"]({"kind": "table", "columns": ["A"], "rows": 2})


def test_images_block_puts_labelled_pictures_in_a_grid():
    mod = load("build_ai_lessons_pdf", BUILD)
    items = [{"src": "visual-codes/images/airplane-before-584w.webp", "label": "Photo", "alt": "An airplane"},
             {"src": "visual-codes/images/airplane-cutaway-584w.webp", "label": "A", "alt": "The airplane, opened up"}]
    out = mod.BLOCKS["images"]({"kind": "images", "items": items})
    assert out.startswith('<div class="images">') and out.count("<figure") == 2
    assert "<figcaption>Photo</figcaption>" in out and "<figcaption>A</figcaption>" in out
    assert "airplane-cutaway-584w.webp" in out and 'alt="The airplane, opened up"' in out
    assert re.search(r"\.images\s*\{[^}]*grid", mod.STYLE)
    assert re.search(r"\.images img\s*\{[^}]*max-height:\s*70mm", mod.STYLE)


def test_every_block_kind_has_a_header_icon():
    """Sidhuvudets ikon väljs efter sidans första block (utom text); en ny blocktyp utan ikon stoppar bygget."""
    mod = load("build_ai_lessons_pdf", BUILD)
    assert set(mod.BLOCKS) == set(mod.ICONS)


def test_missing_picture_in_images_block_stops_the_build():
    mod = load("build_ai_lessons_pdf", BUILD)
    with pytest.raises(FileNotFoundError, match="no-such-picture.webp"):
        mod.BLOCKS["images"]({"kind": "images", "items": [
            {"src": "visual-codes/images/no-such-picture.webp", "label": "A", "alt": "x"}]})


def test_missing_image_stops_the_build():
    mod = load("build_ai_lessons_pdf", BUILD)
    with pytest.raises(FileNotFoundError, match="no-such-picture.jpg"):
        mod.BLOCKS["image"]({"kind": "image", "src": "assets/images/no-such-picture.jpg", "alt": "x"})


@pytest.mark.parametrize("slug,lid", PAIRS)
def test_card_pictures_are_credited_in_the_pdf(slug, lid):
    """Tabler Icons (MIT): kretsen ska följa med när bilderna gör det."""
    blocks = [b for p in lesson(slug, lid)["student_pdf"]["pages"] for b in p["blocks"]]
    uses_icons = any(c.get("icon") for b in blocks for c in b.get("cards", [])) or any(b.get("icons") for b in blocks)
    assert has("Tabler Icons (MIT licence)", pages(pdf(slug, lid))[0]) == uses_icons


# ───── 5–8: bilder för den som inte läser än (planen 2026-11-12-ai-lessons-5-8) ─────

def test_mat_headings_can_carry_icons():
    mod = load("build_ai_lessons_pdf", BUILD)
    out = mod.BLOCKS["mat"]({"kind": "mat", "headings": ["Yes", "No"], "icons": ["check", "x"]})
    assert out.count("<svg") == 2 and "Yes" in out and "No" in out


def test_missing_mat_icon_stops_the_build():
    mod = load("build_ai_lessons_pdf", BUILD)
    with pytest.raises(FileNotFoundError, match="no-such-icon"):
        mod.BLOCKS["mat"]({"kind": "mat", "headings": ["Yes"], "icons": ["no-such-icon"]})


def test_drawing_ticket_has_a_box_instead_of_lines():
    mod = load("build_ai_lessons_pdf", BUILD)
    out = mod.BLOCKS["tickets"]({"kind": "tickets", "question": "Draw a robot.", "count": 2, "draw": True})
    assert out.count("ticket__draw") == 2 and "ticket__line" not in out
    assert "Draw a robot." in out and "Name:" in out


def test_draw_block_gives_a_box_to_draw_in():
    mod = load("build_ai_lessons_pdf", BUILD)
    out = mod.BLOCKS["draw"]({"kind": "draw", "label": "Our robot for a job"})
    assert "Our robot for a job" in out and 'class="draw' in out
    assert re.search(r"\.draw\s*\{", mod.STYLE)


def test_mat_icons_count_for_the_tabler_credit():
    mod = load("build_ai_lessons_pdf", BUILD)
    only_mat = {"student_pdf": {"pages": [{"blocks": [{"kind": "mat", "headings": ["Yes"], "icons": ["check"]}]}]}}
    assert mod._uses_icons(only_mat)


def test_mat_with_too_few_icons_stops_the_build():
    """zip tappar kolumner tyst om ikonerna är färre än rubrikerna."""
    mod = load("build_ai_lessons_pdf", BUILD)
    with pytest.raises(ValueError, match="one icon per heading"):
        mod.BLOCKS["mat"]({"kind": "mat", "headings": ["Yes", "No"], "icons": ["check"]})

