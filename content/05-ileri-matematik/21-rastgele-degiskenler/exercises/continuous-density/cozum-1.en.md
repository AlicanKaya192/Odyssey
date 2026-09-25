**What is asked?** A density's normalising constant, its expected value and the probability of an interval.

**Idea:** The total area must be $1$; the expected value is $\int x f(x) dx$; probability is area.

**Step 1 — $c$.**

$$
\int_0^2 (2x - x^2) \, dx = \Big[x^2 - \tfrac{x^3}{3}\Big]_0^2 = 4 - \tfrac{8}{3} = \tfrac{4}{3}
$$

$c \cdot \frac{4}{3} = 1$, $c = \frac{3}{4}$.

**Step 2 — $E[X]$.**

$$
\begin{aligned}
E[X] &= \tfrac{3}{4} \int_0^2 (2x^2 - x^3) \, dx = \tfrac{3}{4} \Big[\tfrac{2x^3}{3} - \tfrac{x^4}{4}\Big]_0^2 \\
&= \tfrac{3}{4} \left( \tfrac{16}{3} - 4 \right) = \tfrac{3}{4} \cdot \tfrac{4}{3} = 1
\end{aligned}
$$

**Step 3 — The probability.**

$$
\begin{aligned}
P(X \leq 0.5) &= \tfrac{3}{4} \Big[x^2 - \tfrac{x^3}{3}\Big]_0^{0.5} \\
&= \tfrac{3}{4} \left( \tfrac{1}{4} - \tfrac{1}{24} \right) = \tfrac{3}{4} \cdot \tfrac{5}{24} = \tfrac{5}{32}
\end{aligned}
$$

**Check:** $\frac{5}{32} \approx 0.156$; the interval is a quarter of $[0, 2]$ but the density is small near the edge, so the probability must be below $0.25$ ✓.

**Watch out:** Computing a probability before finding $c$; without area $1$ the result is not a probability.

**Answer:** $c = \frac{3}{4}$, $E[X] = 1$, $P = \frac{5}{32}$.
