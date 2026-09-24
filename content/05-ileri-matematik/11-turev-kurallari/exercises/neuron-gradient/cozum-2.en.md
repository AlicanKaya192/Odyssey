**Idea:** As backpropagation does: first compute the derivative of $L$ with respect to $z$, $\delta$, once. Then each parameter multiplies $\delta$ by its own last link.

**Step 1 — $\delta$.** $\delta = \frac{\partial L}{\partial z} = 2(\hat{y} - y) \cdot \sigma'(z) = (-1)(0.25) = -0.25$.

**Step 2 — Share it.** $z = wx + b$: $\frac{\partial L}{\partial w} = \delta \cdot x = -0.5$; $\frac{\partial L}{\partial b} = \delta \cdot 1 = -0.25$.

**Step 3 — The step.** $w = 0 + 0.5 = 0.5$ (and $b = 0.25$).

**Why the same result?** In the first way, while the two derivatives were multiplied separately, the first two links ($-1$ and $0.25$) were written twice. $\delta$ computes that shared part once. For a single neuron the saving is small; in a network with millions of parameters, this sharing is exactly what makes backpropagation fast.

**Answer:** $-0.5$, $-0.25$ and $0.5$.
