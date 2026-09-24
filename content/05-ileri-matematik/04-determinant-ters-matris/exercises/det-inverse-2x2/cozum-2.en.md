**Idea:** You can find the inverse without memorising the formula. $AA^{-1} = I$ means that column 1 of $A^{-1}$, call it $\mathbf{x}$, satisfies $A\mathbf{x} = (1, 0)$, and column 2, $\mathbf{y}$, satisfies $A\mathbf{y} = (0, 1)$. We solve two small systems. This route also shows **why** the formula is correct.

**Step 1 — The determinant.** $\det A = 4 \cdot 6 - 7 \cdot 2 = 10$; not zero, so the systems have unique solutions.

**Step 2 — Column 1: $A\mathbf{x} = (1, 0)$.** With $\mathbf{x} = (p, r)$, row by row:

$$
\begin{aligned}
4p + 7r &= 1 \\
2p + 6r &= 0
\end{aligned}
$$

From the second equation $p = -3r$. Put it into the first:

$$
\begin{aligned}
4(-3r) + 7r &= 1 \\
-5r &= 1 \\
r &= -0.2
\end{aligned}
$$

and $p = -3 \cdot (-0.2) = 0.6$.

**Step 3 — Column 2: $A\mathbf{y} = (0, 1)$.** With $\mathbf{y} = (q, s)$:

$$
\begin{aligned}
4q + 7s &= 0 \\
2q + 6s &= 1
\end{aligned}
$$

Multiply the second equation by 2 and subtract it from the first: $(4q + 7s) - (4q + 12s) = 0 - 2$, so $-5s = -2$ and $s = 0.4$. From the first equation $4q = -7 \cdot 0.4 = -2.8$, $q = -0.7$.

**Step 4 — Put the columns side by side.**

$$
A^{-1} = \begin{bmatrix} 0.6 & -0.7 \\ -0.2 & 0.4 \end{bmatrix}
$$

**Why the same result?** If you solved these two systems with letters ($a, b, c, d$), $ad - bc$ would always appear in the denominator; the formula is exactly a shortcut for this calculation. When the determinant is zero these systems have no solution, and that is why there is no inverse.

**Answer:** $10$; $0.6$, $-0.7$, $-0.2$, $0.4$.
