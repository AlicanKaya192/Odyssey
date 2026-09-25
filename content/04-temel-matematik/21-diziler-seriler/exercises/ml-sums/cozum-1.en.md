**What is asked?** The value of a loss function, an infinite discounted reward, and a partial sum of moving-average weights.

**Idea:** All three are Σ. The first is a finite sum, the second an infinite geometric series, the third a finite geometric series.

**Step 1 — MSE.** The differences $y_i - \hat{y}_i$: $-1, 0, 2, -1$. The squares $1, 0, 4, 1$; total $6$.

$$
\text{MSE} = \frac{6}{4} = 1.5
$$

**Step 2 — Discounted reward.** $a_1 = 2$, $r = 0.8$:

$$
2 + 1.6 + 1.28 + \dots = \frac{2}{1 - 0.8} = 10
$$

**Step 3 — The weights.** $0.5$, $0.25$, $0.125$. The total is $0.875$.

**Check:** For the third with the formula: $0.5 \cdot \frac{1 - 0.5^3}{1 - 0.5} = 1 - 0.125 = 0.875$ ✓.

**Watch out:** If the differences are added without squaring, MSE gives $-1 + 0 + 2 - 1 = 0$: positive and negative errors cancel. That is why the square is there.

**Answer:** $1.5$, $10$, $0.875$.
