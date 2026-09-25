**What is asked?** Whether the difference between two sign-up rates can be explained by random fluctuation.

**Idea:** Each proportion has variance $\frac{p(1 - p)}{n}$; for independent groups the variance of the difference is the sum of the two.

**Step 1 — SE.** $\frac{0.04 \cdot 0.96}{5000} = 0.00000768$ and $\frac{0.05 \cdot 0.95}{5000} = 0.0000095$. The sum is $0.00001718$; the square root $\approx 0.00414$.

**Step 2 — $z$.** $\frac{0.01}{0.00414} \approx 2.41$.

**Step 3 — p.** $2 \cdot (1 - 0.992) = 0.016$. Significant with $\alpha = 0.05$: B's sign-up rate really does seem higher.

**Check:** The $95$ percent confidence interval is $0.01 \pm 1.96 \cdot 0.00414 = [0.0019, \ 0.0181]$; it does not contain $0$ ✓.

**Watch out:** Adding $\text{SE}_A + \text{SE}_B$ for the standard error of the difference; variances add.

**Answer:** $\approx 0.00414$, $\approx 2.41$, $\approx 0.016$.
