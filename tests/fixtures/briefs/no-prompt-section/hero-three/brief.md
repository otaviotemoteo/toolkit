# Brief: fixture with no prompt section

This directory is a fixture. The brief exists but has no section holding the
subject description, so generate.py would have nothing to send and the briefs
check must reject it.

## Acceptance

- The briefs check rejects this directory.
