#!/usr/bin/env python3
"""Build the version-history sheet for a brief.

Exists because the lineage of an asset is the interesting part of it. The
frames are given in order on the command line, and the last one is marked as
the one that was approved.

    python3 scripts/contact_sheet.py OUT.png A.png B.png C.png ...
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAPER = (247, 246, 243)
TILE = (255, 255, 255)
EDGE = (214, 211, 203)
INK = (22, 22, 26)
GREEN = (62, 142, 90)
FONTS = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
         "/System/Library/Fonts/Helvetica.ttc"]


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONTS:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("out", type=Path)
    ap.add_argument("frames", nargs="+", type=Path)
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--cell", type=int, default=620)
    ap.add_argument("--pad", type=int, default=30)
    ap.add_argument("--radius", type=int, default=26)
    args = ap.parse_args()

    for f in args.frames:
        if not f.is_file():
            raise SystemExit(f"no such frame: {f}")

    cols = args.cols
    rows = (len(args.frames) + cols - 1) // cols
    cell, pad, rad = args.cell, args.pad, args.radius
    sheet = Image.new("RGB", (cols*cell + (cols+1)*pad, rows*cell + (rows+1)*pad), PAPER)
    draw = ImageDraw.Draw(sheet)
    font = load_font(round(cell * 0.072))

    for i, path in enumerate(args.frames):
        last = i == len(args.frames) - 1
        x = pad + (i % cols)*(cell + pad)
        y = pad + (i // cols)*(cell + pad)

        im = Image.open(path).convert("RGB")
        s = min(cell/im.width, cell/im.height)
        im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)

        tile = Image.new("RGB", (cell, cell), TILE)
        tile.paste(im, ((cell-im.width)//2, (cell-im.height)//2))

        # Round the corners by pasting the tile through a rounded mask, so the
        # paper shows through instead of the corner being painted over it.
        mask = Image.new("L", (cell, cell), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, cell-1, cell-1], rad, fill=255)
        sheet.paste(tile, (x, y), mask)

        colour = GREEN if last else EDGE
        width = 6 if last else 2
        draw.rounded_rectangle([x, y, x+cell-1, y+cell-1], rad,
                               outline=colour, width=width)

        # The badge sits inside the frame so it survives a thumbnail, but small
        # enough to clear the artwork: at the first size it tried, it landed on
        # the character's head in the last frame.
        b = round(cell * 0.098)
        m = round(cell * 0.026)
        draw.rounded_rectangle([x+m, y+m, x+m+b, y+m+b], round(b*0.32),
                               fill=GREEN if last else INK)
        label = str(i + 1)
        box = draw.textbbox((0, 0), label, font=font)
        draw.text((x+m+(b-(box[2]-box[0]))/2 - box[0],
                   y+m+(b-(box[3]-box[1]))/2 - box[1]),
                  label, font=font, fill=PAPER)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.out)
    print(f"{len(args.frames)} frames, {cols}x{rows}, {sheet.size} -> {args.out}")


if __name__ == "__main__":
    main()
