#!/usr/bin/env python3
"""Generate one illustration from a brief.

The style anchor from docs/ILLUSTRATION_SPEC.md is appended here rather than
written into each brief, so that changing the visual system is one edit and not
a search across every brief that ever existed.

--init exists because a subject that is already approved must not be redrawn
from noise: docs/solutions/pose-variation-is-not-generation.md. The sidecar
written beside every image is what makes that chain readable afterwards:
docs/solutions/the-model-has-no-memory.md.

    python3 src/generate.py briefs/hero-character/brief.md
    IMAGE_BACKEND=openai python3 src/generate.py briefs/hero-character/brief.md
    python3 src/generate.py briefs/hero-character/brief.md --key '#FF00FF'
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from adapters import ImageRequest, get_backend  # noqa: E402

SPEC = ROOT / "docs" / "ILLUSTRATION_SPEC.md"

# Paper, not a chroma key. Mode B stopped cutting out, so the background is
# the page ground itself. One definition, imported by the checks too.
DEFAULT_KEY = "#F7F6F3"


def style_anchor(key_color: str) -> str:
    """Pull the anchor out of the spec so there is exactly one copy of it."""
    text = SPEC.read_text(encoding="utf-8")
    m = re.search(r"## The style anchor.*?```text\n(.*?)```", text, re.S)
    if not m:
        raise SystemExit(f"could not find the style anchor block in {SPEC}")
    return m.group(1).strip().replace("<KEY_COLOR>", key_color)


def diffusion_anchor(key_color: str) -> tuple[str, str]:
    """The positive and negative blocks, in that order, from the spec.

    Same single-source rule as style_anchor: the visual system is edited in one
    file, never copied into a brief.
    """
    text = SPEC.read_text(encoding="utf-8")
    m = re.search(r"## The diffusion anchor(.*?)(?=\n## )", text, re.S)
    if not m:
        raise SystemExit(f"could not find the diffusion anchor section in {SPEC}")
    blocks = re.findall(r"```text\n(.*?)```", m.group(1), re.S)
    if len(blocks) != 2:
        raise SystemExit(
            f"the diffusion anchor in {SPEC} needs exactly two text blocks, "
            f"positive then negative; found {len(blocks)}"
        )
    positive, negative = (b.strip().replace("<KEY_COLOR>", key_color) for b in blocks)
    return positive, negative


def subject_from_brief(path: Path, heading: str = "## Prompt") -> str:
    """Everything under the given heading in the brief is the subject."""
    text = path.read_text(encoding="utf-8")
    m = re.search(rf"^{re.escape(heading)}\s*\n(.*?)(?=\n## |\Z)", text, re.S | re.M)
    if not m:
        raise SystemExit(
            f"{path} has no {heading!r} section. The brief describes the subject; "
            "the style anchor is appended from the spec."
        )
    body = m.group(1).strip()
    if not body:
        raise SystemExit(f"the {heading!r} section in {path} is empty")
    # Everything under the heading is sent verbatim, so a note to the reader
    # written here is sent to the model as if it described the picture. This
    # happened: a paragraph explaining when the control section is used sat
    # inside ## Prompt and was sent with every run. Prompt prose never needs
    # bold, so bold is the marker of commentary that escaped.
    if "**" in body:
        raise SystemExit(
            f"the {heading!r} section in {path} contains bold text, which means "
            "a note to the reader is inside the prompt and is being sent to the "
            "model. Move it under its own '## ' heading."
        )
    return body


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("brief", type=Path)
    ap.add_argument("--backend", default=None, help="overrides IMAGE_BACKEND")
    ap.add_argument("--size", default="1024x1024")
    ap.add_argument("--key", default=DEFAULT_KEY,
                    help="background colour. Paper by default: mode B "
                         "stopped cutting out, so it is not a chroma key")
    ap.add_argument("--control", type=Path, default=None,
                    help="hold this drawing's structure, leaving colour free")
    ap.add_argument("--control-type", default="canny",
                    choices=("canny", "depth", "hed", "normal", "pose"))
    ap.add_argument("--control-strength", type=float, default=0.6)
    ap.add_argument("--init", type=Path, default=None,
                    help="start from this image instead of from noise")
    ap.add_argument("--init-strength", type=float, default=0.4,
                    help="how strongly --init pulls the result, 0.0 is none")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the assembled prompt and stop")
    args = ap.parse_args()

    # Resolve so a relative path works from anywhere and relative_to() below
    # has two absolute paths to compare.
    args.brief = args.brief.resolve()

    if not args.brief.exists():
        raise SystemExit(f"no such brief: {args.brief}")

    # The backend is resolved before the prompt is built, because which anchor
    # the prompt gets depends on what kind of model is going to read it.
    backend = get_backend(args.backend)

    # With a control image the composition arrives as pixels, so the prose does
    # not have to carry it, and a shorter prompt dilutes its clauses less.
    heading = "## Prompt with structure" if args.control else "## Prompt"
    try:
        subject = subject_from_brief(args.brief, heading)
    except SystemExit:
        if heading == "## Prompt":
            raise
        print(f"note: {args.brief.name} has no {heading!r}; using '## Prompt'")
        subject = subject_from_brief(args.brief)

    if backend.prompt_dialect == "diffusion":
        positive, negative = diffusion_anchor(args.key)
        prompt = f"{subject}\n\n{positive}"
    else:
        prompt, negative = f"{subject}\n\n{style_anchor(args.key)}", ""

    if negative and not backend.uses_negative:
        print(f"warning: backend {backend.name!r} discards the negative prompt; "
              f"{len(negative)} characters of prohibition will not be applied")

    if args.dry_run:
        print(prompt)
        if negative:
            print("\n--- negative ---\n")
            print(negative)
        return

    ok, why = backend.available()
    if not ok:
        raise SystemExit(
            f"backend {backend.name!r} is not available: {why}\n"
            f"run with IMAGE_BACKEND=fake to exercise the pipeline without a key."
        )

    # Versioned filenames, never overwrite. An approved asset that got silently
    # replaced is the one mistake in this pipeline that cannot be undone.
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.brief.parent / "out"
    out = out_dir / f"{args.brief.parent.name}-{backend.name}-{stamp}.png"

    print(f"backend {backend.name} · model {backend.model} · {args.size}")
    result = backend.generate(
        ImageRequest(prompt=prompt, negative_prompt=negative,
                     size=args.size, out_path=out,
                     init_image=args.init.resolve() if args.init else None,
                     init_strength=args.init_strength,
                     control_image=args.control.resolve() if args.control else None,
                     control_type=args.control_type,
                     control_strength=args.control_strength)
    )

    # The prompt travels with the image. An image whose prompt was lost can
    # only be re-guessed, not iterated on.
    sidecar = out.with_suffix(".json")
    brief_ref = args.brief.relative_to(ROOT) if args.brief.is_relative_to(ROOT) else args.brief
    sidecar.write_text(json.dumps({
        "brief": str(brief_ref),
        "backend": result.backend,
        "model": result.model,
        "size": args.size,
        "key_color": args.key,
        "generated_at": stamp,
        "cost_note": result.cost_note,
        "dialect": backend.prompt_dialect,
        "control_image": str(args.control) if args.control else None,
        "control_type": args.control_type if args.control else None,
        "control_strength": args.control_strength if args.control else None,
        "prompt_section": heading,
        "init_image": str(args.init) if args.init else None,
        "init_strength": args.init_strength if args.init else None,
        "prompt": result.prompt,
        "negative_prompt": result.negative_prompt,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"wrote {result.path}")
    print(f"      {sidecar.name}")
    if result.cost_note:
        print(f"cost  {result.cost_note}")


if __name__ == "__main__":
    main()
