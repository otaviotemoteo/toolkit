# Brief: project card, phishing

**Where it lives:** the project card on the home grid, and larger at the top of
the project's own page.
**Type:** drawn diagram, 16:9, on the same paper ground as the other cards.
**The idea in one sentence:** the bait that the benchmark caught every time gets through on real traffic.

**Why a scene and not a screen.** A card image that shows the product's interface
would need text, and a diffusion model cannot write. The card shows the moment
in someone's day where the product matters instead, which needs no words at all.
See `docs/asset-map.md`.

## Prompt

A big fishing hook hangs from a thin dark line that comes down from the top
edge of the picture, and a closed paper envelope is caught on the hook, tilted.
Behind it, a simple flat line chart: a thick smooth line in muted indigo runs
high and level across the left half, then drops steeply toward the bottom right,
the falling part drawn in muted orange. Three thin light grey horizontal guide
lines sit behind the chart.

Plain empty off-white paper around everything, with generous margins.

## Acceptance

- No letters, words or numbers anywhere, including on screens, charts and signs.
- No people. Only the hook, the envelope and the chart.
- Every filled area is flat. No gradients, no glow, no cast shadow.
- Muted, desaturated colours from the spec's Tokens table.
- Plain off-white ground, no walls or scenery beyond the objects named.
- The situation reads in about three seconds at card size, roughly 360px wide.

**Budget:** composition at 768x432, candidates at 1024x576, 16:9.
**Estimated cost:** zero. Local, `IMAGE_BACKEND=local`.

## Recipe

**Not generated. Drawn.** Four seeds of a chart with a hooked envelope over it
came back with the line bent into a worm and the hook floating attached to
nothing, and the four before those were a plain chart that read as nothing at
all. A chart is geometry: every value means something, and a model that cannot
write cannot be trusted to hold a line straight for a reason either. This is the
diagram route in `docs/asset-map.md`, and it is the first asset here to take it.

```bash
python3 scripts/draw_chart.py briefs/card-phishing/approved/card-phishing-v1.png
```

The paper grain is generated from a fixed seed. Two earlier versions lifted it
from an approved card: the first printed that card's whole scene in here as a
ghost, and the second, taking only its high frequencies, printed its outlines
embossed, because the high frequency of a drawing is its edges. Grain is noise,
so grain is made.
