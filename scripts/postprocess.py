#!/usr/bin/env python3
"""Correct a generated image deterministically, instead of generating it again.

Written up, with the two thresholds it got wrong first, in
docs/solutions/correct-the-image-not-the-prompt.md.

Every prompt is a sample. Two runs of the same brief differ, and a defect fixed
by re-rolling is a defect fixed by luck, which means it comes back. See
docs/solutions/the-model-has-no-memory.md.

The usual answer is to push the defect into the negative prompt, and here that
answer is unavailable: the backend that produces this project's approved style
is guidance-distilled and discards the negative block entirely. See
docs/solutions/the-negative-block-was-carrying-the-style.md. So prohibitions
either become affirmations in the positive block, which is unreliable, or they
become a correction applied afterwards, which is not.

Two corrections, both chosen because they are safe on flat artwork and would be
reckless on a photograph.

**clean-ground** removes soft shading from the background. A drop shadow under a
desk is a large, low-contrast blob sitting on the paper; real artwork is far from
the paper colour. Filling inward from the border with a generous tolerance finds
the blob, and dilating the artwork mask first keeps the fill off anti-aliased
edges, which are in the same colour band and must survive.

**snap-palette** pulls every sizeable flat region onto the nearest colour in the
spec's own token table, read from the spec at run time rather than copied here.
Small regions are left alone: syntax colours on a screen are meant to be many,
and a palette that eats them is a palette applied too eagerly.

    python3 scripts/postprocess.py IN.png OUT.png --clean-ground
    python3 scripts/postprocess.py IN.png OUT.png --snap-palette --clean-ground
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "docs" / "ILLUSTRATION_SPEC.md"


def tokens() -> np.ndarray:
    """Every hex colour in the spec's token tables. One copy, read at run time."""
    text = SPEC.read_text(encoding="utf-8")
    hexes = re.findall(r"`#([0-9A-Fa-f]{6})`", text)
    if not hexes:
        raise SystemExit(f"no token colours found in {SPEC}")
    seen = list(dict.fromkeys(h.upper() for h in hexes))
    return np.array([[int(h[i:i+2], 16) for i in (0, 2, 4)] for h in seen])


def border_colour(a: np.ndarray) -> np.ndarray:
    edges = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    return np.median(edges, axis=0)


def artwork_threshold(d: np.ndarray) -> int:
    """Where shading stops and artwork begins, found rather than chosen.

    In a flat palette the two are nowhere near each other: on the desk asset the
    drop shadow reached 70 units from the paper and the nearest real colour sat
    at 466. Between them the histogram is empty, and the middle of that empty
    stretch is the only threshold that cannot be argued with.

    Picking the number by hand is what went wrong the first time. At 60 the
    darkest part of the shadow counted as artwork, so the guard ring around it
    blocked the fill from reaching the rest, and the shadow survived a pass that
    reported success.
    """
    hist, edges = np.histogram(d[d > 12], bins=60, range=(12, 612))
    empty = hist < d.size * 0.00002
    best_len = best_start = 0
    run = 0
    for i, e in enumerate(empty):
        run = run + 1 if e else 0
        if run > best_len:
            best_len, best_start = run, i - run + 1
    if best_len < 3:
        return 150
    lo, hi = edges[best_start], edges[best_start + best_len]
    return int((lo + hi) / 2)


def clean_ground(a: np.ndarray, keep: int | None = None, flat: int = 8,
                 guard: int = 3) -> tuple[np.ndarray, int]:
    """Erase anything faint that sits on the background and is not artwork.

    **Not safe on a pale subject.** This finds the ground by walking inward from
    the image border through everything faint. In a style with no outlines a
    white t-shirt is a few units from the paper and continuous with it, so the
    walk goes straight into the figure: run on the walking character it erased
    the folds across his chest and reported success. Use it on a scene whose
    subject is dark against paper, which is what it was written for, and leave
    it off for anything pale. See
    docs/solutions/clean-ground-cannot-see-an-outline-that-is-not-there.md.
    """
    bg = border_colour(a)
    d = np.abs(a - bg).sum(axis=2)
    if keep is None:
        keep = artwork_threshold(d)
        print(f"clean-ground: artwork starts at distance {keep}, found from the "
              f"gap in the histogram")

    artwork = (d > keep).astype(np.uint8)
    # Anti-aliased edges sit in the same band as shading. Growing the artwork
    # mask by a few pixels puts them out of reach of the fill.
    protected = cv2.dilate(artwork, np.ones((guard * 2 + 1,) * 2, np.uint8))

    faint = ((d <= keep) & (protected == 0)).astype(np.uint8)
    n, labels = cv2.connectedComponents(faint, connectivity=8)

    border = set(labels[0]) | set(labels[-1]) | set(labels[:, 0]) | set(labels[:, -1])
    border.discard(0)
    reachable = np.isin(labels, list(border))

    shading = reachable & (d > flat)

    # Filling with the border colour leaves a patch. The paper in a generated
    # image is not perfectly uniform: it carries a faint texture and a slight
    # vignette, so a flat fill reads as a lighter sticker outline hugging every
    # object. Inpainting takes its colour from the immediate surroundings
    # instead, which is the difference between removing a shadow and replacing
    # it with a halo.
    mask = cv2.dilate(shading.astype(np.uint8),
                      np.ones((3, 3), np.uint8), iterations=1)
    src = np.ascontiguousarray(a.astype(np.uint8)[:, :, ::-1])
    filled = cv2.inpaint(src, mask, 5, cv2.INPAINT_TELEA)
    out = filled[:, :, ::-1].astype(int)
    return out, int(shading.sum())


