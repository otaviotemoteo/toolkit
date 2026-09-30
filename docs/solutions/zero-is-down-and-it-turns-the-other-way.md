---
title: Zero is down, and every library turns the other way from the one before it
date: 2026-09-29
tags: [animation, rigging, geometry]
enforced_by: prose
code_in: scripts/build_contact.py, scripts/preview_contact.py
---

## What happened

Three separate sign errors in one rig, each of which looked like a different
bug.

The arm was built from a direction helper written as `(sin d, cos d)`, so that
zero points straight down. That is a reasonable convention and it is the wrong
one: it grows counter-clockwise on a screen, and CSS `rotate()` grows clockwise.
The arm was therefore drawn at the mirror of every angle the rig stored, and the
rest pose reached up past his ear instead of hanging at his side. The pose that
was solved for and the pose that was drawn were reflections, and both looked
deliberate.

Then the same mistake again, in the other direction, in the code that works out
where the wrist is so that the hand can be swapped out of sight. Its rotation
matrix was the inverse of the right one, so the wrist was reported at 572 when
it was really at 976, the desk was at 600, and the check that exists to prove
the swap happens behind the desk cheerfully reported that it did not.

And before either of those, PIL: `Image.rotate` turns counter-clockwise, so
every preview has to negate what the rig stores.

## What each of them cost

Nothing catastrophic and about an hour in total, which is the point. A sign
error in a rig does not crash and does not look like a sign error. It looks like
a badly chosen pose, or a limb that is too long, or a pivot in the wrong place,
and every one of those has a plausible fix that makes the real problem harder to
see. The first one was diagnosed as "the target is too close to the shoulder"
and nearly fixed by moving the hand.

## The convention, written down once

- Zero is straight down.
- The angle grows **clockwise**, because that is what CSS does and the page is
  what ships.
- In a y-down coordinate system that makes the direction `(-sin d, cos d)`, and
  the rotation of an offset `(x, y)` by `d` is
  `(x cos d - y sin d, x sin d + y cos d)`.
- Anything rendering a preview in Python negates, because PIL turns the other
  way.

## The check that would have caught it in seconds

Not a unit test on the matrix. A printout of where the wrist ends up at a few
points around the loop, next to the height of the desk. A joint's angle is hard
to read and impossible to eyeball; a joint's position is a number that can be
compared with another number. Both sign errors were found by printing the wrist
and seeing 572 where 976 belonged.

## Where it is enforced

Prose here, plus the docstrings of `_along` in `scripts/build_contact.py` and of
`wrist_y` in `scripts/preview_contact.py`, which are the two places the
convention has to be right. `preview_contact.py` prints the wrist's height at
both hand swaps, so the number that catches this is produced on every run rather
than only when someone suspects something.
