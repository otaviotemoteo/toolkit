# Brief: the greeting

**Where it lives:** beside "To talk to me" at the foot of the portfolio, the last
thing anyone sees.
**Type:** a looping puppet cut from the approved character, over a workstation
that occludes it.
**The idea in one sentence:** he is working, he catches you looking, he comes up
to say hello, and he goes back to work.

## What changed in v2, and why

v1 was generated from noise. It produced a competent young man who was not the
one at the top of the page: different face, different line, cyan trousers instead
of denim. Identity is the whole point of the asset, so v2 stops generating the
person at all. **The figure is cut from
`briefs/hero-character/approved/hero-character-v2-cutout.png`**, which is the
approved character himself, and only the parts that drawing does not contain are
generated: an arm that can lift, and the desk in front.

This is the gate in `CLAUDE.md` applied honestly: the next asset starts from the
approved character, never from noise.

The second change is the motion. v1 rose once and held, and the arm was one
rigid piece hinged at the shoulder, which reads as a lever rather than an arm.
v2 loops through four beats and hinges twice.

## The loop

| Beat | What moves |
|---|---|
| working | head tilted down toward the screens, body low behind the desk |
| notices | head comes up to the viewer, body still low |
| rises | body lifts until the chest clears the desk, arm starts to leave the hip |
| greeting | forearm arrives beside the head, hand open in a thumb-and-little-finger greeting, two small wags |
| back | everything reverses and settles, then a pause before it starts again |

**The arm hinges twice.** The upper arm turns about the shoulder and the forearm
turns about the elbow, and the elbow is given a later start and a later finish
than the shoulder. A single hinge makes a straight bar sweep an arc, which is
the exact thing the eye reads as mechanical. The lag is what makes it an arm.

**The head is the cheapest beat and does the most work.** It turns about the base
of the neck, exactly as the hero's does, and the whole first half of the loop is
that one rotation.

## The workstation

Two widescreen monitors side by side on a wooden desk, seen from behind, so this
reads as the far side of the hero's own workstation rather than a different room.
The hero shows the same desk from the front; this is the reverse view, which is
why the screens are not visible and the desk is a plain unbroken panel.

It is also an occluder. Everything the animation does not want to draw goes
behind it, so the front panel has to be opaque from side to side and tall enough
to hide him at his lowest point. What is hidden costs nothing: rising from a
chair is then a translation, not a second drawing of a body.

**Framing:** the stage is 1000x720 and every layer is the whole of it.

**Forbidden:** a visible screen, a keyboard seen from above, a chair, a second
person, anything of the desk's top surface.

**The prompt below was run and the result was not used.** Three drafts at
1024x640 came back with the right furniture and the wrong drawing: a wood grain
where the system asks for flat colour, a green cast on the paper, and the desk
seen from above rather than straight on. The workstation is built from the
approved hero's plate instead, which is the same decision the figure gets and
for the same reason. The prompt stays because the brief has to say what was
tried, and because the next backend that can hold this style should be given the
same scene to fail or pass at.

## Prompt

A wide wooden desk seen straight from the front, filling the width of the
picture, with two identical widescreen computer monitors standing side by side
on it. Both monitors are seen from behind: matte near-black rectangles on narrow
stands, each with a slight bulge in the middle of its back panel, and one cable
leaving the lower edge of each and curving down behind the desk.

The desk top is a straight horizontal band of mid-brown wood, and below it the
front panel is one flat area of the same wood, unbroken from one side of the
picture to the other, reaching the bottom edge.

Everything else is plain empty off-white paper.

## Note on the control section

Used when a control image supplies the composition. The arm uses it, because the
arm is generated with the character's own sleeve as an init and the prose then
says only what it is made of.

## Prompt with structure

A young man standing facing the viewer with both arms hanging relaxed at his
sides, hands open, clear of his hips. Light skin, short dark brown hair, a plain
white short-sleeved t-shirt, mid-blue denim jeans, black sneakers. Flat even
colour, plain empty paper behind him.

## Acceptance

The three that decide whether it can move at all.

- The desk's front panel is opaque and unbroken across the whole width, so
  anything behind it is hidden at any height down to the bottom edge.
- Neither monitor shows a screen, because both face away.
- The arm layer has visible paper between the forearm and the body along its
  whole length, wide enough to cut along.

Then the visual system.

- Every filled area is flat, with no gradient and no cast shadow.
- The colours are the ones in the spec's Tokens table and no others.
- The background is plain paper and nothing else.
- No readable words appear anywhere.

Then the motion, judged on the built loop rather than on any single drawing.

- The hand travels along a curve, not a straight arc about one centre.
- The elbow arrives after the shoulder and leaves after it, visibly.
- The head reaches the viewer before the body starts to rise.
- Nothing pops: no layer appears or disappears while it is over open paper.
- The loop's last frame and its first frame are the same pose.

And the one only a person can judge.

- Beside the approved hero at the top of the same page, it reads as the same man,
  because it is the same drawing.

**Budget:** local, `IMAGE_BACKEND=local`. Drafts at 12 steps, candidates at 24.
**Estimated cost:** zero.

## Recipe

Nothing is generated. One command builds the whole asset from files already
approved, and a second renders the loop as a contact sheet so it can be judged
without a browser.

```bash
./.venv/bin/python scripts/build_contact.py                 # nine files
./.venv/bin/python scripts/preview_contact.py --frames 18   # the loop, as a sheet
```

`build_contact.py` reads `briefs/hero-character/approved/hero-character-v2-cutout.png`
and the hero's own `scene/` layers and plate. It writes eight stage-sized layers
and `rig.json` into `approved/v2/`, then the WebP copies go to the site.

`preview_contact.py` holds the same timing the page does and prints the wrist's
height at each hand swap, which is how the swaps are known to happen behind the
desk rather than over open paper.

Three things about this asset are written down because each of them cost a
rebuild:

- **The person is never drawn.** See
  `docs/solutions/the-second-drawing-is-a-different-person.md`.
- **The arm is drawn in the greeting pose, not at rest**, because at rest it
  hangs off the bottom of the stage and rasterises to nothing. See
  `docs/solutions/a-layer-holds-only-the-pose-it-was-drawn-in.md`.
- **Zero is down and angles grow clockwise**, the CSS sense. See
  `docs/solutions/zero-is-down-and-it-turns-the-other-way.md`.

The desk's height is not free either. The torso still carries the hero's crossed
arms, so the desk has to stay above them at full rise: `RISE` at 134 leaves
nineteen pixels of margin, and raising it further puts a second pair of forearms
on the desk.
