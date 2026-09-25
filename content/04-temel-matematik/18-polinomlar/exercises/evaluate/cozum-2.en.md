**Idea:** By the remainder theorem, $P(a)$ is the remainder on division by $(x - a)$. Synthetic division gives this remainder without any powers, using only multiplication and addition.

**Step 1 — $a = 2$.** The coefficients are $2, -1, 4, -7$.

| | $2$ | $-1$ | $4$ | $-7$ |
|---|---|---|---|---|
| $a = 2$ | | $4$ | $6$ | $20$ |
| result | $2$ | $3$ | $10$ | $13$ |

**Step 2 — $a = -1$.**

| | $2$ | $-1$ | $4$ | $-7$ |
|---|---|---|---|---|
| $a = -1$ | | $-2$ | $3$ | $-7$ |
| result | $2$ | $-3$ | $7$ | $-14$ |

**Step 3 — $a = 1$.** Multiplying by $1$ at each step just adds the numbers as they are: $2$, $1$, $5$, $-2$. The last number is the sum of the coefficients.

**Why the same result?** Synthetic division is the step-by-step calculation of $P(x) = ((2x - 1)x + 4)x - 7$; opening the brackets gives the polynomial itself. So the last number is exactly $P(a)$.

**Answer:** $13$, $-14$ and $-2$.
