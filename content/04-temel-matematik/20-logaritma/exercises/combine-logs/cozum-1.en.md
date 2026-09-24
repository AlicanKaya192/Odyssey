**What is asked?** The sum and difference of three logarithms equals a single number. We cannot work out the terms one by one (they are not whole numbers), so we combine them first and calculate afterwards.

**Idea:** Logarithms with the same base can be combined:

$$
\begin{aligned}
\log_b x + \log_b y &= \log_b (x \cdot y) \quad (\text{product rule}) \\
\log_b x - \log_b y &= \log_b \frac{x}{y} \quad (\text{quotient rule})
\end{aligned}
$$

Why? A logarithm is an exponent. When powers are multiplied, exponents add ($b^m \cdot b^n = b^{m+n}$); that is why adding logarithms corresponds to multiplying inside.

**Step 1 — Combine the terms being added.** Both have base 6, so the product rule applies:

$$
\begin{aligned}
\log_6 12 + \log_6 18 &= \log_6 (12 \cdot 18) \\
&= \log_6 216
\end{aligned}
$$

**Step 2 — Combine the term being subtracted.** With the quotient rule:

$$
\begin{aligned}
\log_6 216 - \log_6 6 &= \log_6 \frac{216}{6} \\
&= \log_6 36
\end{aligned}
$$

**Step 3 — Find the value.** $\log_6 36$ asks: which power of 6 is 36? $6^2 = 36$, so:

$$
\log_6 36 = 2
$$

**Watch out:** Combining $\log_6 12 + \log_6 18$ as $\log_6 (12 + 18)$ is wrong. Adding logarithms turns into **multiplying** inside.

**Answer:** 2.
