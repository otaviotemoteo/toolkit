---
title: clean-ground cannot see an outline that is not there
date: 2026-09-11
tags: [post-processing, flat-style, silent-failure, prose-only]
enforced_by: prose
code_in: scripts/postprocess.py
---

## What happened

The walking figure went through the usual two corrections, `--clean-ground` and
`--snap-palette`, and came out with white gashes torn across his chest and
shoulder. The pass printed `51971 pixels of shading removed` and exited zero.
The damage only became visible three steps later, in the walk cycle.

## Why

`clean_ground` finds the ground the same way `cutout_flat` finds it: the
background is the region **connected to the image border**. It then erases
anything faint inside that region, which is how a drop shadow under a desk
disappears.

That reasoning has a hidden premise, and this visual system breaks it. The style
has **no outlines**. A white t-shirt at `#FBFBF9` sits about 8 units from the
paper, with no line between them, so the shirt is not merely similar to the
background, it is continuous with it. The walk inward from the border does not
stop at the figure, because from where it stands there is no edge to stop at.
Everything on the shirt that is slightly darker than flat, which is exactly the
folds, then qualifies as shading on the ground.

It is the same root as `the-wrong-keyer.md`, one step later in the pipeline. That
one was about a key that erased the shirt. This one is about a fill that walks
into it.

## Why this is prose and not a check

Three mechanical tests were written and all three failed to separate the two
cases, which is worth recording so nobody spends the afternoon again:

- **Colour of what is about to be erased.** Both cases erase pixels nearest a
  non-paper token: 8 percent on the figure, 16 percent on the desk scene. The
  case that must pass scores worse than the case that must fail.
- **Inside the artwork's bounding box.** The desk's own shadow is inside the
  desk's bounding box too.
- **Connected to the border.** Both are, which is the whole problem.

What actually separates them is whether the erased region is part of the subject
or resting against it, and that is the question the pass was already trying and
failing to answer. A check built on any of the three would be a check that
misclassifies, which is worse than none: it would either block the case the tool
exists for, or pass the case that destroys a drawing.

## The rule

**`--clean-ground` is for a scene whose subject is dark against paper.** Leave
it off for anything pale. `--snap-palette` is unconditional and safe: it moves
large flat areas onto token colours and cannot reach into a silhouette.

For this character the recipe is `--snap-palette`, then `cutout_flat.py`, then
`split_puppet.py`, and it is recorded beside the asset.

## Where it is enforced

Prose, in the `clean_ground` docstring in `scripts/postprocess.py`, which names
this file. `docs/solutions/README.md` allows prose when the mistake is not
mechanically detectable, and the section above is the evidence that this one is
not, at least not by any test tried here.
