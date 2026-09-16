#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Per-part health scan across a skin directory. Run BEFORE cross-image assembly.

For each part it reports:
  - transparent-hole count across the 6 base faces (0 = intact; arms with holes are unusable)
  - near-white pixel count (saturation < 18 and brightness > 235) -> risk of invisible in-game
  - mean saturation of the part

Usage:
    python part_scan.py ref_dir
"""
import colorsys
import glob
import os
import sys
from PIL import Image

# 6 base-face boxes per part, (x0, y0, x1, y1) EXCLUSIVE (same convention as FACES in
# render_check.py / references/uv_layout.md). See references/uv_layout.md.
PARTS = {
    "head":  [(8, 0, 16, 8), (16, 0, 24, 8), (0, 8, 8, 16), (8, 8, 16, 16),
              (16, 8, 24, 16), (24, 8, 32, 16)],
    "torso": [(20, 16, 28, 20), (28, 16, 36, 20), (16, 20, 20, 32), (20, 20, 28, 32),
              (28, 20, 32, 32), (32, 20, 40, 32)],
    "rarm":  [(44, 16, 48, 20), (48, 16, 52, 20), (40, 20, 44, 32), (44, 20, 48, 32),
              (48, 20, 52, 32), (52, 20, 56, 32)],
    "larm":  [(36, 48, 40, 52), (40, 48, 44, 52), (32, 52, 36, 64), (36, 52, 40, 64),
              (40, 52, 44, 64), (44, 52, 48, 64)],
    "rleg":  [(4, 16, 8, 20), (8, 16, 12, 20), (0, 20, 4, 32), (4, 20, 8, 32),
              (8, 20, 12, 32), (12, 20, 16, 32)],
    "lleg":  [(20, 48, 24, 52), (24, 48, 28, 52), (16, 52, 20, 64), (20, 52, 24, 64),
              (24, 52, 28, 64), (28, 52, 32, 64)],
}


def part_stats(im, boxes):
    p = im.load()
    trans = 0
    sats = []
    bright = []
    for (x0, y0, x1, y1) in boxes:
        for y in range(y0, y1):
            for x in range(x0, x1):
                r, g, b, a = p[x, y]
                if a == 0:
                    trans += 1
                    continue
                h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
                sats.append(s * 255)
                bright.append(v * 255)
    ms = sum(sats) / len(sats) if sats else 0
    nearwhite = sum(1 for s, v in zip(sats, bright) if s < 18 and v > 235)
    return trans, ms, nearwhite


if __name__ == "__main__":
    REF = sys.argv[1] if len(sys.argv) > 1 else "."
    files = sorted(glob.glob(os.path.join(REF, "*.png")))
    print("=== transparent holes per part (base 6 faces; 0 = intact) ===")
    print(f"{'file':36s}" + "".join(f"{p:>7s}" for p in PARTS))
    for path in files:
        im = Image.open(path).convert("RGBA")
        cells = []
        for part, boxes in PARTS.items():
            t, _, _ = part_stats(im, boxes)
            cells.append(f"{t:>7d}")
        print(f"{os.path.basename(path):36s}" + "".join(cells))
    print()
    print("=== near-white px / mean saturation per part (near-white = invisible-in-game risk) ===")
    for path in files:
        im = Image.open(path).convert("RGBA")
        out = []
        for part, boxes in PARTS.items():
            t, ms, nw = part_stats(im, boxes)
            out.append(f"{part}:{nw:>3d}/{ms:>4.0f}")
        print(f"{os.path.basename(path):36s} " + "  ".join(out))