def snap_palette(a: np.ndarray, min_area: int = 2000,
                 max_move: int = 120) -> tuple[np.ndarray, int]:
    """Move large flat areas onto the nearest token colour."""
    pal = tokens()
    flat = a.reshape(-1, 3)
    colours, counts = np.unique(flat, axis=0, return_counts=True)

    out = a.copy()
    moved = 0
    for colour, count in zip(colours, counts, strict=True):
        if count < min_area:
            continue
        dist = np.abs(pal - colour).sum(axis=1)
        j = int(dist.argmin())
        if dist[j] == 0 or dist[j] > max_move:
            continue
        mask = (a == colour).all(axis=2)
        out[mask] = pal[j]
        moved += int(mask.sum())
    return out, moved


def white_balance(a: np.ndarray, paper=(247, 246, 243), border: int = 12,
                  reach: float = 0.30, floor: float = 0.15) -> tuple[np.ndarray, list]:
    """Remove a colour cast, using the paper as the known white.

    The local model tints every flat ground it is given: mint, sage, pale
    yellow. The tint is not only in the ground, it sits over the whole image,
    so repainting the ground alone leaves grey houses green. What the image
    should look like is known at one point, the paper, so the gap between the
    ground it drew and the real paper measures the cast, the way a camera
    reads it off a grey card.

    Applied uniformly it overshoots: a green apron the brief asked for turns
    blue. So the correction is full on near-neutral pixels, where the cast is
    all there is, and fades on saturated ones, which are object colour. The
    ground's own saturation is subtracted first, because on a tinted image the
    ground is the one thing whose saturation is entirely cast.
    """
    b = border
    edge = np.concatenate([a[:b].reshape(-1, 3), a[-b:].reshape(-1, 3),
                           a[:, :b].reshape(-1, 3), a[:, -b:].reshape(-1, 3)])
    bg = np.median(edge, axis=0).astype(float)
    gain = np.array(paper, float) / np.maximum(bg, 1)
    mx, mn = a.max(axis=2), a.min(axis=2)
    sat = (mx - mn) / np.maximum(mx, 1)
    bsat = (bg.max() - bg.min()) / max(bg.max(), 1)
    w = np.clip(1 - (sat - bsat) / reach, floor, 1)[..., None]
    out = np.clip(a * (1 + (gain - 1) * w), 0, 255).astype(int)
    return out, [int(v) for v in bg]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("src", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--clean-ground", action="store_true")
    ap.add_argument("--snap-palette", action="store_true")
    ap.add_argument("--white-balance", action="store_true",
                    help="remove the colour cast, reading white off the paper")
    ap.add_argument("--keep", type=int, default=None,
                    help="above this distance it is artwork. Detected when omitted")
    ap.add_argument("--guard", type=int, default=3,
                    help="pixels of protection around artwork edges")
    args = ap.parse_args()

    if not (args.clean_ground or args.snap_palette or args.white_balance):
        raise SystemExit("nothing to do: pass --clean-ground, --snap-palette or --white-balance")

    im = Image.open(args.src).convert("RGB")
    a = np.asarray(im).astype(int)

    if args.white_balance:
        a, bg = white_balance(a)
        print(f"white-balance: ground was {tuple(bg)}, now paper")
    if args.clean_ground:
        a, n = clean_ground(a, keep=args.keep, guard=args.guard)
        print(f"clean-ground: {n} pixels of shading removed")
    if args.snap_palette:
        a, n = snap_palette(a)
        print(f"snap-palette: {n} pixels moved onto token colours")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(a.astype(np.uint8)).save(args.out)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
