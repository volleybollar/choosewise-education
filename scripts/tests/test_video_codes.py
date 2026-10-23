"""Vakter för sidan Visual codes for video (/visual-codes/video/).

Datafilen är sidans enda källa: varje kort, varje kopieringsknapp och varje
mediafil byggs från den. Testerna här säkrar att den är hel och — viktigast —
att prompten på varje kort är exakt den som gav klippet. Annars ljuger sidan.
"""
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "visual-codes/video/codes-video-en.json"
# Genereringsloggen ligger utanför repot (testmappen). Saknas den hoppas
# jämförelsen över — på en annan maskin finns den inte.
JOBS = Path.home() / "Projekt/Choosewise/visual-codes-video-test/jobs.tsv"

ORDER = ["see-the-invisible", "processes", "film-language",
         "doesnt-work-yet", "beyond-the-classroom"]
STATUSES = {"works", "partial", "fails"}


def load():
    return json.loads(DATA.read_text(encoding="utf-8"))


def all_codes():
    return [(s, c) for s in load()["sections"] for c in s["codes"]]


def test_sections_in_the_agreed_order():
    assert [s["id"] for s in load()["sections"]] == ORDER


def test_every_code_has_required_fields_and_valid_status():
    slugs = []
    for _, c in all_codes():
        assert c["code"].startswith("/"), c["code"]
        assert re.fullmatch(r"[a-z0-9-]+", c["slug"]), c["slug"]
        assert c["status"] in STATUSES, (c["code"], c["status"])
        assert c["prompt"].startswith(c["code"]), c["code"]
        assert c["description"].strip(), c["code"]
        assert c["source_clip"] and c["source_start"], c["code"]
        slugs.append(c["slug"])
    assert len(slugs) == len(set(slugs)), "slug måste vara unik"


def test_fails_only_in_the_doesnt_work_box():
    for s, c in all_codes():
        if s["id"] == "doesnt-work-yet":
            assert c["status"] == "fails", c["code"]
        else:
            assert c["status"] != "fails", c["code"]


def test_lightshift_and_seasons_exist_and_work():
    by_code = {c["code"]: c for _, c in all_codes()}
    for code in ("/lightshift", "/seasons"):
        assert by_code[code]["status"] == "works"


def normalised_prompts():
    """Prompterna ur jobs.tsv i samma form som på sidan.
    Higgsfield-raderna skrev tillägg som '/orbit + "The camera …"',
    kie-raderna som '/reverse Play …'. Båda blir '/kod tillägg'."""
    prompts = set()
    for line in JOBS.read_text(encoding="utf-8").splitlines():
        cols = line.split("\t")
        if len(cols) < 2:
            continue
        p = re.sub(r' \+ "(.*)"$', r" \1", cols[1].strip())
        prompts.add(p)
    return prompts


def test_prompts_match_what_was_sent():
    if not JOBS.exists():
        pytest.skip("jobs.tsv finns bara på Johans maskin")
    sent = normalised_prompts()
    wrong = [c["code"] for _, c in all_codes() if c["prompt"] not in sent]
    assert wrong == [], f"prompter som aldrig skickades: {wrong}"


# ── Media (byggs av scripts/build-video-codes-media.py) ──────────────────────
import json as _json
import subprocess

MEDIA = ROOT / "visual-codes/video/media"
MAX_CLIP = 900_000          # byte per klipp
MAX_TOTAL = 40_000_000      # byte all video på sidan


def media_files(slug):
    return [MEDIA / f"{slug}.mp4", MEDIA / f"{slug}-poster.webp", MEDIA / f"{slug}-start.webp"]


def test_every_code_has_its_three_media_files():
    missing = [str(p.relative_to(ROOT)) for _, c in all_codes()
               for p in media_files(c["slug"]) if not p.exists()]
    assert missing == []


def test_each_clip_is_within_budget():
    big = {c["slug"]: (MEDIA / f"{c['slug']}.mp4").stat().st_size
           for _, c in all_codes()
           if (MEDIA / f"{c['slug']}.mp4").stat().st_size > MAX_CLIP}
    assert big == {}


def test_total_video_within_budget():
    total = sum((MEDIA / f"{c['slug']}.mp4").stat().st_size for _, c in all_codes())
    assert total <= MAX_TOTAL, total


def test_clips_are_960_wide_for_sharp_retina_cards():
    """Johan 2026-10-23: kortet är ~500 CSS-px brett, på retina behövs ~1000 px."""
    for _, c in all_codes():
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width",
             "-of", "csv=p=0", str(MEDIA / f"{c['slug']}.mp4")],
            capture_output=True, text=True, check=True).stdout.strip()
        assert out == "960", (c["slug"], out)


def test_reverse_sits_in_the_box():
    """Johan 2026-10-23: tre motiv blev aldrig verklighetstrogna."""
    box = next(s for s in load()["sections"] if s["id"] == "doesnt-work-yet")
    assert "/reverse" in [c["code"] for c in box["codes"]]


def test_clips_have_no_audio_track_and_are_h264():
    for _, c in all_codes():
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name",
             "-of", "json", str(MEDIA / f"{c['slug']}.mp4")],
            capture_output=True, text=True, check=True).stdout
        streams = _json.loads(out)["streams"]
        assert [s["codec_type"] for s in streams] == ["video"], c["slug"]
        assert streams[0]["codec_name"] == "h264", c["slug"]


