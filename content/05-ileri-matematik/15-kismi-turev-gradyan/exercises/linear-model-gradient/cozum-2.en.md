**Idea:** Gather the parameters in one vector: $\boldsymbol{\theta} = (w_1, w_2, b)$, and the input as $(x_1, x_2, 1)$. The gradient is one line: $\nabla L = 2(\hat{y} - y)(x_1, x_2, 1)$.

**Step 1 — The gradient.** $2(-1.5)(1, 2, 1) = (-3, -6, -3)$.

**Step 2 — The step.** $\boldsymbol{\theta} \leftarrow (0.5, 0.5, 0) - 0.1 \cdot (-3, -6, -3) = (0.8, 1.1, 0.3)$.

**Step 3 — The loss.** $\hat{y} = (0.8, 1.1, 0.3) \cdot (1, 2, 1) = 3.3$, $L = 0.09$.

**Why the same result?** The same three partial derivatives, written as the components of a vector. The power of this form: with $10$ or $10$ million weights the formula is the same line. Libraries compute the gradient exactly like this, as a vector operation.

**Answer:** $-3$, $-6$, $0.09$.
