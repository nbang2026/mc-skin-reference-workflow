#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Full-body isometric renderer: front / right / top visible, with MC face-orientation lighting.

Oblique projection (front stays undeformed; depth -> screen up-right):
    sx_u = X + 4 - 0.5*Z
    sy_u = 28 - Y + 0.5*Z
Lighting: top 1.00 / front 0.80 / right 0.60 (native MC coefficients).
Occlusion: per-screen-pixel z-buffer, keep the most-forward (highest Z) sample.

Usage:
    python render3d_body.py <skin.png> <out.png> [scale]
"""
import sys
from PIL import Image

SRC = sys.argv[1]
DST = sys.argv[2]
SC = int(sys.argv[3]) if len(sys.argv) > 3 else 14

K_TOP, K_FRONT, K_RIGHT = 1.00, 0.80, 0.60


def build_parts(slim):
    aw = 3 if slim else 4
    ax = 4 if slim else 4
    return [
        ("head", (-4, 24, 0), (8, 8, 8),
         {"front": (8, 8), "right": (0, 8), "top": (8, 0)},
         {"front": (40, 8), "right": (32, 8), "top": (40, 0)}),
        ("body", (-4, 12, 2), (8, 12, 4),
         {"front": (20, 20), "right": (16, 20), "top": (20, 16)},
         {"front": (20, 36), "right": (16, 36), "top": (20, 32)}),
        ("rarm", (ax, 12, 2), (aw, 12, 4),
         {"front": (44, 20), "right": (40, 20), "top": (44, 16)},
         {"front": (44, 36), "right": (40, 36), "top": (44, 32)}),
        ("larm", (-4 - aw, 12, 2), (aw, 12, 4),
         {"front": (36, 52), "right": (32, 52), "top": (36, 48)},
         {"front": (52, 52), "right": (48, 52), "top": (52, 48)}),
        ("rleg", (0, 0, 2), (4, 12, 4),
         {"front": (4, 20), "right": (0, 20), "top": (4, 16)},
         {"front": (4, 36), "right": (0, 36), "top": (4, 32)}),
        ("lleg", (-4, 0, 2), (4, 12, 4),
         {"front": (20, 52), "right": (16, 52), "top": (20, 48)},
         {"front": (4, 52), "right": (0, 52), "top": (4, 48)}),
    ]


im = Image.open(SRC).convert("RGBA")
px = im.load()

slim = all(px[47, y][3] == 0 for y in range(20, 32))
PARTS = build_parts(slim)

W_U, H_U = 20, 36
OX, OY = 8, 4
W, H = int(W_U * SC), int(H_U * SC)

canvas = Image.new("RGBA", (W, H), (26, 26, 32, 255))
cp = canvas.load()
zbuf = [[-1e9] * W for _ in range(H)]


def texel(face, base_xy, ov_xy, a, b):
    ox, oy = ov_xy
    r, g, b_, al = px[ox + a, oy + b]
    if al >= 128:
        return (r, g, b_)
    bx, by = base_xy
    r, g, b_, al = px[bx + a, by + b]
    if al == 0:
        return None
    return (r, g, b_)


def put(px_, py_, z, col, k):
    if not (0 <= px_ < W and 0 <= py_ < H):
        return
    if z > zbuf[py_][px_]:
        zbuf[py_][px_] = z
        r, g, b = col
        alpha = canvas.getpixel((px_, py_))[3]
        cp[px_, py_] = (int(r * k), int(g * k), int(b * k), alpha)


for name, pos, size, btex, otex in PARTS:
    x0, y0, z0 = pos
    w, h, d = size
    x1, y1, z1 = x0 + w, y0 + h, z0 + d

    # front (Z = z1)
    sxa = (x0 + 4 - 0.5 * z1 + OX) * SC
    sxb = (x1 + 4 - 0.5 * z1 + OX) * SC
    sya = (28 - y1 + 0.5 * z1 + OY) * SC
    syb = (28 - y0 + 0.5 * z1 + OY) * SC
    for py_ in range(int(sya), int(syb)):
        Yu = 28 - ((py_ + 0.5) / SC - OY) + 0.5 * z1
        jv = int(y1 - Yu)
        if not (0 <= jv < h):
            continue
        for px_ in range(int(sxa), int(sxb)):
            Xu = (px_ + 0.5) / SC - OX + 4 - 0.5 * z1
            iu = int(Xu - x0)
            if not (0 <= iu < w):
                continue
            c = texel("front", btex["front"], otex["front"], iu, jv)
            if c:
                put(px_, py_, z1, c, K_FRONT)

    # right (X = x1)
    sxa = (x1 + 4 - 0.5 * z1 + OX) * SC
    sxb = (x1 + 4 - 0.5 * z0 + OX) * SC
    sya = (28 - y1 + 0.5 * z0 + OY) * SC
    syb = (28 - y0 + 0.5 * z1 + OY) * SC
    for py_ in range(int(sya), int(syb)):
        for px_ in range(int(sxa), int(sxb)):
            sxu = (px_ + 0.5) / SC - OX
            syu = (py_ + 0.5) / SC - OY
            Z = 2.0 * (x1 + 4 - sxu)
            if not (z0 <= Z < z1):
                continue
            Y = 28 + 0.5 * Z - syu
            jv = int(y1 - 0.5 - Y)
            i = int(z1 - 0.5 - Z)
            if not (0 <= jv < h and 0 <= i < d):
                continue
            a = (d - 1) - i
            c = texel("right", btex["right"], otex["right"], a, jv)
            if c:
                put(px_, py_, Z, c, K_RIGHT)

    # top (Y = y1)
    sxa = (x0 + 4 - 0.5 * z1 + OX) * SC
    sxb = (x1 + 4 - 0.5 * z0 + OX) * SC
    sya = (28 - y1 + 0.5 * z0 + OY) * SC
    syb = (28 - y1 + 0.5 * z1 + OY) * SC
    for py_ in range(int(sya), int(syb)):
        syu = (py_ + 0.5) / SC - OY
        Z = 2.0 * (syu - 28 + y1)
        if not (z0 <= Z < z1):
            continue
        i = int(z1 - 0.5 - Z)
        for px_ in range(int(sxa), int(sxb)):
            sxu = (px_ + 0.5) / SC - OX
            X = sxu - 4 + 0.5 * Z
            iu = int(X - x0)
            if not (0 <= iu < w):
                continue
            b = (d - 1) - i
            c = texel("top", btex["top"], otex["top"], iu, b)
            if c:
                put(px_, py_, Z, c, K_TOP)

canvas.save(DST)
print(f"RENDER3D {DST} {canvas.size} slim={slim} top{K_TOP}/front{K_FRONT}/right{K_RIGHT}")
