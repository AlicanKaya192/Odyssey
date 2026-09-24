**Idea:** Just as the $\mathbf{v}_i$ are the eigenvectors of $A^\mathsf{T}A$, the $\mathbf{u}_i$ are the eigenvectors of $AA^\mathsf{T}$: $AA^\mathsf{T} = U(\Sigma\Sigma^\mathsf{T})U^\mathsf{T}$. Its eigenvalues are again $\sigma_i^2$. We can find $\mathbf{u}_1$ directly without using $\mathbf{v}_1$.

**Step 1 — $AA^\mathsf{T}$.** This time the dot products of the **rows** of $A$:

$$
\begin{aligned}
AA^\mathsf{T} &= \begin{bmatrix} 3 & 0 \\ 4 & 5 \end{bmatrix} \begin{bmatrix} 3 & 4 \\ 0 & 5 \end{bmatrix} \\
&= \begin{bmatrix} 9 & 12 \\ 12 & 41 \end{bmatrix}
\end{aligned}
$$

Trace $50$, determinant $369 - 144 = 225$: the eigenvalues are again $45$ and $5$ ✓.

**Step 2 — The eigenvector for $\lambda = 45$.**

$$
AA^\mathsf{T} - 45I = \begin{bmatrix} -36 & 12 \\ 12 & -4 \end{bmatrix}
$$

The first row: $-36x + 12y = 0$, so $y = 3x$. The eigenvector is $(1, 3)$.

**Step 3 — Scale to unit length.** $\|(1, 3)\| = \sqrt{10}$:

$$
\mathbf{u}_1 = \frac{1}{\sqrt{10}}(1, 3) \approx (0.32,\ 0.95)
$$

**Watch out:** The sign of an eigenvector is free: $-(1, 3)$ is an eigenvector too. In the SVD the sign of $\mathbf{u}_i$ is tied to $\mathbf{v}_i$ through $A\mathbf{v}_i = \sigma_i\mathbf{u}_i$; since the question says "both positive", we chose the positive one.

**Answer:** $(0.32,\ 0.95)$.
