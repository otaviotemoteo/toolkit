# Brief: project card, phishing

**Where it lives:** the project card on the home grid, and larger at the top of
the project's own page.
**Type:** static illustration, 16:9, kept on its own paper ground, no cutout.
**Fallback:** `scripts/draw_chart.py`, the drawn version, if a chart is ever wanted.
**The idea in one sentence:** the bait comes down the line and something has to stand in front of the inbox.

**Why a scene and not a screen.** A card image that shows the product's interface
would need text, and a diffusion model cannot write. The card shows the moment
in someone's day where the product matters instead, which needs no words at all.
See `docs/asset-map.md`.

## Prompt

An open laptop stands in the middle of the picture, seen from the front, its
screen pale and holding one large closed paper envelope. From the top edge of
the picture a thin dark line comes down with a fishing hook on the end of it,
hanging just above the envelope. Two small friendly robots stand on the desk on
either side of the laptop, facing the hook with their arms raised toward it,
blocking it. The robots are simple flat shapes: a rounded body in muted indigo,
a round head with a single dot eye, and a short antenna.

Everything stands on one horizontal ground line on plain empty off-white paper.

## Acceptance

- No letters, words or numbers anywhere, including on screens, charts and signs.
- No people. The robots are objects, with no faces beyond one dot eye each.
- Every filled area is flat. No gradients, no glow, no cast shadow.
- Muted, desaturated colours from the spec's Tokens table.
- Plain off-white ground, no walls or scenery beyond the objects named.
- The situation reads in about three seconds at card size, roughly 360px wide.

**Budget:** composition at 768x432, candidates at 1024x576, 16:9.
**Estimated cost:** zero. Local, `IMAGE_BACKEND=local`.

## Recipe

Generated locally, four seeds at 768x432 and 12 steps, draft `20260921-162753`
chosen, promoted at strength 0.85, then `--white-balance`.

**The two dead ends before it are the point.** A plain chart read as nothing. A
chart with a hooked envelope over it bent the line into a worm and left the hook
attached to nothing, four seeds running. Both were the same mistake: asking a
model for a picture whose meaning lives in exact geometry. `scripts/draw_chart.py`
exists because of that, and it draws a correct, dull chart that is kept as the
fallback here.

What replaced them is not a chart at all. The card shows the bait coming down
the line at an inbox and two small robots standing in front of it, which is what
the project is for rather than what its results table looks like. A scene the
model can invent beats a diagram it has to get right.
