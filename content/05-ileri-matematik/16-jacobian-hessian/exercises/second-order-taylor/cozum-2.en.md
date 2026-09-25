**Idea:** $f$ depends only on $u = x + 2y$: $f = e^u$. At the point, $u = 0.1 + 0.1 = 0.2$. One-variable Taylor is enough.

**Step 1 — Linear.** $e^u \approx 1 + u = 1.2$.

**Step 2 — Second order.** $e^u \approx 1 + u + \frac{u^2}{2} = 1 + 0.2 + 0.02 = 1.22$.

**Why the same result?** $\nabla f \cdot \mathbf{h} = (1, 2) \cdot \mathbf{h} = u$ and $\mathbf{h}^\mathsf{T} H \mathbf{h} = \mathbf{h}^\mathsf{T} \begin{bmatrix} 1 \\ 2 \end{bmatrix} \begin{bmatrix} 1 & 2 \end{bmatrix} \mathbf{h} = u^2$. Here the Hessian is a rank-1 matrix: the function curves only in one direction (along $(1, 2)$) and is flat perpendicular to it.

**Answer:** $1.2$ and $1.22$.
