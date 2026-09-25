**Idea:** $z$ is the log-odds; the odds are $e^{z}$ and the probability is $\frac{\text{odds}}{1 + \text{odds}}$.

**Step 1 — $x = 2$.** Odds $e^{-1} \approx 0.368$; $p = \frac{0.368}{1.368} \approx 0.269$.

**Step 2 — $x = 4$.** Odds $e^{2} \approx 7.389$; $p = \frac{7.389}{8.389} \approx 0.881$.

**Step 3 — Boundary.** $p = 0.5$ means odds $1$, log-odds $0$: $x = \frac{4}{1.5} \approx 2.667$.

**Why the same result?** Dividing numerator and denominator of $\frac{e^z}{1 + e^z}$ by $e^{z}$ gives $\frac{1}{1 + e^{-z}}$; they are the same function. Looking at odds also shows that two extra hours multiply the odds by $e^{3} \approx 20$.

**Answer:** $0.269$, $0.881$ and $2.667$.
