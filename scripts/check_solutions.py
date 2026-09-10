#!/usr/bin/env python3
"""Every lesson names what enforces it, and that thing has to still exist.

The link has to run both ways. A lesson naming a script is half a pointer: the
script is what someone edits a month from now, and if it does not name the
lesson back, the reasoning is one rename away from being unreachable. So a
tracked lesson must be mentioned by every file it claims as its enforcement.

This is the check against a dead harness. A harness does not fail loudly when it
rots; it keeps passing while quietly meaning less. The specific way this one
would rot is a solution file claiming `enforced_by: check` and pointing at a
script that was renamed, or a fixture that was deleted in a tidy-up, leaving a
document that reads like a guarantee and is a memory.

So the pointers are verified. If a lesson says a check enforces it, the check is
on disk. If it names a fixture, the fixture is there. If the index does not list
it, the index is wrong.

    python3 scripts/check_solutions.py            # checks docs/solutions
    python3 scripts/check_solutions.py <dir>      # checks any directory
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ("title", "date", "tags", "enforced_by")
# Fields whose value is a path, or a comma separated list of paths, into the repo.
POINTERS = ("check", "fixture", "code_in", "rule_in")


def is_local(path: Path) -> bool:
    """Whether git is deliberately not tracking this lesson.

    Some lessons are kept on disk and out of the repository, because nothing
    committed depends on them. Those still have to be well formed and still have
    to point at things that exist, but requiring them in an index a fresh clone
    will read would put a dead row in that index.
    """
    try:
        return subprocess.run(
            ["git", "check-ignore", "-q", str(path)],
            cwd=ROOT, capture_output=True,
        ).returncode == 0
    except (OSError, subprocess.SubprocessError):
        # No git, or not a working tree. Treat everything as tracked, which is
        # the stricter reading.
        return False


def frontmatter(text: str) -> dict[str, str] | None:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def paths_in(value: str) -> list[str]:
    """Pull repo paths out of a field that may also carry prose."""
    found = []
    for part in value.split(","):
        part = part.strip()
        # A path here always has a slash or a known extension.
        token = part.split()[0].rstrip(".,") if part else ""
        if token and ("/" in token or token.endswith((".md", ".py"))):
            found.append(token)
    return found


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "docs" / "solutions"
    if not root.is_dir():
        print(f"check_solutions: no such directory: {root}", file=sys.stderr)
        return 2

    index = root / "README.md"
    index_text = index.read_text(encoding="utf-8") if index.is_file() else ""
    files = sorted(f for f in root.glob("*.md") if f.name != "README.md")
    if not files:
        print(f"check_solutions: no solution files in {root}", file=sys.stderr)
        return 2

    failed = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        problems = []

        fm = frontmatter(text)
        if fm is None:
            problems.append(("no frontmatter block",
                             "the index and any future search rely on it",
                             "add a --- block with " + ", ".join(REQUIRED)))
        else:
            for key in REQUIRED:
                if not fm.get(key):
                    problems.append((f"frontmatter is missing {key!r}",
                                     "a lesson with no stated enforcement is a "
                                     "diary entry",
                                     f"add {key} to the frontmatter of {f.name}"))
            for key in POINTERS:
                for target in paths_in(fm.get(key, "")):
                    dest = ROOT / target
                    if not dest.exists():
                        problems.append((
                            f"{key} points at {target}, which does not exist",
                            "a lesson that names a dead enforcement reads like a "
                            "guarantee and is a memory. This is how a harness "
                            "rots without failing",
                            f"restore {target}, or change {key} in {f.name} to "
                            "what actually enforces it now"))
                        continue
                    # A local lesson is deliberately absent from the repository,
                    # so a tracked file must not link to it: that would put a
                    # dead reference in front of anyone who clones this.
                    if is_local(f):
                        continue
                    try:
                        body = dest.read_text(encoding="utf-8", errors="replace")
                    except OSError:
                        continue
                    if f.name not in body:
                        problems.append((
                            f"{target} does not mention {f.name}",
                            "a pointer that runs one way rots from the end nobody "
                            "reads. The file is what gets edited; if it does not "
                            "name the lesson, the reasoning is one rename from "
                            "being unreachable",
                            f"add a line to {target} pointing at "
                            f"docs/solutions/{f.name}"))

        local = is_local(f)
        if not local and f.name not in index_text:
            problems.append((f"{f.name} is not listed in README.md",
                             "an index that omits entries stops being read",
                             f"add a row for {f.name} to {index.name}"))

        if not problems:
            print(f"ok    {f.name}{'  (local)' if local else ''}")
            continue
        failed += 1
        for what, why, fix in problems:
            print(f"FAIL  {f.name}")
            print(f"      what: {what}")
            print(f"      why:  {why}")
            print(f"      fix:  {fix}")

    if failed:
        print(f"\ncheck_solutions: {failed} of {len(files)} files failed")
        return 1
    tracked = sum(1 for f in files if not is_local(f))
    print(f"check_solutions: {len(files)} lessons, {tracked} tracked, "
          f"every pointer alive")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
