**What is asked?** The convexity of a function of two variables, through its Hessian.

**Idea:** If all the eigenvalues of the Hessian are greater than or equal to zero, the function is convex. For a quadratic function the Hessian is constant, so one calculation is enough.

**Step 1 — The Hessian.** $f_{xx} = 4$, $f_{xy} = 2$, $f_{yy} = 2$: $H = \begin{bmatrix} 4 & 2 \\ 2 & 2 \end{bmatrix}$.

**Step 2 — The determinant.** $4 \cdot 2 - 2 \cdot 2 = 4$.

**Step 3 — The eigenvalues.** $\lambda^2 - 6\lambda + 4 = 0$: $\lambda = 3 \pm \sqrt{5}$. The smaller one is $3 - \sqrt{5} \approx 0.764 > 0$.

**Check:** The product of the two eigenvalues is $(3 - \sqrt{5})(3 + \sqrt{5}) = 4 = \det H$ ✓, their sum $6$ = the trace ✓. Both positive: $f$ is strictly convex.

**Watch out:** The second derivative of the $2xy$ term is $f_{xy} = 2$; it contributes nothing to $f_{xx}$.

**Answer:** $\det H = 4$, smaller eigenvalue $\approx 0.764$; convex.
