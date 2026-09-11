# Decisions

Read before reopening a settled question. Each entry says what was decided, why,
and what would justify revisiting it.

## Settled

**No LoRA training.** Decided 2026-09-07, and the reason matters more
than the decision: the value here is the harness, the local pipeline and guided
iteration, and the declared focus is a consistent UI. A LoRA solves arbitrary
pose, which this project can avoid by deciding its poses in advance, and would
cost hours of setup, training and validation on a 16 GB machine for an uncertain
result.

What replaces it: a small library of approved poses, frozen as files and
recomposed, plus transforming parts, which flat illustration with no light
direction accepts well.

Reopen only if an asset genuinely needs a new arbitrary pose, and then only
after counting how many do. If it comes back, it comes back as its own chapter
of the toolkit, chosen rather than pretended into necessity.

**The hero animation is compositing, not generation.** Its own brief carries the
reasoning: `briefs/hero-character/motion.md`.

**The local backend is the route, not a fallback.** The earlier note deferring
MLX in favour of a hosted model is obsolete: local is what phase 1 shipped on.

## Open

**Vectorising the character**, instead of keeping raster layers. Worth trying, and the moment is defined: after the hero closes end to end in raster,
not before.

Why it is worth trying: what makes the reference sites look easy is not the
animation library, it is that the asset arrives as vector with named groups. A
head that exists as an object can be rotated in one line. A flat PNG has no
notion of a head, which is the wall this project hit when trying to separate the
character from the desk.

Why it might work here: automatic tracing does badly on photographs and textured
drawing, and well on flat colour with clean contours, which is the style that was
chosen. Trace, group by region, compare with the raster at 100%. If the line
survives, migrate. If not, adapt and stay in raster, which already works.

**A UI for other people.** For later: an API key field, a loose
brief that a model structures into this format, a generate button, an
approve-or-reject loop. The architecture already allows it, since a UI would sit
on top of `generate.py` rather than replace it. Two cautions for the day it
happens:

1. The model structuring a brief must be given the spec as mandatory context and
   must refuse a brief with no observable acceptance criteria. What makes the
   format work is that it forces decisions, not the format itself. Without that
   it becomes a generator of pretty text and pushes the problem downstream.
2. An API key field in a hosted UI means asking strangers to paste paid
   credentials into your site. Local execution avoids it and costs nothing.

**`zenmux.py` has never been executed.** Its endpoint and response shape are
assumed from OpenAI compatibility. It exists to prove the interface is an
interface, and deserves no confidence until one real call.

**The three-scene strip:** a continuous morph, or three cuts. Decide with the
real cost in hand.
