**Idea:** In a Poisson the expected value is $\lambda$; the MLE is the sample mean. The MLE of a probability is found by plugging in the parameter's MLE.

**Step 1 — MLE.** $\bar{x} = \frac{24}{6} = 4$.

**Step 2 — Probability.** $P(X = 0) = e^{-\lambda}$ is a $g(\lambda)$; by invariance its MLE is $e^{-\hat{\lambda}} = e^{-4} \approx 0.0183$.

**Step 3 — Slope.** $\ell'(\lambda) = n\left(\frac{\bar{x}}{\lambda} - 1\right) = 6\left(\frac{4}{5} - 1\right) = -1.2$.

**Why the same result?** $\frac{\sum x_i}{\lambda} - n = n\left(\frac{\bar{x}}{\lambda} - 1\right)$; the derivative depends only on $\bar{x}$, so the estimate comes out as $\bar{x}$.

**Answer:** $4$, $0.0183$ and $-1.2$.
