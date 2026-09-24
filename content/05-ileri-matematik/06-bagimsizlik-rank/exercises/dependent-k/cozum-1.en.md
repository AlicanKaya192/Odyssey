**What is asked?** The value of $k$ that puts the two vectors on the same line, and the multiple between them.

**Idea:** Making the two vectors the columns of a $2 \times 2$ matrix, being dependent means the determinant is zero (the unit square is squashed into a segment, zero area).

**Step 1 — Matrix and determinant.**

$$
\det \begin{bmatrix} 2 & 3 \\ k & 6 \end{bmatrix} = 2 \cdot 6 - 3 \cdot k = 12 - 3k
$$

**Step 2 — Set it to zero.**

$$
\begin{aligned}
12 - 3k &= 0 \\
k &= 4
\end{aligned}
$$

**Step 3 — Find the multiple.** $\mathbf{u} = (2, 4)$ and $\mathbf{v} = (3, 6)$. From the first components $3 = c \cdot 2$, so $c = 1.5$. Test with the second: $1.5 \cdot 4 = 6$ ✓.

**Reading the result:** With $k = 4$ the two vectors point the same way; together they span only a line. For any other $k$ they would be independent and span the whole plane.

**Answer:** $k = 4$, $c = 1.5$.
