# Cost

Read before anything that could spend money.

## The constraint that decides the route

**There is no card.** This is not an account detail, it is what put phase 1 on
local generation.

Two published claims of free credit were tested and both were false. Treat a
third as a hypothesis until a real call says otherwise, and probe a credential
before building anything on top of it.

## Accounts

| Account | For | State |
|---|---|---|
| local, `mflux` | **images, the current route** | no account, no quota, no cost |
| `platform.openai.com` | images, if a card appears | key valid, no credit. `429 insufficient_quota`, tested 2026-09-04 |
| `aistudio.google.com` | text | key needs no card. Text works. Every image model reports `limit: 0`, tested 2026-09-04 |
| `zenmux.ai` | unused | never called |

## If a card appears

Buy prepaid API credit, not a subscription: no ChatGPT plan includes API credit,
and the two are separate billing systems. At roughly $0.005 an image, eighteen
assets at forty attempts each is under four dollars, which is inside the five
dollar minimum.

That would be worth doing for one reason only: instruction-following models obey
counts, framing and long prompts, which is where local diffusion is weakest.
Identity across assets stays a local, compositing problem either way.

## Local cost, measured

Z-Image at 4 bit on an M5 with 16 GB, peak 5.69 GB, no swap.

| Run | Wall clock |
|---|---|
| 512, 12 steps | 92s |
| 512, 24 steps | 153s |
| 768, 24 steps | 374s |
| 1024, 24 steps | ~480s |

About 31 seconds of every run is fixed overhead, the model loading from disk. A
resident worker would remove it, and has not been built because correctness came
first.
