---
title: The documentation said PNG; the API returned 400
date: 2026-09-07
tags: [vendors, adapters, defensive-parsing]
enforced_by: code
code_in: src/adapters/gemini.py
---

## Symptom

Google's image generation docs show `image/png` and `image/jpeg` as equally
supported for `response_format.mime_type`. The API answered:

```
400: The value 'image/png' is not supported for 'response_format.mime_type'.
Supported values: 'image/jpeg'.
```

## Why it mattered more than it looks

At the time the pipeline still generated onto a chroma background for cutting
out. JPEG places compression artefacts exactly along high-contrast edges, which
is precisely where the key colour meets the drawing, and those artefacts are
what a keyer cannot distinguish from the subject. A silently accepted JPEG would
have degraded every cut-out in a way that only shows at 100% zoom.

## Rule

The vendor's error body is the documentation. Capture it and show it, always:
`urllib` raises on 4xx and the body dies with the exception unless it is read
first, and a status line alone turns a five second fix into a guessing game.

Parse responses by shape, not by path. `src/adapters/gemini.py` walks the whole
response for the first base64 image rather than indexing a documented location,
because the cost of being wrong about the nesting is a spent request and an
unreadable `KeyError`.

## Where it is enforced

`src/adapters/gemini.py`: `find_image()` walks, `MIME` is overridable through
`GEMINI_IMAGE_MIME` so the day PNG is accepted is a variable and not a patch,
and the `HTTPError` handler reads the body before re-raising. The same handler
shape is in `openai_compatible.py`, which is where every vendor that does
follow its own documentation ends up.
