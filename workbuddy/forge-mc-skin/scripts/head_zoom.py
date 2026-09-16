#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Head close-up: front / right / back / top (overlay composited). Use to inspect face details.

Usage:
    python head_zoom.py <skin.png> <out.png> [scale]
"""
import sys
from PIL import Image, ImageDraw

im = Image.open(sys.argv[1]).convert("RGBA")
OUT = sys.argv[2]
SC = int(sys.argv[3]) if len(sys.argv) > 3 else 22


def fc(bx, by, w, h, obx, oby):
    b = im.crop((bx, by, bx + w, by + h)).copy()
    b.alpha_composite(im.crop((obx, oby, obx + w, oby + h)))
    return b


faces = [("front", fc(8, 8, 8, 8, 40, 8)), ("right", fc(0, 8, 8, 8, 32, 8)),
         ("back", fc(24, 8, 8, 8, 56, 8)), ("top", fc(8, 0, 8, 8, 40, 0))]
tiles = []
for n, f in faces:
    big = f.resize((f.width * SC, f.height * SC), Image.NEAREST)
    t = Image.new("RGBA", (big.width, big.height + 22), (28, 28, 34, 255))
    t.paste(big, (0, 22), big)
    ImageDraw.Draw(t).text((4, 5), n, fill=(255, 235, 180, 255))
    tiles.append(t)
pad = 10
sheet = Image.new("RGBA", (sum(t.width for t in tiles) + pad * 5, max(t.height for t in tiles) + pad * 2), (16, 16, 20, 255))
x = pad
for t in tiles:
    sheet.paste(t, (x, pad))
    x += t.width + pad
sheet.save(OUT)
print("HEAD", OUT, sheet.size)
