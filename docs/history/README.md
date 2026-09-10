# History

The archive of what each round of iteration actually produced. Everything in
here except this file is untracked, because it grows without bound and none of
it is needed to use the toolkit.

It is kept anyway, and locally, for one reason: the images a pipeline rejected
are the only evidence of why its rules exist. A spec full of oddly specific
prohibitions reads as superstition until you see the six frames that put each
one there.

## What a round looks like

One directory per round, named for what it was trying to settle.

```
docs/history/
  2026-09-07-hero-first-pass/
    01-probe.png
    02-chroma-monochrome.png
    ...
    notes.md
```

`notes.md` carries the part the images cannot: what question the round was
asking, which frame answered it, and what changed in the spec or the brief as a
result. A directory of pictures with no note is a directory nobody will read.

## What belongs here and what does not

Here: rejected frames, intermediate composites, contact sheets, timing runs,
anything that was true on the day and is not true now.

Not here: an approved asset, which lives in `briefs/<name>/approved/` and is
tracked, because it is a decision rather than a by-product.

## First round, for reference

`2026-09-07-hero-first-pass` covers the hero character from the first technical
probe to the approved figure: twelve generated frames, six of which became the
published contact sheet. What it settled, in order: that the visual system could
be described in a file at all, that the first two visual directions were wrong,
that a guidance-distilled model cannot hold a style but can propose one, and
that identity across assets is a compositing problem rather than a generation
problem.
