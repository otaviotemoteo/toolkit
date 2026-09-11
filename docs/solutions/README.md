# Solutions

One file per lesson that cost something to learn. Not a changelog and not a
diary: `PROGRESS.md` says what is happening now and gets pruned, these say what
is true and stay.

**What earns a place here rather than in a working note.** A lesson is tracked
when something committed depends on it: a check, a piece of the pipeline, a rule
in the spec or the contract. Delete `never-both-blocks.md` and
`scripts/check_anchors.py` becomes a script nobody can justify. Delete
`the-wrong-keyer.md` and `scripts/cutout_flat.py` looks needlessly clever.

A lesson about which account to open, or what a vendor charged on a Tuesday, is
not that. Two of those exist and are kept locally rather than committed;
`docs/workspace.md` lists them. The session log they refer to is untracked for
the same reason.

The rule for putting something here: it was wrong, it is now right, and the
reason it was wrong will still be a live temptation in three months. If a lesson
only matters this week, it belongs in `PROGRESS.md` and should die with it.

**The link runs both ways, and both directions are checked.** The frontmatter
names what enforces a lesson, and that file has to name the lesson back. A
pointer that only runs outward rots from the end nobody reads: the script is
what gets edited a month later, and if it does not mention the lesson, the
reasoning is one rename away from unreachable.

Every file ends with **Where it is enforced**, and the answer has to be one of
three, in this order of preference:

| Enforced by | Use when |
|---|---|
| a check | the mistake is mechanically detectable |
| a spec or contract rule | it needs judgment but has a stable shape |
| prose here only | it is a fact about the world, not about this repo |

A lesson that stays in prose when it could have been a check is a lesson that
will be learned again.

| File | One line |
|---|---|
| `a-flag-can-exist-and-be-ignored.md` | `--negative-prompt` is silently discarded by distilled models |
| `never-both-blocks.md` | a word in the positive and the negative cancels itself |
| `prohibitions-do-not-belong-in-the-positive.md` | writing "no shading" aims at shading |
| `the-wrong-keyer.md` | chroma key, luminance key, and why neither survived |
| `documentation-can-contradict-the-api.md` | the docs said PNG, the API said 400 |
| `pose-variation-is-not-generation.md` | identity cannot be bought with speed |
| `512-answers-some-questions-and-lies-about-others.md` | cheap runs answer one kind of question only |
| `the-model-has-no-memory.md` | drift is sampling, not inconsistency |
| `the-negative-block-was-carrying-the-style.md` | a distilled model cannot hold this style at all |
| `two-raster-layers-cannot-share-a-pixel.md` | overlapping cuts of one drawing ghost when they move |
| `correct-the-image-not-the-prompt.md` | a mechanical defect deserves a mechanical fix |
| `a-pivot-in-pixels-is-a-pivot-at-one-size.md` | a coordinate is meaningless without its space |
| `clean-ground-cannot-see-an-outline-that-is-not-there.md` | a pale subject is continuous with the paper |
