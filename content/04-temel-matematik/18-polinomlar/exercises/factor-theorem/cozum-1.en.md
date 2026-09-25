**What is asked?** A coefficient, the smallest root of the polynomial and the remainder of a division.

**Idea:** The factor theorem says $P(2) = 0$; that gives $k$. Then the polynomial is factored, and the remainder theorem gives the remainder.

**Step 1 — $k$.**

$$
\begin{aligned}
P(2) &= 8 + 4k - 8 - 12 = 4k - 12 \\
4k - 12 &= 0 \quad \Rightarrow \quad k = 3
\end{aligned}
$$

**Step 2 — The factors.** $P(x) = x^3 + 3x^2 - 4x - 12$. Group in twos:

$$
\begin{aligned}
x^3 + 3x^2 - 4x - 12 &= x^2(x + 3) - 4(x + 3) \\
&= (x + 3)(x^2 - 4) \\
&= (x + 3)(x - 2)(x + 2)
\end{aligned}
$$

The roots are $-3$, $-2$, $2$; the smallest is $-3$.

**Step 3 — The remainder.** For $(x + 1)$, $a = -1$: $P(-1) = -1 + 3 + 4 - 12 = -6$.

**Check:** $P(-3) = -27 + 27 + 12 - 12 = 0$ ✓, $P(-2) = -8 + 12 + 8 - 12 = 0$ ✓.

**Watch out:** The remainder on division by $(x + 1)$ is $P(-1)$, not $P(1)$; $P(1) = -12$ would be the wrong answer.

**Answer:** $k = 3$, smallest root $-3$, remainder $-6$.
