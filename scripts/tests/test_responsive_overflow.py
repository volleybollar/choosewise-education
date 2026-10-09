"""Ingen sida får scrolla i sidled på en telefon.

Täcker Evidence-sidorna och bloggen. Listan växer när fler sidor rättas —
en sweep 2026-10-09 hittade 19 sidor med överflöd vid 320 px.

Varför ett renderingstest bland 743 statiska: regressionen som gav upphov
till den här filen passerade hela sviten. `white-space: nowrap` lades på
`.band-none` för att hindra "no EEF strand" att brytas till två rader, och
gjorde därmed rutnätskolumnens min-content till hela frasens bredd —
`grid-template-columns: 1fr 1fr 1fr` kan inte krympa under min-content, så
dokumentet blev upp till 161 px för brett. Ingen statisk vakt kan se det;
bredden finns först när webbläsaren räknat.

Bredderna mäts per sidladdning, inte per omladdning — CSS:en är responsiv,
så det räcker att ändra viewporten. 320 px är den smalaste bredd värd att
hålla (iPhone SE); de breda finns med därför att samma nowrap sprängde
sidan även vid 1024 px, på kort vars band är längre ("no independent
meta-analysis"). En vakt som bara mätte mobil hade missat det.
"""
from __future__ import annotations

import functools
import http.server
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
WIDTHS = (320, 390, 768, 1024)

PAGES = (
    ["evidence/"]
    + sorted(f"evidence/{d.name}/" for d in (ROOT / "evidence").iterdir()
             if d.is_dir() and d.name != "data")
    + ["blog/", "sv/blog/"]
    + sorted(f"{d}/posts/{f.name}" for d in ("blog", "sv/blog")
             for f in (ROOT / d / "posts").glob("*.html"))
)

MEASURE = "() => document.documentElement.scrollWidth - document.documentElement.clientWidth"


@pytest.fixture(scope="module")
def site():
    """Lokal server: sidorna hämtar sina kort ur evidence/data/*.json, så
    file:// räcker inte."""
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


def test_no_page_scrolls_sideways(site, browser):
    page = browser.new_page(viewport={"width": WIDTHS[0], "height": 800})
    try:
        bad = []
        for rel in PAGES:
            page.goto(f"{site}/{rel}", wait_until="networkidle")
            for width in WIDTHS:
                page.set_viewport_size({"width": width, "height": 800})
                overflow = page.evaluate(MEASURE)
                if overflow > 0:
                    bad.append(f"{rel} @{width}px sticker ut {overflow} px")
        assert not bad, "\n".join(bad)
    finally:
        page.close()


LINES = """(sel) => [...document.querySelectorAll(sel)].map(el => {
  const cs = getComputedStyle(el);
  const inner = el.offsetHeight
    - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom)
    - parseFloat(cs.borderTopWidth) - parseFloat(cs.borderBottomWidth);
  return Math.round(inner / parseFloat(cs.lineHeight));
})"""


MAX_BAND_LINES = 2


def test_the_band_pill_does_not_blow_out_on_desktop(site, browser):
    """Det `white-space: nowrap` fanns till för, utan dess bieffekt.

    Nowrap löste rätt problem på fel sätt: det gjorde rutnätskolumnens
    min-content till hela frasens bredd och sprängde sidan. Borttaget
    bryts "no EEF strand" i stället till fem rader om kortet är för smalt.

    Gränsen är två rader, inte en: "no EEF strand" står på en rad vid alla
    bredder, medan den längre "no independent meta-analysis found" tar två
    och ser bra ut så. Femradersfallet är felet.

    Två saker håller bandet inom gränsen, och vakten bryr sig inte om
    vilken: kortet är brett nog (minbredd 360 px) ELLER container queryn
    har staplat metric-blocket. Verifierat rött när BÅDA tas bort — då
    blir bandet fem rader. Vakten mäter kravet, inte mekanismen, så
    CSS:en får byggas om fritt så länge bandet håller sig inom två rader.
    """
    page = browser.new_page(viewport={"width": 1024, "height": 800})
    try:
        bad = []
        for rel in ("evidence/ai-literacy/", "evidence/feedback/"):
            page.goto(f"{site}/{rel}", wait_until="networkidle")
            lines = page.evaluate(LINES, ".band-none")
            assert lines, f"{rel}: inga .band-none att mäta — vakten vore tom"
            if max(lines) > MAX_BAND_LINES:
                bad.append(f"{rel}: band på {max(lines)} rader")
        assert not bad, "\n".join(bad)
    finally:
        page.close()


POSTS = [p for p in PAGES if "/posts/" in p]

LONGEST_WORD = """() => {
  const h = document.querySelector('.post__header h1');
  if (!h) return null;
  const probe = document.createElement('span');
  probe.style.cssText =
    'position:absolute;visibility:hidden;white-space:nowrap;font:' + getComputedStyle(h).font;
  document.body.appendChild(probe);
  let widest = 0, word = '';
  for (const w of h.textContent.trim().split(/\\s+/)) {
    probe.textContent = w;
    const px = probe.getBoundingClientRect().width;
    if (px > widest) { widest = px; word = w; }
  }
  probe.remove();
  return {widest: Math.round(widest), room: h.clientWidth, word};
}"""


def test_a_post_title_never_breaks_mid_word_on_a_phone(site, browser):
    """`overflow-wrap: break-word` hindrar överflödet men delar ordet.

    Sajten heter choosewise.education — ett enda ord, 351 px brett vid
    rubrikens 36 px, i en 272 px spalt. Utan den här vakten läser
    rubriken "choosewise.educ / ation". Brytningen är inte ett fel i
    sig, den är nätet; kravet är att nätet inte ska behöva användas på
    sajtens eget namn.
    """
    page = browser.new_page(viewport={"width": WIDTHS[0], "height": 800})
    try:
        bad = []
        for rel in POSTS:
            page.goto(f"{site}/{rel}", wait_until="networkidle")
            m = page.evaluate(LONGEST_WORD)
            assert m, f"{rel}: ingen .post__header h1 — vakten vore tom"
            if m["widest"] > m["room"]:
                bad.append(f"{rel}: “{m['word']}” är {m['widest']} px "
                           f"i en {m['room']} px spalt")
        assert not bad, "\n".join(bad)
    finally:
        page.close()
