#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Isometric 3D preview renderer + 36-face integrity check + visibility check for 64x64 skins.

Usage:
    python render_check.py skin.png [--out preview.png]
Prints:
    - 36-face integrity: transparent-pixel count per face (0 = intact)
    - visibility: garment faces that are washed-out white (invisible under MC lighting)
    - saves a flat 6-part front preview PNG for quick visual review.

See references/uv_layout.md for the FACES coordinate table and the slim-arm tolerance note.
"""
import sys
from PIL import Image, ImageDraw

# 64x64 Steve layout: (face_name, (x0, x1, y0, y1))
FACES = {
    "head": [("top", (8, 16, 0, 8)), ("bottom", (16, 24, 0, 8)),
             ("right", (0, 8, 8, 16)), ("front", (8, 16, 8, 16)),
             ("left", (16, 24, 8, 16)), ("back", (24, 32, 8, 16))],
    "body": [("top", (20, 28, 16, 20)), ("bottom", (28, 36, 16, 20)),
             ("right", (16, 20, 20, 32)), ("front", (20, 28, 20, 32)),
             ("left", (28, 32, 20, 32)), ("back", (32, 40, 20, 32))],
    "right_arm": [("top", (44, 48, 16, 20)), ("bottom", (48, 52, 16, 20)),
                  ("right", (40, 44, 20, 32)), ("front", (44, 48, 20, 32)),
                  ("left", (48, 52, 20, 32)), ("back", (52, 56, 20, 32))],
    "left_arm": [("top", (36, 40, 48, 52)), ("bottom", (40, 44, 48, 52)),
                 ("right", (32, 36, 52, 64)), ("front", (36, 40, 52, 64)),
                 ("left", (40, 44, 52, 64)), ("back", (44, 48, 52, 64))],
    "right_leg": [("top", (4, 8, 16, 20)), ("bottom", (8, 12, 16, 20)),
                  ("right", (0, 4, 20, 32)), ("front", (4, 8, 20, 32)),
                  ("left", (8, 12, 20, 32)), ("back", (12, 16, 20, 32))],
    "left_leg": [("top", (20, 24, 48, 52)), ("bottom", (24, 28, 48, 52)),
                 ("right", (16, 20, 52, 64)), ("front", (20, 24, 52, 64)),
                 ("left", (24, 28, 52, 64)), ("back", (28, 32, 52, 64))],
}


def check_faces(path: str) -> dict:
    """Scan all 36 faces for transparent pixels. Returns per-face hole counts."""
    im = Image.open(path).convert("RGBA")
    px = im.load()
    report = {"holes": [], "total_holes": 0}
    for part, faces in FACES.items():
        for face_name, (x0, x1, y0, y1) in faces:
            holes = sum(1 for x in range(x0, x1) for y in range(y0, y1) if px[x, y][3] == 0)
            if holes:
                report["holes"].append(f"{part}.{face_name}: {holes}px transparent")
                report["total_holes"] += holes
    report["pass"] = report["total_holes"] == 0
    return report


def _saturation(r: int, g: int, b: int) -> int:
    return max(r, g, b) - min(r, g, b)


# Visibility only checks torso + limbs side faces (top/bottom are legit highlight surfaces).
VISIBILITY_FACES = [
    ("body.front", "body.right", "body.left", "body.back"),
    ("right_arm.front", "right_arm.right", "right_arm.left", "right_arm.back"),
    ("left_arm.front", "left_arm.right", "left_arm.left", "left_arm.back"),
    ("right_leg.front", "right_leg.right", "right_leg.left", "right_leg.back"),
    ("left_leg.front", "left_leg.right", "left_leg.left", "left_leg.back"),
]
FACE_SKIN_BOX = (9, 13, 12, 15)


def _skin_baseline(px) -> tuple:
    x0, y0, x1, y1 = FACE_SKIN_BOX
    totals = [0, 0, 0]
    count = 0
    for x in range(x0, x1):
        for y in range(y0, y1):
            r, g, b, a = px[x, y]
            if a < 128:
                continue
            totals[0] += r; totals[1] += g; totals[2] += b
            count += 1
    return tuple(c / count for c in totals) if count else (245, 220, 205)


def _is_skin_like(mean, baseline, tolerance: int = 45) -> bool:
    return all(abs(m - b) < tolerance for m, b in zip(mean, baseline))


def check_visibility(path: str, threshold: int = 30) -> dict:
    """Flag garment faces washed-out white (invisible under MC rendering).

    Top/bottom faces excluded. Faces matching the skin baseline excluded (intentional
    exposed skin). A face is flagged only when >85% of its pixels are both low-saturation
    and very bright.
    """
    im = Image.open(path).convert("RGBA")
    px = im.load()
    baseline = _skin_baseline(px)
    washed = []
    for group in VISIBILITY_FACES:
        for face_key in group:
            part, face_name = face_key.split(".")
            x0, x1, y0, y1 = dict(FACES[part])[face_name]
            total = washed_px = 0
            totals = [0, 0, 0]
            for x in range(x0, x1):
                for y in range(y0, y1):
                    r, g, b, a = px[x, y]
                    if a < 128:
                        continue
                    total += 1
                    totals[0] += r; totals[1] += g; totals[2] += b
                    if _saturation(r, g, b) < threshold and min(r, g, b) > 190:
                        washed_px += 1
            if not total:
                continue
            mean = tuple(c / total for c in totals)
            if _is_skin_like(mean, baseline):
                continue
            if washed_px / total > 0.85:
                washed.append(f"{face_key}: {washed_px / total:.0%} washed-out pixels")
    return {"washed_faces": washed, "pass": not washed, "baseline": [round(c) for c in baseline]}


def render_preview(path: str, out: str, scale: int = 8) -> str:
    """Render a flat 6-part front preview (head/body/arms/legs) to a PNG."""
    im = Image.open(path).convert("RGBA")
    W, H = 16 * scale, 32 * scale
    canvas = Image.new("RGBA", (W, H), (28, 28, 34, 255))
    draw = ImageDraw.Draw(canvas)

    def blit(box, dx, dy):
        x0, y0, x1, y1 = box
        crop = im.crop((x0, y0, x1, y1)).resize(
            ((x1 - x0) * scale, (y1 - y0) * scale), Image.NEAREST
        )
        canvas.alpha_composite(crop, (dx, dy))

    blit((8, 8, 16, 16), 4 * scale, 0)
    blit((20, 20, 28, 32), 4 * scale, 8 * scale)
    blit((44, 20, 48, 32), 0, 8 * scale)
    blit((36, 52, 40, 64), 12 * scale, 8 * scale)
    blit((4, 20, 8, 32), 4 * scale, 20 * scale)
    blit((20, 52, 24, 64), 8 * scale, 20 * scale)
    canvas.save(out)
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: render_check.py skin.png [--out preview.png]")
        sys.exit(1)
    src = sys.argv[1]
    out = "preview.png"
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    fc = check_faces(src)
    vis = check_visibility(src)
    print("36-FACE:", "PASS" if fc["pass"] else "FAIL", "| holes:", fc["holes"])
    print("VISIBIL:", "PASS" if vis["pass"] else "FAIL", "| washed:", vis["washed_faces"])
    p = render_preview(src, out)
    print("PREVIEW :", p)
