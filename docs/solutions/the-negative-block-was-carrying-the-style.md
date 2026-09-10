---
title: The negative block was carrying the style, and losing it cost more than predicted
date: 2026-09-07
tags: [prompting, diffusion, controlnet, prediction-wrong, retracted-rule]
enforced_by: contract rule
rule_in: CLAUDE.md, and src/adapters/local_mflux.py LocalControlNetBackend
---

## The prediction, and it was wrong

ControlNet was proposed to separate two axes that `--image-strength` cannot:
hold the structure of an approved drawing while leaving colour free. In mflux,
Z-Image ControlNet runs on the turbo variant, which is guidance-distilled, so
`--negative-prompt` and `--guidance` are both `ignored` and the spec's 472
characters of prohibition are discarded.

That cost was stated in advance and estimated as survivable, on the reasoning
that a line drawing used as a control already prevents most of what those words
prevented.

## What actually came back

Every colour requirement was met: blue jeans, white shirt, black sneakers, brown
desk, black tower, coloured code on the screens. And the visual system was gone.
The hand-drawn ink line, which is the identity of the entire project, had been
replaced by flat vector illustration with soft texture and rendered shading.
Readable text appeared on the screens. The composition did not follow the
control image either.

The prohibitions were not redundant with the control image. They were the style.
`painterly`, `airbrush`, `gradient`, `shading`, `readable words`: every one of
those things came back the moment nothing was pushing against it.

## Why this is worth a file rather than a retry

The failure is at the level of the approach, not the parameter. Raising
`--control-strength` or switching `canny` for `hed` might recover the
composition, and would do nothing about the style, because the style loss comes
from the model being distilled and not from how the control was applied.

Three attempts had been budgeted before falling back. Two of them were not
spent, because tuning a parameter cannot fix a cause that is not the parameter.
That is the useful part of having said "three attempts" out loud beforehand: it
makes stopping at one a decision rather than a mood.

## Rule, written and then retracted the same hour

The rule written here was: a guidance-distilled model is not usable for this
visual system at all, and any backend reporting `uses_negative = False` is for
experiments only, never for a candidate.

**Otávio approved that image as the new direction for the project.** So the rule
is retracted, and the retraction is more instructive than the rule was.

What survives is the observation, which was accurate: without the negative block
the output is not the style the spec described. What was wrong was the leap from
"not what the spec says" to "not usable". The spec is a description of an
intention, and the person whose intention it is had not seen this option yet.

The corrected rule:

- A backend with `uses_negative = False` cannot be trusted to **hold** a visual
  system, because nothing pushes back on what the model drifts toward. That part
  stands and is why the warning stays in the CLI.
- It can still **propose** one. An image that fails the spec is evidence about
  the spec as often as it is evidence about the image, and the owner of the
  design is the one who decides which.

## What I got wrong about my own role

The quality gate exists to check work against an agreed intention. It is not a
licence to reject a direction on the owner's behalf. The correct report was
"this violates the spec in these four ways, here it is", and that is what was
delivered, but it was framed as a failure rather than as a question.

## Where it is enforced

`LocalControlNetBackend` declares `uses_negative = False`, and `generate.py`
prints the character count of the prohibition being discarded before it runs.
The backend is kept rather than deleted, because knowing that this branch is
closed is worth more than the disk it occupies, and because a future
non-distilled ControlNet would make it live again.
