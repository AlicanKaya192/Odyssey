**What is asked?** The effect of a coefficient on the odds, a probability, and the value needed to pass a threshold.

**Idea:** Odds $= e^{\text{log-odds}}$; $p = \frac{\text{odds}}{1 + \text{odds}}$.

**Step 1 — Factor.** $e^{0.7} \approx 2.014$: each visit roughly doubles the odds.

**Step 2 — $x = 0$.** Odds $e^{-2} \approx 0.1353$; $p = \frac{0.1353}{1.1353} \approx 0.119$.

**Step 3 — Threshold.** $-2 + 0.7x \geq 0$, $x \geq 2.857$; as a whole number, $3$.

**Check:** $x = 3$: log-odds $0.1$, $p \approx 0.525 \geq 0.5$ ✓; $x = 2$: log-odds $-0.6$, $p \approx 0.354$ ✗.

**Watch out:** The coefficient is not added to the probability: starting at $0.119$ and adding $0.7$ per visit gives nonsense.

**Answer:** $\approx 2.014$, $\approx 0.119$, $3$.
