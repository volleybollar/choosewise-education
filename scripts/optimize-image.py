#!/usr/bin/env python3
"""Convert PNG/JPEG images to web-optimized WebP for choosewise.education.

Common use cases:

    # Optimize a single blog cover or guide screenshot
    python3 scripts/optimize-image.py sv/blog/posts/assets/fortbildning.png

    # Walk a folder and convert every PNG/JPG that doesn't already have a fresh .webp
    python3 scripts/optimize-image.py sv/blog/posts/assets/

    # Custom width (e.g. for thumbnails)
    python3 scripts/optimize-image.py path/to/image.png --width 800

    # Generate multiple sizes for srcset
    python3 scripts/optimize-image.py image.png --sizes 800,1600

    # Replace the original after a successful conversion
    python3 scripts/optimize-image.py image.png --remove-original

Defaults:
    width    = 1600 (max; never enlarges)
    quality  = 82
    output   = same folder, same basename, .webp extension

Idempotent: skips files where a .webp already exists and is newer than the source,
unless --force is passed.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required. Install with: pip install Pillow")


SUPPORTED_INPUT = {".png", ".jpg", ".jpeg"}


def optimize(src: Path, *, widths: list[int], quality: int, force: bool,
             remove_original: bool) -> int:
    """Convert one image. Returns total bytes written across all generated WebPs."""
    img = Image.open(src)
    # Drop alpha for JPEGs that have it; preserve for PNGs (WebP handles both)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA" if "A" in img.mode else "RGB")

    src_w = img.width
    src_size = src.stat().st_size
    total_out = 0
    outputs: list[Path] = []

    for width in widths:
        # Single-size mode → no width suffix; multi-size mode → -<W>w suffix
        if len(widths) == 1:
            out = src.with_suffix(".webp")
        else:
            out = src.with_name(f"{src.stem}-{width}w.webp")

        if out.exists() and not force and out.stat().st_mtime >= src.stat().st_mtime:
            print(f"  skip {out.name} (already up to date — use --force to redo)")
            outputs.append(out)
            continue

        # Never enlarge: if source is narrower than target width, keep source width
        target_w = min(width, src_w)
        target_h = round(img.height * target_w / src_w)
        resized = img.resize((target_w, target_h), Image.LANCZOS) if target_w != src_w else img

        # method=6 is the slowest/best WebP encoder pass; worth it for one-off uploads
        resized.save(out, "WEBP", quality=quality, method=6)
        total_out += out.stat().st_size
        outputs.append(out)
        print(f"  ✓ {out.name} → {target_w}×{target_h}, {out.stat().st_size / 1024:.1f} KB")

    saved = src_size - total_out
    pct = 100 * saved / src_size if src_size else 0
    label = "saved" if saved >= 0 else "grew"
    print(f"  source: {src_size / 1024:.1f} KB → {total_out / 1024:.1f} KB total ({label} {abs(pct):.1f}%)")

    if remove_original and total_out > 0:
        src.unlink()
        print(f"  removed original: {src.name}")

    return total_out


def collect_targets(path: Path) -> list[Path]:
    """Walk a path and return all PNG/JPG files (skipping anything inside .git)."""
    if path.is_file():
        return [path] if path.suffix.lower() in SUPPORTED_INPUT else []
    return sorted(
        p for p in path.rglob("*")
        if p.is_file()
        and p.suffix.lower() in SUPPORTED_INPUT
        and ".git" not in p.parts
    )


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Convert PNG/JPG to web-optimized WebP.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("\n\n", 2)[1],  # show usage block in --help
    )
    ap.add_argument("path", type=Path, help="File or directory to process")
    ap.add_argument("--width", type=int, default=1600,
                    help="Max width in pixels (default: 1600). Aspect preserved; never enlarges.")
    ap.add_argument("--sizes", type=str,
                    help="Comma-separated widths for srcset, e.g. 800,1600. Overrides --width.")
    ap.add_argument("--quality", type=int, default=82,
                    help="WebP quality 0-100 (default: 82). Photos: 78-85, illustrations: 85-92.")
    ap.add_argument("--force", action="store_true",
                    help="Re-convert even if .webp already exists and is newer.")
    ap.add_argument("--remove-original", action="store_true",
                    help="Delete the source PNG/JPG after successful conversion.")
    args = ap.parse_args()

    if not args.path.exists():
        sys.exit(f"Error: {args.path} does not exist")

    widths = ([int(w) for w in args.sizes.split(",")]
              if args.sizes else [args.width])

    targets = collect_targets(args.path)
    if not targets:
        sys.exit(f"No PNG/JPG files found under {args.path}")

    print(f"Optimizing {len(targets)} file(s) → WebP @ q{args.quality}, widths={widths}")
    print()

    grand_total = 0
    for src in targets:
        rel = src.relative_to(args.path.parent if args.path.is_file() else args.path)
        print(f"{rel}")
        grand_total += optimize(src, widths=widths, quality=args.quality,
                                force=args.force, remove_original=args.remove_original)
        print()

    print(f"Done. Total output: {grand_total / 1024:.1f} KB across {len(targets)} source file(s).")


if __name__ == "__main__":
    main()
