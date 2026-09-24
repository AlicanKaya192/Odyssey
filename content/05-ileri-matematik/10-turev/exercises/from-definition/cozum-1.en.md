**What is asked?** The derivative of a function at two points, from the definition.

**Idea:** The definition: expand $\frac{f(a + h) - f(a)}{h}$, cancel $h$, then let $h \to 0$.

**Step 1 — $f'(2)$.** $f(2) = 4 + 6 = 10$.

$$
\begin{aligned}
f(2 + h) &= 4 + 4h + h^2 + 6 + 3h = 10 + 7h + h^2 \\
\frac{f(2 + h) - f(2)}{h} &= \frac{7h + h^2}{h} = 7 + h \;\to\; 7
\end{aligned}
$$

**Step 2 — $f'(-1)$.** $f(-1) = 1 - 3 = -2$.

$$
\begin{aligned}
f(-1 + h) &= 1 - 2h + h^2 - 3 + 3h = -2 + h + h^2 \\
\frac{f(-1 + h) - f(-1)}{h} &= \frac{h + h^2}{h} = 1 + h \;\to\; 1
\end{aligned}
$$

**Check:** Central difference, $h = 0.1$: $\frac{f(2.1) - f(1.9)}{0.2} = \frac{10.71 - 9.31}{0.2} = 7$ ✓.

**Watch out:** Forgetting the $3h$ in $3(2 + h)$ gives $f'(2) = 4$; write every term of the expansion.

**Answer:** $f'(2) = 7$, $f'(-1) = 1$.
