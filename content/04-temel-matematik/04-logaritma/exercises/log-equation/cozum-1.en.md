**1. Combine with the product rule:**

$$
\log_2 \big((x + 2)(x - 4)\big) = 4
$$

**2. Rewrite with the definition** ($\log_2 A = 4 \iff A = 2^4$):

$$
(x + 2)(x - 4) = 16
$$

**3. Expand the brackets and set to zero:**

$$
x^2 - 4x + 2x - 8 = 16
\quad\Rightarrow\quad
x^2 - 2x - 24 = 0
$$

**4. Factorise.** Two numbers whose product is $-24$ and sum is $-2$: $-6$ and $4$.

$$
(x - 6)(x + 4) = 0
\quad\Rightarrow\quad
x = 6 \;\text{ or }\; x = -4
$$

**5. Check every candidate in the original equation:**

| Candidate | $x + 2$ | $x - 4$ | Valid? |
|---|---|---|---|
| $x = 6$ | $8 > 0$ | $2 > 0$ | ✓ |
| $x = -4$ | $-2 < 0$ | $-8 < 0$ | ✕ (negative numbers have no logarithm) |

**Check:** $\log_2 8 + \log_2 2 = 3 + 1 = 4$. ✓

**Where did the false solution come from?** In the first step we combined the two logarithms. For $x = -4$, $(x+2)(x-4) = (-2)(-8) = 16$ is positive, so the combined form looks defined. But $\log_2(-2)$ and $\log_2(-8)$ in the original equation are undefined. Combining hid the condition; checking brought it back.

**Answer: 6**
