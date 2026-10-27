#!/usr/bin/env python3
"""Ask Crossref whether a source has been retracted, flagged or corrected.

Crossref links each notice (retraction, expression of concern, correction) to
the article it updates; Retraction Watch data is included. A DOI with no
notices is "clean".

Usage:
    /usr/bin/python3 scripts/audit_retraction_check.py DOI [DOI ...]
"""
from __future__ import annotations

import json
import sys
from urllib.parse import quote
from urllib.request import Request, urlopen

API = "https://api.crossref.org/works?filter=updates:{doi}&rows=50"
STATUS_BY_TYPE = {
    "retraction": "retracted",
    "withdrawal": "retracted",
    "removal": "retracted",
    "expression_of_concern": "concern",
    "correction": "corrected",
    "erratum": "corrected",
}
SEVERITY = ["clean", "corrected", "concern", "retracted"]


def check_doi(doi: str, fetch=urlopen) -> dict:
    request = Request(API.format(doi=quote(doi, safe="/")), headers={"User-Agent": "choosewise-evidence-audit/1.0"})
    items = json.loads(fetch(request).read())["message"]["items"]
    status, notices = "clean", []
    for item in items:
        for update in item.get("update-to", []):
            if update.get("DOI", "").lower() != doi.lower():
                continue
            found = STATUS_BY_TYPE.get(update.get("type"))
            if found is None:
                continue
            if item["DOI"] not in notices:
                notices.append(item["DOI"])
            if SEVERITY.index(found) > SEVERITY.index(status):
                status = found
    return {"doi": doi, "status": status, "notices": notices}


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        print(json.dumps(check_doi(arg)))
