**What is asked?** The singular values of a rank-1 matrix: how many are non-zero and how large?

**Idea:** Rank = number of non-zero singular values. A rank-1 matrix is a single layer: $A = \mathbf{a}\mathbf{b}^\mathsf{T}$. Such a matrix has the single singular value $\sigma_1 = \|\mathbf{a}\|\,\|\mathbf{b}\|$.

**Step 1 — The rank.** Both columns are $(2, 1)$: the columns are dependent, rank $1$. So $\sigma_2 = 0$.

**Step 2 — Write it as a column times a row.** Each row is a multiple of $(1, 1)$ ($2$ times and $1$ times):

$$
A = \begin{bmatrix} 2 \\ 1 \end{bmatrix} \begin{bmatrix} 1 & 1 \end{bmatrix}
$$

**Step 3 — Turn the lengths into unit vectors.** $\mathbf{a} = (2, 1)$, $\|\mathbf{a}\| = \sqrt{5}$; $\mathbf{b} = (1, 1)$, $\|\mathbf{b}\| = \sqrt{2}$:

$$
A = \sqrt{5}\sqrt{2} \cdot \underbrace{\tfrac{1}{\sqrt{5}}\begin{bmatrix} 2 \\ 1 \end{bmatrix}}_{\mathbf{u}_1} \underbrace{\tfrac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \end{bmatrix}}_{\mathbf{v}_1^\mathsf{T}}
$$

**Step 4 — The singular value.**

$$
\sigma_1 = \sqrt{5} \cdot \sqrt{2} = \sqrt{10} \approx 3.16
$$

**Check:** The sum of the squares of the entries is $4 + 4 + 1 + 1 = 10 = \sigma_1^2 + \sigma_2^2$ ✓.

**Reading the result:** $A$ squashes the whole plane onto a line along $\mathbf{u}_1 = (2, 1)/\sqrt{5}$; the unit circle becomes a segment (half-length $\sqrt{10}$).

**Answer:** $\sigma_1 \approx 3.16$, $\sigma_2 = 0$.
