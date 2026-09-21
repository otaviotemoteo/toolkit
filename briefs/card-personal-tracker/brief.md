# Brief: project card, personal tracker

**Where it lives:** the project card on the home grid, and larger at the top of
the project's own page.
**Type:** static illustration, 16:9, kept on its own paper ground, no cutout.
**The idea in one sentence:** a year of small check-ins adds up to a record you can actually read.

**Why a scene and not a screen.** A card image that shows the product's interface
would need text, and a diffusion model cannot write. The card shows the moment
in someone's day where the product matters instead, which needs no words at all.
See `docs/asset-map.md`.

## Prompt

A person with short curly hair and a muted mustard sweater sits at a small
round table on the right half of the picture, smiling slightly as they tap
their phone. On the left half, a large flat board is divided into a three by
three grid of nine small square panels. Each panel holds one simple flat icon
drawn in muted indigo, muted green, muted orange or muted mustard: a running
shoe, an open book, a dumbbell, a water bottle, a bicycle, a guitar, a pair of
headphones, a sun and a moon. Six of the panels carry a small muted green check
mark in the corner, and one carries a small muted orange cross.

Everything stands on one horizontal ground line on plain empty off-white paper.

## Acceptance

- No letters, words or numbers anywhere, including on screens, charts and signs.
- The people are strangers: none of them is the portfolio's character, and none
  wears his white t-shirt with blue jeans.
- Every filled area is flat. No gradients, no glow, no cast shadow.
- Muted, desaturated colours from the spec's Tokens table.
- Plain off-white ground, no walls or scenery beyond the objects named.
- The situation reads in about three seconds at card size, roughly 360px wide.

**Budget:** composition at 768x432, candidates at 1024x576, 16:9.
**Estimated cost:** zero. Local, `IMAGE_BACKEND=local`.

## Recipe

Generated locally. The first round put the figure alone in the right third with
half the picture empty, and it read as somebody on a phone rather than as this
product. The prompt first gained an easel holding a round chart of twelve wedges, which
is the method the app came from. It read as a painting on a stand rather than as
anything to do with habits. The easel became a board of nine panels, three by
three, each holding one activity, most ticked and one crossed, which is what the
app actually shows. Draft `20260921-161238` chosen: the other three seeds drifted
to four columns and scrambled the icons. Promoted to 1024x576
by passing that draft back in as the init image rather than by reusing its seed:
a seed at another resolution is a different picture. Strength 0.75 still reframed it and drained the green out of the days, so this
one went at 0.85. The looser a picture's composition, the more strength it needs
to survive being enlarged.

```bash
MFLUX_CACHE_GB=2 MFLUX_SEED=11 MFLUX_STEPS=20 IMAGE_BACKEND=local \
  python3 src/generate.py briefs/card-personal-tracker/brief.md --size 1024x576 \
  --init <draft upscaled to 1024x576> --init-strength 0.85
python3 scripts/postprocess.py <that output> approved/card-personal-tracker-v1.png --white-balance
```

The model tinted the whole image, not only the ground, and `--white-balance`
removes that cast. See `docs/solutions/a-colour-cast-is-not-uniform.md`.
`MFLUX_CACHE_GB=2` because at the default 6 this machine went into swap and one
draft took 31 minutes instead of 74 seconds.
