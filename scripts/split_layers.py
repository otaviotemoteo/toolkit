#!/usr/bin/env python3
"""Cut an approved character into the layers the hero animation moves.

Four rebuilds went into the cuts below, and the reasoning for each is in
docs/solutions/two-raster-layers-cannot-share-a-pixel.md.

The animation is compositing, not generation: the body never changes, the neck
turns half of what the head turns, and the head carries the rest. See
briefs/hero-character/motion.md, and
docs/solutions/pose-variation-is-not-generation.md for why generating poses was
rejected before this existed.

Three things here are deliberate and easy to get wrong.

**The cuts are found, not typed.** A standing figure has one narrow place
between the hair and the shoulders, and that is the neck. Measuring the width of
the alpha mask row by row finds it on any character, so this does not have to be
retuned by hand for the next one.

**No two layers share a pixel.** The first version cut a separate neck and let
it overlap the head, so that a rotation would slide the seam across solid pixels
instead of across a hole. It ghosted: the same skin appeared in both layers at
two different angles, and the jaw grew a ragged double edge that was obvious at
any zoom. Overlap is the right instinct for a rig whose parts are drawn
separately, and the wrong one for parts cut out of a single flat drawing.

**One joint, not two.** So the head carries the neck with it and turns about the
base of the neck, where the collar is. The collar is static and opaque, and at
the pivot itself nothing moves at all, so the joint is covered at every angle
the brief allows. The two-bone neck that `motion.md` specified was abandoned for
this reason and the brief now records it.

**The body starts at the pivot.** Not above it. Anything static sitting higher
than the joint can peek out from behind the part that rotates.

**The tab fades out instead of ending.** Even on bare skin a hard edge shows: the
rotation resamples the layer, the cut row becomes partly transparent, and it
blends against the body underneath as a faint line straight across the neck.
Ramping the tab's alpha to nothing over its last rows removes it, because there
is no longer an edge to catch the light, only the same skin twice.

**The head's tab stops on bare skin.** It reaches a little past the joint so the
collar has something to cover, and only a little: the first attempt reached far
enough to include the collar line itself, which then rotated with the head and
appeared twice, one arc against the other. A tab must end where there is nothing
to see, because whatever it ends on is duplicated the moment anything turns.

    python3 scripts/split_layers.py IN.png OUT_DIR
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def find_neck(solid: np.ndarray, search_to: float = 0.40) -> tuple[int, int]:
    """The narrowest run of rows between the top of the head and the shoulders.

    Returns the first and last row of that run, so a neck that is narrow for
    fifty rows is reported as a band rather than as one arbitrary line inside it.
    """
    width = solid.sum(axis=1)
    filled = np.where(width > 0)[0]
    if not len(filled):
        raise SystemExit("the image is empty")
    top = int(filled[0])
    limit = int(top + (solid.shape[0] - top) * search_to)

    # Ignore the first rows: a single hair spike is narrow and is not a neck.
    start = top + max(8, (limit - top) // 12)
    band = width[start:limit]
    if not len(band):
        raise SystemExit("no room to look for a neck")
    narrowest = int(band.min())
    rows = [start + i for i, v in enumerate(band) if v <= narrowest * 1.15]
    return rows[0], rows[-1]


def find_eyes(head: Image.Image) -> list[tuple[int, int, int, int]]:
    """The two dark ovals in the middle of the face.

    Found by shape rather than by coordinate, so the next character does not
    need the numbers retyped. Eyebrows sit above the eyes and are wider than
    they are tall, which is what separates the two pairs; anything that is not
    one of exactly two similar shapes is reported as not found, because a
    wrong guess here moves a facial feature and that is worse than not moving
    one at all.
    """
    a = np.asarray(head.convert("RGBA"))
    dark = ((a[..., :3].astype(int).sum(axis=2) < 260) & (a[..., 3] > 128))
    n, _, stats, _ = cv2.connectedComponentsWithStats(dark.astype(np.uint8), 8)

    found = []
    for i in range(1, n):
        x, y, w, h, area = stats[i]
        if not (60 <= area <= 3000):
            continue
        if h <= w:            # wider than tall: an eyebrow or a mouth
            continue
        if y < head.height * 0.25:   # too high on the head to be an eye
            continue
        found.append((int(x), int(y), int(w), int(h)))

    if len(found) != 2:
        return []
    found.sort()
    (x0, y0, w0, h0), (x1, y1, w1, h1) = found
    # A face has two eyes at the same height and of the same size. Anything
    # else means the detection caught something it should not have.
    if abs(y0 - y1) > max(h0, h1) * 0.4 or abs(h0 - h1) > max(h0, h1) * 0.5:
        return []
    return found


def split_eyes(head: Image.Image, out: Path, pad: int = 3) -> dict | None:
    """Lift the eyes onto their own layer and heal the face behind them."""
    boxes = find_eyes(head)
    if not boxes:
        return None

    a = np.asarray(head.convert("RGBA"))
    mask = np.zeros(a.shape[:2], np.uint8)
    for x, y, w, h in boxes:
        mask[y:y + h, x:x + w] = 1

    eyes = np.zeros_like(a)
    keep = mask.astype(bool)
    eyes[keep] = a[keep]
    Image.fromarray(eyes, "RGBA").save(out / "eyes.png")

    # Paint skin over where they were, taken from the surrounding face, so the
    # layer beneath is a complete face rather than a face with two holes.
    grown = cv2.dilate(mask, np.ones((pad * 2 + 1,) * 2, np.uint8))
    bgr = np.ascontiguousarray(a[..., :3][:, :, ::-1])
    healed = cv2.inpaint(bgr, grown, 5, cv2.INPAINT_TELEA)[:, :, ::-1]
    base = a.copy()
    base[..., :3] = healed
    Image.fromarray(base, "RGBA").save(out / "head.png")

    return {"file": "eyes.png", "boxes": boxes}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("src", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--feather", type=int, default=14,
                    help="rows over which the head tab fades into the body")
    ap.add_argument("--tab", type=int, default=18,
                    help="rows the head reaches past the joint. Keep it on bare "
                         "skin: anything drawn inside the tab appears twice")
    ap.add_argument("--neck-top", type=int, default=None, help="override detection")
    ap.add_argument("--neck-bottom", type=int, default=None, help="override detection")
    args = ap.parse_args()

    im = Image.open(args.src).convert("RGBA")
    solid = np.asarray(im)[..., 3] > 128
    w, h = im.size

    top, bottom = find_neck(solid)
    if args.neck_top is not None:
        top = args.neck_top
    if args.neck_bottom is not None:
        bottom = args.neck_bottom

    # The pivots sit on the centre of the figure at each joint.
    xs = np.where(solid[top:bottom + 1].any(axis=0))[0]
    cx = int((xs.min() + xs.max()) / 2) if len(xs) else w // 2

    o = args.tab
    bands = {
        # From the joint down, and never above it: a static pixel higher than
        # the pivot can appear from behind the head when the head turns.
        "body": (bottom, h),
        # Hair, face and the whole neck, reaching past the joint so the collar
        # always has something to cover.
        "head": (0, min(h, bottom + o)),
    }

    args.out.mkdir(parents=True, exist_ok=True)

    def feathered(layer: Image.Image, rows: int) -> Image.Image:
        """Fade the bottom rows of a layer to nothing."""
        if rows <= 0 or layer.height <= rows:
            return layer
        a = np.asarray(layer).copy()
        ramp = np.linspace(1.0, 0.0, rows).reshape(-1, 1)
        a[-rows:, :, 3] = (a[-rows:, :, 3] * ramp).astype(np.uint8)
        return Image.fromarray(a, "RGBA")

    manifest = {
        "source": str(args.src),
        "size": [w, h],
        "neck_band": [top, bottom],
        "overlap": o,
        # One joint, at the base of the neck. See the module docstring for why
        # the second joint was removed.
        "pivots": {"head": [cx, bottom]},
        "draw_order": ["body", "head"],
        "layers": {},
    }

    for name, (y0, y1) in bands.items():
        layer = im.crop((0, y0, w, y1))
        if name == "head":
            layer = feathered(layer, args.feather)
        path = args.out / f"{name}.png"
        layer.save(path)
        manifest["layers"][name] = {"file": path.name, "top": y0, "height": y1 - y0}
        print(f"{name:5s} rows {y0:4d}..{y1:4d}  {layer.size[0]}x{layer.size[1]}")

    # The head layer has just been written, so this reads it back and replaces
    # it with a version whose eyes have been lifted off and painted over.
    eyes = split_eyes(Image.open(args.out / "head.png"), args.out)
    if eyes:
        manifest["layers"]["eyes"] = {"file": "eyes.png",
                                      "top": bands["head"][0],
                                      "height": bands["head"][1] - bands["head"][0]}
        manifest["draw_order"].append("eyes")
        manifest["eye_boxes"] = eyes["boxes"]
        print(f"eyes  {len(eyes['boxes'])} found at {eyes['boxes']}, "
              f"face healed behind them")
    else:
        print("eyes  not found: the head layer keeps them, and they will not move")

    (args.out / "layers.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"\nneck band rows {top}..{bottom}, pivots at x={cx}")
    print(f"wrote {args.out}/layers.json")


if __name__ == "__main__":
    main()
