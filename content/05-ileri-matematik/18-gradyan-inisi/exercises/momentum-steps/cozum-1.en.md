**What is asked?** The first three steps of gradient descent with and without momentum.

**Idea:** With momentum, the velocity $v$ is updated first ($0.9$ of the old velocity plus the new gradient), then $w$ moves by the velocity.

**Step 1 — Momentum.**

| $k$ | $w_k$ | $L'(w_k)$ | $v_{k+1}$ | $w_{k+1}$ |
|---|---|---|---|---|
| $0$ | $1$ | $2$ | $2$ | $0.8$ |
| $1$ | $0.8$ | $1.6$ | $3.4$ | $0.46$ |
| $2$ | $0.46$ | $0.92$ | $3.98$ | $0.062$ |

**Step 2 — Without momentum.** $w \leftarrow w - 0.2w = 0.8w$: $0.8$, $0.64$, $0.512$.

**Check:** In three steps momentum reached $0.062$ and plain descent $0.512$: the built-up velocity sped descent up a lot ✓.

**Watch out:** Momentum is also prone to overshooting: a few more steps and $w$ crosses to the other side of zero and swings back. The larger $\beta$, the longer this swinging lasts.

**Answer:** $0.46$, $0.062$ and $0.512$.
