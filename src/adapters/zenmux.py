"""ZenMux, an OpenAI-compatible gateway.

Needed for video in phase 2 because oil-motion pins minimax/minimax-h3 there,
and since the account has to exist anyway it can serve images too, which is one
account instead of two.

Pay As You Go: one credit is one dollar, no recurrence. The project notes flag
that per-token pricing on their site is not transparent, so check the model's
rate before loading credit.

Untested. It is here so the second backend exists and the interface is proven
to be an interface rather than a wrapper around one vendor, which is the whole
reason the adapter was built before it was needed.
"""

from __future__ import annotations

import base64
import json
import urllib.error
import urllib.request
from pathlib import Path

from .base import ImageBackend, ImageRequest, ImageResult, env_key

ENDPOINT = "https://zenmux.ai/api/v1/images/generations"


class ZenMuxBackend(ImageBackend):
    name = "zenmux"

    def __init__(self, model: str | None = None) -> None:
        self.model = model or env_key("ZENMUX_IMAGE_MODEL") or "google/gemini-2.5-flash-image"

    def available(self) -> tuple[bool, str]:
        if not env_key("ZENMUX_API_KEY"):
            return False, "ZENMUX_API_KEY is not set"
        return True, ""

    def generate(self, request: ImageRequest) -> ImageResult:
        key = env_key("ZENMUX_API_KEY")
        if not key:
            raise RuntimeError("ZENMUX_API_KEY is not set")

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
            detail = e.read().decode(errors="replace")[:600]
            raise RuntimeError(f"ZenMux returned {e.code}: {detail}") from None

        item = body["data"][0]
        out = request.out_path or Path("out/zenmux.png")
        out.parent.mkdir(parents=True, exist_ok=True)

        if "b64_json" in item:
            out.write_bytes(base64.b64decode(item["b64_json"]))
        else:
            with urllib.request.urlopen(item["url"], timeout=300) as r:
                out.write_bytes(r.read())

        return ImageResult(
            path=out, backend=self.name, model=self.model,
            prompt=request.prompt,
            cost_note=f"billed to zenmux.ai, model {self.model}",
        )
