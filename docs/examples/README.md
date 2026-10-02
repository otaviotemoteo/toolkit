# Examples

One asset, followed from its first failed run to the image that was approved.
Every picture here was generated locally through mflux, on the briefs shown, and
every one has its JSON sidecar beside it, so the prompt quoted in the text can be
checked against the prompt that was actually sent.

Nothing was staged for this page. These are the real frames of the afternoon
that produced `briefs/hero-character/`, kept because a rule like "never write a
prohibition in the positive block" reads as superstition until you see the image
that put it there.

## If you look at one pair

Frames 4 and 5 were sent the same prompt except for one paragraph.

<table>
<tr>
<td><img src="hero-first-pass/4-desk-behind-him.png" width="340" alt="rejected"></td>
<td><img src="../../briefs/hero-character/approved/hero-character-v1.png" width="340" alt="approved"></td>
</tr>
<tr>
<td><b>Rejected.</b> "The desk is entirely to his right, never behind him." The desk went behind him.</td>
<td><b>Approved.</b> The same, plus: "The desk is narrow and occupies only the right half of the scene. Between him and the desk there is a vertical strip of empty background."</td>
</tr>
</table>

The first says where the desk must not be. The second says what is there
instead. That is most of what this folder has to teach, and
[case 4](bad-briefs.md#4-a-relation-written-as-a-prohibition) and
[the good brief](good-brief.md) are the two halves of it.

## Read in this order

| | Page | What you get from it |
|---|---|---|
| 1 | [`bad-briefs.md`](bad-briefs.md) | four briefs that failed, the image each produced, the fault you can point at, and the rule it broke |
| 2 | [`good-brief.md`](good-brief.md) | the brief that was approved, why it worked, and what is still wrong with it |
| 3 | [`../guide.md`](../guide.md) | the commands, when you want to run your own |

## The five frames

| # | Backend | What came back | Verdict | Read |
|---|---|---|---|---|
| 1 | `local` | sketch on a striped green ground, screens nearly empty | rejected | [bad, case 1](bad-briefs.md#1-the-brief-that-argued-with-itself) |
| 2 | `local` | every colour right, desk cropped by the frame and behind him | rejected | [bad, case 2](bad-briefs.md#2-right-colours-wrong-frame) |
| 3 | `local-cn` | flat style, a blank face, and a ghost of a second man | rejected | [bad, case 3](bad-briefs.md#3-the-prose-and-the-control-disagreed) |
| 4 | `local-cn` | a face at last, and the desk straight through his legs | rejected | [bad, case 4](bad-briefs.md#4-a-relation-written-as-a-prohibition) |
| 5 | `local-cn` | figure clear of the desk, flat, on plain paper | **approved as v1** | [good](good-brief.md) |

<table>
<tr>
<td><img src="hero-first-pass/1-ink-on-chroma.png" width="180" alt="frame 1"></td>
<td><img src="hero-first-pass/2-right-colours-wrong-frame.png" width="180" alt="frame 2"></td>
<td><img src="hero-first-pass/3-ghost-of-the-control.png" width="180" alt="frame 3"></td>
<td><img src="hero-first-pass/4-desk-behind-him.png" width="180" alt="frame 4"></td>
<td><img src="../../briefs/hero-character/approved/hero-character-v1.png" width="180" alt="frame 5, approved"></td>
</tr>
<tr><td>1</td><td>2</td><td>3</td><td>4</td><td>5, approved</td></tr>
</table>

## How each case is laid out

The same four parts every time, so the pages can be skimmed:

1. **What was sent.** The part of the prompt that mattered, quoted from the
   sidecar.
2. **What came back.** The image.
3. **What is wrong, observably.** Something you can point at, not an opinion.
4. **The rule, and what changed.** The lesson in `docs/solutions/` and the edit
   that followed.

## What these examples are not

They are not a claim that the last brief is a recipe. A diffusion model samples,
so the same brief gives a different image on the next run, and frame 5 was
accepted with defects that are listed on its page. A good brief makes a good
image likely; it does not make it certain. What
transfers is the reading of a failure: look at the image, find the sentence in
the prompt that asked for it, and change that sentence rather than rolling
again.

They are also the beginning of the story and not the end. The character the
hero actually ships with was not generated here, and the scene that moves was
cut from an approved drawing rather than generated at all. `good-brief.md` ends
on why, and `docs/guide.md` section 6 is the rule that came out of it.

## The files

```
docs/examples/hero-first-pass/
    1-ink-on-chroma.png              .json
    2-right-colours-wrong-frame.png  .json
    3-ghost-of-the-control.png       .json
    4-desk-behind-him.png            .json
briefs/hero-character/
    brief.md                         the brief, as it stands today, rewritten since
    approved/hero-character-v1.png   .json    frame 5
    approved/README.md               the recipe and the accepted defects
```

Frames 1 to 4 are copies of rejected runs. In normal use a rejected run stays in
`briefs/<name>/out/`, which is untracked; these four are tracked only because
they are the examples.
