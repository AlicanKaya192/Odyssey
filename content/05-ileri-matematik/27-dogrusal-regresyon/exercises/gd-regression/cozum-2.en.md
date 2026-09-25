**Idea:** Since $J'(w) = 28(w - w^*)$, the update becomes $w_{t+1} - w^* = (1 - 28\eta)(w_t - w^*)$: the error shrinks by a fixed factor at each step.

**Step 1 — $w^*$ and the gradient.** $w^* = \frac{22}{14} \approx 1.571$; $J'(0) = 28(0 - 1.571) = -44$.

**Step 2 — One step.** The factor is $1 - 0.28 = 0.72$. $w_1 - w^* = 0.72 \cdot (-1.571)$, so $w_1 = 0.28 \cdot 1.571 = 0.44$.

**Step 3 — Outcome.** The error is multiplied by $0.72$ at each step; $w_t \to w^* \approx 1.571$.

**Why the same result?** For a quadratic loss the gradient is proportional to the distance from the minimum; so gradient descent heads geometrically fast to the same solution, that of the normal equations. With $\eta > \frac{2}{28}$ the factor's absolute value would exceed $1$ and the steps would diverge.

**Answer:** $-44$, $0.44$ and $1.571$.
