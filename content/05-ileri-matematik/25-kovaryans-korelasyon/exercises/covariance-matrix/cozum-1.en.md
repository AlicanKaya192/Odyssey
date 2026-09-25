**What is asked?** The covariance matrix and correlation from a centred data matrix.

**Idea:** The entries of $X^\mathsf{T}X$ are dot products of columns; dividing by $n - 1$ gives the covariances.

**Step 1 — $\Sigma_{11}$.** The first column with itself: $4 + 1 + 0 + 1 + 4 = 10$; $\frac{10}{4} = 2.5$.

**Step 2 — $\Sigma_{12}$.** The dot product of the columns: $2 + 2 + 0 + 1 + 4 = 9$; $\frac{9}{4} = 2.25$. The second column also gives $\frac{10}{4} = 2.5$:

$$
\Sigma = \begin{pmatrix} 2.5 & 2.25 \\ 2.25 & 2.5 \end{pmatrix}
$$

**Step 3 — Correlation.** $r = \frac{2.25}{\sqrt{2.5 \cdot 2.5}} = 0.9$.

**Check:** $\Sigma$ is symmetric; for $w = (1, -1)$, $w^\mathsf{T}\Sigma w = 2.5 + 2.5 - 4.5 = 0.5 \geq 0$ ✓ (positive semi-definite).

**Watch out:** Computing $XX^\mathsf{T}$ gives a $5 \times 5$ matrix; the covariance matrix must be as large as the number of features, $2 \times 2$.

**Answer:** $2.5$, $2.25$, $0.9$.
