"""Vakter för översiktssidan Study + AI (/study/), menyvalet och SEO-posterna.

Översiktssidan visar bara verktyg som finns, och kommande verktyg nämns inte
vid namn (samma regel som Think + AI och Pedagogy + AI). Menyvalet står
direkt efter Pedagogy + AI.
Spec: docs/superpowers/specs/2026-11-12-study-moves-design.md.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HUB = ROOT / "study/index.html"
HEADER = ROOT / "assets/partials/header-en.html"
# Förslag 2–5 på Study + AI-sidan, som inte är byggda (specens Non-goals).
UNANNOUNCED = ["Test Countdown", "Study Experiment", "Homework Upgrade", "Study Season"]


def test_hub_has_one_card():
    html = HUB.read_text(encoding="utf-8")
    assert "<h1>Study + AI</h1>" in html
    assert re.findall(r'<a class="think-card"[^>]*href="([^"]+)"', html) == ["/study-moves/"]


def test_hub_card_icon_exists():
    html = HUB.read_text(encoding="utf-8")
    srcs = re.findall(r'<img class="think-card__icon" src="([^"]+)"', html)
    assert srcs == ["/study-moves/icons/study-moves.svg"]
    icon = ROOT / srcs[0].lstrip("/")
    assert icon.exists()
    svg = icon.read_text(encoding="utf-8")
    # Samma Blueprint-stil som de andra verktygsikonerna: 48×48, linjer i
    # accentblått och en detalj i koppar.
    assert 'viewBox="0 0 48 48"' in svg and 'stroke="#0B3A6F"' in svg and "#C2793A" in svg
    assert set(re.findall(r"#[0-9A-Fa-f]{6}", svg)) == {"#0B3A6F", "#C2793A"}


def test_hub_names_no_unannounced_tools():
    html = HUB.read_text(encoding="utf-8")
    for name in UNANNOUNCED:
        assert name not in html, name
    assert "More tools" not in html


def test_menu_link_after_pedagogy():
    lines = HEADER.read_text(encoding="utf-8").splitlines()
    pedagogy = next(i for i, l in enumerate(lines) if 'href="/pedagogy/"' in l)
    assert 'href="/study/"' in lines[pedagogy + 1] and ">Study + AI<" in lines[pedagogy + 1]


def test_og_images_absolute():
    for page, png in (("study/index.html", "study-en.png"), ("study-moves/index.html", "studymoves-en.png")):
        html = (ROOT / page).read_text(encoding="utf-8")
        m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        assert m and m.group(1) == f"https://choosewise.education/assets/images/brand/og/{png}", page
        assert (ROOT / "assets/images/brand/og" / png).exists(), png
        assert (ROOT / "assets/images/brand/og" / png.replace(".png", ".svg")).exists(), png


def test_llms_lists_both_pages():
    text = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "## Study + AI" in text
    section = text[text.index("## Study + AI"):]
    section = section[:section.find("\n## ", 1)] if "\n## " in section[1:] else section
    assert "https://choosewise.education/study/" in section
    assert "https://choosewise.education/study-moves/" in section
    # Avsnittet står efter Pedagogy + AI.
    assert text.index("## Pedagogy + AI") < text.index("## Study + AI")


def test_sitemap_lists_both_pages():
    text = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for url in ("https://choosewise.education/study/", "https://choosewise.education/study-moves/"):
        assert f"<loc>{url}</loc>" in text, url


def test_both_pages_have_seo_block():
    for page, url in (("study/index.html", "/study/"), ("study-moves/index.html", "/study-moves/")):
        html = (ROOT / page).read_text(encoding="utf-8")
        assert f'<link rel="canonical" href="https://choosewise.education{url}">' in html, page
        assert '<link rel="icon" href="/favicon.svg" type="image/svg+xml">' in html, page
