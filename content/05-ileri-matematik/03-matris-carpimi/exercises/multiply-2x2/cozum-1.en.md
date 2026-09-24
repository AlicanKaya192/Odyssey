**What is asked?** The product of two $2 \times 2$ matrices; the result is $2 \times 2$ as well, so four numbers.

**Idea:** Matrix multiplication is not done entry by entry. The entry of $C$ in row $i$, column $j$ is the **dot product** of row $i$ of $A$ and column $j$ of $B$: multiply matching numbers and add.

First separate the rows and the columns:

- Rows of $A$: $(2, -1)$ and $(3, 4)$
- Columns of $B$: $(1, 0)$ and $(2, -3)$

**Step 1 — $c_{11}$:** row 1 with column 1.

$$
c_{11} = 2 \cdot 1 + (-1) \cdot 0 = 2 + 0 = 2
$$

**Step 2 — $c_{12}$:** row 1 with column 2.

$$
\begin{aligned}
c_{12} &= 2 \cdot 2 + (-1) \cdot (-3) \\
&= 4 + 3 = 7
\end{aligned}
$$

**Step 3 — $c_{21}$:** row 2 with column 1.

$$
c_{21} = 3 \cdot 1 + 4 \cdot 0 = 3
$$

**Step 4 — $c_{22}$:** row 2 with column 2.

$$
\begin{aligned}
c_{22} &= 3 \cdot 2 + 4 \cdot (-3) \\
&= 6 - 12 = -6
\end{aligned}
$$

$$
C = \begin{bmatrix} 2 & 7 \\ 3 & -6 \end{bmatrix}
$$

**Watch out:** Multiplying entry by entry would give $\begin{bmatrix} 2 & -2 \\ 0 & -12 \end{bmatrix}$. That is a different operation (the Hadamard product).

**Answer:** $c_{11} = 2$, $c_{12} = 7$, $c_{21} = 3$, $c_{22} = -6$.
