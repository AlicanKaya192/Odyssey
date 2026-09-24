**Idea:** Let us do the same product through the columns. $A\mathbf{x}$ is a weighted sum of the columns of $A$, with the components of $\mathbf{x}$ as weights: column 1 taken $x_1$ times, column 2 taken $x_2$ times, column 3 taken $x_3$ times, all added up.

**Step 1 — Pair columns with weights.** The columns of $A$ are $(1, 3)$, $(-2, 1)$, $(0, 2)$; the components of $\mathbf{x}$ are $4$, $1$, $-1$:

$$
A\mathbf{x} = 4 \begin{bmatrix} 1 \\ 3 \end{bmatrix} + 1 \begin{bmatrix} -2 \\ 1 \end{bmatrix} + (-1) \begin{bmatrix} 0 \\ 2 \end{bmatrix}
$$

**Step 2 — Multiply each column by its weight.**

$$
\begin{aligned}
4 \cdot (1,\ 3) &= (4,\ 12) \\
1 \cdot (-2,\ 1) &= (-2,\ 1) \\
-1 \cdot (0,\ 2) &= (0,\ -2)
\end{aligned}
$$

**Step 3 — Add.** Top components together, bottom components together:

$$
\begin{aligned}
\text{top} &= 4 - 2 + 0 = 2 \\
\text{bottom} &= 12 + 1 - 2 = 11
\end{aligned}
$$

**Why the same result?** Every number from the first method appears here too, just added in a different order. The row view computes each component separately; the column view shows that the result is **built from** the columns of $A$. That second view is the key to understanding, later on, whether an equation has a solution at all.

**Answer:** $(2, 11)$.