# ── I webbläsaren: korten, videon och tillgängligheten ───────────────────────
import functools
import http.server
import socketserver
import threading

PAGE = "visual-codes/video/"


@pytest.fixture(scope="module")
def site():
    """Lokal server: sidan hämtar korten ur JSON, så file:// räcker inte."""
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    class Server(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
        daemon_threads = True

    srv = Server(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()


@pytest.fixture(scope="module")
def browser():
    """Riktig Chrome, inte Playwrights Chromium: den senare saknar H.264 och
    kan därför aldrig spela klippen — testerna om uppspelning vore meningslösa."""
    pw = pytest.importorskip("playwright.sync_api").sync_playwright().start()
    try:
        b = pw.chromium.launch(channel="chrome")
    except Exception:
        pw.stop()
        pytest.skip("Google Chrome saknas — uppspelningstesterna kräver H.264")
    yield b
    b.close()
    pw.stop()


def open_page(browser, site, **ctx):
    context = browser.new_context(viewport={"width": 1280, "height": 900}, **ctx)
    page = context.new_page()
    page.goto(f"{site}/{PAGE}", wait_until="networkidle")
    page.wait_for_selector(".vcv-card")
    return context, page


def test_page_renders_one_card_per_code(site, browser):
    context, page = open_page(browser, site)
    try:
        assert page.locator(".vcv-card").count() == len(all_codes())
    finally:
        context.close()


def test_no_failed_requests(site, browser):
    """Varje video, poster och startbild som sidan pekar på måste finnas."""
    context, page = open_page(browser, site)
    try:
        bad = page.evaluate("""async () => {
          const urls = new Set();
          document.querySelectorAll('video').forEach(v => { urls.add(v.src); urls.add(v.poster); });
          document.querySelectorAll('.vcv-start img').forEach(i => urls.add(i.src));
          const out = [];
          for (const u of urls) {
            const r = await fetch(u, { method: 'HEAD' });
            if (!r.ok) out.push(r.status + ' ' + u);
          }
          return out;
        }""")
        assert bad == []
    finally:
        context.close()


def test_copy_button_carries_the_full_prompt(site, browser):
    prompt = next(c["prompt"] for _, c in all_codes() if c["slug"] == "selectivecolor")
    context, page = open_page(browser, site)
    try:
        got = page.get_attribute('.vcv-card[data-slug="selectivecolor"] .vc-card__code', "data-copy")
        assert got == prompt
    finally:
        context.close()


def test_only_visible_videos_play(site, browser):
    context, page = open_page(browser, site)
    try:
        page.locator('.vcv-card[data-slug="lightshift"]').scroll_into_view_if_needed()
        page.wait_for_timeout(2500)
        state = page.evaluate("""() => [...document.querySelectorAll('video')].map(v => {
          const r = v.getBoundingClientRect();
          return { playing: !v.paused, visible: r.bottom > 0 && r.top < innerHeight };
        })""")
        playing = [s for s in state if s["playing"]]
        assert playing, "minst ett synligt klipp ska spela"
        assert all(s["visible"] for s in playing), "ett klipp utanför skärmen spelar"
    finally:
        context.close()


def test_reduced_motion_means_no_autoplay(site, browser):
    context, page = open_page(browser, site, reduced_motion="reduce")
    try:
        page.locator('.vcv-card[data-slug="lightshift"]').scroll_into_view_if_needed()
        page.wait_for_timeout(1500)
        assert page.evaluate("() => [...document.querySelectorAll('video')].every(v => v.paused)")
    finally:
        context.close()


def test_video_toggles_with_keyboard(site, browser):
    context, page = open_page(browser, site, reduced_motion="reduce")
    try:
        video = page.locator(".vc-hero .vcv-video").first
        video.focus()
        page.keyboard.press("Space")
        page.wait_for_timeout(800)
        assert video.evaluate("v => !v.paused")
        page.keyboard.press("Space")
        page.wait_for_timeout(300)
        assert video.evaluate("v => v.paused")
    finally:
        context.close()


def test_videos_side_by_side_share_top_and_bottom(site, browser):
    """Johan 2026-10-23: två kort bredvid varandra ska ha klippen på samma
    vågräta linjer — en Add-rad eller ett märke i det ena kortet får inte
    skjuta ner dess video."""
    context, page = open_page(browser, site)
    try:
        rows = page.evaluate("""() => {
          const out = [];
          document.querySelectorAll('.vc-grid').forEach(grid => {
            const byRow = {};
            grid.querySelectorAll('.vcv-card').forEach(card => {
              const key = Math.round(card.getBoundingClientRect().top);
              const v = card.querySelector('.vcv-media').getBoundingClientRect();
              (byRow[key] = byRow[key] || []).push([card.dataset.slug, Math.round(v.top), Math.round(v.bottom)]);
            });
            Object.values(byRow).forEach(r => { if (r.length > 1) out.push(r); });
          });
          return out;
        }""")
        assert rows, "inga rader med flera kort — testet mäter inget"
        bad = [r for r in rows if len({t for _, t, _ in r}) > 1 or len({b for _, _, b in r}) > 1]
        assert bad == [], bad[:3]
    finally:
        context.close()
