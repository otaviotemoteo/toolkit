"""Every vendor that speaks the OpenAI image API, in one adapter.

There were two files here, `openai_backend.py` and `zenmux.py`. Stripped of
their names they differed in four lines: the endpoint, the default model, one
comment and the cost note. Everything else, the request shape, the auth header,
the error handling, the two response forms, was duplicated. A third vendor on
the same protocol would have duplicated it again, and the directory would have
grown one file per company rather than one file per way of talking.

So the rule here is **one adapter per protocol, not one per vendor**. Protocols
are few and change slowly. Vendors are unbounded.

A provider is data:

- listed in `PROVIDERS` below, three lines, no code
- or not listed at all, and configured entirely from the environment with
  IMAGE_ENDPOINT, IMAGE_API_KEY and IMAGE_MODEL

The second form is the important one. It means a vendor nobody has heard of can
be used today, by someone who never opens this repository, with no release.

What does not belong here is a vendor that only looks compatible. Gemini has its
own file because its response is a tree to walk rather than a list to index, and
because it rejects the MIME type its own documentation specifies. See
docs/solutions/documentation-can-contradict-the-api.md. Bending this adapter to
cover it would put a vendor's quirk in the shared path, which is the thing the
adapter layer exists to prevent.
"""

from __future__ import annotations

import base64
import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from .base import ImageBackend, ImageRequest, ImageResult, env_key


@dataclass(frozen=True)
class Provider:
    """Everything that differs between two vendors of the same protocol."""

    name: str
    endpoint: str
    default_model: str
    # Where the bill lands, in words a human recognises. Printed with the
    # result, because a cost that is never stated is a cost nobody checked.
    billed_at: str
    # Environment variables, by convention <NAME>_API_KEY and <NAME>_IMAGE_MODEL.
    # Spelled out rather than derived so that an odd one can be listed as it is.
    key_var: str = ""
    model_var: str = ""

    def keys(self) -> tuple[str, str]:
        upper = self.name.upper().replace("-", "_")
        return (self.key_var or f"{upper}_API_KEY",
                self.model_var or f"{upper}_IMAGE_MODEL")


PROVIDERS: dict[str, Provider] = {
    # Prepaid API credit, which no subscription includes. There is no free
    # credit on a new account: that was claimed, tested and false. See
    # docs/cost.md.
    "openai": Provider(
        name="openai",
        endpoint="https://api.openai.com/v1/images/generations",
        # The cheap tier on purpose. Rendering at the expensive one should be a
        # decision someone typed, not a default they inherited.
        default_model="gpt-image-1-mini",
        billed_at="platform.openai.com",
    ),
    # A gateway rather than a model vendor. Never executed: the endpoint and the
    # response shape are assumed from compatibility and have never been proven
    # against the real service.
    "zenmux": Provider(
        name="zenmux",
        endpoint="https://zenmux.ai/api/v1/images/generations",
        default_model="google/gemini-2.5-flash-image",
        billed_at="zenmux.ai",
    ),
}

# The escape hatch: a provider that is not in the table at all.
GENERIC = Provider(
    name="openai-compatible",
    endpoint="",
    default_model="",
    billed_at="whichever account IMAGE_API_KEY belongs to",
    key_var="IMAGE_API_KEY",
    model_var="IMAGE_MODEL",
)


class OpenAICompatibleBackend(ImageBackend):
    prompt_dialect = "instruction"

    def __init__(self, provider: Provider | str | None = None,
                 model: str | None = None) -> None:
        if isinstance(provider, str):
            provider = PROVIDERS.get(provider, GENERIC)
        self.provider = provider or GENERIC
        self.name = self.provider.name
        key_var, model_var = self.provider.keys()
        self.key_var = key_var
        self.model = model or env_key(model_var) or self.provider.default_model
        self.endpoint = env_key("IMAGE_ENDPOINT") or self.provider.endpoint

    def available(self) -> tuple[bool, str]:
        if not self.endpoint:
            return False, "no endpoint: set IMAGE_ENDPOINT, or name a provider in PROVIDERS"
        if not self.model:
            return False, f"no model: set {self.provider.keys()[1]}"
        if not env_key(self.key_var):
            return False, f"{self.key_var} is not set"
        return True, ""

    def generate(self, request: ImageRequest) -> ImageResult:
        ok, why = self.available()
        if not ok:
            raise RuntimeError(why)
        key = env_key(self.key_var)

        payload = {
            "model": self.model,
            "prompt": request.prompt,
            "size": request.size,
            "n": 1,
            **request.extra,
        }
        req = urllib.request.Request(
            self.endpoint,
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
            # losing it turns a five second fix into a guessing game.
            detail = e.read().decode(errors="replace")[:600]
            raise RuntimeError(f"{self.name} returned {e.code}: {detail}") from None

        item = body["data"][0]
        out = request.out_path or Path(f"out/{self.name}.png")
        out.parent.mkdir(parents=True, exist_ok=True)

        if "b64_json" in item:
            out.write_bytes(base64.b64decode(item["b64_json"]))
        else:
            with urllib.request.urlopen(item["url"], timeout=300) as r:
                out.write_bytes(r.read())

        return ImageResult(
            path=out,
            backend=self.name,
            model=self.model,
            prompt=request.prompt,
            cost_note=f"billed to {self.provider.billed_at}, model {self.model}",
        )
