"""Vakter för översiktssidan Think + AI (/think/), menyvalet och SEO-posterna.

Översiktssidan visar bara verktyg som finns. Kommande verktyg nämns inte vid
namn (Johans beslut 2026-10-27).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HUB = ROOT / "think/index.html"
HEADER = ROOT / "assets/partials/header-en.html"
UNANNOUNCED = ["Flawed Answer", "Side by Side", "Sparring Partner", "Thinking Profile"]


def test_hub_has_one_card_to_thinking_moves():
    html = HUB.read_text(encoding="utf-8")
    cards = re.findall(r'<a class="think-card"[^>]*href="([^"]+)"', html)
    assert cards == ["/thinking-moves/"]


def test_hub_mentions_more_tools_without_names():
    html = HUB.read_text(encoding="utf-8")
    assert "More tools" in html
    for name in UNANNOUNCED:
        assert name not in html, name


def test_menu_link_after_gap_tracer():
    lines = HEADER.read_text(encoding="utf-8").splitlines()
    gap = next(i for i, l in enumerate(lines) if 'href="/gap-tracer/"' in l)
    assert 'href="/think/"' in lines[gap + 1] and ">Think + AI<" in lines[gap + 1]


def test_og_images_absolute():
    for page, png in (("think/index.html", "think-en.png"), ("thinking-moves/index.html", "thinkingmoves-en.png")):
        html = (ROOT / page).read_text(encoding="utf-8")
        m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        assert m and m.group(1) == f"https://choosewise.education/assets/images/brand/og/{png}", page
        assert (ROOT / "assets/images/brand/og" / png).exists(), png


def test_llms_lists_both_pages():
    text = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "https://choosewise.education/think/" in text
    assert "https://choosewise.education/thinking-moves/" in text
