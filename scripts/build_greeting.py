#!/usr/bin/env python3
"""Assemble the greeting: a body, a forearm that lifts, and a hand swapped at the top.

Three drawings go in and three layers come out. The split is not tidiness, it is
what the model can actually do: asked for a figure waving, it drew the shaka
correctly and then drew it the size of his head, floating beside him. It holds
the shape or the scale, never both. So the body is drawn with both arms down,
the hand is drawn on its own, and they are joined here.

What this does, in order:

- finds the waving forearm as a skin coloured component, which works because the
  style is flat and the arms hang clear of the hips
- finds the wrist the way split_layers.py finds the neck, by measuring the width
  of the component row by row and taking the narrowest band
- cuts the forearm at the elbow with a tab reaching up under the sleeve, and the
  body is drawn over that tab, so a rotating forearm never opens a wedge
- builds two versions of the arm: as drawn, and with the shaka hand in place of
  his own, rotated back by the angle the runtime will rotate it forward, so the
  hand stands upright at the top of the wave

    python3 scripts/build_greeting.py <body.png> <hand.png> <out_dir>

The cut comes before any colour correction, and that order is not cosmetic:
correcting the cast first left the white t-shirt seven units from the ground and
the cutout swallowed it. See docs/solutions/cut-before-you-correct-the-cast.md.

Superseded by scripts/build_contact.py, which stopped generating the person at
all. See docs/solutions/the-second-drawing-is-a-different-person.md. This file
is kept because it is what produced the v1 approved assets.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
TOKENS = {
    "SKIN": (0xF2, 0xD5, 0xC0), "HAIR": (0x2B, 0x21, 0x18), "SHIRT": (0xFB, 0xFB, 0xF9),
    "DENIM": (0x4A, 0x6F, 0xA5), "SOLE": (0x16, 0x16, 0x1A),
}
TAB_ROWS = 46          # how far the forearm reaches up under the sleeve
SWING_DEG = 150        # how far the runtime lifts it, from hanging to beside his ear


def classify(rgb: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    names = list(TOKENS)
    d = np.stack([((rgb.astype(int) - np.array(TOKENS[n])) ** 2).sum(-1) for n in names], -1)
    lab = np.argmin(d, -1)
    lab[alpha < 128] = -1
    return lab


def find_hand(mask: np.ndarray) -> np.ndarray:
    """The hand, not the biggest thing in the picture.

    The drawing that has the gesture right also has a small figure standing
    beside it, and that figure has the larger area, so picking by size picked the
    man. A hand held up is about as wide as it is tall; a standing person is
    twice as tall as wide. Shape decides.
    """
    n, comp, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    parts = [i for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] > 1500]
    if not parts:
        raise SystemExit("nothing found where a hand was expected")
    def squareness(i: int) -> float:
        return stats[i, cv2.CC_STAT_WIDTH] / max(stats[i, cv2.CC_STAT_HEIGHT], 1)

    best = max(parts, key=squareness)
    return comp == best


def wrist_row(mask: np.ndarray, lo: float = 0.55, hi: float = 0.92) -> int:
    """The narrowest row in the lower part of the forearm: that is the wrist."""
    rows = np.flatnonzero(mask.any(1))
    top, bottom = int(rows[0]), int(rows[-1])
    span = bottom - top
    a, b = top + int(span * lo), top + int(span * hi)
    widths = [(int(mask[y].sum()), y) for y in range(a, b) if mask[y].any()]
    if not widths:
        raise SystemExit("the forearm has no wrist to find")
    return min(widths)[1]


def build(body_path: Path, hand_path: Path, out_dir: Path, side: str) -> dict:
    body = np.array(Image.open(body_path).convert("RGBA"))
    alpha = body[..., 3]
    h, w = alpha.shape
    lab = classify(body[..., :3], alpha)

    skin = cv2.morphologyEx((lab == 0).astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, comp, stats, cent = cv2.connectedComponentsWithStats(skin, 8)
    parts = [i for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] > 1200]
    if len(parts) < 3:
        raise SystemExit(
            f"found {len(parts)} skin shapes, expected a face and two arms. The arms "
            "are touching the body, which the brief forbids for exactly this reason."
        )
    # The face is the highest one; the arms are the other two, picked by side.
    face = min(parts, key=lambda i: stats[i, cv2.CC_STAT_TOP])
    arms = [i for i in parts if i != face]
    arms.sort(key=lambda i: cent[i][0])
    arm_idx = arms[0] if side == "left" else arms[-1]
    arm = comp == arm_idx

    wrist = wrist_row(arm)
    elbow_row = int(np.flatnonzero(arm.any(1))[0])
    xs = np.flatnonzero(arm[elbow_row:elbow_row + 10].any(0))
    pivot = [int((xs[0] + xs[-1]) // 2), elbow_row]

    top = max(0, elbow_row - TAB_ROWS)
    # The tab is the sleeve directly above the forearm and nothing else. Taking
    # the whole band took the sleeve's anti-aliased edge with it, and those pale
    # pixels flicked out past the body as the arm turned. Restricted to the
    # sleeve's own colours and eroded, they stay under the body that covers them.
    sleeve = np.isin(lab, [0, 2])            # skin or shirt
    band = sleeve.copy()
    band[:top] = False
    band[elbow_row:] = False
    keep = np.zeros_like(arm)
    lo, hi = max(int(xs[0]) - 2, 0), int(xs[-1]) + 2
    keep[:, lo:hi] = True
    tab = cv2.erode((band & keep).astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)

    forearm = arm.copy()
    forearm[wrist:] = arm[wrist:]          # keep his own hand for the resting arm
    arm_full = forearm | tab

    # The body keeps everything except the forearm, and keeps the sleeve, which is
    # what hides the tab when the arm turns.
    body_raw = (alpha >= 128) & ~arm

    hand_img = np.array(Image.open(hand_path).convert("RGBA"))
    hand_mask = find_hand(hand_img[..., 3] >= 128)
    hy, hx = np.nonzero(hand_mask)
    hand_crop = hand_img[hy.min():hy.max() + 1, hx.min():hx.max() + 1].copy()
    hm = hand_mask[hy.min():hy.max() + 1, hx.min():hx.max() + 1]
    hand_crop[..., 3] = np.where(hm, hand_crop[..., 3], 0)

    # Scale the drawn hand to the forearm it lands on, then rotate it back by the
    # angle the runtime will add, so it stands upright once the arm is up.
    forearm_w = int(arm[wrist].sum())
    scale = (forearm_w * 2.35) / hand_crop.shape[1]
    # One sense of rotation, written down once: the rig stores the direction the
    # way CSS means it, positive clockwise, because the site is what turns the
    # arm. PIL turns the other way, so anything rendered here negates it. Not
    # writing that down cost an afternoon of arms lifting into the body and
    # disappearing behind it.
    turn = -1 if side == "right" else 1          # css sense, positive clockwise
    bake = turn * SWING_DEG
    drawn = Image.fromarray(hand_crop)
    if side == "left":
        # The hand was drawn as a right hand. On the other arm it is mirrored,
        # which costs nothing and stops the thumb pointing the wrong way.
        drawn = drawn.transpose(Image.FLIP_LEFT_RIGHT)
    hand = drawn.resize(
        (max(1, int(hand_crop.shape[1] * scale)), max(1, int(hand_crop.shape[0] * scale))),
        Image.LANCZOS,
    ).rotate(bake, Image.BICUBIC, expand=True)

    def clean(mask: np.ndarray, min_area: int = 200) -> np.ndarray:
        """Drop the crumbs. The sleeve's edge leaves a few dozen pale pixels that
        belong to no shape, and they travel with the arm as a trail of specks."""
        n_, comp_, stats_, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
        out = np.zeros_like(mask)
        for i in range(1, n_):
            if stats_[i, cv2.CC_STAT_AREA] >= min_area:
                out |= comp_ == i
        return out

    def layer(mask: np.ndarray) -> Image.Image:
        out = body.copy()
        out[..., 3] = np.where(mask, alpha, 0)
        return Image.fromarray(out)

    out_dir.mkdir(parents=True, exist_ok=True)
    layer(clean(body_raw, 400)).save(out_dir / "body.png")
    arm_full = clean(arm_full)
    layer(arm_full).save(out_dir / "arm-rest.png")

    # The waving arm: the forearm without his own hand, with the drawn one on the end.
    cut = arm_full.copy()
    cut[wrist + 4:] = False
    wave = layer(cut)
    wx = np.flatnonzero(arm[wrist])
    anchor = (int((wx[0] + wx[-1]) / 2 - hand.width / 2), int(wrist - hand.height * 0.28))
    wave.alpha_composite(hand, (max(0, anchor[0]), max(0, anchor[1])))
    wave.save(out_dir / "arm-wave.png")

    return {
        "canvas": [w, h],
        "pivot": pivot,
        "wrist": int(wrist),
        "swing_deg": SWING_DEG,
        "turn": turn,
        "side": side,
        "draw_order": ["arm", "body"],
        "layers": {"body": "body.png", "arm_rest": "arm-rest.png", "arm_wave": "arm-wave.png"},
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("body", type=Path)
    ap.add_argument("hand", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--side", choices=("left", "right"), default="right",
                    help="which arm waves, as the viewer sees it")
    args = ap.parse_args()
    rig = build(args.body.resolve(), args.hand.resolve(), args.out_dir.resolve(), args.side)
    (args.out_dir / "rig.json").write_text(json.dumps(rig, indent=2) + "\n")
    print(f"elbow at {rig['pivot']}, wrist at y={rig['wrist']}, swing {rig['swing_deg']} degrees")
    return 0


if __name__ == "__main__":
    sys.exit(main())
