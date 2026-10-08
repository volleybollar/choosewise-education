"""Omstylingen får inte ändra ett ord i prompt-PDF:erna.

Och de svenska tecknen måste överleva typsnittsbytet — faller
renderaren tillbaka på ett systemsnitt bryts radbrytningen.
Granskningsfokus 2.

Facit sparas före stilbytet med:
  mkdir -p /tmp/pdf-parity-before
  for f in teachers-en principals-en matematik-sv larare-sv skolchefer-sv; do
    pdftotext -layout "assets/pdfs/prompts/$f.pdf" "/tmp/pdf-parity-before/$f.txt"
  done

Obs: uppgiftsbriefen namnger det svenska matte-provet "mathematics-sv", men
den filen finns inte — svenska matte-PDF:en heter matematik-sv.pdf (det
svenska ordet, inte en bokstavlig översättning av den engelska slugen).
SAMPLES nedan använder det verkliga filnamnet.

Fix-rond (uppgiftsgivarens omdöme): den ursprungliga versionen av
test_content_is_unchanged jämförde extract(pdf).split() mot facit.split().
Det gjorde testet känsligt för HUR pdftotext råkar tokenisera spärrade
versaler ("PROMPT LIBRARY" -> "P R O M P T L I B R A RY"), inte för om
innehållet faktiskt flyttat sig — noll ord, meningar eller sidbrytningar
rör sig i verkligheten, bara hur extraktionsverktyget delar upp spärrad
text i "ord". Ersatt med en per-sida teckenmultimängd (Counter över alla
icke-blanka tecken), som är okänslig för tokenisering men fångar varje
verklig textändring. Bevis på det senare: test_fingerprint-testerna
nedan.

Fingeravtryckets kända begränsning: det är en multimängd PER SIDA, så det
är blint för omkastning INOM en sida — två meningar som byter plats på
samma sida, med samma tecken kvar, skulle passera. Medvetet och korrekt
avvägt (en CSS-omstyling kastar inte om textens ordning, bara färg och
typsnitt) men värt att säga rakt ut, eftersom testets enda uppgift är att
vara pålitligt. Flytt ÖVER en sidgräns fångas fortfarande (se
test_fingerprint_catches_text_moved_across_a_page_boundary).
"""
import subprocess
from pathlib import Path

import pytest

from . import pdf_fingerprint as fp

ROOT = Path(__file__).resolve().parents[2]
PDF_DIR = ROOT / "assets/pdfs/prompts"
BEFORE = Path("/tmp/pdf-parity-before")

SAMPLES = ["teachers-en", "principals-en", "matematik-sv", "larare-sv", "skolchefer-sv"]

extract = fp.extract
_pages = fp.pages
_fingerprint = fp.fingerprint


# Fix-rond: ett saknat facit gav pytest.skip, inte pytest.fail. Efter en
# omstart eller en färsk klon av repot finns inget /tmp/pdf-parity-before,
# och grinden som bevisar "inte ett ord ändrat" degraderar tyst till tystnad
# i stället för att fela — en suite full av gula skip kan se grön ut i
# sammanfattningen utan att ha bevisat något. Ett saknat facit är nu ett
# fel, med instruktionen för hur det återskapas i meddelandet.
def _require_baseline(slug: str) -> Path:
    baseline = BEFORE / f"{slug}.txt"
    if not baseline.exists():
        pytest.fail(
            f"Inget facit för {slug} i {BEFORE} — testet kan inte bevisa att "
            "innehållet är oförändrat utan det. Återskapa med:\n"
            "  mkdir -p /tmp/pdf-parity-before\n"
            "  for f in teachers-en principals-en matematik-sv larare-sv skolchefer-sv; do\n"
            '    pdftotext -layout "assets/pdfs/prompts/$f.pdf" "/tmp/pdf-parity-before/$f.txt"\n'
            "  done"
        )
    return baseline


@pytest.mark.parametrize("slug", SAMPLES)
def test_content_is_unchanged(slug):
    baseline = _require_baseline(slug)
    before = _pages(baseline.read_text())
    after = _pages(extract(PDF_DIR / f"{slug}.pdf"))
    moved = _moved(before, after)
    assert moved == [], f"{slug}: innehållet ändrades på sida {moved}"


