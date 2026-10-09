"""Every relative asset path in a guide template must resolve on disk.

430f6d0 moved fourteen guide templates into _unpublished/exports/ without
re-pathing the images they reference: a relative ../assets/... that used to
resolve correctly from exports/ silently broke from its new, one-level-
deeper home. Chromium renders a missing <img> as a tiny broken-image
placeholder and prints its alt text as fallback body text — which the
character-level text fingerprint in test_guide_pdf_parity.py cannot tell
apart from real content (that is exactly how the gemini-notebooklm images
went missing for an entire task without the parity test noticing).

This guard is static — no render needed — and would have caught that break
the day it landed instead of several tasks later.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

# Same discovery regex as test_build_scripts.py's HTML_REF, duplicated
# rather than imported: scripts/tests/ is a package, and test files can't
# import each other directly (see pdf_fingerprint.py's docstring for why
# that module exists as a plain module instead of a test file).
HTML_REF = re.compile(r'["\']([\w./-]*exports/[\w.-]+\.html)["\']')

# The wave's eleven guide builders (build-guide-pdfs.py's BUILDERS, minus
# the dropped nlm one — see pdf_fingerprint.py's comment for why). Listed
# explicitly rather than globbed: exports/ also holds build-wise-pdf.py and
# build-wise-ratt-png.py, which are Johan's own and nothing to do with this
# wave's guide templates.
SCRIPTS = [
    ROOT / "exports" / name
    for name in [
        "build-claude-pdf.py",
        "build-claude-quickstart-pdf.py",
        "build-presentationsteknik-pdf.py",
        "build-presentationsteknik-quickstart-pdf.py",
        "build-gemini-notebooklm-pdf.py",
        "build-gemini-quickstart-pdf.py",
        "build-copilot-pdf.py",
        "build-copilot-quickstart-pdf.py",
        "build-apple-intelligence-pdf.py",
        "build-apple-intelligence-quickstart-pdf.py",
        "build-ai-for-elever-pdf.py",
    ]
]

ASSET_SRC = re.compile(r'(?:src|href)="(\.\.[^"]+)"')


def _templates() -> list[Path]:
    templates: set[Path] = set()
    for script in SCRIPTS:
        for ref in HTML_REF.findall(script.read_text(encoding="utf-8")):
            templates.add(ROOT / ref)
    return sorted(t for t in templates if t.exists())


@pytest.mark.parametrize("template", _templates(), ids=lambda p: str(p.relative_to(ROOT)))
def test_relative_asset_paths_resolve(template: Path):
    text = template.read_text(encoding="utf-8")
    missing = sorted({
        ref for ref in ASSET_SRC.findall(text)
        if not (template.parent / ref).resolve().exists()
    })
    assert not missing, f"{template.relative_to(ROOT)}: broken relative asset path(s): {missing}"
