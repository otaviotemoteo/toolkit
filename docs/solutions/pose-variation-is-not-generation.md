---
title: Generating a pose from scratch is not slow, it is wrong
date: 2026-09-07
tags: [animation, identity, pipeline, img2img]
enforced_by: code
code_in: src/generate.py --init, src/adapters/local_mflux.py
---

## The question that led here

Eight minutes per image at 1024 looks fatal once the plan needs eighteen assets
plus a grid of animation poses. Where is the throughput going to come from?

## The reframe

For the animation it is not a throughput problem. `briefs/hero-character/motion.md`
requires that between any two adjacent cells the only difference is head angle
and pupil position, with shirt, shoulder line, desk and monitors pixel identical,
and that the face stays recognisably the same person across all nine cells.

Generation from noise cannot satisfy that at any speed. Every call is a fresh
draw: the face changes, the shirt changes, the desk moves. A faster generator
produces wrong frames sooner.

## The mechanism that is both correct and cheaper

Start from the approved image instead of from noise. With an init image the
model does not begin at pure noise, it begins partway through the denoise and
runs only the tail of the schedule. So a pose variation costs a fraction of the
still it came from, **and** it holds identity, because it inherited it.

The correct path and the fast path are the same path. Generating from scratch
was the worse option on both axes at once.

**Measured, and narrower than first claimed.** The saving scales with how much
influence the init image is given, because influence is what decides how much of
the schedule is skipped. At low influence there is barely any saving: a 1024
recolour at strength 0.35 took 7min30 for 28 steps, about the same as generating
it from noise, because almost the whole schedule still ran.

That is not a contradiction, it is the parameter doing its job. A large change
needs a free model and pays for it. Pose variation is the opposite case, a small
change from an approved frame, so it runs at high influence and that is where
both the speed and the identity come from.

State it precisely: **img2img is cheaper when the change is small.** The
animation is the small-change case. The recolour was not.

For identity across many assets rather than many frames, the next tool up is a
LoRA trained on the approved character. `mflux-train` exists; untried.

## Rule

Any asset that must contain an already-approved subject starts from that
subject's image, never from noise. From-scratch generation is for a subject that
does not exist yet.

## Where it is enforced

`src/generate.py` takes `--init` and `--init-strength`, `ImageRequest` carries
them, and `local_mflux.py` passes them through. The sidecar records both, so an
image made from another image says so and the chain back to the original is
readable.
