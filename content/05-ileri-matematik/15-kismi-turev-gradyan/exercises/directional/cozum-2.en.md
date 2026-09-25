**Idea:** Go back to the definition of the directional derivative: walk a distance $t$ from $(2, 1)$ in the direction $\mathbf{u}$, write the height as a function of $t$, and differentiate at $t = 0$.

**Step 1 — The path.** $x = 2 + 0.6t$, $y = 1 + 0.8t$.

**Step 2 — The height.** $g(t) = (2 + 0.6t)^2 + 3(1 + 0.8t)^2$.

**Step 3 — The derivative.** $g'(t) = 2(2 + 0.6t)(0.6) + 6(1 + 0.8t)(0.8)$; $g'(0) = 2.4 + 4.8 = 7.2$.

**Why the same result?** The two terms of $g'(0)$ are $f_x \cdot u_1 = 4 \cdot 0.6$ and $f_y \cdot u_2 = 6 \cdot 0.8$: the chain rule produces the dot product by itself. This is exactly the proof of $D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u}$. The gradient components are also the directional derivatives along $\mathbf{u} = (1, 0)$ and $(0, 1)$: $4$ and $6$.

**Answer:** $4$, $6$, $7.2$.
