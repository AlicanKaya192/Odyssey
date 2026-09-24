**What is asked?** Two equations in two unknowns. In matrix language $A\mathbf{x} = \mathbf{b}$, and the solution is $\mathbf{x} = A^{-1}\mathbf{b}$.

**Idea:** With numbers we solve $3x = 6$ by dividing by 3. Matrices have no division; instead we multiply both sides on the left by $A^{-1}$: $A^{-1}A\mathbf{x} = \mathbf{x}$.

**Step 1 — Matrix form.** The coefficients go row by row into $A$, the right-hand sides into $\mathbf{b}$:

$$
\begin{bmatrix} 2 & 1 \\ 5 & 3 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 4 \\ 11 \end{bmatrix}
$$

**Step 2 — The determinant.**

$$
\det A = 2 \cdot 3 - 1 \cdot 5 = 6 - 5 = 1
$$

Not zero: the system has exactly one solution.

**Step 3 — The inverse.** Swap, flip signs, divide by $1$:

$$
A^{-1} = \begin{bmatrix} 3 & -1 \\ -5 & 2 \end{bmatrix}
$$

**Step 4 — $\mathbf{x} = A^{-1}\mathbf{b}$.** Row times vector:

$$
\begin{aligned}
\begin{bmatrix} 3 & -1 \\ -5 & 2 \end{bmatrix} \begin{bmatrix} 4 \\ 11 \end{bmatrix} &= \begin{bmatrix} 3 \cdot 4 - 1 \cdot 11 \\ -5 \cdot 4 + 2 \cdot 11 \end{bmatrix} \\
&= \begin{bmatrix} 12 - 11 \\ -20 + 22 \end{bmatrix} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}
\end{aligned}
$$

**Check:** Put them into the original equations: $2 \cdot 1 + 2 = 4$ ✓ and $5 \cdot 1 + 3 \cdot 2 = 11$ ✓.

**Watch out:** $A^{-1}$ multiplies **on the left**. Writing $\mathbf{b}$ first and $A^{-1}$ on the right ($\mathbf{b}A^{-1}$) is undefined.

**Answer:** $x = 1$, $y = 2$.
