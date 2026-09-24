**Idea:** Write $x = a + h$; $x \to a$ means $h \to 0$. Once the expression is expanded in $h$, the $h$ cancels.

**Step 1 — The first limit.** $x = 3 + h$:

$$
\frac{(3 + h)^2 - 9}{h} = \frac{6h + h^2}{h} = 6 + h \;\to\; 6
$$

**Step 2 — The second limit.** $x = 2 + h$:

$$
\begin{aligned}
x^2 - 5x + 6 &= 4 + 4h + h^2 - 10 - 5h + 6 \\
&= h^2 - h
\end{aligned}
$$

Divided by $h$: $h - 1 \to -1$.

**Why the same result?** Writing $x = a + h$ makes the factor $(x - a)$ visible as $h$; cancelling $h$ is the same job as cancelling the factor. This way of writing is used directly in the derivatives section: $\frac{f(a + h) - f(a)}{h}$.

**Answer:** $6$ and $-1$.
