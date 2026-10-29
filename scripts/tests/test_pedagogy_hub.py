"""Vakter för översiktssidan Pedagogy + AI (/pedagogy/), menyvalet och SEO-posterna.

Översiktssidan visar bara verktyg som finns, och kommande verktyg nämns inte
vid namn (samma regel som Think + AI, Johans beslut 2026-10-27). Rubriken
Pedagogy + AI är Johans (2026-10-29).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HUB = ROOT / "pedagogy/index.html"
HEADER = ROOT / "assets/partials/header-en.html"
UNANNOUNCED = ["Retrieval Rhythm", "Two-Minute Debrief", "Unit Studio", "Pedagogy Compass"]


def test_hub_has_one_card_to_lesson_lens():
    html = HUB.read_text(encoding="utf-8")
    assert "<h1>Pedagogy + AI</h1>" in html
    assert re.findall(r'<a class="think-card"[^>]*href="([^"]+)"', html) == ["/lesson-lens/"]


def test_hub_card_icon_exists():
    html = HUB.read_text(encoding="utf-8")
    src = re.search(r'<img class="think-card__icon" src="([^"]+)"', html).group(1)
    assert (ROOT / src.lstrip("/")).exists(), src


def test_hub_names_no_unannounced_tools():
    html = HUB.read_text(encoding="utf-8")
    for name in UNANNOUNCED:
        assert name not in html, name
    assert "More tools" not in html


def test_menu_link_after_think():
    lines = HEADER.read_text(encoding="utf-8").splitlines()
    think = next(i for i, l in enumerate(lines) if 'href="/think/"' in l)
    assert 'href="/pedagogy/"' in lines[think + 1] and ">Pedagogy + AI<" in lines[think + 1]


def test_og_images_absolute():
    for page, png in (("pedagogy/index.html", "pedagogy-en.png"), ("lesson-lens/index.html", "lessonlens-en.png")):
        html = (ROOT / page).read_text(encoding="utf-8")
        m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        assert m and m.group(1) == f"https://choosewise.education/assets/images/brand/og/{png}", page
        assert (ROOT / "assets/images/brand/og" / png).exists(), png


def test_llms_lists_both_pages():
    text = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "https://choosewise.education/pedagogy/" in text
    assert "https://choosewise.education/lesson-lens/" in text
