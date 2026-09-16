#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Originality dedup: do NOT mistake downloaded art for original work.

Two reliable offline signals are combined (see references/dedup_calibration.md for why
the older aHash / cosine / IoU signals were dropped):
  D1  alpha-aware dHash (16x16 = 256 bit) + exact byte hash
  D2  pixel-wise divergence (RGB tol 24, alpha strict) -> fraction of differing pixels

Usage:
    python dedup.py target.png ref_dir
        -> prints verdict for one target vs the baseline index in ref_dir
    python dedup.py --all ref_dir
        -> prints a verdict for every file in ref_dir vs the rest

Verdicts:
    duplicate_exact   byte hash identical
    duplicate_near    dHash hamming <= 25 (~10%)  (forbidden to claim as original)
    derived           pixel divergence <= 15%     (recolored / tweaked derivative)
    clear             none of the above            (safe as original candidate)
"""
import glob
import hashlib
import os
import sys
from PIL import Image


def _gray(path: str, size: tuple) -> Image.Image:
    """Alpha-aware grayscale: flatten onto mid-gray so transparent area is neutral."""
    im = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", im.size, (128, 128, 128, 255))
    bg.alpha_composite(im)
    return bg.convert("L").resize(size, Image.LANCZOS)


def byte_hash(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def dhash(path: str, size: int = 16) -> int:
    """Gradient hash (16x16 = 256 bit), alpha-aware. 8x8 is too coarse for 64x64 skins."""
    px = list(_gray(path, (size + 1, size)).tobytes())
    bits = 0
    for row in range(size):
        for col in range(size):
            if px[row * (size + 1) + col] > px[row * (size + 1) + col + 1]:
                bits |= 1 << (row * size + col)
    return bits


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def pixel_divergence(path_a: str, path_b: str, tol: int = 24) -> float:
    """Fraction of differing pixels. alpha must match; RGB diff <= tol counts as same.

    Calibrated: independent works 0.23-0.46 / same-source tweaks 0.10-0.15 / ~identical < 0.10.
    """
    a = Image.open(path_a).convert("RGBA")
    b = Image.open(path_b).convert("RGBA")
    if a.size != b.size:
        b = b.resize(a.size, Image.NEAREST)
    w, h = a.size
    pa, pb = a.load(), b.load()
    diff = 0
    for y in range(h):
        for x in range(w):
            ra, ga, ba, aa = pa[x, y]
            rb, gb, bb, ab = pb[x, y]
            if (aa > 128) != (ab > 128):
                diff += 1
                continue
            if aa <= 128:
                continue
            if max(abs(ra - rb), abs(ga - gb), abs(ba - bb)) > tol:
                diff += 1
    return diff / (w * h)


def build_index(ref_dir: str) -> list:
    index = []
    for path in sorted(glob.glob(os.path.join(ref_dir, "*.png"))):
        try:
            im = Image.open(path)
            if im.size not in {(64, 64), (64, 32)}:
                continue
            index.append({
                "file": os.path.basename(path),
                "size": im.size,
                "byte": byte_hash(path),
                "dhash": dhash(path, 16),
            })
        except Exception:  # noqa: BLE001
            continue
    return index


def check(target: str, index: list, ref_dir: str = ".",
          near_threshold: int = 25, derived_threshold: float = 0.15) -> dict:
    """Compare target against the baseline index (same-size peers only)."""
    tb = byte_hash(target)
    td = dhash(target, 16)
    tsize = Image.open(target).size
    base = os.path.dirname(target) or ref_dir
    matches = []
    for entry in index:
        if entry["file"] == os.path.basename(target) or entry["size"] != tsize:
            continue
        peer = os.path.join(base, entry["file"])
        if entry["byte"] == tb:
            matches.append({"against": entry["file"], "verdict": "duplicate_exact"})
        elif hamming(entry["dhash"], td) <= near_threshold:
            matches.append({"against": entry["file"], "verdict": "duplicate_near"})
        elif pixel_divergence(target, peer) <= derived_threshold:
            matches.append({"against": entry["file"], "verdict": "derived"})
    return {
        "file": os.path.basename(target),
        "verdict": "clear" if not matches else matches[0]["verdict"],
        "matches": matches,
    }


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--all":
        ref = args[1] if len(args) > 1 else "."
        idx = build_index(ref)
        for entry in idx:
            c = check(os.path.join(ref, entry["file"]), idx, ref)
            print(f"{entry['file']:34s} {c['verdict']:14s} {c['matches']}")
    elif len(args) >= 2:
        print(check(args[0], build_index(args[1]), args[1]))
    else:
        print("usage: dedup.py target.png ref_dir  |  dedup.py --all ref_dir")
