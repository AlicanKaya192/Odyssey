**Idea:** The number of false alarms $X$ is a binomial variable with $n = 20$ and $p = 0.05$.

**Step 1 — Expected value.** $E[X] = np = 1$.

**Step 2 — At least one.** $P(X \geq 1) = 1 - P(X = 0) = 1 - \binom{20}{0} 0.05^0 \, 0.95^{20} \approx 0.642$.

**Step 3 — Threshold.** To keep the overall false alarm probability at most $0.05$, $P(X \geq 1) \leq 20 \alpha' \leq 0.05$ is enough; $\alpha' = 0.0025$.

**Why the same result?** The binomial term $P(X = 0)$ is the probability of "no test gives a false alarm"; the product in the first way is the same number.

**Answer:** $1$, $0.642$ and $0.0025$.
