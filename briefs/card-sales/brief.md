# Brief: project card, sales

**Where it lives:** the project card on the home grid, and larger at the top of
the project's own page.
**Type:** static illustration, 16:9, kept on its own paper ground, no cutout.
**The idea in one sentence:** the owner sees the money arrive while the seller is still with the customer.

**Why a scene and not a screen.** A card image that shows the product's interface
would need text, and a diffusion model cannot write. The card shows the moment
in someone's day where the product matters instead, which needs no words at all.
See `docs/asset-map.md`.

## Prompt

A small shop counter seen from the side. In the foreground a smiling
salesperson in a green apron holds a phone in one hand and hands a paper bag
across the counter to a customer. In the background, raised a little behind
them, a manager sits at a desk and looks at a computer monitor showing a simple
bar chart whose bars step upward from left to right.

The people wear plain clothes in muted indigo, muted green, muted mustard and
grey. Everything stands on one horizontal ground line on plain empty off-white
paper.

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

Generated locally, three seeds at 768x432 and 12 steps, and the draft stamped
`215736` chosen by eye against the acceptance list above. Promoted to 1024x576
by passing that draft back in as the init image rather than by reusing its seed:
a seed at another resolution is a different picture. Strength 0.75 kept the
composition and redrew the detail; 0.55 reinterpreted the scene.

```bash
MFLUX_CACHE_GB=2 MFLUX_SEED=11 MFLUX_STEPS=20 IMAGE_BACKEND=local \
  python3 src/generate.py briefs/card-sales/brief.md --size 1024x576 \
  --init <draft upscaled to 1024x576> --init-strength 0.75
python3 scripts/postprocess.py <that output> approved/card-sales-v1.png --white-balance
```

The model tinted the whole image, not only the ground, and `--white-balance`
removes that cast. See `docs/solutions/a-colour-cast-is-not-uniform.md`.
`MFLUX_CACHE_GB=2` because at the default 6 this machine went into swap and one
draft took 31 minutes instead of 74 seconds.
