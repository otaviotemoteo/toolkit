"""The one interface every image backend implements.

Nothing above this layer knows which vendor answered. That is the whole point:
the prompt spec in docs/ILLUSTRATION_SPEC.md is ours and does not move, and
swapping OpenAI for ZenMux or for a local model is a change to one file plus an
environment variable.

The dependency this creates is a build-time dependency, not a runtime one. The
generated images are static files; the finished site calls no API at all.
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ImageRequest:
    """What every backend receives. Vendor-neutral by construction."""

    prompt: str
    # Only diffusion backends use this. It is a separate field rather than more
    # text in prompt because the two are sent to different places: guidance runs
    # the model once on each and pushes the result away from this one.
    negative_prompt: str = ""
    # Square by default: the sprite atlas work downstream wants square cells,
    # and a non-square source has to be padded or cropped somewhere.
    size: str = "1024x1024"
    # Where the file lands. The caller owns naming, not the backend, so that
    # versioned filenames stay a project rule rather than a vendor accident.
    out_path: Path | None = None
    # Start from an existing image instead of from noise. This is how a pose
    # variation keeps the identity of an approved asset: generating from
    # scratch re-rolls the face every time, at any speed.
    init_image: Path | None = None
    # How strongly the init image influences the result. 0.0 is no influence.
    init_strength: float = 0.4
    # Hold the structure of an existing drawing while leaving colour free. This
    # is the axis init_image cannot separate: init_image inherits pixels, so
    # holding the shape also holds the colour that was in it.
    control_image: Path | None = None
    control_type: str = "canny"
    control_strength: float = 0.6
    # Backend-specific knobs. Anything in here is by definition not portable,
    # so it stays quarantined in one field instead of leaking into the shape.
    extra: dict = field(default_factory=dict)


@dataclass
class ImageResult:
    path: Path
    backend: str
    model: str
    # The prompt exactly as sent. Kept because a result whose prompt was lost
    # cannot be iterated on, only re-guessed.
    prompt: str
    negative_prompt: str = ""
    # Whatever the vendor said about cost, when it says anything at all.
    cost_note: str = ""


class ImageBackend(ABC):
    """Implement this and register it in __init__.py. That is the whole contract."""

    name: str = "unnamed"
    model: str = "unknown"
    # Which anchor from the spec this backend should be handed. An
    # instruction-following model reads prohibitions as prose; a diffusion model
    # needs them in a negative prompt, and giving it the prose version aims at
    # exactly the words it should avoid.
    prompt_dialect: str = "instruction"
    # False for guidance-distilled backends, where the negative prompt is
    # accepted and discarded. Declared so the CLI can say so out loud rather
    # than letting the prohibitions vanish quietly.
    uses_negative: bool = True

    @abstractmethod
    def generate(self, request: ImageRequest) -> ImageResult:
        """Produce one image and write it to request.out_path."""

    def available(self) -> tuple[bool, str]:
        """Whether this backend can run right now, and why not if it cannot.

        Checked before any I/O so the CLI can say "no key" instead of failing
        halfway through with a vendor error nobody can read.
        """
        return True, ""


def env_key(*names: str) -> str | None:
    """First non-empty environment variable among names, or None."""
    for n in names:
        v = os.environ.get(n)
        if v and v.strip():
            return v.strip()
    return None
