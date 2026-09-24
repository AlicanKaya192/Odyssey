**Idea:** Instead of trial and error, we can write the number inside directly as a **power of the base**. Then this rule finishes the job:

$$
\log_b (b^k) = k
$$

Why? $\log_b (b^k)$ asks "to which power must I raise $b$ to get $b^k$?"; the answer is plainly $k$. A logarithm and an exponent with the same base cancel each other.

**Step 1 — Write $81$ as a power of 3.** $81 = 9 \cdot 9 = 3 \cdot 3 \cdot 3 \cdot 3 = 3^4$.

**Step 2 — Write $\frac{1}{8}$ as a power of 2.** $8 = 2^3$, and one over a power is a negative exponent:

$$
\frac{1}{8} = \frac{1}{2^3} = 2^{-3}
$$

**Step 3 — Apply the rule.**

$$
\begin{aligned}
\log_3 81 + \log_2 \tfrac{1}{8} &= \log_3 3^4 + \log_2 2^{-3} \\
&= 4 + (-3) \\
&= 1
\end{aligned}
$$

**When does it help?** Whenever you can write the number inside as a power of the base, this is the fastest route. If you cannot (like $\log_3 10$), the result is not a whole number.

**Answer:** 1.
