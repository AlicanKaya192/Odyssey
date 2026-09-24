**What is asked?** $3A - 2B$ is a new $2 \times 2$ matrix. We want its four entries.

**Idea:** For matrices, scaling and subtraction work **entry by entry**, just as for vectors. Multiplications first, then the subtraction:

- Multiplying a matrix by a number multiplies every entry by that number.
- Subtracting two matrices subtracts the entries in the same position (both must be the same size; here both are $2 \times 2$).

**Step 1 — Multiply $A$ by 3.** Each of the four entries triples:

$$
3A = \begin{bmatrix} 3 \cdot 2 & 3 \cdot (-1) \\ 3 \cdot 0 & 3 \cdot 3 \end{bmatrix} = \begin{bmatrix} 6 & -3 \\ 0 & 9 \end{bmatrix}
$$

**Step 2 — Multiply $B$ by 2.**

$$
2B = \begin{bmatrix} 2 \cdot 1 & 2 \cdot 4 \\ 2 \cdot (-2) & 2 \cdot 1 \end{bmatrix} = \begin{bmatrix} 2 & 8 \\ -4 & 2 \end{bmatrix}
$$

**Step 3 — Subtract entries in the same position.** Top left minus top left, top right minus top right, and so on:

$$
\begin{aligned}
c_{11} &= 6 - 2 = 4 \\
c_{12} &= -3 - 8 = -11 \\
c_{21} &= 0 - (-4) = 4 \\
c_{22} &= 9 - 2 = 7
\end{aligned}
$$

$$
C = \begin{bmatrix} 4 & -11 \\ 4 & 7 \end{bmatrix}
$$

**Watch out:** In $c_{21}$ a negative number is subtracted: $0 - (-4) = +4$. Writing $-4$ here is the most common slip.

**Answer:** $c_{11} = 4$, $c_{12} = -11$, $c_{21} = 4$, $c_{22} = 7$.
