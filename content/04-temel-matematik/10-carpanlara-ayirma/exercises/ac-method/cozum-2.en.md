**Idea:** Expanding $(ax + b)(cx + d)$ we need $ac = 6$, $bd = -2$ and the middle coefficient $ad + bc = 1$. There are few options for $ac$ and $bd$; let us try the middle coefficient for each.

**Step 1 — Options.** $0 < a < c$ and $ac = 6$: $(a, c) = (1, 6)$ or $(2, 3)$. $bd = -2$: $(b, d) \in \{(1, -2), (-1, 2), (2, -1), (-2, 1)\}$.

**Step 2 — The middle coefficient $ad + bc$.**

| $(a, c)$ | $(b, d)$ | $ad + bc$ |
|---|---|---|
| $(2, 3)$ | $(1, -2)$ | $-4 + 3 = -1$ |
| $(2, 3)$ | $(-1, 2)$ | $4 - 3 = 1$ ✓ |
| $(2, 3)$ | $(2, -1)$ | $-2 + 6 = 4$ |
| $(1, 6)$ | $(-1, 2)$ | $2 - 6 = -4$ |

**Step 3 — The result.** $a = 2$, $b = -1$, $c = 3$, $d = 2$: $(2x - 1)(3x + 2)$.

**Why the same result?** The two numbers of the $ac$ method ($4$ and $-3$) are exactly the products $ad$ and $bc$ in this table: $2 \cdot 2 = 4$, $(-1) \cdot 3 = -3$. The trial table does the same search by brute force; it works when there are few options.

**Answer:** $2$, $-1$, $3$, $2$.
