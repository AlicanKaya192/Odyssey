**What is asked?** The parameter of an exponential distribution and two quantities computed from it.

**Idea:** $\ell'(\lambda) = \frac{n}{\lambda} - \sum t_i = 0$.

**Step 1 — MLE.** $\sum t_i = 12$, $n = 5$. $\hat{\lambda} = \frac{5}{12} \approx 0.417$.

**Step 2 — $P(T > 3)$.** $e^{-3 \cdot 5/12} = e^{-1.25} \approx 0.287$.

**Step 3 — Median.** $m = \frac{\ln 2}{\hat{\lambda}} = 0.6931 \cdot 2.4 \approx 1.66$ years.

**Check:** The mean lifetime is $\frac{1}{\hat{\lambda}} = 2.4$; the exponential is right-skewed, so the median is below the mean ✓.

**Watch out:** Confusing $\hat{\lambda}$ with $\bar{t} = 2.4$; $\lambda$ is a rate ($0.417$ failures per year), the mean lifetime is its reciprocal.

**Answer:** $\approx 0.417$, $\approx 0.287$, $\approx 1.66$.
