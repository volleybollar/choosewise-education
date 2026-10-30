"""Rättelser efter slutgranskningen av Two-Minute Debrief (2026-10-30).

Varje test återskapar ett fynd från granskningen och håller det borta.
"""
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from conftest_debrief import browser, fill, open_page, page, site  # noqa: E402,F401
from test_two_minute_debrief_saved import DAY, KEY, item, now_ms, seeded, stored  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def today():
    return time.strftime("%Y-%m-%d", time.localtime())


def test_page_ids_are_unique():
    # Fynd I2: avsnittet "Why it works" och textrutan hade samma id.
    html = (ROOT / "two-minute-debrief/index.html").read_text(encoding="utf-8")
    ids = re.findall(r'\bid="([^"]+)"', html)
    assert len(ids) == len(set(ids)), sorted({i for i in ids if ids.count(i) > 1})


def test_batch_prompt_says_one_lesson(page):
    one = page.evaluate("(d) => window.TwoMinuteDebrief.buildBatchPrompt([d])", item())
    assert "think through 1 lesson from today" in one
    two = page.evaluate("(d) => window.TwoMinuteDebrief.buildBatchPrompt([d, d])", item())
    assert "think through 2 lessons from today" in two


def test_run_debriefs_can_be_put_back_in_the_batch(site, browser):
    # Fynd I1: efter kopieringen gick prompten inte att få tillbaka.
    p = seeded(site, browser, [item(id="a", date=today(), savedAt=now_ms(), analysed=True)])
    assert p.is_disabled("#td-batch-copy")
    p.locator("#td-saved li").first.get_by_role("button", name=re.compile("^Run again")).click()
    assert stored(p)[0]["analysed"] is False
    assert "DEBRIEF 1: 8B maths" in p.input_value("#td-batch-prompt")
    p.context.close()


def test_batch_marks_exactly_what_was_shown(site, browser):
    # Fynd M2: markeringen ska gälla debrieferna i den visade prompten, inte en ny beräkning.
    p = seeded(site, browser, [item(id="a", date=today(), savedAt=now_ms())])
    shown = p.input_value("#td-batch-prompt")
    assert "DEBRIEF 1:" in shown
    p.evaluate("""() => { const real = Date; window.Date = class extends real {
        constructor(...a) { if (a.length) { super(...a); } else { super(real.now() + 86400000); } }
        static now() { return real.now() + 86400000; } }; }""")
    p.click("#td-batch-copy")
    p.wait_for_function("document.getElementById('td-batch-prompt').value === ''", timeout=3000)
    assert stored(p)[0]["analysed"] is True
    p.context.close()


def test_journal_cells_cannot_start_a_formula(page):
    # Fynd M1: en cell som börjar med = + - @ eller " tolkas av Excel.
    row = page.evaluate("(s) => window.TwoMinuteDebrief.journalRow(s)",
                        item(goal="=SUM(A1)", evidence='"quoted', surprise="+1", next="- worked examples"))
    cols = row.split("\t")
    assert len(cols) == 8
    for c in cols[2:6]:
        assert not re.match(r'^[=+\-@"]', c), c


def test_follow_up_ignores_debriefs_saved_today(site, browser):
    # Fynd M3: noten ska inte peka på debriefen man nyss sparade.
    p = seeded(site, browser, [item(id="a", date=today(), savedAt=now_ms())])
    p.fill("#td-group", "8B maths")
    assert p.is_hidden("#td-followup")
    p.context.close()


def test_follow_up_adds_a_full_stop(site, browser):
    p = seeded(site, browser, [item(id="a", date="2026-10-28", savedAt=now_ms() - DAY, next="Word problems, Thursday")])
    p.fill("#td-group", "8B maths")
    assert p.inner_text("#td-followup") == "Last time (28 Oct): Word problems, Thursday. What did your check show?"
    p.context.close()


def test_saved_row_buttons_name_their_debrief(site, browser):
    # Fynd M4: knapparna i listan ska säga vilken debrief de gäller.
    p = seeded(site, browser, [item(id="a", date="2026-10-28", savedAt=now_ms())])
    li = p.locator("#td-saved li").first
    assert li.get_by_role("button", name="Copy journal row, 28 Oct, 8B maths").count() == 1
    assert li.get_by_role("button", name="Delete, 28 Oct, 8B maths").count() == 1
    assert "td-followup" in p.get_attribute("#td-evidence", "aria-describedby")
    p.context.close()


def test_delete_all_asks_first(site, browser):
    # Fynd M5: ett feltryck ska inte radera två veckors debriefer.
    p = seeded(site, browser, [item(id="a", savedAt=now_ms())])
    p.once("dialog", lambda d: d.dismiss())
    p.click("#td-delete-all")
    assert len(stored(p)) == 1
    p.once("dialog", lambda d: d.accept())
    p.click("#td-delete-all")
    assert stored(p) == []
    p.context.close()


def test_failed_save_says_so(site, browser):
    # Fynd M6: när lagringen är full ska läraren få veta det.
    p = open_page(site, browser)
    fill(p)
    p.evaluate("""() => { const orig = Storage.prototype.setItem;
        Storage.prototype.setItem = function (k, v) { if (k === 'choosewise.debrief.v1') throw new Error('quota'); return orig.call(this, k, v); }; }""")
    p.click("#td-save")
    assert "Couldn't save" in p.inner_text("#td-hint")
    assert p.input_value("#td-goal") != ""
    p.context.close()


def test_incomplete_entries_are_ignored(site, browser):
    # Fynd M7: poster utan alla fält eller med ogiltig månad räknas inte.
    bad = [{"id": "x", "date": "2026-13-01", "savedAt": now_ms(), "group": "g", "grade": "8", "goal": "g",
            "evidence": "e", "surprise": "", "next": "n", "analysed": False},
           {"date": "2026-10-28", "savedAt": now_ms(), "group": "g"}]
    p = seeded(site, browser, bad + [item(id="ok", savedAt=now_ms())])
    assert p.locator("#td-saved li").count() == 1
    p.context.close()
