**What is asked?** How large the accuracy difference between two models is compared with random fluctuation.

**Idea:** Each accuracy is a sample proportion; for two independent test sets the variance of the difference is the sum of the two variances.

**Step 1 — A.** $\sqrt{\frac{0.88 \cdot 0.12}{1000}} = \sqrt{0.0001056} \approx 0.0103$.

**Step 2 — The difference.** For B, $\sqrt{\frac{0.9 \cdot 0.1}{1000}} \approx 0.0095$. The standard error of the difference is $\sqrt{0.0001056 + 0.00009} \approx 0.0140$.

**Step 3 — $z$.** $\frac{0.02}{0.0140} \approx 1.43$.

**Check:** The standard error of the difference is smaller than the sum of the two ($0.0198$) and larger than the bigger one ($0.0103$) ✓.

**Watch out:** $1.43$ standard errors is below two: even though the difference is $2$ percent, it can be explained by random fluctuation. Saying "B is better" needs more test data.

**Answer:** $\approx 0.0103$, $\approx 0.0140$, $\approx 1.43$.
