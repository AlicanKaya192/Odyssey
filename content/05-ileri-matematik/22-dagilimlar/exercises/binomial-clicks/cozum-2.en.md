**Idea:** $X = X_1 + \dots + X_8$; each $X_i$ is a Bernoulli($0.25$). The expected value by linearity, the probabilities by counting and independence.

**Step 1 — Exactly $2$.** The two who click can be chosen in $\binom{8}{2} = 28$ ways; each choice has probability $0.25^2 \cdot 0.75^6$ (independence). The product is $\approx 0.3115$.

**Step 2 — The expected value.** $E[X] = \sum E[X_i] = 8 \cdot 0.25 = 2$; without knowing the distribution.

**Step 3 — At least one.** Nobody clicking is $8$ independent "no"s: $0.75^8$. The complement is $0.8999$.

**Why the same result?** The binomial formula is these three steps in short: $\binom{n}{k}$ is the choice, $p^k(1 - p)^{n - k}$ independence, $np$ linearity.

**Answer:** $0.3115$, $2$ and $0.8999$.
