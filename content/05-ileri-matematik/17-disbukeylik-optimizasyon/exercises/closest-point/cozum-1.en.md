**What is asked?** The point of a line closest to the origin, and the squared distance.

**Idea:** The squared distance is $x^2 + y^2$; the constraint is $3x + 4y = 25$. Set up the Lagrange condition.

**Step 1 — The condition.** $(2x, 2y) = \lambda(3, 4)$: $x = \frac{3\lambda}{2}$, $y = 2\lambda$.

**Step 2 — The constraint.** $3 \cdot \frac{3\lambda}{2} + 4 \cdot 2\lambda = \frac{25\lambda}{2} = 25$: $\lambda = 2$. The point is $(3, 4)$.

**Step 3 — The value.** $9 + 16 = 25$; the distance is $5$.

**Check:** $(3, 4)$ is on the line: $9 + 16 = 25$ ✓. Another point on the line, $(7, 1)$: $49 + 1 = 50 > 25$ ✓.

**Watch out:** Since $f$ is convex and the constraint linear, the single candidate found is the global minimum; looking for a maximum makes no sense (the line goes off to infinity).

**Answer:** $(3, 4)$, smallest value $25$.
