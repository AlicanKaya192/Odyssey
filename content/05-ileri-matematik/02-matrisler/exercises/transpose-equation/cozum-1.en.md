**What is asked?** The first matrix on the left has two unknowns ($x$, $y$), the second has one ($z$). We want the three numbers that make the equation hold.

**Idea:** Two operations happen in order: first the transpose ($^\mathsf{T}$), then the addition. The transpose turns rows into columns. Addition is entry by entry. In the end, two matrices are equal when **every entry** is equal, which gives us simple equations.

**Step 1 — Take the transpose.** Row 1 $(x,\ 2)$ becomes column 1, row 2 $(y,\ 5)$ becomes column 2:

$$
\begin{bmatrix} x & 2 \\ y & 5 \end{bmatrix}^\mathsf{T} = \begin{bmatrix} x & y \\ 2 & 5 \end{bmatrix}
$$

Note: $2$ and $y$ swapped places; $x$ and $5$ on the diagonal stayed put.

**Step 2 — Add the second matrix.** Add entries in the same position:

$$
\begin{aligned}
\begin{bmatrix} x & y \\ 2 & 5 \end{bmatrix} + \begin{bmatrix} 1 & 3 \\ 0 & z \end{bmatrix} &= \begin{bmatrix} x + 1 & y + 3 \\ 2 + 0 & 5 + z \end{bmatrix}
\end{aligned}
$$

**Step 3 — Match the right side entry by entry.** The right side is $\begin{bmatrix} 4 & 7 \\ 2 & 9 \end{bmatrix}$:

$$
\begin{aligned}
x + 1 &= 4 \quad \Rightarrow \quad x = 3 \\
y + 3 &= 7 \quad \Rightarrow \quad y = 4 \\
5 + z &= 9 \quad \Rightarrow \quad z = 4
\end{aligned}
$$

**Check:** The bottom-left corner has no unknown: $2 + 0 = 2$, and the right side also has $2$. The question is consistent. ✓

**Watch out:** Forget the transpose and $y$ stays where $2$ is, giving a wrong equation like $y + 0 = 2$.

**Answer:** $x = 3$, $y = 4$, $z = 4$.
