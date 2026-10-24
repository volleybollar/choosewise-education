#!/usr/bin/env python3
"""Build the data files for /gap-tracer/ from Marble Skill Taxonomy.

Reads the JSON files in a local clone of withmarbleapp/os-taxonomy (no code
from that repo is run) and writes small files to gap-tracer/data/:

  skills.json            every skill: name, check question, evidence,
                         curriculum labels, prerequisites, hasActivities
  activities/<id>.json   practice activities, only for skills that keep any
  meta.json              Marble snapshot, build date and counts for the page

Filtering follows the spec (docs/superpowers/specs/2026-10-24-gap-tracer-design.md):
activities that need Marble's app are dropped, activities with a curriculum
omission marker in a shown field are dropped, and only Common Core, the
Australian Curriculum and the National Curriculum in England are kept.

Usage:
    /usr/bin/python3 scripts/build-gap-tracer-data.py ~/Projekt/os-taxonomy
    /usr/bin/python3 scripts/build-gap-tracer-data.py ~/Projekt/os-taxonomy --built-date 2026-10-24
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "gap-tracer" / "data"

# The only activity fields the page shows. Everything else (rationale,
# sourceClaims) stays out of the output, which also keeps out most of
# Marble's omission markers.
SHOWN_FIELDS = ("title", "learnerActions", "intendedInsight", "feedback")

KEPT_CURRICULA = ("ccss-math", "ccss-ela", "acara-v9", "uk-nc-2013")

# Words that mean an activity happens on a screen in Marble's app and can't
# be done with paper, objects and conversation. Better one good activity too
# many dropped than one screen activity left in (spec §6).
SCREEN_WORDS = (
    "tap", "taps", "tapping", "tapped",      # touch-screen gestures
    "drag", "drags", "dragging", "dragged", "draggable",  # moving things on a screen
    "swipe", "swipes", "swiping",
    "click", "clicks", "clicking",
    "slider", "sliders",                     # app controls
    "toggle", "toggles",
    "button", "buttons",
    "screen", "screens", "on-screen", "onscreen",
    "interactive",                           # "an interactive line", "interactive model"
    # Added after the first hand check (30 kept activities): these slipped through.
    "reveal", "reveals", "revealing", "revealed",  # "tap to reveal", "reveal each term in the scene"
    "flap", "flaps",                         # digital lift-the-flap labels
    "immersive", "first-person",             # "immersive view" of the night sky
    "simulation", "simulations", "simulated",
    "animation", "animated",
    "readout", "readouts",                   # "a live readout of the radius"
    "dial", "dials",                         # "turn the eruption dial"
    "zoom", "zooms",
    "in-role",                               # Marble's AI characters ("an in-role dentist")
    # Added after the final review: simulation language. Words that also name
    # real things ("virtual image", "device", "replay the count") stay out.
    "flythrough", "step through",            # "watch (or step through) as they divide"
    "gauge", "gauges",                       # "observe a sea-level gauge"
    "panel", "panels",                       # "a consequences panel", "a question panel"
    "app", "apps",                           # "a planetarium/star app"
    "time-lapse", "in the model",
    "species counter", "tool is available",
)

# NGSS isn't shown (Johan's decision 2026-10-24), and every NGSS reference
# needs WestEd's trademark notice. Activities that mention it are dropped.
NGSS_RE = re.compile(r"\bNGSS\b", re.IGNORECASE)
SCREEN_RE = re.compile(r"\b(?:" + "|".join(re.escape(w) for w in SCREEN_WORDS) + r")\b",
                       re.IGNORECASE)

MARKER = "[curriculum wording omitted"


def shown_text(activity: dict) -> str:
    """All text of the fields the page shows, joined."""
    parts = []
    for field in SHOWN_FIELDS:
        value = activity.get(field, "")
        parts.extend(value if isinstance(value, list) else [value])
    return "\n".join(parts)


def needs_screen(activity: dict) -> bool:
    """True if a shown field describes an on-screen step."""
    return bool(SCREEN_RE.search(shown_text(activity)))


def has_marker(activity: dict) -> bool:
    """True if a shown field contains Marble's omission marker."""
    return MARKER in shown_text(activity)


def standard_label(key: str, uk_index: dict) -> str | None:
    """Readable label for a curriculum key, or None for curricula we don't show."""
    slug, _, code = key.partition(":")
    if slug in ("ccss-math", "ccss-ela"):
        return f"Common Core {code}"
    if slug == "acara-v9":
        return f"Australian Curriculum {code}"
    if slug == "uk-nc-2013" and key in uk_index:
        # England has no official codes; Marble's ids mean nothing to a teacher.
        data = uk_index[key]
        parts = ["England", key_stage(data["keyStage"])]
        if data.get("subject"):  # about 50 Key Stage 3 records have no subject
            parts.append(data["subject"])
        return " · ".join(parts)
    return None


