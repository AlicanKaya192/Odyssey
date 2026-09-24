**Idea:** The first two questions can be answered without finding the eigenvalues at all: the sum is always the trace, the product always the determinant. For the third one we do need the eigenvalues.

**Step 1 — The trace.** The sum of the diagonal:

$$
\operatorname{tr} A = 2 + 3 + (-1) = 4
$$

**Step 2 — The determinant.** Expand along the first column; only the $2$ is non-zero:

$$
\det A = 2 \cdot \begin{vmatrix} 3 & 5 \\ 0 & -1 \end{vmatrix} = 2 \cdot (-3 - 0) = -6
$$

**Step 3 — $A^2$ needs the eigenvalues.** The characteristic polynomial:

$$
\det(A - \lambda I) = (2 - \lambda)(3 - \lambda)(-1 - \lambda)
$$

The roots are $2, 3, -1$. The eigenvalues of $A^2$ are their squares: $4, 9, 1$; the largest is $9$.

**Watch out:** "The square of the largest eigenvalue" is not always the largest eigenvalue of $A^2$. If the eigenvalues were $2$ and $-3$, the largest eigenvalue would be $2$, but the largest of $A^2$ would be $(-3)^2 = 9$. You need to look at absolute values.

**Answer:** $4$, $-6$, $9$.
