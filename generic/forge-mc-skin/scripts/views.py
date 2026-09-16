#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Three-view preview (front / right / back), overlay composited, for judging appearance.

A single flat front image hides hair volume and proportion problems. Use this to compare
candidate sources and check the result looks right.

Usage:
    python views.py <skin.png> <out.png> [scale]
"""
import sys
from PIL import Image, ImageDraw

SRC = sys.argv[1]
OUT = sys.argv[2]
SC = int(sys.argv[3]) if len(sys.argv) > 3 else 9

im = Image.open(SRC).convert("RGBA")


def is_slim(img):
    p = img.load()
    return all(p[47, y][3] == 0 for y in range(20, 32))


AW = 3 if is_slim(im) else 4  # arm width (slim = Alex model)


def face(bx, by, w, h, obx=None, oby=None):
    b = im.crop((bx, by, bx + w, by + h))
    if obx is not None:
        b = b.copy()
        b.alpha_composite(im.crop((obx, oby, obx + w, oby + h)))
    return b


def build(kind):
    c = Image.new("RGBA", (16, 32), (0, 0, 0, 0))
    if kind == "front":
        parts = [(face(8, 8, 8, 8, 40, 8), (4, 0)),
                 (face(20, 20, 8, 12, 20, 36), (4, 8)),
                 (face(44, 20, AW, 12, 44, 36), (0, 8)),
                 (face(36, 52, AW, 12, 52, 52), (16 - AW, 8)),
                 (face(4, 20, 4, 12, 4, 36), (4, 20)),
                 (face(20, 52, 4, 12, 4, 52), (8, 20))]
    elif kind == "right":
        parts = [(face(0, 8, 8, 8, 32, 8), (0, 0)),
                 (face(16, 20, 4, 12, 16, 36), (2, 8)),
                 (face(40, 20, 4, 12, 40, 36), (0, 8)),
                 (face(0, 20, 4, 12, 0, 36), (2, 20)),
                 (face(16, 52, 4, 12, 0, 52), (2, 20))]
    else:  # back
        parts = [(face(24, 8, 8, 8, 56, 8), (4, 0)),
                 (face(32, 20, 8, 12, 32, 36), (4, 8)),
                 (face(52, 20, AW, 12, 52, 36), (0, 8)),
                 (face(44, 52, AW, 12, 60, 52), (16 - AW, 8)),
                 (face(12, 20, 4, 12, 12, 36), (4, 20)),
                 (face(28, 52, 4, 12, 12, 52), (8, 20))]
    for piece, dst in parts:
        c.alpha_composite(piece, dst)
    return c


views = [("front", build("front")), ("right", build("right")), ("back", build("back"))]
pad = 12
tiles = []
for name, v in views:
    big = v.resize((v.width * SC, v.height * SC), Image.NEAREST)
    tile = Image.new("RGBA", (big.width, big.height + 22), (28, 28, 34, 255))
    tile.paste(big, (0, 22), big)
    ImageDraw.Draw(tile).text((4, 5), name, fill=(255, 235, 180, 255))
    tiles.append(tile)

W = sum(t.width for t in tiles) + pad * (len(tiles) + 1)
H = max(t.height for t in tiles) + pad * 2
sheet = Image.new("RGBA", (W, H), (16, 16, 20, 255))
x = pad
for t in tiles:
    sheet.paste(t, (x, pad))
    x += t.width + pad
sheet.save(OUT)
print("VIEWS", OUT, sheet.size, f"(arm width={AW})")
