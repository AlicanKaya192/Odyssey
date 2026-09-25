**Idea:** In a Poisson the ratio of successive probabilities is simple: $\frac{P(k)}{P(k - 1)} = \frac{\lambda}{k}$. Start from $P(0)$ and multiply your way forward.

**Step 1 — $P(0)$.** $e^{-4} \approx 0.01832$.

**Step 2 — Walk.** $P(1) = P(0) \cdot 4 = 0.07326$; $P(2) = P(1) \cdot 2 = 0.14653$; $P(3) = P(2) \cdot \frac{4}{3} = 0.19537$; $P(4) = P(3) \cdot 1 = 0.19537$.

**Step 3 — At least $2$.** $1 - 0.01832 - 0.07326 = 0.90842$.

**Why the same result?** $\frac{\lambda^k / k!}{\lambda^{k-1} / (k-1)!} = \frac{\lambda}{k}$; the formula is these factors built up. At $k = \lambda$ the ratio is $1$, which is why $P(3) = P(4)$.

**Answer:** $0.0183$, $0.1954$ and $0.9084$.
