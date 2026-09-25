**What is asked?** The kind of two critical points and the minimum value.

**Idea:** Look at the eigenvalues of the Hessian (or its determinant and diagonal) at each critical point.

**Step 1 — The Hessian.** $H = \begin{bmatrix} 6x & 0 \\ 0 & 2 \end{bmatrix}$: diagonal, with eigenvalues $6x$ and $2$.

**Step 2 — $(1, 0)$.** Eigenvalues $6$ and $2$, both positive: a minimum. $f(1, 0) = 1 - 3 = -2$.

**Step 3 — $(-1, 0)$.** Eigenvalues $-6$ and $2$: different signs, a saddle. $\det H = -12$.

**Check:** Moving from $(-1, 0)$ in the $x$ direction, $f$ decreases ($f(-1.1, 0) = 1.969 < 2$); in the $y$ direction it increases ($f(-1, 0.1) = 2.01 > 2$): a saddle ✓.

**Watch out:** The value at $(-1, 0)$ is $f = 2$, which can look like a local maximum; but in the $y$ direction it is a bottom. Looking in only one direction misleads.

**Answer:** $x = 1$, value $-2$, $\det H = -12$.
