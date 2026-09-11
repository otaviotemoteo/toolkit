# One command that answers whether this repo is worth building on right now.
# Budget: under 30 seconds. A verification nobody waits for is not run.
#
#   make check      everything below, in order
#   make lint       style, imports, obvious mistakes
#   make briefs     every asset directory carries its brief
#   make anchors    the positive and negative blocks do not contradict
#   make solutions  every recorded lesson still names a live enforcement
#   make scene      every scene manifest describes files that exist
#   make render     every joint stays put at every render size
#   make mutation   proves the briefs check is capable of failing
#   make smoke      the pipeline runs end to end, no key, no cost
#   make setup      create the venv and install both requirement files
#   make setup-local  add the Apple Silicon generation stack (large)

PY  := ./.venv/bin/python
PIP := ./.venv/bin/pip

.PHONY: check lint briefs anchors solutions scene render mutation smoke setup setup-local

check: lint briefs anchors solutions scene render mutation smoke
	@echo "check: ok"

lint:
	@$(PY) -m ruff check src scripts

briefs:
	@$(PY) scripts/check_briefs.py

anchors:
	@$(PY) scripts/check_anchors.py

solutions:
	@$(PY) scripts/check_solutions.py

scene:
	@$(PY) scripts/check_scene.py

# Node rather than python, because it imports preview/hero.js and tests the
# renderer's own function instead of a restatement of it.
render:
	@node scripts/check_render.mjs

# Every fixture under tests/fixtures/ is broken on purpose and must be rejected.
# If one of them passes, the check is the thing that is broken, not the fixture.
mutation:
	@fail=0; \
	for f in tests/fixtures/briefs/*/; do \
		if $(PY) scripts/check_briefs.py "$$f" >/dev/null 2>&1; then \
			echo "MUTATION SURVIVED: $$f passed check_briefs and must not."; fail=1; \
		fi; \
	done; \
	for f in tests/fixtures/anchors/*.md; do \
		if $(PY) scripts/check_anchors.py "$$f" >/dev/null 2>&1; then \
			echo "MUTATION SURVIVED: $$f passed check_anchors and must not."; fail=1; \
		fi; \
	done; \
	if $(PY) scripts/check_solutions.py tests/fixtures/solutions >/dev/null 2>&1; then \
		echo "MUTATION SURVIVED: tests/fixtures/solutions passed check_solutions and must not."; fail=1; \
	fi; \
	if $(PY) scripts/check_scene.py tests/fixtures/scenes/scene.json >/dev/null 2>&1; then \
		echo "MUTATION SURVIVED: tests/fixtures/scenes passed check_scene and must not."; fail=1; \
	fi; \
	if node scripts/check_render.mjs tests/fixtures/render/px-origin.mjs >/dev/null 2>&1; then \
		echo "MUTATION SURVIVED: tests/fixtures/render passed check_render and must not."; fail=1; \
	fi; \
	if [ $$fail -eq 1 ]; then \
		echo "  A check cannot detect the thing it exists to detect."; exit 1; \
	fi; \
	echo "mutation: every fixture correctly rejected"

smoke:
	@$(PY) scripts/smoke.py

setup:
	python3.11 -m venv .venv
	$(PIP) install -r requirements.txt -r requirements-dev.txt

# Kept separate from setup: someone using a hosted backend should not have to
# download an ML stack to render a placeholder.
setup-local:
	$(PIP) install -r requirements-local.txt
