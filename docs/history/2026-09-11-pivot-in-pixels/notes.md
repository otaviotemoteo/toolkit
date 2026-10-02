# The head that left the neck

Otávio opened the preview and the head was floating clear of the collar in the
grid, shifted right and lifted. His reading was that the lean angle was too big.

It was not the angle. `preview/hero.js` handed CSS a `transform-origin` of
`178px 238px`, the pivot in the character's own file pixels. A layer on the page
is an `<img>` that CSS scales, so px there means rendered px, and the two agree
only at file resolution.

Measured live in the browser, same page, same moment:

| rendered | head `<img>` | origin should be | origin was | joint slides at 6.5 deg |
|---|---|---|---|---|
| hero | 282 x 195 | 181px | 238px | about 6px |
| grid cell | 92 x 63 | 58.6px | 238px | 21.2px across, 14.0px up |

In the cell the pivot sat 175px below the chin, almost three head heights
outside the layer.

Replaced with `48.1% 92.97%`, a share of the element's own box. Drift after:
0.04px across, 0.02px down.

`pivot-before-after.png` renders both origins at the measured cell size, 358px.

Why it got through: the hero was reviewed at full size and at 4x zoom on the
collar, which is the same render size twice. The error is proportional to the
distance from file resolution, so reviewing at one size cannot see it.

Now `scripts/check_render.mjs` resolves the origin at four widths from 40px to
1102px and fails above 0.01px. It imports `originFor` and `TURNS_WITH` from
`preview/hero.js` instead of restating them.
Lesson: `docs/solutions/a-pivot-in-pixels-is-a-pivot-at-one-size.md`.
