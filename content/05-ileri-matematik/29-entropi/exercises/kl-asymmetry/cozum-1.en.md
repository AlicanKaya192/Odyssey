**What is asked?** The KL divergence in both directions, and the cross-entropy.

**Idea:** $D_{\mathrm{KL}}(A \parallel B) = \sum a\log_2\frac{a}{b}$; the weights come from the first distribution.

**Step 1 — $P \parallel Q$.** $0.9 \cdot 0.848 + 0.1 \cdot (-2.322) \approx 0.763 - 0.232 = 0.531$.

**Step 2 — $Q \parallel P$.** $0.5 \cdot (-0.848) + 0.5 \cdot 2.322 \approx -0.424 + 1.161 = 0.737$.

**Step 3 — $H(P, Q)$.** $-0.9\log_2 0.5 - 0.1\log_2 0.5 = 1$.

**Check:** $H(P) \approx 0.469$ and $H(P, Q) - H(P) = 1 - 0.469 = 0.531$ ✓.

**Watch out:** The two KLs differ: $Q \parallel P$ is larger because $P$ gives only $0.1$ to the second outcome, which $Q$ gives half the time; that term dominates.

**Answer:** $\approx 0.531$, $\approx 0.737$, $1$.
