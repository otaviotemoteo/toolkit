---
title: A layer holds only the pose it was drawn in
date: 2026-09-29
tags: [animation, rigging, rasters]
enforced_by: prose
code_in: scripts/build_contact.py
---

## What happened

The arm was drawn the way a rig is normally authored: hanging straight down from
the shoulder, at rest, so that every angle in the rig could be read as the angle
the limb actually makes. That is the right instinct and it produced two empty
files.

The stage is 1000 by 720. The shoulder sits at y=609 in it, and the arm is 369
pixels long. Hanging down, the elbow lands at 803 and the wrist at 978, both off
the bottom of a 720 pixel canvas. `arm-fore.png` and both hands rasterised to
nothing at all, and the loop played with an invisible forearm for two rounds
before their bounding boxes were checked.

## The part that is easy to get wrong twice

A rotation does not recover them. It is tempting to think of the layer as a
limb that happens to be pointing down, and of the rig as something that will
swing it up into view later. It is not: the layer is a rectangle of pixels, the
rotation is applied to that rectangle, and pixels that were never written cannot
be turned into view. Whatever fell outside the canvas at rasterisation time is
gone before the rig ever runs.

## The fix

Draw each segment in the pose it has to be seen in, and store the rig's angles
as deltas from that pose. The greeting is the pose that is seen, so the greeting
is what is drawn, and the greeting is zero in the rig. The rest pose is then the
delta that swings the arm down, off the bottom of the stage, where the desk
hides it anyway.

This reads backwards for about a minute and then stops. The canvas has to hold
the extreme it is looked at in, not the extreme it starts from.

## The general form

A raster layer is not a limb. It is the intersection of a limb and a rectangle,
and the rectangle is chosen by whoever draws it. Choose it for the frame that is
seen.

## Where it is enforced

Prose here, and `scripts/build_contact.py`, whose arm section says it in two
sentences at the point where someone would otherwise "fix" it back. The empty
file is also its own alarm: a layer that rasterises to nothing has no bounding
box, and that is the first thing to check when a rig moves and nothing appears.
