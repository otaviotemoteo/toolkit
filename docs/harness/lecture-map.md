# Harness lecture map

A lookup table, not a summary. The ten lectures not read in full live here so that
when a symptom shows up the right one gets opened, instead of the whole course
getting re-read. Read [`foundations.md`](foundations.md) for the ideas; read this when something is
going wrong.

The WHEN column is judged against one context: one developer, one personal
project, reviewing everything by hand, no parallel agents and nothing running in
the cloud.

Base URL for every link: `https://walkinglabs.github.io/learn-harness-engineering/en/lectures/`
(swap `/en/` for `/pt-BR/` for Brazilian Portuguese.)

| Symptom, as it actually shows up | Lecture | Remedy in one line | When |
|---|---|---|---|
| "This model is not good enough, I should pay for a bigger one." | 01, [why capable agents still fail](https://walkinglabs.github.io/learn-harness-engineering/en/lectures/lecture-01-why-capable-agents-still-fail/) | Before changing model, walk five layers: unclear task, missing context, broken environment, no verification, lost state. | NOW |
| "I explained that yesterday and it does not know it today." | 03, [the repository as system of record](https://walkinglabs.github.io/learn-harness-engineering/en/lectures/lecture-03-why-the-repository-must-become-the-system-of-record/) | Anything decided in conversation gets written to a file near the code it affects. Stale docs are worse than none, because they mislead with authority. | NOW |
| "I started a new session and it re-explored the project for fifteen minutes." | 05, [long-running tasks lose continuity](https://walkinglabs.github.io/learn-harness-engineering/en/lectures/lecture-05-why-long-running-tasks-lose-continuity/) | Progress file plus a decision log plus git checkpoints. Target: a new session is productive within three minutes. | NOW |
| "Every session starts with ten minutes of figuring out how to run things." | 06, [initialization needs its own phase](https://walkinglabs.github.io/learn-harness-engineering/en/lectures/lecture-06-why-initialization-needs-its-own-phase/) | Split setup from work. Init ends when the project can start, test, show progress, and name the next task. | NOW |
| "I asked for one thing and got twelve files changed, none of it finished." | 07, [agents overreach and under-finish](https://walkinglabs.github.io/learn-harness-engineering/en/lectures/lecture-07-why-agents-overreach-and-under-finish/) | WIP equals one, scope written in a file rather than said in chat, and completion proven by a command that runs. | NOW |
| "It said the feature was done and half of it is missing." | 08, [feature lists are harness primitives](https://walkinglabs.github.io/learn-harness-engineering/en/lectures/lecture-08-why-feature-lists-are-harness-primitives/) | Every item carries three fields: what it does, the command that proves it, and its current state. Only the command flips the state. | LATER |
| "Every piece works and the whole thing does not." | 10, [end-to-end testing changes results](https://walkinglabs.github.io/learn-harness-engineering/en/lectures/lecture-10-why-end-to-end-testing-changes-results/) | Only a full pipeline run counts as verified. Architecture rules become checks that run, and failure messages carry the fix. | NOW |
| "It ran a long time, something broke, and it cannot say what happened." | 11, [observability belongs inside the harness](https://walkinglabs.github.io/learn-harness-engineering/en/lectures/lecture-11-why-observability-belongs-inside-the-harness/) | Two kinds of trace: runtime signals for what happened, written artifacts for why it was decided. | LATER |
| "I am typing the same three instructions every day." | 13, [loop engineering](https://walkinglabs.github.io/learn-harness-engineering/en/lectures/lecture-13-loop-engineering/) | A goal, a verification, a stop condition. Then watch for verification debt and comprehension rot, which accumulate quietly. | LATER |
| "I have several loops and no idea which one broke." | 14, [graph engineering](https://walkinglabs.github.io/learn-harness-engineering/en/lectures/lecture-14-graph-engineering/) | Make dependency, veto authority and stable metrics explicit before drawing anything. | NOT YET |

## Notes on the LATER and NOT YET rows

**08** is marked LATER rather than NOW because this repo already has the shape by
accident: `briefs/<name>/brief.md` carries a description and an `## Acceptance`
section, which is two of the three fields. What is missing is the third, a state
that only a command can change. Promote it when there are enough assets that
their status stops fitting in one head.

**11** is LATER for the same reason: the pipeline is one Python file and a JSON
sidecar next to every image, which is already a process artifact. Observability
becomes worth building when a run is long enough that watching it is not an
option.

**13** presupposes trusting an agent to work unattended, which is explicitly not
where this project is. **14** presupposes 13.

Nothing here is marked DOES NOT APPLY. The two that came closest, 13 and 14, are
not irrelevant, they are premature, and the distinction matters: a graph is a bad
answer today and might be a good one later, whereas the team-scale practices
listed at the end of `foundations.md` are answers to a problem this project will
never have.

## The one to read in full first

**Lecture 07.** The other nine either overlap with the four already read in depth
or describe problems this project does not have yet. 07 does not overlap, and its
failure mode is the one that costs a solo reviewer the most: work that looks
substantial, touches many files, and cannot be verified, which is exactly the
kind of output that is expensive to review and tempting to accept.
