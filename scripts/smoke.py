#!/usr/bin/env python3
"""Run the whole generation path end to end, with no key and no cost.

Unit-testing the pieces would not catch what this catches. The failures that
actually happen here live between the pieces: the style anchor heading gets
renamed in the spec and the regex stops matching, the sidecar stops being
written, the backend registry loses a name. Each part still looks correct on
its own.

The fake backend exists precisely so this can run on every check.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
PY = sys.executable
BRIEF = ROOT / "briefs" / "hero-character" / "brief.md"

import generate  # noqa: E402  one definition of the background colour


def run(args: list[str], env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PY, str(ROOT / "src" / "generate.py"), *args],
        capture_output=True, text=True,
        env={**os.environ, **(env or {})},
    )


def spec_anchor() -> str:
    """The anchor block, parsed without reusing generate.py's regex.

    Two independent readings of the same file that have to agree. If they stop
    agreeing, one of them is wrong and this says so before an image is paid for.
    """
    text = (ROOT / "docs" / "ILLUSTRATION_SPEC.md").read_text(encoding="utf-8")
    after_heading = text.split("## The style anchor", 1)
    if len(after_heading) != 2:
        fail("docs/ILLUSTRATION_SPEC.md has no '## The style anchor' heading")
    fences = after_heading[1].split("```")
    if len(fences) < 3:
        fail("the style anchor heading is not followed by a fenced block")
    return fences[1].removeprefix("text").strip()


def fail(msg: str) -> None:
    print(f"FAIL  smoke: {msg}")
    print("      fix:  run the same command by hand to see the full error")
    raise SystemExit(1)


def main() -> None:
    dry = run([str(BRIEF), "--dry-run"])
    if dry.returncode != 0:
        fail(f"--dry-run exited {dry.returncode}: {dry.stderr.strip()}")
    if len(dry.stdout.strip()) < 200:
        fail("--dry-run produced almost nothing, so the brief or the spec is not "
             "being read")

    # Read the anchor out of the spec here, with a parse written independently
    # of the one in generate.py, and require that it actually reached the
    # prompt. Asserting on specific style wording instead would mean editing
    # this file every time the visual system changes, which is how a check
    # stops being run.
    anchor = spec_anchor().replace("<KEY_COLOR>", generate.DEFAULT_KEY)
    if anchor not in dry.stdout:
        fail("the style anchor from docs/ILLUSTRATION_SPEC.md is not in the "
             "assembled prompt, so every generated image would be missing the "
             "visual system")
    if "<KEY_COLOR>" in dry.stdout:
        fail("the <KEY_COLOR> placeholder was never substituted, so the chroma "
             "background would be generated as the literal word")

    # Generate into a throwaway copy so the check never writes into briefs/.
    with tempfile.TemporaryDirectory() as tmp:
        asset = Path(tmp) / "smoke-asset"
        asset.mkdir()
        shutil.copy(BRIEF, asset / "brief.md")

        gen = run([str(asset / "brief.md")], env={"IMAGE_BACKEND": "fake"})
        if gen.returncode != 0:
            fail(f"the fake backend exited {gen.returncode}: {gen.stderr.strip()}")

        pngs = list((asset / "out").glob("*.png"))
        sidecars = list((asset / "out").glob("*.json"))
        if len(pngs) != 1:
            fail(f"expected one png, found {len(pngs)}")
        if len(sidecars) != 1:
            fail(f"expected one json sidecar, found {len(sidecars)}")

        data = json.loads(sidecars[0].read_text(encoding="utf-8"))
        if not data.get("prompt"):
            fail("the sidecar has no prompt in it, so the image could not be "
                 "regenerated from what was saved beside it")
        if data.get("backend") != "fake":
            fail(f"the sidecar says backend {data.get('backend')!r}, expected 'fake'")

    print("smoke: dry run, fake generation, png and sidecar all ok")


if __name__ == "__main__":
    main()
