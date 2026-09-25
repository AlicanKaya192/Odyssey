**Idea:** $\sum (x - \bar{x})(y - \bar{y}) = \sum xy - n\bar{x}\bar{y}$.

**Step 1 — Covariance.** $\sum xy = 100 + 180 + 325 + 450 + 810 = 1865$. $n\bar{x}\bar{y} = 5 \cdot 5 \cdot 68 = 1700$. The difference is $165$; $\frac{165}{4} = 41.25$.

**Step 2 — Correlation.** $\sum x^2 - n\bar{x}^2 = 155 - 125 = 30$ and $\sum y^2 - n\bar{y}^2 = 24050 - 23120 = 930$.

$$
r = \frac{165}{\sqrt{30 \cdot 930}} = \frac{165}{167.03} \approx 0.988
$$

**Step 3 — Minutes.** $\sum xy$ and $n\bar{x}\bar{y}$ are both multiplied by $60$: $2475$.

**Why the same result?** It is the sum form of the identity $E[(X - \mu_X)(Y - \mu_Y)] = E[XY] - \mu_X\mu_Y$; in $r$ the $n - 1$ cancels between numerator and denominator, so we can work with the sums directly.

**Answer:** $41.25$, $0.988$ and $2475$.
