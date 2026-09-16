#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Directional lighting relight for a skin: per-pixel gradient + face-orientation micro-shade.

Light comes from the upper-left-front of the viewer. Keeps the original strand/fold
structure and remaps colors onto an 8-step ramp. Only acts on "pink-family" pixels
(R>G, B>G, R>B) so skin / eye-white / gray pants / white zipper / dark outlines are spared.

Usage:
    python relight.py <in.png> <out.png> [head|all]
"""
import sys
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else "bocchi_assembled.png"
DST = sys.argv[2] if len(sys.argv) > 2 else "bocchi_lit.png"
SCOPE = sys.argv[3] if len(sys.argv) > 3 else "head"

# 8-step pink ramp (bright -> dark); bright tint = pink-white, dark tint = purple-pink.
# Saturation rises as brightness falls so the result stays visible in-game.
RAMP = [
    (255, 222, 234),
    (252, 206, 223),
    (248, 189, 212),
    (241, 170, 197),
    (226, 148, 179),
    (207, 126, 158),
    (183, 105, 138),
    (157, 85, 118),
]

# part: (overlay offset x,y), then 6 faces (name, base_x, base_y, w, h)
PARTS = {
    "head": ((32, 0), [
        ("top", 8, 0, 8, 8), ("bottom", 16, 0, 8, 8),
        ("right", 0, 8, 8, 8), ("front", 8, 8, 8, 8),
        ("left", 16, 8, 8, 8), ("back", 24, 8, 8, 8)]),
    "body": ((0, 16), [
        ("top", 20, 16, 8, 4), ("bottom", 28, 16, 8, 4),
        ("right", 16, 20, 4, 12), ("front", 20, 20, 8, 12),
        ("left", 28, 20, 4, 12), ("back", 32, 20, 8, 12)]),
    "rarm": ((0, 16), [
        ("top", 44, 16, 4, 4), ("bottom", 48, 16, 4, 4),
        ("right", 40, 20, 4, 12), ("front", 44, 20, 4, 12),
        ("left", 48, 20, 4, 12), ("back", 52, 20, 4, 12)]),
    "larm": ((16, 0), [
        ("top", 36, 48, 4, 4), ("bottom", 40, 48, 4, 4),
        ("right", 32, 52, 4, 12), ("front", 36, 52, 4, 12),
        ("left", 40, 52, 4, 12), ("back", 44, 52, 4, 12)]),
    "rleg": ((0, 16), [
        ("top", 4, 16, 4, 4), ("bottom", 8, 16, 4, 4),
        ("right", 0, 20, 4, 12), ("front", 4, 20, 4, 12),
        ("left", 8, 20, 4, 12), ("back", 12, 20, 4, 12)]),
    "lleg": ((-16, 0), [
        ("top", 20, 48, 4, 4), ("bottom", 24, 48, 4, 4),
        ("right", 16, 52, 4, 12), ("front", 20, 52, 4, 12),
        ("left", 24, 52, 4, 12), ("back", 28, 52, 4, 12)]),
}

# Face-orientation factor: light from upper-left -> right face (screen-right) darker, top brightest.
FACE_K = {"top": 1.05, "front": 1.00, "left": 1.02, "right": 0.94, "back": 0.92, "bottom": 0.88}
OV_BOOST = 1.03  # overlay is the protruding outer layer, slightly more lit


def is_hair(c):
    """Pink-family test: R>G, B>G, R>B AND enough saturation.

    The saturation floor is mandatory: a white zipper (234,232,233) satisfies R>G/B>G
    but its saturation is ~0.4%, so without the floor it would be wrongly relit as hair.
    """
    r, g, b, a = c
    if a == 0 or not (r > g and b > g and r > b):
        return False
    return (max(r, g, b) - min(r, g, b)) >= 10


def active(scope):
    names = ["head"] if scope == "head" else list(PARTS)
    out = []
    for n in names:
        (odx, ody), faces = PARTS[n]
        for fname, bx, by, w, h in faces:
            out.append((fname, bx, by, w, h, 0, 0))
            out.append((fname, bx, by, w, h, odx, ody))
    return out


def main():
    im = Image.open(SRC).convert("RGBA")
    px = im.load()
    jobs = active(SCOPE)

    lums = []
    for fname, bx, by, w, h, dx, dy in jobs:
        for y in range(h):
            for x in range(w):
                c = px[bx + dx + x, by + dy + y]
                if is_hair(c):
                    lums.append((c[0] + c[1] + c[2]) / 3.0)
    lums.sort()
    if not lums:
        print("no hair pixels")
        return
    lo = lums[int(len(lums) * 0.05)]
    hi = lums[int(len(lums) * 0.95)]
    if hi - lo < 40:
        hi = lo + 40

    touched = 0
    for fname, bx, by, w, h, dx, dy in jobs:
        k = FACE_K[fname] * (OV_BOOST if dx or dy else 1.0)
        for y in range(h):
            for x in range(w):
                c = px[bx + dx + x, by + dy + y]
                if not is_hair(c):
                    continue
                r, g, b, a = c
                lum = (r + g + b) / 3.0
                t = max(0.0, min(1.0, (lum - lo) / (hi - lo)))
                t = 0.15 + 0.85 * t
                u = (w - 1 - x) / max(1, w - 1)      # left bright, right dark
                v = (h - 1 - y) / max(1, h - 1)      # top bright, bottom dark
                dirv = 0.18 + 0.72 * (0.62 * u + 0.38 * v)
                gv = (0.45 * t + 0.55 * dirv) * k
                gv = max(0.0, min(1.0, (gv - 0.16) / 0.70))
                idx = int(round((1.0 - gv) * 7))
                nr, ng, nb = RAMP[idx]
                px[bx + dx + x, by + dy + y] = (nr, ng, nb, a)
                touched += 1

    im.save(DST)
    print(f"LIT[{SCOPE}] {DST}  relit {touched} px  t-range[{lo:.0f},{hi:.0f}]")


if __name__ == "__main__":
    main()
