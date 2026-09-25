**Idea:** Use the geometry of the partial derivative directly: put in the variable to be held fixed right away, leaving a function of one variable, and differentiate that.

**Step 1 — The slice $y = 2$.** $g(x) = f(x, 2) = 4x^3 - 8x + 8$. $g'(x) = 12x^2 - 8$, $g'(1) = 4$.

**Step 2 — The slice $x = 1$.** $h(y) = f(1, y) = y^2 - 4y + y^3$. $h'(y) = 2y - 4 + 3y^2$, $h'(2) = 4 - 4 + 12 = 12$.

**Why the same result?** $\frac{\partial f}{\partial x}(1, 2)$ is the slope at $x = 1$ of the cut of the surface by the plane $y = 2$; $g$ is exactly that cut. When the partial derivative is wanted at a single point, this way works with fewer letters.

**Answer:** $4$ and $12$.
