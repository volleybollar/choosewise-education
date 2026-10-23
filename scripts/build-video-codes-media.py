#!/usr/bin/env python3
"""Bygger mediafilerna till /visual-codes/video/ ur testmappens råklipp.

För varje kod i visual-codes/video/codes-video-en.json skapas tre filer i
visual-codes/video/media/:
  <slug>.mp4          klippet: H.264, 960 px brett (skarpt på retina), utan ljud, högst 900 kB
  <slug>-poster.webp  första bildrutan — visas innan videon har laddat
  <slug>-start.webp   startbilden som skickades till modellen (584 px)

Källorna ligger utanför repot (de är råmaterial, inte publiceringsfiler):
  <source>/clips/<source_clip>.mp4
  <source>/start/<source_start>

Kör:  /usr/bin/python3 scripts/build-video-codes-media.py
      [--source ~/Projekt/Choosewise/visual-codes-video-test] [--only <slug>]
Filer som redan finns och är nyare än källan hoppas över.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "visual-codes/video/codes-video-en.json"
MEDIA = ROOT / "visual-codes/video/media"
DEFAULT_SOURCE = Path.home() / "Projekt/Choosewise/visual-codes-video-test"

MAX_CLIP = 900_000   # samma gräns som testet i scripts/tests/test_video_codes.py
START_CRF = 28


def up_to_date(target, source):
    return target.exists() and target.stat().st_mtime >= source.stat().st_mtime


def encode_clip(src, dst):
    """Koda om till 960 px H.264 utan ljud. Ryms filen inte i budgeten
    höjs komprimeringen (crf) två steg i taget tills den gör det."""
    crf = START_CRF
    while True:
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-an",
             "-vf", "scale=960:-2", "-c:v", "libx264", "-crf", str(crf),
             "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
             str(dst)],
            check=True)
        if dst.stat().st_size <= MAX_CLIP or crf >= 40:
            return crf
        crf += 2


def make_poster(src, dst):
    """Första bildrutan som webp, så kortet aldrig är en tom svart ruta."""
    tmp = dst.with_suffix(".png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src),
                    "-vf", "scale=960:-2", "-frames:v", "1", str(tmp)], check=True)
    Image.open(tmp).save(dst, "WEBP", quality=80)
    tmp.unlink()


def make_start(src, dst):
    im = Image.open(src).convert("RGB")
    if im.width > 584:
        im = im.resize((584, round(584 * im.height / im.width)), Image.LANCZOS)
    im.save(dst, "WEBP", quality=82)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    ap.add_argument("--only")
    args = ap.parse_args()

    MEDIA.mkdir(parents=True, exist_ok=True)
    data = json.loads(DATA.read_text(encoding="utf-8"))
    total = 0
    for section in data["sections"]:
        for code in section["codes"]:
            slug = code["slug"]
            if args.only and slug != args.only:
                continue
            clip = args.source / "clips" / f"{code['source_clip']}.mp4"
            start = args.source / "start" / code["source_start"]
            for src in (clip, start):
                if not src.exists():
                    sys.exit(f"{slug}: källfilen saknas: {src}")

            mp4 = MEDIA / f"{slug}.mp4"
            if not up_to_date(mp4, clip):
                crf = encode_clip(clip, mp4)
                print(f"{slug}: {mp4.stat().st_size // 1000} kB (crf {crf})")
            poster = MEDIA / f"{slug}-poster.webp"
            if not up_to_date(poster, clip):
                make_poster(clip, poster)
            start_out = MEDIA / f"{slug}-start.webp"
            if not up_to_date(start_out, start):
                make_start(start, start_out)
            total += mp4.stat().st_size
    print(f"totalt video: {total / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
