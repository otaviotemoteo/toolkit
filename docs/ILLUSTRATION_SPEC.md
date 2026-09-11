# Illustration spec

The visual system for every generated image. Written from scratch for these
tokens rather than adapted from someone else's spec, so that every rule here
exists for a reason we can name.

---

## The one rule everything follows

**Flat shapes, muted colour, soft grain. What is alive is not what has colour,
it is what changes.**

Every illustration is built from clean flat shapes filled with muted colour and
finished with a soft paper grain. No gradient, no rendered light, no attempt at
volume. It reads as a considered illustration rather than as a sketch or a
render, which is the register that sits calmly on a page next to text.

This replaced a hand-drawn ink line, which was itself a replacement for a
monochrome technical drawing. Both earlier versions are in
`docs/solutions/`. The direction settled here after seeing the three side by
side: the ink line read as charming but restless beside body copy, and the flat
version reads as calm without reading as generic.

Colour is therefore the baseline, not the signal. What carries meaning is
**difference between assets**: the character, the furniture and the machine are
identical wherever they appear, so the set reads as one place at different
moments rather than as a pile of separate drawings.

This replaced an earlier rule, that colour lived only in the machinery. That
rule was coherent and it was abandoned deliberately, because the coloured
character reads as a person and the monochrome one read as a diagram. The cost
is real: the accent no longer signals by being the only colour, so the signal
had to move to change.

## Tokens

Never invent a colour outside this list.

Ground and line.

| Token | Hex | Where |
|---|---|---|
| `PAPER` | `#F7F6F3` | background of every illustration |
| `PAPER-DEEP` | `#EFEEE9` | raised surface, a far wall |
| `INK` | `#16161A` | every outline, and true black objects |
| `INK-SOFT` | `#5A5A66` | secondary line, distant object, cable |
| `ACCENT` | `#5D5D9C` | interface accent, and anything that moves |
| `WASH` | `#ECECF5` | soft fill behind an accent element |

The character. Fixed across every asset; changing one of these is changing who
he is.

| Token | Hex | Where |
|---|---|---|
| `SKIN` | `#F2D5C0` | face, neck, arms, hands |
| `HAIR` | `#2B2118` | hair, drawn as mass rather than outline |
| `SHIRT` | `#FBFBF9` | the white t-shirt, a shade off the paper so it reads |
| `DENIM` | `#4A6FA5` | the blue trousers |
| `SOLE` | `#16161A` | the black sneakers |

The workstation.

| Token | Hex | Where |
|---|---|---|
| `WOOD` | `#A9764C` | the desk top and its legs |
| `CASE` | `#1E1E22` | monitor bezels, laptop body, the tower |
| `SCREEN` | `#101018` | the dark interior of every screen |

The code on screens. Muted on purpose: these are the most saturated colours in
the system and they still sit below a highlighter.

| Token | Hex |
|---|---|
| `CODE-A` | `#5D5D9C` |
| `CODE-B` | `#C77D5A` |
| `CODE-C` | `#6E9E6B` |
| `CODE-D` | `#C9A34E` |

Paper steps for edges and surfaces, taken from the wireframe:
`#E2E1DC`, `#DCDAD3`, `#D6D3CB`, `#CBC8C0`.

## Texture

One texture, and it is not shading. **Diagonal hatching at 45 degrees**, 4px
stroke with 6px of space, in `INK` at 4.5% opacity, or in `ACCENT` at 6-7% when
the surface belongs to the machinery.

```css
repeating-linear-gradient(45deg, rgba(22,22,26,.045) 0 4px, transparent 4px 10px)
repeating-linear-gradient(45deg, rgba(93,93,156,.07)  0 4px, transparent 4px 10px)
```

Every shadow in every illustration is this hatch. There is no soft shadow, no
gradient fill, no airbrush, no halftone dot. Hatching reads as technical
drawing, which is the register this whole system is in.

## Line and mass

This is the rule that decides whether an illustration works, and it is the one
most likely to be violated by a generator left to itself.

**Flat fill inside the line, and the fill never shades.** A shirt is a contour
with one flat colour inside it. A monitor is a bezel of one flat dark with a
screen of another. There is no highlight, no shadow side, no blend from light to
dark anywhere on any surface.

