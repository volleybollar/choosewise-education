#!/usr/bin/env python3
"""Extract structured prompt data from source PDFs into JSON.

For every folder in manifest.PACKS, runs `pdftotext -layout` on the .pdf
inside, parses out:
  - cover_count   : the "120" in "120 CHATTPROMPTAR"
  - parts         : list of {"title": "Del 1: ...", "prompts": [...]}

Writes one JSON file per pack to exports/prompts/data/<slug>.json.

Boilerplate (glossary, framework, chatbot list, usage block) is *not*
extracted — it's identical across all packs and lives in the HTML
templates. Only the parts that differ are stored per-pack.

Run:
  python3 exports/prompts/extract-prompts.py           # all packs
  python3 exports/prompts/extract-prompts.py 13-hkk    # single slug
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from manifest import PACKS, SOURCE_DIR

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def pdftotext(pdf_path: Path) -> str:
    """Run pdftotext -layout and return the decoded text."""
    r = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        capture_output=True, text=True, check=True,
    )
    return r.stdout


def find_pdf(folder: Path):
    """Each source folder has exactly one .pdf. Pick it."""
    pdfs = list(folder.glob("*.pdf"))
    return pdfs[0] if pdfs else None


# "Del N: title" appears in multi-part packs (e.g. 1 Lärare has Del 1 + Del 2).
# Most packs are single-part and use a simple "Promptar för X" heading instead.
PART_HEADER_RE = re.compile(r"^\s*Del\s+(\d+)\s*:\s*(.+?)\s*$", re.MULTILINE)
SIMPLE_HEADER_RE = re.compile(r"^\s*Promptar\s+(?:för|om|kopplat\s+till|från)\s+(.+?)\s*$", re.MULTILINE)

# The GDPR warning is the last line of the boilerplate — always present.
GDPR_MARKER_RE = re.compile(r"Tänk på GDPR!?", re.IGNORECASE)

COVER_COUNT_RE = re.compile(r"^\s*(\d{2,4})\s+CHATTPROMPTAR\b", re.MULTILINE)


def extract_parts(text: str) -> list[dict]:
    """Split text into parts with prompts.

    Two shapes:
      1. Multi-part (rare): "Del 1: …", "Del 2: …" markers inside the body
      2. Single-part (most packs): one "Promptar för X" heading after
         the boilerplate, then a flat list of prompts.

    We first chop off the boilerplate by locating the GDPR warning line,
    then parse whatever comes after.
    """
    # Chop boilerplate: everything after the GDPR warning is prompt content
    gdpr = GDPR_MARKER_RE.search(text)
    body = text[gdpr.end():] if gdpr else text

    # Try multi-part first
    del_markers = list(PART_HEADER_RE.finditer(body))
    if del_markers:
        parts = []
        for i, m in enumerate(del_markers):
            start = m.end()
            end = del_markers[i + 1].start() if i + 1 < len(del_markers) else len(body)
            prompts = split_prompts(body[start:end])
            parts.append({
                "number": int(m.group(1)),
                "title": m.group(2).strip(),
                "prompts": prompts,
            })
        return parts

    # Fall back: single-part. Use the "Promptar för X" heading if present.
    simple = SIMPLE_HEADER_RE.search(body)
    start = simple.end() if simple else 0
    title = simple.group(1).strip() if simple else ""
    prompts = split_prompts(body[start:])
    return [{"number": 1, "title": title, "prompts": prompts}] if prompts else []


def split_prompts(body: str) -> list[str]:
    """Parse the Del-body into a list of prompts.

    Strategy: walk line-by-line. A new prompt starts when a line begins
    with an imperative opener (Skapa, Ge, Föreslå, …). Continuation
    lines (wrapped PDF text) are glued onto the current prompt.

    This is more robust than blank-line paragraph splitting because
    the source PDFs have stray "1." bullet artifacts and occasional
    missing blank lines that break the paragraph assumption.
    """
    lines = [l.strip() for l in body.splitlines()]
    # Strip leading bullets then drop noise lines (page numbers, stray "1." bullets, separators)
    lines = [strip_bullet(l) for l in lines]
    lines = [l for l in lines if l and not is_noise(l)]

    prompts = []
    current = []
    for line in lines:
        if starts_prompt(line):
            # Flush the previous prompt, if any
            if current:
                p = " ".join(current).strip()
                p = re.sub(r"\s+", " ", p)
                if len(p) >= 20 and is_prompt(p):
                    prompts.append(p)
            current = [line]
        elif current:
            # Continuation of the current prompt
            current.append(line)
        # Else: line before the first prompt opens — probably a subheading
        # like "(En del begrepp är på engelska...)". Skip it.

    # Flush the last prompt
    if current:
        p = " ".join(current).strip()
        p = re.sub(r"\s+", " ", p)
        if len(p) >= 20 and is_prompt(p):
            prompts.append(p)

    return prompts


def is_noise(line: str) -> bool:
    """Is this line PDF-layout noise (page number, stray bullet, separator)?"""
    if re.fullmatch(r"\d{1,3}\.?", line):     # "5" or "12."
        return True
    if re.fullmatch(r"[\s\-_—–]+", line):     # horizontal rules
        return True
    return False


def starts_prompt(line: str) -> bool:
    """Does this line open a new prompt (first word is an imperative)?"""
    first = line.split(None, 1)[0] if line else ""
    return first in IMPERATIVE_OPENERS


# First-word heuristic: prompts consistently open with an imperative verb
# (SV or EN — packs like "10 Engelska gymnasiet" have prompts in English)
# or a question word. If the paragraph doesn't start with one of these AND
# has no [brackets], it's probably a subheading.
IMPERATIVE_OPENERS = {
    # Swedish imperatives
    "Skapa", "Ge", "Föreslå", "Skriv", "Förklara", "Använd",
    "Utveckla", "Lista", "Gör", "Bygg", "Rita", "Utforma",
    "Identifiera", "Beskriv", "Sammanfatta", "Analysera",
    "Hjälp", "Planera", "Designa", "Producera", "Jämför",
    "Berätta", "Rekommendera", "Översätt", "Visa",
    # Swedish question openers and research-style openers
    "Vad", "Hur", "Varför", "När", "Vilka", "Vilken", "Vilket",
    "Baserat", "Enligt", "Utifrån",
    # English imperatives (used in English-subject packs)
    "Create", "Give", "Suggest", "Write", "Explain", "Use",
    "Develop", "List", "Make", "Build", "Design", "Produce",
    "Identify", "Describe", "Summarize", "Summarise", "Analyze", "Analyse",
    "Help", "Plan", "Compare", "Tell", "Recommend", "Translate", "Show",
    "Draw", "Outline",
    # English question openers
    "What", "How", "Why", "When", "Which", "Who",
}

# Leading bullet characters to strip before checking the opener
BULLET_PREFIX_RE = re.compile(r"^[•●◦‣⁃\-*]\s+")


def strip_bullet(line: str) -> str:
    """Strip leading bullet-point characters (•, ●, -, *, etc.)."""
    return BULLET_PREFIX_RE.sub("", line)


def is_prompt(text: str) -> bool:
    """Heuristic: is this paragraph a prompt rather than a subheading?"""
    if "[" in text and "]" in text:
        return True
    first = text.split(None, 1)[0] if text else ""
    return first in IMPERATIVE_OPENERS


def extract_pack(pack: dict) -> dict:
    """Extract one pack's structured data."""
    folder = SOURCE_DIR / pack["folder"]
    pdf = find_pdf(folder)
    if not pdf:
        raise RuntimeError(f"No PDF found in {folder}")

    text = pdftotext(pdf)

    count_match = COVER_COUNT_RE.search(text)
    cover_count = int(count_match.group(1)) if count_match else None

    parts = extract_parts(text)

    return {
        "folder": pack["folder"],
        "slug_sv": pack.get("slug_sv"),
        "slug_en": pack.get("slug_en"),
        "cover_count": cover_count,
        "total_prompts": sum(len(p["prompts"]) for p in parts),
        "parts": parts,
    }


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    targets = [p for p in PACKS if only is None or only in (p.get("slug_sv"), p.get("slug_en"))]
    if not targets:
        print(f"No packs matched '{only}'")
        return 1

    for pack in targets:
        try:
            data = extract_pack(pack)
        except Exception as e:
            print(f"  ✗ {pack['folder']}: {e}")
            continue

        out = DATA_DIR / f"{pack.get('slug_sv') or pack.get('slug_en')}.json"
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        sv_lbl = "SV-only" if pack.get("sv_only") else "translatable"
        sp = " [SPECIAL]" if pack.get("special") else ""
        print(f"  ✓ {pack['folder']:<40s} → {out.name}  "
              f"({data['total_prompts']} prompts · {len(data['parts'])} parts · {sv_lbl}{sp})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
