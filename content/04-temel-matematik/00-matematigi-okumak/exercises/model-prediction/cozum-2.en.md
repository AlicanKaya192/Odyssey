**Idea:** Writing the features, weights and products in a table shows at a glance which feature pushes the prediction which way. Tables exactly like this are used to explain models.

**Step 1 — Build the table.**

| Part | Value | Weight | Contribution |
|---|---|---|---|
| $x_1$ | $80$ | $0.5$ | $+40$ |
| $x_2$ | $6$ | $-2$ | $-12$ |
| constant $b$ | | | $+10$ |

**Step 2 — Add the contributions.**

$$
40 - 12 + 10 = 38
$$

**Step 3 — The squared error.** $(35 - 38)^2 = (-3)^2 = 9$. Taking the difference the other way round ($\hat{y} - y = 3$) gives the same square: $3^2 = 9$.

**Reading the result:** The table shows that $x_2$, because of its negative weight, pulls the prediction **down** by $12$ units. The sign of a weight says whether that feature raises the prediction or not.

**Answer:** $38$ and $9$.
