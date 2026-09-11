# Asset map

What gets made, and by which route. Read this before opening a new brief: the
route decides the brief's shape, the cost, and what can check the result.

`docs/ILLUSTRATION_SPEC.md` sets the number at eighteen illustrations and says
the thing that shrinks the work: **what changes between assets is what is on the
screens, and nothing else.** The character, the desk, the tower, the cables,
their positions and their colours never change. So most of what is left is not
eighteen drawings. It is one drawing and seventeen screens.

## The five routes

| Route | Produced by | Deliverable | Cost per asset | Checked by |
|---|---|---|---|---|
| Fixed identity | already approved, never regenerated | layer PNGs plus `scene.json` | none | `check_scene`, `check_render` |
| Scene still | the approved scene, with screen content composited in | one PNG | none | palette and geometry checks |
| Motion | runtime transforms on the identity layers | `scene.json` plus a small script | none | `check_render` |
| Diagram | a written description, drawn as vector | SVG, inline in the page | none | palette check against the spec tokens |
| Generation | a model, from a brief | one PNG, then approval | minutes of local compute | `check_briefs`, `check_anchors` |

The order matters. **Generation is the last route, not the first.** It is the
only one that is not reproducible, the only one that costs time, and the only
one where the same input can give a different output. Everything above it is a
function.

## How to pick

Ask one question about the thing being made:

**Does it need pixels that were never drawn?**

If no, it is composition, and the identity is preserved by reusing the same
pixels rather than by hoping. A different angle of the same flat object, a
different screen, a different crop, a different arrangement, all no.

If yes, it is generation. A real head turn is yes: the far ear disappears and
the nose crosses the silhouette. An arm that is currently hidden behind crossed
arms is yes, and no amount of inpainting invents it, because inpainting heals
small areas and does not draw limbs.

## Fixed identity, and why it travels

The character is the one asset that is not a picture. It is a small package that
any page can mount:

```
briefs/hero-character/approved/scene/
    scene.json    the contract: canvas, layers, pivots, limits
    plate.png     desk and everything on it
    body.png      static
    head.png      rotates about the base of the neck
    eyes.png      rotates with the head, then translates
preview/hero.js   about 150 lines, no dependencies, mounts into any element
```

Nothing else is required, there is no build step and no framework. That is the
whole reason to keep it: a fixed character that reacts to a cursor is a visual
identity that is alive rather than a logo, and it can appear in more than one
place without being redrawn for each.

**What must hold for that to stay true.** `scene.json` is the contract, so
anything that reads it reads only it, never the pixel numbers directly. The
files are frozen: a new version is a new number, and the old one stays. And the
layers stay mutually exclusive, because two layers cut from one flat drawing
cannot share a pixel. See
`docs/solutions/two-raster-layers-cannot-share-a-pixel.md`.

## Scene stills, the seventeen

The spec's rule means each of these is the approved scene with different screen
content: a diff, a test run, a stack trace, a graph, a terminal mid command.

Screen content is the most deterministic thing in the project. It is monospaced
text on a dark rectangle. It can be rendered exactly and placed on the monitor
with a perspective transform from the four corners, so the same scene yields as
many assets as there is content to put on it, with no drift and no sampling.

What this needs before it can start: the monitor corners measured once and added
to `scene.json` as a new field, a renderer for the screen itself, and a check
that the corners lie inside the plate and form a convex quadrilateral.

The honest risk: the generated screens carry a slight glow and the bezel eats a
few pixels at the edge. If a composited screen reads as a sticker, it is the
same failure as the flat colour fill that left a halo, and the same class of fix
applies. Nothing settles it except trying it.

## Diagrams

A diagram is not an illustration and does not go near a diffusion model. The
route is: write the description, have it drawn as vector, ship the SVG inline.

Why inline SVG rather than a PNG: it stays sharp at any size, it costs almost
nothing to transfer, its text is selectable and readable by a screen reader, and
its colours are the same tokens as everything else rather than a rendering of
them. That last point is checkable, which a PNG is not.

The brief for a diagram carries what any brief carries, plus the thing being
explained and the one sentence a reader should leave with. If a diagram needs a
paragraph of explanation beside it, the diagram has not been written yet.

## Motion

One asset is animated so far, and the rule that produced it is worth keeping:
**the acceptance criterion decides the route**. `motion.md` required the body
and the desk to be pixel identical between states. No generator delivers that,
so the route stopped being generation before any image was made.

Anything else that moves gets the same test first.

## Where each asset stands

| Asset | Route | State |
|---|---|---|
| `hero-character` | fixed identity, motion | approved, animated, frozen |
| `hero-desk` | generation | brief written, image generated, kept as proof the brief works. The shipped plate is a crop of the approved scene, because it shares lineage with the character and nothing has to be matched by eye |

The remaining seventeen are not named yet. Naming them is a decision about the
page, not about this repository, and a brief without a place to live is a brief
nobody can accept.
