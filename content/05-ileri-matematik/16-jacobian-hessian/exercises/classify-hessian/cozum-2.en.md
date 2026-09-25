**Idea:** $f = g(x) + y^2$ with $g(x) = x^3 - 3x$: the two variables are independent. Study each as a function of one variable.

**Step 1 — $g$.** $g' = 3x^2 - 3$, $g'' = 6x$. At $x = 1$: $g'' > 0$, a local minimum, $g(1) = -2$. At $x = -1$: $g'' < 0$, a local maximum.

**Step 2 — $y^2$.** A minimum at $y = 0$, with value $0$.

**Step 3 — Combine.** $(1, 0)$: a bottom in both directions, minimum $-2$. $(-1, 0)$: a top along $x$ and a bottom along $y$: a saddle. $\det H = g''(-1) \cdot 2 = -12$.

**Why the same result?** When the variables separate, the Hessian is diagonal and its eigenvalues are exactly the one-variable second derivatives. The general Hessian test does this separation along the eigenvector directions when the variables are mixed (off-diagonal $f_{xy} \neq 0$).

**Answer:** $1$, $-2$ and $-12$.
