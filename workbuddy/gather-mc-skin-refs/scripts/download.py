#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch download Minecraft skins from direct links (minecraftskins.com /uploads/skins/).

Reads a jobs file (JSON list of [label, url]) and downloads 5-20 real 64x64 skins.

Usage:
    python download.py jobs.json ref_dir
    python download.py            # runs a tiny demo job (replace with real links)

Hard rules (see references/failure_modes.md F1-F4):
  - Always send a browser User-Agent, else the host returns 403.
  - Carry Referer: https://www.minecraftskins.com/  (lowers 403 rate; Cloudflare throttles).
  - Use /uploads/skins/, NEVER /uploads/preview-skins/  (that path is a 288x256 render,
    not a 64x64 skin texture, and will be rejected by the size whitelist).
  - Idempotent: skip existing valid files. Retry with exponential backoff (<=5 tries).
"""
import glob as _glob
import json
import os
import sys
import time
import urllib.request

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
)
TIMEOUT = 25
MAX_RETRIES = 5
BACKOFF = 3


def download(url: str, dest: str) -> bool:
    """Download url -> dest with retry/backoff. Returns True on success."""
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        print(f"SKIP  {os.path.basename(dest)} (exists)")
        return True
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Referer": "https://www.minecraftskins.com/",
                },
            )
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                data = resp.read()
            with open(dest, "wb") as fh:
                fh.write(data)
            print(f"OK    {os.path.basename(dest)}: {len(data)} bytes")
            return True
        except Exception as exc:  # noqa: BLE001
            print(f"RETRY {os.path.basename(dest)} [{attempt}/{MAX_RETRIES}]: {exc}")
            time.sleep(BACKOFF * attempt)
    print(f"FAIL  {os.path.basename(dest)}")
    return False


def run(jobs: list, ref_dir: str) -> dict:
    """jobs: list of (label, url). Returns summary counts."""
    os.makedirs(ref_dir, exist_ok=True)
    ok = 0
    for label, url in jobs:
        if download(url, os.path.join(ref_dir, f"dl_{label}.png")):
            ok += 1
    return {"total": len(jobs), "ok": ok, "fail": len(jobs) - ok}


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        jobs_path, ref_dir = sys.argv[1], sys.argv[2]
        with open(jobs_path, "r", encoding="utf-8") as fh:
            jobs = json.load(fh)
    else:
        # Demo only — replace with real /uploads/skins/ links extracted from search pages.
        jobs = [
            ("demo01", "https://www.minecraftskins.com/uploads/skins/2023/08/01/sample-12345.png"),
        ]
        ref_dir = "ref_demo"
        print("[demo] supply jobs.json + ref_dir for real use")
    print(run(jobs, ref_dir))
