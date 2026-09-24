**Idea:** ReLU has two cases: $0$ if its inside is negative, the inside itself otherwise. Write the network as a single function in two pieces, then put in the inputs.

**Step 1 — The boundary.** $2x - 3 \ge 0 \Leftrightarrow x \ge 1.5$.

**Step 2 — Two pieces.**

$$
y = \begin{cases} 3(2x - 3) + 1 = 6x - 8, & x \ge 1.5 \\ 3 \cdot 0 + 1 = 1, & x < 1.5 \end{cases}
$$

**Step 3 — The values.** $x = 4 \ge 1.5$: $y = 24 - 8 = 16$. $x = 1 < 1.5$: $y = 1$.

**Why the same result?** The layer-by-layer calculation picks one of these pieces at each input and applies it. The piecewise form shows this for all inputs at once and makes plain how ReLU lets the network "bend".

**Answer:** $16$ and $1$.
