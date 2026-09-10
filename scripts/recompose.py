#!/usr/bin/env python3
"""Rebuild a scene from the pieces of an approved image, without generating.

Written the moment Otávio pointed out the obvious: re-rolling a whole image to
change the size of one object throws away the character that was just approved,
when the pieces are already separable. Every generation is a new sample; a
composite is arithmetic.

It works here because the visual system makes it work. Flat colour with no
light direction means a piece can be moved or resized without any shadow
becoming wrong, and a plain background means the pieces separate on a colour
test rather than needing a mask anyone has to draw.

    python3 scripts/recompose.py IN.png OUT.png --split 478 \
        --left-scale 0.88 --right-scale 1.35 --gap 90
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def background(a: np.ndarray) -> np.ndarray:
    edges = np.concatenate([a[0:6].reshape(-1, 3), a[-6:].reshape(-1, 3)])
    return np.median(edges, axis=0)


def bbox(ink: np.ndarray, x0: int, x1: int) -> tuple[int, int, int, int]:
    sub = ink[:, x0:x1]
    ys = np.where(sub.any(axis=1))[0]
    xs = np.where(sub.any(axis=0))[0]
    return x0 + int(xs.min()), int(ys.min()), x0 + int(xs.max()) + 1, int(ys.max()) + 1


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("src", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--split", type=int, required=True,
                    help="column separating the two pieces")
    ap.add_argument("--left-scale", type=float, default=1.0)
    ap.add_argument("--right-scale", type=float, default=1.0)
    ap.add_argument("--gap", type=int, default=80,
                    help="empty pixels between the two pieces")
    ap.add_argument("--threshold", type=int, default=60)
    args = ap.parse_args()

    im = Image.open(args.src).convert("RGB")
    a = np.asarray(im).astype(int)
    bg = background(a)
    ink = np.abs(a - bg).sum(axis=2) > args.threshold

    left = bbox(ink, 0, args.split)
    right = bbox(ink, args.split, im.width)

    def piece(box, scale):
        crop = im.crop(box)
        size = (max(1, round(crop.width * scale)), max(1, round(crop.height * scale)))
        return crop.resize(size, Image.LANCZOS)

    lp, rp = piece(left, args.left_scale), piece(right, args.right_scale)

    canvas = Image.new("RGB", im.size, tuple(int(v) for v in bg))
    total = lp.width + args.gap + rp.width
    if total > im.width:
        raise SystemExit(
            f"the pieces need {total}px and the canvas is {im.width}px. "
            f"Reduce a scale or the gap by at least {total - im.width}px."
        )

    # Both pieces keep the ground line they were drawn on, so nothing floats.
    ground = max(left[3], right[3])
    x = (im.width - total) // 2
    canvas.paste(lp, (x, ground - lp.height))
    canvas.paste(rp, (x + lp.width + args.gap, ground - rp.height))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(args.out)

    man_h, desk_w = lp.height, rp.width
    print(f"left  {left} scaled {args.left_scale} -> {lp.width}x{lp.height}")
    print(f"right {right} scaled {args.right_scale} -> {rp.width}x{rp.height}")
    print(f"gap {args.gap}px, margins {x}px, ground y={ground}")
    print(f"desk width / man height = {desk_w / man_h:.2f} (was 0.48)")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
