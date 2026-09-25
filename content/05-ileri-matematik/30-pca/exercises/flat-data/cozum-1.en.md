**What is asked?** The variance in a given direction, the eigenvalues, and the meaning of a zero eigenvalue.

**Idea:** $u^\mathsf{T}\Sigma u$ directly; for the eigenvalues $\lambda_1 + \lambda_2 = \operatorname{tr}$, $\lambda_1\lambda_2 = \det$.

**Step 1 — Directional variance.** $\frac{1}{2}(1, 1)\Sigma(1, 1)^\mathsf{T} = \frac{1}{2} \cdot 9 = 4.5$.

**Step 2 — Eigenvalues.** $\lambda_1 + \lambda_2 = 5$, $\lambda_1\lambda_2 = 0$: $\lambda_1 = 5$, $\lambda_2 = 0$.

**Step 3 — Meaning.** There is no spread in one direction: all the points lie on a single line. The features' correlation is $\frac{2}{2 \cdot 1} = 1$.

**Check:** $4.5 \leq 5 = \lambda_1$ ✓; no direction's variance can exceed the largest eigenvalue.

**Watch out:** The direction $(1, 1)$ is the first that comes to mind but not the best; since the diagonal entries differ, the best direction is along $(2, 1)$.

**Answer:** $4.5$, $5$, $0$.
