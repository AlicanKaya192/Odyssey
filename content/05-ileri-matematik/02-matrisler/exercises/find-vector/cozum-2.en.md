In the column view the question is: with which coefficients do I build $(7, 2)$ from the columns $(2, 1)$ and $(1, -1)$?

$$
x_1 \begin{bmatrix} 2 \\ 1 \end{bmatrix} + x_2 \begin{bmatrix} 1 \\ -1 \end{bmatrix} = \begin{bmatrix} 7 \\ 2 \end{bmatrix}
$$

From the second component $x_1 = 2 + x_2$. Substitute into the first:

$$
\begin{aligned}
2(2 + x_2) + x_2 &= 7 \\
4 + 3x_2 &= 7 \\
x_2 &= 1
\end{aligned}
$$

and $x_1 = 2 + 1 = 3$. Check: $3\,(2, 1) + 1\,(1, -1) = (6, 3) + (1, -1) = (7, 2)$. ✓

"Solve $A\mathbf{x} = \mathbf{b}$" and "build $\mathbf{b}$ from the columns" are the same question. In the Gaussian elimination chapter we will do this systematically for large systems.

**Answer: $x_1 = 3$, $x_2 = 1$**
