---
title: Cut before you correct the cast, because the cast is what separates them
date: 2026-09-29
tags: [post-processing, colour, cutout, order-of-operations]
enforced_by: prose
code_in: scripts/build_greeting.py
---

## What happened

The greeting's body came back from the cutout with no t-shirt. Head, arms,
jeans and shoes, and a hole where the torso should be. Lowering the tolerance
did not help: at every setting from 4 to 14 the shirt was gone, and at 4 the
paper's grain came through as subject instead.

## Why

The pipeline was: correct the colour cast, then cut the background away. Both
steps were right and the order was wrong.

The local model tints the whole image, and here the ground came out green. The
white shirt did not. Measured on the actual drawing:

| | ground | shirt | distance |
|---|---|---|---|
| as generated | 195, 223, 200 | 227, 226, 216 | 50 |
| after `--white-balance` | 242, 245, 239 | 247, 244, 238 | 7 |

`cutout_flat.py` finds the background as the region connected to the border
within a tolerance. At a distance of 50 the shirt is unreachable. At 7 it is the
background. **The correction removed the very difference the cut relies on**, and
it did so on purpose: neutralising a cast is exactly the act of making a tinted
white and a true white agree.

## The rule

**Cut first, correct afterwards.** The alpha comes from the drawing as the model
made it, where the cast is still doing the work of separating the subject from
its ground, and the corrected colour is composited back behind that alpha.

```python
alpha = cutout(raw)                  # while the ground is still green
rgb   = white_balance(raw)           # now neutralise everything
out   = dstack([rgb, alpha])
```

It generalises past colour: **a correction that makes two things look alike
destroys any later step that needed to tell them apart.** Anything that
normalises, snaps, flattens or denoises belongs after every step that separates.

## Where it is enforced

Prose, and the recipe in `briefs/contact-greeting/brief.md`, which runs the two
in this order. `scripts/postprocess.py` cannot enforce it: it does not know what
will be done next, and from inside the correction the result looks perfect.
