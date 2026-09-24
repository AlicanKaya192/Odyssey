**Idea:** Each column of $AB$ is $A$ times that column of $B$. So we do two separate matrix–vector products. For a matrix–vector product we can use the column view too: $A\mathbf{b}$ is the sum of the columns of $A$ weighted by the components of $\mathbf{b}$.

The columns of $A$ are $\mathbf{a}_1 = (2, 3)$ and $\mathbf{a}_2 = (-1, 4)$.

**Step 1 — Column 1 of $C$: $A\,(1, 0)$.** The weights are $1$ and $0$: only column 1 of $A$ is left.

$$
1 \begin{bmatrix} 2 \\ 3 \end{bmatrix} + 0 \begin{bmatrix} -1 \\ 4 \end{bmatrix} = \begin{bmatrix} 2 \\ 3 \end{bmatrix}
$$

**Step 2 — Column 2 of $C$: $A\,(2, -3)$.** Add 2 times column 1 of $A$ and $-3$ times column 2:

$$
\begin{aligned}
2 \begin{bmatrix} 2 \\ 3 \end{bmatrix} - 3 \begin{bmatrix} -1 \\ 4 \end{bmatrix} &= \begin{bmatrix} 4 \\ 6 \end{bmatrix} + \begin{bmatrix} 3 \\ -12 \end{bmatrix} \\
&= \begin{bmatrix} 7 \\ -6 \end{bmatrix}
\end{aligned}
$$

**Step 3 — Put the columns side by side.**

$$
C = \begin{bmatrix} 2 & 7 \\ 3 & -6 \end{bmatrix}
$$

**Why the same result?** In the first method we computed each entry separately; here we produced the two entries of a column together. The numbers added are the same, only grouped differently. This view shortens the work a lot when $B$ has simple columns like $1, 0$.

**Answer:** $2$, $7$, $3$, $-6$.
