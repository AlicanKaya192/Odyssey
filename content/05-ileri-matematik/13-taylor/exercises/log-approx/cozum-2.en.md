**Idea:** Build the expansion from the Taylor formula instead of from memory: compute the derivatives of $f(x) = \ln(1 + x)$ at $0$.

**Step 1 — The derivatives.** $f' = (1 + x)^{-1}$, $f'' = -(1 + x)^{-2}$, $f''' = 2(1 + x)^{-3}$. At $0$: $f(0) = 0$, $f'(0) = 1$, $f''(0) = -1$, $f'''(0) = 2$.

**Step 2 — The coefficients.** $\frac{1}{1!} = 1$, $\frac{-1}{2!} = -\frac{1}{2}$, $\frac{2}{3!} = \frac{1}{3}$: $x - \frac{x^2}{2} + \frac{x^3}{3}$.

**Step 3 — The values.** Two terms give $0.18$; the third term is $\frac{0.008}{3}$.

**Why the same result?** The expansion in the table comes from these derivatives; since the $k$-th derivative is $(-1)^{k-1}(k - 1)!$, dividing by $k!$ leaves $\frac{(-1)^{k-1}}{k}$: denominators $1, 2, 3, \ldots$ and alternating signs.

**Answer:** $0.18$ and $\approx 0.0027$.
