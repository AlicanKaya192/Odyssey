**What is asked?** The stretch factors of the vectors whose direction $B$ does not change.

**Idea:** $B\mathbf{v} = \lambda\mathbf{v}$ has a non-zero solution only when $B - \lambda I$ is singular: $\det(B - \lambda I) = 0$.

**Step 1 — $B - \lambda I$.** $\lambda$ is subtracted only on the diagonal:

$$
B - \lambda I = \begin{bmatrix} 4 - \lambda & 1 \\ 2 & 3 - \lambda \end{bmatrix}
$$

**Step 2 — The determinant.**

$$
\begin{aligned}
\det(B - \lambda I) &= (4 - \lambda)(3 - \lambda) - 1 \cdot 2 \\
&= 12 - 7\lambda + \lambda^2 - 2 \\
&= \lambda^2 - 7\lambda + 10
\end{aligned}
$$

**Step 3 — Set it to zero and factorise.** Two numbers with product $10$ and sum $-7$: $-2$ and $-5$.

$$
\lambda^2 - 7\lambda + 10 = (\lambda - 2)(\lambda - 5) = 0
$$

The eigenvalues are $\lambda = 2$ and $\lambda = 5$.

**Check:** The sum $2 + 5 = 7 = 4 + 3$ (the trace) ✓; the product $2 \cdot 5 = 10 = \det B$ ✓.

**Watch out:** The diagonal entries ($4$ and $3$) are **not** the eigenvalues. That holds only for triangular matrices; here the off-diagonal $1$ and $2$ affect the result too.

**Answer:** $2$ and $5$.
