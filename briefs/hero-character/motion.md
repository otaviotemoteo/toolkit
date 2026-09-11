# Brief: hero character, motion

Read `brief.md` first. That describes the illustration; this describes what it
does once it is on the page.

**Where it lives:** home page hero
**The idea in one sentence:** he notices you.

## This replaced a plan, and the reason matters

The first version of this brief specified generated video: route A of oil-motion,
a 3x3 sampling grid, a sprite atlas, a 240 frame budget. It was abandoned on
2026-09-07, and not because it was expensive.

It was abandoned because of a line in its own acceptance criteria: between two
adjacent states, the body, desk and monitors had to be **pixel identical**. No
generative method delivers that. Every call is a fresh sample; the face changes,
the shirt changes, the desk moves. A faster generator produces wrong frames
sooner. See `docs/solutions/pose-variation-is-not-generation.md` and
`docs/solutions/the-model-has-no-memory.md`.

So the motion is composition and runtime, not generation. Pixel identical stops
being a target and becomes a property: it is the same file underneath.

## The layers

Three, from back to front, plus the plate behind them.

| Layer | What it is | Moves |
|---|---|---|
| `plate` | desk, monitors, laptop, tower | never |
| `body` | the figure from the base of the neck down | never |
| `head` | everything above it, including the whole neck | rotates |
| `eyes` | the two dark ovals, lifted off the face | rotates with the head, then translates |

`scripts/split_layers.py` produces them from the approved cutout. The cuts are
found rather than typed: a standing figure has exactly one narrow place between
the hair and the shoulders, and measuring the width of the alpha mask row by row
locates it on any character.

The eyes are lifted onto their own layer and the face beneath them is healed by
inpainting, so what is left is a complete face rather than a face with two
holes. That is what lets the eyes travel further than the head.

## One joint, not two, and why

This brief originally specified a two-bone neck: the neck taking half the angle
about its base, the head taking the other half about the top of the neck. That
is how a puppet rig is built and it was wrong here.

Two layers cut from **one flat drawing** share the same pixels in their overlap.
Showing that skin at two angles draws it twice, offset, and the jaw grew a
ragged double edge. Three further versions of the same mistake followed: a
duplicated collar, a step across the neck, a hairline where the tab ended. Each
is written up in `docs/solutions/two-raster-layers-cannot-share-a-pixel.md`.

What survived is a set of rules, and they are now the design:

- no two layers contain the same drawn content
- the head's tab past the joint ends on bare skin, and fades rather than stops
- the part that moves only rotates, about a pivot on the joint
- the static part starts at the pivot and never above it

## What moves, and how far

**The head rotates** up to about 6.5 degrees toward the pointer, about the base
of the neck. It does not translate: rotation leaves the pivot exactly where it
was, so the neck stays continuous with the collar, and any translation slides
the whole head against a body that did not move.

**The eyes carry the head's rotation and add a small offset of their own**, up
to about 3.5 pixels horizontally and 2.5 vertically. They can translate freely
because nothing is attached to them. All of the expression that the head gave up
lives here.

**Nothing else changes, in any state.** Not by inspection: `plate` and `body`
are the same files at the same coordinates in every frame.

## Runtime

Cursor position becomes an angle through `atan2`, the angle is smoothed so the
head does not snap, and the smoothed value picks a cell plus a residual rotation.
One transform write per animation frame, and only when the value actually
changed.

When the pointer leaves the hero, everything returns to `H0` over roughly half a
second. With no pointer at all, as on a phone, `H0` is what shows.
`prefers-reduced-motion` gets `H0` and nothing else, handled once in the
primitive rather than per component.

## Acceptance

- Plate and body are byte identical in every state. Not verified by eye: they
  are the same files, and if they are not, that is the bug.
- At maximum lean, inspected at four times zoom, the neck reads as continuous:
  no double collar, no step across the skin, no line where the head's tab ends.
  The whole-figure view is not sufficient. Every one of the four seam faults
  found so far was invisible at full-figure scale.
- The eyes move further than the head, and the face behind them has no holes.
- No layout shift. The hero occupies the same box at every angle.
- On a touch device and under reduced motion, the rest state renders and nothing
  moves.
- `make scene` passes, which is what holds the pivot inside its layer and the
  body at or below the joint.

## Budget

Zero. The motion generates nothing: it is one approved drawing, cut into three
layers by a script, transformed by the browser.

The four head cells described below would be the only generation cost this brief
could ever incur, and they are not needed for the version that works.

## Open

**Whether a real turn is needed at all.** The lean plus eye tracking reads as
"he notices you" without a single new drawing, which was the whole point of the
brief. A true turn, where the far ear disappears and the nose crosses the
silhouette, needs drawings rather than transforms: a small grid of approved head
cells, `H-2` to `H2`, with transforms interpolating between neighbours.

That is the oil-motion grid idea with two differences that decide everything:
the cells are few and checked by hand rather than sampled from a generated
space, and the body never enters the grid, so identity below the collar cannot
drift at all.

It is deliberately not built. Decide after living with the lean for a while: if
it reads as stiff, four generations at roughly four minutes each is the cost,
and `docs/solutions/two-raster-layers-cannot-share-a-pixel.md` already says what
the cells must not contain.

**Whether any of this survives vectorisation.** If the character becomes SVG
with named groups, the layers stop being cropped rasters and become objects, and
every seam rule above becomes irrelevant rather than satisfied. See the open
decision in `CLAUDE.md`.
