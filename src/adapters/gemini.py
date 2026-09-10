"""Google Gemini image generation, direct to the Gemini API.

Here because of a hard constraint rather than a preference: there is no card,
and Google AI Studio issues a key without one. OpenAI refused with 429
insufficient_quota on 2026-09-04, which is a billing state, not a code problem.

The model is the same one the ZenMux entry in .env.example already pointed at,
so this removes an aggregator and its credit balance from the path rather than
adding a new vendor to the plan.

Two details that matter for this project specifically:

PNG, never JPEG. The spec generates onto a flat chroma key background that
cutout.py keys out afterwards. JPEG puts compression artefacts along every edge
where the key colour meets the drawing, and those artefacts are exactly what a
keyer cannot distinguish from the subject.

Prompt adherence is why this is preferred over a local diffusion model. The
style anchor is mostly negative instruction, no fill, no soft shadow, no
gradient, and instruction-following models honour that kind of prose far better
than a diffusion model does.

The documentation and the API disagree about supported output formats, and the
parsing below is deliberate rather than defensive out of habit. See
docs/solutions/documentation-can-contradict-the-api.md.

Untested until it runs. The endpoint and response shape come from the API
documentation read on 2026-09-04; the parsing below is deliberately tolerant of
the exact nesting so a shape change surfaces as a readable error rather than a
KeyError.
"""

from __future__ import annotations

import base64
import json
import urllib.error
import urllib.request
from pathlib import Path

from .base import ImageBackend, ImageRequest, ImageResult, env_key

ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"

# Only image/jpeg is accepted here today. Overridable so that the day PNG is
# supported this is one environment variable and not a code change.
MIME = __import__("os").environ.get("GEMINI_IMAGE_MIME", "image/jpeg")

# The API takes an aspect ratio and a size bucket, not pixel dimensions.
RATIOS = {
    (1, 1): "1:1", (3, 2): "3:2", (2, 3): "2:3", (3, 4): "3:4", (4, 3): "4:3",
    (4, 5): "4:5", (5, 4): "5:4", (9, 16): "9:16", (16, 9): "16:9", (21, 9): "21:9",
}


def to_ratio_and_size(size: str) -> tuple[str, str]:
    """Turn '1024x1024' into ('1:1', '1K'), picking the nearest legal ratio."""
    try:
        w, h = (int(v) for v in size.lower().split("x"))
    except ValueError:
        raise RuntimeError(
            f"size {size!r} is not WIDTHxHEIGHT, for example 1024x1024"
        ) from None

    target = w / h
    ratio = min(RATIOS.items(), key=lambda kv: abs(kv[0][0] / kv[0][1] - target))[1]

    longest = max(w, h)
    for limit, bucket in ((512, "0.5K"), (1024, "1K"), (2048, "2K")):
        if longest <= limit:
            return ratio, bucket
    return ratio, "4K"


def find_image(node: object) -> str | None:
    """First base64 image payload anywhere in the response.

    Walking the tree rather than indexing a documented path: the cost of being
    wrong about the nesting is a burned request and an unreadable KeyError.
    """
    if isinstance(node, dict):
        if node.get("type") == "image" and isinstance(node.get("data"), str):
            return node["data"]
        for v in node.values():
            found = find_image(v)
            if found:
                return found
    elif isinstance(node, list):
        for v in node:
            found = find_image(v)
            if found:
                return found
    return None


class GeminiBackend(ImageBackend):
    name = "gemini"

    def __init__(self, model: str | None = None) -> None:
        self.model = model or env_key("GEMINI_IMAGE_MODEL") or "gemini-3.1-flash-image"

    def available(self) -> tuple[bool, str]:
        if not env_key("GEMINI_API_KEY", "GOOGLE_API_KEY"):
            return False, (
                "GEMINI_API_KEY is not set. Get one at aistudio.google.com, "
                "which issues a key without a card"
            )
        return True, ""

    def generate(self, request: ImageRequest) -> ImageResult:
        key = env_key("GEMINI_API_KEY", "GOOGLE_API_KEY")
        if not key:
            raise RuntimeError("GEMINI_API_KEY is not set")

        ratio, bucket = to_ratio_and_size(request.size)
        payload = {
            "model": self.model,
            "input": [{"type": "text", "text": request.prompt}],
            "response_format": {
                "type": "image",
                # The API rejects image/png on this endpoint (400, tested
                # 2026-09-04). See the note above on why that is a problem for
                # the chroma key, and MIME below for the override.
                "mime_type": MIME,
                "aspect_ratio": ratio,
                "image_size": bucket,
            },
            **request.extra,
        }
        req = urllib.request.Request(
            ENDPOINT,
            data=json.dumps(payload).encode(),
            headers={"x-goog-api-key": key, "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                body = json.loads(resp.read())
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:600]
            raise RuntimeError(f"Gemini returned {e.code}: {detail}") from None

        data = find_image(body)
        if not data:
            # A refusal comes back as a normal 200 with text instead of an
            # image, and saying so beats writing a zero-byte png.
            raise RuntimeError(
                "the response carried no image. The model may have refused the "
                f"prompt, or the response shape may have changed. Body starts: "
                f"{json.dumps(body)[:600]}"
            )

        out = request.out_path or Path("out/gemini.png")
        if MIME == "image/jpeg":
            out = out.with_suffix(".jpg")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(base64.b64decode(data))

        return ImageResult(
            path=out, backend=self.name, model=self.model,
            prompt=request.prompt,
            cost_note=f"gemini api free tier, model {self.model}, {ratio} {bucket}",
        )
