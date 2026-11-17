"""Vakter för översiktssidan What teachers do (/what-teachers-do-354716b7/).

Sidan är bara för Skool-medlemmar: den nås via en dold länk och länkas aldrig
från resten av sajten. Den är handskriven HTML med egen CSS och utan JavaScript
(utom sajtens gemensamma include.js för sidhuvud och sidfot). Siffrorna och
texterna kommer från spec del A (A1–A8).
Spec: docs/superpowers/specs/2026-11-14-what-teachers-do-design.md.
"""
import re
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLUG = "what-teachers-do-354716b7"
PAGE = ROOT / SLUG / "index.html"
CSS = ROOT / "assets/css/what-teachers-do.css"
QL = "/quality-ladder-ec1c2f8c/"

SECTIONS = ["wt-time", "wt-stress", "wt-ai", "wt-rules", "wt-tasks", "wt-parts", "wt-sources"]

TASKS = ["Planning teaching", "Teaching", "Keeping order in class",
         "Marking, assessing and evaluating knowledge", "Colleagues and meetings",
         "Individual support", "Administration and documentation",
         "Creating and adapting materials", "Student welfare and support measures",
         "Communicating with parents", "Generating ideas"]
CLASSROOM = "https://www.skool.com/choosewise-7103/classroom"
PARTS = ["Quality Ladder", "Paperwork Pack", "Barrier Planner", "The course", "Ideas first"]


def html():
    return PAGE.read_text(encoding="utf-8")


def section(sid):
    m = re.search(rf'<section[^>]*id="{sid}".*?</section>', html(), re.S)
    assert m, sid
    return m.group(0)


def text_of(fragment):
    """Texten i ett HTML-stycke: taggar borta, tecken avkodade, blanksteg samlade."""
    no_tags = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", unescape(no_tags)).strip()


def tasks():
    """De elva uppgiftsraderna i #wt-tasks som HTML-bitar."""
    return re.findall(r'<li class="wt-task">.*?</li>\s*(?=<li class="wt-task">|</ol>)',
                      section("wt-tasks"), re.S)


def new_cell(row):
    m = re.search(r'<div class="wt-task__new">(.*?)</div>', row, re.S)
    assert m
    return m.group(1)


# ───── Sidans byggstenar ─────

def test_sections_in_order():
    assert re.findall(r'<section[^>]*id="(wt-[a-z]+)"', html()) == SECTIONS


def test_hero():
    page = html()
    assert '<span class="eyebrow">For Choosewise members · All school stages</span>' in page
    assert "<h1>What teachers do</h1>" in page
    assert ("Teachers have too little time, and new teachers also lack experience. This package "
            "goes through the eleven tasks that fill a teacher's week, shows where the time and "
            "the stress sit, and gives each task a way to do it with less work and teaching that "
            "is as good or better.") in text_of(page)


