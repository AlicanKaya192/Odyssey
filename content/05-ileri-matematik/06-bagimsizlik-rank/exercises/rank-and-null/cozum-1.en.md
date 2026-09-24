**What is asked?** How many independent columns there are (the rank), and one of the vectors $A$ sends to zero.

**Idea:** The rank is the number of pivots after elimination. Columns without a pivot are free variables; giving them values produces the null-space vectors.

**Step 1 — Clear column 1.** $R_2 \to R_2 - 2R_1$, $R_3 \to R_3 - R_1$:

$$
\begin{bmatrix} 1 & 2 & 3 \\ 0 & 0 & 0 \\ 0 & -1 & -2 \end{bmatrix}
$$

Row 2 became all zeros: it was twice row 1.

**Step 2 — Move the zero row down.** $R_2 \leftrightarrow R_3$:

$$
\begin{bmatrix} 1 & 2 & 3 \\ 0 & -1 & -2 \\ 0 & 0 & 0 \end{bmatrix}
$$

**Step 3 — Count the pivots.** Columns 1 and 2 have pivots, column 3 does not: $\operatorname{rank} A = 2$.

**Step 4 — The null space.** The echelon form says two equations:

$$
\begin{aligned}
x + 2y + 3z &= 0 \\
-y - 2z &= 0
\end{aligned}
$$

$z$ is free. Put in $z = 1$: the second equation gives $y = -2$; the first gives $x = -2y - 3z = 4 - 3 = 1$.

**Check:** $A(1, -2, 1)$:

$$
\begin{aligned}
1 - 4 + 3 &= 0 \\
2 - 8 + 6 &= 0 \\
1 - 2 + 1 &= 0
\end{aligned}
$$

✓

**Reading the result:** Rank–nullity: $2 + 1 = 3$ columns. The null space is the line $t\,(1, -2, 1)$; column 1 $- 2 \cdot$ column 2 $+$ column 3 $= \mathbf{0}$, so this vector is exactly the dependence among the columns.

**Answer:** $\operatorname{rank} A = 2$; $x = 1$, $y = -2$.
