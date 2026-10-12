"""Innehållsförteckningens sidnummer mot den renderade PDF:en.

Våg 2b:s dyraste fel: 13 av 15 hårdkodade sidnummer i Claude-guidens
förteckning var fel, och ingen vakt såg det — texten granskades sexton
gånger utan att någon öppnade dokumentet. Copilot-rundan byggde vakten
men band den till en guide; den här rundan gör den guide-agnostisk
(spec §7).

Vakten läser numren ur mallen och letar upp varje avsnitts faktiska
startsida i den renderade PDF:en. Ankarsträngarna är valda ur
`pdftotext`-utskriften, inte ur HTML:en: extraktionen spärrar versaler
oförutsägbart ("PA R T 1"), så en spärrad etikett vore ett ankare som
aldrig matchar. Sökningen börjar på sidan efter förteckningen själv —
annars matchar varje ankare förteckningens egen rad.

Claude-guiden står UTANFÖR kartan, med avsikt. Dess förteckning
använder `toc-title`/`toc-page-num` i stället för `toc__title`/
`toc__page`, numren är nollutfyllda ("04"), och arton rader delar sidor
mellan delrubrik och underrad, vilket gör ankarvalet tvetydigt. Att ta
in den kräver en andra radregex och arton ankare verifierade mot en PDF
den här rundan inte renderar om. Att Claudes femton nummer står
ovaktade sedan våg 2b är en känd lucka och står i överlämningen.
"""
from __future__ import annotations

import re

import pytest

from . import pdf_fingerprint as fp
from . import surfacecheck

GUIDE_TOC = {
    # Copilots sex ankare, flyttade oförändrade ur test_copilot_toc.py.
    # Två av dem byttes under Copilot-rundan efter kontroll mot
    # pdftotext-utskriften: Part 3:s ankare sa "CDP" (texten säger "EDP"),
    # och "About this guide" matchade även sidan 3.
    "copilot": {
        "template": "_unpublished/exports/copilot-print-a4-en.html",
        "pdf": "_unpublished/assets/pdfs/guides/copilot-guide-en.pdf",
        "toc_page": 2,
        "anchors": {
            "Why this guide exists": "Why this guide exists",
            "Part 1 · Get started": "Which product are you actually using?",
            "Part 2 · Work smarter": "Copilot Chat (with your work data)",
            "Part 3 · Compliance & licensing": "What EDP actually gives you",
            "FAQ": "Questions teachers ask",
            "About this guide": "Johan Lindström, October 2026",
        },
    },
    # Gemini: tio rader, tio ankare, alla verifierade mot den renderade
    # PDF:en 2026-10-12 — varje ankare träffar först på den sida
    # avsnittet faktiskt börjar på. Inget ankare är hämtat ur en spärrad
    # etikett; openarna står som "PA R T 1", "O R I E N TAT I O N",
    # "BONUS CHAPTER" och "PROMPTS" i utskriften.
    "gemini": {
        "template": "_unpublished/exports/gemini-notebook-print-a4-en.html",
        "pdf": "_unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf",
        "toc_page": 2,
        "anchors": {
            "Introduction":
                "Before the how, a word on the why",
            "Understanding Gemini and Gemini Notebook":
                "two complementary views onto a single Google account",
            # Bytt i Task 14: rundan döpte om "NotebookLM" till "Gemini
            # Notebook" i löptexten (branding), så det gamla ankaret gav
            # SAKNAS mot den omrenderade PDF:en. Nytt ankare hämtat ur
            # samma pdftotext-utskrift, samma mening, bara ordet bytt.
            "Part 1 · Getting Started":
                "If you have never opened Gemini or Gemini Notebook, start here",
            "Part 2 · Working Smarter":
                "returning to Gemini or Gemini Notebook for the same kind of task",
            "Part 3 · Scale & Lead":
                "for educators who want to do more than save personal time",
            "Part 4 · Google Workspace for Education":
                "Many schools run Google Workspace for Education",
            # Ankaret står i den ingress Task 7 skrev om. Ledet
            # "If you teach or lead a school in an EU member state"
            # bevarades ordagrant där; resten av meningen byttes.
            "Bonus Chapter · The EU AI Act for schools":
                "If you teach or lead a school in an EU member state",
            "The Styles Library":
                "The same notebook and the same prompt will produce very different outputs",
            "Prompts":
                "Copy these prompts, adapt them to your context, run them",
            "FAQ":
                "Is the free tier enough?",
        },
    },
}

