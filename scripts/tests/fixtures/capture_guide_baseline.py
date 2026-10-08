"""Fångar facit för de 22 guide-PDF:erna.

Körs den om efter en stiländring skriver den över facit med det nya
läget och paritetstestet slutar betyda något. Den vägrar därför skriva
över ett befintligt facit om inte --force anges.

--only RELATIV/SOKVAG riktar omfångningen mot namngivna PDF:er och
lämnar övriga nycklar exakt som de står. Det är det enda sättet att
omfånga en delmängd utan att slå av vakten för resten.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tests import pdf_body_text as bt  # noqa: E402
from tests import pdf_fingerprint as fp  # noqa: E402


def merge_baseline(existing: dict, updates: dict) -> dict:
    """Byter ut de namngivna nycklarna och lämnar resten orörda."""
    unknown = set(updates) - set(existing)
    if unknown:
        raise KeyError(f"okända nycklar: {sorted(unknown)}")
    return {**existing, **updates}


def _only_from_argv(argv: list) -> list:
    out = []
    for i, arg in enumerate(argv):
        if arg == "--only" and i + 1 < len(argv):
            out.append(argv[i + 1])
    return out


def main(argv: list) -> int:
    force = "--force" in argv
    only = _only_from_argv(argv)

    if only:
        unknown = [r for r in only if r not in fp.GUIDE_PDFS]
        if unknown:
            return _fail(f"--only fick okända sökvägar: {unknown}")
        targets = only
    else:
        if fp.BASELINE.exists() and not force:
            return _fail(
                f"{fp.BASELINE} finns redan. Kör med --only för en delmängd, "
                "eller --force bara om du MENAR att slänga hela facit — efter "
                "en ändring är det liktydigt med att slå av paritetsvakten."
            )
        targets = fp.GUIDE_PDFS

    page_updates, body_updates = {}, {}
    for rel in targets:
        path = fp.ROOT / rel
        if not path.exists():
            return _fail(f"saknas: {rel}")
        entry = fp.capture(path)
        page_updates[rel] = entry
        body_updates[rel] = bt.capture(rel)
        print(f"{len(entry['pages']):3} sidor  {len(entry['images']):2} bilder  {rel}")

    _write(fp.BASELINE, page_updates, only)
    _write(bt.BASELINE, body_updates, only)
    print(f"\nfacit skrivet: {len(targets)} PDF:er{' (delmängd)' if only else ''}")
    return 0


def _write(path: Path, updates: dict, selective: bool) -> None:
    if selective and path.exists():
        data = merge_baseline(json.loads(path.read_text(encoding="utf-8")), updates)
    else:
        data = updates
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _fail(msg: str) -> int:
    print(msg, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
