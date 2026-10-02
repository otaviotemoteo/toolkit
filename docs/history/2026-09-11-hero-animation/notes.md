# 2026-09-11, the hero animation

The round that took the hero from an approved still to a hero that moves, with
no generation in the motion at all.

## What it was asking

Whether a flat illustration can be cut into layers and animated by transform,
and whether the seam survives inspection.

## What it produced

| File | What it shows |
|---|---|
| `01`, `02`, `03` | the composed hero at three states, rendered from the same four files |
| `04` | the collar at rest and at maximum lean, four times zoom. The test that mattered |
| `05`, `06` | the desk, first and second generation |
| `07` | the desk with its drop shadow removed mechanically rather than re-generated |

## What it settled

**Four seam faults, none visible at full-figure scale.** A ghosted jaw from
overlapping layers sharing pixels; a duplicated collar from a tab that reached
too far; a step across the neck from translating the head; a hairline where the
tab stopped abruptly. Each was found only by looking at the collar at four times
zoom, and each is written up.

**The two-bone neck came out.** It is the right rig for parts drawn separately
and the wrong one for parts cut from a single drawing.

**Correction beat re-generation.** The desk's drop shadow survived two rounds of
prompting, because nothing in a positive prompt reliably prevents a generator
from drawing a shadow, and the backend in use discards negative prompts
entirely. It was removed afterwards in one pass, deterministically.

**Two thresholds had to be found rather than chosen.** The artwork threshold for
shadow removal, picked by hand at first and wrong in a way that reported
success; and the neck, which is measured from the alpha mask rather than typed.

## What shipped

The desk cropped from the approved scene, not the generated one, because it and
the character came from the same image. The generated desk is kept as proof the
brief works.
