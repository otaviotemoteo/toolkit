"""Local generation on Apple Silicon, through mflux.

Two decisions here are argued elsewhere rather than in this docstring:
docs/solutions/a-flag-can-exist-and-be-ignored.md, on why this uses the base
model and not the faster distilled one, and
docs/solutions/pose-variation-is-not-generation.md, on why an init image is the
mechanism for a pose rather than an optimisation.

Chosen because there is no card and every hosted free tier we tested was
either gone or never included images. This one cannot be revoked, rate limited
or repriced, which after two false claims of free credit is worth more than
convenience.

The model is Z-Image base, 6B, quantised to 4 bit and downloaded already
quantised from the project's own Hugging Face org. That skips the step the
usual advice describes, saving a 16 bit checkpoint and converting it locally:
no large download and no conversion peak on a 16 GB machine.

Why the base variant and not the turbo one, which is faster: turbo is
guidance-distilled. Guidance is the mechanism that makes a negative prompt
exist at all, since it runs the model on both prompts each step and pushes the
result away from the negative. Distilled variants force guidance to zero, so
they accept --negative-prompt and discard it in silence. Half of this project's
visual system is prohibition, so that trade is not available to us.

Known cost, accepted for now: this shells out, so every image reloads the model
from disk. The CLI is the surface mflux documents and describes in machine
readable form, and correctness comes before throughput. If iteration gets
tedious, the fix is a resident worker process, not a different model.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from .base import ImageBackend, ImageRequest, ImageResult

DEFAULT_MODEL = "mflux-community/z-image-base-mflux-q4"
BASE_MODEL = "z-image"
COMMAND = "mflux-generate-z-image"


class LocalMFluxBackend(ImageBackend):
    name = "local"
    prompt_dialect = "diffusion"

    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.environ.get("MFLUX_MODEL") or DEFAULT_MODEL

    def _binary(self) -> str | None:
        # Prefer the one in this venv over anything on PATH, so the backend does
        # not silently run a different install than the one requirements-local
        # describes.
        local = Path(__file__).resolve().parents[2] / ".venv" / "bin" / COMMAND
        if local.is_file():
            return str(local)
        return shutil.which(COMMAND)

    def available(self) -> tuple[bool, str]:
        if not self._binary():
            return False, (
                f"{COMMAND} not found. Install with "
                "./.venv/bin/pip install -r requirements-local.txt"
            )
        return True, ""

    def generate(self, request: ImageRequest) -> ImageResult:
        binary = self._binary()
        if not binary:
            raise RuntimeError(f"{COMMAND} not found")

        width, height = (int(v) for v in request.size.lower().split("x"))
        steps = os.environ.get("MFLUX_STEPS", "24")
        # Must stay above 1.0. At or below it, guidance is off, there is no
        # second pass, and everything in the negative block is discarded.
        guidance = os.environ.get("MFLUX_GUIDANCE", "3.5")
        if float(guidance) <= 1.0:
            raise RuntimeError(
                f"MFLUX_GUIDANCE is {guidance}, which disables guidance and "
                "throws the negative prompt away. Use a value above 1.0."
            )

        out = request.out_path or Path("out/local.png")
        out.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            binary,
            "--model", self.model,
            "--base-model", BASE_MODEL,
            "--prompt", request.prompt,
            "--negative-prompt", request.negative_prompt,
            "--guidance", guidance,
            "--steps", steps,
            "--width", str(width),
            "--height", str(height),
            "--output", str(out),
            # Peak memory lands in the VAE decode, not in the weights. Tiling it
            # is what keeps a 16 GB machine off swap.
            "--vae-tiling",
            "--mlx-cache-limit-gb", os.environ.get("MFLUX_CACHE_GB", "6"),
        ]
        if request.init_image:
            if not request.init_image.is_file():
                raise RuntimeError(f"no such init image: {request.init_image}")
            cmd += ["--image-path", str(request.init_image),
                    "--image-strength", str(request.init_strength)]

        seed = os.environ.get("MFLUX_SEED")
        if seed:
            cmd += ["--seed", seed]

        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            tail = (proc.stderr or proc.stdout).strip()[-800:]
            raise RuntimeError(f"{COMMAND} exited {proc.returncode}:\n{tail}")
        if not out.is_file():
            raise RuntimeError(
                f"{COMMAND} reported success but wrote no file at {out}"
            )

        return ImageResult(
            path=out, backend=self.name, model=self.model,
            prompt=request.prompt, negative_prompt=request.negative_prompt,
            cost_note=(f"local, no cost, {steps} steps at guidance {guidance}"
                       + (f", from {request.init_image.name} at strength "
                          f"{request.init_strength}" if request.init_image else "")),
        )


CN_COMMAND = "mflux-generate-z-image-controlnet"
CN_MODEL = "mflux-community/z-image-turbo-controlnet-union-2-1-mflux-q4"


class LocalControlNetBackend(LocalMFluxBackend):
    """Structure from a reference drawing, colour from the prompt.

    The one thing init_image cannot do. An init image is inherited pixel by
    pixel, so holding a shape also holds whatever colour was in it; that is why
    a pale pair of trousers stayed pale at every strength that kept the
    composition. A control image is converted to an edge map first, so it
    carries shape and nothing else.

    The price is stated rather than hidden: ControlNet Union for Z-Image runs on
    the turbo variant, which is guidance-distilled. `--negative-prompt` and
    `--guidance` are both `ignored` there. Every prohibition in the spec's
    negative block is discarded. That is survivable here only because a line
    drawing used as the control already prevents most of what those words
    prevented, and it is the reason this is a separate backend rather than a
    flag: the loss should be visible in the registry.
    """

    name = "local-cn"
    prompt_dialect = "diffusion"
    uses_negative = False

    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.environ.get("MFLUX_CN_MODEL") or CN_MODEL

    def _binary(self) -> str | None:
        local = Path(__file__).resolve().parents[2] / ".venv" / "bin" / CN_COMMAND
        if local.is_file():
            return str(local)
        return shutil.which(CN_COMMAND)

    def available(self) -> tuple[bool, str]:
        if not self._binary():
            return False, f"{CN_COMMAND} not found; run make setup-local"
        return True, ""

    def generate(self, request: ImageRequest) -> ImageResult:
        binary = self._binary()
        if not binary:
            raise RuntimeError(f"{CN_COMMAND} not found")
        if not request.control_image or not request.control_image.is_file():
            raise RuntimeError(
                "the controlnet backend needs --control pointing at a drawing "
                "whose structure should be held"
            )

        width, height = (int(v) for v in request.size.lower().split("x"))
        steps = os.environ.get("MFLUX_CN_STEPS", "12")
        out = request.out_path or Path("out/local-cn.png")
        out.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            binary,
            "--model", self.model,
            "--prompt", request.prompt,
            "--control", f"{request.control_type}:{request.control_image}:"
                         f"{request.control_strength}",
            "--steps", steps,
            "--width", str(width),
            "--height", str(height),
            "--output", str(out),
            "--vae-tiling",
            "--mlx-cache-limit-gb", os.environ.get("MFLUX_CACHE_GB", "6"),
        ]
        seed = os.environ.get("MFLUX_SEED")
        if seed:
            cmd += ["--seed", seed]

        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            tail = (proc.stderr or proc.stdout).strip()[-800:]
            raise RuntimeError(f"{CN_COMMAND} exited {proc.returncode}:\n{tail}")
        if not out.is_file():
            raise RuntimeError(f"{CN_COMMAND} reported success but wrote no file")

        return ImageResult(
            path=out, backend=self.name, model=self.model,
            prompt=request.prompt, negative_prompt="",
            cost_note=(f"local controlnet, no cost, {steps} steps, "
                       f"{request.control_type} at {request.control_strength}. "
                       f"Negative prompt discarded: this model is distilled"),
        )
