**What is asked?** A linear model's weight and constant from two of its predictions, then the error on one example.

**Idea:** $\hat{y} = wx + b$ is a line: $w$ is the slope and $b$ where it crosses the $y$-axis. The two predictions are two points of the line.

**Step 1 — The slope.**

$$
w = \frac{19 - 7}{6 - 2} = \frac{12}{4} = 3
$$

**Step 2 — $b$.** $(2, 7)$: $7 = 3 \cdot 2 + b$, $b = 1$. The model is $\hat{y} = 3x + 1$.

**Step 3 — The error.** At $x = 4$ the prediction is $\hat{y} = 13$; the true value is $15$. The error is $15 - 13 = 2$.

**Check:** $x = 6$: $3 \cdot 6 + 1 = 19$ ✓. The error is positive: the point is $2$ units above the line, so the model predicted this example too low.

**Watch out:** Writing the error the other way round, $\hat{y} - y$, flips the sign ($-2$). It makes no difference in the loss, where it is squared, but for "did it predict too low or too high" the order matters.

**Answer:** $w = 3$, $b = 1$, error $2$.
