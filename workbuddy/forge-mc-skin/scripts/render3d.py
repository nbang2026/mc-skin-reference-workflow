#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Head isometric renderer: shows front / right / top at once, with MC face-orientation lighting.

Minecraft face-brightness: top 1.00 / front (N,S) 0.80 / right (E,W) 0.60 / bottom 0.50.
Oblique projection: each depth unit -> screen offset (+0.5, -0.5); front face stays 1:1.

Usage:
    python render3d.py <skin.png> <out.png> [scale]
"""
import sys
from PIL import Image

SRC = sys.argv[1]
DST = sys.argv[2]
SC = int(sys.argv[3]) if len(sys.argv) > 3 else 28

K_TOP, K_FRONT, K_RIGHT = 1.00, 0.80, 0.60
DZ_X, DZ_Y = 0.5, -0.5

BASE = {"front": (8, 8), "right": (0, 8), "top": (8, 0)}
OV = {"front": (40, 8), "right": (32, 8), "top": (40, 0)}

im = Image.open(SRC).convert("RGBA")
px = im.load()


def sample(face, a, b):
    """a,b = in-face texel (0..7). Returns overlay-composited color."""
    bx, by = BASE[face]
    ox, oy = OV[face]
    cr, cg, cb, ca = px[ox + a, oy + b]
    if ca >= 128:
        return (cr, cg, cb, ca)
    return px[bx + a, by + b]


def shade(c, k):
    r, g, b, a = c
    return (int(r * k), int(g * k), int(b * k), a)


U = 12
W = H = int(U * SC)
out = Image.new("RGBA", (W, H), (26, 26, 32, 255))
op = out.load()

for py_ in range(H):
    for px_ in range(W):
        X = (px_ + 0.5) / SC
        Y = (py_ + 0.5) / SC
        col = None
        if 0 <= X < 8 and 4 <= Y < 12:                      # front
            col = shade(sample("front", int(X), int(Y - 4)), K_FRONT)
        else:
            i = 2.0 * (X - 8.0)                            # right
            j = Y - 4.0 + (X - 8.0)
            if 0 <= i < 8 and 0 <= j < 8:
                col = shade(sample("right", int(7 - i), int(j)), K_RIGHT)
            else:
                k = 2.0 * (4.0 - Y)                        # top
                u = X - (4.0 - Y)
                if 0 <= k < 8 and 0 <= u < 8:
                    col = shade(sample("top", int(u), int(7 - k)), K_TOP)
        if col:
            op[px_, py_] = col

out.save(DST)
print(f"RENDER3D {DST} {out.size} top{K_TOP}/front{K_FRONT}/right{K_RIGHT}")
