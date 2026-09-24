**What is asked?** How many numbers divide $360$ exactly, and how many of them lie in a given range.

**Idea:** If the batch size is $k$, then $360 = k \cdot (\text{number of batches})$; so $k$ is a divisor of $360$. The number of divisors comes from the prime factors; for the range we list the divisors in pairs.

**Step 1 — Prime factors.**

$$
360 = 2^3 \cdot 3^2 \cdot 5
$$

**Step 2 — The number of divisors.** Every divisor has the form $2^a \cdot 3^b \cdot 5^c$; there are $4$ choices for $a$, $3$ for $b$, $2$ for $c$:

$$
(3 + 1)(2 + 1)(1 + 1) = 24
$$

**Step 3 — List the divisors in pairs.**

| Small | Large |
|---|---|
| $1$ | $360$ |
| $2$ | $180$ |
| $3$ | $120$ |
| $4$ | $90$ |
| $5$ | $72$ |
| $6$ | $60$ |
| $8$ | $45$ |
| $9$ | $40$ |
| $10$ | $36$ |
| $12$ | $30$ |
| $15$ | $24$ |
| $18$ | $20$ |

$12$ pairs, $24$ divisors ✓.

**Step 4 — Between $10$ and $50$.** From the left, $10, 12, 15, 18$; from the right, $45, 40, 36, 30, 24, 20$:

$$
4 + 6 = 10
$$

**Watch out:** When searching in pairs, skip non-divisors such as $7$ ($360 = 7 \cdot 51 + 3$) and $11$, but do not forget $8$ and $9$.

**Answer:** $24$ choices; $10$ of them are between $10$ and $50$.
