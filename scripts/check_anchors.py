#!/usr/bin/env python3
"""The two halves of the diffusion anchor must not contradict each other.

Written because the mistake had already been made. The first diffusion anchor
asked for indigo code and 45 degree hatching in the positive block while listing
`colour` and `cross hatching` in the negative one. Guidance runs the model on
both and pushes the result away from the negative, so the two instructions
cancelled: the screens came back nearly white and no hatching ever appeared.
The rule against it was written in the spec two paragraphs above the block that
broke it, which is exactly the kind of rule prose cannot enforce.

A word in both blocks is not a style opinion, it is a contradiction, and a
contradiction is detectable. So this detects it.

Why it exists, and the second bug it caught within the hour:
docs/solutions/never-both-blocks.md
docs/solutions/prohibitions-do-not-belong-in-the-positive.md

    python3 scripts/check_anchors.py                 # checks the real spec
    python3 scripts/check_anchors.py <spec.md>       # checks any spec
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import generate  # noqa: E402  the one definition of how an anchor is extracted

# Words that carry no instruction and would collide constantly.
STOP = {
    "a", "an", "and", "the", "of", "in", "on", "at", "to", "with", "no", "not",
    "or", "for", "is", "are", "it", "its", "that", "this", "any", "all", "as",
    "by", "from", "into", "out", "up", "down", "where", "needed", "there",
    "plain", "short", "small", "large", "one", "two", "three", "around",
}


def terms(text: str) -> set[str]:
    """Significant words, crudely singularised so line and lines collide."""
    found = set()
    for w in re.findall(r"[a-z]+", text.lower()):
        if len(w) < 3 or w in STOP:
            continue
        found.add(w[:-1] if w.endswith("s") and not w.endswith("ss") else w)
    return found


def main() -> int:
    spec = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else generate.SPEC
    if not spec.is_file():
        print(f"check_anchors: no such spec: {spec}", file=sys.stderr)
        return 2

    # Point the extractor at whichever spec is under test, so the check and the
    # generator keep sharing one definition of what an anchor is.
    original, generate.SPEC = generate.SPEC, spec
    try:
        try:
            positive, negative = generate.diffusion_anchor(generate.DEFAULT_KEY)
            instruction = generate.style_anchor(generate.DEFAULT_KEY)
        except SystemExit as e:
            print(f"FAIL  {spec.name}")
            print(f"      what: {e}")
            print("      why:  generate.py extracts the anchors at run time; if "
                  "they cannot be found, every image loses the visual system")
            print("      fix:  restore the headings and the fenced text blocks")
            return 1
    finally:
        generate.SPEC = original

    problems = 0

    if len(instruction.strip()) < 100:
        print(f"FAIL  {spec.name}\n      what: the instruction anchor is nearly empty")
        problems += 1

    overlap = sorted(terms(positive) & terms(negative))
    if overlap:
        print(f"FAIL  {spec.name}")
        print(f"      what: {len(overlap)} word(s) in both the positive and the "
              f"negative block: {', '.join(overlap)}")
        print("      why:  guidance pushes the result away from the negative "
              "block, so a word in both aims at and away from the same thing "
              "and the model splits the difference")
        print("      fix:  decide which block owns each word and delete it from "
              "the other. If the thing is wanted, only the positive keeps it")
        problems += 1

    if problems:
        return 1
    print(f"check_anchors: {spec.name} ok, "
          f"{len(terms(positive))} positive and {len(terms(negative))} negative "
          f"terms, no overlap")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
