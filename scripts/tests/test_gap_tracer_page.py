"""Gap Tracer i en riktig webbläsare: sökning, byggstenar, plan och återkoppling.

Testerna använder den committade datan i gap-tracer/data/. Kedjan som bär
dem: Equivalent fractions (mt_FbDKeLfBCo) bygger på Finding halves and
quarters (mt_g3W0mdADVu), som bygger på What Is a Half? (mt_-hTTat0mBR).
Spec: docs/superpowers/specs/2026-10-24-gap-tracer-design.md.
"""
import functools
import http.server
import json
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

TARGET = "mt_FbDKeLfBCo"      # Equivalent fractions
HALVES = "mt_g3W0mdADVu"      # Finding halves and quarters (age 5+)
HALF = "mt_-hTTat0mBR"        # What Is a Half?
NO_PREREQS = "mt_-vvVxpOHG2"  # Ordering Events in Time
ENGLISH = "mt_-1okUh0Jdv"     # Comparing Structure in Information Texts

NO_ACTIVITIES = ("No practice activities for this skill yet — activities currently "
                 "exist only in Mathematics and Science.")
FETCH_FAILED = "Couldn't load the practice activities — check your connection and try again."


@pytest.fixture(scope="module")
def site():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):  # sviten ska vara tyst
            pass

    handler = functools.partial(Quiet, directory=str(ROOT))

    class Server(socketserver.TCPServer):
        allow_reuse_address = True

    srv = Server(("127.0.0.1", 0), handler)
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
    p.set_default_timeout(5000)  # allt är lokalt; 30 s per fel gör sviten seg
    p.errors = []
    p.on("pageerror", lambda e: p.errors.append(str(e)))
    p.on("console", lambda m: m.type == "error" and p.errors.append(m.text))
    # Sidan pekar på Johans riktiga Google Sheet. Ingen test får lägga rader där.
    p.route("https://script.google.com/**", lambda route: route.fulfill(status=200))
    p.goto(f"{site}/gap-tracer/", wait_until="networkidle")
    yield p
    p.close()


def pick(page, query, skill_id):
    page.fill("#gt-search", query)
    page.click(f'.gt-result[data-id="{skill_id}"]')


def answer(page, skill_id, value):
    page.locator(f'.gt-block[data-id="{skill_id}"] .gt-answer[data-answer="{value}"]').first.click()


def plan_ids(page):
    return page.eval_on_selector_all("#gt-plan-items .gt-plan__item", "els => els.map(e => e.dataset.id)")


def test_search_finds_equivalent_fractions_with_activity_badge(page):
    page.fill("#gt-search", "equivalent fractions")
    hit = page.locator(f'.gt-result[data-id="{TARGET}"]')
    assert hit.locator(".gt-result__name").inner_text() == "Equivalent fractions"
    assert hit.locator(".gt-badge").inner_text().lower() == "practice activities"


def test_search_by_curriculum_code(page):
    page.fill("#gt-search", "AC9M4N03")
    assert page.locator(".gt-result").count() > 0
    assert "AC9M4N03" in page.locator(".gt-result").first.inner_text()


def test_skill_without_activities_shows_the_exact_line(page):
    pick(page, "Comparing Structure in Information Texts", ENGLISH)
    item = page.locator(f'#gt-plan-items .gt-plan__item[data-id="{ENGLISH}"]')
    assert NO_ACTIVITIES in item.inner_text()


def test_name_is_filled_and_no_placeholder_leaks(page):
    page.fill("#gt-name", "Sam")
    pick(page, "equivalent fractions", TARGET)
    assert "{{" not in page.inner_text("main")
    assert "Sam" in page.locator(f'.gt-block[data-id="{HALVES}"] .gt-block__question').first.inner_text()


def test_name_change_updates_shown_questions(page):
    pick(page, "equivalent fractions", TARGET)
    page.fill("#gt-name", "Alex")
    assert "Alex" in page.locator(f'.gt-block[data-id="{HALVES}"] .gt-block__question').first.inner_text()


def test_no_opens_the_next_layer(page):
    pick(page, "equivalent fractions", TARGET)
    answer(page, HALVES, "no")
    page.locator(f'.gt-block[data-id="{HALVES}"] .gt-deeper').first.click()
    assert page.locator(f'.gt-block[data-id="{HALF}"]').count() >= 1


def test_plan_puts_foundations_first_and_target_last(page):
    pick(page, "equivalent fractions", TARGET)
    answer(page, HALVES, "no")
    page.locator(f'.gt-block[data-id="{HALVES}"] .gt-deeper').first.click()
    answer(page, HALF, "unsure")
    assert plan_ids(page) == [HALF, HALVES, TARGET]


def test_order_plan_pure(page):
    # c bygger på a och b, b bygger på a. a är delad och ska komma en gång, först.
    order = page.evaluate("""() => {
        const skills = new Map([
            ['c', {id: 'c', prereqs: [{id: 'b'}, {id: 'a'}]}],
            ['b', {id: 'b', prereqs: [{id: 'a'}]}],
            ['a', {id: 'a', prereqs: []}],
        ]);
        return GapTracer.orderPlan('c', new Set(['a', 'b']), skills);
    }""")
    assert order == ["a", "b", "c"]


