# Brief: strip scene, burning

**Where it lives:** panel one of the strip, and collapsing through panel two.
Only the flames survive from this drawing; the rack behind them is thrown away.
**Type:** static illustration, cut afterwards into a single fire layer
**The idea in one sentence:** the same machine, on fire, so the flames can be
lifted off it.

**Why the rack is drawn again and then discarded.** The flames have to sit on
the rack correctly, wrapping its edges and rising from the right places, and a
model asked for flames on plain paper draws flames that belong to nothing. So
the whole burning scene is generated, and the fire alone is taken out of it. The
rack that ships is always the one from `briefs/strip-scene/`, unchanged, which
is what makes the three panels the same place.

**How the fire is separated:** by colour, not by hand. Every colour in this
system is cool and muted except two, and the calm scene is forbidden from using
either. So in this drawing, warm equals fire. It is a mechanical selection with
nothing to judge.

**Reference and control image:** the approved calm scene. Pass it as the control
so the rack lands in the same place and at the same size. If the rack shifts,
the flames still work, because only the flames are kept.

**Framing:** square, 1024x1024, matching the calm scene. Left third empty.

**Required:** the same rack, with flames rising from its slots and licking up its
sides. Flames drawn flat, in `#C77D5A` and `#C9A34E`, as clean rounded tongues
with no gradient and no glow.

**Forbidden:** smoke, sparks, embers, light spilling onto the paper, any warm
tint on the rack itself or on the ground. A warm pixel that is not a flame ends
up in the fire layer and then floats in the panel with nothing under it.

## Prompt

A tall dark server rack stands alone on plain off-white paper, seen straight on,
and it is on fire. Flames rise from the gaps between its horizontal slots and
lick up both of its sides, reaching a little above the top of the cabinet. The
flames are drawn as clean rounded tongues of flat colour, warm orange with paler
yellow centres, with no glow around them and no blending inside them.

The rack occupies the right two thirds of the image. The left third is empty
off-white paper with nothing in it at all. Everything rests on one horizontal
ground line.

There is no smoke and there are no sparks. The paper around the flames stays the
same plain off-white it is everywhere else, with no warm tint and no light
spilling onto it. The cabinet itself stays dark and unlit.

## Note on the control section

Used instead of the section above when the calm scene is passed as the control
image, which is the normal case here.

## Prompt with structure

The same dark server rack, on fire. Flames rising from the gaps between its
slots and up both sides, drawn as rounded tongues of flat warm orange with paler
yellow centres, no glow, no blending, no smoke, no sparks. The cabinet stays
dark and unlit, the paper around it stays plain off-white with no warm tint.

## Acceptance

The first four decide whether the fire can be lifted off the drawing. Failing
them makes the whole image unusable.

- The only warm pixels in the image are flames. Nothing orange or yellow appears
  on the rack, on the cables, on the ground line or on the paper.
- The flames have hard edges. No glow, halo or soft falloff anywhere around them.
- The flames read as a connected group rising from the rack, not as scattered
  specks that would leave holes when lifted.
- There is no smoke and there are no sparks.

Then the visual system.

- Every filled area is flat, the flames included.
- The colours are the ones in the spec's Tokens table and no others.
- The background is plain paper and nothing else.
- No readable words appear anywhere.

## Recipe

```bash
# 1. the calm scene, approved first and never regenerated after that
# 2. this drawing, with the calm scene as the control image
# 3. lift the flames out by colour
python3 scripts/lift_fire.py briefs/strip-fire/approved/burning-v1.png \
    briefs/strip-fire/approved/fire.png
```

The fire layer composites over the calm scene. Panel two is not a drawing: it is
the fire layer collapsing toward the ground line, driven by scroll, until it is
the accent rule that carries into the project grid.

**Budget:** one image per iteration, 1024x1024, PNG.
**Estimated cost:** zero locally, or one hosted image.
