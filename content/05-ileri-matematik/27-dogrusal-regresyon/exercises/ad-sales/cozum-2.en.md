**Idea:** The columns of $X$ are $(1, 1, 1, 1, 1)$ and $x$; solve $X^\mathsf{T}Xw = X^\mathsf{T}y$.

**Step 1 — Matrices.** $X^\mathsf{T}X = \begin{pmatrix} 5 & 15 \\ 15 & 55 \end{pmatrix}$, $X^\mathsf{T}y = \begin{pmatrix} 25 \\ 83 \end{pmatrix}$ ($\sum xy = 3 + 10 + 12 + 28 + 30 = 83$).

**Step 2 — Solution.** The determinant is $50$.

$$
\begin{pmatrix} b \\ w \end{pmatrix} = \frac{1}{50}\begin{pmatrix} 55 \cdot 25 - 15 \cdot 83 \\ -15 \cdot 25 + 5 \cdot 83 \end{pmatrix} = \frac{1}{50}\begin{pmatrix} 130 \\ 40 \end{pmatrix}
$$

$b = 2.6$, $w = 0.8$.

**Step 3 — Prediction.** $(1, 6) \cdot (2.6, \ 0.8) = 7.4$.

**Why the same result?** The deviation formula is what you get by solving the $2 \times 2$ system of normal equations by hand and simplifying; both are the solution of the same equations.

**Answer:** $0.8$, $2.6$ and $7.4$.
