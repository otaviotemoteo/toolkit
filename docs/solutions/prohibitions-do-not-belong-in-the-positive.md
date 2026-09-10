---
title: A prohibition written into the positive prompt asks for the thing
date: 2026-09-07
tags: [prompting, diffusion, spec, self-inflicted]
enforced_by: check
check: scripts/check_anchors.py
---

## Symptom

Minutes after writing `never-both-blocks.md` and its check, the check failed on
a freshly written anchor. One word: `shading`.

## Cause

The rewritten positive block read `evenly flat areas of muted colour inside the
outlines with no shading`. That sentence is correct English and wrong prompt.
A diffusion model has no operator for "no": it embeds the text, and the token
that is present is the token being aimed at. Writing `no shading` in the
positive block is a request for shading, weakened.

The negative block already carried `shading`, so the word was in both, which is
how the existing check found it. Two different bugs, one detector.

## Rule

The positive block contains only nouns and qualities that should be present.
Every "no", "without", "never" and "avoid" belongs in the negative block, as the
bare noun.

This is exactly the difference between an instruction-following model and a
diffusion model, and it is why the spec carries two anchors rather than one.
Instruction models read `no filled black clothing` and comply.

## Where it is enforced

`scripts/check_anchors.py` catches the common case, where the forbidden word
also appears in the negative block. It does not catch a prohibition written in
the positive for something the negative never mentions. That gap is known and
left open on purpose: closing it means detecting negation in prose, and a check
that guesses is worse than a check with a stated limit.
