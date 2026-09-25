**What is asked?** How a penalty term changes the best weight and the curvature of the loss.

**Idea:** The loss is a convex function of $w$; the point where the derivative is zero is the global minimum.

**Step 1 — The sums.** $\sum x_i^2 = 1 + 4 = 5$, $\sum x_i y_i = 2 + 6 = 8$.

**Step 2 — The derivative.** $L'(w) = -2 \cdot 8 + 2 \cdot 5 w + 2\lambda w = 0$: $w = \frac{8}{5 + \lambda}$.

**Step 3 — The values.** $\lambda = 0$: $w = \frac{8}{5} = 1.6$. $\lambda = 1$: $w = \frac{8}{6} = \frac{4}{3} \approx 1.333$.

**Step 4 — The curvature.** $L''(w) = 2(5 + \lambda) = 12$.

**Check:** The penalty pulled the weight towards zero ($1.6 \to 1.33$); that is ridge's job. $L'' > 0$: strictly convex ✓.

**Watch out:** Forgetting $2\lambda w$ in the derivative gives $1.6$, as if $\lambda$ had no effect.

**Answer:** $\frac{8}{5}$, $\frac{4}{3}$ and $12$.
