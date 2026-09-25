**Idea:** Show convexity without computing eigenvalues: write the expression as a sum of convex pieces.

**Step 1 — Rearrange.** $2x^2 + 2xy + y^2 = x^2 + (x^2 + 2xy + y^2) = x^2 + (x + y)^2$.

**Step 2 — The rules.** $x^2$ is convex. $(x + y)^2$ is the convex $u^2$ with the linear $u = x + y$ put in: convex. The sum is convex.

**Step 3 — The numbers.** The determinant and eigenvalues still need the Hessian: $\det H = 4$, eigenvalues $3 \pm \sqrt{5}$, the smaller $0.764$.

**Why the same result?** The sum of squares is zero only when $x = 0$ and $x + y = 0$, that is, only at the origin. This is the algebraic counterpart of the Hessian's eigenvalues being strictly positive: $\mathbf{h}^\mathsf{T} H \mathbf{h} = 2\big(h_1^2 + (h_1 + h_2)^2\big) > 0$.

**Answer:** $4$ and $0.764$.
