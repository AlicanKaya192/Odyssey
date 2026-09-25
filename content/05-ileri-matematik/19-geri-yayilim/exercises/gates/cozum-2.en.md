**Idea:** Near the point $z > y$ ($1 > -2$), and small wiggles do not change this; there $\max(y, z) = z$. Locally the function is $f = xy + z$.

**Step 1 — The local form.** $f = xy + z$.

**Step 2 — The partial derivatives.** $\frac{\partial f}{\partial x} = y = -2$, $\frac{\partial f}{\partial y} = x = 3$, $\frac{\partial f}{\partial z} = 1$.

**Why the same result?** The max node's rule "send only to the winner" comes from max behaving, at that point, like a function equal to the winning input. ReLU is the same logic: $\max(0, z)$ is $z$ when $z > 0$ and $0$ otherwise.

**Answer:** $-2$, $3$, $1$.
