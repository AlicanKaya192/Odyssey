**Idea:** $\operatorname{Cov} = \sum p(x, y)(x - 0.5)(y - 0.4)$.

**Step 1 — $E[XY]$.** $\sum p(x, y)\,xy = 0.3 \cdot 1 = 0.3$.

**Step 2 — Covariance.** Cells: $(0, 0)$: $0.4 \cdot (-0.5)(-0.4) = 0.08$; $(0, 1)$: $0.1 \cdot (-0.5)(0.6) = -0.03$; $(1, 0)$: $0.2 \cdot (0.5)(-0.4) = -0.04$; $(1, 1)$: $0.3 \cdot (0.5)(0.6) = 0.09$. Sum $0.1$.

**Step 3 — Correlation.** $\frac{0.1}{0.5 \cdot 0.49} \approx 0.408$ ($\sigma_X = 0.5$, $\sigma_Y = \sqrt{0.24} \approx 0.49$).

**Why the same result?** Expanding the product in the definition gives $E[XY] - E[X]E[Y]$; summing cell by cell computes the same expected value without that expansion.

**Answer:** $0.3$, $0.1$ and $0.408$.
