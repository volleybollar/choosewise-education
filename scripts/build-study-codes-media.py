#!/usr/bin/env python3
"""Bygger bilderna till /visual-codes/study/ ur testmappens PNG:er.

För varje kod i visual-codes/study/codes-study-en.json, och för de tre
handskrivna bilderna överst på sidan (EXTRAS), skapas två filer i
visual-codes/study/images/:
  <slug>.webp        1024 px bred – full storlek, öppnas när man klickar
  <slug>-512w.webp   512 px bred – visas på kortet

Källorna ligger utanför repot (de är råmaterial, inte publiceringsfiler):
  <source>/<fil i fältet 'source'>

Kör:  /usr/bin/python3 scripts/build-study-codes-media.py
      [--source ~/Projekt/Choosewise/visual-codes-study-test]
Filer som är nyare än källan hoppas över.
"""
import argparse
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "visual-codes/study/codes-study-en.json"
IMAGES = ROOT / "visual-codes/study/images"
DEFAULT_SOURCE = Path.home() / "Projekt/Choosewise/visual-codes-study-test"

# Bilderna i sidans överdel, som inte hör till något kort
EXTRAS = {
    "hero-cheatsheet": "fotosyntes/cheatsheet.png",
    "hero-quizmate": "fotosyntes/quizmate-tillagg-final.png",
    "feynman-codeonly": "fotosyntes/feynman.png",
}
SIZES = {"": 1024, "-512w": 512}


def build(slug, src):
    for suffix, width in SIZES.items():
        dst = IMAGES / f"{slug}{suffix}.webp"
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            continue
        im = Image.open(src).convert("RGB")
        if im.width > width:
            im = im.resize((width, round(width * im.height / im.width)), Image.LANCZOS)
        im.save(dst, "WEBP", quality=80)
        print(f"{dst.name}  {dst.stat().st_size // 1024} kB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = ap.parse_args()

    IMAGES.mkdir(parents=True, exist_ok=True)
    jobs = dict(EXTRAS)
    for section in json.loads(DATA.read_text(encoding="utf-8"))["sections"]:
        for c in section["codes"]:
            jobs[c["slug"]] = c["source"]
    for slug, rel in jobs.items():
        build(slug, args.source / rel)


if __name__ == "__main__":
    main()
