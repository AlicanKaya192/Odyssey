**Idea:** The trick that produced the geometric series formula works even if you forget the formula: multiply the sum by $r$ (or by its reciprocal) and subtract the shifted copy.

**Step 1 — The repeating decimal.** Let $x = 0.4545\dots$ Then $100x = 45.4545\dots$ Subtract: $99x = 45$, $x = \frac{45}{99} = \frac{5}{11}$.

**Step 2 — The series.** $S = \frac{2}{5} + \left( \frac{2}{5} \right)^2 + \dots$ Multiply both sides by $\frac{2}{5}$: $\frac{2}{5} S = \left( \frac{2}{5} \right)^2 + \dots$ Subtract: $\frac{3}{5} S = \frac{2}{5}$, $S = \frac{2}{3}$.

**Step 3 — The ratio.** $S = 6 + 6r + 6r^2 + \dots$ and $S = 6 + r S$ (everything after the first term is $r$ times the series). $9 = 6 + 9r$, $r = \frac{1}{3}$.

**Why the same result?** The equality $S - rS = a_1$ is the formula $S = \frac{a_1}{1 - r}$ itself; we re-derived it in each question. $100x - x$ is the same subtraction for $r = \frac{1}{100}$.

**Answer:** $\frac{5}{11}$, $\frac{2}{3}$ and $\frac{1}{3}$.
