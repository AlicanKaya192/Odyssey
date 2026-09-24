**What is asked?** Where a point lands after two transformations. The order matters: rotation first, then the stretch.

**Idea:** Write the matrix of each transformation, multiply the point by the first one, then the result by the second. We build the matrices with the column rule: column 1 is where $\mathbf{e}_1$ goes, column 2 where $\mathbf{e}_2$ goes.

**Step 1 — The rotation matrix.** Turning by $90°$ sends $\mathbf{e}_1 = (1, 0)$ up to $(0, 1)$ and $\mathbf{e}_2 = (0, 1)$ left to $(-1, 0)$:

$$
R = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}
$$

**Step 2 — Rotate the point.**

$$
\begin{aligned}
R \begin{bmatrix} 3 \\ 1 \end{bmatrix} &= \begin{bmatrix} 0 \cdot 3 + (-1) \cdot 1 \\ 1 \cdot 3 + 0 \cdot 1 \end{bmatrix} \\
&= \begin{bmatrix} -1 \\ 3 \end{bmatrix}
\end{aligned}
$$

**Step 3 — The stretch matrix.** $\mathbf{e}_1$ doubles to $(2, 0)$; $\mathbf{e}_2$ stays:

$$
S = \begin{bmatrix} 2 & 0 \\ 0 & 1 \end{bmatrix}
$$

**Step 4 — Stretch the rotated point.** $x$ doubles, $y$ stays:

$$
S \begin{bmatrix} -1 \\ 3 \end{bmatrix} = \begin{bmatrix} 2 \cdot (-1) \\ 3 \end{bmatrix} = \begin{bmatrix} -2 \\ 3 \end{bmatrix}
$$

**Watch out:** Reversing the order and stretching first would give $(6, 1)$, then rotating would give $(-1, 6)$. A different point.

**Answer:** $(-2, 3)$.
