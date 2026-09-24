**Idea:** Making the basis vectors the columns of a matrix $B$ gives $c_1\mathbf{b}_1 + c_2\mathbf{b}_2 = B\mathbf{c}$. The coordinates are the solution of $B\mathbf{c} = \mathbf{x}$: $\mathbf{c} = B^{-1}\mathbf{x}$. When many vectors need coordinates in the same basis, $B^{-1}$ is found once and each vector takes a single product.

**Step 1 — The basis matrix.**

$$
B = \begin{bmatrix} 1 & 1 \\ 2 & -1 \end{bmatrix}
$$

**Step 2 — Determinant and inverse.** $\det B = 1 \cdot (-1) - 1 \cdot 2 = -3$. Swap, flip signs, divide by $-3$:

$$
B^{-1} = \frac{1}{-3} \begin{bmatrix} -1 & -1 \\ -2 & 1 \end{bmatrix} = \frac{1}{3} \begin{bmatrix} 1 & 1 \\ 2 & -1 \end{bmatrix}
$$

**Step 3 — $\mathbf{c} = B^{-1}\mathbf{x}$.**

$$
\begin{aligned}
\mathbf{c} &= \frac{1}{3} \begin{bmatrix} 1 \cdot 5 + 1 \cdot 1 \\ 2 \cdot 5 - 1 \cdot 1 \end{bmatrix} \\
&= \frac{1}{3} \begin{bmatrix} 6 \\ 9 \end{bmatrix} = \begin{bmatrix} 2 \\ 3 \end{bmatrix}
\end{aligned}
$$

**Why the same result?** The two equations of the first method are exactly the rows of $B\mathbf{c} = \mathbf{x}$. And $\det B \ne 0$ says $\mathbf{b}_1$ and $\mathbf{b}_2$ are independent, that is, really a basis.

**Answer:** $(2, 3)$.
