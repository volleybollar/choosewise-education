"""Resultatvyn på /study-experiment/ i en riktig webbläsare.

Läraren skriver in förutsägelserna och poängen från lapparna, och
assets/js/study-experiment.js räknar och ritar resultatet medan hon skriver.
Allt sätts med textContent, så ingen text från fälten blir HTML. parseScores
och summarize är rena funktioner och anropas direkt via window.StudyExperiment.
Spec: docs/superpowers/specs/2026-11-13-study-experiment-design.md.
"""
import functools
import http.server
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TYPE_SCORES = "Type the scores from the slips to see your class's result."
SCORES = "3 5\n4 4\n5 3\n2 6"


@pytest.fixture(scope="module")
def site():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    class Server(socketserver.TCPServer):
        allow_reuse_address = True

    srv = Server(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()


@pytest.fixture(scope="module")
def browser():
    pw = pytest.importorskip("playwright.sync_api").sync_playwright().start()
    b = pw.chromium.launch()
    yield b
    b.close()
    pw.stop()


@pytest.fixture
def page(site, browser):
    p = browser.new_page()
    p.goto(f"{site}/study-experiment/", wait_until="networkidle")
    p.wait_for_function("window.StudyExperiment && typeof window.StudyExperiment.buildPrompt === 'function'")
    yield p
    p.close()


def predictions(page, twice="", tested="", same=""):
    page.fill("#se-pred-twice", str(twice))
    page.fill("#se-pred-tested", str(tested))
    page.fill("#se-pred-same", str(same))


def scores(page, text):
    page.fill("#se-scores", text)


def summary(page):
    return page.inner_text("#se-summary")


def groups(page):
    return page.locator("#se-chart .se-chart__group")


def group_titles(page):
    return [t.strip() for t in page.locator("#se-chart .se-chart__title").all_text_contents()]


def parse(page, text, maximum=6):
    return page.evaluate("([t, m]) => window.StudyExperiment.parseScores(t, m)", [text, maximum])


def test_parse_formats(page):
    got = parse(page, "3 5\n3,5\n3/5\n 3   5 \n3\t5\n\n4;2")
    assert got["pairs"] == [[3, 5], [3, 5], [3, 5], [3, 5], [3, 5], [4, 2]]
    assert got["bad"] == []


def test_parse_bad_lines(page):
    got = parse(page, "3-5\n7 2\n3.5 4\nabc\n2 2")
    assert got["pairs"] == [[2, 2]]
    assert got["bad"] == [1, 2, 3, 4]


def test_summarize_pure(page):
    got = page.evaluate(
        "() => window.StudyExperiment.summarize([[3,5],[4,4],[5,3],[2,6]], {twice: 15, tested: 7, same: 3})")
    assert got["n"] == 4
    assert got["avgTwice"] == 3.5
    assert got["avgTested"] == 4.5
    assert got["better"] == {"twice": 1, "tested": 2, "same": 1}
    assert got["predicted"] == {"twice": 15, "tested": 7, "same": 3}
    assert got["predictedTotal"] == 25
    empty = page.evaluate("() => window.StudyExperiment.summarize([], {twice: 0, tested: 0, same: 0})")
    assert empty["n"] == 0
    assert empty["avgTwice"] is None and empty["avgTested"] is None
    assert empty["predictedTotal"] == 0


def test_summary_counts(page):
    predictions(page, 15, 7, 3)
    scores(page, SCORES)
    text = summary(page)
    assert "4 slips." in text
    assert "3.5 of 6" in text
    assert "4.5 of 6" in text
    assert "2 scored higher on the text they tested" in text
    assert "1 on the text they read twice" in text
    assert "1 the same" in text
    assert "15 of 25 predicted" in text


def test_summary_is_paragraphs(page):
    predictions(page, 15, 7, 3)
    scores(page, SCORES)
    assert page.locator("#se-summary p").count() == 4
    assert page.locator("#se-summary p").first.inner_text().strip() == "4 slips."


def test_one_slip_is_singular(page):
    scores(page, "3 5")
    assert "1 slip." in summary(page)
    assert "1 slips" not in summary(page)


def test_chart_rows(page):
    predictions(page, 15, 7, 3)
    scores(page, SCORES)
    assert groups(page).count() == 2
    assert group_titles(page) == ["What you predicted", "What happened"]
    rows = page.locator("#se-chart .se-chart__row")
    assert rows.count() == 6
    labels = [t.strip() for t in page.locator("#se-chart .se-chart__label").all_text_contents()]
    assert labels == ["Read twice", "Tested myself", "About the same"] * 2
    counts = [t.strip() for t in page.locator("#se-chart .se-chart__count").all_text_contents()]
    assert "15 (60 %)" in counts
    assert "2 (50 %)" in counts
    assert counts == ["15 (60 %)", "7 (28 %)", "3 (12 %)", "1 (25 %)", "2 (50 %)", "1 (25 %)"]
    widths = page.eval_on_selector_all("#se-chart .se-chart__bar", "els => els.map(e => e.style.width)")
    assert widths == ["60%", "28%", "12%", "25%", "50%", "25%"]


def test_zero_count_row_has_no_bar_width(page):
    scores(page, "3 5\n2 6")
    widths = page.eval_on_selector_all("#se-chart .se-chart__bar", "els => els.map(e => e.style.width)")
    assert widths == ["0%", "100%", "0%"]
    mins = page.eval_on_selector_all("#se-chart .se-chart__bar", "els => els.map(e => e.style.minWidth)")
    assert mins == ["", "2px", ""]
    counts = [t.strip() for t in page.locator("#se-chart .se-chart__count").all_text_contents()]
    assert counts[0] == "0 (0 %)"


def test_errors_named(page):
    scores(page, "3 5\n9 1")
    assert page.text_content("#se-errors").strip() == "Line 2 is not two scores between 0 and 6, so it is left out."
    assert "1 slip." in summary(page)


def test_errors_one_sentence_per_line_and_cleared(page):
    scores(page, "x\n3 5\ny")
    text = page.text_content("#se-errors")
    assert "Line 1 is not two scores between 0 and 6, so it is left out." in text
    assert "Line 3 is not two scores between 0 and 6, so it is left out." in text
    scores(page, "3 5")
    assert page.text_content("#se-errors") == ""


def test_errors_region_stays_in_the_accessibility_tree(page):
    # Ett tomt live-område som göms med display:none läses inte upp första gången.
    assert page.get_attribute("#se-errors", "aria-live") == "polite"
    assert page.eval_on_selector("#se-errors", "e => getComputedStyle(e).display") != "none"


def test_zero_slips(page):
    scores(page, "")
    assert summary(page).strip() == TYPE_SCORES
    assert "NaN" not in page.inner_text("#se-results")
    assert "undefined" not in page.inner_text("#se-results")
    assert page.is_hidden("#se-even")
    assert groups(page).count() == 0


def test_only_bad_lines_counts_as_zero_slips(page):
    scores(page, "abc\n9 9")
    assert summary(page).strip() == TYPE_SCORES
    assert "NaN" not in page.inner_text("#se-results")
    assert page.is_hidden("#se-even")


def test_even_note(page):
    scores(page, "5 3\n4 4")
    assert page.is_visible("#se-even")
    scores(page, "3 5")
    assert page.is_hidden("#se-even")
    scores(page, "4 4")
    assert page.is_visible("#se-even")


def test_no_predictions_hides_row(page):
    predictions(page)
    scores(page, "3 5")
    assert groups(page).count() == 1
    assert group_titles(page) == ["What happened"]
    assert "predicted" not in summary(page)


def test_predictions_without_scores(page):
    predictions(page, 4, 1, 0)
    assert group_titles(page) == ["What you predicted"]
    assert summary(page).strip() == TYPE_SCORES
    assert "NaN" not in page.inner_text("#se-results")


def test_negative_and_decimal_predictions(page):
    predictions(page, -3, 2.5, "")
    scores(page, "3 5")
    assert group_titles(page) == ["What happened"]
    assert "predicted" not in summary(page)


def test_max_changes_validation(page):
    page.fill("#se-max", "10")
    scores(page, "8 9")
    assert page.text_content("#se-errors").strip() == ""
    assert "1 slip." in summary(page)
    assert "of 10 on average" in summary(page)
    page.fill("#se-max", "")
    assert page.text_content("#se-errors").strip() == "Line 1 is not two scores between 0 and 6, so it is left out."
    assert summary(page).strip() == TYPE_SCORES
    for bad_max in ("0", "21", "2.5"):
        page.fill("#se-max", bad_max)
        assert "between 0 and 6" in page.text_content("#se-errors"), bad_max


def test_no_html_rendered(page):
    scores(page, "<b>1</b> 2")
    assert "Line 1 is not two scores" in page.text_content("#se-errors")
    assert page.locator("#se-results b").count() == 0
