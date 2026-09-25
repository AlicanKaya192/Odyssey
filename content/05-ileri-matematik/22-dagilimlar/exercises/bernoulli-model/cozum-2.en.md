**Idea:** Turn the likelihood into a sum with logarithms; the loss of logistic regression is exactly the negative of this.

**Step 1 — Log-likelihood.** $\ln 0.8 + \ln 0.4 + \ln 0.9 \approx -0.2231 - 0.9163 - 0.1054 = -1.2448$. $e^{-1.2448} \approx 0.288$.

**Step 2 — Expected value.** Linearity: $\sum p_i = 2.3$.

**Step 3 — Variance.** $\sum p_i(1 - p_i) = 0.49$.

**Why the same result?** The logarithm of a product is the sum of the logarithms; the log loss ($1.2448 / 3 \approx 0.415$ per example) is the average of the negative of this sum. The Maximum Likelihood section generalises this link.

**Answer:** $0.288$, $2.3$ and $0.49$.
