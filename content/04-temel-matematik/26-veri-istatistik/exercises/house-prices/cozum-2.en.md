**Idea:** The mean is the number that makes the deviations add up to zero. How far the outlier pulls the mean can be computed this way too.

**Step 1 — Mean without the outlier.** Six houses between $1.2$ and $2.1$ add up to $10.2$: mean $1.7$.

**Step 2 — The seventh house.** $9.8$ is $8.1$ above this mean. Shared among seven houses it raises the mean by $\frac{8.1}{7} \approx 1.157$: $1.7 + 1.157 \approx 2.857$.

**Step 3 — The median.** The outlier does not change the order; the middle of seven values is still the fourth, $1.8$.

**Why the same result?** When a new value is added, the mean shifts by $\frac{1}{n}$ of that value's distance from the old mean. This is the calculation $\frac{10.2 + 9.8}{7}$ split into parts.

**Answer:** $2.857$, $1.8$ and $1.7$.
