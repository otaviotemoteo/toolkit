"""Backend registry. One place decides which vendor runs.

Selection is by the IMAGE_BACKEND environment variable, defaulting to fake, so
that a missing key produces a placeholder and a clear message rather than a
surprise charge or an unreadable vendor error.

**A file here is a protocol, not a company.** Four names below are real
implementations because each talks in a genuinely different way: a placeholder,
a local model in this process, a vendor tree that has to be walked, and the
OpenAI image API. Every vendor speaking that last one shares a single adapter
and appears as data, or as nothing at all. See `openai_compatible.py`.

Three ways to reach a hosted vendor, in order of how much this repository has
to know about it:

    IMAGE_BACKEND=openai                    listed in PROVIDERS
    IMAGE_BACKEND=anything IMAGE_ENDPOINT=  not listed, configured by env
    IMAGE_BACKEND=fake                      nothing hosted at all

The middle one is the point. A vendor this project has never heard of needs no
file, no entry and no release.
"""

from __future__ import annotations

import os

from .base import ImageBackend, ImageRequest, ImageResult, env_key
from .fake import FakeBackend
from .gemini import GeminiBackend
from .local_mflux import LocalControlNetBackend, LocalMFluxBackend
from .openai_compatible import PROVIDERS, OpenAICompatibleBackend

# Backends whose behaviour is not the OpenAI image protocol.
BACKENDS: dict[str, type[ImageBackend]] = {
    "fake": FakeBackend,
    "gemini": GeminiBackend,
    "local": LocalMFluxBackend,
    "local-cn": LocalControlNetBackend,
}

DEFAULT = "fake"


def available_names() -> list[str]:
    return sorted(set(BACKENDS) | set(PROVIDERS))


def get_backend(name: str | None = None) -> ImageBackend:
    key = (name or os.environ.get("IMAGE_BACKEND") or DEFAULT).strip().lower()
    if key in BACKENDS:
        return BACKENDS[key]()
    # A listed provider, or an unlisted one the environment fully describes.
    # Anything else is a typo, and a typo that silently produced a backend with
    # no endpoint would fail much later and much less clearly.
    if key in PROVIDERS or env_key("IMAGE_ENDPOINT"):
        return OpenAICompatibleBackend(key)
    raise SystemExit(
        f"unknown backend {key!r}. available: {', '.join(available_names())}. "
        f"For a vendor that is not listed, set IMAGE_ENDPOINT and IMAGE_API_KEY "
        f"and use any name."
    )


__all__ = [
    "BACKENDS", "DEFAULT", "PROVIDERS", "available_names", "get_backend",
    "ImageBackend", "ImageRequest", "ImageResult", "OpenAICompatibleBackend",
]
