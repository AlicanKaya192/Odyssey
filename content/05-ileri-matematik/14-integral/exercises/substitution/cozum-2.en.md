**Idea:** Solve the first integral by expanding it as a polynomial; solve the second by guessing the antiderivative and confirming by differentiation.

**Step 1 — Expand.** $(x^2 + 1)^3 = x^6 + 3x^4 + 3x^2 + 1$; times $2x$: $2x^7 + 6x^5 + 6x^3 + 2x$.

**Step 2 — Integrate.**

$$
\left[\frac{x^8}{4} + x^6 + \frac{3x^4}{2} + x^2\right]_0^1 = \frac{1}{4} + 1 + \frac{3}{2} + 1 = \frac{15}{4}
$$

**Step 3 — Guess.** $(e^{2x})' = 2e^{2x}$; half of it will do: $F = \frac{e^{2x}}{2}$. $F(\ln 2) - F(0) = \frac{4}{2} - \frac{1}{2} = \frac{3}{2}$.

**Why the same result?** Expanding $\frac{(x^2 + 1)^4}{4}$ gives $\frac{x^8}{4} + x^6 + \frac{3x^4}{2} + x^2 + \frac{1}{4}$: the same antiderivative, differing only by a constant ($\frac{1}{4}$) that cancels in the definite integral. Substitution is the shortcut that skips the long expansion.

**Answer:** $\frac{15}{4}$ and $\frac{3}{2}$.
