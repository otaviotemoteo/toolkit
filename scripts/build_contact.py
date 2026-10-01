#!/usr/bin/env python3
"""Assemble the contact greeting: a looping puppet cut from the approved hero.

The first version of this asset generated a new person and got a competent
stranger: different face, different line, different trousers. Identity is the
whole point of an asset that sits at the foot of a portfolio, so nothing here
generates a person. The figure is the approved character himself, cut up, and
the monitors are the approved hero's own monitors with their screens filled in
so they read from behind. Only the arm is new, and it is drawn rather than
generated, because a limb in this style is a tapered capsule and a capsule is
something a script can lay down exactly on the character's own palette.

    python3 scripts/build_contact.py [outdir]

What comes out, all of them the size of the stage so the page can stack them
with no arithmetic of its own:

    desk.png        the workstation, drawn last, and the occluder
    torso.png       the character from the neck down, left sleeve removed
    head.png        everything above the neck, eyes lifted off
    eyes.png        the two ovals alone
    arm-upper.png   shoulder to elbow, with the sleeve that hides the joint
    arm-fore.png    elbow to wrist
    hand-rest.png   a relaxed hand
    hand-shaka.png  thumb and little finger out
    rig.json        pivots, poses and the desk line

The lessons this file exists because of, all three of them paid for here:
docs/solutions/the-second-drawing-is-a-different-person.md (why nothing below is
generated), docs/solutions/a-layer-holds-only-the-pose-it-was-drawn-in.md (why
the arm is drawn waving rather than at rest) and
docs/solutions/zero-is-down-and-it-turns-the-other-way.md (the angle convention
every function here obeys).

Why the sleeve travels with the arm: two raster layers cannot share a pixel, so
the sleeve belongs to whichever one turns. The torso is cut back to the armhole
and given a round white shoulder underneath, and since both the cap and the
sleeve are the shirt's white, the seam cannot be seen at any angle. See
docs/solutions/two-raster-layers-cannot-share-a-pixel.md.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
HERO = ROOT / "briefs/hero-character/approved"
CUTOUT = HERO / "hero-character-v2-cutout.png"
SCENE = HERO / "scene"
PLATE = SCENE / "plate.png"

# The stage. 1.4:1, which is what the contact block gives the illustration.
STAGE = (940, 680)
DESK_Y = 560          # the desk's top edge; everything below it is hidden
MONITOR_SCALE = 0.9   # close to the plate's own resolution, so nothing is upscaled
# One in the middle, which is what he sits behind, and one on the right to fill
# the desk out. The paper to the left of the middle one is where the arm goes.
MONITOR_X = (410, 755)
SS = 3                # supersampling for everything this script draws

# Sampled from the approved character and the approved plate, never invented.
SKIN = (252, 184, 148, 255)
SKIN_LINE = (240, 138, 100, 255)   # the darker peach the drawing uses for creases
SHIRT = (251, 251, 251, 255)
BEZEL = (32, 35, 43, 255)
BEZEL_BACK = (44, 48, 58, 255)     # the slight bulge on a monitor's back panel
WOOD = (176, 96, 58, 255)
WOOD_EDGE = (150, 78, 45, 255)

# The character, in the cutout's own 370x1173 pixels.
# The character and the monitors come out of the same approved drawing, so how
# big he is next to them is a measurement rather than a choice: the hero scene
# places him at 0.868 against a plate drawn at 1.0. The first version of this
# asset used 1.25 against monitors at 0.62, twice the right size, and a man
# twice the height of his own monitor reads as a collage rather than a room.
HERO_RATIO = 0.868
CHAR_SCALE = HERO_RATIO * MONITOR_SCALE
CHAR_X = 245          # where the cutout's left edge lands on the stage
REST_Y = 224          # where its top edge lands while he is working
RISE = 158            # how far up he comes, in stage pixels
# Where the hand ends up, in stage pixels, with him already risen. The pose is
# solved from this rather than guessed at in degrees: a target is something that
# can be checked against the monitor it must not disappear behind, and a pair of
# angles is not. It is out to the side rather than next to his ear, because the
# shoulder sits only just clear of the monitor and a hand held by the ear folds
# the elbow to a hundred and thirty degrees to get there.
GREET_WRIST = (215, 195)

# The loop, as windows into it: [leaving, arrived, starting back, home]. It lives
# in the rig because two things play it, the preview here and the page, and a
# timeline written down twice is a timeline that drifts. A frame judged on a
# contact sheet is only the frame that ships if both read the same numbers.
#
# The windows overlap on purpose. He notices before he rises, the elbow folds
# before the shoulder opens and unfolds after it, and the body starts back down
# while the arm is still coming in. Nothing begins only once something else has
# finished, which is the difference between an animation and a list of moves.
# The body does finish rising before the arm starts, and that one is not taste:
# the shoulder is behind the monitor until he is up, and an arm whose shoulder
# cannot be seen reads as an arm lying on the desk by itself.
TIMING = {
    "notice": [0.12, 0.20, 0.82, 0.92],
    "rise": [0.18, 0.36, 0.80, 0.95],
    "elbow": [0.36, 0.58, 0.78, 0.94],
    "shoulder": [0.38, 0.60, 0.76, 0.91],
    "wrist": [0.42, 0.64, 0.78, 0.93],
    "wag": [0.66, 0.82],
    # Both ends of this one are checked against the arm's own geometry rather
    # than chosen: preview_contact.py prints how far the wrist is below the desk
    # at each swap, and a gesture that appears over open paper is a pop.
    "shaka": [0.26, 0.90],
}

NECK = 238            # the row split_layers cut the head at
SHOULDER = (88, 300)  # the joint the arm turns about, in character pixels
ARMHOLE = ((100, 262), (66, 470))  # the seam the torso is cut back to
SLEEVE_HEM = 396      # the row below which the approved drawing is all arms

SLEEVE_LEN = 104      # down the arm from the shoulder, in character pixels
UPPER_LEN = 155
FORE_LEN = 140
W_SHOULDER = 78
W_HEM = 68
W_ELBOW = 56
W_WRIST = 46


# ── small drawing helpers ────────────────────────────────────────────────────
# Everything is drawn at SS times the final size and reduced at the end, which
# is the whole of the anti-aliasing strategy. The character's own art has no
# outline, so neither does anything here: shapes are laid down flat and the only
# darker marks are the creases the drawing itself uses.

def _canvas() -> Image.Image:
    return Image.new("RGBA", (STAGE[0] * SS, STAGE[1] * SS), (0, 0, 0, 0))


def taper(d: ImageDraw.ImageDraw, p0, p1, w0, w1, fill) -> None:
    """A limb: a quad between two circles, so the joint stays filled when it bends."""
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    n = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / n, dx / n
    d.polygon([
        (x0 + nx * w0 / 2, y0 + ny * w0 / 2), (x1 + nx * w1 / 2, y1 + ny * w1 / 2),
        (x1 - nx * w1 / 2, y1 - ny * w1 / 2), (x0 - nx * w0 / 2, y0 - ny * w0 / 2),
    ], fill=fill)
    for (x, y), w in ((p0, w0), (p1, w1)):
        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=fill)


def band(d: ImageDraw.ImageDraw, p, deg, width, thickness, fill) -> None:
    """A stripe across a limb. A short `taper` would be a disc: it caps its ends."""
    a = _along(p, deg, -thickness / 2)
    b = _along(p, deg, thickness / 2)
    r = math.radians(deg)
    nx, ny = math.cos(r), math.sin(r)
    d.polygon([(a[0] + nx * width / 2, a[1] + ny * width / 2),
               (b[0] + nx * width / 2, b[1] + ny * width / 2),
               (b[0] - nx * width / 2, b[1] - ny * width / 2),
               (a[0] - nx * width / 2, a[1] - ny * width / 2)], fill=fill)


def reduce(img: Image.Image) -> Image.Image:
    return img.resize(STAGE, Image.LANCZOS)


def char_to_stage(x: float, y: float, top: float = REST_Y) -> tuple[float, float]:
    return CHAR_X + x * CHAR_SCALE, top + y * CHAR_SCALE


def place(layer: Image.Image, img: Image.Image, x: float, y: float) -> None:
    layer.alpha_composite(img, (round(x), round(y)))


# ── the workstation ──────────────────────────────────────────────────────────

def monitor_back() -> Image.Image:
    """The hero's own monitor with its screen filled in, so it reads from behind.

    Drawing a monitor from scratch would have been quicker and would not have
    matched: the bezel's corner radius, the neck's taper and the base's ellipse
    are all decisions already taken in the approved art. Filling the screen is
    the smallest edit that turns a front into a back.
    """
    plate = Image.open(PLATE).convert("RGBA")
    # One monitor with its stand. The crop stops at 259 on purpose: below that
    # the plate has the keyboard, and a keyboard seen from above cannot be in a
    # picture taken from behind the desk.
    mon = plate.crop((49, 24, 331, 259))
    a = np.array(mon).astype(int)
    opaque = a[..., 3] > 128

    # The screen is the large light-ish region inside the bezel. Filling every
    # pixel that is not already bezel-dark, inside the bezel's own rows, leaves
    # the silhouette untouched and removes the picture.
    dark = opaque & (a[..., 0] < 90) & (a[..., 1] < 95) & (a[..., 2] < 110)
    ys = np.where(dark.any(axis=1))[0]
    screen_rows = slice(ys.min(), ys.min() + int((ys.max() - ys.min()) * 0.72))
    region = opaque.copy()
    region[: screen_rows.start] = False
    region[screen_rows.stop:] = False
    a[region] = BEZEL
    back = Image.fromarray(a.astype(np.uint8), "RGBA")

    # One flat bulge, the only thing a back has that a front does not.
    d = ImageDraw.Draw(back)
    x0, x1 = 0.22 * back.width, 0.78 * back.width
    y0, y1 = ys.min() + 0.16 * (ys.max() - ys.min()), ys.min() + 0.70 * (ys.max() - ys.min())
    d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=BEZEL_BACK)
    return back


def workstation() -> Image.Image:
    """Desk and monitors, drawn over everything, opaque to the bottom edge."""
    layer = _canvas()
    d = ImageDraw.Draw(layer)
    w, h = STAGE[0] * SS, STAGE[1] * SS
    top = DESK_Y * SS

    # A flat panel rather than the hero's three-quarter view, because this is the
    # far side of the same desk and the far side shows no top surface.
    d.rectangle([0, top + 22 * SS, w, h], fill=WOOD)
    d.rectangle([0, top, w, top + 22 * SS], fill=WOOD_EDGE)

    mon = monitor_back()
    mw = round(mon.width * MONITOR_SCALE * SS)
    mh = round(mon.height * MONITOR_SCALE * SS)
    mon = mon.resize((mw, mh), Image.LANCZOS)
    for cx in MONITOR_X:
        place(layer, mon, cx * SS - mw / 2, top - mh + 5 * SS)

    return reduce(layer)


# ── the character ────────────────────────────────────────────────────────────

def _shirt_below(img: Image.Image) -> Image.Image:
    """Replace everything under the sleeve hem with a plain t-shirt.

    The approved drawing has his arms crossed, and they cannot stay. At the
    hero's own scale a seated man's forearms sit below the top of his own
    monitor, which is true of every desk anyone has worked at, so no height of
    desk and no amount of rise hides them: they show through the gap beside the
    monitor's stand. And a pair of crossed forearms behind a man who is waving
    is a man with three arms.

    So below the sleeve hem the torso becomes what a t-shirt is: one flat shape,
    wide at the sleeve caps and narrowing to the waist. It carries no arms at
    all. Both of his real ones are accounted for: the one that waves is its own
    layer, and the other is where a working man's other hand is, under the desk.
    """
    a = np.array(img)
    rows = np.arange(a.shape[0])
    cols = np.arange(a.shape[1])[None, :]
    # Two anchors and a straight taper between them. The upper one is the
    # silhouette at the hem, so the shape leaves the sleeves without a step.
    t = np.clip((rows - SLEEVE_HEM) / 74.0, 0, 1)
    left = 14 + (58 - 14) * t
    right = 336 + (296 - 336) * t
    band = rows >= SLEEVE_HEM

    a[band] = 0
    inside = band[:, None] & (cols >= left[:, None]) & (cols <= right[:, None])
    a[inside] = SHIRT
    return Image.fromarray(a, "RGBA")


def _armhole_cut(img: Image.Image) -> Image.Image:
    """Erase the sleeve the arm layer is about to own, and round off what is left."""
    a = np.array(img)
    (ax, ay), (bx, by) = ARMHOLE
    rows = np.arange(a.shape[0])
    t = np.clip((rows - ay) / (by - ay), 0, 1)
    seam = ax + (bx - ax) * t
    band = (rows >= ay - 40) & (rows <= by)
    cols = np.arange(a.shape[1])[None, :]
    mask = band[:, None] & (cols < seam[:, None])
    a[mask] = 0
    out = Image.fromarray(a, "RGBA")

    # A white shoulder under the sleeve, so no angle can open a gap. Both are the
    # shirt's white, so the join is invisible rather than merely hidden.
    d = ImageDraw.Draw(out)
    sx, sy = SHOULDER
    r = W_SHOULDER * 0.52
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=SHIRT)
    return out


def figure() -> tuple[Image.Image, Image.Image, Image.Image]:
    """torso, head, eyes, each on a stage-sized transparent layer."""
    head_src = Image.open(SCENE / "head.png").convert("RGBA")
    eyes_src = Image.open(SCENE / "eyes.png").convert("RGBA")
    body_src = Image.open(SCENE / "body.png").convert("RGBA")   # rows NECK..

    full = Image.new("RGBA", (370, 1173), (0, 0, 0, 0))
    full.alpha_composite(body_src, (0, NECK))
    torso_src = _armhole_cut(_shirt_below(full))

    def lay(src: Image.Image, char_y: int) -> Image.Image:
        layer = Image.new("RGBA", STAGE, (0, 0, 0, 0))
        w = round(src.width * CHAR_SCALE)
        h = round(src.height * CHAR_SCALE)
        place(layer, src.resize((w, h), Image.LANCZOS), *char_to_stage(0, char_y))
        return layer

    return lay(torso_src, 0), lay(head_src, 0), lay(eyes_src, 0)


# ── the arm ──────────────────────────────────────────────────────────────────
# Each segment is drawn in the greeting pose rather than hanging down, and the
# rig's angles are deltas from it. Drawn hanging down, the forearm and the hand
# fall off the bottom of the stage and are lost: a layer cannot store pixels it
# does not have room for, and a rotation cannot bring back what was never
# rasterised. The pose that has to be on canvas is the one that is seen.


def _greet_frame() -> dict:
    """Where every joint sits in the drawn pose, in stage pixels."""
    a1, rel, _ = solve(GREET_WRIST)
    a2 = a1 + rel
    s = CHAR_SCALE
    sx, sy = char_to_stage(*SHOULDER)          # the layer frame, before he rises
    ex, ey = _along((sx, sy), a1, UPPER_LEN * s)
    wx, wy = _along((ex, ey), a2, FORE_LEN * s)
    return {"a1": a1, "a2": a2, "rel": rel,
            "shoulder": (sx, sy), "elbow": (ex, ey), "wrist": (wx, wy)}


def _along(p, deg, dist):
    """A point `dist` away from `p` in the direction `deg`.

    Zero is straight down and the angle grows clockwise, which is what CSS
    rotate() does. A y-down coordinate system turns that into (-sin, +cos), and
    getting it backwards is not a small error: it is the arm reaching for the
    ceiling instead of the floor, which is exactly what the first build did.
    """
    r = math.radians(deg)
    return p[0] - math.sin(r) * dist, p[1] + math.cos(r) * dist


def arm_upper() -> Image.Image:
    layer = _canvas()
    d = ImageDraw.Draw(layer)
    f = _greet_frame()
    s = CHAR_SCALE * SS
    S = tuple(v * SS for v in f["shoulder"])
    hem = _along(S, f["a1"], SLEEVE_LEN * s)
    elbow = tuple(v * SS for v in f["elbow"])

    taper(d, S, hem, W_SHOULDER * s, W_HEM * s, SHIRT)
    taper(d, _along(S, f["a1"], (SLEEVE_LEN - 6) * s), elbow,
          W_HEM * 0.93 * s, W_ELBOW * s, SKIN)
    # The band of skin the sleeve's edge sits on. The approved drawing has one on
    # both arms; without it the sleeve floats.
    band(d, _along(S, f["a1"], (SLEEVE_LEN - 1) * s), f["a1"],
         W_HEM * 0.92 * s, 7 * s, SKIN_LINE)
    return reduce(layer)


def arm_fore() -> Image.Image:
    layer = _canvas()
    d = ImageDraw.Draw(layer)
    f = _greet_frame()
    s = CHAR_SCALE * SS
    taper(d, tuple(v * SS for v in f["elbow"]), tuple(v * SS for v in f["wrist"]),
          W_ELBOW * s, W_WRIST * s, SKIN)
    return reduce(layer)


def _hand(shaka: bool) -> Image.Image:
    """The hand, drawn upright in its own frame and then turned onto the wrist.

    Drawing it directly in stage coordinates meant reasoning about a gesture
    through two angles at once, and what came out was a pointing finger twice
    running. Here the hand is drawn hanging straight down from a wrist at the
    origin, where left is left, and the only rotation is the one that puts it on
    the end of the forearm.

    Units are the wrist's own width, so the drawing is the same shape whatever
    the character is scaled to.
    """
    f = _greet_frame()
    w = W_WRIST * CHAR_SCALE * SS
    pad = 3.0                                   # room for the digits, in w
    local = Image.new("RGBA", (round(w * pad * 2),) * 2, (0, 0, 0, 0))
    origin = (local.width / 2, local.height / 2 - w * pad * 0.55)
    d = ImageDraw.Draw(local)

    def at(u, v):
        return origin[0] + u * w, origin[1] + v * w

    def box(u0, v0, u1, v1, r):
        d.rounded_rectangle([*at(u0, v0), *at(u1, v1)], radius=r * w, fill=SKIN)

    def crease(v, u0=-0.26, u1=0.24):
        d.line([at(u0, v), at(u1, v - 0.05)], fill=SKIN_LINE,
               width=max(1, int(w * 0.06)))

    if shaka:
        box(-0.60, 0.02, 0.60, 1.24, 0.44)
        taper(d, at(-0.40, 0.42), at(-1.24, 1.06), w * 0.40, w * 0.30, SKIN)
        taper(d, at(0.42, 0.68), at(1.18, 1.38), w * 0.34, w * 0.26, SKIN)
        crease(0.46)
        crease(0.74)
    else:
        box(-0.54, 0.0, 0.54, 1.00, 0.46)
        crease(0.36, -0.22, 0.22)
        crease(0.60, -0.22, 0.22)

    # Turn it onto the forearm. PIL turns the other way, hence the sign.
    local = local.rotate(-f["a2"], resample=Image.BICUBIC, center=origin)

    layer = _canvas()
    wx, wy = (v * SS for v in f["wrist"])
    layer.alpha_composite(local, (round(wx - origin[0]), round(wy - origin[1])))
    return reduce(layer)


def hand_rest() -> Image.Image:
    return _hand(False)


def hand_shaka() -> Image.Image:
    return _hand(True)


# ── the rig ──────────────────────────────────────────────────────────────────

def solve(target: tuple[float, float]) -> tuple[float, float, tuple[float, float]]:
    """Shoulder and elbow angles that put the wrist on `target`, plus the elbow.

    Two links and a point is a triangle, so this is the law of cosines and not
    an optimiser. Both solutions are computed and the one whose elbow sits
    further from the body is kept: the other reaches the same point with the
    whole arm thrown over his head, which is a different gesture, a worse one,
    and one that buries the elbow behind a monitor.

    Degrees are measured from straight down and grow clockwise, the sense CSS
    rotates in and therefore the only sense worth storing.
    """
    sx, sy = char_to_stage(*SHOULDER, top=REST_Y - RISE)
    l1, l2 = UPPER_LEN * CHAR_SCALE, FORE_LEN * CHAR_SCALE
    dx, dy = target[0] - sx, target[1] - sy
    reach = math.hypot(dx, dy)
    reach = min(max(reach, abs(l1 - l2) + 1e-6), l1 + l2 - 1e-6)
    base = math.degrees(math.atan2(-dx, dy))
    alpha = math.degrees(math.acos((l1 * l1 + reach * reach - l2 * l2) / (2 * l1 * reach)))

    best = None
    for shoulder in (base + alpha, base - alpha):
        shoulder = (shoulder + 180) % 360 - 180
        ex, ey = _along((sx, sy), shoulder, l1)
        fore_abs = math.degrees(math.atan2(-(target[0] - ex), target[1] - ey))
        elbow = (fore_abs - shoulder + 180) % 360 - 180
        if best is None or ex < best[2][0]:
            best = (shoulder, elbow, (ex, ey))
    return best


def rig() -> dict:
    nx, ny = char_to_stage(178, NECK)   # the hero's own head pivot
    f = _greet_frame()

    def pct(p):
        return [round(p[0] / STAGE[0] * 100, 3), round(p[1] / STAGE[1] * 100, 3)]

    # Deltas from the drawn pose, so the greeting is zero and costs nothing.
    return {
        "stage": list(STAGE),
        "desk_y": DESK_Y,
        "rise": RISE,
        "neck": pct((nx, ny)),
        "shoulder": pct(f["shoulder"]),
        "elbow": pct(f["elbow"]),
        "wrist": pct(f["wrist"]),
        "pose": {
            "rest": {"shoulder": round(4.0 - f["a1"], 2),
                     "elbow": round(2.0 - f["rel"], 2),
                     "wrist": 10.0},
            "greet": {"shoulder": 0.0, "elbow": 0.0, "wrist": 0.0},
        },
        "wag_deg": 7,
        "timing": TIMING,
    }


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "briefs/contact-greeting/approved/v2"
    out.mkdir(parents=True, exist_ok=True)

    torso, head, eyes = figure()
    layers = {
        "desk.png": workstation(),
        "torso.png": torso,
        "head.png": head,
        "eyes.png": eyes,
        "arm-upper.png": arm_upper(),
        "arm-fore.png": arm_fore(),
        "hand-rest.png": hand_rest(),
        "hand-shaka.png": hand_shaka(),
    }
    for name, img in layers.items():
        img.save(out / name)
    (out / "rig.json").write_text(json.dumps(rig(), indent=2) + "\n", encoding="utf-8")

    print(f"build_contact: wrote {len(layers)} layers and rig.json to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
