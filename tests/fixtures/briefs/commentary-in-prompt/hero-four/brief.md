# Brief: commentary inside the prompt

Broken on purpose. The note below is addressed to whoever reads the brief, but
it lives under `## Prompt`, so `generate.py` sends it to the model as part of
the description. `make mutation` requires this to be rejected.

## Prompt

A young man stands on plain paper.

**On the section below.** This sentence is a note to the reader and must never
reach the model.

## Acceptance

- Rejected by `scripts/check_briefs.py`.
