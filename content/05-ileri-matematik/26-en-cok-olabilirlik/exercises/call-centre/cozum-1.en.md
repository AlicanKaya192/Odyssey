**What is asked?** The MLE of a Poisson parameter, a probability computed with it, and the slope at another point.

**Idea:** $\ell'(\lambda) = \frac{\sum x_i}{\lambda} - n$.

**Step 1 — MLE.** $\sum x_i = 24$, $n = 6$. $\frac{24}{\lambda} = 6$, $\hat{\lambda} = 4$.

**Step 2 — No calls.** $P(X = 0) = \frac{4^0 e^{-4}}{0!} = e^{-4} \approx 0.0183$.

**Step 3 — $\ell'(5)$.** $\frac{24}{5} - 6 = -1.2$. Negative: $5$ is too large; the maximum is to the left.

**Check:** $\ell''(\lambda) = -\frac{24}{\lambda^2} < 0$; $\hat{\lambda} = 4$ really is the maximum ✓.

**Watch out:** The $\ln x_i!$ terms in the log-likelihood do not depend on $\lambda$; they vanish in the derivative.

**Answer:** $4$, $\approx 0.0183$, $-1.2$.
