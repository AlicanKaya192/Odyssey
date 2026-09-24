**Idea:** Leaving $h$ as a letter shows where the error comes from.

**Step 1 — The expansions.** $(2 + h)^3 = 8 + 12h + 6h^2 + h^3$ and $(2 - h)^3 = 8 - 12h + 6h^2 - h^3$.

**Step 2 — The forward difference.** $\dfrac{12h + 6h^2 + h^3}{h} = 12 + 6h + h^2$. $h = 0.1$: $12 + 0.6 + 0.01 = 12.61$.

**Step 3 — The central difference.** In the difference the even powers cancel: $\dfrac{24h + 2h^3}{2h} = 12 + h^2$. $h = 0.1$: $12.01$.

**Why the same result?** We did the same calculation with a letter instead of numbers. The gain: the forward difference's error is $6h + h^2$, proportional to $h$; the central difference's error is $h^2$. Making $h$ ten times smaller shrinks the forward error tenfold and the central error a hundredfold. That is why gradient checking uses the central difference.

**Answer:** $12.61$ and $12.01$.
