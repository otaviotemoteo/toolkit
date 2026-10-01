#!/usr/bin/env python3
"""Render the contact loop as frames, so it can be judged before it is coded.

The timing lives here and in the page, and the two have to agree. This is the
copy that can be looked at: a loop that only exists in a browser is a loop that
gets tuned by reload, and a reload shows one frame at a time. A contact sheet
shows the whole run at once, which is the only way to see that the elbow leaves
before the shoulder does or that the hand pops while it is over open paper.

    python3 scripts/preview_contact.py [dir] [--frames 24] [--sheet out.png]

PIL turns counter-clockwise and CSS turns clockwise. The rig stores the CSS
sense, because the page is what ships; every rotate() below negates. The whole
convention, and the three sign errors that paid for writing it down, are in
docs/solutions/zero-is-down-and-it-turns-the-other-way.md.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PAPER = (247, 246, 243, 255)


def smooth(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def span(t: float, a: float, b: float) -> float:
    """How far through the window [a, b] the loop is, eased."""
    return smooth((t - a) / (b - a)) if b > a else 0.0


def pose(t: float, rig: dict) -> dict:
    """The whole loop, as numbers, read from the rig's own timeline.

    The windows are not written here. They are in rig.json, because the page
    plays the same loop and a timeline written down twice is a timeline that
    drifts: the contact sheet would stop being evidence about what ships.
    """
    rest, greet = rig["pose"]["rest"], rig["pose"]["greet"]
    T = rig["timing"]

    def swing(name: str) -> float:
        a, b, c, d = T[name]
        return span(t, a, b) - span(t, c, d)

    notice, rise = swing("notice"), swing("rise")
    sh, el, wr = swing("shoulder"), swing("elbow"), swing("wrist")

    # Two wags at the top, damped, and only while the arm is actually up.
    wag = 0.0
    w0, w1 = T["wag"]
    if w0 < t < w1:
        k = (t - w0) / (w1 - w0)
        wag = math.sin(k * math.pi * 2.4) * rig["wag_deg"] * (1 - k) ** 0.7

    def lerp(a, b, k):
        return a + (b - a) * k

    s0, s1 = T["shaka"]
    return {
        "rise": rise * rig["rise"],
        "head_deg": lerp(6.5, 0.0, notice),
        "head_dy": lerp(7.0, 0.0, notice),
        "eye_dy": lerp(3.0, 0.0, notice),
        "shoulder": lerp(rest["shoulder"], greet["shoulder"], sh),
        "elbow": lerp(rest["elbow"], greet["elbow"], el) + wag,
        "wrist": lerp(rest["wrist"], greet["wrist"], wr) + wag * 0.6,
        "shaka": s0 < t < s1,
    }


def wrist_y(p: dict, rig: dict) -> float:
    """Where the wrist actually is, so a hand can be swapped out of sight.

    A gesture that appears while the hand is over open paper is a pop. The two
    swaps have to happen behind the desk, and the only way to know they do is to
    work out where the hand is rather than to trust the numbers in the timeline.
    """
    stage = rig["stage"]
    sx = rig["shoulder"][0] / 100 * stage[0]
    sy = rig["shoulder"][1] / 100 * stage[1]
    ex = rig["elbow"][0] / 100 * stage[0] - sx
    ey = rig["elbow"][1] / 100 * stage[1] - sy
    wx = rig["wrist"][0] / 100 * stage[0] - sx
    wy = rig["wrist"][1] / 100 * stage[1] - sy

    def spin(x, y, deg):
        r = math.radians(deg)
        return x * math.cos(r) - y * math.sin(r), x * math.sin(r) + y * math.cos(r)

    fx, fy = spin(wx - ex, wy - ey, p["elbow"])
    ax, ay = spin(ex + fx, ey + fy, p["shoulder"])
    return sy + ay - p["rise"]


def turn(img: Image.Image, deg: float, pivot_pct, stage) -> Image.Image:
    if abs(deg) < 0.01:
        return img
    cx = pivot_pct[0] / 100 * stage[0]
    cy = pivot_pct[1] / 100 * stage[1]
    return img.rotate(-deg, resample=Image.BICUBIC, center=(cx, cy))


def frame(t: float, L: dict, rig: dict) -> Image.Image:
    stage = tuple(rig["stage"])
    p = pose(t, rig)
    out = Image.new("RGBA", stage, PAPER)

    head = turn(L["head"], p["head_deg"], rig["neck"], stage)
    head = head.transform(stage, Image.AFFINE, (1, 0, 0, 0, 1, -p["head_dy"]),
                          resample=Image.BICUBIC)
    eyes = turn(L["eyes"], p["head_deg"], rig["neck"], stage)
    eyes = eyes.transform(stage, Image.AFFINE,
                          (1, 0, 0, 0, 1, -p["head_dy"] - p["eye_dy"]),
                          resample=Image.BICUBIC)
    body = Image.new("RGBA", stage, (0, 0, 0, 0))
    body.alpha_composite(L["torso"])
    body.alpha_composite(head)
    body.alpha_composite(eyes)

    arm = Image.new("RGBA", stage, (0, 0, 0, 0))
    hand = L["hand-shaka"] if p["shaka"] else L["hand-rest"]
    hand = turn(hand, p["wrist"], rig["wrist"], stage)
    fore = Image.new("RGBA", stage, (0, 0, 0, 0))
    fore.alpha_composite(L["arm-fore"])
    fore.alpha_composite(hand)
    fore = turn(fore, p["elbow"], rig["elbow"], stage)
    arm.alpha_composite(L["arm-upper"])
    arm.alpha_composite(fore)
    arm = turn(arm, p["shoulder"], rig["shoulder"], stage)

    figure = Image.new("RGBA", stage, (0, 0, 0, 0))
    figure.alpha_composite(arm)
    figure.alpha_composite(body)
    figure = figure.transform(stage, Image.AFFINE, (1, 0, 0, 0, 1, p["rise"]),
                              resample=Image.BICUBIC)

    out.alpha_composite(figure)
    out.alpha_composite(L["desk"])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", nargs="?",
                    default=str(ROOT / "briefs/contact-greeting/approved/v2"))
    ap.add_argument("--frames", type=int, default=24)
    ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--sheet", default="/tmp/contact-sheet.png")
    ap.add_argument("--scale", type=float, default=0.32)
    a = ap.parse_args()

    d = Path(a.dir)
    rig = json.loads((d / "rig.json").read_text())
    names = ["desk", "torso", "head", "eyes", "arm-upper", "arm-fore",
             "hand-rest", "hand-shaka"]
    L = {n: Image.open(d / f"{n}.png").convert("RGBA") for n in names}

    frames = [frame(i / a.frames, L, rig) for i in range(a.frames)]
    w = round(frames[0].width * a.scale)
    h = round(frames[0].height * a.scale)
    rows = math.ceil(len(frames) / a.cols)
    sheet = Image.new("RGB", (w * a.cols, h * rows), (255, 255, 255))
    for i, f in enumerate(frames):
        sheet.paste(f.convert("RGB").resize((w, h), Image.LANCZOS),
                    ((i % a.cols) * w, (i // a.cols) * h))
    sheet.save(a.sheet)
    print(f"preview_contact: {len(frames)} frames to {a.sheet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
