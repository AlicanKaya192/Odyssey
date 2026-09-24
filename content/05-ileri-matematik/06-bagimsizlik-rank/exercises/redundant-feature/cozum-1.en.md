**What is asked?** How many independent pieces of information the table holds (the rank), and the direction that leaves the model's weights undetermined (the null space).

**Idea:** Rank = number of independent columns. Finding the relation among the columns gives both the rank and the null space.

**Step 1 — Column 3.** $1.2 = 120 / 100$, $0.8 = 80 / 100$, … in every row column 3 is $\tfrac{1}{100}$ of column 1:

$$
\mathbf{a}_3 = \tfrac{1}{100}\,\mathbf{a}_1
$$

Column 3 is redundant; it adds no new direction.

**Step 2 — Are columns 1 and 2 independent?** $120 / 3 = 40$, $80 / 2 = 40$, but $150 / 4 = 37.5$. The ratio is not constant: $\mathbf{a}_1$ is not a multiple of $\mathbf{a}_2$. They are independent.

**Step 3 — The rank.** Two independent columns, and the third is a multiple of one of them: $\operatorname{rank} X = 2$.

**Step 4 — The null space.** $X(1, 0, c) = \mathbf{a}_1 + c\,\mathbf{a}_3 = \mathbf{a}_1 + \tfrac{c}{100}\,\mathbf{a}_1 = \left(1 + \tfrac{c}{100}\right)\mathbf{a}_1$. For this to be zero:

$$
\begin{aligned}
1 + \frac{c}{100} &= 0 \\
c &= -100
\end{aligned}
$$

**Check:** In row 1, $120 \cdot 1 + 3 \cdot 0 + 1.2 \cdot (-100) = 120 - 120 = 0$ ✓; the other rows vanish the same way.

**Reading the result:** If a model's weights are $\mathbf{w}$, then $\mathbf{w} + t\,(1, 0, -100)$ gives **exactly the same** predictions: 1 unit more weight on feature 1 and 100 units less on feature 3 cancel out. The data cannot tell these weights apart; the fix is to drop the redundant column.

**Answer:** $\operatorname{rank} X = 2$, $c = -100$.
