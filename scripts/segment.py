#!/usr/bin/env python3
"""Split an illustration into its separate objects, by connectivity.

A vertical cut does not work: in the approved hero the man's arm and the desk's
left edge overlap in x, so any column that misses one clips the other. What
actually separates them is that they are not touching, which is a question about
connectivity rather than about position.

Implemented here rather than pulled in, because scipy would be a large
dependency for one function and this runs in under a second on 1024x1024.

    python3 scripts/segment.py IMAGE.png            # list the objects
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image


def background(a: np.ndarray) -> np.ndarray:
    edges = np.concatenate([a[0:6].reshape(-1, 3), a[-6:].reshape(-1, 3)])
    return np.median(edges, axis=0)


def ink_mask(im: Image.Image, threshold: int = 60) -> np.ndarray:
    a = np.asarray(im.convert("RGB")).astype(int)
    return np.abs(a - background(a)).sum(axis=2) > threshold


def components(mask: np.ndarray, min_pixels: int = 400) -> list[dict]:
    """Label 8-connected regions. Iterative, so a tall figure cannot blow the stack."""
    h, w = mask.shape
    labels = np.zeros((h, w), dtype=np.int32)
    out: list[dict] = []
    current = 0
    neigh = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for sy in range(h):
        row = mask[sy]
        for sx in np.where(row)[0]:
            if labels[sy, sx]:
                continue
            current += 1
            stack = [(sy, int(sx))]
            labels[sy, sx] = current
            pixels = []
            while stack:
                y, x = stack.pop()
                pixels.append((y, x))
                for dy, dx in neigh:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not labels[ny, nx]:
                        labels[ny, nx] = current
                        stack.append((ny, nx))
            if len(pixels) < min_pixels:
                continue
            ys = [p[0] for p in pixels]
            xs = [p[1] for p in pixels]
            out.append({
                "label": current,
                "pixels": len(pixels),
                "box": (min(xs), min(ys), max(xs) + 1, max(ys) + 1),
                "cx": sum(xs) / len(xs),
            })
    out.sort(key=lambda c: -c["pixels"])
    return out, labels


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    im = Image.open(Path(sys.argv[1]))
    comps, _ = components(ink_mask(im))
    print(f"{len(comps)} objects of 400 pixels or more:")
    for c in comps:
        x0, y0, x1, y1 = c["box"]
        print(f"  label {c['label']:3d}  {c['pixels']:7d}px  "
              f"box {x0:4d},{y0:4d} .. {x1:4d},{y1:4d}  "
              f"({x1-x0}x{y1-y0})  centre x {c['cx']:.0f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
