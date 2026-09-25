**Idea:** $D_{\mathrm{KL}}(A \parallel B) = H(A, B) - H(A)$. Compute the cross-entropy and entropy separately for each direction.

**Step 1 — $P \parallel Q$.** $H(P, Q) = 1$ (every $q = 0.5$), $H(P) \approx 0.469$. Difference $0.531$.

**Step 2 — $Q \parallel P$.** $H(Q, P) = -0.5\log_2 0.9 - 0.5\log_2 0.1 \approx 0.076 + 1.661 = 1.737$; $H(Q) = 1$. Difference $0.737$.

**Step 3 — $H(P, Q)$.** $1$.

**Why the same result?** $\sum a\log\frac{a}{b} = \sum a\log a - \sum a\log b = -H(A) + H(A, B)$. The asymmetry shows here too: in the two directions both the cross-entropies and the entropies subtracted differ.

**Answer:** $0.531$, $0.737$ and $1$.
