"""Sparade debriefer, kvällsprompten och uppföljningsnoten på /two-minute-debrief/.

Debriefer sparas bara i lärarens egen webbläsare (localStorage, nyckeln
choosewise.debrief.v1) och tas bort efter 14 dagar. "Idag" är besökarens
lokala datum, aldrig UTC.
Spec: docs/superpowers/specs/2026-10-30-two-minute-debrief-design.md.
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from conftest_debrief import browser, fill, open_page, page, site  # noqa: E402,F401

KEY = "choosewise.debrief.v1"
DAY = 24 * 3600 * 1000


def item(**kw):
    base = {"id": "a", "date": "2026-11-02", "savedAt": 0, "group": "8B maths", "grade": "8",
            "goal": "Solve two-step equations.", "evidence": "11 of 27 divided first.", "surprise": "",
            "next": "Word problems, Thursday.", "analysed": False}
    base.update(kw)
    return base


def seeded(site, browser, items, **kw):
    """Öppnar sidan med de givna sparade debrieferna redan i lagringen."""
    script = f"localStorage.setItem({json.dumps(KEY)}, {json.dumps(json.dumps(items))});"
    return open_page(site, browser, init_script=script, **kw)


def stored(page):
    return json.loads(page.evaluate(f"localStorage.getItem({json.dumps(KEY)})") or "[]")


def now_ms():
    return int(time.time() * 1000)


def test_save_lists_and_clears_answers(page):
    fill(page, surprise="Low energy.")
    page.click("#td-save")
    items = stored(page)
    assert len(items) == 1
    assert items[0]["group"] == "8B maths" and items[0]["surprise"] == "Low energy." and items[0]["analysed"] is False
    assert len(items[0]["date"]) == 10
    for f in ("#td-goal", "#td-evidence", "#td-surprise", "#td-next"):
        assert page.input_value(f) == "", f
    assert page.input_value("#td-group") == "8B maths"
    assert page.locator("#td-saved li").count() == 1
    assert "8B maths" in page.inner_text("#td-saved")


def test_save_needs_the_required_fields(page):
    assert page.is_disabled("#td-save")
    fill(page)
    assert not page.is_disabled("#td-save")


def test_delete_one_and_delete_all(site, browser):
    t = now_ms()
    p = seeded(site, browser, [item(id="a", savedAt=t), item(id="b", group="10A English", savedAt=t)])
    assert p.locator("#td-saved li").count() == 2
    p.locator("#td-saved li").filter(has_text="10A English").get_by_role("button", name="Delete").click()
    assert [i["id"] for i in stored(p)] == ["a"]
    p.click("#td-delete-all")
    assert stored(p) == []
    assert p.locator("#td-saved li").count() == 0
    p.context.close()


def test_batch_uses_todays_unanalysed_and_marks_them(site, browser):
    t = now_ms()
    today = time.strftime("%Y-%m-%d", time.localtime(t / 1000))
    yesterday = time.strftime("%Y-%m-%d", time.localtime(t / 1000 - 86400))
    p = seeded(site, browser, [item(id="y", date=yesterday, savedAt=t - DAY, group="Yesterday group"),
                               item(id="a", date=today, savedAt=t, group="8B maths"),
                               item(id="b", date=today, savedAt=t, group="10A English", grade="10")])
    text = p.input_value("#td-batch-prompt")
    assert "DEBRIEF 1:" in text and "DEBRIEF 2:" in text and "DEBRIEF 3:" not in text
    assert "Yesterday group" not in text
    assert p.get_attribute("#td-batch-copy", "data-copy") == text
    p.click("#td-batch-copy")
    # Markeringen sker ett varv efter klicket, när kopieringen har läst texten.
    p.wait_for_function("document.getElementById('td-batch-prompt').value === ''", timeout=3000)
    assert {i["id"]: i["analysed"] for i in stored(p)} == {"y": False, "a": True, "b": True}
    assert p.input_value("#td-batch-prompt") == ""
    assert p.is_disabled("#td-batch-copy")
    assert p.inner_text("#td-batch-hint") == "No unanalysed debriefs saved today."
    p.context.close()


def test_prune_drops_items_older_than_14_days(site, browser):
    t = now_ms()
    p = seeded(site, browser, [item(id="old", savedAt=t - 15 * DAY), item(id="new", savedAt=t - 2 * DAY)])
    assert [i["id"] for i in stored(p)] == ["new"]
    kept = p.evaluate("(a) => window.TwoMinuteDebrief.prune(a.list, a.now).map(function (x) { return x.id; })",
                      {"list": [item(id="x", savedAt=t - 14 * DAY - 1), item(id="z", savedAt=t - 14 * DAY + 60000)],
                       "now": t})
    assert kept == ["z"]
    p.context.close()


def test_follow_up_note_shows_last_next(site, browser):
    t = now_ms()
    p = seeded(site, browser, [item(id="a", date="2026-10-27", savedAt=t - DAY, next="Old next."),
                               item(id="b", date="2026-10-28", savedAt=t, next="Word problems, Thursday.")])
    assert p.is_hidden("#td-followup")
    p.fill("#td-group", "8B maths")
    assert p.is_visible("#td-followup")
    assert p.inner_text("#td-followup") == "Last time (28 Oct): Word problems, Thursday. What did your check show?"
    assert p.get_attribute("#td-evidence", "placeholder").startswith("Check: 20 of 27 right, up from 11.")
    p.fill("#td-group", "9D science")
    assert p.is_hidden("#td-followup")
    assert p.get_attribute("#td-evidence", "placeholder") == "On the exit ticket, 11 of 27 divided before subtracting."
    p.context.close()


def test_follow_up_note_matches_group_loosely(site, browser):
    p = seeded(site, browser, [item(id="b", date="2026-10-28", savedAt=now_ms())])
    p.fill("#td-group", "  8b   MATHS ")
    assert p.is_visible("#td-followup")
    p.context.close()


def test_today_uses_local_date(site, browser):
    ctx = browser.new_context(timezone_id="Europe/Stockholm")
    p = ctx.new_page()
    p.clock.set_fixed_time("2026-11-02T22:30:00Z")  # 23:30 i Stockholm
    p.goto(f"{site}/two-minute-debrief/", wait_until="networkidle")
    p.wait_for_function("window.TwoMinuteDebrief !== undefined", timeout=5000)
    assert p.evaluate("window.TwoMinuteDebrief.localDate(new Date())") == "2026-11-02"
    fill(p)
    p.click("#td-save")
    assert stored(p)[0]["date"] == "2026-11-02"
    ctx.close()


def test_works_without_storage(site, browser):
    script = ("Object.defineProperty(window, 'localStorage', {get: function () { throw new Error('blocked'); }});")
    p = open_page(site, browser, init_script=script)
    assert p.is_visible("#td-storage-note")
    assert p.is_hidden("#td-save")
    assert p.is_hidden("#td-saved-area")
    fill(p)
    assert p.input_value("#td-prompt").startswith("Do not include student names")
    assert not p.is_disabled("#td-copy")
    p.context.close()


def test_corrupt_storage_is_treated_as_empty(site, browser):
    for bad in ("{not json", '{"a":1}', '[1, "x", null]'):
        script = f"localStorage.setItem({json.dumps(KEY)}, {json.dumps(bad)});"
        p = open_page(site, browser, init_script=script)
        assert p.locator("#td-saved li").count() == 0, bad
        fill(p)
        p.click("#td-save")
        assert len(stored(p)) == 1, bad
        p.context.close()


def test_copy_journal_row_button_matches_journalRow(site, browser):
    it = item(id="a", savedAt=now_ms(), surprise="Low\tenergy")
    p = seeded(site, browser, [it])
    button = p.locator("#td-saved li").first.get_by_role("button", name="Copy journal row")
    expected = p.evaluate("(s) => window.TwoMinuteDebrief.journalRow(s)", it)
    assert button.get_attribute("data-copy") == expected
    p.context.close()
