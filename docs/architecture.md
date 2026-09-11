# Architecture

Read before adding a backend or changing the pipeline.

## The shape

```
docs/ILLUSTRATION_SPEC.md   the visual system. One copy of each prompt anchor
src/adapters/base.py        the interface. Nothing above it knows which vendor ran
src/adapters/fake.py        placeholder, no key, no cost, no network
src/adapters/local_mflux.py mflux on Apple Silicon, plus the ControlNet variant
src/adapters/openai_backend.py
src/adapters/gemini.py
src/adapters/zenmux.py      never executed. See docs/decisions.md
src/adapters/__init__.py    the registry, selected by IMAGE_BACKEND
src/generate.py             brief plus anchor, sent to the selected backend
scripts/                    the checks, the cutout, the recomposer, the sheet
briefs/<name>/brief.md      one per asset
briefs/<name>/approved/     frozen assets, with the recipe beside each
briefs/<name>/out/          untracked build output, with a sidecar per image
```

## Why the adapter exists

To keep no vendor load-bearing. The dependency is at build time, not runtime:
the assets are static files afterwards and the finished site calls no API at
all. Swapping vendors is one file in `adapters/` plus an environment variable,
and the prompt spec belongs to the project rather than to any provider.

This has already paid for itself three times. Adding Gemini, adding local
generation, and adding ControlNet were each one new file and one registry line,
with nothing above `base.py` touched.

## What a backend must declare

Two methods, `generate()` and `available()`, plus two attributes that exist
because of specific failures:

- `prompt_dialect` decides which anchor the backend is handed. An
  instruction-following model reads prohibitions as prose; a diffusion model
  needs them in a separate negative block, and handing it the prose version aims
  at exactly the words it should avoid.
- `uses_negative` says whether the negative block will actually be applied.
  Guidance-distilled models accept it and discard it in silence, which quietly
  deletes half a visual system. When this is false the CLI prints how many
  characters of prohibition are about to be thrown away.

`fake.py` is the shortest complete example.

## The single copy rule

The style anchors live in the spec and nowhere else. `generate.py` extracts them
by regex at run time, so changing the visual system is one edit rather than a
search through every brief ever written.

The same rule covers the background colour, defined once as `DEFAULT_KEY` in
`generate.py` and read by the smoke test too. The first version of that test
hardcoded its own copy and failed the day the colour changed, which is how the
rule was learned.

## What travels with an image

Every generated image gets a JSON sidecar holding the exact prompt, the negative
prompt, the backend, the model, the dialect, and any init or control image with
its strength. An image whose prompt was lost can only be guessed at again, never
iterated on, and a composite made from another image says so in writing.
