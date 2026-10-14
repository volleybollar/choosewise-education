"""Leveransen är de engelska PDF:erna, inte HTML:en de renderas ur.

Varje annan vakt i rundan läser HTML. Rättas HTML:en utan att PDF:erna
renderas om går hela sviten grön medan filen som går till Skool
fortfarande bär den svenska inramningen. Den här vakten läser det som
levereras.

Den täcker också quick-starten, som med avsikt står utanför
ytkonsistensvakten (spec §5) och annars inte bevakas av något som läser
dess innehåll.

Förbudslistan är PER GUIDE. Copilot-rundan valde väg A rakt av och kan
därför förbjuda "Sweden", "Swedish" och "GDPR" bart. Gemini-rundan kan
inte: ett källbelagt svenskt praktikexempel stannar (spec §9 tillåter
det uttryckligen), och en promptmall innehåller ordet GDPR som
platshållare läsaren själv fyller i. En delad lista vore en vakt som
styr innehållet i stället för att vakta det.
"""
from __future__ import annotations

import hashlib
import re
import subprocess

import pytest

from . import pdf_fingerprint as fp

GUIDE_DELIVERY = {
    "copilot": {
        "pdfs": (
            "_unpublished/assets/pdfs/guides/copilot-guide-en.pdf",
            "_unpublished/assets/pdfs/guides/copilot-quick-start-en.pdf",
        ),
        # Oförändrad ur test_copilot_delivery.py.
        "forbidden": (
            "Swedish", "Sweden", "Skolverket", "IMY", "Schrems", "GDPR",
            "April 2026", "kr 350",
        ),
        "untouched": (),
    },
    "gemini": {
        "pdfs": (
            "_unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf",
            "_unpublished/assets/pdfs/guides/gemini-notebook-quick-start-en.pdf",
        ),
        # Inramningen och den artikelnivå-GDPR spec §3 väljer bort, sträng
        # för sträng. Inget bart "Sweden"/"Swedish" och inget bart "GDPR":
        # se modulens docstring. Och inget bart "April 2026" — sju
        # meningar bär datumet som ett DATERAT PRODUKTPÅSTÅENDE ("Since 8
        # April 2026 the two tools sync bidirectionally"), och de står
        # eller faller på sin källa, inte på rundans datumstämpel. De två
        # STÄMPLARNA bevakas i stället var och en på sin plats, av
        # test_geminis_cover_and_closing_carry_the_rounds_date nedan.
        "forbidden": (
            "Skolverket", "IMY", "Schrems",
            "Swedish schools",
            "Swedish and other EU languages",
            "Sweden, as of April 2026",
            "Sweden is a notable example",
            "GDPR fundamentals",
            "Standard GDPR discipline",
            "carrying GDPR risk",
            "the GDPR and the EU AI Act",
            "Article 6(1)(e)",
            "Article 30",
            "national data protection authority",
            "Every EU member state has one",
            "phases in through 2026 and beyond",
            "Limited risk",
            "I have a full-time job",
        ),
        # Spec §1: de svenska ytorna ska komma ut byte-identiska. Båda
        # byggarna renderar EN *och* SV i samma körning, så de skrivs
        # varje gång de engelska renderas om.
        "untouched": (
            "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-sv.pdf",
            "_unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-sv.pdf",
        ),
    },
    "apple-intelligence": {
        "pdfs": (
            "_unpublished/assets/pdfs/guides/apple-intelligence-guide-en.pdf",
            "_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-en.pdf",
        ),
        # Runda 1:s lista förbjuder BARA strängar de levererade PDF:erna
        # redan är fria från. Guiden bär `Swedish`, `IMY`, `Schrems` och
        # `Siri 2.0` legitimt — de är sanna påståenden om en guide som ännu
        # inte är omskriven, och att förbjuda dem nu vore att göra billigaste
        # vägen till grönt att stryka innehåll. De läggs till i runda 2, vid
        # omrenderingen.
        #
        # Bara den FÖRSTA raden står i versalspärrad form: pdftotext spärrar
        # versaler, så URL:en `/guides/apple-intelligence` står som
        # `/ G U I D E S / A P P L E - I N T E L L I G E N C E` i utskriften,
        # och en needle skriven som vanlig URL hade aldrig matchat. De två
        # följande raderna är vanliga, ospärrade prosafragment ur samma
        # struckna mening ("…download the 25-page premium PDF from the same
        # page.") och behöver ingen sådan spärrning.
        "forbidden": (
            "/ G U I D E S / A P P L E",
            "from the same page",
            "download the 25-page premium PDF",
            "Skolverket",
            "NotebookLM",
            "Copilot",
        ),
        # Båda byggarna renderar EN *och* SV i samma körning, så de svenska
        # filerna skrivs varje gång de engelska renderas om. Raden jämför
        # bytes mot merge-basen.
        "untouched": (
            "_unpublished/assets/pdfs/guides/apple-intelligence-guide-sv.pdf",
            "_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf",
        ),
    },
}