def test_fill_name_pure(page):
    assert page.evaluate("GapTracer.fillName('Can {{name}} count?', '  Sam ')") == "Can Sam count?"
    assert page.evaluate("GapTracer.fillName('Can {{name}} count?', '')") == "Can the child count?"
    assert page.evaluate("GapTracer.fillName('{{name}} can count.', '')") == "The child can count."


def test_disclaimer_visible_at_top_and_in_plan(page):
    pick(page, "equivalent fractions", TARGET)
    boxes = page.locator(".gt-disclaimer")
    assert boxes.count() == 2
    for i in range(2):
        assert boxes.nth(i).is_visible()
        assert "It doesn't diagnose." in boxes.nth(i).inner_text()


def test_meta_fields_are_filled(page):
    page.wait_for_function("document.querySelector('[data-meta=marbleCommit]').textContent !== ''")
    empty = page.eval_on_selector_all("[data-meta]", "els => els.filter(e => !e.textContent.trim()).length")
    assert empty == 0
    assert page.locator('[data-meta="marbleCommit"]').first.inner_text() == "79aa2be"
    meta = json.loads((ROOT / "gap-tracer/data/meta.json").read_text(encoding="utf-8"))
    maths = page.locator('[data-meta="counts.bySubject.Mathematics.withActivities"]').inner_text()
    assert maths == str(meta["counts"]["bySubject"]["Mathematics"]["withActivities"])


def test_plan_shows_activities_and_evidence(page):
    pick(page, "equivalent fractions", TARGET)
    answer(page, HALVES, "no")
    item = page.locator(f'#gt-plan-items .gt-plan__item[data-id="{HALVES}"]')
    item.locator(".gt-activity").first.wait_for()
    text = item.inner_text()
    assert "You'll know it's working when:" in text
    assert "Try this:" in text
    assert NO_ACTIVITIES not in text


# ---- Review Focus (planen): fem lägen specen inte nämner ----

def test_empty_and_no_match_search(page):
    page.fill("#gt-search", "zzzz")
    assert "No skills match" in page.inner_text("#gt-results")
    page.fill("#gt-search", "")
    assert page.locator(".gt-result").count() == 0
    assert page.errors == []


def test_target_without_prereqs(page):
    pick(page, "Ordering Events in Time", NO_PREREQS)
    assert "This skill has no earlier building blocks in the map." in page.inner_text("#gt-check")
    assert plan_ids(page) == [NO_PREREQS]


def test_html_in_name_is_text(page):
    page.fill("#gt-name", "<b>Sam</b>")
    pick(page, "equivalent fractions", TARGET)
    assert page.locator("#gt-check b").count() == 0
    assert "<b>Sam</b>" in page.inner_text("#gt-check")


def test_changing_no_to_yes_updates_plan(page):
    pick(page, "equivalent fractions", TARGET)
    answer(page, HALVES, "no")
    assert plan_ids(page) == [HALVES, TARGET]
    answer(page, HALVES, "yes")
    assert plan_ids(page) == [TARGET]


def test_failed_activity_fetch_never_claims_no_activities(page):
    page.route("**/gap-tracer/data/activities/**", lambda route: route.fulfill(status=500))
    pick(page, "equivalent fractions", TARGET)
    item = page.locator(f'#gt-plan-items .gt-plan__item[data-id="{TARGET}"]')
    item.locator(".gt-error").wait_for()
    assert FETCH_FAILED in item.inner_text()
    assert NO_ACTIVITIES not in item.inner_text()


# ---- Återkoppling: bara ja/nej, aldrig namnet (spec §5) ----

def test_feedback_sends_only_the_four_fields(page):
    sent = []
    page.route("https://example.test/feedback", lambda route: (sent.append(route.request.post_data), route.fulfill(status=200)))
    page.evaluate("document.getElementById('gt-feedback').dataset.telemetryUrl = 'https://example.test/feedback'")
    page.fill("#gt-name", "Sam")
    pick(page, "equivalent fractions", TARGET)
    answer(page, HALVES, "no")
    page.click('#gt-feedback [data-feedback="yes"]')
    page.wait_for_timeout(300)
    assert len(sent) == 1
    body = json.loads(sent[0])
    assert set(body) == {"answer", "skillId", "gapCount", "timestamp"}
    assert body["answer"] == "yes" and body["skillId"] == TARGET and body["gapCount"] == 1
    assert "Sam" not in sent[0]
    assert page.locator(".gt-feedback__thanks").is_visible()


def test_feedback_without_url_makes_no_request(page):
    requests = []
    page.on("request", lambda r: r.method == "POST" and requests.append(r.url))
    page.evaluate("document.getElementById('gt-feedback').dataset.telemetryUrl = ''")
    pick(page, "equivalent fractions", TARGET)
    page.click('#gt-feedback [data-feedback="no"]')
    page.wait_for_timeout(300)
    assert requests == []
    assert page.locator(".gt-feedback__thanks").is_visible()


