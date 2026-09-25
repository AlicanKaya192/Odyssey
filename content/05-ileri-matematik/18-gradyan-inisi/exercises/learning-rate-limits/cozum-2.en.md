**Idea:** Start at $w_0 = 1$ and take a few steps; the behaviour shows the factor directly.

**Step 1 — $\eta = 0.3$.** $L'(1) = 6$: $w_1 = 1 - 1.8 = -0.8$. $L'(-0.8) = -4.8$: $w_2 = -0.8 + 1.44 = 0.64$. The ratio $\frac{w_1}{w_0} = -0.8$.

**Step 2 — $\eta = \frac{1}{6}$.** $w_1 = 1 - \frac{6}{6} = 0$: the bottom in one step.

**Step 3 — Find the limit.** The size of the ratio must not exceed $1$: $6\eta - 1 < 1$, $\eta < \frac{1}{3}$.

**Why the same result?** A few steps are the numerical picture of the rule $w_{k+1} = (1 - 6\eta)w_k$. The second derivative telling the best step ($\eta = \frac{1}{L''}$) is Newton's method in one variable: the exact step on a parabola.

**Answer:** $\frac{1}{3}$, $-0.8$, $\frac{1}{6}$.
