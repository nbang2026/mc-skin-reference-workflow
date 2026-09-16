#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Side-by-side compare the head / torso / leg of several skins (overlay composited).

Usage:
    python compare.py ref_dir out.png CODE1 CODE2 ...
Each CODE matches a downloaded file dl_{CODE}_*.png in ref_dir; the three part strips are
laid out for one-screen visual comparison when picking assembly sources.
"""
import glob
import os
import sys
from PIL import Image, ImageDraw

REF = sys.argv[1]
OUT = sys.argv[2]
codes = sys.argv[3:]
SC = 16


def fc(im, bx, by, w, h, obx, oby):
    b = im.crop((bx, by, bx + w, by + h)).copy()
    b.alpha_composite(im.crop((obx, oby, obx + w, oby + h)))
    return b


rows = []
for code in codes:
    hits = sorted(glob.glob(os.path.join(REF, f"dl_{code}_*.png")))
    if not hits:
        print(f"skip {code}: no file")
        continue
    im = Image.open(hits[0]).convert("RGBA")
    head = fc(im, 8, 8, 8, 8, 40, 8)
    body = fc(im, 20, 20, 8, 12, 20, 36)
    leg = fc(im, 4, 20, 4, 12, 4, 36)
    strip = Image.new("RGBA", (8 + 8 + 4 + 2, 12), (0, 0, 0, 0))
    strip.alpha_composite(head.resize((8, 8), Image.NEAREST), (0, 2))
    strip.alpha_composite(body, (9, 0))
    strip.alpha_composite(leg, (18, 0))
    big = strip.resize((strip.width * SC, strip.height * SC), Image.NEAREST)
    t = Image.new("RGBA", (big.width + 70, big.height), (30, 30, 36, 255))
    t.paste(big, (66, 0), big)
    ImageDraw.Draw(t).text((4, big.height // 2 - 6), code, fill=(255, 240, 200, 255))
    rows.append(t)

w = max(r.width for r in rows) + 16
h = sum(r.height for r in rows) + 8 * (len(rows) + 1)
sheet = Image.new("RGBA", (w, h), (18, 18, 22, 255))
y = 8
for r in rows:
    sheet.paste(r, (8, y))
    y += r.height + 8
sheet.save(OUT)
print("CMP", OUT, sheet.size)
