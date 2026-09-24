**Idea:** Find the null space first; the rank–nullity theorem ($\operatorname{rank} + \dim(\text{null space}) = 3$) then gives the rank.

**Step 1 — The null-space equation.** $X(1, 0, c) = \mathbf{0}$, row by row:

$$
\begin{aligned}
120 + 1.2c &= 0 \\
80 + 0.8c &= 0 \\
150 + 1.5c &= 0 \\
100 + 1.0c &= 0
\end{aligned}
$$

All four give the same answer: $c = -100$. The null space contains a non-zero vector, so its dimension is at least 1.

**Step 2 — Could the null space be larger?** If its dimension were 2, the rank would be $3 - 2 = 1$, so every column would be a multiple of a single vector. But columns 1 and 2 are not proportional ($120/3 = 40$, $150/4 = 37.5$). So the rank is at least 2 and the null space has dimension at most 1.

**Step 3 — The rank.** The null space has dimension exactly 1:

$$
\operatorname{rank} X = 3 - 1 = 2
$$

**The link to machine learning:** Linear regression tries to invert $X^\mathsf{T}X$. Since $X$ is not of full rank ($2 < 3$), $X^\mathsf{T}X$ is singular and the closed-form formula fails. Libraries then either raise an error or pick one of the infinitely many solutions (usually the one with the smallest weights).

**Answer:** $2$ and $-100$.
