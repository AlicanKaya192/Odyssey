**What is asked?** A $3 \times 3$ determinant, and what happens to it when the matrix is multiplied by 2.

**Idea:** Expansion along the first row: each first-row entry is multiplied by the $2 \times 2$ determinant left after deleting its row and column; the signs are $+, -, +$.

**Step 1 — $a_{11} = 2$.** Delete row 1 and column 1; what is left is $\begin{bmatrix} 3 & 2 \\ 1 & 2 \end{bmatrix}$:

$$
2 \cdot (3 \cdot 2 - 2 \cdot 1) = 2 \cdot 4 = 8
$$

**Step 2 — $a_{12} = 0$.** Zero times anything is zero; this term needs no calculation.

**Step 3 — $a_{13} = 1$.** Delete row 1 and column 3; what is left is $\begin{bmatrix} 1 & 3 \\ 1 & 1 \end{bmatrix}$:

$$
1 \cdot (1 \cdot 1 - 3 \cdot 1) = -2
$$

**Step 4 — Add with the signs.**

$$
\det A = 8 - 0 + (-2) = 6
$$

**Step 5 — $\det(2A)$.** In $2A$ each of the three rows is multiplied by 2. Multiplying one row by 2 multiplies the determinant by 2; for three rows that is $2 \cdot 2 \cdot 2 = 2^3 = 8$:

$$
\det(2A) = 2^3 \cdot \det A = 8 \cdot 6 = 48
$$

**Watch out:** $\det(2A) = 2 \cdot 6 = 12$ is the most common slip. Geometrically: when all three edges of a cube double, the volume grows 8 times.

**Answer:** $\det A = 6$, $\det(2A) = 48$.
