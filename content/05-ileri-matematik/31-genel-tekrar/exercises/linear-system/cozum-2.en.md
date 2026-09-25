**Idea:** $x_i = \frac{\det A_i}{\det A}$, where $A_i$ is $A$ with its $i$th column replaced by $b$.

**Step 1 — $\det A$.** $10$.

**Step 2 — $x_1$.** $\det\begin{pmatrix} 7 & 1 \\ 8 & 4 \end{pmatrix} = 28 - 8 = 20$; $x_1 = 2$.

**Step 3 — $x_2$.** $\det\begin{pmatrix} 3 & 7 \\ 2 & 8 \end{pmatrix} = 24 - 14 = 10$; $x_2 = 1$.

**Why the same result?** Expanding each component of $A^{-1}b$ gives exactly these determinant ratios; Cramer's rule is multiplication by the inverse written component by component. Handy for small systems; for large ones Gaussian elimination is cheaper.

**Answer:** $10$, $2$ and $1$.
