**What is asked?** The weight that makes the squared error for two data points smallest, and that error.

**Idea:** Each square is quadratic in $w$, and so is their sum. An upward-opening parabola has its smallest value at the vertex, $w = -\frac{b}{2a}$.

**Step 1 — Expand the squares.**

$$
\begin{aligned}
(7 - 2w)^2 &= 49 - 28w + 4w^2 \\
(5 - w)^2 &= 25 - 10w + w^2
\end{aligned}
$$

**Step 2 — Add.**

$$
E(w) = 5w^2 - 38w + 74
$$

**Step 3 — The vertex.**

$$
w = -\frac{-38}{2 \cdot 5} = \frac{38}{10} = 3.8
$$

**Step 4 — The smallest error.** Working out the errors directly is easy: $7 - 2 \cdot 3.8 = -0.6$ and $5 - 3.8 = 1.2$:

$$
E(3.8) = 0.36 + 1.44 = 1.8
$$

**Reading the result:** The first point wants $w = 3.5$ and the second $w = 5$; no $w$ satisfies both exactly. The best compromise is $3.8$, and the remaining error $1.8$ is above zero. Linear regression finds exactly this compromise.

**Answer:** $w = 3.8$; the smallest error is $1.8$.
