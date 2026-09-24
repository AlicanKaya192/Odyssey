**What is asked?** $A^{-1}$, using Gauss–Jordan.

**Idea:** Write $I$ next to $A$. Turn the left side into $I$ with row operations; the same operations turn the $I$ on the right into $A^{-1}$. That is because the sequence of operations turning $A$ into $I$ is the same as multiplying by $A^{-1}$ on the left.

**Step 1 — Start.**

$$
\left[\begin{array}{cc|cc} 1 & 2 & 1 & 0 \\ 3 & 7 & 0 & 1 \end{array}\right]
$$

**Step 2 — Clear below in column 1.** $R_2 \to R_2 - 3R_1$: $(3 - 3,\ 7 - 6 \mid 0 - 3,\ 1 - 0)$.

$$
\left[\begin{array}{cc|cc} 1 & 2 & 1 & 0 \\ 0 & 1 & -3 & 1 \end{array}\right]
$$

The second pivot on the left is already $1$; no scaling needed.

**Step 3 — Clear above the second pivot.** $R_1 \to R_1 - 2R_2$: $(1 - 0,\ 2 - 2 \mid 1 + 6,\ 0 - 2)$.

$$
\left[\begin{array}{cc|cc} 1 & 0 & 7 & -2 \\ 0 & 1 & -3 & 1 \end{array}\right]
$$

The left side is $I$, so the right side is $A^{-1}$.

$$
A^{-1} = \begin{bmatrix} 7 & -2 \\ -3 & 1 \end{bmatrix}
$$

**Check:**

$$
\begin{bmatrix} 1 & 2 \\ 3 & 7 \end{bmatrix} \begin{bmatrix} 7 & -2 \\ -3 & 1 \end{bmatrix} = \begin{bmatrix} 7 - 6 & -2 + 2 \\ 21 - 21 & -6 + 7 \end{bmatrix} = I
$$

✓

**Answer:** $A^{-1} = \begin{bmatrix} 7 & -2 \\ -3 & 1 \end{bmatrix}$.
