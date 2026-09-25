**What is asked?** The total probability of a positive result, the probability of illness after a positive, and the update after a second positive.

**Idea:** $P(+)$ by total probability, the posterior by Bayes' rule; for the second test the posterior is the new prior.

**Step 1 — $P(+)$.** $0.98 \cdot 0.005 = 0.0049$ and $0.03 \cdot 0.995 = 0.02985$. Total $0.03475$.

**Step 2 — The posterior.** $\frac{0.0049}{0.03475} \approx 0.141$.

**Step 3 — The second test.** Prior $p = 0.141$:

$$
\begin{aligned}
&\frac{0.98 \cdot 0.141}{0.98 \cdot 0.141 + 0.03 \cdot 0.859} \\
&= \frac{0.1382}{0.1382 + 0.0258} \approx 0.843
\end{aligned}
$$

**Check:** The posterior is larger than the prior ($0.005$) ✓, but after one test it stays at $14$ percent: the disease is rare.

**Watch out:** Taking the prior as $0.005$ again for the second test throws away the information from the first test.

**Answer:** $0.03475$, $\approx 0.141$, $\approx 0.843$.
