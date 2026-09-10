# toolkit

A small set of tools for generating illustrations that come out looking like one
system instead of like six different afternoons.

**In one sentence:** you write a brief describing what should be in the picture,
and it produces an image in a visual system defined once, from whichever image
model you have credit with.

---

## What it's for

Generating illustration for a project is easy to start and hard to keep
consistent. The first image is fine. The fourth has a different line weight, the
sixth picked up a gradient somewhere, and by the tenth the set no longer reads as
belonging to the same hand. The usual fix is a designer, and the second usual fix
is doing it by hand in a vector editor, which is the same fix with more evenings.

This takes the other route: the visual system is written down once, in one file,
and appended to every prompt automatically. A brief says what is in the scene.
The style says how everything is drawn. Neither one can drift into the other.

The trade is that it will not draw anything outside its own system. There is one
palette, one texture, two line weights, and a rule that colour appears only on
things that are running or moving. Asked for something warmer or softer or more
detailed, the honest answer is that the system has to change first, in the file,
where the change applies to everything already made. That is a real limitation
and it is also the entire point.

## What you actually do with it

**Once, at the start.** Write the visual system in `docs/ILLUSTRATION_SPEC.md`:
the colours, the texture, what is never allowed. There is exactly one copy of
the style block, and every generated image gets it appended.

**Per illustration.** Write a brief: where it lives, what must be in it, what
must not, and how you will know it came out right. Run it with no backend
configured to see the assembled prompt and a placeholder, which costs nothing
and catches most mistakes. Then run it for real.

**When something is wrong.** Change the brief, not the seed. The result lands in
a versioned file with the exact prompt saved beside it, so the next attempt
starts from what was actually sent rather than from memory.

## The ideas behind it

- **The style lives in one place and the subject lives in another.** A brief
  describes a scene and never describes a line weight. Changing the visual system
  is one edit, not a search through every brief ever written.
- **No vendor is load-bearing, and none is required.** Generation sits behind a
  single interface chosen by an environment variable, and the default real
  backend runs on your own machine through mflux, with no account, no quota and
  no cost. Hosted backends are there for when an instruction-following model is
  the better tool, not because anything depends on one.
- **A backend declares what it will ignore.** Guidance-distilled models accept a
  negative prompt and discard it in silence, which quietly deletes half of a
  visual system. Backends that do this say so, and the CLI prints how many
  characters of prohibition are about to be thrown away.
- **The default backend costs nothing and calls nobody.** It produces a
  placeholder, which means the whole path can be exercised before any key exists,
  and a broken pipeline can be told apart from a broken prompt.
- **The prompt travels with the image.** An image whose prompt was lost can only
  be guessed at again, never iterated on.
- **Nothing approved is ever overwritten.** Filenames are timestamped. The one
  mistake here that cannot be undone is silently replacing a good asset.

- **Every lesson names what enforces it.** `docs/solutions/` holds one file per
  mistake that cost something, each declaring whether a check, a spec rule or
  plain prose is what stops it happening again. A check that no longer exists
  fails the build, because a rule pointing at a deleted enforcement reads like a
  guarantee and is a memory.

## Where the images go

Into `briefs/<name>/out/`, next to the brief that produced them, with a JSON
sidecar holding the prompt, the backend, the model and the settings.

The images themselves are build output and are not committed. The brief and the
sidecar are, because those are what regenerate the image. If a specific asset
should be versioned, add it explicitly.

---

## For developers

```bash
make setup          # venv, runtime and dev requirements
make setup-local    # the Apple Silicon generation stack, large

# see the assembled prompt, generate nothing, spend nothing
./.venv/bin/python src/generate.py briefs/hero-character/brief.md --dry-run

# placeholder, no key and no model needed
./.venv/bin/python src/generate.py briefs/hero-character/brief.md

# for real, locally, at no cost
IMAGE_BACKEND=local ./.venv/bin/python src/generate.py briefs/hero-character/brief.md

# hold the structure of an existing drawing, leaving colour free
IMAGE_BACKEND=local-cn ./.venv/bin/python src/generate.py briefs/hero-character/brief.md \
    --control reference-drawing.png --control-strength 0.85

make check          # lint, briefs, anchors, solutions, mutation, smoke
```

`make check` runs in under a second and needs no key. It includes deliberately
broken fixtures, so every check is watched failing on every run: a check with a
wrong glob and a check that works are indistinguishable in a terminal otherwise.

| Path | What's in it |
|---|---|
| `docs/ILLUSTRATION_SPEC.md` | the visual system, and one copy of each prompt anchor |
| `docs/solutions/` | one file per lesson, each naming what enforces it |
| `docs/workspace.md` | what is deliberately untracked, and what belongs there |
| `src/adapters/` | one interface, one backend per file, chosen by `IMAGE_BACKEND` |
| `src/generate.py` | brief plus anchor, sent to whichever backend is selected |
| `scripts/` | the checks, the cutout, the recomposer, the contact sheet |
| `briefs/<name>/approved/` | approved assets, with the recipe beside each |

Adding a backend is a file in `src/adapters/` implementing `generate()` and
`available()`, plus a line in the registry. `fake.py` is the shortest example.

Python 3.11, Pillow and numpy. Local generation uses
[mflux](https://github.com/mflux-community/mflux) on Apple Silicon. Background
removal is `scripts/cutout_flat.py`, which treats the background as the region
connected to the border rather than as a colour to match, so a white shirt on
off-white paper survives it.

The spec format is structurally modelled on
[oil-visual](https://github.com/oil-oil/oil-visual) (MIT). The visual system here
is unrelated to theirs.
