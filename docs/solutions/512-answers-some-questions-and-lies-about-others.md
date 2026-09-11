---
title: Iterating at 512 answers colour and presence, and misleads about everything else
date: 2026-09-07
tags: [iteration, measurement, local-generation]
enforced_by: contract rule
rule_in: CLAUDE.md, and briefs/hero-character/brief.md Budget
---

## Where this came from

Generating a candidate at 1024 costs about eight minutes locally. Measured
alternatives on the same machine and model:

| Configuration | Wall clock |
|---|---|
| 512, 12 steps | 92s |
| 512, 24 steps | 153s |
| 768, 24 steps | 374s |
| 1024, 24 steps | ~480s |

So 512 is roughly five times cheaper per attempt, and the obvious move is to
iterate there and promote the winner.

## What actually happened

A 512 run was used to test two specific corrections: trousers that had come out
pale should be blue, and a computer tower that had come out hollow should be
filled. Both landed, in 92 seconds instead of eight minutes. The question it was
asked, it answered.

Everything else drifted. The character's proportions changed, the face shifted,
the background invented a vertical white band that the negative block explicitly
forbids, and the ground line ran edge to edge through the frame. Judged as a
candidate the image is a clear reject; judged as an answer to the question it
was asked it is a clean success.

## Why

Two causes, and it is worth separating them.

Fewer pixels is less capacity: at 512 the model has less room to hold detail, so
fine structure and likeness degrade first. That part is inherent.

The rest is the init strength, which had to be low for the change to be allowed
to happen at all, and a freely denoising model reinvents whatever the prompt is
not actively holding. A background is exactly the sort of thing nobody holds.

## Rule

**512 is for questions, 1024 is for candidates.**

Ask a 512 run one question at a time, and only questions of the form "did this
change take": a colour, an object appearing or disappearing, a rough placement.
Never judge likeness, proportion, line quality, background cleanliness or
framing from a 512 run, and never treat one as a candidate for acceptance.

The corollary that saves the most time: when a 512 answers yes, do not promote
that image. Regenerate at 1024, and choose how by asking one question about the
change itself.

**Amended the same day, because the first version of this corollary was wrong.**
It said to go back to the last good 1024 and apply the confirmed change there at
high init strength. That fails whenever the init image already contains the old
value, because an init image is inherited, not overridden: the old 1024 had pale
trousers, so at the strength that held the composition it also held the trousers
pale, and at the strength that let them change it let the face change too.

The test is whether the init image contains a counter-example to the change:

| The change | Regenerate how |
|---|---|
| adds or moves something the init does not contradict | from the init, high strength |
| replaces a value the init already shows | from noise, same brief |

Generating from noise costs the composition and buys the change. That is a real
price, and the reason a LoRA is on the roadmap: it is the only tool here that
holds identity without holding everything else with it.

## Where it is enforced

Hard constraint 10 in `CLAUDE.md`, and the Budget line of each brief which
now names both numbers so the cost of an attempt is visible while writing one.
