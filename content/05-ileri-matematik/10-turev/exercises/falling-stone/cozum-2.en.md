**Idea:** See the limit with numbers before calculating it: compute the average speed on $[3, 3 + h]$ for shrinking $h$ and watch where the numbers go.

**Step 1 — The average.** As in the first solution, $20$.

**Step 2 — A table.**

| $h$ | $s(3 + h)$ | average speed |
|---|---|---|
| $1$ | $80$ | $35$ |
| $0.1$ | $48.05$ | $30.5$ |
| $0.01$ | $45.3005$ | $30.05$ |

**Step 3 — From the left.** $h = -0.01$: $s(2.99) = 44.7005$, average $\frac{44.7005 - 45}{-0.01} = 29.95$. From both sides, $30$.

**Why the same result?** Each row of the table is a value of the formula $30 + 5h$; the limit is the table's "infinitely small $h$" row. The numbers show the direction, the limit gives the exact value.

**Answer:** $20$ and $30$.
