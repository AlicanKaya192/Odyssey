**What is asked?** The coefficients of the quotient and the remainder.

**Idea:** At each step divide the leading term of what is left by the leading term of the divisor, multiply back by the divisor and subtract. Stop when the degree of what is left is less than $1$.

**Step 1.** $x^3 \div x = x^2$. $x^2(x - 3) = x^3 - 3x^2$. Subtract:

$$
\begin{aligned}
&(x^3 - 4x^2 + 2x + 5) - (x^3 - 3x^2) \\
&= -x^2 + 2x + 5
\end{aligned}
$$

**Step 2.** $-x^2 \div x = -x$. $-x(x - 3) = -x^2 + 3x$. Subtract:

$$
\begin{aligned}
&(-x^2 + 2x + 5) - (-x^2 + 3x) \\
&= -x + 5
\end{aligned}
$$

**Step 3.** $-x \div x = -1$. $-1 \cdot (x - 3) = -x + 3$. Subtract: $(-x + 5) - (-x + 3) = 2$.

The quotient is $x^2 - x - 1$ and the remainder $2$.

**Check:** The remainder theorem: $P(3) = 27 - 36 + 6 + 5 = 2$ ✓.

**Watch out:** When subtracting, every sign of the second row flips: $2x - 3x = -x$, not $2x + 3x$.

**Answer:** $p = -1$, $q = -1$, remainder $2$.
