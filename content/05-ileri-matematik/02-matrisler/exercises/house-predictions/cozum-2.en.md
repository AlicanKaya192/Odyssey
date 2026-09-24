**Idea:** Look at the same product through the columns. $X\mathbf{w}$ is the sum of the columns of $X$ weighted by $\mathbf{w}$. Every column of $X$ is a feature (area, rooms, age), so each column product gives that feature's **contribution to all three prices** in one go.

**Step 1 — The area's share.** Multiply the area column by its weight $100$:

$$
100 \begin{bmatrix} 1.2 \\ 0.8 \\ 1.5 \end{bmatrix} = \begin{bmatrix} 120 \\ 80 \\ 150 \end{bmatrix}
$$

**Step 2 — The rooms' share.** Multiply the rooms column by $20$:

$$
20 \begin{bmatrix} 3 \\ 2 \\ 4 \end{bmatrix} = \begin{bmatrix} 60 \\ 40 \\ 80 \end{bmatrix}
$$

**Step 3 — The age's share.** Multiply the age column by $-2$; an older house loses more:

$$
-2 \begin{bmatrix} 10 \\ 25 \\ 5 \end{bmatrix} = \begin{bmatrix} -20 \\ -50 \\ -10 \end{bmatrix}
$$

**Step 4 — Add the shares and $b$.** Each row is added up on its own:

$$
\begin{aligned}
\hat{y}_1 &= 120 + 60 - 20 + 10 = 170 \\
\hat{y}_2 &= 80 + 40 - 50 + 10 = 80 \\
\hat{y}_3 &= 150 + 80 - 10 + 10 = 230
\end{aligned}
$$

**Why the same result?** In the first method we added the same numbers row by row, here column by column. The order of addition does not change the result.

**Why this view helps:** You can see at once why house 2 comes out cheap: its age contributes $-50$, the biggest drop of the three. Explaining a model's prediction by splitting it into feature contributions rests on exactly this idea.

**Answer:** $170$, $80$, $230$.
