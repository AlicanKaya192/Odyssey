**Idea:** The best point is $w^* = 4$. Let the distance be $d = w - 4$; one step multiplies $d$ by a fixed number.

**Step 1 — The factor.** $w - 0.25 \cdot 2(w - 4) - 4 = (w - 4)(1 - 0.5)$: $d \leftarrow 0.5 \, d$.

**Step 2 — The distances.** $d_0 = -4$, $d_1 = -2$, $d_2 = -1$, $d_3 = -0.5$.

**Step 3 — Convert back.** $w = 4 + d$: $2$, $3$, $3.5$.

**Why the same result?** On a quadratic loss, gradient descent multiplies the distance by $1 - \eta\lambda$ at each step; here $\lambda = L'' = 2$ and $1 - 0.5 = 0.5$. This view gives where you will be after any number of steps in one formula: $w_k = 4 - 4 \cdot 0.5^k$.

**Answer:** $2$, $3$, $3.5$.
