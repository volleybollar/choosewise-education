"""Vakter för communitysidan (/community/).

Sidan är ett mellansteg som skickar educators vidare till Choosewise-
communityt på Skool. Den byggs färdig nu men är dold tills Skool öppnar för
alla: noindex, utanför sajtkartan och olänkad från resten av sajten (Johans
beslut 2026-11-11). Lanseringen följer checklistan i docs/community-launch.md,
och där står vilka av vakterna nedan som ska ändras den dagen.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "community" / "index.html"
SKOOL = "https://www.skool.com/choosewise-7103"


def html():
    return PAGE.read_text(encoding="utf-8")


def section(sid):
    m = re.search(rf'<section[^>]*id="{sid}".*?</section>', html(), re.S)
    assert m, sid
    return m.group(0)


def test_page_is_noindex():
    assert '<meta name="robots" content="noindex,nofollow">' in html()
    assert 'rel="canonical"' not in html()


def test_hero_headline_and_source():
    hero = section("cm-hero")
    assert "Students are 2× more likely to use AI to do the work for them without clear guidance." in hero
    for s in ["ThinkYoung", "OpenAI", "2026", "5,000", "13–19", "10 European countries", "36%", "18%"]:
        assert s in hero, s


def test_join_button_in_hero():
    assert f'href="{SKOOL}"' in section("cm-hero")
    assert "target=" not in section("cm-hero")


SECTIONS = ["cm-hero", "cm-gap", "cm-why", "cm-inside", "cm-who", "cm-close"]


def css():
    return (ROOT / "assets/css/community.css").read_text(encoding="utf-8")


def img_alt(src_part):
    m = re.search(rf'<img[^>]*src="[^"]*{src_part}[^"]*"[^>]*>', html())
    assert m, src_part
    alt = re.search(r'alt="([^"]*)"', m.group(0))
    assert alt, f"{src_part} saknar alt"
    return alt.group(1)


def test_sections_in_order():
    positions = [html().index(f'id="{s}"') for s in SECTIONS]
    assert positions == sorted(positions)


def test_gap_figures():
    for s in ["43%", "36%", "21%", "Students are not waiting for a policy."]:
        assert s in section("cm-gap"), s


def test_johans_three_points():
    why = section("cm-why")
    for s in ["Become the educator who can give that guidance", "Learn at your own pace",
              "Learn with other educators", "By educators, for educators"]:
        assert s in why, s


def test_whats_inside_has_four_items_and_no_research_briefs():
    inside = section("cm-inside")
    for s in ["The course", "The guide library", "Weekly live Q&amp;A", "Tried &amp; Tested", "and more"]:
        assert s in inside, s
    assert "research" not in html().lower()


def test_bio_wording():
    who = section("cm-who")
    assert "eleven leading professional development in EdTech" in who
    assert "More than 10,000 teachers and principals trained, the last four years with AI at the centre." in who


def test_close_has_promo_and_second_button():
    close = section("cm-close")
    assert "community-web.webp" in close and f'href="{SKOOL}"' in close
    assert html().count(f'href="{SKOOL}"') == 2


def test_images_have_meaningful_alt():
    # Säljbilden bär communityts fyra delar som text i bilden.
    promo = img_alt("community-web")
    for s in ["Course", "Guides", "Prompts", "Network"]:
        assert s in promo, s
    assert img_alt("portrait-johan-lindstrom") == "Portrait of Johan Lindström"


def test_no_price_and_no_serif():
    assert "$" not in html() and "/month" not in html()
    for s in ["Instrument Serif", "--font-quote"]:
        assert s not in css() and s not in html(), s


def test_portrait_crop_anchored_to_top():
    assert "object-position: center top" in css()


def test_og_card_exists_and_is_referenced():
    # Länken delas till founding members innan sidan lanseras.
    assert '<meta property="og:image" content="https://choosewise.education/assets/images/brand/og/community-en.png">' in html()
    assert '<meta property="og:title"' in html() and '<meta property="og:description"' in html()
    for ext in ("svg", "png"):
        assert (ROOT / f"assets/images/brand/og/community-en.{ext}").exists(), ext


# ---- Rättningar efter slutgranskningen -------------------------------------

LINK = re.compile(r'''(?:choosewise\.education|["'(=]|\.\.)/community(?![\w-])|["'(]community/''')
SCANNED = (".html", ".md", ".js", ".json", ".xml", ".txt", ".css")


def links_to_community(text):
    return bool(LINK.search(text))


def test_link_pattern_catches_every_form():
    for text in ['href="/community/"', 'href="/community"', 'href="community/"',
                 'href="../community/"', "url = '/community/'", "[join](/community/)",
                 "https://choosewise.education/community", "choosewise.education/community/"]:
        assert links_to_community(text), text
    for text in ["https://www.skool.com/community/x", 'href="/community-guidelines/"',
                 "/* /community/ — sidlokala stilar */"]:
        assert not links_to_community(text), text


def test_page_is_not_linked_anywhere():
    # Fram till lanseringen får ingenting på sajten peka hit: sidor, partials,
    # blogginläggens .md, skript som bygger länkar, data, sajtkarta, llms, robots.
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                             text=True, check=True).stdout.split("\n")
    hits = [p for p in tracked
            if p.endswith(SCANNED)
            and not p.startswith(("community/", "_unpublished/", "scripts/"))
            and links_to_community((ROOT / p).read_text(encoding="utf-8"))]
    assert not hits, hits


sys.path.insert(0, str(Path(__file__).parent))
from conftest_debrief import browser, site  # noqa: E402,F401


def boxes(site, browser, width, selector):
    ctx = browser.new_context(viewport={"width": width, "height": 900})
    p = ctx.new_page()
    p.goto(f"{site}/community/", wait_until="networkidle")
    found = p.eval_on_selector_all(
        selector, "els => els.map(e => { const r = e.getBoundingClientRect();"
                  " return [Math.round(r.top + scrollY), Math.round(r.left)]; })")
    ctx.close()
    return found


def test_whats_inside_is_two_by_two_on_desktop(site, browser):
    found = boxes(site, browser, 1280, "#cm-inside .cm-item")
    assert len({t for t, _ in found}) == 2 and len({l for _, l in found}) == 2, found


def test_gap_figures_never_leave_one_alone(site, browser):
    for width in (320, 430, 768, 1280):
        rows = len({t for t, _ in boxes(site, browser, width, ".cm-stat")})
        assert rows in (1, 3), (width, rows)


def test_close_band_meets_the_footer(site, browser):
    ctx = browser.new_context(viewport={"width": 1280, "height": 900})
    p = ctx.new_page()
    p.goto(f"{site}/community/", wait_until="networkidle")
    p.wait_for_selector("footer")
    gap = p.evaluate("() => document.querySelector('footer').getBoundingClientRect().top"
                     " - document.querySelector('#cm-close').getBoundingClientRect().bottom")
    ctx.close()
    assert abs(gap) < 1, gap
