# render fixtures

`px-origin.mjs` is the transform-origin this repository actually shipped: the
pivot in file pixels, handed to CSS as if the element were always rendered at
file resolution.

`make mutation` runs `scripts/check_render.mjs` against it and requires a
failure. A pass means the check no longer detects a moving joint, and the hero
can come apart with every check green.

The reasoning, and the measurements that found it, are in
`docs/solutions/a-pivot-in-pixels-is-a-pivot-at-one-size.md`.
