---
title: A word in both the positive and the negative block cancels itself
date: 2026-09-07
tags: [prompting, diffusion, spec, self-inflicted]
enforced_by: check
check: scripts/check_anchors.py
fixture: tests/fixtures/anchors/overlap-spec.md
---

## Symptom

The first coloured generation came back with nearly white monitor screens and no
hatching anywhere, while the brief asked for indigo code on the screens and 45
degree hatching for shade. The obvious reading was that the model was ignoring
the prompt.

## Cause

It was obeying it. The diffusion anchor asked for `muted desaturated indigo` and
`45 degree diagonal hatching` in the positive block, and listed `colour` and
`cross hatching` in the negative one. Classifier-free guidance runs the model on
both prompts at every step and pushes the result away from the negative, so each
of those pairs aimed at and away from the same thing. The model split the
difference, which is what it is supposed to do.

## What makes this worth a file

The rule against it was already written, in the spec, two paragraphs above the
block that broke it. Knowing the rule and writing it down did not prevent the
violation, and neither did rereading the section while editing it. That is the
whole argument for checks over prose in one example.

## Rule

Nothing appears in both blocks. If a thing is wanted, only the positive knows
about it. If it is unwanted, only the negative does.

## Where it is enforced

`scripts/check_anchors.py`, in `make check`. It extracts both blocks through
`generate.py`, so the check and the generator cannot drift on what an anchor is,
crudely singularises the words, and fails on any intersection.

The fixture at `tests/fixtures/anchors/overlap-spec.md` is the real mistake,
preserved, so `make mutation` can be watched catching it.
