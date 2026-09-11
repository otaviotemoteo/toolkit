# toolkit

Read this first. If anything here contradicts another file, this wins.

**Language.** Reply to the developer in whatever language they write to you in.
Write every repository artefact in English: documentation, check failure
messages, code comments, commit messages. The conversation is theirs; the
repository is for whoever clones it.

## What this is

A tool that generates the illustrations for a portfolio site and outlives it.
A brief says what is in a picture, a spec says how everything is drawn, and the
two are joined and sent to whichever backend is selected.

It produces images, and the layers and manifest that let an image move. It does
not produce a site: `scene.json` is the contract, and `preview/` is a harness
for checking that contract rather than a page anyone ships.

Phase 1 closed with the character approved. Phase 2 closed with the hero
animating, by compositing rather than generation.

## Hard constraints

1. **Nothing is generated without an approved brief.** Every image, animation
   and video.
2. **Say what will change before generating, then wait.** The developer's
   review is the gate that decides whether the work continues. A run fired
   without it is a decision taken in their place.
3. **Acceptance criteria must be observable.** "No filled black area larger than
   the character's hair" qualifies. "Looks good" does not.
4. **Never overwrite an approved asset.** New version, new number, old one stays.
5. **Never propose manual designer work.** No Figma, no vector editing, no path
   cleanup by hand. If a solution needs it, it is the wrong solution: stop and
   propose another.
6. **There is no card.** Warn about cost before spending, and treat any claim of
   free credit as a hypothesis until a real call proves it. See `docs/cost.md`.
7. **A backend that discards the negative prompt cannot hold a visual system,
   though it can propose one.** Never a candidate on its own. See
   `docs/solutions/the-negative-block-was-carrying-the-style.md`.
8. **Check the `status` of every flag the design depends on, not whether it
   exists.** A flag accepted and silently discarded is the most expensive
   failure here, because it looks like a badly written prompt. See
   `docs/solutions/a-flag-can-exist-and-be-ignored.md`.
9. **The model has no memory.** Each run receives two strings and nothing else:
   not the previous image, not the acceptance criteria, not the conversation. A
   requirement absent from the prompt did not reach it. See
   `docs/solutions/the-model-has-no-memory.md`.
10. **512 is for a question, 1024 is for a candidate.** Never judge likeness,
    proportion, line or framing from a draft, and never promote one. See
    `docs/solutions/512-answers-some-questions-and-lies-about-others.md`.
11. **One asset at a time.** Show it and wait.
12. **Read `PROGRESS.md` at the start of every session and update it before the
    end.** What was decided in conversation and is not written there did not
    happen. It is untracked; `docs/workspace.md` says why.
13. **If a result is wrong, the brief is the first suspect.** Rerunning an
    unchanged brief and expecting a different image is how credit burns.
14. **Every lesson that cost something becomes a file in `docs/solutions/`,**
    naming what enforces it, and that thing must name it back. Both directions
    are checked.
15. **Honest assessment over praise.** Say what is wrong before saying what
    works.

## Verification

```bash
make check        # lint, briefs, anchors, solutions, scene, render, mutation, smoke
make setup        # venv and dependencies
make setup-local  # the Apple Silicon generation stack, large
```

`make check` runs in under a second and needs no key. `make mutation` inside it
runs every check against fixtures broken on purpose: if one passes, the check is
what is broken, not the fixture.

Commands for generating an image are in `README.md`. To see the hero move, serve
the repository root and open `preview/index.html`.

## Where to look, and when

| Read | When |
|---|---|
| `PROGRESS.md` | first thing, every session |
| `docs/ILLUSTRATION_SPEC.md` | **mandatory before generating anything** |
| `briefs/<name>/brief.md` | before touching that asset |
| `docs/solutions/README.md` | before proposing something that feels obvious |
| `docs/asset-map.md` | before opening a brief, to pick the route |
| `docs/architecture.md` | before adding a backend or changing the pipeline |
| `docs/cost.md` | before anything that could spend money |
| `docs/decisions.md` | before reopening a settled question |
| `docs/workspace.md` | when an expected file is missing from the repository |

Installed in `~/.claude/skills/`: `oil-visual` gave the spec its structure;
`oil-motion` gave the runtime pattern. Its video and sprite atlas routes do not
apply here, and `briefs/hero-character/motion.md` says why.

## Where we are

Phases 1 and 2 are closed. The character is approved and frozen, the hero
animates from three layers and one rotation, and eight checks run in under a
second. Fourteen lessons are recorded, each naming what enforces it.

**The hero, as built:** an approved drawing, cut by script into a static body, a
head that rotates about the base of the neck, and eyes lifted off the face with
the skin healed behind them. Nothing is generated at run time and nothing is
generated per state. `plate` and `body` are byte-identical in every frame
because they are the same files.

**Next:** the remaining assets. The character is a fixed input for all of them
now, composited rather than redrawn, so identity across the set is a property
rather than a risk.

**Open, with a trigger:** a real head turn needs drawings rather than
transforms, and is deliberately not built. See `briefs/hero-character/motion.md`.
Vectorising the character is the other one, and its trigger has now passed: the
hero closed in raster. See `docs/decisions.md`.

**Gate:** the next asset starts from the approved character, never from noise.
