**Idea:** Without using the quotient rule at all: write $f(x) = x \cdot (x^2 + 1)^{-1}$; the product rule, with the chain rule in the second factor.

**Step 1 — The derivative of the second factor.** $\big((x^2 + 1)^{-1}\big)' = -(x^2 + 1)^{-2} \cdot 2x$.

**Step 2 — The product rule.**

$$
\begin{aligned}
f'(x) &= 1 \cdot (x^2 + 1)^{-1} + x \cdot \big(-2x (x^2 + 1)^{-2}\big) \\
&= \frac{(x^2 + 1) - 2x^2}{(x^2 + 1)^2} = \frac{1 - x^2}{(x^2 + 1)^2}
\end{aligned}
$$

**Step 3 — The values.** $f'(2) = -\frac{3}{25}$; the top $1 - x^2 = 0$ gives $x = 1$.

**Why the same result?** The quotient rule is itself derived from these two rules; bringing to a common denominator gives the same fraction. If you forget the rule, this road is always open.

**Answer:** $-\frac{3}{25}$ and $1$.
