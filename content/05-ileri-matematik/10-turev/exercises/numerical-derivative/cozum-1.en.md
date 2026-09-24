**What is asked?** The estimates two numerical derivative formulas give with the same $h$.

**Idea:** Compute the values and put them into the formulas. Since the true value is known, we will also see which is better.

**Step 1 — The values.** $f(2.1) = 9.261$, $f(2) = 8$, $f(1.9) = 6.859$.

**Step 2 — The forward difference.** $\dfrac{9.261 - 8}{0.1} = \dfrac{1.261}{0.1} = 12.61$.

**Step 3 — The central difference.** $\dfrac{9.261 - 6.859}{0.2} = \dfrac{2.402}{0.2} = 12.01$.

**Check:** The errors: $0.61$ for the forward difference, $0.01$ for the central one. With the same $h$, the central difference is sixty times more accurate ✓.

**Watch out:** In the central difference the bottom is $2h = 0.2$; dividing by $h$ gives a result twice as big, $24.02$.

**Answer:** $12.61$ and $12.01$.
