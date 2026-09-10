# Brief: hero character, motion

Read `brief.md` first. That describes the still illustration; this describes what
it does once it is on the page. Nothing here is generated until the still is
approved, because the video inherits whatever the still got wrong.

**Where it lives:** home page hero, right side, above the fold
**Type:** parameter-driven, not a loop
**The idea in one sentence:** he notices you.

## What moves

**Head and eyes follow the cursor.** Nothing else.

The body stays exactly as drawn: arms crossed, weight even, feet planted. The
desk, monitors, laptop, tower and cables never move a pixel. The only thing that
changes between one frame and the next is the angle of the head and the position
of the pupils.

This is the cheapest of the three options that still reads as alive, and the
constraint is doing real work: because only the head moves, the neck is the only
place the drawing has to stay consistent, which is where a video model is most
likely to hold together.

## What never changes

Identity, proportion, line weight, hatching, framing, and the position of every
object in the scene. If the shirt changes shape between frames, or the desk
shifts, or the character's height moves, the frame is rejected. This is the
failure mode of AI video and the reason the still is approved first.

## The range

Two axes, because the cursor moves in two dimensions and a single left-to-right
strip cannot express both.

| | Far left | Centre | Far right |
|---|---|---|---|
| **Cursor high** | head turned left, chin slightly up | facing viewer, chin up | head turned right, chin slightly up |
| **Cursor centre** | head turned left, level | facing viewer, neutral, the still | head turned right, level |
| **Cursor low** | head turned left, chin slightly down | facing viewer, chin down | head turned right, chin slightly down |

The centre cell is the approved still. Everything else is a departure from it.

**Limits:** the head turns at most about 25 degrees to either side and tilts at
most about 12 degrees up or down. Past that it stops being a glance and starts
being a stretch, and a video model loses the face.

## Stages

Route A with `parameter_space: 2d`. Rather than one continuous video, generate
the extremes as keyframes and let the pipeline sample between them.

- `K0` centre, level. This is the approved still.
- `K1` head fully left, level
- `K2` head fully right, level
- `K3` centre, chin up
- `K4` centre, chin down

Each keyframe changes one thing from `K0` and holds everything else. Corners are
interpolated rather than generated: a model asked to turn the head and tilt it
at the same time tends to redraw the face.

## Runtime

Cursor position becomes an angle, the angle is smoothed so the head does not
snap, and the smoothed value picks a cell in the atlas. One DOM write per
animation frame, and only when the chosen cell actually changes.

When the pointer leaves the hero, the head returns to centre over roughly half a
second. When there is no pointer at all, as on a phone, the still is what shows.
`prefers-reduced-motion` gets the still and nothing else, handled once in the
primitive rather than per component.

## Acceptance

- The head follows the cursor across the full width and height of the hero
  without jitter at the extremes, and without snapping back when the cursor
  crosses the centre.
- Between any two adjacent cells, the only difference is head angle and pupil
  position. Shirt shape, shoulder line, desk and monitors are pixel-identical.
- The face stays recognisably the same person in all nine reference cells.
- On a touch device and under reduced motion, the still renders and nothing
  moves.
- Hair, ear and chin outlines survive the cutout at 100% zoom.

## Budget

Run `motion_budget.py --strict` before generating anything, with the real display
size, not a guess:

```bash
python3 ~/.claude/skills/oil-motion/scripts/motion_budget.py \
  --frames 240 --display 480x480 --dpr 2 --max-texture 4096 \
  --access random --strict
```

If the budget does not close, reduce the sampling grid before reducing quality.
A coarser grid with clean frames beats a fine grid that has to be compressed
until the line weight blurs.

**Estimated cost:** unknown until the budget runs and the ZenMux rate for
`minimax/minimax-h3` is checked on the day. Video is the one place in this
project where cost needs explicit confirmation before generating, so this brief
is not complete until that number is filled in here.

## Open

- Whether the pupils need their own frames or can be a small transform on top of
  the head frames. The second is much cheaper and may be enough; decide after
  seeing `K1` and `K2`.
- Whether four keyframes plus interpolation is sufficient, or whether the
  diagonal corners need generating too. Test with interpolation first.
