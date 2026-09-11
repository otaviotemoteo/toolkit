# Approved

Frozen assets. This directory is **not** in `.gitignore`, unlike `../out/`,
because these are decisions rather than build output.

Nothing here is ever overwritten. A new version gets a new number, and the old
one stays: an approved asset that was silently replaced is the one mistake in
this pipeline that cannot be undone.

## hero-character-v1

Approved on 2026-09-07. The recipe, so it can be reproduced or used as
a starting point:

| | |
|---|---|
| backend | `local-cn` |
| model | `mflux-community/z-image-turbo-controlnet-union-2-1-mflux-q4` |
| control | a line drawing of the same scene, `canny` at strength 0.85 |
| seed | 42 |
| steps | 14 |
| size | 1024x1024 |
| brief section | `## Prompt with structure` |

The exact prompt is in `hero-character-v1.json` beside the image. The negative
block was **not** applied: this backend is guidance-distilled and discards it,
which is why the style is flat rather than the hand-drawn line the spec
described before this image changed the spec.

Known defects, accepted at approval rather than overlooked: an orange artefact
between the chin and the collar, odd white shapes where the sleeves meet the
forearms, legs slightly long for the torso, and no clearly readable laptop on
the desk. They were judged smaller than the risk of re-rolling the whole image
to chase them.


## hero-character-v2

Approved on 2026-09-07, and the character the project actually uses.

| | |
|---|---|
| `hero-character-v2-source.png` | the original, 1254x1254, figure alone on white |
| `hero-character-v2-cutout.png` | RGBA, 370x1173, background removed |

**Not produced by this pipeline.** It was generated in ChatGPT, which is the
split this project had already reasoned its way to: the still is a
prompt-adherence problem and an instruction-following model is better at it,
while identity across assets is a compositing problem and belongs here.

The consequence has to be stated rather than glossed: **there is no sidecar and
no prompt for this image**, so it cannot be regenerated or iterated the way
everything else here can. It is a fixed input, not a reproducible output. If it
is ever lost, it is lost. That is the price of the split and it was worth
paying, but it is a real hole in a repo whose first principle is that the prompt
travels with the image.

The cutout comes from `scripts/cutout_flat.py` at tolerance 3, erode 2. On
`PAPER` and `PAPER-DEEP` the edge is invisible. On a dark ground a faint pale
fringe is still visible, inherited from the light stroke in the source art. Not
fixed, because every ground in this project is paper.


## scene/

The hero as the animation consumes it: a plate, three character layers, and a
manifest that says where each goes and what turns about what.

| File | What |
|---|---|
| `plate.png` | the desk, cut out of the approved scene, background removed |
| `body.png` | the figure from the base of the neck down. Never moves |
| `head.png` | everything above, including the neck, with the eyes lifted off |
| `eyes.png` | the two ovals alone |
| `scene.json` | placement, draw order, pivot, and the limits of the motion |

Produced by `scripts/split_layers.py` from `hero-character-v2-cutout.png`, plus
`scripts/postprocess.py` and `scripts/cutout_flat.py` for the plate. Rebuilding
it is a script run, not a decision, which is why only the approved sources are
irreplaceable.

`scene.json` is the contract between this repository and whatever renders the
hero. `make scene` checks it against the files beside it; `preview/index.html`
is the harness that proves it composes.

The cuts and the pivot are not arbitrary and should not be nudged without
reading `docs/solutions/two-raster-layers-cannot-share-a-pixel.md` first. Four
rebuilds are behind them.
