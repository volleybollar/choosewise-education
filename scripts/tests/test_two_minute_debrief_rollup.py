"""Veckosammanställningen på /two-minute-debrief/.

Läraren kryssar i sparade debriefer från de senaste 7 dagarna (alla ikryssade
från början) eller klistrar in rader från enhetsjournalen.
Spec: docs/superpowers/specs/2026-10-30-two-minute-debrief-design.md.
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from conftest_debrief import browser, open_page, page, site  # noqa: E402,F401
from test_two_minute_debrief_saved import DAY, item, now_ms, seeded  # noqa: E402

HINT = "Tick saved debriefs or paste rows from your unit journal."


def test_rollup_lists_last_seven_days_ticked(site, browser):
    t = now_ms()
    p = seeded(site, browser, [item(id="old", group="Old group", savedAt=t - 8 * DAY),
                               item(id="a", group="8B maths", savedAt=t - DAY),
                               item(id="b", group="10A English", grade="10", savedAt=t)])
    boxes = p.locator("#td-rollup-list input[type=checkbox]")
    assert boxes.count() == 2
    assert all(boxes.nth(i).is_checked() for i in range(2))
    assert "Old group" not in p.inner_text("#td-rollup-list")
    text = p.input_value("#td-rollup-prompt")
    assert "8B maths, Grade 8 | Goal: Solve two-step equations. | Evidence: 11 of 27 divided first." in text
    assert "10A English, Grade 10" in text
    assert text == p.evaluate("(t) => window.TwoMinuteDebrief.buildRollupPrompt(t)",
                              text.split("Debriefs:\n")[1].split("\n\nReply in plain text")[0])
    assert p.get_attribute("#td-rollup-copy", "data-copy") == text
    p.context.close()


def test_rollup_line_format(page):
    line = page.evaluate("(s) => window.TwoMinuteDebrief.rollupLines(s)",
                         [item(date="2026-10-28", surprise="", next="Word problems.")])
    assert line == ("2026-10-28 | 8B maths, Grade 8 | Goal: Solve two-step equations. | "
                    "Evidence: 11 of 27 divided first. | Surprise: None given | Next: Word problems.")


def test_unticking_removes_a_debrief(site, browser):
    t = now_ms()
    p = seeded(site, browser, [item(id="a", group="8B maths", savedAt=t), item(id="b", group="10A English", savedAt=t)])
    p.locator("#td-rollup-list li").filter(has_text="10A English").locator("input").uncheck()
    text = p.input_value("#td-rollup-prompt")
    assert "8B maths" in text and "10A English" not in text
    p.context.close()


def test_pasted_journal_rows_are_included(site, browser):
    p = seeded(site, browser, [item(id="a", savedAt=now_ms())])
    p.fill("#td-rollup-paste", "2026-10-20\tGrade 9 · 9D science\tBalance equations\tA feeling")
    text = p.input_value("#td-rollup-prompt")
    assert "8B maths, Grade 8" in text
    assert "2026-10-20\tGrade 9 · 9D science\tBalance equations\tA feeling" in text
    p.context.close()


def test_rollup_needs_something(page):
    assert page.input_value("#td-rollup-prompt") == ""
    assert page.is_disabled("#td-rollup-copy")
    assert page.inner_text("#td-rollup-hint") == HINT
    page.fill("#td-rollup-paste", "   ")
    assert page.is_disabled("#td-rollup-copy")


def test_rollup_updates_after_a_save(page):
    page.fill("#td-group", "8B maths")
    page.fill("#td-goal", "Goal.")
    page.fill("#td-evidence", "Evidence.")
    page.fill("#td-next", "Next.")
    page.click("#td-save")
    assert page.locator("#td-rollup-list input").count() == 1
    assert "8B maths" in page.input_value("#td-rollup-prompt")


def test_rollup_works_with_paste_only_without_storage(site, browser):
    script = "Object.defineProperty(window, 'localStorage', {get: function () { throw new Error('blocked'); }});"
    p = open_page(site, browser, init_script=script)
    assert p.is_hidden("#td-rollup-list")
    p.fill("#td-rollup-paste", "2026-10-26 8B maths goal evidence")
    assert "2026-10-26 8B maths goal evidence" in p.input_value("#td-rollup-prompt")
    assert not p.is_disabled("#td-rollup-copy")
    p.context.close()
