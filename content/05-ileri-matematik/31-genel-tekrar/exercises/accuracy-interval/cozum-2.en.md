**Idea:** The number correct is Binomial$(400, 0.85)$: mean $340$, standard deviation $\sqrt{400 \cdot 0.85 \cdot 0.15} = \sqrt{51} \approx 7.14$.

**Step 1 — SE.** The proportion is the count over $400$: $\frac{7.14}{400} \approx 0.0179$.

**Step 2 — Lower bound.** As a count, $340 - 1.96 \cdot 7.14 \approx 326$; as a proportion $\frac{326}{400} \approx 0.815$.

**Step 3 — Upper bound.** $340 + 14 = 354$; $\frac{354}{400} = 0.885$.

**Why the same result?** Proportion and count differ by a fixed factor of $400$; the mean, standard deviation and bounds all scale by it.

**Answer:** $0.0179$, $0.815$ and $0.885$.
