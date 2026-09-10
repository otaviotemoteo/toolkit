"""Backend registry. One place decides which vendor runs.

Selection is by the IMAGE_BACKEND environment variable, defaulting to fake, so
that a missing key produces a placeholder and a clear message rather than a
surprise charge or an unreadable vendor error.
"""

from __future__ import annotations

import os

from .base import ImageBackend, ImageRequest, ImageResult
from .fake import FakeBackend
from .gemini import GeminiBackend
from .local_mflux import LocalControlNetBackend, LocalMFluxBackend
from .openai_backend import OpenAIBackend
from .zenmux import ZenMuxBackend

BACKENDS: dict[str, type[ImageBackend]] = {
    "fake": FakeBackend,
    "gemini": GeminiBackend,
    "local": LocalMFluxBackend,
    "local-cn": LocalControlNetBackend,
    "openai": OpenAIBackend,
    "zenmux": ZenMuxBackend,
}

DEFAULT = "fake"


def get_backend(name: str | None = None) -> ImageBackend:
    key = (name or os.environ.get("IMAGE_BACKEND") or DEFAULT).strip().lower()
    if key not in BACKENDS:
        raise SystemExit(
            f"unknown backend {key!r}. available: {', '.join(sorted(BACKENDS))}"
        )
    return BACKENDS[key]()


__all__ = [
    "BACKENDS", "DEFAULT", "get_backend",
    "ImageBackend", "ImageRequest", "ImageResult",
]
