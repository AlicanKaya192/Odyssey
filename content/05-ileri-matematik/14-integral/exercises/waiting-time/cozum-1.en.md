**What is asked?** The total area of a probability density, the probability of an interval and the median.

**Idea:** Every probability is an area under the density; the antiderivative is $-e^{-2x}$.

**Step 1 — The total.** $\int_0^{t} 2e^{-2x} \, dx = 1 - e^{-2t}$; as $t \to \infty$, $e^{-2t} \to 0$: the total is $1$ ✓.

**Step 2 — $P(X \le 1)$.** $1 - e^{-2} \approx 1 - 0.1353 = 0.8647$.

**Step 3 — The median.** $1 - e^{-2m} = \frac{1}{2} \Rightarrow e^{-2m} = \frac{1}{2} \Rightarrow m = \frac{\ln 2}{2} \approx 0.347$.

**Check:** The mean wait is $E[X] = \frac{1}{2}$ minute; the median ($0.347$) is below the mean because the distribution is skewed to the right: many short waits and a few long ones ✓.

**Watch out:** $f(1) = 2e^{-2} \approx 0.27$ is not a probability; it is the value of the density. Probability is area.

**Answer:** $1$, $0.865$ and $0.347$.
