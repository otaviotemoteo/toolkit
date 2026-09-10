# The workspace

This repository is deliberately smaller than the working directory it lives in.
Several files that matter are untracked, and this document is the map of them,
so the way of working can be reconstructed without the files themselves.

Read this if you are an agent picking the project up, or a person deciding what
to recreate.

## Why the split exists

Two kinds of writing accumulate in a project like this and they age at opposite
speeds.

One kind is about **the toolkit**: how a brief is shaped, what the visual system
forbids, why a check exists, what a past mistake cost. It is true for anyone who
clones the repo and it stays true next month. That is tracked.

The other kind is about **this run of the work**: what is done, what is blocked,
what was read last week, drafts, rejected frames. It is real and it is useful,
and asking a stranger to read it is asking them to carry someone else's Tuesday.
That is untracked.

The rule when adding a file: would someone with a different project want this?
If yes, it is tracked. If it only makes sense to whoever is holding this one, it
is not.

## What is untracked, and what belongs in each

### `PROGRESS.md`

Session state. Read at the start of every session, written before the end.

Four sections: current verified state, done, blocked with what unblocks each,
and decisions with dates. Anything decided in conversation and not written here
did not happen.

It is untracked because it describes a moment. A cloned repo starts a new one on
its first session rather than inheriting someone else's.

### `docs/foundations.md`, `docs/harness-map.md`, `docs/breakdowns.md`

Reading notes on harness engineering and on design systems for agents, taken
while setting this project up. `foundations.md` is the vocabulary,
`harness-map.md` is a symptom-to-remedy lookup table, `breakdowns.md` covers
what shipped agent products do that the literature does not describe.

Untracked because they are notes on how we work rather than on how the toolkit
works. Recreate them by reading the sources, not by copying the notes: the value
was in the reading.

### `docs/templates/`

Third-party templates, downloaded verbatim from the harness engineering course
and never adapted. Untracked because they are not ours to redistribute, and
because a template that has been quietly edited is worse than no template.

### `reference/`

Context for the portfolio this toolkit was built to serve: the brief for the
site, the pipeline notes, the six project write-ups. In Portuguese, and specific
to one person's portfolio.

Untracked because none of it is needed to use the toolkit. If you are adapting
this to another project, this directory is where your own equivalent goes.

### `docs/writeups/`

Drafts, posts, and contact sheets about the work. Output about the process
rather than part of it.

### Two files inside `docs/solutions/`

`free-credit-is-a-hypothesis.md` and `subscription-is-not-api-credit.md`. The
rest of that directory is tracked, because each of those lessons explains
something that was committed. These two do not: they are about which accounts to
open and what they cost, no code depends on either, and the transferable part is
already a hard constraint in `CLAUDE.md`. A stranger cloning this does not need
a record of someone else's billing.

### `docs/history/`

The archive of rejected frames and iteration rounds. Has its own README, which
is tracked. See it for the shape of a round.

## What is tracked, and why

| Path | Why it survives a clone |
|---|---|
| `README.md`, `CLAUDE.md` | what this is, and the contract for working in it |
| `docs/ILLUSTRATION_SPEC.md` | the visual system, and the one copy of each prompt anchor |
| `docs/solutions/` | one file per lesson that cost something, each naming what enforces it |
| `docs/workspace.md` | this file |
| `src/`, `scripts/`, `Makefile` | the pipeline, the checks, and the single verification command |
| `tests/fixtures/` | deliberately broken inputs, so every check can be watched failing |
| `briefs/<name>/brief.md` | worked examples of the format the whole system depends on |
| `briefs/<name>/approved/` | approved assets and the recipe that produced each |

Generated images under `briefs/*/out/` are untracked build output. The brief and
the JSON sidecar are what regenerate them, and those are tracked.

## Starting this project fresh

1. `make setup`, then `make setup-local` if you intend to generate locally.
2. `make check`. It should pass in under a second, and it exercises the whole
   pipeline on a backend that costs nothing and needs no key.
3. Create `PROGRESS.md` with the four sections above and fill in what you know.
4. Read `CLAUDE.md`, then `docs/ILLUSTRATION_SPEC.md`, then the index in
   `docs/solutions/`. In that order: the contract, the system, then the scars.
