**What is asked?** For each eigenvalue, the direction that $B$ merely stretches by that amount.

**Idea:** Write $B\mathbf{v} = \lambda\mathbf{v}$ as $(B - \lambda I)\mathbf{v} = \mathbf{0}$. Since $\lambda$ is a genuine eigenvalue, $B - \lambda I$ is singular: its two rows carry the same information, and one is enough.

**Step 1 — $\lambda = 2$.**

$$
B - 2I = \begin{bmatrix} 2 & 1 \\ 2 & 1 \end{bmatrix}
$$

Both rows are the same: $2x + y = 0$. Put in $x = 1$: $y = -2$. The eigenvector is $(1, -2)$.

**Step 2 — $\lambda = 5$.**

$$
B - 5I = \begin{bmatrix} -1 & 1 \\ 2 & -2 \end{bmatrix}
$$

The first row says $-x + y = 0$, so $y = x$. For $x = 1$, $y = 1$. The eigenvector is $(1, 1)$. (The second row, $2x - 2y = 0$, says the same.)

**Step 3 — Check.** Multiply each eigenvector by $B$:

$$
\begin{aligned}
B \begin{bmatrix} 1 \\ -2 \end{bmatrix} &= \begin{bmatrix} 4 - 2 \\ 2 - 6 \end{bmatrix} = \begin{bmatrix} 2 \\ -4 \end{bmatrix} = 2 \begin{bmatrix} 1 \\ -2 \end{bmatrix} \\
B \begin{bmatrix} 1 \\ 1 \end{bmatrix} &= \begin{bmatrix} 5 \\ 5 \end{bmatrix} = 5 \begin{bmatrix} 1 \\ 1 \end{bmatrix}
\end{aligned}
$$

Both hold. ✓

**Reading the result:** The two eigenvectors are not perpendicular ($1 \cdot 1 + (-2) \cdot 1 = -1$). Since $B$ is not symmetric, that is to be expected.

**Answer:** for $\lambda = 2$, $y = -2$; for $\lambda = 5$, $y = 1$.
