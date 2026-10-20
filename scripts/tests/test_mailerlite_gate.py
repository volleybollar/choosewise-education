"""E-postgrinden (assets/js/mailerlite-gate.js) i en riktig webbläsare.

POST:en till MailerLite fångas med page.route och läses fält för fält:
det är den som avgör vad Johan får veta om prenumeranten. Testsidan är
scripts/tests/fixtures/gate.html, så vakten är oberoende av sajtens sidor.
"""
from __future__ import annotations

import functools
import http.server
import socketserver
import threading
from pathlib import Path
from urllib.parse import parse_qs

import pytest

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = "/scripts/tests/fixtures/gate.html"
ML = "**/assets.mailerlite.com/**"


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
def page(browser):
    ctx = browser.new_context()
    p = ctx.new_page()
    p.posts = []      # fångade MailerLite-POST:ar, som dict fält -> värde
    p.pdf_hits = []   # PDF-adresser webbläsaren försökte öppna

    def on_ml(route):
        p.posts.append({k: v[0] if v else "" for k, v in
                        parse_qs(route.request.post_data or "", keep_blank_values=True).items()})
        route.fulfill(status=200, body="")

    def on_pdf(route):
        p.pdf_hits.append(route.request.url)
        route.fulfill(status=200, body="%PDF-1.4", headers={"content-type": "application/pdf"})

    p.route(ML, on_ml)
    p.route("**/*.pdf", on_pdf)
    yield p
    ctx.close()


def submit(page, gate="#gate-a", email="test@school.edu", role=None):
    page.click(gate)
    page.wait_for_selector(".modal-backdrop--open")
    page.fill("#gate-email", email)
    if role is not None:
        page.select_option("select[name=role]", role)
    page.click(".modal__submit")
    page.wait_for_selector(".modal__success--visible")


def test_payload_carries_source_role_and_pdf(page, site):
    page.goto(f"{site}{FIXTURE}?src=yt")
    submit(page, role="teacher")
    body = page.posts[-1]
    assert body["fields[signup_source]"] == "yt"
    assert body["fields[role]"] == "teacher"
    assert body["fields[pdf_url]"] == "https://choosewise.education/assets/pdfs/free/ai-or-human-en.pdf"
    assert body["fields[requested_guide]"] == "ai-or-human-en"
    assert body["fields[email]"] == "test@school.edu"


def test_source_survives_navigation(page, site):
    page.goto(f"{site}{FIXTURE}?src=ig")
    page.goto(f"{site}{FIXTURE}")
    submit(page, gate="#gate-b")
    assert page.posts[-1]["fields[signup_source]"] == "ig"


@pytest.mark.parametrize("query", ["", "?src=%3Cscript%3E", "?src=" + "a" * 21])
def test_source_defaults_to_site_and_is_sanitised(page, site, query):
    page.goto(f"{site}{FIXTURE}{query}")
    submit(page)
    assert page.posts[-1]["fields[signup_source]"] == "site"


def test_role_is_optional(page, site):
    page.goto(f"{site}{FIXTURE}")
    submit(page)
    assert page.posts[-1]["fields[role]"] == ""


def test_download_offered_when_post_fails(page, site):
    page.unroute(ML)
    page.route(ML, lambda route: route.abort())
    page.goto(f"{site}{FIXTURE}")
    submit(page)
    link = page.locator(".modal__success a")
    assert link.is_visible()
    assert link.get_attribute("href") == "/assets/pdfs/free/ai-or-human-en.pdf"


def test_success_copy_does_not_claim_email_was_sent(page, site):
    page.goto(f"{site}{FIXTURE}")
    submit(page)
    text = page.inner_text(".modal__success")
    assert "We've sent" not in text
    assert "Confirm your email" in text


def test_returning_subscriber_skips_the_modal(page, site):
    page.goto(f"{site}{FIXTURE}")
    submit(page)
    assert page.evaluate("localStorage.getItem('cw-subscribed')") == "1"
    page.goto(f"{site}{FIXTURE}")
    with page.expect_request("**/teachers-en.pdf"):
        page.click("#gate-b")
    assert len(page.posts) == 1
    assert any(u.endswith("/assets/pdfs/prompts/teachers-en.pdf") for u in page.pdf_hits)


def test_email_is_never_stored_in_the_browser(page, site):
    page.goto(f"{site}{FIXTURE}")
    submit(page, email="secret@school.edu")
    dump = page.evaluate("JSON.stringify({...localStorage}) + JSON.stringify({...sessionStorage})")
    assert "secret@school.edu" not in dump


def test_gate_still_works_when_storage_throws(page, site):
    page.add_init_script("""
      for (const s of [window.localStorage, window.sessionStorage]) {
        Object.getPrototypeOf(s).getItem = () => { throw new Error('blocked'); };
        Object.getPrototypeOf(s).setItem = () => { throw new Error('blocked'); };
      }
    """)
    page.goto(f"{site}{FIXTURE}?src=yt")
    submit(page)
    assert page.posts[-1]["fields[email]"] == "test@school.edu"