def key_stage(raw: str) -> str:
    """Marble spells it "Key Stage 2", "Key stage 2" and "KS3"; show one form."""
    m = re.match(r"(?i)^(lower |upper )?(?:key stage|ks)\s*(.+)$", raw.strip())
    if not m:
        return raw
    prefix = (m.group(1) or "").capitalize()
    return f"{prefix}key stage {m.group(2)}" if prefix else f"Key stage {m.group(2)}"


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True,
                               separators=(",", ":")) + "\n", encoding="utf-8")


def build(src: Path, out: Path, built_date: str) -> dict:
    data = src / "data"
    topics = json.loads((data / "topics.json").read_text(encoding="utf-8"))["topics"]
    deps = json.loads((data / "dependencies.json").read_text(encoding="utf-8"))["dependencies"]
    research = json.loads((data / "teaching-research.json").read_text(encoding="utf-8"))["records"]
    curricula = json.loads((data / "curriculum-standards.json").read_text(encoding="utf-8"))["curricula"]

    uk_index = {t["key"]: t["data"] for c in curricula if c["slug"] == "uk-nc-2013" for t in c["topics"]}

    prereqs: dict[str, list] = {}
    for d in deps:
        prereqs.setdefault(d["topicId"], []).append({"id": d["prerequisiteId"], "strength": d["strength"]})
    for edges in prereqs.values():
        edges.sort(key=lambda e: e["strength"] != "hard")  # stable: hard first, then file order

    removed_screen = removed_marker = removed_ngss = kept = 0
    activities: dict[str, list] = {}
    for record in research:
        keep = []
        for a in record["learn"]["activities"]:
            if has_marker(a):
                removed_marker += 1
            elif NGSS_RE.search(shown_text(a)):
                removed_ngss += 1
            elif needs_screen(a):
                removed_screen += 1
            else:
                keep.append({f: a[f] for f in SHOWN_FIELDS})
        if keep:
            activities[record["topicId"]] = keep
            kept += len(keep)

    skills = []
    for t in sorted(topics, key=lambda t: t["id"]):
        labels = []
        for key in t.get("standards", []):
            label = standard_label(key, uk_index)
            if label and label not in labels:
                labels.append(label)
        skills.append({
            "id": t["id"], "name": t["name"], "subject": t["subject"], "domain": t["domain"],
            "ageStart": t["ageRangeStart"], "ageEnd": t["ageRangeEnd"],
            "description": t["description"], "check": t["assessmentPrompt"],
            "evidence": t["evidence"], "standards": labels,
            "prereqs": prereqs.get(t["id"], []), "hasActivities": t["id"] in activities,
        })

    by_subject: dict[str, dict] = {}
    for s in skills:
        row = by_subject.setdefault(s["subject"], {"skills": 0, "withActivities": 0})
        row["skills"] += 1
        row["withActivities"] += s["hasActivities"]

    commit, _, date = subprocess.run(
        ["git", "-C", str(src), "log", "-1", "--format=%h|%cs"],
        capture_output=True, text=True, check=True,
    ).stdout.strip().partition("|")

    meta = {
        "marbleCommit": commit, "marbleDate": date, "builtDate": built_date,
        "counts": {
            "skills": len(skills),
            "dependencies": sum(len(s["prereqs"]) for s in skills),
            "skillsWithActivities": len(activities),
            "bySubject": by_subject,
            "activitiesKept": kept,
            "removedScreen": removed_screen,
            "removedMarker": removed_marker,
            "removedNgss": removed_ngss,
        },
    }

    act_dir = out / "activities"
    act_dir.mkdir(parents=True, exist_ok=True)
    for old in act_dir.glob("*.json"):  # skills can lose all activities between builds
        old.unlink()
    for topic_id, acts in activities.items():
        write_json(act_dir / f"{topic_id}.json", {"id": topic_id, "activities": acts})
    write_json(out / "skills.json", {"skills": skills})
    write_json(out / "meta.json", meta)
    return meta


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("source", type=Path, help="local clone of withmarbleapp/os-taxonomy")
    parser.add_argument("--built-date", default=datetime.date.today().isoformat())
    args = parser.parse_args()
    meta = build(args.source.expanduser(), OUT_DIR, args.built_date)
    c = meta["counts"]
    print(f"{c['skills']} skills, {c['dependencies']} prerequisites, "
          f"{c['skillsWithActivities']} with activities ({c['activitiesKept']} kept, "
          f"{c['removedScreen']} screen-only and {c['removedMarker']} with markers removed) "
          f"— Marble {meta['marbleCommit']} ({meta['marbleDate']})")


if __name__ == "__main__":
    main()
