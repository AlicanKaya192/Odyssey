**Idea:** A rule for counting consecutive integers without listing them: from $a$ to $b$ (both included) there are $b - a + 1$ integers. First we turn the condition into the "both ends included" form.

**Step 1 — Write it with both ends included.** For integers, $-4 < x$ is the same as $x \ge -3$. The condition is:

$$
-3 \le x \le 2
$$

**Step 2 — Count.**

$$
2 - (-3) + 1 = 5 + 1 = 6
$$

Why the $+1$? From $-3$ to $2$ there are $5$ steps but $6$ numbers: a fence with 5 gaps has 6 posts.

**Step 3 — Find the sum from the average.** The average of consecutive numbers is the average of the two ends:

$$
\frac{-3 + 2}{2} = -\frac{1}{2}
$$

Sum = average $\times$ count $= -\tfrac{1}{2} \cdot 6 = -3$.

**Why the same result?** The first method listed the numbers one by one; this one counted the same numbers with a formula. For very long ranges (say $-100 < x \le 250$) this is the only practical way.

**Answer:** $6$ and $-3$.