def test_feedback_is_hidden_when_printing(page):
    pick(page, "equivalent fractions", TARGET)
    page.emulate_media(media="print")
    assert not page.locator("#gt-feedback").is_visible()
    assert page.locator("#gt-plan .gt-disclaimer").is_visible()


# ---- Slutgranskningen ----

def test_print_hides_site_nav(page):
    pick(page, "equivalent fractions", TARGET)
    page.emulate_media(media="print")
    assert page.locator("nav.nav").count() >= 1
    assert not page.locator("nav.nav").first.is_visible()


def go_deeper(page, levels):
    """Svara No på den djupaste byggstenen som har förkunskaper och öppna nästa nivå."""
    for _ in range(levels):
        block = page.locator(".gt-block:has(> .gt-deeper)").last
        block.locator(":scope > .gt-answers .gt-answer[data-answer='no']").click()
        block.locator(":scope > .gt-deeper").click()


def test_deep_layers_do_not_scroll_sideways_on_phone(page):
    page.set_viewport_size({"width": 375, "height": 800})
    pick(page, "equivalent fractions", TARGET)
    go_deeper(page, 4)
    depth = page.evaluate("Math.max(...[...document.querySelectorAll('.gt-block')].map(b => { let d = 0, n = b; while ((n = n.parentElement.closest('.gt-check__list'))) d++; return d; }))")
    assert depth >= 4
    assert page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth") == 0


def test_choosing_a_skill_moves_focus_to_step_2(page):
    pick(page, "equivalent fractions", TARGET)
    assert page.evaluate("document.activeElement.id") == "gt-step-2-title"


def test_focus_moves_into_the_new_layer(page):
    pick(page, "equivalent fractions", TARGET)
    answer(page, HALVES, "no")
    page.locator(f'.gt-block[data-id="{HALVES}"] .gt-deeper').first.click()
    assert page.evaluate(f"document.activeElement.closest('.gt-block')?.dataset.id") == HALF
    assert page.evaluate("document.activeElement.classList.contains('gt-answer')")


def test_yes_after_going_deeper_drops_what_lies_under_it(page):
    pick(page, "equivalent fractions", TARGET)
    answer(page, HALVES, "no")
    page.locator(f'.gt-block[data-id="{HALVES}"] .gt-deeper').first.click()
    answer(page, HALF, "no")
    assert plan_ids(page) == [HALF, HALVES, TARGET]
    answer(page, HALVES, "yes")
    assert plan_ids(page) == [TARGET]
    assert not page.locator(f'.gt-block[data-id="{HALF}"]').first.is_visible()
    answer(page, HALVES, "no")  # tillbaka: svaren därunder finns kvar
    assert plan_ids(page) == [HALF, HALVES, TARGET]


def test_retry_after_failed_fetch(page):
    failing = {"on": True}
    page.route("**/gap-tracer/data/activities/**",
               lambda route: route.fulfill(status=500) if failing["on"] else route.continue_())
    pick(page, "equivalent fractions", TARGET)
    item = page.locator(f'#gt-plan-items .gt-plan__item[data-id="{TARGET}"]')
    item.locator(".gt-error").wait_for()
    failing["on"] = False
    item.locator(".gt-retry").click()
    page.locator(f'#gt-plan-items .gt-plan__item[data-id="{TARGET}"] .gt-activity').first.wait_for()


def test_plan_intro_does_not_overpromise(page):
    pick(page, "equivalent fractions", TARGET)
    intro = page.inner_text(".gt-plan__intro")
    assert "builds on the one before it" not in intro
    assert "after the skills it builds on" in intro


def test_hidden_controls_stay_hidden(page):
    # Sajtens CSS (display: flex/grid på .btn och listor) får inte ta över hidden.
    page.evaluate("document.getElementById('gt-feedback').dataset.telemetryUrl = ''")
    pick(page, "equivalent fractions", TARGET)
    assert not page.locator(f'.gt-block[data-id="{HALVES}"] .gt-deeper').first.is_visible()
    page.click('#gt-feedback [data-feedback="yes"]')
    assert not page.locator(".gt-feedback__buttons").is_visible()


def test_nav_links_to_gap_tracer_in_english_only():
    # Sidan finns bara på engelska, så den svenska menyn ska inte länka dit.
    en = (ROOT / "assets/partials/header-en.html").read_text(encoding="utf-8")
    sv = (ROOT / "assets/partials/header-sv.html").read_text(encoding="utf-8")
    link = '<li><a class="nav__link" href="/gap-tracer/">Gap Tracer</a></li>'
    assert link in en
    # Bredvid det andra interaktiva verktyget, mellan AI or human? och Claude.
    assert en.index('href="/ai-or-human/"') < en.index(link) < en.index('href="/guides/claude/"')
    assert "/gap-tracer/" not in sv