The failure this prevents is the one that ruins the register. The moment a
generator starts rendering light, the drawing stops being a drawing and starts
being a bad 3D render: soft shadow under the chin, gradient down the trousers, a
shine on the monitor. Flat fill keeps it a drawing that happens to be coloured.

**Test:** cover the outlines and what is left should look like paper cut-outs,
not like a photograph with the edges traced.

## Line weight

Two weights, and only two.

- **Contour**, roughly 3px at 1024 wide: the outline of a figure, a monitor
  frame, a desk edge.
- **Detail**, roughly 1.5px: fingers, cables, code lines, small props.

**Drawn, not ruled.** The line is allowed to wobble, to overshoot a corner, to
show a construction stroke that was never erased. This is deliberate and it is
the character of the whole system: it reads as made by a person, which is the
one thing a generated illustration usually fails to read as.

What it is not: scribbled, hairy, or so loose the form is unclear. One or two
searching lines per limb, not twenty.

## What changes between assets, and what never does

This is the rule that replaced "colour lives in the machinery".

**Never changes, anywhere.** The line register and the palette. And wherever the
character or the desk appear: his face, hair, build, clothes and their colours,
the desk, the tower, the cables, the pen cup, their positions and their colours.

**Within the desk scenes, only the screens change.** The difference between two
of them is the difference between two moments at the same desk: a diff, a test
run, a stack trace, a graph, a terminal mid-command. Those briefs carry a
`## Screens` section, and it is the only field expected to differ.

**Outside the desk scenes, everything changes but the register.** The set this
spec serves is small and mostly not the desk: a shared spreadsheet, two contrasting
personas, a stack of layers, a three panel strip. They share the palette, the
line weight and the flat mass, and nothing else. An earlier version of this file
claimed the whole set was one desk with different screens on it. That was
written before the inventory existed, and the inventory says otherwise.

## Composition

- Off-white ground, never pure white. `PAPER`, with `PAPER-DEEP` if a wall or
  surface needs to separate.
- One ground line. Objects sit on it. No floating, no drop shadow beneath.
- Generous margin. Nothing touches the frame.
- Front-on or slight three-quarter. No dramatic perspective, no vanishing point
  doing work.

## Never

- Gradient or shading inside any filled area
- Glow, blur, soft shadow, cast shadow on the floor, glassmorphism
- 3D, photorealism, texture that imitates a material
- Halftone dots, stippling, cross-hatching that is not the 45 degree hatch
- Decorative clutter: plants, coffee cups, sticky notes, floating icons
- Text inside the illustration unless the brief asks for it by name
- Watermark, signature, frame border

## Two modes

Pick one before generating. Do not mix.

**Mode A, composed illustration.** The image explains something by itself and
carries its own labels. Rare here: most explanation lives in HTML.

**Mode B, subject on paper.** The illustration is composed into a layout that
supplies the words. This is the default for this project. Generate directly on
`PAPER`, and do not cut anything out.

Cutting out was tried and abandoned. The measurements behind that, and the two
keyers that failed before this one, are in
`docs/solutions/the-wrong-keyer.md`. A chroma key needs a perfectly flat
background, which diffusion models do not produce: the first real generation
came back with a pale mint instead of the requested `#00FF00`, striped, with a
soft blob in one corner. A luminance key works beautifully for pure line art and
stops working the moment the character is coloured, because blue trousers are
neither ink nor paper.

Since the page ground is `PAPER` anyway, a baked-in paper background is not a
compromise, it is one fewer step that can fail. Revisit only for an asset that
must overlap something that is not paper.

`<KEY_COLOR>` therefore means `#F7F6F3` unless a brief says otherwise.

## The style anchor

Append verbatim to every Mode B prompt. Replace `<KEY_COLOR>`.

```text
Style: flat illustration with clean rounded forms and a fine paper grain, in
the register of a considered editorial drawing rather than a sketch or a render.
Every surface is one even area of muted colour, laid down without blending,
without highlight and without a shadow side. The lighting is flat and even
across the whole scene, with no direction to it.
Light skin, dark brown hair, a plain white t-shirt, blue trousers and black
sneakers. A brown wooden desk, matte black monitor bezels, a matte black laptop
body and a matte black computer tower. Dark screens carrying lines of code in
muted syntax colours.
Flat front-facing view. Objects rest on a single ground line.
The background is a plain flat <KEY_COLOR> field with nothing in it: no
scenery, no wall, no shape behind the subject. Keep generous padding; nothing
in the artwork touches the image border. PNG format.
```

