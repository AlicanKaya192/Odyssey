**What is asked?** First the determinant, then the inverse. The order matters: if the determinant were zero, there would be no inverse.

**Idea:** For $2 \times 2$

$$
\begin{bmatrix} a & b \\ c & d \end{bmatrix}^{-1} = \frac{1}{ad - bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}
$$

Here $a = 4$, $b = 7$, $c = 2$, $d = 6$.

**Step 1 — The determinant.** The product of the main diagonal minus the product of the other diagonal:

$$
\det A = 4 \cdot 6 - 7 \cdot 2 = 24 - 14 = 10
$$

Not zero, so the inverse exists. Also, $A$ multiplies areas by 10, so its inverse will divide them by 10.

**Step 2 — Swap and flip signs.** $4$ and $6$ swap places; $7$ and $2$ stay put but change sign:

$$
\begin{bmatrix} 6 & -7 \\ -2 & 4 \end{bmatrix}
$$

**Step 3 — Divide by the determinant.** Divide every entry by $10$:

$$
A^{-1} = \frac{1}{10} \begin{bmatrix} 6 & -7 \\ -2 & 4 \end{bmatrix} = \begin{bmatrix} 0.6 & -0.7 \\ -0.2 & 0.4 \end{bmatrix}
$$

**Check:** Multiply $A$ by the matrix before the division; it must give $10I$:

$$
\begin{aligned}
\begin{bmatrix} 4 & 7 \\ 2 & 6 \end{bmatrix} \begin{bmatrix} 6 & -7 \\ -2 & 4 \end{bmatrix} &= \begin{bmatrix} 24 - 14 & -28 + 28 \\ 12 - 12 & -14 + 24 \end{bmatrix} \\
&= \begin{bmatrix} 10 & 0 \\ 0 & 10 \end{bmatrix}
\end{aligned}
$$

Divided by $10$ this is $I$. ✓

**Watch out:** $7$ and $2$ do **not** change places, only their signs change. Swapping them too is the most common slip.

**Answer:** $\det A = 10$; $A^{-1} = \begin{bmatrix} 0.6 & -0.7 \\ -0.2 & 0.4 \end{bmatrix}$.
