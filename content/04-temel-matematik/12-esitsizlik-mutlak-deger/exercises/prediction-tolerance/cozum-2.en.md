**Idea:** First find the range of accepted predictions, then the inputs giving them. Thinking in two steps separates the part that does not depend on the model (the tolerance) from the part that does (the prediction formula).

**Step 1 — Accepted predictions.** Centre $15$, radius $3$:

$$
12 \le \hat{y} \le 18
$$

**Step 2 — Inputs giving the boundary predictions.**

$$
\begin{aligned}
2x + 1 = 12 &\;\Rightarrow\; x = 5.5 \\
2x + 1 = 18 &\;\Rightarrow\; x = 8.5
\end{aligned}
$$

**Step 3 — The range.** $\hat{y} = 2x + 1$ increases as $x$ increases, so $12 \le \hat{y} \le 18$ means exactly $5.5 \le x \le 8.5$.

**Why the same result?** The first route put the prediction formula inside the condition and solved it in one go; this one found the prediction range first and then solved each boundary. Because the prediction is increasing, boundaries go to boundaries.

**Answer:** $5.5$ and $8.5$.
