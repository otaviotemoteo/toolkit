---
title: A published claim of free credit is a hypothesis until a call proves it
date: 2026-09-07
tags: [cost, vendors, planning]
enforced_by: contract rule
rule_in: docs/cost.md
---

## Symptom

Two routes were planned around free credit. Both were dead on arrival.

| Claim | Reality |
|---|---|
| A new OpenAI account carries $5 of credit, no card | `429 insufficient_quota` on the first call |
| Gemini's free tier includes image generation | `limit: 0` on all six image models |

The Gemini case is the instructive one, because the key was not the problem:
text generation succeeded on the same key in the same minute. The free tier
exists and image generation is simply not in it.

## Cause

Both claims came from documentation and from secondary sources that were
recent, specific, and confidently written. Neither was current. Vendor free
tiers are marketing surface and they move faster than anything that describes
them, including the vendor's own pages.

## Rule

A free tier is not a fact until this project has made a real call against it and
seen a success. Until then it is written down as an assumption with a date, and
nothing is planned on top of it.

The corollary, which cost more than the rule: **do not build the route before
testing the credential.** The Gemini adapter was written before a single call
had been made, and the entire investment was decided by one HTTP status.

## What it cost, and what it did not

Two adapters that did not run in phase 1. Not wasted, exactly: the OpenAI one
becomes live the day a card exists, and both proved the adapter layer does what
it claims, since adding each was one file and one registry line with nothing
above `base.py` touched.

But the ordering was wrong. Probe first, build second.

## Where it is enforced

`docs/cost.md`, which names both failures with their dates so the next claim
meets a stated prior instead of an open mind, and hard constraint 6 in
`CLAUDE.md`, which says to treat any third claim as a hypothesis.
