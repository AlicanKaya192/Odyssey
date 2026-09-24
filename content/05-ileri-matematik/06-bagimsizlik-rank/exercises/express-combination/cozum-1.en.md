**What is asked?** Whether $\mathbf{v}_3$ can be built from the first two vectors; if so, the three vectors really carry only two independent directions.

**Idea:** Expand $a\,\mathbf{v}_1 + b\,\mathbf{v}_2$ into components and set it equal to $\mathbf{v}_3$. Three equations in two unknowns: two equations give $a$ and $b$, the third is a check.

**Step 1 — Expand the combination.**

$$
\begin{aligned}
a(1, 0, 2) + b(0, 1, 1) &= (a,\ b,\ 2a + b)
\end{aligned}
$$

**Step 2 — Match.**

$$
\begin{aligned}
a &= 2 \\
b &= 3 \\
2a + b &= 7
\end{aligned}
$$

**Step 3 — Test with the third equation.** $2 \cdot 2 + 3 = 7$ ✓. All three equations hold: $\mathbf{v}_3 = 2\mathbf{v}_1 + 3\mathbf{v}_2$.

**Step 4 — The rank.** $\mathbf{v}_1$ and $\mathbf{v}_2$ are independent (neither is a multiple of the other), and $\mathbf{v}_3$ is their combination. The number of independent columns is $2$: $\operatorname{rank} = 2$.

**Watch out:** If the third equation failed (say $\mathbf{v}_3 = (2, 3, 8)$), $\mathbf{v}_3$ would not be in the span of the first two and the rank would be $3$.

**Answer:** $a = 2$, $b = 3$, rank $2$.
