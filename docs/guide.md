# The manual

Every command, in the order you need them. `README.md` is the tour and says why
the thing is built this way; this page says how to use it.

Written for someone arriving from another repository. Nothing here assumes you
have read anything else, and each section links to the lesson behind it for when
you want the reasoning.

| | |
|---|---|
| [1. Install and pick a backend](#1-install-and-pick-a-backend) | getting it to run at all |
| [2. Generate an image](#2-generate-an-image) | the main command |
| [3. Take the green out](#3-take-the-green-out) | the backend's colour cast |
| [4. Cut the background off](#4-cut-the-background-off) | flat art on plain paper |
| [5. Write a brief that works](#5-write-a-brief-that-works) | the rules that were paid for |
| [6. Do not redraw something already approved](#6-do-not-redraw-something-already-approved) | the one that matters most |
| [7. Make it move](#7-make-it-move) | layers, rigs and manifests |
| [8. Verify](#8-verify) | what `make check` proves |
| [9. When it comes out wrong](#9-when-it-comes-out-wrong) | symptom to cause |

---

## 1. Install and pick a backend

```bash
make setup          # venv, runtime and dev requirements
make setup-local    # the Apple Silicon generation stack. Large, and optional
make check          # under a second, needs no key. Run it before you trust anything
```

Copy `.env.example` to `.env` and set `IMAGE_BACKEND`. With no key at all it
still runs: the `fake` backend writes a placeholder, which is enough to see the
assembled prompt and catch most mistakes before spending anything.

| `IMAGE_BACKEND` | What it is | Needs |
|---|---|---|
| `fake` | a placeholder image. The default | nothing |
| `local` | mflux on Apple Silicon | `make setup-local` |
| `local-cn` | the same, with a ControlNet input | `make setup-local` |
| `openai` | OpenAI images | `OPENAI_API_KEY` |
| `gemini` | Gemini images | `GEMINI_API_KEY` |
| anything else | any OpenAI-compatible endpoint | `IMAGE_ENDPOINT`, `IMAGE_API_KEY`, `IMAGE_MODEL` |

A vendor is data here, not code. Adding one is a row in `PROVIDERS` inside
`src/adapters/openai_compatible.py`, or nothing at all plus those three
environment variables. A whole new protocol is a file in `src/adapters/`
implementing `generate()` and `available()`; `fake.py` is the shortest example.

**Check what a backend will ignore, not what it accepts.** Guidance-distilled
models take a negative prompt and throw it away in silence, which deletes half of
a visual system and looks exactly like a badly written brief. Backends that do
this say so, and the CLI prints how many characters of prohibition are about to
be discarded. See `docs/solutions/a-flag-can-exist-and-be-ignored.md` and
`docs/solutions/the-negative-block-was-carrying-the-style.md`.

---

## 2. Generate an image

```bash
# see the whole assembled prompt, generate nothing, spend nothing
./.venv/bin/python src/generate.py briefs/hero-character/brief.md --dry-run

# for real, locally, at no cost
IMAGE_BACKEND=local ./.venv/bin/python src/generate.py briefs/hero-character/brief.md

# a different size or shape
IMAGE_BACKEND=local ./.venv/bin/python src/generate.py briefs/my-asset/brief.md --size 1024x640
```

The image goes to `briefs/<name>/out/` with a JSON sidecar holding the prompt,
the backend, the model and every setting. **The prompt travels with the image.**
An image whose prompt was lost can only be guessed at again, never iterated on.

Useful flags, all optional:

| Flag | For |
|---|---|
| `--init FILE --init-strength 0.8` | start from an existing image instead of from noise |
| `--control FILE --control-strength 0.85` | hold another drawing's structure, leave colour free |
| `--key '#FFFFFF'` | the background colour to ask for |
| `--size 1024x1024` | anything the backend accepts |
| `--backend NAME` | overrides `IMAGE_BACKEND` for one run |

Environment knobs for the local backend: `MFLUX_STEPS` (12 for a draft, 24 for a
candidate), `MFLUX_SEED` to make a run repeatable, `MFLUX_CACHE_GB=2` on a 16 GB
machine to stay off swap.

**512 is for a question, 1024 is for a candidate.** A small fast run answers "did
my change take effect". It lies about likeness, proportion, line and framing, so
never judge acceptance criteria from one and never promote one. See
`docs/solutions/512-answers-some-questions-and-lies-about-others.md`.

---

## 3. Take the green out

Local models tint the paper. The whole image drifts a few units toward green or
blue, and because it drifts the subject too, the eye reads it as a bad scan.

```bash
./.venv/bin/python scripts/postprocess.py in.png out.png --white-balance
```

This removes the cast **each pixel carries**, in Lab, clipped so nothing is ever
pushed past neutral and weighted down on saturated pixels so object colour
survives. A single global shift does not work: the cast is not uniform, and
subtracting the background's cast from everything turns skin grey. See
`docs/solutions/a-colour-cast-is-not-uniform.md`.

Three corrections live in the same script:

| Flag | What it fixes | Safe when |
|---|---|---|
| `--white-balance` | the colour cast | always |
| `--clean-ground` | soft shading the model put on the background | the subject is **not** pale. It eats a white shirt |
| `--snap-palette` | large flat areas drifting off the spec's palette | the areas really are flat |

> **Order matters, and getting it wrong costs the subject.** If you are also
> going to cut the background out, **cut first and correct after**. The cast is
> part of what separates a white shirt from off-white paper: correct it first and
> the two go from fifty units apart to seven, and the cutout swallows the shirt.
> See `docs/solutions/cut-before-you-correct-the-cast.md`.

Correcting rather than re-rolling is the general rule, not a shortcut. Every run
is a fresh sample, so a defect fixed by generating again was fixed by luck and
will be back. See `docs/solutions/correct-the-image-not-the-prompt.md`.

---

## 4. Cut the background off

```bash
./.venv/bin/python scripts/cutout_flat.py in.png out.png --tolerance 3 --erode 2 --trim
```

The background is **not a colour to match, it is the region connected to the
border**. The fill starts at the edges and eats inward through everything that
matches; whatever it cannot reach is the subject. That is why a white t-shirt six
units from the paper it stands on survives, when every "is this pixel white" test
erases the torso.

| Flag | Use it when |
|---|---|
| `--tolerance N` | raise it if background survives in corners, lower it if the subject gets eaten |
| `--erode N` | a pale ring is left around the subject |
| `--feather N` | the edge is too hard for the ground it will sit on |
| `--trim` | you want the file cropped to the subject |
| `--onto FILE` | composite the result onto something straight away |

Chroma key and luminance key were both tried and both failed. What each one
looked like when it broke is in `docs/solutions/the-wrong-keyer.md`.

---

## 5. Write a brief that works

A brief lives at `briefs/<name>/brief.md`. Two headings are required and
`make briefs` fails without them:

- `## Prompt` — sent verbatim as the subject. Everything under it reaches the
  model, nothing else does.
- `## Acceptance` — how you will know it came out right.

One heading is optional: `## Prompt with structure` is used **instead** of
`## Prompt` when you pass `--control`, and it is deliberately much shorter,
because the control image already says where everything goes and the prose only
has to say what things are made of.

Copy `briefs/hero-character/brief.md`. It is the model, and `make briefs` names
it when it fails.

### The rules that were paid for

**Everything has to be in the prompt.** The model has no memory. It receives two
strings and nothing else: not the previous image, not the acceptance criteria,
not the conversation. A requirement that is only in the acceptance list did not
reach it. See `docs/solutions/the-model-has-no-memory.md`.

**Never write a prohibition in the positive block.** "No shading", "without a
shadow", "not cropped" all aim at the thing. Prohibitions belong in the negative
block, which lives once in `docs/ILLUSTRATION_SPEC.md` and is appended automatically.
See `docs/solutions/prohibitions-do-not-belong-in-the-positive.md`.

**Never use a word that is already in the negative block.** Asked for and
forbidden in the same run, it cancels, and what comes out is a half measure of
both. `make briefs` checks every brief against the negative block and fails on a
collision; it has caught `glow`, `frame`, `plants` and `scenery` in real briefs.
See `docs/solutions/never-both-blocks.md`.

**Describe materials and layout, never style.** Line weight, grain, palette and
lighting come from the spec and are appended to every prompt. A brief that says
"flat vector style" is fighting the one place that is supposed to decide it.

**Be concrete about position, and say the negative space out loud.** "A wide gap
of empty paper separates him from the desk, roughly a third of his own body
width" survives. "Next to the desk" does not.

**Split an ask the model cannot do in one go.** Asked for a figure waving, it
drew the gesture correctly and then drew it the size of his head. It can hold the
shape or the scale, not both. Two drawings, each asking for the one thing it does
well, cost nothing extra when the parts end up on separate layers anyway.

**Acceptance criteria have to be observable.** "No filled black area larger than
the character's hair" can be checked. "Looks good" cannot, and a brief nobody can
judge gets a bad result accepted or a good one re-rolled on instinct.

**If the result is wrong, the brief is the first suspect.** Re-running an
unchanged brief and expecting a different image is how credit burns.

**Keep the anchor free of the subject.** Anything in the shared style block is
sent with every asset. A workstation that sat in the anchor turned up in six
profile drafts that had no desk in their briefs, and a line about the character's
clothes would have put his shirt on six strangers.

**Record what you tried, in the brief.** A `## Recipe` section at the bottom
saying which run was used, at what size, with what init, is what makes an asset
reproducible a month later.

---

## 6. Do not redraw something already approved

This is the rule that matters most once there is more than one asset.

A brief cannot pin identity. It specifies what is in the picture, and identity
lives below that: how far apart the eyes sit, where the hairline breaks, how wide
the neck is against the collar. The model resamples all of it on every run, so a
longer brief buys a closer stranger. Thirteen runs of a brief copied clause for
clause from an approved character produced a competent young man who was not him.

So, in this order:

1. **Can the approved drawing be cut to give this?** Cut it.
   `scripts/split_layers.py` finds the joints by measuring rather than by being
   told where they are.
2. **Can the shape be drawn from the approved drawing's own colours?** Draw it.
   A limb in a flat style is a tapered capsule with a round cap at each end, and
   a script lays that down exactly, on colours sampled from the character.
   `scripts/build_contact.py` is a worked example that generates nothing at all.
3. **Only then generate**, and only with `--init` pointing at the approved image,
   never from noise. That is both the correct path and the cheaper one: an init
   skips part of the denoise schedule.

Generation is last because it is the only one of the three that can come back
with somebody else. See `docs/solutions/the-second-drawing-is-a-different-person.md`
and `docs/solutions/pose-variation-is-not-generation.md`.

**Scale between two things from the same drawing is a measurement.** If a
character and a desk were drawn together once, their relative size is already
decided and can be read off the manifest. Choosing it again by eye is how a man
ends up twice the height of his own monitor.

---

## 7. Make it move

Animation here is compositing, not generation. Nothing is generated at run time
and nothing is generated per frame.

```bash
./.venv/bin/python scripts/split_layers.py character.png out/   # body, head, eyes
./.venv/bin/python scripts/build_contact.py                     # the contact loop
./.venv/bin/python scripts/preview_contact.py --frames 18       # judge it as a sheet
```

The output is a set of layers plus a manifest (`scene.json`, `rig.json`) saying
where each goes, what turns about what, and how far. That manifest is the
contract between this repository and whatever renders it. `make scene` and
`make render` check it.

Five things to know before you build a rig:

- **A pivot in pixels is a pivot at one size.** Express `transform-origin` as a
  share of the element's own box, or the head leaves the neck at every size but
  the one you tested. `docs/solutions/a-pivot-in-pixels-is-a-pivot-at-one-size.md`.
- **Zero is down and angles grow clockwise**, which is what CSS does. In a y-down
  system that is `(-sin d, cos d)`. PIL turns the other way, so anything
  previewing in Python negates.
  `docs/solutions/zero-is-down-and-it-turns-the-other-way.md`.
- **A layer holds only the pose it was drawn in.** Draw a limb hanging at rest
  and it falls off the bottom of the canvas and rasterises to nothing; a rotation
  cannot recover pixels that were never written. Draw the pose that is seen and
  store the rig's angles as deltas from it.
  `docs/solutions/a-layer-holds-only-the-pose-it-was-drawn-in.md`.
- **No two layers may share a pixel.** Overlapping cuts of one flat drawing ghost
  the moment they move. `docs/solutions/two-raster-layers-cannot-share-a-pixel.md`.
- **Put the timeline in the manifest, not in both players.** The preview and the
  page have to agree, and a timeline written down twice drifts, which quietly
  turns the contact sheet into evidence about nothing.

**Judge a loop as a sheet, not by reloading.** A browser shows one frame at a
time, so tuning by reload cannot see that the elbow leaves before the shoulder
or that a hand pops into view over open paper. A contact sheet shows the whole
run at once. Anything that must happen out of sight should be checked by
arithmetic as well: `preview_contact.py` prints how far below the desk the wrist
is at each hand swap, rather than trusting the numbers in the timeline.

---

## 8. Verify

```bash
make check
```

Eight checks, under a second, no key:

| Target | What it proves |
|---|---|
| `lint` | style, imports, obvious mistakes |
| `briefs` | every asset has a brief, with a prompt and acceptance criteria, and no word the negative block forbids |
| `anchors` | the positive and negative blocks do not contradict each other |
| `solutions` | every recorded lesson still names a live enforcement, **and that file names the lesson back** |
| `scene` | every scene manifest describes files that exist |
| `render` | every joint lands in the same place at four render sizes |
| `mutation` | every check is watched failing against a fixture broken on purpose |
| `smoke` | the pipeline runs end to end, no key, no cost |

`mutation` is the one worth explaining. A check with a wrong glob and a check
that works look identical in a terminal. So every run also feeds each check a
fixture that must be rejected, and the build fails if one of them passes.

---

## 9. When it comes out wrong

| What you see | What it usually is |
|---|---|
| the paper is green or blue | the backend's cast. `postprocess.py --white-balance` |
| the cutout ate a white shirt | you corrected the cast before cutting. Cut first |
| a thing you forbade keeps appearing | you wrote the prohibition in the positive block |
| a thing you asked for never appears | it is also in the negative block. `make briefs` will say so |
| the style drifted | the backend discards the negative prompt. Distilled models do this silently and say so when they run |
| something appears in every asset that is in no brief | it is in the shared anchor |
| the same brief gives different people | that is sampling, not a bug. Stop generating the subject, start compositing it |
| a layer moved and nothing appeared | the layer rasterised empty. Check its bounding box |
| a joint is right at one size and wrong at another | the pivot is in pixels |
| two parts of one drawing ghost when they move | they share pixels. Cuts have to be exclusive |

---

## Where everything else is

| Path | What is in it |
|---|---|
| `docs/ILLUSTRATION_SPEC.md` | the visual system, and one copy of each prompt anchor |
| `docs/solutions/` | one file per lesson, each naming what enforces it |
| `docs/asset-map.md` | the routes an asset can take, and how to pick one |
| `docs/architecture.md` | the pipeline, and how to add a backend |
| `docs/cost.md` | read before anything that could spend money |
| `docs/decisions.md` | settled questions, so they stay settled |
| `docs/workspace.md` | what is deliberately untracked, and why |
