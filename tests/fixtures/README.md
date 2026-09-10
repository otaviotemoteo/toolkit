# Mutation fixtures

Deliberately broken inputs. `make mutation` runs each check against its own
fixtures and fails if any of them passes.

| Directory | Check it must defeat |
|---|---|
| `briefs/` | `scripts/check_briefs.py` |
| `anchors/` | `scripts/check_anchors.py` |
| `solutions/` | `scripts/check_solutions.py` |

A check nobody has watched fail is indistinguishable, in the terminal, from a
check with a wrong glob: both print nothing and exit zero. These exist so that
difference is visible on every run.

The two files under `solutions/` fail for deliberately different reasons:
`dead-pointer.md` names a script that does not exist, and `one-way-pointer.md`
names one that does exist and does not point back. One rule each, so neither can
pass by accident when the other is what broke.

Every fixture here is a mistake that was actually made, not an invented one.
Adding a rule to a check means adding the fixture that the new rule rejects.
