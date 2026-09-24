**Idea:** Find the GCD without factorising, using division with remainder (Euclid). Then use the link $\text{GCD} \cdot \text{LCM} = a \cdot b$ to get the LCM with one division.

**Step 1 — Divide the larger by the smaller.**

$$
126 = 84 \cdot 1 + 42
$$

**Step 2 — Divide the divisor by the remainder.**

$$
84 = 42 \cdot 2 + 0
$$

The remainder is $0$: the last divisor, $42$, is the GCD.

**Step 3 — Get the LCM from the link.**

$$
\text{LCM} = \frac{84 \cdot 126}{42} = 84 \cdot 3 = 252
$$

We used $126 \div 42 = 3$ to shrink the multiplication.

**Why the same result?** Euclid rests on the fact that "every number dividing two numbers also divides their difference"; the common divisors are kept at every step while the numbers shrink. The product link comes from prime factors: for each prime, the smaller exponent (going to the GCD) plus the larger exponent (going to the LCM) equals the sum of the exponents in the two numbers.

**Answer:** $42$ and $252$.
