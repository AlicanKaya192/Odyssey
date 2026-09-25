**Idea:** Polynomial regression makes new features from $x$ and builds a linear model. The feature vector is $(1, x, x^2, x^3)$ and the weight vector $(w_0, w_1, w_2, w_3)$; the prediction is the sum of their matching products.

**Step 1 — $x = 2$.** Features $(1, 2, 4, 8)$, weights $(1, 2, -1, 0.5)$:

$$
\begin{aligned}
&1 \cdot 1 + 2 \cdot 2 + 4 \cdot (-1) + 8 \cdot 0.5 \\
&= 1 + 4 - 4 + 4 = 5
\end{aligned}
$$

**Step 2 — $x = -2$.** Features $(1, -2, 4, -8)$:

$$
1 - 4 - 4 - 4 = -11
$$

**Step 3 — The error.** $6 - 5 = 1$.

**Why the same result?** Adding up the matching products is computing the polynomial term by term; we just wrote the powers into a list first. This view also shows why the model is "linear in the $w$'s": the $w$'s are only multipliers.

**Answer:** $5$, $-11$ and $1$.