def test_time_table():
    block = section("wt-time")
    assert ">Where the time goes</h2>" in block
    table = re.search(r"<table.*?</table>", block, re.S).group(0)
    cells = [text_of(c) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", table, re.S)]
    for header in ("OECD average", "Sweden", "United States"):
        assert header in cells, header
    for n in ("22.7 19.2 28.1 7.4 7.2 7.2 4.6 3.8 4.6 3.1 3.4 3.2 3.0 2.9 2.9 2.6 2.7 3.6 "
              "1.8 1.8 2.0 41.0 44.0 45.3").split():
        assert n in cells, n
    for task in ("Teaching", "Planning lessons", "Marking student work", "Working with colleagues",
                 "Administration", "Counselling and guidance", "Parents and guardians",
                 "Total working time"):
        assert task in cells, task
    assert "TALIS 2024" in text_of(block)
    assert ("Tasks are measured one by one and overlap, so they add up to more than the total. "
            "Read them as sizes relative to each other. England did not take part in TALIS 2024."
            ) in text_of(block)
    box = text_of(block[block.index("Across all school stages"):])
    for n in ("49", "39", "52", "38", "46.9"):
        assert n in box, n
    assert ("These surveys cover all school stages, and the US ones ask about a typical week; TALIS "
            "asks about the last week in lower secondary, so the totals differ.") in box


def test_bars_come_from_a_css_variable_and_numbers_stay_text():
    """Varje sifferruta bär --v; staplarna ritas av CSS, siffran är text."""
    block = section("wt-time")
    cells = re.findall(r'<td class="wt-num"[^>]*>', block)
    assert len(cells) == 24
    for c in cells:
        assert re.search(r'style="--v: \d+(\.\d)?"', c), c
    assert "var(--v)" in CSS.read_text(encoding="utf-8")


def test_stress_numbers():
    block = section("wt-stress")
    shown = text_of(block)
    assert ">What weighs most is not what takes longest</h2>" in block
    for n in ("52%", "65%", "40%", "51%", "37%", "45%", "42%", "39%", "35%", "31%", "71%", "55%",
              "34%", "33%", "32%", "54%"):
        assert n in shown, n
    assert ("Planning takes the most time outside lessons, but of the tasks above it stresses the fewest teachers. Administration "
            "stresses most everywhere; in Sweden, marking and adapting for different needs come "
            "next.") in shown


def test_ai_section():
    block = section("wt-ai")
    shown = text_of(block)
    assert ">What AI has been shown to save</h2>" in block
    for s in ("31%", "25 min", "24%", "49 min", "5.9", "32%", "Selwyn"):
        assert s in shown, s
    assert ("So this package promises minutes, not hours. The biggest gains for the most "
            "stressful tasks probably come from cutting work, not from automating it.") in shown
    assert ("The quality of the planned lessons and materials was not lower in either trial."
            in shown)
    assert "Lesson quality was not lower" not in shown
    for sentence in re.split(r"(?<=[.!?])\s+", shown):
        assert not ("13%" in sentence and "32%" in sentence), sentence
    assert "13%" not in shown


def test_three_rules():
    block = section("wt-rules")
    assert ">Three rules for every part</h2>" in block
    items = re.search(r"<ol[^>]*>(.*?)</ol>", block, re.S).group(1)
    assert [text_of(i) for i in re.findall(r"<li>(.*?)</li>", items, re.S)] == [
        "No student names and no student work in any prompt. Names and details are added "
        "afterwards, outside AI.",
        "You decide first, AI drafts after, and you check everything before it reaches students.",
        "Cut before you automate. Work that does not help students is better removed than done "
        "faster.",
    ]


def test_eleven_tasks_in_johans_order():
    block = section("wt-tasks")
    assert ">Eleven tasks, and what helps with each</h2>" in block
    rows = tasks()
    assert len(rows) == 11
    names = [text_of(re.search(r'<h3 class="wt-task__name">(.*?)</h3>', r, re.S).group(1))
             for r in rows]
    assert names == TASKS
    assert "Evaluating knowledge" not in names
    lede = re.search(r'<p class="wt-lede">(.*?)</p>', block, re.S).group(1)
    assert text_of(lede) == ("Most tasks already have some support on Choosewise; the new parts fill "
                             "the gaps.")
    assert "order" not in lede
    for r in rows:
        for part in ("wt-task__time", "wt-task__now", "wt-task__new", "wt-task__label"):
            assert f'class="{part}"' in r, part


def row_part(row, cls):
    return text_of(re.search(rf'<(?:div|p) class="{cls}">(.*?)</(?:div|p)>', row, re.S).group(1))


def test_status_chips():
    rows = tasks()
    for i, row in enumerate(rows, 1):
        cell = new_cell(row)
        shown = text_of(cell)
        # Varje rad namnger sin kurslektion, och den är klar; den länkas inte härifrån.
        assert f"Course lesson {i} Ready" in shown, i
        assert not re.search(rf'<a [^>]*>\s*Course lesson {i}\b', cell), i
        if i == 4:
            # Rad 4: lektionen, Quality Ladder och policyn på en sida, alla klara; de två sista länkade.
            assert shown.count("Ready") == 3, i
            assert f'href="{QL}' in cell, i
            assert "Coming" not in shown, i
        elif i == 1:
            assert shown.count("Ready") == 1 and shown.count("Coming") == 1, i
            assert "<a " not in cell, i
        elif i in (2, 3):
            assert shown.count("Ready") == 1 and "Coming" not in shown, i
            assert "<a " not in cell, i
        else:
            assert shown.count("Ready") == 1 and shown.count("Coming") == 1, i
            assert "<a " not in cell, i
    assert "Worked examples for new teachers Coming" in text_of(new_cell(rows[0]))


def test_keeping_order_row():
    row = tasks()[2]
    time = row_part(row, "wt-task__time")
    assert "55%" in time and "35%" in time and "Sweden" in time
    assert row_part(row, "wt-task__now") == "Nothing yet"
    assert row_part(row, "wt-task__label") == "Promising"


def test_marking_row_merges_evaluating_knowledge():
    row = tasks()[3]
    now = re.search(r'<div class="wt-task__now">(.*?)</div>', row, re.S).group(1)
    items = [text_of(i) for i in re.findall(r"<li>(.*?)</li>", now, re.S)]
    assert items == ["Feedback lens in Lesson Lens", "The check in Homework Upgrade",
                     "Retrieval Rhythm", "Exit tickets in Two-Minute Debrief"]
    new = text_of(new_cell(row))
    assert "Quality Ladder Ready" in new
    assert "One-page feedback policy Ready" in new


def test_task_labels_follow_the_proposals_page():
    labels = [text_of(re.search(r'<div class="wt-task__label">(.*?)</div>', r, re.S).group(1))
              for r in tasks()]
    assert labels == ["Time saving: two randomised trials", "Varies by tool", "Promising",
                      "Promising Strong for retrieval practice", "Promising", "Framework",
                      "Framework", "Promising", "Framework", "Promising", "Promising"]


def test_parts():
    block = section("wt-parts")
    assert ">The parts</h2>" in block
    cards = re.findall(r'<article class="wt-part">.*?</article>', block, re.S)
    assert len(cards) == 5
    names = [text_of(re.search(r"<h3[^>]*>(.*?)</h3>", c, re.S).group(1)) for c in cards]
    assert names == PARTS
    links = [re.findall(r'<a [^>]*href="([^"]*)"[^>]*>(.*?)</a>', c, re.S) for c in cards]
    assert [(h, text_of(t)) for h, t in links[0]] == [(QL, "Open Quality Ladder →")]
    assert [(h, text_of(t)) for h, t in links[3]] == [(CLASSROOM, "Open the course in Skool →")]
    assert all(not l for i, l in enumerate(links) if i not in (0, 3))
    for i in (0, 3):
        assert "Ready" in text_of(cards[i]) and "Coming" not in text_of(cards[i]), i
    for i in (1, 2, 4):
        assert "Coming" in text_of(cards[i]), i
    assert "Eleven lessons in Skool, one per task" in text_of(cards[3])
    assert "seven modules" not in text_of(cards[3]).lower()
    assert "working name" not in text_of(block).lower()
    assert "Five parts, built in this order." in text_of(block)


def test_internal_links_resolve():
    links = re.findall(r'href="(/[^"]*)"', html())
    assert len(links) > 20
    for href in links:
        path = href.split("#")[0].split("?")[0]
        if path.endswith("/"):
            assert (ROOT / path.lstrip("/") / "index.html").exists(), href
        else:
            assert (ROOT / path.lstrip("/")).exists(), href


def test_every_tool_named_in_the_spec_is_linked_where_it_has_a_page():
    """Verktygen i spec A6 pekar på sina riktiga sidor."""
    expected = {
        "Lesson Lens": "/lesson-lens/", "Unit Studio": "/unit-studio-541ebd12/",
        "Pedagogy Compass": "/pedagogy-compass-59ecb8db/", "Thinking Profile": "/thinking-profile/",
        "Thinking Moves": "/thinking-moves/", "Flawed Answer": "/flawed-answer/",
        "Side by Side": "/side-by-side/", "Retrieval Rhythm": "/retrieval-rhythm/",
        "Two-Minute Debrief": "/two-minute-debrief/", "Study Moves": "/study-moves/",
        "Homework Upgrade": "/homework-upgrade-1f0cd17c/", "Test Countdown": "/test-countdown/",
        "Visual codes": "/visual-codes/", "Study codes": "/free/study-codes/",
        "Infographic styles": "/infographic-styles/",
    }
    block = section("wt-tasks")
    found = {text_of(t): h for h, t in re.findall(r'<a [^>]*href="([^"]*)"[^>]*>(.*?)</a>', block, re.S)}
    for name, href in expected.items():
        assert found.get(name) == href, name


def test_sources_are_https():
    block = section("wt-sources")
    assert ">Sources</h2>" in block
    links = re.findall(r'<a [^>]*href="([^"]*)"', block)
    assert len(links) >= 10
    assert all(l.startswith("https://") for l in links), links


def test_no_script_and_css_linked():
    page = html()
    assert re.findall(r'<script[^>]*>', page) == ['<script src="/assets/js/include.js">']
    assert '<link rel="stylesheet" href="/assets/css/what-teachers-do.css' in page
    assert '<link rel="stylesheet" href="/assets/css/thinking-moves.css' in page
    assert 'style="' in page and "<style" not in page


def test_swedish_comments():
    """Varje sektion har minst en förklarande kommentar rakt före sig."""
    page = html()
    for sid in SECTIONS:
        start = page.index(f'id="{sid}"')
        before = page[:start]
        prev = before.rfind("</section>")
        gap = before[prev if prev != -1 else 0:]
        comments = re.findall(r"<!--(.*?)-->", gap, re.S)
        explaining = [c for c in comments if not re.match(r"\s*[a-z-]+:(start|end)\b", c)]
        assert explaining, sid


def test_font_weights_only_from_tokens():
    css = CSS.read_text(encoding="utf-8")
    assert not re.search(r"font-weight:\s*\d", css)


def test_page_head_and_noindex():
    page = html()
    assert "<title>What teachers do — Choosewise</title>" in page
    assert '<meta name="description" content="' in page
    assert '<meta name="robots" content="noindex,nofollow">' in page
    assert 'rel="canonical"' not in page
    assert "og:image" not in page


def test_the_table_scrolls_inside_its_own_wrapper():
    css = CSS.read_text(encoding="utf-8")
    assert re.search(r"\.wt-scroll\s*\{[^}]*overflow-x:\s*auto", css)
    assert '<div class="wt-scroll"' in html()


def test_hidden_page_is_not_linked_anywhere():
    for rel in ["sitemap.xml", "llms.txt", "index.html", "robots.txt", "study/index.html",
                "pedagogy/index.html", "think/index.html"]:
        assert SLUG not in (ROOT / rel).read_text(encoding="utf-8"), rel
    for p in (ROOT / "assets/partials").glob("*"):
        assert SLUG not in p.read_text(encoding="utf-8"), p.name


def test_neither_hidden_slug_appears_in_any_public_html():
    """Ingen öppen HTML-sida får länka till eller nämna de två dolda sidorna."""
    import subprocess
    files = subprocess.run(["git", "ls-files", "*.html"], cwd=ROOT, capture_output=True,
                           text=True, check=True).stdout.splitlines()
    skip = ("what-teachers-do-354716b7/", "quality-ladder-ec1c2f8c/", "_unpublished/", "docs/",
            "exports/")
    checked = 0
    for rel in files:
        if rel.startswith(skip):
            continue
        checked += 1
        text = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
        for slug in ("what-teachers-do-354716b7", "quality-ladder-ec1c2f8c"):
            assert slug not in text, (rel, slug)
    assert checked > 50
