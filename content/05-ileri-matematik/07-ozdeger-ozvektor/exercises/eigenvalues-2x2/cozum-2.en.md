**Idea:** For $2 \times 2$, the sum of the two eigenvalues is the trace and their product is the determinant. Finding two numbers with a known sum and product is often faster than expanding the equation.

**Step 1 — The trace.** The sum of the diagonal:

$$
\operatorname{tr} B = 4 + 3 = 7
$$

**Step 2 — The determinant.**

$$
\det B = 4 \cdot 3 - 1 \cdot 2 = 10
$$

**Step 3 — Find the two numbers.** $\lambda_1 + \lambda_2 = 7$ and $\lambda_1 \lambda_2 = 10$. Factorise $10$: $1 \cdot 10$ (sum 11), $2 \cdot 5$ (sum 7) ✓.

$$
\lambda_1 = 2, \qquad \lambda_2 = 5
$$

**Step 4 — Test with an eigenvector.** For $\lambda = 5$, $B - 5I = \begin{bmatrix} -1 & 1 \\ 2 & -2 \end{bmatrix}$; $y = x$, so $(1, 1)$. $B(1, 1) = (5, 5) = 5 \cdot (1, 1)$ ✓.

**Why the same result?** The characteristic equation is $\lambda^2 - (\operatorname{tr} B)\lambda + \det B = 0$; in a quadratic the roots add up to $-b/a$ and multiply to $c/a$. The shortcut is exactly this rule.

**Answer:** $2$ and $5$.
