**Idea:** Entropy is an expected value: $H = E[I(X)]$. First find each outcome's information, then average with the probabilities.

**Step 1 — Tails.** $I = 3.322$ bits (a $\frac{1}{10}$ event; at $\frac{1}{8}$ it would be exactly $3$ bits).

**Step 2 — Heads.** $I = 0.152$ bits.

**Step 3 — Expected value.** $E[I] = 0.9 \cdot 0.152 + 0.1 \cdot 3.322 \approx 0.469$.

**Why the same result?** $-\sum p\log_2 p = \sum p \cdot (-\log_2 p) = \sum p \cdot I$; the entropy formula is exactly the expected value of the information. The rare outcome's large information is multiplied by its small probability, so it affects the entropy only a little.

**Answer:** $0.469$, $3.322$ and $0.152$.
