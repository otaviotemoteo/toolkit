# Brief: hero desk

**Where it lives:** home page hero, composited to the right of the character
**Type:** static illustration, no figure in it
**The idea in one sentence:** the machine that runs everything, waiting, with a
space beside it where the person goes.

**Why it is a separate asset.** The character and the desk were one image until
2026-09-07, and every change to one re-rolled the other. Splitting them means
the desk can be resized, replaced or re-lit without touching a character that
is already approved, and the two are joined by a script rather than by luck.
See `docs/solutions/the-model-has-no-memory.md`.

**Framing:** square, 1024x1024. The desk occupies the right two thirds. The left
third is empty paper, reserved: `hero-character-v2-cutout.png` is composited
there afterwards, and anything drawn in that space has to be thrown away.

**Reference:** the approved `hero-character-v1.png` and the desk Otávio picked
out of it. Wide and solid, a drawer unit built into one end, two identical
monitors, a laptop, and the tower standing on the floor rather than on the desk.

**Forbidden:** any person, any part of a person, any hand, arm, shoulder or
shadow of one. Chairs. A second desk. Anything in the left third.

## Prompt

A brown wooden desk seen straight on, standing entirely alone. There is no
person anywhere in this image and no part of a person.

The desk is wide and solid. Its left end is a cabinet of three stacked drawers
with small pale handles, and the rest of it is open leg space with a plain
panel behind. On the desk top stand two identical widescreen monitors with matte
black bezels, side by side, and at the right end an open laptop with a matte
black body, its screen turned to face the viewer straight on. A matte black
computer tower stands on the floor at the right, beside the desk and not under
it, roughly half the height of the desk.

The screens are dark and carry short horizontal lines of code in several muted
syntax colours.

The desk occupies the right two thirds of the image. The left third is empty
off-white paper with nothing in it at all. Everything rests on one horizontal
ground line, and nothing touches the edge of the frame.

## Prompt with structure

A brown wooden desk alone, no person and no part of a person anywhere. A cabinet
of three drawers at its left end, open leg space to the right. Two identical
widescreen monitors with matte black bezels on the desk top, an open laptop at
the right end facing the viewer, a matte black tower standing on the floor
beside the desk. Dark screens carrying lines of code in muted syntax colours.
The left third of the image is empty paper.

## Screens

The same calm state as the character brief: ordinary source code sitting still,
a short block of left-aligned lines in two or three of the muted syntax colours,
with a narrow sidebar of shorter marks. Nothing running, nothing failing,
nothing highlighted.

## Acceptance

- No person and no part of one. No hand, arm, shoulder, leg or silhouette.
- The left third of the image is empty background, wide enough to drop a
  standing figure into without overlapping the desk.
- Exactly two monitors, both the same size, one laptop, one tower.
- The tower stands on the floor, not on the desk and not under the desk top.
- The left end of the desk is a cabinet with three drawers.
- Every filled area is flat, with no surface getting lighter or darker across
  itself, and the colours are the ones in the spec's Tokens table.
- Nothing in the drawing touches the frame.
- No readable words appear anywhere.
- Composited beside `hero-character-v2-cutout.png` at a shared ground line, the
  two read as one drawing rather than as two pasted together.

**Budget:** zero. Generated locally on `IMAGE_BACKEND=local-cn`.

| Run | Cost | Good for |
|---|---|---|
| 512, 12 to 20 steps | ~90s | one question: did a change take |
| 1024, 14 steps | ~4min | a candidate worth judging |
