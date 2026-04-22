#!/usr/bin/env python3
"""Translate Swedish prompt JSON files to English via the Anthropic API.

For every translatable pack (not sv_only), reads exports/prompts/data/<slug_sv>.json
and writes exports/prompts/data/<slug_en>-en.json with the part titles and
prompts translated to English. The structure mirrors the SV file so the
downstream generator can consume it the same way.

Bracketed placeholders like [årskurs X] must stay intact, but translated:
  [årskurs X]              → [grade X]
  [ämne]                   → [subject]
  [specifikt tema]         → [specific theme]

Uses claude-sonnet-4-6 by default (good balance of quality and cost).
Skips packs that already have EN data unless --force is passed.

Prerequisites:
  pip install anthropic
  export ANTHROPIC_API_KEY=sk-ant-...

Run:
  python3 exports/prompts/translate-prompts.py            # all packs
  python3 exports/prompts/translate-prompts.py larare     # single pack
  python3 exports/prompts/translate-prompts.py --force    # retranslate all
"""
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from manifest import PACKS

DATA_DIR = Path(__file__).parent / "data"
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 8000  # enough for ~120 prompts per pack

SYSTEM = """You translate Swedish AI-prompt templates for school teachers into natural, professional English.

Rules:
1. Output MUST be valid JSON — match the input schema exactly.
2. Preserve [bracketed placeholders] but translate the Swedish inside them to English. Examples:
   [årskurs X]              → [grade X]
   [ämne]                   → [subject]
   [ämnesområde]            → [subject area]
   [specifikt tema]         → [specific theme]
   [specifikt moment]       → [specific unit]
   [komplext begrepp]       → [complex concept]
   [historiskt skeende]     → [historical event]
   [t.ex. addition]         → [e.g. addition]
3. Keep English pedagogical terms that already appear in Swedish source as-is:
   spaced repetition, active recall, interleaved practice, dual coding,
   scaffolding, chunking, metacognition, self-explanation, elaborative interrogation,
   peer learning, feedback loops, concrete examples.
4. Use international English terms (not US- or UK-specific): "grade" not "year",
   "Upper Secondary" for gymnasium, "PE" for Idrott och hälsa, "Social Studies"
   for Samhällskunskap, "Home Economics" for HKK, "Crafts" for Slöjd,
   "Religious Studies" for Religion.
5. Part titles: translate naturally, keep it short and professional.
6. Tone: clear, direct, practical — written for teachers and school leaders.
7. DO NOT add translator notes, editorial framings, or meta-commentary about
   why English terms are used. Translate only what's in the source. Never add
   sentences like "these terms are kept in English because..." — they didn't
   exist in the source and must not appear in the translation.

Return ONLY the JSON object, nothing else."""


def translate_pack(client, pack: dict, data: dict) -> dict:
    """Call Claude to translate one pack's parts + prompts."""
    # Send a compact payload: just parts with their titles and prompts
    parts_payload = [
        {"number": p["number"], "title": p["title"], "prompts": p["prompts"]}
        for p in data["parts"]
    ]
    user_msg = json.dumps({
        "target_audience": pack.get("eyebrow_en", ""),
        "parts": parts_payload,
    }, ensure_ascii=False)

    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
    ) as stream:
        chunks = [text for text in stream.text_stream]
    out_text = "".join(chunks).strip()

    # Strip code fences if the model added them
    if out_text.startswith("```"):
        out_text = out_text.strip("`")
        # remove optional "json" after opening fence
        if out_text.lstrip().startswith("json"):
            out_text = out_text.lstrip()[4:].lstrip()
        out_text = out_text.rstrip("`").strip()

    translated = json.loads(out_text)

    # Re-emit with same shape as the SV file. The generator looks for
    # `title` (part title) and `prompts` — we use `title` to store EN title
    # so the downstream render_parts_en uses it directly.
    new_parts = []
    for src_p, t_p in zip(data["parts"], translated.get("parts", [])):
        new_parts.append({
            "number": src_p["number"],
            "title": t_p.get("title", "").strip(),
            "prompts": t_p.get("prompts", []),
        })

    return {
        "folder": pack["folder"],
        "slug_sv": pack.get("slug_sv"),
        "slug_en": pack.get("slug_en"),
        "cover_count": data.get("cover_count"),
        "total_prompts": sum(len(p["prompts"]) for p in new_parts),
        "parts": new_parts,
    }


