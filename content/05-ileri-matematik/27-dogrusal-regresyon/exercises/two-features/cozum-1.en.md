**What is asked?** The $2 \times 2$ solution of the normal equations.

**Idea:** $w = (X^\mathsf{T}X)^{-1}X^\mathsf{T}y$.

**Step 1 — Determinant.** $4 \cdot 2 - 2 \cdot 2 = 4$.

**Step 2 — Inverse.** $\frac{1}{4}\begin{pmatrix} 2 & -2 \\ -2 & 4 \end{pmatrix}$.

**Step 3 — Product.**

$$
w = \frac{1}{4}\begin{pmatrix} 2 \cdot 10 - 2 \cdot 6 \\ -2 \cdot 10 + 4 \cdot 6 \end{pmatrix} = \frac{1}{4}\begin{pmatrix} 8 \\ 4 \end{pmatrix} = \begin{pmatrix} 2 \\ 1 \end{pmatrix}
$$

**Check:** $X^\mathsf{T}Xw = (4 \cdot 2 + 2 \cdot 1, \ 2 \cdot 2 + 2 \cdot 1) = (10, 6)$ ✓.

**Watch out:** In the inverse the diagonal entries swap places; the off-diagonal ones only change sign.

**Answer:** $4$, $2$, $1$.
