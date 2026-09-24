**Idea:** Apply the definition once at a general $x$; the resulting formula $f'(x)$ gives every point at once.

**Step 1 — The general expansion.**

$$
\begin{aligned}
f(x + h) - f(x) &= (x + h)^2 + 3(x + h) - x^2 - 3x \\
&= 2xh + h^2 + 3h
\end{aligned}
$$

**Step 2 — Divide and take the limit.** $\frac{2xh + h^2 + 3h}{h} = 2x + 3 + h \to 2x + 3$.

**Step 3 — Put in the points.** $f'(2) = 7$, $f'(-1) = 1$.

**Why the same result?** The first way did the same calculation separately for $x = 2$ and $x = -1$; this way left $x$ as a letter and did it once. The result is also the derivative $2x$ of $x^2$ plus the derivative $3$ of $3x$: the term-by-term rule itself.

**Answer:** $7$ and $1$.
