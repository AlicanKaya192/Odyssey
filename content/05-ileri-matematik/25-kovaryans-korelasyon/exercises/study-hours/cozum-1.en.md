**What is asked?** Covariance, correlation and the effect of a unit change for a small data set.

**Idea:** The average (with $n - 1$) of the products of deviations from the means.

**Step 1 — Covariance.** $\bar{x} = 5$, $\bar{y} = 68$. Deviations: for $x$, $-3, -2, 0, 1, 4$; for $y$, $-18, -8, -3, 7, 22$. Products $54, 16, 0, 7, 88$; sum $165$. $s_{xy} = \frac{165}{4} = 41.25$.

**Step 2 — Correlation.** $s_x^2 = \frac{9 + 4 + 0 + 1 + 16}{4} = 7.5$, $s_y^2 = \frac{324 + 64 + 9 + 49 + 484}{4} = 232.5$.

$$
r = \frac{41.25}{\sqrt{7.5 \cdot 232.5}} = \frac{41.25}{41.76} \approx 0.988
$$

**Step 3 — Minutes.** Multiplying $x$ by $60$ multiplies the covariance by $60$: $41.25 \cdot 60 = 2475$. $r$ does not change.

**Check:** All products are zero or positive; the points lie very close to an increasing line, so $r$ close to $1$ is consistent ✓.

**Watch out:** Dividing by $n$ gives $33$; in a sample $n - 1$ is used. $r$ comes out the same either way, because the divisor cancels.

**Answer:** $41.25$, $\approx 0.988$, $2475$.
