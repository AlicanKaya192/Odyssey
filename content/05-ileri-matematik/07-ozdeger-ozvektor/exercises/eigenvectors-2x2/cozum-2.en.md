**Idea:** Without building $(A - \lambda I)$, put $\mathbf{v} = (1, y)$ straight into $B\mathbf{v} = \lambda\mathbf{v}$. The two components give two equations; one finds $y$, the other is a check.

**Step 1 — Compute $B(1, y)$.**

$$
B \begin{bmatrix} 1 \\ y \end{bmatrix} = \begin{bmatrix} 4 + y \\ 2 + 3y \end{bmatrix}
$$

**Step 2 — $\lambda = 2$: $\,(4 + y,\ 2 + 3y) = (2,\ 2y)$.**

From the first component $4 + y = 2$, so $y = -2$. Test with the second: $2 + 3 \cdot (-2) = -4$ and $2y = -4$ ✓.

**Step 3 — $\lambda = 5$: $\,(4 + y,\ 2 + 3y) = (5,\ 5y)$.**

From the first component $4 + y = 5$, so $y = 1$. The second: $2 + 3 = 5$ and $5y = 5$ ✓.

**Why does it work?** The first-component equation is the first row of $(B - \lambda I)$ rearranged ($4 + y = \lambda \iff (4 - \lambda) + y = 0$). The second component holding as well confirms that $\lambda$ really is an eigenvalue.

**Watch out:** If you try a number that is not an eigenvalue (say $\lambda = 3$), the first component gives $y = -1$ but the second fails: $2 - 3 = -1 \ne -3$.

**Answer:** $-2$ and $1$.
