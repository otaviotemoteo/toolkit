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

**Reference and control image:** the desk from the approved scene, which already
has the right style and is already seen straight on. Recreate the control with:

```python
src = Image.open("briefs/hero-character/approved/hero-scene-final.png")
crop = src.crop((440, 440, 1190, 1175))          # the desk, clear of the figure
# scale to 620 on the long side, paste bottom-right on a 1024 paper canvas,
# leaving the left third empty for the character
```

That crop is also the fallback: if generation cannot match the style, the desk
is already an asset and only needs compositing. Wide and solid, a drawer unit built into one end, two identical
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

A brown wooden desk alone, no person and no part of a person anywhere. Seen from
directly in front: the desk top reads as a straight horizontal band, the front
panel as a flat rectangle, and every edge is parallel to the frame. A cabinet at its left
end holding exactly three drawers, one above another, and open leg space to the
right. Two identical widescreen monitors with matte black bezels on the desk
top, an open laptop at the right end facing the viewer, and a matte black tower
standing on the floor entirely clear of the desk, with a gap of empty paper
between the tower and the nearest desk leg. Dark screens carrying lines of code
in muted syntax colours. The desk and the tower meet the ground line directly,
with clean empty paper immediately beneath and around both. The left third of
the image is empty paper.

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

## Outcome, 2026-09-11

Generated in two rounds. The first came back in three-quarter perspective with a
soft drop shadow, four drawers and the tower overlapping the desk. Moving the
perspective prohibition into the positive block, since this backend discards the
negative one, and raising the control strength to 0.85 fixed the view and the
count. The shadow survived both rounds, because nothing in a positive prompt
reliably prevents a generator from drawing one, and was removed afterwards with
`scripts/postprocess.py --clean-ground`.

**What ships is not this file.** The hero uses the desk cropped out of the
approved scene, for one reason: it and the character came from the same image,
so nothing has to be matched by eye. The generated desk is kept as evidence that
a brief can produce one, and as the fallback if the approved scene is ever lost.

That is not a defeat for the pipeline. Compositing an approved asset is the
pipeline, from the moment the animation stopped being generation.

**Budget:** zero. Generated locally on `IMAGE_BACKEND=local-cn`.

| Run | Cost | Good for |
|---|---|---|
| 512, 12 to 20 steps | ~90s | one question: did a change take |
| 1024, 14 steps | ~4min | a candidate worth judging |
