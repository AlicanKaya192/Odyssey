**Idea:** A shortcut you can memorise for $3 \times 3$: write the first two columns once more on the right. Add the products of the three diagonals going down to the right, subtract the three going down to the left.

**Step 1 — The extended table.** Append columns 1 and 2 to $A$:

$$
\begin{matrix} 2 & 0 & 1 & 2 & 0 \\ 1 & 3 & 2 & 1 & 3 \\ 1 & 1 & 2 & 1 & 1 \end{matrix}
$$

**Step 2 — Diagonals going down to the right (plus).**

$$
\begin{aligned}
2 \cdot 3 \cdot 2 &= 12 \\
0 \cdot 2 \cdot 1 &= 0 \\
1 \cdot 1 \cdot 1 &= 1
\end{aligned}
$$

Total $13$.

**Step 3 — Diagonals going down to the left (minus).**

$$
\begin{aligned}
1 \cdot 3 \cdot 1 &= 3 \\
2 \cdot 2 \cdot 1 &= 4 \\
0 \cdot 1 \cdot 2 &= 0
\end{aligned}
$$

Total $7$.

**Step 4 — The difference.** $\det A = 13 - 7 = 6$, the same as with the expansion.

**Step 5 — Check $\det(2A)$.** Every entry of $2A$ is doubled; each Sarrus product contains **three** entries, so each product grows $2^3 = 8$ times. So does the difference: $8 \cdot 6 = 48$.

**Watch out:** Sarrus only works for $3 \times 3$; it fails for $4 \times 4$ and larger. There the way to go is expansion or Gaussian elimination.

**Answer:** $6$ and $48$.
