**Idea:** The mean of an exponential distribution is $\frac{1}{\lambda}$. The MLE of the mean is $\bar{t}$; by invariance everything can be written in terms of $\bar{t}$.

**Step 1 — MLE.** $\bar{t} = 2.4$; $\hat{\lambda} = \frac{1}{2.4} \approx 0.417$.

**Step 2 — $P(T > 3)$.** $e^{-3/\bar{t}} = e^{-3/2.4} = e^{-1.25} \approx 0.287$.

**Step 3 — Median.** $m = \bar{t}\ln 2 = 2.4 \cdot 0.6931 \approx 1.66$.

**Why the same result?** $\frac{n}{\sum t_i} = \frac{1}{\bar{t}}$; the solution of the derivative equation and "the reciprocal of the mean" are the same expression.

**Answer:** $0.417$, $0.287$ and $1.66$.
