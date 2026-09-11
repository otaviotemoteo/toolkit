# Brief: hero character

**Where it lives:** home page hero, right side, above the fold
**Type:** static illustration now; becomes pointer-driven in phase 2
**The idea in one sentence:** the person who built all of this, standing beside
the machine that runs it, at rest and paying attention.

**Reference:** two images generated before this project started. The
first is full colour, cartoon, warm; the pose and framing are exactly right and
this brief keeps them. The second is the same scene in black and white, and it
is the useful failure: it is too heavy, because the shirt, trousers, monitors
and tower are all filled solid black, which turns the drawing into a silhouette
study. This brief keeps the first one's composition and fixes the second one's
mass problem with outline instead of fill.

**Framing:** square, 1024x1024 source. Displayed at roughly 480x480 CSS at
DPR 2, so the source has room to spare.

**Required:** one young man standing on the left, arms crossed, relaxed, facing
the viewer with a small smile. To his right a desk with two monitors side by
side and an open laptop, code visible on all three screens. A tower under the
desk with cables. A pen cup. Everything sits on one ground line.

**Forbidden:** any colour other than the indigo on the screens. Filled black
clothing. Soft shadow under any object. Perspective drama. Plants, mugs, sticky
notes, posters. Any text.

## Prompt

A young man stands well over on the left side of the scene, facing the viewer,
arms crossed comfortably across his chest, weight even on both feet. Light skin,
short tousled dark brown hair, a small easy smile, simple dot eyes. He wears a
plain white short-sleeved t-shirt and black sneakers. His legs are covered by
mid-blue denim jeans, and the blue runs the whole length of both legs from waist
to ankle, the same solid blue throughout.

A wide gap of empty paper separates him from the furniture. He is not leaning on
the desk and not touching it; there is roughly a third of his own body width of
clear space between his shoulder and the nearest edge of it.

To the right of that gap stands a brown wooden desk on straight legs, seen
straight on. On the desk, two identical widescreen monitors side by side with
black bezels, and to their right an open laptop with a black body turned
slightly toward the viewer. The screens are dark and carry short horizontal
lines of code in several different muted colours, a few lines of each, the way
syntax highlighting looks from across a room. Under the right side of the desk
sits a computer tower filled in solid near-black from top to bottom, with two or
three cables curving loosely up to the desk. A small cup of pens at the far
right edge.

Everything rests on one horizontal ground line, on plain empty off-white paper.
The man is roughly as tall as the desk is wide.

## Note on the control section

**On the section below.** It is used instead of `## Prompt` when a control image
supplies the composition, and it is much shorter on purpose: the control image
already says where everything is, so the prose says only what everything is made
of. Length dilutes, and the screens kept coming out empty while they sat in the
third paragraph of a long prompt. Everything under the heading is sent verbatim,
so no commentary belongs inside it.

## Prompt with structure

A young man with light skin and short dark brown hair, wearing a plain white
t-shirt, mid-blue denim jeans and black sneakers, standing to the left of the
desk with his arms crossed. The desk is entirely to his right, never behind him,
and his whole body is visible and clear of it. His face is fully
drawn and turned toward the viewer: two clear eyes, eyebrows, a nose, and a
small closed smile. Every surface of him is evenly lit, one flat tone per area,
with no darker side and no shading under the chin or the arms.

The desk is large: its top is about as wide as the man is tall, and it is heavy
and solid rather than slight. It occupies the right half of the scene without
touching the right edge. A wide band of empty background separates him from it,
wider than his own shoulders, and no part of the desk passes behind him.

Beside him stands a brown wooden desk holding two identical widescreen monitors
of exactly the same size, side by side, and an open laptop at the far right
corner of the desk with its screen turned to face the viewer straight on, not
angled away. The computer tower stands on the floor beside the desk rather than
on top of it. The screens are dark and carry lines of code in muted syntax
colours.

## Screens

The first asset, so the calmest state: ordinary source code, sitting still. Each
of the three screens shows a short block of left-aligned lines in two or three
of the muted syntax colours, with a narrow sidebar of shorter marks. Nothing is
running, nothing is failing, nothing is highlighted.

## Acceptance

- Every filled area is flat. No surface gets lighter or darker across itself.
- The colours are the ones in the spec's Tokens table and no others.
- The line reads as hand-drawn, with at least one visible construction or
  overshoot stroke somewhere, and no vector or ruled look anywhere.
- There is clear empty paper between the man and the desk, wide enough to see at
  a glance. He does not touch or lean on it.
- Any shading present is 45 degree hatching. Nothing casts a shadow on the floor
  and no edge is soft or blurred.
- The background is plain paper and nothing else: no wall, no vignette, no shape
  behind the subject.
- Nothing in the drawing touches the frame.
- No readable words appear anywhere. The code is marks, not text.
- The scene is recognisable as "a developer standing next to a workstation" in
  about three seconds.

**Budget:** one image per iteration, 1024x1024, PNG.
**Estimated cost:** zero. Generated locally on `IMAGE_BACKEND=local`, which has
no account and no quota.

| Run | Cost | Good for |
|---|---|---|
| 512, 12 to 20 steps | ~92s | one question: did a change take |
| 1024, 24 to 28 steps | ~480s | a candidate worth judging against Acceptance |

Never judge this brief's acceptance criteria from a 512 run. See
`docs/solutions/512-answers-some-questions-and-lies-about-others.md`.
