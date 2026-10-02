# Foundations

Reading notes on three sources about how to work with coding agents. This is not
a plan and not a set of rules for this repo; it is the vocabulary the rest of the
harness documents are written in. Every percentage below is a claim made by its
source, not something measured here.

Sources: the Harness Engineering course (lectures 02, 04, 09, 12), the Every
guide on compound engineering, and Vercel's post on `design.md`.

## The five subsystems

The course's frame: a harness is everything outside the model weights, and a
missing subsystem is a hole nothing else compensates for.

1. **Instructions.** The file the agent reads first: purpose, stack, hard
   constraints, and pointers out. About 100 lines, a directory rather than an encyclopedia.
2. **Tools.** Enough access to actually act: shell, package manager, test runner,
   granted at least privilege.
3. **Environment.** The runtime made self-describing: lockfiles, pinned versions,
   a container if the thing has to run anywhere else.
4. **State.** Continuity across sessions, usually one `PROGRESS.md`: done, in
   flight, blocked. Read at the start, written before the end.
5. **Feedback.** The verification commands, named explicitly in the instructions
   so the agent runs them instead of guessing.

Two lines from the course worth keeping literally. Anything the agent cannot see
does not exist, which is why the repository has to be the record. And feedback is
the cheapest subsystem to build and the one that pays back first.

## The compound loop

1. **Plan.** Turn a request into a written blueprint before any code exists.
2. **Work.** Execute the plan, in isolation, tracking progress as you go.
3. **Review.** Assess the result against dimensions the author was not thinking
   about while writing it.
4. **Compound.** Write the lesson somewhere permanent so the same correction is
   never given twice.

The claimed split is 80% on planning and review, 20% on doing and recording. The
whole argument rests on step 4: a fix that stays in the conversation is a fix
that gets re-earned next month.

## The three layers

Vercel's system separates what an agent needs to know into three artifacts that
fail differently:

- **Prose** (`design.md`). Judgment that cannot be reduced to a value: hierarchy,
  what to lead with, what to leave out. Also, explicitly, the names of the
  patterns to avoid.
- **Stylesheet and tokens.** The mechanics as usable primitives, loaded at render
  time rather than read into context, so the token budget goes to judgment.
- **Evaluation.** Deterministic checks for the mechanical failures, human
  judgment for the rest, with fixed scenarios so the guidance is the only
  variable that moves.

## Where the three agree

They use different vocabulary for the same five ideas.

- **The repository is the memory.** State subsystem, `CLAUDE.md` plus
  `docs/solutions/`, a public file at a stable URL. Same claim: if it is not a
  file, it will not survive the session.
- **A correction goes to the narrowest layer that can enforce it.** The course
  says prefer executable constraint to enumerated instruction; compound says
  encode taste in systems instead of catching it in review; Vercel routes each
  accepted fix to prose, stylesheet, or a deterministic check. Three phrasings of
  one triage.
- **The entry file is scarce, not free.** All three treat the always-loaded
  document as a budget being spent, and all three push detail outward.
- **Done is not decided by the one who did it.** Externalised termination in the
  course, parallel review agents in compound, blind comparison in Vercel.
- **Naming a failure makes it avoidable.** Vercel says it outright about
  anti-patterns; the course's actionable error messages and compound's tagged
  solution docs are the same move applied to runtime and to memory.

## Where they disagree

- **Autonomy.** Compound is the outlier: its stage 5 has agents proposing work
  unprompted, and it treats supervision as the bottleneck to remove. The course
  spends a whole lecture on the fact that agents mis-report completion, and
  Vercel keeps a human deciding what enters the system. Compound answers this
  with safety nets rather than review, which is a bet on coverage, not an
  agreement.
- **Parallelism.** Compound runs 14 review agents on a pull request and 40 for a
  deep plan. Vercel describes one agent and a review harness. The course barely
  raises it before lectures 13 and 14. This is the largest structural difference
  between the three.
- **Where judgment lives.** Vercel is the most confident that prose can carry
  taste, and also the most honest about the cost: different models read the same
  paragraph differently, so the mechanics had to move into a stylesheet and the
  known failures into checks.
- **Evidence.** The course cites clean progressions (20 to 60 to 80 to 100
  percent as subsystems are added; 45 to 72 percent after splitting a bloated
  instruction file). Vercel reports 39 failures against 91 and then says six
  pages are too small a sample to claim quality improved. The numbers point the
  same way, but only one source states its own uncertainty, and that difference
  in candour is worth more than either figure.

## Ideas that appear in only one source

Flagged because convergence is easy to hallucinate.

- **Position inside the file matters** (course, lecture 04). A constraint at line
  300 of 600 is very likely ignored; hard rules go at the top or the bottom.
- **Ablation** (course, lecture 02). Remove one subsystem at a time and measure
  the drop, to find out which one is actually carrying the work.
- **The five conditions for a clean session** (course, lecture 12): build passes,
  tests pass, progress recorded, no stale artifacts, next session can start
  without manual setup.
- **Naming anti-patterns explicitly** (Vercel).
- **Fixed scenarios with the guidance as the only variable** (Vercel).
- **Solution documents with metadata, written to be found later** (compound).
- **Separating the worker from the checker as different agents** (course,
  lecture 09).

## Does not apply to me

One person, one project at a time, reviewing everything, no team and no cloud.

- **Agent fleets.** Fourteen reviewers in parallel is a way of buying back
  attention a team does not have. I am the second reviewer, and I am reading
  everything anyway.
- **Worktree isolation and parallel features.** Solves contention between people
  or between concurrent tasks. There is neither here.
- **Stage 5 autonomy.** Presupposes trust that has not been earned yet, and the
  monitoring to catch it when it is misplaced.
- **Weekly complaint aggregation.** Needs a population of users producing
  complaints. There is one user.
- **Per-module quality scorecards.** Useful across dozens of modules; noise
  across four files.
- **Ablation, for now.** The most rigorous exercise in the course and the most
  expensive: it means running the same battery of tasks repeatedly. Worth doing
  once there is a repeatable battery and a harness mature enough to make the
  question interesting.
- **Loop and graph engineering** (lectures 13 and 14). They assume the autonomy
  described above.
