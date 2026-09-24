**Idea:** The system can also be solved with determinants alone, without writing the inverse (**Cramer's rule**). To find an unknown, replace that unknown's column of $A$ with $\mathbf{b}$ and divide the new determinant by $\det A$:

$$
x = \frac{\det A_x}{\det A}
\qquad
y = \frac{\det A_y}{\det A}
$$

Why does it work? Expanding $\mathbf{x} = A^{-1}\mathbf{b}$ with the $2 \times 2$ inverse formula gives $\det A$ in the denominator and exactly these small determinants in the numerator.

**Step 1 — $\det A$.** $2 \cdot 3 - 1 \cdot 5 = 1$.

**Step 2 — For $x$.** Replace column 1 (the coefficients of $x$, $2, 5$) with $\mathbf{b} = (4, 11)$:

$$
\det A_x = \begin{vmatrix} 4 & 1 \\ 11 & 3 \end{vmatrix} = 12 - 11 = 1
$$

$$
x = \frac{1}{1} = 1
$$

**Step 3 — For $y$.** Replace column 2 ($1, 3$) with $\mathbf{b}$:

$$
\det A_y = \begin{vmatrix} 2 & 4 \\ 5 & 11 \end{vmatrix} = 22 - 20 = 2
$$

$$
y = \frac{2}{1} = 2
$$

**When is it used?** For small systems with two or three unknowns, especially when only **one** unknown is asked for, it is quick. For large systems it is very slow; Gaussian elimination is used there.

**Answer:** $x = 1$, $y = 2$.
