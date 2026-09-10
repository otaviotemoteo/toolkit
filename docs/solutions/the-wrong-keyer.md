---
title: Chroma key was the wrong tool, and luminance key only worked while the drawing was monochrome
date: 2026-09-07
tags: [pipeline, cutout, spec, measurement]
enforced_by: spec rule
rule_in: docs/ILLUSTRATION_SPEC.md, Two modes
---

## Symptom

Mode B specified generation onto a flat `#00FF00` field, cut out afterwards by
`cutout.py`. The first real generation returned a pale mint background instead,
striped, with a soft blob in one corner.

## Measurement, not impression

Sampling the image every seventh pixel: **7903 distinct colours**, corners
ranging from `(188,253,194)` to `(201,250,212)`. A keyer needs a tolerance
tighter than the variation it is keying, and there was no such tolerance.

This is not a prompting failure to be fixed by a better prompt. A diffusion
model produces a field of related colours because that is what it is; asking for
a perfectly uniform rectangle asks it to stop being a diffusion model in one
region of the canvas.

## The intermediate answer, and why it died

For black line on light paper, the ink is the alpha: set `alpha = 1 - luminance`
and no flat background is needed, only a light one. It worked beautifully, and
every thin cable and shoe seam survived.

It stopped working the same day, when the character became coloured, because
blue trousers are neither ink nor paper and a luminance key gives them partial
alpha.

## Rule

Mode B generates on `PAPER` and cuts nothing out. The page ground is paper
anyway, so a baked-in paper background is not a compromise, it is one fewer step
that can fail. `<KEY_COLOR>` now means `#F7F6F3`.

Revisit only for an asset that must overlap something that is not paper, and
when that day comes, prefer generating the subject at a size that does not need
compositing over reintroducing a keyer.

## What this removed

An acceptance criterion the model failed every time, a whole category of edge
artefact, and a dependency on `cutout.py` for the common case.

## The keyer that finally worked

Three were tried, and the third is in `scripts/cutout_flat.py`.

The insight is that the background is not a colour to match, it is **the region
connected to the border**. Fill inward from the edge through everything within a
few units of the border colour; whatever the fill cannot reach is the subject.

That is what makes a white t-shirt survive. In the approved character the shirt
sits 6 units from the background out of a possible 765, so any test asking "is
this pixel white" erases the torso. The flood fill never asks: the shirt is
enclosed by the drawing, so the fill cannot get to it, so it stays.

Two details that took a second pass:

- The tolerance cannot be raised to swallow anti-aliased edge pixels, because it
  has to stay below the distance of the shirt. So the pale ring along every edge
  is removed morphologically instead, by eroding the mask two pixels.
- A faint fringe survives on dark grounds, inherited from a light stroke in the
  source art. Left alone: every ground in this project is paper, and on paper it
  is invisible. Measured, not assumed.

## Where it is enforced

`docs/ILLUSTRATION_SPEC.md`, Two modes, which carries this reasoning so the next
person to propose a chroma key meets the measurement instead of the conclusion.
`DEFAULT_KEY` in `src/generate.py` is the single definition of the colour, read
by the smoke test too.