## The diffusion anchor

A second expression of the same system, for local diffusion models. It exists
because those models read differently, not because the visual system changed.

An instruction-following model is told "no filled black" in a sentence and
mostly obeys. A diffusion model is steered by classifier-free guidance: at every
step it runs once on the positive prompt and once on the negative one, and the
result is pushed away from the second. A prohibition written as prose in the
positive prompt therefore does the opposite of what it says, because the words
present in the text are the words being aimed at.

So the prohibitions move out of the prose and into their own block, and they
change grammar: comma-separated nouns, not sentences.

Two rules follow from that mechanism, and both are load-bearing:

- **Guidance must be above 1.0.** Below it, guidance is off, there is no second
  pass, and the negative block is silently discarded. Distilled models, anything
  named turbo or schnell, force guidance to zero and can never honour a negative
  prompt at all.
- **Nothing appears in both blocks.** A word in the positive and the negative at
  once is the model being pulled in both directions, and what comes out is a
  half measure rather than either instruction.

**The anchor carries only what is true of every asset.** It used to name the
desk, the monitor bezels, the tower and the screens, and that clause was sent
with every run of every brief. A brief asking for a figure alone on empty paper
got a workstation three clauses later and the model drew one, in all six
samples. The clause was also redundant: both desk briefs describe the desk in
their own prose, colours included. What is not universal belongs in the brief
that wants it.

Nothing was added to the negative block in its place. A shared prohibition on
desks would break the brief whose subject is a desk.

Positive. Replace `<KEY_COLOR>`.

```text
flat illustration with clean rounded forms and a fine paper grain, flat even
lighting across the whole scene, every surface one even area of muted colour
laid down without blending, light skin, dark brown
hair, plain white t-shirt, blue trousers, black sneakers,
plain empty <KEY_COLOR> background, generous padding around the artwork
```

Negative.

```text
photograph, photorealistic, 3d render, cgi, painterly, oil painting, watercolour,
airbrush, gradient, highlight, specular, glow, bloom, blur, soft shadow, cast
shadow, drop shadow, ambient occlusion, depth of field, vignette, wall,
wallpaper, scenery, shape behind the subject, halftone dots, stippling, neon,
garish, oversaturated, plants, mugs, sticky notes, posters, watermark,
signature, frame, border, cropped
```

## Retry, do not regenerate

When something is wrong, change one thing and hold everything else. Regenerating
from the same prompt and hoping for a different result is how credit gets burned.

```text
Keep the scene, composition, character, pose, objects, line weights, hatching
and colour exactly as they are.
Change only <the one thing>.
Do not alter anything else, do not add or remove any element.
```

## Quality gate

Before an image is accepted:

- The subject is recognisable in about three seconds.
- Every filled area is flat. Pick any surface and its colour should be the same
  at both ends of it.
- The palette is the one in Tokens. No colour appears that is not on that list.
- The line reads as hand-drawn: at least one visible construction or overshoot
  stroke, and no sign of a vector or a ruler.
- Any shading present is 45 degree hatching. No soft shadow, and nothing casts a
  shadow onto the floor.
- The background is empty. No wall, no vignette, no shape behind the subject.
- Nothing touches the frame, and there is clear space between the character and
  the furniture.
- No readable words appeared that the brief did not ask for.
- The screens match this brief's `## Screens` section, and nothing else in the
  image differs from the approved reference.

## What was taken from oil-visual, and what was not

`oil-visual` (MIT, github.com/oil-oil/oil-visual) is the structural model for
this file. Four things were taken because they are craft rather than identity:

1. The A/B mode split, and the rule to choose one before generating.
2. The verbatim-text block that stops a generator inventing or misspelling
   labels.
3. The surgical retry instruction above.
4. `scripts/cutout.py`, called directly rather than copied.

Everything visual was written from scratch. The original is built on manga ink,
circular halftone, a stick figure in round glasses and a warm-yellow Border
Collie, and the two systems are opposites in texture: theirs is organic and
dotted, this one is geometric and hatched. Adapting theirs would have made it
impossible to tell which rules are craft and which are someone else's taste.