# ───────────────────────────────────────────────────────────────────────
# Diskrimineringsbevis: fingeravtrycksjämförelsen ovan är inte tandlös.
# Ett test som accepterar allt är värre än inget test. De här muterar en
# kopia av ett riktigt facit I MINNET — skriver aldrig till filen på
# disk — och visar att jämförelsen faktiskt larmar på varje verklig
# defektklass. Om någon framtida "förenkling" av _fingerprint tappar
# känsligheten är det de här testerna som upptäcker det.
# ───────────────────────────────────────────────────────────────────────

def _load_baseline_pages(slug: str) -> list[str]:
    return _pages(_require_baseline(slug).read_text())


def _moved(before_pages: list[str], after_pages: list[str]) -> list[int]:
    assert len(before_pages) == len(after_pages), (
        f"sidantalet ändrades, {len(before_pages)} -> {len(after_pages)}"
    )
    return [
        i + 1
        for i, (a, b) in enumerate(zip(before_pages, after_pages))
        if _fingerprint(a) != _fingerprint(b)
    ]


def test_fingerprint_accepts_unchanged_content():
    pages = _load_baseline_pages("larare-sv")
    assert _moved(pages, list(pages)) == []


def test_fingerprint_catches_single_character_change():
    """Minsta möjliga defekt: ett enda tecken ändrat på en sida."""
    pages = _load_baseline_pages("larare-sv")
    target = next(i for i, p in enumerate(pages) if p.strip())
    chars = list(pages[target])
    pos = next(i for i, c in enumerate(chars) if not c.isspace())
    chars[pos] = "X" if chars[pos] != "X" else "Y"
    mutated = list(pages)
    mutated[target] = "".join(chars)
    assert _moved(pages, mutated) == [target + 1]


def test_fingerprint_catches_a_changed_word():
    pages = _load_baseline_pages("larare-sv")
    target = next(i for i, p in enumerate(pages) if "lärare" in p)
    mutated = list(pages)
    mutated[target] = mutated[target].replace("lärare", "rektorer", 1)
    assert _moved(pages, mutated) == [target + 1]


def test_fingerprint_catches_a_removed_sentence():
    pages = _load_baseline_pages("larare-sv")
    target = next(i for i, p in enumerate(pages) if ". " in p)
    sentence_start = pages[target].index(". ") + 2
    mutated = list(pages)
    mutated[target] = pages[target][:sentence_start] + pages[target][sentence_start + 20:]
    assert _moved(pages, mutated) == [target + 1]


def test_fingerprint_catches_a_removed_page():
    pages = _load_baseline_pages("larare-sv")
    assert len(pages) > 1
    mutated = pages[:-1]
    with pytest.raises(AssertionError, match="sidantalet ändrades"):
        _moved(pages, mutated)


def test_fingerprint_catches_text_moved_across_a_page_boundary():
    pages = _load_baseline_pages("larare-sv")
    target = next(i for i in range(len(pages) - 1) if pages[i].strip() and pages[i + 1].strip())
    mutated = list(pages)
    moved_chunk = mutated[target][-10:]
    mutated[target] = mutated[target][:-10]
    mutated[target + 1] = moved_chunk + mutated[target + 1]
    assert set(_moved(pages, mutated)) == {target + 1, target + 2}


@pytest.mark.parametrize("slug", ["larare-sv", "skolchefer-sv", "matematik-sv"])
def test_swedish_characters_survive(slug):
    text = extract(PDF_DIR / f"{slug}.pdf")
    assert any(ch in text for ch in "åäöÅÄÖ"), "svenska tecken saknas helt"
    # Ett saknat snitt ger ofta ersättningstecken i stället för diakriter.
    assert "�" not in text


@pytest.mark.parametrize("slug", ["larare-sv", "teachers-en"])
def test_font_is_not_a_fallback(slug):
    """Helvetica (näst i fontstacken) renderar å/ä/ö lika bra som Hanken
    Grotesk, så test_swedish_characters_survive skulle förbli grönt även om
    @font-face-sökvägen gick sönder och renderaren tyst föll tillbaka — samma
    osynliga felklass som drabbade delningskortsrenderaren tidigare i den här
    vågen. Ett svenskt och ett engelskt prov, så att ett språkspecifikt
    byggfel inte kan gömma sig."""
    result = subprocess.run(
        ["pdffonts", str(PDF_DIR / f"{slug}.pdf")],
        capture_output=True, text=True, check=True,
    )
    assert "HankenGrotesk" in result.stdout, (
        f"{slug}: inbäddat typsnitt är inte Hanken Grotesk — "
        f"renderaren har troligen fallit tillbaka:\n{result.stdout}"
    )


def test_every_pack_rendered():
    assert len(list(PDF_DIR.glob("*.pdf"))) >= 124
