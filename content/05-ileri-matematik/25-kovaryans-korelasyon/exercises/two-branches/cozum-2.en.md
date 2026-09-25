**Idea:** $X + Y = w^\mathsf{T}(X, Y)$ with $w = (1, 1)$; its variance is $w^\mathsf{T}\Sigma w$.

**Step 1 — Matrix.** $\Sigma = \begin{pmatrix} 25 & 12 \\ 12 & 36 \end{pmatrix}$; off-diagonal $r\sigma_X\sigma_Y = 12$.

**Step 2 — Sum.** $w = (1, 1)$: $w^\mathsf{T}\Sigma w$ is the sum of all entries, $25 + 12 + 12 + 36 = 85$.

**Step 3 — Difference.** $w = (1, -1)$: the off-diagonal terms get a minus sign, $25 - 12 - 12 + 36 = 37$.

**Why the same result?** $w^\mathsf{T}\Sigma w = \sum_{i,j} w_i w_j \Sigma_{ij}$; for two variables this is exactly $\operatorname{Var}X + \operatorname{Var}Y \pm 2\operatorname{Cov}$.

**Answer:** $12$, $85$ and $37$.
