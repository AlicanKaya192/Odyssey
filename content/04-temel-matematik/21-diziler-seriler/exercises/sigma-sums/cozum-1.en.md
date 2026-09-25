**What is asked?** The values of three sums written with Σ.

**Idea:** The sum rules and the known formulas: $\sum_{i=1}^{n} i = \frac{n(n + 1)}{2}$, geometric series $a_1 \frac{1 - r^n}{1 - r}$.

**Step 1 — The first.**

$$
\begin{aligned}
\sum_{i=1}^{20} (2i - 3) &= 2 \sum_{i=1}^{20} i - \sum_{i=1}^{20} 3 \\
&= 2 \cdot 210 - 20 \cdot 3 = 360
\end{aligned}
$$

**Step 2 — The second.** The terms are $3, 6, 12, \dots, 96$: $a_1 = 3$, $r = 2$, $6$ terms.

$$
3 \cdot \frac{1 - 2^6}{1 - 2} = 3 \cdot 63 = 189
$$

**Step 3 — The third.** Write the sum starting at $5$ as a difference of sums starting at $1$:

$$
\sum_{i=5}^{12} i = \sum_{i=1}^{12} i - \sum_{i=1}^{4} i = 78 - 10 = 68
$$

**Check:** The third has $8$ terms ($12 - 5 + 1$) with mean $\frac{5 + 12}{2} = 8.5$; $8 \cdot 8.5 = 68$ ✓.

**Watch out:** Counting $\sum 3$ as $3$ is a common mistake; a constant is added once per term: $20 \cdot 3 = 60$.

**Answer:** $360$, $189$, $68$.
