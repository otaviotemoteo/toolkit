"""OpenAI image generation.

Phase 1 runs here because a new account gets $5 of credit with no card, which
is dozens of iterations at the cheap tier. Iterate on gpt-image-1-mini until
the prompt is right, then render once on the full model.

Cost, from the project notes: roughly $0.005 to $0.006 per image on the mini
tier. Check the current rate before assuming.
"""

from __future__ import annotations

import base64
import json
import urllib.error
import urllib.request
from pathlib import Path

from .base import ImageBackend, ImageRequest, ImageResult, env_key

ENDPOINT = "https://api.openai.com/v1/images/generations"


class OpenAIBackend(ImageBackend):
    name = "openai"

    def __init__(self, model: str | None = None) -> None:
        # Default to the cheap tier on purpose. Rendering at the expensive tier
        # should be a decision someone typed, not a default they inherited.
        self.model = model or env_key("OPENAI_IMAGE_MODEL") or "gpt-image-1-mini"

    def available(self) -> tuple[bool, str]:
        if not env_key("OPENAI_API_KEY"):
            return False, "OPENAI_API_KEY is not set"
        return True, ""

    def generate(self, request: ImageRequest) -> ImageResult:
        key = env_key("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY is not set")

        payload = {
            "model": self.model,
            "prompt": request.prompt,
            "size": request.size,
            "n": 1,
            **request.extra,
        }
        req = urllib.request.Request(
            ENDPOINT,
            data=json.dumps(payload).encode(),
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                body = json.loads(resp.read())
        except urllib.error.HTTPError as e:
            # The vendor's error body says far more than the status line, and
            # losing it turns a five-second fix into a guessing game.
            detail = e.read().decode(errors="replace")[:600]
            raise RuntimeError(f"OpenAI returned {e.code}: {detail}") from None

        item = body["data"][0]
        out = request.out_path or Path("out/openai.png")
        out.parent.mkdir(parents=True, exist_ok=True)

        if "b64_json" in item:
            out.write_bytes(base64.b64decode(item["b64_json"]))
        else:
            with urllib.request.urlopen(item["url"], timeout=300) as r:
                out.write_bytes(r.read())

        return ImageResult(
            path=out, backend=self.name, model=self.model,
            prompt=request.prompt,
            cost_note=f"billed to platform.openai.com, model {self.model}",
        )
