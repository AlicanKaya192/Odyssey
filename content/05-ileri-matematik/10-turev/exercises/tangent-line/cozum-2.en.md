**Idea:** Without using the table of derivatives, find the slope directly from the definition. $(1 + h)^3 = 1 + 3h + 3h^2 + h^3$.

**Step 1 — The difference.**

$$
\begin{aligned}
f(1 + h) &= 1 + 3h + 3h^2 + h^3 - 2 - 2h \\
&= -1 + h + 3h^2 + h^3
\end{aligned}
$$

**Step 2 — The slope.** $\frac{f(1 + h) - (-1)}{h} = 1 + 3h + h^2 \to 1$.

**Step 3 — The tangent.** The line with slope $1$ through $(1, -1)$: $y = x - 2$.

**Why the same result?** The table's $(x^3)' = 3x^2$ comes from exactly this expansion: $(x + h)^3 - x^3 = 3x^2 h + 3xh^2 + h^3$, divided by $h$, with $h \to 0$. The table is the definition done once.

**Answer:** $1$ and $-2$.
