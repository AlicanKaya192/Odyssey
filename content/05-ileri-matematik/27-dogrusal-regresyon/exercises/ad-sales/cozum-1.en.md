**What is asked?** The single-feature least squares line and a prediction.

**Idea:** $w = \frac{S_{xy}}{S_{xx}}$, $b = \bar{y} - w\bar{x}$.

**Step 1 — Slope.** Deviations: for $x$, $-2, -1, 0, 1, 2$; for $y$, $-2, 0, -1, 2, 1$. $S_{xy} = 4 + 0 + 0 + 2 + 2 = 8$, $S_{xx} = 10$. $w = 0.8$.

**Step 2 — Intercept.** $5 - 0.8 \cdot 3 = 2.6$.

**Step 3 — Prediction.** $2.6 + 0.8 \cdot 6 = 7.4$.

**Check:** The residuals are $-0.4$, $0.8$, $-1$, $1.2$, $-0.6$; they sum to $0$ ✓.

**Watch out:** $x = 6$ is just outside the range of the data; the prediction is an extrapolation and should be used with care.

**Answer:** $0.8$, $2.6$, $7.4$.
