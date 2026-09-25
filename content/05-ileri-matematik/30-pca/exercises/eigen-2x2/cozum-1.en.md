**What is asked?** The eigenvalues of the covariance matrix and the share explained by the first component.

**Idea:** The eigenvalues are the variances along the component directions; their sum is the total variance.

**Step 1 — Equation.** $(5 - \lambda)^2 = 16$, $5 - \lambda = \pm 4$.

**Step 2 — Eigenvalues.** $\lambda_1 = 9$, $\lambda_2 = 1$.

**Step 3 — Share.** $\frac{9}{10} = 0.9$.

**Check:** $\lambda_1 + \lambda_2 = 10$, the same as the trace ✓; $\lambda_1\lambda_2 = 9 = 25 - 16$, the same as the determinant ✓.

**Watch out:** The share is not computed from the diagonal entries ($\frac{5}{10}$); that is the share of an original feature. The component, a combination of both features, carries more.

**Answer:** $9$, $1$, $0.9$.
