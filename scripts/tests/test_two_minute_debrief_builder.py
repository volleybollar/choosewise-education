"""Debriefens promptbyggare på /two-minute-debrief/ i en riktig webbläsare.

Prompttexten är fastställd i planen och bor i assets/js/two-minute-debrief.js.
Ändra den bara tillsammans med PDF:ens luckprompter
(exports/build-two-minute-debrief-pdf.py).
Spec: docs/superpowers/specs/2026-10-30-two-minute-debrief-design.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from conftest_debrief import browser, fill, page, site  # noqa: E402,F401

D = {"group": "8B maths", "grade": "8", "goal": "Solve two-step equations.",
     "evidence": "11 of 27 forgot to divide the + 5.", "surprise": "", "next": "Word problems, Thursday."}

DEBRIEF_FORMAT = """Reply in plain text, no tables, in exactly this format:
LIKELY CAUSES: two possible explanations, numbered 1 and 2, each tied to this lesson's content, and what would tell them apart. Look beyond the first explanation: missing prior knowledge, too much new at once, a common misconception, a task that did not make students think about the goal, or too little practice.
NEXT LESSON: one concrete move aimed at the more likely cause, with minutes. Not "re-teach".
CHECK FIRST: one quick question or task, written exactly as students will see it, and when to move on, for example "Move on if about 4 in 5 get it right". If the evidence is only a feeling, also say what to look at to turn the feeling into evidence.
ONE QUESTION: one question back to the teacher, to think further."""

EXPECTED_DEBRIEF = """Do not include student names or student results in this conversation.

You are helping a Grade 8 teacher think through a lesson with 8B maths that did not go as planned. Base everything on what the teacher writes below, and tie every point to this lesson's content.

Goal: Solve two-step equations.
Evidence: 11 of 27 forgot to divide the + 5.
Surprise: None given
Next: Word problems, Thursday.

""" + DEBRIEF_FORMAT

EXPECTED_ROLLUP = """Do not include student names or student results in this conversation.

You are helping a teacher look back on a week of lesson debriefs. Each debrief has a date, a group, a goal, evidence, a surprise and a next step. Some evidence starts with the result of a check from an earlier lesson.

Debriefs:
LINE ONE
LINE TWO

Reply in plain text, no tables, in exactly this format:
PATTERNS: up to three patterns across the week that one lesson would not show. After each, name the debriefs it comes from by date and group.
WHAT WORKED: any change whose later check showed improvement. If there are no check results yet, write "Not enough check results yet".
ONE CHANGE FOR NEXT WEEK: one concrete change to the teacher's routine.
ONE QUESTION: one question back to the teacher."""


def call(page, fn, arg):
    return page.evaluate(f"(a) => window.TwoMinuteDebrief.{fn}(a)", arg)


def test_debrief_prompt_is_exact(page):
    assert call(page, "buildDebriefPrompt", D) == EXPECTED_DEBRIEF


def test_empty_surprise_reads_none_given(page):
    assert "Surprise: None given" in call(page, "buildDebriefPrompt", D)
    assert "Surprise: Low energy." in call(page, "buildDebriefPrompt", dict(D, surprise="Low energy."))


def test_builder_fills_prompt_and_hint(page):
    fill(page)
    assert page.input_value("#td-prompt") == EXPECTED_DEBRIEF
    assert page.inner_text("#td-hint") == "Your prompt is ready."
    assert not page.is_disabled("#td-copy")


def test_builder_requires_fields(page):
    for field in ("#td-group", "#td-goal", "#td-evidence", "#td-next"):
        fill(page)
        page.fill(field, "  ")
        assert page.input_value("#td-prompt") == "", field
        assert page.is_disabled("#td-copy"), field
        assert page.inner_text("#td-hint") == "Fill in group, goal, evidence and next to see your prompt."


def test_copy_button_matches_prompt(page):
    fill(page)
    assert page.get_attribute("#td-copy", "data-copy") == page.input_value("#td-prompt")


def test_batch_prompt_numbers_each_debrief(page):
    text = call(page, "buildBatchPrompt", [D, dict(D, group="10A English", grade="10")])
    assert text.startswith("Do not include student names or student results in this conversation.\n\n")
    assert "You are helping a teacher think through 2 lessons from today that did not go as planned." in text
    assert "DEBRIEF 1: 8B maths, Grade 8\nGoal: Solve two-step equations." in text
    assert "DEBRIEF 2: 10A English, Grade 10" in text
    assert "Reply in plain text, no tables. For each debrief, write its number and group as a heading, then exactly this format:" in text
    assert text.count("LIKELY CAUSES:") == 1 and text.count("ONE QUESTION:") == 1


def test_rollup_prompt_is_exact(page):
    assert call(page, "buildRollupPrompt", "LINE ONE\nLINE TWO") == EXPECTED_ROLLUP


def test_hinge_prompt_needs_group_and_goal(page):
    assert page.input_value("#td-hinge-prompt") == ""
    assert page.is_disabled("#td-hinge-copy")
    page.fill("#td-group", "8B maths")
    page.fill("#td-goal", "Solve two-step equations.")
    text = page.input_value("#td-hinge-prompt")
    assert text == call(page, "buildHingePrompt", {"group": "8B maths", "grade": "8", "goal": "Solve two-step equations."})
    assert "Write one hinge question for a Grade 8 lesson with 8B maths. The goal of the lesson: Solve two-step equations." in text
    assert "Give four options, A to D, of about the same length." in text
    assert not page.is_disabled("#td-hinge-copy")
    assert page.get_attribute("#td-hinge-copy", "data-copy") == text


def test_journal_row_has_eight_columns_even_with_tabs_and_newlines(page):
    saved = dict(D, date="2026-11-02", goal="Line one\nline\ttwo", surprise="")
    row = call(page, "journalRow", saved)
    cols = row.split("\t")
    assert len(cols) == 8
    assert cols[0] == "2026-11-02"
    assert cols[1] == "Grade 8 · 8B maths"
    assert cols[2] == "Line one line two"
    assert cols[6] == "" and cols[7] == ""
    assert "\n" not in row


def test_normalize_group(page):
    assert call(page, "normalizeGroup", "  8B   Maths ") == "8b maths"


def test_user_text_is_never_html(page):
    fill(page, goal='<img src=x onerror="window.pwned=1">')
    assert '<img src=x onerror="window.pwned=1">' in page.input_value("#td-prompt")
    assert page.evaluate("document.querySelectorAll('main img').length") == 0
    assert page.evaluate("window.pwned === undefined")
