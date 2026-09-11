---
title: A pivot written in pixels is a pivot at one size only
date: 2026-09-11
tags: [animation, rendering, css, silent-failure]
enforced_by: check
check: scripts/check_render.mjs
fixture: tests/fixtures/render/README.md
code_in: preview/hero.js
---

## What was wrong

The head's joint is a point measured in the character's own file: x 178,
y 238, the base of the neck. The renderer handed that straight to CSS.

```js
return `${pivot[0]}px ${pivot[1] - L.top}px`;   // "178px 238px"
```

A layer on the page is an `<img>` that CSS scales to whatever width the
container gives it. `transform-origin` in px is measured against the element as
rendered, not against the file the number came from. The two agree at exactly
one size: file resolution. Nowhere else.

## Why it was not caught

The error is proportional to how far the element is from its native size, so it
hides at the size you review at and grows as the page shrinks. Measured in the
browser, on the same page, at the same moment:

| rendered | head `<img>` | origin should be | origin was | joint slides at 6.5 deg |
|---|---|---|---|---|
| hero | 282 x 195 | 181px | 238px | about 6px |
| grid cell | 92 x 63 | 58.6px | 238px | 21.2px across, 14.0px up |

In the cell the pivot sat 175px below the bottom of the head, nearly three head
heights outside it. The head was not turning on the neck. It was swinging on the
end of a long invisible arm hanging below the character, and the neck left the
collar entirely.

The hero had been checked at full size and at 4x zoom on the collar. Both were
the same render size. The whole class of fault was outside what was looked at.

## The two wrong explanations, in the order they are tempting

**"The angle is too large."** It is the first thing the picture suggests and it
is not the fault. Reducing `lean_deg` scales the escape down without removing
it, and leaves it proportional to render size, so it comes back on a smaller
screen. A number tuned until a symptom is tolerable at one viewport is not a
fix, it is a disguise.

**"`scripts/check_scene.py` already checks the pivot."** It checks that the
pivot lies inside its layer, which it does, in the manifest, in file
coordinates. The manifest was right the whole time. The renderer was wrong about
what unit the manifest was in. A contract check cannot catch a consumer
misreading the contract.

## What replaced it

A share of the element's own box, which the browser resolves against whatever
size the element happens to be:

```js
return `${(pivot[0] / ch.file_size[0]) * 100}% ` +
       `${((pivot[1] - L.top) / L.height) * 100}%`;
```

For the head, `48.1% 92.97%`, at every size. Measured drift of the neck point at
full lean afterwards: 0.04px across, 0.02px down. Subpixel, which is the only
acceptable number here, because rotation about a pivot is defined by the pivot
not moving.

## The general form

**A coordinate is meaningless without the space it was measured in.** Every
number this repository takes out of an image file, pivots, eye boxes, the neck
band, is in file space. Anything that renders is in layout space. Crossing
between them is a conversion, and a conversion that is skipped looks exactly
like a conversion that was done, until something is displayed at a size nobody
tried.

## Where it is enforced

`scripts/check_render.mjs`, in `make check` and `make mutation`. It imports
`originFor` and `TURNS_WITH` from `preview/hero.js` rather than restating the
arithmetic, for the same reason `scripts/check_anchors.py` extracts through
`generate.py`: a check holding its own copy of the thing it checks stops
checking on the day the original is edited. It resolves the origin at four
render widths, from 40px to 1102px, and fails if the point the layer turns on is
more than 0.01px from the pivot at any of them.

`tests/fixtures/render/px-origin.mjs` is the old version, kept and required to
fail.