GUIDES = tuple(GUIDE_DELIVERY)

# Task 13 har renderat om PDF:erna — båda paren (huvudguidens och
# quick-startens) går nu grönt rakt av. Tom till nästa guide fyller den
# igen. Mängden är PER PDF, inte per guide, samma form som
# XFAIL_UNTIL_RECOUNTED i test_guide_toc.py: (guide, identitet).
XFAIL_UNTIL_RERENDERED = set()


def delivery_for(guide: str) -> dict:
    try:
        return GUIDE_DELIVERY[guide]
    except KeyError:
        raise KeyError(
            f"okänd guide {guide!r}, kända: {sorted(GUIDE_DELIVERY)}"
        ) from None


def _flat(rel: str) -> str:
    """pdftotext -layout bryter rader mitt i meningar; en sträng som
    'Swedish schools' står med radbrytning emellan i den renderade
    filen. Platta till allt blankt till ett mellanslag innan sökning."""
    return re.sub(r"\s+", " ", fp.extract(fp.ROOT / rel))


# Ett äkta sidantalspåstående handlar om GUIDEN. Mönstret krävde tidigare
# bara `(\d+)-page` var som helst i quick-startens text och plockade då upp
# varje orelaterat räkneexempel: Apples quick-start trycker "Summarise a
# 5-page curriculum PDF" i funktionslistan, och vakten jämförde den femman
# med huvudguidens 25 sidor. Nu krävs att talet står intill ordet "Guide",
# vilket är vad de äkta påståendena gör ("The 25-page Microsoft Copilot
# Guide", "The full 44-page Gemini & Gemini Notebook Guide").
_PAGE_CLAIM = re.compile(r"(\d+)-page[^.]{0,60}?Guide")

# Guider vars quick-start inte gör något sidantalspåstående alls. Vakten
# nedan kan inte jämföra ett tal som inte finns, men frånvaron får inte
# uppstå TYST — en avslutning som redigeras kan annars tappa ett äkta
# påstående utan att något blir rött. Töms av den runda som skriver in ett
# påstående igen. Värdet är skälet.
NO_PAGE_CLAIM = {
    "apple-intelligence":
        "runda 1 tog bort hela meningen 'download the 25-page premium PDF from "
        "the same page' — den var en pekare till en sida som aldrig publiceras "
        "(Johans beslut 2026-10-13) och sidantalspåståendet satt inuti den. "
        "Runda 2 skriver avslutningen och avgör om ett nytt påstående ska in.",
}

# Oskyldiga `\d+-page`-strängar: tal i quick-startens egen prosa som inte
# är ett påstående om guiden. Varje post är en ordagrann sträng ur den
# levererade PDF:en, mätt i `_flat()`-form. Listan finns för att
# ruttnandevakten nedan ska kunna kräva att VARJE bart tal är redovisat.
BARE_PAGE_NUMBERS = {
    "apple-intelligence": ("Summarise a 5-page curriculum PDF",),
}


def _rendered_page_count(rel: str) -> int:
    """Antal sidor i den FAKTISKT renderade pdf:en.

    fp.pages() delar pdftotext-utskriften på formfeed-tecknet (\\f), som
    pdftotext lägger efter VARJE sida — även den sista. En 44-sidig pdf
    ger alltså 45 poster, där den sista är tom. Den tomma avslutande
    posten är inte en sida och får inte räknas med, annars blir talet
    alltid ett för högt."""
    pages = fp.pages(fp.extract(fp.ROOT / rel))
    if pages and pages[-1] == "":
        pages = pages[:-1]
    return len(pages)


def _main_and_quick_start(guide: str) -> tuple[str, str]:
    """Plockar isär en guides pdf-par ur GUIDE_DELIVERY, (huvudguide, quick-start),
    utan att anta ordning — "quick-start" i filnamnet är det som skiljer dem."""
    pdfs = delivery_for(guide)["pdfs"]
    quick = [rel for rel in pdfs if "quick-start" in rel]
    main = [rel for rel in pdfs if "quick-start" not in rel]
    assert len(main) == 1 and len(quick) == 1, (
        f"{guide}: väntade exakt en huvudguide och en quick-start i kartan, "
        f"fick {pdfs}")
    return main[0], quick[0]


def _merge_base() -> str:
    """Grenens avstamp från `main`. Jämförelsepunkten måste ligga före
    rundan: på `HEAD` vore vakten en snubbeltråd i arbetsträdet, och en
    gång committad skada skulle passera för alltid."""
    return subprocess.run(
        ["git", "merge-base", "main", "HEAD"],
        capture_output=True, text=True, check=True, cwd=fp.ROOT).stdout.strip()


