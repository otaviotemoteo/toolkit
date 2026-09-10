#!/usr/bin/env python3
"""Every asset directory carries the brief that produced it.

The rule already exists in prose: nothing is generated without an approved
brief, and each brief lives at briefs/<name>/brief.md. This is the same rule
written a second time, as something that fails.

Why it is worth enforcing rather than remembering: an image whose brief is
missing cannot be iterated on, only guessed at again, and nothing about the
image itself says which one it is. The failure is silent until someone needs to
regenerate, which is exactly when it is most expensive.

The prompt and acceptance rules are checked with the same code generate.py
uses, imported rather than reimplemented, so the check and the generator cannot
drift apart into disagreeing about what a valid brief is.

    python3 scripts/check_briefs.py            # checks briefs/
    python3 scripts/check_briefs.py <root>     # checks any directory of assets
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import generate  # noqa: E402  the one definition of what a brief has to contain

MODEL = "briefs/hero-character/brief.md"


def problems(asset_dir: Path) -> list[tuple[str, str, str]]:
    """Return (what is wrong, why the rule exists, how to fix it) for one asset."""
    found: list[tuple[str, str, str]] = []
    brief = asset_dir / "brief.md"

    if not brief.is_file():
        found.append((
            "no brief.md",
            "an asset with no brief cannot be regenerated or iterated on, only "
            "guessed at again",
            f"create {brief}, using {MODEL} as the model",
        ))
        return found

    try:
        generate.subject_from_brief(brief)
    except SystemExit as e:
        found.append((
            str(e),
            "generate.py sends everything under '## Prompt' as the subject; "
            "without that heading there is nothing to send",
            f"add a '## Prompt' section to {brief} describing the scene",
        ))

    text = brief.read_text(encoding="utf-8")
    if "## Acceptance" not in text:
        found.append((
            "no '## Acceptance' section",
            "a brief with no acceptance criteria cannot be judged, so a bad "
            "result gets accepted or regenerated on instinct instead of on a rule",
            f"add a '## Acceptance' section to {brief} listing what has to be "
            "observably true, the way the criteria in the model brief are",
        ))

    return found


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "briefs"
    if not root.is_dir():
        print(f"check_briefs: no such directory: {root}", file=sys.stderr)
        return 2

    assets = sorted(d for d in root.iterdir() if d.is_dir() and not d.name.startswith("."))
    if not assets:
        print(f"check_briefs: no asset directories under {root}", file=sys.stderr)
        return 2

    failed = 0
    for asset in assets:
        found = problems(asset)
        if not found:
            print(f"ok    {asset.relative_to(root.parent)}")
            continue
        failed += 1
        for what, why, fix in found:
            print(f"FAIL  {asset.relative_to(root.parent)}")
            print(f"      what: {what}")
            print(f"      why:  {why}")
            print(f"      fix:  {fix}")

    if failed:
        print(f"\ncheck_briefs: {failed} of {len(assets)} asset directories failed")
        return 1
    print(f"check_briefs: {len(assets)} ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
