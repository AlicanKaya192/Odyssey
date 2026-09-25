**Idea:** Expand the loss as a quadratic polynomial in $w$; the vertex formula gives the best $w$, and the leading coefficient gives the curvature.

**Step 1 — Expand.**

$$
\begin{aligned}
L(w) &= (2 - w)^2 + (3 - 2w)^2 + \lambda w^2 \\
&= (5 + \lambda) w^2 - 16 w + 13
\end{aligned}
$$

**Step 2 — The vertex.** $w = \frac{16}{2(5 + \lambda)} = \frac{8}{5 + \lambda}$: $\frac{8}{5}$ at $\lambda = 0$, $\frac{4}{3}$ at $\lambda = 1$.

**Step 3 — The curvature.** $L'' = 2(5 + \lambda) = 12$.

**Why the same result?** The coefficient of $w^2$ is $\sum x_i^2 + \lambda$: the penalty makes the parabola steeper (adds $2\lambda$ to the Hessian) and moves the vertex towards zero. With many variables the same happens with the matrix $X^\mathsf{T}X + \lambda I$; for $\lambda > 0$ this matrix is always invertible.

**Answer:** $\frac{8}{5}$, $\frac{4}{3}$, $12$.
