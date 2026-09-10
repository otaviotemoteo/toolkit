"""A backend that generates nothing and costs nothing.

It exists so the whole pipeline - brief, prompt assembly, naming, cutout,
budget check - can be exercised before any API key exists, and so a broken
pipeline can be told apart from a broken prompt.

The placeholder it draws is deliberately in the project's own tokens, and
deliberately ugly enough that nobody mistakes it for a real result.
"""

from __future__ import annotations

import hashlib
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw

from .base import ImageBackend, ImageRequest, ImageResult

PAPER = (247, 246, 243)
INK = (22, 22, 26)
INK_SOFT = (90, 90, 102)
ACCENT = (93, 93, 156)


class FakeBackend(ImageBackend):
    name = "fake"
    model = "placeholder"

    def generate(self, request: ImageRequest) -> ImageResult:
        w, h = (int(x) for x in request.size.lower().split("x"))
        img = Image.new("RGB", (w, h), PAPER)
        d = ImageDraw.Draw(img)

        # 45-degree hatch, the project's one texture, so even the placeholder
        # is in the system.
        step = 10
        for i in range(-h, w, step):
            d.line([(i, h), (i + h, 0)], fill=(22, 22, 26, 12), width=1)

        margin = int(min(w, h) * 0.08)
        d.rectangle([margin, margin, w - margin, h - margin], outline=INK, width=3)

        # A hash of the prompt, so two different prompts are visibly different
        # files and a stale placeholder cannot be mistaken for a fresh one.
        digest = hashlib.sha256(request.prompt.encode()).hexdigest()[:12]
        d.rectangle(
            [margin * 2, h // 2 - 40, margin * 2 + 180, h // 2 + 40],
            outline=ACCENT, width=3,
        )
        d.text((margin * 2 + 16, h // 2 - 10), digest, fill=ACCENT)

        y = margin + 24
        d.text((margin + 20, y), "PLACEHOLDER - no API was called", fill=INK)
        y += 28
        for line in textwrap.wrap(request.prompt, width=max(20, w // 12))[:12]:
            d.text((margin + 20, y), line, fill=INK_SOFT)
            y += 18

        out = request.out_path or Path("out/fake.png")
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out)
        return ImageResult(
            path=out, backend=self.name, model=self.model,
            prompt=request.prompt, cost_note="free",
        )
