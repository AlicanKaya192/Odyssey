**Idea:** Turn powers into sums with logarithms: $\ln(c^n) = n \ln c$.

**Step 1 — Five layers.** $5 \ln 0.25 = 5 \cdot (-1.3863) = -6.931$; $e^{-6.931} \approx 0.000977 = \frac{1}{1024}$.

**Step 2 — The threshold.** $n \ln 0.25 < \ln 0.001$: $n > \frac{-6.908}{-1.386} \approx 4.98$. The smallest integer is $5$.

**Step 3 — Explosion.** $50 \cdot 0.09531 = 4.7655$; $e^{4.7655} \approx 117.4$.

**Why the same result?** The same powers, on a logarithmic scale. This view shows one more thing: the log-gradient changes **linearly** with the number of layers, by $\ln c$ per layer. A factor $c = 1$, that is $\ln c = 0$, means a gradient that does not depend on depth.

**Answer:** $\frac{1}{1024}$, $5$, $117.4$.
