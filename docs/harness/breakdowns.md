# What real harnesses do that the course does not teach

Notes on the course's breakdowns of Pi, Claude Code, Codex and DeepSeek. What
appears in the products but not in the lessons, and what fits one developer.

## Six things the products do that the lectures do not say

**Instruction scope follows the directory tree.** Pi, Claude Code and Codex all
resolve instructions global, then parent directory, then current directory, most
specific loaded last. The course splits the entry file by topic; this splits it
by location. Different axes: a document that only applies inside `briefs/` can
live inside `briefs/`.

**Enforcement moves from prose into the runtime.** Claude Code puts task
boundaries in a permission system and in `PostToolUse` and `Stop` hooks; Codex
puts isolation in a worktree. The course says prefer executable rules. These go
further: the boundary is a property of the environment, so crossing it is
impossible rather than discouraged.

**Compaction is a staged pipeline, not one summary.** Lossless pruning, then
structured distillation, then model summarisation, with a circuit breaker. Pi
refuses the problem and branches the session into a tree instead.

**Replayability is stated as an invariant.** DeepSeek's phrasing is the sharpest:
anything that reached the model must be reconstructable from the log. Lecture 11
asks for observability, which is a goal. This is a testable property.

**Responsibilities split by artifact type, not by subject.** Instructions say
what, skills say how, connectors say where, hooks say when. That split predicts
where a new rule belongs; a `docs/` folder cut by theme does not.

**Only the environment delta is re-sent.** Codex emits the fields that changed
instead of repeating the context each turn. Pure token economics, absent from the
lectures, and the kind of thing that surfaces only once someone pays the bill.

## What fits here

Three of the six, and one is free today.

**Hooks.** Already supported in this setup. A `Stop` hook running the
verification command is the cheapest form of externalised termination: the
session cannot end while the check fails. Highest-value item on this page, and it
belongs in step 5 or step 7.

**Directory-scoped instructions.** Cost nothing, and keep the entry file small.

**Replayability as an invariant.** Half-built by accident already: every
generated image writes a JSON sidecar with the exact prompt. Naming it as a rule
turns a habit into something a check can enforce.

The other three are not advanced, they are answers to absent problems: worktrees
solve contention between concurrent tasks, plugin architectures solve extension
by strangers, permission classifiers solve trust at a scale where reading every
diff is impossible.

## One aside about the templates

The course's templates were the better half of this reading. They are not
redistributed here; they live at `docs/en/resources/templates` in
`walkinglabs/learn-harness-engineering`. `AGENTS.md` is 55 lines
and already answers most of what steps 4, 6 and 7 set out to write from scratch,
and `feature_list.json` is lecture 08 as a file instead of an argument.
