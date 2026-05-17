"""Tests for scripts/build-evidence-cards.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Import via importlib because the script name has a hyphen.
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "build_evidence_cards",
    Path(__file__).resolve().parents[1] / "build-evidence-cards.py",
)
build = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build)


def test_band_for_months_below():
    assert build.band_for_months(2) == "below"
    assert build.band_for_months(0) == "below"
    assert build.band_for_months(None) is None


def test_band_for_months_around():
    assert build.band_for_months(3) == "around"
    assert build.band_for_months(4) == "around"


def test_band_for_months_above():
    assert build.band_for_months(5) == "above"
    assert build.band_for_months(8) == "above"


def test_band_for_d_below():
    assert build.band_for_d(0.10) == "below"
    assert build.band_for_d(0.29) == "below"
    assert build.band_for_d(None) is None


def test_band_for_d_around():
    assert build.band_for_d(0.30) == "around"
    assert build.band_for_d(0.59) == "around"


def test_band_for_d_above():
    assert build.band_for_d(0.60) == "above"
    assert build.band_for_d(1.20) == "above"


SAMPLE_SKILL = {
    "id": "memory-learning-science/spaced-practice-scheduler",
    "manning_name": "spaced-practice-scheduler",
    "display_title": "Spaced Practice Scheduler",
    "description": "Schedule retrieval intervals across a unit so learning is distributed, not massed.",
    "tags": ["spaced", "retrieval"],
    "effect_months": 5,
    "effect_months_source": "EEF Toolkit — Spaced learning strand",
    "effect_months_year": 2021,
    "effect_d": 0.60,
    "effect_d_source": "Latimier, Peyre & Ramus",
    "effect_d_journal": "Educational Psychology Review",
    "effect_d_year": 2021,
    "implementation_cost": "low",
    "implementation_cost_rationale": "Runs inside existing lessons.",
    "manning_label": "strong",
    "manning_url": "https://example.com/skill",
    "verification_status": "verified",
}


def test_render_card_contains_title():
    html = build.render_card(SAMPLE_SKILL, domain_label="Memory & Learning Science")
    assert "Spaced Practice Scheduler" in html


def test_render_card_contains_description():
    html = build.render_card(SAMPLE_SKILL, domain_label="Memory & Learning Science")
    assert "Schedule retrieval intervals" in html


def test_render_card_months_pill_has_above_band_class():
    html = build.render_card(SAMPLE_SKILL, domain_label="Memory & Learning Science")
    assert "metric-pill metric-pill--months band-above" in html
    assert "+5 months" in html


def test_render_card_d_pill_has_above_band_class():
    html = build.render_card(SAMPLE_SKILL, domain_label="Memory & Learning Science")
    assert "metric-pill metric-pill--d band-above" in html
    assert "d = 0.60" in html


def test_render_card_implementation_cost_low_pill():
    html = build.render_card(SAMPLE_SKILL, domain_label="Memory & Learning Science")
    assert "impl-pill impl-pill--low" in html
    assert ">Low<" in html


def test_render_card_includes_tags():
    html = build.render_card(SAMPLE_SKILL, domain_label="Memory & Learning Science")
    assert ">spaced<" in html
    assert ">retrieval<" in html


def test_render_card_includes_interrogate_link():
    html = build.render_card(SAMPLE_SKILL, domain_label="Memory & Learning Science")
    assert 'data-action="interrogate"' in html
    assert 'data-skill-id="memory-learning-science/spaced-practice-scheduler"' in html


def test_render_card_includes_source_attribution():
    html = build.render_card(SAMPLE_SKILL, domain_label="Memory & Learning Science")
    assert "Latimier, Peyre &amp; Ramus" in html
    assert "Educational Psychology Review" in html
    assert "2021" in html
    assert "EEF Toolkit" in html


def test_render_card_missing_effect_d_shows_no_data():
    skill = {**SAMPLE_SKILL, "effect_d": None, "effect_d_source": None, "effect_d_journal": None, "effect_d_year": None}
    html = build.render_card(skill, domain_label="Memory & Learning Science")
    assert "no independent meta-analysis found" in html
    assert "metric-pill--d band-none" in html


def test_render_card_missing_effect_months_shows_no_data():
    skill = {**SAMPLE_SKILL, "effect_months": None, "effect_months_source": None, "effect_months_year": None}
    html = build.render_card(skill, domain_label="Memory & Learning Science")
    assert "no EEF strand" in html
    assert "metric-pill--months band-none" in html


def test_inject_replaces_between_markers():
    template = (
        "<html><body>"
        "<!-- cards:start -->\n"
        "OLD CONTENT\n"
        "<!-- cards:end -->"
        "</body></html>"
    )
    result = build.inject_into_template(template, "NEW CONTENT")
    assert "OLD CONTENT" not in result
    assert "NEW CONTENT" in result
    assert "<!-- cards:start -->" in result
    assert "<!-- cards:end -->" in result


def test_inject_raises_when_markers_missing():
    import pytest
    template = "<html><body>no markers</body></html>"
    with pytest.raises(ValueError, match="cards:start"):
        build.inject_into_template(template, "NEW")
