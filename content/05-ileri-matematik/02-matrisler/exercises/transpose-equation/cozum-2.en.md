**Idea:** Instead of transposing the matrix with unknowns, we can transpose **both sides** of the equation. Two rules make this possible:

$$
\begin{aligned}
(A + B)^\mathsf{T} &= A^\mathsf{T} + B^\mathsf{T} \\
(A^\mathsf{T})^\mathsf{T} &= A
\end{aligned}
$$

This way the matrix with unknowns stays untransposed, and the transpose is applied only to matrices whose numbers we know.

**Step 1 — Transpose both sides.** The transpose of the sum on the left is the sum of the transposes. The first matrix is transposed twice, so it returns to itself:

$$
\begin{bmatrix} x & 2 \\ y & 5 \end{bmatrix} + \begin{bmatrix} 1 & 3 \\ 0 & z \end{bmatrix}^\mathsf{T} = \begin{bmatrix} 4 & 7 \\ 2 & 9 \end{bmatrix}^\mathsf{T}
$$

**Step 2 — Compute the known transposes.** Turn rows into columns:

$$
\begin{bmatrix} x & 2 \\ y & 5 \end{bmatrix} + \begin{bmatrix} 1 & 0 \\ 3 & z \end{bmatrix} = \begin{bmatrix} 4 & 2 \\ 7 & 9 \end{bmatrix}
$$

**Step 3 — Match entry by entry.**

$$
\begin{aligned}
x + 1 &= 4 \quad \Rightarrow \quad x = 3 \\
y + 3 &= 7 \quad \Rightarrow \quad y = 4 \\
5 + z &= 9 \quad \Rightarrow \quad z = 4
\end{aligned}
$$

The top-right corner holds as well: $2 + 0 = 2$. ✓

**Why the same equations?** The transpose only moves entries around; it does not change which entry is added to which. This method moved the transpose onto the known matrices. Transpose rules help you bring an equation into the form that is easiest to read.

**Answer:** $x = 3$, $y = 4$, $z = 4$.