def _delivery_cases():
    for guide, cfg in GUIDE_DELIVERY.items():
        for rel in cfg["pdfs"]:
            marks = ([pytest.mark.xfail(
                        strict=True,
                        reason="röd till Task 13 har renderat om PDF:erna")]
                     if (guide, rel) in XFAIL_UNTIL_RERENDERED else [])
            yield pytest.param(guide, rel, marks=marks, id=f"{guide}:{rel.rsplit('/', 1)[-1]}")


@pytest.mark.parametrize("guide,rel", list(_delivery_cases()))
def test_the_delivered_pdfs_carry_no_abandoned_claim(guide, rel):
    flat = _flat(rel)
    found = [needle for needle in delivery_for(guide)["forbidden"] if needle in flat]
    assert found == [], f"{rel} bär kvar: {found}"


@pytest.mark.parametrize("guide", GUIDES)
def test_the_quick_start_pdf_is_part_of_the_delivery_guard(guide):
    """Quick-starten står utanför ytvakten med avsikt. Faller den också
    ur den här vakten bevakas dess innehåll av ingenting alls."""
    pdfs = delivery_for(guide)["pdfs"]
    assert any("quick-start" in rel for rel in pdfs), guide
    for rel in pdfs:
        assert rel in fp.UNPUBLISHED_GUIDE_PDFS, f"{rel} står inte i facitlistan"


@pytest.mark.parametrize("guide", GUIDES)
def test_each_guides_forbidden_list_is_its_own(guide):
    """Granskningsfokus 1: listan får inte bli delad igen. En guide utan
    egna strängar är en guide vars vakt någon har slagit ihop."""
    cfg = delivery_for(guide)
    assert cfg["forbidden"], f"{guide}: tom förbudslista"
    others = {needle for other, c in GUIDE_DELIVERY.items() if other != guide
              for needle in c["forbidden"]}
    assert set(cfg["forbidden"]) - others, (
        f"{guide}: varje förbjuden sträng delas med en annan guide — "
        "listan har slagits ihop och vaktar inte den här guidens beslut")


def test_geminis_forbidden_list_does_not_ban_what_the_spec_keeps():
    """Granskningsfokus 1, andra halvan. Två saker STANNAR i Gemini-
    guiden och en kopierad Copilot-lista hade förbjudit båda: det
    källbelagda Fristadsskolan-exemplet (spec §9: medvetet, motiverat
    exempel med en post) och promptmallens GDPR-platshållare (spec §3).
    En bar sträng här skulle göra vakten röd för rätt innehåll."""
    forbidden = delivery_for("gemini")["forbidden"]
    for kept in ("Sweden", "Swedish", "GDPR", "EU AI Act", "Article 4"):
        assert kept not in forbidden, (
            f"{kept!r} är en bar sträng i Geminis förbudslista — "
            "den träffar innehåll rundan har beslutat att behålla")


def test_geminis_cover_and_closing_carry_the_rounds_date():
    """Datumstämplarna, var och en på sin plats.

    En bar förbudsrad på "April 2026" går inte för den här guiden (se
    kommentaren i kartan), så omslaget kontrolleras som SIDA 1 och
    avslutningen genom signaturens hela sträng. Det är de två ställen där
    datumet är en stämpel på dokumentet och inte ett påstående om en
    produkt.
    """
    main = "_unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf"
    cover = re.sub(r"\s+", " ", fp.pages(fp.extract(fp.ROOT / main))[0])
    assert "October 2026" in cover, "omslaget bär inte rundans datum"
    assert "April 2026" not in cover, "omslaget bär kvar den gamla stämpeln"
    flat = _flat(main)
    assert "Johan Lindström, October 2026" in flat
    assert "Johan Lindström, April 2026" not in flat


def _untouched_cases():
    for guide, cfg in GUIDE_DELIVERY.items():
        for rel in cfg["untouched"]:
            yield pytest.param(guide, rel, id=f"{guide}:{rel.rsplit('/', 1)[-1]}")


@pytest.mark.parametrize("guide,rel", list(_untouched_cases()))
def test_the_untouched_pdfs_are_byte_identical_to_the_merge_base(guide, rel):
    """Granskningsfokus 5: båda byggarna renderar EN *och* SV utan
    språkargument, så de svenska filerna skrivs varje gång de engelska
    renderas om. Återställs de slarvigt är INNEHÅLLSfacit ändå
    oförändrat — fingeravtrycket är detsamma, bara `CreationDate` har
    rört sig — och hela sviten går grön medan två filer ligger ändrade.
    Den här vakten jämför bytes mot bascommiten, inte innehåll.

    Generaliserad från en Gemini-bunden vakt: den var hårdkodad till
    `GUIDE_DELIVERY["gemini"]["untouched"]`, så Apples två svenska PDF:er
    stod i kartan utan att någon läste dem — vilket tvingade en
    handmätning (SHA-256) under rundan i stället för att vakten gjorde
    det. Nu parametriseras testet över VARJE guides `untouched`."""
    committed = subprocess.run(
        ["git", "show", f"{_merge_base()}:{rel}"],
        capture_output=True, check=True, cwd=fp.ROOT).stdout
    assert hashlib.sha256(committed).hexdigest() == \
           hashlib.sha256((fp.ROOT / rel).read_bytes()).hexdigest(), \
           f"{guide} {rel} är inte byte-identisk med bascommiten — spec §1"


