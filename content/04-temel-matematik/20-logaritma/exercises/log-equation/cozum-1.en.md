**What is asked?** The value of $x$ that satisfies the equation. The question also warns of a trap: algebra may give more than one candidate, but not all of them need to be valid.

**Idea:** We go in three steps:

1. Merge the two logarithms into one with the product rule.
2. Get rid of the logarithm using its definition ($\log_2 A = 4$ means $A = 2^4$); a quadratic equation is left.
3. Try every candidate in the **original** equation, because the inside of a logarithm must be positive.

**Step 1 — Merge with the product rule.** $\log_b x + \log_b y = \log_b (xy)$:

$$
\log_2 \big((x + 2)(x - 4)\big) = 4
$$

**Step 2 — Use the definition.** "2 to the 4th power equals the expression inside":

$$
(x + 2)(x - 4) = 2^4 = 16
$$

**Step 3 — Expand and set to zero.**

$$
\begin{aligned}
x^2 - 4x + 2x - 8 &= 16 \\
x^2 - 2x - 8 - 16 &= 0 \\
x^2 - 2x - 24 &= 0
\end{aligned}
$$

**Step 4 — Factorise.** We want two numbers whose product is $-24$ and whose sum is $-2$: $-6$ and $4$ ($-6 \cdot 4 = -24$, $-6 + 4 = -2$).

$$
(x - 6)(x + 4) = 0
$$

A product is zero only when one of its factors is zero, so there are two candidates: $x = 6$ or $x = -4$.

**Step 5 — Try each candidate in the original equation.** The inside of each logarithm must be positive:

| Candidate | $x + 2$ | $x - 4$ | Valid? |
|---|---|---|---|
| $x = 6$ | $8 > 0$ | $2 > 0$ | ✓ |
| $x = -4$ | $-2 < 0$ | $-8 < 0$ | ✕ (no logarithm of a negative) |

**Check:** For $x = 6$

$$
\log_2 8 + \log_2 2 = 3 + 1 = 4
$$

It holds. ✓

**Where did the false solution come from?** In Step 1 we merged the two logarithms. For $x = -4$, $(x + 2)(x - 4) = (-2)(-8) = 16$ is positive, so the merged form looks defined. But $\log_2(-2)$ and $\log_2(-8)$ in the original equation are undefined. Merging hid this condition; checking brought it back.

**Answer:** 6.
