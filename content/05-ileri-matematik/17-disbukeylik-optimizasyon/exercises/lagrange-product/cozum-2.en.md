**Idea:** The constraint is simple; write $y = 10 - x$ and reduce to a one-variable problem.

**Step 1 — One variable.** $h(x) = x(10 - x) = 10x - x^2$.

**Step 2 — Differentiate.** $h'(x) = 10 - 2x = 0$: $x = 5$, $y = 5$, $h = 25$. $h'' = -2 < 0$: a maximum.

**Step 3 — $\lambda$.** From the Lagrange equation $y = \lambda$, $\lambda = 5$; or from how the largest value changes with $c$.

**Why the same result?** Substituting means walking along the constraint curve; $h'(x) = 0$ is the moment $f$ stops increasing on that walk. Lagrange catches the same moment through parallel gradients, and it also works when the constraint is too complicated to substitute.

**Answer:** $5$, $25$ and $5$.
