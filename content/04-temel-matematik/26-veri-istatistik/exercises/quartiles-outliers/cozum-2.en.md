**Idea:** In sorted data of ten values, the position of each quartile is known in advance.

**Step 1 — The positions.** The median of a half of five values is its third value. The third of the lower half is the $3$rd value overall; the third of the upper half is the $5 + 3 = 8$th.

**Step 2 — Read them off.** The $3$rd value is $17$, the $8$th is $25$.

**Step 3 — The fence.** $25 + 1.5 \cdot (25 - 17) = 37$.

**Why the same result?** Writing the halves out and computing the positions point at the same values; the second works on large data without splitting the table.

**Answer:** $17$, $25$ and $37$.
