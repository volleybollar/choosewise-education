"""Sidvis textfingeravtryck för PDF-paritet.

Vanlig modul, inte testfil — scripts/tests/ är ett paket, så testfiler
kan inte importera varandra direkt.

Fingeravtrycket är en teckenmultimängd PER SIDA. Varför inte ordlistan:
pdftotext tokeniserar spärrade versaler oförutsägbart ("PROMPT LIBRARY"
blir "P R O M P T L I B R A RY"), vilket gör ordjämförelser känsliga för
hur verktyget råkar dela upp text i stället för för om texten ändrats.

Känd begränsning: multimängden är blind för omkastning INOM en sida. Två
meningar som byter plats på samma sida ger samma avtryck. Den som flyttar
innehåll måste alltså titta själv — avtrycket vaktar mot att omstylingen
tappar eller lägger till tecken, inte mot medveten omredigering.
"""
from __future__ import annotations

import hashlib
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PUBLISHED_GUIDE_PDFS = [
    "assets/pdfs/guides/claude-guide-en.pdf",
    "assets/pdfs/guides/claude-guide-sv.pdf",
    "assets/pdfs/guides/claude-quick-start-en.pdf",
    "assets/pdfs/guides/claude-quick-start-sv.pdf",
    "assets/pdfs/presentation-skills-guide-en.pdf",
    "assets/pdfs/presentationsteknik-guide-sv.pdf",
    "assets/pdfs/presentation-skills-summary-en.pdf",
    "assets/pdfs/presentationsteknik-sammanfattning-sv.pdf",
    # nlm-140-prompts-en.pdf dropped from the wave (ruling 2026-10-07): its
    # builder reads /tmp/nlm-prompts-en-chunk{1..4}.json, those chunks don't
    # exist and were never committed, so the PDF can't be rebuilt from this
    # repo at all. Recovering the chunks (or re-translating) is its own job —
    # don't re-add this path until that's solved.
]

UNPUBLISHED_GUIDE_PDFS = [
    "_unpublished/assets/pdfs/guides/ai-for-elever-sv.pdf",
    "_unpublished/assets/pdfs/guides/ai-for-students-en.pdf",
    "_unpublished/assets/pdfs/guides/apple-intelligence-guide-en.pdf",
    "_unpublished/assets/pdfs/guides/apple-intelligence-guide-sv.pdf",
    "_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-en.pdf",
    "_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf",
    "_unpublished/assets/pdfs/guides/copilot-guide-en.pdf",
    "_unpublished/assets/pdfs/guides/copilot-guide-sv.pdf",
    "_unpublished/assets/pdfs/guides/copilot-quick-start-en.pdf",
    "_unpublished/assets/pdfs/guides/copilot-quick-start-sv.pdf",
    "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-en.pdf",
    "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-sv.pdf",
    "_unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-en.pdf",
    "_unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-sv.pdf",
]

GUIDE_PDFS = PUBLISHED_GUIDE_PDFS + UNPUBLISHED_GUIDE_PDFS

BASELINE = Path(__file__).parent / "fixtures" / "guide-pdf-baseline.json"


def extract(pdf: Path) -> str:
    return subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"],
        capture_output=True, text=True, check=True,
    ).stdout


def pages(text: str) -> list[str]:
    return text.split("\f")


def fingerprint(page: str) -> str:
    counts = Counter("".join(page.split()))
    canonical = "".join(f"{ch}{counts[ch]}" for ch in sorted(counts))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def fingerprints(pdf: Path) -> list[str]:
    return [fingerprint(p) for p in pages(extract(pdf))]


def image_sizes(pdf: Path) -> list[list[int]]:
    """Width/height of every real image embedded in the PDF.

    Smask rows (alpha-channel masks that ride along with an image, not
    images themselves) are excluded. Sorted so re-encoding order doesn't
    matter. The text fingerprint above is blind to images by design — this
    is what catches a restyling (or a broken relative path) that silently
    drops or swaps one.
    """
    result = subprocess.run(
        ["pdfimages", "-list", str(pdf)],
        capture_output=True, text=True, check=True,
    )
    sizes = []
    for line in result.stdout.splitlines()[2:]:
        parts = line.split()
        if len(parts) < 5 or parts[2] != "image":
            continue
        sizes.append([int(parts[3]), int(parts[4])])
    return sorted(sizes)


def capture(pdf: Path) -> dict:
    return {"pages": fingerprints(pdf), "images": image_sizes(pdf)}
