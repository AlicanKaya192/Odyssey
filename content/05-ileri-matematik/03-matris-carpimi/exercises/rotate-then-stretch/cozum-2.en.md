**Idea:** Two transformations in a row equal the single transformation given by their product: $S(R\mathbf{x}) = (SR)\mathbf{x}$. We find $SR$ first, then multiply the point once. If the same transformation is applied to many points, this route is much faster.

**Step 1 — Write the order correctly.** "First $R$, then $S$" reads right to left: $SR$.

**Step 2 — Compute the product.** Row times column:

$$
\begin{aligned}
SR &= \begin{bmatrix} 2 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \\
&= \begin{bmatrix} 2 \cdot 0 + 0 \cdot 1 & 2 \cdot (-1) + 0 \cdot 0 \\ 0 \cdot 0 + 1 \cdot 1 & 0 \cdot (-1) + 1 \cdot 0 \end{bmatrix} \\
&= \begin{bmatrix} 0 & -2 \\ 1 & 0 \end{bmatrix}
\end{aligned}
$$

**Step 3 — Apply it to the point.**

$$
\begin{bmatrix} 0 & -2 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} 3 \\ 1 \end{bmatrix} = \begin{bmatrix} -2 \\ 3 \end{bmatrix}
$$

**Check:** The columns of $SR$ must be where $\mathbf{e}_1$ and $\mathbf{e}_2$ end up. $\mathbf{e}_1$ rotates to $(0, 1)$ and stays $(0, 1)$ after the stretch: column 1 is $(0, 1)$. ✓ $\mathbf{e}_2$ rotates to $(-1, 0)$ and stretches to $(-2, 0)$: column 2 is $(-2, 0)$. ✓

**Answer:** $(-2, 3)$.
