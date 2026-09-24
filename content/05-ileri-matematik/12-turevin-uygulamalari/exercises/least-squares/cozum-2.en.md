**Idea:** The loss is a quadratic function of $w$; expand it and find the vertex with $-\frac{b}{2a}$.

**Step 1 — Expand.**

$$
\begin{aligned}
L(w) &= (2 - w)^2 + (3 - 2w)^2 + (7 - 3w)^2 \\
&= 14w^2 - 58w + 62
\end{aligned}
$$

**Step 2 — The vertex.** $w = \frac{58}{2 \cdot 14} = \frac{29}{14}$. The smallest value is $62 - \frac{58^2}{4 \cdot 14} = 62 - \frac{3364}{56} = \frac{27}{14}$.

**Step 3 — The constant model.** $L(c) = 3c^2 - 24c + 62$, vertex $c = \frac{24}{6} = 4$.

**Why the same result?** In $14w^2 - 58w + 62$, $14 = \sum x_i^2$, $58 = 2 \sum x_i y_i$ and $62 = \sum y_i^2$. The vertex formula $\frac{58}{28}$ is exactly $\frac{\sum x_i y_i}{\sum x_i^2}$; setting the derivative to zero and finding the vertex are the same calculation.

**Answer:** $\frac{29}{14}$, $\frac{27}{14}$ and $4$.
