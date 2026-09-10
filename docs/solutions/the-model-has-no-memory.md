---
title: Nothing carries between generations except seed, init image and weights
date: 2026-09-07
tags: [mental-model, iteration, diffusion]
enforced_by: contract rule
rule_in: CLAUDE.md, and the sidecar written by src/generate.py
---

## The observation that prompted this

"Each image is a little different, it advances on one side and regresses on the
other. Is it taking the other images as context and following the guidelines?"

## The answer

No, and the sidecar proves it. What reaches the model on a from-scratch run:

```
keys sent to the model: ['prompt', 'negative_prompt']
prompt chars: 1928 | negative chars: 472
```

Two strings. The model never sees the previous images, the acceptance criteria,
the prose of the spec, the rest of the brief, or the conversation. Every run is
a new process with the weights reloaded and fresh noise.

So the drift is not inconsistency. It is **independent sampling**. Each run
draws a new point, and exactly three things can carry between two runs:

| Carrier | What it preserves |
|---|---|
| seed | everything, if the prompt is byte-identical |
| init image | the pixels |
| LoRA | the identity, in the weights |

That list is complete.

## The consequence that changes how the work is planned

`## Acceptance` is an instrument for judging, not an instruction for generating.
It never reaches the model. That is the correct design, and it means the
criteria constrain **acceptance** and not **generation**.

Which means the loop is not refinement, it is sampling and selecting. Two
1024 runs from the same brief on the same day: one had the composition and pale
trousers, the other had every colour right and a cropped frame with the monitors
running off the edge. Neither is closer to the other; they are two draws.

No parameter fixes that, because no parameter carries "the composition but not
the colours". `--image-strength` is one axis: hold more of everything, or less
of everything.

## What actually decouples the axes

- **ControlNet** conditions on structure rather than pixels, so shapes are held
  and colour is free. In mflux it runs on the turbo variant, where
  `--negative-prompt` and `--guidance` are `ignored`, so the 472 characters of
  prohibition are lost. Less costly than it sounds: a control image already
  prevents most of what those characters prevented.
- **A LoRA** holds identity in the weights and leaves everything else free,
  negative prompt included. It is the right answer and it needs an approved
  image to train on first.

## A second cause worth separating

Prompt length. At 1928 characters the later clauses are diluted: every extra
clause reduces the weight of the others. The trousers are described in the first
paragraph and landed. The screens are described in the third and came back
empty, twice. That is ordering and length, not a parameter, and shortening the
prompt is likely to do more than any setting.

## Where it is enforced

The JSON sidecar beside every image records exactly what was sent, so this is
checkable rather than remembered. `CLAUDE.md` carries the rule that acceptance
criteria are for judging, and the corollary that if a requirement is not in the
prompt string, it did not reach the model.
