#!/usr/bin/env python3
"""Draw the benchmark card, instead of generating it.

Five of the six project cards are scenes with people in them, and a model is
the right tool for those. This one is a chart, and four attempts at it came
back with the line bent into a worm and a fishing hook floating unattached to
anything. That is not bad luck: a chart is geometry, every value in it means
something, and a model that cannot write also cannot be trusted to keep a line
straight for a reason.

So it takes the route docs/asset-map.md already describes for diagrams: drawn
from numbers, in the palette, with nothing sampled. What it has to share with
its five neighbours is the ground, so the paper carries a little grain and the
drawing is supersampled and reduced, which lands its edges as softly as painted
ones.

The shape is the project's result: a detector that scores near the top within
one dataset and falls when it meets another.

    python3 scripts/draw_chart.py <out.png> [--texture <approved card>]
"""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
PAPER = (247, 246, 243)
INDIGO = (93, 93, 156)
ORANGE = (199, 125, 90)
RULE = (214, 211, 203)
SS = 4  # supersample factor


def series(w: int, h: int) -> tuple[list, list]:
    """The two halves of the story, in picture coordinates."""
    rng = random.Random(7)
    high, low = h * 0.30, h * 0.74
    left, right = w * 0.10, w * 0.92
    knee = w * 0.56
    intra, cross = [], []
    x = left
    while x <= knee:
        intra.append((x, high + rng.uniform(-2.5, 2.5)))
        x += (knee - left) / 26
    # The fall is a single smooth arc, not a step: the model does not break, it
    # degrades, and a cliff would say something the numbers do not.
    steps = 30
    for i in range(steps + 1):
        t = i / steps
        x = knee + (right - knee) * t
        y = high + (low - high) * (1 - math.cos(t * math.pi)) / 2
        cross.append((x, y + rng.uniform(-1.5, 1.5)))
    return intra, cross


def draw(w: int = 1024, h: int = 576) -> Image.Image:
    W, H = w * SS, h * SS
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    for i in range(3):
        y = H * (0.42 + i * 0.14)
        d.line([(W * 0.08, y), (W * 0.94, y)], fill=RULE, width=2 * SS)

    intra, cross = series(W, H)
    # Where the data stops coming from the set the model was trained on. Dashed
    # and faint: it is the reason for the fall, not the subject of the picture.
    knee_x = intra[-1][0]
    step = 22 * SS
    y = H * 0.18
    while y < H * 0.86:
        d.line([(knee_x, y), (knee_x, min(y + step * 0.55, H * 0.86))], fill=RULE, width=2 * SS)
        y += step
    d.line(intra, fill=INDIGO, width=9 * SS, joint="curve")
    d.line(cross, fill=ORANGE, width=9 * SS, joint="curve")
    for pts, colour in ((intra, INDIGO), (cross, ORANGE)):
        for x, y in (pts[0], pts[-1]):
            r = 5 * SS
            d.ellipse([x - r, y - r, x + r, y + r], fill=colour)

    im = im.resize((w, h), Image.LANCZOS)

    # Paper grain, made rather than borrowed. Two attempts took it from an
    # approved card: the first printed that card's whole scene in here as a
    # ghost, and the second, taking only the high frequencies, printed its
    # outlines embossed. The high frequency of a drawing is its edges. Grain is
    # noise, so grain is what gets generated, from a fixed seed so the card is
    # the same file every time it is drawn.
    rng = np.random.default_rng(11)
    noise = rng.normal(0, 1, (h, w))
    noise = np.asarray(Image.fromarray(((noise * 40) + 128).clip(0, 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(0.6))).astype(float) - 128
    out = np.asarray(im).astype(float) * (1 + noise / 900)[..., None]
    im = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    return im


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("out", type=Path)
    args = ap.parse_args()
    im = draw()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    im.save(args.out)
    print(f"wrote {args.out} {im.size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
