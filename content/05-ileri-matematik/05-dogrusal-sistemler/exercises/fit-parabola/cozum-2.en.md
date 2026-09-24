**Idea:** Look at the consecutive differences of the $y$ values. Subtracting equations eliminates $a$; taking the difference of the differences eliminates $b$ too and leaves $c$ directly. This is doing the elimination steps in another order.

**Step 1 — Subtract consecutive equations.**

$$
\begin{aligned}
(a + 2b + 4c) - (a + b + c) &= 11 - 6 \\
b + 3c &= 5
\end{aligned}
$$

$$
\begin{aligned}
(a + 3b + 9c) - (a + 2b + 4c) &= 18 - 11 \\
b + 5c &= 7
\end{aligned}
$$

**Step 2 — Subtract these two as well.**

$$
\begin{aligned}
(b + 5c) - (b + 3c) &= 7 - 5 \\
2c &= 2 \;\Rightarrow\; c = 1
\end{aligned}
$$

**Step 3 — Go back.** $b + 3 = 5 \Rightarrow b = 2$; $a + 2 + 1 = 6 \Rightarrow a = 3$.

**Step 4 — Differences for the prediction too.** The differences of the $y$'s are $5, 7$; the difference of differences is $2$ and constant at every step (always so for a parabola). The next difference is $7 + 2 = 9$, the next value $18 + 9 = 27$. With the formula as well, $3 + 8 + 16 = 27$. ✓

**Why does it work?** In $\hat{y} = a + bx + cx^2$, as $x$ increases one by one the consecutive differences grow linearly and the difference of differences is always $2c$. The $2$ here means $c = 1$.

**The link to machine learning:** Here there are exactly as many data points as parameters (3 and 3), and they fit exactly. Real data has many more points and is noisy; then the system is inconsistent and one looks for the parameters with the smallest error (least squares).

**Answer:** $3$, $2$, $1$ and $27$.
