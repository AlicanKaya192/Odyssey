**Idea:** Do synthetic division by $(x - 2)$ while $k$ is still unknown; the last number is the remainder and must be $0$. The same table also gives the quotient.

**Step 1 — The table with $k$.** Coefficients $1, k, -4, -12$, $a = 2$:

| | $1$ | $k$ | $-4$ | $-12$ |
|---|---|---|---|---|
| $a = 2$ | | $2$ | $2k + 4$ | $4k$ |
| result | $1$ | $k + 2$ | $2k$ | $4k - 12$ |

The remainder $4k - 12 = 0$, so $k = 3$.

**Step 2 — The quotient.** With $k = 3$ the last row is $1, 5, 6$: the quotient is $x^2 + 5x + 6 = (x + 2)(x + 3)$. The roots are $2$, $-2$, $-3$.

**Step 3 — The remainder.** A new table with $a = -1$ ($1, 3, -4, -12$): $1$; $3 - 1 = 2$; $-4 - 2 = -6$; $-12 + 6 = -6$. The remainder is $-6$.

**Why the same result?** The last number of the table is always $P(a)$; the expression $4k - 12$ is exactly the $P(2) = 4k - 12$ of the first solution. Instead of grouping, the quotient came ready from the table.

**Answer:** $3$, $-3$ and $-6$.
