**What is asked?** The fractions equal to two decimals with infinitely many digits.

**Idea:** Multiplying the number by a suitable power of $10$ moves the point one full cycle along the repeating part, but the tail stays **the same**. Subtracting one from the other, the infinite tails cancel.

**Step 1 — $x = 0.\overline{4}$.** One digit repeats, so multiply by $10$:

$$
\begin{aligned}
10x &= 4.444\dots \\
x &= 0.444\dots
\end{aligned}
$$

**Step 2 — Subtract.** $10x - x = 4$, so $9x = 4$:

$$
x = \frac{4}{9}
$$

**Step 3 — $y = 0.\overline{12}$.** Two digits repeat, so multiply by $100$:

$$
\begin{aligned}
100y &= 12.1212\dots \\
y &= 0.1212\dots
\end{aligned}
$$

**Step 4 — Subtract and simplify.** $99y = 12$:

$$
y = \frac{12}{99} = \frac{4}{33}
$$

(We divided $12$ and $99$ by their GCD, $3$.)

**Check:** $4 \div 9 = 0.444\dots$ ✓. $4 \div 33$: $40 = 33 \cdot 1 + 7$, $70 = 33 \cdot 2 + 4$; the remainder is $4$ again, so the cycle restarts: $0.1212\dots$ ✓.

**Answer:** $\dfrac{4}{9}$ and $\dfrac{4}{33}$.
