---
title: The second drawing of a person is a different person
date: 2026-09-29
tags: [identity, animation, compositing, briefs]
enforced_by: prose
code_in: scripts/build_contact.py
---

## What happened

The greeting at the foot of the portfolio was generated from its own brief: a
young man, light skin, short dark brown hair, plain white t-shirt, mid-blue
denim, black sneakers, arms at his sides. Every clause was taken from the
approved hero's brief. Thirteen runs went by and the best of them was a
competent young man who was not the one at the top of the page.

Put the two side by side and nothing matches. The face is drawn by a different
hand. The denim came out cyan rather than mid-blue. The paper has a grain the
hero's does not. Read on their own, each drawing satisfies the brief. Read
together, which is the only way anyone reads them, they are two people, and a
portfolio whose last image is a stranger has spent its last impression on the
wrong face.

`pose-variation-is-not-generation.md` had already said to start from the
approved image rather than from noise, and this was the bill for not doing it.

## Why the brief could not have saved it

A brief specifies what is in the picture. Identity is not in the picture, it is
in ten thousand decisions below the level anyone writes down: how far apart the
eyes sit, where the hairline breaks, how much the jaw softens at the chin, how
wide the neck is against the collar. There is no length of prose that pins those
down, because the model resamples all of them on every run. A longer brief buys
a closer stranger.

## What the second version does instead

It does not draw him. The figure is the approved cutout itself, cut into a head
that turns about the neck, eyes that lift off it, and a torso, using the cuts
the hero already uses. The monitors are the approved hero's own monitors with
their screens filled in so they read from behind. What is genuinely new is one
arm, and an arm in this style is a tapered capsule with a round cap at each end,
which a script can lay down on the character's own sampled palette exactly.

So the rule is not "generate from the approved image". It is stronger, and the
order matters:

1. Can the approved drawing be **cut** to give this? Cut it.
2. Can the shape be **drawn** from the approved drawing's own colours? Draw it.
3. Only then generate, and only from the approved image as an init.

The generated route is last because it is the only one that can come back with
somebody else.

## The cost of the rule, stated honestly

Cutting and drawing buys identity and spends flexibility. The torso still has
the hero's crossed arms in it, so the desk has to hide them, and that constrains
how far he is allowed to rise: about a hundred and thirty pixels, no more, or
a second pair of forearms appears above the desk. A generated body would have
had no such constraint and no such likeness. The constraint was the cheaper
half of that trade, but it is a real one and it shaped the whole composition.

## Where it is enforced

Prose here, and `scripts/build_contact.py`, which opens the approved cutout and
the approved plate and generates nothing. Its module docstring says why. The
brief at `briefs/contact-greeting/brief.md` carries the same rule under
"What changed in v2, and why", so it is in front of whoever edits the asset next
rather than only in front of whoever reads this directory.
