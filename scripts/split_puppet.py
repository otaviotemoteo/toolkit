#!/usr/bin/env python3
"""Cut a flat side-on figure into a puppet that can walk.

The head split in scripts/split_layers.py found one joint by measuring the
alpha mask. A walking figure needs the same idea applied to limbs, and the
thing that makes it possible is the same thing that makes everything else here
work: the style is flat. Every part of the body is one solid token colour, so
classifying each pixel to its nearest token and labelling connected components
hands back the parts without a single hand-drawn selection.

What this produces, and why it stops there:

- **Legs rotate at the hip. Nothing else moves.** The four rebuilds behind
  docs/solutions/two-raster-layers-cannot-share-a-pixel.md all came from asking
  one flat drawing for more joints than it can support. Knees and elbows are
  deliberately not cut. The trigger for adding them is written in the strip's
  brief: add them when the walk reads stiff, not before.
- **Every layer is the full canvas.** A layer cropped to its own box has to be
  positioned, and a pivot then has to be expressed relative to that box, which
  is exactly where the hero lost its joint. See
  docs/solutions/a-pivot-in-pixels-is-a-pivot-at-one-size.md. Full canvas layers
  cost a few hundred KB and remove the whole class of error: every pivot is a
  point on one shared canvas.
- **No two layers share a pixel.** Each pixel of the subject goes to exactly
  one layer, checked before anything is written.

    python3 scripts/split_puppet.py <cutout.png> <out_dir>
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

# How far each leg reaches up past its joint, in pixels of the source drawing.
# It has to outlast the sweep: a tab of height h swings h*sin(angle) sideways,
# so 70 covers about 19px at the 16 degrees this walk uses.
TAB_ROWS = 34

# The widest angle the walk uses, from the rig. A tab has to stay hidden at all
# of it, in both directions.
SWING_DEG = 12

# The character's own colours, from docs/ILLUSTRATION_SPEC.md. Read here rather
# than copied so that changing the spec changes the splitter.
TOKENS = {
    "SKIN": (0xF2, 0xD5, 0xC0),
    "HAIR": (0x2B, 0x21, 0x18),
    "SHIRT": (0xFB, 0xFB, 0xF9),
    "DENIM": (0x4A, 0x6F, 0xA5),
    "SOLE": (0x16, 0x16, 0x1A),
}


def classify(rgb: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    """Nearest token per pixel; -1 where the subject is not."""
    names = list(TOKENS)
    d = np.stack([((rgb.astype(int) - np.array(TOKENS[n])) ** 2).sum(-1) for n in names], -1)
    lab = np.argmin(d, -1)
    lab[alpha < 128] = -1
    return lab


def runs(row: np.ndarray, min_width: int = 10) -> list[tuple[int, int]]:
    idx = np.flatnonzero(row)
    if not idx.size:
        return []
    brk = np.flatnonzero(np.diff(idx) > 1)
    starts = np.r_[idx[0], idx[brk + 1]]
    ends = np.r_[idx[brk], idx[-1]]
    return [(int(s), int(e)) for s, e in zip(starts, ends, strict=True) if e - s >= min_width]


def find_crotch(denim: np.ndarray, hold: int = 40) -> int:
    """The row where the trousers stop being one shape and become two.

    Measured, not chosen. A single row with two runs proves nothing: the top
    edge of the denim is ragged and produces stray pairs. The crotch is the
    first row from which two runs survive for `hold` rows together.
    """
    rows = np.flatnonzero(denim.any(1))
    if not rows.size:
        raise SystemExit("no trousers found: is this the right drawing?")
    counts = np.array([len(runs(denim[y])) for y in range(denim.shape[0])])
    for y in range(int(rows[0]), int(rows[-1]) - hold):
        if (counts[y:y + hold] >= 2).all():
            return y
    raise SystemExit(
        "the legs never separate: this drawing cannot become a walking puppet. "
        "Regenerate with the legs apart, which is the first acceptance criterion "
        "in the brief."
    )


def split(src: Path, out_dir: Path) -> dict:
    im = Image.open(src).convert("RGBA")
    a = np.array(im)
    rgb, alpha = a[..., :3], a[..., 3]
    h, w = alpha.shape

    lab = classify(rgb, alpha)
    names = list(TOKENS)
    denim = (lab == names.index("DENIM")).astype(np.uint8)
    denim = cv2.morphologyEx(denim, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))

    crotch = find_crotch(denim)

    # Below the crotch the subject is two separate shapes, one per leg, each
    # carrying its own shoe. Labelling the alpha mask there is enough; nothing
    # has to know which colour a shoe is.
    #
    # The crotch row itself is where they are still touching, by definition, and
    # anti-aliasing keeps them joined for a few rows more. So the labelling
    # starts just below the join and the skipped band is claimed afterwards, by
    # whichever leg is nearer in x. Measured here: at the crotch the mask is one
    # shape, five rows lower it is two.
    band = 0
    for band in range(1, 40):
        probe = (alpha >= 128).astype(np.uint8)
        probe[:crotch + band] = 0
        n, comp, stats, _ = cv2.connectedComponentsWithStats(probe, 8)
        if sum(1 for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] > 2000) >= 2:
            break
    legs = sorted(
        ((stats[i, cv2.CC_STAT_AREA], i) for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] > 2000),
        reverse=True,
    )[:2]
    if len(legs) != 2:
        raise SystemExit(
            f"found {len(legs)} leg shapes below the crotch, expected 2. The "
            "drawing has the legs touching, which the brief forbids for exactly "
            "this reason."
        )

    # The leg whose foot reaches further right is the leading, nearer leg: he
    # walks to the right, so the forward foot is the one the viewer sees in front.
    def foot_x(i: int) -> int:
        return int(stats[i, cv2.CC_STAT_LEFT] + stats[i, cv2.CC_STAT_WIDTH])

    front_i, back_i = sorted((legs[0][1], legs[1][1]), key=foot_x, reverse=True)

    masks: dict[str, np.ndarray] = {}
    for name, idx in (("leg_front", front_i), ("leg_back", back_i)):
        masks[name] = comp == idx

    # Claim the skipped band. Each pixel in it joins the leg whose first labelled
    # row lies nearer in x, so the cut runs straight down the gap between the
    # thighs instead of leaving a wedge that belongs to neither.
    ref = {name: np.flatnonzero(masks[name][crotch + band]) for name in masks}
    if all(r.size for r in ref.values()):
        centres = {name: float(r.mean()) for name, r in ref.items()}
        ys, xs = np.nonzero(alpha[crotch:crotch + band] >= 128)
        for y, x in zip(ys + crotch, xs, strict=True):
            nearest = min(centres, key=lambda k: abs(x - centres[k]))
            masks[nearest][y, x] = True
    # Everything above the cut. The torso carries the head and both arms: one
    # flat drawing supports one joint per limb, and the legs are where a walk is
    # legible. The strip's brief names what unlocks the rest.
    masks["torso"] = (alpha >= 128) & ~masks["leg_front"] & ~masks["leg_back"]

    # Each leg keeps a tab reaching up past the joint, into the hip. Without it
    # a rotating leg cut straight across the top swings its corner out from
    # under the body and opens a wedge of bare paper, which is the same seam the
    # head opened at the collar.
    #
    # The tab is the one place two layers are allowed to hold the same pixel,
    # and the condition is strict: the torso is drawn last and must cover the
    # tab completely at every angle the scene allows. A shared pixel that is
    # visible is a ghost, and that is what
    # docs/solutions/two-raster-layers-cannot-share-a-pixel.md is about.
    tab = TAB_ROWS
    top = max(0, crotch - tab)
    if all(np.flatnonzero(masks[n][crotch + band]).size for n in ("leg_front", "leg_back")):
        centres = {n: float(np.flatnonzero(masks[n][crotch + band]).mean())
                   for n in ("leg_front", "leg_back")}
        # Only trousers. The band above the joint also contains the hand that
        # hangs beside the hip, and claiming it by x alone sent a hand away with
        # a leg. A tab is made of the limb it belongs to, not of whatever is
        # nearby.
        ys, xs = np.nonzero(denim[top:crotch] > 0)
        for y, x in zip(ys + top, xs, strict=True):
            nearest = min(centres, key=lambda k: abs(x - centres[k]))
            masks[nearest][y, x] = True

    # Hip pivots: the top of each leg, centred on the width it actually has
    # there. The pivot sits on the cut, so rotation leaves the cut edge exactly
    # where it was and the trouser stays continuous with the hip above it.
    # The joint is the crotch, not the top of the layer. Since the tab reaches
    # above the joint, reading the pivot off the mask's topmost row would put it
    # on the tab and swing the whole leg from the waist.
    pivots = {}
    for name in ("leg_front", "leg_back"):
        xs = np.flatnonzero(masks[name][crotch + band: crotch + band + 12].any(0))
        pivots[name] = [int((xs[0] + xs[-1]) // 2), crotch]

    overlap = int((masks["leg_front"] & masks["leg_back"]).sum())
    if overlap:
        raise SystemExit(f"the two legs share {overlap} pixels, which ghosts when they move")

    # The tab cannot be made to disappear, so it is made soft.
    #
    # Two exact solutions were tried and both failed on this drawing. Keeping
    # only the tab pixels whose whole orbit stays under the torso removed the
    # ones doing the work and opened a slit at the crotch. Cutting the leg along
    # an arc centred on the pivot, which rotation preserves, needs a radius
    # larger than the hip is wide: the waist here is narrower than the trousers
    # flaring below it, so an arc big enough to close the joint already sticks
    # out of the body at rest.
    #
    # What is left is the answer the neck arrived at. A hard edge reads as a
    # wedge; the same edge faded over its last rows reads as nothing, because
    # the thing it lands on is paper of almost the same value. The tab is short,
    # so the sweep is small, and it fades from fully opaque at the joint to
    # nothing at its top.
    alpha_f = alpha.astype(float)
    for name in ("leg_front", "leg_back"):
        rows = np.arange(top, crotch)
        ramp = np.clip((rows - top) / max(1, crotch - top), 0, 1) ** 0.7
        for y, k in zip(rows, ramp, strict=True):
            sel = masks[name][y]
            if sel.any():
                alpha_f[y, sel] = alpha_f[y, sel] * k

    # How far the top of the tab travels sideways at full swing. Reported so the
    # number is a measurement rather than a hope.
    sweep = (crotch - top) * math.sin(math.radians(SWING_DEG))
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, m in masks.items():
        layer = a.copy()
        src_alpha = alpha_f if name in ("leg_front", "leg_back") else alpha.astype(float)
        layer[..., 3] = np.where(m, np.rint(src_alpha).astype(np.uint8), 0)
        Image.fromarray(layer).save(out_dir / f"{name}.png")

    union = np.zeros_like(alpha, bool)
    for m in masks.values():
        union |= m
    subject = int((alpha >= 128).sum())
    missing = int(((alpha >= 128) & ~union).sum())
    if missing:
        raise SystemExit(f"{missing} pixels of {subject} belong to no layer: a part was lost")

    return {
        "canvas": [w, h],
        "crotch": crotch,
        "draw_order": ["leg_back", "leg_front", "torso"],
        "layers": {n: {"file": f"{n}.png"} for n in masks},
        "pivots": pivots,
        "sweep_px": sweep,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("src", type=Path)
    ap.add_argument("out_dir", type=Path)
    args = ap.parse_args()
    rig = split(args.src.resolve(), args.out_dir.resolve())
    (args.out_dir / "rig.json").write_text(json.dumps(rig, indent=2) + "\n")
    print(f"crotch at y={rig['crotch']}, pivots {rig['pivots']}")
    print(f"tab {TAB_ROWS} rows, sweeping {rig['sweep_px']:.1f}px at {SWING_DEG} degrees")
    print(f"wrote {len(rig['layers'])} layers and rig.json to {args.out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
