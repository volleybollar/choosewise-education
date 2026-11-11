"""Vakter för communitysidan (/community/).

Sidan är ett mellansteg som skickar educators vidare till Choosewise-
communityt på Skool. Den byggs färdig nu men är dold tills Skool öppnar för
alla: noindex, utanför sajtkartan och olänkad från resten av sajten (Johans
beslut 2026-11-11). Lanseringen följer checklistan i docs/community-launch.md,
och där står vilka av vakterna nedan som ska ändras den dagen.
"""
import re
import subprocess
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


def test_page_is_not_linked_anywhere():
    # Fram till lanseringen får ingenting på sajten peka hit.
    tracked = subprocess.run(
        ["git", "ls-files", "*.html"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.split()
    files = [ROOT / p for p in tracked
             if not p.startswith(("community/", "_unpublished/"))]
    files += sorted((ROOT / "assets/partials").glob("*"))
    files += [ROOT / "sitemap.xml", ROOT / "llms.txt", ROOT / "robots.txt"]
    for path in files:
        text = path.read_text(encoding="utf-8")
        for needle in ("/community/", "choosewise.education/community"):
            assert needle not in text, f"{path.relative_to(ROOT)} länkar till sidan"


def test_hero_headline_and_source():
    hero = section("cm-hero")
    assert "Students are 2× more likely to use AI to do the work for them without clear guidance." in hero
    for s in ["ThinkYoung", "OpenAI", "2026", "5,000", "13–19", "10 European countries", "36%", "18%"]:
        assert s in hero, s


def test_join_button_in_hero():
    assert f'href="{SKOOL}"' in section("cm-hero")
    assert "target=" not in section("cm-hero")
