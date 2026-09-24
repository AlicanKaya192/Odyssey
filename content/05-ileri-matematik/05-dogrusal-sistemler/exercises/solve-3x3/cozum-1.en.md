**What is asked?** The $x, y, z$ that satisfy all three equations at once.

**Idea:** Bring the augmented matrix to echelon form (clear below the pivots), then back-substitute starting from the bottom.

**Step 1 — The augmented matrix.**

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 4 \\ 2 & -1 & 1 & 8 \\ 1 & 2 & -1 & -3 \end{array}\right]
$$

**Step 2 — Clear column 1.** The pivot is $1$. $R_2 \to R_2 - 2R_1$ and $R_3 \to R_3 - R_1$. For example row 2: $(2 - 2,\ -1 - 2,\ 1 - 2 \mid 8 - 8) = (0, -3, -1 \mid 0)$.

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 4 \\ 0 & -3 & -1 & 0 \\ 0 & 1 & -2 & -7 \end{array}\right]
$$

**Step 3 — Swap rows.** Using $1$ instead of $-3$ as the pivot of column 2 avoids fractions: $R_2 \leftrightarrow R_3$.

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 4 \\ 0 & 1 & -2 & -7 \\ 0 & -3 & -1 & 0 \end{array}\right]
$$

**Step 4 — Clear column 2.** $R_3 \to R_3 + 3R_2$: $(0,\ -3 + 3,\ -1 - 6 \mid 0 - 21)$.

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 4 \\ 0 & 1 & -2 & -7 \\ 0 & 0 & -7 & -21 \end{array}\right]
$$

**Step 5 — Back-substitute.** From the bottom up:

$$
\begin{aligned}
-7z &= -21 \;\Rightarrow\; z = 3 \\
y - 2z &= -7 \;\Rightarrow\; y = -7 + 6 = -1 \\
x + y + z &= 4 \;\Rightarrow\; x = 4 + 1 - 3 = 2
\end{aligned}
$$

**Check:** Put them into the original equations: $2 - 1 + 3 = 4$ ✓, $4 + 1 + 3 = 8$ ✓, $2 - 2 - 3 = -3$ ✓.

**Answer:** $x = 2$, $y = -1$, $z = 3$.
