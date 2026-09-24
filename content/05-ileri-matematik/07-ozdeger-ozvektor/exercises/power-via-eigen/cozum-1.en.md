**What is asked?** The result of multiplying a vector by the same matrix five times. Instead of five matrix products we use the eigenvectors.

**Idea:** On eigenvectors, $A$ just multiplies by a number: $A^5\mathbf{v} = \lambda^5\mathbf{v}$. If we split the vector into eigenvectors, we multiply each piece by the power of its own eigenvalue and add.

**Step 1 — Split $(3, 1)$ into eigenvectors.** $c_1(1, 1) + c_2(1, -1) = (3, 1)$:

$$
\begin{aligned}
c_1 + c_2 &= 3 \\
c_1 - c_2 &= 1
\end{aligned}
$$

Adding gives $2c_1 = 4$, $c_1 = 2$; then $c_2 = 1$.

$$
\begin{bmatrix} 3 \\ 1 \end{bmatrix} = 2 \begin{bmatrix} 1 \\ 1 \end{bmatrix} + 1 \begin{bmatrix} 1 \\ -1 \end{bmatrix}
$$

**Step 2 — Apply $A^5$ to each piece.** The $(1, 1)$ piece is multiplied by $3^5 = 243$, the $(1, -1)$ piece by $1^5 = 1$:

$$
A^5 \begin{bmatrix} 3 \\ 1 \end{bmatrix} = 2 \cdot 243 \begin{bmatrix} 1 \\ 1 \end{bmatrix} + 1 \cdot 1 \begin{bmatrix} 1 \\ -1 \end{bmatrix}
$$

**Step 3 — Add.**

$$
\begin{bmatrix} 486 + 1 \\ 486 - 1 \end{bmatrix} = \begin{bmatrix} 487 \\ 485 \end{bmatrix}
$$

**Reading the result:** The result is very close to the $(1, 1)$ direction: the $\lambda = 3$ piece triples at every step while the $\lambda = 1$ piece stays put. After a few steps the vector points almost entirely along the dominant eigenvector.

**Answer:** $(487, 485)$.
