**What is asked?** Two probabilities and the decision boundary of a logistic model.

**Idea:** Compute $z$ and feed it to the sigmoid; the boundary is $z = 0$.

**Step 1 — $x = 2$.** $z = 3 - 4 = -1$. $p = \frac{1}{1 + e^{1}} = \frac{1}{3.718} \approx 0.269$.

**Step 2 — $x = 4$.** $z = 6 - 4 = 2$. $p = \frac{1}{1 + e^{-2}} = \frac{1}{1.135} \approx 0.881$.

**Step 3 — Boundary.** $1.5x - 4 = 0$, $x = \frac{8}{3} \approx 2.667$.

**Check:** $2 < 2.667 < 4$: the first probability is below $0.5$, the second above ✓.

**Watch out:** The sign in $e^{-z}$: for $z = -1$, $e^{-z} = e^{1}$, not $e^{-1}$.

**Answer:** $\approx 0.269$, $\approx 0.881$, $\approx 2.667$.
