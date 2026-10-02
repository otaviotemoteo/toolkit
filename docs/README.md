# Docs

Everything under `docs/`, by what you came here to do.

## Use it

| Read | For |
|---|---|
| [`guide.md`](guide.md) | **the manual.** Install, generate, correct, cut, write a brief, build a rig, diagnose |
| [`examples/`](examples/README.md) | four briefs that failed and one that passed, each with its image and its prompt |
| [`ILLUSTRATION_SPEC.md`](ILLUSTRATION_SPEC.md) | the visual system. Mandatory before generating anything |
| [`asset-map.md`](asset-map.md) | whether to generate at all, or to cut, draw or code instead |
| [`cost.md`](cost.md) | what a run costs, in money and in minutes. Read before spending either |
| [`../briefs/`](../briefs/README.md) | thirteen real briefs |

## Change it

| Read | For |
|---|---|
| [`architecture.md`](architecture.md) | the pipeline, and how to add a backend |
| [`decisions.md`](decisions.md) | questions that are settled, and what would reopen each |
| [`workspace.md`](workspace.md) | what is untracked on purpose, when a file you expected is missing |

## Understand why it is built this way

| Read | For |
|---|---|
| [`solutions/`](solutions/README.md) | one file per mistake that cost something, each naming what now prevents it |
| [`history/`](history/README.md) | the notes from each round of iteration: what was asked, what the frames settled |
| [`harness/`](harness/foundations.md) | reading notes on working with coding agents, which gave this repository its shape: one entry file, one check command, a progress file, lessons that name their enforcement |

The three files in `harness/` are notes on other people's work, not rules for
this repository: [`foundations.md`](harness/foundations.md) is the vocabulary,
[`lecture-map.md`](harness/lecture-map.md) is a symptom-to-lecture lookup table,
and [`breakdowns.md`](harness/breakdowns.md) covers what shipped agent products
do that the course does not describe. Every figure in them is its source's
claim, not something measured here.

## A first hour

1. `make setup && make check`, from [`guide.md`](guide.md) section 1.
2. [`examples/README.md`](examples/README.md), top to bottom. Ten minutes.
3. [`guide.md`](guide.md) sections 2 and 5, with
   [`../briefs/hero-character/brief.md`](../briefs/hero-character/brief.md) open.
4. Write `briefs/<your-asset>/brief.md`, run it with `--dry-run`, read the
   prompt, then run it for real.
