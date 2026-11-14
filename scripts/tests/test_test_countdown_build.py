"""Vakter för sidan Test Countdown (/test-countdown/) och dess byggskript.

Hur man testar sig själv, varför planen ser ut som den gör, noterna, lärartexterna,
forskningen och åldersreglerna byggs från test-countdown/countdown-en.json av
scripts/build-test-countdown.py, så att de syns utan JavaScript och kan
indexeras. Planeraren, planen och promptbyggaren är statisk HTML här; deras
JavaScript vaktas av egna tester. Testerna läser den byggda sidan och kör
byggskriptet.
Spec: docs/superpowers/specs/2026-11-14-test-countdown-design.md.
"""
import importlib.util
import json
import re
import shutil
from html import escape
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "test-countdown/index.html"
DATA = ROOT / "test-countdown/countdown-en.json"
BUILD = ROOT / "scripts/build-test-countdown.py"

SECTIONS = ["tc-make", "tc-howto", "tc-why", "tc-teachers", "tc-evidence", "tc-age", "tc-next"]
MARKERS = ["howto", "why", "notes", "share", "noai", "evidence", "age"]


def html():
    return PAGE.read_text(encoding="utf-8")


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def load_build():
    spec = importlib.util.spec_from_file_location("build_test_countdown", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def section(section_id, page=None):
    m = re.search(rf'<section[^>]*id="{section_id}".*?</section>', page or html(), re.S)
    assert m, section_id
    return m.group(0)


def test_render_escapes_text():
    mod = load_build()
    d = {
        "how_to": {"title": "T <i>", "steps": ["A <b>&</b>"]},
        "feels_harder": "F <u>",
        "why": {"title": "W <s>", "intro": "I <em>", "points": ["P <q>"]},
        "short_note": "S <a>", "capped_note": "C <a>", "sensible": "N <a>",
        "share": "Sh <a>", "no_ai": "No <a>", "student_ai": "St <a>",
        "evidence": [{"text": "E <a>", "sources": [{"text": "X <a>", "url": 'https://x.test/?a=1&b="2"'}]}],
        "age_rules": [{"tool": "Tool <a>", "rule": "Rule <a>"}],
        "age_rules_date": "Now <a>",
    }
    outputs = [
        mod.render_howto(d), mod.render_why(d), mod.render_notes(d), mod.render_share(d),
        mod.render_noai(d), mod.render_evidence(d), mod.render_age(d),
    ]
    for out in outputs:
        assert "&lt;" in out, out
        assert not re.search(r"<(b|i|u|s|q|em)>", out), out
        assert "<a>" not in out, out
    # Adressen i en källänk escapas också, så att citattecknet inte bryter ut ur href.
    assert 'href="https://x.test/?a=1&amp;b=&quot;2&quot;"' in outputs[5]


def test_build_fills_every_marker():
    d = data()
    page = html()
    for name in MARKERS:
        assert f"<!-- {name}:start -->" in page and f"<!-- {name}:end -->" in page, name
    howto, why = section("tc-howto"), section("tc-why")
    make, teachers, age = section("tc-make"), section("tc-teachers"), section("tc-age")
    assert escape(d["how_to"]["title"]) in howto
    for step in d["how_to"]["steps"]:
        assert escape(step) in howto, step
    assert escape(d["feels_harder"]) in howto
    assert escape(d["why"]["title"]) in why and escape(d["why"]["intro"]) in why
    for point in d["why"]["points"]:
        assert escape(point) in why, point
    for key in ("short_note", "capped_note", "sensible"):
        assert escape(d[key]) in make, key
    assert escape(d["share"]) in teachers
    assert escape(d["no_ai"]) in teachers
    assert escape(d["student_ai"]) in age
    assert f'({d["age_rules_date"]})' in age
    for rule in d["age_rules"]:
        assert escape(rule["tool"]) in age and escape(rule["rule"]) in age
    # Pekaren till Study Moves för elever från 13 år, med punkt efter länken.
    assert ('<a href="/study-moves/#test-yourself">Test yourself in Study Moves</a>.</p>') in age
    # Den statiska läsaransvarsnoten, samma som i Study Moves.
    assert ("Rules differ between countries and change often. Check your own national rules "
            "and your school policy before students use any AI tool.") in age


def test_notes_start_hidden():
    make = section("tc-make")
    assert re.search(r'<p[^>]*id="tc-short"[^>]*\bhidden\b', make)
    assert re.search(r'<p[^>]*id="tc-capped"[^>]*\bhidden\b', make)
    assert 'class="tc-sensible"' in make


def test_every_evidence_source_linked():
    evidence = section("tc-evidence")
    for item in data()["evidence"]:
        assert escape(item["text"]) in evidence, item["text"]
        for s in item["sources"]:
            assert f'href="{escape(s["url"])}"' in evidence, s["url"]
            assert escape(s["text"]) in evidence, s["text"]


def test_build_is_idempotent(tmp_path):
    (tmp_path / "test-countdown").mkdir()
    shutil.copy(PAGE, tmp_path / "test-countdown/index.html")
    shutil.copy(DATA, tmp_path / "test-countdown/countdown-en.json")
    mod = load_build()
    mod.build(tmp_path)
    first = (tmp_path / "test-countdown/index.html").read_bytes()
    mod.build(tmp_path)
    assert (tmp_path / "test-countdown/index.html").read_bytes() == first


def test_page_is_built_from_current_json(tmp_path):
    # Den incheckade sidan ska vara byggd från den incheckade JSON-filen.
    (tmp_path / "test-countdown").mkdir()
    shutil.copy(PAGE, tmp_path / "test-countdown/index.html")
    shutil.copy(DATA, tmp_path / "test-countdown/countdown-en.json")
    load_build().build(tmp_path)
    assert (tmp_path / "test-countdown/index.html").read_text(encoding="utf-8") == html()


def test_missing_marker_raises():
    with pytest.raises(ValueError):
        load_build()._inject("<p>no markers</p>", "howto", "x")


def test_form_defaults():
    make = section("tc-make")
    form = re.search(r'<form[^>]*id="tc-form".*?</form>', make, re.S).group(0)
    assert 'onsubmit="return false"' in re.search(r'<form[^>]*id="tc-form"[^>]*>', form).group(0)
    # Provdatum (obligatoriskt) och startdatum.
    assert re.search(r'<input[^>]*id="tc-test"[^>]*type="date"[^>]*required|<input[^>]*type="date"[^>]*id="tc-test"[^>]*required', form)
    assert re.search(r'<input[^>]*id="tc-start"[^>]*type="date"|<input[^>]*type="date"[^>]*id="tc-start"', form)
    # Områdena: fyra rader, högst 400 tecken, tre exempelrader.
    assert re.search(r'<textarea[^>]*id="tc-areas"[^>]*rows="4"[^>]*maxlength="400"[^>]*placeholder="Cells&#10;Photosynthesis&#10;Food chains"', form)
    # Minuter: 15/20/30/45 med 20 förvalt.
    minutes = re.search(r'<select[^>]*id="tc-minutes".*?</select>', form, re.S).group(0)
    assert re.findall(r'<option value="(\d+)"', minutes) == ["15", "20", "30", "45"]
    assert re.findall(r'<option value="(\d+)" selected', minutes) == ["20"]
    # Sju dagar, alla ikryssade, värdena 1 till 7 och etiketterna Mon till Sun.
    days = re.search(r'<fieldset[^>]*id="tc-days".*?</fieldset>', form, re.S).group(0)
    boxes = re.findall(r'<input[^>]*type="checkbox"[^>]*>', days)
    assert len(boxes) == 7
    assert all('name="day"' in b and re.search(r"\bchecked\b", b) for b in boxes)
    assert [re.search(r'value="(\d)"', b).group(1) for b in boxes] == [str(i) for i in range(1, 8)]
    labels = re.findall(r"<span>([A-Za-z]{3})</span>", days)
    assert labels == ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    # Privacy-raden står före formuläret.
    assert "<strong>Do not type names.</strong> The plan only needs your test date and what the test covers." in make
    assert make.index("tm-privacy") < make.index('id="tc-form"')


def test_plan_container_and_buttons():
    make = section("tc-make")
    assert re.search(r'<p[^>]*id="tc-hint"[^>]*aria-live="polite"[^>]*>Pick your test date to see your plan\.</p>', make)
    assert 'class="tm-hint"' in re.search(r'<p[^>]*id="tc-hint"[^>]*>', make).group(0)
    plan = re.search(r'<div[^>]*id="tc-plan"[^>]*>.*', make, re.S).group(0)
    assert re.search(r'<div[^>]*id="tc-plan"[^>]*\bhidden\b', make)
    for el in ("tc-plan-title", "tc-plan-total", "tc-plan-list", "tc-link", "tc-print"):
        assert f'id="{el}"' in plan, el
    assert re.search(r'<ol[^>]*id="tc-plan-list"[^>]*class="tc-plan__list"|<ol[^>]*class="tc-plan__list"[^>]*id="tc-plan-list"', plan)
    assert re.search(r'<button[^>]*id="tc-link"[^>]*data-copy=""[^>]*>Copy link to this plan</button>', plan)
    assert re.search(r'<button[^>]*id="tc-print"[^>]*>Print the plan</button>', plan)
    assert 'class="copy-toast" role="status">Copied</span>' in plan
    assert ("Bookmark this page to come back to your plan. The link holds your plan; "
            "nothing is saved anywhere else.") in plan
    # Noterna ligger inne i planen, före knapparna.
    assert plan.index('id="tc-short"') < plan.index('id="tc-link"')


def test_builder_fields_and_defaults():
    teachers = section("tc-teachers")
    builder = re.search(r'id="tc-builder".*', teachers, re.S).group(0)
    for el in ("tc-subject", "tc-subjects", "tc-grade", "tc-language", "tc-prompt", "tc-copy", "tc-prompt-hint"):
        assert f'id="{el}"' in builder, el
    assert '<option value="9" selected>' in builder
    grades = re.findall(r'<option value="(\d+)"', re.search(r'<select[^>]*id="tc-grade".*?</select>', builder, re.S).group(0))
    assert grades == [str(g) for g in range(7, 13)]
    assert re.search(r'<input[^>]*id="tc-subject"[^>]*list="tc-subjects"[^>]*maxlength="60"', builder)
    assert re.search(r'<input[^>]*id="tc-language"[^>]*value="English"[^>]*maxlength="40"', builder)
    assert re.search(r'<textarea[^>]*id="tc-prompt"[^>]*rows="18"[^>]*readonly|<textarea[^>]*id="tc-prompt"[^>]*readonly[^>]*rows="18"', builder)
    assert 'tm-prompt' in re.search(r'<textarea[^>]*id="tc-prompt"[^>]*>', builder).group(0)
    assert re.search(r'<button[^>]*id="tc-copy"[^>]*data-copy=""[^>]*disabled[^>]*>Copy prompt</button>', builder)
    assert re.search(r'<p[^>]*id="tc-prompt-hint"[^>]*aria-live="polite"[^>]*>Make a plan above, then fill in your subject\.</p>', builder)
    assert 'class="copy-toast"' in builder
    # Samma ämnesförslag som Study Moves.
    moves = (ROOT / "study-moves/index.html").read_text(encoding="utf-8")
    options = lambda page, dl: re.findall(r'<option value="([^"]+)">', re.search(rf'<datalist id="{dl}">.*?</datalist>', page, re.S).group(0))
    assert options(builder, "tc-subjects") == options(moves, "sm-subjects")
    # Byggaren ligger före no-AI-noten, och hela lärarsektionen har en egen rubrik.
    assert teachers.index('id="tc-builder"') < teachers.index(escape(data()["no_ai"]))
    assert "Make the quizzes with AI" in teachers


def test_sections_in_order():
    page = html()
    positions = [page.index(f'id="{sid}"') for sid in SECTIONS]
    assert positions == sorted(positions)
    # Markörerna ligger i sektionen där de hör hemma.
    for sid, name in (("tc-howto", "howto"), ("tc-why", "why"), ("tc-make", "notes"), ("tc-teachers", "share"),
                      ("tc-teachers", "noai"), ("tc-evidence", "evidence"), ("tc-age", "age")):
        assert f"<!-- {name}:start -->" in section(sid), (sid, name)


def test_head_hero_and_scripts():
    page = html()
    assert "<title>Test Countdown — choosewise.education</title>" in page
    desc = ("A free study planner for Grades 7–12. Type in your test date and what the test covers, and get short "
            "study sessions on different days instead of one long evening. No AI needed.")
    assert f'<meta name="description" content="{desc}">' in page
    assert f'<meta property="og:description" content="{desc}">' in page
    assert 'content="https://choosewise.education/assets/images/brand/og/testcountdown-en.png"' in page
    assert '<link rel="canonical" href="https://choosewise.education/test-countdown/">' in page
    assert "thinking-moves.css?v=20261029a" in page and "test-countdown.css?v=20261114a" in page
    assert page.index("thinking-moves.css") < page.index("test-countdown.css")
    assert '<a class="tm-back" href="/study/">← Study + AI</a>' in page
    assert "Free study planner · Grades 7–12" in page and "<h1>Test Countdown</h1>" in page
    promises = re.search(r'<ul class="tm-promises">.*?</ul>', page, re.S).group(0)
    assert promises.count("<li><strong>") == 3
    for lead in ("No AI needed.", "Nothing is saved.", "For students and teachers."):
        assert f"<strong>{lead}</strong>" in promises, lead
    for src in ("include.js", "copy-to-clipboard.js", "test-countdown.js"):
        assert f"/assets/js/{src}" in page, src
    nxt = section("tc-next")
    assert '<a href="/study-moves/#spread-it-out">Spread it out in Study Moves</a>' in nxt


def test_local_assets_exist():
    # Sidan får inte peka på en fil som saknas (JavaScript-filen skrivs i senare steg).
    page = html()
    for url in re.findall(r'(?:href|src)="(/assets/[^"?#]+)', page):
        assert (ROOT / url.lstrip("/")).exists(), url
