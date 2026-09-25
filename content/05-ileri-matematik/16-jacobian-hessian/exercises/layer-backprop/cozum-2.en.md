**Idea:** The layer is small; write the loss directly in terms of $x_1$, $x_2$ and $W_{12}$ and take partial derivatives. (As long as the $z$'s stay positive, ReLU does nothing.)

**Step 1 — The loss.** $z_1 = W_{11}x_1 + W_{12}x_2$, $z_2 = 3x_1 - x_2$:

$$
L = \tfrac{1}{2}(z_1 - 1)^2 + \tfrac{1}{2}(z_2 - 1)^2
$$

**Step 2 — With respect to the $x$'s.** $\frac{\partial L}{\partial x_1} = (z_1 - 1) \cdot 1 + (z_2 - 1) \cdot 3 = 2 + 3 = 5$. $\frac{\partial L}{\partial x_2} = (z_1 - 1) \cdot 2 + (z_2 - 1)(-1) = 4 - 1 = 3$.

**Step 3 — With respect to $W_{12}$.** It appears only in $z_1$, with coefficient $x_2$: $(z_1 - 1) \cdot x_2 = 2$.

**Why the same result?** Each partial derivative is the sum over all roads: $x_1$ is tied to $L$ through both $z_1$ (coefficient $1$) and $z_2$ (coefficient $3$). Multiplying by $W^\mathsf{T}$ does all these sums in one matrix operation: row $j$ of $W^\mathsf{T}$ holds the coefficients from $x_j$ to all the $z$'s.

**Answer:** $5$, $3$, $2$.
