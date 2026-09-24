**Idea:** Use the diagonalisation $A = PDP^{-1}$ to write $A^k$ once in terms of $k$, then put in $k = 5$. It gives the result and a way to check it.

**Step 1 — $P$, $D$, $P^{-1}$.** Eigenvectors in the columns, eigenvalues on the diagonal:

$$
P = \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}
\qquad
D = \begin{bmatrix} 3 & 0 \\ 0 & 1 \end{bmatrix}
$$

$\det P = -2$, so $P^{-1} = \tfrac{1}{2}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}$.

**Step 2 — $A^k = PD^kP^{-1}$.** The diagonal of $D^k$ is $3^k$ and $1$:

$$
\begin{aligned}
A^k &= \frac{1}{2} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix} \begin{bmatrix} 3^k & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix} \\
&= \frac{1}{2} \begin{bmatrix} 3^k + 1 & 3^k - 1 \\ 3^k - 1 & 3^k + 1 \end{bmatrix}
\end{aligned}
$$

Check with $k = 1$: $\tfrac{1}{2}\begin{bmatrix} 4 & 2 \\ 2 & 4 \end{bmatrix} = A$ ✓.

**Step 3 — $k = 5$.** $3^5 = 243$:

$$
A^5 = \frac{1}{2} \begin{bmatrix} 244 & 242 \\ 242 & 244 \end{bmatrix} = \begin{bmatrix} 122 & 121 \\ 121 & 122 \end{bmatrix}
$$

**Step 4 — Apply it to the vector.**

$$
\begin{aligned}
A^5 \begin{bmatrix} 3 \\ 1 \end{bmatrix} &= \begin{bmatrix} 366 + 121 \\ 363 + 122 \end{bmatrix} \\
&= \begin{bmatrix} 487 \\ 485 \end{bmatrix}
\end{aligned}
$$

**Why the same result?** In the first method, instead of multiplying by $P^{-1}$, we split the vector into eigenvectors directly; that is exactly computing $P^{-1}\mathbf{x}$ ($c_1 = 2$, $c_2 = 1$).

**Answer:** $487$ and $485$.
