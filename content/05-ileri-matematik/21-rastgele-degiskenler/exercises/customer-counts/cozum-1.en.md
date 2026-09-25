**What is asked?** A missing probability, the expected value and the variance.

**Idea:** The distribution adds up to $1$; the expected value is a weighted average; the variance is the mean of the squares minus the square of the mean.

**Step 1 — $c$.** $0.1 + 0.3 + c + 0.2 = 1$, $c = 0.4$.

**Step 2 — $E[X]$.** $0 \cdot 0.1 + 1 \cdot 0.3 + 2 \cdot 0.4 + 3 \cdot 0.2 = 0.3 + 0.8 + 0.6 = 1.7$.

**Step 3 — The variance.** $E[X^2] = 0.3 + 4 \cdot 0.4 + 9 \cdot 0.2 = 0.3 + 1.6 + 1.8 = 3.7$. $\operatorname{Var}(X) = 3.7 - 1.7^2 = 3.7 - 2.89 = 0.81$.

**Check:** With deviations: $(0 - 1.7)^2 \cdot 0.1 + (1 - 1.7)^2 \cdot 0.3 + (2 - 1.7)^2 \cdot 0.4 + (3 - 1.7)^2 \cdot 0.2 = 0.289 + 0.147 + 0.036 + 0.338 = 0.81$ ✓.

**Watch out:** Writing $(E[X])^2$ instead of $E[X^2]$ makes the variance $0$; $E[X^2]$ is the weighted average of each value squared.

**Answer:** $c = 0.4$, $E[X] = 1.7$, $\operatorname{Var}(X) = 0.81$.
