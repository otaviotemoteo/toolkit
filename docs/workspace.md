# The workspace

What is in the working directory and not in the repository, and why. Read this
when a file a document mentions is not there.

## The rule

**Every document is tracked. What is not tracked is output and session state.**

A document is anything written to be read: a brief, a lesson, a set of notes, a
recipe. If it is worth keeping it is worth showing, and if it is not worth
showing it is deleted rather than hidden. An earlier version of this repository
kept a second, private layer of notes beside the public one, and the two drifted:
tracked files ended up pointing at files only one machine had.

Output is anything a command produced: a generated image, a cut layer, a contact
sheet. It is untracked because it is large, because it can be rebuilt, or because
it belongs to one particular site rather than to the toolkit.

## What is untracked

### `briefs/<name>/out/`

Every run of `src/generate.py` lands here: the image and its JSON sidecar. Most
runs are rejected, so most of this directory is waste, and it grows without
bound. A run that is approved is copied, image and sidecar together, into
`briefs/<name>/approved/` under a new version number.

### `briefs/<name>/approved/`, for every asset except `hero-character`

The approved images of the portfolio this toolkit was built for: six project
cards, a three panel strip, a contact greeting, a walking profile, two desks.
`.gitignore` names each directory.

Their briefs are tracked, because a brief is a document and twelve real ones
teach the format better than one. Their images are not, because they are one
person's site: forty pictures a stranger would download to learn nothing the
briefs and the lessons do not already say. So a brief here may name a file under
its own `approved/` that a clone does not have. That is expected, and
`briefs/README.md` says which briefs those are.

One asset keeps its images, as the worked example: `briefs/hero-character/`.
`docs/examples/` walks through it.

Your own approved assets are tracked like any other file. Nothing in
`.gitignore` matches a directory you create.

### `briefs/<name>/approved/layers/`

The raw output of `scripts/split_layers.py`. It is assembled into
`approved/scene/`, which is tracked, and rebuilding it from the approved cutout
takes a second.

### `preview/strip.html`

A harness page that composes three of the untracked assets and nothing else.
`preview/index.html`, which composes the hero, is tracked.

### The pictures in `docs/history/`

Each round of iteration has a directory there with a `notes.md`, which is
tracked, and the frames the notes talk about, which are not. Four frames of the
first round are tracked as copies under `docs/examples/hero-first-pass/`,
because they are the worked example of a bad brief.

### `PROGRESS.md`

Session state. Read at the start of every session, written before the end.

Four sections: current verified state, done, blocked with what unblocks each,
and decisions with dates. Anything decided in conversation and not written here
did not happen.

It is the only document that is untracked, because it describes a moment rather
than the toolkit. A cloned repository starts a new one on its first session
instead of inheriting someone else's. Anything in it that stays true for longer
than a week belongs in `docs/decisions.md` or `docs/solutions/`, and gets moved
there.

## What is tracked, and why

| Path | Why it survives a clone |
|---|---|
| `README.md`, `CLAUDE.md` | what this is, and the contract for working in it |
| `docs/README.md` | the index of everything under `docs/` |
| `docs/guide.md` | the manual |
| `docs/examples/` | one asset's first round, bad briefs to approved, image by image |
| `docs/ILLUSTRATION_SPEC.md` | the visual system, and the one copy of each prompt anchor |
| `docs/solutions/` | one file per lesson that cost something, each naming what enforces it |
| `docs/harness/` | reading notes on working with coding agents, which is where this repository's shape came from |
| `docs/history/*/notes.md` | what each round of iteration was asking and what it settled |
| `src/`, `scripts/`, `Makefile` | the pipeline, the checks, and the single verification command |
| `tests/fixtures/` | deliberately broken inputs, so every check can be watched failing |
| `preview/` | the harness that proves a scene manifest composes |
| `briefs/<name>/brief.md` | thirteen real briefs |
| `briefs/hero-character/approved/` | the worked asset: images, sidecar, recipe and rig |

## Starting this project fresh

1. `make setup`, then `make setup-local` if you intend to generate locally.
2. `make check`. It should pass in under a second, and it exercises the whole
   pipeline on a backend that costs nothing and needs no key.
3. Create `PROGRESS.md` with the four sections above and fill in what you know.
4. Read `CLAUDE.md`, then `docs/ILLUSTRATION_SPEC.md`, then the index in
   `docs/solutions/`. In that order: the contract, the system, then the scars.
5. Read `docs/examples/`, then write your first brief with `docs/guide.md` open.
