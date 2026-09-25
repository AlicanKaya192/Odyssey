**What is asked?** The probability a Bernoulli model gives to the observed labels, and the expected value and variance of the number of positives.

**Idea:** Each label is Bernoulli($p_i$); independence multiplies the probabilities and adds the expected values and variances.

**Step 1 — Likelihood.** $0.8 \cdot (1 - 0.6) \cdot 0.9 = 0.8 \cdot 0.4 \cdot 0.9 = 0.288$.

**Step 2 — Expected value.** $0.8 + 0.6 + 0.9 = 2.3$.

**Step 3 — Variance.** $0.8 \cdot 0.2 + 0.6 \cdot 0.4 + 0.9 \cdot 0.1 = 0.16 + 0.24 + 0.09 = 0.49$.

**Check:** The most uncertain example ($p = 0.6$) contributes most to the variance ($0.24$) ✓.

**Watch out:** Multiplying by $p_2$ for the example whose label is $0$; for that example the model gives "negative" probability $0.4$.

**Answer:** $0.288$, $2.3$, $0.49$.
