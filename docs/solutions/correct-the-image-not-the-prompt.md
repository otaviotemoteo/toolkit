---
title: Correct the image, not the prompt, when the defect is mechanical
date: 2026-09-11
tags: [pipeline, post-processing, iteration]
enforced_by: code
code_in: scripts/postprocess.py
---

## The problem it answers

Every generation is a sample. A defect fixed by running again is a defect fixed
by luck, and luck does not hold: the next run reintroduces it, or trades it for
another one. See `docs/solutions/the-model-has-no-memory.md`.

The usual lever is the negative prompt, and here that lever is missing. The
backend that produces this project's approved style is guidance-distilled and
discards the negative block entirely, so prohibitions can only be written as
affirmations in the positive block, which is a suggestion rather than a rule.
See `docs/solutions/the-negative-block-was-carrying-the-style.md`.

So a defect that is mechanical should be corrected mechanically, after the fact,
where the result is certain.

## What it does

**Removing shading from the background.** A drop shadow under a desk is a large,
low-contrast blob sitting on the paper, and the generator keeps drawing it
because nothing forbids it. The fill treats the background not as a colour to
match but as the region connected to the border, walks inward, and erases what
it finds that is not artwork.

**Snapping large flat areas to the palette.** The token table in the spec is
read at run time, so there is still exactly one copy of the visual system.
Regions below a size threshold are left alone, because syntax colours on a
screen are meant to be many and a palette applied too eagerly eats them.

## Two things it got wrong first, both instructive

**The threshold was typed, and it was wrong.** At a hand-picked 60, the darkest
part of the shadow counted as artwork, so the guard ring around it blocked the
fill from reaching the rest, and the shadow survived a pass that reported
success. In a flat palette the gap between shading and artwork is enormous: on
the desk the shadow reached 70 units from the paper and the nearest real colour
sat at 466. That gap is visible in the histogram, so the threshold is now found
rather than chosen.

**Filling with a flat colour left a halo.** The paper in a generated image is
not uniform: it carries a faint texture and a slight vignette. Painting the
shadow out with the border colour replaced it with a lighter sticker outline
hugging every object, which is worse than the shadow. Inpainting takes its
colour from the immediate surroundings, and the difference between the two is
the difference between removing a shadow and moving it.

## The limit, stated

This is safe on flat artwork and reckless on a photograph. Both operations
assume a small palette, hard boundaries between regions, and a plain background.
Nothing here should be pointed at an image that does not have those.

## Where it is enforced

Prose here plus `scripts/postprocess.py`, which carries the reasoning and the
measured numbers in its docstring. Not a check: whether an image needed
correcting is a judgement, and a check that guessed would be worse than none.
