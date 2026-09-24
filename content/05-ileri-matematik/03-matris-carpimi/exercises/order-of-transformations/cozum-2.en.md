**Idea:** Each order has a single matrix. "First $R$, then $S$" $= SR$; "first $S$, then $R$" $= RS$. We compute the two products and apply them to $\mathbf{v}$; looking at the matrices also tells us **what kind of transformation** each order is.

**Step 1 — $SR$.** Row times column:

$$
SR = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix} \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} = \begin{bmatrix} 0 & -1 \\ -1 & 0 \end{bmatrix}
$$

**Step 2 — $RS$.**

$$
RS = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}
$$

**Step 3 — Apply them to $\mathbf{v}$.**

$$
\begin{aligned}
SR \begin{bmatrix} 1 \\ 3 \end{bmatrix} &= \begin{bmatrix} -3 \\ -1 \end{bmatrix} \\
RS \begin{bmatrix} 1 \\ 3 \end{bmatrix} &= \begin{bmatrix} 3 \\ 1 \end{bmatrix}
\end{aligned}
$$

**Read the matrices:** $RS = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$ swaps the components: $(x, y) \to (y, x)$, the reflection in the line $y = x$. $SR$ does $(x, y) \to (-y, -x)$: the reflection in the line $y = -x$. A rotation followed by a reflection is again a reflection, but **which mirror** depends on the order.

**Answer:** $(-3, -1)$ and $(3, 1)$.
