**What is asked?** The largest number dividing both numbers, and the smallest number that is a multiple of both.

**Idea:** Prime factors are the building blocks of a number. A divisor of a number is built from some of its prime factors; a multiple contains at least all of them. For the GCD we take what is in both; for the LCM, what is in either.

**Step 1 — Factorise $84$.**

$$
84 = 2 \cdot 42 = 2 \cdot 2 \cdot 21 = 2^2 \cdot 3 \cdot 7
$$

**Step 2 — Factorise $126$.**

$$
126 = 2 \cdot 63 = 2 \cdot 3 \cdot 21 = 2 \cdot 3^2 \cdot 7
$$

**Step 3 — GCD: common primes, smaller exponents.** The common primes are $2$, $3$, $7$. Exponents: for $2$, $\min(2, 1) = 1$; for $3$, $\min(1, 2) = 1$; for $7$, $1$.

$$
\text{GCD} = 2 \cdot 3 \cdot 7 = 42
$$

**Step 4 — LCM: all primes, larger exponents.** $2$ for $2$, $2$ for $3$, $1$ for $7$:

$$
\text{LCM} = 2^2 \cdot 3^2 \cdot 7 = 4 \cdot 9 \cdot 7 = 252
$$

**Check:** $84 = 42 \cdot 2$ and $126 = 42 \cdot 3$ ✓. $252 = 84 \cdot 3 = 126 \cdot 2$ ✓. Also $42 \cdot 252 = 10\,584 = 84 \cdot 126$ ✓.

**Answer:** GCD $42$, LCM $252$.
