"""Vakter för sidan Visual codes for video (/visual-codes/video/).

Datafilen är sidans enda källa: varje kort, varje kopieringsknapp och varje
mediafil byggs från den. Testerna här säkrar att den är hel och — viktigast —
att prompten på varje kort är exakt den som gav klippet. Annars ljuger sidan.
"""
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "visual-codes/video/codes-video-en.json"
# Genereringsloggen ligger utanför repot (testmappen). Saknas den hoppas
# jämförelsen över — på en annan maskin finns den inte.
JOBS = Path.home() / "Projekt/Choosewise/visual-codes-video-test/jobs.tsv"

ORDER = ["see-the-invisible", "processes", "film-language",
         "doesnt-work-yet", "beyond-the-classroom"]
STATUSES = {"works", "partial", "fails"}


def load():
    return json.loads(DATA.read_text(encoding="utf-8"))


def all_codes():
    return [(s, c) for s in load()["sections"] for c in s["codes"]]


def test_sections_in_the_agreed_order():
    assert [s["id"] for s in load()["sections"]] == ORDER


def test_every_code_has_required_fields_and_valid_status():
    slugs = []
    for _, c in all_codes():
        assert c["code"].startswith("/"), c["code"]
        assert re.fullmatch(r"[a-z0-9-]+", c["slug"]), c["slug"]
        assert c["status"] in STATUSES, (c["code"], c["status"])
        assert c["prompt"].startswith(c["code"]), c["code"]
        assert c["description"].strip(), c["code"]
        assert c["source_clip"] and c["source_start"], c["code"]
        slugs.append(c["slug"])
    assert len(slugs) == len(set(slugs)), "slug måste vara unik"


def test_fails_only_in_the_doesnt_work_box():
    for s, c in all_codes():
        if s["id"] == "doesnt-work-yet":
            assert c["status"] == "fails", c["code"]
        else:
            assert c["status"] != "fails", c["code"]


def test_lightshift_and_seasons_exist_and_work():
    by_code = {c["code"]: c for _, c in all_codes()}
    for code in ("/lightshift", "/seasons"):
        assert by_code[code]["status"] == "works"


def normalised_prompts():
    """Prompterna ur jobs.tsv i samma form som på sidan.
    Higgsfield-raderna skrev tillägg som '/orbit + "The camera …"',
    kie-raderna som '/reverse Play …'. Båda blir '/kod tillägg'."""
    prompts = set()
    for line in JOBS.read_text(encoding="utf-8").splitlines():
        cols = line.split("\t")
        if len(cols) < 2:
            continue
        p = re.sub(r' \+ "(.*)"$', r" \1", cols[1].strip())
        prompts.add(p)
    return prompts


def test_prompts_match_what_was_sent():
    if not JOBS.exists():
        pytest.skip("jobs.tsv finns bara på Johans maskin")
    sent = normalised_prompts()
    wrong = [c["code"] for _, c in all_codes() if c["prompt"] not in sent]
    assert wrong == [], f"prompter som aldrig skickades: {wrong}"


# ── Media (byggs av scripts/build-video-codes-media.py) ──────────────────────
import json as _json
import subprocess

MEDIA = ROOT / "visual-codes/video/media"
MAX_CLIP = 900_000          # byte per klipp
MAX_TOTAL = 40_000_000      # byte all video på sidan


def media_files(slug):
    return [MEDIA / f"{slug}.mp4", MEDIA / f"{slug}-poster.webp", MEDIA / f"{slug}-start.webp"]


def test_every_code_has_its_three_media_files():
    missing = [str(p.relative_to(ROOT)) for _, c in all_codes()
               for p in media_files(c["slug"]) if not p.exists()]
    assert missing == []


def test_each_clip_is_within_budget():
    big = {c["slug"]: (MEDIA / f"{c['slug']}.mp4").stat().st_size
           for _, c in all_codes()
           if (MEDIA / f"{c['slug']}.mp4").stat().st_size > MAX_CLIP}
    assert big == {}


def test_total_video_within_budget():
    total = sum((MEDIA / f"{c['slug']}.mp4").stat().st_size for _, c in all_codes())
    assert total <= MAX_TOTAL, total


def test_clips_have_no_audio_track_and_are_h264():
    for _, c in all_codes():
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name",
             "-of", "json", str(MEDIA / f"{c['slug']}.mp4")],
            capture_output=True, text=True, check=True).stdout
        streams = _json.loads(out)["streams"]
        assert [s["codec_type"] for s in streams] == ["video"], c["slug"]
        assert streams[0]["codec_name"] == "h264", c["slug"]
