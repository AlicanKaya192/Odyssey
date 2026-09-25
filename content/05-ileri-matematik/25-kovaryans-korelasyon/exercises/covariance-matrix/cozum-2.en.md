**Idea:** $X^\mathsf{T}X = \sum_i x_i x_i^\mathsf{T}$: the sum of each observation's own $2 \times 2$ outer product.

**Step 1 — Outer products.** $(-2, -1)$: $\begin{pmatrix} 4 & 2 \\ 2 & 1 \end{pmatrix}$; $(-1, -2)$: $\begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix}$; $(0, 0)$: zero; $(1, 1)$: $\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$; $(2, 2)$: $\begin{pmatrix} 4 & 4 \\ 4 & 4 \end{pmatrix}$.

**Step 2 — Sum and divide.** The sum is $\begin{pmatrix} 10 & 9 \\ 9 & 10 \end{pmatrix}$; divided by $4$, $\Sigma_{11} = 2.5$, $\Sigma_{12} = 2.25$.

**Step 3 — Correlation.** $\frac{9}{\sqrt{10 \cdot 10}} = 0.9$; the divisor cancels.

**Why the same result?** Doing the matrix product column by column (dot products) or row by row (a sum of outer products) gives the same matrix; the second shows each observation's contribution to the covariance separately.

**Answer:** $2.5$, $2.25$ and $0.9$.
