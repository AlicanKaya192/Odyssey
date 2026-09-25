**What is asked?** Covariance and correlation from a joint distribution table.

**Idea:** $\operatorname{Cov} = E[XY] - E[X]E[Y]$; both variables are Bernoulli.

**Step 1 — $E[XY]$.** Only the $(1, 1)$ cell contributes: $0.3$.

**Step 2 — Covariance.** $E[X] = 0.2 + 0.3 = 0.5$, $E[Y] = 0.1 + 0.3 = 0.4$. $0.3 - 0.5 \cdot 0.4 = 0.1$.

**Step 3 — Correlation.** $\operatorname{Var}X = 0.25$, $\operatorname{Var}Y = 0.24$. $r = \frac{0.1}{\sqrt{0.06}} \approx 0.408$.

**Check:** The purchase rate is $\frac{0.3}{0.5} = 0.6$ on mobile and $\frac{0.1}{0.5} = 0.2$ on desktop; mobile and purchase go up together, so a positive covariance is consistent ✓.

**Watch out:** Taking $E[XY]$ as $E[X]E[Y] = 0.2$ assumes independence; the covariance would then always be $0$.

**Answer:** $0.3$, $0.1$, $\approx 0.408$.
