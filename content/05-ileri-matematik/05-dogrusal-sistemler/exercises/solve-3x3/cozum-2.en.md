**Idea:** The order of elimination is up to you; you can pick which unknown to eliminate first by looking at the equations. Here the coefficients of $z$ are $+1, +1, -1$: adding equation 3 to the other two removes $z$ in one move and leaves a system in two unknowns.

**Step 1 — Add equations 1 and 3.**

$$
\begin{aligned}
(x + y + z) + (x + 2y - z) &= 4 + (-3) \\
2x + 3y &= 1
\end{aligned}
$$

**Step 2 — Add equations 2 and 3.**

$$
\begin{aligned}
(2x - y + z) + (x + 2y - z) &= 8 + (-3) \\
3x + y &= 5
\end{aligned}
$$

**Step 3 — Solve the two-unknown system.** From the second, $y = 5 - 3x$. Put it into the first:

$$
\begin{aligned}
2x + 3(5 - 3x) &= 1 \\
2x + 15 - 9x &= 1 \\
-7x &= -14 \\
x &= 2
\end{aligned}
$$

and $y = 5 - 3 \cdot 2 = -1$.

**Step 4 — Find $z$.** From equation 1: $2 + (-1) + z = 4$, so $z = 3$.

**Why the same result?** Adding equations is a row operation too ($R_1 \to R_1 + R_3$). Gaussian elimination clears the columns in order from left to right; we merely changed the order and cleared $z$'s column first. Row operations do not change the solutions, so whatever the order you end up in the same place.

**Answer:** $(2, -1, 3)$.
