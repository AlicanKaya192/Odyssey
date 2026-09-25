**Idea:** Draw the boxes on squared paper and count the squares; the area is the number of unit squares.

**Step 1 — The boxes.** The true box is $4$ columns $\times$ $3$ rows $= 12$ squares. The prediction is $4$ columns $\times$ $4$ rows $= 16$ squares.

**Step 2 — The shared squares.** The squares inside both boxes lie between $x = 3$ and $5$ and between $y = 2$ and $4$: $2 \times 2 = 4$ squares.

**Step 3 — Total covered.** Only in the true box $12 - 4 = 8$, only in the prediction $16 - 4 = 12$, in both $4$: total $8 + 12 + 4 = 24$. $\text{IoU} = \frac{4}{24}$.

**Why the same result?** The count "only A + only B + shared" is the formula $A + B - \text{intersection}$ written out: $A + B$ counts the shared region twice, and subtracting it once fixes that.

**Answer:** $4$, $24$ and $\frac{1}{6}$.
