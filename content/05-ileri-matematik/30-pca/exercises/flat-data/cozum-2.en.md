**Idea:** The columns of $\Sigma$, $(4, 2)$ and $(2, 1)$, are multiples of each other; the matrix "sees" only one direction: $(2, 1)$.

**Step 1 — Directional variance.** $\Sigma(1, 1) = (6, 3)$; $\frac{1}{2}(1, 1) \cdot (6, 3) = 4.5$.

**Step 2 — $\lambda_1$.** $\Sigma(2, 1) = (10, 5) = 5 \cdot (2, 1)$: $\lambda_1 = 5$.

**Step 3 — $\lambda_2$.** The perpendicular direction $(1, -2)$: $\Sigma(1, -2) = (0, 0)$, $\lambda_2 = 0$.

**Why the same result?** A zero determinant means the matrix sends some direction to zero; that direction is the eigenvector of $\lambda = 0$. The trace then gives the only remaining eigenvalue. For this data, reducing to $1$ dimension with PCA loses no information at all.

**Answer:** $4.5$, $5$ and $0$.
