#!/usr/bin/env python3
"""Ask Crossref whether a source has been retracted, flagged or corrected.

Two lookups per DOI: the work itself (it must exist, and its "updated-by"
field carries Retraction Watch records) and every notice that updates it.
A DOI with no notices is "clean". An update type this script does not know
is reported as "concern" so a person looks at it, never silently dropped.

Usage:
    /usr/bin/python3 scripts/audit_retraction_check.py DOI [DOI ...]
"""
from __future__ import annotations

import json
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

WORK = "https://api.crossref.org/works/{doi}"
NOTICES = "https://api.crossref.org/works?filter=updates:{doi}&rows=50"
STATUS_BY_TYPE = {
    "retraction": "retracted",
    "withdrawal": "retracted",
    "removal": "retracted",
    "partial_retraction": "retracted",
    "expression_of_concern": "concern",
    "correction": "corrected",
    "corrigendum": "corrected",
    "erratum": "corrected",
    "new_version": "clean",
}
SEVERITY = ["clean", "corrected", "concern", "retracted"]
PREFIX = re.compile(r"^(https?://(dx\.)?doi\.org/|doi:)", re.IGNORECASE)
TIMEOUT = 30


def normalise_doi(doi: str) -> str:
    doi = PREFIX.sub("", doi.strip()).strip().lower()
    if not doi.startswith("10."):
        raise ValueError(f"not a DOI: {doi!r}")
    return doi


def _get(url: str, fetch) -> dict:
    request = Request(url, headers={"User-Agent": "choosewise-evidence-audit/1.0"})
    return json.loads(fetch(request, timeout=TIMEOUT).read())["message"]


def check_doi(doi: str, fetch=urlopen) -> dict:
    doi = normalise_doi(doi)
    path = quote(doi, safe="/")
    try:
        work = _get(WORK.format(doi=path), fetch)
    except HTTPError as error:
        if error.code == 404:
            raise ValueError(f"Crossref does not know {doi}") from error
        raise

    updates = [(u, u.get("DOI")) for u in work.get("updated-by", [])]
    for item in _get(NOTICES.format(doi=path), fetch)["items"]:
        updates += [(u, item["DOI"]) for u in item.get("update-to", []) if u.get("DOI", "").lower() == doi]

    status, notices, types = "clean", [], []
    for update, notice_doi in updates:
        kind = update.get("type", "unknown")
        found = STATUS_BY_TYPE.get(kind, "concern")
        if found == "clean":
            continue
        if kind not in types:
            types.append(kind)
        if notice_doi and notice_doi not in notices:
            notices.append(notice_doi)
        if SEVERITY.index(found) > SEVERITY.index(status):
            status = found
    return {"doi": doi, "status": status, "notices": notices, "types": types}


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        try:
            print(json.dumps(check_doi(arg)))
        except (ValueError, HTTPError, URLError) as error:
            print(json.dumps({"doi": arg, "error": str(error)}))
