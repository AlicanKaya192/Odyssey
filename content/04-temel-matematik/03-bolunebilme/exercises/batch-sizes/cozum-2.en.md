**Idea:** If the batch size is $k$, the number of batches is $360 \div k$. If the size is between $10$ and $50$, the number of batches is between $360 \div 50 = 7.2$ and $360 \div 10 = 36$. So counting the sizes in the range is the same as counting the divisors between $8$ and $36$.

**Step 1 — Total choices.** Every divisor gives a batch size: from $360 = 2^3 \cdot 3^2 \cdot 5$, $4 \cdot 3 \cdot 2 = 24$ choices.

**Step 2 — The range of the number of batches.** If $10 \le k \le 50$, the number of batches $m = 360 \div k$ satisfies

$$
7.2 \le m \le 36
$$

$m$ is also a divisor of $360$ and a whole number, so $8 \le m \le 36$.

**Step 3 — The divisors in this range.** The divisors of $360$ between $8$ and $36$:

$$
8, 9, 10, 12, 15, 18, 20, 24, 30, 36
$$

That is $10$. Each corresponds to a batch size: $m = 8 \to k = 45$, $m = 36 \to k = 10$, …

**Why the same result?** Divisors come in pairs: if $k$ is a divisor, so is $360 \div k$. This pairing sends the sizes between $10$ and $50$ one-to-one to the batch counts between $8$ and $36$; counting either gives the same result.

**Answer:** $24$ and $10$.
