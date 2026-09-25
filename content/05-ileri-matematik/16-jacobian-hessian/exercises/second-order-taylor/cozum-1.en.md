**What is asked?** The first- and second-order Taylor approximations of a function of two variables.

**Idea:** $f(\mathbf{p} + \mathbf{h}) \approx f + \nabla f \cdot \mathbf{h} + \frac{1}{2}\mathbf{h}^\mathsf{T} H \mathbf{h}$.

**Step 1 — The derivatives.** $f_x = e^{x + 2y}$, $f_y = 2e^{x + 2y}$; $f_{xx}$, $f_{xy}$, $f_{yy}$ are $1$, $2$ and $4$ times $e^{x + 2y}$. At $(0, 0)$: $\nabla f = (1, 2)$, $H = \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}$.

**Step 2 — Linear.** $1 + (1, 2) \cdot (0.1, 0.05) = 1 + 0.1 + 0.1 = 1.2$.

**Step 3 — The Hessian term.** $H\mathbf{h} = (0.1 + 0.1, \ 0.2 + 0.2) = (0.2, 0.4)$; $\mathbf{h}^\mathsf{T} H \mathbf{h} = 0.02 + 0.02 = 0.04$; half of it is $0.02$. Total $1.22$.

**Check:** The true value is $e^{0.2} \approx 1.2214$. The error is $0.021$ for the linear approximation and $0.0014$ for the second order ✓.

**Watch out:** Forgetting the $\frac{1}{2}$ makes the second term $0.04$ and the result $1.24$, overshooting the truth.

**Answer:** $1.2$ and $1.22$.
