**Idea:** Gauss's way: pair the first row with the last, the second with the second-to-last. Each pair gives the same total.

**Step 1 — The last row.** Each row adds $3$, and there are $19$ more rows after the first: $12 + 57 = 69$.

**Step 2 — The pairs.** $12 + 69 = 81$, $15 + 66 = 81$, $18 + 63 = 81$… As one goes up the other comes down by the same amount, so the total is always $81$. $20$ rows make $10$ pairs: $10 \cdot 81 = 810$.

**Step 3 — Passing $50$.** $50 - 12 = 38$ seats must be added. In steps of $3$, $12$ additions make $36$ ($48$ seats, not enough) and $13$ make $39$ ($51$ seats). $13$ additions after the first row means row $14$.

**Why the same result?** The $\frac{n}{2}$ in the sum formula is the number of pairs and $(a_1 + a_n)$ the total of each pair. The "number of additions" in step 3 is the $n - 1$ of the formula.

**Answer:** $69$, $810$ and $14$.