def test_every_quick_starts_page_count_claim_matches_its_rendered_main_guide():
    """Task 16 hittade genom att LÄSA att Geminis quick-start påstod
    '40-page' om en guide som faktiskt är 44 sidor — ingen vakt såg det.
    Talet kan bli fel igen på exakt samma tysta sätt, så den här vakten
    härleder huvudguidens sidantal ur den LEVERERADE pdf:en och jämför
    med det '(\\d+)-page'-tal quick-startens pdf trycker, i stället för
    att hårdkoda 44.

    Mönstret är guide-agnostiskt som GUIDE_DELIVERY ovan: en guide vars
    quick-start inte gör ett sådant påstående hoppas bara över (inget
    `continue`-varv ger inget fel) — en avsaknad är inte samma sak som
    en felaktig siffra, och nästa guide kan tas in utan att den här
    testen skrivs om.

    En utebliven träff kräver en deklaration i NO_PAGE_CLAIM, inte tystnad
    — annars kan en redigerad avslutning tappa ett äkta påstående utan att
    något blir rött."""
    mismatches = []
    for guide in GUIDES:
        main_rel, quick_rel = _main_and_quick_start(guide)
        match = _PAGE_CLAIM.search(_flat(quick_rel))
        if match is None:
            assert guide in NO_PAGE_CLAIM, (
                f"{guide}: quick-starten gör inget sidantalspåstående om guiden "
                "och står inte i NO_PAGE_CLAIM — ett äkta påstående försvinner "
                "inte tyst")
            continue
        claimed = int(match.group(1))
        actual = _rendered_page_count(main_rel)
        if claimed != actual:
            mismatches.append(
                f"{guide}: quick-starten säger {claimed}-page, "
                f"huvudguiden är faktiskt {actual} sidor")
    assert mismatches == [], mismatches


@pytest.mark.parametrize("guide", sorted(NO_PAGE_CLAIM))
def test_the_no_page_claim_list_cannot_rot(guide):
    """Listan ska beskriva verkligheten, annars tömmer den sig i prosa.

    Tre sätt den kan ruttna, alla röda här: en post som inte är en känd
    guide, en post utan skäl, och en post vars quick-start FAKTISKT gör ett
    påstående igen — då är skulden betald, och står posten kvar ligger
    påståendet ovaktat. Samma form som UNMAPPED_GUIDE_SURFACES och
    MEASURE_ONLY_INVENTORIES.
    """
    assert guide in GUIDE_DELIVERY, (
        f"{guide} står i NO_PAGE_CLAIM men inte i leveranskartan")
    assert NO_PAGE_CLAIM[guide].strip(), f"post utan skäl: {guide}"
    _, quick_rel = _main_and_quick_start(guide)
    flat = _flat(quick_rel)
    match = _PAGE_CLAIM.search(flat)
    assert match is None, (
        f"{guide}: quick-starten gör ett påstående igen ({match.group(0)!r}) "
        "— stryk posten ur NO_PAGE_CLAIM")

    # Andra sonden, och skälet står här: mönstret ovan kräver literalen
    # `Guide`, så ett omformulerat påstående ("the full 25-page PDF", "a
    # 25-page companion", gemena "the 25-page guide") hade passerat både
    # sidantalsvakten och den här raden, och lämnat påståendet ovaktat
    # bakom en deklaration som ser sann ut. Därför måste varje bart
    # `\d+-page` i quick-starten vara redovisat som oskyldigt.
    stripped = flat
    for phrase in BARE_PAGE_NUMBERS.get(guide, ()):
        assert phrase in stripped, (
            f"{guide}: den redovisade strängen {phrase!r} står inte längre i "
            "quick-starten — stryk eller uppdatera posten i BARE_PAGE_NUMBERS")
        stripped = stripped.replace(phrase, " ")
    leftover = [m.group(0) for m in re.finditer(r"\d+-page", stripped)]
    assert not leftover, (
        f"{guide}: quick-starten bär {leftover} utöver de redovisade "
        "strängarna — är det ett påstående om guiden, stryk posten ur "
        "NO_PAGE_CLAIM; är det ett nytt oskyldigt tal, redovisa det i "
        "BARE_PAGE_NUMBERS")
