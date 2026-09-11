# Brief: strip scene, calm

**Where it lives:** panel three of the strip, and behind all three. It is the
only background drawn: panels one and two are this same picture with the fire
layer composited over it.
**Type:** static illustration, no figure in it
**The idea in one sentence:** the machine, running quietly, the way it looks
when the work is done.

**Why it is one image and not three.** Three finished panels can only be
cross-faded, and then "fogo vira linha" stops happening: the fire disappears and
a line appears somewhere else. With the fire as its own layer over one unchanged
scene, the same element collapses into the line, which is what the wireframe
describes. See `docs/asset-map.md`.

**Reference:** `docs/ILLUSTRATION_SPEC.md`. Same world as the hero desk, seen a
few steps away from it.

**Framing:** square, 1024x1024 source, cropped to the panel afterwards. The rack
occupies the right two thirds and sits on one horizontal ground line. The left
third is empty paper: the walking character is composited there and anything
drawn in that space is thrown away.

**Required:** one upright server rack, dark, with visible horizontal slots and a
few small status marks. Cables leaving the back and curving down to the floor.
Plain paper everywhere else.

**Forbidden, and this one is load-bearing:** no lit screen anywhere, and nothing
warm. The fire layer is separated from its own drawing by colour, and the only
warm colours in this system are the two used by code on screens. A monitor
glowing in this scene makes the fire impossible to cut. Also no figure, no
ground shadow, no text.

## Prompt

A single upright server rack stands alone on plain off-white paper, seen
straight on. It is a tall narrow dark cabinet, about twice as tall as it is
wide, its front face divided into a stack of horizontal slots with thin gaps
between them. A few tiny round status marks sit at the left edge of some slots,
in muted blue and muted green only.

Two or three cables leave the lower back of the cabinet and curve loosely down
to the floor, drawn as simple lines in a soft grey.

The rack occupies the right two thirds of the image. The left third is empty
off-white paper with nothing in it at all. Everything rests on one horizontal
ground line. Nothing glows, nothing is lit, and no screen appears anywhere.

## Note on the control section

Used instead of the section above when a control image supplies the composition.
The prose then says only what things are made of, because the picture already
says where they are.

## Prompt with structure

A tall dark server rack alone on plain off-white paper, its front face a stack
of horizontal slots, a few tiny status marks in muted blue and muted green, two
or three soft grey cables curving from its lower back to the floor. Flat even
colour, no glow, no lit screen, no figure, no shadow. The left third of the
image is empty paper.

## Acceptance

The first three decide whether the fire can be cut out of the other drawing at
all. Failing them makes this scene unusable however good it looks.

- No warm colour appears anywhere: nothing orange, nothing yellow, nothing red.
- No screen, panel or indicator glows or is lit.
- The left third is empty paper, edge to edge.

Then the visual system.

- Every filled area is flat. No surface gets lighter or darker across itself.
- The colours are the ones in the spec's Tokens table and no others.
- Any shading present is 45 degree hatching. Nothing casts a shadow on the floor
  and no edge is soft or blurred.
- The background is plain paper and nothing else.
- Nothing in the drawing touches the frame.
- No readable words appear anywhere.

**Budget:** one image per iteration, 1024x1024, PNG. Composition questions at 512.
**Estimated cost:** zero locally, or one hosted image. Both routes are open and
`docs/cost.md` has the numbers.
