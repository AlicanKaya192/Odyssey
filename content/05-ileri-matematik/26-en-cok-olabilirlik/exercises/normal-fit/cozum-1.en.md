**What is asked?** The MLEs of the two parameters of a normal distribution and the difference from the unbiased variance.

**Idea:** $\hat{\mu} = \bar{x}$, $\hat{\sigma}^2 = \frac{1}{n}\sum(x_i - \bar{x})^2$.

**Step 1 — Mean.** $\frac{60}{5} = 12$.

**Step 2 — MLE variance.** The deviations are $0, 3, -3, 2, -2$; the sum of squares $0 + 9 + 9 + 4 + 4 = 26$. $\frac{26}{5} = 5.2$.

**Step 3 — Unbiased.** $\frac{26}{4} = 6.5$.

**Check:** The deviations sum to $0$ ✓; the MLE variance is always smaller than the unbiased one, by the ratio $\frac{n - 1}{n} = 0.8$ ✓.

**Watch out:** With five observations the difference is $20$ percent; in a small sample it matters which divisor is used.

**Answer:** $12$, $5.2$, $6.5$.
