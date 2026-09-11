# Brief: character in profile

**Where it lives:** the three panel strip that bridges the narrative sections
and the project grid. He walks in during panels one and two, and the strip ends
by cutting to the approved front facing character.
**Type:** static illustration, cut afterwards into a jointed puppet
**The idea in one sentence:** the same person, seen from the side, drawn in a
pose that can be taken apart at the joints.

**Why a new drawing at all.** The approved character stands facing the viewer
with his arms crossed. Walking needs a thigh, a shin and an upper arm that exist
as separate pixels, and nothing behind crossed arms can be recovered. This is
the one case where the answer is a new drawing rather than a transform, and the
route is written up in `docs/asset-map.md`.

**Why profile.** A profile has one eye, half a mouth and no symmetry to match.
Identity in this style is carried by silhouette and by five flat colours, all of
which survive an angle change. A three quarter view would put the face back in
play for no gain.

**Reference:** `briefs/hero-character/approved/hero-character-v2-cutout.png`.
Same person, same clothes, same proportions, turned ninety degrees.

**Framing:** square, 1024x1024. The figure occupies the full height with a
margin of paper on every side. No ground line and no shadow: the strip composites
him onto three different backgrounds, and anything baked into this image has to
be removed from all three.

**Required:** one young man in full profile, facing right, mid-stride. The near
arm and the near leg are clear of the body, with visible paper between them and
the torso. Plain white short sleeved t-shirt, mid blue denim, black sneakers,
dark brown hair drawn as mass.

**Forbidden:** crossed arms, both feet together, any limb overlapping another,
ground line, shadow, background of any kind, readable text.

## Prompt

A young man walks to the right, seen in full profile from the side, his whole
body turned side on so only one eye and one ear are visible. He is caught in the
middle of a step: his right leg is forward with the knee bent and the heel about
to land, his left leg is back with the toe still down, and there is a clear gap
of empty paper between the two legs. His near arm hangs forward and away from
his body, bent at the elbow, with a visible gap of paper between his forearm and
his waist. His far arm swings back behind him.

Light skin, short tousled dark brown hair drawn as one solid mass, a calm
expression, a single simple dot eye. He wears a plain white short sleeved
t-shirt and black sneakers. His legs are covered by mid-blue denim jeans, and
the blue runs the whole length of both legs from waist to ankle, the same solid
blue throughout.

He walks on nothing. The background is plain empty off-white paper, with no
ground line under his feet and no shadow anywhere.

## Note on the control section

**On the section below.** It is used instead of `## Prompt` when a control image
supplies the composition. The control image here is a canny edge map of the
approved character, which holds his build and his clothing edges while leaving
the pose free.

## Prompt with structure

A young man in full profile walking to the right, mid-stride, legs apart and the
near arm swung clear of the body. Flat white t-shirt, mid-blue denim jeans the
same solid blue from waist to ankle, black sneakers, dark brown hair as a solid
mass, light skin, one dot eye. Plain off-white paper behind him, no ground line,
no shadow.

## Acceptance

The first four decide whether the drawing can become a puppet at all. A drawing
that fails them is unusable however good it looks.

- There is visible paper between the two legs at the widest point of the stride,
  at least the width of an ankle.
- There is visible paper between the near forearm and the torso.
- No limb crosses in front of another limb. The far arm and the far leg may be
  hidden behind the body, but nothing overlaps anything.
- Every joint that has to bend, hip, knee, shoulder and elbow, sits on a part of
  the body that is one flat colour, so a cut there does not run through a detail.

Then the visual system, which is the same for every asset here.

- Every filled area is flat. No surface gets lighter or darker across itself.
- The colours are the ones in the spec's Tokens table and no others.
- The line reads as hand-drawn, with no vector or ruled look anywhere.
- Any shading present is 45 degree hatching. Nothing casts a shadow and no edge
  is soft or blurred.
- The background is plain paper and nothing else.
- Nothing in the drawing touches the frame.
- No readable words appear anywhere.

And the one that only a person can judge.

- Held next to the approved front facing character at strip size, it reads as
  the same man. Same build, same hair mass, same five colours.

**Budget:** one image per iteration, 1024x1024, PNG. Composition questions are
asked at 512 first.
**Estimated cost:** zero. Generated locally on `IMAGE_BACKEND=local`, which has
no account and no quota.

## Recipe

The approved drawing did not come from this pipeline, so it has no prompt and
cannot be regenerated. What follows is reproducible from the drawing.

```bash
python3 scripts/postprocess.py approved/profile-walk-v1.png /tmp/w.png --snap-palette
python3 scripts/cutout_flat.py /tmp/w.png approved/profile-walk-cutout.png --tolerance 6 --trim
python3 scripts/split_puppet.py approved/profile-walk-cutout.png approved/puppet
```

`--clean-ground` is deliberately absent. It erased the folds on the shirt and
said it had succeeded: see
`docs/solutions/clean-ground-cannot-see-an-outline-that-is-not-there.md`.

**Open, with a trigger.** Knees, elbows and a swinging arm. The legs alone carry
a walk at strip size, and every extra joint is another seam in a flat drawing
that supports one joint per limb. Cut them when the walk reads stiff beside the
finished backgrounds, not before.
