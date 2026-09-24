**Idea:** The question "is $\mathbf{v}_3$ in the span of $\mathbf{v}_1$ and $\mathbf{v}_2$?" is the question whether the system with columns $\mathbf{v}_1, \mathbf{v}_2$ and right-hand side $\mathbf{v}_3$ has a solution. Let us eliminate the augmented matrix; the same elimination also shows the rank.

**Step 1 — The augmented matrix** $[\mathbf{v}_1\ \mathbf{v}_2 \mid \mathbf{v}_3]$:

$$
\left[\begin{array}{cc|c} 1 & 0 & 2 \\ 0 & 1 & 3 \\ 2 & 1 & 7 \end{array}\right]
$$

**Step 2 — $R_3 \to R_3 - 2R_1$.** $(2 - 2,\ 1 - 0 \mid 7 - 4)$:

$$
\left[\begin{array}{cc|c} 1 & 0 & 2 \\ 0 & 1 & 3 \\ 0 & 1 & 3 \end{array}\right]
$$

**Step 3 — $R_3 \to R_3 - R_2$.**

$$
\left[\begin{array}{cc|c} 1 & 0 & 2 \\ 0 & 1 & 3 \\ 0 & 0 & 0 \end{array}\right]
$$

The last row is $0 = 0$: no contradiction, so a solution exists. The first two rows give $a = 2$, $b = 3$.

**Step 4 — The rank.** The same elimination works on the $3 \times 3$ matrix with the three vectors as columns; since the left side is unchanged, the pivots are again only in columns 1 and 2. $\operatorname{rank} = 2$, determinant $0$.

**Why the same result?** $\operatorname{rank}\,[\mathbf{v}_1\ \mathbf{v}_2] = \operatorname{rank}\,[\mathbf{v}_1\ \mathbf{v}_2 \mid \mathbf{v}_3] = 2$: the right-hand side brought no new pivot, so $\mathbf{v}_3$ adds no new direction.

**Answer:** $2$, $3$ and rank $2$.
