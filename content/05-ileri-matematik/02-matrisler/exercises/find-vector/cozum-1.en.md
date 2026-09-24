**What is asked?** Which vector $\mathbf{x}$, multiplied by this matrix, gives $(7, 2)$? The unknowns are the two components of the vector.

**Idea:** In a matrix-vector product, each component of the result is the dot product of one row of the matrix with $\mathbf{x}$ (the row view). Setting each row equal to the number on the right gives two equations in two unknowns.

**Step 1 — Turn the rows into equations.**

- Row 1 $(2, 1)$: $\ 2x_1 + 1 \cdot x_2$ must be $7$.
- Row 2 $(1, -1)$: $\ 1 \cdot x_1 - x_2$ must be $2$.

$$
\begin{aligned}
2x_1 + x_2 &= 7 \\
x_1 - x_2 &= 2
\end{aligned}
$$

**Step 2 — Add the equations.** One has $+x_2$, the other $-x_2$; adding them cancels it and leaves a single unknown:

$$
\begin{aligned}
(2x_1 + x_2) + (x_1 - x_2) &= 7 + 2 \\
3x_1 &= 9 \\
x_1 &= 3
\end{aligned}
$$

**Step 3 — Find $x_2$.** Put $x_1 = 3$ into the second equation:

$$
\begin{aligned}
3 - x_2 &= 2 \\
x_2 &= 1
\end{aligned}
$$

**Check:** Multiply by the matrix and see whether $(7, 2)$ really comes out:

$$
\begin{aligned}
2 \cdot 3 + 1 \cdot 1 &= 7 \\
1 \cdot 3 - 1 \cdot 1 &= 2
\end{aligned}
$$

Both hold. ✓

**Answer:** $x_1 = 3$, $x_2 = 1$.
