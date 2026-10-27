"""Tests for scripts/audit_retraction_check.py (Evidence Toolkit audit, 2026-10)."""
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audit_retraction_check import check_doi  # noqa: E402

DOI = "10.1234/example.2025.1"


def _fake_fetch(items):
    """Stand-in for urlopen: returns a Crossref-shaped works response."""
    def fetch(request):
        assert f"updates:{DOI}" in request.full_url
        return io.BytesIO(json.dumps({"message": {"items": items}}).encode())
    return fetch


def _notice(notice_doi, update_type):
    return {"DOI": notice_doi, "update-to": [{"DOI": DOI, "type": update_type}]}


def test_retraction_notice_gives_retracted():
    result = check_doi(DOI, fetch=_fake_fetch([_notice("10.1234/retraction", "retraction")]))
    assert result == {"doi": DOI, "status": "retracted", "notices": ["10.1234/retraction"]}


def test_empty_items_gives_clean():
    assert check_doi(DOI, fetch=_fake_fetch([])) == {"doi": DOI, "status": "clean", "notices": []}


def test_correction_gives_corrected():
    result = check_doi(DOI, fetch=_fake_fetch([_notice("10.1234/corr", "correction")]))
    assert result["status"] == "corrected"


def test_notice_reported_by_two_sources_listed_once():
    # Crossref lists the same notice once from the publisher and once from Retraction Watch.
    notice = {"DOI": "10.1234/retraction", "update-to": [
        {"DOI": DOI, "type": "retraction", "source": "publisher"},
        {"DOI": DOI, "type": "retraction", "source": "retraction-watch"},
    ]}
    assert check_doi(DOI, fetch=_fake_fetch([notice]))["notices"] == ["10.1234/retraction"]


def test_retraction_outranks_correction():
    items = [_notice("10.1234/corr", "correction"), _notice("10.1234/retraction", "retraction")]
    assert check_doi(DOI, fetch=_fake_fetch(items))["status"] == "retracted"
