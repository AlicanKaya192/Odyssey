**Idea:** There is a shortcut for the population variance: $\sigma^2 = \overline{x^2} - \bar{x}^2$, the mean of the squares minus the square of the mean. It works without computing deviations.

**Step 1 — The mean of the squares.** $9 + 49 + 49 + 64 + 100 = 271$; $\frac{271}{5} = 54.2$.

**Step 2 — The variance.** $54.2 - 7^2 = 54.2 - 49 = 5.2$. $\sigma \approx 2.280$.

**Step 3 — Sample.** Multiply the population variance by $\frac{n}{n - 1} = \frac{5}{4}$: $5.2 \cdot 1.25 = 6.5$.

**Why the same result?** Expanding $\frac{1}{n} \sum (x_i - \bar{x})^2$ gives $\frac{1}{n} \sum x_i^2 - 2\bar{x} \cdot \frac{1}{n} \sum x_i + \bar{x}^2 = \overline{x^2} - \bar{x}^2$. The two ways are the same algebra in a different order.

**Answer:** $5.2$, $2.280$ and $6.5$.
