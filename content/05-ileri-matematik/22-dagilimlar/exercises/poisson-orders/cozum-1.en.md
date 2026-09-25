**What is asked?** Three probabilities about the number of events arriving at a constant rate.

**Idea:** Independent events at a constant average rate: Poisson$(\lambda = 4)$.

**Step 1 — None.** $e^{-4} \approx 0.0183$.

**Step 2 — Exactly $4$.**

$$
\frac{e^{-4} \, 4^4}{4!} = \frac{256}{24} e^{-4} \approx 10.667 \cdot 0.0183 \approx 0.1954
$$

**Step 3 — At least $2$.** $P(1) = 4e^{-4} \approx 0.0733$. $1 - 0.0183 - 0.0733 = 1 - 5e^{-4} \approx 0.9084$.

**Check:** For a Poisson with mean $4$, $P(3) = P(4) \approx 0.195$; two neighbouring values come out equal when $\lambda$ is a whole number ✓.

**Watch out:** Subtracting only $P(0)$ for "at least $2$" gives "at least $1$".

**Answer:** $\approx 0.0183$, $\approx 0.1954$, $\approx 0.9084$.
