**Idea:** For the sum of the errors there is no need to find each error: $\sum (y - \hat{y}) = \sum y - \sum \hat{y}$. For the absolute values and squares, however, each error must be handled separately.

**Step 1 — The totals.** The sum of the true values and the sum of the predictions:

$$
\begin{aligned}
10 + 7 + 12 + 5 &= 34 \\
13 + 6 + 9 + 8 &= 36
\end{aligned}
$$

**Step 2 — The sum of the errors.**

$$
34 - 36 = -2
$$

Overall the model predicted $2$ thousand too high.

**Step 3 — Absolute values and squares.** There is no shortcut for these, because $|a + b|$ is usually not equal to $|a| + |b|$. The sizes of the errors are $3, 1, 3, 3$:

$$
3 + 1 + 3 + 3 = 10, \qquad 9 + 1 + 9 + 9 = 28
$$

**Why the same result?** Since subtraction is adding the opposite, the sum of four differences equals the difference of the sums. Absolute values and squares "delete" the sign, so this rearrangement does not work for them; they have to be computed one by one as in the first method.

**Answer:** $-2$, $10$ and $28$.
