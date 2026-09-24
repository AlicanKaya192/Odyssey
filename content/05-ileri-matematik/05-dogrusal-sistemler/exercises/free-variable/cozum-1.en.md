**What is asked?** To write **all** solutions of a system with infinitely many solutions using a parameter, and pick the one with $z = 1$.

**Idea:** After elimination, the column without a pivot is a free variable. We call it $t$ and write the others in terms of $t$ by back substitution.

**Step 1 — The augmented matrix.**

$$
\left[\begin{array}{ccc|c} 1 & 1 & 2 & 5 \\ 2 & 3 & 3 & 13 \\ 1 & 2 & 1 & 8 \end{array}\right]
$$

**Step 2 — Clear column 1.** $R_2 \to R_2 - 2R_1$, $R_3 \to R_3 - R_1$:

$$
\left[\begin{array}{ccc|c} 1 & 1 & 2 & 5 \\ 0 & 1 & -1 & 3 \\ 0 & 1 & -1 & 3 \end{array}\right]
$$

**Step 3 — Clear column 2.** $R_3 \to R_3 - R_2$: the last row is all zeros.

$$
\left[\begin{array}{ccc|c} 1 & 1 & 2 & 5 \\ 0 & 1 & -1 & 3 \\ 0 & 0 & 0 & 0 \end{array}\right]
$$

$0 = 0$: no contradiction, but no information either. Column 3 has no pivot, so $z$ is free.

**Step 4 — Back-substitute with $z = t$.**

$$
\begin{aligned}
y &= 3 + z = 3 + t \\
x &= 5 - y - 2z \\
&= 5 - (3 + t) - 2t \\
&= 2 - 3t
\end{aligned}
$$

All solutions: $(2 - 3t,\ 3 + t,\ t)$.

**Step 5 — Choose $z = 1$.** $t = 1$: $x = 2 - 3 = -1$, $y = 3 + 1 = 4$.

**Check:** $(-1, 4, 1)$ in the three equations: $-1 + 4 + 2 = 5$ ✓, $-2 + 12 + 3 = 13$ ✓, $-1 + 8 + 1 = 8$ ✓.

**Reading the result:** Equation 3 is really a combination of equations 1 and 2 ($R_3 = R_2 - R_1$); the three planes meet along a line, and $(2 - 3t,\ 3 + t,\ t)$ is that line.

**Answer:** $x = -1$, $y = 4$.
