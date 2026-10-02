---
title: No ChatGPT subscription feeds the API, and a subscription is the wrong purchase anyway
date: 2026-09-07
tags: [cost, vendors, planning]
enforced_by: prose
---

## The question

Would a ChatGPT subscription let the toolkit use OpenAI's image models, while
also being useful personally?

## The answer

No. ChatGPT subscriptions and the API platform are separate billing systems and
no plan tier includes API credit. A $20 subscription changes nothing about the
`429` that `generate.py` receives.

## The arithmetic that matters more

If a card ever exists, the purchase is prepaid API credit, not a subscription:

- `gpt-image-1-mini` costs roughly $0.005 per image
- 18 assets at a generous 40 attempts each is 720 images
- **about $3.60**, inside the $5 minimum, for the entire project
- and seconds per image instead of the eight minutes a local 1024 render takes

The subscription remains a legitimate separate want. It is simply not a route
into this pipeline, and buying it expecting otherwise is the mistake.

## The pattern under all three of these

This is the third time the same shape appeared: Cursor's plan, then free tiers,
now a subscription. **A product's consumer surface is not its API surface, and
access to one is never access to the other.** Ask what the credential is for
before designing around what it appears to unlock.

## Where it is enforced

Prose, and the accounts table in `docs/cost.md`. This is a fact about vendors, not
about this repo, so there is nothing here for a check to hold onto.
