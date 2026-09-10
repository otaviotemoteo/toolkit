#!/usr/bin/env python3
"""Cut a flat illustration off its plain background, keeping white interiors.

The chroma key this replaces never worked: a diffusion model does not produce a
uniform key colour, and the first real attempt came back as striped pale mint
with a blob in one corner. A luminance key worked while the drawing was pure
line art and died the moment the character was coloured.

What works for a flat illustration on a plain field is neither. The background
is not a colour to match, it is the region **connected to the border**. Fill
inward from the edge through everything that matches the background, and
whatever the fill cannot reach is the subject, including a white t-shirt that is
within a few units of the paper it stands on. That last part is the whole point:
this character's shirt is 6 units from the background out of 765, so any test
that asks "is this pixel white" erases his torso.

    python3 scripts/cutout_flat.py IN.png OUT.png [--tolerance 3] [--feather 1]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("src", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--tolerance", type=int, default=3,
                    help="how far from the border colour still counts as background")
    ap.add_argument("--erode", type=int, default=2,
                    help="pixels to shrink the mask by, to drop the pale ring of "
                         "half-background pixels along every edge")
    ap.add_argument("--feather", type=float, default=0.8,
                    help="blur radius on the alpha edge, in pixels")
    ap.add_argument("--trim", action="store_true",
                    help="crop the result to the subject")
    args = ap.parse_args()

    im = Image.open(args.src).convert("RGB")
    a = np.asarray(im).astype(int)
    h, w, _ = a.shape

    edges = np.concatenate([a[0].reshape(-1, 3), a[-1].reshape(-1, 3),
                            a[:, 0].reshape(-1, 3), a[:, -1].reshape(-1, 3)])
    bg = np.median(edges, axis=0)
    matches = np.abs(a - bg).sum(axis=2) <= args.tolerance

    # Flood inward from every border pixel that matches. Iterative, because a
    # 1254x1254 background is far past Python's recursion limit.
    outside = np.zeros((h, w), dtype=bool)
    stack: list[tuple[int, int]] = []
    for x in range(w):
        for y in (0, h - 1):
            if matches[y, x] and not outside[y, x]:
                outside[y, x] = True
                stack.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if matches[y, x] and not outside[y, x]:
                outside[y, x] = True
                stack.append((y, x))

    while stack:
        y, x = stack.pop()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < h and 0 <= nx < w and matches[ny, nx] and not outside[ny, nx]:
                outside[ny, nx] = True
                stack.append((ny, nx))

    alpha = Image.fromarray(np.where(outside, 0, 255).astype(np.uint8), "L")

    # The border between subject and background is anti-aliased, so a ring of
    # pixels just inside the silhouette is most of the way to white. Left
    # opaque they read as a halo against any darker page. Shrinking the mask
    # discards them; the tolerance cannot, because it has to stay below the
    # distance of the white shirt or the torso disappears with them.
    for _ in range(max(0, args.erode)):
        alpha = alpha.filter(ImageFilter.MinFilter(3))

    if args.feather > 0:
        alpha = alpha.filter(ImageFilter.GaussianBlur(args.feather))

    rgba = im.convert("RGBA")
    rgba.putalpha(alpha)

    if args.trim:
        box = rgba.getbbox()
        if box:
            rgba = rgba.crop(box)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    rgba.save(args.out)

    kept = int((~outside).sum())
    print(f"background {tuple(int(v) for v in bg)}, tolerance {args.tolerance}")
    print(f"subject {kept}px of {h*w} ({100*kept/(h*w):.1f}%), size {rgba.size}")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
