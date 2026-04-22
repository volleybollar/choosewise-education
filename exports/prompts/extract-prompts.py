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

    # Megapromptar have their own structure — long multi-section prompts,
    # not a flat list. Hand them off to the dedicated extractor.
    if pack.get("special"):
        return extract_megapromptar_pack(pack, text)

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


# ══════════════════════════════════════════════════════════════════════
# MEGAPROMPTAR EXTRACTION
#
# Each Megaprompt volume has 5 Megaprompts. Each is a long structured
# prompt with labelled sections (#SAMMANHANG, #MÅL, #SVARSRIKTLINJER …).
# Output schema differs from regular packs:
#   {megaprompts: [{number, title, sections: [{heading, body}, ...]}]}
# ══════════════════════════════════════════════════════════════════════

MEGA_TITLE_RE = re.compile(
    r"^\s*Megaprompt\s*#(\d+)\s*[-–—]\s*(.+?)\s*$",
    re.MULTILINE,
)
# Section headers look like "#SAMMANHANG:", possibly with trailing spaces
SECTION_HEADER_RE = re.compile(r"^\s*#([A-ZÅÄÖ][A-ZÅÄÖ0-9 \-/]*?):\s*$", re.MULTILINE)


def extract_megapromptar_pack(pack: dict, text: str) -> dict:
    """Parse the Megapromptar volume into a list of structured megaprompts."""
    # Skip boilerplate — start from the first "Megaprompt #N - Title" marker
    title_marks = list(MEGA_TITLE_RE.finditer(text))
    megaprompts = []
    for i, m in enumerate(title_marks):
        number = int(m.group(1))
        title = m.group(2).strip()
        body_start = m.end()
        body_end = title_marks[i + 1].start() if i + 1 < len(title_marks) else len(text)
        body = text[body_start:body_end]
        megaprompts.append({
            "number": number,
            "title": title,
            "sections": parse_megaprompt_sections(body),
        })

    return {
        "folder": pack["folder"],
        "slug_sv": pack.get("slug_sv"),
        "slug_en": pack.get("slug_en"),
        "cover_count": len(megaprompts),  # e.g. "5 Megaprompts"
        "total_prompts": len(megaprompts),
        "megaprompts": megaprompts,
    }


def parse_megaprompt_sections(body: str) -> list:
    """Split a single Megaprompt body on #HEADING: markers."""
    marks = list(SECTION_HEADER_RE.finditer(body))
    if not marks:
        # No structured sections found — return body as one unnamed section
        cleaned = _clean_body(body)
        return [{"heading": "", "body": cleaned}] if cleaned else []

    sections = []
    for i, m in enumerate(marks):
        heading = m.group(1).strip()
        start = m.end()
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        raw = body[start:end]
        cleaned = _clean_body(raw)
        if cleaned:
            sections.append({"heading": heading, "body": cleaned})
    return sections


# The Megapromptar PDFs were typeset in a font whose fi/fl ligatures aren't
# decomposed by pdftotext — e.g. "reflektion" comes out as "re ektion".
# Apply a targeted replacement dictionary. Swedish ligature-breaking is
# mechanical: just reinsert "fi" or "fl" at the stripped location.
_LIGATURE_FIXES = {
    # fl
    "re ektion":      "reflektion",
    "re ektera":      "reflektera",
    "re ekter":       "reflekter",
    "själv ektion":   "självreflektion",
    " ervals":        " flervals",
    " yt":            " flyt",
    " öde":           " flöde",
    " öden":          " flöden",
    " exibel":        " flexibel",
    " exibla":        " flexibla",
    " exibilitet":    " flexibilitet",
    "in uens":        "influens",
    " era ":          " flera ",
    # fi
    "speci k":        "specifik",
    "speci ka":       "specifika",
    "de niera":       "definiera",
    "de nition":      "definition",
    "identi era":     "identifiera",
    "identi kation":  "identifikation",
    "klassi cera":    "klassificera",
    "klassi kation":  "klassifikation",
    "certi era":      "certifiera",
    "fotogra er":     "fotografier",
    "fotogra ": "fotografi",  # Fotografier less common; this catches "gra ..." starting
    "gra k":          "grafik",
    "gra sk":         "grafisk",
    "gra ska":        "grafiska",
    " nns":           "finns",
    " nna":           "finna",
    " nner":          "finner",
    " gur":           "figur",
    "verk ga":        "verkliga",
    " ktiv":          "fiktiv",
    " ende ":         "fiende ",
}


def _fix_ligatures(text: str) -> str:
    for broken, fixed in _LIGATURE_FIXES.items():
        text = text.replace(broken, fixed)
    # Drop stray ligature-remnant lines like "fl fl fi fl fl fl fl"
    text = re.sub(r"(?m)^\s*(?:fi|fl)(?:\s+(?:fi|fl))+\s*$", "", text)
    return text


def _clean_body(raw: str) -> str:
    """Normalise a Megaprompt section body.

    - Fix soft-wrapped lines: join within paragraphs, preserve numbered/bullet items
    - Drop page-number noise and footer repetition
    - Collapse runs of whitespace; keep explicit double newlines (paragraph breaks)
    - Reconstruct missing Swedish fi/fl ligatures introduced by pdftotext
    """
    raw = _fix_ligatures(raw)
    lines = [l.rstrip() for l in raw.splitlines()]
    # Drop the chattpromptar footer if it leaks in ("    N" at bottom of page)
    lines = [l for l in lines if not re.fullmatch(r"\s*\d{1,3}\s*", l)]

    # Rejoin wrapped lines: a line that doesn't start with a numbered bullet
    # or sub-bullet is a continuation of the previous line.
    out = []
    for line in lines:
        stripped = line.lstrip()
        if not stripped:
            # Blank line — paragraph separator. Keep at most one blank.
            if out and out[-1] != "":
                out.append("")
            continue
        is_bullet = bool(
            re.match(r"^(\d+\.\s+|\-\s+|\*\*|\*\s+|[•●◦‣⁃]\s+|#[A-ZÅÄÖ])", stripped)
        )
        if is_bullet or not out or out[-1] == "":
            out.append(stripped)
        else:
            # Continuation of the previous line
            out[-1] = out[-1] + " " + stripped

    # Drop leading/trailing blanks
    while out and out[0] == "":
        out.pop(0)
    while out and out[-1] == "":
        out.pop()

    return "\n".join(out)


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
        sp = " [MEGA]" if pack.get("special") else ""
        # Megapromptar packs have `megaprompts`, regular packs have `parts`
        n_blocks = len(data.get("parts", data.get("megaprompts", [])))
        block_lbl = "megaprompts" if pack.get("special") else "parts"
        print(f"  ✓ {pack['folder']:<40s} → {out.name}  "
              f"({data['total_prompts']} prompts · {n_blocks} {block_lbl} · {sv_lbl}{sp})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
