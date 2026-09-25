**What is asked?** The gradient of a two-variable function and the effect of one descent step.

**Idea:** $\nabla f = \left(\frac{\partial f}{\partial x}, \frac{\partial f}{\partial y}\right)$; the new point is $p - \eta\nabla f$.

**Step 1 — $\partial f / \partial x$.** $2xy = 2 \cdot 1 \cdot 2 = 4$.

**Step 2 — $\partial f / \partial y$.** $x^2 + 3 = 4$.

**Step 3 — Step.** The new point is $(1 - 0.4, \ 2 - 0.4) = (0.6, \ 1.6)$. $f = 0.36 \cdot 1.6 + 3 \cdot 1.6 = 0.576 + 4.8 = 5.376$.

**Check:** Initially $f(1, 2) = 2 + 6 = 8$; the step lowered the value ✓. The first-order estimate is $8 - 0.1 \cdot \lVert\nabla f\rVert^2 = 8 - 3.2 = 4.8$; the real drop is a little smaller because the function curves.

**Watch out:** Moving along the gradient (with a plus sign) increases $f$; descent uses a minus.

**Answer:** $4$, $4$, $\approx 5.376$.
