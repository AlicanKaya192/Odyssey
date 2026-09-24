**What is asked?** The semi-axis lengths of the ellipse that $A$ takes the unit circle to.

**Idea:** If $A = U\Sigma V^\mathsf{T}$ then $A^\mathsf{T}A = V(\Sigma^\mathsf{T}\Sigma)V^\mathsf{T}$. So the eigenvalues of $A^\mathsf{T}A$ are the **squares** of the singular values. We find the eigenvalues and take square roots.

**Step 1 — $A^\mathsf{T}A$.** The rows of $A^\mathsf{T}$ are the columns of $A$; each entry is the dot product of two columns:

$$
\begin{aligned}
A^\mathsf{T}A &= \begin{bmatrix} 3 & 4 \\ 0 & 5 \end{bmatrix} \begin{bmatrix} 3 & 0 \\ 4 & 5 \end{bmatrix} \\
&= \begin{bmatrix} 9 + 16 & 0 + 20 \\ 0 + 20 & 0 + 25 \end{bmatrix} = \begin{bmatrix} 25 & 20 \\ 20 & 25 \end{bmatrix}
\end{aligned}
$$

**Step 2 — The eigenvalues.** Trace $50$, determinant $625 - 400 = 225$:

$$
\begin{aligned}
\lambda^2 - 50\lambda + 225 &= 0 \\
(\lambda - 45)(\lambda - 5) &= 0
\end{aligned}
$$

($45 \cdot 5 = 225$, $45 + 5 = 50$.)

**Step 3 — Square roots.**

$$
\begin{aligned}
\sigma_1 &= \sqrt{45} = 3\sqrt{5} \approx 6.71 \\
\sigma_2 &= \sqrt{5} \approx 2.24
\end{aligned}
$$

**Check:** $\sigma_1\sigma_2 = \sqrt{225} = 15 = |\det A| = |15 - 0|$ ✓. Also $\sigma_1^2 + \sigma_2^2 = 50 = 9 + 0 + 16 + 25$ (the sum of the squares of the entries) ✓.

**Watch out:** $A$ is triangular and its eigenvalues are $3$ and $5$; but those are **not** the singular values. Singular values coincide with eigenvalues only for symmetric matrices (with non-negative eigenvalues).

**Answer:** $\sigma_1 \approx 6.71$, $\sigma_2 \approx 2.24$.
