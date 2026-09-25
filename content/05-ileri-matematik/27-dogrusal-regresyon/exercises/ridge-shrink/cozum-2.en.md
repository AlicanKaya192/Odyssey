**Idea:** Set the derivative of the loss with respect to $w$ to zero.

**Step 1 — Derivative.** $\frac{d}{dw}\left[\sum(y - wx)^2 + \lambda w^2\right] = -2\sum xy + 2w\sum x^2 + 2\lambda w$. With $\lambda = 0$, zero at $w = \frac{20}{10} = 2$.

**Step 2 — $\lambda = 10$.** $-40 + 20w + 20w = 0$, $w = 1$.

**Step 3 — Target.** For $w = 1.6$: $2w\sum x^2 = 32$ and $2\lambda w = 3.2\lambda$; $-40 + 32 + 3.2\lambda = 0$, $\lambda = 2.5$.

**Why the same result?** The derivative equation is $w(\sum x^2 + \lambda) = \sum xy$; the formula is its solution. The penalty increases the curvature of the loss and pulls the minimum towards zero.

**Answer:** $2$, $1$ and $2.5$.
