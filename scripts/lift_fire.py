#!/usr/bin/env python3
"""Lift the flames out of a burning scene, by colour.

The strip needs the fire as its own layer so it can flicker and then collapse
into the accent rule that carries into the project grid. Three finished panels
could only be cross-faded, and a cross-fade is not one thing becoming another.

Separating it is mechanical here, and that is not luck. Every colour in
docs/ILLUSTRATION_SPEC.md is cool and muted except the two warm ones used by
code on screens, and briefs/strip-scene/brief.md forbids a lit screen in this
scene for exactly this reason. So in this drawing, warm means fire. There is
nothing to judge and nothing to select by hand, which is the rule in CLAUDE.md
about never proposing manual work, arriving as a consequence rather than as
discipline.

What it does not do: invent. A flame the model drew as scattered specks stays
scattered, and the acceptance criteria in the brief exist to reject that drawing
rather than to repair it here.

    python3 scripts/lift_fire.py <burning.png> <fire.png>
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "docs" / "ILLUSTRATION_SPEC.md"

# The two warm tokens. Named by what they are used for here rather than by their
# name in the spec, which calls them code colours.
WARM = ("CODE-B", "CODE-D")


def spec_tokens() -> dict[str, tuple[int, int, int]]:
    """Every token in the spec, read at run time so the two cannot drift."""
    out: dict[str, tuple[int, int, int]] = {}
    for name, hexv in re.findall(r"\|\s*`([A-Z][A-Z0-9-]*)`\s*\|\s*`#([0-9A-Fa-f]{6})`",
                                 SPEC.read_text(encoding="utf-8")):
        out[name] = tuple(int(hexv[i:i + 2], 16) for i in (0, 2, 4))
    if not out:
        raise SystemExit(f"no colour tokens found in {SPEC}")
    return out


def lift(src: Path, min_area: int = 400) -> tuple[np.ndarray, dict]:
    im = Image.open(src).convert("RGBA")
    a = np.array(im)
    rgb = a[..., :3].astype(int)

    tokens = spec_tokens()
    missing = [n for n in WARM if n not in tokens]
    if missing:
        raise SystemExit(f"the spec no longer defines {missing}; fire has no colour")

    names = list(tokens)
    d = np.stack([np.abs(rgb - np.array(tokens[n])).sum(-1) for n in names], -1)
    nearest = np.array(names)[np.argmin(d, -1)]
    warm = np.isin(nearest, WARM)

    # Anti-aliased edges between a flame and the paper land halfway and read as
    # neither. Closing pulls them in, so the lifted flame keeps its own outline
    # instead of a chewed one.
    m = cv2.morphologyEx(warm.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    # Specks are not fire. A drawing whose flames come apart into crumbs fails
    # its brief; dropping the crumbs here only stops them floating in the panel.
    n, comp, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros_like(m, bool)
    dropped = 0
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            keep |= comp == i
        else:
            dropped += int(stats[i, cv2.CC_STAT_AREA])

    out = a.copy()
    out[..., 3] = np.where(keep, 255, 0)
    ys = np.flatnonzero(keep.any(1))
    xs = np.flatnonzero(keep.any(0))
    report = {
        "flame_px": int(keep.sum()),
        "dropped_px": dropped,
        "pieces": int(sum(1 for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] >= min_area)),
        "box": [int(xs[0]), int(ys[0]), int(xs[-1]), int(ys[-1])] if ys.size else None,
    }
    return out, report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("src", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--min-area", type=int, default=400)
    args = ap.parse_args()

    out, report = lift(args.src.resolve(), args.min_area)
    if not report["flame_px"]:
        raise SystemExit(
            "no warm pixels found. Either the drawing has no fire in it, or the "
            "flames were drawn in a colour the spec does not define."
        )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(out).save(args.out)
    print(f"fire: {report['flame_px']}px in {report['pieces']} piece(s), "
          f"{report['dropped_px']}px of specks dropped, box {report['box']}")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
