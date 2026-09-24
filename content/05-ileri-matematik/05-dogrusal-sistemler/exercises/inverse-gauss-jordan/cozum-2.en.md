**Idea:** Find the same result with the $2 \times 2$ formula we know and see why Gauss–Jordan holds. Comparing the two shows both methods were applied correctly.

**Step 1 — The determinant.**

$$
\det A = 1 \cdot 7 - 2 \cdot 3 = 7 - 6 = 1
$$

**Step 2 — Swap, flip signs, divide by $1$.** $1$ and $7$ swap places; the signs of $2$ and $3$ flip:

$$
A^{-1} = \frac{1}{1} \begin{bmatrix} 7 & -2 \\ -3 & 1 \end{bmatrix}
$$

**Step 3 — Compare.** Exactly the matrix we found on the right side with Gauss–Jordan.

**Why the same?** Every operation in Gauss–Jordan (here $R_2 - 3R_1$ and $R_1 - 2R_2$) is multiplication on the left by a matrix. Since the product of these matrices turns $A$ into $I$, it is $A^{-1}$ itself. The formula is a shortcut for doing these operations once with the letters $a, b, c, d$ and writing down the result; the $ad - bc$ in the denominator is the product of the pivots from elimination ($1 \cdot 1 = 1$).

**When to use which?** For $2 \times 2$ the formula is faster. From $3 \times 3$ upwards the formula gets complicated, while Gauss–Jordan works with the same steps in any size.

**Answer:** $7$, $-2$, $-3$, $1$.
