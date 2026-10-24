"""Tester för scripts/build-gap-tracer-data.py och datan det skriver.

Gap Tracer visar Marbles förkunskapsgraf för lärare och föräldrar. Det
viktigaste testerna vaktar är att verktyget aldrig lovar mer än det håller:
inga skärmövningar som inte går att göra vid köksbordet, inga synliga
utelämningsmarkörer, inga läroplaner vi valt bort och en hasActivities-flagga
som stämmer. Spec: docs/superpowers/specs/2026-10-24-gap-tracer-design.md.
"""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "gap-tracer" / "data"
SOURCE = Path.home() / "Projekt" / "os-taxonomy"

# Import via importlib because the script name has a hyphen.
_spec = importlib.util.spec_from_file_location(
    "build_gap_tracer_data", ROOT / "scripts" / "build-gap-tracer-data.py",
)
gt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gt)


def activity(**fields):
    base = {"title": "x", "learnerActions": [], "intendedInsight": "", "feedback": []}
    base.update(fields)
    return base


def test_needs_screen_catches_app_steps():
    assert gt.needs_screen(activity(
        title="On-screen rehearsal",
        learnerActions=["Tap DROP so the character folds"],
    ))


def test_needs_screen_keeps_paper_folding():
    assert not gt.needs_screen(activity(
        title="Halve, then halve again",
        learnerActions=["Fold (or partition) a symmetrical shape such as a square "
                        "in half, then fold each half in half again"],
    ))


def test_needs_screen_ignores_fields_never_shown():
    assert not gt.needs_screen(activity(rationale="A manipulable on-screen model"))


def test_marker_only_counts_in_shown_fields():
    assert not gt.has_marker(activity(
        sourceClaims=["[curriculum wording omitted; reference 4-PS4-1]"],
    ))
    assert gt.has_marker(activity(
        feedback=["Compare with [curriculum wording omitted; reference 4-PS4-1]"],
    ))


def test_standard_labels():
    uk = {"uk-nc-2013:Ma/KS2/Y3/F/4": {"keyStage": "Key stage 2", "subject": "Mathematics"}}
    assert gt.standard_label("ccss-math:3.NF.3.a", uk) == "Common Core 3.NF.3.a"
    assert gt.standard_label("acara-v9:AC9M4N03", uk) == "Australian Curriculum AC9M4N03"
    assert gt.standard_label("uk-nc-2013:Ma/KS2/Y3/F/4", uk) == "England · Key stage 2 · Mathematics"
    assert gt.standard_label("ngss-k5:1-ESS1-1", uk) is None


# ---- Den committade datan i gap-tracer/data/ ----

def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def test_counts_match_meta():
    skills = load("skills.json")["skills"]
    counts = load("meta.json")["counts"]
    assert len(skills) == counts["skills"]
    assert sum(len(s["prereqs"]) for s in skills) == counts["dependencies"]
    assert sum(s["hasActivities"] for s in skills) == counts["skillsWithActivities"]


def test_no_markers_or_unfilled_placeholders_in_activities():
    # Markören, inte ordet: "If the Southern ocean is omitted…" är riktig text.
    bad = [p.name for p in (DATA / "activities").glob("*.json")
           if "[curriculum wording omitted" in p.read_text(encoding="utf-8")
           or "{{" in p.read_text(encoding="utf-8")]
    assert bad == []


def test_has_activities_matches_files():
    skills = load("skills.json")["skills"]
    files = {p.stem for p in (DATA / "activities").glob("*.json")}
    assert {s["id"] for s in skills if s["hasActivities"]} == files


def test_no_dropped_curricula_in_output():
    # NGSS, Ontario, IB och C3 visas inte (spec §4.3). Kontrollen går på
    # etiketterna och inte på hela filen: slumpade id:n som "mt_Abc3-…"
    # skulle annars ge falsklarm.
    labels = {label for s in load("skills.json")["skills"] for label in s["standards"]}
    kept = ("Common Core ", "Australian Curriculum ", "England · ")
    assert [label for label in labels if not label.startswith(kept)] == []


def test_activities_only_in_maths_and_science():
    skills = load("skills.json")["skills"]
    assert {s["subject"] for s in skills if s["hasActivities"]} <= {"Mathematics", "Science"}


def test_build_is_deterministic(tmp_path):
    if not (SOURCE / "data").exists():
        pytest.skip("~/Projekt/os-taxonomy saknas")
    a, b = tmp_path / "a", tmp_path / "b"
    gt.build(SOURCE, a, "2026-10-24")
    gt.build(SOURCE, b, "2026-10-24")
    files_a = sorted(p.relative_to(a) for p in a.rglob("*") if p.is_file())
    files_b = sorted(p.relative_to(b) for p in b.rglob("*") if p.is_file())
    assert files_a == files_b
    assert all((a / f).read_bytes() == (b / f).read_bytes() for f in files_a)


# ---- Slutgranskningen: skärmövningar som slank igenom, och NGSS ----

def test_needs_screen_catches_simulation_phrases():
    for text in [
        "Seed a few polyps and watch (or step through) as they divide",
        "Watch a species counter climb as the structure grows",
        "Melt components one at a time and observe a sea-level gauge",
        "OPTIONAL interaction if a chain tool is available: watch the bar",
        "An optional flythrough can display a light-travel-time counter",
        "Optional with a question panel that shades each bar",
        "In the model, see that much of the nutrient store is removed",
        "Use a planetarium/star app to spot the Plough",
    ]:
        assert gt.needs_screen(activity(learnerActions=[text])), text


def test_no_kept_activity_mentions_ngss():
    # NGSS visas inte (Johans beslut), och varumärkesnotisen krävs för varje
    # NGSS-omnämnande. En övning som nämner NGSS tas därför bort.
    bad = [p.name for p in (DATA / "activities").glob("*.json")
           if "ngss" in p.read_text(encoding="utf-8").lower()]
    assert bad == []
