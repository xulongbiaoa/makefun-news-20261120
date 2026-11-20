#!/usr/bin/env python3
"""make.fun entry for news-image-20261120.

Writes one image summing up the world news of Friday 20 November 2026
to /output/entry.png. Standard library only; no network.

The image (entry.png, rendered in this repository by render.py) is copied
byte for byte to the output directory, so two runs write identical bytes.
"""
import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
MAX_BYTES = 1_048_576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def check_png(path: Path) -> tuple[int, int]:
    """Validate the image the gate checks: whole PNG, size and dimensions."""
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError(f"image is {len(data)} bytes, over the 1 MiB limit")
    if data[:8] != PNG_MAGIC:
        raise ValueError("image is not a PNG (bad magic bytes)")
    if data[12:16] != b"IHDR":
        raise ValueError("image has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"image is {width}x{height}, over the 1024 limit")
    return width, height


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    if not SOURCE.is_file():
        print(f"missing image: {SOURCE}", file=sys.stderr)
        return 1
    try:
        width, height = check_png(SOURCE)
    except ValueError as exc:
        print(f"invalid entry image: {exc}", file=sys.stderr)
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    if sha256(target) != sha256(SOURCE):
        print("copy mismatch: output differs from source", file=sys.stderr)
        return 1
    print(f"wrote {target} ({width}x{height}, {target.stat().st_size} bytes, "
          f"sha256 {sha256(target)[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
