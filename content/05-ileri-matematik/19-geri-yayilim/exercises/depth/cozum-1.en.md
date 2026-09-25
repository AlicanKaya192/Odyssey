**What is asked?** How fast derivatives multiplied across layers vanish or explode.

**Idea:** After $n$ layers the product is the $n$-th power of the factor.

**Step 1 — Five layers.** $0.25^5 = \frac{1}{4^5} = \frac{1}{1024} \approx 0.000977$.

**Step 2 — The threshold.** $4^4 = 256 < 1000$, $4^5 = 1024 > 1000$: $n = 5$ is the first to fall below $0.001$.

**Step 3 — Explosion.** $1.1^{50} = e^{50 \cdot 0.09531} = e^{4.7655} \approx 117.4$.

**Check:** $1.1^{10} \approx 2.594$; $2.594^5 \approx 117.4$ ✓.

**Watch out:** Even tiny departures of the factor from $1$ compound with depth; $0.9^{50} \approx 0.005$, $1.1^{50} \approx 117$. That is why good initialisation methods try to keep the factor right around $1$.

**Answer:** $\frac{1}{1024}$, $5$ and $\approx 117.4$.
