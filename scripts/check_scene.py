#!/usr/bin/env python3
"""A scene manifest has to describe something that exists and can be composed.

`scene.json` is the contract between this repository, which produces layered
assets, and whatever renders them. The preview page reads it; a site would read
the same file. Nothing else connects the two, so a manifest that has drifted
from the files beside it breaks the hero silently and at runtime.

The rules below are the ones that have already been got wrong here, not
invented ones. The four rebuilds behind them are written up in
docs/solutions/two-raster-layers-cannot-share-a-pixel.md.

- every file named must exist, because layers get renamed during a split
- the draw order must list every layer exactly once, because a layer missing
  from it is simply never drawn and nothing complains
- the pivot must sit inside the band of the layer that rotates about it, since
  a pivot outside its own layer swings the head around a point in mid-air
- the body must not start above the pivot, because anything static higher than
  the joint appears from behind the head as soon as it turns

    python3 scripts/check_scene.py                  # every scene in briefs/
    python3 scripts/check_scene.py <scene.json>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def problems(path: Path) -> list[tuple[str, str, str]]:
    found: list[tuple[str, str, str]] = []
    try:
        scene = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return [(f"cannot be read: {e}", "nothing can render a manifest it cannot "
                 "parse", f"fix the JSON in {path}")]

    here = path.parent
    ch = scene.get("character", {})
    layers = ch.get("layers", {})
    order = ch.get("draw_order", [])

    for name, spec in layers.items():
        f = here / spec.get("file", "")
        if not f.is_file():
            found.append((f"layer {name!r} names {spec.get('file')!r}, which is missing",
                          "the renderer requests it by name and gets a broken image",
                          f"re-run scripts/split_layers.py, or fix the name in {path.name}"))

    plate = scene.get("plate", {})
    if plate and not (here / plate.get("file", "")).is_file():
        found.append((f"the plate names {plate.get('file')!r}, which is missing",
                      "the scene behind the character would not draw",
                      f"restore it or fix the name in {path.name}"))

    if sorted(order) != sorted(layers):
        found.append((f"draw_order is {order} but the layers are {sorted(layers)}",
                      "a layer left out of the order is never drawn, and nothing "
                      "reports it: the character simply loses a part",
                      "list every layer exactly once in draw_order"))

    for joint, pivot in ch.get("pivots", {}).items():
        spec = layers.get(joint)
        if not spec:
            found.append((f"pivot {joint!r} has no layer of that name",
                          "the transform would be applied to nothing",
                          f"name a real layer, one of {sorted(layers)}"))
            continue
        top, bottom = spec["top"], spec["top"] + spec["height"]
        if not (top <= pivot[1] <= bottom):
            found.append((f"pivot {joint!r} is at y={pivot[1]}, outside its layer "
                          f"({top}..{bottom})",
                          "a layer rotating about a point outside itself swings "
                          "through the air instead of turning on a joint",
                          "move the pivot inside the layer, or re-cut the layer"))

        body = layers.get("body")
        if body and joint == "head" and body["top"] < pivot[1]:
            found.append((f"body starts at y={body['top']}, above the pivot at "
                          f"y={pivot[1]}",
                          "static pixels higher than the joint appear from behind "
                          "the head the moment it turns",
                          "cut the body at the pivot, not above it"))

    return found


def main() -> int:
    if len(sys.argv) > 1:
        scenes = [Path(sys.argv[1]).resolve()]
    else:
        scenes = sorted((ROOT / "briefs").glob("*/approved/scene/scene.json"))
    if not scenes:
        print("check_scene: no scene manifests found", file=sys.stderr)
        return 2

    failed = 0
    for path in scenes:
        found = problems(path)
        rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        if not found:
            print(f"ok    {rel}")
            continue
        failed += 1
        for what, why, fix in found:
            print(f"FAIL  {rel}")
            print(f"      what: {what}")
            print(f"      why:  {why}")
            print(f"      fix:  {fix}")

    if failed:
        print(f"\ncheck_scene: {failed} of {len(scenes)} manifests failed")
        return 1
    print(f"check_scene: {len(scenes)} manifest(s) ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