def translate_megaprompts(client, pack: dict, data: dict) -> dict:
    """Translate a megapromptar pack (different schema: structured sections)."""
    mps_payload = [
        {
            "number": mp["number"],
            "title": mp["title"],
            "sections": [{"heading": s["heading"], "body": s["body"]} for s in mp["sections"]],
        }
        for mp in data["megaprompts"]
    ]
    user_msg = json.dumps({
        "target_audience": pack.get("eyebrow_en", ""),
        "note": "Keep the 'heading' field EXACTLY as the Swedish source (do not translate). Translate only 'title' and each section's 'body'. The renderer maps Swedish headings to English labels.",
        "megaprompts": mps_payload,
    }, ensure_ascii=False)

    with client.messages.stream(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
    ) as stream:
        chunks = [text for text in stream.text_stream]
    out_text = "".join(chunks).strip()

    if out_text.startswith("```"):
        out_text = out_text.strip("`")
        if out_text.lstrip().startswith("json"):
            out_text = out_text.lstrip()[4:].lstrip()
        out_text = out_text.rstrip("`").strip()

    translated = json.loads(out_text)

    new_mps = []
    for src_mp, t_mp in zip(data["megaprompts"], translated.get("megaprompts", [])):
        new_sections = []
        for s_src, s_t in zip(src_mp["sections"], t_mp.get("sections", [])):
            new_sections.append({
                "heading": s_src["heading"],
                "body": s_t.get("body", "").strip(),
            })
        new_mps.append({
            "number": src_mp["number"],
            "title": t_mp.get("title", "").strip(),
            "sections": new_sections,
        })

    return {
        "folder": pack["folder"],
        "slug_sv": pack.get("slug_sv"),
        "slug_en": pack.get("slug_en"),
        "cover_count": data.get("cover_count"),
        "total_prompts": len(new_mps),
        "megaprompts": new_mps,
    }


def main():
    try:
        from anthropic import Anthropic
    except ImportError:
        print("ERROR: pip install anthropic")
        return 1

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: set ANTHROPIC_API_KEY")
        return 1

    force = "--force" in sys.argv
    slug_filter = next((a for a in sys.argv[1:] if not a.startswith("--")), None)

    client = Anthropic()
    start = time.time()

    translatable = [
        p for p in PACKS
        if not p.get("sv_only") and p.get("slug_en")
        and (slug_filter is None or slug_filter in (p.get("slug_en"), p.get("slug_sv")))
    ]

    done = 0
    skipped = 0
    errors = 0

    for pack in translatable:
        slug_sv = pack["slug_sv"]
        slug_en = pack["slug_en"]
        sv_path = DATA_DIR / f"{slug_sv}.json"
        en_path = DATA_DIR / f"{slug_en}-en.json"

        if not sv_path.exists():
            print(f"  ⚠ {slug_sv}: SV data missing, skipping")
            skipped += 1
            continue

        if en_path.exists() and not force:
            print(f"  ⟶ {slug_en}: already translated (use --force to redo)")
            skipped += 1
            continue

        try:
            sv_data = json.load(open(sv_path))
            if sv_data["total_prompts"] == 0:
                print(f"  ⚠ {slug_sv}: no prompts, skipping")
                skipped += 1
                continue

            t0 = time.time()
            if "megaprompts" in sv_data:
                en_data = translate_megaprompts(client, pack, sv_data)
                count_label = f"{en_data['total_prompts']:>3} megaprompts"
            else:
                en_data = translate_pack(client, pack, sv_data)
                count_label = f"{en_data['total_prompts']:>3} prompts"
            en_path.write_text(json.dumps(en_data, ensure_ascii=False, indent=2), encoding="utf-8")
            dt = time.time() - t0
            print(f"  ✓ {slug_en:<35s} ({count_label}, {dt:.1f}s)")
            done += 1
        except Exception as e:
            print(f"  ✗ {slug_en}: {type(e).__name__}: {e}")
            errors += 1

    total = time.time() - start
    print(f"\nTranslated {done} packs · skipped {skipped} · errors {errors} · {total:.0f}s total")
    return 0 if errors == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
