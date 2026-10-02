# 2026-09-07, hero character, first pass

Thirteen frames, one afternoon, everything generated locally except the last.
This is the round that took the project from a written spec to an approved
asset, and it changed the spec three times on the way.

## What the round was asking

Whether a visual system written in a file could survive contact with a
generator, and what it costs to make it obey.

## Frame by frame

| # | What it settled |
|---|---|
| 01 | technical probe: the local stack runs at all. **File lost** |
| 02 | first real generation against the spec: ink line on a chroma key ground |
| 03 | the same drawing keyed off its background by luminance, on paper |
| 04 | first colour, by img2img at low influence. Identity drifted |
| 05 | 512 draft: the colour corrections landed, everything else drifted |
| 06 | 1024 at higher influence: identity held, the corrections did not land |
| 07 | 512 from noise: colours landed, composition re-rolled |
| 08 | 1024 from noise: every colour right, framing cropped |
| 09 | **the turn.** ControlNet backend, style collapsed to flat, and Otávio approved it |
| 10 | control at 0.85: layout right, and a ghost of the control drawing behind him |
| 11 | position removed from the prompt: ghost gone, figure back in the centre |
| 12 | position restored: figure moved left, desk still running behind him |
| 13 | desk described by size rather than by his position: **approved as v1** |

## What changed in the repo because of this round

- The visual system was rewritten three times. Monochrome technical drawing,
  then hand-drawn ink with flat colour, then flat forms with a fine grain. Each
  change came from an image showing the spec was wrong, not the other way round.
- Chroma key was abandoned, then luminance key was abandoned, and
  `scripts/cutout_flat.py` replaced both.
- `scripts/check_anchors.py` was written, and failed on the next file written
  after it.
- Eleven files in `docs/solutions/`, one per lesson.
- The animation plan moved from generation to compositing.

## The number that mattered most

Peak memory during a 1024 generation: 5.69 GB on a 16 GB machine, with a browser
and Slack open, no swap. That single measurement is what made local generation a
real option rather than a nice idea.
