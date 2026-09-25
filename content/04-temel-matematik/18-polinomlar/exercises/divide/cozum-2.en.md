**Idea:** The divisor has the form $(x - 3)$, so $a = 3$. Work with the coefficients: bring the first one down, and at each step multiply by $3$ and add to the next.

**Step 1 — The table.**

| | $1$ | $-4$ | $2$ | $5$ |
|---|---|---|---|---|
| $a = 3$ | | $3$ | $-3$ | $-3$ |
| result | $1$ | $-1$ | $-1$ | $2$ |

**Step 2 — Read it off.** The first three numbers are the coefficients of the quotient: $x^2 - x - 1$. The last number is the remainder: $2$.

**Step 3 — Check back.** $(x - 3)(x^2 - x - 1) + 2 = x^3 - x^2 - x - 3x^2 + 3x + 3 + 2 = x^3 - 4x^2 + 2x + 5$ ✓.

**Why the same result?** Synthetic division is long division in short: instead of writing the $x$'s in each row we carry only the coefficients, and instead of subtracting with $-3$ we multiply by $+3$ and add; the two sign changes cancel.

**Answer:** $-1$, $-1$ and $2$.
