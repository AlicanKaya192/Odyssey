**What is asked?** The largest value of a product under a constraint, and the Lagrange multiplier.

**Idea:** At the best point, $\nabla f = \lambda \nabla g$ and $g = c$.

**Step 1 — The gradients.** $\nabla f = (y, x)$, $\nabla g = (1, 1)$.

**Step 2 — The equations.** $y = \lambda$, $x = \lambda$, $x + y = 10$: $\lambda = 5$, $x = y = 5$.

**Step 3 — The value.** $xy = 25$.

**Check:** The meaning of $\lambda$: under $x + y = c$ the largest value is $\frac{c^2}{4}$; its derivative with respect to $c$ is $\frac{c}{2} = 5$ ✓.

**Watch out:** Solving $\nabla f = \mathbf{0}$ ($x = y = 0$) does not satisfy the constraint; in a constrained problem the gradient need not be zero, it must be parallel to the constraint's gradient.

**Answer:** $x = 5$, largest $25$, $\lambda = 5$.
