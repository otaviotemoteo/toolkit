---
title: A flag that exists is not a flag that is honoured
date: 2026-09-07
tags: [tooling, diffusion, model-selection]
enforced_by: contract rule
rule_in: CLAUDE.md, and this file
---

## Symptom

The recommended local setup, from a good source, was FLUX schnell. Every mflux
generation command accepts `--negative-prompt`, so the plan looked fine.

## Cause

mflux publishes a machine readable capability schema in which every flag carries
a `status`, and the statuses are not decoration:

| Model | `--negative-prompt` |
|---|---|
| `schnell`, `dev` | ignored |
| `z-image-turbo` | ignored |
| `flux2` | rejected |
| `z-image` base | conditional, `guidance > 1.0` |
| `qwen-image` | honored |

`schnell` accepts the flag and discards it in silence. Half of this project's
visual system is prohibition, so the entire plan rested on a flag that does
nothing.

The mechanism is worth knowing rather than memorising. A negative prompt exists
only because classifier-free guidance runs the model twice per step, once on
each prompt, and pushes the result away from the negative. Distilled models,
anything named turbo or schnell, were trained to produce the guided result in
one pass. They are twice as fast because the second pass is gone, and the second
pass is where the negative prompt lived. Speed and obedience to prohibition are
the same currency.

## Rule

Before choosing a model, query the capability surface for the **status** of
every flag the design depends on, not for its presence. When the tool does not
publish one, prove the flag changes the output before designing around it.

The generalisation: prefer the source that says how sure it is. mflux marking a
flag `conditional` with the condition spelled out, `guidance > 1.0`, was worth
more than any amount of documentation asserting support.

## Where it is enforced

Prose here, plus the choice recorded in `CLAUDE.md`. Not a check: this is a fact
about the tool rather than about the repo, and a check that shells out to
`mflux-capabilities` would put a ten second dependency inside a verification
command that has to stay fast.
