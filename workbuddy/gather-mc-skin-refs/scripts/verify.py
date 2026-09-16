#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate downloaded skins: PIL-parseable, size in {64x64, 64x32}, feature-hit count.

Usage:
    python verify.py ref_dir
Prints one verdict per file:
    confirmed     64x64 and feature hits > 200  (primary pool)
    legacy_64x32  64x32 and feature hits > 200  (secondary pool)
    weak          64x32/64x64 with 50 < hits <= 200
    rejected      hits <= 50  (not the target character)
    preview        size not in whitelist (e.g. 288x256) -> discard
    corrupt        cannot be opened by PIL -> discard
"""
import glob
import os
import sys
from PIL import Image

VALID_SIZES = {(64, 64), (64, 32)}


def is_target_hair(r: int, g: int, b: int, a: int) -> bool:
    """Default pink-hair discriminator. ADJUST per character (see references/uv_layout.md).

    Warm red dominant, blue >= green, excludes skin/white. Replace for non-pink characters.
    """
    return a > 0 and r > 150 and b > 120 and b >= g and (r - b) > 20 and (r - g) > 15


def is_skin_tone(r: int, g: int, b: int, a: int) -> bool:
    return a > 0 and r > 235 and g > 215 and b > 200


def audit(ref_dir: str, is_target=is_target_hair) -> list:
    results = []
    for path in sorted(glob.glob(os.path.join(ref_dir, "*.png"))):
        name = os.path.basename(path)
        try:
            im = Image.open(path).convert("RGBA")
        except Exception as exc:  # noqa: BLE001
            results.append({"file": name, "verdict": "corrupt", "detail": str(exc)})
            continue
        w, h = im.size
        if (w, h) not in VALID_SIZES:
            results.append({"file": name, "verdict": "preview", "detail": f"{w}x{h}"})
            continue
        px = im.load()
        hits = sum(1 for y in range(h) for x in range(w) if is_target(*px[x, y]))
        if hits > 200 and (w, h) == (64, 64):
            verdict = "confirmed"
        elif hits > 200:
            verdict = "legacy_64x32"
        elif hits > 50:
            verdict = "weak"
        else:
            verdict = "rejected"
        results.append({"file": name, "verdict": verdict, "hits": hits, "size": f"{w}x{h}"})
    return results


if __name__ == "__main__":
    ref_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    for r in audit(ref_dir):
        print(f"{r['verdict']:14s} {r['file']}  hits={r.get('hits', '-')}  {r.get('size', '')}")