# Töms i slutet av varje runda som rättat sin förtecknings nummer.
# En mängd som bara växer slutar vakta något — samma konvention som
# RECAPTURED_THIS_ROUND i test_capture_guide_baseline.py.
XFAIL_UNTIL_RECOUNTED: set = set()

GUIDES = tuple(GUIDE_TOC)

_TOC_ROW = re.compile(
    r'<span class="toc__title">(?P<title>.*?)(?:<span class="toc__sub">.*?</span>)?'
    r'\s*</span>.*?<span class="toc__page">(?P<page>\d+)</span>',
    re.S)


def config_for(guide: str) -> dict:
    try:
        return GUIDE_TOC[guide]
    except KeyError:
        raise KeyError(
            f"okänd guide {guide!r}, kända: {sorted(GUIDE_TOC)}"
        ) from None


def toc_rows(guide: str) -> list:
    """surfacecheck.normalise gör entiteterna till tecken, så nyckeln
    `Part 3 · Scale & Lead` matchar markupens `&amp;`."""
    html = (fp.ROOT / config_for(guide)["template"]).read_text(encoding="utf-8")
    return [(surfacecheck.normalise(re.sub(r"<[^>]+>", " ", m.group("title"))),
             int(m.group("page")))
            for m in _TOC_ROW.finditer(html)]


def _cases():
    for guide, cfg in GUIDE_TOC.items():
        for title in cfg["anchors"]:
            marks = ([pytest.mark.xfail(
                        strict=True,
                        reason="numret är fel i utgångsläget, räknas om i Task 14")]
                     if (guide, title) in XFAIL_UNTIL_RECOUNTED else [])
            yield pytest.param(guide, title, marks=marks, id=f"{guide}:{title}")


def test_an_unknown_guide_is_a_loud_error():
    """En guide som inte finns i kartan får inte ge en tom konfiguration
    — då vaktar vakten ingenting och är grön för det."""
    with pytest.raises(KeyError) as exc:
        config_for("apple-intelligence")
    assert "copilot" in str(exc.value) and "gemini" in str(exc.value)


@pytest.mark.parametrize("guide", GUIDES)
def test_every_guide_in_the_toc_map_has_anchors_for_every_row(guide):
    """Granskningsfokus 2: en guide med tom ankarlista samlar in noll
    parametriseringar, och en tom parametrisering är grön utan att vakta
    något. Den här raden är det som gör en tom lista röd."""
    cfg = config_for(guide)
    assert cfg["anchors"], f"{guide}: ankarlistan är tom"
    assert len(cfg["anchors"]) == len(toc_rows(guide))


@pytest.mark.parametrize("guide", GUIDES)
def test_the_toc_has_the_rows_we_think_it_has(guide):
    """Går regexen sönder blir listan tom, och en tom lista är en grön
    vakt som vaktar ingenting."""
    rows = toc_rows(guide)
    assert [title for title, _ in rows] == list(config_for(guide)["anchors"]), rows


@pytest.mark.parametrize("guide,title", list(_cases()))
def test_every_toc_page_number_matches_the_rendered_pdf(guide, title):
    cfg = config_for(guide)
    claimed = dict(toc_rows(guide))[title]
    anchor = surfacecheck.normalise(cfg["anchors"][title])
    pages = [surfacecheck.normalise(page)
             for page in fp.pages(fp.extract(fp.ROOT / cfg["pdf"]))]
    actual = next((i + 1 for i, page in enumerate(pages)
                   if i + 1 > cfg["toc_page"] and anchor in page), None)
    assert actual is not None, (
        f"ankaret {anchor!r} står inte på någon sida efter {cfg['toc_page']} — "
        "välj ett ankare ur pdftotext-utskriften, inte ur HTML:en")
    assert actual == claimed, (
        f"{guide} {title!r}: förteckningen säger {claimed}, "
        f"avsnittet börjar på {actual}")
