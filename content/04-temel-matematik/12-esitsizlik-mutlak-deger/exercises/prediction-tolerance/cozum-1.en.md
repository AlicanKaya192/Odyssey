**What is asked?** The range of inputs for which a model's prediction is close enough to the target.

**Idea:** The tolerance condition is an absolute-value inequality. Substitute the prediction, turn it into a double inequality and leave $x$ alone in the middle.

**Step 1 — Substitute.**

$$
|2x + 1 - 15| \le 3 \quad\Rightarrow\quad |2x - 14| \le 3
$$

**Step 2 — A double inequality.**

$$
-3 \le 2x - 14 \le 3
$$

**Step 3 — Add $14$, divide by $2$.**

$$
\begin{aligned}
11 &\le 2x \le 17 \\
5.5 &\le x \le 8.5
\end{aligned}
$$

**Check:** $x = 5.5$: $\hat{y} = 12$, $|12 - 15| = 3 \le 3$ ✓. $x = 8.5$: $\hat{y} = 18$, $|18 - 15| = 3$ ✓. $x = 7$: $\hat{y} = 15$, distance $0$ ✓ (the middle of the range).

**Reading the result:** The model hits the target exactly at $x = 7$; since the prediction changes $2$ times as fast as $x$, a tolerance of $3$ leaves a margin of $1.5$ in $x$.

**Answer:** $a = 5.5$, $b = 8.5$.
