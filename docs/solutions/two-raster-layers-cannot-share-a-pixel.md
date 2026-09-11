---
title: Two raster layers cut from one drawing cannot share a pixel
date: 2026-09-11
tags: [animation, compositing, layers, prediction-wrong]
enforced_by: check
check: scripts/check_scene.py
fixture: tests/fixtures/scenes/README.md
code_in: scripts/split_layers.py
---

## What the brief specified

`motion.md` asked for a two-bone neck: the neck rotating half the angle about
its base, the head rotating the other half about the top of the neck, nested so
the head reaches the full angle. That is how a puppet rig is built and it is
what makes a turn read as a person with a spine rather than a cut-out on a pin.

## What happened

It ghosted. The layers were cut with a generous overlap, on the reasoning that a
rotation should slide the seam across solid pixels instead of across a hole. But
overlapping crops of the **same drawing** contain the same skin twice, and
showing the same skin at two different angles draws it twice, offset. The jaw
grew a ragged double edge that was obvious at any zoom.

Overlap is the right instinct for a rig whose parts were drawn separately. It is
the wrong one for parts cut out of a single flat image.

## Three more versions of the same mistake, in order

**The collar appeared twice.** With one joint instead of two, the head carried
the neck and turned about the collar. The head's tab reached far enough below
the joint to include the collar line, so the collar rotated with the head and
sat against the static collar beneath it. A tab duplicates whatever is drawn
inside it.

**A step opened across the neck.** The head was given a small sideways
translation for expression. Rotation about a pivot leaves the pivot exactly
where it was, so the neck stays continuous with the collar. Translation moves
everything, including the point that was supposed to stay put, and the neck
broke where the moving skin met the static skin. The expression moved to the
eyes, which can translate freely because nothing is attached to them.

**A hairline showed where the tab ended.** Even on bare skin, a hard cut shows:
the rotation resamples the layer, the cut row becomes partly transparent, and it
blends against the body underneath as a faint line straight across the neck.
Fading the tab's alpha to nothing over its last rows removed it. There is no
longer an edge to catch the light, only the same skin twice at the same angle.

## Rules

1. No two layers contain the same drawn content.
2. A tab past a joint ends on bare, featureless area. Whatever is drawn inside a
   tab appears twice.
3. The tab fades out rather than stopping.
4. The part that moves only rotates, about a pivot on the joint. Translation is
   for parts with nothing attached to them, like eyes.
5. The static part starts at the pivot and never above it.

## What this cost, and what it bought

Four rebuilds of the split, each caught by looking at the collar at four times
zoom rather than at the whole figure. The whole-figure view showed nothing wrong
in any of the four.

What it bought is a hero that animates with no generation at all: one drawing,
three layers, one rotation, and a body that is byte-identical in every state
because it is the same file.

## Where it is enforced

`scripts/check_scene.py` holds rules 4 and 5, which are checkable from the
manifest alone: a pivot must lie inside the layer that turns about it, and the
body must not start above the pivot. `tests/fixtures/scenes/scene.json` breaks
both, plus two other ways a manifest rots, so the check is watched failing.

Rules 1 to 3 live in `scripts/split_layers.py`, which is what produces the cut,
with the reasoning in its docstring so the next person to widen the tab meets
the argument first.

## The hip, and why the exact solutions lost

The walking puppet hit the same seam one joint lower, and it is worth recording
that the two *correct* answers both failed on this drawing while the soft one
worked.

A leg cut straight across at the crotch opens a wedge of bare paper when it
turns, because the cut line rotates and the body above it does not. The fix is a
tab reaching up past the joint, hidden by the torso. That tab then has the
opposite problem: turned the other way it swings outward and its corner appears
beyond the hip as a blue wedge.

**Keeping only the tab pixels whose whole orbit stays under the torso** is
exact, and it deletes precisely the pixels that were doing the work: the ones
near the silhouette, which are the ones that swing down to cover the wedge. The
protrusion became a slit.

**Cutting the leg along an arc centred on the pivot** is the textbook answer,
because rotation preserves distance from the pivot and an arc maps to itself. It
needs a radius at least as large as the leg is wide at the joint. Measured here:
the trousers span about 100px at the crotch while the waist above them spans
128px and sits offset, so an arc big enough to close the joint already leaves
the body at rest. The drawing's own proportions rule it out.

What worked is what the neck used: **a short tab with its alpha fading out.**
Short, so the sweep is small, 34 rows sweeping 7px at 12 degrees. Faded, so the
part that does leave the body is a few percent of opacity landing on paper of
almost the same value, which is invisible where a hard edge was a wedge.

The general lesson is not about hips. **An exact fix that deletes the thing it
was protecting is worse than an approximate one that hides its own error**, and
in flat raster art a soft edge hides a great deal, because there is so little
contrast for it to betray.
