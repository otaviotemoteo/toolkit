---
title: A colour cast is not uniform, so it cannot be divided out
date: 2026-09-18
tags: [post-processing, colour, local-generation, prediction-wrong]
enforced_by: prose
code_in: scripts/postprocess.py
---

## What happened

Every project card came back from the local model tinted: mint, sage, pale
lime. Not only the ground, the whole picture. Grey houses were green-grey, a
white counter was mint. Repainting the ground alone would have left every object
carrying the tint against a clean paper, which looks worse than a uniform tint.

## Three corrections, and why the first two failed

**A per-channel gain**, the textbook white balance: the ground should be the
paper, so multiply each channel by paper over ground. It turned the green apron
the brief asked for into blue. The correction does not know which green is cast
and which green is a colour somebody chose.

**The same gain, weighted down on saturated pixels.** The apron survived. The
pale counter went pink. A light mint multiplied by the gain clips red and blue at
255 while green stops short, and what is left over is magenta.

**The same idea in Lab, to stop the clipping.** Still pink, and that was the
useful failure, because clipping was not the cause. The model had painted the
ground very green and the counter only a little green. Subtracting the ground's
amount of green from the counter pushes it past neutral whatever the colour
space. **The cast is not uniform**, so no single correction applied to every
pixel can be right.

## What replaced them

Each pixel loses the part of the cast it carries itself: its own offset from
the paper, measured along the cast's direction in the a-b plane, clipped between
nothing and the size of the cast. A pixel can be made neutral and can never be
pushed through neutral into the opposite colour. Saturated pixels are weighted
down because they are object colour, and lightness moves only near the ground's
own lightness, so the ground lands on the paper and nothing else brightens.

On the six cards: the apron stayed green, the calendar squares stayed green, the
counter became white, the houses became grey.

## Where it is enforced

In `white_balance()` in `scripts/postprocess.py`, whose docstring carries the
same three versions. Prose rather than a check, because "does this look
neutral" was judged by eye on six images and there is no fixture that would
have failed the first two versions without also encoding the answer.
