"""Tests for scripts/audit_retraction_check.py (Evidence Toolkit audit, 2026-10)."""
import io
import json
import sys
from pathlib import Path
from urllib.error import HTTPError

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audit_retraction_check import check_doi  # noqa: E402

DOI = "10.1234/example.2025.1"


def _fake_fetch(items, updated_by=None, exists=True):
    """Stand-in for urlopen: answers the work lookup and the updates filter like Crossref."""
    def fetch(request, timeout=None):
        url = request.full_url
        if "filter=updates:" in url:
            assert f"updates:{DOI}" in url
            return io.BytesIO(json.dumps({"message": {"items": items}}).encode())
        assert url.endswith(f"/works/{DOI}")
        if not exists:
            raise HTTPError(url, 404, "Not Found", {}, None)
        return io.BytesIO(json.dumps({"message": {"DOI": DOI, "updated-by": updated_by or []}}).encode())
    return fetch


def _notice(notice_doi, update_type):
    return {"DOI": notice_doi, "update-to": [{"DOI": DOI, "type": update_type}]}


def test_retraction_notice_gives_retracted():
    result = check_doi(DOI, fetch=_fake_fetch([_notice("10.1234/retraction", "retraction")]))
    assert result == {"doi": DOI, "status": "retracted", "notices": ["10.1234/retraction"], "types": ["retraction"]}


def test_empty_items_gives_clean():
    assert check_doi(DOI, fetch=_fake_fetch([])) == {"doi": DOI, "status": "clean", "notices": [], "types": []}


def test_correction_gives_corrected():
    result = check_doi(DOI, fetch=_fake_fetch([_notice("10.1234/corr", "correction")]))
    assert result["status"] == "corrected"


def test_corrigendum_gives_corrected():
    result = check_doi(DOI, fetch=_fake_fetch([_notice("10.1234/corr", "corrigendum")]))
    assert result["status"] == "corrected"


def test_unknown_update_type_is_flagged_not_dropped():
    result = check_doi(DOI, fetch=_fake_fetch([_notice("10.1234/add", "addendum")]))
    assert result["status"] == "concern"
    assert result["types"] == ["addendum"]


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


def test_updated_by_on_the_work_counts_even_without_a_notice_work():
    # Retraction Watch records can sit on the work itself with no separate notice DOI.
    updated_by = [{"DOI": "10.1234/rw", "type": "retraction", "source": "retraction-watch"}]
    assert check_doi(DOI, fetch=_fake_fetch([], updated_by=updated_by))["status"] == "retracted"


@pytest.mark.parametrize("written", [f"https://doi.org/{DOI}", f"doi:{DOI}", f"  {DOI.upper()} ", f"http://dx.doi.org/{DOI}"])
def test_doi_is_normalised_before_lookup(written):
    result = check_doi(written, fetch=_fake_fetch([_notice("10.1234/retraction", "retraction")]))
    assert result["doi"] == DOI
    assert result["status"] == "retracted"


@pytest.mark.parametrize("not_a_doi", ["unconfirmed", "", "example.org/paper"])
def test_non_doi_is_refused(not_a_doi):
    with pytest.raises(ValueError):
        check_doi(not_a_doi, fetch=_fake_fetch([]))


def test_unknown_doi_is_refused_not_clean():
    with pytest.raises(ValueError):
        check_doi(DOI, fetch=_fake_fetch([], exists=False))


def test_cli_reports_a_network_error_per_doi_and_continues():
    from urllib.error import URLError
    from audit_retraction_check import main

    def check(doi):
        if doi == "10.1/broken":
            raise URLError("timed out")
        return {"doi": doi, "status": "clean", "notices": [], "types": []}

    lines = [json.loads(line) for line in main(["10.1/broken", "10.1/fine"], check=check)]
    assert "error" in lines[0]
    assert lines[1]["status"] == "clean"
