# Briefs

One directory per asset. Each holds a `brief.md`, an untracked `out/` that every
run writes into, and an `approved/` for the runs that were accepted.

These are the real briefs of the portfolio this toolkit was built for. They are
kept as worked examples of the format, and `make briefs` checks all of them.

## Start with this one

**[`hero-character/`](hero-character/brief.md)** is the only asset whose images
are in the repository. It has the brief, the approved images with the prompt
that produced them, the recipe, and the layers and manifest that make it move.
[`docs/examples/`](../docs/examples/README.md) follows it from its first failed
run to approval.

## The rest are text

Their approved images are not tracked: they are one person's site, and
[`docs/workspace.md`](../docs/workspace.md) says why. So when one of these
briefs names a file under its own `approved/`, a clone does not have it. Read
them for how a brief is written and for the `## Recipe` at the bottom, which
records what was actually run.

| Brief | What it is | Worth reading for |
|---|---|---|
| [`card-sales`](card-sales/brief.md), [`card-devtrack`](card-devtrack/brief.md), [`card-service-order`](card-service-order/brief.md), [`card-smart-home`](card-smart-home/brief.md), [`card-personal-tracker`](card-personal-tracker/brief.md) | project cards, 16:9, generated | the shortest complete briefs here, and a recipe that promotes a 768 draft to a 1024 candidate through `--init` |
| [`card-phishing`](card-phishing/brief.md) | a card that was tried twice as a chart | two dead ends recorded in the brief: a generated chart bends its own line, a drawn one is correct and says nothing. The card became a scene |
| [`hero-desk`](hero-desk/brief.md), [`contact-desk`](contact-desk/brief.md) | a desk with no figure | describing an object alone, and correcting a shadow afterwards instead of prompting it away |
| [`strip-scene`](strip-scene/brief.md), [`strip-fire`](strip-fire/brief.md) | a scene, and the same scene burning | an acceptance criterion that exists so a later script can work: no lit screen, so warm means fire |
| [`character-profile`](character-profile/brief.md) | the character side-on, cut into a walking puppet | a brief written for what will be cut out of the image, not for the image |
| [`contact-greeting`](contact-greeting/brief.md) | a looping greeting | **the one to read after the hero.** v1 was generated and came back a stranger; v2 is cut from the approved character and generates nothing |
| [`hero-character/motion.md`](hero-character/motion.md) | the hero's animation | a brief for motion, where the acceptance criterion decided the route before any image was made |

## Writing your own

Create `briefs/<name>/brief.md` with at least a `## Prompt` and a
`## Acceptance` section. Section 5 of [`docs/guide.md`](../docs/guide.md) has
the rules, and `make briefs` enforces the ones a script can.
