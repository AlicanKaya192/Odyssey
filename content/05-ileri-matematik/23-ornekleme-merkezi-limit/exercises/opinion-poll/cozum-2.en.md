**Idea:** The number of "yes" answers among $400$ is Binomial$(400, 0.55)$: mean $220$, standard deviation $\sqrt{400 \cdot 0.55 \cdot 0.45} = \sqrt{99} \approx 9.95$.

**Step 1 — SE.** The proportion is the count over $400$: $\frac{9.95}{400} \approx 0.0249$.

**Step 2 — $0.60$.** $0.60 \cdot 400 = 240$ "yes"; $z = \frac{240 - 220}{9.95} \approx 2.01$: $0.022$.

**Step 3 — $n$.** The standard error of the proportion is $\sqrt{\frac{0.2475}{n}}$; for $0.015$, $n = 1100$.

**Why the same result?** The proportion is the binomial count divided by $n$; the mean, standard deviation and threshold are all divided by the same amount, so $z$ stays the same.

**Answer:** $0.0249$, $0.022$ and $1100$.
