**What is asked?** A given number of successes in independent trials, the expected successes, and at least one success.

**Idea:** $8$ independent yes–no trials: $X \sim$ Binomial$(8, 0.25)$.

**Step 1 — Exactly $2$.** $\binom{8}{2} = 28$; $0.25^2 = 0.0625$; $0.75^6 \approx 0.17798$.

$$
P(X = 2) = 28 \cdot 0.0625 \cdot 0.17798 \approx 0.3115
$$

**Step 2 — The expected value.** $np = 8 \cdot 0.25 = 2$.

**Step 3 — At least one.** $P(X = 0) = 0.75^8 \approx 0.1001$; $1 - 0.1001 = 0.8999$.

**Check:** The most likely value should be near the expected value: $P(X = 1) = 8 \cdot 0.25 \cdot 0.75^7 \approx 0.267$, $P(X = 2) \approx 0.311$, $P(X = 3) \approx 0.208$; the peak is at $2$ ✓.

**Watch out:** Forgetting $\binom{8}{2}$ counts only the ordering "the first two clicked, the rest did not" ($0.0111$).

**Answer:** $\approx 0.3115$, $2$, $\approx 0.8999$.
